---
name: rails-query-optimization
description: Optimize ActiveRecord queries to prevent N+1 queries and improve performance. Use when experiencing slow queries, optimizing database access, or implementing eager loading strategies.
---

# Rails Query Optimization Specialist

Specialized in optimizing ActiveRecord queries and preventing N+1 problems.

## When to Use This Skill

- Detecting and fixing N+1 query problems
- Implementing eager loading strategies
- Optimizing slow database queries
- Reducing query count in loops
- Improving API response times

## Core Principles

- **Eager Loading**: Load associations upfront
- **Select Only Needed Columns**: Minimize data transfer
- **Batch Processing**: Use `find_each` for large datasets
- **Query Analysis**: Use `explain` to understand queries
- **Avoid N+1**: Preload associations

## Implementation Guidelines

### Preventing N+1 Queries

```ruby
# Bad: N+1 query
users = User.all
users.each do |user|
    puts user.posts.count  # Generates N queries
end

# Good: Eager loading with includes
users = User.includes(:posts)
users.each do |user|
    puts user.posts.count  # Single query
end

# Good: Count associations efficiently
users = User.left_joins(:posts)
           .select('users.*, COUNT(posts.id) as posts_count')
           .group('users.id')
```

### Eager Loading Strategies

```ruby
# includes: Generates separate queries
User.includes(:posts).where(posts: { published: true })

# preload: Forces separate queries (good when no where clause on association)
User.preload(:posts, :comments)

# eager_load: Uses LEFT OUTER JOIN (good with where clause on association)
User.eager_load(:posts).where(posts: { published: true })

# joins: INNER JOIN (when you don't need association data)
User.joins(:posts).where(posts: { published: true })
```

### Nested Associations

```ruby
# Load nested associations
posts = Post.includes(comments: :user)

posts.each do |post|
    post.comments.each do |comment|
        puts comment.user.name  # No additional queries
    end
end
```

### Select Specific Columns

```ruby
# Bad: Loads all columns
User.all

# Good: Load only needed columns
User.select(:id, :name, :email).where(active: true)

# Use pluck for single column values
active_emails = User.where(active: true).pluck(:email)
```

### Batch Processing

```ruby
# Bad: Loads all records into memory
User.all.each do |user|
    process_user(user)
end

# Good: Process in batches
User.find_each(batch_size: 1000) do |user|
    process_user(user)
end

# Good: Manual batching
User.find_in_batches(batch_size: 1000) do |users|
    users.each { |user| process_user(user) }
end
```

### Existence Checks

```ruby
# Bad: Loads all records
User.where(email: email).present?

# Good: Uses EXISTS query
User.where(email: email).exists?

# Bad: Count when you only need existence
if User.count > 0
    # ...
end

# Good: Use any?
if User.any?
    # ...
end
```

### Query Optimization Patterns

```ruby
# Use select with calculations
order_totals = Order.select('user_id, SUM(total) as total_amount')
                   .group(:user_id)

# Use raw SQL for complex queries
User.find_by_sql([
    'SELECT users.*, COUNT(posts.id) as post_count
     FROM users
     LEFT JOIN posts ON posts.user_id = users.id
     WHERE users.active = ?
     GROUP BY users.id',
    true
])

# Use counter cache
class Post < ApplicationRecord
    belongs_to :user, counter_cache: true
end

# Then access with: user.posts_count (no query)
```

## Debugging Tools

```ruby
# Explain query execution plan
User.includes(:posts).where(active: true).explain

# Log queries in development
ActiveRecord::Base.logger = Logger.new(STDOUT)

# Benchmark queries
require 'benchmark'
time = Benchmark.measure do
    User.includes(:posts).to_a
end
puts time
```

## Tools to Use

- `Read`: Read existing query code
- `Edit`: Modify queries for optimization
- `Bash`: Run query analysis and tests
- `mcp__serena__find_symbol`: Find query usage patterns

### Bash Commands

```bash
# Run specs with query logging
QUERY_LOG=true bundle exec rspec

# Check for N+1 queries with Bullet gem
bundle exec rails s

# Rails console for query testing
bundle exec rails console
```

## Workflow

1. **Identify Slow Queries**: Use logs or monitoring tools
2. **Analyze Query Pattern**: Check for N+1 or missing indexes
3. **Write Tests**: Verify optimization works
4. **Apply Eager Loading**: Use includes/preload/eager_load
5. **Select Columns**: Load only needed data
6. **Verify Performance**: Benchmark before/after
7. **Check Explain Plan**: Understand query execution

## Related Skills

- `rails-model-design`: Understanding associations
- `rails-database-indexes`: Adding indexes for queries
- `rails-rspec-testing`: Testing query performance

## Coding Standards

See [Rails Coding Standards](../_shared/rails-coding-standards.md)

## TDD Workflow

Follow [TDD Workflow](../_shared/rails-tdd-workflow.md)

## Key Reminders

- Always use `includes/preload/eager_load` for associations in loops
- Use `pluck` for single column values
- Use `exists?` instead of `present?` for existence checks
- Use `find_each` for processing large datasets
- Select only needed columns
- Analyze queries with `explain`
- Consider counter cache for frequent counts
- Test query performance with benchmarks
