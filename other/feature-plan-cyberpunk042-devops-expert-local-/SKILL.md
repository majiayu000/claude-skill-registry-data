---
name: feature-plan
description: Execute the DESIGN stage of a feature-development task — produce a design document with explicit decisions, alternatives considered, and trade-offs, gated by operator approval before scaffold/implement begins. Loads when a task is at document→design transition or when the operator says "design X" / "plan how to build X" / "what's the approach for X".
allowed-tools: Read, Write, Edit, Glob, Grep
effort: high
---

# feature-plan

The DESIGN stage skill in the feature-development methodology chain
(`document → design → scaffold → implement → test`). Produce the design
artifact (typically a Decision page in `wiki/decisions/01_drafts/` or a
methodology Design Plan in `wiki/domains/<domain>/`) that captures decisions,
alternatives, and trade-offs BEFORE any scaffold or code is written.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Stage transition**: a task in [wiki/backlog/tasks/](../../../wiki/backlog/tasks/) has `current_stage: document` AND `readiness: 0-25` AND document-stage Done When all checked (gap analysis exists)
- **Direct verb**: operator says "design X", "plan X", "what's the approach", "how should we build X", "design the [feature/module]"
- **After feature-document completes**: document skill has produced wiki pages capturing the gap and requirements; next move is design
- **Refactor model design step**: refactor chain (`document → scaffold → implement → test`) skips design — but for non-trivial refactors operators may explicitly request a design step
- **Architecture review surfaced a gap**: `architecture-review` identifies a missing design decision and recommends authoring one

Do NOT load when:

- Task `current_stage` is `scaffold`, `implement`, or `test` (those are different skills; design is upstream)
- The task is documentation-only (load `feature-document`; documentation tasks stop at document stage)
- The change is routine (load the relevant operational skill — `ops-deploy`, `quality-coverage`, etc.)
- Architectural-scope work (load `architecture-propose` for whole-system designs that span multiple features)

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Read the document-stage artifacts and identify the decision

**Trigger**: skill loaded; current_stage is document-complete confirmed.

**Process**:

1. Read the task file. Note: title, type, Done When, and the document-stage artifacts list (typically a requirements doc + gap analysis in `wiki/domains/<domain>/`).
2. Read the requirements artifact. Identify what the feature MUST do (functional requirements) and what it MUST NOT do (constraints, non-goals).
3. Read the gap analysis. Identify what currently exists vs what the feature requires — the gap IS the scope of what needs to be designed.
4. Frame the design as ONE decision (or a coherent cluster of decisions). Per Decision Page Standards: "Decision section is ONE clear statement." Vague designs ("we'll figure it out as we build") are not designs.
5. List the alternatives you'll evaluate. Per Decision Page Standards: ≥2 alternatives with concrete reasons for rejection.

**Quality bar (Operation 1 done when)**:

- [ ] Document-stage artifacts read and understood (can summarize requirements + gap in your own words)
- [ ] The decision is framed as ONE clear question (e.g., "Should the router pick backends per-request or per-session?")
- [ ] At least 2 alternatives identified
- [ ] Operator confirmed the decision framing before you start authoring

### Operation 2: Author the design artifact

**Trigger**: Operation 1 framing approved.

**Process**:

1. Choose the artifact type:
   - **Single decision** with binary or small-N alternatives → `wiki/decisions/01_drafts/<slug>.md` (use `wiki/config/templates/decision.md`)
   - **Multi-step design** with multiple sub-decisions and a phased approach → `wiki/domains/<domain>/<slug>-design.md` (use `wiki/config/templates/methodology/design-plan.md`)
   - **System architecture** (multiple features, multiple components) → load `architecture-propose` instead
2. Author the artifact following the template's section structure exactly (per LLM Wiki Standards: structure beats freeform). For decisions: Summary → Decision (in `> [!success]` callout) → Alternatives (≥2 subsections, each with `> [!warning] Rejected:`) → Rationale (evidence-backed) → Reversibility (with explanation) → Dependencies (downstream impact).
3. **Each alternative MUST have a concrete rejection reason**. "Considered but didn't fit" is not a reason. Specific evidence: "Rejected: would require N backend changes that we can't validate within this feature's scope" — that's a reason.
4. **Rationale MUST cite evidence**. Source code line references, prior decisions in `wiki/decisions/`, second brain pages (`gateway query --model`), measurement data. "It seemed better" is not rationale.
5. **Reversibility MUST be honest**. Easy = swap a config. Moderate = update N files in a coordinated commit. Hard = changes consumer interface, requires migration.
6. **Dependencies MUST be specific**. Name the modules/files/configs that change if the decision is reversed.
7. Run `python3 -m tools.lint <path>` on the new file. Fix any errors.

**Quality bar (Operation 2 done when)**:

- [ ] Artifact follows template structure exactly (section order matches template)
- [ ] ≥2 alternatives with concrete rejection reasons (each in its own subsection with `> [!warning]` callout)
- [ ] Rationale references specific evidence (file paths, prior decisions, second brain pages, data points)
- [ ] Reversibility classified honestly (easy/moderate/hard) with explanation
- [ ] Dependencies section names downstream files/modules
- [ ] `tools/lint.py` exits 0 for the new file
- [ ] At least one cross-reference to a related wiki page (`Relationships` section non-empty)

### Operation 3: Operator review and adversarial pass

**Trigger**: Operation 2 artifact written and lint-passing.

**Process**:

1. Present the design to the operator. Don't paraphrase — point them to the actual file path and ask them to read it.
2. Adversarially challenge your own design. For each alternative you rejected, steel-man it: "Why might this be the right answer instead?" Capture any insights in the Rationale section.
3. Operator may push back on the framing, the rejected alternatives, or the rationale. **Iterate the file in place** — don't argue, update.
4. When operator says "approved" / "go" / "this is right": commit the artifact. Format: `docs(<scope>): T<id> design — <decision title>`.

**Quality bar (Operation 3 done when)**:

- [ ] Operator has READ the file (not just been told about it)
- [ ] Adversarial pass complete — each alternative was steel-manned at least mentally; insights captured
- [ ] Operator-driven iterations applied (if any)
- [ ] Operator explicitly approved the final design
- [ ] Artifact committed

### Operation 4: Update task state for scaffold transition

**Trigger**: Operation 3 design approved and committed.

**Process**:

1. Open the task file. Update frontmatter: `current_stage: scaffold`, `readiness: 50`, append the design artifact path to `artifacts:`.
2. Add a brief note to the task body: design decision summary (1-3 sentences), link to the artifact.
3. Commit: `chore(backlog): T<id> design → scaffold`.
4. Run `python3 -m tools.lint wiki/backlog/tasks/<task-id>.md` to confirm validation.
5. Inform the operator: "Design done; scaffold stage is next. Load `<task-type>-scaffold` skill or proceed manually if scaffold is trivial."

**Quality bar (Operation 4 done when)**:

- [ ] Task frontmatter shows `current_stage: scaffold`, `readiness: 50`
- [ ] Design artifact path in `artifacts:` list
- [ ] Task body has design summary + artifact link
- [ ] Task lint passes
- [ ] Operator informed of stage advance

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Designing without document-stage artifacts (skip-ahead pattern)

The temptation: operator says "design X" before the document stage finished, or before there's any gap analysis. You think "I have enough context to design from memory." NO — designing without the requirements/gap doc means you're designing from your interpretation of the conversation, not the documented spec.

**Detection**: task's `artifacts:` list under document stage is empty OR the requirements/gap files don't exist on disk.

**The rule**: STOP. Load `feature-document` first. Document stage produces the spec; design stage builds on it. Skipping document is the methodology violation Quality Standards calls "false readiness."

### Gotcha 2: Vague decision ("we'll go with the right approach")

A "design" that says "we'll evaluate options at implement time" is not a design — it's a deferral. The implementing developer will face the same fork in the road with no documented thinking.

**Detection**: your Decision section uses words like "consider", "depending", "as needed", "later we'll decide" — those are deferrals, not decisions.

**The rule**: every design names ONE specific approach as the decision. If you genuinely cannot decide because the requirements don't yet support a decision, the gap is in the document stage — go back there. If the decision is "we don't decide yet because of dependency Y," document THAT as a `[!question]` in the Open Questions section with the unblocking condition.

### Gotcha 3: Alternatives stated without rejection reasons (decision theater)

The Alternatives section lists 3 options. Each says "considered but didn't fit." This passes the structural check (≥2 alternatives) but fails the quality check (no concrete rejection reason). It's "decision theater" — appearance without substance.

**Detection**: each rejection reason is generic ("not a fit", "less aligned", "more complex"). No specific number, file reference, or constraint cited.

**The rule**: every rejection has a CONCRETE reason — a specific cost, a specific risk, a specific incompatibility. "Rejected: requires changing the router signature in 14 places, none of which are part of this feature's scope" is concrete. "Rejected: more complex" is not.

### Gotcha 4: Author then deploy without operator reading the file

Tempting to summarize the design in chat and ask "approved?" without the operator opening the file. They say yes. Two weeks later they discover a section they would have flagged. This is "approval theater" — formal yes without informed consent.

**Detection**: did you point the operator at a file path AND wait for them to read it? Or did you just paraphrase in chat and ask for approval?

**The rule**: the file is the contract. Operator must READ the file (or explicitly delegate that). "Approved based on your summary" is not approval — it's the operator trusting your summary, which is the same risk as having no design at all.

### Gotcha 5: Skipping the adversarial pass (own-design bias)

You authored 3 alternatives + rejected 2. Easy to wave the rejected ones off. But the adversarial pass — steel-manning each rejected alternative — is what catches design errors before they reach implement. Skipping it means biases in your initial framing carry through.

**Detection**: did you try to argue FOR each rejected alternative as if it were the answer? If not, you skipped the pass.

**The rule**: for each rejected alternative, write one sentence in the Rationale that summarizes its strongest case. If that strongest case is actually compelling, the rejection is wrong — revise the decision. The pass is not optional.

## Reference exemplars

Per Extension Standards, reference exemplars are the second brain's `model-builder` and `wiki-agent` skills. For the OUTPUT artifact this skill produces, the gold-standard examples are:

- **Decision page**: `wiki/decisions/01_drafts/4-tier-router-with-profiles-over-hardcoded-routing.md` (in this repo) — passes lint, follows Decision Page Standards exactly
- **Pattern page** (when design surfaces a reusable pattern): `wiki/patterns/01_drafts/profile-as-coordination-bundle.md` (in this repo) — 4 instances, exit criteria, when-not-to section
- **Second brain decision exemplars**: `~/devops-solutions-research-wiki/wiki/decisions/02_validated/`

## Domain context

This skill operates in **backend-ai-platform-python** — see [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml) for design-stage path patterns (`wiki/decisions/`, `wiki/domains/`) and forbidden zones (no `aicp/`, `tests/`, `config/profiles/` writes during design).

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| feature-document | document stage (preceding) | Captures requirements + gap; this skill makes decisions on top |
| feature-implement | implement stage (after scaffold) | Writes code per the design; this skill produces the design |
| architecture-propose | system-wide architecture decisions | Multi-feature scope; this skill is per-feature |
| architecture-review | review of an existing architecture | Reviews; this skill creates |
| feature-iterate | refining an already-shipped feature | Different chain (iterate, not develop); this skill is for greenfield features |
