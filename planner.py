"""A small, dependency-free milk planning tool for a tea stall.

The program intentionally reads observations from data.csv rather than using
generated or downloaded data.  It estimates the milk required for the next
few hours from the observed sales rate and reports a conservative order size.
"""

from __future__ import annotations

import csv
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

REQUIRED_COLUMNS = {"timestamp", "product", "quantity", "milk_ml_per_unit"}


@dataclass(frozen=True)
class Sale:
    timestamp: datetime
    product: str
    quantity: int
    milk_ml_per_unit: float

    @property
    def milk_ml(self) -> float:
        return self.quantity * self.milk_ml_per_unit


def load_sales(csv_path: str | Path) -> list[Sale]:
    """Read and validate hand-collected sales observations from a CSV file."""
    path = Path(csv_path)
    with path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - columns
        if missing:
            raise ValueError("Missing required column(s): " + ", ".join(sorted(missing)))

        sales: list[Sale] = []
        for row_number, row in enumerate(reader, start=2):
            try:
                timestamp = datetime.fromisoformat(row["timestamp"].strip())
                product = row["product"].strip()
                quantity = int(row["quantity"])
                milk_ml_per_unit = float(row["milk_ml_per_unit"])
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Row {row_number} has an invalid timestamp, quantity, or milk amount."
                ) from error
            if not product:
                raise ValueError(f"Row {row_number} has an empty product name.")
            if quantity <= 0 or milk_ml_per_unit < 0:
                raise ValueError(
                    f"Row {row_number} needs a positive quantity and a non-negative milk amount."
                )
            sales.append(Sale(timestamp, product, quantity, milk_ml_per_unit))

    if len(sales) < 20:
        raise ValueError(
            f"Only {len(sales)} entries found. Collect at least 20 real entries before using this tool."
        )
    seen = set()
    per_product: dict[str, float] = {}
    for sale in sales:
        key = (sale.timestamp, sale.product)
        if key in seen:
            raise ValueError(
                f"Duplicate entry for {sale.product} at "
                f"{sale.timestamp.isoformat(timespec='minutes')}."
            )
        seen.add(key)
        first_amount = per_product.setdefault(sale.product, sale.milk_ml_per_unit)
        if first_amount != sale.milk_ml_per_unit:
            raise ValueError(
                f"{sale.product} has two different milk amounts "
                f"({first_amount:g} and {sale.milk_ml_per_unit:g} ml). "
                "Use one agreed amount per product."
            )
        if sale.quantity > 50:
            raise ValueError(
                f"Row for {sale.product} at {sale.timestamp.isoformat(timespec='minutes')} "
                "has a quantity above 50. Please check for a typing mistake."
            )
    return sorted(sales, key=lambda sale: sale.timestamp)


def apply_coverage(sales: Iterable[Sale], coverage_percent: float) -> list[Sale]:
    """Scale logged milk up when the log is known to miss part of the real milk use.

    Example: the owner really used 7.9 L but the log counted 6.67 L, so
    coverage_percent is about 84 and every row's milk is scaled by 100 / 84.
    """
    if not 0 < coverage_percent <= 100:
        raise ValueError("Coverage must be above 0 and at most 100 (percent of real milk the log captured).")
    factor = 100 / coverage_percent
    return [
        Sale(sale.timestamp, sale.product, sale.quantity, sale.milk_ml_per_unit * factor)
        for sale in sales
    ]


def make_plan(
    sales: Iterable[Sale], now: str, hours_to_cover: float, safety_buffer: float
) -> dict[str, float | int | str]:
    """Estimate milk for the next few hours from sales logged in the SAME clock window.

    Example: now="16:30", hours_to_cover=2 uses only the milk logged between
    16:30 and 18:30 (averaged over the observed days), not the all-day average.
    """
    observations = list(sales)
    if hours_to_cover <= 0:
        raise ValueError("Hours to cover must be greater than zero.")
    if safety_buffer < 0:
        raise ValueError("Safety buffer cannot be negative.")
    try:
        start = datetime.strptime(now.strip(), "%H:%M")
    except ValueError as error:
        raise ValueError("Time must look like 16:30 (24-hour HH:MM).") from error

    start_min = start.hour * 60 + start.minute
    end_min = start_min + hours_to_cover * 60
    days = len({sale.timestamp.date() for sale in observations})

    in_window = [
        sale
        for sale in observations
        if start_min <= sale.timestamp.hour * 60 + sale.timestamp.minute < end_min
    ]
    end_label = f"{int(end_min // 60) % 24:02d}:{int(end_min % 60):02d}"
    if not in_window:
        raise ValueError(
            f"No observed sales between {now.strip()} and {end_label}. "
            "The stall may be closed then, or the log has a gap."
        )

    window_ml = sum(sale.milk_ml for sale in in_window) / days
    recommended_ml = window_ml * (1 + safety_buffer / 100)
    products = Counter(sale.product for sale in in_window)

    return {
        "entries": len(in_window),
        "days": days,
        "window_start": now.strip(),
        "window_end": end_label,
        "window_ml": window_ml,
        "recommended_ml": recommended_ml,
        "top_product": products.most_common(1)[0][0],
    }


def daily_stock_plan(
    sales: Iterable[Sale], safety_buffer: float, peak_reserve_ml: float
) -> dict[str, float | int | str | dict[str, float | int]]:
    """Turn one observed business day into a transparent next-day stock plan."""
    observations = list(sales)
    if safety_buffer < 0 or peak_reserve_ml < 0:
        raise ValueError("Safety buffer and peak reserve cannot be negative.")
    dates = {sale.timestamp.date() for sale in observations}
    if len(dates) != 1:
        raise ValueError(
            "Daily mode needs observations from exactly one calendar day. "
            "Use multi-day mode to compare more than one day."
        )

    milk_sales = [sale for sale in observations if sale.milk_ml > 0]
    if not milk_sales:
        raise ValueError("No milk-based sales were found.")

    slots = {
        "Morning (before 12:00)": {"entries": 0, "milk_ml": 0.0},
        "Afternoon (12:00 to 16:59)": {"entries": 0, "milk_ml": 0.0},
        "Evening (17:00 onward)": {"entries": 0, "milk_ml": 0.0},
    }
    for sale in observations:
        hour = sale.timestamp.hour
        slot = (
            "Morning (before 12:00)"
            if hour < 12
            else "Afternoon (12:00 to 16:59)"
            if hour < 17
            else "Evening (17:00 onward)"
        )
        slots[slot]["entries"] += 1
        slots[slot]["milk_ml"] += sale.milk_ml

    observed_ml = sum(sale.milk_ml for sale in observations)
    expected_ml = observed_ml * (1 + safety_buffer / 100)
    rounded_stock_ml = math.ceil(expected_ml / 500) * 500
    bulk_sales = [sale for sale in milk_sales if sale.quantity >= 3]
    bulk_milk_ml = sum(sale.milk_ml for sale in bulk_sales)
    highest_slot = max(slots, key=lambda name: slots[name]["milk_ml"])
    milk_by_hour: dict[int, float] = {}
    for sale in observations:
        milk_by_hour[sale.timestamp.hour] = milk_by_hour.get(sale.timestamp.hour, 0.0) + sale.milk_ml
    busiest_hour = max(milk_by_hour, key=milk_by_hour.get)

    return {
        "entries": len(observations),
        "milk_based_orders": len(milk_sales),
        "observed_ml": observed_ml,
        "expected_ml": expected_ml,
        "rounded_stock_ml": rounded_stock_ml,
        "safety_buffer": safety_buffer,
        "peak_reserve_ml": peak_reserve_ml,
        "slots": slots,
        "highest_slot": highest_slot,
        "busiest_hour": busiest_hour,
        "busiest_hour_ml": milk_by_hour[busiest_hour],
        "bulk_orders": len(bulk_sales),
        "bulk_milk_ml": bulk_milk_ml,
    }


def multi_day_stock_plan(
    sales: Iterable[Sale], safety_buffer: float, peak_reserve_ml: float
) -> dict[str, float | int | str | list[dict[str, float | int | str | dict[str, float | int]]]]:
    """Compare real observation days and plan stock from their average demand."""
    observations = list(sales)
    by_date: dict[object, list[Sale]] = defaultdict(list)
    for sale in observations:
        by_date[sale.timestamp.date()].append(sale)
    if len(by_date) < 2:
        raise ValueError("Multi-day mode needs observations from at least two calendar days.")

    daily_plans = [
        daily_stock_plan(day_sales, safety_buffer, peak_reserve_ml)
        for _, day_sales in sorted(by_date.items())
    ]
    daily_totals = [float(plan["observed_ml"]) for plan in daily_plans]
    average_observed_ml = sum(daily_totals) / len(daily_totals)
    average_expected_ml = average_observed_ml * (1 + safety_buffer / 100)
    rounded_stock_ml = math.ceil(average_expected_ml / 500) * 500
    return {
        "days": len(daily_plans),
        "daily_plans": daily_plans,
        "average_observed_ml": average_observed_ml,
        "average_expected_ml": average_expected_ml,
        "rounded_stock_ml": rounded_stock_ml,
        "min_observed_ml": min(daily_totals),
        "max_observed_ml": max(daily_totals),
        "safety_buffer": safety_buffer,
        "peak_reserve_ml": peak_reserve_ml,
    }


def format_plan(plan: dict[str, float | int | str], hours_to_cover: float, safety_buffer: float) -> str:
    """Format the short-term answer for the stall owner, plus the calculation trail."""
    return "\n".join(
        [
            "SHORT-TERM MILK PLAN",
            f"Window: {plan['window_start']} to {plan['window_end']} ({hours_to_cover:g} hours)",
            f"Based on {plan['entries']} logged sale(s) in that same window, over {plan['days']} day(s)",
            f"Milk used in that window: {plan['window_ml'] / 1000:.2f} L",
            f"Most frequently sold item in that window: {plan['top_product']}",
            f"Safety buffer: {safety_buffer:g}%",
            f"RECOMMENDED MILK TO KEEP: {plan['recommended_ml'] / 1000:.2f} L",
            "",
            "Only a few sales may fall in one window, so treat this as a rough guide.",
            "It does not account for weather, holidays, supplier delays, or an unusual rush.",
        ]
    )


def format_daily_stock_plan(
    plan: dict[str, float | int | str | dict[str, float | int]], lang: str = "en"
) -> str:
    """Format the daily recommendation and its calculation trail for the owner."""
    slots = plan["slots"]
    assert isinstance(slots, dict)
    slot_lines = [
        f"  {name}: {values['entries']} entries, {values['milk_ml'] / 1000:.2f} L"
        for name, values in slots.items()
        if isinstance(values, dict)
    ]
    bulk_share = 100 * float(plan["bulk_milk_ml"]) / float(plan["observed_ml"])
    stock_l = float(plan["rounded_stock_ml"]) / 1000
    reserve_l = float(plan["peak_reserve_ml"]) / 1000
    hour = int(plan["busiest_hour"])
    if lang == "hi":
        quick_note = [
            "RAMESH JI KE LIYE (chhota note)",
            f"Kal subah {stock_l:.1f} litre doodh se shuru karein.",
            f"{hour:02d}:00 baje se pehle aakhri {reserve_l:.1f} litre mat kholiye, jab tak zaroorat na pade.",
        ]
    else:
        quick_note = [
            "RAMESH'S QUICK NOTE",
            f"Start tomorrow with {stock_l:.1f} L of milk.",
            f"Do not open the final {reserve_l:.1f} L before {hour:02d}:00 unless needed.",
        ]
    return "\n".join(
        [
            "NEXT-DAY MILK STOCK PLAN",
            f"Observed entries: {plan['entries']}",
            f"Milk used today: {float(plan['observed_ml']) / 1000:.2f} L",
            f"Safety buffer: {plan['safety_buffer']}%",
            f"Expected requirement: {float(plan['expected_ml']) / 1000:.3f} L",
            f"RECOMMENDED OPENING STOCK: {float(plan['rounded_stock_ml']) / 1000:.1f} L",
            "",
            "Milk by time slot:",
            *slot_lines,
            f"Highest milk-use period: {plan['highest_slot']}",
            "",
            f"Bulk orders (3+ units): {plan['bulk_orders']} of {plan['milk_based_orders']} milk-based orders",
            f"Milk used by bulk orders: {float(plan['bulk_milk_ml']) / 1000:.2f} L ({bulk_share:.0f}% of milk used)",
            f"Busiest clock hour: {int(plan['busiest_hour']):02d}:00 to {int(plan['busiest_hour']) + 1:02d}:00 "
            f"({float(plan['busiest_hour_ml']) / 1000:.2f} L).",
            f"Before {int(plan['busiest_hour']):02d}:00, keep at least {float(plan['peak_reserve_ml']) / 1000:.1f} L unopened in reserve.",
            "",
            *quick_note,
            "",
            "This recommendation is based on one regular working day. Review it after a rain day,",
            "festival, holiday, or any day with an unusual event near the campus.",
        ]
    )


def format_multi_day_stock_plan(
    plan: dict[str, float | int | str | list[dict[str, float | int | str | dict[str, float | int]]]]
) -> str:
    """Format a transparent comparison after two or more real observation days."""
    daily_plans = plan["daily_plans"]
    assert isinstance(daily_plans, list)
    day_lines = [
        f"  Day {index}: {float(day['observed_ml']) / 1000:.2f} L observed"
        for index, day in enumerate(daily_plans, start=1)
    ]
    spread_ml = float(plan["max_observed_ml"]) - float(plan["min_observed_ml"])
    return "\n".join(
        [
            "MULTI-DAY MILK STOCK PLAN",
            f"Real observation days compared: {plan['days']}",
            *day_lines,
            f"Average observed milk: {float(plan['average_observed_ml']) / 1000:.2f} L/day",
            f"Difference between lowest and highest day: {spread_ml / 1000:.2f} L",
            f"Safety buffer: {plan['safety_buffer']}%",
            f"RECOMMENDED OPENING STOCK: {float(plan['rounded_stock_ml']) / 1000:.1f} L",
            "",
            "RAMESH'S QUICK NOTE",
            f"Use {float(plan['rounded_stock_ml']) / 1000:.1f} L as the normal opening stock based on these real days.",
            f"Keep {float(plan['peak_reserve_ml']) / 1000:.1f} L unopened before your busiest hour (see daily mode).",
            "",
            "More real days make this estimate stronger. Keep noting rain, holidays, and college events",
            "because they can change demand more than the average can show.",
        ]
    )