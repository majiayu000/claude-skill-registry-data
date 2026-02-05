---
name: mcp-bridge
description: >
  Use the MCP Code Execution Bridge for context-efficient access to Supabase and
  shadcn tools. Provides API-based database operations (query, insert, update, delete)
  that work without Docker/MCP servers. Use when you need database access or
  component management without loading all tool definitions into context.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# MCP Code Execution Bridge

Use `scripts/mcp/` for context-efficient MCP tool access. This follows the "Code Execution with MCP" pattern - instead of loading all MCP tool definitions into context, you discover and execute tools through CLI/API wrappers.

## When to Use This Skill

Use the MCP Bridge when:

1. **Database Operations** - Query, insert, update, delete data via REST API
2. **MCP Servers Disabled** - API tools work without MCP servers enabled
3. **No Docker Available** - API tools don't require local Supabase
4. **Reducing Context Overhead** - Avoid loading all MCP definitions upfront
5. **Component Management** - Search and install shadcn components

## MCP Unified Server (Recommended)

For best performance, use the unified HTTP server instead of CLI:

**Start the server:**
```bash
npm run mcp:server
```

**Access the WebUI:**
```
http://localhost:3456/ui
```

**Features:**
- 🚀 ~50ms per call (vs ~800ms CLI)
- 🔄 Hot reload when tools are added
- 🖥️ WebUI for browsing and executing tools
- 📊 Execution history tracking
- 🔒 Single-instance protection

**API Endpoints:**
```bash
# Discovery
curl http://localhost:3456/mcp/servers
curl http://localhost:3456/mcp/stats
curl "http://localhost:3456/mcp/tools/search?q=database"

# Execute tools
curl -X POST http://localhost:3456/mcp/servers/supabase/tools/list-users/run \
  -H "Content-Type: application/json" -d '{}'

# View history
curl http://localhost:3456/mcp/history
```

## Quick Start - Database Queries

**Query a table:**
```bash
npm run mcp -- run supabase query-table '{"table":"profiles","limit":5}'
```

**Query with filters:**
```bash
npm run mcp -- run supabase query-table '{"table":"transactions","select":"id,status,property_address","filter":"status=eq.active","limit":10}'
```

**Insert a row:**
```bash
npm run mcp -- run supabase insert-row '{"table":"contacts","data":{"name":"John","email":"john@example.com"}}'
```

**Update rows:**
```bash
npm run mcp -- run supabase update-rows '{"table":"profiles","filter":"id=eq.abc-123","data":{"name":"Updated"}}'
```

**Delete rows:**
```bash
npm run mcp -- run supabase delete-rows '{"table":"contacts","filter":"id=eq.abc-123"}'
```

## Quick Start - SQL Queries (Most Powerful)

**Execute any SQL:**
```bash
npm run mcp -- run supabase run-sql '{"query":"SELECT * FROM profiles LIMIT 5"}'
```

**List all tables:**
```bash
npm run mcp -- run supabase run-sql '{"query":"SELECT tablename FROM pg_tables WHERE schemaname = '\''public'\'' ORDER BY tablename"}'
```

**Create a table:**
```bash
npm run mcp -- run supabase run-sql '{"query":"CREATE TABLE test (id serial PRIMARY KEY, name text)"}'
```

**Check RLS policies:**
```bash
npm run mcp -- run supabase run-sql '{"query":"SELECT tablename, policyname FROM pg_policies WHERE schemaname = '\''public'\''"}'
```

## Quick Start - Storage

**List buckets:**
```bash
npm run mcp -- run supabase list-buckets '{}'
```

**List files in bucket:**
```bash
npm run mcp -- run supabase list-files '{"bucket":"documents","path":""}'
```

**Get public URL:**
```bash
npm run mcp -- run supabase get-public-url '{"bucket":"images","path":"logo.png"}'
```

**Upload a file from local path (auto-detects content type):**
```bash
npm run mcp -- run supabase upload-file '{"bucket":"documents","path":"contracts/deal.pdf","filePath":"./local/contract.pdf"}'
```

**Upload a file (base64 encoded):**
```bash
npm run mcp -- run supabase upload-file '{"bucket":"documents","path":"contracts/deal.pdf","content":"JVBERi0xLjQK...","contentType":"application/pdf"}'
```

**Download a file:**
```bash
npm run mcp -- run supabase download-file '{"bucket":"documents","path":"contracts/deal.pdf"}'
```

## Quick Start - Auth Admin (User Management)

**Create a user:**
```bash
npm run mcp -- run supabase create-user '{"email":"agent@realty.com","password":"secure123","email_confirm":true}'
```

**List users:**
```bash
npm run mcp -- run supabase list-users '{"page":1,"per_page":50}'
```

**Get user by ID:**
```bash
npm run mcp -- run supabase get-user '{"id":"user-uuid-here"}'
```

**Update user:**
```bash
npm run mcp -- run supabase update-user '{"id":"user-uuid","email":"new@example.com","user_metadata":{"role":"admin"}}'
```

**Ban user for 24 hours:**
```bash
npm run mcp -- run supabase update-user '{"id":"user-uuid","ban_duration":"24h"}'
```

**Delete user:**
```bash
npm run mcp -- run supabase delete-user '{"id":"user-uuid"}'
```

## Quick Start - Edge Functions

**Invoke an Edge Function:**
```bash
npm run mcp -- run supabase invoke-function '{"name":"hello-world","payload":{"name":"John"}}'
```

**Invoke with service role key (for admin functions):**
```bash
npm run mcp -- run supabase invoke-function '{"name":"admin-task","useServiceRole":true,"payload":{"action":"cleanup"}}'
```

**List deployed Edge Functions:**
```bash
npm run mcp -- run supabase list-functions '{}'
```

## Quick Start - TypeScript Types (via API)

**Generate types to console:**
```bash
npm run mcp -- run supabase generate-types-api '{}'
```

**Generate types to file:**
```bash
npm run mcp -- run supabase generate-types-api '{"outputPath":"src/types/database.ts"}'
```

**Generate types with multiple schemas:**
```bash
npm run mcp -- run supabase generate-types-api '{"includedSchemas":["public","auth"]}'
```

## Quick Start - BoldSign E-Signature

**List documents with status filter:**
```bash
npm run mcp -- run boldsign list-documents '{"status":"sent","pageSize":10}'
```

**Get detailed document status:**
```bash
npm run mcp -- run boldsign get-document-status '{"documentId":"your-document-id"}'
```

**Send reminder to pending signers:**
```bash
npm run mcp -- run boldsign send-reminder '{"documentId":"your-document-id"}'
```

**Check webhook processing health:**
```bash
npm run mcp -- run boldsign webhook-health '{"hours":24}'
```

**List recent webhook events:**
```bash
npm run mcp -- run boldsign list-webhook-events '{"limit":20}'
```

**Get audit trail for compliance:**
```bash
npm run mcp -- run boldsign get-audit-trail '{"documentId":"your-document-id","format":"json"}'
```

**List available templates:**
```bash
npm run mcp -- run boldsign list-templates '{"searchTerm":"purchase"}'
```

**Test webhook endpoint:**
```bash
npm run mcp -- run boldsign test-webhook '{"eventType":"document.completed"}'
```

**Check BoldSign configuration:**
```bash
npm run mcp -- run boldsign get-config-status '{}'
```

## Quick Start - Stripe Payments

**List customers:**
```bash
npm run mcp -- run stripe list-customers '{"limit":10}'
```

**Search customer by email:**
```bash
npm run mcp -- run stripe list-customers '{"email":"customer@example.com"}'
```

**Get customer with payment methods:**
```bash
npm run mcp -- run stripe get-customer '{"customerId":"cus_abc123","includePaymentMethods":true}'
```

**List recent payments:**
```bash
npm run mcp -- run stripe list-payments '{"limit":10}'
```

**Get payment details (debug failures):**
```bash
npm run mcp -- run stripe get-payment '{"paymentIntentId":"pi_abc123"}'
```

**List subscriptions by status:**
```bash
npm run mcp -- run stripe list-subscriptions '{"status":"active","limit":10}'
```

**Get subscription with upcoming invoice:**
```bash
npm run mcp -- run stripe get-subscription '{"subscriptionId":"sub_abc123","includeUpcomingInvoice":true}'
```

**List invoices for customer:**
```bash
npm run mcp -- run stripe list-invoices '{"customerId":"cus_abc123","status":"paid"}'
```

**List all products:**
```bash
npm run mcp -- run stripe list-products '{"active":true}'
```

**List subscription prices:**
```bash
npm run mcp -- run stripe list-prices '{"type":"recurring","active":true}'
```

**List prices for a product:**
```bash
npm run mcp -- run stripe list-prices '{"productId":"prod_abc123"}'
```

**Check account balance:**
```bash
npm run mcp -- run stripe get-balance '{}'
```

**List disputes (chargebacks):**
```bash
npm run mcp -- run stripe list-disputes '{"limit":10}'
```

**List webhook events:**
```bash
npm run mcp -- run stripe list-webhook-events '{"type":"payment_intent.succeeded","limit":20}'
```

**Check webhook health:**
```bash
npm run mcp -- run stripe webhook-health '{"hours":24}'
```

**Create test customer (test mode only):**
```bash
npm run mcp -- run stripe create-test-customer '{"email":"test@example.com","addTestPaymentMethod":true}'
```

**Check Stripe configuration:**
```bash
npm run mcp -- run stripe get-config-status '{}'
```

## Available Servers

### Supabase (24 API tools + 6 CLI tools)

**PostgREST API Tools (CRUD operations):**

| Tool | Description | Example |
|------|-------------|---------|
| `query-table` | Query tables via PostgREST | `{"table":"profiles","limit":5}` |
| `insert-row` | Insert a row | `{"table":"contacts","data":{...}}` |
| `update-rows` | Update rows (filter required) | `{"table":"profiles","filter":"id=eq.x","data":{...}}` |
| `delete-rows` | Delete rows (filter required) | `{"table":"contacts","filter":"id=eq.x"}` |

**Management API Tools (SQL execution - MOST POWERFUL):**

| Tool | Description | Example |
|------|-------------|---------|
| `run-sql` | Execute ANY SQL query | `{"query":"SELECT * FROM profiles LIMIT 5"}` |

**Storage Bucket Tools:**

| Tool | Description | Example |
|------|-------------|---------|
| `list-buckets` | List all storage buckets | `{}` |
| `create-bucket` | Create a new bucket | `{"name":"images","public":true}` |
| `delete-bucket` | Delete bucket (must be empty) | `{"name":"old-bucket"}` |
| `get-bucket` | Get bucket details | `{"name":"documents"}` |

**Storage File Tools:**

| Tool | Description | Example |
|------|-------------|---------|
| `list-files` | List files in bucket | `{"bucket":"documents","path":""}` |
| `delete-file` | Delete files | `{"bucket":"documents","paths":["old.pdf"]}` |
| `move-file` | Move/rename file | `{"bucket":"docs","fromPath":"a.pdf","toPath":"b.pdf"}` |
| `get-public-url` | Get public URL (public bucket) | `{"bucket":"images","path":"logo.png"}` |
| `create-signed-url` | Get temporary signed URL | `{"bucket":"docs","path":"contract.pdf"}` |
| `upload-file` | Upload file (from path or base64) | `{"bucket":"docs","path":"file.pdf","filePath":"./local.pdf"}` |
| `download-file` | Download file from bucket | `{"bucket":"docs","path":"contract.pdf"}` |

**Auth Admin API Tools (user management):**

| Tool | Description | Example |
|------|-------------|---------|
| `create-user` | Create a new user | `{"email":"user@example.com","password":"secure123"}` |
| `list-users` | List all users with pagination | `{"page":1,"per_page":50}` |
| `get-user` | Get user by ID | `{"id":"user-uuid"}` |
| `update-user` | Update user properties | `{"id":"user-uuid","email":"new@example.com"}` |
| `delete-user` | Delete a user | `{"id":"user-uuid"}` |

**Edge Function Tools:**

| Tool | Description | Example |
|------|-------------|---------|
| `invoke-function` | Invoke an Edge Function | `{"name":"hello","payload":{"key":"value"}}` |
| `list-functions` | List deployed functions | `{}` |

**Management API Tools (requires access token):**

| Tool | Description | Example |
|------|-------------|---------|
| `run-sql` | Execute ANY SQL query | `{"query":"SELECT * FROM profiles LIMIT 5"}` |
| `generate-types-api` | Generate TypeScript types | `{"outputPath":"src/types/database.ts"}` |

**CLI-Based Tools (require local Supabase/Docker):**

| Tool | Description |
|------|-------------|
| `list-tables` | List tables with schema info |
| `execute-sql` | Execute raw SQL |
| `apply-migration` | Apply DDL migrations |
| `get-logs` | Get service logs |
| `get-advisors` | Security/performance advisors |
| `generate-types` | Generate TypeScript types |

### shadcn (4 tools)

| Tool | Description | Example |
|------|-------------|---------|
| `search-items` | Search components | `{"registries":["@shadcn"],"query":"button"}` |
| `view-items` | View component details | `{"items":["@shadcn/button"]}` |
| `get-examples` | Get usage examples | `{"registries":["@shadcn"],"query":"button-demo"}` |
| `get-add-command` | Get install command | `{"items":["@shadcn/button","@shadcn/card"]}` |

### BoldSign (13 tools)

**Document Management:**

| Tool | Description | Example |
|------|-------------|---------|
| `list-documents` | List/search documents | `{"status":"sent","pageSize":10}` |
| `get-document-status` | Get detailed status with signers | `{"documentId":"abc-123"}` |
| `send-reminder` | Remind pending signers | `{"documentId":"abc-123"}` |
| `extend-expiry` | Extend document deadline | `{"documentId":"abc-123","additionalDays":30}` |

**Document Actions:**

| Tool | Description | Example |
|------|-------------|---------|
| `get-audit-trail` | Get signing events and timestamps | `{"documentId":"abc-123","format":"json"}` |
| `revoke-document` | Cancel pending document | `{"documentId":"abc-123","reason":"Terms changed"}` |

**Template Management:**

| Tool | Description | Example |
|------|-------------|---------|
| `list-templates` | List available templates | `{"searchTerm":"purchase","pageSize":10}` |
| `get-template` | Get template details | `{"templateId":"abc-123"}` |
| `send-from-template` | Send doc from template | `{"templateId":"abc-123","roles":[...]}` |

**Webhook & Debugging:**

| Tool | Description | Example |
|------|-------------|---------|
| `list-webhook-events` | Query webhook history | `{"documentId":"abc-123","limit":10}` |
| `webhook-health` | Check webhook processing | `{"hours":24}` |
| `test-webhook` | Send test webhook payload | `{"eventType":"document.completed"}` |
| `get-config-status` | Check BoldSign config | `{}` |

### Stripe (15 tools)

**Customer Management:**

| Tool | Description | Example |
|------|-------------|---------|
| `list-customers` | List/search customers | `{"email":"user@example.com","limit":10}` |
| `get-customer` | Get customer with payment methods | `{"customerId":"cus_abc","includePaymentMethods":true}` |

**Payment Management:**

| Tool | Description | Example |
|------|-------------|---------|
| `list-payments` | List PaymentIntents | `{"customerId":"cus_abc","status":"succeeded"}` |
| `get-payment` | Get payment with charge details | `{"paymentIntentId":"pi_abc"}` |

**Subscription Management:**

| Tool | Description | Example |
|------|-------------|---------|
| `list-subscriptions` | List subscriptions by status | `{"status":"active","limit":10}` |
| `get-subscription` | Get subscription with billing | `{"subscriptionId":"sub_abc","includeUpcomingInvoice":true}` |

**Product & Pricing:**

| Tool | Description | Example |
|------|-------------|---------|
| `list-products` | List products (plans, one-time) | `{"active":true,"limit":10}` |
| `list-prices` | List prices by product/type | `{"type":"recurring","productId":"prod_abc"}` |

**Invoice Management:**

| Tool | Description | Example |
|------|-------------|---------|
| `list-invoices` | List invoices for customer | `{"customerId":"cus_abc","status":"paid"}` |

**Webhook & Debugging:**

| Tool | Description | Example |
|------|-------------|---------|
| `list-webhook-events` | Query Stripe events | `{"type":"payment_intent.succeeded","limit":20}` |
| `webhook-health` | Check webhook processing | `{"hours":24}` |

**Financial Tools:**

| Tool | Description | Example |
|------|-------------|---------|
| `get-balance` | Get account balance | `{}` |
| `list-disputes` | List chargebacks | `{"limit":10}` |

**Testing Tools:**

| Tool | Description | Example |
|------|-------------|---------|
| `create-test-customer` | Create test customer (test mode) | `{"email":"test@example.com","addTestPaymentMethod":true}` |
| `get-config-status` | Check Stripe config | `{}` |

## PostgREST Filter Syntax

The `filter` parameter uses PostgREST syntax:

| Operator | Meaning | Example |
|----------|---------|---------|
| `eq` | Equals | `status=eq.active` |
| `neq` | Not equals | `status=neq.cancelled` |
| `gt` | Greater than | `price=gt.100000` |
| `gte` | Greater than or equal | `price=gte.100000` |
| `lt` | Less than | `price=lt.500000` |
| `lte` | Less than or equal | `price=lte.500000` |
| `like` | Pattern match | `name=like.*John*` |
| `ilike` | Case-insensitive pattern | `name=ilike.*john*` |
| `in` | In list | `status=in.(active,pending)` |
| `is` | Is null/true/false | `deleted_at=is.null` |

**Multiple filters:** Use `&` to combine: `status=eq.active&agent_id=eq.abc-123`

## CLI Commands Reference

```bash
# Discovery
npm run mcp:list                     # List servers
npm run mcp -- list-tools supabase   # List tools
npm run mcp -- describe supabase query-table  # Tool details
npm run mcp:search "database"        # Search tools

# Execution
npm run mcp -- run <server> <tool> '<json>'

# Execution Flags
npm run mcp -- run supabase list-users '{}' --quiet  # Data only, no metadata wrapper
npm run mcp -- run supabase run-sql --input-file query.json  # Read JSON from file (Windows-friendly)

# Convenience Shortcuts
npm run mcp:count transactions       # Quick row count for any table
npm run mcp:users                    # List users (formatted)
npm run mcp:users -- --json          # List users (raw JSON)

# Maintenance
npm run mcp:registry                 # Regenerate after adding tools
```

## CLI Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--quiet`, `-q` | Output data only (no metadata wrapper) | `--quiet` |
| `--input-file`, `-f` | Read JSON input from file | `--input-file input.json` |

**Use `--quiet` for scripting:**
```bash
# Get just the data, no wrapper
npm run mcp -- run supabase list-users '{}' --quiet
```

**Use `--input-file` for Windows or complex JSON:**
```bash
# Create input file
echo '{"query": "SELECT * FROM profiles LIMIT 5"}' > query.json

# Run with file input
npm run mcp -- run supabase run-sql --input-file query.json
```

## Tool Discovery Pattern

```bash
# 1. Find relevant tools
npm run mcp:search "query"

# 2. Get tool details and input schema
npm run mcp -- describe supabase query-table

# 3. Execute with JSON input
npm run mcp -- run supabase query-table '{"table":"profiles"}'
```

## Error Handling

All tools return structured results:

```json
{
  "success": true,
  "data": [...],
  "metadata": {
    "tool": "query-table",
    "server": "supabase",
    "executionTimeMs": 150,
    "executionType": "api"
  }
}
```

**Error response:**
```json
{
  "success": false,
  "error": {
    "code": "HTTP_400",
    "message": "HTTP 400: Bad Request",
    "details": {
      "hint": "Perhaps you meant to reference the column..."
    }
  }
}
```

## Environment Variables

API tools use credentials from `.env`:

```bash
# PostgREST and Storage API
VITE_SUPABASE_URL=https://xxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...
VITE_SUPABASE_SERVICE_ROLE_KEY=eyJ...

# Management API (required for run-sql)
SUPABASE_ACCESS_TOKEN=sbp_xxx...

# Stripe API (required for stripe tools)
STRIPE_SECRET_KEY=sk_test_xxx...  # or sk_live_... for production
STRIPE_WEBHOOK_SECRET=whsec_xxx...
```

Get Supabase access token from: Supabase Dashboard > Account > Access Tokens
Get Stripe keys from: Stripe Dashboard > Developers > API keys

## Creating New Tools

See [ADDING-TOOLS.md](ADDING-TOOLS.md) for step-by-step guide.

**Quick steps:**
1. Add types to `scripts/mcp/types/<server>.types.ts`
2. Create wrapper at `scripts/mcp/servers/<server>/<tool-name>.ts`
3. Export from `scripts/mcp/servers/<server>/index.ts`
4. Run `npm run mcp:registry`

## See Also

- [ADDING-TOOLS.md](ADDING-TOOLS.md) - Creating new tools
- [REFERENCE.md](REFERENCE.md) - Complete API reference
- `scripts/mcp/README.md` - Bridge documentation
