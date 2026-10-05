---
name: mk:sprint-contract
version: 1.0.0
preamble-tier: 3
description: Use when negotiating a file-based sprint contract between the generator (developer) and evaluator before code is written. Translates a product-level spec into testable acceptance criteria with rubric tie-ins. Triggers on /mk:sprint-contract, "draft a sprint contract", "negotiate scope for sprint", or before any harness-driven sprint kicks off.
argument-hint: '[propose | review | amend | sign | validate | sprint-goal] [task-slug | sprint-goal-text] [--sprint N]'
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - AskUserQuestion
source: local
keywords:
  - sprint-contract
  - testable-criteria
  - generator-evaluator-handshake
  - scope-negotiation
  - rubric-tie-in
when_to_use: Use when negotiating a file-based sprint contract between generator (developer) and evaluator before code is written. NOT for plan generation (see mk:plan-creator).
user-invocable: true
owner: lifecycle
criticality: high
status: active
runtime: claude-code
---

# mk:sprint-contract — File-Based Sprint Contract Protocol

Negotiation protocol between generator and evaluator. Produces a signed contract file at `tasks/contracts/{date}-{slug}-sprint-{N}.md` BEFORE the generator writes any source code. Enforced by `gate-enforcement.sh` (Phase 4 extension).

> For single-task plan validation (cook flow), use `mk:validate-plan` instead. `mk:sprint-contract` is for product-level specs feeding into `mk:autobuild` only.

## When to Use

Activate when:
- User runs `/mk:sprint-contract <action> [task-slug]`
- Harness (Phase 5) needs to negotiate a sprint before invoking the generator
- Generator agent needs to read a signed contract before starting implementation
- A previously signed contract needs amendment due to mid-build scope discovery

Skip when:
- `MEOWKIT_AUTOBUILD_MODE=LEAN` (adaptive density bypass for COMPLEX/Opus 4.6 tier)
- The plan is `--fast` mode (overhead exceeds value)
- The task is `/mk:fix simple` (Gate 1 already bypassed; contract bypass too)

## Subcommands

| Subcommand | Owner | Effect |
|---|---|---|
| `propose` | generator (developer agent) | Drafts a contract from the product spec + rubric preset; status: `draft → negotiating` |
| `review` | evaluator | Critiques the proposed contract for testability + scope clarity; produces clarification requests |
| `amend` | generator | Iterates on the contract per evaluator feedback; status stays `negotiating`; rounds += 1 |
| `sign` | both | Both agents commit to the contract via git commit messages; status: `negotiating → signed` |
| `validate` | anyone | Runs `validate-contract.sh` to check schema conformance |
| `sprint-goal` | user | Writes/reads/aligns sprint-LEVEL goal in `tasks/contracts/sprint-state-{date}-sprint-{N}.md` (Agile mode) |

## Workflow (Inline — monolithic, < 150 lines)

### `propose` (generator)

1. Read active product spec from newest `tasks/plans/*/plan.md`
2. Load rubric preset via `mk:rubric/scripts/load-rubric.sh --preset {preset}`
3. Determine sprint `N`: max of existing `tasks/contracts/*-{slug}-sprint-*.md` + 1, default 1
4. Copy `assets/contract-template.md` → `tasks/contracts/{YYMMDD-HHMM}-{slug}-sprint-{N}.md`
5. Populate: 5–15 ACs in Given/When/Then form, each bound to one preset rubric, each with a Verification line. Every preset rubric should have ≥1 AC binding
6. Set frontmatter: `status: negotiating`, `rounds: 0`, `created: {YYMMDD-HHMM}`
7. Run `validate-contract.sh`; fix and re-validate until clean
8. Print: `"Contract proposed at {path}. Awaiting evaluator review."`

### `review` (evaluator)

1. Read newest `negotiating` contract for the active task
2. Per AC check: **Testable?** (probable via browser/curl/CLI) **Rubric-aligned?** (binding matches content) **Scope clear?** (no ambiguity)
3. For each weak AC, append `Round {N+1} (reviewer): AC-{NN} {clarification}` to Negotiation Log
4. If clean, write `Round {N+1} (reviewer): accepted` and proceed to `sign`
5. If clarifications added, increment `rounds` and signal generator to `amend`
6. **HARD CAP: 2 negotiation rounds.** Round 3 escalates to human via AskUserQuestion

### `amend` (generator)

1. Address every clarification from the previous round in the relevant ACs (replace, don't delete)
2. Append `Round {N+1} (proposer): {summary of changes}` to the log
3. Re-run `validate-contract.sh`
4. Signal evaluator to `review` again

### `sign` (both agents in sequence)

The signature workflow uses **two commits per agent** to avoid the chicken-and-egg of "the SHA must be inside the file but the file's commit hasn't happened yet."

1. **Generator (commit 1):** `git add tasks/contracts/{path}.md && git commit -m "contract: generator commits sprint {N} for {slug}"`. The contract file is committed with `generator_signed: pending`.
2. **Generator (commit 2 — capture SHA):** `gen_sha=$(git rev-parse HEAD)`. Edit the frontmatter: `generator_signed: $gen_sha`. Then `git add` + `git commit -m "contract: generator signs sprint {N} for {slug} (sha=$gen_sha)"`. The captured SHA references the COMMIT THAT EXISTED WHEN THE GENERATOR APPROVED — its own first commit.
3. **Evaluator (commit 1):** verify the contract is unchanged from commit 2 above. Then `git add` + `git commit -m "contract: evaluator commits sprint {N} for {slug}"`.
4. **Evaluator (commit 2 — capture SHA):** `eval_sha=$(git rev-parse HEAD)`. Edit the frontmatter: `evaluator_signed: $eval_sha`, `status: signed`. Then `git add` + `git commit -m "contract: evaluator signs sprint {N} for {slug} (sha=$eval_sha)"`.
5. The git log IS the audit trail — every signature commit is verifiable via `git log --oneline tasks/contracts/{path}.md`.
6. After both sign, `gate-enforcement.sh` allows source edits for this sprint.

**Validator enforcement:** `check-contract-signed.sh` rejects placeholder values (`null`, `pending`, `todo`, empty, quoted variants of these). Only a real `git rev-parse HEAD` SHA passes.

### `validate`

```bash
.claude/skills/sprint-contract/scripts/validate-contract.sh tasks/contracts/{path}.md
```

### `sprint-goal` (Agile mode — gated by `agile-sprint-commitment.md` 1)

Sprint-LEVEL goal management. Writes to `tasks/contracts/sprint-state-{date}-sprint-{N}.md` — distinct from per-story sprint-CONTRACT files.

| Action | Form | Effect |
|---|---|---|
| `set` | `mk:sprint-contract sprint-goal set "<text>" --sprint N` | Writes `sprint_goal:` (≤120 chars) to `tasks/contracts/sprint-state-{YYMMDD}-sprint-{N}.md`. Creates the file from `assets/sprint-state-template.md` if absent |
| `show` | `mk:sprint-contract sprint-goal show --sprint N` | Prints current `sprint_goal:` from the newest sprint-state file matching `--sprint N` |
| `align` | `mk:sprint-contract sprint-goal align --plan <path>` | Renders alignment between plan goal (frontmatter `goal:` or first H1) and sprint goal. Advisory — never blocks |

**Concurrent-write safety:** `sprint-goal set` MUST acquire `flock` on the sprint-state file before any read-modify-write. YAML frontmatter append is non-atomic across shells; lock is the only mitigation. Release on completion or error.

**Validator scope:** the existing `validate-contract.sh` is for sprint-CONTRACT files only. Sprint-STATE files have NO validator; YAML is parsed inline by consuming skills (this skill, `mk:agent-detector` Step 0b, `mk:jira-agile`).

**Why this lives here:** `tasks/contracts/` already belongs to this skill; co-locating `sprint-goal` avoids creating a sibling skill that duplicates path discipline.

### Mid-build amendment (post-sign)

The amendment flow MUST null both signature fields BEFORE adding the amendment block. Otherwise stale SHAs from the prior signing round would falsely pass `check-contract-signed.sh`.

1. **Generator opens amendment:**
   - Edit the frontmatter: `status: amended`, `generator_signed: null`, `evaluator_signed: null`
   - Append `### Amendment N — {YYMMDD-HHMM}` under `## Amendments` describing the change
   - DO NOT edit the original signed criteria — append the revised version as a new AC or override note
   - `git commit -m "contract: amendment N for sprint {N} ({slug})"`
2. **Both agents re-sign** following the same two-commit pattern from `sign` action above. New SHAs replace the nulled fields.
3. **`gate-enforcement.sh` enforcement:** between step 1 and step 2 (sigs are null but status is `amended`), source edits are BLOCKED. The check-contract-signed.sh script rejects amended-status contracts that have null/placeholder sigs. This is the intended discipline — you can't push source code while an amendment is in-flight.

Original signed criteria stay visible — amendments are append-only history.

## Adaptive Density Skip

When `MEOWKIT_AUTOBUILD_MODE=LEAN`:

- The contract negotiation is **skipped entirely** (per Phase 5 adaptive density policy for COMPLEX/Opus 4.6 tier — capable models self-derive criteria from the product spec)
- `gate-enforcement.sh` honors the env var and allows source edits without contract verification
- LEAN bypasses are logged to `.meowkit/telemetry/lean-bypass.log` for audit
- LEAN mode is a PROJECT-level setting, not per-file override

## Gotchas

- **Don't mutate signed criteria.** Revisions go in the Amendments section, not by editing original ACs in place
- **Don't exceed 2 negotiation rounds.** Escalate to human on round 3 — agents that can't converge in 2 rounds won't converge in 5
- **Don't skip the rubric tie-in.** Each AC must reference one rubric in the active preset, otherwise the evaluator has no anchor for grading
- **Don't write source code without checking the contract.** `gate-enforcement.sh` will block; the developer agent's "Contract Discipline" section codifies this behavioral requirement too
- **Don't sign without git commits.** The git log is the audit trail — `generator_signed` and `evaluator_signed` fields hold real SHAs, not "yes" placeholders

## References

| File | Purpose |
|---|---|
| `assets/contract-template.md` | Canonical per-story sprint-contract schema with placeholder ACs |
| `assets/sprint-state-template.md` | Sprint-LEVEL state contract template (used by `sprint-goal set`; tracks goal + committed_tickets + amendments + closure summary) |
| `scripts/validate-contract.sh` | Schema + AC-form validator (POSIX-aware Bash 3.2+) |
| `scripts/check-contract-signed.sh` | Gate helper called by `gate-enforcement.sh` to block source edits before sign |
| `references/bdd-to-ac-mapping.md` | How Gherkin scenarios map to acceptance criteria |
| `../../hooks/gate-enforcement.sh` | Hook that enforces the contract gate on Edit/Write of source files |
| `../../agents/developer.md` | Generator agent — owns `propose` and `amend` actions |
| `../../agents/evaluator.md` | Evaluator agent — owns `review` action; also Phase 3 active-verification consumer |
| `../mk:rubric/` | Rubric library — provides composed presets the contract binds to |
| `../mk:evaluate/` | Evaluator skill — reads signed contract via `step-01-load-rubrics.md` |

## Related Rules

- `.claude/rules/gate-rules.md` — Gate 1 contract-signing requirement this skill enforces before source edits are allowed

## Start

For interactive use, run `/mk:sprint-contract propose <task-slug>` to begin negotiation.
For harness-driven use (Phase 5), the harness skill invokes propose → review → amend → sign automatically as a substep between Phase 2 (test red) and Phase 3 (build green).
