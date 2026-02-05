---
name: vaultcpa-coding-standards
description: VaultCPA project coding standards, conventions, and best practices for Next.js, React, TypeScript, Express, and Prisma. Use when reviewing code, writing new features, or setting up development patterns.
allowed-tools: Read, Grep, Glob
---

# VaultCPA Coding Standards

**Version:** 2.0
**Last Updated:** January 2026

This Skill defines the coding standards, architectural patterns, and best practices for the VaultCPA tax and accounting platform.

## Table of Contents

1. [Multi-Tenant Architecture (CRITICAL)](#multi-tenant-architecture-critical)
2. [Frontend Standards (Next.js/React/TypeScript)](#frontend-standards)
3. [Backend Standards (Express/Prisma)](#backend-standards)
4. [Database Patterns](#database-patterns)
5. [Security Requirements](#security-requirements)
6. [Testing Standards](#testing-standards)
7. [Code Review Checklist](#code-review-checklist)

---

## Multi-Tenant Architecture (CRITICAL)

### ⚠️ Golden Rule: EVERY Query Must Filter by organizationId

**This is the most critical security requirement in VaultCPA.**

Data leakage between organizations is a catastrophic failure. Every database query MUST include organizationId filtering.

### ✅ Correct Patterns

```javascript
// Backend - Prisma queries
const clients = await prisma.client.findMany({
  where: {
    organizationId: req.user.organizationId  // ← REQUIRED
  }
});

// With additional filters
const activeClients = await prisma.client.findMany({
  where: {
    organizationId: req.user.organizationId,  // ← ALWAYS FIRST
    status: 'ACTIVE'
  }
});

// Related data queries
const alerts = await prisma.alert.findMany({
  where: {
    organizationId: req.user.organizationId,
    clientId: clientId  // Already scoped to org
  }
});

// Count queries
const totalClients = await prisma.client.count({
  where: {
    organizationId: req.user.organizationId
  }
});
```

### ❌ WRONG - Data Leakage

```javascript
// NEVER DO THIS - Exposes all organizations' data
const clients = await prisma.client.findMany();

// WRONG - Missing organizationId in where clause
const clients = await prisma.client.findMany({
  where: { status: 'ACTIVE' }
});

// WRONG - Only filtering at service layer
// Must filter at database query level
const allClients = await prisma.client.findMany();
return allClients.filter(c => c.organizationId === orgId);
```

### Middleware Pattern

```javascript
// All protected routes use authMiddleware
router.get('/api/clients', authMiddleware, async (req, res) => {
  // req.user.organizationId is guaranteed to exist
  const clients = await prisma.client.findMany({
    where: { organizationId: req.user.organizationId }
  });
  res.json({ success: true, data: clients });
});
```

### Code Review Requirement

**Every PR touching database queries must:**
1. Verify organizationId filter is present
2. Test with multiple organizations to confirm isolation
3. Add a comment in review confirming multi-tenant isolation

---

## Frontend Standards

### Project Structure

```
app/
├── (app)/                    # Main app routes (layout wrapper)
├── (auth)/                   # Authentication routes
├── dashboard/                # Role-based dashboards
│   ├── managing-partner/     # Executive dashboard
│   ├── tax-manager/          # Tax management
│   ├── staff-accountant/     # Staff work dashboard
│   └── system-admin/         # Admin dashboard
└── api/                      # API routes/proxies

components/
├── auth/                     # Authentication components
├── charts/                   # Data visualization
├── home/                     # Dashboard cards
├── layout/                   # Layout components
├── navbar/                   # Navigation
└── sidebar/                  # Sidebar navigation
```

### Next.js App Router Patterns

#### Server vs Client Components

```typescript
// Default to Server Components (no 'use client')
// app/dashboard/page.tsx
export default async function Dashboard() {
  const data = await fetchData(); // Can fetch directly
  return <DashboardLayout data={data} />;
}

// Use 'use client' only when needed
// components/InteractiveChart.tsx
'use client';
import { useState } from 'react';

export default function InteractiveChart() {
  const [filter, setFilter] = useState('all');
  // Client-side interactivity
}
```

**Use Client Components when you need:**
- useState, useEffect, or other React hooks
- Event handlers (onClick, onChange)
- Browser APIs (localStorage, window)
- Third-party libraries that require client-side rendering

#### Dynamic Routes

```typescript
// app/dashboard/clients/[id]/page.tsx
interface PageProps {
  params: { id: string };
  searchParams?: { [key: string]: string | string[] | undefined };
}

export default async function ClientDetailPage({ params }: PageProps) {
  const clientId = params.id;
  // Fetch and render client data
}
```

### TypeScript Standards

#### No `any` Types

```typescript
// ❌ WRONG
function processData(data: any) {
  return data.value;
}

// ✅ Correct - Use specific types
interface ClientData {
  id: string;
  name: string;
  revenue: number;
}

function processData(data: ClientData) {
  return data.revenue;
}

// ✅ Correct - Use generics for flexibility
function processData<T extends { value: number }>(data: T) {
  return data.value;
}

// ✅ Correct - Use unknown when type is truly unknown
function processData(data: unknown) {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    return (data as { value: number }).value;
  }
  throw new Error('Invalid data structure');
}
```

#### Interface Naming

```typescript
// Props interfaces - suffix with Props
interface AlertCardProps {
  alert: NexusAlert;
  onDismiss: () => void;
}

// Data models - no suffix
interface Client {
  id: string;
  name: string;
  organizationId: string;
}

// API responses - suffix with Response
interface AlertsResponse {
  success: boolean;
  data: NexusAlert[];
  pagination?: PaginationInfo;
}
```

### React Component Standards

#### Component Structure

```typescript
'use client';
import { useState, useEffect } from 'react';
import { Card, Button } from '@nextui-org/react';

// 1. Interfaces at top
interface ClientListProps {
  initialClients: Client[];
  organizationId: string;
}

// 2. Component function
export default function ClientList({ initialClients, organizationId }: ClientListProps) {
  // 3. State declarations
  const [clients, setClients] = useState(initialClients);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 4. Effects
  useEffect(() => {
    // Effect logic
  }, [/* dependencies */]);

  // 5. Event handlers
  const handleRefresh = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/clients');
      const data = await response.json();
      setClients(data.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  // 6. Render helpers (if needed)
  const renderClient = (client: Client) => (
    <Card key={client.id}>
      <h3>{client.name}</h3>
    </Card>
  );

  // 7. Early returns for loading/error states
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  // 8. Main render
  return (
    <div>
      {clients.map(renderClient)}
    </div>
  );
}
```

#### Event Handler Naming

```typescript
// Use handle* for event handlers
const handleClick = () => {};
const handleSubmit = () => {};
const handleChange = (value: string) => {};

// Use on* for props
interface ButtonProps {
  onClick: () => void;
  onSubmit: (data: FormData) => void;
}
```

### NextUI Component Usage

```typescript
import {
  Card,
  CardBody,
  CardHeader,
  Button,
  Input,
  Select,
  SelectItem,
  Modal,
  ModalContent
} from '@nextui-org/react';

// Use NextUI components consistently
<Card className="bg-white/5 border border-white/10">
  <CardBody>
    <Button color="primary" variant="flat">
      Action
    </Button>
  </CardBody>
</Card>
```

### Tailwind CSS Standards

```typescript
// Use Tailwind utility classes
<div className="flex items-center justify-between p-4 bg-gray-800 rounded-lg">

// Group related utilities
<div className="
  flex items-center gap-4        // Layout
  p-6 rounded-lg                 // Spacing & shape
  bg-white/5 border border-white/10  // Colors
  hover:bg-white/10 transition-colors // Interactions
">

// Use clsx for conditional classes
import clsx from 'clsx';

<div className={clsx(
  'px-4 py-2 rounded',
  isActive ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700',
  isDisabled && 'opacity-50 cursor-not-allowed'
)}>
```

### Form Handling with Formik

```typescript
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';

const validationSchema = Yup.object({
  name: Yup.string().required('Name is required'),
  email: Yup.string().email('Invalid email').required('Email is required')
});

export default function ClientForm() {
  return (
    <Formik
      initialValues={{ name: '', email: '' }}
      validationSchema={validationSchema}
      onSubmit={async (values, { setSubmitting }) => {
        try {
          await saveClient(values);
        } finally {
          setSubmitting(false);
        }
      }}
    >
      {({ errors, touched, isSubmitting }) => (
        <Form>
          <Field name="name" as={Input} />
          {errors.name && touched.name && <span>{errors.name}</span>}

          <Button type="submit" isLoading={isSubmitting}>
            Save
          </Button>
        </Form>
      )}
    </Formik>
  );
}
```

---

## Backend Standards

### Express Route Structure

```javascript
// Standard route pattern
const express = require('express');
const router = express.Router();
const { authMiddleware } = require('../middleware/auth');
const { validate } = require('../middleware/validation');
const clientController = require('../controllers/clientController');

// GET list (with pagination)
router.get(
  '/api/clients',
  authMiddleware,
  clientController.list
);

// POST create
router.post(
  '/api/clients',
  authMiddleware,
  validate(clientSchema),
  clientController.create
);

// GET by ID
router.get(
  '/api/clients/:id',
  authMiddleware,
  clientController.getById
);

// PUT update
router.put(
  '/api/clients/:id',
  authMiddleware,
  validate(clientUpdateSchema),
  clientController.update
);

// DELETE
router.delete(
  '/api/clients/:id',
  authMiddleware,
  clientController.delete
);

module.exports = router;
```

### Controller Pattern

```javascript
// controllers/clientController.js
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

const clientController = {
  async list(req, res, next) {
    try {
      const { organizationId } = req.user;
      const { page = 1, limit = 20, status } = req.query;

      const where = { organizationId };
      if (status) where.status = status;

      const clients = await prisma.client.findMany({
        where,
        skip: (page - 1) * limit,
        take: parseInt(limit),
        orderBy: { createdAt: 'desc' }
      });

      const total = await prisma.client.count({ where });

      res.json({
        success: true,
        data: clients,
        pagination: {
          page: parseInt(page),
          limit: parseInt(limit),
          total,
          pages: Math.ceil(total / limit)
        }
      });
    } catch (error) {
      next(error);
    }
  },

  async create(req, res, next) {
    try {
      const { organizationId } = req.user;
      const data = {
        ...req.body,
        organizationId,
        createdById: req.user.id
      };

      const client = await prisma.client.create({ data });

      res.status(201).json({
        success: true,
        data: client
      });
    } catch (error) {
      next(error);
    }
  },

  async getById(req, res, next) {
    try {
      const { organizationId } = req.user;
      const { id } = req.params;

      const client = await prisma.client.findFirst({
        where: {
          id,
          organizationId  // Critical: prevent cross-org access
        }
      });

      if (!client) {
        return res.status(404).json({
          success: false,
          error: 'Client not found'
        });
      }

      res.json({
        success: true,
        data: client
      });
    } catch (error) {
      next(error);
    }
  }
};

module.exports = clientController;
```

### API Response Format

```javascript
// Success response
{
  success: true,
  data: { /* resource or array */ }
}

// Success with pagination
{
  success: true,
  data: [/* resources */],
  pagination: {
    page: 1,
    limit: 20,
    total: 150,
    pages: 8
  }
}

// Error response
{
  success: false,
  error: "Descriptive error message"
}

// Validation error response
{
  success: false,
  error: "Validation failed",
  details: [
    { field: "email", message: "Invalid email format" },
    { field: "name", message: "Name is required" }
  ]
}
```

### Input Validation (Joi)

```javascript
const Joi = require('joi');

const clientSchema = Joi.object({
  name: Joi.string().required().min(2).max(100),
  email: Joi.string().email().required(),
  phone: Joi.string().optional().pattern(/^\d{10}$/),
  riskLevel: Joi.string().valid('LOW', 'MEDIUM', 'HIGH', 'CRITICAL').required(),
  metadata: Joi.object().optional()
});

// In routes
const { validate } = require('../middleware/validation');
router.post('/api/clients', authMiddleware, validate(clientSchema), controller.create);
```

### Error Handling

```javascript
// Custom error class
class ApiError extends Error {
  constructor(message, statusCode = 500) {
    super(message);
    this.statusCode = statusCode;
    this.name = 'ApiError';
  }
}

// Error handler middleware (last middleware)
app.use((err, req, res, next) => {
  console.error('[ERROR]', err);

  if (err instanceof ApiError) {
    return res.status(err.statusCode).json({
      success: false,
      error: err.message
    });
  }

  // Prisma errors
  if (err.code === 'P2002') {
    return res.status(409).json({
      success: false,
      error: 'Resource already exists'
    });
  }

  // Default error
  res.status(500).json({
    success: false,
    error: process.env.NODE_ENV === 'production'
      ? 'Internal server error'
      : err.message
  });
});
```

---

## Database Patterns

### Prisma Query Patterns

```javascript
// Always include organizationId
const client = await prisma.client.findFirst({
  where: {
    id: clientId,
    organizationId: req.user.organizationId
  }
});

// Include related data
const client = await prisma.client.findFirst({
  where: { id: clientId, organizationId },
  include: {
    alerts: {
      where: { status: 'PENDING' },
      orderBy: { createdAt: 'desc' }
    },
    decisions: true
  }
});

// Select specific fields only
const clients = await prisma.client.findMany({
  where: { organizationId },
  select: {
    id: true,
    name: true,
    riskLevel: true
  }
});

// Pagination
const clients = await prisma.client.findMany({
  where: { organizationId },
  skip: (page - 1) * limit,
  take: limit,
  orderBy: { createdAt: 'desc' }
});
```

### Audit Trail Pattern

```javascript
// Create with audit trail
const decision = await prisma.professionalDecision.create({
  data: {
    ...decisionData,
    organizationId,
    createdById: req.user.id,
    createdAt: new Date()
  }
});

// Update with audit trail
const updated = await prisma.professionalDecision.update({
  where: { id: decisionId },
  data: {
    ...updates,
    updatedById: req.user.id,
    updatedAt: new Date()
  }
});
```

### Transaction Pattern

```javascript
const result = await prisma.$transaction(async (tx) => {
  // Create client
  const client = await tx.client.create({
    data: { ...clientData, organizationId }
  });

  // Create initial alert
  const alert = await tx.alert.create({
    data: {
      type: 'ONBOARDING',
      clientId: client.id,
      organizationId
    }
  });

  // Log audit trail
  await tx.auditLog.create({
    data: {
      action: 'CLIENT_CREATED',
      resourceId: client.id,
      userId: req.user.id,
      organizationId
    }
  });

  return { client, alert };
});
```

---

## Security Requirements

### Authentication

```javascript
// JWT middleware - verify and attach user
const authMiddleware = async (req, res, next) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');

    if (!token) {
      return res.status(401).json({
        success: false,
        error: 'Authentication required'
      });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded; // Contains id, organizationId, role
    next();
  } catch (error) {
    res.status(401).json({
      success: false,
      error: 'Invalid token'
    });
  }
};
```

### Password Handling

```javascript
const bcrypt = require('bcryptjs');

// Hash password before storing
const hashedPassword = await bcrypt.hash(password, 10);

// Never store plain text
await prisma.user.create({
  data: {
    email,
    password: hashedPassword,  // ALWAYS hashed
    organizationId
  }
});

// Verify password
const isValid = await bcrypt.compare(inputPassword, user.password);
```

### Input Sanitization

```javascript
// Sanitize user input to prevent XSS
const sanitizeHtml = require('sanitize-html');

const cleanContent = sanitizeHtml(userInput, {
  allowedTags: ['b', 'i', 'em', 'strong'],
  allowedAttributes: {}
});
```

### Environment Variables

```javascript
// NEVER commit secrets to git
// Use .env files (in .gitignore)

// .env
DATABASE_URL=postgresql://...
JWT_SECRET=your_secret_here_min_32_chars
JWT_REFRESH_SECRET=different_secret

// Access via process.env
const secret = process.env.JWT_SECRET;

// Validate required variables on startup
if (!process.env.JWT_SECRET) {
  throw new Error('JWT_SECRET is required');
}
```

---

## Testing Standards

### Unit Test Structure (Jest)

```javascript
// __tests__/nexusDetector.test.js
const { SalesNexusDetector } = require('../services/SalesNexusDetector');

describe('SalesNexusDetector', () => {
  let detector;

  beforeEach(() => {
    detector = new SalesNexusDetector();
  });

  describe('California Economic Nexus', () => {
    it('should trigger RED alert when revenue exceeds $500k', () => {
      const result = detector.detect({ CA: 650000 });

      expect(result).toHaveLength(1);
      expect(result[0]).toMatchObject({
        severity: 'RED',
        stateCode: 'CA',
        threshold: 500000
      });
    });
  });
});
```

### Integration Test (Supertest)

```javascript
const request = require('supertest');
const app = require('../app');

describe('POST /api/clients', () => {
  it('should create client with valid data', async () => {
    const response = await request(app)
      .post('/api/clients')
      .set('Authorization', `Bearer ${validToken}`)
      .send({
        name: 'Test Client',
        email: 'test@example.com'
      })
      .expect(201);

    expect(response.body.success).toBe(true);
    expect(response.body.data.name).toBe('Test Client');
  });

  it('should enforce multi-tenant isolation', async () => {
    // Create client in org 1
    await createClient({ organizationId: 'org1' });

    // Try to access with org 2 token
    const response = await request(app)
      .get('/api/clients')
      .set('Authorization', `Bearer ${org2Token}`)
      .expect(200);

    // Should not see org 1's client
    expect(response.body.data).toHaveLength(0);
  });
});
```

---

## Code Review Checklist

### Security ✓
- [ ] Multi-tenant isolation enforced (organizationId filter)
- [ ] No hardcoded secrets or API keys
- [ ] Passwords hashed with bcrypt
- [ ] Input validation on all endpoints
- [ ] SQL injection prevented (Prisma parameterization)
- [ ] XSS prevented (React auto-escaping, input sanitization)

### Code Quality ✓
- [ ] TypeScript types defined (no `any`)
- [ ] Error handling implemented
- [ ] Consistent naming conventions
- [ ] No console.log in production code
- [ ] Comments explain "why", not "what"

### Testing ✓
- [ ] Tests added for new features
- [ ] Critical paths covered (nexus detection, auth)
- [ ] Multi-tenant isolation tested

### VaultCPA Specifics ✓
- [ ] Audit trail created for important operations
- [ ] Tax calculations verified against thresholds
- [ ] Professional decisions documented properly
- [ ] Database migrations are reversible

### Performance ✓
- [ ] No N+1 query patterns
- [ ] Pagination implemented for lists
- [ ] Appropriate indexes exist
- [ ] Large files handled efficiently

---

## File Naming Conventions

```
Frontend:
- Components: PascalCase (ClientCard.tsx)
- Pages: lowercase (page.tsx, layout.tsx)
- Utilities: camelCase (formatCurrency.ts)
- Types: PascalCase (types.ts with PascalCase interfaces)

Backend:
- Routes: camelCase (clientRoutes.js)
- Controllers: camelCase (clientController.js)
- Services: PascalCase (SalesNexusDetector.js)
- Tests: *.test.js or *.spec.js
```

---

## Common Anti-Patterns to Avoid

1. ❌ Missing organizationId filter → Data leakage
2. ❌ Using `any` type → Loss of type safety
3. ❌ Inline business logic in routes → Hard to test
4. ❌ Unhandled promise rejections → Server crashes
5. ❌ Missing error boundaries → Poor UX
6. ❌ N+1 queries → Performance issues
7. ❌ Hardcoded configuration → Deployment problems
8. ❌ Skipping validation → Security vulnerabilities

---

**When using this Skill:**
1. Reference specific sections when reviewing code
2. Cite examples when providing feedback
3. Link to this Skill in PR comments for context
4. Update this Skill when new patterns emerge
