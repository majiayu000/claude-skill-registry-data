---
name: Continuous Learning
description: This skill activates when users want to extract patterns from sessions, save learnings to Serena memory, or improve the copilot based on past experiences. Automatically runs as Stop hook to capture patterns after each session.
---

# Continuous Learning

Extract reusable patterns from sessions and save to Serena memory for future reference.

## When This Activates

- `/wordpress-copilot:learn` command
- Stop hook (automatic at session end)
- User asks to "save this pattern" or "remember this"
- After solving unique problems
- Discovering new WordPress patterns

---

## What Gets Extracted

### 1. Error Resolution Patterns

**Example**: CSP blocking 3D CDNs

```markdown
# WordPress.com CSP Blocking External CDNs

**Problem**: Platform-level CSP headers block cdn.babylonjs.com

**Root Cause**: WordPress.com injects CSP at Nginx layer (before PHP)

**Attempted Fixes**:
1. wpcom_csp_allowed_sources filter ❌
2. header() override in theme ❌
3. custom-redirects.php ❌
4. CSP Manager plugin ❌

**Solution**: Self-hosted WordPress for full CSP control

**When to Use**: Any WordPress.com site requiring custom external CDNs
```

### 2. Framework Workarounds

**Example**: Elementor 3D widget integration

```markdown
# Elementor Widget with Three.js

**Context**: Custom Elementor widget loading Three.js scene

**Challenge**: Elementor's rendering lifecycle conflicts with Three.js initialization

**Solution**: Use requestAnimationFrame after Elementor ready event

```php
elementorFrontend.hooks.addAction('frontend/element_ready/widget', function($scope) {
    requestAnimationFrame(() => {
        initThreeJS($scope.find('.canvas')[0]);
    });
});
```

**When to Use**: Any Elementor widget with complex JavaScript initialization
```

### 3. Performance Optimizations

**Example**: WooCommerce query optimization

```markdown
# Optimize WooCommerce Product Queries

**Problem**: Loading 100 products took 3.2s

**Solution**: Only fetch IDs, then selectively load data

```php
// Before: 3.2s
$products = wc_get_products(['limit' => 100]);

// After: 0.8s
$ids = wc_get_products(['limit' => 100, 'return' => 'ids']);
```

**Impact**: 75% faster (3.2s → 0.8s)

**When to Use**: Any large WooCommerce product queries
```

### 4. Debugging Techniques

**Example**: Tracing WordPress.com CSP source

```markdown
# Diagnose Platform-Level Header Injection

**Problem**: Can't determine where CSP header originates

**Technique**: Multi-layer diagnostic logging

```bash
# Layer 1: Check headers in response
curl -sI https://site.com/ | grep -i content-security

# Layer 2: Test if headers_list() sees it
<?php var_dump(headers_list()); ?>

# Layer 3: Test custom-redirects.php execution order
<?php error_log('custom-redirects executed'); ?>
```

**Conclusion**: If headers_list() doesn't see it, injected at server level

**When to Use**: Diagnosing any unexplained HTTP headers
```

### 5. Project-Specific Conventions

**Example**: SkyyRose branding patterns

```markdown
# SkyyRose Brand Application

**Primary Color**: #B76E79 (rose gold)
**Tagline**: "Where Love Meets Luxury"
**Typography**: Archivo (headings), Hanken Grotesk (body), Inter (system fallback)

**CSS Convention**:
```css
:root {
    --skyy-primary: #B76E79;
    --skyy-transition: cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
```

**Meta Conventions**:
- Collection: _skyyrose_collection (signature, black_rose, love_hurts)
- Featured: _featured (yes/no)

**When to Use**: All SkyyRose theme/plugin development
```

---

## How It Works

### Automatic Extraction (Stop Hook)

```json
// hooks/hooks.json includes Stop hook
{
  "Stop": [{
    "matcher": "*",
    "hooks": [{
      "type": "prompt",
      "blocking": false,
      "prompt": "Review this session for patterns to extract..."
    }]
  }]
}
```

### Manual Extraction (/learn Command)

```markdown
User: "/wordpress-copilot:learn"

Copilot:
1. Reviews recent conversation
2. Identifies patterns worth saving
3. Formats as markdown skill/reference
4. Saves to Serena memory
5. Reports what was learned
```

---

## Pattern Quality Criteria

Only save patterns that are:

1. **Reusable**: Applies to multiple scenarios
2. **Non-obvious**: Not in standard docs
3. **Tested**: Proven to work
4. **Specific**: Concrete code/steps, not theory
5. **Contextual**: Clear when to use

---

## Serena Memory Structure

```
~/.serena/memories/
├── wordpress-patterns/
│   ├── csp-workarounds.md
│   ├── elementor-widget-lifecycle.md
│   └── woocommerce-query-optimization.md
├── debugging-techniques/
│   ├── platform-header-diagnosis.md
│   └── wordpress-com-api-debugging.md
└── skyyrose-conventions/
    ├── branding-standards.md
    ├── collection-metadata.md
    └── 3d-integration-patterns.md
```

---

## Example: Full Pattern Extraction

**Session Context**: User struggled with WordPress.com CSP blocking, tried 5 fixes, discovered platform limitation

**Extracted Pattern**:

```markdown
# WordPress.com Platform CSP Limitation

## Context
WordPress.com Business plan site requiring custom CDNs (cdn.babylonjs.com for 3D viewer)

## Problem
Platform injects Content-Security-Policy headers at Nginx reverse proxy layer.
Theme code cannot override these headers.

## Evidence
```bash
# 1. Curl shows platform CSP
curl -sI https://skyyrose.co/ | grep content-security-policy

# 2. headers_list() in PHP doesn't see it
<?php var_dump(headers_list()); // CSP not in array

# 3. Custom headers get overridden
header('Content-Security-Policy: ...'); // Ignored by platform
```

## Failed Approaches (All 5)
1. **wpcom_csp_allowed_sources filter**: Filter doesn't exist or doesn't apply
2. **header() in theme**: Overridden by platform
3. **Nonce extraction**: Can't extract platform nonce
4. **custom-redirects.php**: Also overridden
5. **CSP Manager plugin**: Uses PHP hooks, same limitation

## Root Cause
Nginx layer injection happens AFTER PHP execution completes.
No PHP code can modify infrastructure-level headers.

## Solutions

### Option A: File Support Ticket (Uncertain)
Request WordPress.com platform team whitelist specific domains.
Success not guaranteed.

### Option B: Migrate to Self-Hosted (Definitive)
- Export site content
- Set up self-hosted WordPress
- Deploy theme with full CSP control
- 2-hour process, $10-25/mo hosting

## When to Use This Pattern
- WordPress.com Business plan
- Custom external CDNs required (3D libraries, specific analytics)
- Platform restrictions blocking features
- Need server-level header control

## Related Patterns
- WordPress.com REST API quirks (index.php?rest_route=)
- WordPress.com SFTP deployment workflow
- Self-hosted migration process
```

---

## When User Requests Learning

1. **Review session**: What problems were solved?
2. **Identify patterns**: Reusable, non-obvious, tested?
3. **Extract structure**: Problem, solution, when to use
4. **Format markdown**: Clear, concise, with code examples
5. **Save to Serena**: Appropriate memory category
6. **Report back**: "Saved pattern: [name] to Serena memory"

---

## Continuous Improvement

As patterns accumulate:
- Skills become more specific
- Fewer "trial and error" attempts
- Faster problem resolution
- Better recommendations

**Goal**: Every unique problem solved should become a reusable pattern for future sessions.
