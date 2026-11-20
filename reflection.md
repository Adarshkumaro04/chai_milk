# Reflection

## What I got wrong at the start
Before I went to the stall I believed daily milk demand followed predictable morning, afternoon, and evening blocks and that every customer order used milk. Then Ramesh told me he bought 9.0 L plus an unopened 500 ml backup packet, left about 1.1 L at closing (so actual use was ~7.9 L), estimates per-cup milk with a steel ladle rather than measuring cups, and sees a 4:00–5:15 PM weekday rush that shifts on Sundays/holidays, and my own log showed 6,670 ml (6.67 L) across 24 irregular rows including non-milk orders and a sale at 20:45. The thing that surprised me most was that my CSV captured only about 84% (6.67 L out of ~7.9 L) of the milk he actually used, showing how easily unlogged orders or off-counter milk use leave a raw tally short without a buffer.

## What I would cut
If I had to remove one thing from the tool it would be extra multi-metric breakdowns or complicated tuning knobs because they add clutter without helping a quick daily milk estimate. Ramesh would never use complex configuration flags or manual spreadsheet-style tracking because he runs a fast counter where speed and simplicity matter most.

## Where AI helped
AI helped me with structuring the CSV parsing and validation logic for zero-milk and malformed rows as well as organizing early markdown drafts. It saved me about an hour or two of boilerplate setup and edge-case structuring because I could test input handling and refine the workflow faster.

## Where AI wasted time or was wrong
One specific time AI was wrong or unhelpful: an earlier draft stated a 6,040 ml (6.04 L) milk total instead of 6,670 ml (6.67 L) and left a leftover citation tag in the text. How I noticed: checking the numbers against `data.csv` and the script output caught the wrong total and percentage, and reviewing the draft text caught the stray citation tag. What I did instead: I corrected the total to 6,670 ml (6.67 L), updated the ratio to ~84% (6.67 ÷ 7.9), removed the stray tag, and aligned the conversation time with closing.

## What I would do with another day
I would log observations across multiple days—including a Sunday or rainy day—to compare weekday vs. weekend rush patterns and test how well the buffer holds up against real day-to-day swings.