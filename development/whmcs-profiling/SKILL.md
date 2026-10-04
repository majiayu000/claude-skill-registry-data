---
name: whmcs-profiling
description: Code profiling for WHMCS
category: Troubleshooting & Debugging
version: 1.0.0
---

# WHMCS Code Profiling Skill

## Overview
This skill provides patterns for profiling code in WHMCS to identify performance bottlenecks.

## Implementation Patterns

### Profiler
```php
<?php
/**
 * WHMCS Code Profiling
 * Profiles code execution time
 */

namespace WHMCS\Module\Diagnostics\Profiler;

class Profiler {
    private $marks = [];

    /**
     * Start profiling
     */
    public function start(string $label): void {
        $this->marks[$label] = [
            'start' => microtime(true),
            'memory_start' => memory_get_usage(true)
        ];
    }

    /**
     * End profiling
     */
    public function end(string $label): array {
        if (!isset($this->marks[$label])) {
            return null;
        }

        $start = $this->marks[$label];
        $duration = microtime(true) - $start['start'];
        $memoryDelta = memory_get_usage(true) - $start['memory_start'];

        return [
            'label' => $label,
            'duration_ms' => round($duration * 1000, 2),
            'memory_delta_mb' => round($memoryDelta / 1024 / 1024, 2)
        ];
    }

    /**
     * Get all profile data
     */
    public function getReport(): array {
        $report = [];
        foreach ($this->marks as $label => $mark) {
            if (isset($mark['end'])) {
                $report[] = $mark;
            }
        }
        return $report;
    }
}
```

## Best Practices

1. **Strategic Markers**: Profile key sections only
2. **Memory Tracking**: Watch for memory issues
3. **Compare Runs**: Track before/after changes
4. **Aggregate Data**: Build performance baselines
5. **Visualize**: Use profiling tools

## Related Skills

- whmcs-debug-mode
- whmcs-api-latency
- whmcs-slow-query
- whmcs-memory-debugging