---
name: feature-document
description: Execute the DOCUMENT stage of a feature-development task — produce a requirements artifact + gap analysis BEFORE any design or code, capturing what the feature must do, what currently exists, and what's missing. Loads when starting a new feature or when the operator says "document the requirements for X" / "what does X need" / "scope X".
allowed-tools: Read, Write, Edit, Glob, Grep
effort: medium
---

# feature-document

The DOCUMENT stage skill — first stage of the feature-development chain
(`document → design → scaffold → implement → test`). Produce the
requirements doc + gap analysis that the design stage will build on.
Document means UNDERSTAND, not BUILD: this stage forbids writing code.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **New task entering document stage**: a task in [wiki/backlog/tasks/](../../../wiki/backlog/tasks/) has `current_stage: document` AND `readiness: 0` (just created from an idea or epic decomposition)
- **Direct verb**: operator says "document X", "scope X", "what does X need", "requirements for X", "what's the spec for X", "gap analysis on X"
- **From idea-capture handoff**: `idea-capture` produced an idea doc, next move is to convert it to a feature spec
- **From pm-plan handoff**: `pm-plan` decomposed an epic into modules/tasks; each task entering work needs document stage first
- **Document model only**: `documentation` chain (single stage) — uses this skill exclusively, no design/scaffold/implement/test follow

Do NOT load when:

- Task `current_stage` is past `document` (load `feature-plan` for design, `feature-implement` for build, etc.)
- Operator wants to design (load `feature-plan` — document is upstream of design)
- The task is just a config tweak (skip document, use `config-*` skills directly)
- Architectural scope (load `architecture-propose` — operates above the per-feature level)

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Read existing context

**Trigger**: skill loaded; current_stage is document.

**Process**:

1. Read the task file. Note: title, type (epic/module/task), the feature's high-level intent.
2. Read the parent epic (if this task belongs to an epic) — the epic's Done When list defines how this task contributes.
3. Read the second brain's view of related concepts: `python3 -m tools.gateway query --model feature-development --full-chain` (canonical artifact chain), and any related model pages (`python3 -m tools.view model <related-model>`).
4. Read existing AICP code that the feature will touch (use Grep to find related modules: `grep -rn "<keyword>" aicp/`). Don't read everything — read enough to know what currently exists.
5. Read existing wiki content related to the feature: `find wiki/ -name "*.md" -exec grep -l "<keyword>" {} +`. Note overlapping concepts.
6. Read related second brain pages via `python3 -m tools.view search "<keyword>"`.

**Quality bar (Operation 1 done when)**:

- [ ] Task + parent context understood (can summarize the feature's intent in 2 sentences)
- [ ] Canonical chain queried (know what artifacts the chain expects at each stage)
- [ ] Existing AICP code touched by the feature identified (specific files named)
- [ ] Related wiki content surveyed (overlap or duplication risk noted)
- [ ] Related second brain pages identified (1-3 pages that inform this feature)

### Operation 2: Author the requirements artifact

**Trigger**: Operation 1 context gathered.

**Process**:

1. Choose the artifact type:
   - **Standard feature** → `wiki/domains/<domain>/<slug>-requirements.md` using `wiki/config/templates/methodology/requirements-spec.md`
   - **Cross-cutting concern** (touches multiple subsystems) → also create a Concept page at `wiki/domains/<domain>/<slug>.md` to anchor the cross-cutting view
   - **Documentation-only task** (no design/code follows) → `wiki/domains/<domain>/<slug>.md` as a Concept page directly
2. Write the requirements artifact following the template structure exactly. Required sections (per LLM Wiki Standards):
   - **Functional requirements** — what the feature MUST do (specific, testable)
   - **Non-functional requirements** — performance, reliability, security constraints
   - **Out of scope** — explicit non-goals (prevents scope creep at design + implement)
   - **Acceptance criteria** — testable statements the test stage will verify
3. **Each requirement is testable**. "Feature is fast" is not testable. "Feature returns within 200ms p95" is testable.
4. **Out of scope is explicit** (per Methodology Standards: "the right model for the job is rarely the biggest model" — narrowing scope is half the design).
5. Cite the second brain pages that informed the requirements (in `sources:` frontmatter).
6. Run `python3 -m tools.lint <path>` on the artifact.

**Quality bar (Operation 2 done when)**:

- [ ] Artifact follows template structure exactly
- [ ] Every functional requirement is testable (assertion possible at test stage)
- [ ] Out of scope section names ≥1 thing this feature WON'T do
- [ ] Acceptance criteria map 1:1 to expected test cases
- [ ] `sources:` cites ≥1 second brain page or AICP wiki page that informed the requirements
- [ ] `tools/lint.py` exits 0

### Operation 3: Author the gap analysis

**Trigger**: Operation 2 requirements artifact complete.

**Process**:

1. Author `wiki/domains/<domain>/<slug>-gaps.md` (or append a `## Gap Analysis` section to the requirements doc if the feature is small).
2. The gap analysis answers ONE question: what currently exists vs what the requirements need? Use a table:

   ```markdown
   | Requirement | Currently exists | Gap | Effort |
   |-------------|------------------|-----|--------|
   | Router emits task_start event | aicp/core/events.py has emitter | Router doesn't call emit() | low |
   | ...                                                                       |
   ```

3. For each gap: classify the effort (low / medium / high) and identify the design decision the gap forces (e.g., "low effort, but requires deciding whether emit is sync or async — design stage").
4. Note dependencies: gaps that depend on OTHER gaps being closed first. The design stage will sequence them.
5. Run `tools/lint.py` on the gap doc.

**Quality bar (Operation 3 done when)**:

- [ ] Each functional requirement has a row in the gap table
- [ ] Each gap has effort classification (low/medium/high)
- [ ] Each gap notes the design decision it forces (where it surfaces in design stage)
- [ ] Inter-gap dependencies explicitly noted
- [ ] `tools/lint.py` exits 0

### Operation 4: Update task state for design transition

**Trigger**: Operation 3 gap analysis complete.

**Process**:

1. Open the task file. Update frontmatter: `current_stage: design`, `readiness: 25`, append both artifact paths to `artifacts:`.
2. Add a brief note to the task body: requirements summary (2-3 sentences), gap count + total effort estimate, link to both artifacts.
3. Commit: `docs(<scope>): T<id> document — requirements + gap analysis`.
4. Run `tools/lint.py wiki/backlog/tasks/<task-id>.md` to confirm validation.
5. Inform the operator: "Document done; design stage is next. Load `feature-plan` to author the design decision."

**Quality bar (Operation 4 done when)**:

- [ ] Task frontmatter shows `current_stage: design`, `readiness: 25`
- [ ] Both artifact paths in `artifacts:` list
- [ ] Task body has 2-3 sentence summary + artifact links
- [ ] Task lint passes
- [ ] Operator informed of stage advance

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Writing code during document stage (forbidden zones violation)

The temptation: while reading existing code in Operation 1, you spot a bug. Tempting to "just fix it." NO — document stage forbids writes to `aicp/`, `tests/`, `config/profiles/` (per [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml) document-stage `forbidden_zones`).

**Detection**: about to use Edit or Write on a path under `aicp/`, `tests/`, or `config/profiles/`.

**The rule**: STOP. File the bug as a separate task. Document stage produces wiki pages only. Per Methodology Standards: "Stage NAMES do not prevent violations. Explicit ALLOWED/FORBIDDEN lists do."

### Gotcha 2: Vague requirements ("feature should work well")

A requirement like "should be fast" or "should be reliable" gives the test stage nothing to assert. Vague requirements pass the structural check (a section exists) but fail the operational check (no testable assertion possible).

**Detection**: any requirement using qualitative terms (fast, reliable, simple, intuitive, scalable) without a measurable bound (`<200ms p95`, `99.9% uptime`, `<5 LOC per call`, etc.).

**The rule**: every requirement must yield a verifiable test. If you can't write a pytest assertion that proves the requirement is met, the requirement is too vague — refine it before leaving document stage.

### Gotcha 3: Skipping the gap analysis

The temptation: requirements are clear, the path forward is "obvious," skip the gap analysis. NO — gap analysis is what TURNS the requirements into a sequenced design plan. Without it, the design stage runs without prioritization.

**Detection**: task's `artifacts:` list under document stage has only the requirements file, no gaps file.

**The rule**: every feature has gaps (otherwise the feature already exists and you're not building anything). Author the gap analysis even if it's a 5-row table — the design stage NEEDS it to sequence work.

### Gotcha 4: Importing requirements from the operator's chat verbatim (paraphrase trap)

The operator describes the feature in chat. Tempting to copy their description into the requirements doc. NO — the operator's chat is a conversation, not a spec. Operators speak in natural language with implicit assumptions; requirements docs need to make assumptions EXPLICIT.

**Detection**: the requirements section reads like spoken English ("we'd like the router to be smart about choosing backends") rather than spec language ("Functional requirement R-1: Router selects backend based on complexity score with thresholds [0.3, 0.6]").

**The rule**: the requirements doc converts conversation to spec. Specs are typed, numbered, and unambiguous. If the operator's intent is unclear, ask — don't paper over with vague spec language.

### Gotcha 5: Out of scope section empty or missing

Methodology Standards: "the right model for the job is rarely the biggest model. Most real work uses 2-3 stage subsets." The same applies within a feature: most features should explicitly EXCLUDE things to stay focused. An empty out-of-scope section is a red flag — what does this feature NOT do?

**Detection**: the Out of Scope section is missing OR contains only "TBD" / "none" / similar placeholder.

**The rule**: every feature has things it deliberately doesn't do. List ≥1. "This feature does NOT add new model configurations — that's a separate task." This prevents scope creep at design and implement stages.

## Reference exemplars

Per Extension Standards, reference exemplars are the second brain's `model-builder` and `wiki-agent` skills. For the OUTPUT artifacts this skill produces:

- **Requirements + gap exemplar**: see `~/devops-solutions-research-wiki/wiki/domains/cross-domain/e003-artifact-type-system-requirements.md` and the companion `*-gaps.md` — the methodology standards' canonical document-stage exemplar.

## Domain context

This skill operates in **backend-ai-platform-python** — see [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml) for document-stage path patterns (`wiki/**/*.md`, `docs/**/*.md`) and forbidden zones (no `aicp/`, `tests/`, `config/profiles/` writes during document).

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| feature-plan | design stage (after) | Builds decisions on top of this skill's requirements + gap |
| feature-implement | implement stage (much later) | Writes code per the design; this skill captures requirements |
| feature-test | test stage (last) | Verifies the implemented feature; this skill defines the acceptance criteria the tests check |
| idea-capture | upstream of feature-document | Converts raw idea to structured idea doc; document converts idea doc to spec |
| pm-plan | upstream when an epic is being decomposed | Decomposes epic into tasks; each task then enters its own document stage |
| architecture-propose | for system-wide architecture | Multi-feature scope; this skill is per-feature |
