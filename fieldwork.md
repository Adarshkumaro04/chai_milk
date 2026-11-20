# Fieldwork: Tea-stall milk planning

**The photo files are included below. Before submission, add the truthful continuous 20-minute observation window and any reconstruction notes.**

## Observation

- Date: 20 November 2026, a regular college working day
- Place: Ideal Tea & Coffee, opposite the main gate of IIIT Allahabad, Jhalwa, Prayagraj
- Stall hours: 07:30 to 21:00
- Two timestamped photos:
  - `photos/stall_cup_measure_0750.png` - 20 November 2026, 07:50:12
  - `photos/stall_menu_2045.png` - 20 November 2026, 20:45:08
- Observation and collection method: I logged 24 sales entries from 07:50 to 20:45. For every entry, I recorded the time, product, quantity, and milk used per unit. The irregular 15-50 minute gaps represent real customer/order arrivals, not fixed time buckets. I also stayed at the stall continuously from **[add the true start time]** to **[add the true end time]** for at least 20 minutes and captured the timestamped photos above. Lemon-tea rows are recorded with 0 ml because they do not use milk. **If any row was reconstructed from a note or memory rather than written at the moment of sale, state that here before submission.**

## Conversation

- Person's name and role: Ramesh, stall owner and tea/snack vendor
- What they said:
  1. “Lecture ke baad 4 se 5 baje ke beech line lag jaati hai, ek saath 5-6 chai ka order aata hai.”
  2. “Doodh bachta nahi, raat ko jo bach gaya woh subah tak kharab ho sakta hai, isliye kam hi rakhta hoon.”
  3. Ramesh said that milk-heavy drinks use more milk but can still be worthwhile because they have a higher selling price.
- What surprised me: Afternoon sales used 3,210 ml (48% of the observed milk), more than the evening. The 11 milk-based orders of three or more units used 4,960 ml, about 74% of the total milk. Ramesh described the main queue as 16:00-17:00, but this one-day log shows the largest hourly milk total at 18:00-19:00 (1,100 ml). This mismatch is a reason to collect a second real day instead of treating one day as a fixed rush-hour rule.

## Raw data

`data.csv` contains one row per observed sale or order.

- Collection method: I recorded the 24 rows on 20 November 2026 while observing sales at the stall. The log covers the full opening day, from the first recorded sale at 07:50 to the last at 20:45.
- Milk-per-unit method: The observed menu items were recorded as follows: masala tea 100 ml, single tea 80 ml, full tea 120 ml, ginger tea 90 ml, elachi tea 100 ml, coffee 150 ml, and milk 200 ml per unit. Lemon tea is recorded as 0 ml.

## Checked summary

The script reproduces these figures from `data.csv`:

- 24 total entries; 20 milk-based entries.
- Total observed milk: 6,670 ml (6.67 L).
- Morning: 1,330 ml; afternoon: 3,210 ml; evening: 2,130 ml.
- 11 milk-based orders with three or more units used 4,960 ml, about 74% of the observed milk.

## Ramesh's reaction to the plain-language output

Show Ramesh the plain-language output in the terminal and record his response below in your own words.

- Did the 8.0 L suggestion sound practical? [add Ramesh's actual response]
- Did he agree with keeping 0.5 L unopened before the data-derived peak hour? [add Ramesh's actual response]
- What would he change in the wording or buffer? [add Ramesh's actual response]
