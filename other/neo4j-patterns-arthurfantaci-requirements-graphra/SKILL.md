---
name: neo4j-patterns
description: Neo4j driver best practices for Python. Use when working with Neo4j connections, Cypher queries, transactions, or GraphRAG implementations.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Neo4j Driver Best Practices

## Connection URI Schemes

| Scheme | Use Case | TLS | Routing |
|--------|----------|-----|---------|
| `neo4j+s://` | Production (Aura, clusters) | ✅ | ✅ |
| `neo4j://` | Local development | ❌ | ✅ |
| `bolt://` | Single instance only | ❌ | ❌ |

**ALWAYS use `neo4j+s://` for production deployments.**

## Driver Instance Pattern

✅ **GOOD** - Create once, reuse:
```python
from contextlib import asynccontextmanager
from neo4j import GraphDatabase

@asynccontextmanager
async def lifespan(app):
    driver = GraphDatabase.driver(
        config.neo4j_uri,
        auth=(config.neo4j_username, config.neo4j_password),
        max_connection_pool_size=5,  # Small for serverless
    )
    driver.verify_connectivity()
    try:
        yield {"driver": driver}
    finally:
        driver.close()
```

❌ **BAD** - Creates new driver per request:
```python
def query(cypher):
    driver = GraphDatabase.driver(...)  # DON'T DO THIS
    result = driver.execute_query(cypher)
    driver.close()
    return result
```

## Transaction Functions

✅ **GOOD** - Use execute_read/execute_write:
```python
def get_articles(driver: Driver, topic: str) -> list[dict]:
    def _query(tx, topic):
        result = tx.run(
            "MATCH (a:Article) WHERE a.topic = $topic RETURN a",
            topic=topic
        )
        return [record.data() for record in result]  # Process IN transaction

    with driver.session(database="neo4j") as session:
        return session.execute_read(_query, topic)
```

❌ **BAD** - Auto-commit with session.run:
```python
def get_articles(driver, topic):
    with driver.session() as session:
        result = session.run(f"MATCH (a:Article) WHERE a.topic = '{topic}' RETURN a")
    return [r.data() for r in result]  # Result consumed OUTSIDE transaction!
```

## Query Parameters

✅ **GOOD** - Always use parameters:
```python
tx.run("MATCH (e) WHERE e.name = $name RETURN e", name=user_input)
```

❌ **BAD** - String concatenation (SQL injection risk):
```python
tx.run(f"MATCH (e) WHERE e.name = '{user_input}' RETURN e")
```

## Serverless Optimization

For Vercel/Lambda deployments:
```python
max_connection_pool_size=5,           # Small pool
connection_acquisition_timeout=30.0,   # Cold start tolerance
```

## Result Processing

**ALWAYS process results within transaction scope:**
```python
def _query(tx, params):
    result = tx.run(query, params)
    return [record.data() for record in result]  # ✅ Inside transaction

# NOT this:
result = session.run(query)
return [record.data() for record in result]  # ❌ Outside transaction
```
