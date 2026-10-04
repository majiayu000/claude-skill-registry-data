---
name: whmcs-debug-mode
description: Debug mode configuration for WHMCS
category: Troubleshooting & Debugging
version: 1.0.0
---

# WHMCS Debug Mode Configuration Skill

## Overview
This skill provides patterns and implementations for configuring debug mode in WHMCS for troubleshooting and development.

## Implementation Patterns

### Debug Mode Manager
```php
<?php
/**
 * WHMCS Debug Mode Configuration
 * Manages debug settings and diagnostics
 */

namespace WHMCS\Module\Diagnostics\Debug;

class DebugModeManager {
    private $db;

    public function __construct() {
        $this->db = \WHMCS\Database\Capsule::connection();
    }

    /**
     * Enable debug mode
     */
    public function enableDebug(array $params): array {
        $config = [
            'debug_enabled' => true,
            'debug_level' => $params['level'] ?? 'verbose',
            'log_queries' => $params['log_queries'] ?? true,
            'log_errors' => $params['log_errors'] ?? true,
            'display_errors' => $params['display_errors'] ?? false,
            'profiler_enabled' => $params['profiler'] ?? false,
            'trace_enabled' => $params['trace'] ?? false
        ];

        $this->updateDebugConfig($config);

        return [
            'success' => true,
            'debug_enabled' => true,
            'config' => $config
        ];
    }

    /**
     * Get debug information
     */
    public function getDebugInfo(): array {
        return [
            'php_version' => PHP_VERSION,
            'memory_usage' => memory_get_usage(true),
            'peak_memory' => memory_get_peak_usage(true),
            'included_files' => count(get_included_files()),
            'loaded_extensions' => get_loaded_extensions(),
            'error_log' => error_log_get_recent(),
            'query_log' => $this->getQueryLog()
        ];
    }

    /**
     * Generate debug report
     */
    public function generateReport(): string {
        $report = [];

        $report[] = "=== WHMCS Debug Report ===";
        $report[] = "Generated: " . date('Y-m-d H:i:s');
        $report[] = "";
        $report[] = "=== System Information ===";
        $report[] = "PHP Version: " . PHP_VERSION;
        $report[] = "WHMCS Version: " . $this->getWHMCSVersion();
        $report[] = "Server: " . $_SERVER['SERVER_SOFTWARE'] ?? 'Unknown';
        $report[] = "";

        $report[] = "=== Memory Usage ===";
        $report[] = "Current: " . $this->formatBytes(memory_get_usage(true));
        $report[] = "Peak: " . $this->formatBytes(memory_get_peak_usage(true));
        $report[] = "";

        $report[] = "=== Recent Errors ===";
        $report[] = implode("\n", $this->getRecentErrors());
        $report[] = "";

        return implode("\n", $report);
    }

    private function formatBytes(int $bytes): string {
        $units = ['B', 'KB', 'MB', 'GB'];
        $i = 0;
        while ($bytes >= 1024 && $i < count($units) - 1) {
            $bytes /= 1024;
            $i++;
        }
        return round($bytes, 2) . ' ' . $units[$i];
    }
}
```

## Database Schema
```sql
CREATE TABLE `mod_debug_logs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `level` ENUM('debug', 'info', 'warning', 'error', 'critical') NOT NULL,
  `message` TEXT NOT NULL,
  `context` TEXT,
  `created_at` DATETIME NOT NULL,
  INDEX `idx_level` (`level`),
  INDEX `idx_created` (`created_at`)
);
```

## Best Practices

1. **Security**: Never enable debug in production
2. **Log Rotation**: Rotate logs to prevent disk full
3. **Sensitive Data**: Don't log passwords or tokens
4. **Performance**: Debug mode impacts performance
5. **Quick Disable**: Have easy way to disable

## Related Skills

- whmcs-log-analysis
- whmcs-stack-traces
- whmcs-profiling
- whmcs-incident-response