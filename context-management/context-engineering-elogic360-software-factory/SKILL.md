---
name: context-engineering
description: Context Engineering — Institutional capability and runbook for context-engineering.
---

# SKILL: Context Engineering
## Domain: Context Compression, Retrieval, Agent Memory, Session State

**Activation triggers:** context window, token budget, agent memory, information
retrieval, context snapshot, session compression, RAG, semantic search, long
conversation, context overflow.

---

## Context Engineering Principles

```
1. COMPRESSION — reduce token count without losing signal
2. RETRIEVAL — fetch only relevant context for the current task
3. LAYERING — system → domain → task → user context hierarchy
4. FRESHNESS — stale context is worse than no context
5. ATTRIBUTION — always know where a fact came from (source tracing)
```

---

## Architecture Snapshot Generator

```python
#!/usr/bin/env python3
# software-factory/context-engine/snapshot.py
# Usage: python3 snapshot.py --domain journal
# Output: compressed JSON snapshot of domain architecture

import argparse
import json
import subprocess
from pathlib import Path

DOMAIN_FILES = {
    "journal": [
        "integral-expert-backend/app/models/journal.py",
        "integral-expert-backend/app/api/v1/endpoints/journal.py",
        "integral-expert-backend/app/services/journal/analytics.py",
        "integral-expert-backend/app/schemas/journal.py",
    ],
    "copy_trading": [
        "integral-expert-backend/app/models/copy_trading.py",
        "integral-expert-backend/app/api/v1/endpoints/copy_trading.py",
        "integral-expert-backend/app/services/copy_trading/",
    ],
    "auth": [
        "integral-market-backend/app/models/user.py",
        "integral-market-backend/app/api/v1/endpoints/auth.py",
        "integral-market-backend/app/services/auth_service.py",
    ],
}

def generate_snapshot(domain: str) -> dict:
    files = DOMAIN_FILES.get(domain, [])
    snapshot = {
        "domain": domain,
        "files": {},
        "exports": {},     # public interface summary
        "warnings": [],    # known issues
    }

    root = Path("/home/elogic360/Desktop/little QUANTUM/Integral Market")

    for file_path in files:
        full_path = root / file_path
        if not full_path.exists():
            snapshot["warnings"].append(f"Missing: {file_path}")
            continue

        # Read and compress (strip comments + docstrings for token efficiency)
        content = full_path.read_text()
        compressed = _compress_python(content)
        snapshot["files"][file_path] = compressed

    return snapshot

def _compress_python(source: str) -> str:
    """Strip docstrings and blank lines to reduce token count ~40%."""
    import ast
    try:
        tree = ast.parse(source)
        # Extract just function/class signatures + type annotations
        lines = source.split("\n")
        relevant = [l for l in lines if (
            l.strip().startswith("class ")
            or l.strip().startswith("def ")
            or l.strip().startswith("async def ")
            or l.strip().startswith("@")
            or ": " in l and "Mapped[" in l
            or l.strip().startswith("__tablename__")
            or l.strip().startswith("__table_args__")
        )]
        return "\n".join(relevant)
    except SyntaxError:
        return source[:2000]   # fallback: first 2000 chars

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True)
    parser.add_argument("--output", default="stdout")
    args = parser.parse_args()

    snapshot = generate_snapshot(args.domain)

    if args.output == "stdout":
        print(json.dumps(snapshot, indent=2))
    else:
        Path(args.output).write_text(json.dumps(snapshot, indent=2))
        print(f"Snapshot written to {args.output}")
```

---

## Retriever (Spec + Memory Search)

```python
#!/usr/bin/env python3
# software-factory/context-engine/retriever.py
# Usage: python3 retriever.py --query "copy trading subscription"
# Returns: ranked list of relevant spec/memory snippets

import argparse
import json
import re
from pathlib import Path

SEARCH_ROOTS = [
    "software-factory/specs/active",
    "software-factory/memory/decisions",
    "software-factory/memory/patterns",
    "software-factory/skills",
]

def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """Simple TF-IDF-style keyword retrieval over markdown files."""
    query_tokens = set(re.findall(r'\b\w{3,}\b', query.lower()))
    root = Path("/home/elogic360/Desktop/little QUANTUM/Integral Market")
    results = []

    for search_root in SEARCH_ROOTS:
        for md_file in (root / search_root).rglob("*.md"):
            content = md_file.read_text(errors="ignore")
            tokens = set(re.findall(r'\b\w{3,}\b', content.lower()))
            overlap = len(query_tokens & tokens)
            if overlap > 0:
                # Extract most relevant snippet (window around first hit)
                snippet = _extract_snippet(content, query_tokens)
                results.append({
                    "file": str(md_file.relative_to(root)),
                    "score": overlap,
                    "snippet": snippet,
                })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

def _extract_snippet(content: str, keywords: set, window: int = 300) -> str:
    """Extract the paragraph most relevant to keywords."""
    paragraphs = content.split("\n\n")
    best = max(
        paragraphs,
        key=lambda p: sum(1 for k in keywords if k in p.lower()),
        default="",
    )
    return best[:window].strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    results = retrieve(args.query, args.top_k)
    for r in results:
        print(f"\n{'='*60}")
        print(f"File: {r['file']} (score: {r['score']})")
        print(r["snippet"])
```

---

## Session Summarizer

```python
#!/usr/bin/env python3
# software-factory/context-engine/summarizer.py
# Compress a long development session into a structured memory entry

import json
from anthropic import Anthropic

client = Anthropic()

SUMMARIZER_SYSTEM = """You are a technical memory writer for the Integral Market engineering team.
Given a development session transcript, extract:
1. Changes made (files modified, decisions made)
2. Problems solved (root causes identified and fixed)
3. Anti-patterns discovered (what to avoid)
4. Open items (what's not yet done)
5. Key lessons (what future agents must know)

Output as structured JSON. Be extremely concise — this becomes part of the codebase memory.
"""

def summarize_session(transcript: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        system=SUMMARIZER_SYSTEM,
        messages=[{
            "role": "user",
            "content": f"Summarize this development session:\n\n{transcript[:50000]}"
        }],
    )
    return json.loads(response.content[0].text)
```

---

## Agent Context Layering

```
For any AI agent working on Integral Market, inject context in this order:

Layer 1 — SYSTEM (always present, ~500 tokens):
  software-factory/CLAUDE.md (core rules)

Layer 2 — DOMAIN (~1000 tokens):
  relevant SKILL.md for the current feature area

Layer 3 — SPEC (~500 tokens):
  software-factory/specs/active/<feature>.md (if exists)

Layer 4 — SNAPSHOT (~2000 tokens):
  python3 context-engine/snapshot.py --domain <domain>

Layer 5 — RETRIEVED MEMORY (~1000 tokens):
  python3 context-engine/retriever.py --query "<task description>"

Layer 6 — TASK (~200 tokens):
  The specific user request

Total budget: ~5000 tokens of context → leaves ample room for generation
```

---

## Memory Update Protocol

```bash
# After every significant implementation, update memory:

DECISIONS_DIR="software-factory/memory/decisions"
PATTERNS_DIR="software-factory/memory/patterns"

# New architectural decision
cat >> "$DECISIONS_DIR/$(date +%Y-%m).md" << EOF

## $(date -I) — <feature name>
**Decision:** <what was decided>
**Rationale:** <why>
**Alternatives rejected:** <what else was considered and why not>
**Files changed:** <list of key files>
EOF

# New pattern discovered
cat >> "$PATTERNS_DIR/anti-patterns.md" << EOF

## $(date -I) — <pattern name>
**Problem:** <what went wrong>
**Root cause:** <why it happened>
**Fix:** <how to avoid it>
**Detection:** <how to spot it in future>
EOF
```

---

## Anti-Patterns

```
✗ Sending the full codebase as context (use snapshots — compress first)
✗ Stale snapshots (regenerate snapshot.py before each major task)
✗ No source attribution in retrieved context (agent can't trust facts without source)
✗ Memory files growing unbounded (archive entries older than 90 days)
✗ Mixing multiple domain snapshots in one prompt (one domain per agent call)
✗ Using retriever for code structure questions (use codegraph_context instead)
✗ Skipping memory update after bug fixes (future agents repeat the same bug)
```
