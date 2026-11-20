# Ideal Tea and Coffee Milk Planner

This tool helps Ramesh, owner of Ideal Tea & Coffee opposite IIIT Allahabad's main gate (Jhalwa, Prayagraj), decide how much milk to buy for the next day. It uses only sales observations I collected at the stall on 20 November 2026, stored in `data.csv`.

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

The program refuses to run until there are at least 20 real entries. It also rejects bad rows with the row number (wrong quantity, bad timestamp), duplicate entries, the same product with two different milk amounts, and quantities above 50. The milk amount per unit comes from the owner; do not guess it.

## What the output means

The default daily mode totals observed milk use, adds the chosen safety buffer, and rounds up to the next half litre so the owner can buy a practical amount. For the recorded day: 6.67 L observed x 1.15 = 7.671 L, rounded up to 8.0 L.

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

RAMESH'S QUICK NOTE
Start tomorrow with 8.0 L of milk.
Do not open the final 0.5 L before 18:00 unless needed.
```

## Field check, 20 Nov 2026

The tool recommended 8.0 L. Ramesh bought 9.0 L that morning and used about 7.9 L (1.1 L was left at closing), so the recommendation was within 0.1 L of his real use, and he over-ordered by about 1 L.

My log counted 6.67 L, which is about 84% of his real use (6.67 / 7.9). The 15% buffer is what covers that gap: without it the tool would have said 7.67 L, below what he actually used.

Ramesh says his weekday rush is 4:00-5:15 PM, but this one-day log's busiest hour is 18:00-19:00. I treat that mismatch as a reason to collect a second real day, not as proof that either one is wrong. He also said he would keep the 0.5 L reserve and lower the buffer on weekends and rainy afternoons.

Full notes and his words are in `fieldwork.md`.

## Demo recording

3-minute screen recording: **[replace with your link]**

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

- It is based on one observation day. A second real day will improve it, but it still will not replace longer-term data.
- My log captured only about 84% of the milk Ramesh actually used, so some orders or milk use are missing from `data.csv`.
- Milk per cup is Ramesh's ladle estimate, not a measured amount.
- Short-term mode uses the average rate over the whole observed day, so it ignores the time of day and will under-estimate during a rush.
- It cannot predict rain, a festival, a nearby event, delivery delays, or an unusual rush. Ramesh says weekends and holidays have a different pattern from weekdays, and the tool does not model that.
- It depends on accurate manual recording.