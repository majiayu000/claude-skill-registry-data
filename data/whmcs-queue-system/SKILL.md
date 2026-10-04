---
name: whmcs-queue-system
description: Async job queue for WHMCS
category: Performance & Monitoring
version: 1.0.0
---

# WHMCS Queue System Skill

## Overview
This skill provides patterns for implementing async job queues in WHMCS.

## Implementation Patterns

### Queue Manager
```php
<?php
/**
 * WHMCS Queue System
 * Manages async job processing
 */

namespace WHMCS\Module\Performance\Queue;

class QueueManager {
    private $db;

    public function __construct() {
        $this->db = \WHMCS\Database\Capsule::connection();
    }

    /**
     * Enqueue job
     */
    public function enqueue(array $job): string {
        $jobId = 'job_' . bin2hex(random_bytes(8));

        $this->db->insert('mod_queue_jobs', [
            'id' => $jobId,
            'type' => $job['type'],
            'payload' => json_encode($job['payload']),
            'priority' => $job['priority'] ?? 5,
            'status' => 'pending',
            'created_at' => date('Y-m-d H:i:s')
        ]);

        return $jobId;
    }

    /**
     * Process jobs
     */
    public function processJobs(int $limit = 10): array {
        $jobs = $this->db->select(
            "SELECT * FROM mod_queue_jobs
             WHERE status = 'pending'
             ORDER BY priority ASC, created_at ASC
             LIMIT ?",
            [$limit]
        );

        $processed = [];
        foreach ($jobs as $job) {
            $result = $this->processJob($job);
            $processed[] = $result;
        }

        return [
            'processed' => count($processed),
            'results' => $processed
        ];
    }

    /**
     * Get queue stats
     */
    public function getStats(): array {
        $stats = $this->db->select(
            "SELECT status, COUNT(*) as count FROM mod_queue_jobs GROUP BY status"
        );

        return array_column($stats, 'count', 'status');
    }
}
```

## Database Schema
```sql
CREATE TABLE `mod_queue_jobs` (
  `id` VARCHAR(50) PRIMARY KEY,
  `type` VARCHAR(100) NOT NULL,
  `payload` TEXT NOT NULL,
  `priority` INT DEFAULT 5,
  `status` ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
  `attempts` INT DEFAULT 0,
  `error' TEXT,
  `created_at' DATETIME NOT NULL,
  `processed_at' DATETIME,
  INDEX `idx_status` (`status`),
  INDEX `idx_priority` (`priority`)
);
```

## Best Practices

1. **Prioritization**: Use priority levels
2. **Retry Logic**: Implement job retries
3. **Error Handling**: Graceful error handling
4. **Monitoring**: Track queue depth
5. **Workers**: Scale workers as needed

## Related Skills

- whmcs-caching-strategies
- whmcs-monitoring-agent
- whmcs-connection-pooling
- whmcs-database-indexing