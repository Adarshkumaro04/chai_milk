"""Command-line entry point for the chai-stall milk planner."""

from __future__ import annotations

import argparse

from planner import (
    apply_coverage,
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
        "--now", default=None, help="Current time as HH:MM, needed for short-term mode (e.g. 16:30)"
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
        "--coverage",
        type=float,
        default=100.0,
        help="Percent of real milk use that the log captured (default: 100, no correction)",
    )
    parser.add_argument(
        "--lang",
        choices=("en", "hi"),
        default="en",
        help="Language of the quick note: en = English, hi = Hindi in Roman letters (daily mode only)",
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
        if args.lang == "hi" and args.mode != "daily":
            raise ValueError("--lang hi works with daily mode only.")
        if args.coverage != 100:
            sales = apply_coverage(sales, args.coverage)
            print(
                f"Coverage correction: my log captures {args.coverage:g}% of real milk use, "
                f"so logged milk is scaled up by {100 / args.coverage:.2f}x.\n"
            )
        if args.mode == "daily":
            plan = daily_stock_plan(sales, args.buffer, args.peak_reserve)
            print(format_daily_stock_plan(plan, args.lang))
        elif args.mode == "multi-day":
            plan = multi_day_stock_plan(sales, args.buffer, args.peak_reserve)
            print(format_multi_day_stock_plan(plan))
        else:
            if not args.now:
                raise ValueError("Short-term mode needs --now HH:MM, for example --now 16:30.")
            plan = make_plan(sales, args.now, args.hours, args.buffer)
            print(format_plan(plan, args.hours, args.buffer))
    except ValueError as error:
        parser.exit(2, f"Input error: {error}\n")
    except FileNotFoundError:
        parser.exit(2, f"Input error: file not found: {args.data}\n")


if __name__ == "__main__":
    main()