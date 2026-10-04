---
name: qa-cell-worker
section: pipeline
description: "Parallel cell-execution subagent. Receives a chunk of audit cells, opens its own browser tab, runs them sequentially within the tab, writes findings to JSONL, returns. Spawned in parallel by qa-argus Step 5.1 when resolvedConfig.workers > 1. Honors the workers setting dynamically: workers=4 spawns 4 of these in parallel, workers=8 spawns 8."
model: sonnet
applyOn: all
needsSetup: true
viewportSensitive: true
interactive: true
ownership: "exclusive: when qa-argus dispatches a cell chunk in parallel, this skill owns the per-cell execution loop"
---

# qa-cell-worker — Parallel Cell-Execution Subagent

This is the **per-worker subagent** that qa-argus dispatches in parallel when `resolvedConfig.workers > 1`. Without it, Step 5 runs a serial `for each cell` loop and the `workers` setting has no effect.

## When this skill runs

Spawned by [qa-argus/SKILL.md Step 5.1](../qa-argus/SKILL.md) via the Agent tool. The parent orchestrator emits N parallel `Agent({ subagent_type: "qa-cell-worker", ... })` calls in ONE message, where N = `resolvedConfig.workers`.

Each spawned worker owns ONE (engine × viewport) and receives:
- `serverName` — its DEDICATED MCP server (e.g. `playwright`, `pw-firefox-mobile`, `pw-webkit-tablet`). All browser calls use `mcp__{serverName}__*`. The server's `--browser` flag fixes the engine — the worker never sets it.
- `engine` — `chromium` | `firefox` | `webkit`.
- `viewportClass` + `viewport` — the viewport this worker tests (`{width, height}`). The worker resizes its browser to this ONCE and keeps it for all cells.
- `chunkIndex` — which worker this is (0..activeWorkers-1)
- `cells[]` — the routes assigned to THIS dispatch at this (engine, viewport). For small sites this is every route at the viewport; for larger sites the orchestrator splits the viewport's routes into **waves** of ≤ `cells_per_worker` cells and dispatches each wave as a separate FRESH Agent call (this is what stops a worker from running out of context and silently dropping the interactive skills). You process exactly the `cells[]` you were given — no more, no less — and you drive EVERY skill (passive AND every interactive) on EVERY one of them. You never touch another (engine, viewport).
- `runId` — for writing findings to `.tmp/{runId}/issues/cell-XXX.jsonl`
- `resolvedConfig` — full audit config (browsers, viewports, enabled skills, content settings, resilience knobs)
- `baseUrl` — app under test

## Hard rules

| # | Rule | Why |
|---|---|---|
| 1 | **MUST use ONLY your assigned MCP server's tools** — every browser call prefixed `mcp__{serverName}__` (e.g. `mcp__pw-firefox-mobile__browser_navigate`). `{serverName}`, `{engine}`, `{viewport}` are given in your dispatch prompt. Your server = your own dedicated browser window of YOUR engine, sized to YOUR viewport. | True parallelism: each worker drives a SEPARATE browser process for one (engine × viewport) — zero contention, correct engine and size. |
| 2 | **MUST log in on your own browser first** (Step 1) — your server runs `--isolated` so it has NO shared cookies. Navigate to the login path, fill email+password (mask password), submit, confirm redirect BEFORE auditing any cell. | Isolated browsers don't inherit the orchestrator's session; each worker authenticates its own browser. |
| 3 | **MUST NOT open extra tabs or touch another server's tools.** Use your browser's default page. Never call the bare `playwright` tools unless that IS your assigned server. | You own a whole browser — tabs are unnecessary; touching a peer's server corrupts that worker's run. |
| 4 | **MUST write findings to `{project-root}/.tmp/{runId}/issues/cell-XXX.jsonl`** — same path the serial loop used. | The downstream Step 5.7.5 annotation sweep and Step 7 bug filer read from this path. |
| 5 | **MUST honor `resilience.cell_total_ms`** — if a cell exceeds the budget, append `cellTimeout` finding and continue to next cell in chunk. | Same protection the serial loop has. |
| 6 | **MUST NOT cross-contaminate cells from other workers.** Only touch cells in YOUR `cells[]` array. | Parent orchestrator already partitioned cells; workers must respect partitioning. |
| 7 | **🚨 EVERY file write — findings, receipts, screenshots, AND any scratch/intermediate — MUST use the FULL ABSOLUTE path under `{project-root}/.tmp/{runId}/issues/` (or `/screenshots/`).** NEVER write a file with a bare/relative name (`cell-001.jsonl`, `cell-003-passive.json`, `cell-004-interactive-raw.json`, etc.). Your CWD is the user's workspace ROOT, so a relative path dumps the file there and pollutes the repo. Do NOT create `-raw`/`-passive`/scratch files at all — stage intermediate data IN MEMORY and write only the canonical `{cell.id}.jsonl`, `{cell.id}-probes.json`, `{cell.id}-interactive.json`, `{cell.id}-parity.json` to their absolute `.tmp/{runId}/issues/` paths. | Relative writes land in the workspace root (confirmed: stray `cell-*-passive.json`/`-raw.json` appeared at repo root). Absolute-only + no-scratch keeps the repo clean. |

## 🪙 TOKEN & TIME DISCIPLINE (mandatory — this is how the audit stays cheap and fast)

These rules cut token consumption and wall-clock without losing coverage. Violating them is the #1 cause of the 500k-token / 30-minute-per-page runs.

| # | Rule | Why it matters |
|---|---|---|
| T1 | **NEVER call `browser_snapshot` (or any full accessibility-tree / full-DOM dump) for DETECTION.** Detection happens ONLY inside the batched `browser_evaluate` probe, which returns compact findings. `browser_snapshot` is the single biggest token cost — one snapshot can be 20–50k tokens. Use it ONLY if you genuinely need a ref to click a specific element you cannot reach by selector, and even then prefer `browser_evaluate` with a selector. | One avoided snapshot ≈ 20–50k tokens saved per use. |
| T2 | **Run ALL passive probes in ONE `browser_evaluate`** (the batched call in Step 3). NEVER one `browser_evaluate` per skill. One call returns one compact object keyed by skill. | 50 separate calls → 1 call: ~50× fewer round-trips. |
| T3 | **Probes return ONLY `{skill, issueType, severity, selector, bbox, description}` — never element HTML, never `outerHTML`, never the page text.** Compact data only. | Keeps each finding ~1 line instead of a paragraph. |
| T4 | **Do NOT re-open individual skill `SKILL.md` files at runtime.** Everything you need is already in `skill-probes.json` (passive probes + interactive specs + frontmatter). Read it ONCE at Step 2. Re-reading 25 SKILL.md files per cell is pure wasted context. | Saves the per-cell re-read tax. |
| T5 | **Use EVENT waits, not fixed sleeps.** Prefer `browser_wait_for({ text })` / wait-for-selector / a single bounded settle. Never stack multiple multi-second `wait_for({ time })` calls "to be safe". Cap any blind wait at the resilience value and do it ONCE. | Fixed sleeps add 10–20s of dead time per cell for nothing. |
| T6 | **Do not narrate per action.** Don't write a reasoning paragraph before each click/probe. Decide the cell's plan once, execute, report the result. | Per-action narration is a large hidden token cost across 60+ actions. |

## Execution flow

### Step 1 — Size your browser to your viewport

Two cases — check `viewport` from your dispatch prompt:

**Case A — viewport has explicit `width` + `height`** (custom sizes like "Laptop 1280", "Desktop 1440"):
```
mcp__{serverName}__browser_resize(viewport.width, viewport.height)   // e.g. 1280×800
```

**Case B — viewport has `name` only, NO `width`/`height`** (named Playwright devices like "iPhone 12", "iPad Air"):
```
// SKIP browser_resize — the MCP server was started with --device "<name>" by qa-preflight,
// so Playwright already set the correct viewport size, mobile UA, touch support, and pixel ratio.
// Calling browser_resize here would OVERRIDE the device emulation and break the mobile UA.
LOG: "[worker] device emulation active: {viewport.name} — skipping browser_resize"
```

**Then install the console-error collector ONCE (for `qa-detect-console-errors`, Step 7c).** `addInitScript` re-runs on EVERY navigation, so a single install at worker start catches load-time unhandled rejections + CSP violations on every cell (a per-cell `browser_evaluate` injection would miss errors that fire during load). Idempotent — safe even if re-run:
```
mcp__{serverName}__browser_run_code_unsafe({ code: `await page.addInitScript(() => {
  if (window.__argusErr) return; var s = window.__argusErr = []; function p(o){ if(s.length<200) s.push(o); }
  addEventListener('unhandledrejection', function(e){ var r=e&&e.reason; p({source:'',kind:(r&&r.name)||'PromiseRejection',text:'Uncaught (in promise) '+((r&&r.message)||(typeof r==='string'?r:''))}); });
  addEventListener('error', function(e){ if(e&&e.error) p({source:e.filename||'',kind:(e.error&&e.error.name)||'Error',text:e.message||String(e.error)}); });
  document.addEventListener('securitypolicyviolation', function(e){ p({source:e.sourceFile||'',kind:'CSPViolation',text:e.violatedDirective+' blocked '+(e.blockedURI||'inline')}); });
}) `})
```

Do NOT log in yet. Phase 1 cells must be captured in an unauthenticated state first.

### Step 2 — Load the SLIM skill list FIRST (NOT the 271KB bundle), then process cells in phase order

**🚨 BEFORE the per-cell loop — read the SLIM skill list (MANDATORY, do this ONCE):**

```
allSkills = JSON.parse(fs.readFileSync("{project-root}/.tmp/{runId}/skill-names.json")).skills
```

🚨 **BUG 1 FIX — read `skill-names.json` (≈14KB: names + `applyOn`/`interactive`/`executable`/`probeCallable` flags), NEVER `skill-probes.json` (271KB of probe SOURCE).** You only need the names + flags to filter by viewport and to build the coverage receipts. The probe SOURCE is loaded into the PAGE via `probes-inject.js` (Step 4b) — it must never enter your context. Reading the 271KB bundle was the ~68k-tokens-per-worker bug.

**Phase ordering is MANDATORY — process cells in this exact order:**

```
// Step A — build the pre-login and post-login batches
// Works for BOTH phased audit plans (c.phase set) AND flat/legacy plans (c.phase absent).
const loginRoute = resolvedConfig.loginPath   // e.g. "/authentication/signin"

// A cell runs BEFORE login if:
//   (a) it was explicitly tagged phase 1 by qa-phase-strategy, OR
//   (b) its route IS the login page itself (catches flat plans where phase is unset)
preLoginCells = cells.filter(c =>
  c.phase === 1 ||
  c.route === loginRoute
)

phase2Cells = cells.filter(c => c.phase === 2)

// Everything else (phase 3 or unphased non-login routes) runs AFTER login
postLoginCells = cells.filter(c =>
  !preLoginCells.includes(c) && c.phase !== 2
)
```

🚨 **SIGN-IN PAGE RULE (no exceptions):**
The login/sign-in route (`resolvedConfig.loginPath`) MUST always be in `preLoginCells`.
If audited after login, Angular/React SPAs silently redirect to dashboard — all probes run
on the wrong page and tag dashboard bugs as sign-in bugs. This is the single most common
source of wrong-route findings.
If `preLoginCells` is empty after the filter above (i.e. the audit plan has no phase-tagged
cells AND the login route doesn't appear in `cells`), skip the pre-login batch silently.

**Process preLoginCells FIRST (no session):** navigate each public/login page, run probes, write JSONL.
This captures the real unauthenticated state: the actual sign-in form, field labels, validation
UI, placeholder text, and layout — exactly what a real user sees before they log in.
The browser has no cookies at this point — public pages render correctly.

**Then log in (between pre-login and post-login):**
```
mcp__{serverName}__browser_navigate({ url: baseUrl + loginPath, waitUntil: "domcontentloaded" })
mcp__{serverName}__browser_type(email into the email/username field)
mcp__{serverName}__browser_type(password into the password field)   // mask password in all output
mcp__{serverName}__browser_click(submit)
// T5: EVENT wait, not a blind 5s sleep. Poll the path; stop the instant we leave the login route (bounded).
mcp__{serverName}__browser_evaluate("() => new Promise(r => { const t0 = Date.now(); const i = setInterval(() => { if (!/sign|login|auth/i.test(location.pathname) || Date.now()-t0 > 6000) { clearInterval(i); r(location.pathname); } }, 200); })")
LOG: "[worker {chunkIndex}] logged in"
```
If login fails: return early with `{ loginFailed: true }`.

**Then process phase2Cells and postLoginCells** with the active session.

### URL VERIFICATION — MANDATORY after every browser_navigate

After navigating to any cell's route, always verify the actual URL before running probes:

```
actualPath = mcp__{serverName}__browser_evaluate("return location.pathname")
if (actualPath !== cell.route) {
  // Navigation redirected — this cell's probes would run on the WRONG page.
  // Write a single info finding and SKIP all probes for this cell.
  write to JSONL: {
    issueType: "cellRedirected",
    severity:  "info",
    route:     cell.route,
    description: "Navigation to " + cell.route + " redirected to " + actualPath +
                 " — cell skipped to avoid probes running on the wrong page"
  }
  continue to next cell   // DO NOT run any probes
}
```

**Why this matters:** SPA apps like Angular redirect authenticated sessions away from the login page to the dashboard. Without this check, all probe findings get tagged with the INTENDED route (/authentication/signin) even though the browser is actually showing a completely different page (dashboard). This produces tickets that describe issues on the wrong page with wrong screenshots.

### Step 3 — Per-cell execution

**🚨 BEFORE the per-cell loop — read the SLIM skill list (MANDATORY, do this ONCE):**

```
allSkills = JSON.parse(fs.readFileSync("{project-root}/.tmp/{runId}/skill-names.json")).skills   // names + flags only, ≈14KB
```

🚨 **FAIL CLOSED — if `skill-names.json` does not exist or `allSkills.length` is 0, ABORT this worker immediately** (return `{ loginFailed: false, aborted: true, reason: "skill-names.json missing" }`). Do **NOT** fall back to model memory and audit "the skills you know" — that produced 9-skill runs labelled as 92-skill coverage. The orchestrator will re-run `bundle-probes.cjs` and re-dispatch. No bundle = no audit.

`skill-names.json` (slim) + `probes-inject.js` (the probe SOURCE, loaded into the page in Step 4b) + `skill-probes.json` (used only by the deterministic runners) are all written by `bundle-probes.cjs` before dispatch. **Use `skill-names.json` to decide which skills to run — never model memory, and never read the 271KB `skill-probes.json` into your context.**

For each `cell` in ordered phase batch (all browser calls prefixed `mcp__{serverName}__`):

1. **Filter skills for this cell** (pure set operation — no judgment):
   ```
   applicableSkills = allSkills.filter(s =>
     (s.applyOn === 'all' || s.applyOn.includes(cell.viewportClass))
   )
   passiveSkills     = applicableSkills.filter(s => s.probe && !s.interactive)
   interactiveSkills = applicableSkills.filter(s => s.interactive)
   ```

2. Navigate, then verify URL before running any probes:
   - `mcp__{serverName}__browser_navigate({ url: baseUrl + cell.route, waitUntil: "domcontentloaded", timeout: 15000 })`
   - T5: do NOT add a blind `wait_for({ time: 1500 })` here — the data-ready poll below (step 2b) is the ONE bounded wait that settles the page. A fixed pre-wait on top of it is dead time.
   - `actualPath = mcp__{serverName}__browser_evaluate("return location.pathname")`
   - **If `actualPath !== cell.route`: write `cellRedirected` info finding, SKIP all probes, continue to next cell.**
     This prevents findings from being tagged to the wrong route when an SPA redirects (e.g. authenticated session redirects `/authentication/signin` → `/admin/dashboard/main`).

   🚨 **LAZY-LOAD SCROLL then SCROLL TO TOP — TWO mandatory steps, in order:**

   **Step A — slow scroll through the entire page (MANDATORY — triggers lazy/virtual DOM rendering):**
   ```
   mcp__{serverName}__browser_evaluate({
     function: `() => new Promise(r => {
       let h = 0;
       const t = setInterval(() => {
         window.scrollBy(0, 300);
         h += 300;
         if (h >= document.body.scrollHeight) {
           clearInterval(t);
           window.scrollTo(0, 0);
           setTimeout(r, 500);
         }
       }, 150);
     })`
   })
   ```
   **Why:** Angular, React, and virtual-scroll frameworks (Angular CDK, AG Grid, ngx-datatable) only render DOM nodes when they enter the viewport. If you skip this scroll, any element below the fold simply does not exist in the DOM — the probe cannot find it, cannot measure it, and will NOT report it. This is the root cause of "only top-of-page issues detected".

   **Step B — scroll back to top (MANDATORY for bbox accuracy):**
   - `mcp__{serverName}__browser_evaluate("window.scrollTo(0,0)")`
   - `mcp__{serverName}__browser_wait_for({ time: 300 })`

   **Why:** `getBoundingClientRect()` is viewport-relative. If the page is scrolled when probes run, every `bbox.y` is offset by `scrollY` — annotations land on the wrong element in the fullPage screenshot (which always starts from document y=0). Scroll=0 makes viewport coords equal document-absolute coords.

   🚨 **Step C — WAIT-FOR-DATA-READY (MANDATORY for SPA pages, prevents the "no records found" false positive on pages that load fine manually):**

   The fixed 1500ms `post_navigate_settle_ms` is too short for data-heavy SPA dashboards (Angular/React/Vue) — REST API calls + Angular zone.js + change detection commonly take 2–4 seconds. If you skip this step, probes see the page DURING its loading state, the table is empty, and your tools emit dozens of false "no data" / "empty state" findings on pages that actually have data.

   Poll up to `data_ready_max_ms` (default 8000ms) until ANY of these is true:

   ```
   mcp__{serverName}__browser_evaluate({
     function: `() => {
       // (a) Loading indicators are GONE — page finished its fetches
       const stillLoading = document.querySelector(
         '[aria-busy="true"], .loading:not(.loading-text), .spinner:not(.spinner-icon), ' +
         '.skeleton, .skeleton-loader, mat-progress-bar, mat-progress-spinner, ' +
         '[class*="loading-spinner"], [class*="skeleton"]'
       );
       if (stillLoading) {
         const cs = getComputedStyle(stillLoading);
         if (cs.display !== 'none' && cs.visibility !== 'hidden' && stillLoading.getBoundingClientRect().width > 0) {
           return { ready: false, reason: 'still loading' };
         }
       }
       // (b) Data IS present — at least one tbody row or list item with real text
       const rowSel = 'tbody tr, [role="row"]:not([role="rowheader"]), li[class*="row"], li[class*="item"], [class*="list-item"]';
       const realRows = [...document.querySelectorAll(rowSel)].filter(r => {
         const t = (r.innerText || '').trim();
         return t.length > 0 && r.getBoundingClientRect().height > 8;
       });
       if (realRows.length > 0) return { ready: true, reason: 'rows present' };
       // (c) Explicit empty-state message rendered ("No records found", "No data", etc.) —
       //     the page reached its final state, just happens to be empty
       const emptyMsg = [...document.querySelectorAll('p, span, div, h2, h3, h4')]
         .find(el => /no\s+(records?|data|results?|items?|entries|matches?)\s+(found|available)?|empty\s+list|nothing\s+found|0\s+results?/i.test((el.innerText || '').trim()));
       if (emptyMsg) return { ready: true, reason: 'empty-state shown' };
       // (d) Error state visible — page failed but reached terminal state
       const errMsg = [...document.querySelectorAll('p, span, div, [role="alert"]')]
         .find(el => /(error|failed|something\s+went\s+wrong|unable\s+to\s+load)/i.test((el.innerText || '').trim().slice(0, 60)));
       if (errMsg) return { ready: true, reason: 'error state' };
       return { ready: false, reason: 'no data yet, no empty/error state' };
     }`
   })
   ```

   Polling protocol:
   - Initial wait: 400ms (let the framework dispatch the fetch).
   - Then evaluate every 400ms, max `data_ready_max_ms / 400` attempts.
   - Stop on `ready: true`.
   - If still not ready at the cap, proceed anyway (some pages legitimately have no data and no empty-state message — better to scan a partial page than infinite-wait).
   - Log: `[worker] cell {cell.id} data-ready: {reason} after {elapsed}ms`.

4. **Take base screenshot BEFORE probes** (MUST use fullPage: true — NEVER omit this flag):
   ```
   mcp__{serverName}__browser_take_screenshot({
     filename: "{ABSOLUTE-project-root}/.tmp/{runId}/screenshots/{cell.id}-base.png",
     fullPage: true
   })
   ```
   🚨 `fullPage: true` is NON-NEGOTIABLE. Without it the screenshot captures only the visible viewport (~900px tall). The annotated PNG will be missing everything below the fold and devs will see a partial page with boxes pointing at nothing. Always `fullPage: true`.

4b. **🪙 LOAD THE PROBE BUNDLE INTO THE PAGE (BUG 1/2 fix — do this ONCE per cell, BEFORE probing):**
   The 271KB of probe source lives in `{project-root}/.tmp/{runId}/probes-inject.js` (written by `bundle-probes.cjs`). Load it INTO THE PAGE so the probe code is held by the BROWSER, never read into your context:
   ```
   mcp__{serverName}__browser_run_code_unsafe({ code: `await page.addScriptTag({ path: "{ABSOLUTE-project-root}/.tmp/{runId}/probes-inject.js" })` })
   ```
   This defines `window.__ARGUS_PROBES` in the page (the full probe library + `runPassive`/`runInteractive` batch helpers). 🚨 You do NOT read `skill-probes.json` into your context — only the slim `skill-names.json` (a few KB, names + flags) for filtering/receipts. Reading the 271KB bundle into context was the ~68k-tokens-per-worker bug.

4c. **PAGE SCOUT — run ONCE per cell, AFTER bundle load (mandatory fingerprint step):**

   The bundle is now loaded (step 4b), so `window.__ARGUS_PROBES.runScout()` is available. Call it now:
   ```
   fingerprint = mcp__{serverName}__browser_evaluate({
     function: `() => window.__ARGUS_PROBES.runScout()`
   })
   ```
   🚨 Do NOT read `skills/qa-page-scout/SKILL.md` at runtime — that violates T4. The scout is compiled into the bundle by `bundle-probes.cjs`.
   Log: `[worker {chunkIndex}] scout {cell.id}: hasForms=${fingerprint.hasForms} hasTables=${fingerprint.hasTables} hasImages=${fingerprint.hasImages} hasNavigation=${fingerprint.hasNavigation} ...`

   The fingerprint is passed to `runPassive()` and `runInteractive()` as `ctx.fingerprint`. Skills whose `requires: [flagA, flagB]` frontmatter has NO matching true flag in the fingerprint are auto-skipped by the inject bundle (marked `{skipped:'scout'}` in the receipt — NOT an error, NOT a finding). Skills with `requires: []` always run.

   **Why this matters:** A login page has no tables, no drag-drop, no charts, no RTL. Without the scout, `runPassive` still calls all 63 passive probes on it. With the scout, ~40 of them are skipped in-page before any DOM query runs. ~77% token reduction per cell on simple pages.

5. **Run ALL passive probes in ONE TINY call — you send a one-liner, NOT probe source (BUG 1/2/3):**
   ```
   probeResult = mcp__{serverName}__browser_evaluate({
     function: `() => window.__ARGUS_PROBES.runPassive("{cell.viewportClass}", { route: "{cell.route}", properNouns: {properNounsJson}, fingerprint: {fingerprintJson}, leaderViewport: "{leaderViewport}" })`
   })
   // {fingerprintJson} = JSON.stringify(fingerprint) from step 3b above
   // {leaderViewport} = the run's leader viewport class, given to you by the orchestrator in your dispatch
   //   prompt (the first of mobile→tablet→laptop→desktop present this run; normally "mobile"). It makes
   //   the bundle run each viewportSensitive:false skill ONCE — on the leader cell — instead of on all 4
   //   viewports (an invariant bug is identical at every width). vs:true skills still run on every viewport.
   //   If for any reason you weren't given {leaderViewport}, pass your own "{cell.viewportClass}" (no gating).
   ```
   The page already has every probe (from step 4b), so this single call runs ALL applicable passive probes in-page and returns the compact `{ skillName: findings[] }` object. **No probe code rides in this call.** That is the whole fix: ~68k tokens of probe source → a 1-line call.
   Log: `[worker {chunkIndex}] cell {cell.id} — runPassive returned {Object.keys(probeResult).length} skill results`

5b. **Dump the probe RECEIPT immediately (MANDATORY — this is the coverage evidence).** Write the FULL `probeResult` object — every skill key, including ones that returned `[]` or `{error}` — to `{project-root}/.tmp/{runId}/issues/{cell.id}-probes.json` (use the Write tool, NOT an `issues/*.jsonl` file):
   ```
   Write("{project-root}/.tmp/{runId}/issues/{cell.id}-probes.json", JSON.stringify(probeResult))
   ```
   This file is the ONLY proof that each passive skill actually executed on this cell. `scripts/coverage-gate.cjs` reads it: a skill whose key is present = ran (covered); a skill whose key is absent = never ran (silent skip → re-dispatched). Skills skipped by the page scout have value `{skipped:'scout'}` — these ARE covered (intentional skip based on page fingerprint, not a missing run). If you skip this dump, the gate treats the entire cell as uncovered and re-runs it. You CANNOT fake coverage by editing the ledger — only a real receipt with the skill's key counts.

7. **Run ALL interactive probes in ONE TINY call (BUG 1/2/3) — again, you send a one-liner, not probe source:**
   ```
   interResult = mcp__{serverName}__browser_evaluate({
     function: `async () => await window.__ARGUS_PROBES.runInteractive("{cell.viewportClass}", {fingerprintJson})`
   })
   // {fingerprintJson} = JSON.stringify(fingerprint) from step 3b — same fingerprint passed to both
   ```
   The page already has every interactive probe (from step 4b). This single awaited call runs ALL applicable `executable` interactive probes in-page (search/sort/crud/forms/tabs/modal/…), each self-restoring page state, and returns `{ skillName: findings[] }`. **No probe code, no 38 separate calls.** That is the BUG 3 fix.
   - **`executable: partial`** skills: after `runInteractive`, perform ONLY the few extra MCP steps in that skill's "## MCP steps (...)" section (a real `browser_resize`/`browser_navigate`/`browser_file_upload`/`browser_drag` the page-probe can't do).
   - **Non-callable / legacy** skills (those with `probeCallable:false` in `skill-names.json`, e.g. `qa-review-content`, `qa-test-cases`): drive their MCP/judgment sequence the legacy way — they are NOT in the injected bundle.

7b. **Dump the interactive RECEIPT (MANDATORY — coverage evidence for the 35 interactive skills).** Write `{project-root}/.tmp/{runId}/issues/{cell.id}-interactive.json` (Write tool) with ONE key per interactive skill in `applicableSkills` — including ones that self-skipped:
   ```
   { "qa-form-validation": {"ran":true,"interacted":true,"findings":3},
     "qa-test-data-controls": {"ran":true,"interacted":false,"findings":0,"skipReason":"no table/filter/search on page"},
     "qa-detect-reflow": {"ran":true,"interacted":true,"findings":1}, ... }
   ```
   `scripts/coverage-gate.cjs` reads this: an interactive skill whose key is present = ran (covered); absent = never driven → re-dispatched. Every interactive skill applicable to this cell MUST have a key here, just as every passive skill must have a key in `{cell.id}-probes.json`. Together the two receipts prove all 92 skills were executed on this cell.

7c. **🚨 CONSOLE + NETWORK RUNTIME ERRORS — LAPTOP CELL ONLY (MANDATORY on the laptop cell — these 2 skills are NOT in the inject bundle, so the in-page batch CANNOT produce them; you MUST drive them here via MCP or they are missed).** `qa-detect-console-errors` and `qa-detect-network-errors` are now `applyOn:[laptop]` (console/network/runtime errors are viewport-invariant, and the full laptop layout renders the most components and fires the most requests, so it surfaces the most — the collapsed mobile view catches fewer). **If `cell.viewportClass !== 'laptop'`, SKIP this entire step 7c** — no console/network capture, no receipt keys; the coverage gate does not expect these two skills off the laptop cell. On the laptop cell, run them AFTER the interactive phase (errors fire on load AND on interaction):

   **A. Console errors** — read BOTH sources and merge:
   ```
   consoleMsgs = mcp__{serverName}__browser_console_messages({ onlyErrors: true })   // Playwright-captured console.error + pageerror (uncaught), incl. load-time
   injected    = mcp__{serverName}__browser_evaluate("() => window.__argusErr || []") // rejections + CSP from the Step 1 addInitScript collector
   ```
   Merge the two arrays. For each entry, classify by `kind`/`text` and attribute origin:
   - `kind === 'CSPViolation'` (or text has `securitypolicyviolation`) → **CSPViolation**
   - text matches `/Uncaught \(in promise\)/` OR `kind === 'PromiseRejection'` → **PromiseRejection**
   - else first `\b(TypeError|ReferenceError|SyntaxError|RangeError|URIError|EvalError)\b` in the text → that kind
   - else → **ConsoleError**
   - **third-party** = the message's source URL host ≠ the page host (`new URL(baseUrl).host`); e.g. analytics / CDN / `chrome-extension://`. first-party = same host or no host.

   Map → issueType + severity, then **bucket by issueType (ONE finding per issueType, count + up to 3 sample messages in the description — never one ticket per duplicate):**
   | condition | issueType | severity |
   |---|---|---|
   | any third-party origin | `thirdPartyError` | low |
   | CSPViolation (first-party) | `cspViolation` | medium |
   | PromiseRejection (first-party) | `unhandledRejection` | high |
   | TypeError/ReferenceError/… (first-party) | `uncaughtException` | high |
   | other console.error (first-party) | `consoleError` | high |

   Finding shape: `{ issueType, severity, selector:null, evidenceType:"console", description:"{n} {issueType} on {route}: [{kind}] {firstMsg} (+{n-1} more)" }`. Emit NOTHING if there were no error messages.

   **B. Network errors** — read the request log:
   ```
   reqs = mcp__{serverName}__browser_network_requests()
   ```
   For each entry: response `status >= 500` → `httpError` (**critical**); `status >= 400` → `httpError` (**high**); a failed request (no response / `requestfailed`) → `requestFailed` (**high**). Dedup by `url`+`status`. Skip same-status noise from third-party beacons if obviously analytics. Finding shape: `{ issueType, severity, selector:null, description:"HTTP {status} response for: {url}" }` or `"Request failed ({failure}): {url}"`.

   **C. Write + receipt (CRITICAL for coverage):** append A+B findings to the cell JSONL in step 8, AND **merge the two skill keys into the existing `{cell.id}-probes.json`** (re-read it, add `"qa-detect-console-errors"` and `"qa-detect-network-errors"` keys set to their findings array — or `[]` when clean — then re-write). Without these keys, `coverage-gate.cjs` treats both skills as never-run and the gate stays INCOMPLETE. A clean page legitimately yields `[]` for both — that still counts as covered.

7d. **🚨 REMAINING NON-INJECT SKILLS (MANDATORY for full 80/80 coverage — drive ONLY on the gated viewport so cost stays bounded; each one is `viewportSensitive:false` → run once per route on its leader cell, NOT on all 4).** All of these are absent from the inject bundle, so the in-page batch cannot produce them. Gate by `cell.viewportClass`:

   **— On the `mobile` cell ONLY (route leader for `viewportSensitive:false` skills):**

   • **qa-detect-orientation-flip** (issueTypes: `landscapeOverflow`, `landscapeContentHidden`, `orientationLosesState`, `orientationNoHandler`): record `{w,h}`; `browser_resize(h, w)` (swap to landscape); `browser_evaluate(() => window.__ARGUS_PROBES.runPassive("mobile",{route}))` and keep only NEW `horizontalOverflow`/clipped results not present in portrait → emit as `landscapeOverflow` / `landscapeContentHidden` (medium); `browser_resize(w, h)` to restore. Interactive receipt key.

   • **qa-detect-fluid-sweep** (issueType: `fluidOverflowAtWidth`): for `w in [320,600,900,1100,1440,1920]`: `browser_resize(w, currentH)` → `browser_evaluate` the overflow check `(() => { const de=document.documentElement; return de.scrollWidth > de.clientWidth + 2; })`. For any width that overflows (especially the in-between 600/900/1100), emit ONE `fluidOverflowAtWidth` (medium) `"horizontal overflow at {w}px (between standard breakpoints)"`. Restore original width. Interactive receipt key.

   *(content/spelling skills — `qa-detect-content-patterns`, `qa-review-content`, `qa-review-hidden-text` — moved to the `laptop` cell below: page text/content is fullest on the laptop layout, not the collapsed mobile view where the hamburger/sidebar hide nav + content.)*

   **— On the `laptop` cell ONLY:**

   • **qa-detect-content-patterns** (passive; issueTypes incl. `encodingMojibake`, `untranslatedKey`, `htmlEntityLiteral`, `markdownLiteral`, `commonTypo`): run ONE deterministic in-page scan — `browser_evaluate` over visible text nodes for: `�`/mojibake → `encodingMojibake`; a bare i18n key pattern `^[a-z][\w]*\.[\w.]+$` rendered as text → `untranslatedKey`; literal `&amp;`/`&lt;`/`&nbsp;` shown on screen → `htmlEntityLiteral`; literal `**bold**` / `__` markdown → `markdownLiteral`; `lorem ipsum` / `TODO`/`FIXME` → the skill's leak issueType. Emit verbatim, one finding per distinct issueType (count + sample). This is pure pattern-match — do NOT judge style. Passive receipt key (merge into `{cell.id}-probes.json`).

   • **qa-review-content** (Sonnet — YOU are a Sonnet worker, so review directly; issueTypes: `spellingError`, `grammarError`, `wordChoice`, `awkwardPhrasing`, `capitalizationInconsistency`, `punctuationError`): `browser_evaluate(() => document.body.innerText.slice(0,4000))`. Flag ONLY unambiguous errors; SKIP any token in `resolvedConfig.content.proper_nouns`; if uncertain, skip. One finding per distinct error with the exact snippet — **never invent**. Interactive receipt key.

   • **qa-review-hidden-text** (Sonnet; same issueTypes, but for non-visible text): `browser_evaluate` collecting all `alt` / `title` / `placeholder` / `aria-label` / `<option>` text. Apply the SAME strict spell/grammar check (proper-noun-aware, no invention). Interactive receipt key.

   • **qa-test-cases** (applyOn `[laptop]`): if `{project-root}/.claude/qa-test-cases.md` does NOT exist → interactive receipt key `{"ran":true,"interacted":false,"skipReason":"no qa-test-cases.md defined"}` (a legit precondition-absent skip). If it exists, drive each listed scenario via MCP and emit pass/fail.

   **— On the `mobile` AND `tablet` cells (viewport-parity needs cross-cell data):**

   • **qa-detect-viewport-parity**: it compares desktop-vs-mobile feature sets, which one cell cannot do. Dump a feature fingerprint to `{project-root}/.tmp/{runId}/issues/{cell.id}-parity.json`: `{ route: "{cell.route}", viewportClass, navItems: <count of visible nav links>, tableCols: <max visible table header cells>, actionButtons: <count of visible buttons in toolbars/rows> }` (one `browser_evaluate`). Mark the interactive receipt key `{"ran":true,"interacted":true,"skipReason":"cross-viewport — compared by scripts/check-viewport-parity.cjs post-pass"}`. The orchestrator's post-pass reads all `*-parity.json`, compares the desktop/laptop fingerprint to mobile, and emits `featureHiddenOnSmallViewport` where a column/action present on desktop is absent on mobile.

   On tablet/laptop/desktop cells NOT listed above, these skills are correctly **not applicable** (their leader is another viewport) — do nothing and do not add their keys; the gate does not expect them there.

8. Write findings to `{project-root}/.tmp/{runId}/issues/{cell.id}.jsonl` (one JSON object per line).

   **🚨 VERBATIM OUTPUT — NEVER FABRICATE (mandatory, no exceptions):**
   Each finding you write MUST be the EXACT object the probe returned. You are a transcriber, not an author. For every probe result object, copy these fields BYTE-FOR-BYTE from the probe's return value:
   - `issueType` — copy exactly. NEVER invent a new one. If the probe returned `horizontalOverflow`, write `horizontalOverflow` — not `elementOverflow`, not `elementExceedsViewport`. If the probe returned `smallTapTarget`, do NOT write `smallTouchTarget`. If it returned `buttonNoName`, do NOT write `unlabelledButton`. Renaming an issueType IS fabrication.
   - `description` — copy the probe's `description` string verbatim. NEVER paraphrase, summarize, embellish, or add facts the probe did not state. The probe says `Image failed to load: {url}` → write that exactly. Do NOT add "(404)", "not found", "naturalWidth=0", "in sidebar", or a page name — the probe never measured those, so asserting them is inventing evidence.
   - `selector` — copy exactly.
   - `bbox` — copy the probe's numeric bbox exactly. NEVER reuse a bbox from another cell, NEVER template a constant box, NEVER guess coordinates. If two cells show the identical bbox, you fabricated it.
   - `severity` — copy exactly.

   You add ONLY the envelope fields the probe cannot know: `runId`, `cellId`, `route` (= the VERIFIED actual path from step 2, not the intended route), `viewport`, `viewportClass`, `browser`, `screenshotPath`. Nothing else.

   If a probe returned `{ error: ... }` for a skill, that skill found nothing fileable on this cell — write NO finding for it. Do not turn an error into an issue. Do not write a finding for a skill that returned an empty array.

   A downstream gate in `file-bugs.cjs` rejects any finding whose `issueType` is not one the skill's probe can emit (loaded from `skill-probes.json → skills[].issueTypes`). Fabricated findings will be dropped and logged — so inventing them wastes the run and produces nothing. Emit only what the probe actually returned.

7. **Annotate immediately after writing JSONL:**
   `node "{project-root}/scripts/annotate-cell.cjs" "{runId}" "{cell.id}"`

8. Cross-skill dedup (in-worker, no MCP call).

9. Stream progress:
   ```
   [worker {chunkIndex}] cell {n}/{cells.length} {route} @ {viewport}/{browser} → {findingsCount} findings
   ```

10. Honor timeout: wrap the whole cell in a budget timer. If `cell_total_ms` exceeded:
   - Append `{ issueType: "cellTimeout", severity: "low", description: "Cell exceeded {N}ms budget" }` to JSONL
   - Skip to next cell

### Step 3 — Release browser

When all your cells are done (or on fatal error), optionally close your browser:
```
mcp__{serverName}__browser_close()
LOG: "[worker {chunkIndex} on {serverName}] done — {processedCount}/{cells.length} cells"
```
(Closing is optional — the MCP server reuses the browser next run. Closing frees RAM sooner when running 4 headed windows.)

### Step 4 — Return

Return a summary to the parent orchestrator:
```json
{
  "workerIndex": <chunkIndex>,
  "serverName":  "<your assigned MCP server>",
  "loginFailed": <bool>,
  "cellsProcessed": <number>,
  "cellsSkipped":   <number>,
  "cellsTimedOut":  <number>,
  "findingsTotal":  <number>
}
```

The parent orchestrator collects these N summaries when all parallel Agent calls return, prints an aggregate, then continues to Step 5.7.5 (annotation sweep) and Step 7 (bug filing).

## Limitations & honesty

- **True parallelism = one browser per (engine × viewport).** `.mcp.json` declares a server for each combination (`playwright` = chromium-desktop primary; `pw-{engine}-{viewport}` for the rest), each `@playwright/mcp --isolated --browser {engine}` (headed by default). `qa-preflight` regenerates `.mcp.json` to match your `browsers × viewports` selection: chromium → 4 windows, +webkit → 8, all three → 12. Each worker resizes its own browser to its viewport and audits all routes there, concurrently with the others.
- **If only the single `playwright` server is present** (user didn't update/restart), workers fall back to TABS in one shared browser — ~2-4× I/O-overlap speedup, not separate windows. The orchestrator detects this at Step 5.0 (`availableServers`) and caps `activeWorkers` accordingly.
- **Pool size caps the worker count.** `activeWorkers = min(workers, availableServers)`. To run more than 4 dedicated browsers, add more `playwright-wK` entries to `.mcp.json` and restart. Note: each headed browser uses real RAM/CPU — 4 is a sensible default; 8–12 headed windows is heavy.
- **Each browser is isolated** (`--isolated`), so every worker logs in independently (Step 1). No shared session.
- **Workers do NOT share findings.** Each worker writes to its own cell JSONL files; the parent merges by globbing the issues directory. There's no shared state.
- **Failures are isolated.** If worker 2 crashes, workers 0, 1, 3 keep running. Their findings are preserved.

## What this skill is NOT

- NOT a detection or test skill — does not emit issueTypes of its own.
- NOT viewport-pinned — handles all viewports its assigned cells require.
- NOT called outside qa-argus Step 5.1 — never invoke this manually.
