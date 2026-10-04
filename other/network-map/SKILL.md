---
name: network-map
description: Map relationships, co-authorships, endorsements, and organizational connections across movement leaders. Reads existing per-leader research in docs/movement_leader_research/ and writes a cross-leader graph. Output table schemas align with the `movement-leader-substrate` Network graph section so per-leader substrate files can be regenerated from this data.
disable-model-invocation: true
---

> **Relationship to substrate.** Per-leader edges (co-authors, endorsements, organizational affiliations) live inside each leader's `{SLUG}_RESEARCH_COLLATED.md` Section 10 (Network graph). This skill produces the **cross-leader** view — clusters, bridges, isolates — by reading all substrates together. The per-leader edge tables in this skill's output MUST match the substrate's column schema so they can be lifted into a substrate refresh.

# Network Map: Trace the Movement Leader Graph

Map the relational web between movement leaders — co-authorships, endorsements, shared organizations, conference circuits, and institutional ties. This skill reads existing research in `docs/movement_leader_research/` to reveal scenius structure: clusters, bridge figures, and isolated candidates.

## Invocation

```
/network-map $ARGUMENTS
```

**Arguments:**
- A leader name: `/network-map Alan Hirsch` — map all connections from one leader
- An organization: `/network-map Forge Network` — map all leaders connected through an org
- `top 20` — map connections among the top 20 ranked candidates
- `clusters` — identify and name the natural clusters
- `bridges` — find leaders who connect otherwise separate clusters
- `isolates` — find candidates with few/no connections to others
- `all` — full network map from all existing research data
- Empty — map from all existing network/ folder data

---

## Before Starting

1. **Read the master ranked list** at `docs/movement_leader_research/tam-search/01-MASTER-RANKED-LIST.md`
2. **Scan existing research folders** — `ls docs/movement_leader_research/` to see which leaders have folders
3. **For each leader in scope**, read their network data:
   - `docs/movement_leader_research/{slug}/_misc/network/collaborators.md`
   - `docs/movement_leader_research/{slug}/network/organizations.md`
   - `docs/movement_leader_research/{slug}/_misc/network/endorsements.md`
   - `docs/movement_leader_research/{slug}/_misc/network/events.md`
   - `docs/movement_leader_research/{slug}/profile/biography.md`
   - `docs/movement_leader_research/{slug}/profile/identity.md`

   Note: only `organizations.md` lives in the canonical `network/` folder; `collaborators.md`, `endorsements.md`, and `events.md` are helper files under `_misc/network/` (as in the reference dossiers `brad-brisco/` and `michael-cooper/`).
4. **Read existing network maps** in `docs/movement_leader_research/network/` if any exist

---

## Phase 1: Define Scope

Based on the argument, determine what to map:

| Mode | Scope | Output |
|------|-------|--------|
| **Leader-centric** | All connections from one leader outward | Ego network map |
| **Org-centric** | All leaders connected through one org | Organization membership map |
| **Top N** | Connections among the top N candidates | Core network structure |
| **Clusters** | Natural groupings across the full research set | Cluster identification |
| **Bridges** | Leaders who connect separate clusters | Bridge figure analysis |
| **Isolates** | Candidates with minimal connections | Gap identification |
| **All** | Complete network from all research data | Full graph |

---

## Phase 2: Extract Connections from Existing Research

For each leader in scope, read their `network/organizations.md` plus the `_misc/network/` helper files (`collaborators.md`, `endorsements.md`, `events.md`) and extract connection edges. Look for:

### Connection Types (weighted by strength)

| Type | Weight | Where to Find |
|------|--------|---------------|
| **Co-authored book** | 5 | _misc/network/collaborators.md, content/books.md |
| **Co-founded organization** | 5 | network/organizations.md |
| **Book endorsement/blurb** | 3 | _misc/network/endorsements.md |
| **Same organization leadership** | 3 | network/organizations.md |
| **Conference co-speakers** | 2 | _misc/network/events.md |
| **Podcast guest on their show** | 2 | content/audio.md |
| **Shared publisher** | 1 | content/books.md |
| **Academic colleague** | 2 | network/organizations.md (academic category) |
| **Cited/referenced in work** | 2 | content/academic.md |
| **Public mutual endorsement** | 2 | _misc/network/endorsements.md |

### Extraction Pattern

For each file, look for mentions of other leaders from the master ranked list. Record:
- Leader A (the folder owner)
- Leader B (the mentioned leader)
- Connection type
- Weight
- Evidence (quote or citation from the source file)

---

## Phase 3: Build the Network Data

Compile all extracted connections into a master table:

```markdown
| Leader A | Leader B | Connection Type | Weight | Evidence |
|----------|----------|----------------|--------|----------|
| Alan Hirsch | Michael Frost | Co-authored book | 5 | "The Shaping of Things to Come" (2003) |
| Alan Hirsch | Dave Ferguson | Book endorsement | 3 | Endorsement on "On the Verge" |
```

---

## Phase 4: Cluster Analysis

Identify natural groupings based on connection density:

### Expected Clusters (validate via research data)

| Cluster Name | Expected Hub Leaders | Binding Element |
|-------------|---------------------|-----------------|
| **Forge/Missional Core** | Hirsch, Frost, Brisco, Roxburgh, Catchim | Forge Network, APEST, missional theology |
| **Multiplication/Exponential** | Ferguson, Wilson, Moore, Wegner | Exponential Conference, church planting |
| **Spiritual Formation** | Caliguire, Barton, Scazzero, Thompson | Soul care, Transforming Center |
| **Justice/Urban** | Perkins, Strickland, Fitch | CCDA, neighborhood mission |
| **Academic/Theological** | McKnight, Smith (J.K.A.), Hunter | Seminary networks |
| **International** | Sayers, Addison, Mawarire, Cotterill | Cross-border movement |
| **Underground/Microchurch** | Sanders, Gaskins, Pulley, Wilkerson | Underground Network |
| **Worship/Liturgy** | Hicks, Ruis, Johnson | Vineyard, liturgical renewal |

---

## Phase 5: Output

### Network Data File

**Output file**: `docs/movement_leader_research/network/network-map.md`

Structure:
```markdown
# Movement Leader Network Map

**Generated:** [date]
**Scope:** [description]

## Summary
- **Leaders mapped**: [count]
- **Connections found**: [count]
- **Clusters identified**: [count]
- **Bridge figures**: [names]
- **Isolates**: [names]

## Connection Table
[Full table from Phase 3]

## Clusters
[Cluster analysis from Phase 4]

## Bridge Figures
[Leaders who connect clusters — high strategic value]

## Isolates
[Leaders with 0-1 connections — may be hidden gems or misaligned]

## Network Insights
- [Key observations about the scenius structure]
- [Gaps: which clusters are underconnected?]
- [Recommendations for strengthening the network]
```

### Per-Leader Network Summary (substrate-conformant)

For each leader with a research folder, also write/update:
`docs/movement_leader_research/{slug}/network/network-summary.md`

**Column schemas must match the substrate's Section 10 (Network graph)** so the substrate can be regenerated without reshaping data:

```
### Co-authors
| Person | Joint works | Edge weight | Notes |

### Endorsements received (sample)
| From | For | Year | URL / note |

### Organizational affiliations
| Organization | Role | Years | URL |
```

Edge weight 1–10. For co-authorship of N books, use `3 + (2 × N)` bounded at 10. Endorsement weight = 3.

```markdown
# Network Summary: [Name]

**Connections**: [count]
**Primary Cluster**: [cluster name]
**Bridge Status**: [bridge/non-bridge]

## Connections
| Connected To | Type | Weight | Evidence |
|-------------|------|--------|----------|

## Shared Organizations
| Organization | Other Leaders |
|-------------|--------------|

## Cluster Position
[Description of where this leader sits in the network]
```

### Visualization Data (optional)

Output a JSON adjacency list to `docs/movement_leader_research/network/network-graph.json`:

```json
{
  "nodes": [
    {"id": "alan-hirsch", "name": "Alan Hirsch", "cluster": "forge-core", "score": 100}
  ],
  "edges": [
    {"source": "alan-hirsch", "target": "michael-frost", "type": "co-author", "weight": 5}
  ]
}
```

---

## Key Rules

1. **Every connection must have evidence.** No assumed connections — cite the source file and passage.
2. **Use weighted connection types** — a co-authored book (5) is not the same as sharing a publisher (1).
3. **Bridge figures are strategically critical.** They connect clusters and multiply the scenius effect.
4. **Only use existing research data.** Do NOT web-search for new connections unless explicitly asked. This skill reads what's already been collected.
5. **The network IS the scenius.** This maps to Movemental's core value proposition of credibility through connection.
6. **Create directories as needed** — `docs/movement_leader_research/network/` if it doesn't exist.
7. **Update, don't overwrite.** If network data already exists, merge new connections.
8. **Cross-reference the master ranked list** — use scores to prioritize which connections matter most.
9. **Flag data gaps** — if a leader's folder is empty or missing network files, note it as a research gap.
