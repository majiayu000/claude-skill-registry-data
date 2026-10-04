---
name: "Stack: Cypher"
description: "Neo4j and Cypher: graph schema design, query patterns, performance optimisation, PostgreSQL integration."
when_to_use: "When writing or reviewing Cypher queries, designing a graph schema or bridging Neo4j with a relational store; the Cypher can live in .cypher files or embedded strings."
user-invocable: false
metadata:
  family: clod-stack
# No paths gate: Cypher mostly lives inside .ts strings, not .cypher files, so
# file identity is an unreliable proxy for relevance
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Neo4j/Cypher Mastery

Comprehensive guide to Neo4j graph database and Cypher query language. Covers fundamental concepts, common patterns, performance optimisation, schema design and integration with PostgreSQL/Supabase.

## When This Skill Applies

Use this skill when:

- Writing Cypher queries
- Designing graph schemas
- Optimising graph traversals
- Building recommendation systems
- Modelling hierarchies or networks
- Integrating Neo4j with relational databases
- Questions about graph database patterns

## Core Concepts

### Nodes, Relationships, Properties

**Nodes** - Entities (nouns):
```cypher
// Simple node
CREATE (u:User)

// Node with properties
CREATE (u:User {
  id: 'user-123',
  name: 'Alice',
  email: 'alice@example.com'
})

// Multiple labels
CREATE (p:Person:Developer {name: 'Bob'})
```

**Relationships** - Connections (verbs):
```cypher
// Simple relationship
CREATE (a)-[:FOLLOWS]->(b)

// Relationship with properties
CREATE (a)-[:FOLLOWS {since: date(), strength: 'strong'}]->(b)

// Relationship types are UPPERCASE by convention
CREATE (a)-[:MEMBER_OF {role: 'admin'}]->(org)
```

**Properties** - Attributes (key-value pairs):
```cypher
// Node properties
{
  id: 'user-123',
  name: 'Alice',
  age: 30,
  verified: true,
  createdAt: datetime()
}

// Relationship properties
{
  since: date(),
  weight: 0.85,
  type: 'professional'
}
```

### Graph Thinking

**Relational mindset**:
```sql
-- Joins and foreign keys
SELECT * FROM users u
JOIN follows f ON f.follower_id = u.id
JOIN users u2 ON f.followed_id = u2.id
WHERE u.id = '123';
```

**Graph mindset**:
```cypher
// Pattern matching
MATCH (u:User {id: '123'})-[:FOLLOWS]->(friend)
RETURN friend;
```

**Key difference**: Relationships are first-class citizens in graphs.

## Cypher Fundamentals

### MATCH - Finding Patterns

**Basic pattern**:
```cypher
// Find all users
MATCH (u:User)
RETURN u;

// Find users with specific property
MATCH (u:User {name: 'Alice'})
RETURN u;

// Find users matching condition
MATCH (u:User)
WHERE u.age > 25
RETURN u;
```

**Relationship patterns**:
```cypher
// Outgoing relationship
MATCH (a)-[:FOLLOWS]->(b)
RETURN a, b;

// Incoming relationship
MATCH (a)<-[:FOLLOWS]-(b)
RETURN a, b;

// Any direction
MATCH (a)-[:FOLLOWS]-(b)
RETURN a, b;

// Multiple relationships
MATCH (a)-[:FOLLOWS]->(b)-[:FOLLOWS]->(c)
RETURN a, b, c;

// Variable length
MATCH (a)-[:FOLLOWS*1..3]->(b)
RETURN a, b;
```

### CREATE - Adding Data

**Create nodes**:
```cypher
// Single node
CREATE (u:User {id: 'user-123', name: 'Alice'})
RETURN u;

// Multiple nodes
CREATE
  (a:User {name: 'Alice'}),
  (b:User {name: 'Bob'}),
  (c:User {name: 'Charlie'});
```

**Create relationships**:
```cypher
// Find existing nodes, create relationship
MATCH (a:User {name: 'Alice'})
MATCH (b:User {name: 'Bob'})
CREATE (a)-[:FOLLOWS]->(b);

// Create nodes and relationships together
CREATE (a:User {name: 'Alice'})-[:FOLLOWS]->(b:User {name: 'Bob'});
```

### MERGE - Create or Match

**Create if not exists**:
```cypher
// Create user only if doesn't exist
MERGE (u:User {id: 'user-123'})
ON CREATE SET u.name = 'Alice', u.createdAt = datetime()
ON MATCH SET u.lastSeen = datetime()
RETURN u;

// Create relationship only if doesn't exist
MATCH (a:User {id: 'user-123'})
MATCH (b:User {id: 'user-456'})
MERGE (a)-[r:FOLLOWS]->(b)
ON CREATE SET r.since = datetime()
RETURN r;
```

**Important**: MERGE matches on entire pattern:
```cypher
// This matches on ALL properties
MERGE (u:User {id: 'user-123', name: 'Alice'})

// Better: Match on unique constraint only
MERGE (u:User {id: 'user-123'})
SET u.name = 'Alice'
```

### SET - Updating Properties

```cypher
// Set single property
MATCH (u:User {id: 'user-123'})
SET u.name = 'Alicia'
RETURN u;

// Set multiple properties
MATCH (u:User {id: 'user-123'})
SET u.name = 'Alicia', u.verified = true
RETURN u;

// Set properties from map
MATCH (u:User {id: 'user-123'})
SET u += {name: 'Alicia', age: 31}
RETURN u;

// Add label
MATCH (u:User {id: 'user-123'})
SET u:Verified
RETURN u;
```

### DELETE - Removing Data

```cypher
// Delete node (only if no relationships)
MATCH (u:User {id: 'user-123'})
DELETE u;

// Delete node and all relationships
MATCH (u:User {id: 'user-123'})
DETACH DELETE u;

// Delete relationship only
MATCH (a:User)-[r:FOLLOWS]->(b:User)
WHERE a.id = 'user-123' AND b.id = 'user-456'
DELETE r;

// Delete properties
MATCH (u:User {id: 'user-123'})
REMOVE u.age, u.verified
RETURN u;
```

### RETURN - Formatting Results

```cypher
// Return nodes
MATCH (u:User)
RETURN u;

// Return specific properties
MATCH (u:User)
RETURN u.id, u.name;

// Alias properties
MATCH (u:User)
RETURN u.name AS userName, u.email AS userEmail;

// Return count
MATCH (u:User)
RETURN count(u) AS totalUsers;

// Return distinct
MATCH (u:User)-[:FOLLOWS]->(friend)
RETURN DISTINCT friend.name;
```

## Additional resources

Worked query patterns and mechanical detail, loaded only when needed:

- [query-patterns.md](query-patterns.md): social graph (followers, blocking), hierarchy (org charts, categories), recommendation (collaborative/content-based filtering), path-finding (shortest path, Dijkstra), access control
- [performance-and-schema.md](performance-and-schema.md): indexes/constraints, PROFILE-driven optimisation tips, batch operations with UNWIND/APOC, schema modelling guidelines (relationships vs properties, multiple labels)
- [postgres-integration.md](postgres-integration.md): shared-key and event-driven sync patterns with Supabase, hybrid query examples

## Success Criteria

Neo4j implementation is successful when:

- Queries leverage graph traversal strengths
- Indexes on frequently queried properties
- Bounded traversals (not unbounded `*`)
- Clear distinction between nodes/relationships/properties
- Integration with relational database clean
- Performance acceptable for use case
- Schema supports future requirements
