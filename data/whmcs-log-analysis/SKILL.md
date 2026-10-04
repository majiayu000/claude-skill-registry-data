---
name: whmcs-log-analysis
description: Log analysis techniques for WHMCS
category: Troubleshooting & Debugging
version: 1.0.0
---

# WHMCS Log Analysis Skill

## Overview
This skill provides patterns and implementations for analyzing logs in WHMCS to identify issues and patterns.

## Implementation Patterns

### Log Analysis Manager
```php
<?php
/**
 * WHMCS Log Analysis
 * Analyzes system logs for issues
 */

namespace WHMCS\Module\Diagnostics\Logs;

class LogAnalysisManager {
    private $db;

    public function __construct() {
        $this->db = \WHMCS\Database\Capsule::connection();
    }

    /**
     * Analyze errors
     */
    public function analyzeErrors(int $serviceId, int $hours = 24): array {
        $from = date('Y-m-d H:i:s', strtotime("-{$hours} hours"));

        $errors = $this->db->select(
            "SELECT * FROM mod_debug_logs
             WHERE level IN ('error', 'critical')
             AND created_at >= ?
             ORDER BY created_at DESC",
            [$from]
        );

        $analysis = [
            'total_errors' => count($errors),
            'by_type' => [],
            'timeline' => [],
            'recommendations' => []
        ];

        foreach ($errors as $error) {
            $type = $this->categorizeError($error->message);
            if (!isset($analysis['by_type'][$type])) {
                $analysis['by_type'][$type] = 0;
            }
            $analysis['by_type'][$type]++;

            $hour = date('Y-m-d H:00', strtotime($error->created_at));
            if (!isset($analysis['timeline'][$hour])) {
                $analysis['timeline'][$hour] = 0;
            }
            $analysis['timeline'][$hour]++;
        }

        // Generate recommendations
        if ($analysis['total_errors'] > 10) {
            $analysis['recommendations'][] = "High error rate detected - investigate root cause";
        }

        return $analysis;
    }

    /**
     * Search logs
     */
    public function searchLogs(string $pattern, int $limit = 100): array {
        $logs = $this->db->select(
            "SELECT * FROM mod_debug_logs
             WHERE message LIKE ?
             ORDER BY created_at DESC
             LIMIT ?",
            ['%' . $pattern . '%', $limit]
        );

        return array_map(function($log) {
            return [
                'id' => $log->id,
                'level' => $log->level,
                'message' => $log->message,
                'context' => json_decode($log->context, true),
                'created_at' => $log->created_at
            ];
        }, $logs);
    }

    private function categorizeError(string $message): string {
        $patterns = [
            'database' => ['sql', 'query', 'mysql', 'connection'],
            'memory' => ['memory', 'allocation', 'limit'],
            'timeout' => ['timeout', 'timed out', 'slow'],
            'authentication' => ['auth', 'login', 'password', 'token']
        ];

        foreach ($patterns as $category => $keywords) {
            foreach ($keywords as $keyword) {
                if (stripos($message, $keyword) !== false) {
                    return $category;
                }
            }
        }

        return 'other';
    }
}
```

## Best Practices

1. **Log Levels**: Use appropriate log levels
2. **Searchable**: Include searchable keywords
3. **Context**: Add context to log entries
4. **Retention**: Set retention policies
5. **Alerting**: Set up alerts for critical errors

## Related Skills

- whmcs-debug-mode
- whmcs-stack-traces
- whmcs-incident-response
- whmcs-monitoring-agent