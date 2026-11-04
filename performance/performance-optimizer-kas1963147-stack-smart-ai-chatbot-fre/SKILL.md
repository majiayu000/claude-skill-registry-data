---
name: performance-optimizer
description: WordPress performance optimization and monitoring. Manage caching, optimize database, compress images, and monitor site speed. Essential for fast-loading sites.
tools_required: [perf_cache, perf_transients, perf_db_optimize, perf_query_analysis, perf_assets, perf_images, perf_cron, perf_http, perf_autoload, perf_monitor]
always_on: false
group: admin
order: 3
suggests: [site-maintenance, database-maintenance]
---

# Performance Optimizer

Complete WordPress performance optimization and speed monitoring.

## When to Use This Skill

- Optimizing site loading speed
- Managing object caching
- Optimizing database performance
- Compressing and optimizing images
- Reducing CSS/JS file sizes
- Analyzing slow queries
- Monitoring performance metrics

## Core Capabilities

### Caching
- Object cache management with `perf_cache`
- Enhanced transient handling with `perf_transients`
- Cache warming strategies
- Cache invalidation

### Database Optimization
- Database cleanup with `perf_db_optimize`
- Query analysis with `perf_query_analysis`
- Slow query identification
- Index optimization

### Asset Optimization
- CSS/JS minification with `perf_assets`
- Image compression with `perf_images`
- Lazy loading configuration
- Asset concatenation

### Advanced Optimization
- Cron optimization with `perf_cron`
- HTTP optimization with `perf_http`
- Autoload optimization with `perf_autoload`
- Real-time monitoring with `perf_monitor`

## Performance Audit Workflow

### Initial Assessment

1. **Baseline Metrics**
   - Run performance scan with `perf_monitor`
   - Document current load times
   - Identify bottlenecks

2. **Database Analysis**
   - Analyze query performance with `perf_query_analysis`
   - Identify slow queries
   - Check database size

3. **Asset Analysis**
   - Review CSS/JS sizes
   - Check image optimization status
   - Identify render-blocking resources

### Optimization Steps

1. **Quick Wins**
   - Enable object caching
   - Optimize autoload with `perf_autoload`
   - Clean expired transients

2. **Database Optimization**
   - Remove post revisions (keep last 5)
   - Delete spam/trash comments
   - Optimize database tables
   - Add missing indexes

3. **Asset Optimization**
   - Minify CSS/JS files
   - Compress images
   - Enable lazy loading
   - Defer non-critical JS

4. **Advanced Optimization**
   - Optimize cron schedule
   - Enable HTTP/2 push
   - Configure browser caching
   - Set up CDN (if available)

## Performance Checklist

### Caching
- [ ] Object cache enabled
- [ ] Page cache active
- [ ] Browser caching configured
- [ ] CDN configured (if applicable)

### Database
- [ ] Auto-drafts cleaned
- [ ] Revisions limited
- [ ] Spam comments removed
- [ ] Transients cleaned
- [ ] Tables optimized

### Assets
- [ ] CSS minified
- [ ] JS minified
- [ ] Images compressed
- [ ] Lazy loading enabled
- [ ] Unused CSS removed

### Server
- [ ] GZIP enabled
- [ ] Keep-alive enabled
- [ ] HTTP/2 enabled
- [ ] PHP version current

## Key Metrics to Track

### Speed Metrics
- **TTFB** (Time to First Byte): < 200ms
- **FCP** (First Contentful Paint): < 1.8s
- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1

### Resource Metrics
- Page size: < 3MB
- HTTP requests: < 50
- Image size: Optimized
- CSS size: < 100KB
- JS size: < 300KB

## Common Issues & Fixes

### Slow Database
```
Problem: Queries taking > 1 second
Fix: 
- Add proper indexes
- Optimize autoload options
- Clean old data
```

### Large Images
```
Problem: Images > 200KB each
Fix:
- Compress to WebP
- Resize to max needed dimensions
- Enable lazy loading
```

### Render-Blocking Resources
```
Problem: JS blocking page render
Fix:
- Defer non-critical JS
- Inline critical CSS
- Async load fonts
```

### Too Many HTTP Requests
```
Problem: 100+ requests per page
Fix:
- Combine CSS/JS files
- Use sprite images
- Lazy load below-fold content
```

## Best Practices

1. **Measure before optimizing** - Get baseline metrics
2. **One change at a time** - Isolate impact
3. **Test on mobile** - Most users are mobile
4. **Monitor continuously** - Performance degrades over time
5. **Cache strategically** - Balance freshness vs speed
6. **Optimize images** - Biggest impact for most sites
7. **Regular maintenance** - Weekly/monthly cleanups
