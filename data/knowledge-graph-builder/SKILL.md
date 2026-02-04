---
name: knowledge-graph-builder
description: Designs and builds knowledge graphs to represent entities, relationships, and semantic connections, with query patterns for Neo4j, RDF, and property graphs.
license: MIT
---

# Knowledge Graph Builder

This skill provides guidance for designing knowledge graphs that capture entities, relationships, and semantic meaning for powerful querying and reasoning.

## Core Competencies

- **Graph Modeling**: Entity-relationship design for graphs
- **Query Languages**: Cypher (Neo4j), SPARQL (RDF), Gremlin
- **Ontology Design**: Schema, taxonomies, semantic relationships
- **Graph Algorithms**: Pathfinding, centrality, community detection

## Knowledge Graph Fundamentals

### What Makes a Knowledge Graph

```
Knowledge Graph = Entities + Relationships + Schema + Semantics

Traditional Database:           Knowledge Graph:
┌────────────────────┐         ┌─────────────────────────────┐
│ Tables with rows   │         │ (Person)──KNOWS──▶(Person)  │
│ Foreign keys       │   vs    │     │                       │
│ JOIN operations    │         │   WORKS_AT                  │
│                    │         │     ▼                       │
└────────────────────┘         │ (Company)──IN──▶(Industry)  │
                               └─────────────────────────────┘
```

### When to Use Knowledge Graphs

| Use Case | Why Graphs Excel |
|----------|------------------|
| Recommendation systems | Traverse connections to find related items |
| Fraud detection | Identify suspicious relationship patterns |
| Knowledge management | Connect concepts and infer relationships |
| Master data management | Unify entities across systems |
| Root cause analysis | Follow causal chains through dependencies |

## Graph Data Modeling

### Entity Design

Identify core entities (nodes):

```cypher
// Person entity with properties
CREATE (p:Person {
    id: 'p001',
    name: 'Alice Chen',
    email: 'alice@example.com',
    created_at: datetime()
})

// Multiple labels for categorization
CREATE (c:Organization:Company:TechCompany {
    id: 'c001',
    name: 'Acme Corp',
    founded: 2010
})
```

### Relationship Design

Model connections with typed, directed edges:

```cypher
// Simple relationship
(person)-[:WORKS_AT]->(company)

// Relationship with properties
(person)-[:WORKS_AT {
    role: 'Engineer',
    start_date: date('2020-01-15'),
    department: 'Engineering'
}]->(company)

// Temporal relationships
(person)-[:EMPLOYED_BY {
    from: date('2018-01-01'),
    to: date('2020-12-31')
}]->(company1)
(person)-[:EMPLOYED_BY {
    from: date('2021-01-01')
}]->(company2)
```

### Common Relationship Patterns

```
Hierarchical:     (Child)──IS_CHILD_OF──▶(Parent)
                  (Employee)──REPORTS_TO──▶(Manager)

Associative:      (Person)──KNOWS──▶(Person)
                  (Document)──REFERENCES──▶(Document)

Temporal:         (Event)──PRECEDES──▶(Event)
                  (Version)──SUPERSEDES──▶(Version)

Categorical:      (Product)──BELONGS_TO──▶(Category)
                  (Concept)──IS_A──▶(Category)

Spatial:          (Location)──NEAR──▶(Location)
                  (Region)──CONTAINS──▶(City)
```

### Schema Definition

```cypher
// Node constraints
CREATE CONSTRAINT person_id IF NOT EXISTS
FOR (p:Person) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT company_id IF NOT EXISTS
FOR (c:Company) REQUIRE c.id IS UNIQUE;

// Property existence
CREATE CONSTRAINT person_name IF NOT EXISTS
FOR (p:Person) REQUIRE p.name IS NOT NULL;

// Indexes for query performance
CREATE INDEX person_name_idx IF NOT EXISTS
FOR (p:Person) ON (p.name);

CREATE INDEX company_industry_idx IF NOT EXISTS
FOR (c:Company) ON (c.industry);
```

## Cypher Query Patterns

### Basic Traversal

```cypher
// Find all colleagues (people who work at same company)
MATCH (person:Person {name: 'Alice Chen'})-[:WORKS_AT]->(company)
      <-[:WORKS_AT]-(colleague:Person)
WHERE colleague <> person
RETURN colleague.name, company.name

// Variable-length paths (1-3 hops)
MATCH path = (start:Person)-[:KNOWS*1..3]->(end:Person)
WHERE start.name = 'Alice Chen' AND end.name = 'Bob Smith'
RETURN path, length(path) as hops
```

### Aggregation

```cypher
// Count relationships
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN c.name, count(p) as employee_count
ORDER BY employee_count DESC

// Collect into lists
MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)
RETURN p.name, collect(s.name) as skills
```

### Recommendations

```cypher
// "People you may know" - friends of friends
MATCH (me:Person {id: $userId})-[:KNOWS]-(friend)-[:KNOWS]-(suggestion)
WHERE NOT (me)-[:KNOWS]-(suggestion) AND me <> suggestion
RETURN suggestion.name, count(friend) as mutual_friends
ORDER BY mutual_friends DESC
LIMIT 10

// Content-based: similar interests
MATCH (me:Person {id: $userId})-[:INTERESTED_IN]->(topic)
      <-[:INTERESTED_IN]-(similar:Person)
WHERE me <> similar
WITH similar, count(topic) as shared_interests
ORDER BY shared_interests DESC
RETURN similar.name, shared_interests
LIMIT 10
```

### Path Analysis

```cypher
// Shortest path
MATCH path = shortestPath(
    (start:Person {name: 'Alice'})-[:KNOWS*]-(end:Person {name: 'Bob'})
)
RETURN path, length(path)

// All shortest paths
MATCH path = allShortestPaths(
    (start:Person)-[:KNOWS*]-(end:Person)
)
WHERE start.name = 'Alice' AND end.name = 'Bob'
RETURN path
```

## Graph Algorithms

### Centrality Measures

| Algorithm | Purpose | Use Case |
|-----------|---------|----------|
| Degree | Connection count | Find popular nodes |
| Betweenness | Bridge detection | Find brokers/bottlenecks |
| PageRank | Influence propagation | Rank importance |
| Closeness | Average distance | Find well-connected nodes |

```cypher
// Using Neo4j Graph Data Science
CALL gds.pageRank.stream('myGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC
LIMIT 10
```

### Community Detection

```cypher
// Louvain for community detection
CALL gds.louvain.stream('myGraph')
YIELD nodeId, communityId
RETURN communityId, collect(gds.util.asNode(nodeId).name) as members
ORDER BY size(members) DESC
```

## Knowledge Graph Patterns

### Entity Resolution

```cypher
// Find potential duplicates
MATCH (p1:Person), (p2:Person)
WHERE p1.id < p2.id
  AND (p1.email = p2.email
       OR (p1.name = p2.name AND p1.birth_date = p2.birth_date))
RETURN p1, p2

// Merge duplicates
MATCH (p1:Person {id: 'keep'}), (p2:Person {id: 'duplicate'})
CALL apoc.refactor.mergeNodes([p1, p2], {
    properties: 'combine',
    mergeRels: true
})
YIELD node
RETURN node
```

### Semantic Layering

```
┌─────────────────────────────────────────────────────┐
│                 Instance Layer                       │
│   (Alice)──KNOWS──▶(Bob)                            │
│   (Alice)──WORKS_AT──▶(Acme)                        │
├─────────────────────────────────────────────────────┤
│                  Schema Layer                        │
│   (:Person)──CAN_KNOW──▶(:Person)                   │
│   (:Person)──CAN_WORK_AT──▶(:Company)               │
├─────────────────────────────────────────────────────┤
│                 Ontology Layer                       │
│   (Person)──IS_A──▶(Agent)                          │
│   (Company)──IS_A──▶(Organization)                  │
└─────────────────────────────────────────────────────┘
```

### Temporal Modeling

```cypher
// State over time
CREATE (person)-[:HAS_STATE {
    valid_from: date('2020-01-01'),
    valid_to: date('2020-12-31')
}]->(state:PersonState {
    status: 'employed',
    salary: 80000
})

// Query state at point in time
MATCH (p:Person {id: $personId})-[r:HAS_STATE]->(s)
WHERE r.valid_from <= date($queryDate)
  AND (r.valid_to IS NULL OR r.valid_to >= date($queryDate))
RETURN s
```

## Best Practices

### Modeling Guidelines

1. **Prefer relationships over properties** when the connection has meaning
2. **Use specific relationship types** (`:MANAGES` not `:RELATED_TO`)
3. **Model for your queries** - understand access patterns first
4. **Keep properties atomic** - no arrays for searchable data
5. **Version nodes, not graphs** - temporal properties on relationships

### Performance Tips

- Index properties used in WHERE clauses
- Use parameters ($userId) not string concatenation
- Limit variable-length paths (*1..5 not *)
- Profile queries with EXPLAIN and PROFILE
- Consider relationship direction in traversals

## References

- `references/cypher-patterns.md` - Advanced Cypher query examples
- `references/graph-modeling.md` - Entity and relationship design patterns
- `references/graph-algorithms.md` - Algorithm selection and configuration
