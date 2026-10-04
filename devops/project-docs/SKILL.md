---
model_tier: medium
name: project-docs
description: "Use when looking for project-specific documentation. Knows which docs exist in agents/reference/docs/ and agents/settings/contexts/ and maps work areas to relevant docs."
domain: process
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

# project-docs

## When to use

Use this skill when:
- Starting work on an unfamiliar area of the codebase
- Need to find relevant documentation for a specific module or feature
- Want to understand project-specific patterns before making changes

Do NOT use when:
- Looking for coding guidelines (use `guidelines` skill)
- Looking for infrastructure docs (use `aws-infrastructure` or `docker` skill)

## Description

This skill maps work areas to their relevant project documentation. It ensures agents
consult the right docs before making changes — preventing mistakes that come from not
understanding project-specific patterns, legacy conventions, or architectural decisions.

## When to Activate

- Before working on **any** area that has project-specific documentation
- When an agent is unsure about project conventions for a specific domain
- When creating or modifying code in areas covered by these docs

## Procedure: Find project documentation

1. Identify the work area from the user's request.
2. Look up the relevant docs in the mapping table below.
3. Read the **context** first (quick orientation), then the **detail docs** if needed.
4. Follow the conventions described in the docs.

## Documentation Structure

```
agents/
├── contexts/          → Quick orientation (read first)
│   ├── *.md           → Technical contexts (multi-tenancy, API versioning, etc.)
│   └── domain/        → Domain/industry knowledge (business logic, terminology)
│       └── job-*.md   → Domain context files (e.g., job-time-tracking.md)
├── docs/              → Deep dives (read when working on the area)
│   └── *.md           → Detailed conventions per topic
├── features/          → Feature plans
├── roadmaps/          → Step-by-step work plans
├── sessions/          → Session tracking
└── overrides/         → Project-specific overrides of .augment/ resources
```

## Domain Contexts

If `agents/settings/contexts/domain/` exists, it contains **business domain knowledge** — industry terms,
regulations, workflows, and edge cases that the agent needs to understand the problem space.

**When to read domain contexts:**
- Before working on any feature that touches business logic
- When you encounter domain-specific terms you don't fully understand
- When writing validations, business rules, or data models for a specific domain

**How to find the right file:**
- List `agents/settings/contexts/domain/` and read files whose name matches the work area
- Files prefixed with `job-` describe industry/profession knowledge
- When in doubt, read all domain context files — they are short orientation docs

## How to Find Relevant Docs

1. **List `agents/settings/contexts/`** — read any context file whose name matches the work area.
2. **List `agents/settings/contexts/domain/`** — read domain knowledge files relevant to the business logic.
3. **List `agents/reference/docs/`** — read detail docs for the specific topic you're working on.
4. **Check module docs** — if working in a module, resolve `{module_root}` from
   `modules.root_paths` and `{agent_folder}` from `modules.agent_folder` (see
   `scripts/_lib/agent_settings.ts::enumerate_modules()`), then check:
   - `{module_root}/{Module}/{agent_folder}/` — module-specific docs
   - `{module_root}/{Module}/{agent_folder}/settings/contexts/` — module-specific contexts (if exists)
   - `{module_root}/{Module}/{agent_folder}/settings/contexts/domain/` — module-specific domain knowledge (if exists)

### Reading order

| Step | What | Why |
|---|---|---|
| 1 | `agents/settings/contexts/*.md` | Quick orientation — big picture in ~100 lines |
| 2 | `agents/settings/contexts/domain/job-*.md` | Domain knowledge — business terms, rules, edge cases |
| 3 | Module `agents/settings/contexts/` | Module-specific contexts (if working in a module) |
| 4 | `agents/reference/docs/*.md` | Deep dive — code examples, conventions, patterns |

### Matching work areas to docs

Match by **filename** — doc filenames describe their topic. Examples:
- Working on API endpoints → look for `controller`, `api-*`, `middleware`, `authentication` docs
- Working on database → look for `database-*`, `multi-tenancy`, `customer-*` docs
- Working on time tracking → look for `job-time-tracking` in domain contexts
- Working on tests → look for `testing`, `seeders` docs

Do NOT hardcode a mapping — always **list the directory** and pick by relevance.

## Rules

- **Always read the context first** — it gives you the big picture in ~100 lines.
- **Read detail docs when you need to write code** — they have code examples and conventions.
- **Don't skip docs because you "know" the pattern** — project-specific conventions often differ
  from standard framework patterns.
- **Update docs when you change conventions** — if your change introduces a new pattern or
  deprecates an old one, update the relevant doc in `agents/reference/docs/`.

## Cross-References

| Skill | Relationship |
|---|---|
| `agent-docs-writing` | When to read/create/update agent docs in general |
| `context-create` | How to create new context documents |
| `module-management` | Module-specific docs in module `agents/` directories |


## Output format

1. Relevant doc paths and their key content summarized
2. Recommendation for which docs to read for the current task

## Gotcha

- Project docs are NOT the same as agent docs — project docs describe the codebase, agent docs describe agent behavior.
- Don't assume a doc exists because the area is important — always check the filesystem first.
- Stale docs are worse than missing docs — always verify doc content against actual code.

## Do NOT

- Do NOT create documentation that duplicates existing docs.
- Do NOT write docs for trivial or self-explanatory code.

## Auto-trigger keywords

- project documentation
- doc mapping
- work area docs
