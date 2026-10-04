---
name: prd
description: "Generate a structured PRD from a WCP work item brief. Reads the work item body as input, produces a pipeline-ready PRD attached as a WCP artifact."
argument-hint: "<callsign>"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - mcp__wcp__wcp_get
  - mcp__wcp__wcp_get_artifact
  - mcp__wcp__wcp_attach
  - mcp__wcp__wcp_comment
---

# Stage 0 — PRD Generation

You **generate a structured PRD** from raw input (feature descriptions, Slack threads, meeting notes, Google Doc exports, etc.) that conforms to the pipeline's PRD template. The human reviews and edits the output before it enters the pipeline — Stage 0 assists, not replaces.

## Inputs

- `$ARGUMENTS` — a WCP callsign (e.g., `SN-3`) identifying the work item whose body contains the brief
- The conventions file (`CLAUDE.md`, `AGENTS.md`, or `CONVENTIONS.md` in the repo root) — pipeline configuration, framework, platforms, directory structure

## Step-by-Step Procedure

### Step 0: Capture Start Time

Run this command via Bash and save the result as STARTED_AT:

```bash
date +"%Y-%m-%dT%H:%M:%S%z"
```

You will use this timestamp in the output frontmatter.

### Step 1: Read Conventions File and Work Item

Locate the **conventions file** in the current repo root — look for `CLAUDE.md`, `AGENTS.md`, or `CONVENTIONS.md` (use the first one found). Read it in full.

From the `## Pipeline Configuration` section, extract:
- **Repository Details** (default branch, test command, branch prefix, etc.)
- All other pipeline config sub-sections (Framework & Stack, Platforms, Directory Structure, etc.)

Then read the WCP work item:

```
wcp_get($ARGUMENTS)
```

The work item's **body** is the raw input brief. If the body is empty or missing, **STOP**:

> "Work item `$ARGUMENTS` has no body/description. Add your raw notes, feature description, or brief to the work item body first, then re-run `/prd $ARGUMENTS`."

### Step 2: Validate

Check whether a PRD already exists for this work item:

```
wcp_get_artifact($ARGUMENTS, "prd.md")
```

- If a `prd.md` artifact already exists → **STOP**:
  > "Work item `$ARGUMENTS` already has a PRD attached. To regenerate, remove the existing prd.md artifact first."
- If no artifact exists → proceed.

### Step 3: Read Context

You already read the conventions file in Step 1. Review the Pipeline Configuration sections for framework, platforms, directory structure, API conventions, and security model.

### Step 4: Generate PRD

Analyze the raw input (work item body) and produce a structured PRD that follows the template. The PRD must include ALL sections from the template — never omit a section. For sections where the raw input provides insufficient information, include the section with placeholder markers.

#### Header

Generate a metadata table at the top of the PRD:

```markdown
# [Feature Name] — PRD

|  |  |
| -- | -- |
| **Product** | [Product name from Pipeline Configuration or raw input] |
| **Version** | 1 |
| **Author** | Stage 0 (Pipeline) |
| **Date** | [Today's date] |
| **Status** | Draft — Review Required |
| **Platforms** | [CONFIRM — suggest based on scope: "Web only", "Web + API", "All platforms"] |
| **Level** | [CONFIRM — suggest 1, 2, or 3 based on scope] |
```

Level guidance — read the Platforms table in Pipeline Configuration to determine which definition set applies:

**If Pipeline Configuration → Platforms lists only ONE active platform:**
- **Level 1** — Small, self-contained changes. Config tweaks, simple UI additions, backend-only adjustments. 1-2 files.
- **Level 2** — Medium scope features. New pages, reports, workflows, settings. Multiple files, one milestone.
- **Level 3** — Large scope features. Significant new capability, multiple milestones.

**If Pipeline Configuration → Platforms lists MULTIPLE active platforms:**
- **Level 1** — Small, single-platform only.
- **Level 2** — Primary platform only (web). New pages, reports, workflows, settings. May involve model + controller + views but stays within one platform.
- **Level 3** — Cross-platform features. Requires coordinated changes across all active platforms. New API endpoints consumed by other platform clients.

#### Section-by-Section Rules

For each section, follow these rules:

**§1 Executive Summary** — Always generate. Synthesize What, Why, and Key Design Principles from the raw input. If the "why" isn't clear, mark: `[NEEDS INPUT — why is this being built?]`

**§2 Goals & Success Metrics** — Extract goals from the raw input. If no metrics are specified, suggest reasonable defaults and mark `[NEEDS REVIEW]`.

**§3 Feature Requirements** — This is the most critical section.
- Extract every requirement from the raw input
- Assign IDs using section-appropriate prefixes (e.g., `ENT-001` for entry/entity, `CFG-001` for configuration, `RPT-001` for reporting, `VAL-001` for validation, `SEC-001` for security, `UI-001` for UI)
- Organize into functional area subsections
- Each requirement must be specific and testable — rewrite vague input into testable statements
- Set Platform based on the suggested Level
- Set Priority: Must (core functionality), Should (important but not blocking), Nice (enhancement)

**§4 Platform-Specific Requirements** — Based on the suggested Level:
- Level 1/2: Fill Web section, mark iOS/Android as "No changes required — Level [N] project"
- Level 3: Attempt to break out requirements per platform from the raw input

**§5 User Flows** — Generate step-by-step user flows from the raw input. If the raw input describes workflows or user interactions, formalize them. If it doesn't, generate reasonable default flows based on the requirements and mark `[NEEDS REVIEW — generated from requirements, verify accuracy]`.

**§6 UI Mockups / Wireframes** — If the feature is UI-heavy, generate ASCII mockups based on descriptions in the raw input. If the feature is backend-only or the raw input doesn't describe UI, write "N/A — backend changes only" or "No mockups provided in source material. Add wireframes or ASCII mockups here if needed."

**§7 Backwards Compatibility** — Include the compatibility matrix if Level 3 or if the raw input mentions API changes. For Level 1/2 web-only features with no API changes, write "N/A — no API or client-facing changes."

**§8 Edge Cases & Business Rules** — Extract from the raw input. Also infer additional edge cases based on the feature type (e.g., empty states, permission boundaries, concurrent access, data limits). Mark inferred cases with `[INFERRED]`.

**§9 Export Requirements** — Include if the feature involves reports, exports, or data output. Otherwise "N/A."

**§10 Out of Scope** — Extract explicit non-goals from the raw input. If the raw input doesn't specify, add `[DEFINE — what is explicitly NOT being built in this version?]`.

**§11 Open Questions** — Collect anything ambiguous or unresolved from the raw input. Also add questions you identified while analyzing the input. Mark each as blocking or non-blocking. Include a final assessment: "Blocking questions remain — resolve before pipeline intake" or "No blocking questions — this PRD is ready for pipeline intake (after human review)."

**§12 Release Plan** — Default to single-phase rollout with a feature flag unless the raw input specifies otherwise. Suggest a feature flag name based on the work item title.

**§13 Assumptions** — List what's assumed to be true based on the raw input and project context.

**Appendix: Linked Documents** — Include links from the raw input. Add a row for the WCP work item.

#### Placeholder Markers

Use these markers consistently:

| Marker | Meaning |
|--------|---------|
| `[CONFIRM]` | Value suggested but needs human confirmation (e.g., Level, Platform) |
| `[NEEDS INPUT — ...]` | Section requires information not present in the raw input |
| `[NEEDS REVIEW]` | Content was generated/inferred and should be verified |
| `[INFERRED]` | Edge case or requirement inferred by the pipeline, not from raw input |
| `[DEFINE — ...]` | Section needs the human to define something specific |

### Step 5: Write Output

1. Capture the completion timestamp via Bash: `date +"%Y-%m-%dT%H:%M:%S%z"` — save as COMPLETED_AT.

2. Prepend YAML frontmatter to the generated PRD content:

```yaml
---
pipeline_stage: 0
pipeline_stage_name: prd
pipeline_project: "$ARGUMENTS"
pipeline_started_at: "<STARTED_AT>"
pipeline_completed_at: "<COMPLETED_AT>"
---
```

3. Attach the PRD to the work item:

```
wcp_attach(
  id=$ARGUMENTS,
  type="prd",
  title="PRD: [Feature Name]",
  filename="prd.md",
  content="[full PRD content with frontmatter]"
)
```

4. Log the completion:

```
wcp_comment(
  id=$ARGUMENTS,
  author="pipeline/prd",
  body="Stage 0 complete — PRD generated and attached as prd.md"
)
```

### Step 6: Report to User

Tell the user:

1. The PRD has been attached to work item `$ARGUMENTS` as `prd.md`
2. **Review is required** — this is a draft, not a final PRD
3. Search for these markers and resolve them:
   - `[CONFIRM]` — verify suggested values (especially Level and Platforms)
   - `[NEEDS INPUT]` — add missing information
   - `[NEEDS REVIEW]` — verify generated content is accurate
   - `[INFERRED]` — confirm inferred edge cases are valid
   - `[DEFINE]` — fill in missing definitions
4. Set Status from "Draft — Review Required" to "Ready for Engineering" when satisfied
5. Then run `/discovery $ARGUMENTS` to start the pipeline

## What NOT To Do

- **Do not run Stage 1.** Stage 0 only generates the PRD. The human reviews it first.
- **Do not skip sections.** Every template section must appear in the output, even if marked with placeholders.
- **Do not invent requirements.** Extract from the raw input or mark as `[NEEDS INPUT]`. Inferred edge cases are OK (marked `[INFERRED]`) but core requirements must come from the source material.
- **Do not set Status to "Ready for Engineering."** The PRD starts as "Draft — Review Required" — only the human promotes it.

---

## Output Template

The generated PRD must follow this structure. Use the section-by-section rules in Step 4 above to fill each section.

```markdown
---
pipeline_stage: 0
pipeline_stage_name: prd
pipeline_project: "[callsign]"
pipeline_started_at: "[ISO 8601 timestamp]"
pipeline_completed_at: "[ISO 8601 timestamp]"
---

# [Feature Name] - PRD

> **Status:** Draft | Review | Approved
> **Author:** [Name]
> **Date:** [Date]
> **Linear Project:** [Link]

---

## 1. Executive Summary

**What:** [1-2 sentences: what we're building]

**Why:** [Business driver: customer request, regulatory, business need, tech debt]

**Key Design Principles:**
- [Non-negotiable principle 1]
- [Non-negotiable principle 2]

---

## 2. Goals & Success Metrics

### Goals
- [Goal 1]
- [Goal 2]

### Success Metrics

| Metric | Target | Timeframe |
|--------|--------|-----------|
| [Metric 1] | [Target] | 30 days |
| [Metric 2] | [Target] | 60 days |
| [Metric 3] | [Target] | 90 days |

---

## 3. Feature Requirements

> Number every requirement with a prefix (e.g., SEC-001 for sections). Each requirement must be specific and testable.

### [Functional Area 1]

| ID | Requirement | Platform | Priority |
|----|------------|----------|----------|
| [XX-001] | [Specific, testable requirement] | [Platform from Pipeline Configuration] / All | Must / Should / Nice |
| [XX-002] | [Specific, testable requirement] | [Platform] | [Priority] |

### [Functional Area 2]

| ID | Requirement | Platform | Priority |
|----|------------|----------|----------|
| [XX-010] | [Specific, testable requirement] | [Platform] | [Priority] |

---

## 4. Platform-Specific Requirements

> Include one subsection per active platform from Pipeline Configuration → Platforms table.
> Mark platforms not in scope as "No changes required — Level [N] project."

### [Primary Platform from Pipeline Configuration]
- [Platform-specific requirements, UI expectations, workflows]

<!-- CONDITIONAL: Include one subsection per additional active platform from Pipeline Configuration → Platforms -->
### [Additional Platform]
- [Platform-specific requirements, UI patterns, device considerations]
- **Old app compatibility:** [What old versions see/don't see — if Pipeline Configuration has Backwards Compatibility section]

<!-- CONDITIONAL: Include only if Pipeline Configuration has API Conventions section -->
### API
- [API requirements that serve all platforms]
- [Authentication/authorization requirements]

---

## 5. User Flows

### Flow 1: [Flow Name]
**Persona:** [Who]
**Entry Point:** [Where they start]

1. [Step 1]
2. [Step 2]
3. [Step 3]
4. **Success:** [What happens when it works]
5. **Error:** [What happens when it fails]

### Flow 2: [Flow Name]
...

---

## 6. UI Mockups / Wireframes

> Include mockups, screenshots, ASCII layouts, or links to design files.

### [Screen/View Name]
` ` `
[ASCII mockup or description]
` ` `

---

## 7. Backwards Compatibility

<!-- CONDITIONAL: Include this section only if Pipeline Configuration has a Backwards Compatibility section.
     Otherwise write: "N/A — no backwards compatibility concerns for this project." -->

### Compatibility Matrix

| Feature | [Column per active platform and old version from Pipeline Configuration → Platforms] |
|---------|:---:|
| [Feature aspect 1] | [Full/Partial/None per platform] |

### Migration Strategy
- [How existing data transitions]
- [What happens to in-progress work]
- [Rollback plan if migration fails]

---

## 8. Edge Cases & Business Rules

| Scenario | Expected Behavior | Platform |
|----------|-------------------|----------|
| [Edge case 1] | [What should happen] | [Platform] |
| [Edge case 2] | [What should happen] | [Platform] |
| [What if user does X?] | [Defined behavior] | [Platform] |
| [What if data is in state Y?] | [Defined behavior] | [Platform] |

---

## 9. Export Requirements

| Export Type | Format | Changes | Backwards Compatible? |
|-------------|--------|---------|----------------------|
| [Report name] | PDF / Excel / CSV | [What changes] | Yes / No / N/A |

---

## 10. Out of Scope

> Explicitly list what we are NOT building. This prevents scope creep.

- [Deferred feature 1]
- [Deferred feature 2]
- [Explicitly excluded capability]

---

## 11. Open Questions

| # | Question | Status | Decision | Blocking? |
|---|----------|--------|----------|-----------|
| 1 | [Question] | Open / Resolved | [Decision if resolved] | Yes / No |
| 2 | [Question] | Open / Resolved | [Decision if resolved] | Yes / No |

> **All blocking questions must be resolved before this PRD enters the pipeline.**

---

## 12. Release Plan

### Phases

| Phase | What Ships | Flag | Audience |
|-------|-----------|------|----------|
| Phase 1 | [Scope] | Beta flag | Internal + select accounts |
| Phase 2 | [Scope] | GA flag | All accounts |

### Feature Flag Strategy
- Flag name: `[flag_name]`
- Rollout: [Per-account / percentage / global]
- Default: Off

---

## 13. Assumptions

> Things we're assuming are true. If false, the approach may need to change.

- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

---

## Appendix: Linked Documents

| Document | Link |
|----------|------|
| Framing Doc | [Link] |
| Linear Project | [Link] |
| Design Files | [Link] |
| Related PRDs | [Link] |
```
