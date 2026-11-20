import csv
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from planner import (
    apply_coverage,
    daily_stock_plan,
    format_daily_stock_plan,
    load_sales,
    make_plan,
    multi_day_stock_plan,
)


class PlannerTests(unittest.TestCase):
    def sales(self):
        start = datetime(2026, 11, 20, 8, 0)
        return [
            type(
                "Sale",
                (),
                {
                    "timestamp": start + timedelta(minutes=6 * item),
                    "product": "Milk tea",
                    "quantity": 1,
                    "milk_ml": 80,
                },
            )()
            for item in range(20)
        ]

    def test_short_term_uses_only_the_matching_clock_window(self):
        # fixture: 20 sales of 80 ml, 08:00 to 09:54, one every 6 minutes
        plan = make_plan(self.sales(), now="08:00", hours_to_cover=1, safety_buffer=10)
        self.assertEqual(plan["entries"], 10)
        self.assertAlmostEqual(plan["window_ml"], 800)
        self.assertAlmostEqual(plan["recommended_ml"], 880)

    def test_short_term_rejects_a_window_with_no_sales(self):
        with self.assertRaisesRegex(ValueError, "No observed sales"):
            make_plan(self.sales(), now="15:00", hours_to_cover=2, safety_buffer=10)

    def test_short_term_rejects_a_bad_time(self):
        with self.assertRaisesRegex(ValueError, "HH:MM"):
            make_plan(self.sales(), now="4pm", hours_to_cover=2, safety_buffer=10)

    def test_load_sales_rejects_less_than_twenty_rows(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data.csv"
            with path.open("w", newline="", encoding="utf-8") as target:
                writer = csv.DictWriter(target, fieldnames=["timestamp", "product", "quantity", "milk_ml_per_unit"])
                writer.writeheader()
                writer.writerow({"timestamp": "2026-11-20T08:00", "product": "Milk tea", "quantity": 1, "milk_ml_per_unit": 80})
            with self.assertRaisesRegex(ValueError, "at least 20 real entries"):
                load_sales(path)

    def test_daily_plan_rounds_stock_to_the_next_half_litre(self):
        plan = daily_stock_plan(self.sales(), safety_buffer=15, peak_reserve_ml=500)
        self.assertEqual(plan["observed_ml"], 1600)
        self.assertEqual(plan["rounded_stock_ml"], 2000)
        self.assertEqual(plan["peak_reserve_ml"], 500)

    def test_multi_day_plan_uses_average_of_real_days(self):
        day_one = self.sales()
        day_two = [
            type(
                "Sale",
                (),
                {
                    "timestamp": sale.timestamp + timedelta(days=1),
                    "product": sale.product,
                    "quantity": sale.quantity,
                    "milk_ml": 120,
                },
            )()
            for sale in day_one
        ]
        plan = multi_day_stock_plan(day_one + day_two, safety_buffer=0, peak_reserve_ml=500)
        self.assertEqual(plan["days"], 2)
        self.assertEqual(plan["average_observed_ml"], 2000)
        self.assertEqual(plan["rounded_stock_ml"], 2000)

    def write_rows(self, folder, rows):
        path = Path(folder) / "data.csv"
        with path.open("w", newline="", encoding="utf-8") as target:
            writer = csv.writer(target)
            writer.writerow(["timestamp", "product", "quantity", "milk_ml_per_unit"])
            writer.writerows(rows)
        return path

    def test_duplicate_row_is_rejected(self):
        rows = [[f"2026-11-20T08:{item:02d}", "tea", 1, 80] for item in range(20)]
        rows[-1] = rows[0]
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "Duplicate entry"):
                load_sales(self.write_rows(folder, rows))

    def test_conflicting_milk_amount_is_rejected(self):
        rows = [[f"2026-11-20T08:{item:02d}", "tea", 1, 80] for item in range(20)]
        rows[-1][3] = 120
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "two different milk amounts"):
                load_sales(self.write_rows(folder, rows))

    def test_busiest_hour_comes_from_the_data(self):
        rows = [[f"2026-11-20T08:{item:02d}", "tea", 1, 80] for item in range(18)]
        rows.extend([["2026-11-20T18:10", "tea", 20, 80], ["2026-11-20T18:40", "tea", 20, 80]])
        with tempfile.TemporaryDirectory() as folder:
            plan = daily_stock_plan(load_sales(self.write_rows(folder, rows)), 15, 500)
        self.assertEqual(plan["busiest_hour"], 18)

    def test_coverage_scales_logged_milk_up(self):
        from planner import Sale
        sale = Sale(datetime(2026, 11, 20, 8, 0), "tea", 2, 100)
        scaled = apply_coverage([sale], 80)
        self.assertAlmostEqual(scaled[0].milk_ml, 250)

    def test_coverage_outside_range_is_rejected(self):
        from planner import Sale
        sale = Sale(datetime(2026, 11, 20, 8, 0), "tea", 1, 80)
        for bad in (0, -5, 120):
            with self.assertRaisesRegex(ValueError, "Coverage"):
                apply_coverage([sale], bad)

    def test_hindi_quick_note_contains_the_stock_number(self):
        plan = daily_stock_plan(self.sales(), safety_buffer=15, peak_reserve_ml=500)
        text = format_daily_stock_plan(plan, lang="hi")
        self.assertIn("litre doodh", text)
        self.assertIn("2.0", text)
        self.assertNotIn("RAMESH'S QUICK NOTE", text)


if __name__ == "__main__":
    unittest.main()