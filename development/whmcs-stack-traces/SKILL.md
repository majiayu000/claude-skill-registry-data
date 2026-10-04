---
name: whmcs-stack-traces
description: Error stack analysis for WHMCS
category: Troubleshooting & Debugging
version: 1.0.0
---

# WHMCS Stack Trace Analysis Skill

## Overview
This skill provides patterns for analyzing error stack traces in WHMCS.

## Implementation Patterns

### Stack Trace Analyzer
```php
<?php
/**
 * WHMCS Stack Trace Analysis
 * Analyzes error stack traces
 */

namespace WHMCS\Module\Diagnostics\Errors;

class StackTraceAnalyzer {
    /**
     * Parse stack trace
     */
    public function parseStackTrace(string $trace): array {
        $lines = explode("\n", $trace);
        $frames = [];

        foreach ($lines as $line) {
            if (preg_match('/#(\d+)\s+(.+?)\((.+?)\)\s+\[([^\]]+)\]/', $line, $matches)) {
                $frames[] = [
                    'number' => $matches[1],
                    'function' => $matches[2],
                    'file' => $matches[3],
                    'line' => $matches[4]
                ];
            }
        }

        return $frames;
    }

    /**
     * Find root cause
     */
    public function findRootCause(array $frames): array {
        // First frame is usually where error originated
        return [
            'file' => $frames[0]['file'] ?? 'unknown',
            'line' => $frames[0]['line'] ?? 0,
            'function' => $frames[0]['function'] ?? 'unknown'
        ];
    }
}
```

## Best Practices

1. **Log All Traces**: Store stack traces in logs
2. **Group by File**: Identify frequent error sources
3. **Filter Framework**: Exclude framework noise
4. **Line Numbers**: Track specific problem lines
5. **Version Correlation**: Link to code version

## Related Skills

- whmcs-debug-mode
- whmcs-log-analysis
- whmcs-crash-analysis
- whmcs-incident-response