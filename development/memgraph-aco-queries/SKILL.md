---
name: memgraph-aco-queries
description: Query and analyze ACO pheromone graphs in Memgraph. Use for prime candidate queries, pheromone analysis, path validation, and convergence monitoring.
allowed-tools: Bash, Read, Grep, Glob
---

# Memgraph ACO Operations

## Connection
```python
from gqlalchemy import Memgraph
mg = Memgraph(host="localhost", port=7687)
```

## Schema

```cypher
// Nodes
(:PrimeCandidate {value: INT, fitness: FLOAT, visits: INT, is_factor: BOOL})
(:Target {n: INT, sqrt_n: FLOAT, found: BOOL})

// Edges
[:TRAIL {pheromone: FLOAT, updated: TIMESTAMP}]

// Indexes
CREATE INDEX ON :PrimeCandidate(value);
CREATE INDEX ON :PrimeCandidate(fitness);
```

## Common Queries

### Initialize prime candidates
```cypher
UNWIND $primes AS p
CREATE (:PrimeCandidate {value: p, fitness: 0.0, visits: 0, is_factor: false})
```

### Deposit pheromone
```cypher
MATCH (p:PrimeCandidate {value: $prime})
SET p.fitness = CASE WHEN p.fitness < $strength THEN $strength ELSE p.fitness END,
    p.visits = p.visits + 1
```

### Global evaporation
```cypher
MATCH ()-[t:TRAIL]->()
SET t.pheromone = GREATEST(0.01, t.pheromone * 0.95)
```

### Get pheromone-weighted candidates
```cypher
MATCH (p:PrimeCandidate)-[t:TRAIL]->(next)
WHERE p.value = $current
RETURN next.value, t.pheromone
ORDER BY t.pheromone DESC
LIMIT 10
```

### Find high-pheromone paths
```cypher
MATCH path = (start:PrimeCandidate)-[t:TRAIL*1..5]->(end:PrimeCandidate)
WHERE ALL(r IN relationships(path) WHERE r.pheromone > 0.5)
RETURN path, reduce(s = 0, r IN relationships(path) | s + r.pheromone) AS total
ORDER BY total DESC
LIMIT 10
```

### Mark factor found
```cypher
MATCH (p:PrimeCandidate {value: $factor})
SET p.is_factor = true, p.fitness = 1.0
```

### Convergence check
```cypher
MATCH (p:PrimeCandidate)
WHERE p.fitness > 0.8
RETURN count(p) AS hot_candidates, avg(p.fitness) AS avg_fitness
```
