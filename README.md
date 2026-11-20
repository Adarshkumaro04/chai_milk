# Ideal Tea and Coffee Milk Planner

This tool helps Ramesh, owner of Ideal Tea & Coffee opposite IIIT Allahabad's main gate, decide how much milk to stock. It uses only sales observations collected at the stall in `data.csv`.

## Run

Requires Python 3.10 or later. No packages need to be installed.

```powershell
python run.py --data data.csv --mode daily --buffer 15 --peak-reserve 500
```

Run the tests:

```powershell
python -m unittest -v
```

## Data format

Enter one real observation per row. `timestamp` must be ISO format such as `2026-11-20T18:15`.

```csv
timestamp,product,quantity,milk_ml_per_unit
2026-11-20T18:10,masala_tea,5,100
```

The program refuses to run until there are at least 20 real entries. Ask the owner for the milk amount used per unit; do not guess it.

## What the output means

The default daily mode totals observed milk use, adds the chosen safety buffer, and rounds up to the next half litre so the owner can buy a practical amount. The supplied observations produce an 8.0 L opening-stock recommendation: 6.67 L observed x 1.15 = 7.671 L, rounded up to 8.0 L.

## Result from the recorded day

```text
NEXT-DAY MILK STOCK PLAN
Observed entries: 24
Milk used today: 6.67 L
Safety buffer: 15.0%
Expected requirement: 7.670 L
RECOMMENDED OPENING STOCK: 8.0 L

Highest milk-use period: Afternoon (12:00 to 16:59)
Busiest clock hour: 18:00 to 19:00 (1.10 L)
Before 18:00, keep at least 0.5 L unopened in reserve.
```

Ramesh described his usual queue as 16:00-17:00, while this one-day log's largest hourly milk total is 18:00-19:00. The project treats that mismatch as evidence to collect a second real day, not as proof that either observation is wrong.

## Demo recording

Add the actual 3-minute recording link here before submission: **[replace with your link]**.

For a short-term estimate during the day:

```powershell
python run.py --data data.csv --mode short-term --hours 2 --buffer 15
```

## Add a second real observation day

Append rows for a second real date to `data.csv`, keeping the same columns and an ISO timestamp. Do not create or estimate a second day. Then compare the real days:

```powershell
python run.py --data data.csv --mode multi-day --buffer 15 --peak-reserve 500
```

Multi-day mode uses the average observed milk across the real days, reports the difference between the lowest and highest day, and rounds the buffered average to the next half litre.

## What it gets wrong

- It assumes the next few hours resemble the observed period.
- It cannot predict rain, a festival, a nearby event, delivery delays, or an unusual rush.
- It depends on accurate manual recording and the owner's stated milk-per-cup amount.
- The current recommendation is based on one observation day. A second real day will improve the estimate but still will not replace longer-term data.

