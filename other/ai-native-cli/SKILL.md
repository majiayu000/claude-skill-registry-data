---
name: ai-native-cli
description: >
  AI-Native CLI design spec. Use when building CLI tools, designing
  command-line interfaces, or scaffolding new CLI projects. Covers
  structured JSON output, error handling, input contracts, safety
  guardrails, exit codes, and agent self-description. Includes an
  audit protocol for verifying CLI compliance.
license: MIT
metadata:
  author: zhuanz
  version: "0.2.0"
---

# Agent-Friendly CLI Spec v0.1

When building or modifying CLI tools, follow these rules to make them safe and
reliable for AI agents to use.

## Core Philosophy

1. **Agent-only** -- output is always JSON, no human-friendly mode
2. **Agent is untrusted** -- validate all input at the same level as a public API
3. **Fail-Closed** -- when validation logic itself errors, deny by default
4. **Verifiable** -- every rule is written so it can be automatically checked

## Layer Model

This spec now uses two orthogonal axes:

- **Layer** answers rollout scope: `core`, `recommended`, `ecosystem`
- **Priority** answers severity: `P0`, `P1`, `P2`

Use layers for migration and certification:

- **core** -- execution contract: JSON, errors, exit codes, stdout/stderr, safety
- **recommended** -- better machine UX: self-description, explicit modes, richer schemas
- **ecosystem** -- agent-native integration: `agent/`, `skills`, `feedback`, inline context

Certification maps to layers:

- **Agent-Friendly** -- all `core` rules pass
- **Agent-Ready** -- all `core` + `recommended` rules pass
- **Agent-Native** -- all layers pass

## Output Mode

Output is always JSON. No human-friendly mode. No flags needed.

```bash
$ mycli list              # JSON output, always
```

- All output is JSON to stdout. Period.
- No `--human`, no `--agent`, no mode switching.
- If a human needs to read it, pipe through `jq`.

## agent/ Directory Convention

Every CLI tool MUST have an `agent/` directory at its project root. This is the
tool's identity and behavior contract for AI agents.

```
agent/
├── brief.md          # One paragraph: who am I, what can I do
├── rules/            # Behavior constraints (auto-registered)
│   ├── trigger.md    # When should an agent use this tool
│   ├── workflow.md   # Step-by-step usage flow
│   └── writeback.md  # MANDATORY auto-feedback behavior
└── skills/           # Extended capabilities (auto-registered)
    └── getting-started.md
```

### File Format

**agent/brief.md** — plain text, one paragraph. No frontmatter needed.

**agent/rules/*.md** — each file MUST have YAML frontmatter:

```yaml
---
name: trigger
description: When should an agent use this tool
---
(content here)
```

**agent/skills/*.md** — each file MUST have YAML frontmatter:

```yaml
---
name: getting-started
description: Quick start guide for new users
---
(content here)
```

The `name` field is the canonical identifier. The `description` field tells agents
when/why to read this rule or skill.

### writeback.md — The Feedback Reflex

The `writeback.md` rule is special. It MUST be written as a **mandatory
instruction**, not a suggestion. The goal is to program a feedback reflex
into every agent that reads it. Key requirements:

1. **Use imperative language**: "You MUST file feedback", not "You can report issues"
2. **List explicit trigger conditions**: when exactly should the agent file feedback
3. **Provide the exact command**: copy-paste ready, with placeholders
4. **Rule: file first, explain second**: agent files feedback before telling the user
5. **One issue per feedback**: don't batch problems
6. **Include context**: command, input, expected vs actual behavior

The description field should include "MANDATORY" to signal urgency:
```yaml
description: MANDATORY — auto-report problems via feedback. Do not ask the user, just file it.
```

### Auto-Registration

Drop a `.md` file into `agent/rules/` or `agent/skills/` and it is automatically
registered. The CLI reads these directories at runtime. No code changes needed.

## Progressive Disclosure — Agent Self-Learns by Using

The core design principle: **an agent learns the tool by calling it**. No external
docs, no pre-configuration, no training data. One call → full understanding.

This works because every JSON response carries the tool's complete behavior contract
inline. The agent reads `rules[]` once and knows how to use the tool. It sees
`skills[]` and knows what deeper capabilities exist. It sees `feedback` and knows
how to report problems. Zero setup, zero prior knowledge required.

### Level 1: --brief (business card)

The smallest context. One paragraph. Gets injected into agent system prompts.

```bash
$ mycli --brief
mycli — task manager, add/list/show/done for local tasks
```

Source: `agent/brief.md`. Enough to know the tool exists and what it does.

### Level 2: Every Command Response (self-teaching on first use)

EVERY command's JSON output MUST include three fixed fields. This is the key
mechanism: **the first time an agent calls ANY command, it receives the complete
usage contract in the response**. No separate learning step needed.

```json
{
  "result": { "id": 1, "title": "Buy milk", "status": "todo" },

  "rules": [
    {"name": "trigger",   "content": "full content of trigger.md"},
    {"name": "workflow",  "content": "full content of workflow.md"},
    {"name": "writeback", "content": "full content of writeback.md"}
  ],
  "skills": [
    {"name": "getting-started", "description": "Quick start guide", "command": "mycli skills getting-started"},
    {"name": "batch-import",    "description": "Import from CSV",   "command": "mycli skills batch-import"}
  ],
  "feedback": "Any problem, bad output, or confusion — run: mycli feedback create --type <bug|requirement|suggestion|bad-output> --message '...'"
}
```

- **rules** — full `.md` content inline, pushed on every call. Agent absorbs them
  automatically. Contains: when to use this tool (trigger), how to use it step by
  step (workflow), how to report problems (writeback). After one call, the agent
  knows everything it needs.
- **skills** — name + description + command. Agent sees what's available and pulls
  on demand when needed. Progressive: learns basics from rules first, goes deeper
  via skills only when the task requires it.
- **feedback** — one-line instruction, always present. Not optional, not an
  escape hatch — it is the **default error-handling behavior**. When an agent
  encounters unexpected output, a confusing response, a bug, or has a feature
  need, it SHOULD immediately call `feedback create` without being asked.
  The feedback field teaches this reflex on every single response.

This forms a closed self-learning + self-healing loop:
  rules teach how → skills teach more → feedback auto-reports problems

**Feedback is automatic, not manual.** The agent sees the feedback instruction
on every call. When something goes wrong, it doesn't ask the user what to do —
it files feedback, stored in `{PROJECT}/feedback/` as a git-tracked artifact.
This means: problems get captured the moment they happen, in code, reviewable,
never lost.

No external CLAUDE.md rules. No AGENTS.md configuration. No README reading.
The tool teaches itself to every agent that calls it, and the agent teaches
the tool what's broken.

### Level 3: --help (full self-description)

Complete identity + capabilities. Only called for deep exploration.

```json
{
  "help": "mycli — full description from agent/brief.md",
  "commands": [
    {"name": "add",  "description": "Create a new task"},
    {"name": "list", "description": "List all tasks"},
    {"name": "done", "description": "Mark task as done (destructive)"}
  ],
  "rules": [
    {"name": "trigger",   "content": "..."},
    {"name": "workflow",  "content": "..."},
    {"name": "writeback", "content": "..."}
  ],
  "skills": [
    {"name": "getting-started", "description": "Quick start guide", "command": "mycli skills getting-started"}
  ],
  "feedback": "Any problem — run: mycli feedback create ..."
}
```

### Level 4: skills <name> (on-demand deep dive)

```bash
$ mycli skills getting-started
{
  "name": "getting-started",
  "content": "full content of getting-started.md",
  "rules": [ ... same rules for context ... ]
}
```

### Summary: Information Architecture

```
--brief              → always in agent's prompt (via sync-agent)
every command        → data + rules + skills list + feedback (always attached)
--help               → brief + commands + rules + skills + feedback (first contact)
skills <name>        → full skill content + rules (on demand)
```

## Certification Requirements

Each level includes all rules from the previous level.
Priority tag `[P0]`=agent breaks without it, `[P1]`=agent works but poorly, `[P2]`=nice to have.

### Level 1: Agent-Friendly (core — 20 rules)

Goal: CLI is a stable, callable API. Agent can invoke, parse, and handle errors.

**Output** — default is JSON, stable schema
- `[P0]` O1: Default output is JSON. No `--json` flag needed
- `[P0]` O2: JSON MUST pass `jq .` validation
- `[P0]` O3: JSON schema MUST NOT change within same version

**Error** — structured, to stderr, never interactive
- `[P0]` E1: Errors → `{"error":true, "code":"...", "message":"...", "suggestion":"..."}` to stderr
- `[P0]` E4: Error has machine-readable `code` (e.g. `MISSING_REQUIRED`)
- `[P0]` E5: Error has human-readable `message`
- `[P0]` E7: On error, NEVER enter interactive mode — exit immediately
- `[P0]` E8: Error codes are API contracts — MUST NOT rename across versions

**Exit Code** — predictable failure signals
- `[P0]` X3: Parameter/usage errors MUST exit 2
- `[P0]` X9: Failures MUST exit non-zero — never exit 0 then report error in stdout

**Composability** — clean pipe semantics
- `[P0]` C1: stdout is for data ONLY (JSON result, buffered until complete)
- `[P0]` C2: logs, progress, warnings go to stderr ONLY
- `[P1]` C8: Progress MUST stream to stderr in real-time, not buffer until exit. For long-running operations, agent must see what's happening during execution, not just the final result.

**Input** — fail fast on bad input
- `[P1]` I4: Missing required param → structured error, never interactive prompt
- `[P1]` I5: Type mismatch → exit 2 + structured error

**Safety** — protect against agent mistakes
- `[P1]` S1: Destructive ops require `--yes` confirmation
- `[P1]` S4: Reject `../../` path traversal, control chars

**Guardrails** — runtime input protection
- `[P1]` G1: Unknown flags rejected with exit 2
- `[P1]` G2: Detect API key / token patterns in args, reject execution
- `[P1]` G3: Reject sensitive file paths (*.env, *.key, *.pem)
- `[P1]` G8: Reject shell metacharacters in arguments (; | && $())

### Level 2: Agent-Ready (+ recommended — 59 rules)

Goal: CLI is self-describing, well-named, and pipe-friendly. Agent discovers capabilities and chains commands without trial and error.

**Self-Description** — agent discovers what CLI can do
- `[P1]` D1: `--help` outputs structured JSON with `commands[]`
- `[P1]` D3: Schema has required fields (help, commands)
- `[P1]` D4: All parameters have type declarations
- `[P1]` D7: Parameters annotated as required/optional
- `[P1]` D9: Every command has a description
- `[P1]` D11: `--help` outputs JSON with help, rules, skills, feedback, commands
- `[P1]` D15: `--brief` outputs `agent/brief.md` content
- `[P1]` D16: Output is always JSON, no human mode
- `[P2]` D2/D5/D6/D8/D10: per-command help, enums, defaults, output schema, version

**Input** — unambiguous calling convention
- `[P1]` I1: All flags use `--long-name` format
- `[P1]` I2: No positional argument ambiguity
- `[P2]` I3/I6/I7: --json-input, boolean --no-X, array params

**Error**
- `[P1]` E6: Error includes `suggestion` field
- `[P2]` E2/E3: errors to stderr, error JSON valid

**Safety**
- `[P1]` S8: `--sanitize` flag for external input
- `[P2]` S2/S3/S5/S6/S7: default deny, --dry-run, no auto-update, destructive marking

**Exit Code**
- `[P1]` X1: 0 = success
- `[P2]` X2/X4-X8: 1=general, 10=auth, 11=permission, 20=not-found, 30=conflict

**Composability**
- `[P1]` C6: No interactive prompts in pipe mode
- `[P2]` C3/C4/C5/C7: pipe-friendly, --quiet, pipe chain, idempotency

**Naming** — predictable flag conventions
- `[P1]` N4: Reserved flags (--brief, --help, --version, --yes, --dry-run, --quiet, --fields)
- `[P2]` N1/N2/N3/N5/N6: consistent naming, kebab-case, max 3 levels, --version semver

**Guardrails**
- `[P1]` I8/I9: no implicit state, non-interactive auth
- `[P1]` G6/G9: precondition checks, fail-closed
- `[P2]` G4/G5/G7: permission levels, PII redaction, batch limits

#### Reserved Flags

| Flag | Semantics | Notes |
|------|-----------|-------|
| `--brief` | One-paragraph identity | For sync into agent config |
| `--help` | Full self-description JSON | Brief + commands + rules + skills + feedback |
| `--version` | Semver version string | |
| `--yes` | Confirm destructive ops | Required for delete/destroy |
| `--dry-run` | Preview without executing | |
| `--quiet` | Suppress rules/skills/feedback from response, return result only. Saves tokens for agents that already learned the tool. | |
| `--fields` | Filter output fields | Save tokens |

### Level 3: Agent-Native (+ ecosystem — 19 rules)

Goal: CLI has identity, behavior contract, skill system, and feedback loop. Agent can learn the tool, extend its use, and report problems — full closed-loop collaboration.

**Agent Directory** — tool identity and behavior contract
- `[P1]` D12: `agent/brief.md` exists
- `[P1]` D13: `agent/rules/` has trigger.md, workflow.md, writeback.md
- `[P1]` D17: agent/rules/*.md have YAML frontmatter (name, description)
- `[P1]` D18: agent/skills/*.md have YAML frontmatter (name, description)
- `[P2]` D14: `agent/skills/` directory + `skills` subcommand

**Response Structure** — inline context on every call
- `[P1]` R1: Every response includes `rules[]` (full content from agent/rules/)
- `[P1]` R2: Every response includes `skills[]` (name + description + command)
- `[P1]` R3: Every response includes `feedback` (feedback guide)

**Meta** — project-level integration
- `[P2]` M1: AGENTS.md at project root
- `[P2]` M2: Optional MCP tool schema export
- `[P2]` M3: CHANGELOG.md marks breaking changes

**Feedback** — built-in feedback system, stored in project code
- `[P1]` F1: `feedback` subcommand (create/list/show)
- `[P1]` F2: Structured submission with version/context/exit_code
- `[P1]` F3: Categories: bug / requirement / suggestion / bad-output
- `[P1]` F4: Feedback stored in project source (`{PROJECT}/feedback/`), committed to git
- `[P1]` F5: `feedback list` / `feedback show <id>` queryable
- `[P2]` F6: Feedback has status tracking (open/in-progress/resolved/closed)
- `[P2]` F7: Feedback JSON has all required fields (id, type, status, message, created_at, updated_at)
- `[P2]` F8: All feedback entries have status field

## Exit Code Table

```
0   success         10  auth failed       20  resource not found
1   general error   11  permission denied 30  conflict/precondition
2   param/usage error
```

## Error Format

```json
{
  "error": true,
  "code": "AUTH_EXPIRED",
  "message": "Access token expired 2 hours ago",
  "suggestion": "Run 'mycli auth refresh' to get a new token"
}
```

## Quick Implementation Checklist

Implement by layer — each phase gets you the next certification level.

**Phase 1: Agent-Friendly (core)**
1. Default output is JSON — no `--json` flag needed
2. Error handler: `{ error, code, message, suggestion }` to stderr
3. Exit codes: 0 success, 2 param error, 1 general
4. stdout = data only (buffered), stderr = logs/progress (real-time streamed)
5. Missing param → structured error (never interactive)
6. `--yes` guard on destructive operations
7. Guardrails: reject secrets, path traversal, shell metacharacters

**Phase 2: Agent-Ready (+ recommended)**
8. `--help` returns structured JSON (help, commands[], rules[], skills[])
9. `--brief` reads and outputs `agent/brief.md` content
10. Reserved flags: --version, --dry-run, --quiet, --fields
12. Exit codes: 20 not found, 30 conflict, 10 auth, 11 permission

**Phase 3: Agent-Native (+ ecosystem)**
13. Create `agent/` directory: `brief.md`, `rules/trigger.md`, `rules/workflow.md`, `rules/writeback.md`
14. Every command response appends: rules[] + skills[] + feedback
15. `skills` subcommand: list all / show one with full content
16. `feedback` subcommand (create/list/show/close/transition), stored in project source
17. AGENTS.md at project root

## Dogfooding — Build It, Then Use It

After implementing a CLI tool, you MUST dogfood it with subagents before
considering it done. This is not optional QA — it is part of the build process.

**Required dogfooding steps:**

1. **Self-audit**: Use the audit protocol (`references/audit.md`) to verify spec
   compliance. Run every dimension. Fix failures before shipping.

2. **Subagent testing**: Launch a subagent (or use `ally run/ask/plan`) to use
   your tool as a real consumer would. The subagent should:
   - Call `--help` and learn the tool from the response
   - Execute the core workflow described in `rules/workflow.md`
   - Hit edge cases: missing params, wrong types, unknown flags
   - File feedback via `feedback create` when something is wrong
   - Verify feedback was stored in `{PROJECT}/feedback/`

3. **Cross-tool testing**: If your tool integrates with others, test the
   integration. Use `ally compare` to run the same task through different tools
   and verify consistent behavior.

4. **Feedback review**: After dogfooding, check `feedback/` directory. Every
   filed feedback is a real bug or gap. Fix them or document why they're
   intentional.

The goal: **by the time a user touches your tool, every obvious failure has
already been caught by an agent and filed as feedback.**

## Feedback System Specification

Every CLI tool MUST have a built-in feedback system for agents to report problems,
request features, and track feedback. Feedback is a first-class project artifact —
it MUST be stored in the project source code and committed to version control.

### Storage

Feedback MUST be stored in the project's source directory, not in hidden user
directories. This ensures feedback is version-controlled and visible to all
contributors.

```
{PROJECT_ROOT}/feedback/
├── 001.json
├── 002.json
└── 003.json
```

Each feedback entry is a single JSON file named `{id}.json`.

**Why in project code, not `~/.toolname/`:**
- Feedback is a project artifact, not user-local state
- Git tracks who reported what and when
- Other developers and agents can see open feedback
- Code review catches feedback patterns (recurring bugs = design problem)
- Feedback survives machine changes

### Feedback Fields

```json
{
  "id": "001",
  "type": "bug",
  "status": "open",
  "message": "list command returns empty when tasks exist",
  "context": {
    "version": "0.1.0",
    "command": "mycli list --json",
    "exit_code": 0
  },
  "created_at": "2026-03-14T00:00:00Z",
  "updated_at": "2026-03-14T00:00:00Z"
}
```

Required fields:
- **id** — unique identifier
- **type** — one of: `bug`, `requirement`, `suggestion`, `bad-output`
- **status** — one of: `open`, `in-progress`, `resolved`, `closed`
- **message** — description of the feedback
- **context** — object with `version`, `command`, `exit_code`
- **created_at** — ISO 8601 timestamp
- **updated_at** — ISO 8601 timestamp

### State Management

| Command | Description |
|---------|-------------|
| `feedback create --type <type> --message <msg>` | Create new feedback entry |
| `feedback list [--type <type>] [--status <status>]` | List feedback, filterable |
| `feedback show <id>` | Show single feedback detail |
| `feedback close <id>` | Close a feedback entry |
| `feedback transition <id> --status <status>` | Change feedback status |

### Queryable

Feedback MUST be filterable by `--type` and `--status`:

```bash
$ mycli feedback list --type bug --status open
$ mycli feedback list --status resolved
