---
name: ecto-query-analysis
description: Analyzes Ecto queries for N+1 problems, missing preloads, and performance issues.
---

# Ecto Query Analysis Skill

Use this skill to analyze Ecto queries for performance issues and optimization opportunities.

## When to Use

- Reviewing Ecto query code
- Investigating slow database queries
- Optimizing database access patterns
- Designing database schemas for performance

## Common Issues

### N+1 Query Problem

**Symptom**: Multiple database queries executed in a loop to fetch associated data.

**Example**:
```elixir
# ❌ Bad - N+1 query problem
def get_users_with_posts do
  users = Repo.all(User)
  Enum.map(users, fn user ->
    posts = Repo.all(from p in Post, where: p.user_id == ^user.id)
    %{user: user, posts: posts}
  end)
end

# ✅ Good - Preload associations
def get_users_with_posts do
  User
  |> preload([:posts])
  |> Repo.all()
end
```

### Missing Indexes

**Symptom**: Frequent queries on non-indexed columns are slow.

**Example**:
```elixir
# ❌ Bad - No index on frequently queried column
# Query: WHERE email = '...' on large table
# Result: Slow sequential scan

# ✅ Good - Add index
# CREATE INDEX users_email_idx ON users(email)
# Query becomes fast index scan
```

### Large Result Sets

**Symptom**: Loading all records into memory unnecessarily.

**Example**:
```elixir
# ❌ Bad - Loading all records
def list_users, do: Repo.all(User)

# ✅ Good - Pagination
def list_users(page, per_page \\ 20) do
  User
  |> limit(^per_page)
  |> offset((page - 1) * ^per_page)
  |> Repo.all()
end
```

## Optimization Strategies

### Preloading

**Associations**: Always preload associations to prevent N+1 queries.

```elixir
# Single association
User |> preload([:posts]) |> Repo.one()

# Multiple associations
User |> preload([:posts, :profile, :settings]) |> Repo.one()

# Nested associations
User |> preload([profile: [:avatar, [:background]]) |> Repo.one()
```

### Selective Preloading

**Only Load Needed Fields**:
```elixir
# Instead of preload(:posts) which loads all fields
User
|> Ash.Query.for_read()
|> Ash.Query.load([:posts, published_posts: [:author]])
|> Ash.Query.filter(posts[:published] == true)
|> Ash.read!()
```

### Query Optimization

**Use Ash Aggregates**:
```elixir
# Instead of loading all posts then counting
def count_published_posts(user_id) do
  Post
  |> Ash.Query.aggregate([:count], :first)
  |> Ash.Query.filter(author_id == ^user_id)
  |> Ash.Query.filter(status == :published)
  |> Ash.read_one!()
end
```

**Use Window Functions**:
```elixir
# Calculate stats efficiently
def get_user_stats(user_id) do
  stats = User
  |> Ash.Query.aggregate([:count, :max_age], :first)
  |> Ash.Query.filter(id == ^user_id)
  |> Ash.read_one!()
  stats
end
```

### Indexing Strategy

**Composite Index**: Index multiple columns often queried together.

```elixir
# For queries filtering by user_id and status
CREATE INDEX posts_user_id_status_idx ON posts(user_id, status)
```

**Partial Index**: Index on prefix for range queries.

```elixir
# For queries filtering by email LIKE 'user%'
CREATE INDEX users_email_prefix_idx ON users(email text_pattern_ops)
```

## Commands to Run

```bash
# Enable query logging
# In config/dev.exs:
config :my_app, MyApp.Repo,
  loggers: [{Ecto.LogEntry, :log, :info}],
  log_sql_queries: true

# Analyze query plans
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

# Check for missing indexes
# In IEx:
Ecto.Adapters.SQL.explain(MyApp.Repo, "EXPLAIN SELECT * FROM users")
```

## Best Practices

### Do

- Always preload associations
- Use selective preloading
- Use aggregates for efficient calculations
- Add indexes on frequently queried columns
- Use pagination for large result sets
- Filter at database level, not in Elixir

### Don't

- Enumerate over associations (N+1 problem)
- Load entire result sets into memory
- Use SELECT * when you only need specific columns
- Ignore query performance warnings
- Skip adding indexes on slow queries

---

## Tools

- **mgrep**: Search for N+1 patterns: `mgrep "N+1 query problems in codebase"`
- **Serena**: Analyze codebase for query optimization opportunities
- **Credo**: Check for code smells in database access code

---

**Use this skill to identify and fix Ecto performance issues.**
