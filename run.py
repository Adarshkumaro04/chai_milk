"""Command-line entry point for the chai-stall milk planner."""

from __future__ import annotations

import argparse

from planner import (
    daily_stock_plan,
    format_daily_stock_plan,
    format_multi_day_stock_plan,
    format_plan,
    load_sales,
    make_plan,
    multi_day_stock_plan,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estimate the milk to keep for a tea stall from real sales observations."
    )
    parser.add_argument("--data", default="data.csv", help="Path to the observed sales CSV")
    parser.add_argument(
        "--mode",
        choices=("daily", "short-term", "multi-day"),
        default="daily",
        help="daily plans one day; multi-day compares real days; short-term projects the next few hours",
    )
    parser.add_argument(
        "--hours", type=float, default=2.0, help="Hours of future demand to cover (default: 2)"
    )
    parser.add_argument(
        "--peak-reserve",
        type=float,
        default=500.0,
        help="Unopened milk to retain before the peak rush, in ml (default: 500)",
    )
    parser.add_argument(
        "--buffer",
        type=float,
        default=15.0,
        help="Safety buffer as a percent (default: 15)",
    )
    args = parser.parse_args()

    try:
        sales = load_sales(args.data)
        if args.mode == "daily":
            plan = daily_stock_plan(sales, args.buffer, args.peak_reserve)
            print(format_daily_stock_plan(plan))
        elif args.mode == "multi-day":
            plan = multi_day_stock_plan(sales, args.buffer, args.peak_reserve)
            print(format_multi_day_stock_plan(plan))
        else:
            plan = make_plan(sales, args.hours, args.buffer)
            print(format_plan(plan, args.hours, args.buffer))
    except ValueError as error:
        parser.exit(2, f"Input error: {error}\n")


if __name__ == "__main__":
    main()
