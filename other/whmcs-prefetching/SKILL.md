---
name: whmcs-prefetching
description: Resource prefetching for WHMCS
category: Performance & Monitoring
version: 1.0.0
---

# WHMCS Resource Prefetching Skill

## Overview
This skill provides patterns for resource prefetching in WHMCS.

## Implementation Patterns

### Prefetch Manager
```php
<?php
/**
 * WHMCS Resource Prefetching
 * Prefetches resources for faster navigation
 */

namespace WHMCS\Module\Performance\Prefetch;

class PrefetchManager {
    /**
     * Generate prefetch hints
     */
    public function generatePrefetchHints(array $pages): string {
        $hints = [];

        foreach ($pages as $page) {
            $hints[] = "<link rel=\"prefetch\" href=\"{$page}\">";
        }

        return implode("\n", $hints);
    }

    /**
     * Prefetch for navigation prediction
     */
    public function predictAndPrefetch(): string {
        return <<<SCRIPT
document.addEventListener("mouseover", function(e) {
    const link = e.target.closest("a");
    if (link && link.href) {
        const prefetch = document.createElement("link");
        prefetch.rel = "prefetch";
        prefetch.href = link.href;
        document.head.appendChild(prefetch);
    }
}, { passive: true });
SCRIPT;
    }
}
```

## Best Practices

1. **DNS Prefetch**: Prefetch DNS for external domains
2. **Preconnect**: Establish early connections
3. **Prefetch Pages**: Prefetch likely next pages
4. **Predictive**: Use navigation prediction
5. **Budget**: Don't prefetch too aggressively

## Related Skills

- whmcs-http2-push
- whmcs-lazy-loading
- whmcs-caching-strategies
- whmcs-browser-caching