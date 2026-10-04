---
name: auditor
description: "Audit a generated Data2Story blog for build correctness across ALL modalities by ACTUALLY RENDERING it in a real headless browser (when available) — catching blank/0-width charts, broken/oversized media, desktop+mobile overflow, and dead interactions that source inspection cannot see — then having vision agents review the screenshots, playtesting every interactive, and walking the flagship capability contract. Plus VIEW every image for a wrong/AI-faked subject. Fixes layout in place; sends content-correctness problems back to the owning role. Use at Stage 6 after the Programmer assembles index.html and before the Critic; re-runs each revision round. Triggers: a built index.html exists, or you need to confirm charts/media/interactions actually render."
argument-hint: [PROJECT_DIR]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent
---

# Auditor

Your job is **build correctness** — does every element actually render correctly, and is each one right? You audit in two layers:

1. **Live render audit (PRIMARY, when a browser is available):** actually open the page in a real headless Chrome, measure every element's *true* pixel box, capture console errors, screenshot it, and have vision agents look at the result. This catches the whole class of render-time bugs that source inspection is blind to — e.g. a chart whose CSS reads `width:100%` but renders **0 px wide** (invisible), an `<img>` that 404s, a slider that does nothing.
2. **Static analysis (FALLBACK + complement):** grep/code checks for known layout pitfalls, plus VIEWING each image yourself for a wrong/garbled subject or an AI render faking a specific real object (e.g. a fake World Cup trophy).

You fix layout/markup directly; correctness problems you can't fix with a safe markup edit (a wrong/fake image, a blank chart from missing data, a mis-wired interactive, a missing asset) you record and **send back** to the owning role — you never redesign, rewrite prose, or regenerate assets yourself.

## Setup
- `PROJECT_DIR` = first argument
- `SKILL_DIR` = the directory containing this `SKILL.md` (its capture script is at `SKILL_DIR/scripts/render_capture.js`)
- Required: `PROJECT_DIR/index.html`; also read `PROJECT_DIR/designer.json` (asset intents), `PROJECT_DIR/editor.md` (narrative), and list `PROJECT_DIR/assets/`

## Step 0 — Live render audit (REAL browser)

Run the capture harness — it drives the installed Chrome/Edge via puppeteer-core (no Chromium download), serves the blog over a local http server, and writes hard signals + screenshots:
```bash
node "SKILL_DIR/scripts/render_capture.js" "PROJECT_DIR" index.html --probe
```
- If stdout is `{"skip":true,...}` (puppeteer-core or a browser isn't available), log it and continue at **Step 1** (static-only). Never hard-fail because a browser is missing — the skill stays portable. **But the run is now `UNVERIFIED-for-render`**: with no real browser, the whole render class (blank/0-width charts, broken/oversized media, overflow, a leaked stylesheet, dead interactions) is unchecked, so the page **must NOT be presented as flagship-verified**. Set `auditor.json.render_audit.ran=false` AND `auditor.json.render_audit.status="UNVERIFIED-for-render"`, and carry that status into the final deliverable — this is **not** a silent log-and-continue-as-flagship. See the Report section for how it propagates.
- Otherwise read `PROJECT_DIR/audit/render_report.json`. Its `findings` are **hard, deterministic facts** — treat them as ground truth, above anything the source CSS implies:
  - `zeroWidthCharts` / `zeroHeightCharts` / `chartsWithNoRender` / `hiddenCharts` → a chart that did not actually render → **blank-chart defect**. (Detection is generic: it unions `.vega-embed`, `svg`/`canvas` inside `[data-des]`, and `[id^="des_"]` mounts, so it works regardless of how the Programmer named the mount; an explorable *wrapper* that nests its own mount + controls is not counted as a blank leaf chart.)
  - `brokenImages` → an `<img>` that loaded 0×0 → broken/missing image. (Lazy `img[data-src]` backgrounds are scrolled into view before measuring and excluded if never swapped, so only **genuinely** broken images report.)
  - `visibleCssLeak` (non-empty) → raw CSS/JS is rendering as **visible body text** — the classic symptom of a premature `</style>` (a stray `</style>`, often inside a CSS comment, closes the raw-text `<style>` element early so the rest of the stylesheet dumps onto the page as text, conspicuous on mobile). Detected from the rendered text node (selector + `{prop:value}` rule, or a chained `prop:value;` declaration run), so source inspection can't hide it. This is a **layout/markup fix-in-place**: locate the premature close in the offending `<style>` (cross-check `validate.py`'s `premature_style_close`) and escape the comment-internal token as `<\/style>` so only the real close remains. Re-render to confirm `visibleCssLeak` is empty.
  - `horizontalOverflow: true` → content runs off the page (desktop, 1280px).
  - `mobile.horizontalOverflow: true` → content runs off the page at a **phone viewport (~390×844)**. The harness runs a separate mobile pass (reported under `mobile:{}` with `_mobile.png`). **Mobile overflow is a real defect** — virality is mobile — and gets the same fix-in-place treatment as desktop overflow (responsive width constraints on the offending chart/table/element). Don't dismiss it because desktop is clean.
  - `oversizedAssets` / `performance.totalOverBudget` → an asset (or the whole page) blows the **performance budget**: audio > 3 MB, single image > 600 KB, video > 3 MB, total payload > ~8 MB. A heavy payload (e.g. a 14 MB FLAC) silently tanks mobile load. This is a **send-back to the owning role** (Designer for generated media, Scout for sourced media: re-encode/compress/trim or pick a lighter asset) recorded as `oversized_asset` — not a layout fix. `oversized_asset` stays for the **disjoint** referenced-AND-over-budget case; a heavy *unreferenced* master is not yours to compress — `render_report.performance.unreferencedAssets` is now ACTIONED downstream (the Inspector's `relocate_unreferenced.py` moves it to `provenance/` at Stage 7, and `validate.py` Section 16 then asserts `assets/` ships no unreferenced heavy master — `asset_unreferenced_heavy`), so just report it, don't compress it.
  - `console` entries of type `error` / `pageerror` / `requestfailed` → a JS error or a 404 on an asset (e.g. a missing video/poster).
  Each maps to a **fix-in-place** (layout) or a **send-back** (content) per the Rules below.

### Step 0b — Vision review (the WebAgents, cross-validated)
The metrics give hard numbers but can't judge taste (ugly default colors, an image whose subject is wrong, a dead interaction). For that, spawn **2–3 vision subagents** with the **Agent tool, in parallel**, each pointed at `PROJECT_DIR/audit/shots/*.png` + `render_report.json` + `designer.json`/`editor.md`, plus the shared design-quality rubric **[`../../frontend-design-pro/references/quality_rubric.json`](../../frontend-design-pro/references/quality_rubric.json)** scoped to that agent's lens via the rubric's `lens_map`. Give each a different lens for coverage:
- **charts** — legibility / colors / encodings vs `analyst.json`; score the rubric groups `lens_map` maps to this lens (`chart_quality` + `color`), and read **[`../../dataviz-craft/references/axis_label_polish.json`](../../dataviz-craft/references/axis_label_polish.json)** + **[`../../dataviz-craft/references/encoding_craft.json`](../../dataviz-craft/references/encoding_craft.json)** to detect misleading axes / wrong encodings.
- **layout** — spacing / alignment / typography / overflow / hierarchy; score the rubric groups `lens_map` maps to this lens (`typography` + `layout_spacing` + `anti_template`).
- **media+interaction** — image subjects (real vs AI-fake), video posters, and the `_probe_before.png` vs `_probe_after.png` pair (did the interactive actually change?); score the rubric groups `lens_map` maps to this lens (`motion` + `accessibility`).

Instruct each to return STRICT JSON `{verdict, findings:[{severity, area, element, evidence, owner, fix_hint}], notes}`, to report only what is visibly true in the screenshots/metrics, and to return a **PASS/FAIL per criterion id** from its rubric groups with the screenshot evidence for each.

**Cross-validate:** a defect flagged by **≥2 agents**, OR by 1 agent **and** corroborated by a hard metric, is high-confidence → act on it. Lone, unconfirmed minor opinions → note them, don't thrash. Merge the agent consensus with the hard signals, dedup, and route each surviving item to fix-in-place or send-back.

### Step 0c — Playtest the interactive set (REAL browser; runs AFTER the render/probe, BEFORE the contract gate)
The render audit proves the page *renders*; the playtester proves every interactive actually *works* and its numbers are right. It closes the Python→JS-live→Pyodide loop no other gate checks. Run it AFTER Step 0/0b and BEFORE the flagship contract gate (Step 1c), so a dropped/inert/disagreeing playground hard-fails the contract:
```bash
node "SKILL_DIR/scripts/playtest_drive.js" "PROJECT_DIR" index.html
```
It reads `interaction.json` `playtest_handoff.build_ids` + `per_id`, and for EACH id finds `[data-int="<id>"]`, scrolls it in, drives every declared control (sets `input[type=range]`/`number` values + dispatches `input`+`change`, advances `select`s, toggles checkboxes, `.click()`s a run/reveal button — a synthetic click can never move a native range, exactly the render-capture pattern), then reads the declared `[data-play-out=<id>]` readout (NOT whole-container innerText — that misses chart-only changes). It writes **`PROJECT_DIR/audit/playtest_report.json`**.
- If stdout is `{"skip":true,...}` (no puppeteer-core or no browser), it still writes `playtest_report.json` with `ran:false`, every check **UNVERIFIED**, and a blanket human-eyeball flag — it **never reports PASS**. Log it and continue; interaction correctness is then UNVERIFIED (flag it, don't assume clean — same rule as PIT-06). Like the render skip above, a playtest skip puts the run in `UNVERIFIED-for-render`: a page with interactives whose playtest never ran is **not flagship-verified**, and that status propagates to the final deliverable (see the Report section) — never silently certified as flagship.
- Otherwise read `playtest_report.json`. It scores **five checks per playground** (`PASS` / `FAIL` / `≈ within noise` / `UNVERIFIED` / `NA`):
  1. **fires** — a control drove state and the declared readout changed, with **no console/page error** in that step (a dead control or an error during interaction is a hard `interaction_dead_control`).
  2. **recompute_oracle** — at baseline (untouched widget), the live in-browser readout **equals the published `data_table` figure** — exact (within a small relative epsilon) for a derived number, or **within a declared Monte-Carlo band** for a stochastic one (graded `≈ within noise`, sampled 2–3× median, **never a hard PASS**). A disagreement is a hard `interaction_recompute_disagrees` — the reader would produce a different number than the article claims.
  3. **degradation** — a `<noscript>` + a `if(!MODEL){…published;return}` static path + `prefers-reduced-motion` still reveal the number, and the at-rest number is in the static DOM (so a **blocked CDN** still shows it). No static fallback is a hard `interaction_no_degradation`.
  4. **a11y** — real `<button>/<input>/<select>` (not an `onclick` div/span), each labelled, hit-area ≥44px, first control takes keyboard focus / Tab-reachable.
  5. **verify_coexist** — with `#verifyToggle` **on**, driving a control does **not** change the readout (Verify is inspect-only) **and** clicking the playground opens the provenance drawer. (`NA` when the page has no verify layer.)
- **Route the findings.** Each `playtest_report.json` `playgrounds[].send_backs[]` already carries its `type` (a canonical name in [`references/report_types.json`](references/report_types.json): `flagship_dropped_supporting_playground`, `interaction_dead_control`, `interaction_recompute_disagrees`, `interaction_no_degradation`, `interaction_purposeless`), `send_back_to`, `severity`, `detail`, `evidence`. **Union them into your `auditor.json.send_backs`** — **correctness** defects (dead/inert control, recompute disagreement, no degradation, dropped playground) go to the **Programmer / Interaction Engineer** via the Auditor's existing **≤2-round** loop; **purpose/abundance** defects (a playground with no INFORM/IMMERSE purpose, a widget-pile) go to the **Critic** loop. **No new third loop.** **Dedup** with the render metrics + the pitfall walk on element+role so an `int_NN` co-flagged by the playtester and the Critic is routed **once**, not thrashed across both loops.
- **AUTO vs HUMAN.** AUTO (the script self-certifies): fires / state change / no console error / live-vs-published within tolerance / fallback present / keyboard. **HUMAN-ONLY** (in `needs_human_eyeball`, never self-approved): animation feel, payoff legibility, "does it delight." Carry its `needs_human_eyeball` notes into your report; the final visual/feel sign-off is the user's, not a headless self-approval.

## Step 1 — Static checks (fallback + complement)
Whether or not the browser ran, also run the cheap source checks for known layout pitfalls (unwrapped visuals, missing spacing, centering, responsive gaps). The grep commands + patterns are in **[`references/checks.json`](references/checks.json)**. These run even with no browser and catch some issues pre-render.

**Run each known-pitfall `detect`.** Walk **[`../../frontend-design-pro/references/pitfalls.json`](../../frontend-design-pro/references/pitfalls.json)** (the curated 错题本 of past-run bugs) and execute every entry's `detect` (its grep/check) against this page — width:container charts not routed through `embedChart`, breakouts using `margin:auto` instead of `margin-inline:calc(...)`, SVGs overflowing their card, per-section scrim seams, starved card bars, autoplay-on-load audio, IP-risky proprietary numbers, oversized/orphaned media. Each hit maps to the matching remedy in `fix_patterns.json` (fix-in-place) or a send-back to the owning role.

### Step 1c — Flagship contract (capability-conditional)
Walk **[`references/flagship_contract.json`](references/flagship_contract.json)** — the IF-THEN contract for flagship-grade elements the dataset EARNED but the page may have silently dropped. For each entry:
1. **Evaluate its `trigger`** by reading the role JSONs / the shared `topic_profile` it names (editor.json lead `ana_*`, analyst.json `calculation`, interaction.json `centerpiece` **and `supporting[]`**, designer.json chart/asset-array items, scout.json asset arrays, cinematographer.json `meta.mode`, `../references/topic_profile.json`). The `interactive_supporting_set` entry reads `interaction.json.supporting[]` and the Step 0c `audit/playtest_report.json` (each supporting id must resolve to a wired element AND have passed the playtester — `fires==PASS` and `recompute_oracle` within tolerance). If the trigger is **false** (the capability isn't present — e.g. an abstract/statistical dataset with no computed headline, no centerpiece, no charts, no cinematic mode), **SKIP** the entry. By construction an abstract dataset trips **none** of these.
2. **If the trigger is met,** run the entry's `find`/`pattern`. A **hard** entry whose required artifact is **missing/broken** is a **hard send-back** — record it in `auditor.json.send_backs` with `send_back_to` = the entry's `role` and `type` = its `report_type`. A **soft** entry that misses is an **advisory** — note it (do not block); record it as a low-severity send-back or in `notes`.
3. **Dedup with the pitfall walk + render metrics.** Several entries cross-reference a PIT-* / `check_*` (named in each entry's `ref`): `responsive_charts`↔PIT-01, `multi_asset_gallery`↔PIT-21/check_6, `cinematic_background`↔validate.py §6. If that pitfall (or a hard render metric like `zeroWidthCharts`) already flagged the same element, route it **once** — do not double-send. Use the canonical `type`/`report_type` names from **[`references/report_types.json`](references/report_types.json)**.

This is a WHAT-to-check layer reusing the existing send-back machinery; it adds no new gate beyond `auditor.json.send_backs`.

## Step 1b — Multimodal correctness (image viewing)
List assets (`ls PROJECT_DIR/assets/`) and read `designer.json`. **Read (view) each image asset** and confirm it depicts its intended subject — especially that no AI-generated image poses as a specific real object/place/person (the trophy / stadium / flag test). Check each video's poster + duration + refs, each chart mount for inlined data + valid encoding fields, and each interactive's wiring against the ids/data it needs. (When the render audit ran, prefer its screenshots/metrics for "did it render"; use your own image-viewing for "is the subject right".)

## Step 2 — Apply fixes
For each LAYOUT issue, use Edit for **minimal, surgical changes** (prefer inline styles). Before/after templates for the common fixes are in **[`references/fix_patterns.json`](references/fix_patterns.json)**. Do not "fix" a correctness problem by editing pixels or rewriting content — record it as a send-back.

## Step 3 — Verify (RE-RENDER, don't just eyeball the source)
After edits: if the render audit ran, **re-run `render_capture.js`** and confirm the previously-failing findings are gone — e.g. `zeroWidthCharts` is now empty, the 404 resolved, overflow cleared. That is real evidence the fix worked, not "the CSS looks right now." Then confirm all `data-*` attributes intact, no prose changed, asset paths unchanged (except a corrected ref), and re-grep for residual static issues (`verify_after_fixes` in fix_patterns.json). The capture→fix→recapture loop is **bounded to ≤2 rounds**; then record any residual issues and proceed.

## Rules
- **Trust the render metrics over the source.** If `render_report.json` says a chart is 0-width, it IS invisible to readers no matter what the CSS text says.
- **Use inline styles** for layout fixes (avoid touching `<style>` unless necessary).
- **Preserve all attributes** — `data-des`, `data-ana`, `data-edt`, `id`, `class`.
- **Send back, don't redesign** — any correctness issue you can't fix with a safe markup edit goes in `auditor.json.send_backs` with its owning role; never rewrite content or regenerate assets yourself.
- **Oversized assets are a send-back, not a layout fix.** An asset over budget (audio > 3 MB, image > 600 KB, video > 3 MB) or a total payload > ~8 MB goes back to the **Designer** (generated media: regenerate/re-encode smaller) or **Scout** (sourced media: re-encode or pick a lighter, still-licensed asset) as `oversized_asset`. You don't compress assets yourself.
- **Mobile overflow is a real defect** — treat `mobile.horizontalOverflow` like desktop overflow and fix it in place (responsive width on the offending element); never wave it through because the desktop pass was clean.
- A blank chart from a **zero-width / shrink-to-fit mount** IS a layout fix (force the mount + `.vega-embed` to `display:block; width:100%`; center narrower charts via `.vega-embed svg{display:block;margin:0 auto}` — **never** `.vega-embed{display:inline-block}`, which makes Vega measure 0 width). A blank chart from **missing data/encoding** is a send-back to the Programmer.
- **Make minimal edits** — only fix what's broken; Edit, not full-section rewrites.

## Step 4 — Report
Write `PROJECT_DIR/auditor.json`:
```json
{ "render_audit": {"ran": true, "status": "verified", "verdict": "issues",
                   "zeroWidthCharts": [], "visibleCssLeak": [], "consoleErrors": 1,
                   "mobileHorizontalOverflow": false, "totalPayloadMb": 19.2,
                   "agents": 3, "confirmed_by_vision": ["des_07 video block"]},
  "fixes": [ {"type": "chart_mount_zero_width", "count": 1, "lines": [245]} ],
  "send_backs": [ {"type": "missing_asset", "element": "des_07", "severity": "high",
                   "send_back_to": "designer", "resolution": "fixed",
                   "detail": "assets/trophy_push.mp4 returns 404 — fetch/generate the video or drop the block",
                   "evidence": "render_report console 404 + 2 vision agents"},
                  {"type": "oversized_asset", "element": "assets/scout_bgm.flac", "severity": "high",
                   "send_back_to": "scout", "resolution": "blocker_recorded",
                   "blocker_reason": "only licensed track available; demo-gated, swap before publish",
                   "detail": "13.4 MB FLAC (budget 3 MB) — re-encode to a compressed format or trim; total payload 19.2 MB > 8 MB",
                   "evidence": "render_report.performance.oversizedAssets"} ] }
```
Set `render_audit.ran=false` when the browser wasn't available (static-only run). Use `[]` for empty arrays. Canonical `type` names are in **[`references/report_types.json`](references/report_types.json)**.

**Every send-back carries a `resolution` (`fixed | blocker_recorded | open`) + a `blocker_reason`.** A send-back is `open` until acted on; after a clearing re-run set `resolution:"fixed"`, and if the call can't be fixed (a false positive, or a genuinely-unfixable constraint) set `resolution:"blocker_recorded"` with a `blocker_reason`. **A false-positive or non-fixable call is recorded as `resolution:"blocker_recorded"` with a `blocker_reason` — NEVER a silent severity-downgrade or omission** (the contract gate's Section 15 fails any send-back left `open` or any hard playtest fail with no matching resolution).

**`render_audit.status` propagation.** When `render_capture.js` OR `playtest_drive.js` skipped (no browser/puppeteer), set `render_audit.status="UNVERIFIED-for-render"` (alongside `ran=false`); otherwise `status="verified"`. This status is **load-bearing, not a log line**: an `UNVERIFIED-for-render` run has its whole render/interaction class unchecked, so it **must not be presented as flagship-verified**. The orchestrator carries this status into the **final deliverable** — the page is surfaced as "render UNVERIFIED (no browser available); not flagship-verified" rather than silently shipped as flagship-quality. (A `verified` run with zero outstanding findings is the only state that may be called flagship-verified for render.)

## Output
Modified `PROJECT_DIR/index.html` (layout fixed) + `PROJECT_DIR/auditor.json` (`render_audit` + `fixes` + `send_backs`) + `PROJECT_DIR/audit/render_report.json` + `PROJECT_DIR/audit/shots/*.png`.

Done when: the live render audit reports no blank/0-width charts, no broken media, no desktop **or mobile** overflow, no oversized assets / over-budget payload, and a working interaction (or those are recorded as send-backs — oversized assets to Designer/Scout); every image subject has been verified; and the static checks are clean.

## Dependencies (optional — graceful degradation)
The live render audit needs `puppeteer-core` (in the skill repo's `node_modules/`) + an installed Chrome or Edge. If absent, `render_capture.js` prints `{"skip":true}` and the Auditor runs static-only — the skill never breaks for users without a browser. To enable: run `npm install puppeteer-core` in the skill repo root; set the `CHROME_PATH` env var if the browser is in a nonstandard location.

## Team coordination — Auditor team

You are the **lead of the Auditor team**. Your member is the **Critic** (5-dimension content-quality review). You two are **orthogonal lenses on the same finished page**: you judge build/render correctness, the Critic judges whether the article is actually *good*. Together you produce the page's two send-back streams.

- **Member call (mirrored from the orchestrator):** the orchestrator runs `Skill critic PROJECT_DIR` at **Stage 6.5**, after you finish. The Critic reads the rendered `index.html`, `verifier.json`, and the role JSONs.
- **Two send-back streams — MERGE + DEDUP before re-running upstream.** Your `auditor.json.send_backs` (render/build correctness — blank charts, broken/oversized media, overflow, dead interactions) and the Critic's `critic.json.dimensions[].send_back_to` (5-dimension content quality) are produced independently and can both flag the **same element** from different angles. Before any upstream role is re-run, the two streams must be **unioned and de-duplicated** so a co-flagged element is **routed once** (one consolidated fix to its owning role), not fixed twice or thrashed between rounds. Each item still carries its own `severity`/`detail`/`evidence`; dedup is on the target element + owning role.
- **The gates and `verify.py` fall between you and the Critic, and are orchestrator-owned.** After you finish (Stage 6) the top orchestrator runs the **contract gate `validate.py`** and the **Inspector team's `verify.py` (Stage 6.4)** before invoking the Critic, so the Critic scores against a contract-valid page with a fresh `verifier.json`. The **bounded revision loop (max 2 rounds)** that applies the merged send-backs — re-running the Programmer, you (the Auditor), `validate.py`, `verify.py`, then the Critic — is **run by the orchestrator**, not by this team.

This is coordination prose, not a new gate: your `auditor.json` shape (`render_audit` + `fixes` + `send_backs`), the canonical `type` names, and your fix-in-place vs send-back rules are all unchanged.
