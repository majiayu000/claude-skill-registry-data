---
name: whmcs-lazy-loading
description: Lazy load assets for WHMCS
category: Performance & Monitoring
version: 1.0.0
---

# WHMCS Lazy Loading Skill

## Overview
This skill provides patterns for lazy loading assets in WHMCS.

## Implementation Patterns

### Lazy Load Manager
```php
<?php
/**
 * WHMCS Lazy Loading
 * Implements lazy loading for images/scripts
 */

namespace WHMCS\Module\Performance\LazyLoad;

class LazyLoadManager {
    /**
     * Generate lazy load attributes
     */
    public function getLazyAttributes(string $type, string $src): array {
        if ($type === 'image') {
            return [
                'loading' => 'lazy',
                'src' => $src,
                'data-src' => $src
            ];
        }

        return ['data-src' => $src, 'class' => 'lazy-load'];
    }

    /**
     * Generate lazy load script
     */
    public function getLazyLoadScript(): string {
        return <<<SCRIPT
document.addEventListener("DOMContentLoaded", function() {
    const lazyImages = document.querySelectorAll("img[data-src]");
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.src = entry.target.dataset.src;
                observer.unobserve(entry.target);
            }
        });
    });
    lazyImages.forEach(img => observer.observe(img));
});
SCRIPT;
    }
}
```

## Best Practices

1. **Native Lazy Loading**: Use loading="lazy" attribute
2. **Intersection Observer**: Use for custom lazy loading
3. **Placeholder Images**: Use lightweight placeholders
4. **Below Fold First**: Lazy load below-the-fold content
5. **CDN Integration**: Lazy load from CDN

## Related Skills

- whmcs-image-optimization
- whmcs-prefetching
- whmcs-resource-optimization
- whmcs-http2-push