---
name: jsgui3-lab-experimentation
description: Use repo lab experiments (src/ui/lab) to answer jsgui3 “how should we do this?” questions, then distill the validated result into durable docs + Skills.
---

# jsgui3 Lab Experimentation

## Scope

- Run existing lab experiments to confirm behavior (event delegation, activation, MVVM, mixins, helpers)
- Create minimal new lab experiments when encountering unknown or disputed jsgui3 behavior
- Promote stable findings into the repo memory system (Skills + Patterns/Lessons + guides when appropriate)

## Inputs

- The question you’re trying to answer (1 sentence)
- The target surface (control/server route/activation path/event semantics/perf)
- Whether you need SSR-only, client activation, or browser semantics (delegation/bubbling)

## Procedure

1. Inventory prior art
   - Search docs first: `node tools/dev/md-scan.js --guide --search "<topic>" --json`
   - Then search sessions: `node tools/dev/md-scan.js --dir docs/sessions --search "<topic>" --json`

2. Check whether a lab experiment already covers it
   - Open lab index: `src/ui/lab/README.md`
   - Open manifest: `src/ui/lab/manifest.json`
   - Optional: render the Lab Console card list (quick sanity): `node src/ui/lab/checks/labConsole.check.js`

3. Run the smallest relevant check(s)
   - Each experiment should have a `check.js` (or `check.all.js`) that exits cleanly.
   - Prefer targeted runs, e.g.:
     - `node src/ui/lab/experiments/002-platform-helpers/check.js`
     - `node src/ui/lab/experiments/004-theme-mixin/check.js`

4. If the answer is still unclear, create a minimal new experiment
   - Create `src/ui/lab/experiments/NNN-short-slug/`
   - Add `README.md` (hypothesis + expected result) and `check.js` (deterministic assertions)
   - Add an entry to `src/ui/lab/manifest.json` and the table in `src/ui/lab/README.md`

5. If the behavior touches event semantics, run the delegation suite
   - Use the shared runner (reuses one browser/page):
     - `node src/ui/lab/experiments/run-delegation-suite.js --scenario=005,006`
   - Add/adjust scenarios if your change affects capture/bubble/selector matching/stopPropagation.

6. If the behavior requires SSR + client activation + real interactivity, run a Puppeteer scenario suite
    - Use the scenario suite runner (single browser, many scenarios):
       - `node tools/dev/ui-scenario-suite.js --suite=scripts/ui/scenarios/control-harness-counter.suite.js`
    - This is the recommended fast path for validating control activation wiring (DOM linking, event listeners, state updates)
       without paying the cost of full Jest/Puppeteer E2E per test.
    - Prefer this over adding more “JS-only DOM semantics” scenarios when what you really need is jsgui3 activation behavior.

7. Distill the validated finding into durable memory
   - Create/extend a Skill (this registry): `docs/agi/SKILLS.md`
   - Add/extend a Pattern if it’s broadly reusable: `docs/agi/PATTERNS.md`
   - Write a guide if it’s a subsystem-level discovery: `docs/guides/…`
   - Record evidence + commands in the current session directory under `docs/sessions/...`

## Validation

- Lab console renders: `node src/ui/lab/checks/labConsole.check.js`
- Run the specific experiment check(s) you relied on (examples):
  - `node src/ui/lab/experiments/001-color-palette/check.js`
  - `node src/ui/lab/experiments/002-platform-helpers/check.js`
  - `node src/ui/lab/experiments/004-theme-mixin/check.js`
- If delegation/event semantics are involved:
  - `node src/ui/lab/experiments/run-delegation-suite.js --scenario=005,006,007,008,011,014`

- If you need SSR + activation + browser interaction coverage:
   - `node tools/dev/ui-scenario-suite.js --suite=scripts/ui/scenarios/control-harness-counter.suite.js`

## Escalation / Research request

Ask for dedicated research if:

- A behavior only reproduces with SSR + activation + bundling and no existing lab harness covers it
- A change appears to require new shared harness utilities (browserHarness / activation harness)
- The experiment needs performance instrumentation (counts, timings, memory) beyond a simple check

## References

- Lab index: `src/ui/lab/README.md`
- Lab manifest: `src/ui/lab/manifest.json`
- Delegation suite runner: `src/ui/lab/experiments/run-delegation-suite.js`
- Puppeteer scenario suites guide: `docs/guides/PUPPETEER_SCENARIO_SUITES.md`
- Pattern: “Lab-First jsgui3 Knowledge Gap Closure” in `docs/agi/PATTERNS.md`
 - General experimental research SOP: `docs/agi/skills/experimental-research-metacognition/SKILL.md`
