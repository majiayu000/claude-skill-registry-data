---
name: architecture
description: "Run pipeline Stage 2 (Architecture) for a project. Designs data model, API endpoints, migrations, and security scoping based on Pipeline Configuration in the conventions file."
argument-hint: "<callsign>"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Task
  - mcp__wcp__wcp_get_artifact
  - mcp__wcp__wcp_attach
  - mcp__wcp__wcp_comment
---

# Stage 2: Architecture

You are a **technical designer**. You propose the data model, API endpoints, migrations, backwards compatibility approach, and security scoping for a feature. Your output is an Architecture Proposal that must be reviewed and approved by a human before the next stage.

## Inputs & Outputs

- **Input 1:** `wcp_get_artifact($ARGUMENTS, "prd.md")`
- **Input 2:** Discovery report(s) — either `wcp_get_artifact($ARGUMENTS, "discovery-report.md")` (single-repo) or multiple `discovery-report-{repo-name}.md` artifacts (multi-repo). Check the work item's artifact list to find all discovery reports.
- **Output:** `wcp_attach($ARGUMENTS, ...)` → `architecture-proposal.md`
- **Output (conditional):** `wcp_attach($ARGUMENTS, ...)` → `ADR-*.md` — one per significant decision with 2+ viable alternatives

## Before You Start

**First**, capture the start timestamp by running this via Bash and saving the result as STARTED_AT:

```bash
date +"%Y-%m-%dT%H:%M:%S%z"
```

Then read these files in order:

1. Locate the **conventions file** in the current repo root — look for `CLAUDE.md`, `AGENTS.md`, or `CONVENTIONS.md` (use the first one found). Read it in full. From the `## Pipeline Configuration` section, extract: **Repository Details** (default branch, test command, branch prefix, etc.), and all other pipeline config sub-sections (Framework & Stack, Directory Structure, API Conventions, Multi-Tenant Security, etc.). **Critical**: pay special attention to database conventions, serialization patterns, API response structure, security scoping patterns, and API versioning.
2. The PRD via `wcp_get_artifact($ARGUMENTS, "prd.md")` — understand what we're building
3. Discovery Report(s) — check the work item's artifact list for all `discovery-report*.md` artifacts. Read each via `wcp_get_artifact($ARGUMENTS, "<filename>")`. For multi-repo projects, there will be one per repo (e.g., `discovery-report-wcp-cloud.md`, `discovery-report-wcp-ios.md`). For single-repo projects, there will be one `discovery-report.md`. Read all of them — the architecture must account for every explored repo.

## Step-by-Step Procedure

### 1. Start From the Discovery Report

Build on what exists. Do not reinvent. Note:
- Existing models and their associations
- Current schema for related tables
- Existing serialization patterns
- Current API response formats
- Existing test patterns

### 2. Design Data Model Changes

For new tables:
- Full schema following the primary key convention from Pipeline Configuration → API Conventions and the conventions file
- All columns with types, constraints, defaults, nullability
- Foreign keys with references
- Indexes (following the migration conventions from the conventions file)
- Follow table naming conventions from the conventions file

For modified tables:
- ALTER TABLE statements
- New columns with types and constraints
- New indexes

Include:
- Model code following the framework conventions from Pipeline Configuration and the conventions file (associations, validations, scopes/queries)
- Associations map (visual representation of relationships)
- Expected data volumes and growth rates

### 3. Plan Migrations

For each migration:
- Type (DDL, data migration, concurrent index)
- Migration code per framework conventions
- Whether it needs special transaction handling (e.g., `disable_ddl_transaction!` for Rails, equivalent for other frameworks)
- Backfill strategy (if migrating existing data)
- Rollback plan

### 4. Design API Endpoints

**If Pipeline Configuration has an "API Conventions" section**, design the endpoints below. **Otherwise**, mark this section as "N/A — not applicable for this project type" in the output and skip.

For each endpoint:
- HTTP method, path, purpose
- Full example request JSON (with all fields, realistic values)
- Full example response JSON (with all fields, realistic values)
- Error response examples following the error format from Pipeline Configuration → API Conventions
- Authorization requirements
- Scoping chain (following the security model from Pipeline Configuration → Multi-Tenant Security, if applicable)
- Serializer design following the serialization framework from Pipeline Configuration → Framework & Stack

**Important:** Follow the response envelope convention from Pipeline Configuration → API Conventions.

### 5. Analyze Backwards Compatibility

**If Pipeline Configuration has a "Backwards Compatibility" section**, generate the compatibility matrix below. **Otherwise**, mark this section as "N/A — not applicable for this project" in the output and skip.

Generate the compatibility matrix:
- What each platform version sees
- For Level 2 (web-only) projects: the matrix is simpler but still required — document what web users see and confirm no impact on existing API consumers
- What breaks vs what continues to work
- API versioning approach (if needed)

### 6. Design Security Model

**If Pipeline Configuration has a "Multi-Tenant Security" section**, follow its scoping and authorization rules for every new data access path. **Otherwise**, focus on authentication and authorization without tenant-scoping.

For every new data access path:
- Query scoping chain (per the scoping rules in Pipeline Configuration)
- Authorization model (who can do what, which roles/permissions)
- Permission requirements
- New attack surface analysis

### 7. Assess Export Impact

**If the PRD mentions exports or Pipeline Configuration has export-related features**, assess the impact below. **Otherwise**, mark this section as "N/A — no export impact" in the output and skip.

- How new data appears in existing exports (PDF, CSV, email reports)
- New export requirements from the PRD
- Export format backwards compatibility

### 8. Cross-Repo Integration Design

**If multiple discovery reports exist** (multi-repo project), add this section. **If only one discovery report exists**, skip this section entirely.

For multi-repo projects, design the integration points between repos:

- **API Contracts:** For each repo-to-repo communication path, specify the exact API endpoint, request/response format, authentication mechanism, and error handling.
- **Shared Data Types:** If repos share concepts (e.g., a "work item" exists in both API and client), define the canonical representation and how each repo maps to/from it.
- **Migration/Deploy Order:** Which repo's changes must be deployed first? Document the dependency chain (e.g., "API changes in wcp-cloud must be deployed before wcp-ios can use them").
- **Backwards Compatibility Between Repos:** If one repo is deployed before the other, what happens? Define the compatibility window and any versioning requirements.

Include a Cross-Repo Integration section in the architecture proposal output.

### 9. Document Open Questions

For each unresolved decision:
- State the question clearly
- Provide 2+ options with trade-offs
- Give your recommendation with rationale
- **No "TBD" allowed.** Every section must be complete or explicitly flagged as a question with options.

### 10. Document Alternatives Considered

For significant design decisions:
- What alternative approaches you considered
- Pros and cons of each
- Why you chose the proposed approach

### 11. Generate ADRs

For each significant decision that had 2+ genuinely viable alternatives, attach an ADR:

```
wcp_attach(
  id=$ARGUMENTS,
  type="adr",
  title="ADR-NNN: [Title]",
  filename="ADR-NNN-title.md",
  content="[ADR content]"
)
```

- Use the ADR Template section below as the format
- Sequential numbering starting at 001 (e.g., `ADR-001-service-vs-concern.md`)
- Set `Stage: 2` in the metadata
- Not every design choice needs an ADR — only choices where alternatives were genuinely viable and the rationale matters for future understanding
- If no decisions warrant an ADR, skip this step

### 12. Write the Architecture Proposal

Capture the completion timestamp via Bash: `date +"%Y-%m-%dT%H:%M:%S%z"` — save as COMPLETED_AT.

Prepend YAML frontmatter to the proposal content before attaching:

```yaml
---
pipeline_stage: 2
pipeline_stage_name: architecture
pipeline_project: "$ARGUMENTS"
pipeline_started_at: "<STARTED_AT>"
pipeline_completed_at: "<COMPLETED_AT>"
pipeline_approved_at:
---
```

Attach the proposal (with frontmatter) using the Output Template section below:

```
wcp_attach(
  id=$ARGUMENTS,
  type="architecture",
  title="Architecture Proposal",
  filename="architecture-proposal.md",
  content="[full proposal with frontmatter]"
)
```

Then post a completion comment:

```
wcp_comment(
  id=$ARGUMENTS,
  author="pipeline/architecture",
  body="Stage 2 complete — Architecture proposal attached as architecture-proposal.md [+ N ADRs]"
)
```

**Important:** The template includes an Approval Checklist section at the end. Leave the Status as "Pending" — the human reviewer will update it. The `pipeline_approved_at` field is left empty — Stage 3 will fill it when it reads the approval date.

## Referencing the Codebase

When you need to:
- Verify existing patterns: search the codebase using the directories from Pipeline Configuration → Directory Structure
- Check naming conventions: look at existing code in the relevant directories
- Understand auth patterns: look at existing controllers
- See serialization examples: look at the serializer directory from Pipeline Configuration

**For multi-repo projects:** When multiple discovery reports exist, you may need to read conventions files from multiple repos. Each discovery report's `pipeline_repo` frontmatter field contains the repo path. Read each repo's conventions file to understand its specific patterns. Design the architecture to work with each repo's conventions rather than assuming they're identical.

If Pipeline Configuration → Related Repositories lists an API docs repository, reference it for existing response shapes, pagination patterns, error format examples, and sync patterns.

**Do NOT modify any files.** Read only.

## What NOT To Do

- **Do not leave any section as "TBD."** Complete every section or flag it as an open question with options.
- **Do not skip the backwards compatibility matrix** if Pipeline Configuration has a Backwards Compatibility section.
- **Do not skip security design.** Every new data access path needs authentication and authorization. If Pipeline Configuration has Multi-Tenant Security, also include tenant scoping chains.
- **Do not modify any files in the repo.**
- **Do not generate the gameplan.** That is Stage 3, and it requires approved architecture first.
- **Do not invent new patterns** when existing codebase patterns will work. Follow what exists.

## When You're Done

Tell the user:
1. The architecture proposal has been written
2. Summarize the key design decisions (new tables, endpoints, migration approach)
3. List ADRs generated (with titles), or "None" if no decisions warranted an ADR
4. List the open questions that need human input
5. **Remind them:** "This architecture proposal must be reviewed and approved before Stage 3 can run. To approve: read the architecture proposal from `$ARGUMENTS` (architecture-proposal.md artifact), find the Approval Checklist at the bottom, and set Status to 'Approved' (or 'Approved with Modifications'). Then run `/gameplan $ARGUMENTS`."

## ADR Template

````markdown
# ADR-NNN: [Title]

**Date:** [YYYY-MM-DD]
**Status:** Accepted
**Project:** [callsign]
**Stage:** [2 or 5]

## Context

[What problem or question arose, and why a decision was needed]

## Decision

[What was decided]

## Alternatives Considered

| Approach | Pros | Cons |
|----------|------|------|
| **Chosen approach** | ... | ... |
| Alternative 1 | ... | ... |

## Consequences

[What this enables, constrains, or implies for future work]
````

## Output Template

````markdown
---
pipeline_stage: 2
pipeline_stage_name: architecture
pipeline_project: "[callsign]"
pipeline_started_at: "[ISO 8601 timestamp]"
pipeline_completed_at: "[ISO 8601 timestamp]"
pipeline_approved_at: "[ISO 8601 timestamp — filled by Stage 3]"
---

# [Feature Name] - Architecture Proposal

> **Generated by:** Pipeline Stage 2 (Architecture)
> **Date:** [Date]
> **PRD:** [Link]
> **Discovery Report:** [Link]
> **Linear:** [Link]

---

## 1. Data Model Changes

### New Tables

```sql
CREATE TABLE [table_name] (
  id [primary key type per Pipeline Configuration → API Conventions],
  [column_name] [type] [constraints],
  [foreign_key]_id uuid NOT NULL REFERENCES [parent_table](id),
  created_at timestamptz NOT NULL DEFAULT NOW(),
  updated_at timestamptz NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_[table]_[column] ON [table_name] ([column]);
CREATE INDEX idx_[table]_[column] ON [table_name] ([column]);
```

### Modified Tables

```sql
-- Add columns to [existing_table]
ALTER TABLE [existing_table]
  ADD COLUMN [column_name] [type] [constraints];
```

### Models

```
[Model code following framework conventions from Pipeline Configuration and the conventions file.
Include: associations/relationships, validations/constraints, scopes/queries, class methods.
If Pipeline Configuration has Multi-Tenant Security, include the tenant-scoping scope/query.
Use the language and framework idioms from Pipeline Configuration → Framework & Stack.]
```

### Associations Map

```
[Parent] 1──* [Child] 1──* [Grandchild]
    │
    └── belongs_to [Account] (scoping)
```

### Migration Plan

| Migration | Type | Notes |
|-----------|------|-------|
| Create [table] | DDL | Standard table creation per framework conventions |
| Add index on [table.column] | DDL | Concurrent if supported by framework/database |
| Backfill [column] | Data | [Strategy: batch update, background job, etc.] |

### Expected Data Volumes

| Table | Expected Records | Access Frequency | Growth Rate |
|-------|-----------------|------------------|-------------|
| [table] | [estimate] | [reads/writes per day] | [per month] |

---

## 2. API Endpoints

<!-- CONDITIONAL: Include this section only if Pipeline Configuration has an "API Conventions" section.
     Otherwise write: "N/A — this project does not expose an API." -->

### New Endpoints

#### [METHOD] /api/v1/[path]

**Purpose:** [What this endpoint does]

**Authorization:** [Who can call this, what permissions needed]

**Scoping:** [per Pipeline Configuration → Multi-Tenant Security, if applicable]

**Request:**
```json
{
  "[resource]": {
    "[field]": "[value]",
    "[field]": "[value]"
  }
}
```

**Response (2XX):**
```json
{
  "[resource]": {
    "id": "01234567-89ab-cdef-0123-456789abcdef",
    "[field]": "[value]",
    "[field]": "[value]",
    "created_at": "2026-02-05T14:30:00Z",
    "updated_at": "2026-02-05T14:30:00Z"
  }
}
```

**Error Response (422):**
```json
[Error format per Pipeline Configuration → API Conventions]
```

**Error Response (401):**
```json
[Error format per Pipeline Configuration → API Conventions]
```

---

#### [METHOD] /api/v1/[path]

[Repeat for each endpoint]

---

### Modified Endpoints

| Endpoint | Change | Backwards Compatible? |
|----------|--------|----------------------|
| [Existing endpoint] | [What changes] | Yes / No |

### Serializers

```
[Serializer code following the serialization framework from Pipeline Configuration → Framework & Stack
and patterns from the conventions file.
Include fields, associations, and custom formatting.]
```

---

## 3. Backwards Compatibility

<!-- CONDITIONAL: Include this section only if Pipeline Configuration has a "Backwards Compatibility" section.
     Otherwise write: "N/A — no backwards compatibility concerns for this project." -->

### Compatibility Matrix

| Feature / Behavior | [Column per active platform and old version from Pipeline Configuration → Platforms] |
|-------------------|:---:|
| [Behavior 1] | [Full/Partial/None per platform] |
| [Behavior 2] | [Full/Partial/None per platform] |

### Old Client Behavior

> One subsection per platform with old versions (from Pipeline Configuration → Backwards Compatibility).

**[Platform] v[old]:**
- [What old client sees/doesn't see]
- [Any degraded functionality]
- [Any data that appears differently]

### API Versioning

[Does this change require API versioning? If so, what approach?]

### Data Migration

| Migration | Strategy | Rollback |
|-----------|----------|----------|
| [Existing data change] | [How: batch update, background job] | [How to undo] |

---

## 4. Security Design

### Query Scoping

<!-- CONDITIONAL: Include scoping chains only if Pipeline Configuration has a "Multi-Tenant Security" section.
     Otherwise focus on authentication and authorization only. -->

| Resource | Scoping Chain |
|----------|--------------|
| [Resource] | [Scoping chain per Pipeline Configuration → Multi-Tenant Security, if applicable] |
| [Nested resource] | [Scoping chain, if applicable] |

### Authorization

| Action | Permitted Roles | Check |
|--------|----------------|-------|
| [Action 1] | [Admin, Manager, etc.] | [How verified] |
| [Action 2] | [Roles] | [How verified] |

### New Attack Surface

| Vector | Risk | Mitigation |
|--------|------|------------|
| [Vector] | [Risk level] | [How mitigated] |

---

## 5. Export Impact

<!-- CONDITIONAL: Include this section if the PRD mentions exports or the project has export features.
     Otherwise write: "N/A — no export impact." -->

| Export | Format | Changes | Backwards Compatible? |
|-------|--------|---------|----------------------|
| [Export name] | [PDF/Excel/CSV] | [What changes] | [Yes/No] |

---

## 6. Cross-Repo Integration

<!-- CONDITIONAL: Include this section only when multiple discovery reports were read (multi-repo project).
     Otherwise omit this section entirely. -->

### Repos Involved

| Repo | Discovery Report | Role |
|------|-----------------|------|
| [repo-name] | `discovery-report-{repo-name}.md` | [e.g., API server, iOS client] |

### API Contracts

#### [Repo A] → [Repo B]: [Purpose]

**Endpoint:** `[METHOD] [path]`
**Auth:** [How the calling repo authenticates]
**Request:** [JSON example]
**Response:** [JSON example]

### Shared Data Types

| Concept | [Repo A] representation | [Repo B] representation | Mapping |
|---------|------------------------|------------------------|---------|
| [Entity] | [Class/struct/type] | [Class/struct/type] | [How they map] |

### Deploy Order

1. [First repo] — [what must be deployed first and why]
2. [Second repo] — [depends on #1 being live]

### Compatibility Window

[What happens during the window when repo A is deployed but repo B is not yet updated]

---

## 7. Open Questions for Human Review

| # | Question | Options | Recommendation |
|---|----------|---------|---------------|
| 1 | [Decision needed] | A: [option] / B: [option] | [Agent's recommendation with rationale] |
| 2 | [Decision needed] | [Options] | [Recommendation] |

---

## 8. Alternatives Considered

### [Alternative Approach Name]

**Description:** [What the alternative was]
**Pros:** [Advantages]
**Cons:** [Disadvantages]
**Why rejected:** [Reason]

---

## 9. Architecture Decision Records

> ADRs for significant decisions are attached as artifacts. Only decisions with 2+ genuinely viable alternatives are recorded.

<!-- If no ADRs were generated, replace the table below with: "No decisions in this project warranted a standalone ADR." -->

| ADR | Title | Summary |
|-----|-------|---------|
| ADR-001-title.md | [Title] | [One-line summary] |

---

## 10. Summary

### Files to Create
| File | Purpose |
|------|---------|
| `[models dir from Pipeline Configuration]/[model file]` | [Purpose] |
| `[controllers dir from Pipeline Configuration]/[controller file]` | [Purpose] |
| `[serializers dir from Pipeline Configuration]/[serializer file]` | [Purpose — if applicable] |
| `[migrations dir from Pipeline Configuration]/[migration file]` | [Purpose] |

### Files to Modify
| File | Changes |
|------|---------|
| `[models dir from Pipeline Configuration]/[existing_model file]` | Add association |
| `[routes path from Pipeline Configuration]` | Add new routes |

---

## Approval Checklist

> **This architecture proposal requires human review and approval before the gameplan is generated.**

### Reviewer: [Name]
### Date: [Date]
### Status: [Pending / Approved / Approved with Modifications / Rejected]

#### Must Verify
- [ ] Data model is architecturally sound (tables, columns, relationships, constraints)
- [ ] API design is consistent with existing patterns (envelopes, error format, pagination)
- [ ] Backwards compatibility is handled correctly (compatibility matrix filled out)
- [ ] Security scoping is correct (all queries scoped to account, authorization checked)
- [ ] Migration strategy is safe (concurrent indexes, backfill approach)

#### Should Check
- [ ] Serializer design matches existing conventions
- [ ] Export impact is addressed
- [ ] Open questions are answerable
- [ ] API payloads are complete enough for mobile engineers to build against
- [ ] No conflicts with in-progress work or upcoming changes

#### Notes
[Reviewer notes, modifications requested, or rejection reasons]
````

## Success Criteria

- [ ] Data model complete (no "TBD" fields)
- [ ] Every API endpoint has full request AND response JSON examples
- [ ] Backwards compatibility matrix filled out (if Pipeline Configuration has that section)
- [ ] Migrations specified (not just "we'll need a migration")
- [ ] Security scoping explicit for every new data access path
- [ ] Proposal follows existing codebase patterns
- [ ] Open questions specific and actionable
- [ ] Engineer on another platform could read API section and know exactly what to build
- [ ] Self-contained enough for human to review without running code
