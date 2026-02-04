---
name: performance-analyzer
description: Automatically analyze performance issues when user mentions slow pages, performance problems, or optimization needs. Performs focused performance checks on specific code, queries, or components. Invoke when user says "this is slow", "performance issue", "optimize", or asks about speed.
---

# Performance Analyzer

Automatically analyze and suggest performance improvements for specific code.

## When to Use This Skill

Activate this skill when the user:
- Says "this is slow" or "performance issue"
- Shows code and asks "how can I optimize this?"
- Mentions "page speed", "load time", or "Core Web Vitals"
- Asks "why is this query slow?"
- References "N+1 problem", "caching", or "optimization"
- Shows performance profiler output

## Quick Analysis Types

### 1. Database Query Analysis

**What to check:**
- N+1 queries
- Missing indexes
- SELECT * instead of specific fields
- Unnecessary JOINs
- Large result sets without pagination

**Example Response:**
```markdown
## Query Performance Issue: N+1 Problem

**Current Code:**
```php
$users = User::loadMultiple();
foreach ($users as $user) {
  $profile = $user->get('field_profile')->entity; // N+1!
}
```

**Problem**: Loading 100 users triggers 101 queries (1 + 100)

**Solution**: Use EntityQuery with eager loading
```php
$query = \Drupal::entityQuery('user')
  ->accessCheck(TRUE);
$uids = $query->execute();
$users = User::loadMultiple($uids);

// Preload profiles in one query
$profile_ids = [];
foreach ($users as $user) {
  $profile_ids[] = $user->get('field_profile')->target_id;
}
$profiles = Profile::loadMultiple($profile_ids);
```

**Impact**: Reduces queries from 101 to 2 (~98% improvement)
```

### 2. Asset Optimization

**What to check:**
- Large unoptimized images
- Unminified CSS/JS
- Blocking resources
- Missing lazy loading
- No CDN usage

### 3. Caching Analysis

**What to check:**
- Missing cache tags
- Cache invalidation issues
- No page cache
- Expensive uncached operations

### 4. Core Web Vitals

**Quick checks:**
- **LCP** (Largest Contentful Paint): Target < 2.5s
- **INP** (Interaction to Next Paint): Target < 200ms
- **CLS** (Cumulative Layout Shift): Target < 0.1

## Response Format

```markdown
## Performance Analysis

**Component**: [What was analyzed]
**Issue**: [Performance problem]
**Impact**: [How it affects users]

### Current Performance
- Metric: [value]
- Grade: [A-F]

### Optimization Recommendations

1. **[Recommendation]** (Priority: High)
   - Current: [problem]
   - Improved: [solution]
   - Expected gain: [percentage/time]

2. **[Next recommendation]**
   ...

### Code Example
[Provide optimized code]
```

## Common Performance Patterns

### Drupal

**Problem**: Lazy loading causing N+1
```php
// Bad
foreach ($nodes as $node) {
  $author = $node->getOwner()->getDisplayName(); // N+1
}

// Good
$nodes = \Drupal::entityTypeManager()
  ->getStorage('node')
  ->loadMultiple($nids);
User::loadMultiple(array_column($nodes, 'uid')); // Preload
```

### WordPress

**Problem**: Inefficient WP_Query
```php
// Bad
$posts = new WP_Query(['posts_per_page' => -1]); // Loads everything

// Good
$posts = new WP_Query([
  'posts_per_page' => 20,
  'fields' => 'ids', // Only IDs
  'no_found_rows' => true, // Skip counting
  'update_post_meta_cache' => false,
  'update_post_term_cache' => false,
]);
```

## Integration with /audit-perf Command

- **This Skill**: Focused code-level analysis
  - "This query is slow"
  - "Optimize this function"
  - Single component performance

- **`/audit-perf` Command**: Comprehensive site audit
  - Full performance analysis
  - Core Web Vitals testing
  - Lighthouse reports

## Quick Tips

💡 **Database**: Index foreign keys, avoid SELECT *
💡 **Caching**: Cache expensive operations, use cache tags
💡 **Assets**: Optimize images, minify CSS/JS, lazy load
💡 **Queries**: Limit results, use eager loading, avoid N+1
