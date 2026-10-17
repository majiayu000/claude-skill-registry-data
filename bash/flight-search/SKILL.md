---
name: flight-search
description: Search Google Flights and monitor fares on tracked routes. Use when someone asks what a flight costs, when the cheapest day to fly is, or asks to be told when a fare drops. Also covers reading the daily flight-watch alert.
---

# Flight search

Eight tools over the `flights` package, which scrapes Google Flights. Available
as MCP tools (`search_flights`, `search_dates`, `search_flexible`, `plan_trip`,
`track_flight`, `check_prices`, `list_tracked`, `remove_tracked`) and as a CLI at
`$FLIGHT_SEARCH_PLUGIN_DIR/scripts/flight_tools.py`.

## The one rule

**An empty result is not an answer until the plugin proves the scraper is alive.**

Everything here scrapes a page Google can change without notice. When it breaks,
the natural symptom is an empty list, which is indistinguishable from "this
route has no flights" and from "the price did not move". So the tools never hand
back a bare empty result as success. You will get one of:

- `status: "ok"` - real priced itineraries in the currency that was requested
- `status: "empty"` - empty, and a live control-route query confirmed the
  scraper works, so the emptiness is real
- `status: "error"` with an `error_kind` - anything else

**Never translate an error into "no flights" or "no price change" when you
report to a human.** That is the single failure this plugin was built to
prevent. If `error_kind` is `scraper_error`, the honest sentence is "the flight
scraper is broken, so I do not know what that fare is doing".

## Searching

```bash
python3 "$FLIGHT_SEARCH_PLUGIN_DIR/scripts/flight_tools.py" search \
  --from LIS --to JFK --date 2026-09-09 --limit 5
```

Filters worth knowing: `--adults`, `--children`, `--cabin`, `--max-stops`,
`--airlines TP,AA`, `--max-price`, `--max-duration-minutes`,
`--max-layover-minutes`, `--depart-after 6 --depart-before 20`,
`--arrive-before 23`. `--from` and `--to` take comma-separated lists for
multi-airport searches (`--from LIS,OPO --to JFK,EWR`).

Flexible dates:

```bash
python3 "$FLIGHT_SEARCH_PLUGIN_DIR/scripts/flight_tools.py" dates \
  --from LIS --to JFK --from-date 2026-09-01 --to-date 2026-09-30
```

That returns a price per departure day plus `cheapest`, `dearest` and `spread`.
Use it before `search` whenever the dates are soft, and lead the answer with the
spread: "the 13th is 70 EUR cheaper than the 12th" is the useful sentence.

## Round trips and multi-city

Same command, different legs:

```bash
# round trip
python3 "$FLIGHT_SEARCH_PLUGIN_DIR/scripts/flight_tools.py" search \
  --from LIS --to JFK --date 2026-09-19 --return-date 2026-09-26

# multi-city, legs in travel order
python3 "$FLIGHT_SEARCH_PLUGIN_DIR/scripts/flight_tools.py" search \
  --leg LIS:PHX:2026-12-20 --leg PHX:SFO:2026-12-27 --leg LAX:LIS:2027-01-06
```

**The `price` on a result is the whole itinerary, not a leg.** Never add the
segment prices together and never quote `price_at_this_step` as a fare - those
are Google's running totals through its own selection flow. If you catch yourself
about to say "and the return leg is another 490", stop: the 490 was the trip.

Multi-leg searches are slow, roughly `top_n ** (legs - 1)` requests. A four-leg
trip takes a minute or two. Say that before starting one rather than going quiet.

## Soft dates at both ends

```bash
python3 "$FLIGHT_SEARCH_PLUGIN_DIR/scripts/flight_tools.py" flexible \
  --from LIS --to PHX --out-window 2026-12-20:2026-12-23 --back-window 2027-01-05:2027-01-08
```

Cheap: it sweeps trip lengths against Google's calendar grid, one request each.
Indicative prices, so follow up with `search` on a pair worth booking.

For a trip that has to touch several cities:

```bash
python3 "$FLIGHT_SEARCH_PLUGIN_DIR/scripts/flight_tools.py" plan \
  --from LIS --visit PHX,SFO,LAX \
  --out-window 2026-12-20:2026-12-23 --back-window 2027-01-05:2027-01-08 --nights PHX=6
```

`plan` picks candidate dates with the cheap grid and then prices real multi-city
itineraries for the best few. Every price it reports is a real search; the grid
only chose the dates. Cities are visited in the order given - if the order is
worth questioning, say so and offer to re-run rather than assuming.

It takes minutes. Ask before starting one, and never schedule it.

## Tracking

```bash
python3 "$FLIGHT_SEARCH_PLUGIN_DIR/scripts/flight_tools.py" track \
  --from LIS --to JFK --date 2026-09-09 --target-price 400 --label "NYC in September"
```

`--target-price` is required. It is the alert condition, and without one every
wobble in a volatile fare becomes a notification. If someone asks to "watch this
flight" without naming a number, ask for one - a sensible opening move is the
current cheapest fare minus ten percent.

Round trips and multi-city trips track the same way - add `--return-date` or
`--leg`. A multi-city route re-runs its full expansion on every check, so track
those sparingly and leave `top_n` at its default.

Alerts fire on transitions, not states: crossing the target, dropping further
below an already-alerted target, breaking, and recovering. A fare sitting below
its target all week is one alert.

The daily heartbeat runs `check_prices` for you. Run it by hand only when
someone asks right now, and expect the run to have polled Google once already
that day.

## Always hand over the link

One-way and round-trip results carry `query.search_url`, which re-runs the same
query on Google Flights. **Include it whenever you report a price.** It turns
"trust the scraper" into something the reader can settle in ten seconds, and it
is the difference between a number and a claim.

Also read `query.url_caveats`. It lists the filters the link cannot carry - cabin
class, passenger count, stop limits, hour windows and the rest. If it is
non-empty, say so when you hand over the link, because the browser page will not
be running the same filtered query and the numbers are allowed to differ.

Multi-city and multi-airport searches get no link, by design. For those, tell the
reader to open Google Flights, switch to Multi-city and enter the legs listed in
the result.

**Multi-leg prices read high and you must say so.** Every result carries
`price_confidence`. When it is `indicative_reads_high` there is also a
`price_warning` - pass its substance on, do not swallow it. Measured on
2026-08-10, a four-leg trip reported 1520 EUR while the site offered a bookable
1003 EUR fare for the same trip, a third lower. The cause is upstream and cannot
be configured away, so the right move is: give the number as a rough indication,
say a cheaper fare probably exists, and point at Google Flights.

When `price_confidence` is `matches_site` (one-way) you can state the number
plainly. It matched the site to the euro on both routes tested.

## Reporting a price to a human

Lead with the number and the currency. The currency is asserted against the
request, so it is trustworthy - say it explicitly anyway, because a price with
no currency is a number with no meaning.

Include: price, currency, airline, stops, total duration, departure time. Skip
the leg-by-leg breakdown unless asked. If the cheapest option is a fourteen-hour
routing through the Azores and the next one up is three hours shorter for
twenty euros more, say that - the cheapest row is not always the answer.

## What this plugin does not do

It does not book, hold, pay for or cancel anything. It searches and it watches.
When a fare is worth acting on, propose it and let the principal decide.
