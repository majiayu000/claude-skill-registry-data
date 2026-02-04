---
name: cliftonsites-backend
description: Use this skill when working with the CliftonSites Supabase backend for any task including understanding database schemas, debugging issues, adding features, querying data, managing RPC functions, reviewing triggers/policies, working with the automation pipeline, security architecture (MFA authentication, RLS, SECURITY DEFINER functions, API route protection), or any database operation. Provides complete expertise on all 12 tables, 25 RPC functions, 5 triggers, RLS policies, SECURITY DEFINER functions, admin MFA authentication, internal API token validation, views, indexes, data flows, and Supabase MCP server operations.
---

# CliftonSites Backend Expert Skill

This skill provides **complete, comprehensive expertise** on the entire CliftonSites Supabase backend. Use this skill for ANY backend-related task - from simple queries to complex debugging to adding new features.

## What This Skill Covers

- **12 Database Tables**: Complete schemas, columns, constraints, relationships
- **25 RPC Functions**: Full documentation, parameters, usage patterns, what they do
- **5 Database Triggers**: What fires when, why, and how they integrate
- **Security Architecture**: MFA authentication, RLS policies, SECURITY DEFINER functions, API route protection
- **RLS Policies**: Row-level security for each table, who can access what (RLS enabled on ALL tables)
- **2 Views**: v_queue_status, v_identification_progress
- **Indexes**: All performance optimizations
- **Data Flows**: How data moves through the system
- **Automation Pipeline**: VM integration, identification, implementation flows
- **Admin Authentication**: MFA-protected admin dashboard with TOTP
- **API Route Protection**: Internal API tokens, session validation
- **Supabase MCP Server**: Complete operations guide for any database task

## Navigation Guide

This skill uses **progressive disclosure** - start here, then dive into detailed references as needed:

### Core References (Read These for Deep Understanding)

1. **`./database-tables-reference.md`** - Complete schemas for all 12 tables
   - Full column definitions with types and constraints
   - Relationships between tables
   - Usage patterns and common queries

2. **`./rpc-functions-reference.md`** - All 25 RPC functions documented
   - Function signatures and parameters
   - What each function does and when to use it
   - Who can execute (permissions) - includes SECURITY DEFINER functions
   - Internal logic and table dependencies

3. **`./triggers-policies-views.md`** - Triggers, RLS, views, indexes
   - All 5 active triggers: what fires when and why
   - Complete RLS policies for each table (RLS enabled on ALL tables)
   - 2 views with their definitions
   - All indexes for performance

4. **`./data-flows-architecture.md`** - System architecture and integration
   - Complete data flow diagrams
   - Automation pipeline architecture
   - VM integration details
   - User journey flows (including authentication)
   - Admin dashboard authentication flow
   - How everything connects

5. **`./security-architecture.md`** - Complete security documentation
   - MFA authentication (TOTP) for admin dashboard
   - RLS policies and SECURITY DEFINER functions
   - API route protection (internal tokens, session validation)
   - Function permission matrix (anon vs service_role)
   - Security verification queries

6. **`./supabase-mcp-guide.md`** - Supabase MCP Server operations
   - How to query tables
   - How to call RPC functions
   - How to check policies, triggers, schemas
   - How to execute any SQL
   - Complete MCP tool reference

7. **`./quick-reference.md`** - Common operations cheat sheet
   - Frequently used queries
   - Common debugging commands
   - Security verification queries
   - Quick lookup for routine tasks

## When to Use This Skill

Use this skill **immediately** when you need to:

### Understanding the Backend
- "What tables exist in the database?"
- "How does the pipeline_businesses table work?"
- "What's the schema for qualified_businesses?"
- "What RPC functions are available?"
- "How does the automation system work?"

### Debugging Issues
- "Why isn't a business showing in the queue?"
- "The outreach trigger isn't firing - why?"
- "What RLS policies affect this query?"
- "Why can't anon role access this table?"
- "What functions query pipeline_businesses?"

### Adding Features
- "I need to add a new column to track X"
- "How do I create a new RPC function?"
- "Where should I store this new data?"
- "What's the pattern for adding automation commands?"
- "How do I trigger outreach for a business?"

### Working with Data
- "Get all businesses in the queue"
- "Check automation status"
- "Query recent logs"
- "Find businesses by status"
- "Get current identification target"

### Reviewing Configurations
- "What triggers exist on qualified_businesses?"
- "What are the RLS policies for automation tables?"
- "What indexes are on pipeline_businesses?"
- "Show me all SECURITY DEFINER functions"
- "What views are available?"

### Security Operations
- "How does admin authentication work?"
- "What functions can anon role execute?"
- "Which tables have RLS enabled?"
- "How do internal API tokens work?"
- "What's protected by MFA?"
- "Verify the security configuration"

## How to Use This Skill Effectively

### Step 1: Identify Your Use Case

Ask yourself: "What am I trying to accomplish?"

- **Quick lookup?** → Use `./quick-reference.md`
- **Understanding a table?** → Use `./database-tables-reference.md`
- **Working with functions?** → Use `./rpc-functions-reference.md`
- **Understanding data flow?** → Use `./data-flows-architecture.md`
- **Need to query?** → Use `./supabase-mcp-guide.md`

### Step 2: Use the Right Tool

**For Querying Data:**
```
Use Supabase MCP server tools:
- mcp__supabase__execute_sql - Run any SQL query
- mcp__supabase__list_tables - See all tables
```

**For Understanding Schema:**
```
Read ./database-tables-reference.md for complete table schemas
OR use: mcp__supabase__list_tables with project_id
```

**For Calling Functions:**
```
Use: mcp__supabase__execute_sql with SELECT function_name(params)
Reference: ./rpc-functions-reference.md for function signatures
```

### Step 3: Apply the Knowledge

**Example Workflow: Adding a New Feature**

1. Read `./database-tables-reference.md` to understand where data should go
2. Read `./rpc-functions-reference.md` to see what functions already exist
3. Read `./data-flows-architecture.md` to understand integration points
4. Use `./supabase-mcp-guide.md` to execute changes
5. Check `./triggers-policies-views.md` to ensure triggers/policies are correct

**Example Workflow: Debugging an Issue**

1. Use `./quick-reference.md` for common debugging queries
2. Use Supabase MCP to execute diagnostic queries
3. Check `./triggers-policies-views.md` if issue relates to permissions or triggers
4. Review `./data-flows-architecture.md` to understand expected behavior
5. Use `./rpc-functions-reference.md` to verify function logic

## Common Operations Quick Start

### Check Current Automation Status

```typescript
// Use Supabase MCP
mcp__supabase__execute_sql({
  project_id: "anmmqjpsahrtmavdzotu",
  query: "SELECT * FROM automation_status"
})
```

### Get Queue Statistics

```typescript
// Call RPC function
mcp__supabase__execute_sql({
  project_id: "anmmqjpsahrtmavdzotu",
  query: "SELECT * FROM get_queue_statistics()"
})
```

### Find a Business by UUID

```typescript
mcp__supabase__execute_sql({
  project_id: "anmmqjpsahrtmavdzotu",
  query: "SELECT * FROM qualified_businesses WHERE uuid = 'abc12345'"
})
```

### Check What Triggers Exist

```typescript
mcp__supabase__execute_sql({
  project_id: "anmmqjpsahrtmavdzotu",
  query: `
    SELECT tgname, tgrelid::regclass, pg_get_triggerdef(oid)
    FROM pg_trigger
    WHERE tgisinternal = false
  `
})
```

### See All RPC Functions

```typescript
mcp__supabase__execute_sql({
  project_id: "anmmqjpsahrtmavdzotu",
  query: `
    SELECT proname, pg_get_function_arguments(oid)
    FROM pg_proc
    WHERE pronamespace = 'public'::regnamespace
    ORDER BY proname
  `
})
```

## Key Architectural Concepts

### Project ID
All Supabase operations use: `anmmqjpsahrtmavdzotu`

### Database Roles
- **anon**: Public access (used by admin dashboard via browser)
- **authenticated**: Logged-in users (future state after security hardening)
- **service_role**: Full access (used by API routes and VM)

### Table Relationships

```
Pipeline Flow:
pipeline_businesses → (VM implementation) → qualified_businesses → (outreach trigger) → Smartlead

Automation Management:
automation_config ← controls → automation_status
automation_commands → processed by VM
automation_runs ← logs runs
automation_logs ← logs details

Payment Flow:
qualified_businesses ← stripe_webhook → stripe_events
                                      → stripe_idempotency
```

### Security Architecture (Fully Implemented)

**The system has comprehensive security hardening:**

#### Admin Authentication (MFA Required)
- All `/admin/*` routes require authenticated session with MFA (AAL2)
- Login page: `/admin/login` (email/password + TOTP)
- MFA setup page: `/admin/setup-mfa` (QR code enrollment)
- Logout button in admin header
- Middleware redirects unauthenticated users to login

#### Database Security
- **RLS enabled on ALL 12 tables**
- Dangerous RPC functions revoked from `anon` and `PUBLIC` roles
- Dashboard functions use SECURITY DEFINER to bypass RLS safely
- All functions have `search_path` set to prevent SQL injection

#### API Route Protection
- Admin API routes validate session with MFA
- Internal routes (activate-site, stop-campaign) require `INTERNAL_API_SECRET`
- Stripe webhook validates signature
- Supabase trigger uses Bearer token for start-campaign

#### Function Permissions
- **anon CAN execute**: `get_queue_statistics()`, `get_current_identification_target()`, `get_automation_status()` (SECURITY DEFINER)
- **anon CANNOT execute**: `claim_next_business()`, `send_automation_command()`, `update_automation_config()`, `advance_identification_position()`, `mark_business_deployed()`, `reset_stale_started_businesses()`
- **service_role**: Can execute ALL functions (used by VM and API routes)

## Integration Points

### VM Automation (DigitalOcean 161.35.11.226)

**Identification Process:**
- Uses `service_role` key
- Calls: `advance_identification_position()`, `get_existing_businesses_for_target()`
- Inserts to: `pipeline_businesses`
- Logs to: `automation_logs`, `automation_runs`

**Implementation Process:**
- Uses `service_role` key
- Calls: `claim_next_business()`, `mark_business_deployed()`
- Reads from: `pipeline_businesses`
- Inserts to: `qualified_businesses`

### Admin Dashboard (cliftonsites.com/admin)

**Authentication Required:** MFA (TOTP) verified session

- **Login Flow:** `/admin/login` → email/password → TOTP code → dashboard
- **First-time MFA:** `/admin/setup-mfa` → scan QR code → verify → dashboard
- Uses `anon` key in browser for Realtime subscriptions
- RPC calls via SECURITY DEFINER functions: `get_queue_statistics()`, `get_current_identification_target()`
- API routes for commands (require session): `/api/admin/automation/command`, `/api/admin/automation/config`
- Direct table queries via anon RLS policies: `automation_config`, `automation_status`, `automation_logs`, `automation_runs`

### Outreach System (Smartlead)

- Trigger: `outreach_on_deployed` fires on `qualified_businesses` INSERT/UPDATE
- Calls: `POST /api/outreach/start-campaign` with Bearer token
- Webhook: `POST /api/outreach/webhook-events` receives events from Smartlead
- Updates: `outreach_*` columns in `qualified_businesses`

### Payment System (Stripe)

- Webhook: `POST /api/stripe-webhook` with signature verification
- Logs to: `stripe_events`, `stripe_idempotency`
- Updates: `qualified_businesses` (claimed, stripe_payment_id, customer_email)
- Triggers: Site activation flow

## Best Practices for Using This Skill

1. **Start with the Right Reference**
   - Don't guess - look it up in the appropriate reference file
   - The references are comprehensive - use them

2. **Use Supabase MCP for All Database Operations**
   - Don't try to use psql or other tools
   - The MCP server is your interface to Supabase
   - See `./supabase-mcp-guide.md` for complete examples

3. **Understand the Data Flow**
   - Before changing anything, review `./data-flows-architecture.md`
   - Understand how your change affects the pipeline
   - Check if triggers will fire

4. **Check Permissions**
   - Review `./triggers-policies-views.md` for RLS policies
   - Understand which role is being used
   - Verify access before querying

5. **Reference Function Logic**
   - Don't assume - check `./rpc-functions-reference.md`
   - Functions may have SECURITY DEFINER or INVOKER modes
   - Some functions query tables that are RLS protected

## Troubleshooting Guide

### "Permission denied" errors
1. Check `./triggers-policies-views.md` for RLS policies on that table
2. Verify which role you're using (anon vs service_role)
3. Check if RLS is enabled on the table

### "Function does not exist" errors
1. Verify function name in `./rpc-functions-reference.md`
2. Check schema (should be `public`)
3. Ensure correct parameter types

### "Trigger not firing" issues
1. Review `./triggers-policies-views.md` for trigger definition
2. Check if condition is met (INSERT vs UPDATE)
3. Verify trigger is enabled

### "Empty query results" issues
1. Check if RLS is blocking access
2. Verify data exists in table (use service_role if needed)
3. Review WHERE clause conditions

## Next Steps

Now that you understand how to use this skill:

1. **Read the reference that matches your task** (see Navigation Guide above)
2. **Use the Supabase MCP guide** to execute operations
3. **Refer back to this SKILL.md** if you need to navigate

**Remember:** This skill contains COMPLETE documentation of the entire backend. Everything you need is here - just navigate to the right reference file.
