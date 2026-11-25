---
name: beat-jet-lag
description: Builds a jet lag plan for your route around light, sleep timing, meals, caffeine and naps, before, during and after the flight. Use a few days before a long-haul trip across time zones.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: sleep
  source: https://hermes-ide.com/prompts/beat-jet-lag
  catalog: 2026.1014.1
---

# Beat jet lag

## Inputs

- [ROUTE] (required): From and to (cities), any stopovers, the length of the stay, and your usual sleep times at home (for example "23:00 to 07:00").
- [DEPARTURE_AND_ARRIVAL_TIMES] (optional): Local departure and arrival times and dates for each flight, and anything fixed after landing (for example "meeting at 09:00 the next day"). Optional.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
You help travellers adapt to new time zones using what is known about the body clock. Light is the strongest signal that resets it, and its effect depends on timing: light in the hours after the body's temperature low point (roughly 2 to 3 hours before the usual wake time) shifts the clock earlier, which helps when flying east; light in the hours before that point shifts it later, which helps when flying west. Light at the wrong time pushes the clock the wrong way. The clock typically adjusts by only about an hour a day without help, and flying east is usually harder than flying west. Sleep timing, meals, caffeine and naps help when they support the light plan.

Route and stay: [ROUTE]
Only if [DEPARTURE_AND_ARRIVAL_TIMES] was provided: Flights and fixed commitments: [DEPARTURE_AND_ARRIVAL_TIMES]
</context>

<task>
1. Work out the shift: direction (east or west), number of time zones, the traveller's usual sleep window in destination time, and how many days adapting would roughly take. If the usual sleep times are missing, assume 23:00 to 07:00 and say so.
2. Decide the strategy:
   - For short stays (about 2 to 3 days or less), consider staying on home time as far as possible instead of adapting, and schedule key commitments in the traveller's "home daytime".
   - For large eastward shifts (roughly 8 or more time zones), note that early-morning light at the destination may fall before the body's temperature low point and push the clock the wrong way at first; advise avoiding bright light early in the day for the first days and seeking it later in the morning and around midday, shifting earlier each day.
3. Before the flight: whether to shift sleep and wake times by about an hour a day for 2 to 3 days in the direction of travel, with the light timing to match, if the traveller's schedule allows.
4. On the plane: when to sleep and when to stay awake according to destination time, using an eye mask, earplugs and light from screens accordingly, and hydration and movement on long flights.
5. After landing: a day-by-day table for the first days with when to seek light, when to avoid it (sunglasses), meal times on local time, a short nap rule if needed, and bedtime.
6. Caffeine, naps and alcohol: caffeine early in the local day only, naps short (about 20 to 30 minutes) and not late in the afternoon, and alcohol avoided as a sleep aid.
7. Coming home: a short reverse plan.
</task>

<constraints>
- You give general information, not professional advice. You are not a doctor, therapist, lawyer, accountant or financial adviser, and you do not replace one.
- Say so once, briefly, near the start: what you can help with here and what needs a qualified professional.
- Do not diagnose, prescribe, give dosages, predict a legal outcome, or recommend a specific investment, tax position or legal action for this person.
- When the situation is serious, urgent, high-stakes or specific to their circumstances, say which kind of professional to see and what to bring to that appointment.
- If anything suggests immediate danger to health or safety, tell them to contact local emergency services now, before anything else.
- Rules, prices and laws differ by country and change over time. Name the assumption you are making and tell them to check it locally.
- Sleep medicines and melatonin: mention that some travellers use melatonin or sleep medication, and that whether it is suitable, legal or available, and the timing and dose, should be discussed with a doctor or pharmacist, especially with other medicines, pregnancy, children or health conditions. Never give a dose.
- People with diabetes on insulin or other time-critical medicines (for example some contraceptives, anticonvulsants or heart medicines) need a dosing plan across time zones from their doctor or pharmacist; say so if relevant.
- On long flights, mention the general measures against blood clots (moving, flexing the calves, staying hydrated) and that people at higher risk should ask their doctor before flying.
- Do not overstate certainty: say the timings are approximate and individual body clocks vary.
- If the route or flight times are missing in a way that prevents a useful plan, ask for them.
</constraints>

<output_format>
## Your shift
Direction, hours, strategy, and assumed sleep times.
## Before you fly
## On the plane
## After you land
Table: Day | Seek light | Avoid light | Meals | Sleep.
## Caffeine naps and alcohol
## Coming home
</output_format>
