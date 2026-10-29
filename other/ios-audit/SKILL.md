---
name: ios-audit
description: "Comprehensive iOS audit for Swift and SwiftUI apps. Runs deterministic collectors for Code Health, UX, Runtime Quality, and Release & Compliance, then synthesizes a complete fresh docs tree plus `audit.html`, `audit.json`, and `audit-diff.md`. Explicitly checks state and config provenance, cross-surface semantic consistency, adaptive device-lane coverage, and storage placement and cleanup policy. Use when the user asks to audit an iOS app, baseline engineering quality, generate architecture or UX docs, replace docs with an audit, find ship blockers, produce a release-readiness report, or diff audits across commits. Requires a Swift or SwiftUI Xcode or Tuist project; for UX, a booted simulator plus `ios-simulator-skill`."
---

# iOS Audit

Use this skill to create a reproducible engineering baseline for a Swift or
SwiftUI app. The audit runs four pillars through four phases:

1. **COLLECT** deterministic evidence from source, tools, and optionally a simulator.
2. **ANALYZE** that evidence and author current-run docs and findings for each pillar.
3. **RENDER** a complete docs tree, `audit.json`, and `audit.html`.
4. **DIFF** the new baseline against an earlier one when available.

The outputs are a replacement documentation tree covering architecture, UX,
operations, quality, and release; a JSON baseline with findings, severity,
priority, evidence, and RICE scores; a self-contained HTML report; and, when a
prior baseline exists, `audit-diff.md` with changes since that run. Use it for
refactor baselines, release reviews, recurring health checks, onboarding, and
auditing drift between runs. Use a focused review when the user needs only a
single question answered.

## Choose the run

- With a booted simulator and a UX workflow YAML, run all four pillars.
- Without either UX prerequisite, pass `--no-ux`; Code Health, Runtime Quality,
  and Release & Compliance still run.
- If this is the first run, omit DIFF. The new `audit.json` becomes the baseline.
- Write docs to the app's `docs/` only when the user wants to replace that tree.
  Otherwise use `--docs-dir .audit/docs-preview/` to keep the output isolated.

The CLI is `scripts/audit.py`. Its subcommands are `collect`, `analyze`,
`render`, and `diff`; `all` runs the sequence and pauses after COLLECT so you
can perform ANALYZE. It prints the raw-input and prompt paths, then waits on
STDIN.

## Run the audit

### 1. Prepare inputs

Install `uv`. `swiftlint` and `periphery` are optional, recommended collectors.
For UX flows, prepare a workflow file in the app repository, a booted simulator,
and the `ios-simulator-skill` in the rendered `ios` plugin. Start from
`examples/movies-do.yaml` or `examples/silly-tavern.yaml`; see
[`references/authoring-workflows.md`](references/authoring-workflows.md) for
workflow syntax and selectors.

Use helper-owned simulator UDIDs when available. In a scaffolded project:

```bash
make run-iphone run-ipad
export IOS_AUDIT_IPHONE_UDID="$(jq -er .udid build/simulators/iphone.json)"
export IOS_AUDIT_IPAD_UDID="$(jq -er .udid build/simulators/ipad.json)"
```

Set each `device_matrix` lane's `udid` to the matching environment variable.
For a single lane without `device_matrix`, pass `--udid "$IOS_AUDIT_IPHONE_UDID"`.
Use explicitly assigned simulators in an unscaffolded project; never rely on
whichever simulator happens to be booted.

Workflow credentials must use environment-variable references. Never commit
plaintext credentials. The collector expands `${VAR}` values at runtime and
fails before the flow starts if a referenced variable is unset. For Xcode UI
tests, forward credentials with the `TEST_RUNNER_` prefix (Xcode 15.3+):

```bash
TEST_RUNNER_MY_APP_TEST_USERNAME="$MY_APP_TEST_USERNAME" \
  xcodebuild test -workspace MyApp.xcworkspace -scheme MyApp ...
```

### 2. Collect

Run collectors against the app repository. `--output` is disposable generated
state: each collection removes and regenerates the entire audit root.

```bash
~/.agents/plugins/plugins/ios/skills/ios-audit/scripts/audit.py collect \
  --repo ~/code/my-app \
  --workflows ~/code/my-app/.audit/workflows.yaml \
  --output ~/code/my-app/.audit
```

Omit `--workflows` when UX is not being collected and pass `--no-ux` when
required. Collectors write JSON under `.audit/raw/`: `meta.json`,
`code_health.json`, `ux.json`, `runtime.json`, and `release.json`. Missing
optional tools are recorded as `tool_missing` where supported; they do not
silently produce equivalent evidence.

### 3. Analyze

For every pillar that ran, follow its prompt and create all required outputs:

1. Read `.audit/raw/<pillar>.json` and inspect the current source needed to
   verify its claims.
2. Read `scripts/analyze/prompts/<pillar>.md` before authoring that pillar.
3. Write authored Markdown under `.audit/docs/` in the structure required by
   the prompt. Treat every listed document as required.
4. Write `.audit/findings/<pillar>.json` as an array matching the `findings`
   schema in `audit-schema.json`. Include `id`, `pillar`, `severity`,
   `priority`, `title`, `summary`, `evidence`, `recommendation`, `rice`, and
   `tags` for each finding.

The pillar names are `code_health`, `ux`, `runtime`, and `release`; their
prompts are under `scripts/analyze/prompts/`. Back every claim with the current
raw inputs and source. Author a fresh docs tree for every run: do not reuse
prior audit prose, findings, screenshots, or thumbnails. Include only
current-run UX screenshots and copy every referenced screenshot into
`.audit/docs/` where the UX prompt requires it.

### 4. Render

```bash
~/.agents/plugins/plugins/ios/skills/ios-audit/scripts/audit.py render \
  --audit ~/code/my-app/.audit \
  --docs-dir ~/code/my-app/docs
```

Rendering merges `.audit/docs/`, `.audit/findings/*.json`, and
`.audit/raw/meta.json`. It writes `audit.json`, `audit.html`, and copies the
freshly authored Markdown into `<docs-dir>/`. Rendering fails if required docs,
findings files, or current-run UX screenshots are missing. Resolve those gaps
before proceeding; a partial report is not a completed audit.

### 5. Diff

```bash
~/.agents/plugins/plugins/ios/skills/ios-audit/scripts/audit.py diff \
  --current ~/code/my-app/.audit/audit.json
```

DIFF uses `docs/audit.json` as the default previous baseline, or accepts
`--baseline PATH`. It writes `audit-diff.md` with fixed, new, regressed, and
demoted findings plus the net RICE change. With no previous baseline, it prints
`First audit — no baseline` and exits successfully.

To run the phases together, use `all` with the same project inputs and desired
docs target:

```bash
~/.agents/plugins/plugins/ios/skills/ios-audit/scripts/audit.py all \
  --repo ~/code/my-app \
  --workflows ~/code/my-app/.audit/workflows.yaml \
  --docs-dir ~/code/my-app/docs
```

Python entrypoints include `uv` script metadata and can run directly or through
`uv run path/to/script.py`.

## Pillars and analysis guides

| Pillar | Evidence and focus | Main docs |
|---|---|---|
| **Code Health** | SwiftLint, Periphery, Tuist graph, file inventory, state/config provenance, layer hierarchies, concurrency and error-handling smells | `docs/architecture/*.md`, `docs/quality/*.md` |
| **UX** | Screenshots, accessibility trees, navigation, components, gestures, repeated semantic surfaces, workflow and device-lane coverage | `docs/ux/` |
| **Runtime Quality** | Logging, errors, retries, timeouts, caches, network resilience, storage placement and cleanup | `docs/operations/` |
| **Release & Compliance** | Privacy manifests, plist and entitlement settings, localization, signing, risky APIs, Fastlane | `docs/release/` |

Read the relevant guide in `references/pillars/` for that pillar's evidence,
tool requirements, output list, and common finding patterns. Read its analysis
prompt for the exact document outline and finding rules. The prompt is the
required authoring contract; the guide explains the collector and pillar.

Each finding carries three separate assessments:

- `severity`: `critical`, `major`, `moderate`, or `minor` describes the harm.
- `priority`: `must`, `should`, `could`, or `wont` describes when to address it.
- `rice`: `{reach, impact, confidence, effort, score}` estimates work value;
  `score = (reach * impact * confidence) / effort`.

Use all three. They can disagree, and that disagreement can be informative.
See [`references/priority-model.md`](references/priority-model.md) for scales
and scoring guidance.

## Project files

UX workflow YAML belongs to the app repository, typically at
`.audit/workflows.yaml` or `.audit/flows/*.yaml`. `workflow-schema.yaml` defines
its format, and `examples/` contains full examples. Keep audit-generated files
out of Git except for `.audit/audit.json` when the project intentionally
checks in a baseline. In that case, ignore `.audit/raw/` and `.audit/docs/`.
Store non-audit notes outside a docs tree that the audit will replace. Run
separate audit output roots for separate device or appearance variants.

The analysis prompts define required documentation and finding outputs. The
schema files define their machine-readable formats. The main implementation
lives in `scripts/collect/`, `scripts/render/`, `scripts/diff/`, and
`scripts/ux/`; Python entrypoints are self-contained scripts. See
[`references/migration-from-ios-flow-audit.md`](references/migration-from-ios-flow-audit.md)
when moving an existing caller from the former `ios-flow-audit` skill.
