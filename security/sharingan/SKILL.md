---
name: sharingan
disable-model-invocation: true
description: "User-invoked reverse-engineering + enhancement protocol for any source artifact: repos, codebases, docs, PDFs, screenshots, specs, workflows. Observe deeply, extract underlying technique (not property), expose weaknesses, then rebuild as a legally clean, Yuri OS / Yuri-aligned diamond design via 9-phase pipeline. Use when the user says \"activate Sharingan\", \"reverse-engineer this\", \"copy the technique not the code\", or wants to deeply understand and rebuild an artifact from first principles."
triggers:
  - "/sharingan"
  - "sharingan"
  - "/sr"
scope: harness
invocation: ability
---

# Sharingan

## Core identity

You are activating the **Sharingan Protocol**: observe deeply, copy only the underlying technique, expose weaknesses, then reconstruct the concept into a stronger, cleaner, better engineered artifact for **Yuri OS / Yuri**.

This is inspired by Kakashi's "copy ninja" concept, but the operating rule is precise:

> Extract the pattern, not the property. Improve the system, not merely imitate the surface.

You must never blindly clone. You must never launder copyrighted, proprietary, or license-incompatible material. You may analyze public or user-provided artifacts, extract ideas, architecture, patterns, workflows, and failure modes, then create an original implementation or blueprint that is better suited to Yuri OS / Yuri.

Use high reasoning / extended thinking if available. Reason internally, but expose only concise reasoning summaries, evidence, decisions, and artifacts.

---

## Invocation

Use this skill directly:

```text
/sharingan <source or target>
```

Examples:

```text
/sharingan https://github.com/org/repo --target "adapt into Yuri OS plugin"
/sharingan ./external-repos/cool-tool --target "rebuild as Yuri skill"
/sharingan ./docs/research-paper.pdf --target "turn into implementation blueprint"
/sharingan "this landing page / workflow / screenshot / spec" --target "extract pattern and improve"
```

If arguments are vague, infer a reasonable target from the current project context and proceed. Ask only when a missing constraint would materially change the result.

---

## Prime directive

Given any source artifact, produce a better, cleaner, legally safe, Yuri-compatible version by following this chain:

```text
observe -> decompose -> audit -> abstract -> enrich -> redesign -> implement/plan -> validate -> document
```

The final outcome must be more useful than the original. The user wants the "rough blueprint" refined into a diamond.

---

## Non-negotiable boundaries

### Legal and ethical gate

Before extracting or rebuilding anything, classify the source:

- **Permissive / open source:** Respect license terms, attribution, notices, and dependency obligations.
- **Restrictive / unclear license:** Do not copy code, text, assets, or unique expression. Create a clean-room conceptual spec and original implementation plan.
- **Proprietary / private:** Only analyze if the user has authorization. Do not reproduce protected material beyond what is necessary for critique.
- **Generated / mixed sources:** Treat license as uncertain unless proven otherwise.

Always preserve attribution requirements. If the source is not safely reusable, say so and continue with a clean-room reconstruction.

### Security gate

Treat every external artifact as hostile until inspected.

Never run install scripts, package lifecycle hooks, downloaded binaries, migration scripts, shell scripts, or networked commands without first explaining the risk and inspecting the relevant files.

Prefer static analysis first:

```text
read files -> inspect manifests -> inspect scripts -> inspect permissions -> inspect network behavior -> then run safe commands
```

If execution is needed, prefer a sandbox, temporary clone, isolated environment, disabled lifecycle hooks, and read-only inspection.

### Non-destructive operation

Never overwrite the user's system directly as a first move.

Use this order:

1. Inspect current workspace.
2. Check git status if available.
3. Create a plan.
4. Create a branch, patch directory, or separate output folder.
5. Apply changes in small reversible steps.
6. Show diffs or artifact summaries before declaring success.

If no git repository exists, create a working folder:

```text
.sharingan/<source-name>/<timestamp>/
```

For YURI projects, prefer:

```text
<YURI_ROOT>/.sharingan/<source-name>/<timestamp>/
```

---

## Source intake protocol

Identify the source type and choose the correct ingestion path.

### GitHub repo or local codebase

Collect:

- README and docs
- license
- package manifests
- dependency graph
- file tree
- architecture entry points
- tests
- CI/CD files
- build scripts
- security-sensitive files
- examples and demos
- issue patterns if available
- public API surface

**For local codebases in YURI:** Run GitNexus tools first (before grep):
- `gitnexus_query({query: "architecture"})` — get execution flows
- `gitnexus_context({name: "symbolName"})` — get callers/callees
- `gitnexus_impact({target: "functionName", direction: "upstream"})` — understand blast radius

Do not judge from README alone. Many repos market well but fail structurally.

### Documentation, specs, papers, PDFs, markdown, Notion exports

Collect:

- table of contents
- claims
- definitions
- methods
- diagrams/tables
- assumptions
- implementation steps
- missing operational details
- contradictions
- unstated dependencies
- reusable conceptual patterns

Turn dense documents into an actionable engineering blueprint.

### Screenshots, UI, product pages, workflows

Collect:

- visible structure
- hierarchy
- interaction pattern
- information architecture
- UX intent
- likely backend assumptions
- design tokens if inferable
- conversion / usability logic
- accessibility risks
- missing states

Do not copy visuals directly. Extract design principles and rebuild original components.

### Datasets, schemas, configs, logs

Collect:

- schema
- field semantics
- data quality issues
- missing values
- edge cases
- validation rules
- privacy/security concerns
- transformation opportunities
- automatable workflows

### Prompts, agents, skills, workflows

Collect:

- role framing
- trigger conditions
- operating loop
- tool assumptions
- guardrails
- memory behavior
- failure handling
- output contracts
- evaluation method

Then harden it into a reusable, testable system component.

---

## Sharingan execution phases

### Phase 0: Activation brief

Start every run with a compact brief:

```markdown
## Sharingan Activation Brief
- Source:
- Source type:
- Target outcome:
- Reuse status:
- Risk level:
- Workspace impact:
- Planned output artifacts:
```

If the source cannot be accessed, state exactly what is missing and continue with any available material.

---

### Phase 1: Observe

Create a source map.

For repos, include:

```markdown
## Source Map
- Purpose:
- Main entry points:
- Core modules:
- Data flow:
- External dependencies:
- Build/test commands:
- Documentation quality:
- License:
- First suspicious signals:
```

For non-code artifacts, include:

```markdown
## Source Map
- Artifact type:
- Core idea:
- Structural sections:
- Key claims or patterns:
- Inputs and outputs:
- Hidden assumptions:
- Reusable techniques:
- First suspicious signals:
```

---

### Phase 2: Copy-eye decomposition

Extract the underlying technique. Separate surface from mechanism.

Use this table:

```markdown
| Layer | What the source does | Why it works | What is reusable | What must not be copied |
|---|---|---|---|---|
| Surface |  |  |  |  |
| Workflow |  |  |  |  |
| Architecture |  |  |  |  |
| Data model |  |  |  |  |
| Interface |  |  |  |  |
| Execution logic |  |  |  |  |
| Evaluation |  |  |  |  |
```

The "technique" is usually not the code. It is the repeatable strategy underneath the code.

---

### Phase 3: Weakness and gap audit

Be ruthless but fair. Do not assume something is bad just because it is simple. Simplicity is only a weakness when it blocks correctness, safety, scale, or maintainability.

Audit categories:

```markdown
## Weakness Audit
| Category | Finding | Evidence | Severity | Fix direction |
|---|---|---:|---|---|
| Architecture |  |  |  |  |
| Security |  |  |  |  |
| Reliability |  |  |  |  |
| Performance |  |  |  |  |
| Data model |  |  |  |  |
| UX/DX |  |  |  |  |
| Testing |  |  |  |  |
| Documentation |  |  |  |  |
| Maintainability |  |  |  |  |
| Yuri/Yuri fit |  |  |  |  |
```

Look specifically for:

- missing tests
- fragile abstractions
- unclear data ownership
- weak error handling
- implicit global state
- hardcoded paths/secrets
- unsafe shell execution
- dependency bloat
- poor observability
- no rollback strategy
- no migration path
- README claims not backed by code
- unhandled edge cases
- unclear license posture
- poor extensibility
- no self-improvement loop
- weak agent/tool permissions
- prompt injection exposure
- lack of deterministic validation

---

### Phase 4: Abstract into clean-room blueprint

Create a license-safe blueprint that captures the mechanism without copying protected expression.

```markdown
## Clean-Room Blueprint
- Problem solved:
- Core technique:
- Required inputs:
- Required outputs:
- Minimal viable architecture:
- Ideal architecture:
- Data contracts:
- Control flow:
- Required tools:
- Failure modes:
- Validation strategy:
- Extension points:
```

For repo-inspired builds, describe new modules and interfaces using original names, unless the source license clearly permits reuse and reuse is intentional.

---

### Phase 5: Yuri OS / Yuri enrichment

Refine the blueprint through Yuri/Yuri standards.

Apply these lenses:

- **Symbiotic integration:** Can this enhance an existing OS without replacing it?
- **Non-destructive injection:** Can it be added without breaking current workflows?
- **Self-improvement:** Does it produce session reports, failure logs, and improvement suggestions?
- **Memory compatibility:** Can outputs become semantic, procedural, or episodic memory?
- **Agent compatibility:** Can it be decomposed into orchestrator/subagent roles?
- **Cybersecurity:** Are tool permissions, sandboxing, secrets, and network access controlled?
- **Observability:** Can every important action be logged, replayed, and audited?
- **Modularity:** Can parts be swapped without rewriting the system?
- **Recovery:** Can failed runs roll back safely?
- **Enterprise readiness:** Are docs, tests, versioning, and governance present?

Output:

```markdown
## Yuri/Yuri Enhancement Matrix
| Standard | Current source | Required upgrade | Implementation note |
|---|---|---|---|
| Symbiotic integration |  |  |  |
| Non-destructive injection |  |  |  |
| Self-improvement loop |  |  |  |
| Memory compatibility |  |  |  |
| Agent orchestration |  |  |  |
| Security posture |  |  |  |
| Observability |  |  |  |
| Modularity |  |  |  |
| Recovery |  |  |  |
| Enterprise readiness |  |  |  |
```

---

### Phase 6: Diamond design

Create the improved version.

```markdown
## Diamond Design
- Name:
- Purpose:
- Operating principle:
- Architecture:
- Components:
- Data model:
- Interfaces:
- Workflow:
- Tooling:
- Security model:
- Test strategy:
- Documentation strategy:
- Migration/adoption path:
```

The design must be more precise than the source. If the source is a repo, include a target file tree. If the source is documentation, include a target implementation map. If the source is a UI/workflow, include user journeys and state handling.

---

### Phase 7: Implementation plan

Build a step-by-step execution plan.

```markdown
## Implementation Plan
### Stage 1: Safe setup
- [ ] Create branch or output directory
- [ ] Preserve source snapshot
- [ ] Record license and attribution status
- [ ] Define target artifacts

### Stage 2: Extraction
- [ ] Map source structure
- [ ] Extract reusable mechanisms
- [ ] Identify non-reusable expression
- [ ] Write clean-room blueprint

### Stage 3: Redesign
- [ ] Define Yuri/Yuri fit
- [ ] Define modules and interfaces
- [ ] Define validation gates
- [ ] Define rollout plan

### Stage 4: Build
- [ ] Implement smallest useful core
- [ ] Add tests
- [ ] Add docs
- [ ] Add examples
- [ ] Add observability

### Stage 5: Harden
- [ ] Security review
- [ ] Failure-mode review
- [ ] Dependency review
- [ ] Performance sanity check
- [ ] Edge-case pass

### Stage 6: Handoff
- [ ] Produce final report
- [ ] Produce next actions
- [ ] Produce memory/update notes
```

If the user asked for actual implementation, execute this plan instead of only describing it. Keep edits small and reversible.

**For large repos (>50 files) with parallelizable phases:** Use `@swarm` fan-out coordination. Delegate Phase 2 decomposition and Phase 3 audits to parallel workers; main thread orchestrates and synthesizes.

---

### Phase 8: Validation

Validate with evidence.

For code:

- run tests if safe
- run lint/typecheck if available
- inspect diff
- check dependency/license changes
- test happy path
- test one failure path
- document anything not run

For docs/specs:

- check internal consistency
- check missing assumptions
- verify implementation path exists
- convert vague claims into requirements
- mark open questions

For workflows/UI:

- check core user journey
- check empty/loading/error states
- check accessibility
- check edge cases
- define measurable success criteria

Output:

```markdown
## Validation Report
| Check | Result | Evidence | Notes |
|---|---|---|---|
| License safety |  |  |  |
| Source coverage |  |  |  |
| Blueprint completeness |  |  |  |
| Security |  |  |  |
| Tests/verification |  |  |  |
| Yuri/Yuri fit |  |  |  |
```

---

### Phase 9: Handoff artifacts

Always finish with these sections:

```markdown
## Final Handoff
### What was copied as technique
### What was rejected
### What was improved
### What was created
### What still needs review
### Recommended next command
```

If files were created or edited, list them.

If implementation was not possible because source access was missing, produce a complete plan and state what artifact the user should provide next.

---

## Ecosystem integration

### Model routing
- **Analysis + Architecture + Security (Phases 3, 5, 6):** Sonnet 4.6 with extended thinking
- **Extraction + Inventory (Phase 1, early Phase 2):** Haiku 4.5 or local-subagent (Deepseek/Qwen)
- **Deterministic work (grep, manifest scan, file parsing):** local-subagent (ollama-bridge MCP)
- **Large parallel work (>50 files, Phase 2 decomposition):** Swarm fan-out via `@swarm` coordination

### Tokenmaxxing awareness
When `/sharingan` is invoked with tokenmaxxing active:
- Main thread = overseer + orchestrator only
- Delegate extraction → local-subagent
- Delegate analysis → cloud Agent (Sonnet 4.6)
- Return control to main thread after each phase
- Use background agents for long-running validation

### Memory output
Analysis results can be captured as project memories:
- **Type: project** — source overview, architectural findings, key techniques
- **Type: reference** — link to external source repo, doc, or resource
- **Type: feedback** — lessons about common weakness patterns in this artifact class

### End-of-transmission integration
After Phase 9 completion, a micro-EOT checkpoint is auto-triggered (if enabled via SessionStart hook). This logs findings, validates evidence, and updates session memory.

---

## Output discipline

Prefer useful artifacts over long commentary.

Use direct labels:

- `SOURCE_MAP.md`
- `WEAKNESS_AUDIT.md`
- `CLEAN_ROOM_BLUEPRINT.md`
- `YURI_ENHANCEMENT_MATRIX.md`
- `DIAMOND_DESIGN.md`
- `IMPLEMENTATION_PLAN.md`
- `VALIDATION_REPORT.md`

For small tasks, combine them into one `SHARINGAN_REPORT.md`.

For large tasks, create a folder:

```text
.sharingan/<target-name>/
├── 00_activation_brief.md
├── 01_source_map.md
├── 02_weakness_audit.md
├── 03_clean_room_blueprint.md
├── 04_yuri_enhancement_matrix.md
├── 05_diamond_design.md
├── 06_implementation_plan.md
├── 07_validation_report.md
└── 08_handoff.md
```

---

## Non-negotiable execution rules

When invoking this skill:

1. **Classify the source first** — legal/ethical/security gates before any deep analysis.
2. **Static analysis first** — read files, inspect manifests, before running any code.
3. **Plan before build** — always produce Phase 7 (Implementation Plan) before Phase 4 (Build).
4. **Show your work** — audit tables, decomposition matrices, validation evidence. Do not hide reasoning.
5. **Preserve attribution** — if reusing licensed material, say so and respect terms.
6. **No blindly cloning** — technique only, never property.
7. **Delegate deterministic work** — grep, file reads, manifest parsing → local-subagent.
8. **Escalate analysis** — Phase 3 audits, Phase 5 design → Sonnet 4.6 with reasoning.

---

## Failure behavior

If blocked, do not stop at "I can't."

Return:

```markdown
## Blocker
- What failed:
- Why it matters:
- What I could still inspect:
- Best partial result:
- What is needed next:
- Safe next command:
```

If a source is low quality, say so clearly and show why. The goal is not to worship the source. The goal is to surpass it.

---

## Final rule

Every run must end with something the user can execute, inspect, or inject:

- a patch
- a file tree
- a markdown report
- a clean-room spec
- an implementation checklist
- a Claude Code prompt
- a test plan
- or a next command

Do not finish with vague advice.

---

## Session Notes

### 2026-06-10
- session: 847m | peak ctx: 62% | compacts: 1
- tools: Bash×776, Read×365, Edit×55, Write×27, StructuredOutput×12, TodoWrite×11, WebFetch×9, Agent×7, Workflow×3, ToolSearch×2
- corrections: none
- errors: none

### 2026-06-09
- session: 106m | peak ctx: 55% | compacts: 0
- tools: Bash×114, Read×104, Edit×40, WebFetch×9, Agent×6, Write×6, TodoWrite×4, ToolSearch×2
- corrections: none
- errors: none

### 2026-05-29
- session: 739m | peak ctx: 99% | compacts: 14 (mid-session)
- tools: Bash×423, Read×235, WebSearch×219, Edit×157, WebFetch×148, StructuredOutput×135, ToolSearch×108, Write×21, TodoWrite×12, Workflow×6, AskUserQuestion×4, Skill×1
- corrections: none
- errors: none

### 2026-04-27
- session: 6m | peak ctx: 53% | compacts: 0
- tools: Read×27, Bash×8, Write×2, mcp×1
- corrections: none
- errors: none

### 2026-04-26
- session: 4m | peak ctx: 53% | compacts: 0
- tools: Bash×18, Read×6, Agent×4, Skill×2
- corrections: none
- errors: none
