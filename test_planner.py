import csv
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from planner import daily_stock_plan, load_sales, make_plan, multi_day_stock_plan


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

    def test_plan_uses_observed_rate_and_buffer(self):
        plan = make_plan(self.sales(), hours_to_cover=2, safety_buffer=10)
        self.assertEqual(plan["entries"], 20)
        self.assertAlmostEqual(plan["total_milk_ml"], 1600)
        self.assertAlmostEqual(plan["forecast_ml"], 1600 / 1.9 * 2)
        self.assertAlmostEqual(plan["recommended_ml"], plan["forecast_ml"] * 1.1)

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


if __name__ == "__main__":
    unittest.main()
