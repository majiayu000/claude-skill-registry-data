---
name: plan-smart-routes
description: "Plans and compares time-aware trips with public transport plus walking by default: live traffic and service checks, weather, opening hours, fares, multi-stop scheduling, ETA uncertainty and map links (Google Maps, Yandex, Moovit, Apple Maps and others). Turkish triggers: buradan şuraya nasıl giderim, kaç dakikada varırım, hangi otobüs/metro, aktarma, yol tarifi, rota planla. More triggers: otobüs saati, metro, çok duraklı rota, trafik."
---

# Plan Smart Routes

## Purpose

Produce a short, usable trip answer backed by current evidence. Analyze broadly, answer compactly. Never turn a generated map link, a static schedule, or an unavailable provider into a claimed live route.

Default to **public transport + necessary walking**, prefer rail/metro over road buses when otherwise comparable, and use driving, cycling, or walking-only only when the user asks or clearly implies it.

## Load the Right References

- Read [intake-and-output.md](references/intake-and-output.md) for every trip request.
- Read [route-synthesis.md](references/route-synthesis.md) whenever comparing, timing, scoring, costing, or scheduling routes.
- Read [provider-capabilities.md](references/provider-capabilities.md) before retrieving provider alternatives or generating navigation links.
- Read [istanbul-sources.md](references/istanbul-sources.md) whenever any leg is in İstanbul.
- Read [open-data-stack.md](references/open-data-stack.md) for GTFS, GTFS-Realtime, OpenTripPlanner, geocoding, OpenStreetMap, or technical integration questions.

## End-to-End Workflow

### 1. Parse the request into time blocks

Extract:

- origin, destination, ordered or reorderable intermediate stops;
- travel date and whether the stated time means **depart at** or **arrive by**;
- mode and constraints: metro-heavy, few transfers, little walking, wheelchair access, luggage, bike, car;
- intent: urgent, balanced, comfortable, or leisure;
- dwell time, appointments, venue closing times, companions, and fare/pass profile;
- shared map URLs and coordinates.

A long visit, an appointment, or a jump from morning to evening starts a new time block. Plan each block separately. Preserve ordered stops within each continuous block.

### 2. Stop on missing essentials

Do not calculate a route until the following are known for the relevant block:

1. origin;
2. destination;
3. date;
4. departure time or required arrival time.

For a visited intermediate stop before another deadline, its dwell time or latest leave time is also essential. Do not invent a visit duration.

“Şimdi” supplies date and departure time. If device location is unavailable, say so and ask for the exact origin or a nearby landmark. Ask one short question containing only the missing fields. If a place is ambiguous, give at most three concrete candidates and ask the user to select one. Do not silently choose a similarly named branch or district.

If wording such as “09:00’da gideceğim/geçeceğim” could mean departure or arrival and the distinction changes the plan, ask. Do not replace clarification with “şöyle varsaydım.”

A large district/neighborhood name alone is not exact enough for an ETA or navigation link. Ask for a square, stop, address, entrance, or pin in the same first question as the missing time fields when it could change the route.

### 3. Resolve locations before routing

Follow redirects on shared map links and extract place identity, coordinates, branch, entrance, and locality when accessible. A Google link is a location reference, not a command to use only Google. Cross-check the same coordinates/name in other available providers and official venue sources.

Prefer explicit coordinates, a shared map pin, or a verified place page. Do not embed the public Nominatim service as a generic automatic geocoder. A route request authorizes the necessary read-only lookups for places supplied in that request, but not persistence. Minimize broad provider fan-out for sensitive exact home/work/medical locations and ask before sending them beyond the providers needed for the answer.

For a supported map URL, safely follow provider redirects and extract only explicit coordinates:

```powershell
python scripts/map_link_resolver.py "https://maps.app.goo.gl/..."
```

This is URL resolution, not place-name geocoding. Verify the returned branch/entrance in the human-visible page.

### 4. Infer the profile without unnecessary questions

- **urgent**: work, school, internship, exam, flight, appointment, “yetişmem lazım”, or a hard deadline;
- **comfortable**: less walking, fewer transfers, luggage, accessibility, or comfort request;
- **leisure**: sightseeing, scenic, relaxed, no deadline;
- **balanced**: otherwise.

When no preference is given, rank all candidates using balanced logic and return the recommended route plus at most two materially different alternatives such as ⚡ faster or 😌 fewer transfers. Do not ask the user to choose a profile first.

### 5. Gather all practical candidates

Search every visible alternative in accessible Google Maps, Yandex Maps, Moovit, official operator planners, and useful regional providers—not just each product’s first suggestion. Add HERE, Bing, Apple Maps, Waze, Citymapper, OpenStreetMap, or a local OpenTripPlanner only where their documented coverage and mode fit.

For every candidate record provider, observed time, route/line sequence, duration, walking, transfers, fare evidence, realtime/static status, and source URL. Mark provider failure as `no_data`; use `no_route` only when the provider actually reports no route. Never infer route results from deep-link generation.

Paid/keyed Google Routes, Yandex routing/matrix, or Moovit APIs are optional adapters only. Without configured credentials, use accessible product pages, official operator data, and no-key navigation links; never pretend the APIs ran.

### 6. Normalize, deduplicate, and hard-filter

Merge candidates with the same material line/stop sequence while preserving every provider’s ETA and evidence. Reject before scoring when a route is cancelled, inactive on that service date, inaccessible under a stated need, misses a hard arrival/opening window, or has an impossible transfer.

Use the local helper after collecting candidates:

```powershell
python scripts/route_toolkit.py score --input routes.json --profile balanced
```

The input schema and scoring rules are in [route-synthesis.md](references/route-synthesis.md). Missing soft metrics are omitted and weights rebalanced; they are never filled with invented values.

### 7. Validate live conditions twice

First check before scoring, then recheck the selected route immediately before answering:

- exact transit line, station, stop, ferry, and transfer alerts;
- cancellations, short turns, frozen/changed services, extra event service;
- road closures, traffic, matches, demonstrations, construction, and large events;
- weather at origin, exposed transfer points, and destination near travel time;
- venue opening hours and last-entry constraints;
- current fare rules relevant to the actual modes and rider.

Official operator/current feeds outrank third-party planners. Record source and observation time. Realtime absence means “no realtime data,” not “on time.” If the trip is outside a forecast/realtime horizon, provide a schedule-only plan and say to recheck near departure.

For İstanbul, run the bounded official signal helper when relevant:

```powershell
python scripts/istanbul_live.py --line M2 --line M7 --bus-line 34AS
```

Add `--include-fares` only when a fare answer is needed. A citywide traffic index is context, not a route-segment ETA.

For personal, non-commercial weather sampling with verified coordinates:

```powershell
python scripts/route_toolkit.py weather --point "41.0082,28.9784|Başlangıç" --point "41.0422,29.0083|Hedef" --at "2026-08-01T09:00:00+03:00"
```

### 8. Compare ETAs conservatively

Use provider predictions as correlated observations, not independent votes. Prefer direct fresh operator realtime and historical calibration when available. Report a planning range and buffer, never “kesin şu dakikada varırsın.” Show confidence as high/medium/low/unknown with one reason.

The helper can compare collected estimates:

```powershell
python scripts/route_toolkit.py compare --input predictions.json
```

For urgent trips, work backward from the required arrival time using the conservative upper duration, transfer risk, entry/walk time, and an explicit safety buffer.

### 9. Optimize stops and opening windows

For reorderable stops, obtain a time-dependent travel matrix from real candidates first. Then use:

```powershell
python scripts/route_toolkit.py optimize --input day-plan.json
```

The helper explores at most eight stops and only supplied travel times. It does not fetch or invent a matrix. For transit, a road-only TSP is not valid; recompute each leg for its actual departure time.

Warn with ⚠️ when a venue will be closed, the arrival window cannot be met, or the latest feasible departure has passed. Suggest the smallest useful change, such as leaving earlier or changing stop order.

### 10. Generate only truthful navigation links

Generate links after route selection and place resolution:

```powershell
python scripts/route_toolkit.py links --origin "41.0082,28.9784|Başlangıç" --waypoint "41.0256,28.9741|Durak" --destination "41.0422,29.0083|Hedef" --mode transit --when "2026-08-01T09:00:00+03:00"
```

Return only providers whose links encode the required points/mode and are plausibly available in that geography. A continuous block may be one Google/HERE/Bing multi-stop link where supported. Separate morning/evening blocks require separate links because one deep link cannot preserve independent appointment times. Explain this in one short sentence, not by fabricating a single timed link.

### 11. Handle fares narrowly

By default calculate only the user’s cost. Mention companions only when the user mentions them; calculate each fare class separately. If known, show pass/abonman usage and pay-as-you-go/student cost. Verify transfer, distance-based, refund, special-line, night, ferry, Marmaray, and Metrobüs rules before totaling. If the fare profile or source is missing, ask only when cost is material; otherwise omit the number rather than guessing.

### 12. Save preferences only with consent

Reading preferences is safe:

```powershell
python scripts/route_toolkit.py preferences show
```

Writing requires explicit user approval and `--allow-write`. Exact home/work labels or coordinates also require `--allow-sensitive`. Never save a one-off route automatically.

## Final Integrity Check

Before answering, verify:

- all time blocks, stops, dwell times, and arrive/depart semantics were preserved;
- the selected service runs on that date and current alerts were checked;
- ETA has a range, buffer, confidence, and source timestamp;
- opening/weather/fare claims are sourced or omitted;
- every link’s encoded capabilities match what the text promises;
- inaccessible providers are omitted rather than presented as failures of the journey;
- the answer follows the compact format in [intake-and-output.md](references/intake-and-output.md).

If current evidence is insufficient, say exactly what is unknown and give a recheck action. Correct uncertainty is better than false precision.
