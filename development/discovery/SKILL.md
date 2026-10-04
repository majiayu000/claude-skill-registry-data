---
name: discovery
description: "Run pipeline Stage 1 (Discovery) for a project. Explores the target codebase to understand current state before designing changes."
argument-hint: "<callsign> [--repo <path>]"
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

# Stage 1: Discovery

You are a **codebase explorer**. Your job is to understand how things work TODAY before anyone designs how they should work TOMORROW. You produce a Discovery Report.

## Argument Parsing

`$ARGUMENTS` contains: `<callsign> [--repo <path>]`

Parse them:
- **CALLSIGN**: The first token — a WCP callsign (e.g., `SN-3`)
- **--repo \<path\>** (optional): Path to a specific repository to explore. When provided, discovery runs against that repo instead of the current working directory.

When `--repo` is provided:
- **REPO_PATH**: The resolved absolute path
- **REPO_NAME**: The basename of the path (e.g., `~/projects/wcp-cloud` → `wcp-cloud`)
- **ARTIFACT_NAME**: `discovery-report-{REPO_NAME}.md` (suffixed)
- **Conventions file**: Read from `REPO_PATH` root, not cwd

When `--repo` is NOT provided:
- **REPO_PATH**: Current working directory
- **REPO_NAME**: (not set)
- **ARTIFACT_NAME**: `discovery-report.md` (unchanged, backward compatible)
- **Conventions file**: Read from cwd root (existing behavior)

## Inputs & Outputs

- **Input:** `wcp_get_artifact(CALLSIGN, "prd.md")`
- **Output:** `wcp_attach(CALLSIGN, ...)` → `ARTIFACT_NAME`

## Before You Start

**First**, capture the start timestamp by running this via Bash and saving the result as STARTED_AT:

```bash
date +"%Y-%m-%dT%H:%M:%S%z"
```

Then read these in order:

1. Locate the **conventions file** in `REPO_PATH` root — look for `CLAUDE.md`, `AGENTS.md`, or `CONVENTIONS.md` (use the first one found). Read it in full. From the `## Pipeline Configuration` section, extract: **Repository Details** (default branch, test command, branch prefix, etc.), and all other pipeline config sub-sections (Framework & Stack, Platforms, Directory Structure, etc.)
2. The PRD: `wcp_get_artifact(CALLSIGN, "prd.md")` — understand what we're building

## Step-by-Step Procedure

### 1. Parse the PRD

Extract:
- Feature areas / functional domains
- Entity names (models, tables, concepts referenced or implied)
- API endpoints referenced or implied
- UI views referenced or implied
- Platform designation (check the PRD header — Level 1, 2, or 3)
- Permissions and access control requirements

### 2. Search the Codebase

For each entity/keyword extracted from the PRD, search the directories listed in Pipeline Configuration → Directory Structure (rooted at `REPO_PATH`). For each directory purpose (Models, Controllers, Views, etc.), search the corresponding path for related code.

For each finding, record:
- File path with line numbers
- Relevant code snippets (not entire files)
- How it relates to the PRD feature

### 3. Search the API Documentation

If Pipeline Configuration → Related Repositories lists an API docs repository, search it.

Look for:
- Existing endpoint documentation for related resources
- Current response shapes and field names
- Pagination patterns used by similar endpoints
- Authentication and error format examples

### 4. Handle Platform Level

Check the PRD header for the project level:

- **Level 1** (small project): Focus on the primary platform. Lightweight discovery.
- **Level 2** (primary platform only): Focus on the primary platform. Mark other platform sections as "N/A — Level 2 (primary platform only) project."
- **Level 3** (all platforms): Search all repositories listed in Pipeline Configuration → Related Repositories that have Active status in Pipeline Configuration → Platforms table.

### 5. Document Cross-Platform Patterns

Even for web-only projects, document:
- How data flows through the system (models → controllers → serializers → response)
- Current serialization format for related resources
- API versioning approach for related endpoints
- How similar existing features are structured (find a comparable feature as a reference)

### 6. Flag Technical Risks

For each risk, include severity (High/Med/Low):
- Code needing significant refactoring to support the new feature
- Missing test coverage in areas that will change
- Performance concerns (N+1 queries, missing indexes, large data volumes)
- Security concerns (unscoped queries, missing authorization)
- Backwards compatibility risks

### 7. Document Open Questions

List ambiguities the PRD doesn't resolve and that code exploration didn't clarify. Each question should:
- Be specific and actionable (not "how should this work?")
- Cite the source (PRD section or code file)
- Indicate whether it's blocking (must be answered before architecture)

### 8. Write the Discovery Report

Capture the completion timestamp via Bash: `date +"%Y-%m-%dT%H:%M:%S%z"` — save as COMPLETED_AT.

Prepend YAML frontmatter to the report content:

```yaml
---
pipeline_stage: 1
pipeline_stage_name: discovery
pipeline_project: "CALLSIGN"
pipeline_repo: "REPO_PATH"
pipeline_started_at: "<STARTED_AT>"
pipeline_completed_at: "<COMPLETED_AT>"
---
```

If `--repo` was specified, include `pipeline_repo` in the frontmatter. If not, omit it.

Attach the report to the work item:

```
wcp_attach(
  id=CALLSIGN,
  type="discovery",
  title="Discovery Report[ — REPO_NAME]",
  filename="ARTIFACT_NAME",
  content="[full report content with frontmatter]"
)
```

When `--repo` is specified, include the repo name in the title (e.g., "Discovery Report — wcp-cloud"). When not specified, use "Discovery Report" (unchanged).

Log the completion:

```
wcp_comment(
  id=CALLSIGN,
  author="pipeline/discovery",
  body="Stage 1 complete — Discovery report attached as ARTIFACT_NAME[ (repo: REPO_NAME)]"
)
```

## What NOT To Do

- **Do not suggest how to build the feature.** That is Stage 2 (Architecture). You document what exists.
- **Do not give opinions on code quality** unless it represents a technical risk.
- **Do not explore unrelated code.** Stay focused on entities and patterns relevant to the PRD.
- **Do not modify any files in the target repos.** Read only.
- **Do not skip the schema lookup.** The current table/schema definitions (schema file path from Pipeline Configuration → Directory Structure) are critical for the Architecture stage.

## Output Template

````markdown
---
pipeline_stage: 1
pipeline_stage_name: discovery
pipeline_project: "[callsign]"
pipeline_repo: "[REPO_PATH — include only when --repo was specified]"
pipeline_started_at: "[ISO 8601 timestamp]"
pipeline_completed_at: "[ISO 8601 timestamp]"
---

# [Feature Name] - Discovery Report[ — REPO_NAME]

> **Generated by:** Pipeline Stage 1 (Discovery)
> **Date:** [Date]
> **PRD:** [callsign]/prd.md
> **Repository:** [REPO_PATH — include only when --repo was specified]

---

## 1. PRD Understanding

### Feature Summary
[Agent's interpretation of what the PRD is asking for - 2-3 sentences]

### Entities Identified
| Entity | PRD Reference | Existing? | Current Location |
|--------|--------------|-----------|-----------------|
| [Entity 1] | [Requirement ID] | Yes / No | `[models directory from Pipeline Configuration]/[entity file]` or N/A |
| [Entity 2] | [Requirement ID] | Yes / No | [Path] or N/A |

### Platforms Affected
> One checkbox per active platform from Pipeline Configuration → Platforms table.

- [ ] [Primary platform from Pipeline Configuration]
- [ ] [Additional platform, if listed in Pipeline Configuration → Platforms]

---

## 2. Current State: Primary Platform

### Related Models
| Model | File | Key Associations | Notes |
|-------|------|------------------|-------|
| [Model] | [models directory from Pipeline Configuration]/model.[ext] | [associations] | [Relevant notes] |

### Current Schema (Related Tables)

```sql
-- [table_name]
-- (from schema file: [schema path from Pipeline Configuration → Directory Structure])
CREATE TABLE [table_name] (
  [column definitions from schema file]
);
```

### Related Controllers
| Controller | File | Actions | Auth Pattern |
|-----------|------|---------|--------------|
| [Controller] | [controllers directory from Pipeline Configuration]/... | index, show, create | [How auth works] |

### Related Serializers
| Serializer | File | Fields Exposed |
|-----------|------|----------------|
| [Serializer] | [serializers directory from Pipeline Configuration]/... | [List of fields] |

### Related API Endpoints (Current)
| Method | Path | Purpose | Response Shape |
|--------|------|---------|---------------|
| GET | `/api/v1/...` | [Purpose] | [Brief shape] |

### Current API Response Examples

```json
// GET /api/v1/[endpoint]
{
  "example": "response"
}
```

### Related Tests
| Test File | Coverage | Type |
|-----------|----------|------|
| [test directory from Pipeline Configuration]/... | [What's tested] | [Test type] |

### Related Background Jobs
| Job | File | Purpose |
|-----|------|---------|
| [Job] | [jobs directory from Pipeline Configuration]/... | [Purpose] |

---

<!-- CONDITIONAL: Repeat the following section for each ADDITIONAL active platform from Pipeline Configuration → Platforms.
     If only one active platform exists, omit these sections entirely. -->

## 3. Current State: [Additional Platform Name]

### Related Code
| Component | File | Type | Notes |
|-----------|------|------|-------|
| [Component] | [Path] | [Component type] | [Notes] |

### Patterns Used
- [Architecture pattern]
- [Networking pattern: how API calls are made]
- [Data persistence approach]

### Related Tests
| Test File | Coverage |
|-----------|----------|
| [Path] | [What's tested] |

---

## 4. Cross-Platform Patterns

<!-- CONDITIONAL: If Pipeline Configuration → Platforms has 2+ active platforms, fill this section.
     If only one active platform, write: "N/A — single-platform project." -->

### Data Flow
```
[How data currently flows between platforms]
```

### Serialization Format
[JSON structure patterns, naming conventions (camelCase vs snake_case), etc.]

### API Versioning
[Current versioning approach, if any]

### How Similar Features Are Built
[Reference to a similar existing feature and how it's structured across platforms]

---

## 5. Technical Risks

| Risk | Severity | Details | Mitigation |
|------|----------|---------|------------|
| [Risk 1] | High / Med / Low | [Details] | [Suggested mitigation] |
| [Risk 2] | [Severity] | [Details] | [Mitigation] |

### Performance Concerns
- [N+1 query risks]
- [Missing indexes]
- [Large data volume concerns]

### Security Concerns
- [Scoping gaps in related code]
- [Authorization issues]

---

## 6. Open Questions

| # | Question | Source | Blocking? |
|---|----------|--------|-----------|
| 1 | [Question discovered during exploration] | [Where it came from] | Yes / No |
| 2 | [Ambiguity in PRD that code didn't resolve] | PRD Section [X] | Yes / No |

---

## 7. Recommendations for Architecture Stage

- [Pattern to follow for the new feature]
- [Existing code to extend vs replace]
- [Suggested approach based on existing patterns]
- [Things to avoid based on what exists]
````

## Success Criteria

- [ ] All PRD entities traced to existing code (or flagged as new)
- [ ] Current data model documented for affected tables
- [ ] Current API payloads documented for affected endpoints
- [ ] Existing code patterns identified
- [ ] Technical risks flagged with severity
- [ ] Open questions specific and actionable
- [ ] Report useful enough that human could skip reading the codebase

## When You're Done

Tell the user:
1. The discovery report has been attached to `CALLSIGN` as `ARTIFACT_NAME`
2. If `--repo` was specified, note which repo was explored
3. Summarize the key findings (entities found, risks flagged, open questions)
4. If this is a multi-repo project (other `discovery-report-*.md` artifacts exist on the work item), remind: "Run `/discovery CALLSIGN --repo <path>` for each additional repo before running `/architecture CALLSIGN`."
5. Otherwise: "You can now review the discovery report, then run `/architecture CALLSIGN` to proceed to the Architecture stage."
