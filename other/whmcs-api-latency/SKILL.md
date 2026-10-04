---
name: whmcs-api-latency
description: Latency analysis for WHMCS
category: Troubleshooting & Debugging
version: 1.0.0
---

# WHMCS API Latency Analysis Skill

## Overview
This skill provides patterns for analyzing API latency in WHMCS.

## Implementation Patterns

### API Latency Analyzer
```php
<?php
/**
 * WHMCS API Latency Analysis
 * Analyzes and reports API performance
 */

namespace WHMCS\Module\Diagnostics\API;

class LatencyAnalyzer {
    private $db;

    public function __construct() {
        $this->db = \WHMCS\Database\Capsule::connection();
    }

    /**
     * Analyze API endpoint latency
     */
    public function analyzeEndpoint(string $endpoint): array {
        $metrics = $this->db->select(
            "SELECT AVG(response_time) as avg_time,
                    MAX(response_time) as max_time,
                    PERCENTILE(response_time, 95) as p95
             FROM mod_api_metrics
             WHERE endpoint = ? AND created_at > DATE_SUB(NOW(), INTERVAL 1 DAY)",
            [$endpoint]
        )[0];

        return [
            'endpoint' => $endpoint,
            'avg_latency_ms' => round($metrics->avg_time, 2),
            'max_latency_ms' => round($metrics->max_time, 2),
            'p95_latency_ms' => round($metrics->p95, 2)
        ];
    }

    /**
     * Identify slow endpoints
     */
    public function identifySlowEndpoints(int $thresholdMs = 500): array {
        return $this->db->select(
            "SELECT endpoint, AVG(response_time) as avg_time
             FROM mod_api_metrics
             WHERE created_at > DATE_SUB(NOW(), INTERVAL 1 DAY)
             GROUP BY endpoint
             HAVING avg_time > ?
             ORDER BY avg_time DESC",
            [$thresholdMs]
        );
    }
}
```

## Best Practices

1. **Set Baselines**: Know normal response times
2. **Track Percentiles**: Use p95/p99 for evaluation
3. **Alert Thresholds**: Set alerts for slow responses
4. **Endpoint Grouping**: Analyze by API category
5. **Trend Analysis**: Track over time

## Related Skills

- whmcs-profiling
- whmcs-slow-query
- whmcs-monitoring-agent
- whmcs-incident-response