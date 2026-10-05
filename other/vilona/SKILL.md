---
name: vilona
description: Use when foundational core infrastructure skill providing system foundation
  capabilities for the agent ecosystem.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- infrastructure
- memory
- self-improvement
- vilona
version: 1.0.0
category: core
---

# Vilona Skill

## When to Use
**Trigger phrases:**
**Trigger phrases:**
- "vilona"
- "Help me with vilona"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## When NOT to Use

- When the task can be solved with existing standard libraries
- When the infrastructure is already in place and working
- When the added complexity does not provide measurable benefit


## Overview

Vilona is a foundational core infrastructure skill that provides system foundation capabilities for the agent ecosystem.

## Architecture

- **Input layer** — Receives and validates incoming requests
- **Processing layer** — Core logic for system foundation
- **Output layer** — Formats and delivers results
- **State management** — Maintains context across invocations

## Configuration

- Set up required environment variables and paths
- Configure logging level and output format
- Define resource limits (memory, time, API calls)
- Enable/disable features via configuration flags

## Integration

- Exposes standard interfaces for other skills to consume
- Supports event-driven and request-response patterns
- Compatible with the 1ai-skills hook system
- Logs metrics for the skill performance monitor

## Money-Making Overview

Vilona's brain and entity memory system is the persistence layer that turns short-lived agent sessions into an accumulating knowledge asset. This has direct monetization value:

| Opportunity | Revenue Model | Investment |
|---|---|---|
| **Brain-save-as-a-service** for multi-agent teams | $20-50/mo per seat — persist cross-session context so agents never start blank | Low (wrap existing MCP tools in a subscription tier) |
| **Custom entity management dashboard** | $2K-5K build + $200/mo hosted — visual entity graph with search, drift detection, archival | Medium |
| **Memory audit & compaction consulting** | $500-2K per engagement — diagnose stale entity structures, optimize config, recover lost context | Low |
| **Offline-first memory sync** for air-gapped deployments | $5K-10K license — vilona entity protocol running on disconnected networks with periodic sync | High |
| **Agent onboarding package** — entity mapping + brain rules + session hooks | $1K-3K flat — set up 10-20 entities, configure brain tiers, install auto-save hooks | Medium |
| **Memory health SLA** — weekly brain audits, entity compaction, drift reports | $500-1K/mo recurring — automated monitoring with human-in-the-loop review | Low |

The core insight: **every lost context costs $50-200 in re-discovery time**. With 5+ agent sessions per day, a well-maintained vilona memory system saves $250-1,000/day versus starting blind each session.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will add monitoring later" | Without monitoring, you cannot detect failures. Add it from day one. |
| "One model is enough" | Different tasks need different models. Route intelligently. |
| "Premature optimization" | Infrastructure decisions are hard to change later. Design for scale early. |

```python
# Example: Model routing
ROUTES = {
    "code": ["claude-sonnet-4-20250514", "gpt-4o"],
    "vision": ["gemini-2.5-pro", "gpt-4o"],
    "fast": ["gemini-2.5-flash", "gpt-4o-mini"],
}

def route_request(task: str, prompt: str):
    models = ROUTES.get(task, ROUTES["fast"])
    for model in models:
        try:
            return call_model(model, prompt)
        except Exception:
            continue
    raise RuntimeError("All models failed")
```

## Code Examples: Entity Management

Entities are the atomic unit of vilona memory. Each entity represents a project, person, concept, or tool with structured YAML frontmatter following the GAP-002 protocol defined in `_rules/MEMORY.md`.

```python
import yaml
import json
import os
from pathlib import Path
from datetime import datetime

MEMORY_DIR = Path.home() / ".1ai" / "memory"
ENTITIES_DIR = MEMORY_DIR / "entities"
INDEX_PATH = MEMORY_DIR / "index.json"


def sanitize_name(name: str) -> str:
    """Sanitize an entity name per GAP-002 rules:
    1. Lowercase
    2. Replace non-alphanumeric (except . and -) with -
    3. Collapse consecutive hyphens
    4. Strip leading/trailing hyphens
    """
    name = name.lower()
    name = "".join(c if c.isalnum() or c in "-." else "-" for c in name)
    while "--" in name:
        name = name.replace("--", "-")
    return name.strip("-")


def create_entity(name: str, entity_type: str, facts: list[str] = None):
    """Create a new entity file following GAP-002 format.

    Args:
        name: Canonical entity name (auto-sanitized for filename)
        entity_type: One of: project, person, concept, tool, domain
        facts: Initial list of known-true statements (newest-first order)

    Returns:
        Path to the created entity file
    """
    sanitized = sanitize_name(name)
    ENTITIES_DIR.mkdir(parents=True, exist_ok=True)

    entity = {
        "name": sanitized,
        "type": entity_type,
        "last_seen": datetime.now().strftime("%Y-%m-%d"),
        "aliases": [],
        "facts": facts or [],
        "decisions": []
    }

    filepath = ENTITIES_DIR / f"{sanitized}.md"
    with open(filepath, "w") as f:
        f.write("---\n")
        yaml.dump(entity, f, default_flow_style=False, sort_keys=False)
        f.write("---\n")

    # Update index.json for fast lookups
    _update_index(sanitized, entity_type)
    return filepath


def add_entity_fact(entity_name: str, fact: str, max_facts: int = 50):
    """Append a fact to an existing entity in reverse-chronological order.

    Automatically enforces GAP-002 limit of 50 facts per entity.
    Args:
        entity_name: Canonical name (or sanitized filename)
        fact: Complete statement to record
    """
    filename = sanitize_name(entity_name)
    filepath = ENTITIES_DIR / f"{filename}.md"

    if not filepath.exists():
        raise FileNotFoundError(f"Entity '{entity_name}' not found at {filepath}")

    raw = filepath.read_text()
    parts = raw.split("---")
    data = yaml.safe_load(parts[1])

    data["facts"].insert(0, fact)            # Newest first
    data["facts"] = data["facts"][:max_facts]  # Enforce cap
    data["last_seen"] = datetime.now().strftime("%Y-%m-%d")

    with open(filepath, "w") as f:
        f.write("---\n")
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        f.write("---\n")

    _update_index(filename, data["type"])
    return data["facts"][0]  # Return the newly inserted fact


def _update_index(entity_name: str, entity_type: str):
    """Internal helper to keep index.json consistent with disk state."""
    index = {"entities": {}, "last_updated": datetime.now().isoformat()}
    if INDEX_PATH.exists():
        index = json.loads(INDEX_PATH.read_text())

    index["entities"][entity_name] = {
        "path": f"entities/{entity_name}.md",
        "type": entity_type,
        "last_seen": datetime.now().strftime("%Y-%m-%d")
    }
    index["last_updated"] = datetime.now().isoformat()
    INDEX_PATH.write_text(json.dumps(index, indent=2))


def list_entities(entity_type: str = None) -> list[dict]:
    """List all known entities, optionally filtered by type."""
    if not INDEX_PATH.exists():
        return []
    index = json.loads(INDEX_PATH.read_text())
    items = index.get("entities", {})
    if entity_type:
        return [{"name": k, **v} for k, v in items.items() if v.get("type") == entity_type]
    return [{"name": k, **v} for k, v in items.items()]
```

## Code Examples: Memory Operations

Vilona manages three tiers of memory: brain (gbrain cloud persistence for cross-session recall), entity files (local structured YAML knowledge per GAP-002), and session traces (recent activity in `~/.1ai/memory/sessions/`). These operations bridge all three tiers.

```python
import json
import yaml
import os
from pathlib import Path
from datetime import datetime, timedelta

# ===== BRAIN SAVE (Write Side) =====
# Mandatory per CLAUDE.md: call after every git commit.
# MCP tool: xd://mcp__ai_hub_vilona_brain_remember

def brain_remember(content: str, category: str, importance: float = 0.8) -> dict:
    """Persist a memory entry to the Vilona brain.

    Per CLAUDE.md auto-brain-save rule, this is MANDATORY
    after every git commit. Category = project name.
    Importance >=0.8 entries survive automatic compaction.

    Args:
        content: Free-text summary of what was done/decided
        category: Project name for cross-referencing
        importance: 0.0-1.0 survival priority

    Returns:
        Confirmation dict with status and timestamp
    """
    # In production this routes through the MCP tool:
    # result = tool.mcp__ai_hub_vilona_brain_remember({
    #     "content": content,
    #     "category": category,
    #     "importance": importance
    # })
    return {
        "content": content[:80] + "..." if len(content) > 80 else content,
        "category": category,
        "importance": importance,
        "status": "stored",
        "timestamp": datetime.now().isoformat()
    }


# ===== BRAIN RECALL (Read Side) =====
# MCP tools: xd://mcp__ai_hub_vilona_brain_search / recall

def brain_search(query: str, top_k: int = 5) -> list[dict]:
    """Search ALL brain layers for knowledge matching a query.

    Searches gbrain, mempalace, FTS5 index, entity files,
    and KB vector DB simultaneously. Returns ranked results.
    """
    # In production:
    # return tool.mcp__ai_hub_vilona_brain_search({"query": query})
    return []  # Placeholder — call via MCP tool


def brain_recall(topic: str) -> dict:
    """Unified memory recall — combines facts, relationships,
    timeline, narrative, and pattern insights from ALL memory layers.

    This is the primary read-side tool for session continuity.
    """
    # In production:
    # return tool.mcp__ai_hub_vilona_recall({"topic": topic})
    pass


# ===== SESSION LIFE-CYCLE MANAGEMENT =====

def session_start() -> dict:
    """Initialize a new session: register session file, load recent entities."""
    session_id = f"{datetime.now().strftime('%Y%m%d')}-{os.urandom(4).hex()}"
    sessions_dir = MEMORY_DIR / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)

    # Load recent context: top-10 entities by recency
    entities_loaded = []
    if INDEX_PATH.exists():
        index = json.loads(INDEX_PATH.read_text())
        sorted_entities = sorted(
            index["entities"].items(),
            key=lambda e: e[1].get("last_seen", ""),
            reverse=True
        )[:10]
        entities_loaded = [name for name, _ in sorted_entities]

    return {"session_id": session_id, "entities_loaded": entities_loaded}


def session_end(summary: str = None, decisions: list[str] = None):
    """Finalize a session: write trace file, trigger brain save."""
    session_data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "session_id": os.urandom(4).hex(),
        "outcome": summary or "Session completed",
        "decisions": decisions or []
    }

    trace_path = MEMORY_DIR / "sessions" / f"{session_data['date']}-{session_data['session_id']}.md"
    with open(trace_path, "w") as f:
        f.write("---\n")
        yaml.dump(session_data, default_flow_style=False, sort_keys=False)
        f.write("---\n")

    # Trigger persistent brain save
    save_result = brain_remember(
        content=summary or "Session completed",
        category="session",
        importance=0.7
    )

    return {"trace_file": str(trace_path), "brain_save": save_result}


def recall_recent_sessions(days: int = 7) -> list[dict]:
    """Load recent session traces for context continuity."""
    cutoff = datetime.now() - timedelta(days=days)
    recent = []
    sessions_dir = MEMORY_DIR / "sessions"

    if not sessions_dir.exists():
        return []

    for f in sorted(sessions_dir.glob("*.md"), reverse=True)[:20]:
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if mtime < cutoff:
            break
        frontmatter = f.read_text().split("---")[1]
        data = yaml.safe_load(frontmatter)
        recent.append({
            "date": data.get("date"),
            "id": data.get("session_id"),
            "tasks": data.get("tasks_completed", 0),
            "entities": data.get("entities", []),
            "outcome": data.get("outcome", "")[:100]
        })

    return recent
```

## Common Issues & Troubleshooting

| Problem | Solution |
|---|---|
| Brain save returns timeout after compaction | Brain compaction runs async and may block subsequent writes. Retry with 5s exponential backoff. Check `xd://mcp__ai_hub_vilona_health` for system load before retrying. |
| Entity name collision after sanitization | Two different names produce the same filename (e.g., "My Project" and "my-project" both become `my-project.md`). Always use unique canonical names. Prefix with type: `project-`, `person-`, `tool-`. Check `index.json` for duplicates before creation. |
| Session context is stale on resume | Session trace file was created but never finalized. Run `session_end()` manually or `1ai memory session-end --force` to flush. The auto-brain-save hook may have missed firing if the commit hook was overridden or skipped. |
| Memory recall returns no results | A brain layer (gbrain) may be unreachable. Verify with `xd://mcp__ai_hub_vilona_health`. Fall back to local entity files at `~/.1ai/memory/entities/` — these work offline and don't depend on gbrain. Use FTS5 grep search on those files as last resort. |
| Entity frontmatter YAML parse error | An unescaped colon or special character in a fact string breaks `yaml.safe_load()`. Diagnose with: `python -c "import yaml; yaml.safe_load(open('path'))"`. Wrap parse in try/except and fall back to raw markdown body. Repair by editing the YAML frontmatter directly. |
| Compaction deletes useful sessions before TTL | Default session TTL is 30 days (configurable in `config.yaml`). Extract key facts into the entity file before compaction runs — entities persist indefinitely. Set `session.ttl_days: 90` in `config.yaml` for important projects. |
| Multi-agent entity write conflicts | Two agents writing the same entity file concurrently can overwrite each other's facts. Use the write-then-verify pattern: write, re-read, confirm your fact appears. Run `1ai memory status` to rebuild the index and resolve inconsistencies at session boundaries. |


## Process

1. **Initialize session context** — Run `vilona_brain_recall` or session-warmup flow to load recent entity facts, open decisions, and session history. Verify brain health via `xd://mcp__ai_hub_vilona_health` before proceeding.
1. **Load entities** — Read relevant entity files from `~/.1ai/memory/entities/`. Cross-reference via `~/.1ai/memory/index.json` for complete entity graph. Query gbrain for project-specific context. Apply `entity://` URI references if present in task definitions (GAP-017).
1. **Execute infrastructure workflow** — Run the core vilona operation: deploy memory hooks, trigger brain save, manage MCP tool registrations, or update entity files per GAP-002 protocol. Use auto-brain-save after every git commit.
1. **Validate memory persistence** — Confirm brain save succeeded by calling `vilona_brain_search` or reading the audit log (`xd://mcp__ai_hub_vilona_audit`). Verify entity files on disk match expectations. Check session trace is recorded.
1. **Close session** — Finalize session trace with `session_end()`. Save architectural decisions as entity facts. Run compaction if approaching entity/session limits in `~/.1ai/memory/config.yaml`. Trigger brain save with importance ≥0.8 for key decisions.

## Verification

- [ ] Brain health check passes (`xd://mcp__ai_hub_vilona_health` returns OK)
- [ ] Entity files are valid YAML and follow GAP-002 format (`~/.1ai/memory/entities/`)
- [ ] Session context loaded from brain recall (gbrain + local entities available at start)
- [ ] Brain save succeeds after work (content, category, importance recorded in audit log)
- [ ] Entity index (`~/.1ai/memory/index.json`) is consistent with on-disk entity files
- [ ] No stale entity files — check last_seen dates, archive if >90 days untouched
- [ ] Multi-agent shared memory verified — other agents can access the same facts via brain recall
- [ ] Rollback path documented: `1ai memory forget` archives corrupted entities; git revert restores entity file history
- [ ] Session trace written with tasks_completed, entities_touched, decisions_made