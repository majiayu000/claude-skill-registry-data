---
name: travel-search-bladebro
description: Find practical ways and travel times between locations using Google Maps, Google Flights and transport-operator websites through Bladebro. Use for how to get from A to B, journey duration, train/bus/transit/driving/walking options, airport transfers, or comparing transport modes.
allowed-tools: Bash(bladebro:*)
---

# Multimodal Travel Search with Bladebro

Find realistic A→B options and door-to-door implications. Prefer primary routing/search surfaces, then verify the operator when timetable or booking details matter.

## Boundaries

- Research and compare only. Do not purchase tickets or complete bookings.
- Distinguish scheduled journey time from total door-to-door time.
- Do not invent transfer times, frequencies or fares.
- Treat schedules/fares as live and date-sensitive.

## Step 1: classify the journey

Use the most appropriate path:

### Local / metro / city-to-city where Maps has transit

Use Google Maps directions:

```text
https://www.google.com/maps/dir/?api=1&origin={ORIGIN}&destination={DESTINATION}&travelmode={MODE}
```

Modes supported by the URL include `transit`, `driving`, `walking`, and `bicycling` where available.

Start with transit when the user has not specified a mode and public transport is plausible.

```bash
bladebro nav "$URL"
bladebro see extract auto --json
```

If needed:

```bash
bladebro see content --json
bladebro see model --json
```

### Long-distance journey where flying may be competitive

Compare:

1. surface option(s): rail/bus/car via Maps or operator search
2. flight option via Google Flights
3. airport access + security/buffer + destination transfer when estimating door-to-door usefulness

Do not compare a 1h flight directly with a 4h train without noting airport overhead.

### Rail/bus/ferry-specific journeys

Use Google Maps/transit or Google Search for discovery, then open the actual operator site to verify current schedules/frequency and fare if the user needs booking-grade detail.

## Step 2: search Maps

Construct the directions URL and extract:

- primary mode
- departure/arrival times if a departure date/time is known
- in-vehicle/journey duration
- transfers
- walking legs
- service/operator names when visible
- alternative routes

When the UI supports departure/arrival time selection and the user's date matters, configure the requested date/time interactively with Bladebro.

## Step 3: flight comparison when relevant

Use the Google Flights natural-language fast path:

```text
https://www.google.com/travel/flights?q=Flights+from+{ORIGIN}+to+{DEST}+on+{YYYY-MM-DD}+one+way
```

Extract representative nonstop/fast/cheap options. Do not over-search flights for short trips where surface transport is clearly dominant unless the user asks.

## Step 4: operator verification

Open the official operator's site when any of these are important:

- exact timetable
- service frequency
- reservations required
- luggage rules
- fare
- engineering works / disruptions
- ferry check-in deadlines

Use visible official-site evidence, not assumptions.

## Door-to-door comparison

Report separate components when useful:

```text
Train: 3h 05m station-to-station
+ ~20m to station
+ ~15m arrival buffer
= ~3h 40m practical door-to-door before destination transfer
```

For flights include realistic airport-access and pre-departure overhead, but label any non-source-specific buffer as an estimate rather than a scheduled fact.

## Output

Use a compact comparison:

| Option | Scheduled time | Practical total | Changes | Indicative cost | Notes |
|---|---:|---:|---:|---:|---|

Recommend one option based on the user's stated priorities: fastest, easiest, cheapest, scenic, luggage-friendly, etc.

## Multi-leg planning

For itinerary requests, evaluate each leg independently and flag weak connections. Prefer robust transfers over theoretically fastest itineraries when the time saving is small.

## Recovery

- CAPTCHA/bot challenge: do not bypass.
- Maps cannot show the requested date: verify with the operator directly.
- Ambiguous station/airport: use the city/location context and state which terminal/station you used.
- Cross-border/international: check whether the route changes operators or requires reservation/security/border time.
