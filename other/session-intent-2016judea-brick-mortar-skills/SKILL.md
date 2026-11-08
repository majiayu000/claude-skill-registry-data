---
name: session-intent
description: Answer "how are people using <site>", "what are visitors doing on <page>", "why is nobody downloading/copying/signing up", "watch the recordings for X", "where do people drop off" for a site that runs PostHog. Score every session against what the page is FOR (an intent spec with file:line per step), then name the step people fail at, the evidence with replay links, and the code change. Use instead of PostHog's AI summaries or reading raw recordings one by one.
---

# session-intent

The idea: you own the page's source, so you know what each visitor was *supposed* to do.
Write that down as an ordered intent spec, then score every PostHog session against it.
The output is one finding: the step people fail at, the counts, two replay links, and the
fix. Under 200 words.

## The pipeline (build it as a small script)

1. **List hosts/pages with sessions** (HogQL over `events` grouped by `$host`, `$pathname`).
2. **Pull sessions for one page** over N days, with their events and, where they exist, the
   recording snapshots.
3. **Score each session** step by step against the intent spec (below): reached, missed, or
   `unknown`.
4. **Summarise** with counts computed in code, then let a model write the finding from the
   counts and a few exemplar sessions. **The model never writes a number**: counts come from
   the scorer and are printed by code.

## Writing an intent spec (`sites/<slug>/intent.json`)

Derive it from the SOURCE; don't ask the site owner.

1. Find the template or generator, not the built HTML. Pin `source_commit` with
   `git rev-parse --short HEAD`.
2. `job`: one sentence, in the visitor's words, naming who it was made for.
3. Steps in order: land -> see the thing -> (optional narrow) -> take it / act on it.
   `success` is the step that means the job got done. Each step's `source` names `file:line`,
   and includes the **layout CSS lines** too (the grid and its media query). Without them a
   model will propose a DOM move that breaks desktop.
4. `match` alternatives per step. Find which custom events the page sends: grep `send('` /
   `posthog.capture` and any shared tracker. Kinds: `pageview`, `event` (+`prop`, `min` /
   `equals` / `contains`), `scroll_px` (rrweb scrollY), `click` (substring of
   `tag#id.class "text"`), `input`.
5. Measure positions at the visitor's real viewport with headless WebKit (e.g. 393x659):
   first row top, CTA top, document height. Put them in `measured_at`. A scroll step's
   `scroll_px` threshold = element top minus one viewport, plus a little.

```json
{"slug": "pricing-page", "url": "https://example.com/pricing/", "source_commit": "abc1234",
 "job": "A shop owner checks what the plan costs and starts a trial.",
 "measured_at": {"viewport": "393x659", "cta_top": 1420, "doc_height": 3900},
 "steps": [
  {"id": "land", "match": [{"kind": "pageview"}], "source": "templates/pricing.html:1"},
  {"id": "see_price", "match": [{"kind": "scroll_px", "min": 800}], "source": "templates/pricing.html:42, static/site.css:118-131"},
  {"id": "start_trial", "success": true, "match": [{"kind": "event", "name": "trial_click"}, {"kind": "click", "contains": "Start trial"}], "source": "templates/pricing.html:77"}
 ]}
```

## Rules (each one cost a cycle)

- **Scroll % is meaningless on long pages.** On a 100k-px list, 3,785px scrolled reads as
  `max_depth 0`. Use `scroll_px` or an in-list interaction with `"decides_miss": false`.
  Never use a % event alone.
- **`filterTestAccounts` does not catch QA bots.** Drop bursts (3+ distinct ids, one device
  profile, within 120s) and print a `left out:` line before quoting a count.
- **Check the device count before calling it a crowd.** 18 sessions can be one iPhone
  reopening a restored Safari tab (every replay opens at the same scrollY and hides in 0.2s).
  Never guess who a visitor is; describe the device and the pattern.
- **Verify the model's fix before reporting it**: inject the CSS or JS into the live page
  with Playwright `add_style_tag` at 393 AND 1440 width, and measure. Verify its tap claims
  against the cached session JSON. Models tend to understate counts.
- Most sessions may have no recording (lazy-loaded recording). Events-only steps are scored
  `unknown` unless an instrumented event can decide them.
- Never edit the site from this skill without the owner's word. Report the fix.

## PostHog API traps

- Snapshots: `GET /api/projects/<id>/session_recordings/<sid>/snapshots?blob_v2=true` lists
  sources, then fetch each with `source=blob_v2&start_blob_key=k&end_blob_key=k` (both are
  required, otherwise 400). JSONL of `[window_id, event]`. Payloads with `cv: "2024-10"` are
  gzip carried as latin-1 strings. **Split on `\n` only**: `splitlines()` breaks inside them.
- HogQL `filterTestAccounts`: pass `"filters": {"filterTestAccounts": true}` AND put
  `{filters}` in the WHERE clause, or it does nothing. A shell eats `$session_id`, so query
  from Python, not curl.
- `/session_recordings/<sid>` 404 means no recording, even when the session has events.
- Use a personal API key with read scopes only.
