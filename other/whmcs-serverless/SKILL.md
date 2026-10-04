---
name: whmcs-serverless
description: Serverless functions for WHMCS
category: Automation & DevOps
version: 1.0.0
---

# WHMCS Serverless Functions Skill

## Overview
This skill provides patterns for implementing serverless functions in WHMCS.

## Implementation Patterns

### Serverless Function Manager
```php
<?php
/**
 * WHMCS Serverless Functions
 * Manages serverless function deployment
 */

namespace WHMCS\Module\DevOps\Serverless;

class ServerlessManager {
    private $db;

    public function __construct() {
        $this->db = \WHMCS\Database\Capsule::connection();
    }

    /**
     * Deploy function
     */
    public function deployFunction(array $params): array {
        $functionId = 'func_' . bin2hex(random_bytes(8));

        $this->db->insert('mod_serverless_functions', [
            'id' => $functionId,
            'name' => $params['name'],
            'runtime' => $params['runtime'] ?? 'nodejs18',
            'code' => base64_encode($params['code']),
            'handler' => $params['handler'] ?? 'index.handler',
            'memory' => $params['memory'] ?? 256,
            'timeout' => $params['timeout'] ?? 30,
            'env_vars' => json_encode($params['env'] ?? []),
            'created_at' => date('Y-m-d H:i:s')
        ]);

        // Deploy to cloud provider
        $this->deployToProvider($functionId, $params);

        return [
            'success' => true,
            'function_id' => $functionId,
            'endpoint' => $this->getEndpoint($functionId)
        ];
    }

    /**
     * Invoke function
     */
    public function invokeFunction(string $functionId, array $payload): array {
        $result = $this->callFunction($functionId, $payload);

        return [
            'success' => true,
            'result' => $result,
            'execution_time_ms' => 0
        ];
    }

    /**
     * List functions
     */
    public function listFunctions(): array {
        return $this->db->select(
            "SELECT id, name, runtime, memory, timeout, status FROM mod_serverless_functions"
        );
    }

    private function deployToProvider(string $functionId, array $params): void {
        // Deploy to AWS Lambda, GCP Functions, or Azure Functions
    }

    private function getEndpoint(string $functionId): string {
        $function = $this->db->select("SELECT name FROM mod_serverless_functions WHERE id = ?", [$functionId])[0];
        return "https://functions.whmcs.com/" . $function->name;
    }
}
```

## Database Schema
```sql
CREATE TABLE `mod_serverless_functions` (
  `id` VARCHAR(50) PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL UNIQUE,
  `runtime` VARCHAR(50) DEFAULT 'nodejs18',
  `code` TEXT NOT NULL,
  `handler` VARCHAR(255) DEFAULT 'index.handler',
  `memory` INT DEFAULT 256,
  `timeout` INT DEFAULT 30,
  `env_vars` TEXT,
  `status` ENUM('active', 'inactive', 'error') DEFAULT 'active',
  `created_at' DATETIME NOT NULL
);
```

## Best Practices

1. **Stateless Functions**: Design for stateless execution
2. **Cold Starts**: Minimize cold start times
3. **Resource Sizing**: Right-size memory/timeout
4. **Error Handling**: Implement robust error handling
5. **Monitoring**: Track function invocations

## Related Skills

- whmcs-cicd-integration
- whmcs-gitops-workflow
- whmcs-secrets-management
- whmcs-monitoring-agent