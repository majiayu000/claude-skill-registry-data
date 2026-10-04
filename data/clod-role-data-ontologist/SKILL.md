---
name: "Role: Data Ontologist"
description: "Polyglot persistence: when to use relational, graph or document databases; integration patterns."
when_to_use: "When choosing a data store or storage pattern for new data, or reviewing a schema or migration; fires on 'which database', 'relational vs graph' and cross-store integration questions."
user-invocable: false
metadata:
  family: clod-role
# No paths gate: "which database?" conversations happen before any schema or
# migration file exists; the skill's core moment has no matching files
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Polyglot Persistence Architecture

Architectural guidance for using multiple database technologies together, with emphasis on PostgreSQL/Supabase (relational), Neo4j (graph), and MongoDB (document). Demonstrates when to use each database type and how to integrate them effectively.

## When This Skill Applies

Use this skill when:

- Designing data architecture for new projects
- Choosing between relational, graph and document databases
- Integrating multiple database types
- Schema design decisions
- Query optimisation across databases
- Migration strategies
- Questions about when to use which database paradigm

## Core Principle

**Start with the graph. Optimise from there.**

Most real-world domains are fundamentally about relationships. The graph is the truest representation of how entities connect. Start by thinking in nodes and edges, then decide where to persist based on access patterns and consistency needs.

**Right database for right data concern**

Don't force all data into one database type. Use:

- **Relational (PostgreSQL/Supabase)** - Structured data, transactions, strong consistency
- **Graph (Neo4j)** - Relationships as primary concern, traversal queries
- **Document (MongoDB)** - Semi-structured data, flexible schemas, nested documents

### Graph-First Modelling Process

Before choosing databases, model the domain as a graph:

1. **Identify nodes**: What are the entities? (Users, Courses, Organisations, Products)
2. **Identify edges**: How do they connect? (ENROLLED_IN, REPORTS_TO, PURCHASED)
3. **Annotate edges**: Do relationships carry data? (role, since, quantity)
4. **Spot patterns**: Trees? DAGs? Social graphs? Bipartite structures?
5. **Then persist**: Given the graph, which parts need relational guarantees, which need traversal, which need flexible schemas?

```cypher
// Step 1-3: Model the domain as a graph first
(:User)-[:MEMBER_OF {role: 'admin', since: date}]->(:Organisation)
(:User)-[:ENROLLED_IN {status: 'active'}]->(:Course)
(:Course)-[:REQUIRES]->(:Course)
(:User)-[:COMPLETED {score: 0.85}]->(:Module)
(:Module)-[:BELONGS_TO]->(:Course)
```

Then decide:

- Users and Organisations → **PostgreSQL** (transactional, auth, billing)
- MEMBER_OF, ENROLLED_IN, REQUIRES → **Neo4j** (traversal, recommendations, paths)
- Course content, Module materials → **MongoDB** (flexible nested content)

## When to Use Relational (PostgreSQL/Supabase)

### Strong Fit

**Transactional Data**:
- User accounts and authentication
- Order processing
- Financial records
- Inventory management

**Structured Records**:
- Clear schema with defined fields
- Data fits naturally into tables
- ACID guarantees required
- Standard CRUD operations
- Strong data integrity constraints

**Examples**:

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Orders table
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  total DECIMAL(10,2),
  status TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Weak Fit

**Highly Connected Data**:
- Social networks (many-to-many relationships)
- Recommendation engines
- Organizational hierarchies with flexible depth

**Reason**: Joins become expensive, recursive queries complex.

**Rapidly Evolving Schemas**:
- Frequently adding new fields
- Different record types need different fields
- Exploratory data modelling

**Reason**: Migrations expensive, rigid structure.

## When to Use Graph (Neo4j)

### Strong Fit

**Relationships as Primary Concern**:
- Social graphs (followers, friends, connections)
- Recommendation systems (collaborative filtering)
- Knowledge graphs
- Access control with inheritance
- Dependencies and prerequisites

**Variable-Depth Traversals**:
- "Find all users within 3 degrees"
- "Shortest path between entities"
- "All ancestors in org chart"
- "Courses needed before advanced topic"

**Examples**:

```cypher
// Social connections
(:User)-[:FOLLOWS]->(:User)
(:User)-[:BLOCKED]->(:User)

// Learning paths
(:Course)-[:REQUIRES]->(:Course)
(:User)-[:COMPLETED]->(:Course)

// Organizational structure
(:Person)-[:REPORTS_TO]->(:Person)
(:Person)-[:MEMBER_OF]->(:Team)
```

### Weak Fit

**Simple Lookups**:
- User by email
- Order by ID
- Product details

**Reason**: Relational databases excel at indexed lookups.

**Large Aggregations**:
- Sum all orders this month
- Count users by region
- Analytics dashboards

**Reason**: SQL aggregations and window functions more powerful.

## When to Use Document (MongoDB)

### Strong Fit

**Semi-Structured Data**:
- Content management systems (blog posts, articles)
- Product catalogs with varying attributes
- User-generated content
- Configuration data
- API responses that need storage

**Nested/Embedded Data**:
- Comments within posts
- Order items within orders
- Addresses within user profiles
- Metadata with varying fields

**Flexible Schemas**:
- Rapid prototyping
- Evolving data models
- Different document types in same collection
- Optional fields vary by record

**Examples**:

```javascript
// Blog post with embedded comments
{
  _id: ObjectId("..."),
  title: "Getting Started with SvelteKit",
  slug: "getting-started-sveltekit",
  author: { id: "user-123", name: "Alice" },
  content: "...",
  tags: ["svelte", "javascript", "tutorial"],
  comments: [
    { id: "comment-1", userId: "user-456", text: "Great article!", createdAt: ISODate("2024-01-15") }
  ],
  metadata: { views: 1250, readingTime: "5 min" },
  publishedAt: ISODate("2024-01-10")
}

// Product with varying attributes
{
  _id: ObjectId("..."),
  name: "Laptop",
  category: "electronics",
  price: 999.99,
  specs: { cpu: "Intel i7", ram: "16GB", storage: "512GB SSD", screen: "15.6 inch" }
}

// Different product type, different fields
{
  _id: ObjectId("..."),
  name: "T-Shirt",
  category: "clothing",
  price: 29.99,
  sizes: ["S", "M", "L", "XL"],
  colors: ["black", "white", "blue"],
  material: "100% cotton"
}
```

### Weak Fit

**Complex Transactions**:
- Multi-step financial operations
- Strong ACID guarantees across documents
- Complex foreign key relationships

**Reason**: Relational databases better at multi-document transactions.

**Relationship-Heavy Data**:
- Social networks
- Graph traversals
- "Friends of friends" queries

**Reason**: Graph databases handle this natively.

**Highly Normalised Data**:
- No duplication tolerance
- Frequent joins needed
- Strong referential integrity

**Reason**: Relational databases enforce this better.

## Decision Framework

### Question 1: What's the primary data concern?

**RELATIONSHIPS** → Neo4j (Graph): social connections, recommendations, dependency trees, path finding

**STRUCTURED ENTITIES** → PostgreSQL (Relational): user accounts, financial transactions, inventory, orders

**DOCUMENTS/CONTENT** → MongoDB (Document): blog posts, product catalogs, CMS content, API data storage

### Question 2: How stable is your schema?

**VERY STABLE** → PostgreSQL: well-defined entities, clear field types, rare schema changes, strong typing needed

**EVOLVING** → MongoDB: prototyping phase, frequently adding fields, different record structures, flexible modelling

**SCHEMA-OPTIONAL** → Neo4j: relationships more important than structure, dynamic properties, graph structure evolves

### Question 3: How is data accessed?

**BY KEY/ID** → PostgreSQL or MongoDB: user by email, product by SKU, order by ID

**BY TRAVERSAL** → Neo4j: friends of friends, shortest path, recommendations

**BY CONTENT/QUERY** → MongoDB: full-text search, filtering nested documents, flexible queries on varying fields

### Question 4: Do you need strong consistency?

**ABSOLUTE** → PostgreSQL: financial transactions, ACID guarantees, multi-step operations

**EVENTUAL OKAY** → MongoDB or Neo4j: content updates, social interactions, non-critical data

### Question 5: Is data naturally nested?

**YES** → MongoDB: posts with comments, orders with line items, documents with metadata

**NO** → PostgreSQL: flat entities, many-to-many relationships, normalised structure

## Additional resources

Worked examples and mechanical detail, loaded only when needed:

- [real-world-examples.md](real-world-examples.md): four full worked splits (social app, learning platform, e-commerce, CMS) showing which data lives where and why
- [integration-and-schema.md](integration-and-schema.md): shared-key/reference/embed/event-sync/aggregation integration patterns, per-database schema design, query optimisation and indexing
- [anti-patterns-and-migration.md](anti-patterns-and-migration.md): common mistakes (document-DB transactions, over-embedding, graph for simple lookups), migration strategy and worked migration scripts

## Success Criteria

Architecture is successful when:

- Each database handles what it does best
- Queries are fast (minimal cross-database operations)
- Data consistency maintained appropriately
- Clear reasoning for database placement
- Can scale databases independently
- Schema evolution manageable
- Team understands the architecture
