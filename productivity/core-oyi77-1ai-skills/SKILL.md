---
name: core
description: Use when knowledge base hub — PARA-structured company memory combining
  company-kb and kb for persistent context, project documentation, and agent recall
  across sessions. Use when working with knowledge base, company knowledge, or persistent
  memory.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- knowledge-base
- memory
- para
- infrastructure
- company
- context
- recall
persona:
  name: Knowledge Base Steward
  title: Master of Organizational Memory
  expertise:
  - Knowledge Management
  - PARA Method
  - Agent Context Engineering
  - Information Architecture
  philosophy: Memory without structure is noise. Structure without recall is a graveyard.
  credentials:
  - Knowledge systems architect
  - Information retrieval specialist
  - Multi-session context engineer
  principles:
  - Write once, retrieve forever
  - Structure for the next agent, not for today
  - Decay is real — refresh or retire
  - Every session starts with context, never blank
version: 1.0.0
category: core
---
## Overview

This skill is the knowledge base hub: PARA-structured company memory combining the company-kb and kb skills for persistent context and project documentation. Use it for cross-session recall and organizational memory. It defines how knowledge is captured, filed, and retrieved.



# Core Knowledge Base Hub — Company Memory & Recall



## Process

Maintain the knowledge base as a live PARA-structured memory that every session reads on start.

1. **Initialize structure** — create the project/area/resource/archive areas if the KB is new.
2. **Capture context** — record current session context, decisions, today's focus, open tasks, and follow-ups in the documented files.
3. **File deliberately** — place each note in the area that makes it findable by the query path, not wherever it was written.
4. **Query on session start** — load context at the beginning of each session so decisions persist across sessions.
5. **Maintain** — update existing notes in place (replace, not duplicate) and archive completed work.

## When Not to Use

- **Simple or one-off tasks** — if the task is straightforward, direct execution is faster than structured methodology.
- **Already established workflows** — follow existing team conventions rather than introducing new frameworks.
- **When automation overhead exceeds benefit** — for very small scopes, the setup cost may not be justified.


## Dependencies

- Python 3.8+ or Node.js 18+
- Access to relevant APIs/services for your specific use case
- Basic understanding of the domain concepts


## Commands

```bash
# Refer to the skill's usage section for specific commands
# Adapt these to your workflow
```
## Money-Making Overview

A well-structured knowledge base is the single highest-leverage investment for an autonomous agent ecosystem. Every hour spent organizing knowledge saves 10 hours of re-discovery and context-switching. Direct revenue impact:

| Capability | ROI Impact | Timeline |
|---|---|---|
| Session-start context loading | Eliminates 10-15 min of re-orientation per session | Day 1 |
| Company knowledge recall | Instant access to strategies, playbooks, finance data | Day 1 |
| PARA-structured memory | Find any document in < 30 seconds vs 10+ minutes | Day 2 |
| Entity-relationship graph | Cross-reference decisions, clients, projects instantly | Week 1 |
| Multi-agent shared memory | All agents operate from the same truth source | Week 1 |
| Auto-decay and archival | Memory stays lean — no information rot | Ongoing |

**Total addressable value:** A mature knowledge base turns a 1-person operation into a 10-person operation by eliminating context loss. Every lost context costs $50-200 in re-discovery time. With 5+ sessions per day, that's $250-1,000/day saved.

## Combined Capabilities

| Capability | kb | company-kb | Combined Power |
|---|---|---|---|
| PARA file structure | Core | — | Unified memory hierarchy |
| Company-specific docs | — | Core | Products, team, procedures, history |
| Session brain / daily notes | Core | — | Session-to-session context continuity |
| Multi-agent read/write | Core | Core | Shared truth source for all agents |
| Semantic search (embedding) | — | — | Vector-aware recall across all knowledge |
| YAML atomic facts | Core | — | Machine-readable structured knowledge |
| Natural-language retrieval | Core | — | "What did we decide about pricing?" |
| Knowledge lifecycle (decay) | Core | — | Auto-archive stale entries |
| Cross-referencing entities | Core | — | Link decisions to projects, people, dates |
| Agent accountability records | — | Core | Track who updated what and when |

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                  AI Agents                        │
│  (Vilona, Paijo, Task Agents, Specialist Agents)  │
└──────────────────────┬──────────────────────────┘
                       │ query / write
                       ▼
┌─────────────────────────────────────────────────┐
│            Knowledge Base Hub                    │
│                                                   │
│  ┌─────────────────┐  ┌──────────────────────┐  │
│  │   kb             │  │   company-kb          │  │
│  │  - PARA access   │  │  - Company entities   │  │
│  │  - Daily notes   │  │  - Products/services  │  │
│  │  - Atomic facts  │  │  - Procedures/playbks │  │
│  │  - Entity graph  │  │  - Team & operations  │  │
│  │  - Decay engine  │  │  - Client history     │  │
│  └────────┬─────────┘  └──────────┬───────────┘  │
│           │                        │              │
└───────────┼────────────────────────┼──────────────┘
            │                        │
            ▼                        ▼
┌─────────────────────────────────────────────────┐
│              PARA File System                    │
│                                                   │
│  projects/        areas/         resources/       │
│  ├── client-a     ├── finance    ├── templates    │
│  ├── mcp-tools    ├── marketing  ├── frameworks   │
│  └── website      ├── devops     └── references   │
│                    └── compliance                  │
│  archives/                                         │
│  └── (stale content auto-moved here)               │
└─────────────────────────────────────────────────┘
```

## First Action in 60 Minutes

### Phase 1: Initialize Knowledge Base Structure (10 min)
```bash
# 1. Verify PARA directory structure exists
ls -la ~/kb/projects/
ls -la ~/kb/areas/
ls -la ~/kb/resources/
ls -ka ~/kb/archives/

# 2. Read today's context — loads session memory
kb read --today
# Expected: daily note with yesterday's summary, current tasks, open decisions

# 3. Quick scan of company entities
company-kb list-entities --type all
company-kb list-entities --type client
company-kb list-entities --type product
```

### Phase 2: Capture Current Session Context (15 min)
```python
import os
from datetime import datetime
from pathlib import Path
import yaml

KB_ROOT = Path(os.environ.get("KB_ROOT", "~/kb")).expanduser()

def ensure_para_dirs():
    """Create PARA directory structure if missing."""
    for category in ["projects", "areas", "resources", "archives"]:
        (KB_ROOT / category).mkdir(parents=True, exist_ok=True)
    print("PARA structure ready")

def write_daily_note(date: datetime = None):
    """Write a session-start daily note with today's plan."""
    date = date or datetime.now()
    daily_dir = KB_ROOT / "areas" / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)

    note_path = daily_dir / f"{date.strftime('%Y-%m-%d')}.md"
    if note_path.exists():
        # Load existing and append session
        existing = note_path.read_text()
        note_path.write_text(f"{existing}\n\n## Session {date.strftime('%H:%M')}\n- ")
        print(f"Appended to existing note: {note_path}")
    else:
        content = f"""# Daily Note: {date.strftime('%Y-%m-%d')}

## Today's Focus
- 

## Tasks
- [ ] 

## Open Decisions
- 

## Follow-ups
- 

## Notes
- 

---
*Auto-generated by KB Hub at {date.isoformat()}*
"""
        note_path.write_text(content)
        print(f"Created daily note: {note_path}")

# Initialize
ensure_para_dirs()
write_daily_note()
```

### Phase 3: Store Atomic Knowledge Facts (15 min)
```python
import yaml

def store_fact(category: str, entity: str, fact: dict):
    """Store a structured fact as YAML in the knowledge base.

    category: 'projects', 'areas', 'resources'
    entity: name of the thing this fact describes
    fact: dict with keys like 'type', 'value', 'source', 'date', 'status'
    """
    # Determine file path
    if category == "projects":
        dir_path = KB_ROOT / "projects" / entity
    elif category == "areas":
        dir_path = KB_ROOT / "areas" / entity
    else:
        dir_path = KB_ROOT / "resources" / entity

    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / "facts.yaml"

    # Load existing or create
    facts = []
    if file_path.exists():
        with open(file_path) as f:
            facts = yaml.safe_load(f) or []

    # Append new fact
    facts.append({
        **fact,
        "recorded_at": datetime.now().isoformat(),
        "recorded_by": "kb-hub"
    })

    with open(file_path, "w") as f:
        yaml.dump(facts, f, default_flow_style=False, sort_keys=False)

    print(f"Stored fact in {file_path}")
    return file_path

# Examples — store immediately useful facts
store_fact("resources", "mcp-clients", {
    "type": "capability",
    "value": "MCP client hub connects agents to 50+ servers",
    "status": "active",
    "priority": "high"
})

store_fact("areas", "pricing-strategy", {
    "type": "decision",
    "value": "Standard tier at $49/mo, Pro tier at $99/mo",
    "date": "2026-07-01",
    "status": "confirmed"
})

store_fact("projects", "website-redesign", {
    "type": "milestone",
    "value": "Design review completed, dev started",
    "status": "in-progress",
    "target": "2026-08-01"
})
```

### Phase 4: Query and Recall (20 min)
```python
def query_kb(search_term: str, max_results: int = 10):
    """Full-text search across entire knowledge base."""
    import subprocess

    results = []
    query = subprocess.run(
        ["rg", "-l", "-i", search_term, str(KB_ROOT)],
        capture_output=True, text=True, timeout=10
    )

    for file_path in query.stdout.strip().split("\n"):
        if not file_path:
            continue

        # Extract a snippet
        snippet = subprocess.run(
            ["rg", "-i", "-m", "3", search_term, file_path],
            capture_output=True, text=True, timeout=5
        )

        rel_path = Path(file_path).relative_to(KB_ROOT)
        results.append({
            "file": str(rel_path),
            "snippet": snippet.stdout.strip()[:300],
            "lines": snippet.stdout.count("\n") + 1
        })

        if len(results) >= max_results:
            break

    if not results:
        print(f"No results for '{search_term}'")
        return []

    print(f"Found {len(results)} results for '{search_term}':")
    for r in results:
        print(f"  📄 {r['file']}")
        print(f"     {r['snippet']}")
        print()

    return results

def read_entity(name: str, category: str = None):
    """Read all knowledge about a specific entity."""
    paths = []

    if category:
        paths = [KB_ROOT / category / name]
    else:
        # Search all categories
        for cat in ["projects", "areas", "resources"]:
            p = KB_ROOT / cat / name
            if p.exists():
                paths.append(p)

    if not paths:
        print(f"No entity found: {name}")
        return

    for p in paths:
        print(f"\n{'='*60}")
        print(f"Entity: {p.relative_to(KB_ROOT)}")
        print(f"{'='*60}")

        if p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and f.suffix in (".md", ".yaml", ".yml"):
                    print(f"\n--- {f.name} ---")
                    print(f.read_text()[:500])
                    if len(f.read_text()) > 500:
                        print("... (truncated, use `kb read` for full)")
        elif p.is_file():
            print(p.read_text()[:1000])

# Query examples
query_kb("pricing")
query_kb("MCP")
read_entity("mcp-clients", "resources")
```

## Concrete Action Flow

### Every Session: KB Warmup Flow
```python
def session_warmup():
    """Run at session start — loads context into agent memory."""

    # 1. Load yesterday's daily note
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    note_path = KB_ROOT / "areas" / "daily" / f"{yesterday}.md"
    if note_path.exists():
        print(f"Yesterday's context:\n{note_path.read_text()[:1000]}")

    # 2. Load open decisions and pending items
    decisions_file = KB_ROOT / "resources" / "decisions.yaml"
    if decisions_file.exists():
        with open(decisions_file) as f:
            decisions = yaml.safe_load(f) or []
        open_decisions = [d for d in decisions if d.get("status") == "open"]
        if open_decisions:
            print(f"\nOpen decisions ({len(open_decisions)}):")
            for d in open_decisions:
                print(f"  - {d['value']}")

    # 3. Check for stale content (auto-decay check)
    stale = check_for_stale_content(days_old=90)
    if stale:
        print(f"\nStale content to review: {len(stale)} items")

    # 4. Write today's session note
    write_daily_note()

    print("\nSession warmup complete. KB is loaded.")
```

### Writing Flow: Capture → Structure → Store → Cross-Reference

```python
def capture_knowledge(entity: str, category: str, content: dict):
    """Full knowledge capture pipeline."""

    # Step 1: Store raw fact
    fact_path = store_fact(category, entity, {
        "type": content.get("type", "note"),
        "value": content["value"],
        "status": content.get("status", "draft"),
        "priority": content.get("priority", "medium")
    })

    # Step 2: Write detailed markdown if needed
    if "detail" in content:
        detail_dir = KB_ROOT / category / entity
        detail_path = detail_dir / f"{entity}-details.md"
        with open(detail_path, "w") as f:
            f.write(f"# {entity}\n\n{content['detail']}\n")
        print(f"Detail written: {detail_path}")

    # Step 3: Update entity index
    index_file = KB_ROOT / "resources" / "entity-index.yaml"
    if index_file.exists():
        with open(index_file) as f:
            index = yaml.safe_load(f) or {}
    else:
        index = {}

    if entity not in index:
        index[entity] = {"category": category, "facts": [], "related": []}

    index[entity]["facts"].append(content["value"])
    index[entity]["last_updated"] = datetime.now().isoformat()

    # Cross-reference with related entities
    if "related" in content:
        index[entity]["related"].extend(content["related"])
        index[entity]["related"] = list(set(index[entity]["related"]))

    with open(index_file, "w") as f:
        yaml.dump(index, f, default_flow_style=False, sort_keys=False)

    print(f"Entity index updated for '{entity}'")
    return fact_path
```

### Retrieval Flow: Query → Filter → Rank → Present

```python
def retrieve_knowledge(query: str, filters: dict = None, top_k: int = 5):
    """Structured retrieval pipeline."""

    # Phase 1: Full-text search
    results = []
    import subprocess
    grep_out = subprocess.run(
        ["rg", "-l", "-i", query, str(KB_ROOT)],
        capture_output=True, text=True, timeout=10
    )

    files = [f for f in grep_out.stdout.strip().split("\n") if f]

    # Phase 2: Apply filters
    if filters:
        if filters.get("category"):
            files = [f for f in files if f"/{filters['category']}/" in f]
        if filters.get("entity"):
            files = [f for f in files if filters["entity"] in f]
        if filters.get("after"):
            after_ts = datetime.fromisoformat(filters["after"])
            files = [f for f in files
                     if datetime.fromtimestamp(Path(f).stat().st_mtime) > after_ts]

    # Phase 3: Rank by freshness + relevance
    scored = []
    for f in files:
        path = Path(f)
        mtime = path.stat().st_mtime
        # Count query hits for relevance score
        hits = subprocess.run(
            ["rg", "-c", "-i", query, str(path)],
            capture_output=True, text=True, timeout=5
        )
        hit_count = int(hits.stdout.strip() or 0)
        freshness_score = min(1.0, (datetime.now().timestamp() - mtime) / 86400 / 30)
        scored.append((hit_count * 10 + (1 - freshness_score) * 5, f))

    scored.sort(key=lambda x: x[0], reverse=True)

    # Phase 4: Present
    for score, f in scored[:top_k]:
        rel = Path(f).relative_to(KB_ROOT)
        snippet = subprocess.run(
            ["rg", "-i", "-m", "5", query, str(f)],
            capture_output=True, text=True, timeout=5
        )
        print(f"[Score: {score:.1f}] {rel}")
        print(f"  {snippet.stdout.strip()[:200]}")
        print()

    return [{"file": Path(f).relative_to(KB_ROOT).as_posix(), "score": s}
            for s, f in scored[:top_k]]
```

### Decay & Archival Flow

```python
def check_for_stale_content(days_old: int = 90):
    """Find knowledge that hasn't been touched in days_old days."""
    from datetime import timedelta

    cutoff = datetime.now() - timedelta(days=days_old)
    stale = []

    for category in ["projects", "areas", "resources"]:
        for f in (KB_ROOT / category).rglob("*.md"):
            if datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
                stale.append(f)

    return stale


def archive_stale_content(dry_run: bool = True):
    """Move stale content to archives/ for preservation without clutter."""
    stale = check_for_stale_content(90)
    archive_dir = KB_ROOT / "archives"
    archive_dir.mkdir(exist_ok=True)

    for path in stale:
        rel = path.relative_to(KB_ROOT)
        archive_path = archive_dir / rel

        if dry_run:
            print(f"[DRY RUN] Would archive: {rel} -> {archive_path}")
        else:
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            path.rename(archive_path)
            print(f"Archived: {rel}")

    if not stale:
        print("No stale content found.")
    return stale if dry_run else None
```

## Verification

- Save a project decision to the knowledge base, then query it back in a fresh session and confirm it retrieves.
- Verify PARA structure: content lands in the documented area (project/area/resource/archive) and is findable by search.
- Check cross-session recall: context loaded at session start includes the decision you stored.
- Confirm the KB stays consistent — updates to an existing note replace, not duplicate.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll remember what we decided last week" | You won't. Neither will the next agent. Write it down or lose it. |
| "The conversation is the memory" | Conversations disappear when the session ends. KB persists. |
| "Structuring by PARA is overkill for one person" | PARA scales from 1 to 100 agents. Start structured or refactor later at 10x cost. |
| "I'll add facts later when I have time" | "Later" never comes. Capture at the moment of decision. |
| "Search is good enough for retrieval" | Search finds strings. Structure finds meaning, decisions, and relationships. |
| "Archiving loses information" | Archiving moves stale data out of active context — it is not deletion. |
| "Only humans need documentation" | Agents need documentation more than humans — they have no intuition to fill gaps. |

## Output Format

When using the knowledge base hub, produce structured recall results:

```json
{
  "query": "pricing decision",
  "results": [
    {
      "file": "areas/pricing-strategy/facts.yaml",
      "relevance_score": 85.0,
      "snippet": "Decision: Standard tier at $49/mo, Pro tier at $99/mo",
      "last_updated": "2026-07-01T14:30:00Z",
      "status": "confirmed"
    }
  ],
  "total_found": 3,
  "total_returned": 2,
  "filters_applied": {"category": "areas"}
}
```

Daily note output:

```json
{
  "date": "2026-07-16",
  "sessions": 2,
  "facts_added": 3,
  "decisions_made": 1,
  "stale_items": 0,
  "entities_referenced": ["mcp-clients", "pricing-strategy", "website-redesign"]
}
```

## Verification Checklist

- [ ] PARA directory structure exists (`projects/`, `areas/`, `resources/`, `archives/`)
- [ ] Daily note is written at session start with today's plan
- [ ] Facts are stored as YAML with timestamps and sources
- [ ] Entity index is maintained for cross-referencing
- [ ] Full-text search (`rg`) returns results from all PARA categories
- [ ] Stale content detection runs and produces actionable list
- [ ] At least 10 facts are stored covering: decisions, capabilities, milestones, references
- [ ] Company-specific entities (products, clients, team) have dedicated entries
- [ ] Session warmup successfully loads yesterday's context + open decisions
- [ ] No orphaned facts — every fact cross-references an entity
- [ ] Rollback: `git revert` works on fact changes; YAML history is recoverable
- [ ] Weekly archival review is scheduled or triggered automatically


## When to Use
Use this skill when working with core.
