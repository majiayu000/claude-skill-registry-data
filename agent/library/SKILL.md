---
name: library
description: HUAOMP Library — acquire, catalog, query, and curate knowledge across 20 departments. Receipt-backed acquisitions, SHA-256 dedup, three-tier access classification.
version: 0.1.0
status: tested
canonical_status: not_yet_global_canon
execution-mode: side_effecting
argument-hint: "<acquire|catalog|query|stats|departments|ingest-ledger> [args]"
category: hummbl-research
---

# library

HUAOMP Library — the HUMMBL knowledge repository. Catalogs, stores, and
queries knowledge across 20 departments with receipt-backed acquisitions
and SHA-256 content dedup.

## When to use

### Explicit invocation
- `[library] acquire <path>` — register a document into the library
- `[library] acquire-batch <dir>` — register all documents in a directory
- `[library] query <text>` — search the catalog by text
- `[library] query --department <dept>` — filter by department
- `[library] query --tier <T1-T13>` — filter by knowledge tier
- `[library] query --lenses H,O` — filter by HUAOMP lenses
- `[library] stats` — collection statistics
- `[library] departments` — per-department breakdown
- `[library] ingest-ledger <path>` — import loop-ledger JSONL entries

### Auto-propose
- When a research session produces documents that should be cataloged
- When importing external sources (Gutenberg, arxiv, Wikipedia)
- When querying the fleet's knowledge base for prior research

## Departments (20)

| Department | Wing Name | Source |
|---|---|---|
| canonical_foundations | The Roots | T1 |
| empirical_research | The Observatory | T2 |
| applied_systems | The Workshop | T3 |
| agentic_systems | The Hive | T4 |
| engineering_practice | The Forge | T5 |
| governance | The Court | T6 |
| emerging_technology | The Horizon | T7 |
| cognition | The Mind | T8 |
| economics | The Exchange | T9 |
| collaboration | The Forum | T10 |
| security | The Citadel | T11 |
| complexity | The Lattice | T12 |
| reasoning | The Compass | T13 |
| arcana | The Pantheon | Fleet |
| operations | The Bridge | Fleet |
| skills | The Library of Skills | Fleet |
| rules | The Codex | Fleet |
| external_humanities | The Alexandria Wing | Gutenberg |
| external_science | The Tigris Wing | arxiv |
| external_world_knowledge | The Bosphorus Wing | Wikipedia |

## Access tiers

- `public` — safe to share externally (default)
- `internal` — fleet-only (AARs, operations, bus history)
- `restricted` — operator-only (tokens, secrets, credentials)

## Storage

- Catalog: `~/.agents/library/catalog.jsonl` (append-only JSONL)
- Index: `~/.agents/library/catalog_index.json` (item_id → line, sha256)
- Receipts: via hummbl-governance kernel ReceiptEngine

## Execution

### acquire
```python
from hummbl_governance.library import Library, Department

lib = Library(state_dir=Path("~/.agents/library"))
entry = lib.acquire(Path("docs/research/findings.md"), agent_id="devin")
```

### query
```python
results = lib.query(text="governance", department=Department.GOVERNANCE)
```

### ingest-ledger
```python
from hummbl_governance.library import import_loop_ledger
successes, failures = import_loop_ledger(
    Path("~/.agents/loop-ledger/intel-surge-ledger.jsonl"),
    lib,
)
```

## Dependencies

- `hummbl_governance.kernel.ReceiptEngine` (optional — for receipt-backed acquisitions)
- `hummbl_governance._file_lock` (for concurrent write safety)
- Python stdlib only — no third-party dependencies
