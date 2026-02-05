---
name: performance-auditing
description: Guide for analyzing and improving application performance including identifying bottlenecks, implementing caching, and optimizing queries. This skill should be used when reviewing performance issues or optimizing code.
---

# Performance Audit Skill

This skill provides elite performance engineering expertise for making applications lightning-fast through systematic optimization.

## When to Use This Skill

Invoke this skill when:
- Analyzing slow page loads or response times
- Identifying performance bottlenecks in code execution
- Designing and implementing caching strategies
- Optimizing database queries and preventing N+1 problems
- Reducing memory consumption or investigating memory leaks
- Improving asset delivery (compression, minification, bundling)
- Implementing lazy loading or code splitting
- Profiling and benchmarking code performance
- Reviewing new features for performance implications
- Establishing performance budgets for critical user journeys

## Core Performance Expertise

### 1. Performance Analysis Methodology

To analyze performance issues effectively:

**Measure First**: Always establish baseline metrics before optimization. Use profiling tools, timing measurements, and performance monitoring to identify actual bottlenecks rather than assumed ones.

**Prioritize Impact**: Focus on optimizations that provide the greatest performance improvement relative to implementation effort. Target the critical path and high-traffic code paths first.

**Consider Trade-offs**: Evaluate each optimization for its impact on code maintainability, complexity, and resource usage. Sometimes a 10% performance gain isn't worth a 50% increase in code complexity.

**Validate Improvements**: After implementing optimizations, measure again to confirm actual performance gains. Be prepared to roll back changes that don't deliver meaningful improvements.

### 2. Caching Strategies

To implement effective caching:

- Choose the appropriate caching layer (browser cache, CDN, application cache, database query cache, computed result cache)
- Implement proper cache invalidation strategies to prevent stale data issues
- Use cache keys that are specific enough to avoid collisions but general enough to maximize hit rates
- Set appropriate TTLs based on data volatility and business requirements
- Implement cache warming for predictable high-traffic scenarios
- Use cache-aside, write-through, or write-behind patterns as appropriate
- Monitor cache hit rates and adjust strategies based on real usage patterns

**Key Rules:**
- Never cache without considering invalidation strategy
- Always measure cache hit rates to validate effectiveness
- Balance cache complexity against actual performance benefits

### 3. Frontend Performance Optimization

To optimize frontend performance, focus on:

**Critical Rendering Path:**
- Minimize render-blocking resources (CSS, JavaScript)
- Prioritize above-the-fold content loading
- Use resource hints (preload, prefetch, preconnect)

**Asset Optimization:**
- Compress and minify JavaScript and CSS
- Optimize images (format, compression, responsive sizes)
- Implement lazy loading for images and off-screen content
- Use code splitting to reduce initial bundle size

**Runtime Performance:**
- Debounce and throttle user interaction handlers
- Use virtual scrolling for large lists
- Offload CPU-intensive tasks to Web Workers
- Implement efficient React re-render patterns (memoization, useMemo, useCallback)

**Key Rules:**
- Always measure with real-world conditions (throttled network, low-end devices)
- Focus on First Contentful Paint (FCP) and Time to Interactive (TTI)
- Avoid premature optimization of rarely-executed code

### 4. Backend Performance Optimization

To optimize backend performance, address:

**Database Performance:**
- Add indexes on frequently queried columns
- Prevent N+1 query problems with eager loading
- Use query explain plans to identify slow operations
- Implement connection pooling for database connections
- Consider read replicas for high-traffic read operations

**Request Processing:**
- Implement pagination and filtering for large datasets
- Use asynchronous processing for long-running tasks
- Batch similar operations to reduce overhead
- Implement request/response compression

**Resource Management:**
- Use connection pooling for external services
- Implement circuit breakers for failing dependencies
- Set appropriate timeouts to prevent resource exhaustion

**Key Rules:**
- Database queries should use indexes, not full table scans
- Long-running operations belong in background jobs, not HTTP requests
- Always implement pagination for unbounded result sets

### 5. Infrastructure Performance

To optimize infrastructure performance:

- Configure CDN caching for static assets
- Implement load balancing for horizontal scaling
- Use appropriate database indexing and sharding strategies
- Enable compression (gzip, brotli) for text-based responses
- Optimize container resource allocation

**Key Rules:**
- CDN cache misses should be minimized through proper cache headers
- Horizontal scaling requires stateless application design
- Monitor resource utilization to right-size infrastructure

## Report Output Format

**IMPORTANT**: The section below defines the COMPLETE report structure that MUST be used. Do NOT create your own format or simplified version.

### Location and Naming
- **Directory**: `/docs/performance/`
- **Filename**: `YYYY-MM-DD-HHMMSS-performance-audit.md`
- **Example**: `2025-10-29-143022-performance-audit.md`

### Report Template

**🚨 CRITICAL INSTRUCTION - READ CAREFULLY 🚨**

You MUST use this exact template structure for ALL performance audit reports. This is MANDATORY and NON-NEGOTIABLE.

**REQUIREMENTS:**
1. ✅ Use the COMPLETE template structure below - ALL sections are REQUIRED
2. ✅ Follow the EXACT heading hierarchy (##, ###, ####)
3. ✅ Include ALL section headings as written in the template
4. ✅ Use the finding numbering format: P-001, P-002, etc.
5. ✅ Include the tables, code examples, and checklists as shown
6. ❌ DO NOT create your own format or structure
7. ❌ DO NOT skip or combine sections
8. ❌ DO NOT create abbreviated or simplified versions
9. ❌ DO NOT number issues as "1, 2, 3" - use P-001, P-002, P-003 format

**If you do not follow this template exactly, the report will be rejected.**

<template>
## Executive Summary

### Audit Overview

- **Target System**: [Application Name/System]
- **Analysis Date**: [Date Range]
- **Analysis Scope**: [Web Application/API/Database/Full Stack]
- **Technology Stack**: [e.g., .NET 8, Umbraco CMS, SQL Server, Elasticsearch, Azure]

### Performance Assessment Summary

| Performance Level | Count | Percentage |
|-------------------|-------|------------|
| Critical Issues   | X     | X%         |
| High Impact       | X     | X%         |
| Medium Impact     | X     | X%         |
| Low Impact        | X     | X%         |
| **Total**         | **X** | **100%**   |

### Key Analysis Results

- **Performance Anti-Patterns**: X critical patterns identified requiring immediate attention
- **Code Optimization Opportunities**: X high-impact optimizations discovered
- **Architecture Assessment**: X/10 performance best practices implemented
- **Overall Code Performance Score**: X/100 (based on static analysis and architectural patterns)

---

## Analysis Methodology

### Performance Analysis Approach

- **Static Code Analysis**: Comprehensive source code review for performance anti-patterns
- **Database Query Analysis**: Review of SQL queries, indexing strategies, and data access patterns
- **Resource Utilization Assessment**: Analysis of memory, CPU, and I/O usage patterns
- **Architecture Performance Review**: Examination of caching, scaling, and optimization strategies

### Analysis Coverage

- **Files Analyzed**: X source files across Y projects
- **Database Queries Reviewed**: X queries and stored procedures
- **API Endpoints Tested**: X endpoints across Y controllers
- **Performance Patterns Checked**: N+1 queries, memory leaks, CPU bottlenecks, I/O blocking

### Analysis Capabilities

- **Pattern Detection**: N+1 queries, inefficient loops, memory leaks, blocking operations
- **Database Analysis**: Missing indexes, expensive queries, deadlock potential
- **Resource Analysis**: Memory allocation patterns, CPU-intensive operations, I/O bottlenecks
- **Architecture Assessment**: Caching strategies, async/await patterns, connection pooling

---

## Performance Findings

### Critical Performance Issues

#### P-001: N+1 Query Problem

**Location**: `src/Website.Core/Services/VendorService.cs:78`
**Performance Impact**: 9.8 (Critical)
**Pattern Detected**: Loading related entities in a loop causing multiple database queries
**Code Context**:

```csharp
foreach (var vendor in vendors)
{
    vendor.Products = context.Products.Where(p => p.VendorId == vendor.Id).ToList();
}
```

**Impact**: Database query count increases linearly with result set size (1 + N queries instead of 1)
**Performance Cost**: 2000ms+ response time for 100 vendors
**Recommendation**: Use Include() for eager loading or projection for specific fields
**Fix Priority**: Immediate (within 24 hours)

#### P-002: Synchronous Database Operations

**Location**: `src/Website.Web/Controllers/ApiController.cs:45`
**Performance Impact**: 9.1 (Critical)
**Pattern Detected**: Synchronous database calls blocking request threads
**Code Context**: Missing async/await pattern in controller actions
**Impact**: Thread pool exhaustion under high load, poor scalability
**Performance Cost**: Thread starvation affecting overall application responsiveness
**Recommendation**: Convert all database operations to async/await pattern
**Fix Priority**: Immediate (within 48 hours)

### High Performance Impact Findings

#### P-003: Large Object Heap Pressure

**Location**: Multiple locations in data processing services
**Performance Impact**: 7.8 (High)
**Pattern Detected**: Large objects (>85KB) causing frequent Gen 2 garbage collection
**Affected Components**:

- `src/Website.AirtableData/Services/ImportService.cs:156`
- `src/Website.ElasticSearch/Services/IndexingService.cs:89`
**Impact**: GC pressure causing application pauses and increased memory usage
**Performance Cost**: 200-500ms GC pauses, 40% higher memory usage
**Recommendation**: Implement streaming for large data sets, use object pooling
**Fix Priority**: Within 1 week

#### P-004: Inefficient Elasticsearch Queries

**Location**: `src/Website.ElasticSearch/Services/SearchService.cs:123`
**Performance Impact**: 7.5 (High)
**Pattern Detected**: Full-text search without field targeting or filtering
**Code Context**: Broad queries without proper field restrictions or caching
**Impact**: High Elasticsearch cluster load, slow search response times
**Performance Cost**: 800ms+ search response time, high CPU usage on ES cluster
**Recommendation**: Implement targeted field searches, result caching, and query optimization
**Fix Priority**: Within 2 weeks

### Medium Performance Impact Findings

#### P-005: Missing Database Indexes

**Location**: Database schema analysis
**Performance Impact**: 6.3 (Medium)
**Pattern Detected**: Frequent WHERE clauses on non-indexed columns
**Affected Tables**:

- `Vendors` table: missing index on `OrganizationId, IsActive`
- `Products` table: missing composite index on `CategoryId, Status, CreatedDate`
**Impact**: Table scans causing slow query performance
**Performance Cost**: 500-1200ms query response time for filtered data
**Recommendation**: Add appropriate indexes based on query patterns
**Fix Priority**: Within 1 month

#### P-006: Inefficient LINQ Queries

**Location**: Multiple service classes
**Performance Impact**: 5.9 (Medium)
**Pattern Detected**: Multiple enumeration of IEnumerable, inefficient projections
**Affected Areas**: Vendor listing, product filtering, category navigation
**Impact**: Unnecessary CPU cycles, increased memory allocation
**Performance Cost**: 200-400ms additional processing time
**Recommendation**: Use ToList() strategically, optimize LINQ expressions
**Fix Priority**: Within 1 month

### Low Performance Impact Findings

#### P-007: Missing Output Caching

**Location**: Web application controllers and views
**Performance Impact**: 3.8 (Low)
**Pattern Detected**: Repeated computation of static or semi-static content
**Missing Caching**: Category lists, navigation menus, vendor counts
**Impact**: Unnecessary CPU usage for frequently accessed data
**Performance Cost**: 50-100ms additional processing per request
**Recommendation**: Implement response caching and memory caching strategies
**Fix Priority**: Within 2 months

---

## Code Pattern Performance Analysis

### Performance Anti-Pattern Detection

- **N+1 Query Patterns**: X instances detected across Y service classes
- **Synchronous Blocking Operations**: X async-convertible operations identified
- **Large Object Allocations**: X locations with >85KB object creation
- **Inefficient LINQ Usage**: X queries with multiple enumeration or suboptimal patterns

### Database Access Pattern Analysis

- **Entity Framework Usage**: X queries analyzed for efficiency patterns
- **Missing Async Patterns**: X database operations identified for async conversion
- **Query Complexity**: X complex queries requiring optimization review
- **Connection Management**: Connection pooling configuration assessment

### Resource Management Pattern Analysis

- **Memory Allocation Patterns**: Large object heap pressure points identified
- **Garbage Collection Pressure**: X locations with excessive object creation
- **Thread Pool Usage**: X blocking operations affecting scalability
- **Caching Opportunities**: X frequently computed operations without caching

---

## Architecture Performance Assessment

### Data Access Layer Analysis

- **Entity Framework Performance**: ⚠️ N+1 queries detected, lazy loading causing issues
- **Connection Pooling**: ✅ Properly configured with appropriate pool sizes
- **Query Optimization**: ❌ Missing indexes and inefficient LINQ expressions
- **Caching Strategy**: ❌ Insufficient caching at data layer

### Application Layer Analysis

- **Async/Await Usage**: ❌ Many synchronous operations blocking threads
- **Memory Management**: ⚠️ Some memory leaks in background services
- **CPU Utilization**: ⚠️ CPU-intensive operations not optimized
- **I/O Operations**: ❌ File operations and API calls not properly optimized

### Infrastructure Analysis

- **Load Balancing**: ✅ Properly configured with health checks
- **CDN Usage**: ⚠️ Static assets cached but optimization needed
- **Database Scaling**: ⚠️ Read replicas available but not fully utilized
- **Monitoring Coverage**: ❌ Limited application performance monitoring

---

## Performance Bottleneck Analysis

### Top 10 Performance Bottlenecks

| Rank | Component | Issue | Impact Score | Response Time Impact |
|------|-----------|-------|--------------|---------------------|
| 1 | VendorService | N+1 Query Problem | 9.8 | +2000ms |
| 2 | ApiController | Sync DB Operations | 9.1 | Thread exhaustion |
| 3 | ImportService | Large Object Heap | 7.8 | +500ms GC pauses |
| 4 | SearchService | Inefficient ES Queries | 7.5 | +800ms |
| 5 | Database | Missing Indexes | 6.3 | +600ms |
| 6 | LINQ Queries | Multiple Enumeration | 5.9 | +300ms |
| 7 | File Operations | Synchronous I/O | 5.2 | +400ms |
| 8 | Caching | Missing Cache Strategy | 4.8 | +200ms |
| 9 | Background Jobs | Memory Leaks | 4.5 | Resource exhaustion |
| 10 | API Serialization | Large Payloads | 3.9 | +150ms |

---

## Technical Recommendations

### Immediate Performance Fixes

1. **Fix N+1 query problems** using Include() or projection in Entity Framework
2. **Convert synchronous operations** to async/await pattern for scalability
3. **Add missing database indexes** for frequently queried columns
4. **Implement connection pooling** for external service calls

### Performance Enhancements

1. **Implement comprehensive caching strategy** using Redis or in-memory caching
2. **Optimize Elasticsearch queries** with proper field targeting and filtering
3. **Add response compression** for API endpoints and static content
4. **Implement lazy loading** for heavy components and data

### Architecture Improvements

1. **Add application performance monitoring** using Application Insights or similar
2. **Implement database read replicas** for read-heavy operations
3. **Add background job optimization** with proper queue management
4. **Implement API rate limiting** and request throttling

---

## Code Optimization Examples

### N+1 Query Fix

**Before (Inefficient)**:

```csharp
var vendors = context.Vendors.ToList();
foreach (var vendor in vendors)
{
    vendor.Products = context.Products.Where(p => p.VendorId == vendor.Id).ToList();
}
```

**After (Optimized)**:

```csharp
var vendors = context.Vendors
    .Include(v => v.Products)
    .ToList();
// OR for specific fields only
var vendorsWithProductCount = context.Vendors
    .Select(v => new VendorViewModel
    {
        Id = v.Id,
        Name = v.Name,
        ProductCount = v.Products.Count()
    })
    .ToList();
```

### Async/Await Implementation

**Before (Blocking)**:

```csharp
[HttpGet]
public IActionResult GetVendors()
{
    var vendors = vendorService.GetAll(); // Synchronous call
    return Ok(vendors);
}
```

**After (Non-blocking)**:

```csharp
[HttpGet]
public async Task<IActionResult> GetVendors()
{
    var vendors = await vendorService.GetAllAsync(); // Asynchronous call
    return Ok(vendors);
}
```

### Caching Implementation

**Before (No Caching)**:

```csharp
public List<Category> GetCategories()
{
    return context.Categories.OrderBy(c => c.Name).ToList();
}
```

**After (With Caching)**:

```csharp
public async Task<List<Category>> GetCategoriesAsync()
{
    const string cacheKey = "categories_all";
    var cached = await cache.GetAsync<List<Category>>(cacheKey);
    if (cached != null)
        return cached;

    var categories = await context.Categories
        .OrderBy(c => c.Name)
        .ToListAsync();

    await cache.SetAsync(cacheKey, categories, TimeSpan.FromMinutes(30));
    return categories;
}
```

---

## Performance Optimization Priorities

### Phase 1: Critical Performance Fixes

- [ ] Fix N+1 queries in `VendorService.cs:78`
- [ ] Convert synchronous database operations to async in `ApiController.cs:45`
- [ ] Add missing database indexes for Vendors and Products tables
- [ ] Implement connection pooling for Elasticsearch service

### Phase 2: High Impact Optimizations

- [ ] Optimize large object allocations in import services
- [ ] Implement caching strategy for frequently accessed data
- [ ] Optimize Elasticsearch queries with proper filtering
- [ ] Fix memory leaks in background job processing

### Phase 3: Medium Impact Improvements

- [ ] Optimize LINQ queries to avoid multiple enumeration
- [ ] Implement response compression and output caching
- [ ] Add database read replicas for read operations
- [ ] Optimize file I/O operations with async patterns

### Phase 4: Performance Monitoring and Fine-tuning

- [ ] Implement comprehensive APM solution
- [ ] Add custom performance counters and metrics
- [ ] Set up automated performance testing
- [ ] Document performance best practices

---

## Estimated Performance Improvement Impact

### Performance Gains by Priority

| Priority Level | Expected Improvement | Implementation Complexity |
|----------------|---------------------|--------------------------|
| Critical Fixes | 60-80% response time improvement | High - requires careful testing |
| High Impact | 30-50% overall performance gain | Medium - architectural changes |
| Medium Impact | 15-25% additional optimization | Medium - code and config changes |
| Low Impact | 5-10% fine-tuning benefits | Low - mostly configuration |

### Resource Utilization Improvements

- **Database Load**: Expected 40-60% reduction in query execution time
- **Memory Usage**: Expected 25-35% reduction in memory pressure
- **CPU Utilization**: Expected 20-30% reduction in CPU usage
- **Thread Pool**: Expected elimination of thread starvation issues

---

## Performance Monitoring Setup Recommendations

### Monitoring Infrastructure Setup

- **Application Performance Monitoring**: Azure Application Insights or New Relic integration
- **Database Monitoring**: SQL Server Extended Events and Performance Dashboard configuration
- **Infrastructure Monitoring**: Azure Monitor or Prometheus + Grafana setup
- **Code-Level Monitoring**: Custom performance counters for identified bottlenecks

### Recommended Performance Tracking

- **Database Query Monitoring**: Track queries identified in this analysis for execution time
- **Memory Allocation Tracking**: Monitor large object heap allocations in flagged components
- **Thread Pool Monitoring**: Track thread starvation in areas with synchronous operations
- **Cache Hit Rate Monitoring**: Measure effectiveness of recommended caching implementations

### Performance Testing Recommendations

- **Load Testing**: Focus on endpoints with identified N+1 query problems
- **Database Performance Testing**: Test queries with missing indexes under load
- **Memory Pressure Testing**: Validate large object allocation fixes
- **Concurrency Testing**: Verify async/await implementations under concurrent load

---

## Summary

This performance analysis identified **X critical**, **Y high**, **Z medium**, and **W low** performance issues across the application stack. The analysis focused on code patterns, database queries, resource utilization, and architectural performance without requiring extensive load testing infrastructure.

**Key Strengths Identified**:

- Good modular architecture with clear separation of concerns
- Proper use of modern .NET 8 features and Umbraco CMS
- Well-structured database schema with appropriate relationships

**Critical Areas Requiring Immediate Attention**:

- N+1 query problems causing database performance issues
- Synchronous operations blocking thread pool resources
- Missing database indexes for frequently queried data
- Inefficient memory allocation patterns in data processing

**Expected Overall Performance Improvement**: 70-90% reduction in response times and 40-60% improvement in resource utilization after implementing all recommendations.
</template>

## Examples

**Example 1: N+1 Query Problem**

Bad approach:
```javascript
const orders = await Order.findAll();
for (const order of orders) {
  order.customer = await Customer.findByPk(order.customerId);
  order.items = await OrderItem.findAll({ where: { orderId: order.id } });
}
```

Good approach:
```javascript
const orders = await Order.findAll({
  include: [
    { model: Customer },
    { model: OrderItem }
  ]
});
```

**Example 2: Inefficient Caching**

Bad approach:
```javascript
// Cache entire dataset, never invalidate
const cache = await getCachedData('all-products');
if (cache) return cache;
const products = await Product.findAll();
await setCachedData('all-products', products, 86400); // 24 hours
```

Good approach:
```javascript
// Cache with granular keys and appropriate TTL
const cacheKey = `products:page:${page}:filter:${filter}`;
const cache = await getCachedData(cacheKey);
if (cache) return cache;

const products = await Product.findAll({ where: filter, limit: 20, offset: page * 20 });
await setCachedData(cacheKey, products, 300); // 5 minutes

// Invalidate on product updates
await invalidateCachePattern('products:*');
```

**Example 3: Unoptimized Asset Loading**

Bad approach:
```html
<!-- Loading full-size images for all screen sizes -->
<img src="/images/hero-4k.jpg" alt="Hero image">
```

Good approach:
```html
<!-- Responsive images with lazy loading -->
<img
  srcset="
    /images/hero-mobile.jpg 640w,
    /images/hero-tablet.jpg 1024w,
    /images/hero-desktop.jpg 1920w
  "
  sizes="(max-width: 640px) 640px, (max-width: 1024px) 1024px, 1920px"
  src="/images/hero-desktop.jpg"
  alt="Hero image"
  loading="lazy"
>
```

## Best Practices

1. **Measure Before and After**: Never optimize without establishing baseline metrics. Use profiling tools to identify actual bottlenecks, then validate improvements with measurements.

2. **Optimize the Critical Path**: Focus on the most-used features and flows first. A 50% improvement on a feature used by 80% of users has more impact than a 90% improvement on a rarely-used feature.

3. **Consider Total Cost**: Evaluate optimizations holistically - faster code that uses 10x more memory or is 5x harder to maintain may not be a good trade-off.

4. **Use Appropriate Tools**: Leverage browser dev tools, database query analyzers, profilers, and APM tools to identify bottlenecks scientifically rather than guessing.

5. **Implement Progressive Enhancement**: Optimize for the common case while gracefully handling edge cases. Don't sacrifice reliability for speed.

6. **Monitor in Production**: Performance in development often differs from production. Implement real user monitoring (RUM) to track actual user experience.

7. **Set Performance Budgets**: Establish and enforce performance budgets for page weight, load time, and critical metrics. Prevent performance regression through automated checks.

8. **Document Trade-offs**: When implementing complex optimizations, document the reasoning, expected benefits, and any maintenance considerations for future developers.

## Quality Assurance Checklist

Before recommending any optimization, verify:

- ✓ Have baseline metrics been established?
- ✓ Does the optimization address a real bottleneck, not premature optimization?
- ✓ Will the solution work under production load conditions?
- ✓ Have potential bugs or edge cases been considered?
- ✓ Is the impact on code readability and maintainability acceptable?
- ✓ Can the improvement be validated through testing?
- ✓ Are monitoring metrics defined to track ongoing effectiveness?

## Common Performance Anti-Patterns

Proactively identify these common issues:

### Database Anti-Patterns
- N+1 queries (missing eager loading)
- Missing indexes on filtered/joined columns
- Using `SELECT *` instead of specific columns
- Fetching all records without pagination
- Executing queries in loops

### Frontend Anti-Patterns
- Loading all JavaScript upfront (no code splitting)
- Large, unoptimized images
- Synchronous, render-blocking scripts
- Excessive re-renders in React (missing memoization)
- Memory leaks from uncleared intervals/listeners

### Caching Anti-Patterns
- Caching without invalidation strategy
- Cache keys too granular (low hit rate)
- Cache keys too broad (stale data)
- No cache monitoring
- Caching entire large datasets

### API Anti-Patterns
- No rate limiting
- Returning excessive data (no field filtering)
- Missing pagination
- Synchronous processing of async operations
- No response compression

## Performance Testing Strategies

To validate performance improvements:

1. **Load Testing**: Simulate concurrent users to identify breaking points
2. **Profiling**: Use CPU and memory profilers to identify hotspots
3. **Benchmarking**: Create reproducible performance tests for critical paths
4. **Real User Monitoring**: Track actual user experience in production
5. **Synthetic Monitoring**: Automated performance tests from various locations

## Context-Aware Analysis

When project-specific context is available in CLAUDE.md files, incorporate:

- **Technology Stack**: Identify framework-specific optimization opportunities
- **Usage Patterns**: Optimize for actual traffic patterns and user behavior
- **Infrastructure**: Consider deployment architecture and resource constraints
- **Performance Requirements**: Align optimizations with business SLAs and budgets

## Communication Guidelines

When reporting performance findings:
- Lead with measured impact (seconds, requests, bytes)
- Provide concrete code examples showing before/after
- Explain the "why" behind optimizations, not just the "what"
- Set realistic expectations for performance improvements
- Acknowledge when existing code is already well-optimized
- Recommend incremental improvements over risky rewrites

Remember: The goal is to make applications measurably faster while maintaining code quality and reliability. Combine deep technical knowledge with practical engineering judgment to deliver optimizations that matter.
