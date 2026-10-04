---
name: whmcs-http2-push
description: HTTP/2 server push for WHMCS
category: Performance & Monitoring
version: 1.0.0
---

# WHMCS HTTP/2 Server Push Skill

## Overview
This skill provides patterns and implementations for HTTP/2 server push configuration in WHMCS for improved page load performance.

## Implementation Patterns

### HTTP/2 Push Manager
```php
<?php
/**
 * WHMCS HTTP/2 Server Push
 * Manages HTTP/2 push for resources
 */

namespace WHMCS\Module\Performance\Http2;

class HTTP2PushManager {
    private $db;

    public function __construct() {
        $this->db = \WHMCS\Database\Capsule::connection();
    }

    /**
     * Configure HTTP/2 push for page
     */
    public function configurePush(array $params): array {
        $resources = $params['resources']; // CSS, JS, fonts, images

        $pushConfig = [];

        foreach ($resources as $resource) {
            $pushConfig[] = [
                'path' => $resource['path'],
                'type' => $resource['type'], // style, script, font, image
                'weight' => $resource['weight'] ?? 1
            ];
        }

        // Generate link headers
        $linkHeaders = $this->generateLinkHeaders($pushConfig);

        return [
            'success' => true,
            'link_headers' => $linkHeaders,
            'resources_count' => count($pushConfig)
        ];
    }

    /**
     * Generate preload link headers
     */
    public function generateLinkHeaders(array $resources): string {
        $headers = [];

        foreach ($resources as $resource) {
            $as = match($resource['type']) {
                'style' => 'style',
                'script' => 'script',
                'font' => 'font',
                'image' => 'image',
                default => 'fetch'
            };

            $headers[] = "<{$resource['path']}>; rel=preload; as={$as}; crossorigin";
        }

        return implode(",\n", $headers);
    }

    /**
     * Push critical CSS
     */
    public function pushCriticalCSS(): string {
        $criticalCSS = file_get_contents(WHMCS_ROOT . '/assets/css/critical.css');

        return "<" . WHMCS_URL . "/assets/css/critical.css>; rel=preload; as=style";
    }
}
```

## Best Practices

1. **Critical Resources Only**: Push above-the-fold content
2. **Prioritization**: Use link priority hints
3. **Avoid Over-Push**: Don't push too many resources
4. **Combine**: Preload combined/minified files
5. **CORS**: Include crossorigin for fonts/assets

## Related Skills

- whmcs-browser-caching
- whmcs-prefetching
- whmcs-resource-optimization
- whmcs-caching-strategies