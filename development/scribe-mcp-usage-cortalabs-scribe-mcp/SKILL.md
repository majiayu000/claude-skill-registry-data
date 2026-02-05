---
name: scribe-mcp-usage
description: Operate the local Scribe MCP tools for logging, project setup, manage_docs workflows, read_file usage, bridge integrations, and sentinel/project mode discipline. Use whenever you need to follow Scribe tool contracts, document management rules, or bridge development.
---

# Scribe MCP Usage

## Navigation (progressive disclosure)
Start here, then open only what you need:

### Core Workflow
- `references/quickstart.md` — minimal correct workflow for any session.
- `references/INDEX.md` — how to search fast across references.
- `references/Operational_Contract.md` — full rules, tool signatures, manage_docs schemas.
- `references/Scribe_Usage.md` — canonical tool usage and examples.

### Tools
- `references/manage_docs.md` — manage_docs details and examples.
- `references/read_file.md` — read_file modes, scope rules, and examples.
- `references/logging.md` — logging discipline and reasoning block.

### Modes & Rules
- `references/modes.md` — project vs sentinel mode rules.
- `references/doc_naming.md` — doc_name vs doc_category rules.

### Bridge System (External MCP Integration)
- `references/bridges/INDEX.md` — bridge system overview and navigation.
- `references/bridges/quickstart.md` — get a bridge running in 5 minutes.
- `references/bridges/manifest.md` — YAML manifest schema reference.
- `references/bridges/plugin.md` — BridgePlugin API reference.
- `references/bridges/hooks.md` — hook lifecycle and execution.
- `references/bridges/permissions.md` — permission system and access control.
- `references/bridges/tools.md` — tool wrapping and custom tools.
- `references/bridges/admin_cli.md` — admin CLI commands.

### Templates
- `assets/templates/` — managed doc templates (research/bug/review/agent card/logs).
- `assets/templates/bridge/` — bridge manifest and plugin templates.

## Non-negotiables (short)
- Use MCP tools directly; no manual substitutes.
- Log after meaningful actions with a reasoning block.
- Use `read_file` for file contents; avoid shell reads.
- Bridges must implement `on_activate()`, `on_deactivate()`, `health_check()`.

---

## manage_docs Quick Reference

### 7 Primary Actions

| Action | Purpose | Required Params |
|--------|---------|-----------------|
| `create` | Create new doc (research/bug/custom) | `doc_name`, `metadata.doc_type` |
| `replace_section` | Replace content by section anchor | `doc_name`, `section`, `content` |
| `apply_patch` | Apply unified diff patch | `doc_name`, `edit` or `patch` |
| `replace_range` | Replace explicit line range | `doc_name`, `start_line`, `end_line`, `content` |
| `replace_text` | Find/replace text pattern | `doc_name`, `metadata.find`, `metadata.replace` |
| `append` | Append content to doc/section | `doc_name`, `content` |
| `status_update` | Update checklist item status | `doc_name`, `section`, `metadata` |

### Global Optional Params
- `project` — cross-project override
- `dry_run` — preview without applying
- `target_dir` — custom target for CREATE

### doc_type Values (INSIDE metadata)
`custom` (default), `research`, `bug`, `review`, `agent_card`

### Create Examples
```python
# Research doc
manage_docs(
    action="create",
    doc_name="RESEARCH_AUTH_20251119",
    metadata={"doc_type": "research", "research_goal": "Analyze auth flow"}
)

# Bug report (doc_name auto-generated)
manage_docs(
    action="create",
    metadata={
        "doc_type": "bug",
        "category": "logic",
        "slug": "auth_leak",
        "severity": "high",
        "title": "Auth token not invalidated"
    }
)

# Custom doc
manage_docs(
    action="create",
    doc_name="COORDINATION_PROTOCOL",
    metadata={"doc_type": "custom", "body": "# Protocol\n\nContent..."}
)
```

### Edit Examples
```python
# Replace section
manage_docs(
    action="replace_section",
    doc_name="architecture",
    section="problem_statement",
    content="## Problem Statement\nNew content here..."
)

# Update checklist
manage_docs(
    action="status_update",
    doc_name="checklist",
    section="phase_1_task_1",
    metadata={"status": "done", "proof": "PR #123 merged"}
)

# Append to section
manage_docs(
    action="append",
    doc_name="architecture",
    section="constraints",
    content="- New constraint added",
    metadata={"position": "inside"}
)

# Replace text (find/replace)
manage_docs(
    action="replace_text",
    doc_name="architecture",
    metadata={"find": "old_term", "replace": "new_term", "replace_all": True}
)

# Replace line range
manage_docs(
    action="replace_range",
    doc_name="phase_plan",
    start_line=45,
    end_line=50,
    content="New content for these lines"
)
```

### Deprecated Actions (still work, route to create)
- `create_research_doc` → `create(metadata={"doc_type": "research"})`
- `create_bug_report` → `create(metadata={"doc_type": "bug"})`
- `create_doc` → `create(metadata={"doc_type": "custom"})`

### Hidden Actions (advanced use)
`list_sections`, `list_checklist_items`, `normalize_headers`, `generate_toc`, `validate_crosslinks`, `search`, `batch`
