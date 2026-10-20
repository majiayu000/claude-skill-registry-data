---
name: research-product
description: Research inverters or batteries from their makers' datasheets and add or update them in the solar-dimension product library through the token-protected API after the user confirms. Use for "/research-product <models | a need | --from file>" or "add <inverter or battery> to the product library".
---

# Research products into the library

Arguments: `<what> [--target local|prod] [--replace]` (default target `local`).

`<what>` is one of:
- **Named models**, e.g. `EG4 6000XP, Pytes V5`: research exactly these.
- **A need**, e.g. `48 V inverter, ≥ 6 kW, split-phase`: search for current models that meet it, pick up to 4 whose maker publishes a datasheet, show the list, then research each.
- **`--from <file.json>`**: a saved search run. Take its products from the JSON's `inverters` and `batteries`; in a spike `--out` file they are in the `output` item of type `message`, in its `output_text` content, whose `text` is a JSON string to parse. Use only `brand`, `model`, `productUrl` and `datasheetUrl` as leads; never copy a run's specs or other keys across (its `productUrl` is not necessarily the maker's page). Research each product again from its datasheet.

Research with Claude Code's own web search and fetch. Never run `scripts/product-search/spike.ts` or any other paid AI API.

## Setup
- Never `cat`, `Read`, `rg` or otherwise print any `.env*` file: `.env.local` holds the token and the production database URL. Shell variables and functions don't survive between commands, so start every command that calls the API with this line. It reads the token, stops if the token or the address is missing, and defines `api`: a `curl` that sends the token and always ends with the HTTP status on a line of its own.
  ```bash
  TOKEN=$(sed -n 's/^CATALOG_API_TOKEN=//p' .env.local | tr -d '"') && BASE=http://localhost:3000 && : "${TOKEN:?CATALOG_API_TOKEN is not in .env.local}" "${BASE:?CATALOG_API_URL is not in .env.local}" && api() { curl -sS -m 30 -w '\n%{http_code}\n' -H "Authorization: Bearer $TOKEN" "$@"; }
  ```
  For `--target prod`, put `BASE=$(sed -n 's/^CATALOG_API_URL=//p' .env.local | tr -d '"')` in place of `BASE=http://localhost:3000`.
- Read the status before the body, every time:
  - `000`: no server answered on that target. Say so and stop. After the write in step 7 it means you don't know whether the write landed: say that, and run the dry run again to see.
  - No status at all, and the shell names a key that is not in `.env.local`: tell the user which key and stop. Do not open the file to look.
  - A status this skill does not list is not a success. Before the write, stop and tell the user. After the write in step 7, treat it like `000`.
- Never print, echo or log the token or any database URL. Pass the token only through `api`.
- Before the first API call, follow "Which database a target writes to" in `.claude/skills/research-appliance/SKILL.md`. It applies to this skill as written: you ask the target itself which database it writes to, and it tells you what to say to the user, what every POST must carry and when to stop. Never look for the database in an env file or in the server's process.

## Steps
1. **List the products** to research (see `<what>`). At most 50 per request, each product once.
2. **Find each one's datasheet** on the maker's site and fetch it. A PDF fetch saves the file and reports its path: `Read` that path with `pages` and read the spec table itself. Take no number from a summary, a reseller page when the datasheet states it, or a similar model. No datasheet found, or it won't load or has no readable table: drop the product and say why.
3. **Fill one item per product** (shape below). Every spec is `{ value, source, asWritten }`:
   - `value`: a number in W, V, A, s, Ah, kWh, %, years, cycles or units; `splitPhase` is `true` or `false`; `chemistry` is `lifepo4`, `agm` or `other`. `source`: the https URL you read it on. `asWritten`: the datasheet's own words for it, copied (at most 200 characters).
   - Not stated: all three `null`. Never estimate, convert from a similar model or fill a typical value.
   - `surges`: every surge or overload level, shortest first, each `{ w, seconds, asWritten, source }`. "12,000W for ≈3.5 s | 11,000W for ≈5 s" is two levels. "2× Pn, 5 s" gets `w` = 2 × the stated rated power. A level in VA only gets `w: null`; a level with no duration gets `seconds: null` (never 0). No level stated: `surges: []`.
   - Battery `nominalV` as written (51.2), not the system class (48).
   - `bmsComms`: the protocols the datasheet names (`can`, `rs485`). Compatible brands (at most 30): only those the maker lists.
   - `extraSpecs`: up to 8 more lines an installer would check, as written (`name` ≤ 60, `value` ≤ 200 characters), each name once whatever its case ("Weight" and "weight" are one line; two are refused): transfer time, IP rating, operating temperature, dimensions, weight, the maker's depth of discharge.
   - `price`: `null`, unless you saw it on a seller's page; then `{ "amount": 1199, "currency": "USD", "seller": "…", "url": "https://…", "seenOn": "YYYY-MM-DD" }` with today's date. Never search for prices.
   - `brand` ≤ 60 and `model` ≤ 80 characters.
4. **Check for duplicates:** `api -o <file> "$BASE/api/catalog/products"` saves the answer to a file in the session scratchpad and prints only the status; on `200`, list them with `jq '.items[] | {key, brand, model, retired}' <file>`. If the product is there under another spelling, use the stored `brand` and `model` exactly. A `retired` product stays retired after a write; say so.
5. **Dry run:** write the JSON array of items to a file in the session scratchpad, then `api -X POST -H "X-Expect-Database: <endpoint>" -H 'Content-Type: application/json' --data @<file> "$BASE/api/catalog/products?dryRun=true"` (add `&replace=true` with `--replace`). `<endpoint>` is the id from "Which database a target writes to". The only query parameters are `dryRun` and `replace`, each exactly `true` or `false` (absent is `false`). Each change has `key`, `status` (`new`, `updated`, `conflicts`, `unchanged`) and:
   - `fills`: fields that were null and get a value;
   - `replaced`: `{ field, stored, found }` for each value overwritten. With `--replace` it is any stated value; without it, only `price`: a different price always replaces the stored one (a first price is a `fills` entry);
   - `cleared`: fields whose stored conflicts this write settles;
   - `conflicts`: `{ field, stored, found }` for each differing value kept aside;
   - `dropped`: `extraSpecs.<name>` for each new extra line not stored because the product already holds 8. The status does not change.
6. **Show the user** one table per product: its status and key; every stated spec with value, `asWritten` and the source's host; then fills, cleared, conflicts (stored → found), every `replaced` entry as stored → found (a changed price shows here even without `--replace`) and every `dropped` line (not stored: the product already has 8 extra lines). Flag: a VA-only or duration-less surge, no parallel limit, any stated value missing `asWritten`. Say where the write goes, in the table and in the question, in the words "Which database a target writes to" gives for the server's answer.
7. **Wait for an explicit yes.** Then send the same file with the same headers to `"$BASE/api/catalog/products"` (or `?replace=true` with `--replace`) and report `created`, `updated`, `unchanged` and `conflicts`. An answer with `changes` instead means the dry run was sent again: nothing was written. A product can be in `updated` and in `conflicts`: it was filled or changed and also read a differing value. Conflicts are kept on the product for review. `--replace` overwrites them; re-sending the stored value with `--replace` keeps it and clears that field's conflicts (`cleared`). Every product sent again, changed or not, has its `last_seen_at` moved.
8. **On errors:**
   - 400: a query parameter other than `dryRun` or `replace`, one not exactly `true` or `false`, or one given twice (`error` names it). Nothing was written; fix the URL and repeat from step 5.
   - 422: show the per-item issues (index and dotted path). Re-read the datasheet and fix the item; never change a value or its words just to pass a limit. Repeat from step 5. Two items with one key are refused as "the same product twice".
   - 409: a stored product with that key no longer passes the schema (`keys` lists them). Nothing was written; report it, the stored row needs fixing first.
   - 412: the server is not on the database you named. It did nothing, and the dry run and the yes are void: start again from "Which database a target writes to", then repeat steps 4 to 7.
   - 428: the POST named no database. Send it again with the header, using the id in the answer you showed the user.
   - 401: the token is not the one that server was started with (this skill reads `CATALOG_API_TOKEN` from `.env.local`). 404 on any route but `/api/catalog/database`: the API is disabled on that target (`CATALOG_API_TOKEN` unset there). 429: too many requests with a wrong token from this address; wait ten minutes. 500: database error; report it and ask the user to retry.

## Item shape

Inverter:
```json
{ "kind": "inverter", "brand": "EG4 Electronics", "model": "6000XP",
  "makerUrl": "https://…", "datasheetUrl": "https://….pdf", "price": null,
  "extraSpecs": [{ "name": "Transfer time", "value": "<15ms @ Single / <30ms @ Parallel", "source": "https://….pdf" }],
  "specs": {
    "continuousW": { "value": 6000, "source": "https://….pdf", "asWritten": "NOMINAL POWER OUTPUT 6000W" },
    "surges": [{ "w": 12000, "seconds": 3.5, "asWritten": "12,000W for ≈3.5 seconds", "source": "https://….pdf" }],
    "batteryVolts": {…}, "splitPhase": {…}, "chargerA": {…}, "pvInputW": {…}, "pvVocMax": {…},
    "maxParallelUnits": {…}, "idleW": {…}, "peakEfficiencyPct": {…}, "warrantyYears": {…},
    "bmsComms": ["can", "rs485"], "compatibleBatteryBrands": [] } }
```

Battery: the same top level with `"kind": "battery"` and
```json
"specs": { "chemistry": {…}, "nominalV": {…}, "ah": {…}, "kWh": {…}, "maxContinuousA": {…}, "peakA": {…},
  "peakSeconds": {…}, "maxParallel": {…}, "cycleLife": {…}, "warrantyYears": {…},
  "bmsComms": [], "compatibleInverterBrands": [] }
```
Every `{…}` is `{ "value", "source", "asWritten" }`. All keys are required; unknown keys are refused.
