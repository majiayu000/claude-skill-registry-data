---
name: functional-designer
description: Designs functional architecture and detailed specifications for PHP/CakePHP applications based on analyzed requirements
---

# Functional Designer

A specialized skill for creating detailed functional designs and technical specifications for PHP/CakePHP applications.

## Core Responsibilities

### 1. Functional Architecture Design

**Component Mapping:**
```yaml
Functional Component Design:
  Controllers:
    - name: [Controller]Controller
    - actions: [list of actions]
    - authentication: required|optional
    - authorization: role-based permissions

  Models:
    - Tables: [list of Table classes]
    - Entities: [list of Entity classes]
    - Associations: [relationships]
    - Validation: [rules]

  Views:
    - Templates: [list of .php files]
    - Elements: [reusable components]
    - Layouts: [page structures]

  Components:
    - Custom components needed
    - Third-party integrations
```

### 2. API Design Specification

**RESTful Endpoint Design:**
```yaml
API Endpoint:
  method: GET|POST|PUT|DELETE
  path: /api/v1/[resource]
  authentication: required|optional

  request:
    headers:
      Content-Type: application/json
      Authorization: Bearer [token]
    body:
      field1: type
      field2: type

  response:
    success:
      status: 200
      body: {data: [...]}
    error:
      status: 400|401|404|500
      body: {error: "message"}
```

### 3. Data Flow Design

**Request Lifecycle:**
```
1. Route → Controller
2. Controller → Authorization Check
3. Controller → Validation
4. Controller → Model/Service
5. Model → Database
6. Model → Entity
7. Controller → View/JSON Response
```

**Data Transformation:**
```php
Input Data → Validation → Business Logic → Entity → Output Format
```

### 4. CakePHP Design Patterns

**MVC Structure:**
```
src/
├── Controller/
│   ├── AppController.php
│   ├── User/
│   │   └── UsersController.php
│   └── Api/
│       └── UsersController.php
├── Model/
│   ├── Table/
│   │   └── UsersTable.php
│   └── Entity/
│       └── User.php
├── View/
│   └── User/
│       └── Users/
│           ├── index.php
│           ├── view.php
│           ├── add.php
│           └── edit.php
└── Service/
    └── UserService.php
```

### 5. Design Document Template

```markdown
# Functional Design: [Feature Name]

## 1. Overview
### Purpose
[Brief description of what this feature does]

### Scope
- In Scope: [what's included]
- Out of Scope: [what's not included]

## 2. Functional Components

### 2.1 Controllers
#### [Name]Controller
- **Purpose**: [description]
- **Actions**:
  - index(): List all records
  - view($id): Display single record
  - add(): Create new record
  - edit($id): Update existing record
  - delete($id): Remove record

### 2.2 Models
#### [Name]Table
- **Fields**:
  - id (integer, primary key)
  - name (string, required)
  - status (integer, default: 1)
  - created (datetime)
  - modified (datetime)

- **Associations**:
  - belongsTo: [Parent]
  - hasMany: [Children]

- **Validation Rules**:
  - name: notEmpty, maxLength(255)
  - email: email, unique

### 2.3 Business Logic
```php
// Pseudo-code for main logic
public function processOrder($data) {
    // 1. Validate input
    // 2. Calculate totals
    // 3. Check inventory
    // 4. Create order
    // 5. Send notifications
    // 6. Return result
}
```

## 3. Database Design

### Tables
```sql
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total DECIMAL(10,2),
    status INT DEFAULT 1,
    created DATETIME,
    modified DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 4. API Specification

### Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/orders | List orders |
| GET | /api/orders/{id} | Get order details |
| POST | /api/orders | Create order |
| PUT | /api/orders/{id} | Update order |
| DELETE | /api/orders/{id} | Delete order |

## 5. Security Considerations
- Authentication: JWT/Session
- Authorization: Role-based (Admin, User, Guest)
- Data Validation: Server-side validation for all inputs
- SQL Injection: Use ORM query builder
- XSS Prevention: Escape output in views

## 6. Performance Considerations
- Pagination for large datasets
- Eager loading for associations
- Query optimization
- Caching strategy
```

## Design Patterns

### 1. Service Layer Pattern
```php
// Service class for complex business logic
class OrderService
{
    private $Orders;
    private $Inventory;

    public function createOrder($data)
    {
        // Complex logic separated from controller
    }
}
```

### 2. Repository Pattern
```php
// Custom finder methods in Table class
class OrdersTable extends Table
{
    public function findPending(Query $query, array $options)
    {
        return $query->where(['status' => 'pending']);
    }
}
```

### 3. Event-Driven Design
```php
// Event listeners for decoupled components
EventManager::instance()->on(
    'Model.Order.afterCreate',
    function ($event, $order) {
        // Send notification
        // Update inventory
        // Log activity
    }
);
```

## Integration Patterns

### 1. Multi-Tenant Design
```php
// Company-specific data access
public function getCompanyOrders($companyId)
{
    $conn = $this->MessageDeliveryDbAccessor
        ->getUserMessageDeliveryDbConnection($companyId);

    $this->Orders->setConnection($conn);
    return $this->Orders->find()->all();
}
```

### 2. Plugin Integration
```yaml
Plugins to integrate:
  - Authentication: CakePHP/Authentication
  - Authorization: CakePHP/Authorization
  - PDF Generation: FriendsOfCake/CakePdf
  - Email: Built-in Mailer
```

### 3. Queue Processing
```php
// Async job processing
QueueManager::push(SendEmailJob::class, [
    'to' => $user->email,
    'template' => 'order_confirmation',
    'data' => $orderData
]);
```

## Output Examples

### Example 1: User Management Design
```yaml
Feature: User Management

Controllers:
  UsersController:
    - index: List users with pagination
    - add: Create user with role assignment
    - edit: Update user profile
    - delete: Soft delete with audit log

Models:
  UsersTable:
    fields: [id, email, password, role_id, status]
    associations:
      - belongsTo: Roles
      - hasMany: Orders
    validation:
      - email: unique, valid format
      - password: min 8 chars, complexity rules

Security:
  - Password hashing: bcrypt
  - Session management: 30 min timeout
  - Role-based access: Admin, Manager, User
```

### Example 2: Reporting Module Design
```yaml
Feature: Sales Reporting

Components:
  ReportGenerator:
    - generateMonthly(): Create monthly report
    - exportPdf(): Convert to PDF
    - sendEmail(): Email to stakeholders

Data Sources:
  - Orders table
  - OrderItems table
  - Products table

Performance:
  - Use database views for complex queries
  - Cache generated reports for 24 hours
  - Background job for large reports
```

## Quality Criteria

### Good Design:
- Clear separation of concerns
- Reusable components
- Scalable architecture
- Follows CakePHP conventions
- Testable code structure

### Poor Design:
- Business logic in controllers
- Direct database queries in views
- Tight coupling between components
- Ignoring framework conventions

## Best Practices

1. **Follow Conventions**: Use CakePHP naming conventions
2. **Keep Controllers Thin**: Move logic to models/services
3. **Use Behaviors**: Share functionality between models
4. **Implement Interfaces**: Define contracts for services
5. **Document Decisions**: Explain why, not just what

Remember: Good design makes implementation straightforward and maintenance easy.