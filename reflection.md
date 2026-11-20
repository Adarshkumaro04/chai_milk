# Reflection

## What I Got Wrong at the Start

At the outset I thought milk consumption and customer demand would be fairly predictable with fairly regular patterns throughout the day, i.e. a fairly distinct morning, afternoon and evening block. The actual data however showed that it was far more erratic. There was a big milk-demand spike for full tea at 16:15, where six units used 720 ml, and another for milk at 18:45, where three units used 600 ml. I also assumed that every order would involve milk and that therefore the number of customers would be a direct indicator of milk requirement. Clearly that wasn't the case because lemon tea uses no milk. That was the first thing that became apparent. You simply can't work out your milk requirement from customer count alone. The second thing was that you can't just set your daily preparation rules in advance. You have to be prepared to change them in response to what Ramesh actually sees at the stall.

## What I Would Cut

I'd steer well clear of all the bells and whistles, the complex forecasting methodologies and all that. The whole point of this is to enable Ramesh to make a quick decision as to how much milk he needs for the day. It's all about simplicity, clarity and ease of use. He should be able to change a threshold as and when he wants to without spending any time at all.

## Where AI Helped

AI helped me get off the ground with the basic code structure (reading the data.csv file, working out the total milk consumption, dealing with the invalid/zero milk entries etc). It also helped me think through some of the potential edge cases and structure my initial thoughts. It saved me a lot of time and allowed me to concentrate on actually watching the stalls and testing the solution.

## Where AI Wasted Time

On occasion the AI would suggest some fairly generic assumptions about how a tea stall works or would put forward examples that were just a bit too perfect in the context of the real world. I had to go back and check those suggestions against what we actually saw and what the original data had to say. I also spent a fair bit of time verifying the calculations and the suggestions it had generated to ensure that the final solution was something that was actually workable and accurate.

**My biggest learning:** A useful solution doesn't have to be complicated. It just needs to solve the problem and work in the way people actually work.
