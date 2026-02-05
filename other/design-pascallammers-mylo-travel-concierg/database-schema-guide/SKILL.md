---
name: database-schema-guide
description: VaultCPA database schema reference with 50+ Prisma models, relationships, and query patterns. Use when working with database models, designing features, or understanding data structure.
allowed-tools: Read, Grep, Glob
---

# VaultCPA Database Schema Guide

**Version:** 2.0
**Last Updated:** January 2026
**Schema Location:** `server/prisma/schema.prisma`

This Skill provides a comprehensive guide to VaultCPA's PostgreSQL database schema, including model relationships, common patterns, and query examples.

## Quick Navigation

- [Schema Overview](#schema-overview)
- [Core Models](#core-models)
- [Common Query Patterns](#common-query-patterns)
- [Relationship Diagrams](#relationship-diagrams)
- [Migration Patterns](#migration-patterns)
- [Data Model Decisions](#data-model-decisions)

For detailed model references, see:
- [Core Models Reference](core-models.md) - Organization, User, Client
- [Compliance Models](compliance-models.md) - Alerts, Nexus, Risk
- [Workflow Models](workflow-models.md) - Tasks, Decisions, Documents

---

## Schema Overview

### Model Categories

**Tenant & Identity (4 models)**
- Organization - Root tenant entity
- User - Team members with CPA credentials
- Permission - Role-based access control
- ApiKey - API authentication

**Core Business (12 models)**
- Client - Primary data subject
- ClientState - Per-state tracking
- BusinessProfile - Business details
- BusinessLocation - Physical locations
- Contact - Client contacts
- GeographicDistribution - Revenue by region
- RevenueBreakdown - Categorized revenue
- CustomerDemographics - Customer analytics
- ClientRevenueHistory - Historical revenue
- StateTaxInfo - State tax thresholds
- OrganizationMetadata - Custom org data
- PerformanceMetric - Business metrics

**Compliance & Risk (10 models)**
- Alert - Multi-purpose alerts
- NexusAlert - State tax nexus specific
- NexusActivity - Activity tracking
- RiskFactor - Risk assessments
- ComplianceStandard - Compliance frameworks
- RegulatoryChange - Law changes
- DataProcessing - Processing records
- AuditLog - System audit trail
- AuditTrail - Business audit trail
- Notification - In-app notifications

**Workflow & Decisions (7 models)**
- Task - Workflow tasks
- TaskStep - Task breakdown
- ProfessionalDecision - High-stakes decisions
- DecisionTable - Decision audit
- Document - File management
- AdvisoryDocument - Client advice
- Comment - Collaborative notes

**Communication (3 models)**
- Consultation - Client meetings
- Communication - Contact log
- ClientCommunication - Interaction tracking

**Tax & Doctrine (4 models)**
- DoctrineRule - Tax rules with versioning
- DoctrineApproval - Approval workflow
- DoctrineVersionEvent - Change history
- DoctrineImpactMetrics - Rule impact

**System & Integration (9 models)**
- Integration - Third-party connections
- Webhook - Webhook configs
- WebhookDelivery - Delivery tracking
- GeneratedDashboard - Custom dashboards
- Template - Reusable content
- Report - Scheduled reports
- ActivityFeed - Team activity
- DataProcessing - Processing jobs

**Total:** 50+ models

---

## Core Models

### Organization (Tenant Root)

```prisma
model Organization {
  id                   String   @id @default(uuid())
  slug                 String   @unique
  name                 String
  subscriptionTier     String   @default("trial")
  subscriptionStatus   String   @default("active")

  // Relationships - ALL data scoped to organization
  users                User[]
  clients              Client[]
  alerts               Alert[]
  tasks                Task[]
  // ... 30+ more relationships
}
```

**Key Points:**
- Root of multi-tenant hierarchy
- Every other model references organizationId
- Subscription and billing tracked here
- Custom settings stored in JSON fields

**Common Queries:**
```javascript
// Get organization with user count
const org = await prisma.organization.findUnique({
  where: { id: orgId },
  include: {
    _count: {
      select: { users: true, clients: true }
    }
  }
});

// Get all orgs expiring soon
const expiring = await prisma.organization.findMany({
  where: {
    subscriptionExpiresAt: {
      lte: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) // 30 days
    }
  }
});
```

---

### User (Team Members)

```prisma
model User {
  id              String   @id @default(uuid())
  organizationId  String   @map("organization_id")
  email           String
  passwordHash    String   @map("password_hash")
  role            String   // MANAGING_PARTNER, TAX_MANAGER, STAFF_ACCOUNTANT, SYSTEM_ADMIN

  // CPA Credentials
  cpaLicense      String?  @map("cpa_license")
  cpaState        String?  @map("cpa_state")
  cpaExpiration   DateTime? @map("cpa_expiration")

  // Relationships
  organization    Organization @relation(fields: [organizationId], references: [id])
  assignedTasks   Task[]       @relation("AssignedUser")
  createdTasks    Task[]       @relation("CreatedByUser")
}
```

**Key Points:**
- Scoped to organization
- Role determines dashboard access
- CPA credentials for compliance tracking
- Audit trail through created/assigned relationships

**Common Queries:**
```javascript
// Get user with permissions
const user = await prisma.user.findFirst({
  where: {
    email,
    organizationId
  },
  include: {
    organization: true,
    permissions: true
  }
});

// Get all CPAs in org
const cpas = await prisma.user.findMany({
  where: {
    organizationId,
    cpaLicense: { not: null }
  }
});
```

---

### Client (Primary Business Entity)

```prisma
model Client {
  id                  String   @id @default(uuid())
  organizationId      String   @map("organization_id")
  name                String
  status              String   @default("prospect")
  riskLevel           String   @default("low")

  // Relationships
  organization        Organization @relation(fields: [organizationId], references: [id])
  alerts              Alert[]
  nexusAlerts         NexusAlert[]
  tasks               Task[]
  decisions           ProfessionalDecision[]
  clientStates        ClientState[]
  revenueHistory      ClientRevenueHistory[]
}
```

**Key Points:**
- Central entity for all client data
- Risk level drives compliance workflows
- State-specific data in related tables
- Extensive relationships (20+ related models)

**Common Queries:**
```javascript
// Get client with all nexus alerts
const client = await prisma.client.findFirst({
  where: {
    id: clientId,
    organizationId
  },
  include: {
    nexusAlerts: {
      where: { status: 'ACTIVE' },
      orderBy: { createdAt: 'desc' }
    },
    clientStates: true,
    revenueHistory: {
      orderBy: { year: 'desc' },
      take: 3 // Last 3 years
    }
  }
});

// Get high-risk clients
const highRisk = await prisma.client.findMany({
  where: {
    organizationId,
    riskLevel: { in: ['HIGH', 'CRITICAL'] }
  },
  include: {
    _count: {
      select: { alerts: true }
    }
  }
});
```

---

### Alert (Multi-Purpose Alerts)

```prisma
model Alert {
  id             String   @id @default(uuid())
  organizationId String   @map("organization_id")
  clientId       String?  @map("client_id")
  type           String   // NEXUS, COMPLIANCE, RISK, DOCUMENT, DEADLINE
  severity       String   // CRITICAL, HIGH, MEDIUM, LOW
  status         String   @default("pending")
  message        String

  // Polymorphic relationships
  client         Client?  @relation(fields: [clientId], references: [id])
  consultation   Consultation? @relation(fields: [consultationId], references: [id])
}
```

**Key Points:**
- Generic alert system for all alert types
- Polymorphic - can relate to different entities
- Status workflow: pending → acknowledged → in_progress → resolved
- Severity determines urgency

---

### NexusAlert (State Tax Nexus Specific)

```prisma
model NexusAlert {
  id              String   @id @default(uuid())
  organizationId  String   @map("organization_id")
  clientId        String   @map("client_id")
  state           String
  type            String   // SALES_TAX, INCOME_TAX, FRANCHISE_TAX, PAYROLL
  severity        String   // RED, ORANGE, YELLOW
  threshold       Decimal?
  currentAmount   Decimal?

  // Doctrine integration
  appliedDoctrineRuleId String? @map("applied_doctrine_rule_id")
  doctrineRule          DoctrineRule? @relation(fields: [appliedDoctrineRuleId], references: [id])
}
```

**Key Points:**
- Specialized for tax nexus alerts
- Links to doctrine rules for professional judgment
- Tracks threshold vs actual amounts
- Color-coded severity (RED/ORANGE/YELLOW)

---

### ProfessionalDecision (High-Stakes Decisions)

```prisma
model ProfessionalDecision {
  id                String   @id @default(uuid())
  organizationId    String   @map("organization_id")
  clientId          String   @map("client_id")
  decisionType      String
  riskLevel         String
  financialExposure Decimal?

  // Decision content
  question          String
  analysis          String
  conclusion        String
  supportingEvidence Json    @default("{}")

  // Peer review
  reviewStatus      String   @default("pending")
  reviewedBy        String?
  reviewedAt        DateTime?

  // Audit trail
  createdById       String   @map("created_by_id")
  createdBy         User     @relation("DecisionCreator", fields: [createdById], references: [id])
}
```

**Key Points:**
- Documents high-stakes professional judgments
- Peer review workflow built-in
- Financial exposure tracking
- Complete audit trail for liability protection

---

### DoctrineRule (Tax Doctrine with Versioning)

```prisma
model DoctrineRule {
  id            String   @id @default(uuid())
  organizationId String? @map("organization_id")
  clientId      String?  @map("client_id")
  scope         String   // FIRM, OFFICE, CLIENT

  version       Int      @default(1)
  status        String   // DRAFT, PENDING_APPROVAL, ACTIVE, DISABLED

  // Rule content
  title         String
  description   String
  taxType       String
  states        String[] // Array of state codes

  // Versioning
  previousVersionId String?
  versionEvents     DoctrineVersionEvent[]
  approvals         DoctrineApproval[]
  impactMetrics     DoctrineImpactMetrics[]
}
```

**Key Points:**
- Reusable tax position rules
- Versioned for compliance
- Scoped to firm/office/client level
- Approval workflow integration
- Impact tracking for audit purposes

---

## Common Query Patterns

### Pattern 1: Multi-Tenant Filtering

```javascript
// ALWAYS include organizationId
const clients = await prisma.client.findMany({
  where: {
    organizationId: req.user.organizationId  // Required!
  }
});

// With additional filters
const activeClients = await prisma.client.findMany({
  where: {
    organizationId: req.user.organizationId,
    status: 'ACTIVE',
    riskLevel: { in: ['HIGH', 'CRITICAL'] }
  }
});
```

### Pattern 2: Pagination

```javascript
const page = 1;
const limit = 20;

const clients = await prisma.client.findMany({
  where: { organizationId },
  skip: (page - 1) * limit,
  take: limit,
  orderBy: { createdAt: 'desc' }
});

const total = await prisma.client.count({
  where: { organizationId }
});

const pages = Math.ceil(total / limit);
```

### Pattern 3: Efficient Relationships (Avoid N+1)

```javascript
// ❌ BAD - N+1 query
const clients = await prisma.client.findMany({ where: { organizationId } });
for (const client of clients) {
  const alerts = await prisma.alert.findMany({
    where: { clientId: client.id }
  });
}

// ✅ GOOD - Single query with include
const clients = await prisma.client.findMany({
  where: { organizationId },
  include: {
    alerts: {
      where: { status: 'PENDING' }
    }
  }
});
```

### Pattern 4: Selective Field Loading

```javascript
// Only fetch needed fields
const clients = await prisma.client.findMany({
  where: { organizationId },
  select: {
    id: true,
    name: true,
    riskLevel: true,
    _count: {
      select: { alerts: true }
    }
  }
});
```

### Pattern 5: Transactions

```javascript
const result = await prisma.$transaction(async (tx) => {
  // Create client
  const client = await tx.client.create({
    data: { ...clientData, organizationId }
  });

  // Create onboarding alert
  const alert = await tx.alert.create({
    data: {
      type: 'ONBOARDING',
      clientId: client.id,
      organizationId
    }
  });

  // Audit log
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

### Pattern 6: Soft Deletes

```javascript
// Instead of deleting, mark as deleted
await prisma.client.update({
  where: { id: clientId },
  data: { deletedAt: new Date() }
});

// Filter out deleted records
const activeClients = await prisma.client.findMany({
  where: {
    organizationId,
    deletedAt: null
  }
});
```

---

## Relationship Diagrams

### Core Entity Relationships

```
Organization (Tenant Root)
│
├─► User (Team members)
│   └─► Task (Assigned work)
│
├─► Client (Business entity)
│   ├─► Alert (All alert types)
│   ├─► NexusAlert (Tax nexus specific)
│   ├─► Task (Client work)
│   ├─► ProfessionalDecision (Judgments)
│   ├─► ClientState (Per-state data)
│   ├─► RevenueHistory (Historical data)
│   ├─► Consultation (Meetings)
│   └─► Document (Files)
│
├─► DoctrineRule (Tax rules)
│   ├─► DoctrineApproval (Approval workflow)
│   ├─► DoctrineVersionEvent (Version history)
│   └─► NexusAlert (Applied to alerts)
│
└─► Integration (Third-party)
    ├─► Webhook (Event configs)
    └─► WebhookDelivery (Delivery log)
```

### Alert Workflow

```
Alert Created (PENDING)
│
├─► Acknowledged (USER_ACTION)
│   └─► In Progress (WORK_STARTED)
│       ├─► Resolved (COMPLETED)
│       └─► Dismissed (NOT_APPLICABLE)
│
└─► Escalated (CRITICAL_SEVERITY)
    └─► Consultation Created
```

### Decision Workflow

```
ProfessionalDecision Created (DRAFT)
│
├─► Submitted for Review (PENDING_REVIEW)
│   ├─► Approved (APPROVED)
│   │   └─► Active (Applied to clients)
│   │
│   └─► Rejected (REJECTED)
│       └─► Back to Draft (REVISIONS_NEEDED)
│
└─► Archived (ARCHIVED)
```

---

## Migration Patterns

### Safe Migration Strategy

**1. Additive Changes (Safe)**
```prisma
// Add optional field
model Client {
  newField String?  // Optional
}

// Deploy migration
// Backfill data if needed
// Make required in next migration
```

**2. Renaming Fields (Zero Downtime)**
```prisma
// Step 1: Add new field
model Client {
  oldName String
  newName String?
}

// Step 2: Dual-write in application
// Step 3: Backfill data
// Step 4: Switch reads to newName
// Step 5: Remove oldName
```

**3. Breaking Changes (Requires Downtime)**
```prisma
// Changing field type or removing required field
// Plan maintenance window
// Run migration during low-traffic period
```

### Migration Commands

```bash
# Development - interactive
cd server
npx prisma migrate dev --name add_client_risk_level

# Production - automated
npx prisma migrate deploy

# Check status
npx prisma migrate status

# Generate Prisma client
npx prisma generate

# View data
npx prisma studio
```

---

## Data Model Decisions

### Why Separate NexusAlert from Alert?

**Reason:** Specialized tax nexus tracking with doctrine rule integration

```
Alert - Generic (all types: compliance, risk, document)
NexusAlert - Tax nexus specific (threshold tracking, doctrine rules)
```

**Benefits:**
- Cleaner schema (nexus-specific fields don't clutter Alert)
- Better query performance (smaller Alert table)
- Doctrine integration without affecting other alerts

### Why ClientState Table?

**Reason:** Per-state tracking for multi-state clients

```
Client (parent)
└─► ClientState[] (one per state where client operates)
    ├─► state: "CA"
    ├─► hasNexus: true
    ├─► registeredForSalesTax: true
    └─► lastFilingDate: 2024-01-15
```

**Benefits:**
- Scalable (clients can operate in 1-50 states)
- Clean queries (get all CA clients, get client's states)
- Historical tracking per state

### Why JSON Fields?

Used for flexible, schema-less data:

```prisma
model Organization {
  settings  Json  @default("{}")  // Customizable settings
  branding  Json  @default("{}")  // Logo, colors, themes
  features  Json  @default("{}")  // Feature flags
}
```

**Use JSON when:**
- Data structure varies by tenant
- Frequent schema changes needed
- Non-queryable configuration data

**Use separate tables when:**
- Need to query/filter on field
- Foreign key relationships needed
- Data integrity constraints required

### Audit Trail Strategy

**Two-Level Approach:**

```
AuditLog - System-level (all actions, auto-generated)
├─► user_id, action, resource_type, resource_id, timestamp

AuditTrail - Business-level (important business events)
├─► decision_id, event_type, description, user_id, timestamp
```

**Why both?**
- AuditLog: Complete system history for debugging
- AuditTrail: Business events for compliance/audit

---

## Index Strategy

### Critical Indexes

```prisma
// Multi-tenant queries
@@index([organizationId])

// Common lookups
@@index([organizationId, status])
@@index([organizationId, createdAt(sort: Desc)])

// Relationship indexes (auto-created by Prisma)
// Fields used in @relation get indexes automatically

// Composite indexes for common queries
@@index([organizationId, clientId, type])
```

### When to Add Indexes

1. **WHERE clauses** - Fields frequently used in filters
2. **ORDER BY** - Fields used for sorting
3. **JOIN operations** - Foreign key fields
4. **Multi-column queries** - Composite indexes

### Index Performance Check

```sql
-- Check query performance
EXPLAIN ANALYZE SELECT * FROM clients WHERE organization_id = '...';

-- See table indexes
SELECT * FROM pg_indexes WHERE tablename = 'clients';

-- Index usage stats
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

---

## Common Mistakes to Avoid

1. ❌ **Missing organizationId filter** → Data leakage
2. ❌ **N+1 queries** → Use include/select
3. ❌ **No pagination** → Memory issues with large datasets
4. ❌ **Not using transactions** → Data inconsistency
5. ❌ **Forgetting indexes** → Slow queries as data grows
6. ❌ **Using findUnique without unique constraint** → Runtime errors
7. ❌ **Not cascading deletes** → Orphaned records

---

## Quick Reference

### Get Organization
```javascript
const org = await prisma.organization.findUnique({
  where: { id: orgId }
});
```

### Get User with Org
```javascript
const user = await prisma.user.findFirst({
  where: { email, organizationId },
  include: { organization: true }
});
```

### Get Client with Alerts
```javascript
const client = await prisma.client.findFirst({
  where: { id: clientId, organizationId },
  include: {
    alerts: { where: { status: 'PENDING' } },
    nexusAlerts: true
  }
});
```

### Create with Audit Trail
```javascript
const client = await prisma.client.create({
  data: {
    ...clientData,
    organizationId,
    createdById: req.user.id,
    createdAt: new Date()
  }
});
```

---

**For detailed model specifications, see:**
- [core-models.md](core-models.md) - Complete field definitions
- [compliance-models.md](compliance-models.md) - Alert and risk models
- [workflow-models.md](workflow-models.md) - Task and decision models

**When using this Skill:**
1. Always verify organizationId filtering
2. Use appropriate query patterns for performance
3. Follow migration best practices
4. Refer to relationship diagrams for data modeling
