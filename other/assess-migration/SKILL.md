---
name: assess-migration
description: "Investigate an existing non-Mendix application (Java, .NET, Python, Node, PHP, …) and produce a structured migration assessment for Mendix. Use when asked to analyse a legacy codebase for migration, build a migration inventory, or size the effort before any MDL is written."
---

# Migration Assessment: Investigating Non-Mendix Projects

This skill guides the investigation of existing non-Mendix applications to produce a structured migration assessment for Mendix.

## When to Use This Skill

Use this skill when:
- A user asks to analyze an existing project for migration to Mendix
- Investigating a codebase in any technology (Java, .NET, Python, Node.js, PHP, etc.)
- Producing a migration inventory or assessment report
- Planning the scope and phases of a migration project

## Investigation Process

### Step 1: Identify the Technology Stack

Determine the application's technology stack by examining:
- Build files (`pom.xml`, `*.csproj`, `package.json`, `requirements.txt`, `Gemfile`, `composer.json`)
- Configuration files (`application.properties`, `appsettings.json`, `web.config`, `.env`)
- Framework indicators (Spring Boot, ASP.NET, Django, Express, Laravel, Rails)
- Database configuration (connection strings, ORM config, migration files)
- Frontend framework (`angular.json`, `next.config.js`, Vue/React/Svelte indicators)

### Step 2: Map the Data Model

Investigate and document all entities, their attributes, and relationships.

**Where to look:**

| Technology | Data Model Location |
|------------|-------------------|
| Java/Spring | `@entity` classes, JPA annotations, Hibernate mappings |
| .NET/EF | `DbContext`, entity classes, EF migrations |
| Django | `models.py` files |
| Rails | `app/models/`, `db/schema.rb` |
| Node.js | Sequelize/TypeORM/Prisma models, Mongoose schemas |
| PHP/Laravel | Eloquent models, migrations |
| Database-first | SQL schema, stored procedures, views |

**Output format:**

```markdown
### data model

#### entities

| entity | attributes | type | Constraints | Mendix mapping |
|--------|-----------|------|-------------|----------------|
| Customer | id | long (auto) | PK | (auto-generated) |
| | name | string(200) | not null | string(200) |
| | email | string(200) | unique | string(200) |
| | creditLimit | decimal(10,2) | | decimal |
| | isActive | boolean | default true | boolean |
| | createdAt | datetime | | datetime |
| Order | id | long (auto) | PK | (auto-generated) |
| | orderNumber | string(50) | unique, not null | string(50) |
| | status | enum | | enumeration |
| | totalAmount | decimal | | decimal |

#### associations

| from | to | type | Mendix mapping |
|------|----|------|----------------|
| Order | Customer | Many-to-One | reference (Order → Customer) |
| Order | OrderLine | One-to-Many | reference (OrderLine → Order) |
| user | role | Many-to-Many | ReferenceSet |

#### enumerations

| Name | values | Used by |
|------|--------|---------|
| OrderStatus | PENDING, PROCESSING, COMPLETED, CANCELLED | Order.status |
| UserRole | ADMIN, MANAGER, user | User.role |
```

### Step 3: Catalog Business Logic and Rules

This is the most critical part. Identify and explicitly document all business logic, validation rules, calculations, and workflows.

**Where to look:**

| Technology | Logic Location |
|------------|---------------|
| Java/Spring | `@service` classes, `@Component`, `@Transactional` methods |
| .NET | Service classes, domain logic, middleware |
| Django | Views, forms, signals, managers |
| Rails | Models (callbacks, validations), services, concerns |
| Node.js | Route handlers, middleware, service modules |
| Database | Stored procedures, triggers, functions, constraints |

**Categorize each piece of logic:**

```markdown
### business Logic

#### validation rules

| rule | Location | description | Mendix mapping |
|------|----------|-------------|----------------|
| VR-001 | CustomerService.validate() | Customer name is required, max 200 chars | validation microflow |
| VR-002 | OrderService.validate() | Order date cannot be in the past | validation microflow |
| VR-003 | DB trigger: trg_check_credit | Credit limit cannot exceed $1M for non-premium | validation microflow + before commit |
| VR-004 | OrderLine model | Quantity must be > 0 | attribute validation |

#### business rules

| rule | Location | description | Mendix mapping |
|------|----------|-------------|----------------|
| BR-001 | OrderService.calculateTotal() | sum of line items * quantity, apply tax | microflow |
| BR-002 | DiscountService.applyDiscount() | 10% for orders > $1000, 15% for premium | microflow |
| BR-003 | CustomerService.updateStatus() | Deactivate customer after 12 months inactive | Scheduled microflow |
| BR-004 | DB proc: sp_close_month | Monthly closing with balance calculations | microflow + scheduled event |

#### workflows / multi-Step Processes

| workflow | Steps | description | Mendix mapping |
|----------|-------|-------------|----------------|
| Order Approval | Submit → Review → Approve/Reject → notify | Orders > $5000 need manager approval | workflow or microflow chain |
| user Onboarding | Register → Verify Email → Complete Profile → Activate | New user registration flow | microflow chain + pages |

#### calculated Fields / Derived data

| Field | Calculation | Location | Mendix mapping |
|-------|-------------|----------|----------------|
| Order.totalAmount | sum(lines.price * lines.qty) | OrderService | calculated attribute or microflow |
| Customer.orderCount | count(orders) | sql view | microflow or calculated attribute |
| Invoice.dueDate | invoiceDate + paymentTerms | InvoiceService | microflow |
```

### Step 4: Inventory Pages and UI

Document all screens, their purpose, and the data they display or edit.

**Where to look:**

| Technology | UI Location |
|------------|-------------|
| Java/Spring MVC | JSP/Thymeleaf templates, controllers |
| .NET MVC/Razor | Views, Razor pages, controllers |
| React/Angular/Vue | Component files, route definitions |
| Django | Templates, URL conf |
| Rails | Views, routes |
| Mobile | Activities/Fragments (Android), ViewControllers (iOS) |

**Output format:**

```markdown
### pages / Screens

| page | type | data | key actions | Mendix mapping |
|------|------|------|-------------|----------------|
| Customer list | overview | Customer (filtered, paged) | search, New, Edit, delete | overview page + datagrid |
| Customer Edit | Form | Customer + Addresses | Save, cancel, Validate | Edit page + dataview |
| Order Dashboard | Dashboard | Orders (grouped by status) | filter, Drill-down | page + multiple DataGrids |
| Order Entry | multi-step form | Order + OrderLines | add line, Calculate, Submit | page + listview + microflows |
| Reports | read-only | Aggregated data | export, Print | page + charts or custom widgets |
| login | authentication | Credentials | login, Forgot password | login page (built-in) |
```

### Step 5: Map Integrations

Document all external system connections, APIs consumed, and APIs exposed.

**Where to look:**
- REST/SOAP client configurations
- HTTP client usage, API base URLs
- Message queue consumers/producers (Kafka, RabbitMQ, SQS)
- File import/export (CSV, Excel, XML, JSON)
- Email sending configuration
- External authentication (OAuth, SAML, LDAP)
- Third-party SDK usage (payment, notification, storage)

**Output format:**

```markdown
### Integrations

#### APIs consumed (Outbound)

| Integration | Protocol | Endpoint | auth | Mendix mapping |
|-------------|----------|----------|------|----------------|
| Payment Gateway | rest | api.stripe.com | api key | rest client (consumed) |
| Email service | rest | api.sendgrid.com | api key | Email module or rest |
| ERP Sync | SOAP | erp.company.com/ws | Certificate | Web service call |
| file storage | SDK | AWS S3 | IAM | FileDocument + custom java |

#### APIs exposed (Inbound)

| Endpoint | method | Purpose | Mendix mapping |
|----------|--------|---------|----------------|
| /api/customers | get, post | Customer CRUD | published rest service |
| /api/orders/{id} | get, put | Order management | published rest service |
| /webhooks/payment | post | Payment notifications | published rest service |

#### data Feeds

| Feed | format | Direction | Frequency | Mendix mapping |
|------|--------|-----------|-----------|----------------|
| Customer export | CSV | Outbound | Daily | Scheduled microflow + export mapping |
| Product catalog | xml | Inbound | Hourly | Scheduled microflow + import mapping |
| Financial data | odata | both | Real-time | external entities (odata) |

#### message Queues / events

| Queue/Topic | Direction | Purpose | Mendix mapping |
|-------------|-----------|---------|----------------|
| order-events | publish | Order status changes | business events |
| inventory-updates | subscribe | Stock level changes | business events |
```

### Step 6: Document Security Model

Investigate how authentication, authorization, user roles, and data access control are implemented.

**Where to look:**

| Technology | Security Location |
|------------|-------------------|
| Java/Spring | Spring Security config, `@PreAuthorize`, `@Secured`, `@RolesAllowed` |
| .NET | `[Authorize]`, Identity config, policies, claims |
| Django | `@login_required`, permissions, groups |
| Rails | Devise, CanCanCan/Pundit policies |
| Node.js | Passport.js, JWT middleware, RBAC libraries |
| Database | GRANT statements, row-level security |

**Output format:**

```markdown
### security

#### authentication

| method | Details | Mendix mapping |
|--------|---------|----------------|
| username/password | local DB with bcrypt | Built-in authentication |
| oauth 2.0 | Google, Microsoft SSO | OIDC SSO module |
| SAML | Corporate IdP | SAML module |
| api Keys | for service accounts | Custom implementation |

#### user roles

| role | description | Rough Privileges | Mendix mapping |
|------|-------------|------------------|----------------|
| Admin | full system access | all CRUD, user management, settings | Administrator role |
| Manager | Department-level access | Approve orders, view reports, manage team | Custom module role |
| user | Standard operations | create/edit own records, view assigned | Custom module role |
| Viewer | read-only access | view only, no modifications | Custom module role |
| api service | Machine-to-machine | Specific api endpoints only | Custom module role |

#### data access rules

| entity | role | create | read | write | delete | constraint |
|--------|------|--------|------|-------|--------|------------|
| Customer | Admin | Yes | all | all | Yes | none |
| Customer | Manager | Yes | Department | Department | No | Department = User.Department |
| Customer | user | No | Own | Own | No | CreatedBy = CurrentUser |
| Order | Manager | Yes | Department | Department | No | status != 'Closed' |

#### row-level security / data Filtering

| rule | description | Mendix mapping |
|------|-------------|----------------|
| Department isolation | users only see their department's data | XPath constraint on entity access |
| Record ownership | users only edit records they created | xpath: `[CreatedBy = '[%CurrentUser%]']` |
| status-based locking | Closed records are read-only | xpath on write: `[status != 'Closed']` |
```

## Assessment Report Template

Combine all findings into a structured report:

```markdown
# Migration Assessment: [Application Name]

## Executive Summary
- **Application**: [Name and brief description]
- **Technology stack**: [languages, frameworks, databases]
- **Size**: [entities, services/controllers, pages, integrations]
- **Complexity**: [Low / Medium / High]
- **Recommended approach**: [Big bang / Phased / Strangler fig]

## Inventory Summary

| Category | count | Complexity | Notes |
|----------|-------|------------|-------|
| entities | X | | |
| associations | X | | |
| enumerations | X | | |
| business rules | X | | list the critical ones |
| validation rules | X | | |
| pages/Screens | X | | |
| Integrations | X | | list external systems |
| user roles | X | | |
| Scheduled jobs | X | | |

## data model
[from Step 2]

## business Logic and rules
[from Step 3 — this is the most important section]

## pages and UI
[from Step 4]

## Integrations
[from Step 5]

## security
[from Step 6]

## Migration Risks

| Risk | impact | Mitigation |
|------|--------|------------|
| Complex stored procedures | Logic may not map 1:1 to microflows | Review and simplify, consider java actions |
| Custom UI components | No direct Mendix equivalent | Evaluate pluggable widgets or custom widgets |
| Real-time integrations | Mendix has different async patterns | Consider business events or polling |
| row-level security complexity | Mendix xpath constraints have limits | Simplify access rules where possible |

## Recommended Migration Phases

1. **Domain model** — entities, associations, enumerations
2. **Core business logic** — validation rules, business rules, calculations
3. **pages** — overview pages, edit forms, dashboards
4. **Integrations** — rest clients, file handling, external systems
5. **security** — roles, access rules, authentication
6. **Testing & cutover** — data migration, parallel running, go-live
```

## Tips

- **Be thorough with business logic**: This is where migrations fail. A missing validation rule or calculation creates bugs that are hard to trace back to the source.
- **Check the database**: Stored procedures, triggers, views, and constraints often contain business logic that isn't visible in application code.
- **Look for implicit rules**: Framework conventions (e.g., Rails validations, Spring annotations) encode rules that are easy to miss.
- **Document what you DON'T migrate**: Some features may not need to be migrated (legacy reports, dead code, deprecated features). Call these out explicitly.
- **Ask about undocumented behavior**: Users often know about special cases and workarounds that aren't in the code.

## Related Skills

- [/migrate-oracle-forms](../migrate-oracle-forms/SKILL.md) - Oracle Forms-specific migration
- [/generate-domain-model](../generate-domain-model/SKILL.md) - Creating entities and associations in MDL
- [/write-microflows](../write-microflows/SKILL.md) - Implementing business logic in MDL
- [/organize-project](../organize-project/SKILL.md) - Folder structure for the migrated project
