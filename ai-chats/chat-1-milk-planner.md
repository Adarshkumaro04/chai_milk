To fit the 1-Day Take-Home Assignment, a strong problem statement needs to be something you can observe yourself within walking distance, tie to one named person, measure across at least 20 real entries (data.csv), and solve with a small, transparent script where one real surprise shows up during your conversation.   
1-Day Take-Home Assignment for SDE 1.docx

Here are concrete problem statement ideas tailored for campus/local life around IIIT Allahabad / Jhalwa, Prayagraj (or back home), built to avoid auto-rejects (no to-do lists, weather apps, chatbots, APIs, or external datasets):   
1-Day Take-Home Assignment for SDE 1.docx

1. Campus Tea / Snack Stall Prep & Wastage
Target Person: A tea/snack stall vendor near campus or Jhalwa.   
1-Day Take-Home Assignment for SDE 1.docx

Problem Statement: Evening rush demand for a specific item (like samosas, buns, or milk tea batches) spikes unpredictably across short windows, causing early stockouts during peak crowds or unsold leftovers at closing.

What You Log (
≥
20
≥20 rows): Batch time, units prepared, units sold per 15–30 min slot, weather/crowd note, and leftover count.

Tool Output: Recommends batch size and refill timing for the next day's rush window based on historical demand and a configurable safety buffer.   
1-Day Take-Home Assignment for SDE 1.docx

2. Hostel / Mess / Canteen Queue & Service Bottlenecks
Target Person: A canteen/mess counter staff member or supervisor.   
1-Day Take-Home Assignment for SDE 1.docx

Problem Statement: During peak meal or snack hours, bottlenecks form at a specific counter or pickup window because service time slows down on certain orders or rush bursts.

What You Log (
≥
20
≥20 rows): Arrival/order timestamp, item/order type, wait or service duration, and queue length at the start of the entry.

Tool Output: Flags peak congestion windows and suggests when to pre-prep high-frequency items or open a second handoff spot.

3. Local Kirana / Stationery / Photocopy Shop Restock Timing
Target Person: A nearby shopkeeper or print/stationery operator.   
1-Day Take-Home Assignment for SDE 1.docx

Problem Statement: Fast-moving everyday items or print/binding supplies run low mid-week or right before exams/rush hours because restocking is based on memory rather than recent sales/usage pace.

What You Log (
≥
20
≥20 rows): Item/job ID, time/date, units sold or pages/sheets used, and remaining stock noted during observation.

Tool Output: Calculates daily burn rate and outputs a reorder alert threshold (days of cover left) for each tracked item.

4. Hostel / Campus Commute & Delivery Handoff Delays
Target Person: A security guard, gate/hostel desk staff member, or delivery/errand point person.   
1-Day Take-Home Assignment for SDE 1.docx

Problem Statement: Peak arrival bursts of deliveries or student/visitor pickups cluster in narrow time blocks, creating congestion or delayed handoffs at a specific gate or desk.

What You Log (
≥
20
≥20 rows): Arrival timestamp, handoff/clearance duration, package/visitor type, and whether a delay/pile-up occurred.

Tool Output: Identifies high-load time blocks and recommends peak handoff windows or batching rules.

5. Household / Family Grocery & Cooking Prep Tracking
Target Person: A family member managing daily meals or household groceries.   
1-Day Take-Home Assignment for SDE 1.docx

Problem Statement: Certain perishable vegetables, dairy items, or staples either run out unexpectedly mid-week or sit unused past peak freshness because buying quantities aren't matched to actual usage cadence.

What You Log (
≥
20
≥20 rows): Item name, date/meal slot, quantity bought/opened, and remaining/wasted quantity observed.

Tool Output: Suggests a simple next-buy quantity and shopping interval so staples last closer to the next market run without overbuying.

Quick Filter Before You Commit (research.md within Hour 1)
Make sure your choice passes all of these checks:

Can you get 
≥
20
≥20 real rows in ~1.5 hours? Counting 20–30 orders, customers, items, or handoffs in one focused stretch is much faster than waiting days for 20 separate days of data.   
1-Day Take-Home Assignment for SDE 1.docx

Is there room for a real surprise? Ask how they currently decide (gut feel, last night's leftover, fixed habit) and look for where their rule of thumb clashes with what you actually see.   
1-Day Take-Home Assignment for SDE 1.docx

Can you easily change a threshold live? Design your script around clear parameters (like a buffer percentage, wait-time limit, or low-stock days threshold) so modifying one number on the 10-minute call is effortless.   
1-Day Take-Home Assignment for SDE 1.docx

Which of these feels easiest for you to walk over to and observe right away for your first commit?