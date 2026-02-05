---
name: architecture-refactor
description: Analyze and refactor backend code to follow entity/service separation patterns. Use when asked to "refactor X to entity pattern", "analyze architecture for X", "extract business rules for X", "separate concerns for X", "create entity for X", or "clean up X service". Triggers on domain concepts like deals, leads, applications, locations, franchisees, etc.
---

# Architecture Refactor

Analyze backend code for a domain concept and refactor to follow the entity/service separation pattern.

## Architecture Overview

```
Controller (HTTP only)
    ↓
Service (orchestration, enforcement, side effects)
    ↓
Entity (business rules as predicates, data access)
    ↓
Database
```

### Layer Responsibilities

| Layer          | Does                                                                                            | Does Not                                          |
| -------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| **Controller** | Parse request, auth, permissions, call service, format response                                 | Business logic, call entities, transactions       |
| **Service**    | Orchestrate entities, enforce rules (throw), business logic, transactions, trigger side effects | Define rules, write SQL, know HTTP                |
| **Entity**     | Define rules (canX → boolean), CRUD, queries, data transformation                               | Throw on rules, call other entities, side effects |

### Key Principle: Rules vs Enforcement

```
ENTITY (defines rules):
  canConvert(deal) → { allowed: false, reason: 'Already converted' }

SERVICE (enforces rules):
  const { allowed, reason } = dealEntity.canConvert(deal);
  if (!allowed) throw new ValidationError(reason);  ← SERVICE THROWS
```

## Workflow

### Step 1: Identify Target Files

When user asks to refactor a concept (e.g., "deals"), locate:

```bash
# Find relevant files
find . -name "*deal*" -type f | grep -E "\.(ts|js)$"
```

Look for:

- `{concept}Service.ts` (e.g., `dealsService.ts`)
- `{concept}Controller.ts` (e.g., `dealsController.ts`)
- `{concept}Entity.ts` if it exists
- Related types in `@fsai/sdk` or local `.types.ts` files

Report what you found:

```
📁 Found files for "deals":
  • api/deals/dealsService.ts (523 lines)
  • api/deals/dealsController.ts (412 lines)
  • contact/deal/dealEntity.ts (89 lines) - partial implementation
  • Types: @fsai/sdk Deal, DealOverview, DealSummary
```

### Step 2: Analyze Current State

Scan the service file and categorize code:

**🔴 SCATTERED BUSINESS RULES** (should be entity predicates)

```typescript
// These patterns should become entity predicates:
if (deal.convertedAt) throw new ValidationError('...')  → canConvert()
if (!deal.applicationId) throw new ValidationError('...')  → canConvert()
if (deal.status === 'won') ...  → canDelete(), isWon()
if (!deal.applicationId && deal.franchiseeOrgId) ...  → isEntityDeal()
```

**🟡 DATA ACCESS** (should move to entity)

```typescript
// Direct database calls should move to entity:
await database.query.deals.findFirst(...)  → entity.getById()
await database.insert(drizzleSchema.deals).values(...)  → entity.create()
await database.update(drizzleSchema.deals).set(...)  → entity.update()
```

**🟠 SIDE EFFECTS** (should be extracted to notification/event classes)

```typescript
// These should be separate:
await notificationsService.franchisees.sendBatch(...)  → dealNotifications.onConverted()
await portalEventsService.fireEvent(...)  → dealEvents.emitConverted()
logger.info('Business event...')  → dealEvents.emit*()
```

**🟢 ORCHESTRATION** (correct location - stays in service)

```typescript
// This is correct for service:
await database.transaction(async () => { ... })
const result = await entityA.create(); await entityB.update();
if (featureFlag) { ... } else { ... }
```

Report findings:

```
🔍 Analysis of dealsService.ts:

BUSINESS RULES (scattered - move to entity):
  • Line 340: if (deal.convertedAt) throw → canConvert()
  • Line 336: if (!deal.applicationId) throw → canConvert()
  • Line 89: implicit - deals require applicationId → document as rule

DATA ACCESS (move to entity):
  • getDealOverview() - 80 lines of joins
  • createDeal() - insert with displayId generation
  • updateDeal() - direct update

SIDE EFFECTS (extract):
  • Line 412: notification batch → dealNotifications.onConverted()
  • Line 380: invitation service → keep in service but after transaction

ORCHESTRATION (correct - keep in service):
  • convertDealToFranchisee() - coordinates multiple entities
  • Transaction at line 350
```

### Step 3: Propose Entity Interface

Based on analysis, propose the entity structure:

```typescript
// Proposed: dealEntity.ts

class DealEntity {
  // ═══════════ Business Rules (Predicates) ═══════════
  // Return boolean or { allowed, reason } - NEVER throw

  isEntityDeal(deal): boolean;
  isApplicationDeal(deal): boolean;
  canConvert(deal): { allowed: boolean; reason?: string };
  canHaveProposedLocations(deal): boolean;
  canHaveAdditionalApplications(deal): boolean;
  canDelete(deal): { allowed: boolean; reason?: string };

  // ═══════════ Data Access ═══════════

  getById(dealId): Promise<Deal | null>;
  getOverview(dealId): Promise<DealOverview | null>;
  getByApplication(applicationId): Promise<string | null>;
  getByBrand(brandId): Promise<DealSummary[]>;

  create(params): Promise<string>;
  update(dealId, updates): Promise<void>;
  markConverted(dealId, franchiseeOrgId): Promise<void>;
  delete(dealId): Promise<void>;
}
```

**Ask user to confirm before proceeding with implementation.**

### Step 4: Implement Entity

Create or update the entity file following this pattern:

```typescript
import { eq, and, desc } from "drizzle-orm";
import { drizzleSchema } from "@fsai/supabase";
import { database } from "../../db/db.js";
import type { Deal, DealOverview } from "@fsai/sdk";

class DealEntity {
  // ═══════════════════════════════════════════════════════════════
  // BUSINESS RULES (Predicates)
  // - Return boolean or { allowed, reason }
  // - NEVER throw
  // - No side effects
  // - Testable in isolation
  // ═══════════════════════════════════════════════════════════════

  isEntityDeal(
    deal: Pick<DealOverview, "applicationId" | "franchiseeOrgId">
  ): boolean {
    return !deal.applicationId && Boolean(deal.franchiseeOrgId);
  }

  isApplicationDeal(deal: Pick<DealOverview, "applicationId">): boolean {
    return Boolean(deal.applicationId);
  }

  canConvert(
    deal: Pick<
      DealOverview,
      "applicationId" | "convertedAt" | "franchiseeOrgId"
    >
  ): { allowed: boolean; reason?: string } {
    if (deal.convertedAt) {
      return { allowed: false, reason: "Deal has already been converted" };
    }
    if (this.isEntityDeal(deal)) {
      return {
        allowed: false,
        reason: "Entity-based deals cannot be converted",
      };
    }
    if (!deal.applicationId) {
      return { allowed: false, reason: "Deal has no application to convert" };
    }
    return { allowed: true };
  }

  canHaveProposedLocations(
    deal: Pick<DealOverview, "applicationId" | "franchiseeOrgId">
  ): boolean {
    return this.isApplicationDeal(deal);
  }

  canDelete(deal: Pick<DealOverview, "convertedAt" | "status">): {
    allowed: boolean;
    reason?: string;
  } {
    if (deal.convertedAt) {
      return { allowed: false, reason: "Cannot delete converted deals" };
    }
    return { allowed: true };
  }

  // ═══════════════════════════════════════════════════════════════
  // DATA ACCESS
  // - Encapsulate all database operations
  // - Handle joins and transformations
  // - Return null for not found (don't throw usually)
  // ═══════════════════════════════════════════════════════════════

  async getById(dealId: string): Promise<Deal | null> {
    const data = await database.query.deals.findFirst({
      where: eq(drizzleSchema.deals.id, dealId),
    });
    return data ?? null;
  }

  async getOverview(dealId: string): Promise<DealOverview | null> {
    // Complex query with joins, transformed to domain shape
    const data = await database.query.deals.findFirst({
      where: eq(drizzleSchema.deals.id, dealId),
      with: {
        dealsAgreementsFees: { with: { agreementFee: true } },
        dealsProposedLocations: true,
        territories: true,
      },
    });

    if (!data) return null;
    return this.mapToOverview(data);
  }

  async create(params: {
    applicationId?: string;
    franchiseeOrgId?: string;
    brandId: string;
  }): Promise<string> {
    const displayId = await this.getNextDisplayId(params.brandId);

    const [data] = await database
      .insert(drizzleSchema.deals)
      .values({
        displayId,
        ...params,
        leadApplicationOwnershipPercentage: params.applicationId ? 100 : null,
      })
      .returning({ id: drizzleSchema.deals.id });

    return data.id;
  }

  async update(dealId: string, updates: Partial<Deal>): Promise<void> {
    await database
      .update(drizzleSchema.deals)
      .set(updates)
      .where(eq(drizzleSchema.deals.id, dealId));
  }

  async markConverted(dealId: string, franchiseeOrgId: string): Promise<void> {
    await database
      .update(drizzleSchema.deals)
      .set({
        convertedAt: new Date().toISOString(),
        franchiseeOrgId,
        status: "won",
      })
      .where(eq(drizzleSchema.deals.id, dealId));
  }

  // ═══════════════════════════════════════════════════════════════
  // PRIVATE HELPERS
  // ═══════════════════════════════════════════════════════════════

  private async getNextDisplayId(brandId: string): Promise<number> {
    const prev = await database.query.deals.findFirst({
      where: eq(drizzleSchema.deals.brandId, brandId),
      orderBy: desc(drizzleSchema.deals.displayId),
      columns: { displayId: true },
    });
    return (prev?.displayId ?? 0) + 1;
  }

  private mapToOverview(data: any): DealOverview {
    // Transform DB shape → domain shape
    return { ...data /* transformed */ };
  }
}

export const dealEntity = new DealEntity();
```

### Step 5: Refactor Service to Orchestrator

Transform service methods to follow this pattern:

```typescript
class DealsService {
  async convertDealToFranchisee(
    dealId: string,
    sendInvitation: boolean,
    userId: string
  ): Promise<string> {
    // 1. FETCH via entity
    const deal = await dealEntity.getOverview(dealId);
    if (!deal) throw new NotFoundError('Deal not found');

    // 2. ENFORCE rules (entity defines, service enforces)
    const { allowed, reason } = dealEntity.canConvert(deal);
    if (!allowed) throw new ValidationError(reason);

    // 3. BUSINESS LOGIC (feature flags, conditional behavior)
    const portalEnabled = await flagsService.isFranchiseePortalEnabled(deal.brandId);
    const shouldInvite = sendInvitation && portalEnabled;

    // 4. ORCHESTRATE (transaction wraps multiple entity calls)
    const franchiseeOrgId = await database.transaction(async () => {
      const orgId = await franchiseeOrgEntity.create({ ... });
      await locationEntity.createFromProposed(deal.proposedLocations, orgId);
      await dealEntity.markConverted(dealId, orgId);
      return orgId;
    });

    // 5. SIDE EFFECTS (after transaction succeeds)
    await dealNotifications.onConverted(deal, franchiseeOrgId);
    await dealEvents.emitConverted(deal, franchiseeOrgId);

    if (shouldInvite) {
      await franchiseeInvitations.sendAll(franchiseeOrgId, deal.brandId, userId);
    }

    return franchiseeOrgId;
  }

  async updateDeal(dealId: string, updates: DealUpdates): Promise<void> {
    const deal = await dealEntity.getById(dealId);
    if (!deal) throw new NotFoundError('Deal not found');

    // Enforce conditional rules via predicates
    if (updates.proposedLocations && !dealEntity.canHaveProposedLocations(deal)) {
      throw new ValidationError('Entity deals cannot have proposed locations');
    }

    await dealEntity.update(dealId, updates);
  }

  // Simple delegation is fine
  async getDealOverview(dealId: string) {
    return dealEntity.getOverview(dealId);
  }
}
```

### Step 6: Extract Side Effects (if needed)

If there's significant notification/event logic, create separate files:

```typescript
// dealNotifications.ts
class DealNotifications {
  async onConverted(
    deal: DealOverview,
    franchiseeOrgId: string
  ): Promise<void> {
    const recipients = deal.applications
      ?.filter((app) => app.email)
      .map((app) => ({
        email: app.email!,
        name: `${app.firstName} ${app.lastName}`,
      }));

    if (!recipients?.length) return;

    try {
      await notificationsService.franchisees.sendDealConversionNotificationBatch(
        {
          recipients,
          brandId: deal.brandId,
          dealId: deal.id,
          franchiseeOrgId,
        }
      );
    } catch (error) {
      logger.error("Failed to send conversion notifications", {
        dealId: deal.id,
        error,
      });
      // Don't rethrow - notifications shouldn't fail the operation
    }
  }

  async onMadeVisible(deal: DealOverview): Promise<void> {
    if (!deal.applicationId) return;
    await notificationsService.applicants.triggerNotification({
      applicationId: deal.applicationId,
      type: "deal_available",
    });
  }
}

export const dealNotifications = new DealNotifications();
```

### Step 7: Report Summary

```
✅ Architecture Refactor Complete: deals

CREATED:
  • api/deals/dealEntity.ts
    - 5 business rule predicates (canConvert, canDelete, isEntityDeal, etc.)
    - 8 data access methods (getById, getOverview, create, update, etc.)

  • api/deals/dealNotifications.ts (optional)
    - onConverted()
    - onMadeVisible()

MODIFIED:
  • api/deals/dealsService.ts
    - Removed 180 lines of data access (→ entity)
    - Removed 45 lines of inline rules (→ entity predicates)
    - Service now orchestrates only

UNCHANGED:
  • api/deals/dealsController.ts (already HTTP-only)

BUSINESS RULES NOW DISCOVERABLE:
  dealEntity.canConvert()
  dealEntity.canDelete()
  dealEntity.canHaveProposedLocations()
  dealEntity.canHaveAdditionalApplications()
  dealEntity.isEntityDeal()
  dealEntity.isApplicationDeal()
```

## File Structure

```
{concept}/
├── {concept}Entity.ts           # Rules + data access
├── {concept}Entity.types.ts     # Types (optional)
├── {concept}Service.ts          # Orchestration
├── {concept}Controller.ts       # HTTP handling
├── {concept}Notifications.ts    # Side effects (optional)
└── {concept}Assertions.ts       # Permission helpers (optional)
```

## Quick Reference: Where Does This Go?

| Code Pattern                                | Location                       |
| ------------------------------------------- | ------------------------------ |
| `if (x.status === 'y') return false`        | Entity (predicate)             |
| `if (!allowed) throw new ValidationError()` | Service (enforcement)          |
| `database.query.*.findFirst()`              | Entity                         |
| `database.transaction()`                    | Service                        |
| `notificationsService.send*()`              | Notifications class or Service |
| `req.params`, `res.json()`                  | Controller                     |
| `assertBrandPermissions()`                  | Controller                     |

## Guidelines

- **Ask before major changes** - Confirm entity interface before implementing
- **Preserve functionality** - Refactor structure, not behavior
- **Match existing patterns** - Follow LeadEntity style if it exists in codebase
- **Incremental is okay** - Can refactor one method at a time
- **Keep services thin** - If >50 lines, something can likely move to entity
- **Rules are predicates** - Return booleans, don't throw

## Triggers

- "refactor deals to entity pattern"
- "analyze architecture for leads"
- "extract business rules from application service"
- "separate concerns for locations"
- "create entity for franchisee"
- "clean up the deals service"
- "where are the rules for deals?"
- "make deals follow the entity pattern"
