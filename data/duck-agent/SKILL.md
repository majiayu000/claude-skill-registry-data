---
name: duck-agent
description: DuckDB file discovery agent with verified absolute paths
version: 1.0.0
---


# Duck Agent

Quick access to all DuckDB databases and code libraries in IES.

## Primary Databases (verified Dec 26, 2025)

| Path | Size | Purpose |
|------|------|---------|
| `/Users/bob/ies/hatchery.duckdb` | 492M | Master hatchery index |
| `/Users/bob/ies/hatchery_analysis.duckdb` | 210M | Hatchery analysis results |
| `/Users/bob/ies/ananas.duckdb` | 108M | Music database |
| `/Users/bob/ies/music-topos/gh_interactome.duckdb` | 67M | GitHub interactome |
| `/Users/bob/ies/openai_world.duckdb` | 42M | OpenAI integration |
| `/Users/bob/ies/music-topos/interaction_entropy.duckdb` | 5.5M | Entropy tracking |
| `/Users/bob/ies/hatchery_order.duckdb` | 536K | Hatchery ordering |

## Hatchery Series

```
/Users/bob/ies/hatchery_order.duckdb
/Users/bob/ies/hatchery_measure.duckdb
/Users/bob/ies/hatchery_geometry.duckdb
/Users/bob/ies/hatchery_analysis.duckdb
/Users/bob/ies/hatchery_algebra.duckdb
/Users/bob/ies/hatchery_topology.duckdb
/Users/bob/ies/hatchery_probability.duckdb
/Users/bob/ies/hatchery_logic.duckdb
/Users/bob/ies/hatchery_category.duckdb
/Users/bob/ies/hatchery_acsets.duckdb
```

## Code Libraries

```
/Users/bob/ies/tools/duckdb_utils.py                           # 385 lines - Primary skill ecosystem interface
/Users/bob/ies/music-topos/lib/exa_research_duckdb.py          # 593 lines - Production ingestion pipeline
/Users/bob/ies/music-topos/lib/ducklake_incremental_sync.py    # 902 lines - Incremental sync
```

## Quick CLI

```bash
# List all tables in hatchery
duckdb /Users/bob/ies/hatchery.duckdb -c "SHOW TABLES;"

# Query GitHub interactome
duckdb /Users/bob/ies/music-topos/gh_interactome.duckdb -c "SELECT * FROM repos LIMIT 10;"

# Check interaction entropy
duckdb /Users/bob/ies/music-topos/interaction_entropy.duckdb -c "SELECT COUNT(*) FROM interactions;"
```



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
duck-agent (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch3: Variations on an Arithmetic Theme

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.