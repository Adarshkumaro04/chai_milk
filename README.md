# Ideal Tea and Coffee Milk Planner

This tool helps Ramesh, owner of Ideal Tea & Coffee opposite IIIT Allahabad's main gate (Jhalwa, Prayagraj), decide how much milk to buy for the next day. It uses only sales observations I collected at the stall on 20 November 2026, stored in `data.csv`.

## Project files

- `research.md`: the problem and two existing solutions
- `fieldwork.md`: photos, my conversation with Ramesh, and how the data was collected
- `data.csv`: my 24 observations from 20 Nov 2026
- `planner.py`, `run.py`, `test_planner.py`: the tool and its tests
- `reflection.md`: what I got wrong and learned
- `ai-chats/`: exported AI conversations

## Run

Requires Python 3.10 or later. No packages need to be installed.

```
python run.py --data data.csv --mode daily --buffer 15 --peak-reserve 500
```

Run the tests:

```
python -m unittest -v
```

## Data format

Enter one real observation per row. `timestamp` must be ISO format such as `2026-11-20T18:15`.

```
timestamp,product,quantity,milk_ml_per_unit
2026-11-20T18:10,masala_tea,5,100
```

The program refuses to run until there are at least 20 real entries. It also gives a clear error for a bad row (with the row number), a duplicate entry, the same product with two different milk amounts, a quantity above 50, or a missing file. The milk amount per unit comes from the owner; do not guess it.

## What the output means

The default daily mode totals observed milk use, adds the chosen safety buffer, and rounds up to the next half litre so the owner can buy a practical amount. For the recorded day: 6.67 L observed x 1.15 = 7.67 L, rounded up to 8.0 L.

## Result from the recorded day

```
NEXT-DAY MILK STOCK PLAN
Observed entries: 24
Milk used today: 6.67 L
Safety buffer: 15.0%
Expected requirement: 7.670 L
RECOMMENDED OPENING STOCK: 8.0 L

Milk by time slot:
  Morning (before 12:00): 8 entries, 1.33 L
  Afternoon (12:00 to 16:59): 8 entries, 3.21 L
  Evening (17:00 onward): 8 entries, 2.13 L
Highest milk-use period: Afternoon (12:00 to 16:59)

Bulk orders (3+ units): 11 of 20 milk-based orders
Milk used by bulk orders: 4.96 L (74% of milk used)
Busiest clock hour: 18:00 to 19:00 (1.10 L).
Before 18:00, keep at least 0.5 L unopened in reserve.

RAMESH'S QUICK NOTE
Start tomorrow with 8.0 L of milk.
Do not open the final 0.5 L before 18:00 unless needed.

This recommendation is based on one regular working day. Review it after a rain day,
festival, holiday, or any day with an unusual event near the campus.
```

## Field check, 20 Nov 2026

The tool recommended 8.0 L. Ramesh bought 9.0 L that morning and used about 7.9 L (1.1 L was left at closing), so the recommendation was within 0.1 L of his real use, and he over-ordered by about 1 L. This compares the tool to the same day it was built from, so it is a sanity check, not a test of forecasting. A second real day would be the real test.

My log counted 6.67 L, which is about 84% of his real use (6.67 / 7.9). The 15% buffer is what covers that gap: without it the tool would have said 7.67 L, below what he actually used.

Ramesh says his weekday rush is 4:00-5:15 PM, but this one-day log's busiest hour is 18:00-19:00. I treat that mismatch as a reason to collect a second real day, not as proof that either one is wrong. He also said he would keep the 0.5 L reserve and lower the buffer on weekends and rainy afternoons.

Full notes and his words are in `fieldwork.md`.

## What Ramesh's answers changed in the tool

- **Log coverage (`--coverage`).** His real use (7.9 L) was higher than my log (6.67 L), so I added an option to correct for the part of the milk my log misses. With `--coverage 84` the tool scales the logged milk up by 100/84 before planning.
- **Hindi note (`--lang hi`).** Ramesh talks in Hindi and does not use a command line, so the daily mode can print its quick note in Hindi (Roman letters).
- **Peak hour from the data.** I stopped hardcoding a "15:30 rush". The reserve is now tied to the busiest clock hour in the log, which is where his answer and my data disagreed.

### Coverage: use it instead of the buffer, not on top of it

The coverage correction and the safety buffer both cover the same gap, so stacking them over-orders.

```
python run.py --data data.csv --coverage 84 --buffer 0
```

```
Coverage correction: my log captures 84% of real milk use, so logged milk is scaled up by 1.19x.
Milk used today: 7.94 L
Safety buffer: 0.0%
Expected requirement: 7.940 L
RECOMMENDED OPENING STOCK: 8.0 L
```

Coverage 84 with buffer 0 gives 8.0 L, which matches the 7.9 L he really used. Coverage 84 with the default 15% buffer on top (`--coverage 84 --buffer 15`):

```
Milk used today: 7.94 L
Safety buffer: 15.0%
Expected requirement: 9.132 L
RECOMMENDED OPENING STOCK: 9.5 L
```

That is 9.5 L, more than he used and more than the 9.0 L he bought. Pick one: the plain 15% buffer (simple), or the coverage correction with a small buffer.

### Hindi quick note

```
python run.py --data data.csv --mode daily --buffer 15 --peak-reserve 500 --lang hi
```

```
RAMESH JI KE LIYE (chhota note)
Kal subah 8.0 litre doodh se shuru karein.
18:00 baje se pehle aakhri 0.5 litre mat kholiye, jab tak zaroorat na pade.
```

Works with daily mode only.

## Short-term estimate

Give the current time and how many hours to cover. The tool uses only the sales logged in the same clock window, not the all-day average.

```
python run.py --data data.csv --mode short-term --now 16:30 --hours 2 --buffer 15
```

```
SHORT-TERM MILK PLAN
Window: 16:30 to 18:30 (2 hours)
Based on 4 logged sale(s) in that same window, over 1 day(s)
Milk used in that window: 1.02 L
Most frequently sold item in that window: elachi_tea
Safety buffer: 15%
RECOMMENDED MILK TO KEEP: 1.17 L

Only a few sales may fall in one window, so treat this as a rough guide.
It does not account for weather, holidays, supplier delays, or an unusual rush.
```

## Demo recording

3-minute screen recording: **[replace with your link]**

## Add a second real observation day

Append rows for a second real date to `data.csv`, keeping the same columns and an ISO timestamp. Do not create or estimate a second day. Then compare the real days:

```
python run.py --data data.csv --mode multi-day --buffer 15 --peak-reserve 500
```

Multi-day mode uses the average observed milk across the real days, reports the difference between the lowest and highest day, and rounds the buffered average to the next half litre.

## What it gets wrong

- It is based on one observation day. A second real day will improve it, but it still will not replace longer-term data.
- My log captured only about 84% of the milk Ramesh actually used, so some orders or milk use are missing from `data.csv`. The 84% figure itself comes from one day.
- Milk per cup is Ramesh's ladle estimate, not a measured amount.
- Short-term mode uses only the sales in one clock window, and on one day that is often just 2-5 sales, so the estimate is rough.
- Coverage and the safety buffer overlap. Using both together over-orders (see above).
- It cannot predict rain, a festival, a nearby event, delivery delays, or an unusual rush. Ramesh says weekends and holidays have a different pattern from weekdays, and the tool does not model that, because I have no weekend data.
- It depends on accurate manual recording.