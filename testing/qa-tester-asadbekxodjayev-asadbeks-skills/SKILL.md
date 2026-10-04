---
name: qa-tester
description: >
  Comprehensive QA testing of web/mobile apps: detects new, changed, and untested
  features via git history and a persistent test ledger, then tests them through
  static code analysis AND live runtime testing with a browser harness that captures
  console errors, network failures, runtime exceptions, and screenshots of every
  page, section, modal, and UI state for visual bug hunting. Use this skill whenever
  the user asks to "test the app", "QA this", "find bugs", "check for UI issues",
  "verify the new feature works", "regression test", "check console errors",
  "review network requests", or after any feature is implemented/modified and needs
  verification — even if they don't explicitly say "QA". Also use when the user asks
  "what hasn't been tested yet" or wants a bug report.
---

# QA Tester

A full QA workflow: figure out **what** to test, test it **three ways** (static code review, instrumented runtime run, visual screenshot review), and produce an evidence-backed bug report. A persistent test ledger remembers what was tested at which commit, so re-runs focus only on new, changed, or previously-failed features.

## Always paired with `qa-automation-engineer` (REQUIRED — both directions)

qa-tester and `qa-automation-engineer` are two halves of one QA system and **run
together no matter which one is invoked**:

- Invoked as **qa-tester** ("test the app / find bugs / QA this") → this runtime +
  visual bug hunt is the *evidence engine*. Immediately co-invoke
  `qa-automation-engineer` so findings feed the durable test pyramid
  (unit · component · integration · e2e · a11y) and the CI gate, and so the run
  publishes to a local **Allure** report (Step 6).
- Invoked as **qa-automation-engineer** (architecture/setup) → it co-invokes
  qa-tester for the runtime/visual layer (already in its bundle).

Net: a qa-tester pass never stops at a markdown report alone, and a
qa-automation-engineer pass never skips real runtime bug-hunting. Announce the
pairing up front.

## The workflow at a glance

```
1. SCOPE      → what needs testing? (ledger + git diff)
2. STATIC     → read the code, find potential bugs before running anything
3. RUNTIME    → run the app + browser harness (console, network, JS errors, screenshots)
4. VISUAL     → examine every screenshot for UI flaws
5. REPORT     → severity-ranked bug report with evidence + update the ledger
6. ALLURE     → publish the evidence to a local Allure report (+ Playwright e2e)
```

Run all six steps for a full QA pass. If the user asks for something narrower ("just check console errors on the dashboard"), run only the relevant steps — but always update the ledger at the end so coverage tracking stays accurate.

---

## Step 1 — Scope: decide what to test

The skill maintains a test ledger at `qa/test-ledger.json` in the project root. It records every feature/route/component tested, the commit hash at test time, the result, and open bugs.

Run the ledger tool to compute scope:

```bash
python <skill_path>/scripts/ledger.py scope          # what needs testing now
python <skill_path>/scripts/ledger.py status         # full coverage overview
```

`scope` cross-references the ledger against `git log` / `git diff` and returns three buckets:

- **NEW** — features/files never recorded in the ledger (added since last QA pass)
- **CHANGED** — features previously tested, but their source files changed since the recorded commit → must be **retested**
- **UNTESTED** — known features with no ledger entry at all

If there is no ledger yet (first run), do a discovery pass: enumerate the app's routes, pages, modals, and major components by reading the router config, page directory (`pages/`, `app/`, `src/screens/`, `lib/screens/`), and navigation code. Seed the ledger with `ledger.py init` and treat everything as UNTESTED.

Confirm the scope with the user **only** when it's very large (e.g., >15 features on a first run) — offer to prioritize. Otherwise just proceed.

## Step 2 — Static analysis: find bugs by reading the code

Before running anything, read the source of every in-scope feature and hunt for defects. Read `references/static-analysis.md` for the full checklist. The high-yield categories:

- **Error handling**: unhandled promise rejections, missing try/catch around fetch/IO, empty catch blocks, errors swallowed without user feedback
- **Network**: no handling for 4xx/5xx, no timeout, no retry where it matters, response shape assumed without validation, race conditions on rapid navigation (stale responses overwriting fresh state), missing request cancellation
- **State/UI logic**: missing loading states, missing empty states, missing error states, derived-state bugs, stale closures, off-by-one in pagination
- **UI/layout risks** (visible in code): hardcoded widths/heights, text that will overflow with long strings or other locales, missing `key` props, z-index conflicts, fixed positioning that breaks on mobile, images without dimensions (layout shift)
- **Forms**: validation gaps, no disabled state during submit (double-submit), error messages not shown per-field
- **i18n**: hardcoded user-facing strings, untranslated keys, date/number formats not locale-aware
- **Security smells**: secrets in client code, `dangerouslySetInnerHTML`/`innerHTML` with user data, missing auth checks on routes
- **Accessibility**: missing alt text, unlabeled inputs, click handlers on non-interactive elements

Log every finding as a **potential bug** (to be confirmed or upgraded at runtime). Findings that can't manifest at runtime in the current build (e.g., dead code) still go in the report at low severity.

## Step 3 — Runtime testing: run the app under instrumentation

### 3a. Start the app

Detect and use the project's own dev command (`npm run dev`, `flutter run -d chrome`, `go run ./cmd/server`, etc.). Start it in the background, wait for the port to respond, and capture the **server-side logs** too — backend errors during testing are findings.

### 3b. Run the browser harness

The bundled harness (`scripts/qa_browser.mjs`, Playwright) visits a list of routes/actions and captures everything:

```bash
cd <skill_path>/scripts && npm install playwright && npx playwright install chromium  # first time only
node <skill_path>/scripts/qa_browser.mjs --config qa/qa-run.json
```

Write a `qa/qa-run.json` describing what to exercise (see `references/runtime-testing.md` for the full config schema and examples). For each target the harness records into `qa/runs/<timestamp>/`:

- **console.json** — every console error/warning with stack traces and the page it happened on
- **network.json** — every request: URL, method, status, duration, response size; flags 4xx/5xx, requests >3s, failed/aborted requests, and non-JSON bodies on JSON endpoints
- **errors.json** — uncaught exceptions and unhandled promise rejections (`pageerror`)
- **screenshots/** — full-page screenshot of every route at desktop (1440×900) and mobile (390×844) viewports, plus per-interaction screenshots (modals opened, forms in error state, dropdowns expanded)

The harness can also execute **interaction scripts** per route: click selectors to open modals, fill and submit forms with both valid and invalid data, trigger hover/focus states, scroll to lazy-loaded sections. Define these in the config so every modal and section gets captured, not just the initial page load. Test the unhappy paths deliberately: submit empty forms, enter oversized/Unicode/RTL strings, navigate while requests are in flight, and (where the config enables it) simulate offline/failed API responses to confirm error states actually render.

If the dev server requires auth, add a login step to the config (`auth` block) so the harness can reach protected pages.

**Non-web apps**: for Flutter mobile, prefer `flutter run -d chrome` for the harness; otherwise use `integration_test` + simulator screenshots (`xcrun simctl io booted screenshot`). For pure backends, skip the browser and test endpoints directly with scripted curl/httpie calls, asserting status codes and response shapes.

### 3c. Triage runtime evidence

Read the harness output files. Every console error, failed request, and uncaught exception is a **confirmed bug** unless clearly benign (e.g., a third-party analytics warning — note it but mark low severity). Match runtime findings against Step-2 potential bugs: a confirmed match upgrades the finding and links the evidence.

## Step 4 — Visual review: examine every screenshot

View each screenshot **yourself** (use the image viewing tool — do not skip this). Read `references/visual-review.md` for the per-screenshot checklist. Look for:

- Overlapping/clipped/truncated elements, text overflow or ellipsis where full text matters
- Broken layout at the mobile viewport: horizontal scroll, squashed columns, unreachable buttons
- Misalignment, inconsistent spacing, inconsistent component styles across pages
- Low contrast text, invisible elements (white on white), broken/missing images or icons
- Empty states that render as blank voids, loading spinners that never resolved (visible in screenshot)
- Untranslated keys (`home.title` showing literally), mixed languages on one screen
- Modal issues: missing backdrop, no close affordance, content overflowing the modal
- Off-brand or visually jarring elements compared to the rest of the app

Compare desktop vs mobile screenshots of the same page side by side. Every visual defect becomes a finding with the screenshot path as evidence.

## Step 5 — Report and update the ledger

Produce the QA report at `qa/reports/qa-report-<date>.md` using `assets/report-template.md`. Rules:

- Every bug gets: **severity** (Critical / High / Medium / Low), **type** (Runtime error / Network / Console / UI-Visual / Logic / A11y / i18n / Security), **feature**, **steps to reproduce**, **evidence** (screenshot path, console/network entry, or file:line), **suggested fix** (concrete, referencing the actual code)
- Severity guide: Critical = data loss, crash, security, blocked core flow · High = feature broken or major visual breakage · Medium = degraded UX, recoverable errors · Low = polish, warnings, minor inconsistencies
- Include a coverage summary: features tested / passed / failed / still untested
- Don't pad: if something passed cleanly, one line in the coverage table is enough

Then update the ledger:

```bash
python <skill_path>/scripts/ledger.py record --feature "<name>" --result pass|fail --bugs <n>
```

`record` stamps the current commit hash automatically, so the next QA run knows these features are covered until their files change again.

Finally, give the user a short summary in chat: bug counts by severity, the 3 worst bugs, and where the full report and screenshots live. Offer to fix the Critical/High bugs — but don't start fixing without confirmation; QA and fixing are separate passes.

## Step 6 — Publish to a local Allure report

The Step 3–4 evidence also publishes to an interactive local **Allure** report, so
the screenshots + console/network/error logs are browsable as HTML (and merge with
the Playwright E2E results owned by `qa-automation-engineer`). Two sources feed the
**same** `allure-results/` directory:

1. **Playwright-native (primary).** When the project has a Playwright suite, the
   `allure-playwright` reporter (wired by `qa-automation-engineer` in
   `playwright.config.ts`, `detail: true`) makes the test runner write native
   *nested* steps, attachments and traces — the runner writes the steps.
2. **Harness bridge.** Convert a `qa/runs/<timestamp>/` harness run into Allure
   results (one test per page × viewport; status from console/HTTP/JS errors;
   screenshots + per-page log slices attached):
   ```bash
   node <skill_path>/scripts/allure-from-run.mjs        # newest run → allure-results/
   node <skill_path>/scripts/allure-from-run.mjs --run qa/runs/<ts> --clean
   ```

Build + serve the local report:

```bash
allure generate allure-results --clean -o allure-report && allure open allure-report
allure serve allure-results        # one-shot: generate to a temp dir + serve
```

`allure` comes from the `allure-commandline` dev dep and needs a local JRE (Java
8+). Keep `allure-results/` and `allure-report/` **gitignored** — they are local,
regenerated artifacts, never committed.

---

## Reference files — read when you reach the relevant step

- `references/static-analysis.md` — full code-review checklist by category, with concrete code smells to grep for (Step 2)
- `references/runtime-testing.md` — qa-run.json config schema, interaction scripting, auth, API mocking/offline simulation, non-web app strategies (Step 3)
- `references/visual-review.md` — per-screenshot inspection checklist and severity calibration for visual bugs (Step 4)

## Scripts

- `scripts/ledger.py` — test ledger: `init`, `scope`, `status`, `record`. Pure stdlib Python.
- `scripts/qa_browser.mjs` — Playwright harness: navigation, interactions, console/network/error capture, multi-viewport screenshots.
- `scripts/allure-from-run.mjs` — Allure bridge: converts a `qa/runs/<ts>/` harness run into Allure 2 results (zero deps, hand-writes the schema) so it renders in the same local Allure report as the Playwright e2e suite (Step 6).

## Principles

- **Evidence over opinion.** Never report a bug without a screenshot, log entry, or file:line to back it.
- **Hunt the unhappy path.** Most bugs live in error states, edge inputs, slow networks, and rapid interactions — not the demo flow.
- **Untested = broken until proven otherwise.** The ledger exists so nothing silently stays untested forever.
- **Changed = untested.** Any source change invalidates prior test results for that feature.
- **Report, then fix.** Keep the QA pass honest by not patching bugs mid-run; the report is the deliverable.
