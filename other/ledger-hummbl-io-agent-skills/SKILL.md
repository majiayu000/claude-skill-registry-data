---
name: ledger
description: Post, query, search, and reindex the Cognitive Ledger (CLP shared memory).
version: 0.1.0
execution-mode: side_effecting
argument-hint: "[post \"CONTENT\" | query [--type lesson] | search \"TERM\" | reindex | boot | status]"
category: fleet-ops
status: candidate
---
## Context Gathering

Before executing this skill, gather the following context:
- **Ledger entries**: Run `wc -l < $PROJECT_ROOT/_state/cognition/ledger.jsonl 2>/dev/null || echo "0"`
- **Index age**: Run `stat -f "%Sm" $PROJECT_ROOT/_state/cognition/index.json 2>/dev/null || echo "no index"`
- **Last entry**: Run `tail -1 $PROJECT_ROOT/_state/cognition/ledger.jsonl 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{d[\"timestamp\"]} [{d[\"type\"]}] {d[\"agent\"]}: {d[\"content\"][:80]}')" 2>/dev/null || echo "(empty)"`

# Ledger Command

Interact with the Cognitive Ledger Protocol (CLP) -- the append-only shared memory for all agents.

## Operations

### post
1. **Emit SKILL_INVOKE** (required before any stateful action):
   ```
   Type: SKILL_INVOKE
   To: all
   Message: [skill=ledger] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
   ```
   (The skill invocation runtime injects the caller's canonical identity as `from_id`.)

2. **Post to ledger**:
   ```bash
   source .venv/bin/activate
   python -m hummbl_governance.cognition post \
     --vendor "${AGENT_VENDOR:?set AGENT_VENDOR to the provider actually running}" \
     --model "${AGENT_MODEL:?set AGENT_MODEL to the model actually running}" \
     --type lesson \
     --scope project \
     --content "The actual knowledge to record" \
     --tags "tag1,tag2"
   # The skill invocation runtime injects the caller's canonical identity as agent.
   ```

Valid types: `lesson`, `decision`, `discovery`, `correction`, `convention`
Valid scopes: `project`, `module`, `file`, `convention`, `process`

### query
Query recent entries with filters:
```bash
python -m hummbl_governance.cognition query [--type TYPE] [--scope SCOPE] [--agent AGENT] [--since YYYY-MM-DD] [--limit N]
```

### search
Full-text search across ledger entries (requires index):
```bash
python -m hummbl_governance.cognition search "search terms"
```

### reindex
Rebuild the BM25 inverted index over all entries:
```bash
python -m hummbl_governance.cognition reindex
```
Run this after bulk imports or if search returns stale results.

### boot
Generate the boot context that agents see at session start:
```bash
python -m hummbl_governance.cognition boot
```

### status
Show ledger stats (entry count, index freshness, last write):
```bash
wc -l _state/cognition/ledger.jsonl
stat -f "%Sm" _state/cognition/index.json
python -m hummbl_governance.cognition state
```

## Content Scanning
All entries are scanned for prompt injection, credential leakage, exfiltration vectors, and invisible Unicode before persistence. Suspicious content is rejected with a `ContentScanError`.

## Key Files
- `cognition/ledger_writer.py` -- write path (flock-based mutual exclusion)
- `cognition/query.py` -- query engine
- `cognition/indexer.py` -- BM25 inverted index
- `cognition/boot_context.py` -- session boot context builder
- `_state/cognition/ledger.jsonl` -- append-only storage
- `_state/cognition/index.json` -- search index
- `_state/cognition/intent.md` -- current intent (Layer 3)

## Skill Chains

### Mandatory

- None — ledger is the persistence layer. Content scanning (built-in) is the safety check.
  The ledger is append-only; no entry can be deleted or modified.

### Advisory

- **Before post**: `[research-ingest]` (for research findings), `[decision-log]` (for ADRs)
- **After bulk import**: `reindex` command (rebuild BM25 index)
- **Query/search**: read-only, no chains needed

## Authority

- **T1 (TRUSTED)**: May post/query/search/reindex without restriction
- **T2 (Active/High)**: May post/query/search/reindex without restriction (append-only is low-risk)
- **T3 (Medium)**: May query/search freely; post/reindex require operator notification
- **T4 (Probationary)**: May query/search only; post/reindex BLOCKED
- **Operator**: Override any restriction
