---
name: ingest-repo
description: Semantic codebase ingestion — given a topic or repo URL, agent maps the dependency graph, identifies key entry points, filters noise files, and synthesizes a structured spec. BloopAI-inspired semantic search over code at macro scale. Triggered by /ingest-repo.
origin: BloopAI/bloop (Apache 2.0) — semantic search + dependency graph concepts
license: MIT
version: 1.0.0
compatibility: bash, git, any language codebase
---

# ingest-repo

## When to Use

- You want to understand a new repo's architecture without reading every file
- You've cloned a large codebase and need to find where a concept lives
- Importing patterns from an open-source repo into Yamtam (skill extraction)
- Triggered by: `/ingest-repo`, "ingest this repo", "map the codebase", "find the entry points", "extract patterns from", "understand the architecture of"

## Do NOT use for

- Single-file lookups — use `grep` or Read directly
- Private repos without explicit authorization
- Replacing full code review — this is a mapping tool, not an audit
- See `deep-research` skill for general topic research without a specific repo

---

## Phase 1 — Repo Snapshot

```bash
#!/usr/bin/env bash
# ingest-repo.sh <repo-path-or-url> <topic>
REPO="${1:-.}"
TOPIC="${2:-architecture}"
OUT_DIR=".claude/ingestion"
mkdir -p "$OUT_DIR"

echo "=== REPO INGESTION: $REPO ===" | tee "$OUT_DIR/report.md"
echo "Topic: $TOPIC" >> "$OUT_DIR/report.md"
echo "" >> "$OUT_DIR/report.md"

# File inventory
echo "## File Inventory" >> "$OUT_DIR/report.md"
find "$REPO" -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.rs" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/vendor/*" ! -path "*/dist/*" \
  | wc -l | xargs -I{} echo "Source files: {}" >> "$OUT_DIR/report.md"

# Entry points (main/index/app files)
echo "" >> "$OUT_DIR/report.md"
echo "## Entry Points" >> "$OUT_DIR/report.md"
find "$REPO" -maxdepth 3 -type f \( -name "main.*" -o -name "index.*" -o -name "app.*" -o -name "server.*" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" \
  | head -20 >> "$OUT_DIR/report.md"

# Dependency map (imports/requires)
echo "" >> "$OUT_DIR/report.md"
echo "## Dependency Hotspots (most-imported files)" >> "$OUT_DIR/report.md"
grep -rh "^import\|^from\|^require\|^use " "$REPO" \
  ! -path "*/node_modules/*" 2>/dev/null \
  | grep -oE '"[^"]+"|'"'"'[^'"'"']+'"'" \
  | tr -d '"'"'" | sort | uniq -c | sort -rn | head -20 >> "$OUT_DIR/report.md"

echo "Ingestion complete: $OUT_DIR/report.md"
```

---

## Phase 2 — Semantic Pattern Extraction

```python
# Extract patterns relevant to a given topic from ingested files
import os, re
from pathlib import Path

def extract_patterns(repo_path: str, topic: str) -> list[dict]:
    """
    Semantic search: find functions/classes related to topic.
    Returns ranked list of {file, line, snippet, relevance}.
    """
    topic_keywords = topic.lower().split()
    results = []

    for path in Path(repo_path).rglob("*"):
        if path.suffix not in {".ts", ".js", ".py", ".go", ".rs"}:
            continue
        if any(skip in str(path) for skip in ["node_modules", ".git", "vendor", "dist"]):
            continue

        try:
            content = path.read_text(errors="ignore")
        except OSError:
            continue

        lines = content.splitlines()
        for i, line in enumerate(lines):
            score = sum(kw in line.lower() for kw in topic_keywords)
            if score > 0 and re.search(r"(function|def |class |export |fn |impl )", line):
                results.append({
                    "file": str(path),
                    "line": i + 1,
                    "snippet": line.strip(),
                    "score": score,
                })

    return sorted(results, key=lambda r: r["score"], reverse=True)[:20]
```

---

## Phase 3 — Spec Synthesis

```markdown
# Ingestion Spec: <repo-name> — Topic: <topic>

## Architecture Summary
- Entry points: [list from Phase 1]
- Core modules: [highest-imported files]
- Pattern density: [functions per file avg]

## Relevant Patterns Found
| File | Line | Pattern | Relevance |
|------|------|---------|-----------|
| path/to/file.ts | 42 | `function cacheAside(...)` | ★★★ |

## Extraction Candidates for Yamtam
- [ ] Pattern A: describe what it does + which yamtam skill it maps to
- [ ] Pattern B: ...

## What to Skip
- Files with >300 lines that are config/generated (noise)
- Vendor/third-party modules
- Test fixtures not relevant to the topic
```

---

## Agent Usage Pattern

```
User: /ingest-repo "optimize memory cache"

Agent steps:
1. Search GitHub for top repos matching topic (use WebSearch)
2. Clone or read repo structure
3. Run Phase 1 snapshot → extract entry points + dependency hotspots
4. Run Phase 2 semantic search for topic keywords in function signatures
5. Synthesize Phase 3 spec → write to .claude/ingestion/report.md
6. Propose: "Found 5 extractable patterns — import as yamtam skill? (y/N)"
```

---

## Anti-Fake-Pass Checklist

- [ ] Report written to `.claude/ingestion/report.md` — not just printed to stdout
- [ ] Noise filtered: node_modules, .git, vendor, dist excluded from all scans
- [ ] Entry points identified: at least 1 main/index/app/server file found
- [ ] Semantic results ranked by relevance score — not random file order
- [ ] Extraction candidates listed with explicit Yamtam skill mapping
- [ ] Agent asks for human confirmation before importing patterns (no auto-import)
