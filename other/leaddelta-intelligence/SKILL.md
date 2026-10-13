---
name: leaddelta-intelligence
description: "LinkedIn relationship intelligence via LeadDelta MCP. Triggers when user asks to 'find warm intro', 'search LinkedIn connections', 'who knows [person/company]', 'find a connector', 'LinkedIn path', or 'warm introduction'. Combines LeadDelta Warm Intro AI (10+ signals) with Nexus Neptune graph paths for maximum relationship intelligence."
---

# LeadDelta Relationship Intelligence Skill

LinkedIn-native relationship intelligence combining LeadDelta's Warm Intro AI (10+ signals) with Nexus Neptune multi-hop graph traversal.

## Prerequisites

- Read `_shared/plugin-context.md` for Nexus domain context
- **LeadDelta connection required**: API key must be configured in Nexus admin (`/admin/ai-config` → Connectors tab)
- Falls back to Neptune-only paths if LeadDelta is unavailable (surfaces this to user)
- MCP tools available: `leaddelta_search_connections`, `leaddelta_warm_intro_ai`, all `nexus_*` relationship tools

## When This Skill Triggers

| User Intent | Example Phrases |
|------------|----------------|
| Warm intro finding | "Who knows someone at Blackstone?", "Find a warm intro to KKR" |
| LinkedIn search | "Search LinkedIn for", "Who in our network works at...", "Find connections at..." |
| Connector discovery | "Who can introduce me to...", "Best person to reach out through" |
| Relationship intelligence | "LinkedIn relationship path", "How connected are we to..." |

## Protocol Overview

```
Intent Classification → LinkedIn Search → Neptune Paths → LeadDelta Warm Intro AI → Combined Scoring → Draft Message
       (parallel)
```

## Phase 1: Intent Classification

Classify the request:
- **Company intro**: Find paths to any person at a target company
- **Person intro**: Find paths to a specific named individual
- **Network search**: Discover relevant people matching criteria
- **Path mapping**: Map connections between two specific people

## Phase 2: Dual-Network Search

Run searches in parallel:

**LeadDelta LinkedIn Network**:
```
leaddelta_search_connections({
  query: "[natural language from user]",
  filters: { company, title, location, industry },
  limit: 25
})
```
Returns: LinkedIn connections with stage, tags, last interaction, connection date.

**Nexus Internal Network**:
```
nexus_search_network({
  query: "[same natural language query]",
  company, title, connection_strength,
  limit: 20
})
```
Returns: CRM contacts with relationship metadata.

## Phase 3: Warm Intro Path Discovery

**LeadDelta Warm Intro AI** (when target company/person known):
```
leaddelta_warm_intro_ai({
  target_company: "...",
  target_person: "...",      // optional
  min_intro_score: 0.5,
  max_results: 10
})
```

LeadDelta scores 10+ signals per potential connector:
1. Length of overlapping employment (weighted highest)
2. Recency of LinkedIn connection
3. LinkedIn messaging activity history
4. Educational overlap (institution + graduation proximity)
5. Department/role proximity at shared employer
6. Mutual connections count
7. Geographic proximity
8. Profile view / engagement history
9. Response rate signals
10. Proprietary LeadDelta relationship indicators

**Neptune Graph Paths** (multi-hop):
```
nexus_find_warm_intro({
  target_company: "...",
  max_hops: 3,
  include_leaddelta: true
})
```

Returns paths ranked by: hop count (fewer = better) × relationship strength × intro quality.

## Phase 4: Combined Scoring

Merge LeadDelta and Neptune paths with unified scoring:

| Signal | Weight | Source |
|--------|--------|--------|
| LeadDelta warm intro score | 40% | LeadDelta AI |
| Neptune path length (inverse) | 25% | Graph DB |
| Relationship recency | 20% | Both |
| Mutual connections | 15% | Both |

**Intro Quality Classification**:
- **Strong** (0.75+): Direct connection or 1-hop with high LeadDelta score — recommend immediately
- **Medium** (0.50-0.75): 2-hop or moderate LeadDelta score — recommend with context
- **Weak** (<0.50): 3+ hops or low scores — surface with caveat

## Phase 5: Message Drafting

Draft personalized intro request messages calibrated to the connector's relationship:

**Tone calibration** (based on `nexus_relationship_score`):
- **A/A+ grade** (85+): Warm, casual — "Hey [name], hope you're well! Quick favor..."
- **B/C grade** (40-70): Professional — "Hi [name], I hope this finds you well. I wanted to reach out..."
- **D/F grade** (<40): Formal — "Dear [name], I hope you are doing well. I'm writing to..."

**Message template**:
```
[Greeting based on relationship grade]

I'm reaching out because I've been trying to connect with [target] 
at [company]. [1 sentence why this matters — deal context or business reason].

Given your [shared context: worked together at X / studied together at Y / 
mutual connection through Z], I thought you might be willing to make an 
introduction.

[Specific ask: Would you be open to a quick intro email? Happy to draft 
the message for you.]

[Closing based on relationship]
```

## Output Format

```markdown
## Warm Intro Paths: [Target Company/Person]

### Best Path ⭐ (intro quality: strong)
[Connector Name] — [Title] at [Company]
- LeadDelta Score: 0.87/1.0
- Employment overlap: 3.2 years at Goldman Sachs
- Messaging activity: high (last contact 12 days ago)
- Mutual connections: 8

**Suggested Message**:
> "Hey [Connector], hope you're well! I've been trying to connect with [Target] 
> at [Company] re: [context]. Given you both worked at Goldman, would you be 
> open to making an intro? Happy to draft the message."

---

### Path 2 (intro quality: medium)
[Connector Name] — via [Intermediate Person]
- Combined Score: 0.61/1.0
- 2 hops: [You] → [Connector] → [Target]

---

### LeadDelta LinkedIn Network (X additional paths)
[Additional LeadDelta connectors with scores]

---

### No Paths Found?
If 0 paths found: Surface this to user and recommend:
1. Import team LinkedIn connections via `nexus_import_connections`
2. Expand search to 4-5 hops via `nexus_get_intro_paths_between`
3. Consider cold outreach with a highly personalized approach
```

## Error Handling

| Scenario | Response |
|----------|---------|
| LeadDelta API key not configured | Surface to user: "LeadDelta connection not configured. Showing Neptune paths only. Configure at /admin/ai-config → Connectors." |
| LeadDelta API timeout (15s) | Fall back to Neptune only, note LeadDelta unavailability |
| No paths found (0 results both) | Recommend LinkedIn import or cold outreach |
| Target not in any network | Suggest broader company search or industry-level search |
| LeadDelta rate limit hit | Queue request, show cached results if available |

## Integration Points

This skill integrates with:
- **`/nexus-network` command** — primary CLI trigger
- **`relationship-graph` agent** — orchestrates multi-step relationship workflows
- **Nexus CRM** — enriched contacts surface in `/relationships/contacts`
- **Deal flow** — warm paths to target companies link to deal records
- **LP Management** — relationship paths to LP contacts inform fundraising strategy
