---
name: whmcs-slow-query
description: Slow query identification for WHMCS
category: Troubleshooting & Debugging
version: 1.0.0
---

# WHMCS Slow Query Identification Skill

## Overview
This skill provides patterns for identifying and optimizing slow database queries in WHMCS.

## Implementation Patterns

### Slow Query Analyzer
```php
<?php
/**
 * WHMCS Slow Query Analysis
 * Identifies and optimizes slow queries
 */

namespace WHMCS\Module\Database;

class SlowQueryAnalyzer {
    private $db;

    public function __construct() {
        $this->db = \WHMCS\Database\Capsule::connection();
    }

    /**
     * Get slow queries
     */
    public function getSlowQueries(int $thresholdMs = 1000, int $limit = 50): array {
        return $this->db->select(
            "SELECT * FROM mod_slow_queries
             WHERE execution_time > ?
             ORDER BY execution_time DESC
             LIMIT ?",
            [$thresholdMs, $limit]
        );
    }

    /**
     * Analyze query execution plan
     */
    public function analyzeQueryPlan(string $query): array {
        $explain = $this->db->select("EXPLAIN " . $query);

        return [
            'query' => $query,
            'plan' => $explain,
            'suggestions' => $this->generateSuggestions($explain)
        ];
    }

    /**
     * Generate optimization suggestions
     */
    private function generateSuggestions(array $plan): array {
        $suggestions = [];

        foreach ($plan as $step) {
            if (($step['type'] ?? '') === 'ALL') {
                $suggestions[] = "Full table scan detected on {$step['table']}";
            }

            if (($step['key'] ?? null) === null) {
                $suggestions[] = "No index used in {$step['table']}";
            }
        }

        return $suggestions;
    }
}
```

## Best Practices

1. **Set Threshold**: Define what 'slow' means
2. **Log Everything**: Capture all slow queries
3. **Analyze Regularly**: Review slow query patterns
4. **Index Creation**: Create indexes for slow queries
5. **Query Optimization**: Rewrite inefficient queries

## Related Skills

- whmcs-database-indexing
- whmcs-query-caching
- whmcs-profiling
- whmcs-log-analysis