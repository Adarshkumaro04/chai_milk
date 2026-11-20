# Fieldwork: Tea-stall milk planning

## Observation

- Date: 20 November 2026, a regular college working day
- Place: Ideal Tea & Coffee, opposite the main gate of IIIT Allahabad, Jhalwa, Prayagraj
- Stall hours: 07:30 to about 20:45 (Ramesh says he usually closes around 20:30)
- Two timestamped photos:
  - `photos/stall_cup_measure_0750.png` - 20 November 2026, 07:50:12
  - `photos/stall_menu_2045.png` - 20 November 2026, 20:45:08
- Continuous observation window: I stayed at the stall from 16:30 to 16:50  (at least 20 minutes).
- Collection method: I logged 24 sales entries from 07:50 to 20:45. For every entry, I recorded the time, product, quantity, and milk used per unit. The irregular 15-50 minute gaps are the real gaps between orders I noted, not fixed time buckets. Lemon-tea rows are recorded with 0 ml because they do not use milk.

## Conversation with Ramesh

- Name and role: Ramesh, owner of Ideal Tea & Coffee
- When and where: 2026-11-20, around 20:50 (right after the evening wrap-up), at the stall counter
- Language: Hindi / Hinglish; English below is my translation

What he told me:

1. Milk bought today: He bought 9.0 L in the morning crate plus a 500 ml backup packet (not opened today). About 1.1 L was left at closing. He usually closes around 8:30 PM, but today work continued until about 8:45 PM.
   - His words: "Subah 9 liter ki crate li thi aur 500 ml ka extra packet rakha tha, par woh khola nahi. Aam taur par 8:30 baje ke aas-paas band karte hain, par aaj 8:45 tak kaam chala aur 1.1 liter bacha tha."

2. Rush hour: On weekday lecture/office days the main rush is 4:00 to 5:15 PM. On Sundays and holidays the 4 PM rush drops by nearly half and shifts later to 6:30-8:00 PM.
   - His words: "College ya office wale din 4 se 5:15 baje bheed rehti hai; Sunday ya chhutti wale din 4 baje wali bheed aadhi se bhi kam ho jaati hai aur shaam 6:30 se 8 baje ke beech aati hai."

3. Stock-out: Last Tuesday around 6:15 PM, after a rain crowd, he ran out of milk and turned away 8-10 customers. His helper bought two 500 ml packets at retail price. (This is what he told me; I did not see it myself.)
   - His words: "Pichhle Tuesday ko 6:15 baje baarish ke baad achanak bheed aayi thi to doodh khatam ho gaya tha, 8-10 grahak lautane pade aur ladke ko retail se 500 ml ke do packet lane bheja."

4. Milk per cup: He does not measure with a measuring cup; he estimates using a steel ladle and boiling ratio. The per-unit milk values in my CSV are therefore his estimates, not measurements.
   - His words: "Naap ke nahi daalta, steel ki karchhi aur ubaalne ke hisaab se andaaze se daalta hoon."

5. Reaction to the tool: 8.0 L "feels close" for a normal weekday. He would not reduce the 0.5 L reserve because emergency dairy runs cost extra and waste time, but he would lower the buffer on weekends and rainy afternoons when demand slows.
   - His words: "Normal din ke hisaab se 8 liter ka hisaab kaafi kareeb lagta hai; 0.5 liter ka backup kam nahi karunga, par weekend ya baarish mein thoda kam rakhenge."

What surprised me: My log counted 6.67 L, only about 84% of the roughly 7.9 L he actually used (9.0 L bought minus 1.1 L left). Without a buffer the tool's 7.67 L would have been below his real use; only the 15% buffer and the round-up to 8.0 L covered it. Also, Ramesh described the weekday rush as 4:00-5:15 PM, but my one-day log shows the largest hourly milk total at 18:00-19:00 (1,100 ml). One day cannot settle this, so a second real day is needed.

## Raw data

`data.csv` contains one row per observed sale or order.

- Collection method: see "Collection method" above. The log runs from the first recorded sale at 07:50 to the last at 20:45.
- Milk-per-unit values used: masala tea 100 ml, single tea 80 ml, full tea 120 ml, ginger tea 90 ml, elachi tea 100 ml, coffee 150 ml, milk 200 ml, lemon tea 0 ml. These are Ramesh's ladle estimates (see Conversation, point 4), not measured amounts.

## Checked summary

The script reproduces these figures from `data.csv`:

- 24 total entries; 20 milk-based entries.
- Total logged milk: 6,670 ml (6.67 L).
- Morning: 1,330 ml; afternoon: 3,210 ml (48%); evening: 2,130 ml.
- 11 milk-based orders with three or more units used 4,960 ml, about 74% of the logged milk.
- Busiest clock hour: 18:00-19:00 (1,100 ml).

## Field check

The tool recommended 8.0 L. Ramesh bought 9.0 L and used about 7.9 L (1.1 L left at closing), so the recommendation was within 0.1 L of real use, and he over-ordered by about 1 L. My log counted about 84% of his real use, so the 15% buffer is what covers the gap.

## Ramesh's reaction to the plain-language output

- 8.0 L suggestion: he said it "feels close" for a normal weekday.
- 0.5 L reserve: he would keep it, because emergency dairy runs cost extra and waste time.
- Buffer: he would lower it on weekends and rainy afternoons, when demand slows.