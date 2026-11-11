---
name: pair-process-bootstrap
description: "Orchestrates full project setup: PRD verification, project categorization, checklist completion, standards generation, quality gate setup, and PM tool configuration. Composes /pair-process-specify-prd, /pair-capability-setup-pm, /pair-capability-record-decision, and assess-* (optional). Idempotent — detects completed phases and resumes."
version: 0.4.1
author: Foomakers
---

# /pair-process-bootstrap — Project Bootstrap

Orchestrate the complete project setup sequence. Transforms a PRD into a fully configured project with adopted standards, quality gates, and PM tool integration. Each phase checks output existence before acting — re-invocation resumes from the first incomplete phase.

## Process Profile

<!-- process-step: id=bootstrap -->

Executable form of the **`bootstrap`** step, and a composer of `specify-prd`, `define-subdomains`, `define-bounded-contexts`. A **direct** invocation while a step is disabled by the project's profile warns and asks for confirmation; a **composed** one never prompts — it degrades exactly as a step that is not installed. No section ⇒ no-op. See [process-profile gate](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/process-profile-gate.md).

## Composed Skills

| Skill                   | Type       | Required                                                                      |
| ----------------------- | ---------- | ----------------------------------------------------------------------------- |
| `/pair-process-specify-prd`          | Process    | Yes — invoked if PRD is missing or template                                   |
| `/pair-capability-setup-pm`             | Capability | Yes — invoked in finalization phase for PM tool configuration                 |
| `/pair-capability-record-decision`      | Capability | Yes — invoked for each bootstrap decision (categorization, tech choices, etc) |
| `/pair-capability-assess-architecture`  | Capability | Optional — architecture pattern assessment. Graceful degradation if absent.   |
| `/pair-capability-assess-stack`         | Capability | Optional — tech stack assessment (core sections). Graceful degradation if absent. |
| `/pair-capability-assess-testing`       | Capability | Optional — testing strategy assessment. Graceful degradation if absent.       |
| `/pair-capability-assess-infrastructure`| Capability | Optional — infrastructure assessment. Graceful degradation if absent.         |
| `/pair-capability-assess-observability` | Capability | Optional — observability assessment. Graceful degradation if absent.          |
| `/pair-capability-assess-methodology`   | Capability | Optional — methodology assessment. Graceful degradation if absent.            |
| `/pair-capability-assess-pm`            | Capability | Optional — PM tool assessment (delegates to /pair-capability-setup-pm). Graceful degradation if absent. |
| `/pair-capability-assess-ai`            | Capability | Optional — AI development tools assessment. Graceful degradation if absent.   |

## Phase 0: PRD Verification (BLOCKING)

### Step 0.1: Check PRD State

1. **Check**: Does [adoption/product/PRD.md](../../../.pair/adoption/product/PRD.md) exist and is it populated (not a template)?
   - A file is a template if it contains `[Product/feature name]` or `[Creation date]`.
2. **Skip** (populated PRD): Extract project name and key constraints. Move to Phase 1.
3. **Act** (missing or template): Compose `/pair-process-specify-prd`.
   - Wait for PRD approval before proceeding.
4. **Verify**: PRD exists and is populated. If not → **HALT**.

### Step 0.2: Extract Key Constraints from PRD

1. **Act**: Read PRD and extract:
   - Target users and scale expectations
   - Budget and timeline constraints
   - Team size and technical skills
   - Compliance and integration requirements
   - Key features (P0/P1/P2)
2. **Verify**: Key constraints documented in session state.

## Phase 1: Project Categorization

### Step 1.1: Check Existing Categorization

1. **Check**: Does [adoption/decision-log/](../../../.pair/adoption/decision-log) contain a `*-project-categorization.md` file?
2. **Skip**: If categorization already recorded, read it and move to Phase 2.
3. **Act**: Proceed to categorization analysis.

### Step 1.2: Categorize Project

1. **Act**: Evaluate project indicators from PRD:
   - Team size and budget constraints
   - Scale expectations and performance needs
   - Compliance and integration complexity
   - Timeline pressures and market requirements

2. **Act**: Present categorization with evidence:

   > Based on PRD analysis, this project fits **[Type X]** categorization:
   > - **Type A (Pet/PoC)**: Small team (1-3), minimal budget, single user or small group, no compliance, fast iteration
   > - **Type B (Startup/Scale-up)**: Growing team (3-15), moderate budget, scaling users, some integrations, rapid growth
   > - **Type C (Enterprise)**: Large team (15+), significant budget, many users, compliance requirements, complex integrations
   >
   > Evidence: [specific PRD indicators]
   >
   > Does this categorization match your project?

3. **Act**: On confirmation, compose `/pair-capability-record-decision`:
   - `$type`: `non-architectural`
   - `$topic`: `project-categorization`
   - `$summary`: "Project categorized as Type [X] — [category name]"

4. **Verify**: Categorization decision recorded.

## Phase 2: Checklist Completion

### Step 2.1: Check Existing Adoption Files

1. **Check**: Scan [adoption/tech/](../../../.pair/adoption/tech) for existing files. Classify each as populated or template:
   - `architecture.md`
   - `tech-stack.md`
   - `infrastructure.md` (optional — not all project types need it)
   - `ux-ui.md` (optional — not all project types need it)
   - `way-of-working.md`

2. **Skip**: Files that are already populated — do not re-generate.
3. **Act**: Build a checklist of missing or template files to complete.

### Step 2.2: Assessment Phase (Optional)

1. **Check**: Are assess-\* skills installed? Scan installed skills directory for `assess-*` skills.
2. **Act** (installed): Compose assess-\* skills in recommended sequence. Each skill checks its own adoption file first — already-decided domains are skipped automatically (resolution cascade).

   **Recommended sequence** (respects adoption file dependencies):
   1. `/pair-capability-assess-architecture` → writes `architecture.md` (needed by stack and infrastructure)
   2. `/pair-capability-assess-stack` → writes core sections of `tech-stack.md` (needed by testing and AI)
   3. `/pair-capability-assess-testing` → writes testing section of `tech-stack.md`
   4. `/pair-capability-assess-ai` → writes AI section of `tech-stack.md`
   5. `/pair-capability-assess-infrastructure` → writes `infrastructure.md` (needed by observability)
   6. `/pair-capability-assess-observability` → writes observability section of `infrastructure.md`
   7. `/pair-capability-assess-methodology` → writes methodology section of `way-of-working.md`
   8. `/pair-capability-assess-pm` → writes PM section of `way-of-working.md` (delegates to `/pair-capability-setup-pm`)

   **Section ownership** (prevents parallel write conflicts):

   | Adoption File        | Section            | Owner Skill            |
   | -------------------- | ------------------ | ---------------------- |
   | `architecture.md`    | Full file          | `/pair-capability-assess-architecture` |
   | `tech-stack.md`      | Core sections      | `/pair-capability-assess-stack`        |
   | `tech-stack.md`      | Testing section    | `/pair-capability-assess-testing`      |
   | `tech-stack.md`      | AI section         | `/pair-capability-assess-ai`           |
   | `infrastructure.md`  | Core sections      | `/pair-capability-assess-infrastructure` |
   | `infrastructure.md`  | Observability      | `/pair-capability-assess-observability`|
   | `way-of-working.md`  | Methodology        | `/pair-capability-assess-methodology`  |
   | `way-of-working.md`  | PM tool            | `/pair-capability-assess-pm`           |
   | `way-of-working.md`  | Quality gates      | `/pair-process-bootstrap` (Step 3.2)|

   **Parallel safety**: Skills writing different adoption files can run in parallel. Skills writing different sections of the same file are safe if each respects section ownership. The recommended sequence avoids any conflicts.

   **Partial installation**: If only some assess-\* skills are installed, compose those and skip the rest with a warning. Each assess-\* skill is independent — partial installation is supported.

3. **Act** (not installed): Warn and proceed with manual assessment:

   > assess-\* skills are not yet installed. Proceeding with manual assessment.
   > For each technical area, I'll reference the guidelines and ask you to make decisions directly.

4. **Verify**: Assessment data collected (via skills or manually). All adoption files written by assess-\* skills are consistent.

### Step 2.3: Gather Information per Section

For each missing adoption file, work through the relevant checklist section. Reference the [Bootstrap Checklist](../../../.pair/knowledge/assets/bootstrap-checklist.md) for section-specific questions.

1. **Architecture** — scale, integrations, compliance, patterns
   - Reference: [Architecture Guidelines](../../../.pair/knowledge/guidelines/architecture/README.md)

2. **Tech Stack** — languages, frameworks, libraries with versions
   - Reference: [Technical Standards](../../../.pair/knowledge/guidelines/technical-standards/README.md)

3. **Infrastructure** — deployment, CI/CD, monitoring, environments
   - Reference: [Infrastructure Guidelines](../../../.pair/knowledge/guidelines/infrastructure/README.md)

4. **UX/UI** — design system, accessibility, device support
   - Reference: [UX Guidelines](../../../.pair/knowledge/guidelines/user-experience/README.md)

5. **Way of Working** — processes, quality gates, release cycles
   - Reference: [Collaboration Guidelines](../../../.pair/knowledge/guidelines/collaboration/README.md)

**Rules**:

- Ask 3-4 focused questions per section
- Wait for developer responses before proceeding
- Record each significant decision via `/pair-capability-record-decision` (`non-architectural` → ADL, `architectural` → ADR)

## Phase 3: Standards Generation

### Step 3.1: Generate Adoption Documents

For each missing adoption file (in order: architecture → tech-stack → infrastructure → ux-ui → way-of-working):

1. **Check**: Is this file already populated? If yes, skip.
2. **Act**: Generate the document following:
   - [Adopted Standards format](../../../.pair/adoption/tech/README.md) (if format guide exists)
   - Concise, prescriptive English
   - Specific versions and configuration details
   - References to KB guidelines for detailed rationale
3. **Act**: Present key decisions with rationale for developer review.
4. **Act**: Iterate on feedback until approved.
5. **Act**: Save to [adoption/tech/](../../../.pair/adoption/tech)`<filename>.md`.
6. **Verify**: File written, consistent with other adoption files.

### Step 3.2: Quality Gate Setup

1. **Check**: Does [adoption/tech/way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) already contain a Custom Gate Registry with entries?
2. **Skip**: If quality gates already configured, move to Phase 4.
3. **Act**: Ask the developer:

   > **Quality gate setup:**
   > The standard pipeline includes: type checking, testing, linting, formatting.
   >
   > Do you want custom quality gates beyond the standard pipeline?
   > Examples: security scanning, bundle size checks, smoke tests, accessibility audits.
   >
   > If yes, describe the additional gates. If no, I'll configure the standard pipeline only.

4. **Act**: For each quality gate (standard + custom):
   - Add entry to the Custom Gate Registry in `way-of-working.md` with: Order, Gate name, Command, Scope Key, Required flag, Description
   - Create placeholder script entries (in `package.json` scripts or technology-specific equivalent) so the gate infrastructure is executable from day one

5. **Act**: Record quality gate decisions via `/pair-capability-record-decision`:
   - `$type`: `non-architectural`
   - `$topic`: `quality-gate-setup`

6. **Verify**: Quality gates documented in way-of-working and placeholder scripts exist.

## Phase 4: Finalization

### Step 4.1: Consistency Verification

1. **Act**: Re-read all adoption files:
   - [architecture.md](../../../.pair/adoption/tech/architecture.md)
   - [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md)
   - [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md)
   - infrastructure.md and ux-ui.md (if generated)
2. **Act**: Verify cross-document consistency:
   - Tech stack versions match architecture references
   - Way-of-working references correct tools from tech-stack
   - Infrastructure aligns with architecture patterns
3. **Act**: Fix any inconsistencies found.
4. **Verify**: All documents are internally and cross-referentially consistent.

### Step 4.2: PM Tool Configuration

1. **Check**: Is PM tool already configured in way-of-working.md?
2. **Skip**: If configured, confirm and move to Step 4.3.
3. **Act**: Compose `/pair-capability-setup-pm`. The skill handles tool selection, configuration, and ADL recording.
4. **Verify**: PM tool configured and recorded.

### Step 4.3: Final Summary

1. **Act**: Present bootstrap completion summary to the developer for final approval:

   > **Bootstrap complete.** All adoption files generated and approved.
   > Review the summary below and confirm everything is correct.

2. **Verify**: Developer approves. If not → iterate on specific concerns.

## Output Format

```text
BOOTSTRAP COMPLETE:
├── PRD:             [verified | created via /pair-process-specify-prd]
├── Categorization:  [Type A | Type B | Type C] — [ADL path]
├── Adoption Files:
│   ├── architecture.md:    [generated | existing | skipped]
│   ├── tech-stack.md:      [generated | existing | skipped]
│   ├── infrastructure.md:  [generated | existing | skipped | n/a]
│   ├── ux-ui.md:           [generated | existing | skipped | n/a]
│   └── way-of-working.md:  [generated | existing | skipped]
├── Quality Gates:   [N gates configured — standard + custom]
├── PM Tool:         [configured via /pair-capability-setup-pm | already configured]
├── Decisions:       [N decisions recorded (ADR: X, ADL: Y)]
└── Status:          [Complete | Partial — details]
```

## HALT Conditions

- **PRD missing or template and /pair-process-specify-prd fails** (Phase 0) — cannot bootstrap without product context
- **Project categorization rejected** (Phase 1) — developer must confirm before technical decisions
- **Critical technical decision unresolved** (Phase 2) — cannot generate adoption files with gaps
- **Adoption file generation rejected** (Phase 3) — each document needs developer approval

On HALT: report the blocker clearly, propose resolution, wait for developer.

## Idempotent Re-invocation

Re-invoking `/pair-process-bootstrap` on a partially completed project is safe and expected:

1. **PRD**: detects existing populated PRD, skips Phase 0.
2. **Categorization**: detects existing ADL entry for `project-categorization`, skips Phase 1.
3. **Adoption files**: checks each file individually — only generates missing/template files.
4. **Quality gates**: detects existing Custom Gate Registry entries, skips Step 3.2.
5. **PM tool**: detects existing configuration in way-of-working, confirms and skips.
6. **Decisions**: existing ADL/ADR entries are not re-created.

Phase completion is detected via output file existence — never re-does completed work.

## Graceful Degradation

- **assess-\* skills not installed**: Skip assessment phase, reference guideline files directly, ask developer for manual decisions. Log: "assess-\* skills not installed — using manual assessment."
- **/specify-prd not installed**: HALT at Phase 0 if PRD is missing. Suggest creating PRD manually using how-to-01.
- **/setup-pm not installed**: Skip PM configuration in Phase 4. Warn: "PM tool not configured — /pair-capability-setup-pm not installed."
- **/record-decision not installed**: Skip decision recording. Warn: "Decisions not recorded — /pair-capability-record-decision not installed. Document decisions manually in adoption files."
- **Bootstrap checklist asset not found**: Use Phase 2 section questions as fallback — they cover the same areas.
- **Adoption directory doesn't exist**: Create `adoption/tech/` and `adoption/decision-log/` on first write.

## Notes

- This is the most complex process skill — it orchestrates the full project setup sequence.
- Each phase is independent: completion of one phase doesn't require re-running previous phases.
- The developer can stop between phases. Re-invoke to resume (idempotency ensures correct state).
- All decisions during bootstrap are recorded via `/pair-capability-record-decision`. Non-architectural → ADL. Architectural → ADR.
- Quality gate setup ensures the gate infrastructure is executable from day one (not deferred to first implementation).
- Content source: how-to-02 Phases 0-4. How-to-02 retains orchestration flow, this skill has operational detail.
