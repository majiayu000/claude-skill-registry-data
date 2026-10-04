---
name: dining-places
description: >
  Turns a user's exported Google Maps saved places (starred places + custom
  Lists from a Google Takeout "Saved" + "Maps" export) into a personal dining
  knowledge base, then gives eating-out advice that (1) surfaces relevant places
  they already saved, (2) infers their taste, and (3) supplements with fresh
  web/Places research — clearly labelling what is "yours" vs "new", plotting
  results on a map, summarising them in a comparison table, and offering a
  booking link per place. Use whenever the user asks where to eat / drink, for
  restaurant or bar recommendations, for somewhere near a location, or references
  their saved places / want-to-go list / starred spots. Works at home and while
  travelling. Trigger phrases: "where should I eat", "dinner rec", "good
  restaurant near", "from my saved places", "my want to go list", "somewhere for
  drinks", "book a table", "what's good in this area", "use my saved spots".
---

# Dining-Places Skill

A personal dining knowledge base built from a user's Google Maps export, used to
give calibrated eating-out advice.

Data source: a **Google Takeout** export (categories **Saved** + **Maps**)
delivered to the user's Drive `My Drive/Takeout` folder, typically on a recurring
schedule. The data arrives as one or more `.zip` archives (e.g.
`takeout-…-001.zip`, `…-002.zip`) — the CSV/JSON files live *inside* the zips and
the parser reads them directly (no manual unzip needed).

> Reality check: Google has **no API** for personal saved places. Takeout is the
> only route, and the saved data contains place **name + list + note + URL**, plus
> coordinates/address **only** for individually-saved places. Cuisine, rating,
> price, and hours are added at advice-time via a Places search tool.

---

## The two data sources (read both)

A Takeout export contains **two different structures**, and they barely overlap —
you must use both:

| Source | What it is | Coordinates? |
|---|---|---|
| `Maps (your places)/Saved Places.json` | Individually saved / starred places (GeoJSON) | ✅ Yes, + address |
| `Saved/<List name>.csv` (one CSV per List) | Lists — Favourites, **Want to go**, **To visit**, custom lists | ❌ No (Title, Note, URL, Tags only) |

**Critical consequence:** a neighbourhood/geo filter ("places in a given neighbourhood") only
works on rows that have coordinates. The List CSVs usually have none, so the
large "Want to go" / "To visit" lists are **invisible to a location search**
unless you enrich them first. For a location-scoped request:

1. Geo-filter the coordinate-bearing places directly.
2. For List places with no coordinates, resolve them via the Places search tool
   (name + any note/address) to attach coordinates, **then** geo-filter — so both
   sources feed the result.

The included parser (`scripts/parse_takeout_maps.py`) reads both the GeoJSON and
the List CSVs and supports both the current (lowercase) and legacy (Title-case)
Takeout GeoJSON schemas.

---

## Runtime — where this works best

| Environment | Can it run? | Notes |
|---|---|---|
| Agentic / code-execution environment | ✅ Full | Downloads every zip in `My Drive/Takeout`, writes bytes to disk, parses. Preferred. |
| Plain chat | ⚠️ Partial | The Drive download tool returns base64; small exports work, larger ones are clunky. Download the zips locally and run the parser there if needed. |

---

## Step-by-step workflow

### Step 1 — Get the latest export (zips in Drive)
1. List the `My Drive/Takeout` folder, newest first, and read each file id.
   (Newly-delivered files can lag in search; if a zip is missing, ask the user
   for its share link and read the id from `…/file/d/<id>/view`.)
2. Download **every** zip from the newest export (there may be `-001`, `-002`, …)
   and write each to a working folder. Keep them together.
3. If a cached `references/saved_places.json` snapshot exists and no newer export
   is present, use the snapshot (fast path).

### Step 2 — Parse into the knowledge base
Point the parser at the folder of zips (it extracts each internally and merges
them; no manual unzip, no `Saved/` folder required):
```bash
python3 scripts/parse_takeout_maps.py <folder> --out references/saved_places.json --dedupe
# or a single archive:  python3 scripts/parse_takeout_maps.py <archive>.zip
```
This merges every List CSV + the saved-places GeoJSON into one normalized list:
`name, source_list, note, address, lat, lng, maps_url`. Cache the result.

### Step 3 — Match the request to saved places (use BOTH sources)
Filter the knowledge base by the location in the request (home neighbourhood, or
the city being travelled to). Coordinate-bearing places (the starred GeoJSON)
filter directly. **List places have no coordinates and must be enriched, or they
are silently excluded** — this is the single most common failure mode, so do not
skip it.

Procedure for a location-scoped request:
1. **Geo-filter** the coord-bearing places against the target area (fast, free).
2. **Select** coord-less List places worth resolving: pre-filter by name/note
   keywords against the request (cuisine, vibe, list relevance) so you resolve a
   small candidate set, not all of them.
3. **Resolve** that candidate set via the Places search tool, **location-biased to
   the target area**, to attach `lat`/`lng` (and rating/cuisine/price for free).
4. **Keep** the ones that fall inside the area; merge with step 1.
5. **Cache** every newly-resolved `lat`/`lng` back into `references/saved_places.json`
   so each place is looked up at most once — the snapshot self-completes over time.

If, after enrichment, few/no saved places match (common when travelling), say so
plainly and lean on Step 4.

> **Optional one-time backfill:** if you want every List place searchable
> immediately rather than lazily, run a build-time geocoding pass over all
> coord-less rows (requires a Maps/Places API key) and write the coordinates into
> the snapshot. If you create a key, restrict it: API restriction = Geocoding API
> (+ Places API if resolving by name), application restriction = None or your IP.
> The lazy approach above needs no key and converges to the same place.

### Step 4 — Enrich + supplement (saved-first, then widen, taste-calibrated)
1. **Surface saved matches first**, enriched with current detail via the Places
   search tool (rating, cuisine, price, area, opening status, a maps link).
2. **Infer a taste profile** from the saved set (cuisines, neighbourhoods, vibe)
   — keep it to ~1 line.
3. **Widen with fresh recommendations** that fit that profile, found via Places /
   web search (recent, well-reviewed), excluding anything already saved.
4. **Always label provenance**: ⭐ Saved vs ✨ New.

### Step 5 — Respond (default output: map + table + booking links)
Lead with the bottom line, then detail by importance. Default to:

- **A map** of the candidates via the map-display tool, each pin tagged ⭐ Saved /
  ✨ New with a one-line note.
- **A comparison table**: name, ⭐/✨, cuisine, current rating, price, why.
- **A booking route per place**: prefer a direct reservation link (the venue's own
  page, or a reservation platform that lists it). If a reservation **connector**
  is connected *and* lists the venue, offer to book — but always confirm
  place / date / party size before submitting, and never auto-submit silently.

Adapt the body to the ask:

| Request shape | Body format |
|---|---|
| "where should I eat near X" | bottom line + short ranked list, ⭐/✨ tags, map, table, booking links |
| "compare these / shortlist" | comparison table (+ map) |
| "plan an evening / area crawl / trip" | a map in itinerary mode |
| quick single ask | 2–3 sentences, one clear pick + a backup |

---

## Booking notes

- Most independent / neighbourhood restaurants book through **their own website**
  or a platform like Dish Cult, SevenRooms, Tock, OpenTable, or Resy. Coverage
  varies a lot by country and city — verify with a quick search before claiming a
  venue is on any given platform.
- Reservation platforms with thin coverage in a given area (e.g. Resy outside its
  core cities) frequently **don't list neighbourhood spots** — fall back to the
  venue's own booking page rather than forcing a platform widget.
- Booking is a side-effecting action: confirm the exact details with the user and
  let them complete any login / final submit.

---

## references/

- `saved_places.json` — cached normalized snapshot (rebuilt when a newer export
  lands). **Personal data — git-ignored; never commit.**
- `known_ids.md` — optional local cache of the Drive `Takeout` folder id.
  **Personal data — git-ignored; never commit.** See `*.example` templates.

## Script reference — `scripts/parse_takeout_maps.py`

| Flag | Description |
|---|---|
| `folder` (positional) | A Takeout `.zip`, a folder of zips, or an extracted folder; searched recursively, zips auto-extracted |
| `--out PATH` | Write normalized JSON (else stdout); prints a per-list count summary |
| `--dedupe` | Drop duplicate place names (keep first) |
