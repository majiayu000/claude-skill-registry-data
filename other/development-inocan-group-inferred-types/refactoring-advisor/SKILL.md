---
name: refactoring-advisor
description: Provides refactoring recommendations for PHP/CakePHP code to improve maintainability, performance, and adherence to best practices
---

# PHP/CakePHP Refactoring Advisor

A specialized skill for identifying refactoring opportunities and providing actionable recommendations for PHP/CakePHP applications.

## Core Responsibilities

### 1. Code Smell Detection

**Long Method:**
```php
// 🔴 Code Smell: Method > 50 lines
public function processOrder($data)
{
    // 100+ lines of code doing multiple things
    // Validation logic
    // Calculation logic
    // Database operations
    // Email sending
    // Logging
}

// ✅ Refactored: Extracted methods
public function processOrder($data)
{
    $this->validateOrderData($data);
    $total = $this->calculateOrderTotal($data);
    $order = $this->createOrder($data, $total);
    $this->sendOrderConfirmation($order);
    $this->logOrderCreation($order);
    return $order;
}

private function validateOrderData($data) { /* ... */ }
private function calculateOrderTotal($data) { /* ... */ }
private function createOrder($data, $total) { /* ... */ }
private function sendOrderConfirmation($order) { /* ... */ }
private function logOrderCreation($order) { /* ... */ }
```

**Large Class:**
```php
// 🔴 Code Smell: Class with too many responsibilities
class UserController extends AppController
{
    // 50+ methods handling everything
    public function login() { }
    public function register() { }
    public function sendEmail() { }
    public function generateReport() { }
    public function processPayment() { }
    // ... many more
}

// ✅ Refactored: Separated concerns
class UserController extends AppController
{
    public function login() { }
    public function register() { }
}

class ReportController extends AppController
{
    public function generate() { }
}

class PaymentService
{
    public function process() { }
}
```

**Duplicate Code:**
```php
// 🔴 Code Smell: Duplicated logic
public function approveApplication($id)
{
    $app = $this->Applications->get($id);
    $app->status = 3;
    $app->approved_date = date('Y-m-d');
    $this->Applications->save($app);
    $this->sendNotification($app->user_id, 'approved');
}

public function rejectApplication($id)
{
    $app = $this->Applications->get($id);
    $app->status = 4;
    $app->rejected_date = date('Y-m-d');
    $this->Applications->save($app);
    $this->sendNotification($app->user_id, 'rejected');
}

// ✅ Refactored: Extract common logic
public function updateApplicationStatus($id, $status)
{
    $app = $this->Applications->get($id);
    $app = $this->Applications->updateStatus($app, $status);
    $this->Applications->save($app);
    $this->sendStatusNotification($app);
}
```

### 2. Design Pattern Application

**Repository Pattern:**
```php
// 🔴 Before: Direct table access everywhere
class UsersController extends AppController
{
    public function getActiveUsers()
    {
        return $this->Users->find()
            ->where(['status' => 1, 'del_flg' => 0])
            ->contain(['Orders', 'Company'])
            ->order(['created' => 'DESC'])
            ->all();
    }
}

// ✅ After: Repository pattern
// src/Repository/UserRepository.php
class UserRepository
{
    private $Users;

    public function __construct()
    {
        $this->Users = TableRegistry::getTableLocator()->get('Users');
    }

    public function findActive()
    {
        return $this->Users->find('active')
            ->contain(['Orders', 'Company'])
            ->order(['created' => 'DESC']);
    }
}

// Controller using repository
class UsersController extends AppController
{
    private $userRepository;

    public function initialize(): void
    {
        parent::initialize();
        $this->userRepository = new UserRepository();
    }

    public function getActiveUsers()
    {
        return $this->userRepository->findActive()->all();
    }
}
```

**Service Layer Pattern:**
```php
// 🔴 Before: Business logic in controller
class OrdersController extends AppController
{
    public function create()
    {
        // Complex business logic in controller
        $data = $this->request->getData();

        // Validate inventory
        foreach ($data['items'] as $item) {
            $product = $this->Products->get($item['product_id']);
            if ($product->stock < $item['quantity']) {
                $this->Flash->error('在庫不足');
                return;
            }
        }

        // Calculate totals
        $total = 0;
        foreach ($data['items'] as $item) {
            $total += $item['price'] * $item['quantity'];
        }

        // Create order
        // Update inventory
        // Send email
        // etc...
    }
}

// ✅ After: Service layer
// src/Service/OrderService.php
class OrderService
{
    public function createOrder(array $data): OrderResult
    {
        $validation = $this->validateInventory($data['items']);
        if (!$validation->isValid()) {
            return OrderResult::error($validation->getErrors());
        }

        $total = $this->calculateTotal($data['items']);
        $order = $this->processOrder($data, $total);

        return OrderResult::success($order);
    }

    private function validateInventory(array $items) { }
    private function calculateTotal(array $items) { }
    private function processOrder(array $data, float $total) { }
}

// Simplified controller
class OrdersController extends AppController
{
    public function create()
    {
        $result = $this->OrderService->createOrder($this->request->getData());

        if ($result->isSuccess()) {
            $this->Flash->success('注文完了');
            return $this->redirect(['action' => 'view', $result->getOrder()->id]);
        }

        $this->Flash->error($result->getErrorMessage());
    }
}
```

**Factory Pattern:**
```php
// 🔴 Before: Complex object creation in multiple places
$notification = new EmailNotification();
$notification->setTo($user->email);
$notification->setSubject('Order Confirmation');
$notification->setTemplate('order_confirm');
$notification->setData($orderData);
$notification->send();

// ✅ After: Factory pattern
class NotificationFactory
{
    public static function create(string $type, array $config): NotificationInterface
    {
        switch ($type) {
            case 'email':
                return new EmailNotification($config);
            case 'sms':
                return new SmsNotification($config);
            case 'line':
                return new LineNotification($config);
            default:
                throw new InvalidArgumentException("Unknown notification type: {$type}");
        }
    }
}

// Usage
$notification = NotificationFactory::create('email', [
    'to' => $user->email,
    'template' => 'order_confirm',
    'data' => $orderData,
]);
$notification->send();
```

### 3. Performance Refactoring

**Query Optimization:**
```php
// 🔴 Before: N+1 queries
$users = $this->Users->find()->all();
foreach ($users as $user) {
    $orderCount = $this->Orders->find()
        ->where(['user_id' => $user->id])
        ->count();
    $user->order_count = $orderCount;
}

// ✅ After: Single query with join
$users = $this->Users->find()
    ->select([
        'Users.id',
        'Users.name',
        'order_count' => $this->Orders->find()->func()->count('Orders.id')
    ])
    ->leftJoinWith('Orders')
    ->group(['Users.id'])
    ->all();
```

**Caching Implementation:**
```php
// 🔴 Before: Expensive calculation every time
public function getMonthlyStats($month)
{
    $stats = [];
    $startDate = new DateTime("first day of {$month}");
    $endDate = new DateTime("last day of {$month}");

    // Complex calculations
    $stats['total_orders'] = $this->calculateTotalOrders($startDate, $endDate);
    $stats['revenue'] = $this->calculateRevenue($startDate, $endDate);
    $stats['new_users'] = $this->calculateNewUsers($startDate, $endDate);

    return $stats;
}

// ✅ After: With caching
public function getMonthlyStats($month)
{
    $cacheKey = "monthly_stats_{$month}";

    return Cache::remember($cacheKey, function () use ($month) {
        $stats = [];
        $startDate = new DateTime("first day of {$month}");
        $endDate = new DateTime("last day of {$month}");

        $stats['total_orders'] = $this->calculateTotalOrders($startDate, $endDate);
        $stats['revenue'] = $this->calculateRevenue($startDate, $endDate);
        $stats['new_users'] = $this->calculateNewUsers($startDate, $endDate);

        return $stats;
    }, 'daily'); // Cache for 24 hours
}
```

**Lazy Loading to Eager Loading:**
```php
// 🔴 Before: Lazy loading
$applications = $this->Applications->find()->all();
foreach ($applications as $app) {
    // Each access triggers a query
    echo $app->user->name;
    echo $app->category->name;
    echo $app->allocation->status;
}

// ✅ After: Eager loading
$applications = $this->Applications->find()
    ->contain(['Users', 'Categories', 'Allocations'])
    ->all();
```

### 4. CakePHP-Specific Refactoring

**Component Extraction:**
```php
// 🔴 Before: Repeated code in controllers
class UsersController extends AppController
{
    public function export()
    {
        // CSV export logic
        $data = $this->Users->find()->all();
        $csv = fopen('php://output', 'w');
        // ... export logic
    }
}

class OrdersController extends AppController
{
    public function export()
    {
        // Same CSV export logic repeated
        $data = $this->Orders->find()->all();
        $csv = fopen('php://output', 'w');
        // ... export logic
    }
}

// ✅ After: Component
// src/Controller/Component/CsvExportComponent.php
class CsvExportComponent extends Component
{
    public function export($query, array $fields)
    {
        $data = $query->all();
        $csv = fopen('php://output', 'w');
        // ... reusable export logic
        return $csv;
    }
}

// Usage in controllers
class UsersController extends AppController
{
    public function initialize(): void
    {
        parent::initialize();
        $this->loadComponent('CsvExport');
    }

    public function export()
    {
        $query = $this->Users->find();
        return $this->CsvExport->export($query, ['id', 'name', 'email']);
    }
}
```

**Behavior Implementation:**
```php
// 🔴 Before: Repeated model logic
class UsersTable extends Table
{
    public function beforeSave($event, $entity, $options)
    {
        if ($entity->isNew()) {
            $entity->created_by = $this->getCurrentUserId();
        }
        $entity->modified_by = $this->getCurrentUserId();
    }
}

class OrdersTable extends Table
{
    public function beforeSave($event, $entity, $options)
    {
        // Same audit logic repeated
        if ($entity->isNew()) {
            $entity->created_by = $this->getCurrentUserId();
        }
        $entity->modified_by = $this->getCurrentUserId();
    }
}

// ✅ After: Behavior
// src/Model/Behavior/AuditableBehavior.php
class AuditableBehavior extends Behavior
{
    public function beforeSave(EventInterface $event, EntityInterface $entity, ArrayObject $options)
    {
        $userId = $this->getCurrentUserId();

        if ($entity->isNew()) {
            $entity->created_by = $userId;
        }
        $entity->modified_by = $userId;
    }
}

// Usage in tables
class UsersTable extends Table
{
    public function initialize(array $config): void
    {
        $this->addBehavior('Auditable');
    }
}
```

### 5. Testing Improvements

**Extract Test Helpers:**
```php
// 🔴 Before: Repeated test setup
class UserControllerTest extends TestCase
{
    public function testIndex()
    {
        // Complex authentication setup
        $user = $this->Users->get(1);
        $this->session(['Auth.User' => $user]);
        // ... test logic
    }

    public function testView()
    {
        // Same authentication setup repeated
        $user = $this->Users->get(1);
        $this->session(['Auth.User' => $user]);
        // ... test logic
    }
}

// ✅ After: Test helper trait
trait AuthenticationTestTrait
{
    protected function loginAs($userId = 1)
    {
        $user = $this->getTableLocator()->get('Users')->get($userId);
        $this->session(['Auth.User' => $user->toArray()]);
        return $user;
    }

    protected function loginAsAdmin()
    {
        return $this->loginAs($this->getAdminUserId());
    }
}

class UserControllerTest extends TestCase
{
    use AuthenticationTestTrait;

    public function testIndex()
    {
        $this->loginAs();
        // ... test logic
    }

    public function testAdminView()
    {
        $this->loginAsAdmin();
        // ... test logic
    }
}
```

### 6. Database Refactoring

**Normalization:**
```sql
-- 🔴 Before: Denormalized table
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_name VARCHAR(255),
    user_email VARCHAR(255),
    user_phone VARCHAR(20),
    product_name VARCHAR(255),
    product_price DECIMAL(10,2),
    quantity INT
);

-- ✅ After: Normalized tables
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20)
);

CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10,2)
);

CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,
    created DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

## Refactoring Process

### 1. Identify Candidates
```yaml
Indicators:
  - High cyclomatic complexity (> 20)
  - Long methods (> 50 lines)
  - Large classes (> 500 lines)
  - Duplicate code blocks
  - Deep nesting (> 3 levels)
  - Too many parameters (> 4)
  - Feature envy
  - Data clumps
```

### 2. Prioritize Refactoring
```yaml
Priority Matrix:
  High:
    - Security vulnerabilities
    - Performance bottlenecks
    - Frequently modified code
    - High-bug areas

  Medium:
    - Code smells in stable code
    - Moderate complexity
    - Occasional modifications

  Low:
    - Cosmetic issues
    - Rarely modified code
    - Low-impact areas
```

### 3. Refactoring Steps
```yaml
Process:
  1. Write tests for current behavior
  2. Make small, incremental changes
  3. Run tests after each change
  4. Commit working code frequently
  5. Document significant changes
```

## Refactoring Catalog

### Method-Level Refactoring
- Extract Method
- Inline Method
- Extract Variable
- Inline Variable
- Replace Temp with Query
- Split Temporary Variable
- Remove Assignments to Parameters
- Substitute Algorithm

### Class-Level Refactoring
- Extract Class
- Inline Class
- Extract Interface
- Move Method
- Move Field
- Extract Superclass
- Extract Subclass
- Collapse Hierarchy
- Form Template Method
- Replace Inheritance with Delegation

### Data Refactoring
- Replace Magic Number with Constant
- Encapsulate Field
- Replace Array with Object
- Replace Data Value with Object
- Change Value to Reference
- Change Reference to Value

### Conditional Refactoring
- Decompose Conditional
- Consolidate Conditional Expression
- Consolidate Duplicate Conditional Fragments
- Replace Nested Conditional with Guard Clauses
- Replace Conditional with Polymorphism
- Introduce Null Object

### API Refactoring
- Rename Method
- Add Parameter
- Remove Parameter
- Separate Query from Modifier
- Parameterize Method
- Replace Parameter with Explicit Methods
- Preserve Whole Object
- Replace Parameter with Method Call

## Output Format

```markdown
## Refactoring Recommendations: [Component Name]

### Executive Summary
- **Technical Debt Score**: High/Medium/Low
- **Estimated Effort**: X days
- **Risk Level**: Low/Medium/High
- **ROI**: High/Medium/Low

### Priority 1: Critical Refactoring

#### 1. Extract Service Layer from OrdersController
**Problem**: Controller contains 300+ lines of business logic
**Impact**: Hard to test, violates SRP, difficult to maintain

**Solution**:
```php
// Create OrderService class
class OrderService {
    public function processOrder($data) { }
    public function validateOrder($data) { }
    public function calculateTotals($items) { }
}
```

**Benefits**:
- Improved testability
- Reusable business logic
- Clear separation of concerns

**Estimated Time**: 4 hours

### Priority 2: Important Refactoring

#### 1. Replace N+1 Queries with Eager Loading
**Location**: ApplicationsController::index()

**Current Code**:
```php
foreach ($applications as $app) {
    $user = $app->user; // Triggers query
}
```

**Refactored Code**:
```php
$applications = $this->Applications->find()
    ->contain(['Users'])
    ->all();
```

**Performance Gain**: 50% reduction in database queries

### Priority 3: Nice-to-Have

#### 1. Extract Validation Rules to Separate Class
- Move validation logic from controller to dedicated validator
- Estimated time: 2 hours
- Low risk, medium benefit

### Implementation Plan

Week 1:
- [ ] Extract OrderService (8h)
- [ ] Fix N+1 queries (4h)
- [ ] Add caching layer (4h)

Week 2:
- [ ] Normalize database tables (8h)
- [ ] Extract common behaviors (4h)
- [ ] Update tests (4h)

### Metrics to Track
- Cyclomatic complexity reduction
- Test coverage improvement
- Performance benchmarks
- Bug reduction rate
```

## Best Practices

1. **Test First**: Ensure tests exist before refactoring
2. **Small Steps**: Make incremental changes
3. **Preserve Behavior**: Don't change functionality while refactoring
4. **Commit Often**: Keep refactoring commits separate
5. **Document Decisions**: Explain why refactoring was done
6. **Measure Impact**: Track improvements

Remember: Refactoring is about improving code structure without changing behavior. Always have tests in place before refactoring.