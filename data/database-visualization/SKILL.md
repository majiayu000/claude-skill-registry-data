---
name: database-visualization
description: Expert in creating database diagrams and visual representations. Use when generating ERDs, schema diagrams, or visualizing database relationships with Mermaid.js.
allowed-tools: Read, Grep, Bash
---

# Database Visualization Skill

Expert knowledge for creating entity-relationship diagrams (ERDs) and visual representations of database schemas using Mermaid.js.

## Mermaid.js ERD Syntax

Mermaid.js is a text-based diagramming tool that renders beautiful diagrams from markdown-like syntax.

### Basic ERD Structure

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains

    CUSTOMER {
        int customer_id PK
        string name
        string email UK
    }

    ORDER {
        int order_id PK
        int customer_id FK
        date order_date
    }
```

### Relationship Cardinality

Mermaid uses special notation for relationship cardinality:

| Cardinality | Left | Right | Syntax | Example |
|-------------|------|-------|--------|---------|
| Zero or one | `|o` | `o|` | `\|o--o\|` | Optional one-to-one |
| Exactly one | `||` | `||` | `\|\|--\|\|` | Required one-to-one |
| Zero or more | `}o` | `o{` | `}o--o{` | Many-to-many |
| One or more | `}|` | `|{` | `}\|--\|{` | One to many (required) |

**Common Patterns:**

```mermaid
erDiagram
    %% One-to-many (most common)
    PARENT ||--o{ CHILD : has

    %% Many-to-many (via junction table)
    STUDENT }o--o{ COURSE : enrolls
    STUDENT ||--o{ ENROLLMENT : has
    COURSE ||--o{ ENROLLMENT : includes

    %% One-to-one
    USER ||--|| USER_PROFILE : has

    %% Optional relationships
    ORDER ||--o| SHIPMENT : "may have"
```

### Entity Attributes

Define entity attributes with:
- Column name
- Data type
- Constraints (PK, FK, UK)
- Optional description

```mermaid
erDiagram
    USERS {
        int UserId PK "Auto-increment primary key"
        nvarchar50 Username UK "Unique username"
        nvarchar255 Email UK "Unique email"
        nvarchar255 PasswordHash "Hashed password"
        datetime2 CreatedAt "Account creation timestamp"
        bit IsActive "Account status flag"
    }
```

### Relationship Labels

Add meaningful labels to relationships:

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : "places"
    ORDER ||--|{ ORDER_ITEM : "contains"
    PRODUCT ||--o{ ORDER_ITEM : "included in"
    CATEGORY ||--o{ PRODUCT : "categorizes"
```

## SQL Server to Mermaid Mapping

### Data Type Mapping

| SQL Server Type | Mermaid Notation | Example |
|----------------|------------------|---------|
| `INT` | `int` | `UserId int PK` |
| `BIGINT` | `bigint` | `OrderId bigint PK` |
| `NVARCHAR(n)` | `nvarchar{n}` | `Username nvarchar50 UK` |
| `NVARCHAR(MAX)` | `nvarcharMAX` | `Content nvarcharMAX` |
| `VARCHAR(n)` | `varchar{n}` | `Code varchar20` |
| `DECIMAL(p,s)` | `decimal{p_s}` | `Price decimal10_2` |
| `DATETIME2` | `datetime2` | `CreatedAt datetime2` |
| `DATE` | `date` | `BirthDate date` |
| `TIME` | `time` | `OpenTime time` |
| `BIT` | `bit` | `IsActive bit` |
| `UNIQUEIDENTIFIER` | `guid` | `RowGuid guid PK` |

### Constraint Notation

- `PK` - Primary Key
- `FK` - Foreign Key
- `UK` - Unique Key
- `PK_FK` - Composite primary key + foreign key (junction tables)

## Complete Examples

### E-Commerce Schema

```mermaid
erDiagram
    CUSTOMERS ||--o{ ORDERS : places
    ORDERS ||--|{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : "ordered in"
    CATEGORIES ||--o{ PRODUCTS : categorizes
    CUSTOMERS ||--o{ ADDRESSES : has
    ORDERS ||--o| SHIPMENTS : "shipped via"

    CUSTOMERS {
        int CustomerId PK
        nvarchar100 CustomerName
        nvarchar255 Email UK
        nvarchar20 Phone
        datetime2 CreatedAt
        bit IsActive
    }

    ADDRESSES {
        int AddressId PK
        int CustomerId FK
        nvarchar200 Street
        nvarchar100 City
        nvarchar50 State
        nvarchar20 ZipCode
        nvarchar50 Country
    }

    ORDERS {
        int OrderId PK
        int CustomerId FK
        datetime2 OrderDate
        decimal10_2 TotalAmount
        nvarchar20 Status
    }

    ORDER_ITEMS {
        int OrderItemId PK
        int OrderId FK
        int ProductId FK
        int Quantity
        decimal10_2 UnitPrice
        decimal10_2 Subtotal
    }

    PRODUCTS {
        int ProductId PK
        int CategoryId FK
        nvarchar200 ProductName
        nvarcharMAX Description
        decimal10_2 Price
        int Stock
        bit IsActive
    }

    CATEGORIES {
        int CategoryId PK
        nvarchar100 CategoryName UK
        nvarchar500 Description
    }

    SHIPMENTS {
        int ShipmentId PK
        int OrderId FK UK
        nvarchar100 Carrier
        nvarchar50 TrackingNumber
        datetime2 ShippedDate
        datetime2 DeliveredDate
    }
```

### Blog Platform Schema

```mermaid
erDiagram
    USERS ||--o{ POSTS : writes
    USERS ||--o{ COMMENTS : writes
    POSTS ||--o{ COMMENTS : has
    CATEGORIES ||--o{ POSTS : contains
    POSTS }o--o{ TAGS : tagged
    POSTS ||--o{ POST_TAGS : has
    TAGS ||--o{ POST_TAGS : applied_to

    USERS {
        int UserId PK
        nvarchar50 Username UK
        nvarchar255 Email UK
        nvarchar255 PasswordHash
        nvarchar200 DisplayName
        nvarcharMAX Bio
        datetime2 CreatedAt
        datetime2 LastLoginAt
        bit IsActive
    }

    POSTS {
        int PostId PK
        int UserId FK
        int CategoryId FK
        nvarchar200 Title
        nvarchar500 Slug UK
        nvarcharMAX Content
        nvarcharMAX Excerpt
        datetime2 PublishedAt
        datetime2 UpdatedAt
        int ViewCount
        nvarchar20 Status
    }

    COMMENTS {
        int CommentId PK
        int PostId FK
        int UserId FK
        int ParentCommentId FK
        nvarcharMAX Content
        datetime2 CreatedAt
        bit IsApproved
    }

    CATEGORIES {
        int CategoryId PK
        nvarchar100 CategoryName UK
        nvarchar200 Slug UK
        nvarchar500 Description
    }

    TAGS {
        int TagId PK
        nvarchar50 TagName UK
        nvarchar100 Slug UK
    }

    POST_TAGS {
        int PostId PK_FK
        int TagId PK_FK
    }
```

### Many-to-Many with Attributes (Enrollment System)

```mermaid
erDiagram
    STUDENTS ||--o{ ENROLLMENTS : enrolls
    COURSES ||--o{ ENROLLMENTS : has
    INSTRUCTORS ||--o{ COURSES : teaches

    STUDENTS {
        int StudentId PK
        nvarchar100 FirstName
        nvarchar100 LastName
        nvarchar255 Email UK
        date DateOfBirth
        datetime2 EnrolledDate
    }

    COURSES {
        int CourseId PK
        int InstructorId FK
        nvarchar100 CourseName
        nvarchar20 CourseCode UK
        int Credits
        decimal10_2 Price
    }

    ENROLLMENTS {
        int EnrollmentId PK
        int StudentId FK
        int CourseId FK
        datetime2 EnrollmentDate
        char2 Grade
        decimal5_2 Score
        nvarchar20 Status
    }

    INSTRUCTORS {
        int InstructorId PK
        nvarchar100 FirstName
        nvarchar100 LastName
        nvarchar255 Email UK
        nvarchar100 Department
    }
```

## Best Practices

### 1. Consistent Entity Naming

Choose either singular or plural and stick with it:
- ✅ Plural: `USERS`, `ORDERS`, `PRODUCTS`
- ✅ Singular: `USER`, `ORDER`, `PRODUCT`
- ❌ Mixed: `USER`, `ORDERS`, `PRODUCT`

### 2. Clear Relationship Labels

Use verb phrases that read naturally:
```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : "places"
    %% Reads as: "Customer places Order"

    ORDER ||--|{ ORDER_ITEM : "contains"
    %% Reads as: "Order contains Order Items"
```

### 3. Show Important Attributes

Include enough detail to understand the schema, but don't overcrowd:
- ✅ Primary keys, foreign keys, unique constraints
- ✅ Key business attributes
- ✅ Important data types
- ❌ Every single column (too cluttered)

### 4. Group Related Entities

Organize entities logically in the diagram:
```mermaid
erDiagram
    %% User-related entities
    USERS ||--|| USER_PROFILES : has
    USERS ||--o{ ADDRESSES : has

    %% Order-related entities
    ORDERS ||--|{ ORDER_ITEMS : contains
    ORDERS ||--o| SHIPMENTS : "shipped via"
```

### 5. Use Composite Keys Appropriately

For junction tables in many-to-many relationships:
```mermaid
erDiagram
    POST_TAGS {
        int PostId PK_FK
        int TagId PK_FK
        datetime2 TaggedAt
    }
```

## Rendering Mermaid Diagrams

### In Markdown Files

````markdown
```mermaid
erDiagram
    USERS ||--o{ POSTS : writes
    ...
```
````

### In GitHub

GitHub automatically renders Mermaid diagrams in:
- README.md files
- Issue descriptions
- Pull request descriptions
- Wiki pages

### In VS Code

Install the "Markdown Preview Mermaid Support" extension to see live previews.

### Online Editors

- [Mermaid Live Editor](https://mermaid.live/)
- [Mermaid Chart](https://www.mermaidchart.com/)

## Common Patterns

### Self-Referencing Relationships

```mermaid
erDiagram
    EMPLOYEES ||--o{ EMPLOYEES : "manages"
    CATEGORIES ||--o{ CATEGORIES : "parent of"

    EMPLOYEES {
        int EmployeeId PK
        nvarchar100 Name
        int ManagerId FK "References EmployeeId"
    }
```

### Inheritance/Subtype Pattern

```mermaid
erDiagram
    MEDIA ||--o{ POSTS : "is a"
    MEDIA ||--o{ PHOTOS : "is a"

    MEDIA {
        int MediaId PK
        nvarchar20 MediaType "Post or Photo"
        datetime2 CreatedAt
    }

    POSTS {
        int MediaId PK_FK
        nvarchar200 Title
        nvarcharMAX Content
    }

    PHOTOS {
        int MediaId PK_FK
        nvarchar500 Url
        nvarchar200 Caption
    }
```

### Audit Columns Pattern

Show audit columns when relevant:
```mermaid
erDiagram
    PRODUCTS {
        int ProductId PK
        nvarchar200 ProductName
        decimal10_2 Price
        datetime2 CreatedAt
        int CreatedBy FK
        datetime2 UpdatedAt
        int UpdatedBy FK
        bit IsDeleted
    }
```

## When to Use This Skill

Use this skill when:
- Designing new database schemas
- Documenting existing databases
- Creating technical documentation
- Explaining database structure to team members
- Planning schema migrations
- Reverse-engineering databases
- Teaching database design concepts

Simply mention "ERD", "diagram", "visualize schema", or "Mermaid" and this knowledge will be applied to create clear, professional database visualizations.
