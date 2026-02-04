---
name: subscription-schemas
description: Production-ready Supabase database schemas for customers, subscriptions, payments, invoices, and webhook events with comprehensive Row Level Security policies. Use when setting up payment infrastructure, creating subscription tables, implementing secure payment data storage, or configuring RLS policies for multi-tenant payment systems.
allowed-tools: Read, Write, Bash, mcp__plugin_nextjs-frontend_design-system, mcp__plugin_supabase_supabase
---

# Subscription Schemas

Production-ready Supabase database schemas for subscription and payment management with comprehensive security policies.

## Security Requirements

This skill follows strict security rules:

- **NO hardcoded database credentials** - All connection strings use placeholders
- **Environment variable references** - Code reads from `SUPABASE_URL` and `SUPABASE_KEY`
- **Row Level Security (RLS)** - All tables protected with comprehensive policies
- **Data encryption** - Sensitive payment data properly protected
- **Audit logging** - Webhook events tracked for compliance

All examples use placeholder values like `your_supabase_url_here`.

## Database Schema Overview

The subscription schema consists of five core tables:

1. **customers** - Customer profiles linked to auth.users
2. **subscriptions** - Active and historical subscriptions
3. **payments** - Payment transaction records
4. **invoices** - Invoice history and status
5. **webhook_events** - Payment provider webhook logs

## Table Relationships

```
auth.users (Supabase Auth)
    ↓
customers (1:1 with users)
    ↓
subscriptions (1:many)
    ↓
payments (1:many per subscription)
invoices (1:many per subscription)

webhook_events (independent audit log)
```

## Use When

- Setting up a new subscription-based application
- Implementing payment tracking for SaaS products
- Migrating payment infrastructure to Supabase
- Adding Row Level Security to payment tables
- Configuring multi-tenant payment isolation
- Creating invoice and payment history tracking
- Implementing webhook event logging for Stripe/Paddle/LemonSqueezy

## Instructions

### Phase 1: Create Database Tables

1. **Review table schemas**:
   - Read `templates/customers_table.sql` for customer profiles
   - Read `templates/subscriptions_table.sql` for subscription management
   - Read `templates/payments_table.sql` for payment records
   - Read `templates/invoices_table.sql` for invoice tracking
   - Read `templates/webhook_events_table.sql` for webhook logging

2. **Execute table creation**:
   ```bash
   bash scripts/create-payment-tables.sh
   ```

   This script will:
   - Create all five tables with proper indexes
   - Set up foreign key relationships
   - Add check constraints for data validation
   - Create updated_at triggers

### Phase 2: Implement Row Level Security

1. **Review RLS policies**:
   - Read `templates/rls_policies.sql` for complete policy definitions
   - Understand customer data isolation
   - Review subscription access controls
   - Check payment data protection rules

2. **Enable RLS and create policies**:
   ```bash
   bash scripts/setup-rls-policies.sh
   ```

   This script will:
   - Enable RLS on all payment tables
   - Create SELECT policies for authenticated users
   - Create INSERT policies with validation
   - Create UPDATE policies with ownership checks
   - Create DELETE policies (restricted)

### Phase 3: Run Complete Migration

1. **Use the complete schema migration**:
   ```bash
   bash scripts/migrate-schema.sh
   ```

   This orchestrates:
   - Table creation in correct order
   - Index creation for performance
   - RLS policy setup
   - Validation of schema structure

2. **Verify migration success**:
   ```bash
   bash scripts/validate-schema.sh
   ```

   Validates:
   - All tables exist
   - Indexes are created
   - RLS is enabled
   - Policies are active
   - Foreign keys are valid

### Phase 4: Test RLS Policies

1. **Review RLS testing examples**:
   - Read `examples/rls-testing-examples.sql`
   - Test customer data isolation
   - Verify subscription access controls
   - Confirm payment data protection

2. **Run sample queries**:
   - Read `examples/sample-queries.sql`
   - Test common subscription queries
   - Verify payment history retrieval
   - Check invoice generation queries

## Security Compliance

### Row Level Security Policies

All tables implement RLS with these principles:

1. **Customer Isolation**: Users only access their own customer record
2. **Subscription Ownership**: Users only see their own subscriptions
3. **Payment Privacy**: Payment records restricted to owners
4. **Invoice Access**: Invoices accessible only to associated customers
5. **Webhook Audit**: Webhook events visible to admins only

### Data Protection

- **Sensitive fields**: Payment methods, billing details encrypted
- **PII protection**: Customer data isolated per user
- **Audit trail**: All webhook events logged
- **No direct access**: All queries filtered through RLS

### Environment Variables

Connection configuration reads from:

```bash
SUPABASE_URL=your_supabase_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here  # For migrations only
```

## Available Scripts

### create-payment-tables.sh
Creates all five payment tables with proper structure, indexes, and constraints.

**Usage:**
```bash
bash scripts/create-payment-tables.sh
```

**Environment Required:**
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

### setup-rls-policies.sh
Enables RLS and creates comprehensive security policies for all tables.

**Usage:**
```bash
bash scripts/setup-rls-policies.sh
```

**Environment Required:**
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

### migrate-schema.sh
Orchestrates complete schema setup including tables, indexes, and RLS.

**Usage:**
```bash
bash scripts/migrate-schema.sh
```

**Environment Required:**
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

### validate-schema.sh
Validates that all tables, indexes, and policies are correctly configured.

**Usage:**
```bash
bash scripts/validate-schema.sh
```

**Environment Required:**
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`

## Available Templates

### customers_table.sql
Customer profile table with Supabase Auth integration.

**Fields:**
- `id` (uuid, primary key)
- `user_id` (uuid, foreign key to auth.users)
- `email` (text)
- `name` (text)
- `billing_address` (jsonb)
- `created_at`, `updated_at` (timestamptz)

### subscriptions_table.sql
Subscription tracking with status and billing cycles.

**Fields:**
- `id` (uuid, primary key)
- `customer_id` (uuid, foreign key)
- `plan_id` (text)
- `status` (enum: active, canceled, past_due, trialing)
- `current_period_start`, `current_period_end` (timestamptz)
- `cancel_at_period_end` (boolean)
- `created_at`, `updated_at` (timestamptz)

### payments_table.sql
Payment transaction records.

**Fields:**
- `id` (uuid, primary key)
- `subscription_id` (uuid, foreign key)
- `amount` (numeric)
- `currency` (text)
- `status` (enum: succeeded, pending, failed)
- `payment_method` (text)
- `provider_payment_id` (text)
- `created_at` (timestamptz)

### invoices_table.sql
Invoice generation and tracking.

**Fields:**
- `id` (uuid, primary key)
- `subscription_id` (uuid, foreign key)
- `invoice_number` (text, unique)
- `amount_due` (numeric)
- `amount_paid` (numeric)
- `status` (enum: draft, open, paid, void)
- `due_date` (date)
- `created_at`, `updated_at` (timestamptz)

### webhook_events_table.sql
Webhook event logging for audit and replay.

**Fields:**
- `id` (uuid, primary key)
- `provider` (text, e.g., 'stripe', 'paddle')
- `event_type` (text)
- `payload` (jsonb)
- `processed` (boolean)
- `created_at` (timestamptz)

### rls_policies.sql
Complete RLS policy definitions for all tables with customer isolation.

## Available Examples

### complete-schema-migration.sql
Complete migration script showing full schema setup in one file.

### sample-queries.sql
Common query patterns:
- Get active subscriptions for user
- Retrieve payment history
- Generate invoice summaries
- Check subscription status

### rls-testing-examples.sql
Test cases for RLS policies:
- Verify customer isolation
- Test subscription access
- Validate payment privacy
- Confirm admin-only webhook access

## Requirements

- Supabase project with database access
- Service role key for migrations (secure storage required)
- Anon key for client-side queries
- PostgreSQL extensions: `uuid-ossp`, `pgcrypto`

## Migration Strategy

### Initial Setup
1. Run `create-payment-tables.sh` to create schema
2. Run `setup-rls-policies.sh` to enable security
3. Run `validate-schema.sh` to confirm setup

### Schema Updates
1. Create new migration file in `templates/`
2. Test in development environment first
3. Apply using `migrate-schema.sh`
4. Always validate after migrations

### Rollback Support
Each template includes a rollback section:
```sql
-- Rollback
DROP TABLE IF EXISTS table_name CASCADE;
```

## Performance Considerations

### Indexes Created
- `customers.user_id` - Fast auth lookups
- `subscriptions.customer_id` - Customer subscription queries
- `subscriptions.status` - Status filtering
- `payments.subscription_id` - Payment history
- `invoices.subscription_id` - Invoice retrieval
- `webhook_events.provider, event_type` - Event filtering

### Query Optimization
- Use explicit WHERE clauses with RLS
- Include `auth.uid()` checks in queries
- Cache frequently accessed data
- Use `EXPLAIN ANALYZE` for slow queries

## Integration with Payment Providers

### Stripe
- Use `webhook_events` to log Stripe webhooks
- Map `provider_payment_id` to Stripe payment intent IDs
- Store Stripe customer ID in `customers.metadata`

### Paddle
- Log Paddle webhooks with `provider='paddle'`
- Map subscription IDs to Paddle subscription IDs
- Store Paddle customer ID in customer metadata

### LemonSqueezy
- Track LemonSqueezy events in webhook_events
- Map variant IDs to plan_id in subscriptions
- Store LemonSqueezy customer ID in metadata

## Compliance Notes

- **PCI DSS**: No credit card numbers stored (use payment provider tokens)
- **GDPR**: Customer data can be deleted via user_id cascade
- **Audit Trail**: All webhook events logged for compliance
- **Data Retention**: Configure automated archival policies as needed
