---
name: sdd-propose
description: |-
  Use when creating a new change with all SDD artifacts — proposal, delta specs, design, and tasks. Triggers: "propose a change", "create a change for X", "I want to implement feature Y", "start a new change", "let's build X".
---

# SDD Propose

Create a change directory with all SDD artifacts.
Generates artifacts in dependency order: proposal → delta specs → design → tasks.

> `SPECS_ROOT` is resolved by the `sdd` router before this skill runs.
> Replace `.specs/` with your project's actual specs root in all paths below.

## Writing Style

Write the proposal, delta specs, design, and tasks in the voice of a professional technical writer.
Prefer ASD-STE100 Simplified Technical English: short sentences, one instruction per sentence, active voice, and one term per concept.
Keep identifiers, commands, paths, and RFC 2119 keywords exact.

## When to Use

- Starting a new feature or behavioral change
- User knows what they want to build and is ready to create a full change
- No active change exists for this work

## When Not to Use

- Existing specs to convert from another tool — use `sdd-translate`
- Deriving specs from code analysis — use `sdd-derive`
- A change already exists and needs implementation — use `sdd-apply`
- Need to think before speccing — use `sdd-explore` first

## Invocation Notice

- Tell the user when this skill is running: `sdd-propose`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Process

### Phase 1: Understand the Change

Ask the user:

1. **What are we building?**
   — feature, bugfix, refactor, migration?
2. **Change name** — kebab-case identifier (e.g., `user-auth-refresh`, `payment-retry`)
3. **Which capabilities does it touch?**
   — which existing specs are affected?
4. **What user value does this deliver?**
   — capture as one or more user stories (_As a {role}, I want {goal}, so that {value}_); see `references/sdd-change-formats.md` § 1.1.

Check `.specs/NORTH-STAR.md`.
If it is missing, offer to draft a candidate product north star (a 2–4 sentence elevator pitch) from the README and existing specs for the user to ratify — the change's user stories ladder up to it.
Do not invent or finalize it silently; the north star is a product decision the user owns.

Read `.specs/specs/` to understand existing baseline specs before generating deltas.
If `.specs/specs/` is empty or does not exist, generate delta specs using only ADDED sections — all behavior is new.

If the user isn't sure about scope, offer `sdd-explore` first.

### Phase 2: Generate proposal.md

Create `.specs/changes/<name>/proposal.md`.

See `references/sdd-change-formats.md` for the proposal format.

Write with the user's input:

- Intent: the why — problem being solved
- User Stories: the cross-cutting product value this change delivers, each laddering to `NORTH-STAR.md` (see `references/sdd-change-formats.md` § 1.1)
- Scope: concrete in/out lists
- Approach: high-level direction
- Open Questions: unresolved decisions (if any)

Present to user and confirm before continuing.

### Phase 3: Schema Baseline (if schemas configured)

If `.specs/.sdd/schema-config.yaml` exists:

1. Generate current schema snapshots and store in `.specs/changes/<name>/schemas/before/`.
2. Add a `## Schema Impact` section to `proposal.md` describing expected schema changes — new endpoints, new or modified models, removed operations.
   See `references/sdd-schema.md` § 2 for the format.
3. Create `.specs/changes/<name>/schemas/expected.md` with a prose description of the expected schema diff. `sdd-verify` uses this to cross-check actual changes at verify time.

If no schema config exists but `.specs/schemas/` contains files, emit a visible warning:

> **WARNING:** Found schema artifacts in `.specs/schemas/` but no `.specs/.sdd/schema-config.yaml`. Schema snapshots will not be captured for this change. Run `sdd-derive` or create the config manually to enable schema tracking.

If no schema config exists and `.specs/schemas/` is empty or absent, skip silently.

### Phase 4: Generate Delta Specs

Create `.specs/changes/<name>/specs/<capability>/spec.md` for each affected capability.

Order capabilities by build dependency — contract-defining and foundation capabilities before consumers — and use the same order in `proposal.md`'s Scope list, in `design.md`'s Decisions and Architecture, and in `tasks.md`'s task groups.
See `references/sdd-change-formats.md` § 4 for the principle and worked example.

**Read `references/sdd-spec-formats.md` § 1 before writing any requirement.**
It defines what a requirement is (contract shapes, authoring primitive, artifact separation) and is the primary guidance for this phase.

For each affected capability, ask: **what new contract are we adding, changing, or removing?**
State each requirement as a contract statement (guarantee, invariant, prohibition, precondition-consequence, or observable-state relationship — see § 1.1).
Lean toward universal claims where they apply.

For each universal SHALL claim, apply the **partition heuristic** in `references/sdd-spec-formats.md` § 1.6: ask whether the claim's input space splits along semantic lines the spec already names (lifecycle states, identity/equivalence, multi-source composition, derived-pair invariants).
If yes, write one scenario per partition; if no, a single scenario is fine.
Use spec vocabulary only — never partition along code paths or write-sites.

Mechanism thinking is expected here — algorithms, thresholds, strategies, data structures.
Park those thoughts in the proposal's `## Approach` section as they surface; they formalize in Phase 5 (`design.md`).
Do not put mechanism into the spec itself.

Restate a signature (function, method, endpoint, or command) in spec prose only where its shape is the contract.
The shape is the contract when external consumers depend on its names, types, or order (the published-interface test in `references/sdd-spec-formats.md` § 1.4).
Otherwise, state the behavior and leave the signature to the code and `design.md`.
A restated internal signature goes stale on any refactor that keeps the behavior, and the spec then disagrees with code that still meets the contract.

Delta-format rules:

- Read the existing baseline spec before writing the delta
- Only include capabilities that actually change
- Use only ADDED/MODIFIED/REMOVED/RENAMED sections that apply — omit empty sections
- Write the marker once as a `##` section heading, then the requirements under it: `## ADDED Requirements`, `### Requirement: {Name}`, `#### Scenario: {Name}`.
  Do not fuse the marker to a requirement heading (`## ADDED Requirement: {Name}`).
  `sdd-sync` strips the marker and keeps the level you gave it, producing a baseline requirement no later change can match by name (`references/sdd-spec-formats.md` § 4).
- MODIFIED: copy the full baseline requirement (text + every still-applicable scenario), then edit in place — the block must be the complete post-change requirement, because `sdd-sync` replaces it wholesale (`references/sdd-spec-formats.md` § 4).
  Note prior behavior in a `> Previously: …` line.
  The copy carries any call-path pin the baseline has; check the copied requirement against `references/sdd-spec-formats.md` § 1.4 and each copied scenario against § 1.5 point 4, and restate a pin as its outcome, so the proposal's approval covers the fix.
- Add a `Serves: {story-slug}` backlink to each requirement, naming the proposal user stories it advances (M:N; `references/sdd-change-formats.md` § 1.1).
  The backlink is delta-only and stripped at sync.
  A requirement that serves no story is a signal of over-engineering — drop it, or add the story that justifies it.

Present specs to user and confirm before continuing.

### Phase 5: Generate design.md

Create `.specs/changes/<name>/design.md`.

See `references/sdd-change-formats.md` for the design format.

Include:

- Context: architectural constraints or existing decisions that affect this change
- Decisions: each non-obvious choice with rationale and alternatives considered
- Architecture: ASCII diagrams of component relationships, data flows
- Risks: what could go wrong and mitigation
- Verification Waivers (optional): any SHALL requirement that genuinely cannot have automated execution evidence — include the requirement name, the reason automation is infeasible, a manual evidence reference, and a `Recorded` date or commit SHA.
  `sdd-verify` will otherwise flag any SHALL without runnable evidence as CRITICAL, and uses `Recorded` for provenance checking.
  See `references/sdd-change-formats.md` § 2 for the format.

Only include sections with content — omit empty sections.

#### Suggest Formal Verification Where Tests Only Sample

Formal verification is opt-in: suggest it, never start it.
Suggest it once, in one short message, when a requirement in this change meets all three conditions:

1. The requirement governs behavior whose failing cases are rare combinations: concurrency or distributed protocols (locking, replication, consensus, cache coherence), crash recovery and retries, transaction or ordering guarantees, authorization invariants, or a core algorithm that must be correct for every input.
2. Failure is expensive: data loss or corruption, a security breach, financial error, or state that cannot be recovered.
3. The requirement is a universal claim ("never", "always", "at most once") over a space that the planned tests and property-based tests only sample.
   Past incidents in that area that tests missed are strong evidence.

Name the requirement and the reason each condition holds.
Say that formal verification is separate work (a model or a proof, run with the `formal-verification` skill), not a task in this change.

If the user declines, continue and record nothing.
If the user accepts, finish this proposal unchanged; the formal work reads this change's requirements and runs on its own.
Every SHALL still needs its evidence-producing task in Phase 6, because a formal result does not replace it.

Present to user and confirm before continuing.

### Phase 6: Generate tasks.md

Create `.specs/changes/<name>/tasks.md`.

See `references/sdd-change-formats.md` for the tasks format.

Rules:

- Tasks are atomic — each can be done and tested independently

- Order tasks and groups by build dependency per `references/sdd-change-formats.md` § 4 — each task must depend only on capabilities built by earlier tasks; never order alphabetically or by order of discussion

- Group by component or phase, sequencing foundation groups before consumer groups

- Every task is a concrete action, not an outcome

- Every SHALL requirement must be paired with at least one task that produces runnable evidence — a named test (unit, integration, or e2e), a schema check, or a captured-output step.
  If automated evidence is genuinely infeasible, the requirement must appear in `design.md` § Verification Waivers with a manual evidence reference.
  `sdd-verify` enforces this rule.

- For each SHALL, enumerate the **foreseeable write-sites** the design implies — every code path the design names that produces or modifies the contract-asserted value: canonical path plus any alternative paths in `design.md` (deduplication shortcuts, cache fast-paths, retry/fallback branches, idempotency early-returns, merge or composition steps).
  Each foreseeable write-site needs its own paired evidence-producing test task — one test on the canonical path is not evidence for the shortcut, retry, or merge.
  Write-sites that emerge later during implementation are handled by `sdd-apply`'s write-site emergence rule and `sdd-verify`'s write-site enumeration; covering the foreseeable ones here keeps verify from flagging them.

- For each universal SHALL that needs generated evidence (`references/sdd-spec-formats.md` § 1.7), add a property-based or differential test task.
  Name in the task:

  - its form: a pure-function property, a stateful model (a sequence of generated operations checked against a model of the state), or a differential test;
  - the property, or the oracle;
  - the partitions and domain features its generator covers.

  One task can cover several requirements that share an oracle or a generator.
  When a property test already covers part of the claim, the task extends that test.
  Add the task by default; the user deletes it during task review if they do not want it.

### Phase 7: Validate

- [ ] Change directory exists: `.specs/changes/<name>/`

- [ ] `proposal.md` has Intent, User Stories, Scope (in/out), Approach

- [ ] Each user story uses _As a/I want/so that_ (value clause kept) and ladders to `NORTH-STAR.md`

- [ ] Delta specs use only ADDED/MODIFIED/REMOVED/RENAMED sections (no baseline format), each written once as a `##` heading holding `### Requirement:` entries

- [ ] `scripts/check_spec_format.py` passes on every delta spec:

  ```text
  uv run --quiet <skill_root>/scripts/check_spec_format.py .specs/changes/<name>/specs/
  ```

- [ ] Each requirement is a contract statement — a property about observable state that stands on its own without its scenarios (see `references/sdd-spec-formats.md` § 1)

- [ ] Universal SHALL claims have partition coverage per the heuristic in `references/sdd-spec-formats.md` § 1.6 — when a positive signal fires, scenarios cover each partition

- [ ] Mechanism (algorithms, thresholds, strategies, retry policies) appears in `design.md` or the proposal's Approach, not in spec text

- [ ] Each code name in a SHALL sentence is public API, a protocol member in the requirement that defines it, or an observable name (span, metric, error class, setting); any other name pins a call path (`references/sdd-spec-formats.md` § 1.4).
  Each THEN line checks only what its requirement promises (§ 1.5).
  This reaches named identifiers only; mechanism described in prose (an internal component, an internal object being created) still needs the refactor test.

- [ ] Each delta requirement carries a `Serves:` backlink to a proposal story, or is deliberately left unserved and surfaced as such

- [ ] `design.md` has at least one Decision with rationale

- [ ] `tasks.md` has atomic tasks, and tasks/groups are ordered by build dependency per `references/sdd-change-formats.md` § 4 — no task depends on a capability not yet built by an earlier task

- [ ] Affected capabilities appear in the same build-dependency order across `proposal.md` Scope, `design.md`, and `tasks.md` groups

- [ ] Every SHALL requirement maps to at least one evidence-producing task (test, schema check, or captured output) OR appears in `design.md` § Verification Waivers with a manual evidence reference

- [ ] Every foreseeable write-site implied by `design.md` (canonical path plus any alternative paths the design names — shortcuts, retries, merges) is paired with its own evidence-producing test task

- [ ] Every universal SHALL that needs generated evidence (`references/sdd-spec-formats.md` § 1.7) is covered by a property-based or differential test task that names its form, its property or oracle, and the partitions its generator covers

- [ ] No delta markers in `.specs/specs/` (baseline specs untouched)

### Phase 7a: Assess Change Order

Skip this phase if no other active change exists.

Compare the new change with every other active change (`references/sdd-change-formats.md` § 6):

1. **Shared requirements:** list each requirement that the new change's delta specs and another change's delta specs both name (§ 6.2).
2. **Dependencies:** for each other change, decide whether either change needs the other first, and of which kind and to which gate (§ 6.1).
   Read the other change's proposal, design, and tasks, not only its delta specs.
   A capability or rework dependency often shares no requirement.

Present the findings to the user with a recommended order and the reason for it.
When the user confirms, add the new change to `.specs/changes/ORDER.md`, or create the file from the template in § 6.3 if a dependency or shared requirement exists and the file does not.
If the file exists and the new change has no dependency and no shared requirement, add it under `## Independent`.

### Phase 8: Commit the Change Directory

After the user approves the artifacts, commit `.specs/changes/<name>/`, plus `.specs/changes/ORDER.md` if Phase 7a changed it, and nothing else.
Ask before committing, and use the project's commit conventions.
Draft the message with the `commit-message` skill if it is available.

This commit is the proposal commit.
`sdd-apply` does not start until it exists, and the spec-drift check (`references/sdd-change-formats.md` § 5.5) diffs every later spec edit against it.
Without it, no one can tell which spec text the user approved and which text changed during implementation.

## Output

- `.specs/changes/<name>/proposal.md`
- `.specs/changes/<name>/specs/<capability>/spec.md` per affected capability (delta format)
- `.specs/changes/<name>/design.md`
- `.specs/changes/<name>/tasks.md`
- `.specs/changes/ORDER.md`, created or updated when other active changes exist (Phase 7a)
- The proposal commit containing all of the above

Summary: change name, capabilities affected, task count, proposal commit SHA.

## Common Mistakes

- Not reading existing baseline specs before writing deltas
- Writing baseline format in change specs (missing ADDED/MODIFIED/REMOVED markers)
- Writing `## ADDED Requirement: {Name}` once per requirement, instead of one `## ADDED Requirements` section holding `### Requirement:` entries
- Writing scenarios that carry the contract instead of illustrating it — if deleting the scenarios leaves the requirement untestable, the requirement text is under-specified (see `references/sdd-spec-formats.md` § 1.5)
- Writing one scenario for a universal claim whose input space partitions along signals from `references/sdd-spec-formats.md` § 1.6 (lifecycle, identity, multi-source composition, derived-pair) — verify will flag this as partition-incomplete coverage
- Restating an internal function or method signature in a requirement when only its behavior is the contract
- Partitioning along code paths or write-sites in scenarios — that is mechanism; partitions must use spec vocabulary only
- Generating only canonical-path test tasks when `design.md` names alternative paths (shortcuts, retries, merges) — each foreseeable write-site needs its own paired test task, not just the canonical one
- Creating tasks that are too coarse (one task = "implement auth" instead of atomic steps)
- Ordering capabilities or task groups alphabetically or by order of discussion — ordering must follow build dependency per `references/sdd-change-formats.md` § 4 so the implementer never builds in anticipation of a missing capability
- Generating all artifacts without pausing for user confirmation between phases
- Ending without the proposal commit, or committing files other than the change directory and `ORDER.md` with it
- Proposing a change while other changes are active without checking for dependencies and shared requirements
- Using non-kebab-case change names
- Dropping the "so that {value}" clause from a user story — the value clause is the scope ceiling that bounds implementation effort, not decoration
- Writing a requirement that serves no user story (gold-plating) — every requirement should advance a story or be cut

## References

- `references/sdd-spec-formats.md` — baseline spec, delta spec, scenario formats
- `references/sdd-change-formats.md` — proposal, design, tasks, and `ORDER.md` formats
- `references/sdd-schema.md` — schema artifacts and lifecycle policy
- `scripts/check_spec_format.py` — checks each delta spec's heading structure; exits non-zero on a malformed spec
