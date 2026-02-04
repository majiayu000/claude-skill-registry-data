---
name: backend-design
description: Design robust, scalable backend architectures that complement Design OS frontend components. Use this skill when planning APIs, database schemas, and server-side logic for products designed in Design OS.
---

This skill guides creation of backend architectures that properly support props-based frontend components from Design OS. The goal is to create APIs and data layers that match exactly what the UI expects.

## Backend Design Principles

### 1. API-First Thinking

Design APIs before implementation:
- Each component callback prop = one API endpoint
- Props interface = response shape
- Form submissions = request body shape

### 2. Match Frontend Contracts

The UI is already designed. Your API must match:

```typescript
// Frontend expects:
interface InvoiceListProps {
  invoices: Invoice[]
  onView: (id: string) => void
  onEdit: (id: string) => void
  onDelete: (id: string) => void
  onCreate: () => void
}

// Backend provides:
GET /api/invoices → Invoice[]
GET /api/invoices/:id → Invoice
PUT /api/invoices/:id → Invoice
DELETE /api/invoices/:id → void
POST /api/invoices → Invoice
```

### 3. Database Schema from Types

Convert TypeScript interfaces to database tables:

```typescript
// Frontend type:
interface Invoice {
  id: string
  clientId: string
  lineItems: LineItem[]
  status: 'draft' | 'sent' | 'paid'
  total: number
  createdAt: string
}

// Database schema:
CREATE TABLE invoices (
  id UUID PRIMARY KEY,
  client_id UUID REFERENCES clients(id),
  status VARCHAR(20) CHECK (status IN ('draft', 'sent', 'paid')),
  total DECIMAL(10,2),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE line_items (
  id UUID PRIMARY KEY,
  invoice_id UUID REFERENCES invoices(id),
  description TEXT,
  quantity INTEGER,
  unit_price DECIMAL(10,2)
);
```

### 4. Business Logic Layer

Identify logic that lives on the server:

**Calculations:**
- Invoice totals (don't trust client-side math)
- Tax calculations
- Aggregations and reports

**Validations:**
- Required fields
- Business rules (can't delete sent invoice)
- Authorization checks

**Workflows:**
- Status transitions
- Notifications
- Scheduled tasks

### 5. Error Handling

Design consistent error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invoice cannot be deleted after being sent",
    "field": "status"
  }
}
```

Match error states to frontend empty/error states.

## Architecture Patterns

### Simple (Monolith)
Best for MVPs and small teams:
- Single codebase
- Direct database access
- Session-based auth

### Modular Monolith
Best for growing products:
- Feature modules within single codebase
- Shared database with clear boundaries
- Easier to split later

### Service-Oriented
Best for large teams:
- Separate services per domain
- API gateway
- Independent scaling

## Technology Selection Guide

**Node.js/Express/Fastify:**
- Matches frontend JS skills
- Large ecosystem
- Good for real-time features

**Python/FastAPI:**
- Clean API definition
- Async by default
- Good for data-heavy apps

**Go:**
- High performance
- Simple deployment
- Good for microservices

**Ruby on Rails/Laravel:**
- Rapid development
- Batteries included
- Good for CRUD apps

## Testing Strategy

Match frontend test requirements:

1. **Unit tests** — Business logic, calculations
2. **Integration tests** — API endpoint behavior
3. **Contract tests** — Ensure API matches frontend expectations
4. **E2E tests** — Full user flows (frontend + backend)

## Checklist Before Implementation

- [ ] Every component callback has a corresponding API endpoint
- [ ] Response shapes match TypeScript interfaces exactly
- [ ] Error responses match frontend error handling
- [ ] Empty states return empty arrays, not errors
- [ ] Auth/permissions designed for all endpoints
- [ ] Database schema supports all entity relationships
- [ ] Business validation rules documented
- [ ] API versioning strategy decided
