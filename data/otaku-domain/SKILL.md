---
name: otaku-domain
description: Convention management domain knowledge for Otaku Odyssey. Use when implementing features related to conventions, attendees, vendors, sponsors, panels, or volunteers.
allowed-tools: Read, Write, Edit, Bash
---

# Otaku Odyssey Domain Knowledge

## Core Domain Concepts

### Convention Lifecycle
```
Planning → Pre-Registration → Active Registration → Convention Days → Post-Convention
```

### Applicant Types & Workflows

All applicant types follow a similar workflow but with domain-specific variations:

#### Attendees (Badge Holders)
```
Register → Select Badge Type → Payment → Confirmation → Check-in at Convention
```
- Badge types: Weekend, Single Day (Fri/Sat/Sun), VIP, Child, Comp
- Status: registered, paid, checked_in, cancelled

#### Vendors (Booth Holders)
```
Application → Review → Approval/Waitlist → Payment → Booth Assignment → Convention
```
- Booth types: Standard, Corner, Island, Artist Alley
- Status: draft, submitted, under_review, approved, rejected, waitlisted, confirmed

#### Sponsors (Financial Partners)
```
Application → Tier Selection → Review → Approval → Payment → Benefit Fulfillment
```
- Tiers: Bronze ($250), Silver ($500), Gold ($1000), Platinum ($2000), Diamond ($3000)
- Benefits: Logo placement, vendor tables, weekend passes, hotel accommodations
- Status: draft, submitted, approved, rejected, active, completed

#### Panelists (Content Creators)
```
Panel Proposal → Review → Approval → Room/Time Assignment → Convention
```
- Panel types: Discussion, Workshop, Q&A, Screening, Performance
- Status: proposed, under_review, approved, scheduled, completed, cancelled

#### Volunteers (Staff)
```
Application → Training Assignment → Shift Selection → Convention Work → Hours Tracking
```
- Departments: Registration, Security, Events, Tech, Guest Relations
- Status: applied, approved, trained, active, inactive

## Schema Relationships

```
Convention (root)
├── Attendees (via badges)
├── Vendors (via applications)
│   └── Vendor Products
├── Sponsors (via applications)
│   └── Sponsor Tier Benefits
├── Panels (via proposals)
│   └── Panelists (many-to-many)
├── Volunteers (via applications)
│   └── Volunteer Shifts
├── Hotels (partnerships)
│   └── Room Blocks
└── Schedule
    └── Events/Sessions
```

## Common Field Patterns

### Convention Reference
Every convention-scoped entity needs:
```typescript
conventionId: text("convention_id")
  .notNull()
  .references(() => conventions.id, { onDelete: "cascade" }),
```

### Application Workflow Fields
```typescript
status: applicationStatusEnum("status").default("draft").notNull(),
submittedAt: timestamp("submitted_at"),
reviewedAt: timestamp("reviewed_at"),
reviewedBy: text("reviewed_by").references(() => users.id),
reviewNotes: text("review_notes"),
```

### Payment Integration
```typescript
stripePaymentIntentId: text("stripe_payment_intent_id"),
stripeCustomerId: text("stripe_customer_id"),
paymentStatus: paymentStatusEnum("payment_status").default("pending"),
paidAt: timestamp("paid_at"),
amountPaid: decimal("amount_paid", { precision: 10, scale: 2 }),
```

### Contact Fields
```typescript
contactName: text("contact_name").notNull(),
contactEmail: text("contact_email").notNull(),
contactPhone: text("contact_phone"),
```

## Pricing Logic

### Badge Pricing
- Early bird discount before cutoff date
- Child badges free under age 6
- Group discounts for 10+ badges
- Comped badges for sponsors/volunteers

### Vendor Pricing
- Base price by booth type
- Corner premium (+25%)
- Electricity add-on
- Multi-day discount

### Sponsor Tiers
```typescript
const SPONSOR_TIERS = {
  bronze: { price: 250, passCount: 2, tableCount: 0 },
  silver: { price: 500, passCount: 4, tableCount: 1 },
  gold: { price: 1000, passCount: 6, tableCount: 2 },
  platinum: { price: 2000, passCount: 8, tableCount: 2, hotelNights: 2 },
  diamond: { price: 3000, passCount: 10, tableCount: 3, hotelNights: 3 },
};
```

## UI Patterns

### Dashboard Layout
```
/(dashboard)/
├── conventions/[id]/
│   ├── overview/          # Stats, recent activity
│   ├── attendees/         # Badge management
│   ├── vendors/           # Vendor applications
│   ├── sponsors/          # Sponsor management
│   ├── panels/            # Panel scheduling
│   ├── volunteers/        # Staff management
│   ├── schedule/          # Event calendar
│   └── settings/          # Convention config
```

### Application Review Flow
```tsx
// Always include:
// 1. Application details
// 2. Review history
// 3. Action buttons (Approve/Reject/Waitlist)
// 4. Notes field for reviewer comments
```

### Status Badges
```tsx
const statusColors = {
  draft: "gray",
  submitted: "blue",
  under_review: "yellow",
  approved: "green",
  rejected: "red",
  waitlisted: "orange",
};
```

## Business Rules

### Vendor Capacity
- Maximum vendors per convention (configurable)
- Waitlist when capacity reached
- Auto-promote from waitlist on cancellation

### Panel Scheduling
- No speaker double-booking
- Room capacity validation
- Time slot conflict detection

### Volunteer Shifts
- Minimum shift length: 2 hours
- Maximum hours per day: 8
- Required rest between shifts: 8 hours

### Sponsor Benefits
- Benefits tied to tier, not individual
- Pro-rated benefits for late sponsors
- Rollover logic for unused benefits

## Error Messages

Use domain-appropriate error messages:
```typescript
// Good
throw new TRPCError({
  code: "BAD_REQUEST",
  message: "Cannot submit application: required fields missing",
});

// Bad
throw new TRPCError({
  code: "BAD_REQUEST", 
  message: "Validation failed",
});
```

## Testing Patterns

```typescript
// Test data factories
const createTestConvention = () => ({
  name: "Test Con 2025",
  startDate: new Date("2025-06-15"),
  endDate: new Date("2025-06-17"),
});

const createTestVendor = (conventionId: string) => ({
  conventionId,
  businessName: "Test Vendor",
  contactEmail: "test@vendor.com",
  boothType: "standard",
});
```

## Checklist for Domain Features

- [ ] Follows applicant workflow pattern
- [ ] Includes convention reference
- [ ] Has appropriate status enum
- [ ] Includes audit timestamps
- [ ] Has payment fields if applicable
- [ ] Contact information captured
- [ ] Review workflow fields present
- [ ] Status-appropriate validation
