---
name: convert-to-copilot
description: "This skill should be used when converting a Claude Code agent (+ its launch command + its skills) into a single GitHub Copilot agent (.github/agents/*.agent.md) with supporting context files under .copilot_utils/{agent_name}/. Load when someone says 'convert to copilot', 'make copilot agent', 'copilot version of this agent', 'port this agent to copilot', or when /convert-to-copilot is invoked with an agent file path."
---

# Convert Claude Code → GitHub Copilot Agent

Converts a Claude Code agent + command + skills into a `.github/agents/*.agent.md` with supporting
files in a per-agent `.copilot_utils/{agent_name}/` directory.

---

## Canonical Output Structure

```
.github/
└── agents/
    └── {agent_name}.agent.md       ← single merged file (agent + command)

.copilot_utils/
└── {agent_name}/
    ├── context/                    ← WHAT to use (knowledge, conventions, reference)
    │   └── {skill}.md
    └── trees/                      ← HOW to decide (branching, if/else logic)
        └── {skill}.md
```

**External guide:** https://github.com/endorphin-ai/vs-code-copilot-agents/blob/main/COPILOT_AGENTS_GUIDE.md

---

## Three-File Separation Principle

Every file has exactly one role:

| File Type   | Location                               | Contains                                      | Example                                          |
| ----------- | -------------------------------------- | --------------------------------------------- | ------------------------------------------------ |
| **Agent**   | `.github/agents/`                      | WHAT to do — workflow, phases, orchestration  | "Read file, apply tree, validate, create output" |
| **Tree**    | `.copilot_utils/{agent_name}/trees/`   | HOW to decide — if/else branching logic       | "If label contains X → use path Y"               |
| **Context** | `.copilot_utils/{agent_name}/context/` | WHAT to use — reference info, patterns, rules | "Available scaffolds: A, B, C"                   |

**NEVER embed knowledge or decision logic in the agent body.** Reference files instead:

- Decisions → `**Apply tree:** .copilot_utils/{agent_name}/trees/{file}.md`
- Reference → `**Reference:** .copilot_utils/{agent_name}/context/{file}.md`

---

## Variables

```
{agent_file}      = $ARGUMENTS (path to Claude agent .md file)
{command_file}    = (path to Claude command .md — ask if not provided)
{agent_name}      = (extracted from agent frontmatter `name` field)
{output_agent}    = .github/agents/{agent_name}.agent.md
{output_dir}      = .copilot_utils/{agent_name}
{trees_dir}       = .copilot_utils/{agent_name}/trees
{knowledge_dir}   = .copilot_utils/{agent_name}/context
{output_folder}   = .copilot-convert-results
```

---

## External Reference (fetch first)

```
WebFetch https://raw.githubusercontent.com/endorphin-ai/vs-code-copilot-agents/main/COPILOT_AGENTS_GUIDE.md
```

Authoritative Copilot spec. If anything in this skill conflicts with the guide, the guide wins.

---

## ALWAYS_DO

- **ALWAYS** fetch the external guide before starting conversion
- **ALWAYS** read the full agent, command, and every linked skill before writing any output
- **ALWAYS** merge command description triggers and `argument-hint` into the Copilot agent `description` field
- **ALWAYS** use `manage_todo_list` with `"operation": "write"` + full todoList before any work starts — bare JSON arrays fail
- **ALWAYS** drop `color`, `memory`, `isolation`, `skills`, `allowed-tools` from converted frontmatter
- **ALWAYS** validate every `.copilot_utils/{agent_name}/` path referenced in the body resolves to a real file

## NEVER_DO

- **NEVER** create `.prompt.md`, `.instructions.md`, or `.github/skills/` — Copilot uses a single merged agent file
- **NEVER** use `"fetch"` in `tools[]` — the correct alias is `"web"`
- **NEVER** embed decision logic or knowledge reference content inline in the agent body — always reference the file
- **NEVER** call `manage_todo_list` with a bare JSON array — always include `"operation": "write"`
- **NEVER** preserve `color`, `memory`, `isolation`, `skills`, `allowed-tools` fields in converted frontmatter

---

## Progress Tracking (mandatory)

```
TaskCreate(subject="Phase 1: Read all source files",       status="pending")
TaskCreate(subject="Phase 2: Scaffold output directories", status="pending")
TaskCreate(subject="Phase 3: Build agent frontmatter",     status="pending")
TaskCreate(subject="Phase 4: Convert agent body",          status="pending")
TaskCreate(subject="Phase 5: Write output files",          status="pending")
TaskCreate(subject="Phase 6: Validate",                    status="pending")
TaskCreate(subject="Phase 7: Conversion report",           status="pending")
```

---

## Phase Overview

| Phase | Action                                                            | Output                                |
| ----- | ----------------------------------------------------------------- | ------------------------------------- |
| 1     | Read agent, command, all skills                                   | `{output_folder}/1-source-context.md` |
| 2     | Create `.copilot_utils/{agent_name}/` directories                 | directories on disk                   |
| 3     | Build Copilot frontmatter                                         | `{output_folder}/3-frontmatter.md`    |
| 4     | Convert body: tracking, references, skill refs, memory            | `{output_folder}/4-body.md`           |
| 5     | Write `{output_agent}` + all `.copilot_utils/{agent_name}/` files | final output files                    |
| 6     | Validate against checklist                                        | `{output_folder}/6-validation.md`     |
| 7     | Print conversion report                                           | console                               |

Phases 1–3: `references/conversion-phases.md`
Phase 4: `references/conversion-body.md`
Phases 5–7: `references/conversion-output.md`

---

## Key Conversion Rules

### Skill → copilot_utils Mapping

| Skill content type                             | Destination                            |
| ---------------------------------------------- | -------------------------------------- |
| SKILL.md — knowledge, conventions, reference   | `{knowledge_dir}/{skill}.md`           |
| SKILL.md — decision trees, "if X then Y" logic | `{trees_dir}/{skill}.md`               |
| templates, schemas, output formats             | `{knowledge_dir}/{skill}-templates.md` |
| example files                                  | `{knowledge_dir}/{skill}-examples.md`  |
| shell scripts (`.sh`), python (`.py`)          | project `scripts/` or tool call inline |

**Classification rule:**

- "When you see X, do Y" / branching / diagnosis → **trees/**
- "Here is how things work, here are conventions" → **context/** (knowledge)
- Skill has both → copy full file to **context/**, extract decision sections to **trees/**

### Tool Mapping (quick reference)

| Claude                  | Copilot `tools[]`                  |
| ----------------------- | ---------------------------------- |
| Read                    | `"read"`                           |
| Write / Edit            | `"edit"`                           |
| Bash                    | `"execute"`                        |
| Grep / Glob             | `"search"`                         |
| WebFetch / WebSearch    | `"web"` ⚠️ NOT `"fetch"`           |
| TaskCreate / TaskUpdate | `"todo"`                           |
| Agent (sub-agent)       | `"agent"`                          |
| Jira MCP                | `"atlassian/*"` or explicit mcp ID |
| GitHub MCP              | `"github/*"`                       |

Full table + wildcards + execute variants: `references/tool-mapping.md`

### Model Expansion

| Claude    | Copilot                  |
| --------- | ------------------------ |
| `opus`    | `"Claude Opus 4.5"`      |
| `sonnet`  | `"Claude Sonnet 4.5"`    |
| `haiku`   | `"Claude Haiku 4.5"`     |
| `inherit` | omit or use most capable |

### manage_todo_list Format

Initial setup (one call before any work):

```json
{ "operation": "write", "todoList": [{ "id": 1, "title": "Phase 1: ...", "status": "not-started" }] }
```

Per-phase updates:

```json
{ "operation": "update", "updates": [{ "id": 1, "status": "in-progress" }] }
{ "operation": "update", "updates": [{ "id": 1, "status": "completed" }] }
```

### `handoffs` — VS Code sub-agent delegation

When Claude agent spawns sub-agents (`Task(subagent_type=...)`), convert based on `target`:

- `target: 'vscode'` → use `handoffs` in frontmatter
- `target: 'github-copilot'` → use `runSubagent()` in body

Full patterns: `references/advanced-patterns.md` and `references/advanced-subagents.md`

---

## Frontmatter Rules

| Field           | Required    | Notes                                      |
| --------------- | ----------- | ------------------------------------------ |
| `description`   | **Yes**     | Single-quoted, 50–150 chars                |
| `tools`         | Optional    | Omit = all tools; list for least-privilege |
| `model`         | Recommended | Full name: `'Claude Sonnet 4.5'`           |
| `name`          | Optional    | Defaults to filename                       |
| `target`        | Optional    | `'vscode'` or `'github-copilot'`           |
| `infer`         | Optional    | `false` to require explicit argument       |
| `argument-hint` | Optional    | VS Code only                               |
| `handoffs`      | Optional    | VS Code only — sub-agent delegation        |

Drop from Claude: `color`, `memory`, `isolation`, `skills`, `allowed-tools`

---

## Validation Checklist

Before writing any output file, verify:

- [ ] `{output_agent}` exists with `description` (50-150 chars, single-quoted)
- [ ] `tools` array uses correct aliases (`"web"` not `"fetch"`, `"todo"` not `"task"`)
- [ ] `description` contains trigger phrases from original command
- [ ] No separate command / prompt / instruction file was created
- [ ] Progress tracking uses `manage_todo_list` with `operation: write` format
- [ ] Every `.copilot_utils/{agent_name}/` path referenced in body resolves to a real file
- [ ] Agent body references knowledge via `**Reference:**` syntax (not embedded inline)
- [ ] Agent body references trees via `**Apply tree:**` syntax (not embedded inline)
- [ ] `handoffs` present when VS Code + sub-agents; `runSubagent()` when GitHub Copilot + sub-agents
- [ ] Agent body ≤ 30,000 characters

---

## References

- `references/conversion-phases.md` — phases 1–3: reading sources, scaffold, frontmatter build
- `references/conversion-body.md` — phase 4: full body conversion rules (task tracking, skill refs, memory)
- `references/conversion-output.md` — phases 5–7: write files, validate, conversion report
- `references/tool-mapping.md` — full tool/model tables, frontmatter fields, wildcards
- `references/advanced-patterns.md` — reference syntax, dynamic params, variable flow, execution strategy
- `references/advanced-subagents.md` — handoffs, runSubagent, parallel ops, return format, manage_todo_list
- `examples/pr-reviewer.md` — complete worked example
- `scripts/convert-agents.sh` — scaffold script (structure only, no content transformation)
- `assets/copilot-agent-template.md` — Copilot agent frontmatter template
- External: https://github.com/endorphin-ai/vs-code-copilot-agents/blob/main/COPILOT_AGENTS_GUIDE.md
