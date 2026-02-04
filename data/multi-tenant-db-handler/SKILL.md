---
name: multi-tenant-db-handler
description: Handles multi-tenant database connections and operations for CakePHP projects using company-specific database patterns
---

# Multi-Tenant Database Handler

A specialized skill for managing multi-tenant database architectures in CakePHP projects, particularly for systems using company-specific database instances.

## Core Concepts

### 1. Database Naming Pattern

**Pattern** (company-specific databases):
```
[app_prefix]_company_{company_id}
```

**Example** (anonymized from actual project):
```
example_app_company_{company_id}

Examples:
example_app_company_1001  # Company ID 1001
example_app_company_9999  # Test company (PHPUNIT_COMPANY_ID)
```

### 2. Connection Management Component

**MessageDeliveryDbAccessorComponent pattern:**
```php
// Get company-specific connection
$conn = $this->MessageDeliveryDbAccessor->getUserMessageDeliveryDbConnection($companyId);

// Set connection for table
$ApplicationsTable = TableRegistry::getTableLocator()->get('Applications');
$ApplicationsTable->setConnection($conn);

// Use the table with company-specific database
$applications = $ApplicationsTable->find()
    ->where(['status' => $status])
    ->all();
```

### 3. Database Architecture

**Pattern** (multi-tier database structure):
```
1. Account Database (Shared)
   - [app]_account_schema
   - Contains: companys, company_users
   - Shared across all companies

2. Client Database (Shared)
   - [app]_client_schema
   - Contains: master data, configurations
   - Shared across all companies

3. Company Databases (Per-tenant)
   - [app_prefix]_company_%d
   - Contains: applications, addresses, messages
   - Unique per company
```

**Example** (anonymized from actual project):
```
1. Account Database: example_account_schema
2. Client Database: example_client_schema
3. Company Databases: example_app_company_%d
```

## Connection Patterns

### 1. Dynamic Connection Creation

**Create connection on-demand:**
```php
function getUserMessageDeliveryDbConnection($company_id) {
    $defConn = Configure::read('Datasources.deliver_default');
    $defConn['database'] = vsprintf($defConn['database'], [$company_id]);

    $connectionName = "Connection_" . $defConn['database'];

    if (!in_array($connectionName, ConnectionManager::configured())) {
        ConnectionManager::setConfig($connectionName, $defConn);
    }

    return ConnectionManager::get($connectionName);
}
```

### 2. Connection Release

**Clean up connections after use:**
```php
function releaseUserMessageDeliveryDbConnection($company_id) {
    $defConn = Configure::read('Datasources.deliver_default');
    $connectionName = "Connection_" . vsprintf($defConn['database'], [$company_id]);

    if (in_array($connectionName, ConnectionManager::configured())) {
        ConnectionManager::get($connectionName)->disconnect();
    }
}
```

### 3. Read Replica Support

**Handle read replicas for scalability:**
```php
function getReplicaUserMessageDeliveryDbConnection($company_id) {
    // Try replicas first
    $replicaConf = Configure::read('Datasources.deliver_replication');

    // Fall back to master if replica unavailable
    if (!$replicaAvailable) {
        return getUserMessageDeliveryDbConnection($company_id);
    }
}
```

## Test Environment Configuration

### Test Database Names

**Pattern** (test databases):
```php
// Account schema test database
'test_default_test_session_001'

// Client schema test database
'test_client_9999001'

// Company-specific test database
'test_[app_prefix]_company_9999'  // PHPUNIT_COMPANY_ID = 9999
```

**Example** (anonymized from actual project):
```php
'test_example_app_company_9999'
```

### Test Connection Setup

**In test bootstrap:**
```php
// Configure test connections
ConnectionManager::setConfig('test_deliver_default', [
    'className' => Connection::class,
    'driver' => Mysql::class,
    'host' => env('DB_HOST', 'db'),
    'username' => env('DB_USER', 'root'),
    'password' => env('DB_PASS', 'root'),
    'database' => 'test_[app_prefix]_company_%d',
    'encoding' => 'utf8mb4',
    'timezone' => 'Asia/Tokyo',
]);
```

## Common Operations

### 1. Switch Database Context

```php
// In Controller
public function viewApplications($companyId)
{
    // Get company-specific connection
    $conn = $this->MessageDeliveryDbAccessor
        ->getUserMessageDeliveryDbConnection($companyId);

    // Apply to table
    $this->Applications->setConnection($conn);

    // Now queries run against company database
    $applications = $this->Applications->find()->all();
}
```

### 2. Cross-Database Queries

```php
// Get user from account database
$user = $this->EcoCompanyUsers->get($userId);

// Switch to company database
$conn = $this->MessageDeliveryDbAccessor
    ->getUserMessageDeliveryDbConnection($user->eco_company_id);

// Get company-specific data
$this->Applications->setConnection($conn);
$userApplications = $this->Applications->find()
    ->where(['created_by' => $userId])
    ->all();
```

### 3. Batch Processing

```php
// Process multiple companies
$companies = $this->EcoCompanys->find()
    ->where(['del_flg' => 0])
    ->all();

foreach ($companies as $company) {
    // Get company connection
    $conn = $this->MessageDeliveryDbAccessor
        ->getUserMessageDeliveryDbConnection($company->id);

    // Process company data
    $this->Applications->setConnection($conn);
    $this->processCompanyApplications($company);

    // Release connection
    $this->MessageDeliveryDbAccessor
        ->releaseUserMessageDeliveryDbConnection($company->id);
}
```

## Error Handling

### Connection Failures

```php
try {
    $conn = $this->MessageDeliveryDbAccessor
        ->getUserMessageDeliveryDbConnection($companyId);
} catch (\Exception $e) {
    Log::error('Failed to connect to company database: ' . $companyId);
    throw new \RuntimeException('Database connection failed');
}
```

### Invalid Company ID

```php
// Validate company exists before connection
$company = $this->EcoCompanys->find()
    ->where(['id' => $companyId, 'del_flg' => 0])
    ->first();

if (!$company) {
    throw new NotFoundException('Company not found');
}

// Safe to connect
$conn = $this->MessageDeliveryDbAccessor
    ->getUserMessageDeliveryDbConnection($companyId);
```

## Best Practices

### 1. Connection Pooling
- Reuse existing connections when possible
- Release connections after batch operations
- Monitor connection count

### 2. Security
- Never expose company IDs in URLs
- Validate company access permissions
- Use prepared statements for all queries

### 3. Performance
- Use read replicas for read-heavy operations
- Cache frequently accessed data
- Batch operations when processing multiple companies

### 4. Testing
- Always use PHPUNIT_COMPANY_ID (9999) for tests
- Create test databases with migration runner
- Clean up test data after each test

## Anti-Patterns to Avoid

### ❌ Hardcoded Database Names
```php
// WRONG
$conn = ConnectionManager::get('[app_prefix]_company_1001');
```

### ❌ Manual Connection String Building
```php
// WRONG
$database = '[app_prefix]_company_' . $companyId;
```

### ❌ Forgetting to Release Connections
```php
// WRONG - No release
$conn = $this->getUserMessageDeliveryDbConnection($companyId);
// ... use connection
// Missing: releaseUserMessageDeliveryDbConnection()
```

### ❌ Cross-Company Data Access
```php
// WRONG - Accessing another company's data
$conn1 = $this->getUserMessageDeliveryDbConnection($company1);
$conn2 = $this->getUserMessageDeliveryDbConnection($company2);
// Never mix data between companies
```

## Integration with Other Skills

- Works with `fixture-generator` for test data creation
- Used by `test-guardian` agent for multi-tenant test validation
- Essential for `migration-validator` in multi-database setups

## CakePHP Version Compatibility

- CakePHP 4.x: Full support with ConnectionManager
- CakePHP 3.x: Legacy support (different API)
- Requires PHP 7.4+ for typed properties