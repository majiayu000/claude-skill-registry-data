---
name: verify-api
description: Compare provider DTOs and WireMock test payloads with live responses from the real public API (currently NBP), and capture real responses as test fixtures. Use when adding or changing DTOs, when a WireMock payload was hand-written, or when the API might have changed.
argument-hint: "[provider] [endpoint path or DTO name]"
---

# Verify DTOs against the live API

Goal: our DTOs and test payloads must match what the API really returns, so that a "passing" WireMock test means the client works in production.

## Steps

1. **List the endpoints to check.** Take the URL builders (`src/OpenUrzednik.Nbp/UrlBuilder/NbpUrlBuilderFactory.cs`, `NbpUrlBuilder.cs`) and the DTOs in `src/<Provider>/Dto/`. Narrow to `$ARGUMENTS` if given.
2. **Call the real API** with the read-only `curl -s` and `?format=json`. For NBP, cover:
   - every table (`a`, `b`, `c`) for both `exchangerates/tables/{t}` and `exchangerates/rates/{t}/{code}`
   - `cenyzlota`
   - each URL shape: latest, `last/{n}`, `today`, `{date}`, `{from}/{to}`
   - error cases: a future date, an out-of-range `last/{n}` (> 255), a date with no publication (weekend), a too-long range. Record the status code **and the body text** (NBP returns plain-text messages such as `400 BadRequest - Błędny zakres dat`).
   
   Keep the request count low: NBP is a public service, so don't loop or hammer it.
3. **Compare with the DTOs:**
   - A `required` property missing from any real response is a **bug**: deserialization will fail.
   - Report extra fields we ignore, type mismatches (number vs string, date formats) and casing.
4. **Compare with the WireMock tests** in `tests/OpenUrzednik.IntegrationTests/<Provider>/WireMock/`. Flag every hand-written body that differs in shape from the real one.
5. **Capture fixtures** when asked, or when fixing a mismatch: save real bodies under `tests/OpenUrzednik.IntegrationTests/<Provider>/Fixtures/<endpoint-shape>.json` (trim long arrays to 2–3 items, keep the real structure) and load them in the WireMock tests instead of inline JSON.
6. **Report** a table: endpoint | status | fields in response | DTO verdict (OK / missing required / extra / type mismatch) | test payload verdict. List the limits you observed (max `last/{n}`, max date range, earliest date) next to the values used in `Validation/`.

Don't change validators based on one observation without saying so: point out differences from the documented limits and let the maintainer decide.
