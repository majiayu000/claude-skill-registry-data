---
name: browser-cron-sweeps
description: >-
  Use when cron sweeps drive browsers against anti-bot sites.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cron, browser, cdp, playwright, anti-bot, captcha, sweep, legal-watchdog, fast-fail]
    triggers: [browser sweep, cron browser, wyobiz, TSPD, postback hang, concurrent cron, shared browser backend, anti-bot wall]
    related_skills: [hermes-legal-watchdog, recurring-status-checks, captcha-bypass-browsers, cron-watchdog]
---

# Browser Cron Sweeps — Shared Backends, Anti-Bot Walls, Fast-Fail

Recurring cron jobs (legal sweeps, compliance calendars, background checks, reputation monitors) frequently need to drive browser backends against government portals and data-broker sites. This skill captures the cross-cutting realities of doing that from cron context.

## Concurrent Cron Jobs Share Browser Backends

When multiple cron sweeps fire in the same window (observed: daily legal sweep + weekly background sweep + compliance calendar all launching together), they share the SAME Chrome DevTools MCP and Playwright MCP instances. This is not a failure of any one job — it is the steady state.

**Symptoms:**
- `new_page` / `navigate` returns "browser was restarted or reconnected since the last call"
- Page IDs silently shift or vanish between calls ("No page found")
- Your snapshot shows another job's pages (DDG searches, court portals, county appraiser sites)
- `select_page` succeeds but the next snapshot is a different tab

**Mitigation:**
1. Re-list pages and re-select your tab before EVERY snapshot — never assume the last selection held
2. Run fill → click → evaluate as ONE tight sequence with no unrelated calls in between
3. Use `evaluate_script` (main world) for state checks rather than snapshots where possible
4. If the browser keeps getting restarted, fast-fail the interactive check and fall back to API/curl sources or mark the source UNREACHABLE. Do NOT retry the same rung expecting a different result.

## Anti-Bot Wall Fast-Fail Signatures

Not every block is a CAPTCHA. Identify the wall type from the response and fast-fail accordingly — grinding on a blocked source wastes the whole sweep.

| Wall | Signature | Response |
|------|-----------|----------|
| **Imperva / TSPD** (e.g. `wyobiz.wyo.gov` via curl) | ~45KB page, `window["bobcmn"] = "..."` script containing a `/TSPD/` marker, no `<title>`, no form/viewstate | Fast-fail curl — no viewstate extraction possible. Real browser backend only. |
| **PWH-Alert / "abusive automated request"** (e.g. `ftc.gov` via curl) | Block page with apology text | Fast-fail curl; use Federal Register API or CDP browser |
| **ASP.NET postback hang** (e.g. WY SOS FilingSearch) | Form fills correctly, Search triggers a "Loading..." spinner that never resolves; `[id*=UpdateProgress]` visible | SITE-SIDE, NOT backend-specific — Playwright hits the identical hang as CDP. Do not burn turns switching browser backends. Reload + retry once, then mark UNREACHABLE and use fallback (web_search `site:` query, API, or manual human check) |
| **DuckDuckGo dual CAPTCHA** | Lite AND HTML both show the duck puzzle | Same bot-detection backend — fast-fail DDG entirely, switch engines |

## Fallback Ladder (browser unavailable or blocked)

1. **Playwright MCP** — independent backend; use when CDP is down or profile-locked. Note: it shares the same "concurrent cron" contention, and site-side hangs (ASP.NET postback) affect it identically.
2. **Federal Register API via curl** — `federalregister.gov/api/v1/articles.json` — the single most productive path when all browser backends are unavailable. Bypasses CAPTCHAs, returns structured JSON. MSYS note: URL-encode square brackets as `%5b`/`%5d`.
3. **web_search `site:` queries** — e.g. `site:sos.wyo.gov "the company" LLC` — often returns nothing indexed for ASP.NET state portals; don't treat empty results as proof of absence.
4. **Manual human check** — mark UNREACHABLE and recommend a human-operated browser.

## Cron-Context Report Patterns

- If the sweep produced a real report, deliver it with the blocked sources explicitly listed (source + block type).
- If the sweep is a compliance calendar and the entity status is unverifiable, report `🟡 NOT VERIFIED` with the block reason and a manual-check recommendation — do not fabricate an ACTIVE status.
- Before burning turns on a blocked state portal, check local repo records first (e.g. `legal-team/counsel/calendar/filing-calendar.md` for a documented Filing ID or formation date) — if the due date is computable offline, the site check becomes optional verification.

## Pitfalls

- **Don't fight siblings.** Concurrent cron jobs sharing browser backends is expected; adapt with re-list/re-select, not retries.
- **Don't blame the backend for a site-side hang.** If CDP and Playwright both hang the same way, it's the site. Verify with one alternate backend max, then move on.
- **Don't parse TSPD/Imperva pages.** No viewstate, no form — there is nothing to extract.
- **Don't treat "no indexed results" as "entity doesn't exist."** State portals' ASP.NET search apps are typically not indexed by search engines.
- **Don't report unverified entity status as ACTIVE.** Mark it NOT VERIFIED with the block type.
