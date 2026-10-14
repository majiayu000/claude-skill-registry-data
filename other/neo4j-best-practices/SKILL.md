---
name: neo4j-best-practices
description: Neo4j best practices for Cypher query optimization, graph data modeling, indexing, and safe execution of LLM-generated Cypher
scope: core
user-invocable: false
---

# Neo4j Best Practices

## Query Optimization

### PROFILE / EXPLAIN (CRITICAL)
- Use `EXPLAIN` to validate a query plan without executing it — the mandatory pre-execution gate for any generated Cypher
- Use `PROFILE` to see actual DB hits, rows, and time per operator when a query is already known-safe
- Watch for `NodeByLabelScan`/`AllNodesScan` where an index seek (`NodeIndexSeek`) was expected — usually a missing index or non-sargable predicate
- Watch for `CartesianProduct` — almost always an unintended disconnected pattern; add a relationship or `WHERE` join condition
- Watch for `Eager` operators — they materialize the whole intermediate result and block streaming; common with `MERGE` combined with earlier writes/reads in the same query

### Query Shape (CRITICAL)
- Filter as early as possible — put label and property predicates on the first `MATCH`, not after a chain of traversals
- Use `WHERE` on indexed properties, not on computed/derived expressions (kills index usage)
- Prefer directed, typed relationship patterns (`-[:FOLLOWS]->`) over untyped/undirected ones — undirected patterns force the planner to consider both directions
- Bound variable-length paths (`[:LINKS*1..3]`) — unbounded (`*`) traversals on non-trivial graphs risk combinatorial blowup
- Use `LIMIT` with `ORDER BY` early in multi-part queries (`WITH ... LIMIT ...`) to avoid sorting the full result set

## Data Modeling

### Node Labels vs Properties (CRITICAL)
- A value becomes a **label** when it is used to filter/scan a large subset of the graph, participates in relationships, or needs its own indexes/constraints
- A value stays a **property** when it is descriptive, high-cardinality, or never independently queried
- Avoid modeling everything as generic `Entity` nodes with a `type` property — this collapses the type system into runtime string comparisons and defeats label-based indexing

### Relationships (CRITICAL)
- Relationship type encodes the semantic verb (`:PURCHASED`, `:AUTHORED`) — do not reuse one generic relationship type (`:RELATED_TO`) with a property to distinguish meaning
- Choose a single consistent direction per relationship type based on the dominant query direction; query the reverse direction with `<-[]-` rather than modeling both directions
- Avoid supernodes: a node with relationship fan-out in the tens of thousands (e.g., a "Country" node connected to every citizen) degrades traversal and lock behavior — consider intermediate/bucket nodes

### Time and History
- Model temporal facts as relationship properties (`since`, `until`) or intermediate event nodes when a fact changes over time, rather than overwriting node properties and losing history

## Indexes and Constraints

### Index Types (CRITICAL)
- Range index: default for equality/range lookups on scalar properties — create for every property used in `WHERE`/`MERGE` matching at scale
- Text index: substring/`CONTAINS`/`ENDS WITH` queries on string properties (range indexes only accelerate prefix/exact matches)
- Point index: spatial `point()` property queries
- Full-text index: relevance-ranked, tokenized text search (`db.index.fulltext.queryNodes`)

### Constraints (CRITICAL)
- Uniqueness constraint on every natural key used for `MERGE` — without it, concurrent `MERGE` can create duplicate nodes
- Property-existence constraint (Enterprise) for properties the application always expects to be present
- Constraints implicitly create a backing index — do not create a redundant explicit index on the same property

## Go Driver (neo4j-go-driver v5)

### Session and Transaction Management (CRITICAL)
- One `neo4j.DriverWithContext` per process; open short-lived `Session`s per unit of work, never share a session across goroutines
- Use `ExecuteRead`/`ExecuteWrite` (managed transactions) instead of manual `BeginTransaction` — they provide automatic retry on transient errors (leader switch, deadlock)
- Never build Cypher via string concatenation/`fmt.Sprintf` with user data — always pass a `map[string]any` of parameters as the second argument to `Run`/`ExecuteRead`
- Set explicit context timeouts (`context.WithTimeout`) on every session/transaction to bound worst-case latency
- Configure `neo4j.Config.MaxConnectionPoolSize` and `ConnectionAcquisitionTimeout` for the expected concurrency; do not leave pool size unbounded

### Result Handling
- Prefer `result.Collect(ctx)` for small bounded results, streaming iteration (`result.Next(ctx)`) for large results — avoid materializing unbounded result sets in memory

## Safe Execution of LLM-Generated Cypher (CRITICAL)

This is the primary safety layer for any natural-language-to-Cypher feature.

1. **Read-only enforcement**: execute generated Cypher only through a session/user restricted to the `reader` role (or `neo4j.AccessModeRead` on the transaction), never a writer-capable session
2. **Mandatory parameterization**: reject any generated query that embeds literal values instead of `$param` placeholders — this also defends against Cypher injection from upstream LLM output
3. **Pre-execution `EXPLAIN` gate**: run `EXPLAIN <query>` first; reject on syntax/semantic errors before touching real data, and inspect the plan for scan operators that indicate a missing index or runaway cardinality
4. **Destructive-clause blocklist**: statically reject queries containing `DETACH DELETE`, `DELETE`, `REMOVE`, `SET`, `CREATE`, `MERGE`, `CALL { ... } IN TRANSACTIONS`, `LOAD CSV`, or any `apoc.*` write/refactor procedure — a read-only-role session is defense-in-depth, not a substitute for this check
5. **Query complexity bounds**: cap unbounded variable-length paths, enforce a default `LIMIT`, and set a server-side query timeout for LLM-originated queries specifically (`dbms.transaction.timeout` or a per-query `neo4j.WithTxTimeout`)
6. **No local text2cypher models**: this project uses remote LLM APIs only — do not introduce Neo4j's locally-hosted text2cypher fine-tuned models or any component requiring local inference weights

## PostgreSQL-as-Source-of-Truth Pattern

- Treat Neo4j as a **rebuildable projection** of PostgreSQL, not an independent system of record — every node/relationship should be traceable back to a Postgres row
- Prefer full-rebuild-from-Postgres for correctness-critical launches; move to incremental sync (CDC, outbox pattern, or scheduled diff) only once the projection shape has stabilized
- Version the projection logic (mapping Postgres tables/columns to Cypher `MERGE` statements) alongside schema migrations so the graph can always be regenerated deterministically
- Do not accept direct writes to Neo4j from application code paths that bypass the sync/rebuild pipeline — this breaks the rebuildability guarantee

## References
- [Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [Cypher Query Tuning](https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/)
- [Neo4j Go Driver Manual](https://neo4j.com/docs/go-manual/current/)
- [neo4j-go-driver Go package docs](https://pkg.go.dev/github.com/neo4j/neo4j-go-driver/v5/neo4j)
- [Index Configuration](https://neo4j.com/docs/operations-manual/current/performance/index-configuration/)
- [Constraints](https://neo4j.com/docs/cypher-manual/current/constraints/)
- [Graph Data Modeling Guide](https://neo4j.com/docs/getting-started/data-modeling/guide-data-modeling/)
- [Access Control / Roles](https://neo4j.com/docs/operations-manual/current/authentication-authorization/access-control/)
