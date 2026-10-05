---
name: feature
description: >
  Spec-driven feature development with KB-centric workflow.
  Supports any project — discovers KB automatically from sibling directories.
  Manages full cycle: research, spec, implement, verify.
  Use when starting new features, resuming work on existing specs,
  or checking status of in-progress features.
argument-hint: "<new | continue | status> [feature description or spec path]"
user-invocable: true
---

# Feature Development Skill

Spec-driven development using a Knowledge Base (Obsidian vault) as persistent context.
Specs live in `<kb_root>/repos/<project>/design/` so context survives across sessions.

User-input prompt presentation follows the banner convention in
`docs/user-input-banner-convention.md`. Every real decision fork in this
skill uses the generic `AWAITING YOUR INPUT` banner (or the
`APPROVAL REQUIRED` variant for the HARD GATE); status updates do not
carry the banner.

### Caveman activation in this flow

Caveman compression is mandatory in this flow. The wire prefix `[COMPRESSION:terse]` MUST be prepended to every subagent Task description and to every Codex MCP `developer-instructions:` field within this flow. Machine-output payloads (haiku scorer JSON, `render_findings` / `dedupe_findings` IO, parser inputs) are exempt per `skills/caveman/SKILL.md` §7.

## Modes

Parse `$ARGUMENTS` to determine the mode:

| Input | Mode | Action |
|-------|------|--------|
| `new <description>` or bare non-path description | **New** | Research codebase, write spec, get approval |
| `continue [spec-path]` | **Continue** | Resume from last checkpoint in spec |
| bare path to an existing `*.md` file (not prefixed with `new`) | **Continue** | Treat as `continue <spec-path>` |
| `status` or `status --all` | **Status** | Show actionable specs (or everything with `--all`) |
| `checklist <add\|done\|fail\|start-soak\|list> …` | **Checklist** | Manage post-merge items on a SHIPPED spec |
| `verify <spec-path>` | **Verify** | Auto-resolve blockers, flip to VERIFIED if every item is done |
| `extend <description>` | **Extend** | Append a new step to the active spec's Implementation Checklist + workdoc (scope addition) |
| `new <description> --follows-up <spec-path>` | **New (follow-up)** | Like **New**, but links the new spec to a prior one via `follows_up` |
| `discard [spec-path]` | **Discard** | Delete feature branch + set spec DISCARDED (explicit; not tied to hand-off) |
| `grill [spec-path]` | **Grill** | Optional interactive interview gate hardening a DRAFT spec before approval |

**Removed-flag hard-fail** (per `docs/cut-spec-policy.md`). If `$ARGUMENTS` contains `--from-investigation`, hard-stop with `ERROR: --from-investigation was removed in cut spec design/2026-04-27-cut-from-investigation.md. Read that spec for the migration path.` Do NOT route the input through any of the existing modes.

---

## Workflow phases overview

```
1. Research + write spec + exec workdoc  →  user approves spec (HARD GATE)
2. Spec self-review + cross-audit (Claude + Codex)  →  fix if CRITICAL/HIGH
3. Baseline test  →  implement step-by-step with compliance checks per step
   (large multi-step features: opt-in continuous parallel diff-audits — see §Implement)
4. Verify (full test suite)
5. Code audit (cross-auditor mode:full on diff — closed gate, per-finding triage)  →  hand-off (merge / PR / keep / discard)
```

## Confirmation cadence

Once agreed to a direction, drive to completion without re-asking. See `docs/confirmation-cadence.md`.

## Session resume — KB scan

At the beginning of any development session, before doing anything else:
1. Check Claude memory for the KB path for this project
2. If found: scan `<kb>/repos/<project>/design/` for specs with status IN_PROGRESS or AUDIT_PASSED
3. If in-progress work exists: summarise it (feature name, current phase, next step) and ask whether to continue or start something new
4. If nothing in progress: run the research-queue scan (below), then ask what the user wants to work on

Do this proactively — do not wait for the user to ask.

### Research-queue scan (no-in-flight branch)

When step 2 finds no IN_PROGRESS / AUDIT_PASSED specs, the next session is at risk of being blind to a queue published by the prior session's `/research conclude --queue-spec`. Surface those queued specs before declaring "nothing in progress":

- **Scan semantics** (Continue mode is single-project by nature — it routes to a single resolved project): recursively walk `<kb>/repos/<project>/research/` and include every `.md` file at **any depth, including direct children** (depth-0 like `<research>/<slug>.md` — the canonical write path of `/research new` per `skills/research/SKILL.md`). Implementations MUST cover depth-0 and deeper. Examples: `find <root> -type f -name '*.md'`; Python `pathlib.Path(<root>).rglob('*.md')`; bash with `shopt -s globstar` AND explicit dual-pattern `<root>/*.md` + `<root>/**/*.md` to handle direct children. A bare `**/*.md` glob without `globstar` enabled (e.g. macOS system bash 3.2 default) silently misses depth-0 — do NOT spell the contract that way. Status mode uses an all-projects scan — see §Status mode.
- For each matched note, parse the **frontmatter** (NOT body — `queued_specs:` is a frontmatter list per `skills/research/references/research-template.md`). Skip silently when:
  - `status: CONCLUDED` is not set (only CONCLUDED notes publish a stable queue), OR
  - `queued_specs:` is null / missing / empty list.
- Defensive handling for manually-edited frontmatter:
  - If `queued_specs:` is **non-sequence** (string / scalar / mapping / malformed YAML), emit one-line warning `⚠ malformed queued_specs in <note path>: not a YAML sequence` and skip the note.
  - If a list element is **missing required `slug` or `scope`** (or either is empty/whitespace-only), emit `⚠ malformed queued_specs item in <note path>: <reason>` and skip the offending item (continue with valid siblings).
  - If `queued_specs[].slug` fails the validation regex `^[a-z0-9][a-z0-9-]*$` (lowercase ASCII alphanumerics + hyphens; no leading hyphen — same producer-side rule at `skills/research/SKILL.md` §Conclude mode), emit one-line warning `⚠ malformed queued_specs item in <note path>: slug fails validation regex (got <slug>)` and skip the offending item. Closes the producer/reader asymmetry: producer validates at write; reader re-validates at read so a manually-edited frontmatter (e.g. `slug: *` or `slug: real*`) cannot smuggle glob metachars into the materialization-lookup form `<kb>/repos/<project>/design/<YYYY>-<MM>-<DD>-<slug>.md`.
- For each valid item: look up materialization status by matching the canonical date-prefixed form `<kb>/repos/<project>/design/<YYYY>-<MM>-<DD>-<slug>.md` within the SAME project as the source note (literal 4-2-2 numeric date prefix + `-` + the queued slug + `.md` — NOT a bare `*-<slug>.md` glob, which would over-match longer slugs ending in `-<slug>` such as `mandatory-audit-foo.md` matching the queued slug `audit-foo`). Apply the **Materialization status** branching (see §Continue mode for the full table).
- Render the queued items inline in the no-in-flight summary so the user sees the handoff queue before answering "what to work on".

## Phase 0: KB Discovery

KB discovery algorithm (resolving `kb_path` and `project` via `.ai-dev-team.local.yml → .ai-dev-team.yml → memory → sibling → ask`) follows `docs/kb-discovery.md` — single source of truth.

### Feature-skill extensions

Feature skill reads `codex.model` and `codex.reasoning_effort` from the resolved config and passes them through to `developer-codex` / `cross-auditor`.

---

## New: Research + Spec

### Step 1 — Research

Read both KB and codebase before writing anything:

1. Ask Librarian agent (or read directly): `<kb_path>/repos/<project>/design/` for existing specs
2. Read any relevant KB docs: domain context, related project docs, glossary
3. Explore source code in the project directory: understand architecture, existing patterns, files that will change
4. Identify: reusable patterns, files to change, dependencies, risks, what already exists
5. Read AGENTS.md, CLAUDE.md, .github/CONTRIBUTING.md, and README.md §Development/§Contributing/§Testing in the target repo if they exist. Lift any directive placement / naming / layout / branch-style rules verbatim into spec §2 Current State as a 'Repo conventions' subsection (`### 2.X Repo conventions`). After lifting, **reconcile any test-placement / test-layout convention against R5-R7** in `skills/feature/references/code-quality-rules.md`. On conflict, **R7 wins** (sibling-file test layout for new files, even where the repo uses inline): §2 Repo conventions records the prior inline/mixed convention PLUS the R7 override, and the convention-shift line goes in the spec **§7 Log** (`- YYYY-MM-DD: introduced sibling-file test layout per R7; repo previously used inline` per R7 step 3) — NOT in §2 Current State. The reconciled placement then flows into the §5 step + workdoc `allowed_scope` as a concrete sibling test file path. Worked example: when module names are dynamic/generated, scope by **directory** (e.g. `src/foo/` + `src/foo/*_tests.rs`), not just the production file path, so the sibling test file is never silently dropped from `allowed_scope`.

### Step 2 — Write spec and initialize execution workdoc

You (the feature skill orchestrator) write both artifacts directly.

Authoring style: caveman-style per skills/caveman/SKILL.md §8 — see skills/feature/references/kb-authoring-style.md.

**Spec**: create at `<kb_path>/repos/<project>/design/YYYY-MM-DD-<slug>.md`. Create the directory if it doesn't exist. Use the template from `references/spec-template.md`. Key sections:
- **Context** — why this feature exists
- **Current State** — how the system works today (reference KB pages and source files)
- **Design** — changes table, data model, API, configuration
- **Branch** — `<type>/YYYY-MM-DD-<slug>` where `<type>` is the resolved `change_type` (see CLAUDE.md §Contribution flow + `skills/feature/references/developer-workflow.md` §Git Workflow and the change-type prompt below — one of `feat / fix / refactor / ci / docs / test / chore`) (or specify different base if needed)
- **Implementation Checklist** — ordered, concrete steps (each is a reviewable behavioral unit)
- **Verification** — how to test end-to-end
- **Log** — append-only decisions and progress

**Repo-convention enforcement in §5**: if §2 lists a Repo conventions subsection that constrains a checklist step's decision (test placement, file layout, branch naming, commit style, linter format, language version), the corresponding §5 Implementation Checklist step MUST specify the exact placement/value — never 'developer's call' / 'at developer's discretion' / 'as you see fit' / 'at agent discretion'. For test-placement specifically: where a lifted convention conflicts with R5-R7, **R7 wins** — the §5 step uses the sibling-file layout and lists the concrete sibling test file path(s) in the step's `allowed_scope`, and the convention-shift line is recorded in the spec **§7 Log** (not §2). Spec-mode cross-audit (see `agents/cross-auditor.md` §spec mode) flags such ambiguity as HIGH.

YAML frontmatter:
```yaml
---
title: <feature title>
project: <project>
type: spec
status: DRAFT
branch: <type>/YYYY-MM-DD-<slug>
change_type: <type>
created: YYYY-MM-DD
# Optional: project_type gates the security R-rule cluster at code-audit time.
# Allowlist: smart_contract | backend | frontend | data_pipeline.
# Explicit typeless: `none` — declared no applicable allowlist type; loader runs at
#   "all" scope and attests rules_loaded: true (standing acceptance, does not gate).
#   Unset/None stays degraded (rules_loaded: false).
# Resolution chain: spec frontmatter → .ai-dev-team.local.yml → .ai-dev-team.yml → None.
# See references/spec-template.md for the full fallback contract.
# project_type: <smart_contract|backend|frontend|data_pipeline|none>
tags: [spec, <project>]
---
```

**Execution workdoc**: create at `<kb_path>/repos/<project>/design/workdocs/<slug>/exec.md`. Also create `captures/` directory (it will hold test output files written during implementation).

For each checklist step, write a `planned` block in exec.md:
```yaml
## Step N: <step title from checklist>

### Planned
goal: <one sentence — the observable behavioral change>
allowed_scope: <glob for files this step may touch, e.g. src/module/**>
failing_test_cmd: <command to run before implementation — empty if no test>
expected_failure_pattern: <substring expected in failure output>
passing_test_cmd: <command to run after implementation>
expected_pass_pattern: <substring expected in passing output>
integration_probe_cmd: (optional — command to confirm feature is reachable at runtime)
expected_probe_signal: (optional)

### Observed
actual_files_touched: []
commit_shas: []
red_capture: captures/step-NN-red.txt
green_capture: captures/step-NN-green.txt
probe_capture:
notes: ""
```

Leave all `observed` fields empty — the orchestrator fills `observed` from the developer's `report.json` before spawning the compliance-checker (per §Implement; the developer never writes `exec.md` or the spec).

Quick facts for implementation steps:
- Each implementation step requires evidence captures (failing test → implement → passing test → compliance check)
- A step is not done until green_capture exists and matches expected_pass_pattern

**Agent pre-tag (optional).** For each step in §5, optionally tag the recommended agent inline using the `@<agent>` suffix defined in `references/spec-template.md` §5 — leave untagged if the step's nature doesn't clearly match a single routing trigger.

**Change-type prompt.** Before the Prerequisites prompt, resolve the spec's `change_type`. Infer from the user's description (case-insensitive, first match wins; evaluate in this order):

1. `fix | bug | hotfix | regression | broken` → `fix`
2. `refactor | extract | rename | reorganize | restructure` → `refactor`
3. `docs | documentation | readme` → `docs`
4. `ci | workflow | github actions | gh actions | pipeline` → `ci`
5. `test | coverage | smoke | assertion` (when the primary subject is tests) → `test`
6. `chore | bump | deps` → `chore`
7. default → `feat`

Then confirm with the user via a banner prompt:

---
## ⏸ AWAITING YOUR INPUT

Inferred change type: **<type>**. Branch will be
`<type>/YYYY-MM-DD-<slug>`. Override with one of
`feat / fix / refactor / ci / docs / test / chore`, or accept.

**Change type?**

Empty answer → accept inferred value. Any of the seven literals → use that. Anything else → re-prompt with the same banner and an "invalid value" preamble. Write the resolved value into spec frontmatter as `change_type:` and substitute into the `branch:` field (e.g. `branch: feat/2026-04-18-my-slug`). Append to spec Log: `- YYYY-MM-DD: change_type=<type> (inferred|user-override)`.

**Prerequisites prompt.** Before moving to approval, ask the user:

---
## ⏸ AWAITING YOUR INPUT

Any deploy prerequisites? One-off ops steps that must run after the merge before the feature works (migrations, worker restarts, cache reset). One per line. Empty input = none.

**What are the deploy prerequisites?**

Write the answer into the YAML block in spec section `## 6.2 Deploy & manual verification` as `deploy_prerequisites`. Each non-empty line becomes one YAML-quoted list entry. Empty input maps to `deploy_prerequisites: []`.

**Smoke check.** Then ask the user:

---
## ⏸ AWAITING YOUR INPUT

Fastest manual smoke check — command to run post-deploy to confirm the feature is alive. (Empty = no smoke check configured.)

**What command should the smoke check run?**

If the user leaves it empty, write `smoke_check: null` in `## 6.2 Deploy & manual verification` and skip the next question. If the user gives a command, write `smoke_check: {command: <verbatim command, YAML-quoted>, expected: <expected output, YAML-quoted>}` and ask:

---
## ⏸ AWAITING YOUR INPUT

Expected substring in the command output? (Empty = no explicit expectation; success is defined by exit code alone.)

**What substring should appear in the smoke-check output?**

If the user leaves the expected-output prompt empty, write `expected: ""`.

**Post-merge checklist seeding.** Before moving to approval, ask the user:

---
## ⏸ AWAITING YOUR INPUT

Any other post-merge obligations? Cross-team dependencies, blockers on other specs, soak periods. Deploy prereqs from §6.2 will be added automatically on hand-off.

**What post-merge obligations should be tracked?**

If the user names any, populate the `items:` YAML block in spec section `## 8. Post-merge checklist` following the schema in `references/spec-template.md`. If there are none, leave `items: []`. The checklist can be edited later via `/feature checklist`.

Spawn **Librarian** only if you need to update MOC indexes afterward.

**Attack-surface profile slot-filling.** Before moving to approval, present 5 banners in sequence:

**Banner 1 — caller_identity** (also acts as the `not_applicable` short-circuit gate):

```
## ⏸ AWAITING YOUR INPUT

Attack-surface profile (1/5) — Caller identity. Who calls this code path? Pick one:

- `anonymous-public` — accessible without auth (public API, web form, signup endpoint)
- `authenticated-user` — end-user behind auth (logged-in session, OAuth-bearing request)
- `service-account` — internal service-to-service call (machine credential, mTLS)
- `cron` — scheduled job / background worker
- `webhook-external` — incoming webhook from a third-party service we don't control
- `mixed` — multiple callers; describe in §3 Design
- `unspecified` — caller_identity not relevant or skip
- `n/a` — entire attack-surface profile not applicable (smart-contract, doc-only, internal CLI without network surface). Sets `not_applicable: true` and skips remaining prompts.

**Caller identity?**
```

If user answers `n/a`: set `not_applicable: true`, all other fields set to literal `null` per §3.3 canonical rule, skip Banners 2–5, write §1.1 with `not_applicable: true` AND every other field as `null`, proceed to Step 3 HARD GATE.

Otherwise: parse answer against the enum (lowercase, leading/trailing whitespace stripped). On match, store the value. On mismatch (anything not in the enum and not `n/a` / `skip`), re-prompt with the same banner and an "invalid value" preamble. Empty answer → `unspecified`.

**Banner 2 — external_input**:

```
## ⏸ AWAITING YOUR INPUT

Attack-surface profile (2/5) — External input. Does any code path accept user-uploaded files, externally-provided URLs, third-party-API parsed data, or any data crossing a trust boundary? `yes` / `no` / `skip` (default no).

**External input?**
```

`yes` → `external_input: true`. `no` / `skip` / empty → `external_input: false`.

**Banner 3 — rate_limit**:

```
## ⏸ AWAITING YOUR INPUT

Attack-surface profile (3/5) — Rate limit. Is the entry point rate-limited and per what dimension?

- `per-ip` — limit by source IP
- `per-user` — limit by authenticated user
- `per-api-key` — limit by API key
- `per-tenant` — limit by tenant/org
- `none` — no rate limiting
- `unspecified` — rate-limit policy unclear or out-of-scope, or `skip`

**Rate limit?**
```

Parse against enum. Empty / `skip` → `unspecified`.

**Banner 4 — abuse_scenarios**:

```
## ⏸ AWAITING YOUR INPUT

Attack-surface profile (4/5) — Abuse scenarios. What would a malicious caller try? 1-3 sentences in free form. Empty / `skip` = no abuse scenarios captured (slot stays `null`).

**Abuse scenarios?**
```

Free-form. Whitespace-trim. Empty / `skip` → `abuse_scenarios: null`. Otherwise the orchestrator MUST serialize the answer via a YAML library's safe-dump (`yaml.safe_dump` in Python, `js-yaml` `dump` in JS) with default flow style — NOT manual string concatenation. The library handles single-quote doubling, double-quote escaping, embedded colons, leading dashes, multi-byte unicode, and embedded newlines correctly. Reject answers containing the U+0000 NUL byte before passing to the dumper.

**Banner 5 — framework_version_target**:

```
## ⏸ AWAITING YOUR INPUT

Attack-surface profile (5/5) — Framework version target. For backend specs: framework + version (e.g. `Django 5.0`, `Express 4.x`, `FastAPI 0.110+`). Empty / `skip` / not-backend = `null`.

**Framework version target?**
```

Free-form. Empty / `skip` → `null`. Otherwise the orchestrator MUST serialize the answer via a YAML library's safe-dump (`yaml.safe_dump` in Python, `js-yaml dump` in JS) with default flow style — NOT manual string concatenation. Same protocol as Banner 4 abuse_scenarios. The library handles single-quote doubling, double-quote escaping, embedded colons, leading dashes, multi-byte unicode, and embedded newlines correctly. Reject answers containing the U+0000 NUL byte before passing to the dumper.

After all 5 prompts (or after the n/a short-circuit on Banner 1), the orchestrator writes the answers into spec `## 1.1 Attack-surface profile` block, appends one Log line `- YYYY-MM-DD: attack-surface profile recorded (caller_identity=<v>; external_input=<v>; rate_limit=<v>; framework=<v>)` (or for short-circuit: `- YYYY-MM-DD: attack-surface profile not applicable`), then proceeds to Step 3 HARD GATE.

### §1.2 STRIDE-lite threat model prompts

**Gating**: if `not_applicable: true` OR `external_input != true` (from Banner 2 above), skip this section entirely — do not prompt, do not write §1.2 to the spec — and proceed to Step 3 HARD GATE.

If `external_input == true`, present the following 6 banners in sequence:

**Banner STRIDE-1 — Spoofing**:

```
## ⏸ AWAITING YOUR INPUT

STRIDE-lite (1/6) — Spoofing. How could an attacker impersonate a legitimate caller for this feature? 1-3 sentences in free form, or `skip` (default null). External_input is true, so this row is recommended but not required.

**Spoofing mitigation?**
```

Free-form. Empty / `skip` → `spoofing: null`. Otherwise serialize via `yaml.safe_dump` / `js-yaml dump` — NOT manual string concatenation.

**Banner STRIDE-2 — Tampering**:

```
## ⏸ AWAITING YOUR INPUT

STRIDE-lite (2/6) — Tampering. What data could an attacker modify in transit or at rest for this feature? 1-3 sentences, or `skip` (default null).

**Tampering mitigation?**
```

Free-form. Empty / `skip` → `tampering: null`. Otherwise serialize via `yaml.safe_dump` / `js-yaml dump` — NOT manual string concatenation.

**Banner STRIDE-3 — Repudiation**:

```
## ⏸ AWAITING YOUR INPUT

STRIDE-lite (3/6) — Repudiation. What action could a caller perform and then deny for this feature? 1-3 sentences, or `skip` (default null).

**Repudiation mitigation?**
```

Free-form. Empty / `skip` → `repudiation: null`. Otherwise serialize via `yaml.safe_dump` / `js-yaml dump` — NOT manual string concatenation.

**Banner STRIDE-4 — InfoDisclosure**:

```
## ⏸ AWAITING YOUR INPUT

STRIDE-lite (4/6) — InfoDisclosure. What sensitive data could leak via logs, responses, or error messages for this feature? 1-3 sentences, or `skip` (default null).

**InfoDisclosure mitigation?**
```

Free-form. Empty / `skip` → `info_disclosure: null`. Otherwise serialize via `yaml.safe_dump` / `js-yaml dump` — NOT manual string concatenation. Reject U+0000 NUL byte.

**Banner STRIDE-5 — DoS**:

```
## ⏸ AWAITING YOUR INPUT

STRIDE-lite (5/6) — DoS. What cheap input could exhaust resources for this feature? 1-3 sentences, or `skip` (default null).

**DoS mitigation?**
```

Free-form. Empty / `skip` → `dos: null`. Otherwise serialize via `yaml.safe_dump` / `js-yaml dump` — NOT manual string concatenation.

**Banner STRIDE-6 — EoP**:

```
## ⏸ AWAITING YOUR INPUT

STRIDE-lite (6/6) — EoP. What bug could let an unprivileged caller perform a privileged action for this feature? 1-3 sentences, or `skip` (default null).

**EoP mitigation?**
```

Free-form. Empty / `skip` → `eop: null`. Otherwise serialize via `yaml.safe_dump` / `js-yaml dump` — NOT manual string concatenation.

After all 6 banners, the orchestrator writes `## 1.2 STRIDE-lite threat model` section into the spec with the collected `stride_lite` answers (serialized via library safe-dump), appends one Log line `- YYYY-MM-DD: stride-lite threat model recorded (spoofing=<truthy?>; tampering=<truthy?>; repudiation=<truthy?>; info_disclosure=<truthy?>; dos=<truthy?>; eop=<truthy?>)`, and proceeds to Step 3 HARD GATE.

### Grill gate — optional DRAFT-hardening sub-phase

Grill is **off by default**. It is a DRAFT-hardening sub-phase placed `DRAFT → [grill] → APPROVED` — NOT a new state-machine token (status enum unchanged, zero migration). It runs HERE, after spec drafting + slot-filling and before the Step 3 approval HARD GATE, so approval reflects the grilled spec. Most specs never grill.

**Mutate-then-validate ordering.** Grill MUTATES the spec (removes over-builds, flips decisions); the Step 3.5 cross-audit VALIDATES the settled spec. Grill before audit so the gold-standard audit runs last on what ships — cheaper to move a decision than to re-audit a diff.

**Invocation (opt-in).** `/feature grill [spec-path]` — runs the gate inline now, or standalone later on any existing DRAFT (the standalone dispatch — spec resolution, DRAFT-only precondition, return — lives in `## Grill mode`). Off by default; never auto-runs.

**Neutral auto-suggest — never blocks, never gates, no repeat prompts.** When high-risk signals fire — `project_type: smart_contract`, OR §1.1 `external_input: true`, OR the spec description/title hits `payment / auth / migration / irreversible / consensus` — surface ONE neutral one-line suggestion that the optional grill is available, e.g.:

```
Optional grill gate available (high-risk signals: <which>). Run `/feature grill` or skip.
```

Single non-repeating suggestion: no blocking, no gating, no re-prompt, never auto-runs. The user runs grill or skips; either way the flow proceeds to Step 3.

**Interactive + INLINE.** The interview runs inline in the main conversation, human in the loop — NOT a backgrounded subagent, NOT the `agents/investigator.md` debate engine (a round-based debate is the wrong control structure for an interview).

**What grill does** — see `skills/feature/references/grill-protocol.md` for the full interview discipline (branch-map traversal, the 3 load-bearing mechanics, coarse route, Decisions write-back schema, coverage / termination, `--focus`, cadence). Do NOT restate it here. Output folds back per that write-back contract: a `## Decisions` table, risk deltas into §3.6 Risks, a §9 Log line, and `grill_status` / `grill_date` / `grill_coverage` frontmatter.

**grill_status — skipped vs null (explicit-decline vs never-engaged).** `grill_status: skipped` is the **explicit-decline** value: when grill is **offered** — the high-risk auto-suggest above fired, OR `/feature grill` was invoked — and the user **declines / skips**, the orchestrator writes `grill_status: skipped` (+ `grill_date: null`, `grill_coverage: null`) to the spec frontmatter before proceeding to Step 3. When grill is **never engaged at all** (the default silent off-by-default path — grill was never surfaced), `grill_status` stays `null` (= legacy_unknown / not-applicable); do NOT force every spec to `skipped`. Either way `grill_status: skipped` is a first-class **non-degraded** value (grill is optional). Grill NEVER gates approval or audit; `grill_coverage` deferred branches are advisory only. Skipping is not a degraded state — the degraded predicate references no grill field.

### Step 3 — Get approval

Present a summary and wait for user approval before implementing.

<HARD-GATE>
Do NOT spawn any developer agent, write any code, or take any implementation action until the user has explicitly approved the spec. This applies to every feature regardless of perceived simplicity. "It looks straightforward" is not approval.
</HARD-GATE>

---
## ⏸ APPROVAL REQUIRED

The draft spec is ready for review at `<spec_path>`. No implementation, no developer spawn, no code edits happen before you approve.

- Approve → set `status: APPROVED`, continue to Step 3.5 spec review.
- Reject → return to drafting with your feedback.

**Approve to proceed?**

Set spec `status: APPROVED` after explicit user approval.

### Step 3.5 — Spec review (two passes)

After approval, immediately ask:

---
## ⏸ AWAITING YOUR INPUT

Run spec audit before implementation?

1. Yes — recommended if the spec involves external APIs, new business logic, or non-trivial data flows
2. Skip — for simple config/plumbing changes where you're confident in the spec

**Run spec audit?**

If the user chooses **Skip**: set `status: AUDIT_PASSED`, set `spec_audit_evidence: skipped` and `spec_audit_blockers: ['spec audit skipped by user']`, append to Log: `"spec audit skipped by user"`, proceed directly to Implement. (Setting AUDIT_PASSED rather than keeping APPROVED ensures continue mode does not re-enter the audit loop on resume.)

If the user chooses **Yes** (or gives no explicit answer): run both passes below.

---

Review the spec and execution workdoc before any code is written.

#### Pass 1: Self-review (orchestrator)

Before calling any agent, check both documents for basic completeness:

- No placeholder text (`{...}`, `TBD`, etc.) in spec or workdoc planned fields
- Every checklist step has a corresponding entry in exec.md with `planned.goal` and `planned.passing_test_cmd` at minimum
- `allowed_scope` is set for every step (not empty)
- No step depends on something defined in a later step
- `planned.failing_test_cmd` is either set or intentionally empty (not just forgotten — flag if the step's goal implies testable behavior)
- Spec `Verification` section describes concrete commands, not vague prose

If any check fails: fix the spec/workdoc directly (or ask the user for the missing information) before proceeding to Pass 2.

#### Pass 2: Cross-audit (dual-model)

Track `spec_audit_iteration` (start at 1, increment on each re-spawn). Track `spec_audit_fixed_ids` (list of finding IDs the user fixed — accumulate across rounds). Track `spec_audit_next_id` (integer — the next finding ID to allocate; start at 1, update to `highest_id_in_report + 1` after each round).

Spawn `cross-auditor` subagent with the **same parameter block as the initial full-mode spawn (§Code audit Pass 2)**, with these spec-mode deltas:

- `mode`: `spec` (was `full`)
- `audit_slug`: `<slug>-spec` (was `<slug>-code`)
- `scope`: `<spec_path>` (was newline-joined auditable paths from Pass 1)
- ADD: `workdoc_path: <workdoc_path>` (the execution workdoc — spec-only)
- ADD: `next_finding_id: <spec_audit_next_id>` (spec-only — ensures IDs don't collide across rounds when no findings doc exists)
- OMIT: `kb_path` (spec mode does not write to KB)
- OMIT: `accepted_ids` (no per-finding triage in spec mode)
- OMIT: `base_branch` (spec mode does not need git context)
- `iteration`: `<spec_audit_iteration>` (was `<code_audit_iteration>`)
- `previously_fixed`: `<spec_audit_fixed_ids>` (was `<code_audit_fixed_ids>`)

`project_type` resolution: identical to code mode (spec frontmatter → .ai-dev-team.local.yml → .ai-dev-team.yml → None).

The cross-auditor returns findings inline (no KB writes in spec mode).

**Grill-aware Pass 2 (when the spec was grilled).** If the spec carries `grill_status: ran` and a `## Decisions` table, the orchestrator passes that `## Decisions` table to the cross-auditor (BOTH halves — Claude half via `agents/references/cross-auditor-mode-focus.md` §spec mode, Codex half via the `agents/references/cross-auditor-codex-dispatch.md` spec-mode template) as an independent backstop input. The grill-aware audit additionally (a) verifies each `evidence-ref` citation **RESOLVES** — the cited path/line/literal actually exists (NOT semantic adequacy of the evidence, which stays the user's call), (b) inspects the deferred branches, (c) reports grill-overlap separately so grilled decisions and independent audit findings stay distinguishable. The spec audit stays **MANDATORY by default**: grill running does NOT remove or alter the existing explicit user-Skip path (the Skip button above + the mid-flow "skip / proceed anyway" override, both still recording `spec_audit_evidence: skipped`) — the Skip path is **preserved** unchanged. **Grill NEVER gates:** `grill_coverage` `deferred > 0` is advisory, never a Step 3.5 fail.

#### 3.5a Cross-auditor return-contract gate

**branch-guard (callsite 1).** Run the §3.5d branch-guard around this spawn — capture `pre_spawn_branch`/`pre_spawn_head` BEFORE the spawn, and after the cross-auditor returns assert current branch == `pre_spawn_branch` AND strict `HEAD == pre_spawn_head` (callsites 1-4 are strict-equality, NOT ancestor-mode) BEFORE any further git / Log / triage action. On violation apply the §3.5d step-4 recovery split (4a/4b/4c) and continue-gate.

Before the CRITICAL/HIGH triage below runs, **apply the §3.5b-2 recovery algorithm** to the cross-auditor's raw inline return. This is callsite 1 of the 6 §3.5b-2 callsites — the feature spec-audit Pass 2 spawn. Capture the raw return to `<spec-path>.contract-violation-iter<N>-attempt<M>.raw.txt` per §3.5b-1, invoke `hooks/lib/check_dispatch_response.py --mode spec --expected-claude-model claude-opus` (add `--project ai-dev-team` when the spec frontmatter resolves `project: ai-dev-team`), and branch on the classifier exit code per §3.5b-2 step 4. The classifier output **gates** whether the triage below runs: only an Exit-0 `policy_gate: null` with `model_gate: null` PROCEED reaches the CRITICAL/HIGH triage (a non-null `model_gate` routes to the §3.5b-2e model-attestation gate); an Exit-0 `policy_gate: STOP_AND_DISCUSS` raises the §3.5b-2a banner, an Exit-1 violation enters the §3.5b-2b retry-outcome matrix, and an Exit-2 classifier crash raises the §3.5b-2c classifier-crash banner.

**If CRITICAL or HIGH findings:**
1. Present findings to user
2. Update spec/workdoc (user edits in Obsidian, or ask Claude to apply the fix). The finding's fix suggestion is advisory — one hypothesis; derive the remedy from the finding Description + failure class.
3. Collect IDs of findings the user fixed → append to `spec_audit_fixed_ids`
4. Update `spec_audit_next_id` = highest finding ID in this round's report + 1
5. Increment `spec_audit_iteration`
6. Before re-spawn, see §3.5c Stop criteria — REOPEN findings or same-defect-class on 2+ iters trigger a comprehensive sweep AFTER `/compact` or via a fresh-context subagent; hard cap iter ≤ 5 unless an explicit §3.1c-regex Log line justifies the exception. Then re-run Pass 1 self-review and re-spawn cross-auditor with updated `iteration` and `previously_fixed`.
7. Repeat until no CRITICAL/HIGH remain
8. Set spec `status: AUDIT_PASSED`. Populate `spec_audit_evidence:` from the cross-auditor's final-iteration return signal per §3.5b READ path. Copy `evidence_blockers:` verbatim into `spec_audit_blockers:` (parse-failure → `contract_violated` per §3.5b).

**If no CRITICAL or HIGH findings:**
> Spec review passed — the spec is saved to KB. Moving to implementation.
> 💡 Consider running `/compact` before implementation to trim conversation history.

Set spec `status: AUDIT_PASSED`. Populate `spec_audit_evidence:` from the cross-auditor's final-iteration return signal per §3.5b READ path. Copy `evidence_blockers:` verbatim into `spec_audit_blockers:` (parse-failure → `contract_violated` per §3.5b).

**Mid-flow skip**: if the user says "skip" or "proceed anyway" at any point during the audit — stop, set `status: AUDIT_PASSED`, set `spec_audit_evidence: skipped` and `spec_audit_blockers: ['spec audit skipped by user']`, append to Log: `"spec audit skipped by user"`.

### 3.5b Audit evidence

Per spec `2026-04-27-audit-evidence-enum.md`. Every audit-terminal site (spec audit AUDIT_PASSED + code-audit Log markers) records WHAT evidence backs the audit by populating two paired frontmatter fields: `*_audit_evidence:` (enum) and `*_audit_blockers:` (list of strings naming what blocked the dual-model gold standard, empty when `dual_model`).

**Enum values:**

- `dual_model` — both Claude and Codex halves of the cross-auditor returned findings (or both confirmed clean) — the gold standard.
- `single_model` — one half returned findings, the other half failed and the orchestrator proceeded under the documented fail-open rule (`agents/cross-auditor.md` Step 1 fail-open path).
- `self_fallback` — the cross-auditor agent itself could not complete (stall, timeout, MCP failure, premature merge) and the orchestrator performed manual self-verification per the iter-2 fallback rule (`feedback_iter_2_audit_fallback.md`). The cross-auditor never returns a usable signal in this case.
- `contract_violated` — the cross-auditor *ran* but its output contract is broken: (a) inline return (spec mode) missing/malformed `evidence_class:` or `evidence_blockers:` final lines; (b) any `evidence_blockers` list item fails YAML-safety scalar validation per cross-auditor's serialization rule; (c) code/full mode — the expected `<kb>/repos/<project>/security/<audit_slug>-findings.md` file is missing on disk after the agent returns. The cross-auditor never writes this value (by definition can't reliably self-diagnose); the orchestrator records it. Recovery (re-spawn, manual self-verify per `feedback_iter_2_audit_fallback.md`, or ship as-is) is a separate orchestrator decision that may further update the final evidence value.
- `skipped` — no audit was performed against findings: user clicked Skip on the spec-audit prompt, OR mid-flow "skip / proceed anyway" override, OR the code-audit zero-diff branch fired (`no auditable files in diff`).

**Reader semantics for `null` (legacy specs).** All pre-enum specs lack these fields. Readers (filters, smoke pins, analytical scripts) MUST treat `null` / missing as `legacy_unknown` — distinct from any enum value, NOT flagged as degraded, NOT compared against `dual_model` directly. The canonical degraded-flag predicate is `*_audit_evidence ∈ {single_model, self_fallback, contract_violated, skipped}`. The inverse "not equal to dual_model" form is forbidden because it would flag every legacy spec forever.

**Honesty-gate-not-approval-gate.** This subsection records evidence; the routine case introduces NO new mid-flow user banner per `feedback_ai_dev_team_repo_autonomy.md`. Future tooling (`/feature status`, smoke pins, future analysis) reads the field programmatically and surfaces degraded rows for human review out-of-band.

**`self_fallback` discipline remains user-enforced.** The iter-2 fallback memory `feedback_iter_2_audit_fallback.md` continues to define the six criteria for when manual self-verification is authorized. This subsection adds the honest record (the field) but NOT a machine-readable gate against criteria violations. The machine gate is a follow-up spec — see DRAFT `2026-04-27-self-fallback-machine-gate.md`. Recording a `self_fallback` value here means "I did manual review", NOT "the criteria were verified".

**Orchestrator READ path (handshake → spec frontmatter).** The cross-auditor transmits two sibling fields back to the orchestrator: `evidence_class:` (enum — see `agents/cross-auditor.md` §When to set for the cross-auditor's binary emit allowlist) and `evidence_blockers:` (list).

- **Code/full mode (file-backed)** — production-file parser. The cross-auditor writes a findings.md with the two scalars in the leading top-of-file YAML frontmatter block (NO `### findings.md` heading anchor — that anchor only applies to smoke validation against the agent SOURCE template). The orchestrator reads from the produced findings.md as `awk '/^---$/{c++; next} c==1' <audit_slug>-findings.md | grep -E '^(evidence_class|evidence_blockers): '`. The production file's H1 is `# Audit Findings: <scope>`, not `### findings.md` — the production parser is unanchored on top-of-file YAML.
- **File-existence check (code/full mode only).** Before reading frontmatter, the orchestrator MUST check that `<kb>/repos/<project>/security/<audit_slug>-findings.md` exists on disk after the cross-auditor returns. If absent, record `*_audit_evidence: contract_violated` with blocker `'findings.md missing at <path>'` (use the resolved absolute or `<kb>`-relative path, sanitized per the Orchestrator blocker sanitization rule below) and skip the YAML extraction.
- **Spec mode (inline return)** — the orchestrator's consumer-side parser is **`hooks/lib/check_dispatch_response.py --mode spec`**, invoked by the §3.5b-2 recovery algorithm (the helper is the single authoritative spec-mode parser). The helper anchors on the LAST `# CROSS-AUDIT EVIDENCE FOOTER` sentinel line and reads the `evidence_class:` / `evidence_blockers:` lines that follow it; it tolerates a footer whose `evidence_blockers` list literal legitimately spans more than one physical line (the newline-unsafe defect — classified `BLOCKER_YAML_UNSAFE_NEWLINE`, a specifically-named violation) and routes the forgotten-footer / trailing-prose-after-footer cases to `MISSING_FOOTER`. The producer-side contract — three-line EOF-adjacent footer, sentinel marker, the rationale covering the forgotten-footer-with-example-echo and trailing-prose-after-real-footer failure modes — is documented canonically (parse per `agents/references/cross-auditor-evidence-handshake.md` §Spec-mode return contract); the `tail -3` parser shape described there is the producer-side reference description of the well-formed EOF-adjacent footer, and `hooks/lib/check_dispatch_response.py` is the authoritative consumer-side implementation (it additionally distinguishes the newline-unsafe defect from a plain missing footer — a distinction a literal `tail -3` cannot make). Routing on parser failure is the §3.5b-2 recovery algorithm's exit-code branch: any classification other than `CLEAN_DUAL` / `CLEAN_SINGLE` is a contract violation (exit 1) carrying the §3.5b-2b `violation_blocker` phrasing; the classifier crashing on its own (exit 2) raises the §3.5b-2c classifier-crash banner.

**Contract-violation rule.** If the cross-auditor's return signal cannot be parsed (either footer line absent/malformed, OR any `evidence_blockers` list item fails YAML-safety scalar validation per cross-auditor's serialization rule: newline→space, truncate to 199 chars, `'`→`''` escape, single-quoted form), OR (code/full mode only) the expected `<kb>/repos/<project>/security/<audit_slug>-findings.md` file is missing on disk after the agent returns, the orchestrator MUST record `*_audit_evidence: contract_violated` and the specific violation as a blocker (e.g. `'cross-auditor return missing evidence_class footer line'`, `'cross-auditor return malformed evidence_class footer'`, `'evidence_blockers entry failed YAML-safety validation'`, `'findings.md missing at <path>'`). Additionally, if the parsed `evidence_class` value is not exactly one of `dual_model | single_model` (the cross-auditor's binary emit allowlist — the agent never writes the orchestrator-only values, so any other token signals a buggy or regressed emitter; including empty/whitespace-only values, which pass the parser shape check but carry no signal), the orchestrator MUST also record `*_audit_evidence: contract_violated` with blocker `'cross-auditor emitted disallowed evidence_class value: <sanitized-value>'` (sanitize the offending value through the Orchestrator blocker sanitization rule below before embedding). Additionally, the orchestrator MUST validate the cross-field invariant between `evidence_class` and `evidence_blockers` per the cross-auditor emit contract (`agents/cross-auditor.md` §When to set): `evidence_class: dual_model` MUST pair with `evidence_blockers: []` (empty list); a non-empty list paired with `dual_model` routes to `*_audit_evidence: contract_violated` with blocker `'cross-auditor emitted dual_model with non-empty evidence_blockers: <sanitized-value>'`. `evidence_class: single_model` MUST pair with a non-empty `evidence_blockers` list; an empty list paired with `single_model` routes to `*_audit_evidence: contract_violated` with blocker `'cross-auditor emitted single_model with empty evidence_blockers'`. Both blocker phrasings pass through the Orchestrator blocker sanitization rule below before embedding in spec frontmatter.

The orchestrator's recovery action — re-spawn the cross-auditor, manually self-verify per `feedback_iter_2_audit_fallback.md` six criteria, or ship the unresolved label as-is — is a separate decision that MAY further update the final evidence value (re-spawn success → final `*_audit_evidence` reflects the successful retry's `evidence_class`; manual self-verify per six criteria → final `*_audit_evidence: self_fallback`). The recovery path is **automated** by the §3.5b-2 recovery algorithm below — every cross-auditor return at any of the 6 callsites runs the §3.5b-2 capture → classify → branch sequence, which dispatches a bounded retry and routes unrecovered violations to a banner.

**Orchestrator blocker sanitization rule.** Every blocker string the orchestrator generates (file-existence-check `<path>`; `self_fallback` cause + tracking entry; explicit-Skip phrasing; Contract-violation example phrasings — including the disallowed-`evidence_class` value embedded per the X2 allowlist clause above) MUST pass through the same YAML-safety sanitizer as cross-auditor blockers (per `agents/cross-auditor.md` §YAML-safety serialization rule for blocker strings: newline→space; truncate to 199 chars and append `…` if truncated; escape single quotes by doubling (`'` → `''`); single-quoted YAML scalar form — see `agents/cross-auditor.md` §YAML-safety serialization rule for blocker strings for the canonical 4-step ordering). The blocker emission path is symmetric on both sides of the handshake — without this symmetry, a path containing an apostrophe (e.g. `/Users/.../it's-a-spec/...`) emitted into the file-existence-check blocker via the `<path>` slot would corrupt the spec's YAML frontmatter and silently de-card the spec from every reader (Status mode, smoke pins, analytical scripts).

**Historical-event storage rule.** Prior `contract_violated` events that were superseded by a successful retry or manual self-verify are recorded in the spec Log ONLY (e.g. `- YYYY-MM-DD: spec audit retry — prior contract_violated event 'cross-auditor return missing evidence_class footer line' on iter-N; recovered iter-N+1`), NOT in `*_audit_blockers`. The `*_audit_blockers` list is tied to the FINAL `*_audit_evidence` value: `dual_model` keeps its `[]` invariant; `single_model` carries Codex-fail-open reasons; `contract_violated` carries the active violation phrasing; `self_fallback` carries the named cause + tracking entry; `skipped` carries the user-skip / zero-diff phrasing. Historical-event accumulation in `*_audit_blockers` is forbidden because it would erase the schema's "blockers describe what blocks the FINAL gold standard" semantics from the parent spec §3.1.

The orchestrator copies `evidence_blockers` from the handshake verbatim into `*_audit_blockers`, then prepends any orchestrator-side blockers (e.g. for `self_fallback`: the named cause + tracking entry; for zero-diff skip: `'no auditable files in diff'`; for explicit Skip: `'spec audit skipped by user'`).

#### 3.5b-1 Raw-response atomic-write protocol

The §3.5b-2 recovery algorithm (referenced from each of the 6 cross-auditor callsites) opens with a **capture step**: the raw cross-auditor response is written to disk BEFORE classification, because that captured file is the single source of post-mortem diagnostic state — without it, a same-iteration retry erases the only evidence of what the cross-auditor actually emitted. The capture MUST be atomic, and capture-failure MUST stop the flow.

**Capture paths** (every path carries an `-attempt<M>` suffix — `M=1` for the initial spawn, `M=2` for a retry — so attempt-2 never overwrites attempt-1 evidence):

- **Spec mode** (callsite 1): `<spec-path>.contract-violation-iter<N>-attempt<M>.raw.txt` — sibling file next to the spec file in `<kb>/repos/<project>/design/`. Raw cross-auditor inline-return text verbatim.
- **Code/full feature mode** (callsites 2/3/4): `<kb>/repos/<project>/security/<audit_slug>-contract-violation-iter<N>-attempt<M>.raw.txt` — alongside the findings.md path. Raw cross-auditor inline-return text verbatim (NOT the findings.md frontmatter — that is already on disk at `<audit_slug>-findings.md`).
- **Standalone `/cross-audit`** (callsites 5/6): TWO files — `<...>-contract-violation-iter<N>-attempt<M>.raw.txt` (raw response, captured BEFORE classification) plus a sidecar `<...>-contract-violation-iter<N>-attempt<M>.json` (written AFTER classification, carrying `classifier_output` + embedded-or-referenced raw response per skills/cross-audit/SKILL.md §3.4d).

**Atomic-write protocol.** The atomic-write uses `O_EXCL`-equivalent semantics — a pre-existing target at the `(iter, attempt)` slot is an **error, NOT a silent overwrite** (the same audit slug + iteration + attempt cannot legitimately fire twice; a pre-existing target means a programming bug elsewhere in the orchestrator double-fired, and it MUST fail loud):

```python
# Atomic capture of the raw cross-auditor response. <capture-path> is the
# mode-specific contract-violation-iter<N>-attempt<M>.raw.txt path above.
import os

def capture_raw_response(capture_path, raw_text):
    # capture_path is the contract-violation-iter<N>-attempt<M>.raw.txt path.
    # O_EXCL: raises FileExistsError if <capture-path> already exists.
    try:
        # os.open + O_EXCL atomic write of the contract-violation-iter
        # capture — pre-existing target raises, never silently clobbered.
        fd = os.open(capture_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        # Pre-existing capture target — orchestrator double-fired for the
        # same (iter, attempt) pair. Distinct error class so the §3.5b-2c
        # capture-failure banner can name it. Do NOT overwrite.
        raise PreExistingCaptureTarget(capture_path)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(raw_text)
```

Alternative implementation via a same-directory temp file (same-filesystem `os.rename` is atomic on POSIX) — equivalent guarantee, also fails loud on a pre-existing target:

```python
# Equivalent atomic-write of the contract-violation-iter<N>-attempt<M>.raw.txt
# capture via temp-file + rename. Verify the canonical target is absent first.
tmp = capture_path + ".tmp"
with open(tmp, "w", encoding="utf-8") as fh:
    fh.write(raw_text)
if os.path.exists(capture_path):
    raise PreExistingCaptureTarget(capture_path)   # fail loud, never clobber
os.rename(tmp, capture_path)
```

The standalone sidecar JSON (`contract-violation-iter<N>-attempt<M>.json`) is written with the same atomic-write protocol AFTER classification. Its shape is **exit-code aware** (§3.5b-2 step 3): on classifier exit 0/1 the `classifier_output` field is populated from the classifier's stdout JSON and `classifier_exit` records the exit code; on classifier exit 2 (crash — empty stdout, no JSON) `classifier_output` is `null`, `classifier_exit` is `2`, and `classifier_stderr` carries the classifier's stderr truncated to 1000 chars. The `raw_response` field carries the full text inline when the raw byte count ≤ 65536 (64 KiB) or `null` plus a `raw_response_path` reference otherwise — independent of the classifier exit code (the raw response is captured in step 1, before classification).

On atomic-write failure — disk full, permission denied, read-only filesystem, or pre-existing target — the orchestrator jumps to the §3.5b-2 capture-failure banner and STOPS (a retry without a captured response would erase the diagnostic). `PreExistingCaptureTarget` is reported with the distinct phrasing `Pre-existing capture target: <path> — orchestrator double-fired for the same (iter, attempt) pair`.

#### 3.5b-2 Cross-auditor return-contract recovery algorithm

Automates the recovery path that §3.5b's Contract-violation rule formerly carved out. After **every** cross-auditor return at any of the 6 callsites (§2.2 of the source spec — feature spec audit, feature code audit Pass 2 spawn, feature code-audit triage-loop re-spawn, feature Continue-mode resume re-spawn, standalone `/cross-audit` initial dispatch, standalone Phase 5 re-audit re-spawn), the orchestrator runs this sequence. All capture paths carry the `-attempt<M>` suffix per §3.5b-1 so an attempt-2 retry never overwrites attempt-1 evidence.

1. **Capture the raw response atomically** as a `contract-violation-iter<N>-attempt<M>.raw.txt` file per §3.5b-1. On atomic-write failure (disk full, permission denied, read-only filesystem, or pre-existing target) → jump to the **capture-failure banner** (§3.5b-2c) and STOP.
2. **Invoke the classifier** — `python3 hooks/lib/check_dispatch_response.py --mode <spec|code|full> --raw-response-file <captured-.raw.txt-path> --audit-slug <slug> --iteration <N> --expected-claude-model claude-opus` plus `--findings-path <path>` for code/full mode, plus `--expected-head "$(git rev-parse HEAD)"` and `--require-rules-loaded` for code/full mode ONLY (callsites 2/3/4 — the code-audit spawns run on the feature branch and are `mode: full`, so the R-rule loader always runs; the spec-mode callsite 1 passes NO head channel, and likewise passes NO `--require-rules-loaded` — both flags are code/full-only and rules-bearing/HEAD-bearing, `--expected-head` mirroring the audited_head file-backed-only emit asymmetry and `--require-rules-loaded` because the inline spec-mode channel carries no rules keys, so the spec-mode callsite 1 passes neither), plus `--project ai-dev-team` ONLY when the resolved spec frontmatter has `project: ai-dev-team`. Read the JSON from stdout, the exit code, and stderr.
3. **(Standalone mode only)** Write the sidecar JSON atomically at `contract-violation-iter<N>-attempt<M>.json` per §3.5b-1. The sidecar shape is **exit-code aware** — the orchestrator reads step 2's exit code first: for exit 0/1 (the classifier ran and produced a JSON) `classifier_output` is populated from step 2's stdout JSON and `classifier_exit` records `0`/`1`; for exit 2 (classifier crash — empty stdout, no JSON) `classifier_output` is `null`, `classifier_exit` is `2`, and `classifier_stderr` carries the classifier's stderr (truncated to 1000 chars). On sidecar-write failure → capture-failure banner (§3.5b-2c) and STOP.
4. **Branch on the classifier exit code:**
   - **Exit `2`** (classifier crash — the classifier's own failure; we cannot tell whether the response was valid) → **classifier-crash banner** (§3.5b-2c).
   - **Exit `0` AND `policy_gate: null`** → evaluate `model_gate` per §3.5b-2e (policy_gate FIRST, model_gate SECOND): `model_gate` non-null → the §3.5b-2e model-attestation gate; `model_gate: null` → evaluate `head_gate` per §3.5b-2f (head_gate THIRD): `head_gate` non-null → the §3.5b-2f audited-HEAD gate; `head_gate: null` → evaluate `rules_gate` per §3.5b-2g (rules_gate FOURTH): `rules_gate` non-null → the §3.5b-2g degraded-rules gate; `rules_gate: null` → **PROCEED**. PROCEED requires all four gates null. On the PROCEED path, copy `evidence_class` + `blockers_yaml` from the classifier JSON into the spec frontmatter (feature mode) or render the Phase 3 banner (standalone mode). `blockers_yaml` is the verbatim blocker source ONLY on this clean path (Exit-0); a `contract_violated` outcome instead records the classifier's `violation_blocker` phrasing per §3.5b-2b. Standard rest-of-flow.
   - **Exit `0` AND `policy_gate: STOP_AND_DISCUSS`** → the §3.5b-2a project-policy gate fires (ai-dev-team `CLEAN_SINGLE`). **BANNER.**
   - **Exit `1`** (any of the 10 violation classifications) → contract violation. Branch into the §3.5b-2b retry-outcome decision.

##### 3.5b-2a Project-policy post-classification gate

For `project: ai-dev-team`, `classification: CLEAN_SINGLE` does NOT auto-proceed. Per project policy `feedback_ai_dev_team_dual_model_cross_audit_always.md`: a `single_model` result from a Codex stall must be STOP-and-DISCUSS, not a silent fold to `single_model` evidence. The classifier flags this via `policy_gate: STOP_AND_DISCUSS` (set only when `--project ai-dev-team` was passed AND `classification == CLEAN_SINGLE`). The gate is **detected by the classifier flag but enforced by this orchestrator prose** — the classifier never blocks. Consumer projects (no `--project ai-dev-team`) keep the existing fail-open path (PROCEED with `*_audit_evidence: single_model`) per §3.5b. The orchestrator renders this banner:

---
## ⏸ AWAITING YOUR INPUT

Cross-auditor returned `CLEAN_SINGLE` — Claude-only audit (Codex stalled with reason: `<reason>`). For ai-dev-team project, project policy requires `dual_model` terminal evidence.

Options:
1. **Re-spawn cross-auditor** to retry Codex (may take 8-15 min; counts as a TRANSPORT retry — does NOT consume `*_audit_iteration` per §3.1c cap-regex semantics). Re-spawn outcome governed by §3.5b-2b Matrix B.
2. **STOP and discuss** — pause the flow; review whether to escalate the Codex outage, or accept `single_model` evidence as a documented one-time exception with an explicit Log directive.
3. **Accept single_model** (override project policy for this audit) — record `<phase>_audit_evidence: single_model`, append the Log directive `- YYYY-MM-DD: project-policy override — accepted single_model evidence for <slug> iter-<N>: <reason>`.

**Which option?**

---

##### 3.5b-2b Retry-outcome decision matrix

When the initial classifier exit = 1 (any violation), the recovery algorithm dispatches **one** retry per `feedback_session_handoff_queue_visibility.md` retry-discipline. The retry is a TRANSPORT retry — it does NOT consume `*_audit_iteration` (the iter ≤ 5 cap counts SEMANTIC re-spawns only). Before the retry, append a historical-event Log line per §3.5b Historical-event storage rule (single-line form; the `.raw.txt` sibling / standalone sidecar JSON carries the diagnostic detail). The retry uses **identical parameters** to the initial spawn (same `audit_slug`, `iteration`, `previously_fixed`, `accepted_ids`, `next_finding_id`).

**Source of the `<initial-blocker>` / `<retry-blocker>` strings.** For a `contract_violated` outcome, `*_audit_blockers` carries the **violation-description phrasing**, NOT `blockers_yaml`. The classifier emits this phrasing in its JSON `violation_blocker` field — a canonical per-classification string (e.g. `SINGLE_MODEL_WITHOUT_BLOCKERS` → `'cross-auditor emitted single_model with empty evidence_blockers'`; `FINDINGS_MISSING` → `'findings.md missing at <path>'` with the path slot filled). `violation_blocker` is non-null for every one of the 10 violation classifications and `null` for the two clean classifications. In the matrix below, `<initial-blocker>` is the initial classification's `violation_blocker`, `<retry-blocker>` is the retry classification's `violation_blocker`. (The classifier's `blockers_yaml` field is the YAML-list literal of the *parsed* `evidence_blockers` content — useful only on the clean path; for most violation classes it is `[]` and is NOT the blocker source.)

**Matrix A — contract-violation initial (initial classifier exit = 1):**

| Initial class | Retry class | Final `*_audit_evidence` | Final `*_audit_blockers` |
|---|---|---|---|
| Any violation | `CLEAN_DUAL` | `dual_model` (write gated on `model_gate: null` — see note) | `[]` |
| Any violation | `CLEAN_SINGLE` (consumer project) | `single_model` (write gated on `model_gate: null` — see note) | `['codex audit unavailable: <reason>']` |
| Any violation | `CLEAN_SINGLE` (ai-dev-team) | gated by §3.5b-2a (Re-spawn / STOP / Accept — per user choice) | per user choice |
| Any violation | SAME violation classification | `contract_violated` | `['<initial-blocker>']` (verbatim — same defect both attempts) |
| Any violation | DIFFERENT violation classification | `contract_violated` | `['<retry-blocker>']` (retry phrasing wins; initial recorded in Log per §3.5b Historical-event storage rule) |
| Any violation | classifier exit-2 (crash on retry) | `contract_violated` | `['<initial-blocker>'; 'classifier crash on retry: <stderr-excerpt>']` |

**Matrix B — `CLEAN_SINGLE` policy-gate re-spawn (entered when §3.5b-2a Option 1 "Re-spawn" is chosen for an ai-dev-team `CLEAN_SINGLE` initial):**

| Initial (policy-gated) | Re-spawn class | Final `*_audit_evidence` | Final `*_audit_blockers` |
|---|---|---|---|
| `CLEAN_SINGLE` + policy gate | `CLEAN_DUAL` | `dual_model` (write gated on `model_gate: null` — see note) | `[]` |
| `CLEAN_SINGLE` + policy gate | `CLEAN_SINGLE` (Codex still stalled) | re-render §3.5b-2a banner with attempt-2 reason | per final user choice |
| `CLEAN_SINGLE` + policy gate | Any violation (one of 10) | `contract_violated` | `['<retry-blocker>']` |
| `CLEAN_SINGLE` + policy gate | classifier exit-2 (crash) | `contract_violated` | `['classifier crash on §3.5b-2a re-spawn: <stderr-excerpt>; initial CLEAN_SINGLE preserved at <raw-path-attempt-1>']` |

The SAME-violation, DIFFERENT-violation, and classifier-exit-2-on-retry cases route to the AWAITING YOUR INPUT terminal banner (the standalone terminal banner in skills/cross-audit/SKILL.md §3.4d for standalone mode, or the feature-mode contract-violation terminal banner §3.5b-2d for feature-flow — NOT the per-finding triage banner, which has no findings to present when the classifier gate blocked the read). All blocker phrasing is sanitized through the §3.5b Orchestrator blocker sanitization rule before being recorded. **Two distinct blocker sources, by outcome:** the clean path (`CLEAN_DUAL` → `[]`; `CLEAN_SINGLE` consumer → Codex-fail-open reason) records the classifier's `blockers_yaml` field verbatim; the `contract_violated` path records the classifier's `violation_blocker` phrasing per the source rule above. `blockers_yaml` MUST NOT be used as the blocker source on the `contract_violated` path — for most violation classes it is `[]`, which would erase the active violation phrasing that §3.5b's Historical-event storage rule requires. Classifier `stderr` excerpts in the exit-2 rows are also orchestrator-sanitized before embedding.

**Clean-recovery rows re-evaluate `model_gate`/`head_gate`/`rules_gate` (note for Matrix A `→ CLEAN_DUAL` / `→ CLEAN_SINGLE (consumer)` rows and Matrix B `→ CLEAN_DUAL` row).** When a retry / re-spawn recovers to a clean classification, the final `*_audit_evidence` write is gated on ALL of `model_gate: null` (§3.5b-2e), `head_gate: null` (§3.5b-2f), and `rules_gate: null` (§3.5b-2g) — each gate is re-evaluated on the **recovered-clean retry's JSON**, identically to the §3.5b-2 step-4 exit-0 branch. All three null → write the final evidence as the matrix row specifies; a non-null `model_gate` / `head_gate` / `rules_gate` on the recovered-clean retry JSON → route to the corresponding gate (§3.5b-2e / §3.5b-2f / §3.5b-2g) INSTEAD of writing the evidence. Because the violation retry / policy-gate re-spawn already consumed attempt2, the shared transport budget is spent, so §3.5b-2e skips its MISSING retry and raises the banner directly (Option 1 = "Retry from scratch", per the budget-conditional rule); `head_gate` and `rules_gate` never consume the transport budget (their re-spawn options are semantic iterations), so a recovered-clean retry that re-attests a mismatch or degradation routes to the §3.5b-2f / §3.5b-2g banner directly.

##### 3.5b-2c Capture-failure and classifier-crash banners

**Capture-failure banner** (atomic write of the `.raw.txt` or sidecar JSON failed) — without a captured response a retry would erase the diagnostic, so the flow STOPS:

---
## ⏸ AWAITING YOUR INPUT

Cross-auditor returned with contract violation `<classification>`, but raw-response capture FAILED at `<capture-path>.tmp`: `<errno message>`.

Without a captured response, a retry would erase the diagnostic evidence. Three options:

1. **Fix the filesystem issue** (clear disk, fix permissions) and re-run `/feature continue` — the recovery flow resumes from "capture + retry" with the diagnostic preserved.
2. **Skip capture and retry anyway** (LOSSY — diagnostic lost). Record `<phase>_audit_evidence: contract_violated` with blocker `'capture failed and skipped: <errno>; retry attempt-2 result <classification>'`.
3. **Ship as-is** without retry — `<phase>_audit_evidence: contract_violated` with blocker `'capture failed; no retry attempted: <errno>'`.

**Which option?**

---

**Classifier-crash banner** (`hooks/lib/check_dispatch_response.py` exited 2 — its own failure; distinct from a contract violation because we do not know whether the response was valid):

---
## ⏸ AWAITING YOUR INPUT

`hooks/lib/check_dispatch_response.py` exited with code 2 (classifier crash). Stderr:

```
<classifier stderr verbatim, truncated to 1000 chars>
```

Raw response captured to `<capture-path>` for manual inspection. Three options:

1. **Re-run the classifier with `--debug`** (re-enables the full traceback to stderr; user pastes paths) — the orchestrator does NOT auto-retry; the user diagnoses.
2. **Manual self-verify** per `feedback_iter_2_audit_fallback.md` six criteria — the orchestrator proceeds with `<phase>_audit_evidence: self_fallback` and blocker `'classifier crash + manual self-verify: <stderr-excerpt>'`.
3. **Re-spawn cross-auditor** ignoring the classifier crash — treat as if the classifier had returned `MISSING_FOOTER` and follow the §3.5b-2b matrix; the classifier is invoked again on the retry.

**Which option?**

---

##### 3.5b-2d Feature-mode contract-violation terminal banner

For the SAME-violation / DIFFERENT-violation / classifier-exit-2-on-retry branches of the §3.5b-2b retry-outcome matrix in **feature mode** — an Exit-1 violation that the one bounded retry did NOT recover. The §3.5a / callsite-2 gate prose states the classifier output **gates** whether triage runs: on an unrecovered violation no trusted findings were read, so there is nothing for the per-finding triage banner to present. This banner is the feature-mode counterpart of the standalone §3.4d terminal banner — both halves of the handshake terminate symmetrically. The orchestrator records `<phase>_audit_evidence: contract_violated` with the §3.5b-2b matrix blocker, then renders:

---
## ⏸ AWAITING YOUR INPUT

Cross-auditor contract violation — auto-respawn attempted, classifier output:
- attempt-1: `<initial-classification>` — `<initial-blocker>` (capture: `<raw-path-attempt-1>`)
- attempt-2: `<retry-classification>` — `<retry-blocker>` (capture: `<raw-path-attempt-2>`)

The classifier gate prevented findings from being read, so there is no per-finding triage to run. Spec frontmatter is set to `<phase>_audit_evidence: contract_violated`. Options:

1. **Manual self-verify** per `feedback_iter_2_audit_fallback.md` six criteria — read the raw responses, decide whether to proceed; the orchestrator records `<phase>_audit_evidence: self_fallback` with the named cause + tracking entry.
2. **Retry from scratch** — re-run the cross-audit (the cross-auditor is re-spawned with the same parameter block), treating the unrecovered violation as a transient transport failure.
3. **Ship as-is** — keep `<phase>_audit_evidence: contract_violated`; the spec carries the degraded-flag glyph and the active violation phrasing in `<phase>_audit_blockers`.

**Which option?**

---

##### 3.5b-2e Model-attestation gate

Fires on classifier **exit 0** when the classifier JSON carries `model_gate` non-null (set only when `--expected-claude-model claude-opus` was passed AND the classification is `CLEAN_*`; violations and exit-1 supersede — their retry machinery runs first, and the gate is re-evaluated on a recovered-clean retry's JSON). The two gate values: `MODEL_ATTESTATION_MISSING` (the cross-auditor's `claude_model` line is absent/malformed) and `MODEL_DEGRADED` (attested model does not start with `claude-opus` — e.g. a silent Fable→Opus fallback at spawn, or `claude_model: unknown`).

**Exit-0 decision table.** Evaluated ON the §3.5b-2 step-4 exit-0 branch, **policy_gate FIRST, model_gate SECOND**, before the evidence copy into spec frontmatter:

| policy_gate | model_gate | route |
|---|---|---|
| null | null | PROCEED (unchanged) |
| null | set | model-gate protocol below |
| STOP_AND_DISCUSS | null | §3.5b-2a banner (unchanged) |
| STOP_AND_DISCUSS | set | §3.5b-2a banner FIRST, with one preamble line added: `Note: model_gate=<value> also fired (attested <claimed>).` After the policy-gate resolution: a re-spawn re-evaluates BOTH gates on the new JSON; an accept-single_model outcome falls through to the model-gate protocol on the SAME JSON |

**Model-gate protocol:**

- `MODEL_ATTESTATION_MISSING` → ONE transport retry with **identical params** (the agent forgot the line; does NOT consume `*_audit_iteration`). The retry's response is captured by the universal §3.5b-2 step-1 capture under the existing `contract-violation-iter<N>-attempt<M>.raw.txt` stem — the clean-response-under-a-`contract-violation-*`-name overload is pre-existing §3.5b-2 behavior, deliberately kept; no new stem. Still MISSING after the retry → banner below. MISSING-retry outcome cases: clean + match → PROCEED; clean + still MISSING → banner; clean + DEGRADED → banner (degraded phrasing); exit-1 violation → §3.5b-2b matrix with the retry budget consumed (terminal banner row); exit-2 → §3.5b-2c classifier-crash banner.
- `MODEL_DEGRADED` → banner immediately (no auto-retry — the user decides; the fallback may be transient OR a quota outage).

**Retry accounting (shared with §3.5b-1, no parallel counter).** The model-gate MISSING retry IS a §3.5b-1 attempt: it uses the next `-attempt<M>` index (normally attempt2) and the same capture-path scheme — never overwrites prior captures. The ONE-transport-retry budget is **per (callsite, iteration)** and SHARED across §3.5b-2b violation retries, §3.5b-2a Matrix-B re-spawns, and this gate. If attempt2 is already consumed (e.g. an exit-1 violation retry recovered to CLEAN but attestation is missing) → skip the retry, banner directly.

**Banner** (AWAITING YOUR INPUT, mirrors §3.5b-2a). **Option 1 is BUDGET-state-conditional** — the discriminator is whether the shared transport attempt2 is consumed, NOT the gate value. It applies identically to `MODEL_DEGRADED` AND `MODEL_ATTESTATION_MISSING` (a DEGRADED entry can arrive budget-spent: MISSING → transport retry → clean+DEGRADED, or an exit-1 violation retry recovering to clean+DEGRADED). attempt2 UNCONSUMED → Option 1 = "Re-spawn cross-auditor" (consumes attempt2). attempt2 CONSUMED → Option 1 = "Retry from scratch" — a new SEMANTIC iteration consuming `*_audit_iteration`, NOT a third transport attempt (attempt3 is forbidden; the unbounded same-gate re-spawn loop is the failure mode this precondition kills). Every budget-exhausted banner (MISSING-after-retry AND DEGRADED-after-retry alike) lists both capture paths (`...-attempt1.raw.txt`, `...-attempt2.raw.txt`) in its summary, mirroring the §3.5b-2d terminal-banner shape.

---
## ⏸ AWAITING YOUR INPUT

Model attestation gate fired — `model_gate=<value>`. Cross-auditor attested `<claimed>`; the audit half is expected to run `claude-opus*`. iter=`<N>`.

[If attempt2 consumed:] Captures: `<raw-path-attempt-1>`, `<raw-path-attempt-2>`.

Options:

1. **Re-spawn cross-auditor** (attempt2 unconsumed) / **Retry from scratch** (attempt2 consumed — a new semantic iteration consuming `*_audit_iteration`; attempt3 is forbidden) — the outcome is re-evaluated by the same gate, bounded per the rule above.
2. **Accept degraded run** — the findings stay valid (the Opus half ran, not an absent half); record the Log directive and proceed. The evidence enum is untouched.
3. **STOP and discuss** — pause; review Fable quota / outage.

**Which option?**

---

**Log grammar (FEATURE MODE — append-only spec Log, written for every gate firing AND for the chosen action; the standalone flow has no spec Log and uses the §Standalone mapping sidecar+workdoc destinations in `skills/cross-audit/SKILL.md`):**

`- YYYY-MM-DD: model_degraded — cross-auditor attested <claimed>; expected claude-opus*; iter=<N>; action=<respawn|accepted|stopped>`

`<claimed>` is sanitized via the §3.5b Orchestrator blocker sanitization rule before embedding. Match-success runs log nothing (no noise; the sidecar JSON already carries `claude_model`).

##### 3.5b-2f Audited-HEAD gate

Fires on classifier **exit 0** when the classifier JSON carries `head_gate` non-null (set only when `--expected-head "$(git rev-parse HEAD)"` was passed AND the classification is `CLEAN_*`; violations and exit-1 supersede — their retry machinery runs first, and the gate is re-evaluated on a recovered-clean retry's JSON). The two gate values: `HEAD_ATTESTATION_MISSING` (the cross-auditor's `audited_head` line is absent/malformed) and `HEAD_MISMATCH` (attested oid does not equal the expected feature-branch HEAD).

**Gate order — policy_gate FIRST, model_gate SECOND, head_gate THIRD.** `head_gate` is acted on ONLY after `policy_gate` and `model_gate` have resolved null/cleared (the §3.5b-2 step-4 exit-0 branch). The classifier computes `head_gate` INDEPENDENTLY of the other gates, so a co-fire JSON carries multiple non-null gates at once; the ordering is enforced here in orchestrator consumption, not in the classifier. On a policy/model re-spawn, all gates are re-evaluated on the new JSON.

**No transport-retry, no auto-retry.** `head_gate` NEVER consumes the shared §3.5b-1 one-transport-retry budget and never auto-retries. BOTH values (`HEAD_ATTESTATION_MISSING` AND `HEAD_MISMATCH`) route directly to the canonical audited-HEAD mismatch banner (the same banner as the §Hand-off audited-HEAD gate) — its **Re-audit the delta** option IS the retry (a SEMANTIC iteration that re-spawns the cross-auditor and re-pins the new HEAD). There is no §3.5b-2e-style MISSING transport retry for this gate.

##### 3.5b-2g Degraded-rules gate

Fires on classifier **exit 0** when the classifier JSON carries `rules_gate` non-null (set only when `--require-rules-loaded` was passed AND the classification is `CLEAN_*`; violations and exit-1 supersede — their retry machinery runs first, and the gate is re-evaluated on a recovered-clean retry's JSON). The two gate values: `RULES_NOT_LOADED` (the cross-auditor attested `rules_loaded: false` — the R-rule cluster did not load, e.g. an unreachable rules file or an unset `project_type`) and `RULES_ATTESTATION_MISSING` (the `rules_loaded` line is absent/malformed when the flag was passed).

**Gate order — policy_gate FIRST, model_gate SECOND, head_gate THIRD, rules_gate FOURTH.** `rules_gate` is acted on ONLY after `policy_gate`, `model_gate`, and `head_gate` have resolved null/cleared (the §3.5b-2 step-4 exit-0 branch). The classifier computes `rules_gate` INDEPENDENTLY of the other gates, so a co-fire JSON carries multiple non-null gates at once; the ordering is enforced here in orchestrator consumption, not in the classifier. On a policy/model/head re-spawn, all gates are re-evaluated on the new JSON.

**No transport-retry, no auto-retry, NO auto-proceed.** `rules_gate` NEVER consumes the shared §3.5b-1 one-transport-retry budget and never auto-retries. Rules degradation is an environment condition (unreachable rules file / unset `project_type`) — an identical-params transport retry hits the same environment and re-attests the same degradation, so there is no automatic proceed. BOTH values (`RULES_NOT_LOADED` AND `RULES_ATTESTATION_MISSING`) route directly to the banner below.

---
## ⏸ AWAITING YOUR INPUT

Degraded-rules gate fired — `rules_gate=<value>`. The R-rule cluster did not load for this audit (reason: `<rules_reason|absent>`); the findings cover focus-areas only, not the project-specific rule cluster. iter=`<N>`.

Options:

1. **Fix environment and re-spawn** — restore the rules-file reachability (`CLAUDE_PLUGIN_ROOT` / the plugin checkout) and set `project_type` in the spec frontmatter or `.ai-dev-team.yml` (or declare `project_type: none` for a legitimately typeless project). Then a SEMANTIC re-spawn (consumes `*_audit_iteration`; the refreshed findings re-attest) with all gates re-evaluated on the new JSON.
2. **Accept degraded run** — the findings stay valid as focus-areas-only coverage; record the Log directive and proceed. The evidence enum is untouched (`dual_model` stays `dual_model` — rules coverage is orthogonal to model count; the Log line is the honest record).
3. **STOP and discuss** — pause; review the environment cause.

**Which option?**

---

**Log grammar (append-only spec Log, written for every gate firing AND for the chosen action):**

`- YYYY-MM-DD: rules_gate — <value>; reason=<rules_reason|absent>; iter=<N>; action=<respawn|accepted|stopped>`

`<rules_reason>` is sanitized via the §3.5b Orchestrator blocker sanitization rule before embedding (absent → the literal `absent`). Clean runs log nothing (no noise; the sidecar JSON already carries `rules_loaded`).

### 3.5c Stop criteria

Per MISSION rule #11 (spec/code audit stop criteria) and MISSION rule #10 (orchestrator-delegation discipline) as the paired control. This subsection documents how the rules apply at orchestrator-runtime decision points after each cross-audit iteration. Applies to BOTH spec audit (§3.5 Pass 2) and code audit (§Code audit Pass 2) phases.

**Three signals direct the orchestrator to stop blind cross-auditor re-spawns and run a comprehensive sweep instead of a surgical retry:**

1. **REOPEN finding** — the cross-auditor flags a sibling at a parallel surface of a previously-fixed defect class. Run a comprehensive sweep BEFORE the next iter — do not surgically patch the named surface and re-spawn.
2. **Same-defect-class continuation on 2+ consecutive iters** — comprehensive sweep covering ALL parallel surfaces of that class. Different IDs, same defect shape, two iters in a row = stop and sweep.
3. **Hard cap iter ≤ 5** for both spec audit and code audit. Cap exceeded only with explicit Log-line justification matching the §3.1c canonical regex `^- [0-9]{4}-[0-9]{2}-[0-9]{2}: (spec|code) audit iteration > 5 justified [—-] .+$`.

**Paired control with rule #10 — context refresh is mandatory.** The comprehensive sweep on REOPEN OR same-defect-class on 2+ iters MUST be performed AFTER `/compact` (working-memory reset) OR by spawning a fresh-context subagent (developer-senior or cross-auditor) that re-reads the artifact from disk. Polluted-orchestrator surgical retries are the failure mode this case study established (see `2026-04-27-audit-evidence-enum.md`). The orchestrator records WHICH refresh path was used in the spec Log:

- `- YYYY-MM-DD: REOPEN sweep — context refreshed via /compact`
- `- YYYY-MM-DD: REOPEN sweep — context refreshed via fresh @<agent>`

**Phase split — spec audit (§3.5 Pass 2) is gating, not hard-blocking.**

When iteration count reaches `iter ≥ 5` cap OR a REOPEN-cycle trigger fires from the cross-auditor, the orchestrator MUST present the banner below — no silent escape to Implement remains.

---
## ⏸ AWAITING YOUR INPUT

**Audit iteration cap reached.** Per MISSION rule #11 spec-audit gating-not-hard-blocking semantics, the orchestrator pauses for explicit user direction at the cap. Choose one:

1. **Continue with justification** — defect class still converging OR comprehensive sweep producing value. Requires Log-line justification matching the §3.1c canonical regex `^- [0-9]{4}-[0-9]{2}-[0-9]{2}: (spec|code) audit iteration > 5 justified [—-] .+$` BEFORE iter-6 starts.
2. **Accept residue with explicit sign-off** — user names the specific residue being shipped open; orchestrator appends Log line `- YYYY-MM-DD: spec audit residue accepted at iter-N — <verbatim user rationale>` and proceeds to Implement.
3. **Scope-cut** — drop part of the spec; orchestrator trims §5 Implementation Checklist per user direction; returns to Pass 1 self-review for the reduced scope.
4. **Abandon** — close spec without ship; sets `status: DISCARDED`; appends Log line `- YYYY-MM-DD: spec abandoned at iter-N audit cap — <verbatim user rationale>`.

**Which option?**

---

Per `docs/user-input-banner-convention.md` inverse rule: the banner above appears ONLY at the iter ≥ 5 cap OR a REOPEN-cycle trigger. Routine residue-recording at iter ≤ 4 does NOT show this banner.

**Phase split — code audit (§Code audit Pass 2) preserves the closed gate.** The per-finding `fix` / `accept` / `defer` mechanism remains the only legitimate way to clear CRITICAL/HIGH findings. Stop criteria here means "stop blind re-spawning of the cross-auditor" — when the comprehensive sweep finds no new parallel surfaces, the residue is funneled through per-finding triage:

- `accept` with rationale (deliberate risk acceptance, or false-positive call with explanation),
- `defer` with follow-up spec slug (genuine future work the merge does not block on),

— **NOT skip-to-hand-off**. The iteration cap counts cross-auditor re-spawns. Funneling residue through per-finding triage IS the legitimate exit from the audit loop; the cap protects against the polluted-orchestrator-keeps-re-spawning failure mode, NOT against the closed gate itself.

**Hard-cap escape hatch** (rule #11 §3.1c). When a spec legitimately needs > 5 iters (cross-cutting refactor with many surfaces, security-sensitive code where verification rigor IS the value, first-of-class spec introducing new design patterns), append a Log line matching the §3.1c canonical regex BEFORE iter-6 starts. Recognition is by ERE regex (NOT free-floating substring) — the regex requires BOL Log-entry prefix, phase token (`spec` or `code`), literal middle ` audit iteration > 5 justified`, mandatory space + dash (em-dash or ASCII hyphen) + space separator, and a non-empty reason tail. Empty tails fail to match.

### 3.5d Orchestrator branch-guard (post-cross-audit primary-worktree assertion)

An incident (2026-06-16) left the PRIMARY worktree's HEAD checked out on `main` instead of the feature branch after a cross-audit, so every subsequent orchestrator action (commit + Log + checkoff + smoke) silently landed on a broken `main` base and passed smoke as a false-green. This branch-guard plus the §3.2 read-only-git contract neutralize that drift REGARDLESS of isolation — the cross-auditor now runs IN-PLACE by default (worktree only in PR / `--materialize` / `--worktree` mode), so the read-only contract is the front-line defense and this guard is the orchestrator-side backstop, now MORE load-bearing because a default in-place audit shares the primary working tree instead of an isolated copy. The existing developer-side `Pre-commit branch assertion` (`skills/feature/references/developer-workflow.md` §Git Workflow) did NOT catch it because those were ORCHESTRATOR actions, which never pass through the developer-only assertion. The **branch-guard** below closes that gap for the orchestrator's own post-cross-audit git / commit / Log / checkoff writes. It reuses ONLY the branch-assertion INTENT (never proceed off the captured branch; never on `main`/`master`) — NOT the developer rule's mechanics: the restore target is the captured `pre_spawn_branch` (NOT the frontmatter `branch:`), and a gone branch is recreated at `pre_spawn_head` (NOT at `<base>`).

The branch-guard wraps EVERY cross-auditor return in `/feature`. Run step 1 BEFORE the spawn, steps 2-6 AFTER control returns, BEFORE any further git / commit / Log / checkoff action. It is invoked from all FIVE guarded callsites (1 spec-audit Pass 2; 2 code-audit Pass 2 initial; 3 code-audit triage-loop re-spawn; 4 Continue-mode resume re-spawn; 5 continuous per-step diff-audit). The HEAD-comparison mode differs by callsite (strict equality for callsites 1-4; ancestor for callsite 5).

1. **Capture (before spawn).** Record `pre_spawn_branch` = `git branch --show-current` and `pre_spawn_head` = `git rev-parse HEAD`. Also read `expected_branch` (spec frontmatter `branch:`). If `pre_spawn_branch` is empty (detached HEAD), record `pre_spawn_branch=DETACHED` and treat any post-spawn mismatch as the step-4(a) detached-HEAD hard-stop.
   - **Implement-phase pre-spawn precondition (callsites 2-5 ONLY).** BEFORE the spawn, assert `pre_spawn_branch == expected_branch` AND `pre_spawn_branch ∉ {main, master}`. On mismatch → STOP, AWAITING-YOUR-INPUT: orchestrator was already off the feature branch before the spawn (already on `main`/`master`, or on a different branch than `expected_branch`); restore to `expected_branch` + re-capture `pre_spawn_head` before spawning, or surface for manual decision. Do NOT spawn. This is the enforced gate for the step-3 callsites-2-5 `pre_spawn_branch == expected_branch` invariant — without it a pre-spawn off-branch state (e.g. ALREADY on `main`) reads back as a false-green at step 3 (post-spawn branch == pre_spawn_branch == `main`, both checks satisfied).
   - **Callsite-1 (spec-audit Pass 2) is EXEMPT** from this precondition: the feature branch may not exist yet, so `pre_spawn_branch` is legitimately the base (`main`/`master`). Capture `pre_spawn_branch`/`pre_spawn_head` as-is; do NOT assert `== expected_branch` or `∉ {main, master}` for callsite 1.
2. **Re-read (after return).** Run `git branch --show-current` + `git rev-parse HEAD`.
3. **HEAD-comparison mode depends on callsite:**
   - **Callsites 1-4** (phase-level audits — no legit commit happens during them): require current branch == `pre_spawn_branch` AND **strict equality `HEAD == pre_spawn_head`**. For callsites 2-4 (Implement phase) the step-1 pre-spawn precondition already enforced `pre_spawn_branch == expected_branch` AND `pre_spawn_branch ∉ {main, master}`; re-assert the SAME condition post-spawn — current branch must STILL equal `expected_branch` and STILL be `∉ {main, master}` (callsite 1 EXEMPT — base is legit there).
   - **Callsite 5 ONLY** (diff-audit — runs in parallel with the impl chain; legitimate append-only fixup commits MAY advance HEAD): the step-1 pre-spawn precondition already enforced `pre_spawn_branch == expected_branch` AND `pre_spawn_branch ∉ {main, master}`; re-assert current branch == `pre_spawn_branch` (== `expected_branch`, still `∉ {main, master}`) AND `pre_spawn_head` is an ancestor of the current HEAD via `git merge-base --is-ancestor <pre_spawn_head> HEAD`. A non-ancestor HEAD (history rewrite) is a violation, not a legit advance. Callsites 1-4 must NOT use ancestor-mode — strict equality is required there.
4. **On violation, split recovery by failure class** (the recovery MUST restore the SAME invariant the step-3 check asserts; a plain `git checkout` does not move a branch tip, so HEAD-moved violations are NOT checkout-recoverable):
   - **(4a) Detached HEAD** (`pre_spawn_branch=DETACHED`, or current `git branch --show-current` empty): hard-stop AWAITING-YOUR-INPUT banner — the orchestrator cannot safely guess a restore target. Do NOT continue.
   - **(4b) Wrong branch** (current branch != `pre_spawn_branch`, both non-empty): restore via `git checkout <pre_spawn_branch>`; or **if that branch is gone, recreate it at the captured tip** `git checkout -b <pre_spawn_branch> <pre_spawn_head>` (recreate at `pre_spawn_head`, NOT at base — base would discard the captured state). Append Log `- YYYY-MM-DD: branch-guard — cross-audit left primary on <observed>; restored to <pre_spawn_branch>@<sha>`. Re-verify branch == `pre_spawn_branch`, then re-apply the step-3 HEAD check.
   - **(4c) Branch correct but HEAD check fails** (callsites 1-4: `HEAD != pre_spawn_head`; callsite 5: `pre_spawn_head` not an ancestor of HEAD): this is the **HEAD-moved-on-correct-branch hard-stop** — NOT checkout-recoverable (`git checkout` is a no-op when the branch is already right). Raise an AWAITING-YOUR-INPUT banner reporting `pre_spawn_head` vs current HEAD and offering a manual `git reset`/revert decision (do NOT auto-reset — same rationale as step 6). Do NOT imply checkout fixes it. Do NOT continue.
5. **Continue-gate — blocks on branch AND HEAD AND expected_branch.** NEVER continue the per-step loop / Log / checkoff while ANY of: the branch != `pre_spawn_branch`; the callsite's step-3 HEAD condition is unsatisfied; or (**callsites 2-5 ONLY**) `pre_spawn_branch` (and hence the current branch) != `expected_branch` OR `pre_spawn_branch ∈ {main, master}`. The gate blocks on ALL applicable conditions, not branch alone — otherwise a branch-correct / HEAD-wrong state OR a pre-spawn-already-on-`main` state (both false-greens this guard prevents) slips through. Callsite 1 is EXEMPT from the expected_branch term (base is legit there).
6. **Local-base divergence is NOT auto-reset.** If the guard detects that the local base branch (`main`/`master`) was advanced by a stray commit while HEAD was off-branch, it MUST NOT run `git reset --hard` automatically (the trigger predicate is fuzzy and the command is destructive — a wrong call nukes real local commits). Instead append Log `- YYYY-MM-DD: branch-guard — local <base> may carry a stray audit-induced commit; manual review required` and raise an AWAITING-YOUR-INPUT **no-auto-reset --hard base-divergence banner** offering: (a) `git reset --hard origin/<base>` after the user confirms the stray commit is audit-induced and not a real merge, or (b) leave it for manual cleanup. `<base>` is resolved via the orchestrator's existing base-detection idiom `git branch -r | grep -E 'origin/(master|main)$'` (NOT assumed). The guard's own job is only: restore the feature branch, refuse to proceed off-branch, surface the base divergence.

---

## Implement

### Baseline test

Before spawning any developer, detect the base branch (`git branch -r | grep -E 'origin/(master|main)$'` — prefer `master` if both exist), ensure you are on it (or the branch specified in the spec `branch:` field), then run the **verifier** subagent:

```
project_path: <project_path>
```

- **PASS**: proceed to agent selection.
- **FAIL**: stop. Report to user: "Baseline is not clean — N test(s) failing before any new code. Resolve these first or they'll be falsely attributed to the new feature."
- **No test suite detected** (verifier detects no test config): skip this step and note it in the spec Log.

Note: verifier runs against the current checkout — make sure the base branch is checked out before calling it.

### Agent selection

Before starting implementation, ask the user which agent to use:

See `skills/feature/references/agent-routing.md` for routing triggers and the canonical Log format.

---
## ⏸ AWAITING YOUR INPUT

**Which developer should implement this?**

1. **Codex (GPT xhigh — model from ~/.codex/config.toml)** ← default — saves Claude tokens, corporate subscription, use aggressively
2. **Senior (Opus)** — only when Codex falls short: highly ambiguous scope, extensive codebase exploration needed, ultra-complex cross-cutting changes

**Which agent?**

If the current checklist step in §5 carries a `@codex` or `@senior` suffix (case-insensitive; the orchestrator lowercases before matching), evaluate the tag against the routing matrix in `skills/feature/references/agent-routing.md`: the tag is honored iff the step's description matches at least one positive trigger for the tagged agent AND no anti-trigger contradicts it. On honored tag, pre-fill that agent as the banner default and log rationale using the **actual matched positive trigger** — one of `T-C1` / `T-C2` / `T-C3` for `@codex`, one of `T-S1` / `T-S2` / `T-S3` / `T-S4` / `T-S5` for `@senior` (never `T-S0`, which is reserved for the fallback case where no positive trigger matched) — with `notes=pre-tagged by spec author` appended. Log only after the user confirms the banner pick (rationale-logging fires post-confirmation per the existing Agent-selection flow); if the user overrides the tagged default, log the final pick with its own rationale, not the tag's. On tag-trigger mismatch (tag present but positive-trigger check fails, or an anti-trigger hits), treat as untagged and emit a one-line preamble warning above the banner noting the mismatch. On malformed tag (unknown agent, wrong spacing, or any suffix form other than `@codex`/`@senior`), hard-stop with a banner asking the user to correct the checklist line before continuing — do NOT silently untag. Untagged steps → use the routing matrix triggers as today.

**Remember the choice**: once the user has picked an agent, append to the spec Log per the canonical format in `skills/feature/references/agent-routing.md` §Rationale logging. Continue mode reads the most recent `last_agent=` entry from the Log and offers that as the default on resume (the user can still override).

**Set `status: IN_PROGRESS` before dispatch.** After agent selection and BEFORE dispatching the developer, the orchestrator sets the spec frontmatter `status: IN_PROGRESS` (this was formerly the developer's job; it is now orchestrator-owned, because the developer never writes the spec — see `skills/feature/references/developer-workflow.md` §What you write).

#### Option 1: Codex (developer-codex agent)

Spawn `developer-codex` subagent with:
- `spec_path`: path to the spec file
- `workdoc_path`: `<kb_path>/repos/<project>/design/workdocs/<slug>/exec.md`
- `project_path`: path to the source repo
- `task`: steps to implement (works best when spec has explicit file paths and clear requirements)

#### Option 2: Senior (developer-senior agent)

Spawn `developer-senior` subagent with:
- `spec_path`: path to the spec file
- `workdoc_path`: `<kb_path>/repos/<project>/design/workdocs/<slug>/exec.md`
- `project_path`: path to the source repo
- `task`: "full spec" or specific steps

### Orchestrator-sole-KB-writer per-step loop

The orchestrator is the sole KB writer, serially — the developer writes only source-repo commits + `captures/` (including `report.json`) and never the spec or `exec.md` (see `skills/feature/references/developer-workflow.md` §What you write). The orchestrator drives the per-step loop:

1. **Dispatch ONE step at a time** with read-only `spec_path` / `workdoc_path` and a writable `captures/` dir. A PASS gate (step 4) MUST clear before the next step is dispatched — no multi-step batch where a later step's commit lands before an earlier step's fixup, which would span the checker's `git diff <first>^ <last>` range across an unrelated step (spurious scope/semantic verdicts). One-step dispatch keeps each step's commit range contiguous.
2. **The developer** runs its per-step protocol (red → implement → green → probe → lint → commit), writes the captures + `captures/step-NN-report.json`, and returns the report pointer. It does NOT spawn the compliance-checker and does NOT write the spec or `exec.md`.
3. **The developer returns** the `report.json` pointer for the step.
4. **The orchestrator, per step IN ORDER**, reads `report.json`:
   - **If `report.json` `status: blocked`** → to stay coherent with the Continue-mode resume contract, the orchestrator MUST: (a) set spec frontmatter `status: BLOCKED` (NOT leave it `IN_PROGRESS` — Continue-mode routes on frontmatter `BLOCKED`; if left `IN_PROGRESS` it resumes and silently re-dispatches the blocked step); (b) append a Log line in the Continue grammar `- YYYY-MM-DD: BLOCKED — waiting on step N: <blocker>; prior_status=IN_PROGRESS` (the grammar Continue-mode reads for the unblock prompt); (c) leave the step unchecked; (d) STOP. Do NOT copy `observed`, do NOT spawn the checker, do NOT check off (the developer no longer writes the blocker Log, so the orchestrator owns this).
   - **Else (`status: done`)** → in this exact order: (1) **append the R1/R2 justification to the spec Log BEFORE the checker** (the checker reads the spec Log, NOT `observed.notes`, for R1/R2 — see below; if `report.json` carries an R7 convention-shift line the orchestrator appends that too, but as audit-trail, since R5-R7 are NOT checker-gated); (2) copy EVERY `observed` field from `report.json` into `exec.md` `observed` (`actual_files_touched`, `commit_shas` — UNION on rework, never overwrite, preserving the checker's "ordered list of ALL commits incl fixup" precondition; `commit_message_grep`; `red_capture`; `green_capture`; `probe_capture`; `notes`); (3) spawn `spec-compliance-checker` (it reads `exec.md` + the spec Log from disk — its contract is UNCHANGED); (4) on **PASS**: check off the step (`- [ ]` → `- [x]`) — checkoff is the ONLY spec write that stays post-PASS — and append the remaining Log (progress + `report.json` `log_note` / `design_decision` / `change_type_shift` not already Logged in step 1); on **FAIL/DRIFT**: write `fix_source: compliance-rework` + `boundary_inputs:` (or `boundary_inputs_na:`) into the affected step N's planned block per §Fix-dispatch contract BEFORE the re-dispatch, then re-dispatch the developer with the issues per §Fix-dispatch contract (root cause + invariant + input domain) → the developer re-commits (APPENDS the fixup SHA) + rewrites `report.json` → the orchestrator re-copies `observed` (UNION `commit_shas`) + re-spawns the checker (the justification Log from step 1 is append-once — see below, NOT re-appended on re-spawn). The rework sub-loop is orchestrator-side.

**Append R1/R2 justification to the spec Log BEFORE spawning the checker.** The compliance-checker reads the **spec Log** (not `observed.notes`) for R1/R2 justification (it gates R1/R2/R3/R8; R5-R7 are convention-text references, NOT checker-gated — see `agents/spec-compliance-checker.md`): R2 requires a `- YYYY-MM-DD: core test <file> changed …` Log entry (plus matching spec §3 intent) before it PASSes a core-test assertion edit; R1 expects the public-API reason in the spec Log. So when `report.json` carries an R1/R2 justification (`log_note` / `notes`), the orchestrator MUST append it to the spec Log in the checker-readable grammar BEFORE spawning the checker — R2 = `- YYYY-MM-DD: core test <file> changed …`, R1 = the public-API reason. An R7 convention-shift line (`report.json` `notes`) is also appended to the spec Log, but as audit-trail only — R7 is not checker-gated, so its Log append is a record, not a checker precondition. This append is **append-once before the first checker spawn for the step**: on a FAIL/DRIFT re-spawn, do NOT re-append the same justification (idempotent — the Log entry already exists from the first spawn). Only the `[ ]→[x]` checkoff stays post-PASS. (Contrast R3: only R3's regression description rides `report.json` `notes` → `observed.notes` → the checker — the checker reads R3 from `observed.notes`, but R1/R2 from the spec Log.)

**Copy observed BEFORE spawning the checker.** Because the orchestrator copies every `report.json` field into `exec.md` `observed` BEFORE spawning the compliance-checker, the checker reads `exec.md` exactly as before (including `commit_message_grep` for its tier-1 SHA-rewrite fallback). For this to hold, `report.json` MUST carry every `observed` field the checker reads (per the schema in `skills/feature/references/developer-workflow.md`).

**Continue-mode reconcile rule (crash-safety).** Continue resumes from the first unchecked `- [ ]` step. A crash after the developer commits + writes `report.json` but before the orchestrator's checkoff leaves a committed-but-unchecked step. Reconcile: if an unchecked step has BOTH `report.json` AND the commit present in `captures`/git → ingest the report + run the checker (do NOT blind re-dispatch). The durable triad = commits (git) + captures + `report.json`, all surviving any crash.

### Fix-dispatch contract

Every developer dispatch that fixes a failure — compliance FAIL/DRIFT rework, verify-FAIL rework, code-audit finding fix, diff-audit finding fix — MUST carry three fields. A dispatch with any of the three absent is BLOCKED; the orchestrator derives them from the failure Description + the code BEFORE dispatching, never from the suggestion's letter:

- **root cause** — why the failure happens, not just where it surfaced.
- **invariant** — what must hold after the fix.
- **input domain / adversarial members** — the class of inputs/states to cover, not just the observed example.

The finding's `Fix (advisory)` line is one hypothesis, never the contract — the remedy derives from the failure, not from the suggestion's letter.

**Boundary-inputs write rule (R3-FC gate precondition).** BEFORE any fix dispatch, the orchestrator (sole KB writer) writes into the fix step's NUMERIC planned block two machine-readable keys: `fix_source:` — one of `code-audit X<id>` / `diff-audit X<id>` / `verify-fail` / `compliance-rework` — and EITHER `boundary_inputs:` (a YAML list of concrete failure-class members the fix's test battery must exercise, sourced from the finding's `failure_class` field when present, else derived from the input-domain field above) OR `boundary_inputs_na:` (a string justifying that the failure is genuinely not class-shaped). Silence is NOT an opt-out: a fix step carrying `fix_source:` with NEITHER `boundary_inputs:` NOR `boundary_inputs_na:` FAILs the compliance-checker's R3-FC gate (fail-closed — orchestrator omission cannot silently disable the gate). Write-targets per flow (all NUMERIC steps — no non-numeric block form exists): compliance FAIL/DRIFT rework and verify-FAIL rework → the affected step N's planned block; diff-audit finding fix → the OWNING step N (the step whose commit range produced the finding); code-audit finding fix → an APPENDED numeric step N (= max existing step number + 1, per the `/feature extend` precedent — see §Code audit Pass 2 step 5 "Dispatch fix workers").

### Continuous parallel diff-audits (large multi-step features — opt-in)

For LARGE multi-step features (later steps build on earlier code), do NOT defer all auditing to the Phase-5 code-audit gate. Run narrow cross-audits CONTINUOUSLY, in parallel with implementation: as each step (or small batch) lands its commit, audit that step's diff in an isolated worktree while the main implementation chain proceeds. Early defect detection — keep a clean base for subsequent code, catch defects before they compound across layers, spread audit load over deltas instead of one large final PR.

**Opt-in, not default.** This applies ONLY to large multi-step features (heuristic: §5 has many steps — e.g. ≥6 — OR the user opts in). Small features keep the single Phase-5 closed gate; do NOT force per-step audits on every feature. At implement-start for a qualifying spec, the orchestrator offers continuous diff-audits via the banner below and logs the choice (`- YYYY-MM-DD: continuous diff-audits=<on|off> (large-feature opt-in)`).

---
## ⏸ AWAITING YOUR INPUT

This spec is large (`<N>` steps). Choose the implementation-phase audit mode:

1. **Continuous parallel diff-audits** ← recommended — audit each step's diff in an isolated worktree as it lands, in parallel with implementation
2. **Single Phase-5 gate only** — defer all auditing to hand-off

**Which auditing mode?**

---

**How the orchestrator runs one step's diff-audit.** When a step's commit lands (its compliance-check has PASSED — see §Orchestrator-sole-KB-writer per-step loop), the orchestrator launches a narrow audit of that step's commit range by invoking the standalone `/cross-audit` skill in ref-range mode with worktree materialization:

`/cross-audit <prev-step-sha>..<step-sha> --mode full --severity high --materialize=worktree`

**branch-guard (callsite 5 — owned by `/feature`, NOT standalone `/cross-audit`).** This is the highest-frequency callsite (once per step + once per fixup). The guard wraps the `/cross-audit … --materialize=worktree` sub-invocation ON THE MAIN WORKTREE: run the §3.5d branch-guard — capture `pre_spawn_branch`/`pre_spawn_head` BEFORE the `/cross-audit` invocation, and after control returns from `/cross-audit` to `/feature` assert current branch == `pre_spawn_branch` (== `expected_branch` in this phase) AND, because legit append-only fixup commits MAY advance HEAD here, the ancestor check `git merge-base --is-ancestor <pre_spawn_head> HEAD` (callsite 5 ONLY uses `merge-base --is-ancestor`; callsites 1-4 use strict `HEAD == pre_spawn_head`) BEFORE the orchestrator does any further git / Log / checkoff. A non-ancestor HEAD is a violation → §3.5d step-4(c) HEAD-moved-on-correct-branch hard-stop. On a wrong-branch violation apply §3.5d step-4(b); the continue-gate blocks on branch AND the ancestor condition. This keeps the change `/feature`-only — `skills/cross-audit/SKILL.md` is unchanged.

`/cross-audit` owns the whole mechanism end-to-end (see `skills/cross-audit/SKILL.md`): it creates a dedicated worktree at `refB` (`git worktree add /tmp/cross-audit-<audit_slug> <refB>`), runs the dual-model `cross-auditor` (Claude + Codex independently → consolidate) against ONLY that commit range, persists findings to KB, and registers worktree cleanup (`git worktree remove --force` + `rm -rf`, best-effort) on completion or error. Do NOT hand-roll the worktree create/cleanup around a direct `cross-auditor` spawn — `/cross-audit` already owns it.

**Mechanics:**
- **Worktree isolation** — the diff-audit runs in `/tmp/cross-audit-<audit_slug>`, a DEDICATED worktree pinned at the step's commit, so it does not contend with the active implementation worktree. NEVER run a diff-audit in the active implementation worktree.
- **Narrow scope** — audit only the step/batch commit range `<prev-step-sha>..<step-sha>`, NOT the whole codebase.
- **Dual-model** — the same dual-model `cross-auditor` machinery as §Code audit Pass 2 (Claude + Codex independently, then consolidate). Per project policy, terminal cross-audit evidence stays `dual_model`.
- **KB single-writer + per-audit findings isolation** — the orchestrator stays the SOLE writer of the spec + `exec.md` (per §Orchestrator-sole-KB-writer per-step loop); the diff-audit cross-auditors REPORT findings only. `/cross-audit` ref-range mode derives a per-range `audit_slug` (`YYYY-MM-DD-range-<sanitized-refA>__<sanitized-refB>` — see the audit_slug derivation in `skills/cross-audit/SKILL.md`) that is inherently UNIQUE per step range, so each step's diff-audit writes a distinct `<audit_slug>-findings.md` and parallel audits never collide on a shared findings file.

**Sequencing & invalidation (does NOT weaken the serial per-step compliance gate).** The per-step COMPLIANCE gate (§Orchestrator-sole-KB-writer per-step loop — one step at a time, gated by the step-4 PASS check before the next dispatch, on the MAIN worktree) is UNCHANGED. The diff-audit is a SEPARATE, non-blocking layer that runs in its own worktree and therefore does not block the impl chain. Every fix is an APPEND-ONLY fixup commit at HEAD (the existing rework sub-loop appends fixup SHAs — it never rebases or amends an already-landed step), so a diff-audit fix never rewrites history and later steps' already-passed compliance ranges (`git diff <first>^ <last>`) are NOT invalidated; the fixup itself gets its own compliance check + diff-audit. On a CRITICAL/HIGH from a diff-audit, the orchestrator PAUSES dispatch of NEW steps until that finding is triaged and the fix re-audited (below). The Phase-5 terminal gate on the full PR diff is the final backstop for anything a narrow diff-audit missed.

**Triage + fix loop (reuses the §Code audit state machine).** Diff-audit findings flow through the SAME finding state machine and per-finding triage as the Phase-5 gate (`OPEN → FIXED → VERIFIED | REOPENED | ACCEPTED | DEFERRED`; per-finding `fix` / `accept` / `defer` with rationale — see §Code audit Pass 2). The orchestrator (sole KB writer) tracks each step's fix/accept/defer decisions itself. On `fix`: developer re-dispatch per §Fix-dispatch contract (orchestrator-side, append-only fixup commit at HEAD), then re-audit by RE-RUNNING the narrow audit over the UPDATED range that now includes the fixup — `/cross-audit <prev-step-sha>..<fixup-sha> --mode full --severity high --materialize=worktree` — a fresh ref-range audit that re-checks whether the finding is resolved. The §3.5d branch-guard (callsite 5, ancestor-mode `merge-base --is-ancestor`) wraps this fixup re-audit invocation on the MAIN worktree exactly as it wraps the initial diff-audit above. Do NOT rely on `/cross-audit`'s findings-doc re-audit-detection to recover the range: ref-range scope is NOT persisted in findings frontmatter (see `agents/references/cross-auditor-output-format.md`), so the range MUST be re-passed explicitly; the orchestrator re-applies its tracked accept/defer decisions to the fresh findings rather than depending on `previously_fixed`/`accepted_ids`/`next_finding_id` auto-derivation (the latter is spec-mode-only). Loop the narrow range until no CRITICAL/HIGH remain `OPEN`/`REOPENED`. §3.5c Stop criteria apply (REOPEN / same-defect-class → comprehensive sweep; iter ≤ 5 cap). The authoritative finding-state record + per-finding triage doc is the Phase-5 terminal gate on the full PR diff. **Concrete fixup compliance gate (makes the "the fixup itself gets its own compliance check" promise above concrete).** On `fix`, BEFORE the developer dispatch the orchestrator writes `fix_source: diff-audit X<id>` + `boundary_inputs:` (or `boundary_inputs_na:`) into the OWNING step's planned block (the step whose commit range produced the finding) per §Fix-dispatch contract; after the fix developer returns `report.json`, the orchestrator copies `observed` (UNION the fixup SHA) + re-spawns `spec-compliance-checker` on that owning step with the §Orchestrator-sole-KB-writer per-step loop step-4 verdict handling (FAIL/DRIFT → re-dispatch → re-copy `observed` → re-spawn; PASS → proceed) BEFORE the narrow re-audit re-runs.

**Does NOT replace the Phase-5 final code-audit gate.** The mandatory §Code audit closed gate on the full PR diff still runs at hand-off. Continuous diff-audits are an early-detection layer that de-risks the terminal gate and keeps the base clean throughout — not a substitute for it.

### Git conventions

Feature skill follows the plugin's canonical Git Workflow — see `skills/feature/references/developer-workflow.md` §Git Workflow. Key points relevant at hand-off: small logical commits per step, no `Co-authored-by`, no pushing (user owns push/PR). The canonical section includes the load-bearing pre-commit branch assertion and post-merge bug flow.

---

## Verify

After implementation is complete, spawn the **verifier** subagent:

```
project_path: <project_path>
spec_path: <spec_path>
scope: <list of changed files from spec checklist>
```

- **PASS**: All results are captured in the workdoc.
  Verify passed. Moving to code audit. Do **not** set a terminal status (`VERIFIED` or `SHIPPED`) yet — wait until the user selects a preserving option (merge, push, or keep). §3.4a applies the correct terminal (`VERIFIED` or `SHIPPED`) after hand-off. Setting a terminal before hand-off means a discard would leave the spec permanently marked terminal with no surviving branch.
- **FAIL**: present failures to user. Analyze the verifier report to identify which checklist step(s) are responsible. Spawn the developer with `rework step N: fix test failure: <relevant excerpt>. Root cause: <root cause>. Invariant: <invariant that must hold after the fix>. Input domain: <input domain / adversarial members to cover>` for each affected step (fields per §Fix-dispatch contract — dispatch blocked while any is absent). Re-verify after fix. At dispatch time the orchestrator also writes `fix_source: verify-fail` + `boundary_inputs:` (or `boundary_inputs_na:`) into the affected step N's planned block per §Fix-dispatch contract; then, after the rework developer returns `report.json` and BEFORE re-running the verifier, the orchestrator copies `observed` (UNION the fixup SHAs) + spawns `spec-compliance-checker` on step N with the §Orchestrator-sole-KB-writer per-step loop step-4 verdict handling (FAIL/DRIFT → re-dispatch per §Fix-dispatch contract → re-copy `observed` → re-spawn the checker; PASS → proceed) — re-verify only after the checker returns PASS.
- **NO_TESTS**: no test suite detected. If step-level captures (green_capture + compliance PASS) exist for all steps, treat as PASS. If any step lacks captures, ask the user for manual sign-off (see banner below). On sign-off, proceed to code audit. Log the absence of a project-level test suite.

---
## ⏸ AWAITING YOUR INPUT

No test suite was detected and one or more steps lack green captures. Manual sign-off is required before code audit.

**Do you confirm implementation is complete?**

---

## Code audit

After verify passes, run a mandatory code audit prior to hand-off. This is
a closed gate: every CRITICAL or HIGH finding must be triaged
per-finding as `fix`, `accept`, or `defer` before the flow can move on.
The only automatic bypass is the zero-diff case where the diff filter
finds no auditable files in diff.

#### Pass 1: Diff filter (orchestrator self-check)

Before calling any agent, resolve the base branch with:
```bash
base=$(git branch -r | grep -E 'origin/(master|main)$' | head -1 | sed 's|.*origin/||')
```

Then compute the candidate audit scope with:
```bash
git diff --name-only --diff-filter=AMRCT "origin/${base}...HEAD"
```

Use the post-filtered destination paths as the audit scope. Exclude
binary files and submodule gitlinks after the `git diff` call. If the
filtered result contains no auditable paths, append this Log marker and
write the matching spec frontmatter, then proceed directly to hand-off.

Log marker base form (anchor):

`- YYYY-MM-DD: code audit: no auditable files in diff; skipping`

Log marker extended template (per §3.5b — append `evidence=<value>; blockers=[...]` literals to the base form). For zero-diff this is always `evidence=skipped; blockers=['no auditable files in diff']`:

> `- YYYY-MM-DD: code audit: no auditable files in diff; skipping; evidence=skipped; blockers=['no auditable files in diff']`

Spec frontmatter write (immediately adjacent to the marker append): set `code_audit_evidence: skipped` and `code_audit_blockers: ['no auditable files in diff']`. Per §3.5b: zero-diff is folded into `skipped` because no audit ran against findings.

#### Pass 2: Cross-audit (dual-model)
Track `code_audit_iteration` (start at 1). Track
`code_audit_fixed_ids` and `code_audit_accepted_ids` (both empty on the
first round). For `next_finding_id`, do not keep a separate variable in
feature-skill state: on re-spawn, the cross-auditor auto-derives it
from the highest existing `X<N>` ID in the KB findings file.

Spawn `cross-auditor` with mode: full on the diff (dual-model). Parameters:
- `scope`: newline-joined auditable paths from Pass 1
- `mode`: `full`
- `audit_slug`: `<slug>-code`
- `iteration`: `<code_audit_iteration>`
- `previously_fixed`: `<code_audit_fixed_ids>`
- `accepted_ids`: `<code_audit_accepted_ids>`
- `kb_path`: `<kb_path>`
- `project`: `<project>`
- `working_directory`: `<cwd>`
- `base_branch`: `<base>`
- `project_type`: resolve via `spec_frontmatter.project_type → .ai-dev-team.local.yml → .ai-dev-team.yml → None` (the cross-auditor emits a degraded warning at the H1-bullet emit location in findings.md when this resolves to `None` or a non-allowlist value — see `agents/cross-auditor.md` §R-rule cluster gate)

If `project_type` resolves to `None`, the cross-auditor normalizes the R-rule filter to `"all"` per `references/code-quality-rules.md` Trigger A, emits a degraded warning header in the findings document at the H1 bullet block (per `agents/cross-auditor.md` §R-rule cluster gate "Warning emit location"), and runs the filter as usual — rules with `applies_to: ["all"]` continue to load; rules with project-specific `applies_to` lists do not match. This is by design — silent skip ships R-rules dead. To activate full project-specific R-rule loading, set `project_type:` in spec frontmatter (recommended), in the project's `.ai-dev-team.local.yml`, or in `.ai-dev-team.yml`.

**branch-guard (callsite 2).** Run the §3.5d branch-guard around this spawn — capture `pre_spawn_branch`/`pre_spawn_head` BEFORE the spawn, and after the cross-auditor returns assert current branch == `pre_spawn_branch` AND strict `HEAD == pre_spawn_head` (callsites 1-4 are strict-equality, NOT ancestor-mode) BEFORE the Log marker / any git action. On violation apply the §3.5d step-4 recovery split (4a/4b/4c) and continue-gate.

**Cross-auditor return-contract gate (callsite 2).** When the cross-auditor returns for round `N`, **apply the §3.5b-2 recovery algorithm** before the Log marker is written. This is callsite 2 of the 6 §3.5b-2 callsites — the feature code-audit Pass 2 initial spawn. Capture the raw return to `<kb>/repos/<project>/security/<audit_slug>-contract-violation-iter<N>-attempt<M>.raw.txt` per §3.5b-1, invoke `hooks/lib/check_dispatch_response.py --mode full --findings-path <kb>/repos/<project>/security/<audit_slug>-findings.md --expected-claude-model claude-opus --expected-head "$(git rev-parse HEAD)" --require-rules-loaded` (add `--project ai-dev-team` when the spec frontmatter resolves `project: ai-dev-team`), and branch on the classifier exit code per §3.5b-2 step 4. The classifier output **gates** whether the iteration Log marker below is written: only an Exit-0 `policy_gate: null` with `model_gate: null` AND `head_gate: null` AND `rules_gate: null` PROCEED writes the marker with the round's `evidence=<value>; blockers=[...]` (a non-null `model_gate` routes to the §3.5b-2e model-attestation gate; a non-null `head_gate` routes to the §3.5b-2f audited-HEAD gate; a non-null `rules_gate` routes to the §3.5b-2g degraded-rules gate); an Exit-0 `policy_gate: STOP_AND_DISCUSS` raises the §3.5b-2a banner, an Exit-1 violation enters the §3.5b-2b retry-outcome matrix, and an Exit-2 classifier crash raises the §3.5b-2c classifier-crash banner.

The cross-auditor persists code findings in KB. After the cross-auditor
returns findings for round `N`, write this Log marker immediately. Do
not write it before the spawn call:

`- YYYY-MM-DD: code audit iteration=N; fixed_ids=[...]; accepted_ids=[...]`

The first round uses the same marker schema as every later round:
`fixed_ids=[]` and `accepted_ids=[]`. Post-return timing narrows the
crash window: the cross-auditor writes `<slug>-code-findings.md` and
`<slug>-code-workdoc-iterN.md` before it returns, so a crash between
the cross-auditor returning and the Log marker being written leaves
those KB artifacts on disk but no `iteration=N` Log line. Resume takes
the no-entry fresh-run branch and re-runs iteration N (so N=1 the
first time around); because the cross-auditor's persistence is
idempotent on `audit_slug` + `iteration` (findings merge by id,
per-iteration workdoc is rewritten in place), replaying the same
iteration converges to the same or a newer finding set. The guarantee
is **no findings lost**, not **no redone work** — a crashed iteration
may be replayed.

**If CRITICAL or HIGH findings with status `OPEN` or `REOPENED`
exist:**
1. Present the findings to the user grouped by severity.
2. Stop for per-finding triage. The user must choose an action for each
   finding; there is no phase-level bypass here.

---
## ⏸ AWAITING YOUR INPUT

Code audit found CRITICAL or HIGH findings. Reply with one action per
finding using `X<id> -> fix`, `X<id> -> accept: <reason>`, or
`X<id> -> defer: <reason>; spec=<follow-up-slug>`.

Use `accept` for deliberate risk acceptance and for false positives with
the rationale `false positive — both auditors erred: <explanation>`.

**Which action should be recorded for each finding?**

3. **Collect decisions.** For each finding, record the user's chosen
   action in memory and update the finding's status in the findings
   file at `<kb>/repos/<project>/security/<slug>-code-findings.md`. A single
   round may mix `fix`, `accept`, and `defer` across different IDs.
   **Do not spawn any developer yet — collection is pure bookkeeping
   before the checkpoint in step 4.**
   - `fix` -> `OPEN|REOPENED -> FIXED`. Record the finding as `FIXED`
     and add its id to `pending_fixed`. Developer spawn happens in
     step 5 (dispatch), after the checkpoint is on disk.
   - `accept` -> `OPEN|REOPENED -> ACCEPTED`. Require a reason note.
     Add the id to `pending_accepted`.
   - `defer` -> `OPEN|REOPENED -> DEFERRED`. Require a reason note
     plus a follow-up spec slug. Add the id to `pending_deferred`.
4. **Checkpoint.** After every finding in the round has a recorded
   action, append the crash-safe checkpoint marker **before any
   developer work starts**:

`- YYYY-MM-DD: code audit decisions recorded; iteration=N; pending_fixed=[...]; pending_accepted=[...]; pending_deferred=[...]`

   Treat `pending_accepted` and `pending_deferred` as the carry-forward
   suppression set for the next round. Both sets feed
   `code_audit_accepted_ids` on re-spawn. With this marker on disk,
   a crash between triage and developer work resumes cleanly — the
   decisions-recorded routing branch picks up from dispatch.

5. **Dispatch fix workers.** For each finding in `pending_fixed`,
   sequentially spawn the developer using the most recent
   `last_agent=` from the spec Log as the default (the user may
   override), with:
   `task: "rework: fix code-audit finding X<id> in <file>:<line> — <excerpt>. Root cause: <root cause>. Invariant: <invariant that must hold after the fix>. Input domain: <input domain / adversarial members to cover>. Suggested fix (advisory): <fix_suggestion>."`
   plus `spec_path`, `workdoc_path`, and `project_path`. The Root cause /
   Invariant / Input domain fields are mandatory per §Fix-dispatch contract
   (dispatch blocked while any is absent); the suggested fix is advisory — one
   hypothesis derived from the finding, never the contract. Wait for each
   developer to confirm its commit before dispatching the next id. The
   finding's status stays `FIXED` (pre-verification) after the
   developer returns; re-audit in step 7 promotes `FIXED → VERIFIED`
   or reopens the finding.

   **Append the numeric fix step + gate it before the verifier (R3-FC
   on the anchor-incident flow).** A code-audit finding has no owning
   step, so BEFORE dispatching the fix the orchestrator APPENDS a
   numeric fix step per the `/feature extend` precedent. Add the
   checklist line `- [ ] Step N: fix X<id> — <finding title>` to spec
   §5 (where `N = max existing step number + 1`) and a matching
   workdoc block `## Step N: fix X<id> — <finding title>` with a full
   planned block: goal, allowed_scope, failing/passing test cmds,
   `fix_source: code-audit X<id>`, and `boundary_inputs:` /
   `boundary_inputs_na:` per §Fix-dispatch contract, plus a spec Log
   line. The dispatch `task` becomes `step N only`, carrying the same
   rework fields (root cause / invariant / input domain / advisory
   fix). After the developer returns `report.json`, the orchestrator
   runs the standard §Orchestrator-sole-KB-writer per-step loop step-4
   verdict handling on step N: copy `observed` → spawn
   `spec-compliance-checker` on step N → on FAIL/DRIFT re-dispatch per
   §Fix-dispatch contract, re-copy `observed`, re-spawn the checker; on
   PASS check off step N. This per-step compliance gate (the checker
   verdict BLOCKS, it does not advise) runs BEFORE the step-6 verifier
   re-run below.
6. **Re-run the `verifier` subagent** once every fix developer has
   returned.
   - `PASS`: continue to the next audit round.
   - `FAIL`: use the Verify FAIL rework loop, then re-run `verifier`.
     Once it returns `PASS`, continue to the next audit round.
   - `NO_TESTS`: use the Verify NO_TESTS manual sign-off rules, then
     continue.
7. Re-spawn `cross-auditor` with the same parameter block as the initial full-mode spawn at §Code audit Pass 2 (including `project_type` resolved per the spec-frontmatter → `.ai-dev-team.local.yml` → `.ai-dev-team.yml` → `None` chain), updating only `iteration=N+1`, `previously_fixed=pending_fixed`, and `accepted_ids=(pending_accepted ∪ pending_deferred)`.
7a. **branch-guard (callsite 3).** Run the §3.5d branch-guard around this re-spawn — capture `pre_spawn_branch`/`pre_spawn_head` BEFORE the re-spawn, and after the cross-auditor returns assert current branch == `pre_spawn_branch` AND strict `HEAD == pre_spawn_head` (callsites 1-4 are strict-equality, NOT ancestor-mode) BEFORE the Log marker append. On violation apply the §3.5d step-4 recovery split (4a/4b/4c) and continue-gate. **Apply the §3.5b-2 recovery algorithm** to this re-spawn's classifier output before the Log marker append below — this is callsite 3 of the 6 §3.5b-2 callsites (the code-audit triage-loop re-spawn). The re-spawn's classifier invocation passes `--expected-head "$(git rev-parse HEAD)"` and `--require-rules-loaded` (callsite 3). The project-policy gate (§3.5b-2a), retry-outcome matrix (§3.5b-2b), model-attestation gate (§3.5b-2e), audited-HEAD gate (§3.5b-2f), and degraded-rules gate (§3.5b-2g) apply identically. Classifier output gates whether step 8 fires (Exit-0 `policy_gate: null` with `model_gate: null` AND `head_gate: null` AND `rules_gate: null` PROCEED — a non-null `model_gate` routes to the §3.5b-2e model-attestation gate, a non-null `head_gate` routes to the §3.5b-2f audited-HEAD gate, a non-null `rules_gate` routes to the §3.5b-2g degraded-rules gate) or §3.5b-2b/2c routes to a banner.
8. After the cross-auditor returns, append:
`- YYYY-MM-DD: code audit iteration=N+1; fixed_ids=[...]; accepted_ids=[...]`

9. Repeat the loop until no CRITICAL or HIGH findings remain in `OPEN`
   or `REOPENED`. `FIXED` findings count as clean only after a later
   audit round verifies them. Before re-spawn, see §3.5c Stop criteria
   — REOPEN findings or same-defect-class on 2+ iters trigger a
   comprehensive sweep (paired control with rule #10: AFTER `/compact`
   or via a fresh-context subagent); hard cap iter ≤ 5 (counts
   cross-auditor re-spawns) unless an explicit §3.1c-regex Log line
   justifies the exception; residue is funneled through per-finding
   `accept` / `defer` triage, NOT skip-to-hand-off.

**If there are no CRITICAL or HIGH findings, or all such findings have
been resolved:**
- Append the Log marker (extended template — `evidence=<value>; blockers=[...]; audited_head=<oid>`):
`- YYYY-MM-DD: code audit passed; iteration=N; verified=[...], accepted=[...], deferred=[...]; evidence=<value>; blockers=[...]; audited_head=<oid>`
  The trailing `<oid>` is **COPIED from the findings-frontmatter `audited_head:` pin** (same READ path as `code_audit_evidence:` below — what the auditor actually attested), NOT re-derived via `git rev-parse` at marker-write time. The zero-diff skip marker is unchanged (no audit ran → nothing to pin).
- Spec frontmatter write (immediately adjacent to the marker append): set `code_audit_evidence:` from the cross-auditor's final-iteration return signal per §3.5b READ path (code/full mode parses both `evidence_class:` and `evidence_blockers:` from the leading top-of-file YAML frontmatter of the produced `<slug>-code-findings.md`). Copy `evidence_blockers:` verbatim into `code_audit_blockers:` (parse-failure → `contract_violated` per §3.5b).
- Completion here means no finding remains `OPEN` or `REOPENED`.
- `💡 Consider running `/compact` before the hand-off step.`
- Move to hand-off.

---

## Hand-off

After the code audit phase completes (either a `code audit passed` marker
or the zero-diff `code audit: no auditable files in diff; skipping`
marker has been appended to the Log), run a two-phase hand-off seed
before showing the 4-option menu. This is per-item reconciliation:
re-read §6.2 on every hand-off; only `deploy_prerequisites` participate
in seeding. `smoke_check` is never seeded into §8.

**Phase 1 — compute delta (before the 4-option menu, in memory only)**

1. Read §6.2 `deploy_prerequisites` via `§6.2 handling`. If the list is
   empty or §6.2 is absent, stage no §8 items and no seed Log entry.
2. Build the set of normalized descriptions already present in §8,
   regardless of item status or `source:` tag. `done`, `failed`, and
   `pending` all count for dedup.
3. For each prereq in order, compute its normalized form. If it already
   exists in the §8 set, skip it. Otherwise allocate the next id as
   `max(existing §8 id, 0) + 1 + staged_count`, and stage:
   ```yaml
   - id: <n>
     type: action
     description: <verbatim prereq string>
     owner: user
     source: §6.2:deploy_prerequisites
     status: pending
     notes: null
     resolved_at: null
   ```
4. Add each newly staged normalized description to the working set so
   in-batch duplicates are deduped too.
5. If `N = len(staged_items)` is greater than zero, stage the Log entry
   `- YYYY-MM-DD: auto-seeded N deploy prerequisites from §6.2 to §8`.
6. If §6.2 is malformed, emit the warning from `§6.2 handling`, stage no §8
   items, and instead stage the malformed Log entry
   `- YYYY-MM-DD: hand-off: §6.2 block malformed — seeding skipped, manual review required`.

**Audited-HEAD gate (before the 4-option menu).** When the terminal code-audit
record is a `code audit passed` marker (a code audit actually ran), read
`audited_head:` from the leading frontmatter of
`<kb>/repos/<project>/security/<slug>-code-findings.md` and compare it to
`git rev-parse HEAD` on the feature branch:

- Equal → proceed to the 4-option menu.
- `audited_head:` missing, or unequal → render the audited-HEAD mismatch banner
  below. **Never a silent pass.** Fix commits that land after the last audit
  round move HEAD; this compare catches them even though each round's classifier
  check passed at its own time.

**Zero-diff carve-out:** when the terminal code-audit record is the zero-diff
skip (`code audit: no auditable files in diff; skipping` marker /
`code_audit_evidence: skipped` with blocker `'no auditable files in diff'`), the
gate is N/A — no audit ran, nothing was pinned, a findings doc may not exist;
**skip the gate SILENTLY**. The gate applies ONLY when a `code audit passed`
marker exists.

---
## ⏸ AWAITING YOUR INPUT

Audited-HEAD mismatch — the terminal code audit signed off a different commit than the current feature-branch HEAD. `audited_head=<oid|absent>` vs `HEAD=<oid>`.

Options:

1. **Re-audit the delta** — re-spawn the cross-auditor per the existing §Code audit Pass 2 parameter block (counts a SEMANTIC iteration; the refreshed findings re-pin the new HEAD). This is the retry path for this gate.
2. **Accept with justification** — append the Log directive `- YYYY-MM-DD: audited-head mismatch accepted — audited=<oid|absent> head=<oid>: <reason>` and proceed.
3. **Stop** — pause the hand-off.

**Which option?**

---

After phase 1 and the audited-HEAD gate, show the commit list and present exactly these 4 options:

```
git log --oneline <base>..<branch>
```

After the user picks a preserving option and phase 2 status is set (§3.4a), run `python3 tests/backlog_archive.py --dry-run` and present the archive-approval banner if any done items are found — full protocol in `§3.4a`. Option 4 (Discard) does NOT trigger the backlog_archive check.

---
## ⏸ AWAITING YOUR INPUT

Implementation complete. What would you like to do?

1. Merge into `<base-branch>` locally
2. Push feature branch (I'll merge to staging and open a PR myself)
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

**Which option?**

> Note: merging into `staging` / `testnet` / `pre-prod` for testing is a separate manual step the user handles. The plugin only merges into the base branch (`master` or `main`).

### §3.4a Post-handoff status transition

Phase 2 applies only after a preserving option succeeds. Set frontmatter
`shipped_at: YYYY-MM-DD` (today), then decide status via `§3.4a`:

**Terminal-evidence precondition (before any `status: SHIPPED` / `status: VERIFIED` write).**
Assert BOTH `spec_audit_evidence:` and `code_audit_evidence:` are present in the
spec frontmatter with a value from the 5-value enum
`{dual_model, single_model, self_fallback, contract_violated, skipped}`. If
either key is **absent / literal-null / off-enum** → do NOT flip the status;
render the terminal-evidence refusal banner below. Degraded-but-honest enum
values (`skipped`, `single_model`, …) still flip — they are honest records; the
gate targets absence / literal-null / off-enum only (the silent-bypass
signatures). The flow always writes these keys (spec-audit terminal sites at
AUDIT_PASSED, code-audit terminal sites at the passed / zero-diff markers), so
an absent key means the flow was bypassed. **Never flip with absent keys.**

---
## ⏸ AWAITING YOUR INPUT

Terminal-status write blocked — cannot flip to `SHIPPED` / `VERIFIED` without
audit evidence. Defective key(s):

- `<key>`: <absent | literal-null | off-enum value `<value>`>

Repair path: run the missed audit phase (spec audit → `spec_audit_evidence`;
code audit → `code_audit_evidence`), OR record an explicit enum value with a Log
directive if the phase legitimately ran degraded.

**Repair how?**

---

- Malformed §6.2 → force `status: SHIPPED`, append the staged malformed Log
  line, and leave manual review required.
- Else if post-phase-2 §8 has any `pending` or `failed` item →
  `status: SHIPPED`.
- Else → `status: VERIFIED`.

`DONE` remains accepted as a legacy synonym of `VERIFIED` when reading older specs, but new transitions must write `VERIFIED`.

After phase 2 status is set, run the backlog archive check:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/tests/backlog_archive.py" "<kb_path>" --project <project> --dry-run
```

If AUTO count N + CANDIDATE count M > 0, present the approval banner. Two variants:

- **M ≥ 1** (candidates exist):

  > ## ⏸ AWAITING YOUR INPUT
  > Backlog has **N** unambiguously-done item(s) ready to archive. **M** more look done (number matches a done table row) — approve which to archive:
  > - `#<id>` "<block_title>" ↔ "<matched_row_title>" — *<hint>*
  > - (one line per candidate from `--dry-run` CANDIDATES section)
  > Reply `all` / a list of ids / `none` (auto set only) / `skip`.
  > **Approve which candidates?**

  On reply `all` → `--apply --archive-candidates <all-ids>`; a list of ids → `--apply --archive-candidates <ids>`; `none` → `--apply` (no `--archive-candidates`, AUTO set only); `skip` → nothing.

- **M = 0** (AUTO-only, no candidates):

  > ## ⏸ AWAITING YOUR INPUT
  > Backlog has **N** done item(s) ready to archive (all unambiguous). Reply `ok` to archive / `skip`.
  > **Archive now?**

  On `ok` → `--apply` (no `--archive-candidates`); `skip` → nothing.

After any `--apply`, show the diff; the user reviews and commits. The archiver never commits. `--dry-run` always runs before `--apply`; `--apply` only on explicit reply. Not fired at session-start (#76a).

---

**Option 1 — Merge into base branch locally:**
```bash
git checkout <base-branch> && git pull && git merge <branch>
```
Run verifier once more on the merged result. If green, apply phase 2:
append staged §8 items, append the staged Log line if any, set `shipped_at`,
and decide status per `§3.4a`. Then run the backlog_archive.py check per `§3.4a`. **Do not delete the feature branch** — leave
the branch reference in place (useful for reflection and quick rollback).

**Option 2 — Push feature branch:**
```bash
git push -u origin <branch>
```
Report the branch name. After a clean push, apply phase 2: append staged §8
items, append the staged Log line if any, set `shipped_at`, and decide
status per `§3.4a`. Then run the backlog_archive.py check per `§3.4a`.

**Option 3 — Keep as-is:** Do nothing externally. Report the branch name.
Apply phase 2 unconditionally: append staged §8 items, append the staged Log
line if any, set `shipped_at`, and decide status per `§3.4a`. Then run the backlog_archive.py check per `§3.4a`.

**Option 4 — Discard:** discard the in-memory delta and delegate to the
Discard mode below (same flow as `/feature discard <spec-path>`). Any
failure path before a preserving option succeeds also discards the staged
delta with no spec mutation.

---

## Continue mode

/feature continue resumes from the last incomplete step — no context recovery needed

When resuming (`/feature continue` or `/feature <spec-path>`):

1. Run KB discovery (Phase 0)
1a. **No-in-flight branch** — if `/feature continue` was invoked with no `<spec-path>` AND the §Session resume — KB scan found no IN_PROGRESS / AUDIT_PASSED specs, run the **research-queue scan** (per §Session resume — KB scan, primary surface) before declaring "nothing in progress". Read `queued_specs:` from CONCLUDED research-note frontmatter via a recursive walk of `<kb>/repos/<project>/research/` covering all `.md` files at any depth, including direct children (depth-0 and deeper — implementations MUST cover both; e.g. `find -type f -name '*.md'` or Python `rglob('*.md')` or bash with `shopt -s globstar` plus explicit dual-pattern `<root>/*.md` + `<root>/**/*.md`); look up materialization status of each queued slug against the canonical date-prefixed form `<kb>/repos/<project>/design/<YYYY>-<MM>-<DD>-<slug>.md` (literal 4-2-2 numeric date prefix + `-` + queued slug + `.md` — NOT a bare `*-<slug>.md` glob), and apply the **Materialization status branching** below to decide whether to render or suppress each item.

**Materialization status branching** (covers all design-spec lifecycle states + no-match + multi-match — used by both the no-in-flight branch above and Status mode's `### Queued from retrospectives` section):

| Matched design status | Continue mode (no-in-flight branch) | Status mode (`### Queued from retrospectives` row) |
|---|---|---|
| (no match — no `*-<slug>.md` file exists) | render: `queued — not yet materialized` | render row |
| `DRAFT` / `APPROVED` | render: `queued — spec drafted but not in flight: see <matched-design-relative-path>` | render row (annotated) |
| `BLOCKED` | render: `queued — spec drafted but BLOCKED: see <matched-design-relative-path>` | render row (annotated) |
| `IN_PROGRESS` / `AUDIT_PASSED` | suppress (already surfaced by in-flight scan) | suppress |
| `VERIFIED` (or legacy `DONE`) / `SHIPPED` | suppress (terminal — work done) | suppress |
| `DISCARDED` | render: `queued — prior attempt discarded; consider re-queue or remove` | render row (annotated) |

`<matched-design-relative-path>` is the project-relative path returned by the lookup glob in §Session resume — KB scan (e.g. `design/2026-04-30-shared-absence-helper-extraction.md` — the full date-prefixed basename, NOT a bare `<slug>.md`). Following the bare-slug form would emit a broken Obsidian link because the actual file on disk carries the date prefix.

Edge cases:
- **Multi-match** (date-prefixed lookup `<YYYY>-<MM>-<DD>-<slug>.md` returns >1 result — i.e. the same slug shipped on different dates): pick the lexicographically newest match (date prefix sorts naturally) AND emit a one-line warning `⚠ multiple design files match slug <slug>; using newest <date-prefix>`. The date-prefix anchor narrows multi-match risk to genuine duplicates (same slug across different date prefixes) — it eliminates the slug-suffix-collision class (e.g. queued slug `audit-foo` vs longer existing slug `mandatory-audit-foo`), which the prior `*-<slug>.md` glob would have silently matched.
- **Same slug in N different research notes**: Continue mode renders once with a comma-joined source list; Status mode renders N rows preserving source-note attribution.
- **No eager cache**: scan reads disk on every invocation (research notes are bounded; ≤100 expected at peak per project).
- **No-mutation guarantee**: the scan never modifies source frontmatter. Render layer reflects current design state; source notes stay append-only.

2. Read the spec file. Check the `status` field in frontmatter:
   - `DRAFT` → Spec not yet approved. Present it to the user and ask for approval. Resume from Step 3 (Get approval).
   - `APPROVED` → Resume from Step 3.5 (spec self-review → cross-audit).
   - `AUDIT_PASSED` → Resume from Implement (baseline test → agent selection → implementation).
   - `IN_PROGRESS` → Find the first unchecked `- [ ]` step. Resume from there. Ask which agent to use. If no unchecked step exists (all `[x]`): implementation is complete — resume flow is Verify → Code audit → Hand-off. Code-audit entry depends on the most recent code-audit Log marker. Four marker kinds plus one no-entry routing branch — five resume paths total (`code audit passed`, `code audit: no auditable files in diff; skipping`, `code audit decisions recorded`, `code audit iteration=N`, plus the no-entry fresh-run branch). Route using the table below (read Log markers chronologically; use the most recent `code audit …` line):

     | Log state (most recent code-audit marker) | Routing decision |
     |---|---|
     | `code audit passed` | Skip straight to hand-off. Code audit already complete. |
     | `code audit: no auditable files in diff; skipping` | Skip to hand-off — deterministic empty-diff skip already applied. |
     | `code audit decisions recorded; iteration=N; pending_*` | Re-run the verifier, then re-spawn `cross-auditor` with the same parameter block as the initial full-mode spawn at §Code audit Pass 2 (including `project_type` resolved per the spec-frontmatter → `.ai-dev-team.local.yml` → `.ai-dev-team.yml` → `None` chain), updating only `iteration=N+1`, `previously_fixed=pending_fixed`, and `accepted_ids=(pending_accepted ∪ pending_deferred)`. **branch-guard (callsite 4):** run the §3.5d branch-guard around this re-spawn — capture `pre_spawn_branch`/`pre_spawn_head` BEFORE the re-spawn, and after the cross-auditor returns assert current branch == `pre_spawn_branch` AND strict `HEAD == pre_spawn_head` (callsites 1-4 are strict-equality, NOT ancestor-mode) BEFORE resuming the triage loop; on violation apply the §3.5d step-4 recovery split (4a/4b/4c) and continue-gate. **Apply the §3.5b-2 recovery algorithm** (callsite 4 of 6) to the re-spawn's classifier output before resuming the triage loop; the re-spawn's classifier invocation passes `--expected-head "$(git rev-parse HEAD)"` and `--require-rules-loaded` (callsite 4); project-policy gate (§3.5b-2a), retry-outcome matrix (§3.5b-2b), model-attestation gate (§3.5b-2e), audited-HEAD gate (§3.5b-2f), and degraded-rules gate (§3.5b-2g) apply identically. |
     | `code audit iteration=N` (without a later `decisions recorded` or `passed` marker) | Round N findings were returned but triage is pending — **do not** re-spawn the cross-auditor. Re-read the findings file at `<kb>/repos/<project>/security/<slug>-code-findings.md`, collect the findings whose status is `OPEN` or `REOPENED`, re-present them to the user, and resume the §Code audit triage loop from step 1 with those findings. |
     | No code-audit Log entry at all | Fresh code-audit run: re-run the verifier first to confirm the baseline is still green (defensive), then spawn `iteration=1` with `previously_fixed=[]` and `accepted_ids=[]`. |

     Malformed or truncated trailing code-audit Log lines are ignored; fall back to the last complete recognized marker above. If the only code-audit entry is unrecognized, treat it as no code-audit Log entry and take the fresh-run branch.
   - `BLOCKED` → Report the unblock condition from the most recent `BLOCKED — waiting on ...` Log entry and ask the banner below. If yes, revert status to the prior state (IN_PROGRESS or AUDIT_PASSED, whichever the Log indicates) and resume. If no, stop.

---
## ⏸ AWAITING YOUR INPUT

Spec is BLOCKED on `<condition from the most recent Log entry>`.

- Yes → resume work from the prior state.
- No → stop.

**Is the unblock condition now satisfied?**
   - `SHIPPED` → Feature is merged but post-merge checklist has open items. Run auto-resolve for `depends_on` blockers (see Verify mode), then, before rendering pending items, apply this Quick-check decision tree:
     1. Parse §6.2 via the parsing contract in `§6.2 handling` and read `smoke_check`. If `smoke_check` is null or missing, skip the banner and render pending items as usual. If §6.2 is malformed, also skip the banner and continue to pending-items render.
     2. Read §6.2 `deploy_prerequisites` and build the set of unresolved §8 items. Status is `pending` OR `failed`; both mean the operational work is not complete, and only `done` items drop out of the gate. For each prereq, compute its normalized form and compare it against each unresolved §8 item's normalized description, regardless of `source:` tag. If any normalized §6.2 prereq matches any unresolved §8 item's normalized description, render the deferred banner and skip the command:

        ```
        ⚡ Quick check: complete deploy prerequisites below first.
        ```

        The status-rule asymmetry with §3.4 is intentional and load-bearing: `failed` is still unresolved because the next action is to fix and retry, and filtering by `source:` alone is wrong because user-added §8 items without that tag still represent unresolved ops work.
     3. Otherwise render the live banner:

        ```
        ⚡ Quick check (from spec §6.2):
            <command>
            Expected: <expected>
        ```

        If `smoke_check.expected` is an empty string, omit the `Expected:` line entirely.
     4. Then show the checklist: open items grouped by type with owner and what's pending. Offer the user the obvious next move based on what is open — mark an action done, start a soak, run `/feature verify`, etc. Do not re-enter the implement loop.
   - `VERIFIED` (or legacy `DONE`) → Feature complete and observed. Report completion status and stop.
   - `DISCARDED` → Feature was discarded. Report this and stop.
3. Report current state: spec name, status, completed steps count, next step, any blockers from the Log section
4. Ask which agent to use for remaining work (only if resuming implementation). If the Log contains a `last_agent=...` entry, present it as the default in the banner below.

**Legacy `last_agent=middle` normalisation (Log default).** If the most recent Log `last_agent=` value is `middle` (a stale value from before the Middle developer agent was retired on 2026-04-25 — including the case where it is the only `last_agent=` entry), normalise the banner default to `codex` (the matrix default) and prefix the banner with this preamble line:

> Note: spec Log says `last_agent=middle`, but the Middle developer agent was retired on 2026-04-25; defaulting to `codex`. Pick a different agent if appropriate.

Pressing Enter then accepts `codex`, not `middle`. Older Log entries are ignored if a more recent `codex`/`senior` entry exists — Continue mode evaluates only the most recent `last_agent=` line. The normalisation does not mutate the Log; the legacy entry stays for audit history.

**Step-tag handling on resume (separate path — DO NOT conflate with the rule above).** If the next unchecked step in §5 carries an `@middle` tag (a stale tag from before the agent was retired), this is a tag-acceptance case, not a default-normalisation case. It hits the malformed-tag rule in `skills/feature/SKILL.md` Per-step pre-tag handling (the §"Per-step agent pre-tag" tag-acceptance narrative in this same SKILL.md) and **hard-stops** with the standard malformed-tag banner asking the user to correct the checklist line. It does NOT silently normalise. Distinct paths: Log default normalises silently with a preamble; step-tag hard-stops and demands a correction.

---
## ⏸ AWAITING YOUR INPUT

Resuming implementation. Pick the developer for the remaining steps. The most recent `last_agent=<codex|senior>; rationale=<T-X#>` entry in the spec Log is offered as the default — press Enter to accept it, or name a different agent. (If the first unchecked step carries an `@<agent>` tag in §5 and the tag would be honored by the §3.4 acceptance rule — positive trigger matches AND no anti-trigger contradicts — that tag overrides the spec-level `last_agent=` default for this specific step: Continue mode presents the tagged agent as the banner default, not the Log value. A tag that §3.4 would reject is treated as untagged on resume too: Continue mode falls back to the `last_agent=` Log value and emits the same mismatch warning above the banner. A malformed tag hard-stops on resume just as on fresh implement, per §3.3 malformed-tag handling.)

**Which developer (default is the `last_agent` from Log)?**

---

## Grill mode

Standalone invocation of the optional grill gate (`/feature grill [spec-path]`) — runs the DRAFT-hardening interview on its own, outside a fresh New-flow run. Use when a spec was drafted earlier and you want to grill it before approval. Grill is off by default and NEVER gates; this handler just wires the standalone dispatch (spec resolution, precondition, return) around the same interview the inline `### Grill gate` runs. The interview discipline itself lives in `skills/feature/references/grill-protocol.md` — do NOT restate it here.

1. Run KB discovery (Phase 0).
2. Resolve the target spec:
   - `[spec-path]` argument supplied → that spec.
   - omitted, and a spec is under discussion this session → that spec.
   - otherwise → prompt with the banner below listing DRAFT specs.

---
## ⏸ AWAITING YOUR INPUT

No spec-path was supplied to `/feature grill` and no spec is under discussion. Pick a DRAFT spec to grill, or reply `cancel` to abort.

`<numbered list of DRAFT specs>`

**Which spec should be grilled?**

3. Precondition — grill hardens a **DRAFT** before approval:
   - `status: DRAFT` → run grill.
   - any other status → refuse, leave state untouched (this is a catch-all: it covers `APPROVED` / `AUDIT_PASSED` / `IN_PROGRESS` / `BLOCKED` / `SHIPPED` / `VERIFIED` (or legacy `DONE`) / `DISCARDED` and any future enum value — do NOT re-enumerate). Tell the user: "Grill is a pre-approval DRAFT-hardening gate; this spec is already `<status>`. A change to an already-approved spec belongs in a re-draft (reject the spec back to DRAFT first) or a follow-up spec — not a post-hoc grill."
4. Run the interview per `skills/feature/references/grill-protocol.md` (branch-map traversal, the 3 load-bearing mechanics, coarse route, coverage / termination, `--focus`, cadence). Interactive + INLINE — never a backgrounded subagent (a live interview cannot be backgrounded; the human is the gate).
5. Fold the output back per that write-back contract: a `## Decisions` table, risk deltas into `### 3.6 Risks`, a `## 9. Log` line, and `grill_status: ran` / `grill_date` / `grill_coverage` frontmatter. (On an explicit decline / stop-before-start, write `grill_status: skipped` per the `### Grill gate` skipped-vs-null rule.)
6. Return / stop after write-back. Grill does NOT auto-advance to the Step 3 approval gate — the user re-enters the flow (`/feature continue <spec-path>`) to reach the approval HARD GATE on the grilled spec. Grill NEVER gates.

---

## Discard mode

Explicit discard outside hand-off. Use when the user decides mid-implementation (or on resume) to throw the feature away.

1. Run KB discovery (Phase 0).
2. Resolve the spec from `spec-path`. If no argument, prompt the user with the banner below and a list of IN_PROGRESS / AUDIT_PASSED / BLOCKED specs.

---
## ⏸ AWAITING YOUR INPUT

No spec-path was supplied to `/feature discard`. Pick one of the active specs below to discard, or reply `cancel` to abort.

`<numbered list of IN_PROGRESS / AUDIT_PASSED / BLOCKED specs>`

**Which spec should be discarded?**

3. Refuse if `status: VERIFIED` (or legacy `DONE`) — spec is closed. Tell the user: "Spec already verified; to undo, revert the merge commit(s) via git."
4. Refuse if `status: SHIPPED` — feature merged with an open post-merge checklist. Tell the user: "Spec already shipped. Use `/feature checklist` to manage open items, or revert the merge commit(s) if you need to roll back."
5. Refuse if `status: DISCARDED` — already gone.
6. Show the commit list and branch name, then ask for typed confirmation via the banner below.

```
git log --oneline <base>..<branch>
```

---
## ⏸ AWAITING YOUR INPUT

This will permanently delete branch `<branch>` and all commits listed above. There is no undo.

**Type the word `discard` to confirm — any other reply aborts. Confirm?**

7. On confirmation: `git checkout <base-branch> && git branch -D <branch>` (use `-D` — force, since the branch likely isn't merged into base). Set `status: DISCARDED`, append Log: `- YYYY-MM-DD: feature discarded by user`.
8. On any other answer: abort, leave state untouched.

---

## Status mode

1. Run KB discovery (Phase 0)
2. Find all specs: `<kb_path>/repos/*/design/YYYY-MM-DD-*.md`
3. Read status, implementation checklist, and post-merge checklist (section 8) from each
4. For every `SHIPPED` spec: run the auto-resolve pass (see Verify mode) so blockers pointing at now-verified specs collapse before we render
5. Filter: by default, hide `VERIFIED` (or legacy `DONE`), `DISCARDED`, and `BLOCKED` (they are not actionable now). Always show `SHIPPED`. If the argument is `status --all`, show every spec regardless of status.
6. Group the visible specs into named sections:

```
### Active
| Spec | Project | Status | Progress | Branch | Audit |
|------|---------|--------|----------|--------|-------|
| ... | ... | IN_PROGRESS | 3/7 steps | <type>/... | dual / dual |
| ... | ... | AUDIT_PASSED | 0/5 steps | <type>/... | ⚠ skipped / — |
| ... | ... | AUDIT_PASSED | 0/5 steps | <type>/... | ⚠ contract_violated / — |

### Shipped — awaiting your action
(SHIPPED with at least one pending `action` item, or any `failed` item.)

| Spec | Project | Open item | Since |
|------|---------|-----------|-------|
| ... | ... | action: Deploy v1.2 to mainnet | 2026-04-17 |

### Shipped — blocked on others
(SHIPPED where the only pending items are `blocker`s — manual or depends_on still unresolved.)

| Spec | Project | Blocked on |
|------|---------|------------|
| ... | ... | frontend-team: UI ships · depends_on: design/2026-04-20-ui.md |

### Shipped — soaking
(SHIPPED where the only pending items are `soak`s.)

| Spec | Project | Soak | Started | Remaining |
|------|---------|------|---------|-----------|
| ... | ... | 7 days stable in prod | 2026-04-18 | 5 days |
```

### Queued from retrospectives
(CONCLUDED research notes with `queued_specs:` — items not yet at terminal `VERIFIED`/`SHIPPED` and not in active flight.)

Scan semantics: recursively walk `<kb>/repos/*/research/` (all projects, mirroring the existing all-project Status-mode contract on `<kb_path>/repos/*/design/YYYY-MM-DD-*.md`) and include every `.md` file at **any depth, including direct children** (depth-0 like `<research>/<slug>.md` — the canonical `/research new` write path). Implementations MUST cover depth-0 and deeper (e.g. `find -type f -name '*.md'` or Python `rglob('*.md')` or bash with `shopt -s globstar` plus explicit dual-pattern `<root>/*.md` + `<root>/**/*.md`); a bare `**/*.md` glob without `globstar` silently misses direct children. Project attribution: take the path segment immediately after `<kb>/repos/` (equivalently, the directory containing `research/`) — this is the project name regardless of nesting depth inside `research/`. For example: `<kb>/repos/ai-dev-team/research/release-retrospective/2026-04-28-investigator-round-2.md` resolves to project `ai-dev-team`, NOT `release-retrospective`. Frontmatter `status: CONCLUDED` filter and `queued_specs:` parsing follow the same rules as §Session resume — KB scan (defensive handling for malformed YAML / missing-required-field; warning emission unchanged). Materialization lookup uses the same date-prefix-anchored canonical form `<kb>/repos/<X>/design/<YYYY>-<MM>-<DD>-<slug>.md` as §Session resume — KB scan (NOT a bare `*-<slug>.md` glob — that would over-match longer slugs ending in `-<slug>`).

| Source note | Project | Queued spec | Queued since | State |
|------|------|---------|------|------|
| 2026-04-28-investigator-round-2 | ai-dev-team | #56 removed-cli-flag-hard-fail | 2026-04-28 | not yet materialized |
| 2026-04-28-investigator-round-2 | ai-dev-team | #57 shared-absence-helper-extraction | 2026-04-28 | DRAFT — see design/2026-04-30-shared-absence-helper-extraction.md |

**Status mode render rules**:

- **Source note**: filename without `.md` extension and without leading `release-retrospective/` directory. Hyperlinkable in Obsidian.
- **Project**: parent-of-`research/` directory of the matched source note (`<kb>/repos/<X>/research/...` → `<X>`). Mirrors the existing all-project contract.
- **Queued spec**: `<id> <slug>` if `id` is present in frontmatter; just `<slug>` otherwise (matching the schema's id-optional rule).
- **Queued since**: the `created:` field of the source note (original publication date — NOT the latest update).
- **State**: render decision from the Materialization status branching table in §Continue mode. Includes legacy `DONE` synonym treatment (terminal — work done; suppressed). When the branching table emits a `see <matched-design-relative-path>` reference, use the full date-prefixed basename returned by the lookup (matching the example row at `2026-04-30-shared-absence-helper-extraction.md`), never a bare `<slug>.md` form — that would produce a broken Obsidian link.
- **Sort**: by Queued since, **oldest first** — surfaces backlog age.
- **Omit the section entirely if no rows match** (consistent with other Status sections).

**Audit column rendering (per §3.5b):** the `Audit` column on the `### Active` table renders `<spec_audit_evidence> / <code_audit_evidence>` from the spec frontmatter. Render rules:

- `null` (legacy_unknown — pre-enum spec) → render `—` (em-dash). Do NOT flag.
- `dual_model` → render `dual`. Do NOT flag.
- Any of `single_model`, `self_fallback`, `contract_violated`, `skipped` → prepend a `⚠ ` warning glyph. The canonical degraded-flag predicate is `*_audit_evidence ∈ {single_model, self_fallback, contract_violated, skipped}` — apply this independently to `spec_audit_evidence` and to `code_audit_evidence`. Both fields use the same predicate.

Continue mode is unchanged — it routes a single resolved spec, not a row table, so there's nothing to flag there.

Omit any section that has no rows. If a SHIPPED spec has mixed pending types, place it in the most-actionable section (action → blocked → soaking, in that priority).

To move a spec to `BLOCKED` during development, append `- YYYY-MM-DD: BLOCKED — waiting on <condition>` to the spec Log and flip `status: BLOCKED`. Continue mode reads the most recent such Log entry and asks whether the condition is satisfied on resume. (Do not confuse this with a `blocker` *item* in the post-merge checklist — those belong to SHIPPED specs that are already merged.)

### KB drift — <project>

After the spec-section render, fold in a single non-blocking KB-drift headline. Phase-0 discovery (step 1) already resolved `kb_path` + `project`; **best-effort** run the offline KB-drift scanner against that ONE project and take line 1 of its `--summary` output:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/tests/kb_drift_scan.py" "<kb_path>" --project <project> --summary
```

**Scope/label**: the spec tables above span specs **all-project** (`repos/*`), but this drift fold is **single-project** — it covers only the Phase-0-resolved `<project>` (matching `/kb-audit`'s single-project default). The header MUST carry the project qualifier `### KB drift — <project>` so the reader never mistakes a one-project drift count for a global one.

Render rules:

- **Findings present (scanner exit 1)**: render the `### KB drift — <project>` header, then ONE line — the `--summary` headline (line 1) — then `(run /kb-audit for detail)`. Do not expand the grouped detail here; `/kb-audit` is the detailed surface. If the headline includes `C7:` (backlog done-item bloat), append one recommend-line: `  → Run python3 tests/backlog_archive.py <kb_path> --project <project> --dry-run to review archived candidates.`
- **0 findings (exit 0)**: **omit** the `### KB drift — <project>` section entirely (consistent with the omit-empty-section rule used by the other Status sections).
- **Scanner/vault unavailable (exit 2, `python3` absent, `kb_path`/`project` unresolved)**: omit the section silently — **never block or error** the status render.

Non-blocking, single-line, single-project-scoped + labeled. No `--all` interaction (the fold always covers only the resolved project, regardless of `status --all`).

---

## Checklist mode

Manage the post-merge checklist of a `SHIPPED` spec. All actions mutate the
YAML block under `## 8. Post-merge checklist` in the spec file. All actions
also append a single line to the spec Log describing the change.

### `checklist add <spec-path> <type> "<desc>" [options]`

Append a new item. `<type>` ∈ `{action, blocker, soak}`. Allocate the next
integer `id` (max existing id + 1, or 1). Defaults: `status: pending`,
`owner: user`, `notes: null`, `resolved_at: null`.

Type-specific options:
- `action`: none required.
- `blocker`: `--owner=<team>` (defaults to `user`), `--depends-on=<path>` where
  path is relative to `<kb_path>/repos/<project>/` (e.g.
  `design/2026-04-20-ui.md`). If the path escapes the project or is cross-KB,
  leave `depends_on: null` — the item becomes manual-only.
- `soak`: `--duration-days=<N>` required; `started_at` stays `null` until
  `start-soak` is called.

Works even when spec is in `IN_PROGRESS` — items can be anticipated during
development. Refuses to add items to `VERIFIED` (or legacy `DONE`) / `DISCARDED` specs.

### `checklist done <spec-path> <n> [--note="..."]`

Set item `n` to `status: done`, `resolved_at: <today>`. Record the optional
note. Refuses if the item is already `done` / `failed`. Refuses for soak items
whose `started_at` is still `null` (start the soak first, or the entry is
pointless).

### `checklist fail <spec-path> <n> --note="..."`

Set item `n` to `status: failed`, `resolved_at: <today>`. The `--note` is
**required** — the note is the record of what went wrong. A `failed` item
blocks `/feature verify`; resolve it by (a) flipping back to `done` with a
justifying note after the underlying issue is handled, or (b) opening a
follow-up spec via `/feature new` and leaving the item failed while the
follow-up tracks the remediation.

### `checklist start-soak <spec-path> <n>`

Set `started_at: <today>` on a `soak` item. Refuses if the item is not type
`soak` or if `started_at` is already set.

### `checklist list [spec-path]`

Render the checklist for a single spec (spec-path given) or for every
`SHIPPED` spec in the KB (no argument). Group output by project and by item
status. This is what `/feature status` calls internally for the shipped
groups.

### Auto-resolve pass

Whenever any checklist command runs, and at the start of `/feature status`
and `/feature verify`, walk the spec's `blocker` items. For each item with
`status: pending` and a non-null `depends_on`:

1. Resolve the path to `<kb_path>/repos/<project>/<depends_on>`. If it does
   not exist: skip (manual-only) and note once.
2. Read that spec's frontmatter `status`. If `VERIFIED` (or legacy `DONE`):
   flip this item to `status: done`, `resolved_at: <today>`, append a Log
   line: `- YYYY-MM-DD: auto-resolved blocker #<id> — depends_on <path> is VERIFIED`.
3. Otherwise: leave pending.

Auto-resolve never reaches outside the project's own KB — cross-project
dependencies stay pending until the user flips them manually.

---

### §6.2 handling

Use this parsing contract everywhere §6.2 is read (hand-off seeder,
Continue-mode SHIPPED renderer, Verify mode) so behavior stays identical.

**Pre-parse normalization**
- Strip a leading UTF-8 BOM if present.
- Normalize CRLF and bare CR line endings to LF.
- Match fence info strings case-insensitively; accept `yml` as a synonym for
  `yaml`.
- Treat any tab-indented fenced content line as a parse failure; tabs are
  invalid YAML indentation here.
- If multiple `## 6.2 Deploy & manual verification` headings exist, the
  first one wins and later duplicates are ignored.

**Block discovery**
- Locate `## 6.2 Deploy & manual verification`.
- Within the region from that heading to the next H2 (or EOF), take the
  first fenced code block whose info string is `yaml`, `yml`, or empty
  (case-insensitive). Ignore prose outside the block.

**Keys and types**
- `deploy_prerequisites` MUST be a YAML sequence of scalar strings. Any other
  type is invalid.
- `smoke_check` MUST be null or a mapping with exactly `command` and
  `expected`, both scalar strings. Any other shape is invalid. These
  spellings all resolve to null case-insensitively: key absent, empty value,
  `null`, `Null`, `NULL`, `~`, `empty`, `absent`.
- Unknown top-level keys are ignored for forward-compat.

**Canonical empty cases**
- `deploy_prerequisites: []` means the seed pass is a no-op.
- `smoke_check: null` means the Continue-mode Quick-check banner is
  suppressed.
- If §6.2 is entirely missing, treat it as both empty cases above.

**Failure handling**
- Malformed §6.2 means no fenced block, unparseable YAML, tab-indented
  content, or invalid typing. Emit:
  `⚠️ §6.2 block is malformed in <spec-path>; skipping deploy-recommendations actions. Fix the YAML or remove §6.2.`
- Do not crash and do not mutate §8.
- Hand-off seeder: force `status: SHIPPED`, and append to Log:
  `- YYYY-MM-DD: hand-off: §6.2 block malformed — seeding skipped, manual review required`
- Continue-SHIPPED renderer: suppress the Quick-check banner and continue to
  pending-items render.
- Verify mode: before auto-resolve, refuse with
  `Verification refused: §6.2 block is malformed. Fix the YAML or remove §6.2, then re-run.`
  Do not run auto-resolve, do not tally, leave status `SHIPPED`, and append
  no Log entry.

**String normalization**
- Trim leading and trailing whitespace.
- Collapse runs of internal whitespace to a single space.
- Lowercase.
- Strip a trailing period or semicolon.

Comparison uses the normalized form. Storage keeps the original text.

---

## Verify mode

`/feature verify <spec-path>` — attempt to close the post-merge cycle.

1. Read spec frontmatter `status`. Accept only `SHIPPED`; refuse otherwise.
2. Before auto-resolve, read §6.2 via the parsing contract in `§6.2 handling`.
   If §6.2 is malformed, emit the warning, refuse verification with
   `Verification refused: §6.2 block is malformed. Fix the YAML or remove §6.2, then re-run.`
   Do not run auto-resolve, do not tally items, leave status `SHIPPED`
   unchanged, append no Log entry, and make no §8 mutation.
3. Run the auto-resolve pass (see above) so recent upstream verifications
   propagate before the check.
4. Tally items:
   - All `status: done` → **terminal-evidence precondition first**: assert BOTH
     `spec_audit_evidence:` and `code_audit_evidence:` are present in the spec
     frontmatter with a value from the 5-value enum
     `{dual_model, single_model, self_fallback, contract_violated, skipped}`;
     either **absent / literal-null / off-enum** → do NOT flip, render the §3.4a
     terminal-evidence refusal banner naming the defective key(s) + defect shape
     + repair path. Otherwise flip spec `status: VERIFIED`, append Log
     `- YYYY-MM-DD: VERIFIED — all post-merge items closed`. Report success.
     After the status flip, run the backlog archive check:
     ```bash
     python3 "${CLAUDE_PLUGIN_ROOT}/tests/backlog_archive.py" "<kb_path>" --project <project> --dry-run
     ```
     If AUTO count N + CANDIDATE count M > 0, present the approval banner. Two variants:
     - **M ≥ 1** (candidates exist): show `## ⏸ AWAITING YOUR INPUT` banner listing AUTO count N + each candidate (`#<id>` "<block_title>" ↔ "<matched_row_title>" — *<hint>*), reply `all`/ids/`none`/`skip`. **Approve which candidates?** On reply → `--apply --archive-candidates <approved-ids>`; `none` → `--apply` (AUTO only); `skip` → nothing.
     - **M = 0** (AUTO-only): show `## ⏸ AWAITING YOUR INPUT` banner: "Backlog has **N** done item(s) ready to archive (all unambiguous). Reply `ok` to archive / `skip`." **Archive now?** On `ok` → `--apply` (no `--archive-candidates`); `skip` → nothing.
     After any `--apply`, show the diff; the user reviews and commits. The archiver never commits. `--dry-run` runs before `--apply`; `--apply` only on explicit reply. Not fired at session-start (#76a).
   - Any `failed` → refuse. Report each failed item with its note; tell the
     user to resolve via `checklist done <n> --note=...` or to open a
     follow-up spec.
   - Any `pending` → refuse. Report each pending item with what is
     outstanding (action description, blocker target, soak remaining days).

Verify does not advance soak timers automatically — if a soak's
`started_at + duration_days` has passed but the item is still `pending`, it
is treated as pending. The user runs `checklist done <n>` once they are
satisfied with the soak result (nothing blew up).

---

## Scope addition mid-flow

When the orchestrator is working inside a spec and the user introduces a new requirement that was not in the approved scope ("also need X", "нужно ещё Y", "забыли добавить Z", "ещё одна доработка", "one more thing", "by the way we should also…"), do **not** silently absorb it. Detect the intent and prompt a single fork.

**Intent phrases** (not exhaustive — the orchestrator should use judgement):
- "also need / also add / additionally / on top of that / one more thing / by the way / while we're at it / forgot to mention"
- "нужно ещё / также / кстати / забыли про / ещё одна доработка / дополнительно"

**Decision by context of the active spec:**

1. **Spec is `DRAFT` / `APPROVED` / `AUDIT_PASSED` / `IN_PROGRESS`** — ask exactly the banner below.

---
## ⏸ AWAITING YOUR INPUT

Scope addition detected. The current spec is still in flight.

- **Extend** → new step in the Implementation Checklist + matching `planned` block in the exec workdoc; spec stays in its current state. Runs `/feature extend <description>`.
- **Split** → separate follow-up spec linked via `follows_up`. Runs `/feature new <description> --follows-up <active-spec-path>`.

**Extend or split?**

2. **Spec is `SHIPPED`** — ask the banner below.

---
## ⏸ AWAITING YOUR INPUT

The spec is already merged. Do not re-open it for new implementation work. Two options:

- (a) post-merge action item (only if this is a manual step, not new code) — adds via `/feature checklist add <spec> action "<desc>"`.
- (b) new follow-up spec linked via `follows_up`.

**Which option — (a) or (b)?**

3. **Spec is `VERIFIED` (or legacy `DONE`)** — ask the banner below.

---
## ⏸ AWAITING YOUR INPUT

The spec is already verified and closed. A new follow-up spec (linked via `follows_up`) is the only option — VERIFIED never silently reverts to SHIPPED.

**Create the follow-up spec now?**

4. **No active spec / scope unclear** — fall through to the normal `/feature new` or `/feature continue` prompts from the trigger map. Do not invent an implicit extension.

Whichever option is chosen, append one Log line to the source spec documenting the decision ("scope extended — added step N: <desc>" / "follow-up spec created at <path>" / "post-merge action item N added: <desc>"). Silent scope creep is forbidden.

---

## Extend mode

`/feature extend <description>` — append a new step to a spec's Implementation Checklist and create the matching workdoc entry.

1. Resolve the target spec. If `$ARGUMENTS` contains a spec-path, use that; otherwise use the spec currently under discussion (ask if ambiguous).
2. Refuse on `SHIPPED` / `VERIFIED` (or legacy `DONE`) / `DISCARDED` — follow-up specs and post-merge action items are the right tools there (see *Scope addition mid-flow*).
3. If the spec is `DRAFT` / `APPROVED`, add the step via a normal spec edit in section `## 5. Implementation Checklist`; skip the workdoc write (no workdoc exists until `AUDIT_PASSED`).
4. If the spec is `AUDIT_PASSED` / `IN_PROGRESS`:
   - Append `- [ ] Step N: <description>` to the Implementation Checklist (N = next integer).
   - Append a matching `## Step N: <title>` block in the workdoc at `<kb_path>/repos/<project>/design/workdocs/<slug>/exec.md` with a `planned` block. Prompt the user for any of `goal` / `allowed_scope` / `passing_test_cmd` / `expected_pass_pattern` the description does not make obvious — these must be set before implementation starts. Leave `observed` empty.
   - Append to spec Log: `- YYYY-MM-DD: scope extended — added step N (<short description>)`.
5. Do **not** re-run the full audit loop. The existing audit covered the original scope; the new step gets its regular compliance check at implementation time. If the addition is substantial (new external API, new data model, cross-cutting), surface this and recommend `/feature new --follows-up` instead — it is a judgement call, not a hard rule.

### Follow-up specs (`--follows-up`)

`/feature new <description> --follows-up <prior-spec-path>` behaves like normal **New** except:

- Frontmatter is populated with `follows_up: <prior-spec-path>` (relative to `<kb_path>/repos/<project>/`, same convention as `depends_on`).
- One line is appended to the prior spec's Log: `- YYYY-MM-DD: follow-up spec created at <new-path>`.
- The new spec's **Context** section opens with a one-paragraph summary of what changed in the prior spec and why this work was split off (the orchestrator drafts it; the user may edit).
- `/feature status` renders the follow-up chain next to each spec row (`follows: <prior-slug>` / `followed-by: <new-slug>`) so the lineage is visible.

---

## Rules

- **Spec is source of truth.** Read at session start. Update as you work.
- **No implementation without approved spec.** Research and spec come first.
- **Log is append-only.** Never edit past entries.
- **One feature per spec.** Don't combine unrelated changes.
- **Specs in KB, code in source repos.**
- **Always offer agent choice** before implementation begins.
- **Merge ≠ done.** A spec with a non-empty post-merge checklist moves to
  `SHIPPED` on hand-off, not `VERIFIED`. Only `/feature verify` with every
  checklist item closed can reach `VERIFIED`.
- **No silent scope creep.** Every mid-flow scope addition must be explicit:
  a new step in the Implementation Checklist (extend), a post-merge action
  item (checklist add), or a linked follow-up spec (`--follows-up`). Record
  the decision in the source spec's Log.
