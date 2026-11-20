# Reflection

## What I Got Wrong at the Start

When I started this project, I assumed that milk consumption would follow a predictable pattern throughout the day, with separate morning, afternoon, and evening demand. However, after visiting Ideal Tea & Coffee and observing actual sales, I realised that orders do not happen at fixed intervals. Demand changes throughout the day, and sometimes a few large orders can suddenly increase milk consumption. I also initially assumed that every item sold at the stall required milk, but items like lemon tea do not use milk at all. Another thing I overlooked was that the milk used in each cup is based on Ramesh's experience and estimation rather than exact measurements. These observations helped me understand that real-world demand is not always as simple as it looks in a dataset.

## What I Would Cut

I would avoid adding complicated forecasting methods, unnecessary charts, and too many configuration options. The main purpose of this project is to help Ramesh decide how much milk he should arrange for the day. He does not need a complicated system; he needs a quick and understandable recommendation. I would keep the interface simple and allow him to adjust the safety buffer depending on the day, weather, and expected rush.

## Where AI Helped

AI helped me get started with the code, especially reading the CSV file, calculating total milk consumption, and handling invalid entries and products that use zero milk. It also helped me think about possible edge cases and organise the initial implementation. This saved time during development and allowed me to focus more on field observations, checking the calculations, and understanding the actual needs of the stall owner.

## Where AI Wasted Time

At times, AI suggested assumptions that sounded reasonable but did not match the actual working conditions of the tea stall. I had to verify its suggestions using my recorded sales and conversations with Ramesh. For example, my recorded data showed milk consumption of 6.67 litres, whereas Ramesh estimated that he actually used around 7.9 litres that day. The tool recommended 8 litres, which was close to his actual usage, but this was mainly possible because of the additional safety buffer. I also learned that testing the recommendation against the same day's data does not prove that the system can accurately predict future demand.

## Final Takeaway

My biggest learning from this project was that a useful solution should be built around the actual needs of the person using it. After discussing the recommendation with Ramesh, I learned that he was comfortable with 8 litres for a normal weekday and preferred keeping the 500 ml emergency reserve. He also suggested reducing the buffer on weekends and rainy days when demand is lower. This feedback helped me understand that user experience and real-world observations matter just as much as the code. I would now like to test the system on another working day before making any claims about its accuracy.