---
name: pm-plan
description: Generate or update a project plan with explicit milestones, dependencies, deliverables, effort estimates, critical path. For AICP this means breaking an architecture (`docs/architecture.md`) or epic (`wiki/backlog/epics/*.md`) into 5-10 milestones, each producing something testable, no milestone >2-3 sessions, and persisting to `.aicp/state.yaml` (or wiki epic body). Distinct from `pm-assess` (now-state synthesis), `pm-status-report` (cadence outward report), `idea-refine` / `architecture-propose` (which feed INTO this skill). Loads when the operator says "plan", "milestones", "break this into phases", "what's the roadmap", "decompose this".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# pm-plan

The forward-decomposition skill. Reads the source-of-truth (idea doc, architecture, epic) and produces 5-10 milestones with dependencies, deliverables, effort, and a critical path. Distinct from `pm-assess` (now-state), `pm-status-report` (cadence outward), `idea-refine` and `architecture-propose` (which produce the artifacts this skill plans against).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "plan", "make a plan", "generate a roadmap", "break this into milestones", "decompose this", "phases", "what's the ordering", "ordered roadmap".
- **Architecture-just-shipped signal**: an `architecture-propose` produced a fresh architecture doc; the operator wants to translate it into executable milestones.
- **Epic-needs-decomposition**: an epic in `wiki/backlog/epics/` is sized large and needs to be broken into per-task work.
- **Replanning**: existing plan is stale (incidents, mission shift, hardware unlock changed assumptions); operator wants to redo the plan.

Do NOT load when:

- Operator wants now-state, not forward — load `pm-assess`.
- Operator wants a single-task design (not multi-milestone) — load `feature-plan`.
- Operator wants to refine an idea before architecture — load `idea-refine`.
- Operator wants to propose a system design — load `architecture-propose` (this skill plans an EXISTING design).
- Operator wants per-sprint capacity tracking only — that's a status-report concern, not planning.

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Read source artifacts and gather constraints

**Trigger**: skill loaded; operator named the artifact to plan from (or it's clear from project state).

**Process**:

1. Locate the source-of-truth being planned:
   - `docs/architecture.md` (project-level architecture).
   - `wiki/backlog/epics/<epic>.md` (an epic to decompose).
   - `docs/idea.md` (idea, needs `architecture-propose` first — defer to that).
2. Read CONSTRAINTS that bound the plan. AICP-specific:
   - Hardware: dual-GPU 19GB VRAM, 64GB RAM, single-active-backend with LRU eviction, MAX_ACTIVE_BACKENDS=3.
   - Profile system: 11 profiles; `default` audit-safe, `personal` shared-pool — band-1 gets different backend per profile.
   - Reliability stage 4 (deferred work).
   - Brain compliance Tier 4/4 STRUCTURAL (already reached).
   - Operator constraints from CLAUDE.md identity profile (solo execution, Goldilocks SDLC default per task).
3. Read the CURRENT state to avoid replanning what's done:
   ```bash
   cat .aicp/state.yaml 2>/dev/null
   git log --since="3 months ago" --oneline | head -30   # what's already shipped
   ls wiki/backlog/epics/*.md 2>/dev/null   # other open epics that may overlap
   ```
4. Identify EXTERNAL dependencies (things this plan can't control):
   - Cloud provider availability (Anthropic, OpenRouter, Ollama Cloud).
   - Sister-project deliverables (openfleet feature X must exist before AICP can integrate).
   - Operator availability (vacation, calendar windows).
5. Get a sizing read from the operator: target horizon (this sprint / this quarter / this milestone-set spans 6 months) — affects granularity.

**Quality bar (Operation 1 done when)**:

- [ ] Source-of-truth artifact identified and read.
- [ ] Hardware/profile/system constraints captured.
- [ ] Current shipped state read (don't replan what's done).
- [ ] External dependencies enumerated.
- [ ] Target horizon agreed with operator (or explicit default like "Q2 plan, ~12 weeks").

### Operation 2: Decompose into milestones

**Trigger**: Operation 1 source + constraints understood.

**Process**:

1. Apply decomposition rules:
   - **5-10 milestones total**. Fewer than 5 → milestones too big; more than 10 → not milestones, those are tasks.
   - **Each milestone produces something TESTABLE**. "Refactor module X" alone isn't testable; "Refactor module X with no test count regression" is.
   - **No milestone >2-3 sessions of work**. If a milestone is bigger, decompose it further (it's actually 2 milestones).
   - **Vertical slices over horizontal layers**. A milestone "Add cloud-backend X end-to-end" beats a milestone "Add cloud-backend layer for all backends" — the first ships value, the second is plumbing without value.
2. For each milestone, fill this shape:
   ```yaml
   - id: M<NN>
     name: <one-line title>
     description: <2-3 sentences: what changes after this milestone>
     deliverables:
       - <concrete artifact: file, command output, demo>
       - ...
     dependencies:
       - M<NN-1>   # internal dependencies on prior milestones
       - external: <list of external blockers>
     effort: S | M | L   # S=single session, M=2 sessions, L=3 sessions max
     test_signal: <how do we KNOW this milestone shipped?>
     risk: <one-line — what could derail this milestone>
   ```
3. Identify the CRITICAL PATH — the longest chain of dependent milestones. The plan's calendar duration is determined by this chain, not by the sum of all milestones.
4. Identify PARALLELIZABLE milestones (no shared dependencies) — those can run concurrently if operator wants.
5. Identify the FIRST milestone — the one that delivers earliest value with smallest blast radius. The "if I had to ship something tomorrow, this is what I'd ship" milestone.
6. Sanity-check against constraints:
   - VRAM-heavy milestones can't run in parallel on single-host AICP.
   - Brain-compliance-affecting milestones should be ordered to maintain Tier 4.
   - Cloud-cost-affecting milestones should be checked against monthly spend ceiling.

**Quality bar (Operation 2 done when)**:

- [ ] 5-10 milestones, each with all 6 fields filled.
- [ ] Each milestone produces testable output.
- [ ] No milestone >L (3 sessions).
- [ ] Critical path explicitly identified.
- [ ] First milestone (earliest value, smallest blast radius) identified.
- [ ] Constraint sanity-checks done (VRAM / brain / cost).

### Operation 3: Persist + present for review

**Trigger**: Operation 2 milestones authored.

**Process**:

1. Persist where the project conventionally tracks plans:
   - **AICP**: `.aicp/state.yaml` `milestones:` field (small project) OR `wiki/backlog/epics/<epic>.md` (epic-scoped).
   - **Sister projects**: respect their convention (Plane project view, openfleet's standing-orders).
2. Generate a one-page SUMMARY for the operator (the "wall version"):
   ```
   PLAN — <topic>, target <horizon>

   Critical path: M01 → M03 → M05 → M07 → M09  (≈<N> sessions)
   Parallelizable: M02 alongside M01, M04 alongside M03, M06 alongside M05.

   M01 (S, no deps) — <name>: <one-line>
   M02 (S, no deps) — <name>: <one-line>
   M03 (M, deps: M01) — <name>: <one-line>
   ...

   Risks (top 3):
   - <risk-name>: <impact>. Mitigation: <plan>.
   ...

   Suggested first milestone to start: M01 (load: <which skill / what command>).
   ```
3. Present to operator BEFORE committing the plan to disk. Operator approves / adjusts / rejects:
   - Common adjustments: combine two small milestones; split a milestone that's actually two; reorder for risk-mitigation.
   - If the operator rejects substantially, re-do Operation 2 with the new framing — don't paper over a bad plan with edits.
4. After approval, commit the persisted plan as a SEPARATE commit:
   ```
   git add .aicp/state.yaml   # or wiki/backlog/epics/<epic>.md
   git commit -m "plan(<topic>): <N> milestones, target <horizon>"
   ```

**Quality bar (Operation 3 done when)**:

- [ ] Plan persisted to project's plan location.
- [ ] One-page summary delivered to operator with critical path, parallelizable milestones, top 3 risks, suggested first milestone.
- [ ] Operator approval received (or revisions absorbed via re-Operation-2).
- [ ] Plan committed as a separate commit.

### Operation 4: Wire to execution

**Trigger**: Operation 3 plan approved + persisted.

**Process**:

1. For each milestone, identify the SKILL that executes it:
   - Architecture-tied → `feature-document` → `feature-plan` → `feature-implement` → `feature-test` → `feature-review`.
   - Foundation-bootstrap → `foundation-deps` / `foundation-docker` / `foundation-testing` / etc.
   - Refactor-tied → `refactor-architecture` / `refactor-split` / `refactor-extract` / etc.
   - Ops-tied → `ops-deploy` / `ops-rollback` / `ops-maintenance`.
2. For the FIRST milestone, file a task immediately:
   ```bash
   python3 -m tools.gateway task new --title "<M01 name>"
   # or operator's preferred path
   ```
3. Update `.aicp/state.yaml` `current_task` if the first milestone becomes the active task.
4. Optional cross-link to brain:
   - If the plan is significant enough (mission-level) — file a brief contribution to `wiki/log/` so cross-project agents see the direction.
   - Don't spam every milestone-set into the brain — only mission/quarter-level plans warrant it.

**Quality bar (Operation 4 done when)**:

- [ ] Each milestone has a named execution skill (or "no skill — manual operator work").
- [ ] First milestone's task filed (or "first milestone is informational, no task needed").
- [ ] state.yaml current_task updated if applicable.
- [ ] Mission-level plan cross-linked to brain (or explicitly skipped: "tactical plan, not mission-level").

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Horizontal-layer milestones that ship no value

Plan reads: M01 "Add data layer for all backends", M02 "Add transport layer for all backends", M03 "Add UI layer for all backends". Three months in, NOTHING is end-to-end usable. Operator can't demo, can't test integration, can't tell what's working. The plan optimized for layer-purity, not for value delivery.

**The rule**: Operation 2 step 1 — vertical slices over horizontal layers. M01 should be "Cloud-backend X end-to-end (data + transport + UI)"; M02 should be "Cloud-backend Y end-to-end". Each milestone delivers an integration test that PASSES at milestone completion. If a milestone has no end-to-end test, it's not a milestone — it's plumbing pretending to be one.

### Gotcha 2: Effort estimates that are pure aspiration

Every milestone in the plan is sized "S". Twelve milestones × 1 session each = 12 sessions to ship. Reality at session 6: 4 milestones done. The "S" estimates were "what I hope this takes", not "what it has historically taken".

**The rule**: Operation 2 step 2 anchors effort to historical evidence. If `git log --shortstat` shows recent milestones taking N sessions, similar future milestones default to N. Adjust DOWN only with concrete reason (smaller scope / similar pattern already done). NEVER everything-is-S — the plan must contain at least one M and one L unless every milestone is genuinely small (rare).

### Gotcha 3: Critical path not actually the critical path

Plan claims critical path is M01 → M03 → M07. But M07 actually depends on M05 which depends on M02 — there's a longer chain hidden in the dependencies. Operator paces work assuming 3-link critical path; reality is 5-link, plan slips by 40%.

**The rule**: Operation 2 step 3 traces critical path FROM EACH leaf-milestone backward, takes the LONGEST resulting chain. Verify by drawing the dep graph (mental or text). If you can't trace each milestone back to a chain head, the dependencies are incomplete.

### Gotcha 4: Forgetting external dependencies

Plan has zero external dependencies listed. Operator builds against an OpenRouter feature that's still in beta — feature gets retracted week 8. Plan slips, the dependency wasn't surfaced as risk.

**The rule**: Operation 1 step 4 enumerates external deps. Operation 2 step 2 lists them per milestone. If a milestone has no external dep, say so explicitly ("dependencies: external: none"). Silence on external deps means "we forgot to check", not "there are none".

### Gotcha 5: First milestone too big

Plan starts with M01 "Build the foundation: deps + Docker + CI + testing + auth + database + config". A 6-week first milestone, no incremental value, operator stalls trying to nail everything at once.

**The rule**: Operation 2 step 5 — first milestone is SMALL, delivers earliest value, smallest blast radius. If your first milestone is "set up everything", split it into M01 "smallest end-to-end working slice" and M02-M0N "expand the slice". The first thing on disk should be runnable in a session, not a quarter.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning. Specifically for plan ARTIFACTS, the AICP Post-Anthropic 5-stage arc (Stage 1-5) is a real example of mission-level milestones with critical path; see [docs/architecture/post-anthropic-mission.md](../../../docs/architecture/post-anthropic-mission.md).

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP plans tend to be mission-driven (Post-Anthropic was 5 stages over months) or epic-scoped (a refactor or evolution). Plans live in `.aicp/state.yaml` (project-level) or `wiki/backlog/epics/*.md` (epic-level). Hardware/profile constraints are first-class — VRAM-heavy milestones can't run in parallel; profile changes affect routing tier_map and must coordinate with `config-deploy`. Brain-compliance milestones (Tier 1→2→3→4) are sequential by definition; this skill respects that ordering. Sister projects (openfleet, dspd, nnrt) use Plane (DSPD) or standing-orders.yaml (openfleet) for plans.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| pm-assess | Now-state synthesis | Now; this skill is forward |
| pm-status-report | Cadence outward report | Outward; this skill is internal planning |
| pm-handoff | Cross-session continuity | Continuity; this skill is forward decomposition |
| pm-retrospective | Look-back analysis | Backward; this skill is forward |
| feature-plan | Single-feature design | Single feature; this skill is multi-milestone |
| architecture-propose | Propose a system architecture | Produces input; this skill plans against it |
| idea-refine | Refine an idea before architecture | Earlier in pipeline; this skill plans architecture-level work |
| evolve-scale | Scale to multi-host | Specific evolution; this skill is generic planning |
