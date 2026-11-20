# Research: Ideal Tea and Coffee Milk and Batch Prep Planner

## Problem in Five Lines

Ramesh runs a local tea and snack stall and currently estimates daily milk quantities by rough habit rather than item-level demand across time windows.

Different drinks use different milk volumes, such as 100 ml for masala tea, 80 ml for single tea, 120 ml for full tea, 150 ml for coffee, and 200 ml for milk; lemon tea uses none.

Demand fluctuates unevenly across morning, afternoon/snack, and evening rush windows, creating a risk of tight supply during surges and leftover milk when demand slows.

A lightweight script over real stall observations can convert recorded item quantities into total milk demand and suggest a practical prep quantity with a configurable buffer.

This gives Ramesh a quick daily reference without turning his fast-paced counter into a complex software workflow.

## Existing solutions

### 1. Spreadsheet inventory or manual-ledger tracking

Spreadsheet templates assume the user has time to maintain structured tables, formulas, and ongoing manual updates around busy service windows. At a fast-moving tea and snack stall, opening a sheet or adjusting formulas during rush hours interrupts service and quickly falls out of date. Ramesh needs one fast output from recorded counts and per-unit milk values, not a workbook to manage.

### 2. POS and restaurant inventory software

Full POS and inventory systems, such as Petpooja or Square-style billing and stock tools, are designed for multi-staff billing, receipts, tax/catalog management, and broader restaurant stock workflows. For a small stall focused on quick counter orders and daily milk planning, these suites add setup overhead, screen clutter, and features Ramesh does not need. A small command-line tool that reads a CSV log and outputs a suggested milk quantity with an adjustable buffer better fits this scale.

## Sources actually read

1. [Safety Stock](https://www.investopedia.com/terms/s/safetystock.asp)
   - Safety stock helps protect against demand spikes and variability, reducing stockouts during busy periods.
   - Too much buffer increases waste and excess cost, while too little can lead to missed sales during a surge.
   - A simple buffer rule is a practical first step before using more complex variance-based estimates.
2. [Cold Food Storage Charts](https://www.foodsafety.gov/food-safety-charts/cold-storage-charts)
   - Perishable items such as milk are sensitive to holding conditions and time.
   - Excess preparation can increase the chance of waste and spoilage alongside its cost.
   - Demand buffers should be balanced with batch awareness so the stall does not over-prepare milk.
