---
name: architecture-review
description: Review an architecture document for gaps, risks, and improvements — produce a structured review against 8 criteria (completeness, over/under-engineering, security, dependencies, testability, deployability, missing pieces) with a Ready / Needs Revision / Major Rethink verdict and per-issue specific fixes. Loads after `architecture-propose` produces a draft, or when the operator says "review the architecture" / "audit this design" / "what's wrong with the architecture".
allowed-tools: Read, Write, Edit, Glob, Grep
effort: high
---

# architecture-review

The DESIGN-stage paired skill that critically evaluates an architecture document produced by `architecture-propose` (or any pre-existing `docs/architecture.md`). Distinct from `architecture-propose` (authors) — this skill audits, scores, and prescribes targeted fixes.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **After architecture-propose**: a fresh `docs/architecture.md` exists and needs an independent second pass.
- **Direct verb**: operator says "review the architecture", "audit this design", "what's wrong with the architecture", "is this design ready to build".
- **Pre-implementation gate**: a feature-development task is at design→scaffold transition, the architecture is the source artifact, and you want a quality check before generating types/Protocols.
- **Drift check**: the architecture was written months ago, the project has evolved, and the operator wants to know what's now stale.

Do NOT load when:

- No `docs/architecture.md` exists — load `architecture-propose` to author one first.
- The change is a refactor proposal — load `refactor-architecture` (proposes restructure) or `pm-assess` (broader project state).
- The reviewer is an external code reviewer (PR review of code) — load `feature-review` instead.
- The architecture is itself proposing a major rethink — let `architecture-propose` finish before reviewing.

## Operations

This skill has 3 named operations. Execute in order.

### Operation 1: Read inputs and frame the review

**Trigger**: skill loaded; `docs/architecture.md` exists.

**Process**:

1. Read [docs/architecture.md](../../../docs/architecture.md) (or operator-named path) end-to-end. Don't skim — every section gets evaluated.
2. Read [docs/idea.md](../../../docs/idea.md) (or the idea doc the architecture was derived from). The architecture must address what the idea asked for.
3. Read [CLAUDE.md](../../../CLAUDE.md) identity profile to confirm scope baseline (type, domain, scale, phase).
4. State the review framing back to the operator: *"Reviewing docs/architecture.md against 8 criteria. The architecture is for [type/domain/scale]; idea source is [path]. Anything specific you want me to weight heavier?"* and wait for confirmation or scope adjustment.

**Quality bar (Operation 1 done when)**:

- [ ] Architecture doc fully read (not skimmed).
- [ ] Idea doc + CLAUDE.md identity baseline read.
- [ ] Review framing confirmed with operator (default 8 criteria, OR weighted per operator request).

### Operation 2: Score against the 8 criteria

**Trigger**: Operation 1 framing confirmed.

**Process**:

For each of the 8 criteria below, write a finding in this format:

```
### <criterion>
Status: PASS | CONCERN | FAIL
Evidence: <specific quote or section reference from architecture.md>
Reasoning: <why this is the score>
Specific fix (if not PASS): <concrete action — what to change, where>
```

The 8 criteria:

1. **Completeness** — Does every requirement from the idea doc have a home in the architecture? List any orphan requirements (in idea but not in architecture).
2. **Over-engineering** — Is anything more complex than needed for the current stage (per CLAUDE.md `phase` and `scale`)? Symptom: components/layers that exist for a future scale the project isn't at yet.
3. **Under-engineering** — Will anything obviously break at moderate scale? Symptom: single point of failure that will need re-architecting at 10× current load.
4. **Security** — Are there exposed attack surfaces (auth gaps, missing input validation boundaries, secret-in-config patterns)?
5. **Dependencies** — Are there risky external dependencies (single-vendor lock, unmaintained libs, large transitive trees)? Are any unnecessary?
6. **Testability** — Can each component be tested independently? Are interfaces narrow enough to mock?
7. **Deployability** — Can this be deployed incrementally (component by component) or only as one big-bang? Can it roll back?
8. **Missing pieces** — What's not addressed at all (observability, error handling, config management, backup, monitoring, …)?

After writing the 8 findings, assign a verdict:

- **Ready to build** — all PASS, or CONCERN-level only.
- **Needs revision** — ≥1 FAIL but the architecture's core shape is sound; targeted fixes will resolve.
- **Major rethink** — multiple FAILs OR the core shape doesn't fit the requirements; restart from `architecture-propose`.

**Quality bar (Operation 2 done when)**:

- [ ] All 8 criteria scored — none skipped.
- [ ] Each non-PASS finding includes specific fix (what to change, where in the doc).
- [ ] Each finding cites evidence (a quote or section reference), not just opinion.
- [ ] Verdict assigned with explicit reason.

### Operation 3: Deliver findings

**Trigger**: Operation 2 findings written.

**Process**:

1. Decide delivery mode based on operator preference and finding density:
   - **Inline review comments** (preferred for ≤5 findings): edit `docs/architecture.md` adding `> [!warning] REVIEW:` callouts at the relevant sections.
   - **Separate review doc** (preferred for >5 findings or major rethink): write `docs/architecture-review.md` with the full structured findings + verdict.
2. Add a `## Verdict` section at the top of whichever delivery mode is chosen, including: overall verdict, count of FAIL/CONCERN/PASS findings, top 3 fixes ranked by leverage.
3. Update the source task file (if present) with `current_stage: design → review-pending` and add the review doc path to `artifacts:`.
4. Suggest the next skill: if Ready to build → `scaffold`; if Needs revision → re-load `architecture-propose` for the targeted edits; if Major rethink → load `architecture-propose` from scratch.

**Quality bar (Operation 3 done when)**:

- [ ] Findings delivered (inline or separate doc).
- [ ] Verdict at the top, with FAIL/CONCERN/PASS counts and top 3 fixes.
- [ ] Operator told what's next based on verdict.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Pass-because-it-exists scoring

Marking a section PASS just because it's present in the architecture doc. Symptom: the Security section says "we use TLS" and you write `Status: PASS, Evidence: section exists`. The section being THERE is not the same as it being SUFFICIENT.

**The rule**: PASS means the section answers the criterion at the depth needed for the project's `phase` and `scale`. A one-line "we use TLS" Security section in a `phase: production` `scale: medium` project is FAIL — it doesn't address auth, data protection, or access control. Score by depth, not presence.

### Gotcha 2: Over-engineering blindness ("seems comprehensive")

Architectures that propose Kubernetes operators, multi-region replication, and event-sourcing for a `phase: prototype` `scale: small` project. The architecture LOOKS thorough but is wildly over-engineered. The reviewer who likes "comprehensive" doesn't catch this.

**The rule**: cross-check every component against CLAUDE.md `phase` and `scale`. A component that earns its place at `production / large` is over-engineered at `prototype / small`. Specifically flag: dedicated message queues for <100 events/day, multi-region for single-operator projects, custom auth services where library auth would do.

### Gotcha 3: Missing pieces blindness

The 8th criterion is "what's not addressed at all". This is the hardest — you can only spot what's missing if you compare against a checklist of what a complete architecture USUALLY covers. Easy to skip ("nothing missing that I noticed").

**The rule**: explicitly walk this list per review: observability, error handling, config management, backup/recovery, monitoring, deployment rollback, secret management, rate limiting, audit logging, schema migration. Anything NOT in the architecture is a finding.

### Gotcha 4: Verdict drift ("CONCERN with caveats" → Ready to build)

Producing a verdict that doesn't match the findings. Symptom: 2 FAILs and 4 CONCERNs but verdict is "Ready to build with minor follow-ups". This dilutes the verdict's signal — the next reader can't trust it.

**The rule**: count the findings. ≥1 FAIL = at minimum "Needs revision". ≥3 FAIL or ≥1 FAIL on Completeness/Security/Under-engineering = "Major rethink". The verdict is a function of the findings; don't soften it.

### Gotcha 5: Reviewing without reading the idea doc

Skipping Operation 1 step 2 (read the idea doc). The completeness criterion is meaningless without the source-of-truth requirements list. You'll mark Completeness PASS because the architecture covers everything you can imagine — but you can't see the gap to what was actually requested.

**The rule**: if `docs/idea.md` (or the named source) doesn't exist or you didn't read it, you cannot score Completeness. Either read it or explicitly mark Completeness "UNABLE TO ASSESS — no idea doc available; recommend running idea-capture and re-reviewing".

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill operates in the **backend-ai-platform-python** domain. See [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml) for design-stage allowed paths (`wiki/decisions/`, `wiki/domains/`, ADRs, tech specs) — review findings live in design-stage artifacts.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| architecture-propose | No architecture exists | Authors the doc; this skill reviews it |
| feature-review | Code-level review of a built feature | Reviews code; this skill reviews the design that preceded code |
| pm-assess | Whole-project state audit | Broader scope; architecture-review is design-doc-specific |
| refactor-architecture | Existing system, restructuring proposal | Authors a restructure; this skill could review the resulting proposal |
| quality-audit | Umbrella quality review | Calls this skill as one of its sub-audits |
