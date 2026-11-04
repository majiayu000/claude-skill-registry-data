---
name: activities-search-bladebro
description: Find and compare restaurants, bars, cafes, sights, museums, parks, tours, adventure parks and other things to do using Google Maps and the web through Bladebro. Use for what to do, where to eat/drink, attractions, nightlife, activities, or nearby recommendations.
allowed-tools: Bash(bladebro:*)
---

# Activities Search with Bladebro

Use Google Maps as the primary discovery surface because it combines location, ratings, reviews, opening information and categories. Use the broader web only to verify details Maps does not establish reliably.

## Boundaries

- Research/recommend only. Do not complete reservations, ticket purchases or payment.
- Never fabricate opening hours, prices, reservation availability, age limits or attraction restrictions.
- Treat hours/availability as time-sensitive.

## Search strategy

Translate the request into 1–4 targeted Maps queries rather than one broad query.

Examples:

- `cocktail bars in Hell's Kitchen New York`
- `craft beer near Bryant Park New York`
- `best museums Washington DC`
- `adventure parks near Miami Florida`
- `BBQ restaurants Charleston South Carolina`

Google Maps URL:

```text
https://www.google.com/maps/search/?api=1&query={URL_ENCODED_QUERY}
```

For each query:

```bash
bladebro nav "$URL"
bladebro see extract auto --json
```

If the result feed is lazy-loaded:

```bash
bladebro act collect max=30 timeout=30 --json
```

Use `bladebro see content --json` or `bladebro see model --json` if structured extraction misses important fields.

## Evaluate candidates

Capture when visible:

- name
- category
- rating
- review count
- price level / explicit prices
- neighborhood/address cue
- opening status/hours
- distance/travel-time cue when shown
- standout review themes
- website/reservation/ticket link when relevant

Favor evidence quality over raw star rating. A 4.7 with 2,000 reviews generally carries more signal than a 5.0 with 8 reviews, but do not turn this into a rigid formula.

## Review synthesis

For finalists, open the place detail and inspect recent/relevant review text. Summarize recurring themes; do not quote long reviews.

Useful dimensions:

- restaurants: food quality, specific dishes, service, noise, value, dietary fit
- bars: cocktails/beer quality, atmosphere, seating, noise, queues
- sights/museums: time needed, crowding, must-see exhibits, advance tickets
- parks/adventure: duration, physical intensity, weather dependence, age/height restrictions if visible

## Geographic fit

When proximity matters, include the user's anchor in every search query. For multiple shortlisted places, use Maps directions or hand off to the `travel-search` skill for actual journey times.

## Fresh verification

For details that materially affect the plan, open the official site in a separate tab and verify:

- current opening hours/closure days
- ticket/reservation requirements
- official prices
- temporary closures
- age/height/access restrictions

Do this especially for attractions and adventure parks.

## Output

Default to 5 recommendations maximum:

| Place | Rating | Area | Best for | Watch-out |
|---|---:|---|---|---|

Then give one best-fit choice. For itinerary-like requests, group by neighborhood/area to minimize transit.

## Recovery

- Consent: handle normally.
- CAPTCHA/bot challenge: do not bypass.
- Map results hard to extract: switch to list/feed, use `collect`, then inspect finalists individually.
- Ambiguous city/place: resolve using the user's trip context or explicit location in the request; otherwise use the most geographically specific interpretation supported by the page.
