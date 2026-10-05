---
name: kb
category: core
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
version: 2.0.0
description: Use when querying and maintaining the knowledge base for project context, decisions, and architecture documentation on session start.
tags:
- infrastructure
- memory
- self-improvement
- para
- persistence
---

# Knowledge Base (KB)

## Overview

The Knowledge Base (KB) is a PARA-structured persistent memory system for AI agents.
It survives agent compactions, session boundaries, and context window limits by storing
facts, decisions, architecture records, and project state in files on disk.

**PARA stands for:**
- **P**rojects — active deliverables with deadlines
- **A**reas — ongoing responsibilities without end dates
- **R**esources — reference material, templates, cross-references
- **A**rchives — stale content, git-preserved, never deleted

The KB works alongside the `memory` MCP tools (`search_nodes`, `open_nodes`,
`read_graph`, `create_entities`, `add_observations`, `create_relations`) and the
file-based scratchpad pattern. Use all three layers together:

| Layer | Scope | Persistence | Example |
|---|---|---|---|
| KB files | Long-term org memory | Indefinite (git) | `~/kb/projects/foo/facts.yaml` |
| MCP knowledge graph | Relationship graph | Per-session + recall | Entities, relations, observations |
| Scratchpad file | Active session bridge | < 30 min | `~/.kb-session-context.md` |

## Workflow

The KB lifecycle follows a predictable loop across every agent session:

```
Session Start → Load Context → Check Decisions → Work & Capture → Log → Session End
```

### Per-Session Loop

1. **Cold start** — MCP server connects, scratchpad is checked for < 30 min state
2. **Load yesterday** — last session's End-of-Session Summary is retrieved
3. **Open decisions** — all facts with `status: open` across every category
4. **Work** — agent performs tasks, captures facts as they arise
5. **Log decisions** — every resolved decision gets a fact with `status: confirmed`
6. **End-of-Session** — summary written, scratchpad updated, git commit + brain save

### Weekly Loop

1. Archive projects untouched > 90 days
2. Prune stale observations
3. Rebuild entity cross-reference index
4. Review open decisions for closure
5. Verify all code blocks in KB skills parse correctly

---
## Querying the Knowledge Base

### Using MCP Memory Tools

The `memory` MCP server exposes a knowledge graph. Query it with structured tools:

**search_nodes** — find entities by name or pattern:

```python
# Python — via MCP
result = tool.memory_search_nodes(query="client-alpha")
for node in result.nodes:
    print(f"{node.name}: {node.entity_type}")
    for obs in node.observations:
        print(f"  - {obs}")
```

**open_nodes** — load full entity details including all observations and relations:

```python
nodes = tool.memory_open_nodes(names=["client-alpha", "website-redesign"])
for node in nodes:
    print(f"=== {node.name} ({node.entity_type}) ===")
    for obs in node.observations:
        print(f"  {obs}")
```

**read_graph** — dump the entire knowledge graph for cold-start initialization:

```python
graph = tool.memory_read_graph()
print(f"Entities: {len(graph.entities)}")
print(f"Relations: {len(graph.relations)}")
```

### Using Filesystem grep

When the MCP server is unavailable, fall back to filesystem tools:

```bash
# Find all facts about a specific entity
grep -r "entity: client-alpha" ~/kb/

# List all open decisions across every project
grep -r "status: open" ~/kb/projects/ --include="facts.yaml"

# Quick count of entities per category
for d in projects areas resources; do
    count=$(find ~/kb/$d -maxdepth 2 -name "facts.yaml" | wc -l)
    echo "$d: $count entities"
done

# Search daily notes for a keyword
rg "blocker" ~/kb/areas/daily/
```

---

## Writing to the Knowledge Base

### Creating Entities

Register a new entity in the knowledge graph:

```python
# Start tracking a project entity
tool.memory_create_entities([
    {
        "name": "client-alpha-website",
        "entityType": "project",
        "observations": [
            "Client: Alpha Corp",
            "Deadline: 2026-09-30",
            "Stack: Next.js + Tailwind + Supabase",
            "Status: in_progress"
        ]
    }
])
```

### Adding Observations

Add facts to an existing entity as you discover them:

```python
# Attach new facts mid-session
tool.memory_add_observations([
    {
        "entityName": "client-alpha-website",
        "observations": [
            "Decided: use Stripe for payments, not Paddle",
            "API contract: GET /api/projects returns paginated list",
            "Blocker: waiting for client to send brand assets"
        ]
    }
])
```

### Creating Relations

Link entities to model dependencies, influences, and ownership:

```python
# Wire up relationships between entities
tool.memory_create_relations([
    {
        "source": "client-alpha-website",
        "target": "payment-integration",
        "relationType": "depends_on"
    },
    {
        "source": "client-alpha-website",
        "target": "auth-patterns",
        "relationType": "references"
    },
    {
        "source": "alice",
        "target": "client-alpha-website",
        "relationType": "owns"
    }
])
```

### File-Based Storage (YAML)

Canonical writer for per-entity YAML fact files alongside the knowledge graph:

```python
import yaml
from datetime import datetime
from pathlib import Path

KB = Path.home() / "kb"

def save_fact(entity: str, category: str, value: str, **kw):
    """Append one fact to a per-entity YAML file.

    Args:
        entity: the thing being described (project, tool, client)
        category: 'projects', 'areas', or 'resources'
        value: the fact text
        **kw: optional metadata (status, priority, related, source)
    """
    dir_ = KB / category / entity
    dir_.mkdir(parents=True, exist_ok=True)
    facts_file = dir_ / "facts.yaml"

    facts = []
    if facts_file.exists():
        with open(facts_file) as f:
            facts = yaml.safe_load(f) or []

    facts.append({
        "value": value,
        "recorded_at": datetime.now().isoformat(),
        **kw
    })

    with open(facts_file, "w") as f:
        yaml.dump(facts, f, default_flow_style=False, sort_keys=False)

    return facts_file
```

---

## Maintenance

### Pruning Stale Observations

Knowledge graphs accumulate noise. Run periodic pruning:

```python
def prune_stale_observations(days_threshold=90):
    """Flag observations older than threshold for review."""
    from datetime import timedelta

    cutoff = datetime.now() - timedelta(days=days_threshold)
    stale = []

    for category in ["projects", "areas", "resources"]:
        for facts_file in (KB / category).rglob("facts.yaml"):
            with open(facts_file) as f:
                records = yaml.safe_load(f) or []

            fresh = []
            for rec in records:
                recorded = datetime.fromisoformat(rec["recorded_at"])
                if recorded < cutoff and rec.get("status") != "archived":
                    stale.append({
                        "file": str(facts_file),
                        "value": rec["value"],
                        "recorded_at": rec["recorded_at"]
                    })
                else:
                    fresh.append(rec)

            if len(fresh) != len(records):
                with open(facts_file, "w") as f:
                    yaml.dump(fresh, f, default_flow_style=False, sort_keys=False)

    return stale
```

### Weekly Review Checklist

- [ ] Move completed projects from `projects/` to `archives/`
- [ ] Delete observations marked "obsolete" or "superseded"
- [ ] Verify all open decisions still need resolution
- [ ] Run `entity-index-gen.py` to rebuild the cross-reference
- [ ] Check that today's daily note has an End-of-Session Summary

### Archiving Stale Content

```bash
#!/usr/bin/env bash
# archive-stale.sh — move projects untouched for 90+ days to archives
KB=~/kb
CUTOFF=$(date -d "90 days ago" +%s)

for dir in "$KB"/projects/*/; do
    last=$(git -C "$KB" log -1 --format="%at" -- "$dir" 2>/dev/null || echo 0)
    if [ "$last" -gt 0 ] && [ "$last" -lt "$CUTOFF" ]; then
        name=$(basename "$dir")
        mv "$dir" "$KB/archives/projects/$name"
        echo "Archived: $name"
    fi
done
```

---

## Session Start Routine

This is the critical cold-start flow every agent session should execute.

### Step 1 — Check the Scratchpad Bridge

```python
from pathlib import Path
from datetime import datetime, timedelta

SCRATCHPAD = Path.home() / ".kb-session-context.md"

def load_session_context():
    """Read the bridge file if it exists and is fresh (< 30 min)."""
    if not SCRATCHPAD.exists():
        return {"state": "cold_start", "context": {}}

    mtime = datetime.fromtimestamp(SCRATCHPAD.stat().st_mtime)
    if datetime.now() - mtime > timedelta(minutes=30):
        return {"state": "stale", "context": {}}

    text = SCRATCHPAD.read_text()
    context = {}
    for line in text.split("\n"):
        if line.startswith("- "):
            key, _, val = line[2:].partition(": ")
            context[key.lower()] = val

    return {"state": "warm", "context": context}
```

### Step 2 — Load the Knowledge Graph

```python
# Re-establish entity context
graph = tool.memory_read_graph()
stale_entities = [e.name for e in graph.entities
                  if "stale" in (e.observations or [])]

# Open entities related to today's focus
focus = "client-alpha"
related = tool.memory_open_nodes(names=[focus])

for node in related:
    print(f"Loaded: {node.name} — {len(node.observations)} observations")
```

### Step 3 — Create Today's Daily Note

```python
def ensure_daily_note():
    """Create today's note if it doesn't exist."""
    KB = Path.home() / "kb"
    today = datetime.now().strftime("%Y-%m-%d")
    note_file = KB / "areas" / "daily" / f"{today}.md"

    if note_file.exists():
        return note_file

    # Load yesterday's summary for continuity
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_file = KB / "areas" / "daily" / f"{yesterday}.md"
    yesterday_summary = ""
    if yesterday_file.exists():
        text = yesterday_file.read_text()
        if "## End-of-Session Summary" in text:
            yesterday_summary = text.split("## End-of-Session Summary", 1)[1]

    content = f"""# Daily Note: {today}

## Session Focus
_(What is the single most important outcome this session?)_

## Continuity Context
{yesterday_summary}

## Open Decisions Needing Input

## Plan
- [ ]

## Decisions Made Today

## End-of-Session Summary
_Write before closing — this bridges the next session._
"""
    note_file.parent.mkdir(parents=True, exist_ok=True)
    note_file.write_text(content)
    return note_file
```

### Step 4 — Load Open Decisions

```python
def load_open_decisions():
    """Return every entity fact with status=open."""
    KB = Path.home() / "kb"
    decisions = []

    for category in ["projects", "areas", "resources"]:
        for facts_file in (KB / category).rglob("facts.yaml"):
            with open(facts_file) as f:
                records = yaml.safe_load(f) or []

            for rec in records:
                if rec.get("status") in ("open", "pending"):
                    decisions.append({
                        "entity": facts_file.parent.name,
                        "category": category,
                        "value": rec["value"]
                    })

    return decisions
```

### Full Bash Session Starter

```bash
#!/usr/bin/env bash
# kb-session.sh — run at every agent session start
KB=~/kb
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d yesterday +%Y-%m-%d)
NOTE=$KB/areas/daily/$TODAY.md

# Step 1: Load yesterday's summary
if [ -f "$KB/areas/daily/$YESTERDAY.md" ]; then
    echo "=== Yesterday's Summary ==="
    sed -n '/## End-of-Session Summary/,$ p' \
        "$KB/areas/daily/$YESTERDAY.md" | head -20
fi

# Step 2: Check open decisions
echo ""
echo "=== Open Decisions ==="
grep -rl "status: open" "$KB"/{projects,areas,resources}/*/facts.yaml 2>/dev/null \
    | while read -r f; do
        entity=$(basename "$(dirname "$f")")
        grep -A1 "value:" "$f" | head -2
        echo "  (entity: $entity)"
    done || echo "  None"

# Step 3: Create today's note
if [ ! -f "$NOTE" ]; then
    cat > "$NOTE" <<EOF
# Daily Note: $TODAY

## Session Focus

## Decisions Made Today

## End-of-Session Summary

---
EOF
    echo ""
    echo "Created $NOTE — edit the focus line and begin."
fi
```

---

## Verification

- Save a project decision to the knowledge base, then query it back in a fresh session and confirm it retrieves.
- Verify PARA structure: content lands in the documented area (project/area/resource/archive) and is findable by search.
- Check cross-session recall: context loaded at session start includes the decision you stored.
- Confirm the KB stays consistent — updates to an existing note replace, not duplicate.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I remember what happened last session" | Agents lose everything on compaction. Without KB files, you start blank. |
| "The code comments are enough documentation" | Comments describe *what*; KB describes *why* you chose that approach. |
| "YAML facts are too structured for quick notes" | Unstructured daily notes cost nothing. Structure grows as the entity matures. |
| "I'll backfill facts when the project settles" | The gap between "I know this" and "I wrote this" is where information rot begins. |
| "grep is fast enough for recall" | grep finds text. Semantic relationships need the knowledge graph. |
| "My projects are too small for PARA" | PARA scales down to one file per entity. Starting flat means refactoring 200 files later. |
| "The scratchpad file is enough" | The scratchpad handles *active* bridging; the KB handles *permanent* organizational memory. |
| "Daily notes are for humans, not agents" | Agents read more daily notes than humans do — they have zero tacit context. |
| "I don't need relations — tags are fine" | Relations model causality and dependency. Tags model membership. Both are needed. |
| "Archiving is busywork" | Without archiving, every grep finds 3-year-old context about dead projects. |

---

## Verification Checklist

- [ ] `~/kb/{projects,areas,resources,archives}` directory tree exists
- [ ] Today's daily note is present at `~/kb/areas/daily/YYYY-MM-DD.md`
- [ ] Yesterday's daily note contains an End-of-Session Summary section
- [ ] `save_fact()` writes valid YAML re-readable with `yaml.safe_load()`
- [ ] Entity facts contain `recorded_at`, `value`, and `status` fields
- [ ] `load_open_decisions()` returns at least one result before cleanup
- [ ] Knowledge graph has at least 3 entity types registered
- [ ] Scratchpad bridge file is written on session end, checked on session start
- [ ] Scratchpad older than 30 minutes is treated as stale (not loaded)
- [ ] `prune_stale_observations(90)` returns no false positives
- [ ] All Python code blocks parse without syntax errors
- [ ] All bash code blocks pass `bash -n` syntax check
- [ ] Archive script has been run at least once
- [ ] YAML fact files are under git — `git log --oneline` shows fact history
- [ ] Weekly review checklist completed within the last 7 days

---

## When to Use

Use this skill when working with kb. Specifically:

- **Every session start** — load context, check open decisions, create daily note
- **After every decision** — capture as a YAML fact with `status: open` or
  `status: confirmed`
- **At session end** — write End-of-Session Summary, update scratchpad, commit
- **During investigations** — store entity facts as you discover them
- **Weekly** — review stale content, archive untouched projects
- **When spawning subagents** — share relevant KB entities via `local://` URIs
  so subagents start with context instead of cold
