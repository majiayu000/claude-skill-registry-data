---
name: architecture-propose
description: Propose a system architecture from an idea document — produce a buildable, reviewed `docs/architecture.md` covering components, layers, data flow, stack, deployment, security, scaling, and first 5 milestones. Loads when an idea is captured but no architecture exists, or when the operator says "propose architecture" / "design the system" / "how should we structure this".
argument-hint: [path to idea doc, default docs/idea.md]
allowed-tools: Read, Write, Edit, Glob, Grep
effort: high
---

# architecture-propose

The DESIGN-stage skill that converts a captured idea (typically the output of `idea-capture` or `idea-refine`) into a concrete, buildable system architecture document. Produces `docs/architecture.md` with the 9 standard sections, ready for `architecture-review` and operator sign-off.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Stage transition**: a task in [wiki/backlog/tasks/](../../../wiki/backlog/tasks/) has `current_stage: design` AND `methodology_model: feature-development` (or `project-lifecycle`) AND no `docs/architecture.md` exists yet.
- **Direct verb**: operator says "propose architecture", "design the architecture", "how should we structure this", "draft an architecture", "what's the system layout".
- **After idea-capture / idea-refine**: an idea document exists at `docs/idea.md` (or operator-named path) and the next stage is design.

Do NOT load when:

- Architecture already exists — load `architecture-review` to assess fit instead.
- Operator wants a code-level design (single feature, single module) — load `feature-plan` instead; architecture-propose is for system-level.
- The change is a refactor of existing architecture — load `refactor-architecture`; this skill is for greenfield or major redesign.
- No idea document exists — load `idea-capture` first to produce the input.

## Operations

This skill has 3 named operations. Execute in order. Each operation has its own Process, Quality bar, and Gotchas.

### Operation 1: Read inputs and confirm scope

**Trigger**: skill loaded; operator named (or defaulted to) an idea doc path.

**Process**:

1. Read the idea document at the path in `$ARGUMENTS` (default `docs/idea.md`). If missing, STOP and tell the operator to run `idea-capture` first.
2. Read [README.md](../../../README.md) and [CLAUDE.md](../../../CLAUDE.md) if they exist — these declare the existing project identity (type, domain, scale, phase) which architecture must be consistent with.
3. Read any pre-existing `docs/architecture*.md` to detect overlap or conflict.
4. Identify the **architectural question being answered**: greenfield system, replacement, extension of existing? State this back to the operator in one sentence and wait for confirmation before drafting.

**Quality bar (Operation 1 done when)**:

- [ ] Idea doc read; if missing, STOPPED with clear redirect to `idea-capture`.
- [ ] Project context (CLAUDE.md identity profile + README + any existing architecture) read.
- [ ] One-sentence framing of the architectural question stated and operator-confirmed.
- [ ] No FORBIDDEN paths per the design stage in [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml) (`aicp/`, `tests/`, `config/profiles/` are off-limits at design stage).

### Operation 2: Draft the architecture document

**Trigger**: Operation 1 confirmed.

**Process**:

1. Write `docs/architecture.md` with these 9 sections in order. Each section has a content bar — see the Quality bar below.

   ```markdown
   # [Project Name] — Architecture

   ## Overview
   One paragraph: what the system does and how it's structured.

   ## Components
   For each component:
   - **Name**: What it is
   - **Responsibility**: What it does (single responsibility)
   - **Interfaces**: How other components talk to it
   - **Technology**: What it's built with and why

   ## Layer Structure
   How components are organized (e.g., layers, services, modules).
   Include a directory structure proposal.

   ## Data Flow
   How data moves through the system. Key pathways.

   ## Technology Stack
   | Layer | Technology | Rationale |
   |-------|-----------|-----------|

   ## External Dependencies
   What this system depends on and why.

   ## Deployment Model
   How this runs: containers, serverless, bare metal, etc.

   ## Security Considerations
   Auth, data protection, access control.

   ## Scalability Path
   How this grows from MVP to production scale.

   ## First 5 Milestones
   Ordered steps to build this, each producing something testable.
   ```

2. Cross-link relevant brain knowledge: if the brain (`~/devops-solutions-research-wiki/`) has a domain page covering the project's domain, reference it inline (e.g., `[[Backend AI Platform Domain]]`).
3. For each `## Component`, name **the consumer**: which existing or planned component will invoke it? Architecture without consumers produces orphan components.
4. For `## Technology Stack`, every row's `Rationale` must answer "why this and not the alternative" — never just restate what the technology is.

**Quality bar (Operation 2 done when)**:

- [ ] All 9 sections present, in order, with the prescribed structure.
- [ ] Overview is exactly one paragraph (not bullet-pointed; not multi-paragraph).
- [ ] Components section names ≥1 component AND each has all 4 sub-fields (Name, Responsibility, Interfaces, Technology).
- [ ] Technology Stack rationale is a comparison ("X over Y because…"), not a description.
- [ ] First 5 Milestones each name ≥1 testable artifact (a passing test, a CLI command output, a deployable unit).
- [ ] Layer Structure includes a directory tree proposal (not just prose).
- [ ] Architecture is consistent with CLAUDE.md identity profile (no contradiction with existing type/domain/phase).

### Operation 3: Review with operator and finalize

**Trigger**: Operation 2 draft written.

**Process**:

1. Present the architecture document path to the operator and a 3-line summary: scope, key technology choice, biggest risk.
2. Wait for operator review. Common feedback patterns: "this component is missing", "this stack choice is wrong", "scaling path doesn't address X". Apply each as a targeted edit, not a rewrite.
3. After each round of edits, re-validate against the Operation 2 quality bar — corrections must not break section structure.
4. When the operator says "approved" or equivalent: update the task's `current_stage: design → scaffold` if a task file exists. Add `docs/architecture.md` to the task's `artifacts:` list.
5. Suggest the next skill to load: `architecture-review` for an independent second-pass, or `scaffold` to advance to the next stage.

**Quality bar (Operation 3 done when)**:

- [ ] Operator reviewed the document at least once.
- [ ] All operator feedback either incorporated OR explicitly rejected with rationale ("we don't add X because Y").
- [ ] Task file (if present) advanced to scaffold stage with architecture.md in artifacts.
- [ ] Next-step skill suggested.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: The "tech inventory" trap

Listing technologies without rationale. Symptom: Technology Stack rows whose Rationale is "Python is good", "Postgres is reliable", or "Docker is industry standard". This is a **description**, not a justification. The operator can't evaluate the choice — they don't see what was rejected and why.

**The rule**: every Rationale must include the comparison: *"Postgres over MongoDB because: (a) the data is highly relational with FK constraints, (b) the team has Postgres ops experience, (c) the read patterns favor SQL aggregations over document scans"*. If you can't name an alternative, you haven't designed.

### Gotcha 2: Orphan components (the architecture analog of OpenArms Bug 6)

A component listed in `## Components` that has no consumer. Reads cleanly in isolation but never gets called by anything. At implement time, someone writes its code, no one imports it.

**The rule**: for each component, name the consuming component(s). Trace at least one path from system entry (CLI, HTTP request, scheduled job) to every named component. If a component is unreachable from any entry, it shouldn't be in the architecture.

### Gotcha 3: Skipping the existing-context read (Operation 1 step 2)

Drafting an architecture that contradicts what's already in CLAUDE.md (type, domain, scale, phase) or in any existing `docs/architecture*.md`. Symptom: a "fresh design" that proposes a domain or pattern incompatible with the project's stated identity.

**The rule**: read CLAUDE.md, README.md, and any pre-existing architecture docs FIRST. If your draft contradicts them, either change the draft OR explicitly call the contradiction out: *"this proposal redefines the project domain from X to Y because…"* — make it visible, not silent.

### Gotcha 4: Layer Structure as prose

Writing the layer structure as paragraphs ("the data layer talks to the service layer which talks to the API layer…"). Reads fine but is not a buildable specification. The implementer can't tell whether `aicp/core/` or `aicp/services/` is correct.

**The rule**: include a literal directory tree (file-tree code-block style) in Layer Structure. Even if it's aspirational, the tree forces decisions that prose hides. The implementer treats the tree as the spec.

### Gotcha 5: First 5 Milestones as wishes

Listing milestones like "1. Core working, 2. Polish, 3. Production-ready". These aren't milestones — they're aspirations. They name no artifact, gate, or test.

**The rule**: each of the 5 milestones names a **testable artifact** — a CLI command that runs, a test file that passes, a Docker image that deploys, a function that returns a known value. If you can't write a one-line verification command, the milestone isn't a milestone.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill operates in the **backend-ai-platform-python** domain. See [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml) for design-stage allowed paths (`wiki/decisions/`, `wiki/domains/`, ADRs, tech specs) and forbidden zones (`aicp/`, `tests/`, `config/profiles/` — those are implement/test territory).

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| idea-capture | Before architecture exists | Captures raw intent into `docs/idea.md`; architecture-propose consumes that |
| idea-refine | Idea exists but is unclear | Sharpens the idea via guided questioning before architecture begins |
| architecture-review | Architecture exists | Reviews for gaps/risks; architecture-propose authors |
| feature-plan | Single feature, not whole system | Smaller scope; architecture is system-wide, feature-plan is per-feature |
| refactor-architecture | Existing architecture, restructuring | Behavior-preserving restructure; architecture-propose is greenfield or major redesign |
| scaffold | After architecture approved | Builds the directory tree + types + Protocols from the architecture spec |
