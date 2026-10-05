---
name: skill-finder
description: |
  Navigation aid for the processkit skill catalog — maps natural-language
  cues and task types to the right skill. Read this when you are unsure
  which skill applies to the current task, when the user names a task
  without naming a skill, or at session start when orienting to an
  unfamiliar project. Always the first skill to consult; never the last.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-skill-finder
    version: "1.0.0"
    created: 2026-04-08T00:00:00Z
    category: processkit
    layer: 1
    core: true   # proposed: always install regardless of [skills].include/exclude
                 # pending aibox companion issue for content_install.rs change
    provides:
      mcp_tools:
        - find_skill
        - list_skills
        - catalog
---

# Skill Finder

## Intro

When you are unsure which skill to use, start here. This skill maps
what the user is asking for to the skill that handles it. It is not a
skill you invoke to do work — it is a skill you read to decide what to
invoke next.

## Overview

### By trigger phrase

Find the phrase that most closely matches what the user said, then load
that skill before proceeding.

| If the user says… | Skill to load |
|---|---|
| "refactor this", "clean up the code" | `refactoring` |
| "review this PR", "code review" | `code-review` |
| "write a test", "test this", "TDD" | `tdd-workflow` |
| "testing strategy", "what tests do we need" | `testing-strategy` |
| "debug this", "find the bug", "why is this failing" | `debugging` |
| "design the API", "API contract" | `api-design` |
| "system design", "design this system" | `system-design` |
| "architecture", "how should we structure this" | `software-architecture` |
| "domain model", "DDD" | `domain-driven-design` |
| "module structure", "package boundaries", "split this up" | `software-modularization` |
| "new service", "microservice", "extract this into a service" | `microservice-creation` |
| "events", "event-driven", "pub-sub" | `event-driven-architecture` |
| "deploy", "CI/CD pipeline", "set up CI" | `ci-cd-setup` |
| "Docker", "Dockerfile", "containerise this" | `dockerfile-review` |
| "Kubernetes", "k8s", "set up the cluster" | `kubernetes-basics` |
| "Terraform", "infrastructure as code" | `terraform-basics` |
| "write SQL", "SQL query", "query the database" | `sql-patterns` |
| "SQL style", "format the SQL" | `sql-style-guide` |
| "database design", "schema design" | `database-modeling` |
| "database migration", "migrate the schema" | `database-migration` |
| "NoSQL", "MongoDB", "document store" | `nosql-patterns` |
| "secure this", "security review" | `secure-coding` |
| "threat model" | `threat-modeling` |
| "secrets", "API keys", "credential management" | `secret-management` |
| "auth", "authentication", "OAuth" | `auth-patterns` |
| "logging", "log this" | `logging-strategy` |
| "metrics", "monitoring", "dashboards" | `metrics-monitoring` |
| "trace", "distributed tracing" | `distributed-tracing` |
| "alert", "on-call", "PagerDuty" | `alerting-oncall` |
| "postmortem", "incident review" | `postmortem-writing` |
| "incident", "on fire", "outage" | `incident-response` |
| "profile this", "find the bottleneck", "performance" | `performance-profiling` |
| "load test", "stress test" | `load-testing` |
| "Python" | `python-best-practices` |
| "TypeScript", "JavaScript" | `typescript-patterns` |
| "Go", "Golang" | `go-conventions` |
| "Rust" | `rust-conventions` |
| "Java" | `java-patterns` |
| "FastAPI", "Python API" | `fastapi-patterns` |
| "gRPC", "protobuf" | `grpc-protobuf` |
| "GraphQL" | `graphql-patterns` |
| "Flutter", "mobile app" | `flutter-development` |
| "Tailwind", "CSS utility classes" | `tailwind` |
| "frontend design", "UI components" | `frontend-design` |
| "AI fundamentals", "ML concepts", "machine learning basics" | `ai-fundamentals` |
| "analyse data", "pandas", "polars", "dataframe" | `pandas-polars` |
| "data pipeline", "ETL", "data engineering" | `data-pipeline` |
| "data quality", "data validation" | `data-quality` |
| "data science", "notebook", "EDA" | `data-science` |
| "visualise data", "chart this" | `data-visualization` |
| "RAG", "retrieval", "vector search" | `rag-engineering` |
| "embeddings", "vector database" | `embedding-vectordb` |
| "prompt engineering", "write a prompt" | `prompt-engineering` |
| "evaluate the LLM", "benchmark the model" | `llm-evaluation` |
| "which model should I use", "recommend a model", "which LLM is best", "help me pick an AI model", "route tasks to the right model", "which Claude should I use" | `model-recommender` |
| "ML pipeline", "train a model" | `ml-pipeline` |
| "feature engineering" | `feature-engineering` |
| "diagram", "draw", "whiteboard", "Excalidraw" | `excalidraw` |
| "infographic", "SVG chart" | `infographics` |
| "logo", "brand mark", "SVG icon" | `logo-design` |
| "mobile design", "iOS", "Android UI" | `mobile-app-design` |
| "SEO", "search optimisation", "meta tags" | `seo-optimization` |
| "Word document", "docx" | `docx-authoring` |
| "PowerPoint", "slides", "pptx" | `pptx-authoring` |
| "Excel", "spreadsheet", "xlsx" | `xlsx-modeling` |
| "PDF", "generate a PDF" | `pdf-workflow` |
| "LaTeX", "academic paper" | `latex-authoring` |
| "write a PRD", "product requirements" | `prd-writing` |
| "user research", "user interview" | `user-research` |
| "data story", "present the analysis" | `data-storytelling` |
| "legal review", "contract review" | `legal-review` |
| "write an email", "draft a message" | `email-drafter` |
| "status update", "progress report" | `status-update-writer` |
| "onboard", "new joiner guide" | `onboarding-guide` |
| "changelog", "what changed in this release" | `changelog` |
| "plan the release", "version bump", "semver" | `release-semver` |
| "write a decision", "document this decision", "ADR" | `decision-record` |
| "backlog", "work items", "create a ticket" | `workitem-management` |
| "register an artifact", "catalog this document", "store this deliverable", "link this design file" | `artifact-management` |
| "log this event", "audit trail" | `event-log` |
| "remember this", "note this idea", "capture this" | `note-management` |
| "write a standup", "daily update" | `standup-context` |
| "write a handover", "shutting down", "container restart" | `session-handover` |
| "status briefing", "catch me up", "state of things" | `status-briefing` |
| "groom the context", "clean up context" | `context-grooming` |
| "archive context", "cold tier", "archive old workitems" | `context-archiving` |
| "prune runtime", "cleanup aibox runtime", "clean up agent worktrees", "reclaim runtime disk" | `runtime-prune` |
| "check all open issues", "check all PRs", "merge ready PRs", "repo reconcile", "commit and push all", "repository cleanup" | `repo-management` |
| "resolve all migrations", "resolve pk-doctor findings", "reconcile the project", "resolve issues and pull requests" | `project-reconciliation` |
| "second opinion", "devil's advocate", "poke holes in this" | `devils-advocate` |
| "multiple perspectives", "board of advisors" | `board-of-advisors` |
| "research this", "I'm not sure about this fact" | `research-with-confidence` |
| "build a new skill", "author a skill", "library expert skill" | `skill-builder` |
| "review this skill", "is this skill good" | `skill-reviewer` |
| "route this task", "what should I do", "which tool", "route_task" | `task-router` |
| "session start", "which skill applies", "check skill-finder", "1% rule" | `skill-gate` |
| "dependency audit", "check dependencies" | `dependency-audit` |
| "dependency management", "update packages" | `dependency-management` |
| "choose a branching strategy", "Gitflow", "GitHub Flow", "trunk-based development", "release branch strategy" | `git-branching` |
| "git workflow", "branch naming", "commit message" | `git-workflow` |
| "shell script", "bash script" | `shell-scripting` |
| "caching", "cache strategy" | `caching-strategies` |
| "concurrency", "async", "parallelism" | `concurrency-patterns` |
| "webhook", "callback URL" | `webhook-integration` |
| "error handling", "exception handling" | `error-handling` |
| "documentation", "write the docs" | `documentation` |
| "retrospective", "retro", "post-release review", "post-mortem", "lessons learned" | `retrospective` |
| "estimation", "story points", "planning poker" | `estimation-planning` |

### By directory (physical layout)

Skills are organized into 7 category subdirectories on disk. Use the
directory name as the `category:` value when authoring or filtering:

| Directory | Contents |
|---|---|
| `processkit/` | 46 skills for operating the processkit system |
| `engineering/` | 47 skills: software design, architecture, backend, languages |
| `devops/` | 16 skills: infrastructure, CI/CD, ops, monitoring |
| `data-ai/` | 11 skills: data science, ML, AI/LLM, embeddings |
| `product/` | 11 skills: product management, discovery, communication |
| `documents/` | 8 skills: document and content authoring |
| `design/` | 5 skills: visual, UI, and frontend design |

### By category

A curated selection of the most commonly used skills per task domain.
For the full catalog, read `skills/INDEX.md`.

**Process**
- `task-router` — primary routing entry point: maps task to skill + process override + MCP tool
- `workitem-management` — create, transition, and query WorkItems
- `decision-record` — capture architectural and product decisions as DecisionRecords
- `artifact-management` — register and retrieve completed deliverables
- `event-log` — write auditable log entries for any project event
- `note-management` — capture, review, and promote fleeting ideas and insights
- `session-handover` — write an end-of-session handover before shutdown
- `standup-context` — write a standup update (done / doing / next / blockers)
- `status-briefing` — generate a session-start orientation from project state
- `context-grooming` — periodically prune and compact the project context
- `runtime-prune` — inspect and invoke safe cleanup for
  runtime-manager-owned state
- `release-semver` — plan and execute a semver release
- `retrospective` — post-release blameless retrospective (4 signals, dual-emit Artifact+LogEntry)

**Architecture**
- `software-architecture` — high-level system design patterns and trade-offs
- `system-design` — designing systems from requirements to components
- `api-design` — REST, RPC, and event-based API contracts
- `domain-driven-design` — bounded contexts, aggregates, ubiquitous language
- `software-modularization` — module and package boundary design
- `microservice-creation` — service extraction, communication patterns, orchestration
- `event-driven-architecture` — pub-sub, event sourcing, CQRS

**Code quality**
- `code-review` — reviewing diffs and PRs for correctness, style, and risk
- `refactoring` — safe, incremental refactoring strategies
- `tdd-workflow` — test-first development cycle
- `testing-strategy` — choosing the right test types and coverage targets
- `debugging` — systematic bug investigation and root-cause analysis
- `error-handling` — error propagation, recovery, and user-facing messages

**Security**
- `secure-coding` — OWASP top 10, input validation, output encoding
- `threat-modeling` — STRIDE analysis and risk prioritisation
- `secret-management` — credential storage, rotation, and injection
- `auth-patterns` — authentication and authorization patterns

**Infrastructure**
- `ci-cd-setup` — pipeline design and configuration
- `dockerfile-review` — image hardening, layer optimisation, multi-stage builds
- `kubernetes-basics` — Deployments, Services, ConfigMaps, autoscaling
- `terraform-basics` — resource definitions, state management, modules

**Observability**
- `logging-strategy` — structured logging, levels, and retention
- `metrics-monitoring` — metric types, dashboards, SLOs
- `distributed-tracing` — trace propagation, span design, sampling
- `incident-response` — triage, mitigation, and communication during incidents

**Data and AI**
- `rag-engineering` — retrieval-augmented generation pipelines
- `prompt-engineering` — prompt design, few-shot examples, chain-of-thought
- `llm-evaluation` — benchmarking and red-teaming language models
- `model-recommender` — pick the right AI model via spider-chart profiles and task-plan routing
- `data-pipeline` — ETL/ELT design and orchestration
- `pandas-polars` — dataframe operations and transformations

**Document creation**
- `docx-authoring` — python-docx for Word documents
- `pptx-authoring` — python-pptx for presentations
- `xlsx-modeling` — openpyxl for spreadsheets and financial models
- `pdf-workflow` — WeasyPrint / ReportLab / pypdf for PDF generation

**Role-specific**
- `prd-writing` — product requirements documents
- `user-research` — interview guides, synthesis, personas
- `data-storytelling` — turning analysis into decisions for non-technical audiences
- `legal-review` — pre-consultation contract and compliance review
- `email-drafter` — professional email drafting with copy-paste output

**Meta**
- `skill-builder` — design and author new processkit skills, including
  library expert recipe skills
- `skill-reviewer` — review a skill against the processkit standard
- `research-with-confidence` — structured research with explicit confidence labels
- `devils-advocate` — adversarial analysis of a plan or proposal
- `board-of-advisors` — multi-perspective simulation with named advisor archetypes
- `status-briefing` — session-start orientation (also listed under Process)

### How to use a skill

Once you have identified the right skill:

1. Read the skill's `SKILL.md` — start with the **Intro** (3 sentences) to
   confirm it is the right match. If yes, read **Overview** for the workflow.
2. Follow the skill's instructions, adapting to the project's specific context.
3. Use **Full reference** only for edge cases or field-by-field specs.
4. If the skill has an MCP server (`mcp/SERVER.md`), its tools are available
   as function calls — the skill's Overview section describes when to use them.

If no skill in this index matches, check `skills/INDEX.md` for the full
catalog, or use `skill-builder` to author a new skill for the gap.

## Catalog queries

The `catalog` MCP tool provides user-facing skill discovery. Use it when
the user wants to browse, filter, or export the skill roster rather than
find a specific skill for a task.

### Trigger phrases

| User says… | Action |
|---|---|
| "list skills", "what skills do we have" | `catalog()` — full list, Markdown |
| "show me all skills in engineering" | `catalog(category="engineering")` |
| "show me all skills in <category>" | `catalog(category="<category>")` |
| "skills as JSON", "give me the skill list as JSON" | `catalog(output="json")` |
| "skills with model in the name", "find skills about model" | `catalog(keyword="model")` |
| "list skills with columns name and layer" | `catalog(columns=["name","layer"])` |
| "show processkit skills as YAML" | `catalog(category="processkit", output="yaml")` |

### Tool signature

```python
def catalog(
    category: str | None = None,
    tag: str | None = None,
    keyword: str | None = None,
    columns: list[str] | None = None,
    sort_by: str | None = None,
    output: str = "markdown",  # "markdown" | "json" | "yaml"
) -> str | list[dict]
```

**Defaults:** all skills, `columns=["name","category","description"]`,
`sort_by="name"`, `output="markdown"`.

**Available columns:**

| Column | Source |
|---|---|
| `name` | `name` frontmatter field |
| `category` | Category directory name |
| `description` | First line of `description` frontmatter field |
| `tags` | `metadata.processkit.tags` list |
| `version` | `metadata.processkit.version` |
| `layer` | `metadata.processkit.layer` |
| `allowed_tools` | `metadata.processkit.provides.mcp_tools` list |
| `has_mcp` | True if `mcp/server.py` exists for the skill |
| `skill_md_path` | Relative path to SKILL.md from project root |

### Example invocations

**1. Default — all skills as a Markdown table (name, category, description)**

```
catalog()
```

Returns a Markdown table with ~130+ rows, sorted by name.
Shape: `str` (Markdown table).

**2. Filter by category, JSON output**

```
catalog(category="processkit", output="json")
```

Returns only processkit-category skills as a JSON array.
Shape: `list[dict]` — e.g.
`[{"name": "artifact-management", "category": "processkit",
"description": "Register and retrieve completed deliverables."}, …]`

**3. Keyword search, restricted columns**

```
catalog(keyword="model", columns=["name", "category", "description"])
```

Returns all skills whose `name` or `description` contains "model"
(case-insensitive). Shape: `str` (Markdown table).

**4. Custom columns with YAML output**

```
catalog(columns=["name", "layer", "has_mcp"], output="yaml")
```

Returns a YAML fenced code block listing name, layer, and has_mcp for
every skill, sorted by name.

**5. Tag filter**

```
catalog(tag="routing", columns=["name", "category", "tags"])
```

Filters to skills that carry `"routing"` in their frontmatter `tags`
list (exact match, case-insensitive).

## Gotchas

- **Loading this skill every time instead of once.** skill-finder is an
  orientation aid, not a workflow skill. Read it once to identify the right
  skill, then load that skill and work from it. Do not keep skill-finder
  loaded alongside the working skill — it consumes context without adding
  value once you have identified the skill to use.
- **Treating the trigger-phrase table as exhaustive.** The table maps common
  phrases; it is not a complete index of all 120+ skills. If no phrase
  matches, scan the by-category section or read `skills/INDEX.md`. If
  the task is genuinely novel, use `skill-builder` to create a skill for it.
- **Skipping skill-finder when the task is "obvious."** The most common
  mistake is loading a skill by name from memory and discovering mid-task
  that the skill does not quite fit. Thirty seconds with the trigger-phrase
  table prevents an incorrect skill invocation. Default to checking even for
  familiar task types.
- **Using the category labels to filter instead of the trigger phrases.**
  The categories help humans browse; agents should match on trigger phrases,
  not category names. "Code quality" does not tell you whether to load
  `code-review`, `refactoring`, or `tdd-workflow` — the trigger phrase does.
- **Not updating skill-finder when new skills are added.** When a new skill
  is added to the catalog, add its trigger phrases to the table and its
  one-liner to the appropriate category. skill-finder is only reliable if
  it is kept current. The `skill-builder` skill includes a reminder to
  update this index.
- **Confusing skill-finder with skill-builder.** skill-finder helps you
  find an existing skill. skill-builder helps you create a new one. If
  skill-finder returns no match, the correct next step is `skill-builder`,
  not a general-purpose attempt to solve the task without a skill.
- **Ignoring the `core: true` intent when customising skill packages.**
  Until aibox enforces `core: true` in the install pipeline, project owners
  who configure `[skills].include` must add `skill-finder` explicitly.
  Omitting it means agents lose the navigation aid exactly when the catalog
  is most customised and therefore hardest to navigate.

## Full reference

### The `core: true` flag

The `core: true` field in this skill's frontmatter is a **proposed**
convention. It signals intent: this skill should be installed unconditionally,
regardless of `[skills].include` or `[skills].exclude` configuration in
`aibox.toml`.

**Current status:** the flag is present in the frontmatter as documentation.
aibox does not yet enforce it — a companion aibox issue will land the
`content_install.rs` change. Until then, project owners must include
`skill-finder` in any explicit `[skills].include` list.

**Why it matters:** a project owner who limits the installed skills to a
curated subset has, by definition, the most non-obvious skill catalog. That
is precisely when skill-finder is most needed. A skill that can be excluded
provides weaker guarantees than one that cannot.

### Keeping this index current

When adding a new skill to processkit:
1. Add 1–3 trigger phrases to the trigger-phrase table
2. Add a one-liner under the appropriate category in the by-category section
3. If no existing category fits, add a new category

The `skill-builder` skill includes a step reminding the author to update
skill-finder. The `skill-reviewer` skill checks that skill-finder has been
updated.
