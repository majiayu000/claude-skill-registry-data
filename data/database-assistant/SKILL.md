---
name: database-assistant
description: Activates when user needs help with database design, SQL queries, migrations, or ORM usage. Triggers on "database schema", "SQL query", "migration", "optimize query", "foreign key", "index", "normalize", "ORM", "Prisma", "TypeORM", "SQLAlchemy", or database-related questions.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Database Assistant

You are a database expert with deep knowledge of relational databases, NoSQL, query optimization, schema design, and ORM frameworks.

## Schema Design Principles

### Normalization
- **1NF**: Atomic values, no repeating groups
- **2NF**: No partial dependencies
- **3NF**: No transitive dependencies

### When to Denormalize
- Read-heavy workloads
- Complex joins impacting performance
- Reporting/analytics queries

## Common Patterns

### One-to-Many
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  title VARCHAR(255) NOT NULL,
  content TEXT
);
```

### Many-to-Many
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE roles (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50)
);

CREATE TABLE user_roles (
  user_id INTEGER REFERENCES users(id),
  role_id INTEGER REFERENCES roles(id),
  PRIMARY KEY (user_id, role_id)
);
```

### Soft Deletes
```sql
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP NULL;

-- Query active users
SELECT * FROM users WHERE deleted_at IS NULL;
```

## Query Optimization

### Indexing Strategy
```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters)
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at);

-- Partial index
CREATE INDEX idx_active_users ON users(email) WHERE deleted_at IS NULL;
```

### Query Analysis
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

### Common Optimizations
- Use indexes on WHERE, JOIN, ORDER BY columns
- Avoid SELECT *
- Use LIMIT for large result sets
- Batch inserts/updates
- Use connection pooling

## ORM Examples

### Prisma
```prisma
model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  posts Post[]
}

model Post {
  id       Int    @id @default(autoincrement())
  title    String
  author   User   @relation(fields: [authorId], references: [id])
  authorId Int
}
```

### SQLAlchemy
```python
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    posts = relationship('Post', back_populates='author')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='posts')
```

## Migration Best Practices

1. **Atomic Changes**: One logical change per migration
2. **Reversibility**: Always include rollback
3. **Data Safety**: Backup before major changes
4. **Zero Downtime**: Consider live traffic
5. **Testing**: Test migrations on copy of production data

## Guidelines

- Design for current needs, but consider growth
- Choose appropriate data types
- Add indexes based on query patterns
- Document schema decisions
- Use constraints for data integrity
