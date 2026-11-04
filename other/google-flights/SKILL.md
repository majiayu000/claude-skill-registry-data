---
name: google-flights-bladebro
description: Search Google Flights for live fares, schedules, stops, duration and booking-provider options using Bladebro. Use for flight searches, airfare comparisons, nonstop routes, schedules, cabin comparisons, or when to fly.
allowed-tools: Bash(bladebro:*)
---

# Google Flights Search with Bladebro

Use Google Flights through Bladebro. Prefer the natural-language Google Flights URL fast path for ordinary one-way/round-trip searches.

## Boundaries

- Research and compare only. Do not complete purchases or payment.
- Prices are live observations and may change.
- Do not claim baggage, seat-selection, change/refund, or fare-family terms unless explicitly visible.

## Fast path

Construct:

```text
https://www.google.com/travel/flights?q=Flights+from+{ORIGIN}+to+{DEST}+on+{YYYY-MM-DD}[+returning+{YYYY-MM-DD}][+one+way][+business+class][+N+passengers]
```

Examples:

```text
Flights from MIA to NAS on 2026-10-13 one way 2 passengers
Flights from CPH to JFK on 2026-09-26 returning 2026-10-18 2 passengers
Flights from JFK to CPH on 2026-10-18 business class 2 passengers
```

Navigate and inspect:

```bash
bladebro nav "$URL"
bladebro see extract auto --json
```

If auto-extract is not sufficient:

```bash
bladebro see content --json
bladebro see model --json
```

## Default cabin behavior

- If the user specifies a cabin, use it.
- If the user asks for cheapest/budget, use economy.
- Otherwise use economy by default. Do not automatically run a business-class comparison unless it is decision-relevant or requested.

## Interactive fallback

Use the interactive Google Flights form for:

- multi-city
- premium economy when the URL parser ignores it
- infants / complex passenger mix
- URL fast-path failures

Use accessible labels/text and Bladebro batching. Typical flow:

1. Navigate to `https://www.google.com/travel/flights`.
2. Configure trip type/cabin/passengers.
3. Fill origin and destination and select autocomplete suggestions.
4. Select dates.
5. Search.
6. Extract results.

Prefer `browser.act` semantics exposed through CLI commands (`bladebro act ...`) and use deltas rather than full snapshots after each change.

## Result fields

Capture:

- airline(s)
- departure/arrival airport and local time
- stops
- total duration
- overnight/+1 date cue
- displayed fare
- cabin if known
- Google labels such as Best/Cheapest when shown
- meaningful layover airport/duration when visible

Do not infer the operating carrier or fare rules from branding alone.

## Flexible-date searches

If the user asks "when is cheapest" or gives a range:

1. Use Google Flights date/price graph if exposed.
2. Compare a small number of promising dates rather than enumerating every date manually.
3. Report the date pair and displayed fare, plus the search timestamp context.

## Booking/provider handoff

When the user picks a flight:

1. Open the corresponding flight result.
2. Extract provider/airline booking options and prices.
3. Return links if Bladebro exposes hrefs.
4. Stop before purchase/account/payment actions.

## Output

Use compact numbered blocks rather than a wide table:

1. Airline — Nonstop · 3h 10m
   10:15 → 13:25 · DKK 1,240

Include 5–8 useful choices max unless the user asks for exhaustive results. End with one best-fit recommendation and why.

## Recovery

- Consent: dismiss/handle normally.
- CAPTCHA/bot challenge: do not solve or bypass; report it.
- No results: verify airport ambiguity and dates.
- Locale/currency mismatch: state the displayed currency.
- Stale UI/ref: rely on Bladebro self-healing refs; if needed use visible text or refresh `see model`.
