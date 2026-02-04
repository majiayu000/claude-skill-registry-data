---
name: wordpress-site-speed-auditor
description: Performs comprehensive WordPress site speed and performance audits. Use when analyzing WordPress themes, plugins, or sites for performance optimization opportunities, checking image/video optimization, database queries, caching, or identifying speed bottlenecks.
---

# WordPress Site Speed Auditor

This skill provides a comprehensive performance audit framework for WordPress sites, themes, and plugins.

## When to Use This Skill

Invoke this skill when:
- Analyzing a WordPress theme or plugin for performance issues
- User requests a site speed audit or performance review
- Investigating slow page loads or performance complaints
- Optimizing a WordPress site for better Core Web Vitals
- Reviewing code before deployment to catch performance issues

## Audit Checklist

### 1. Image & Media Optimization

**Check for:**
- [ ] **Image formats** - Are modern formats (WebP, AVIF) used? Check for JPEG/PNG that could be converted
- [ ] **Image compression** - Are images optimized/compressed? Look for large file sizes (>100KB for thumbnails, >500KB for full-size)
- [ ] **Lazy loading** - Is `loading="lazy"` attribute present on images below the fold?
- [ ] **Responsive images** - Are `srcset` and `sizes` attributes used for different screen sizes?
- [ ] **Image dimensions** - Are images sized correctly in code or oversized and scaled down with CSS?
- [ ] **Video hosting** - Are videos self-hosted (bad) or externally hosted on YouTube/Vimeo (good)?
- [ ] **Video lazy loading** - Do videos use lazy loading or load on user interaction?
- [ ] **Background images** - Are large background images optimized and served responsively?
- [ ] **Favicon size** - Is favicon appropriately sized (not a 500KB PNG)?
- [ ] **SVG optimization** - Are SVG files minified and cleaned of unnecessary metadata?

**Recommendations:**
- Convert JPEG/PNG to WebP (30% smaller file sizes)
- Use lazy loading for all images below the fold
- Implement responsive images with `srcset`
- Use external video hosting (YouTube, Vimeo) with lazy loading
- Optimize images before upload or use plugins (Smush, ShortPixel, Imagify)

### 2. Database & Query Optimization

**Check for:**
- [ ] **N+1 queries** - Multiple queries in loops (check `WP_Query` inside loops)
- [ ] **Unoptimized queries** - Complex queries without proper indexing
- [ ] **Post revisions** - Excessive post revisions in database
- [ ] **Transients** - Expired transients not cleaned up
- [ ] **Autoloaded data** - Excessive autoloaded options (>1MB is concerning)
- [ ] **Database size** - Bloated database with spam comments, trashed posts
- [ ] **Query caching** - Missing object caching for repeated queries
- [ ] **Direct SQL** - Raw `$wpdb` queries that bypass caching
- [ ] **Meta queries** - Inefficient meta_query usage without indexes
- [ ] **Taxonomies** - Heavy taxonomy queries without caching

**Tools to use:**
- Query Monitor plugin - Identifies slow queries and query counts
- WP-CLI: `wp db optimize` - Optimize database tables
- WP-CLI: `wp transient delete --all` - Clear expired transients
- WP-CLI: `wp post list --post_type=revision --format=count` - Count revisions

**Recommendations:**
- Limit post revisions in wp-config.php: `define('WP_POST_REVISIONS', 3);`
- Clean database regularly (WP-Optimize plugin)
- Implement object caching (Redis, Memcached)
- Add indexes for frequently queried meta keys
- Use transients for expensive query results
- Implement proper query result caching

### 3. Plugin & Theme Performance

**Check for:**
- [ ] **Plugin count** - More than 20-25 active plugins is concerning
- [ ] **Heavy plugins** - Plugins loading excessive resources (use Query Monitor)
- [ ] **Outdated plugins** - Old plugins not updated for modern PHP/WordPress
- [ ] **Plugin conflicts** - Multiple plugins doing similar things
- [ ] **Unused features** - Theme or plugin features loaded but not used
- [ ] **Bloated themes** - Themes with excessive built-in features
- [ ] **Page builders** - Heavy page builders (Elementor, Divi) when not needed
- [ ] **Third-party scripts** - Excessive external scripts (analytics, ads, social)
- [ ] **Font loading** - Multiple font weights/variants loaded unnecessarily
- [ ] **Icon libraries** - Full Font Awesome loaded for 2-3 icons

**Recommendations:**
- Deactivate and remove unused plugins
- Replace heavy plugins with lightweight alternatives
- Use Query Monitor to identify resource-intensive plugins
- Choose lightweight themes (GeneratePress, Astra, Kadence)
- Avoid page builders for simple sites
- Limit font weights and character sets
- Use SVG icons instead of icon fonts

### 4. Caching Implementation

**Check for:**
- [ ] **Page caching** - Is static HTML being generated and served?
- [ ] **Browser caching** - Are proper cache headers set for static assets?
- [ ] **Object caching** - Is persistent object caching (Redis/Memcached) enabled?
- [ ] **Opcode caching** - Is OPcache enabled on the server?
- [ ] **Cache preloading** - Is cache automatically generated for critical pages?
- [ ] **Cache exclusions** - Are dynamic pages (cart, checkout) properly excluded?
- [ ] **CDN integration** - Are static assets served from a CDN?
- [ ] **Cache invalidation** - Does cache clear properly on content updates?

**Recommendations:**
- Install caching plugin (WP Rocket, WP Super Cache, W3 Total Cache)
- Enable page caching for anonymous users
- Implement object caching with Redis or Memcached
- Configure browser caching with far-future expiration headers
- Use CDN (Cloudflare, BunnyCDN, StackPath) for static assets
- Enable cache preloading for better first-visit performance

### 5. Asset Optimization (CSS/JS)

**Check for:**
- [ ] **Render-blocking resources** - CSS/JS blocking initial page render
- [ ] **Unminified assets** - CSS/JS files not minified
- [ ] **Uncombined files** - Multiple small CSS/JS files not combined
- [ ] **Unused CSS** - Large CSS files with unused selectors
- [ ] **Unused JavaScript** - Heavy JS libraries loaded but barely used
- [ ] **Inline critical CSS** - Critical above-the-fold CSS not inlined
- [ ] **Deferred JavaScript** - Non-critical JS not deferred or async
- [ ] **jQuery dependency** - Unnecessary jQuery for simple interactions
- [ ] **Legacy JavaScript** - Old JS not using modern ES6+ features
- [ ] **Source maps** - Source maps loaded in production

**Recommendations:**
- Minify CSS/JS files (Autoptimize, WP Rocket)
- Combine files where appropriate (be careful with HTTP/2)
- Defer non-critical JavaScript with `defer` or `async` attributes
- Inline critical above-the-fold CSS
- Remove unused CSS (PurgeCSS, UnCSS)
- Load JavaScript in footer when possible
- Use vanilla JavaScript instead of jQuery for simple tasks
- Enable GZIP/Brotli compression (reduces files by 70-90%)

### 6. Server & Hosting Configuration

**Check for:**
- [ ] **PHP version** - Using PHP 7.4 or older (should be 8.1+)
- [ ] **Server resources** - Memory limits, max execution time
- [ ] **HTTP/2 or HTTP/3** - Modern HTTP protocol support
- [ ] **GZIP/Brotli compression** - Compression enabled for text assets
- [ ] **Keep-Alive** - Connection persistence enabled
- [ ] **DNS lookup time** - Slow DNS resolution
- [ ] **Server location** - Geographic distance from target audience
- [ ] **Shared hosting** - Resource limitations from shared environment
- [ ] **Server response time** - TTFB (Time To First Byte) over 200ms

**Recommendations:**
- Upgrade to PHP 8.1 or 8.2 (30-50% performance improvement)
- Increase PHP memory limit to at least 256MB
- Ensure HTTP/2 or HTTP/3 is enabled
- Enable GZIP or Brotli compression
- Use quality managed WordPress hosting (WP Engine, Kinsta, Cloudways)
- Consider upgrading from shared to VPS/dedicated hosting
- Use server closer to target audience or implement CDN

### 7. Core Web Vitals & User Experience

**Check for:**
- [ ] **Largest Contentful Paint (LCP)** - Should be under 2.5 seconds
- [ ] **First Input Delay (FID)** - Should be under 100 milliseconds
- [ ] **Cumulative Layout Shift (CLS)** - Should be under 0.1
- [ ] **First Contentful Paint (FCP)** - Should be under 1.8 seconds
- [ ] **Time to Interactive (TTI)** - Should be under 3.8 seconds
- [ ] **Total Blocking Time (TBT)** - Should be under 200 milliseconds
- [ ] **Layout shifts** - Images without dimensions causing shifts
- [ ] **Font loading** - FOUT (Flash of Unstyled Text) or FOIT (Flash of Invisible Text)

**Tools to measure:**
- Google PageSpeed Insights
- GTmetrix
- WebPageTest
- Chrome DevTools Lighthouse
- Core Web Vitals Chrome extension

**Recommendations:**
- Optimize LCP element (usually hero image or heading)
- Add width/height attributes to images to prevent CLS
- Use font-display: swap for web fonts
- Minimize JavaScript execution time for better FID/TBT
- Implement critical CSS for faster FCP
- Preload key resources (fonts, hero images)

### 8. HTTP Requests & Resource Loading

**Check for:**
- [ ] **Total HTTP requests** - More than 50 requests is concerning
- [ ] **Third-party requests** - Excessive external domain requests
- [ ] **Duplicate resources** - Same resource loaded multiple times
- [ ] **Large resources** - Files over 1MB being loaded
- [ ] **Blocking resources** - Resources blocking page render
- [ ] **Preconnect/prefetch** - Missing resource hints for external domains
- [ ] **Lazy loading scripts** - Scripts loading when not needed
- [ ] **Analytics overhead** - Multiple tracking scripts

**Recommendations:**
- Reduce total HTTP requests (combine files, use sprites)
- Minimize third-party script usage
- Use resource hints: `preconnect`, `dns-prefetch`, `preload`
- Defer non-critical resources
- Implement lazy loading for images and iframes
- Consolidate analytics tools (use Google Tag Manager)
- Remove duplicate resources

### 9. WordPress-Specific Optimizations

**Check for:**
- [ ] **Heartbeat API** - Running too frequently
- [ ] **Embeds** - wp-embed.js loading when not needed
- [ ] **Emojis** - Emoji script/styles loading unnecessarily
- [ ] **Dashicons** - Dashicons loading on frontend
- [ ] **REST API** - Excessive REST API calls on frontend
- [ ] **wp-cron** - Heavy scheduled tasks during peak traffic
- [ ] **Gutenberg styles** - Block styles loading when not using blocks
- [ ] **jQuery Migrate** - Old jQuery migrate script still loading

**Recommendations:**
- Disable/limit Heartbeat API frequency
- Remove emoji scripts if not needed
- Dequeue Dashicons on frontend (unless using them)
- Disable embeds if not using WordPress embeds
- Replace wp-cron with real cron jobs
- Remove jQuery Migrate if not needed
- Conditionally load Gutenberg styles only when needed

### 10. Code Quality & Best Practices

**Check for:**
- [ ] **Inline styles** - Excessive inline CSS in HTML
- [ ] **Inline scripts** - JavaScript directly in HTML
- [ ] **External dependencies** - Heavy external libraries for simple tasks
- [ ] **Unoptimized loops** - Expensive operations in loops
- [ ] **File I/O in loops** - File reads/writes in repeated operations
- [ ] **Remote requests** - API calls without caching/timeouts
- [ ] **Error suppression** - Using @ operator hiding performance issues
- [ ] **Debug mode** - WP_DEBUG enabled in production
- [ ] **Disabled caching** - Development constants in production

**Recommendations:**
- Move inline styles to external stylesheets
- Move inline scripts to external files
- Cache expensive operation results
- Avoid file operations in loops
- Cache external API responses with transients
- Remove debug mode and development constants in production
- Use WordPress coding standards and best practices

## Audit Output Format

Provide audit results in this structure:

```
## WordPress Performance Audit Results

### Critical Issues (Fix Immediately)
1. [Issue] - [Impact] - [Recommendation]

### High Priority (Fix Soon)
1. [Issue] - [Impact] - [Recommendation]

### Medium Priority (Optimize When Possible)
1. [Issue] - [Impact] - [Recommendation]

### Low Priority (Nice to Have)
1. [Issue] - [Impact] - [Recommendation]

### Strengths (Already Optimized)
1. [What's working well]

## Estimated Performance Impact
- Current estimated load time: [X] seconds
- After optimizations: [Y] seconds
- Potential improvement: [Z]%

## Implementation Priority
1. [First thing to fix - highest impact/effort ratio]
2. [Second priority]
3. [Third priority]
```

## Key Performance Metrics to Report

Always include these metrics when available:
- Page load time (target: <3 seconds)
- Time to First Byte (target: <200ms)
- Total page size (target: <2MB)
- Number of HTTP requests (target: <50)
- Largest Contentful Paint (target: <2.5s)
- First Input Delay (target: <100ms)
- Cumulative Layout Shift (target: <0.1)

## Tools & Commands Reference

**WP-CLI Commands:**
```bash
wp plugin list --status=active  # List active plugins
wp db optimize                  # Optimize database
wp transient delete --all       # Clear transients
wp cache flush                  # Clear cache
wp option list --autoload=yes   # Check autoloaded options
```

**Query Monitor Checks:**
- Database queries (count and slow queries)
- HTTP API requests
- Hooks & actions
- Scripts & styles
- Languages (translation files)

**Browser DevTools:**
- Network tab - Resource sizes and timing
- Performance tab - Flame charts and bottlenecks
- Lighthouse - Core Web Vitals and performance score
- Coverage tab - Unused CSS/JS

## Remember

- Focus on **high-impact, low-effort** optimizations first
- **Measure before and after** every optimization
- **Test on real devices** with throttled connections
- **Don't over-optimize** - diminishing returns after core issues fixed
- **Mobile performance** is critical for SEO and user experience
- **Core Web Vitals** directly impact Google rankings
