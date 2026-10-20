---
name: research-appliance
description: Research an appliance's running watts, start surge and duty cycle, then add or update it in the solar-dimension catalog through the token-protected API after the user confirms. Use for "/research-appliance <description>" or "add <appliance> to the catalog".
---

# Research an appliance into the catalog

Arguments: `<description> [--target local|prod]` (default `local`).

## Setup
- Never `cat`, `Read`, `rg` or otherwise print any `.env*` file: `.env.local` holds the token and the production database URL. Shell variables and functions don't survive between commands, so start every command that calls the API with this line. It reads the token, stops if the token or the address is missing, and defines `api`: a `curl` that sends the token and always ends with the HTTP status on a line of its own.
  ```bash
  TOKEN=$(sed -n 's/^CATALOG_API_TOKEN=//p' .env.local | tr -d '"') && BASE=http://localhost:3000 && : "${TOKEN:?CATALOG_API_TOKEN is not in .env.local}" "${BASE:?CATALOG_API_URL is not in .env.local}" && api() { curl -sS -m 30 -w '\n%{http_code}\n' -H "Authorization: Bearer $TOKEN" "$@"; }
  ```
  For `--target prod`, put `BASE=$(sed -n 's/^CATALOG_API_URL=//p' .env.local | tr -d '"')` in place of `BASE=http://localhost:3000`.
- Read the status before the body, every time:
  - `000`: no server answered on that target. Say so and stop. After the write in step 6 it means you don't know whether the write landed: say that, and run the dry run again to see.
  - No status at all, and the shell names a key that is not in `.env.local`: tell the user which key and stop. Do not open the file to look.
  - A status this skill does not list is not a success. Before the write, stop and tell the user. After the write in step 6, treat it like `000`.
- Never print, echo or log the token or any database URL. Pass the token only through `api`.

## Which database a target writes to
`--target` picks the server, not the database: a server writes to the database it was started with. `.env.local` points at the **production** database, and `vercel env pull .env.local` keeps restoring that, so a local server started from it (`npm run dev`, `npm run start`) writes to production. Only a server started on another Neon branch does not.

Before the first API call, ask the server you are about to write to:
```bash
api "$BASE/api/catalog/database"
```
A `200` answers `{"endpoint":"ep-…","environment":"…"}`: the Neon endpoint id of the server's database (an id, not a credential) and what the server can say about it. That decides what you tell the user, in the table you show them and again in the question you ask before writing:
- `"environment":"production"`: "this writes to PRODUCTION".
- `"environment":"test"`: "this writes to the test database `<endpoint>`, not production". The server says this only for the endpoint in `TEST_DB_ENDPOINT`, which the e2e guard sets after checking the database (`node scripts/start-on-test-db.ts` starts such a server). The item still has to go to prod separately (`--target prod`) to reach real users.
- `"environment":"unknown"`, or any value not listed here: "this writes to `<endpoint>`, a database the server cannot vouch for: treat it as PRODUCTION". It is not the production endpoint the app knows, but nothing checked it.
- Anything else, that is any status but `200`, or a `200` without an `endpoint`: stop. Nothing is written through a server that does not name its database, and no POST can succeed without that name. Tell the user what it answered: 401, the token is not the one that server was started with; 404, the API is disabled there or the server runs a build from before this route; 429, too many requests with a wrong token from this address, wait ten minutes; 500, the server cannot read its own database setting.

Every POST, the dry run and the write, carries `-H "X-Expect-Database: <endpoint>"`. Type the id into the command itself, never through a shell variable: curl drops a header whose value is empty, and the server refuses a POST without it (428). A server that is no longer on that database (it was restarted, or another one took the port) answers 412 and does nothing. Then the dry run and the user's yes are void: show the `database` in the answer and start again from this section (ask, check for duplicates, dry run, table, a new yes). The id in the header is always the one in the answer you showed the user, never one taken from a 412.

That request is the only way to learn the database. Never read `DATABASE_URL` from an env file and never inspect the server's process (`ps`, `lsof`): the first prints production credentials, and neither shows what the running server uses.

With `--target prod` the answer should be `"environment":"production"`. If the server names its database as anything else, stop and tell the user: either `CATALOG_API_URL` is not the production site, or the production database moved and `PRODUCTION_DB_ENDPOINT` in `src/lib/db-endpoint.ts` is out of date.

## Steps
1. **Research** typical values for the described appliance (one row per distinct size or type the user asked for):
   - `watts`: typical running watts (integer).
   - `surge`: start surge in watts (integer, ≥ watts). Resistive loads (heaters, stoves, kettles) have surge = watts; motors and compressors are 2–3×; inverter compressors ~1.3×.
   - `duty`: share of each hour it draws power while in use (0 < duty ≤ 1). Match the existing items: fridge 0.35, microwave 0.08, water heater 0.25.
   - `kind`: `continuous` (duty 1), `cycling` (turns on and off: fridges, AC, heaters) or `momentary` (runs for seconds at a time: gate motors, barriers, garage doors). `null` lets the engine derive it from the duty (1 → continuous, else cycling), so only set it for momentary items or to override.
   - `surgeClass`: how long the start-up lasts: `inrush` (electronics, ~20 ms), `motor` (~1 s: pumps, fans, gates, inverter AC), `compressor` (~3 s: fridges, freezers, conventional AC). `null` lets the engine derive it from the compressor type and the surge ratio; set it when the appliance is unusual. It must be `null` when surge equals watts.
   - Momentary items only: `burstSeconds` (seconds per run, ≤ 600) and `cyclesPerHour` (runs per hour, ≤ 120), with burst × cycles ≤ 3600. The engine uses burst × cycles ÷ 3600 as the duty; set `duty` to that figure too (it is what the admin table shows). Both must be `null` for every other kind.
   - Keep one source (URL or datasheet) for each number.
2. **Write labels** in the same tone as the existing items: EN and ES `name` (short, with size if it matters, e.g. "Induction cooktop, 2 burners") and `note` (how it cycles, e.g. "~10 min per hour of cooking"). Spanish is Latin American.
3. **Check for duplicates:** `api "$BASE/api/catalog/appliances"`. Reuse an existing id if the item is already there (that makes it an update). Otherwise make an id with lowercase letters, digits and dashes, 2-48 characters, starting with a letter or digit. Ids shaped like `custom1`, `custom2`, … are reserved for the app's own custom loads and are always rejected.
4. **Dry run:** write a JSON array of items to a file in the session scratchpad, then `api -X POST -H "X-Expect-Database: <endpoint>" -H 'Content-Type: application/json' --data @<file> "$BASE/api/catalog/appliances?dryRun=true"`. Items are shaped `{ id, category, watts, surge, duty, tons: null, acType: null, kind: null, surgeClass: null, burstSeconds: null, cyclesPerHour: null, labels: { en: {name, note}, es: {name, note} } }`. Category is one of Kitchen, Living, Climate, Air conditioning, Work, Utility, Security, Personal. The four load-kind keys may be omitted (they default to null); see step 1 for when to set them.
   - For category `Air conditioning`: `tons` (a positive number) and `acType` (`inverter` or `conventional`) are required, not null.
   - For every other category: `tons` and `acType` must both be `null`. The API rejects a request that sets either field outside Air conditioning, or that omits them for it.
5. **Show the user a table:** id, new or changed (with old → new), EN name, ES name, watts, surge, duty, kind and surge class when set (with burst seconds × cycles per hour for momentary items), and the source for each number. Mention any item of 3 kW or more (the app flags it as needing a 240 V split-phase inverter).
6. **Wait for an explicit yes** to a question that says where the write goes (see "Which database a target writes to"). Then send the same file with the same headers to `"$BASE/api/catalog/appliances"` and report `created` / `updated`. An answer with `changes` instead means the dry run was sent again: nothing was written.
7. **On errors:** 422 → show the per-item issues, fix, and repeat from step 4. 400 → a query parameter other than `dryRun`, one not exactly `true` or `false`, or one given twice (`error` names it); nothing was written, fix the URL and repeat from step 4. 412 → the server is not on the database you named: it did nothing, and the dry run and the yes are void (see "Which database a target writes to"). 428 → the POST named no database: send it again with the header, using the id in the answer you showed the user. 401 → the token is not the one that server was started with (this skill reads `CATALOG_API_TOKEN` from `.env.local`). 404 on any route but `/api/catalog/database` → the API is disabled on that target (`CATALOG_API_TOKEN` unset there). 429 → too many requests with a wrong token from this address; wait ten minutes. 500 → database error; report and ask the user to retry.
