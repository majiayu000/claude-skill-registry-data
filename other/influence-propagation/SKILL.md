---
name: influence-propagation
description: "Layer 7 Interperspectival Network Analysis and Influence Flow"
---

# influence-propagation

> Layer 7: Interperspectival Network Analysis and Influence Flow

**Version**: 1.1.0 (music-topos enhanced)
**Trit**: -1 (Validator - verifies influence patterns)
**Bundle**: network

## Overview

Influence-propagation traces how ideas, topics, and behaviors spread through social networks. It extends bisimulation-game with second-order network analysis, measuring reach multipliers and idea adoption rates.

## Enhanced Integration: Condensed + Sheaf NNs

### Cellular Sheaf for Influence Flow

```ruby
# lib/influence_propagation.rb
module InfluencePropagation
  def self.trace_idea_adoption(idea:, origin_user:, network:, seed: 0x42D)
    # Use condensed stacks for network structure
    stack = WorldBroadcast::CondensedAnima.analytic_stack(
      network.map { |n| n[:id] }
    )
    
    # Convert to cellular sheaf for diffusion analysis
    sheaf = WorldBroadcast::CondensedAnima.to_cellular_sheaf(stack)
    
    # Trace diffusion through Laplacian
    adoption_timeline = []
    sheaf[:edges].each do |edge|
      if idea_present?(edge[:src], idea)
        adoption_timeline << {
          user: edge[:tgt],
          via: edge[:src],
          confidence: sheaf_similarity(edge)
        }
      end
    end
    
    {
      adoption_timeline: adoption_timeline,
      adoption_rate: adoption_timeline.size.to_f / network.size,
      key_amplifiers: find_amplifiers(adoption_timeline)
    }
  end
  
  def self.second_order_network(center_user:, depth: 2)
    # Profinite approximation for network layers
    direct = get_direct_connections(center_user)
    second = direct.flat_map { |d| get_direct_connections(d) }.uniq
    
    {
      direct_network: direct,
      second_order: second - direct,
      reach_multiplier: second.size.to_f / [direct.size, 1].max
    }
  end
end
```

### DuckDB Network Schema

```sql
CREATE TABLE network_nodes (
    user_id VARCHAR PRIMARY KEY,
    username VARCHAR,
    interaction_count INT,
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    network_depth INT  -- 1 = direct, 2 = second-order
);

CREATE TABLE influence_edges (
    edge_id VARCHAR PRIMARY KEY,
    source_user VARCHAR,
    target_user VARCHAR,
    edge_type VARCHAR,  -- 'follow', 'reply', 'repost', 'quote'
    weight FLOAT,
    created_at TIMESTAMP
);

CREATE TABLE idea_adoptions (
    adoption_id VARCHAR PRIMARY KEY,
    idea_fingerprint VARCHAR,
    user_id VARCHAR,
    adopted_at TIMESTAMP,
    confidence FLOAT,
    via_user VARCHAR  -- who they learned from
);

-- Reach multiplier query
WITH direct AS (
    SELECT COUNT(DISTINCT target_user) as direct_reach
    FROM influence_edges WHERE source_user = ?
),
second_order AS (
    SELECT COUNT(DISTINCT e2.target_user) as second_reach
    FROM influence_edges e1
    JOIN influence_edges e2 ON e1.target_user = e2.source_user
    WHERE e1.source_user = ?
)
SELECT second_reach / NULLIF(direct_reach, 0) as reach_multiplier
FROM direct, second_order;
```

### Hy Perspective Mapping

```hy
;; influence_perspectives.hy
(defclass ThreadNetworkPerspective []
  "Analyze threads from multiple observer perspectives"
  
  (defn __init__ [self]
    (setv self.perspectives {}))
  
  (defn analyze-concept-flow [self acset]
    "Trace how concepts flow through thread network"
    (setv flow {})
    (for [[key rel] (.items acset.related)]
      (setv from-concept (get rel "from"))
      (setv to-concept (get rel "to"))
      (when (not-in from-concept flow)
        (setv (get flow from-concept) {:outgoing [] :incoming []}))
      (when (not-in to-concept flow)
        (setv (get flow to-concept) {:outgoing [] :incoming []}))
      (.append (get (get flow from-concept) "outgoing") to-concept)
      (.append (get (get flow to-concept) "incoming") from-concept))
    flow)
  
  (defn find-concept-hubs [self acset]
    "Find concepts that connect many other concepts (hubs)"
    (setv flow (self.analyze-concept-flow acset))
    (setv hub-scores {})
    (for [[concept data] (.items flow)]
      (setv score (+ (len (get data "outgoing")) 
                     (len (get data "incoming"))))
      (setv (get hub-scores concept) score))
    (sorted (.items hub-scores) :key (fn [x] (get x 1)) :reverse True)))
```

## Influence Metrics

| Metric | Description | Formula |
|--------|-------------|---------|
| reach_multiplier | Amplification factor | second_order / direct |
| adoption_rate | % network adopting | adopters / network_size |
| decay_half_life | Idea persistence | -ln(2) / decay_rate |
| betweenness | Bridge importance | Σ(σ_st(v)/σ_st) |

## GF(3) Triad Integration

| Trit | Skill | Role |
|------|-------|------|
| -1 | **influence-propagation** | Validates network flow patterns |
| 0 | bisimulation-game | Coordinates equivalence checking |
| +1 | pulse-mcp-stream | Generates network data |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## Justfile Recipes

```makefile
# Build network from interactions
influence-build center="barton" depth="2":
    ruby -I lib -r influence_propagation -e "puts InfluencePropagation.second_order_network(center_user: '{{center}}', depth: {{depth}}).to_json"

# Trace idea propagation
influence-trace idea="category theory" days="30":
    duckdb interactions.duckdb -c "SELECT * FROM idea_adoptions WHERE idea_fingerprint LIKE '%{{idea}}%' AND adopted_at > NOW() - INTERVAL '{{days}} days'"

# Hy perspective analysis
influence-hy:
    uv run hy -c "(import influence_perspectives) (print 'Ready')"
```

## Related Skills

- `bisimulation-game` - Network equivalence checking
- `pulse-mcp-stream` (Layer 1) - Live data source
- `cognitive-surrogate` (Layer 6) - Uses perspective data
- `condensed-analytic-stacks` - Sheaf structure for networks
