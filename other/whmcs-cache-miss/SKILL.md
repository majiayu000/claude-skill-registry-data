---
name: whmcs-cache-miss
description: Cache miss analysis for WHMCS
category: Troubleshooting & Debugging
version: 1.0.0
---

# WHMCS Cache Miss Analysis Skill

## Overview
This skill provides patterns for analyzing cache misses in WHMCS.

## Implementation Patterns

### Cache Miss Analyzer
```php
<?php
/**
 * WHMCS Cache Miss Analysis
 * Analyzes cache miss patterns
 */

namespace WHMCS\Module\Diagnostics\Cache;

class CacheMissAnalyzer {
    private $db;

    public function __construct() {
        $this->db = \WHMCS\Database\Capsule::connection();
    }

    /**
     * Analyze cache miss patterns
     */
    public function analyzeMisses(int $hours = 24): array {
        $misses = $this->db->select(
            "SELECT cache_key, COUNT(*) as miss_count
             FROM mod_cache_stats
             WHERE operation = 'miss'
             AND created_at > DATE_SUB(NOW(), INTERVAL ? HOUR)
             GROUP BY cache_key
             ORDER BY miss_count DESC
             LIMIT 50",
            [$hours]
        );

        $totalMisses = array_sum(array_column($misses, 'miss_count'));
        $hits = $this->getTotalHits($hours);

        return [
            'total_misses' => $totalMisses,
            'total_hits' => $hits,
            'miss_ratio' => $hits > 0 ? round($totalMisses / ($totalMisses + $hits) * 100, 2) : 100,
            'top_missed_keys' => $misses
        ];
    }

    /**
     * Identify cache patterns
     */
    public function identifyPatterns(): array {
        $patterns = $this->db->select(
            "SELECT SUBSTRING_INDEX(cache_key, '_', 2) as pattern,
                    COUNT(*) as count
             FROM mod_cache_stats
             GROUP BY pattern
             ORDER BY count DESC
             LIMIT 10"
        );

        return array_map(fn($p) => [
            'pattern' => $p->pattern,
            'count' => $p->count
        ], $patterns);
    }

    private function getTotalHits(int $hours): int {
        $result = $this->db->select(
            "SELECT COUNT(*) as hits FROM mod_cache_stats
             WHERE operation = 'hit'
             AND created_at > DATE_SUB(NOW(), INTERVAL ? HOUR)",
            [$hours]
        );
        return $result[0]->hits ?? 0;
    }
}
```

## Best Practices

1. **Track All Misses**: Log every cache miss
2. **Analyze Patterns**: Find frequent miss patterns
3. **Prefetch Strategy**: Predict and prefetch
4. **TTL Optimization**: Adjust TTL based on patterns
5. **Key Design**: Improve cache key design

## Related Skills

- whmcs-caching-strategies
- whmcs-query-caching
- whmcs-monitoring-agent
- whmcs-log-analysis