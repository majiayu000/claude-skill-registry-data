---
name: qa-plan
description: "Generate a QA test plan for a sprint or feature. Reads CDDs and story files, classifies stories by test type, and produces a structured test plan covering automated tests, manual verification, smoke test scope, and sign-off requirements. Run before sprint begins or when starting a major feature."
argument-hint: "[sprint | feature: system-name | story: path]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion
agent: qa-lead
---

## QA policy, facts and authority

Apply `standards/evidence-lifecycle.md`, `standards/notes-adr-sync.md` and existing
collaboration authority. Read actual `workflow/workflow-catalog.yaml`, domain,
current transition and established project QA scope, including initialized
`memory_bank/t1_axioms/qa_context.md` or the existing owning Story/plan/decision.
QA orchestration is optional by default; strict obligations need explicit source,
authority and exact checks/scope. Review mode does not select strict QA. Absent
optional Memory Bank/QA Context with no actual strict selection uses the catalog's
default optional orchestration; disclose absence without requiring initialization.
Unknown applies to unresolved actual required applicability or conflicting policy,
not optional context absence. Resolve that affected scope before dependent claims;
Honor actual user-specified per-effect approval conditions when determining coverage;
do not invent strict obligations or passing results.
Optional orchestration never waives required Story AC, governing DoD, decisions,
evidence or required review. Type tables are starting points; actual owners decide
requirements. Each required check retains PASS/FAIL/NotRun/Blocked/Pending; N/A
needs a governing applicability reason and cannot erase a failure.

Separate sufficiency, actual execution, independence, acceptance and completion.
Files/keywords/counts, planning cases and self-checks prove none of the other facts.
Read relied-on bodies and minimum required direct/indirect dependency closure;
retain full SHA-256/byte sizes, recoverable originals and original-path witnesses.
Disclose reading omissions. Exact bound historical results may be reused only
where selected workflow permits, labeled historical with original runtime/observer,
inputs and scope; never call them this run's execution. Missing required originals
or observations leave affected checks incomplete. Risk acceptance is a separate
scoped record; it cannot change FAIL/NotRun/Blocked/Pending to PASS or completion.

Reuse named paths/effects authority across roles/retries; before new authority show
draft and complete effect set, asking only for material new scope. Review-only
invokes no write entrypoint. Report-only writes its new report, excluding inputs,
indexes, session/sprint/stage state and closure. Existing report paths require a
new revision with prior evidence preserved; index effects need their own covered
scope and historical links. Optional Memory Bank absence uses Story/report/
conversation fallback without initialization, publication or activation.

## User Guide

- When to use: Generate a QA test plan for a sprint or feature. Reads CDDs and story files, classifies stories by test type, and produces a structured test plan covering automated tests, manual verification, smoke test scope, and sign-off requirements. Run before sprint begins or when starting a major feature.
- Inputs: Command arguments: `/qa-plan [sprint | feature: system-name | story: path]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None; a plan is input, not executed evidence.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

# QA Plan

This skill generates a structured QA plan for a sprint, feature, or individual
story. It reads all in-scope story files and their referenced CDDs, classifies
each story by test type, and produces a plan that tells developers exactly what
to automate, what to verify manually, what the smoke test scope is, and when
testing sign-off is required.

Run this before a sprint begins so the team knows upfront what testing work
is required. A test plan written after implementation is a post-mortem, not a
plan.

**Output:** `production/qa/qa-plan-[sprint-slug]-[date].md`

---

## Phase 0: Domain Detection

Resolve substantive concept bodies, actual configuration and explicit project
decisions under `standards/technical-preferences.md` before domain-specific work.

- **Game**: consistent Game concept/configured legacy Game evidence → use `[Game]` paths below.
- **Product**: consistent Product concept or populated legacy Product sections can
  establish Product without a concept → use `[Product]` paths below.
- **Unknown**: no substantive evidence or conflicting/mixed owners; resolve the
  affected scope or ask before applying its requirements. Neutral planning continues.

Filenames, copied placeholders and concept absence do not establish a domain.
Do not default to Game or require a new concept when configured legacy Product
facts already resolve the actual scope.

## Dual-Domain Parity Contract

| Area | Game branch | Product branch |
|------|-------------|----------------|
| Context reads | Game Concept, module index, story files, CDD formulas/acceptance, engine notes, control manifest | Product Concept, module index, story files, CDD data/contracts/acceptance, API/CLI/workflow/auth/migration notes, control manifest |
| Steps | Classify Logic, Integration, Visual/Feel, UI, Config/Data stories; assign automated/manual/playtest evidence; define smoke scope | Classify API, CLI, Data/Migration, Auth/Permission, Workflow, UI, Integration, Ops/Deployment, Config stories; assign contract/migration/permission/workflow/manual evidence; define smoke scope |
| Outputs | `production/qa/qa-plan-[scope]-[date].md` with automated tests, manual playtest/evidence requirements, smoke list, sign-offs | `production/qa/qa-plan-[scope]-[date].md` with contract tests, CLI smoke, migration dry-run, auth/permission checks, integration traces, user-test/manual evidence, deployment smoke, sign-offs |
| Next steps | `/smoke-check sprint`, `/team-qa`, `/test-evidence-review`, `/regression-suite` | `/smoke-check sprint`, `/team-qa`, `/test-evidence-review`, `/regression-suite`, `/release-checklist` for deployment/package risk |

---

## Phase 1: Parse Scope

**Argument:** `$ARGUMENTS` (blank = ask user via AskUserQuestion)

Determine scope from the argument:

- **`sprint`** — read the most recent file in `production/sprints/`, extract
  every story file path referenced. If `production/sprint-status.yaml` exists,
  use it as the primary story list and fall back to the sprint plan for story
  metadata.
- **`feature: [system-name]`** — glob story files under `production/epics/`, filter
  to stories whose file path or title contains the system name. Also check the
  epic index file (`EPIC.md`) in that system's directory.
- **`story: [path]`** — validate that the path exists and load that single file.
- **No argument** — use `AskUserQuestion`:
  - "What is the scope for this QA plan?"
  - Options: "Current sprint", "Specific feature (enter system name)",
    "Specific story (enter path)", "Full epic"

After resolving scope, report: "Building QA plan for [N] stories in [scope]."

If a story file path is referenced but the file does not exist, note it as
MISSING and continue with the remaining stories. Do not fail the entire plan
for one missing file.

---

## Phase 2: Load Inputs

For each in-scope story file, read the full file and extract:

- **Story title** and story ID (from filename or header)
- **Story Type** field (if present in the file header — e.g., `Type: Logic`)
- **Acceptance criteria** — the complete numbered/bulleted list
- **Implementation files** — listed under "Files to Create / Modify" or similar
- **[Game] Engine notes** / **[Product] Technology notes** — any API warnings or version-specific notes
- **CDD reference** — the CDD path(s) cited
- **ADR reference** — the ADR(s) cited
- **Estimate** — hours or story points if present
- **Dependencies** — other stories this one depends on

After reading stories, load supporting context once (not per story):

- `design/cdd/module-index.md` — to understand system priorities and which
  CDDs are approved
- For each unique CDD referenced across all stories: read only the
   **Acceptance Criteria**, substantive rules/contracts, edge cases/dependencies and
   relevant **[Game] Formulas** / **[Product] Data Model**. Follow required attachments
   to closure and disclose reading limits; two sections do not guarantee all obligations.
- `docs/architecture/control-manifest.md` — scan for forbidden patterns that
  automated tests should guard against (if the file exists)

If no CDD is referenced in a story, note it as a gap but do not block the plan.
The story will be classified using acceptance criteria alone.

---

## Phase 3: Classify Each Story

For each story, assign a Story Type. If the story already has a `Type:` field
in its header, use that value and validate it against the criteria below. If the
field is missing or ambiguous, draft classification from actual AC/owner/surface and resolve required applicability; keywords are hints, not proof of capability or policy.

### [Game] Game Story Types

| Story Type | Classification Indicators |
|---|---|
| **Logic** | Acceptance criteria reference calculations, formulas, numerical thresholds, state transitions, AI decisions, data validation, buff/debuff stacking, economy transactions, or any testable computation |
| **Integration** | Criteria involve two or more systems interacting, signals or events propagating across system boundaries, save/load round-trips, network sync, or persistence |
| **Visual/Feel** | Criteria reference animation behaviour, VFX, shader output, "feels responsive", perceived timing, screen shake, particle effects, audio sync, or visual feedback quality |
| **UI** | Criteria reference menus, HUD elements, buttons, screens, dialogue boxes, inventory panels, tooltips, or any player-facing interface element |
| **Config/Data** | Changes are limited to balance tuning values, data files, or configuration — no new code logic is involved |

### [Product] Product Story Types

| Story Type | Classification Indicators | Test Approach |
|---|---|---|
| **API** | Criteria reference endpoints, request/response shape, status codes, rate limiting, pagination, OpenAPI/Swagger specs | Contract test — validate request/response shape, status codes, error format |
| **CLI** | Criteria reference command-line interface, flags, positional arguments, stdout/stderr output, exit codes, shell completion | Smoke test — run command with valid/invalid args, check exit codes and output |
| **Data/Migration** | Criteria reference database schema changes, data transforms, ETL steps, migration reversibility, data integrity checks | Migration test — apply forward, verify schema, apply reverse, verify clean rollback |
| **Auth/Permission** | Criteria reference login/logout flows, role-based access, token handling, session management, permission gates | Permission test — verify allowed user gets 200, denied user gets 403/401 |
| **Workflow** | Criteria involve multiple steps, state transitions, integration between 2+ services/modules, event/queue processing | Integration test — simulate full workflow end-to-end, verify each transition |
| **UI** | Criteria reference screens, components, forms, accessibility, responsive layout, user interaction flows | Manual step-through OR automated UI test (storybook/playwright/cypress) |
| **Integration** | Criteria involve external service calls, third-party APIs, webhooks, message queues | Integration test with mocks/sandbox — verify retry logic, timeout handling, error propagation |
| **Ops/Deployment** | Criteria reference CI/CD config, deployment steps, monitoring, alerting, infrastructure-as-code | Deployment test — dry-run deploy, verify health checks, verify rollback |
| **Config** | Changes are limited to configuration values, environment variables, feature flags — no new code logic is involved | Spot-check config values in target environment |

**Mixed stories**: assign the primary type based on which acceptance criteria carry
the highest implementation risk, and note the secondary type.

**[Game]** Mixed Logic+Integration or Visual+UI combinations are the most common.
**[Product]** Mixed API+Auth or Workflow+Data combinations are the most common.

After classifying all stories, produce a classification summary table in
conversation before proceeding to Phase 4. This gives the user visibility into
how tests will be allocated.

---

## Phase 4: Generate Test Plan

Assemble the full QA plan document. Use the template that matches the detected domain.

### [Game] Game QA Plan Template

````markdown
# QA Plan: [Sprint/Feature Name]
**Date**: [date]
**Generated by**: /qa-plan
**Scope**: [N stories across [N systems]]
**Engine**: [engine name from standards/technical-preferences.md, or "Not configured"]
**Sprint File**: [path to sprint plan if applicable]

---

## Test Summary

| Story | Type | Automated Test Required | Manual Verification Required |
|-------|------|------------------------|------------------------------|
| [story title] | Logic | Unit test — `tests/unit/[system]/` | None |
| [story title] | Integration | Integration test — `tests/integration/[system]/` | Smoke check |
| [story title] | Visual/Feel | None (not automatable) | Screenshot + lead sign-off |
| [story title] | UI | Interaction walkthrough | Manual step-through |
| [story title] | Config/Data | Data validation test | Spot-check in-game values |

---

## Automated Tests Required

### [Story Title] — [Type]
**Test file path**: `tests/[unit|integration]/[system]/[story-slug]_test.[ext]`
**What to test**:
- [Specific formula or rule from the CDD Formulas section]
- [Each named state transition or decision branch]
- [Each side effect that should or should not occur]

**Edge cases to cover**:
- Zero/minimum input values (e.g., 0 damage, empty inventory)
- Maximum/boundary input values (e.g., max level, stat cap)
- Invalid or null input (e.g., missing target, dead entity)
- [Any edge case explicitly called out in the CDD Edge Cases section]

**Estimated test count**: ~[N] unit tests

[If no CDD formula reference was found for this story, note:]
*No formula found in referenced CDD — test cases must be derived from acceptance
criteria directly. Review the CDD Formulas section before writing tests.*

---

## Manual QA Checklist

### [Story Title] — [Type]
**Verification method**: [Screenshot + designer sign-off | Playtest session |
Manual step-through | Comparison against reference footage]
**Who must sign off**: [designer / lead-programmer / qa-lead / art-lead]
**Evidence to capture**: [screenshot of X | video clip of Y | written playtest
notes | side-by-side comparison]

Checklist:
- [ ] [Specific observable condition — concrete and falsifiable]
- [ ] [Another condition]
- [ ] [Every acceptance criterion translated into a manual check item]

*If any criterion uses subjective language ("feels", "looks", "seems"), it must
be supplemented with a specific benchmark or a playtest protocol note.*

---

## Smoke Test Scope

Critical paths to verify before any QA hand-off for this sprint:

1. Game launches to main menu without crash
2. New game / new session can be started
3. [Primary mechanic introduced or changed this sprint]
4. [Any system with a regression risk from this sprint's changes]
5. Save / load cycle completes without data loss (if save system exists)
6. Performance is within budget on target hardware (no new frame spikes)

*Smoke tests are verified by the developer via `/smoke-check`. Reference this
list when running that skill.*

---

## Playtest Requirements

| Story | Playtest Goal | Min Sessions | Target Player Type |
|-------|--------------|--------------|-------------------|
| [story] | [What question must the session answer?] | [N] | [new player / experienced] |

**Sign-off requirement**: Playtest notes must be written to
`production/session-logs/playtest-[sprint]-[story-slug].md` and reviewed by
the [designer / qa-lead] before the story can be marked COMPLETE.

If no stories require playtest validation: *No playtest sessions required for
this sprint.*

---

## Definition of Done — This Sprint

A story is DONE when ALL of the following are true:

- [ ] All acceptance criteria verified — via automated test result OR documented
      manual evidence (screenshot, video, or playtest notes with sign-off)
- [ ] Test file exists at the specified path for all Logic and Integration stories
- [ ] Manual evidence document exists for all Visual/Feel and UI stories
- [ ] Required AC/evidence actually passes; `/smoke-check` required only in selected smoke/strict scope, otherwise recommended follow-up
- [ ] No regressions introduced
- [ ] Required review completed under actual selected workflow/input/independence; mode skip stays explicitly skipped
- [ ] Story file updated to `Status: Complete` (via `/story-done`)
````

### [Product] Product QA Plan Template

````markdown
# QA Plan: [Sprint/Feature Name]
**Date**: [date]
**Generated by**: /qa-plan
**Scope**: [N stories across [N systems]]
**Technology**: [language/framework from standards/technical-preferences.md, or "Not configured"]
**Sprint File**: [path to sprint plan if applicable]

---

## Test Summary

| Story | Type | Test Approach | Required Evidence |
|-------|------|---------------|-------------------|
| [story title] | API | Contract test — `tests/contract/[system]/` | Automated test passing |
| [story title] | CLI | Smoke test — `tests/smoke/[system]/` | CLI output + exit code |
| [story title] | Data/Migration | Migration test — `tests/migration/` | Forward + reverse log |
| [story title] | Auth/Permission | Permission test — `tests/auth/` | 200/403 response log |
| [story title] | Workflow | Integration test — `tests/integration/[system]/` | End-to-end trace |
| [story title] | UI | Manual OR E2E — `tests/e2e/` or manual walkthrough | Screenshot or test log |
| [story title] | Integration | Integration test with sandbox — `tests/integration/[system]/` | Mock responses + error cases |
| [story title] | Ops/Deployment | Dry-run deploy — CI pipeline | Deploy log + health check |
| [story title] | Config | Spot-check | Config diff + env log |

---

## Automated Tests Required

### [Story Title] — [Type]
**Test file path**: `tests/[contract|smoke|migration|auth|integration|e2e]/[system]/[story-slug]_test.[ext]`
**Framework**: [pytest / vitest / cargo test / go test — from project config]
**What to test**:
- [Specific behaviour from the CDD Data Model or acceptance criteria]
- [Each named API endpoint, CLI flag combination, or state transition]
- [Each side effect that should or should not occur]

**Edge cases to cover**:
- Empty/null input (e.g., empty request body, missing required field)
- Boundary values (e.g., max page size, zero results, limit reached)
- Invalid input (e.g., malformed JSON, wrong content type, expired token)
- Concurrency/race conditions (if applicable)
- [Any edge case explicitly called out in the CDD or story]
- Downstream failure modes (what happens when a dependency is unavailable?)

**Estimated test count**: ~[N] tests

[If no CDD data model reference was found for this story, note:]
*No data model found in referenced CDD — test cases must be derived from acceptance
criteria directly. Review the CDD Data Model section before writing tests.*

---

## Manual QA Checklist

### [Story Title] — [Type]
**Verification method**: [Manual step-through | Comparison against spec |
Accessibility audit | Exploratory testing | CLI walkthrough]
**Who must sign off**: [lead-programmer / qa-lead / product owner]
**Evidence to capture**: [screenshot of X | CLI output log | API response log |
accessibility report | side-by-side comparison]

Checklist:
- [ ] [Specific observable condition — concrete and falsifiable]
- [ ] [Another condition]
- [ ] [Every acceptance criterion translated into a manual check item]

*If any criterion uses subjective language ("easy to use", "looks right", "feels
fast"), it must be supplemented with a specific benchmark (e.g., "user completes
task in <30s", "page renders in <200ms p95").*

---

## Smoke Test Scope

Critical paths to verify before any QA hand-off for this sprint:

**[Product]**
1. Application starts without crash (server / CLI entry point / app launch)
2. Health check endpoint returns 200 (if API service)
3. [Primary feature introduced or changed this sprint]
4. [Any integration with a regression risk from this sprint's changes]
5. Database migration runs forward and reverse without error (if migrations exist)
6. Performance is within budget (p95 latency, error rate, memory)

*Smoke tests are verified by the developer via `/smoke-check`. Reference this
list when running that skill.*

---

## User Testing Requirements (if applicable)

| Story | Test Goal | Min Participants | Target User Type |
|-------|-----------|-----------------|-----------------|
| [story] | [What question must user testing answer?] | [N] | [new user / power user] |

**Sign-off requirement**: User testing notes must be written to
`production/session-logs/usertest-[sprint]-[story-slug].md` and reviewed by
the product owner before the story can be marked COMPLETE.

If no stories require user testing: *No user testing sessions required for
this sprint.*

---

## Definition of Done — This Sprint

A story is DONE when ALL of the following are true:

- [ ] All acceptance criteria verified — via automated test result OR documented
      manual evidence (screenshot, CLI output log, or user testing notes with sign-off)
- [ ] Test file exists at the specified path for all API, Data/Migration, Auth, and Workflow stories
- [ ] Manual evidence document exists for all UI and CLI stories
- [ ] Required AC/evidence actually passes; `/smoke-check` required only in selected smoke/strict scope, otherwise recommended follow-up
- [ ] No regressions introduced (existing test suite passes)
- [ ] Required review completed under actual selected workflow/input/independence; mode skip stays explicitly skipped
- [ ] Story file updated to `Status: Complete` (via `/story-done`)
````

When generating content, use the actual story titles, CDD formula/data model text,
and acceptance criteria extracted in Phase 2. Do not use placeholder text — every
test entry should reflect the real requirements of these specific stories.

---

## Phase 5: Write Output

Show the complete plan in conversation (or a summary if the plan is very long),
then verify existing authorization for the exact plan path/create-or-update effect. Continue when covered; only if missing or materially new ask:

"May I write this QA plan to `production/qa/qa-plan-[sprint-slug]-[date].md`?"

Write the plan exactly as generated — do not truncate.

Do not write T3 memory-bank evidence from `/qa-plan`. A QA plan is source
context for later QA evidence, not an evidence record. `/smoke-check`,
`/team-qa`, `/playtest-report`, and `/test-evidence-review` maintain
`memory_bank/t3_archive/qa_evidence_index.md` when approved evidence exists.

Planning/write operation can finish with declared gaps; no runtime/Story qualification is implied. Existing plan updates preserve entries/rationale within named effects; no implicit index/state write.

After writing:

"QA plan written to `production/qa/qa-plan-[sprint-slug]-[date].md`.

Next steps:
- Share this plan with the team before sprint implementation begins
- **[Game]** Run `/smoke-check sprint` after all stories are implemented to gate QA hand-off
- **[Product]** Run `/smoke-check sprint` after all stories are implemented to gate QA hand-off
- For test-requiring stories, create the test files at the listed paths
  before marking stories done — `/story-done` checks for them"

---

## Collaborative Protocol

- **Use named plan-write authority**: Phase 5 reuses covered existing authorization; only missing authority or materially new paths/effects require a write question. Content agreement and drafting alone do not authorize writing.
- **Classify conservatively**: **[Game]** when a story is ambiguous between Logic and
  Integration, classify it as Integration — it requires both unit and
  integration tests. **[Product]** when ambiguous between API and Workflow, classify
  as Workflow — it requires end-to-end verification.
- **Do not invent test cases** beyond what acceptance criteria and CDD content
  support. If critical content is absent from the CDD, flag it rather than guessing.
- Additional Game playtest/Product user testing is optional unless actual Story/DoD/catalog/current phase or selected QA scope requires it. Required behavior stays unverified until actual evidence; plan drafting does not satisfy it.
- Use `AskUserQuestion` for scope selection when no argument is provided.
  Keep other phases non-interactive: present findings, reuse covered plan authority,
  and ask only for missing or materially new write scope.
