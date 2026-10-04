---
name: royalti-api
description: Royalti.io REST API v2.6 pattern reference for developers. Covers authentication, CRUD patterns, pagination, error handling, webhooks, WebSocket events, data models, DDEX distribution, AI chat, source creator, global search, checklist workflows, music publishing, billing, and more. Use when helping developers integrate with the Royalti API (api.royalti.io) or when writing integration code, API documentation, or troubleshooting API issues.
license: MIT
compatibility: Works with Claude Code, Claude Desktop, Cursor, OpenAI Codex, GitHub Copilot, OpenClaw, Gemini CLI, Amp, Goose, Roo Code, OpenCode, Letta, and any tool supporting the Agent Skills open standard.
metadata:
  author: Royalti.io
  version: "2.1.0"
---

# Royalti API v2.6 — Developer Reference

Pattern reference for integrating with the Royalti.io REST API.

**Base URL:** `https://api.royalti.io`
**Current Version:** 2.6.4
**Architecture:** Multi-tenant (workspace-scoped)

---

## 1. Authentication

### Token Types

| Token | Prefix | Expiry | Use Case |
|-------|--------|--------|----------|
| JWT Access Token | — | 6 hours | All API requests |
| JWT Refresh Token | — | 1 day | Obtain new access tokens |
| Workspace API Key | `RWAK` | Never (revocable) | Programmatic workspace access |
| User API Key | `RUAK` | Never (revocable) | Programmatic user access |

### Two-Step JWT Login

```bash
# Step 1: Login — returns refresh token + workspace list
curl -X POST https://api.royalti.io/auth/login \
  -H "Content-Type: application/json" \
  -d '{ "email": "user@example.com", "password": "secret" }'

# Response:
# {
#   "refresh_token": "eyJ...",
#   "workspaces": [{ "id": "ws_abc", "name": "My Label", ... }]
# }

# Step 2: Exchange refresh token for access token (scoped to a workspace)
curl https://api.royalti.io/auth/authtoken?currentWorkspace=ws_abc \
  -H "Authorization: Bearer <refresh_token>"

# Response:
# { "data": { "access_token": "eyJ..." } }
```

### Using the Access Token

All subsequent requests include the access token:

```bash
curl https://api.royalti.io/artist/ \
  -H "Authorization: Bearer <access_token>"
```

### API Key Authentication

API keys can be used instead of JWT tokens. Pass them in the `Authorization` header:

```bash
# Workspace API key
curl https://api.royalti.io/artist/ \
  -H "Authorization: Bearer RWAK_abc123..."

# User API key
curl https://api.royalti.io/asset \
  -H "Authorization: Bearer RUAK_def456..."
```

### API Key Auth Resolution (Internals)

Understanding how RWAK/RUAK keys resolve to a workspace context helps debug auth errors:

```
1. Token prefix detected as RWAK/RUAK (not JWT)
2. ApiKeys table lookup → finds TenantId
3. Tenants table lookup → finds workspace (must be status='active')
4. Tenants.user field → used to find the owner TenantUser via TenantUser.findByPk()
5. Owner TenantUser populates req.user for all downstream handlers
```

**Key detail:** `Tenants.user` must store a `TenantUser.id` (UUID), NOT a `User.id`. These are different tables with different PKs. If this field is wrong, the API returns `"Workspace user not found"` (HTTP 404) despite the API key being valid.

The `Tenants.user` field is also used by:
- **Accounting endpoints** — to exclude the workspace owner from payee/due calculations
- **Admin auth** — to resolve workspace context for admin JWT tokens

### Other Auth Methods

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `POST /auth/loginlink` | POST | Magic link login |
| `POST /auth/forgotpassword` | POST | Request password reset |
| `PATCH /auth/resetpassword?code=CODE` | PATCH | Apply password reset |
| `GET /auth/google` | GET | Google OAuth |
| `GET /auth/linkedin` | GET | LinkedIn OAuth |
| `GET /auth/facebook` | GET | Facebook OAuth |

### Rate Limiting

- Login endpoint: **20 requests per 3 minutes** per IP
- AI endpoints: Rate limited per tenant subscription tier (billing-period aligned)
- Other endpoints: No documented limits (subject to fair use)

### RBAC Roles (ascending privilege)

```
guest < user < admin < owner < super_admin < main_super_admin
```

### Feature Gating

Certain API features require subscription-level feature flags:

| Feature Flag | Required For |
|-------------|-------------|
| `royaltyAccess` | Royalty file upload, source creator, analytics |
| `aiAgent` | AI chat conversations and messages |
| `addonsAccess` | DDEX, Merlin, Publisher addons |

Addon-specific checks: `ddex`, `publisher`, `merlin` — require the addon to be enabled on the tenant.

---

## 2. Request Patterns

### Standard Headers

```
Authorization: Bearer <access_token | API_KEY>
Content-Type: application/json
```

### Pagination (all list endpoints)

| Param | Default | Description |
|-------|---------|-------------|
| `page` | `1` | Page number |
| `size` | `10`–`20` | Items per page (max `100`) |
| `sort` | `updatedAt` | Sort field |
| `order` | `desc` | `asc` or `desc` |

```bash
GET /artist/?page=2&size=25&sort=artistName&order=asc
```

### Filtering (analytics endpoints)

| Param | Type | Description |
|-------|------|-------------|
| `start` | `YYYY-MM-DD` | Date range start |
| `end` | `YYYY-MM-DD` | Date range end |
| `dsp` | CSV string | Filter by DSP/platform |
| `country` | CSV string | Filter by territory (ISO 3166-1 alpha-2) |
| `artists` | CSV string | Filter by artist IDs |
| `upc` | CSV string | Filter by UPC |
| `isrc` | CSV string | Filter by ISRC |
| `aggregator` | CSV string | Filter by distributor |
| `type` | string | Filter by sale type |
| `periodFilterType` | `accounting` or `sale` | Date filtering mode |
| `includePreviousPeriod` | boolean | Include comparison data |
| `table_name` | string | Filter by royalty file source table |

### Search

Many list endpoints support a `search` query param for text-based filtering:

```bash
GET /artist/?search=drake&page=1&size=10
```

### Bulk Operations

Most resources support bulk create and delete:

```bash
POST /artist/bulk          # Create multiple artists
DELETE /artist/bulk/delete  # Delete multiple artists
POST /asset/bulksplits     # Assign splits to multiple assets
```

---

## 3. Response Patterns

### Success Response

```json
{
  "status": "success",
  "message": "Operation successful",
  "data": { ... }
}
```

### Paginated List Response

Response shapes vary by resource. Most use `data[]`, but some use resource-specific keys:

```json
// Standard shape (labels, splits, payments, expenses, revenue, notifications)
{
  "status": "success",
  "data": [ ... ],
  "totalItems": 142,
  "totalPages": 15,
  "currentPage": 1
}

// Users — uses "Users" key, no "status" field
{
  "message": "success",
  "totalItems": 10,
  "Users": [ ... ],
  "totalPages": 1,
  "currentPage": 1
}

// Artists — uses "Artists" key, includes "filteredItems"
{
  "totalItems": 50,
  "Artists": [ ... ],
  "totalPages": 5,
  "currentPage": 1,
  "filteredItems": 50
}

// Products — uses "Products" key
// Assets — uses "data" key
```

**Tip:** Always check for both `data` and the resource-specific key (e.g., `Users`, `Artists`, `Products`) when parsing list responses.

### Summary Response (v2.6.4+)

Available on: `/artist/summary`, `/asset/summary`, `/product/summary`, `/user/summary`, `/split/summary`, `/payment/summary`, `/expense/summary`, `/revenue/summary`, `/file/summary`

```json
{
  "message": "Summary retrieved successfully",
  "summary": {
    "total": 250,
    "byStatus": { "active": 200, "inactive": 50 },
    "byFormat": { "Single": 120, "Album": 80, "EP": 50 },
    "byType": { "Audio": 230, "Video": 20 },
    "revenue": { "total": 15000.50, "currency": "USD" }
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": ["optional", "array", "of", "details"]
  }
}
```

### Common HTTP Status Codes

| Code | Meaning |
|------|---------|
| `200` | Success |
| `201` | Created |
| `400` | Bad request / validation error |
| `401` | Unauthorized (missing or invalid token) |
| `403` | Forbidden (insufficient role/permissions) |
| `404` | Resource not found |
| `409` | Conflict (duplicate, schema disparity) |
| `422` | Unprocessable entity |
| `429` | Rate limited |
| `500` | Server error |

---

## 4. Core Resources

All resources follow the same CRUD pattern unless noted. Every resource is workspace-scoped (multi-tenant).

### Standard CRUD Pattern

```
GET    /{resource}/          # List (paginated)
POST   /{resource}/          # Create
GET    /{resource}/{id}      # Get by ID
PUT    /{resource}/{id}      # Update
DELETE /{resource}/{id}      # Delete
GET    /{resource}/summary   # Summary stats (v2.6.4+)
GET    /{resource}/download/csv  # CSV export
POST   /{resource}/bulk      # Bulk create
DELETE /{resource}/bulk/delete   # Bulk delete
```

### Users (`/user/`)

Standard CRUD plus:

| Endpoint | Description |
|----------|-------------|
| `GET /user/{id}/stats` | User royalty statistics |
| `GET /user/{id}/monthly` | Monthly breakdown |
| `GET /user/{id}/artists` | User's artists |
| `GET /user/{id}/assets` | User's assets |
| `GET /user/{id}/products` | User's products |
| `GET /user/{id}/aut` | User accounting data |
| `GET /user/invites` | Pending invitations |
| `POST /user/invites/{id}/resend` | Resend invitation |
| `POST /user/invites/{id}/cancel` | Cancel invitation |

### Artists (`/artist/`)

Standard CRUD plus:

| Endpoint | Description |
|----------|-------------|
| `GET /artist/{id}/assets` | Artist's tracks |
| `GET /artist/{id}/products` | Artist's releases |
| `GET /artist/{id}/splits` | Artist's splits |
| `GET /artist/{id}/splits/{type}` | Splits by type |
| `PUT /artist/{id}/splits/{type}` | Update split by type |
| `DELETE /artist/{id}/splits/{type}` | Delete split by type |
| `POST /artist/{id}/splits` | Create artist default split |
| `GET /artist/{id}/stats` | Artist analytics |
| `POST /artist/{id}/merge` | Merge duplicate artists |
| `POST /artist/bulksplit` | Bulk assign splits |
| `POST /artist/download/csv` | Download artist CSV |

Key fields: `artistName`, `signDate`, `label`, `publisher`, `copyright`, `externalId`, `artistImg`, `links` (spotify/youtube/instagram/etc.), `genres`, `realName`, `pseudonyms`

### Assets / Tracks (`/asset`)

Standard CRUD plus:

| Endpoint | Description |
|----------|-------------|
| `GET /asset/{id}/artists` | Track's artists |
| `GET /asset/{id}/stats` | Track analytics |
| `POST /asset/{id}/setdefaultsplit` | Set default split |
| `GET /asset/{id}/media` | Track media files |
| `DELETE /asset/{id}/media/{mediaName}` | Delete media |
| `GET /asset/{id}/ddex-metadata` | DDEX metadata |
| `GET /asset/{id}/ddex-readiness` | DDEX readiness check |
| `GET /asset/{assetId}/works` | Musical works (ISWC) |
| `POST /asset/bulksplits` | Bulk assign splits |
| `DELETE /asset/bulk/deletesplit` | Bulk remove splits |
| `POST /asset/bulk/defaultsplit` | Bulk set default splits |

Key fields: `title`, `ISRC`, `type` (Audio|Video|Ringtone|YouTube), `version`, `displayArtist`, `mainArtist[]`, `mainGenre[]`, `subGenre[]`, `explicit`, `language`, `tempo`, `key`, `mood[]`, `lyrics`, `label`, `copyright`, `publisher`

### Products / Releases (`/product/`)

Standard CRUD plus:

| Endpoint | Description |
|----------|-------------|
| `GET /product/{id}/artists` | Release's artists |
| `GET /product/{id}/assets` | Release's tracks |
| `GET /product/{id}/stats` | Release analytics |
| `POST /product/{id}/setdefaultsplit` | Set default split |
| `GET /product/{id}/media` | Release artwork/media |
| `GET /product/{id}/delivery` | Delivery info |
| `GET /product/{id}/delivery/status` | Delivery status |
| `POST /product/batch-delivery` | Batch deliver releases |
| `GET /product/{id}/deliveries` | Delivery history |
| `POST /product/{id}/deliveries/{deliveryId}/retry` | Retry failed delivery |
| `GET /product/delivery-providers` | Available distributors |
| `GET /product/download/metadata` | Metadata export |

Key fields: `title`, `UPC`, `format` (Single|EP|Album|LP), `release_date`, `takedown_date`, `label`, `display_artist`, `type` (Audio|Video), `catalog_number`, `status` (active|inactive|pending|Live|Taken Down|Scheduled|Error), `distribution`, `external_id`

### Splits (`/split/`)

Standard CRUD plus:

| Endpoint | Description |
|----------|-------------|
| `POST /split/default` | Create split from artist default |
| `POST /split/match` | Find splits matching criteria |
| `DELETE /split/bulk/catalog-splits` | Remove catalog-level splits |

Split types: `simple`, `conditional`, `temporal`

```json
{
  "entity_type": "artist",
  "entity_id": "uuid",
  "split_type": "conditional",
  "effective_date": "2025-01-01",
  "shares": [
    { "user": "user-uuid-1", "percentage": 60 },
    { "user": "user-uuid-2", "percentage": 40 }
  ],
  "conditions": {
    "territories": ["US", "GB", "CA"],
    "mode": "include",
    "sources": ["Spotify", "Apple Music"],
    "period_start": "2025-01-01",
    "period_end": "2025-12-31",
    "memo": "North America streaming deal"
  }
}
```

**Rules:** Shares must sum to 100. `entity_type` is `artist`, `product`, or `asset`. Conditions are optional (omit for simple splits).

### Royalties / Analytics (`/royalty/`)

Read-only analytics endpoints. All support the standard filter params (start, end, dsp, country, etc.). Requires `royaltyAccess` feature.

| Endpoint | Description |
|----------|-------------|
| `GET /royalty/` | Main summary |
| `GET /royalty/month` | Monthly trends |
| `GET /royalty/dsp` | By DSP/platform |
| `GET /royalty/country` | By country/territory |
| `GET /royalty/artist` | By artist |
| `GET /royalty/product` | By product/release |
| `GET /royalty/asset` | By track |
| `GET /royalty/tables` | By data source |
| `GET /royalty/saletype` | By sale type (stream, download, etc.) |
| `GET /royalty/aggregator` | By distributor |
| `GET /royalty/accountingperiod` | By accounting period |

Analytics response shape:

```json
{
  "Downloads": 1500,
  "Streams": 250000,
  "Royalty": 1234.56,
  "Count": 251500,
  "RatePer1K": 4.91,
  "RoyaltyPercentage": 45.2,
  "CountPercentage": 38.7,
  "PreviousRoyalty": 1100.00,
  "PreviousCount": 220000
}
```

`PreviousRoyalty` and `PreviousCount` are only present when `includePreviousPeriod=true`.

### Accounting (`/accounting/`)

| Endpoint | Description |
|----------|-------------|
| `GET /accounting/{id}/stats` | User accounting stats |
| `GET /accounting/transactions` | Transaction list |
| `GET /accounting/transactions/summary` | Transaction summary |
| `GET /accounting/transactions/monthly` | Monthly transaction breakdown |
| `GET /accounting/getcurrentdue` | Current amount due per user |
| `GET /accounting/gettotaldue` | Total outstanding across workspace |
| `POST /accounting/refresh` | Recalculate accounting |
| `POST /accounting/refreshstats` | Refresh stats cache |
| `POST /accounting/users/{id}/recalculate` | Recalculate single user |
| `POST /accounting/tenant/recalculate` | Recalculate entire workspace |
| `GET /accounting/queue/status` | Processing queue status |

### Payments (`/payment/`)

Standard CRUD. Supports both JSON and `multipart/form-data` (for attaching receipts).

| Endpoint | Description |
|----------|-------------|
| `GET /payment/summary` | Payment totals |
| `POST /payment/bulk` | Bulk create payments |

### Payment Requests (`/payment-request/`)

| Endpoint | Description |
|----------|-------------|
| `GET /payment-request/` | List requests |
| `GET /payment-request/{id}` | Get request |
| `POST /payment-request/{id}/approve` | Approve request |
| `POST /payment-request/{id}/decline` | Decline request |

### Royalty Files (`/file/`)

| Endpoint | Description |
|----------|-------------|
| `GET /file/royalty` | List uploaded royalty files |
| `GET /file/royalty/{id}` | Get file details |
| `DELETE /file/royalty/{id}` | Delete file |
| `GET /file/summary` | File summary stats |
| `POST /file/createroyalty` | Upload royalty file |
| `GET /file/upload-url` | Get presigned upload URL |
| `POST /file/confirm-upload-completion` | Confirm upload finished |
| `GET /file/detection/{sessionId}` | Poll auto-detection status |
| `POST /file/confirm-detection/{sessionId}` | Confirm detected format |
| `GET /file/auto-processing-config` | Auto-processing settings |
| `POST /file/enable-auto-processing` | Enable auto-processing |
| `GET /file/sources` | List royalty sources (DSPs) |
| `GET /file/{id}/download` | Download file |
| `GET /file/processing/{jobId}` | Processing job status |
| `POST /file/session/{sessionId}/start-source-creator` | Bridge to source creator for unknown formats |
| `POST /file/upload-from-drive` | Upload from Google Drive |

### Labels (`/labels/`)

Standard CRUD plus:

| Endpoint | Description |
|----------|-------------|
| `GET /labels/hierarchy` | Label tree structure |

### Releases (`/releases`)

Full release lifecycle with media management:

**Release CRUD:**

| Endpoint | Description |
|----------|-------------|
| `POST /releases` | Create release (draft) |
| `GET /releases` | List releases |
| `GET /releases/stats` | Release statistics |
| `GET /releases/{id}` | Get release details |
| `PUT /releases/{id}` | Update release |
| `DELETE /releases/{id}` | Delete release |

**Lifecycle Workflow:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `POST /releases/{id}/submit` | user | Submit for review |
| `POST /releases/{id}/review` | admin | Start review |
| `POST /releases/{id}/feedback` | admin | Add feedback |
| `POST /releases/{id}/revert-status` | admin | Revert release status |

**Release Media:**

| Endpoint | Description |
|----------|-------------|
| `POST /releases/{id}/media/files` | Upload release files (artwork, etc.) |
| `POST /releases/{id}/media/links` | Submit release links |
| `GET /releases/{id}/media` | Get release media |
| `DELETE /releases/{id}/media/{mediaId}` | Delete release media |

**Track Management:**

| Endpoint | Description |
|----------|-------------|
| `POST /releases/{id}/tracks` | Create track in release |
| `PUT /releases/{id}/tracks/{trackId}` | Update track |
| `DELETE /releases/{id}/tracks/{trackId}` | Delete track |
| `POST /releases/{id}/tracks/reorder` | Reorder release tracks |
| `POST /releases/{id}/tracks/link-asset` | Link existing asset to release |

**Track Media:**

| Endpoint | Description |
|----------|-------------|
| `POST /releases/{id}/tracks/{trackId}/media/file` | Upload track audio/video file |
| `POST /releases/{id}/tracks/{trackId}/media/link` | Submit track link |
| `GET /releases/{id}/tracks/{trackId}/media` | Get track media |
| `DELETE /releases/{id}/tracks/{trackId}/media/{mediaId}` | Delete track media |

### Expenses & Revenue

Both follow standard CRUD at `/expense/` and `/revenue/` with summary endpoints.

### Notifications (`/notifications/`)

| Endpoint | Description |
|----------|-------------|
| `GET /notifications/` | List notifications |
| `PATCH /notifications/{id}/read` | Mark as read |
| `PATCH /notifications/read-all` | Mark all as read |
| `GET /notifications/unread-count` | Unread count |

### Downloads / Reports (`/download/`)

| Endpoint | Description |
|----------|-------------|
| `POST /download/generate` | Generate report download |
| `GET /download/{id}/status` | Check generation status |
| `GET /download/list` | List available downloads |

---

## 5. Global Search (`/search`)

Cross-entity search across the entire catalog.

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /search?q={query}&types={types}` | user | Global search |
| `GET /search/recent` | user | Get recent searches |
| `DELETE /search/recent` | user | Clear search history |

**Query Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| `q` | string | Search query text |
| `types` | CSV string | Entity types to search (e.g., `artist,product,asset,user`) |

---

## 6. Royalty Sources (`/sources`)

Manage royalty data sources (DSPs, distributors, custom sources).

**Tenant Routes:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /sources` | user | List tenant's royalty sources |
| `POST /sources` | user | Create new tenant source |
| `GET /sources/{id}` | user | Get source details |
| `PUT /sources/{id}` | user | Update source |
| `DELETE /sources/{id}` | user | Delete source |
| `POST /sources/{id}/activate` | user | Activate source |
| `POST /sources/{id}/deactivate` | user | Deactivate source |

---

## 7. Source Creator (`/source-creator`)

AI-powered wizard for creating new royalty source definitions. Requires `royaltyAccess` feature.

**Analysis & Mapping:**

| Endpoint | Description |
|----------|-------------|
| `POST /source-creator/analyze` | Upload and analyze file (multipart) |
| `POST /source-creator/ai-map-columns` | Get AI column mapping suggestions (rate limited) |
| `PUT /source-creator/sessions/{id}/mappings` | Save user-confirmed mappings |
| `PUT /source-creator/sessions/{id}/periods` | Confirm accounting periods |
| `POST /source-creator/sessions/{id}/suggest-name` | Get smart name suggestion |

**Query Generation & Testing:**

| Endpoint | Description |
|----------|-------------|
| `POST /source-creator/generate-queries` | Generate BigQuery SQL from mappings (rate limited) |
| `POST /source-creator/test-queries` | Test queries against sample data |

**Save & Reuse:**

| Endpoint | Description |
|----------|-------------|
| `POST /source-creator/save` | Save as draft source |
| `POST /source-creator/reuse` | Reuse existing source for new file |
| `GET /source-creator/sources/{id}/mappings` | Get source column mappings |
| `GET /source-creator/sources/{id}/queries` | Get source queries |

**Session Management:**

| Endpoint | Description |
|----------|-------------|
| `GET /source-creator/sessions` | List sessions |
| `GET /source-creator/sessions/{id}` | Get session details |
| `DELETE /source-creator/sessions/{id}` | Delete session |

**Admin Routes** (super admin only):

| Endpoint | Description |
|----------|-------------|
| `GET /source-creator/admin/drafts` | List all draft sources across tenants |
| `GET /source-creator/admin/sessions/{id}` | Get full session detail |
| `POST /source-creator/admin/{id}/promote` | Promote draft to global source |

### Source Creator Flow

```
1. POST /source-creator/analyze              → Upload file, get column analysis
2. POST /source-creator/ai-map-columns       → Get AI mapping suggestions
3. PUT  /source-creator/sessions/{id}/mappings → Confirm mappings
4. PUT  /source-creator/sessions/{id}/periods  → Confirm accounting periods
5. POST /source-creator/generate-queries      → Generate BigQuery SQL
6. POST /source-creator/test-queries          → Validate against sample data
7. POST /source-creator/save                  → Save as draft source
   (Admin) POST /source-creator/admin/{id}/promote → Promote to global
```

---

## 8. Checklist / Data Quality (`/checklist`)

Data quality validation, catalog enrichment, and workflow orchestration. Requires admin role.

**Validation Checks:**

| Endpoint | Description |
|----------|-------------|
| `GET /checklist/royaltyassets` | Assets appearing in royalty data but not in catalog |
| `GET /checklist/royaltyproducts` | Products appearing in royalty data but not in catalog |
| `GET /checklist/assetsplits` | Assets missing split assignments |
| `GET /checklist/productsplits` | Products missing split assignments |
| `GET /checklist/allsplits` | All split coverage issues |
| `GET /checklist/missingroyaltysplits` | Royalty items without splits |
| `GET /checklist/artistsplits` | Artist split user issues |
| `GET /checklist/missingprimaryartists` | Assets/products missing primary artists |
| `GET /checklist/duplicateartists` | Duplicate artist detection |
| `GET /checklist/productswithoutassets` | Products with no linked assets |
| `GET /checklist/assetswithoutproducts` | Assets with no linked products |

**Import from Royalty Data:**

| Endpoint | Description |
|----------|-------------|
| `POST /checklist/royaltyassets/import` | Import missing assets from royalty data |
| `POST /checklist/royaltyproducts/import` | Import missing products from royalty data |

**Catalog Enrichment:**

| Endpoint | Description |
|----------|-------------|
| `POST /checklist/assets/enrich` | Enrich assets with external metadata |
| `POST /checklist/products/enrich` | Enrich products with external metadata |
| `GET /checklist/enrichment` | List enrichment items |
| `GET /checklist/enrichment/job/{jobId}` | Get enrichment job status |
| `GET /checklist/enrichment/{id}` | Get enrichment item details |
| `PUT /checklist/enrichment/{id}` | Update enrichment item |
| `POST /checklist/enrichment/approve` | Approve enrichment items |
| `POST /checklist/enrichment/reject` | Reject enrichment items |
| `POST /checklist/enrichment/re-enrich` | Re-enrich rejected items |
| `POST /checklist/enrichment/cleanup` | Cleanup enrichment items |

**Workflow Orchestration:**

| Endpoint | Description |
|----------|-------------|
| `POST /checklist/workflow` | Start a checklist workflow |
| `GET /checklist/workflow` | List workflows |
| `GET /checklist/workflow/{id}` | Get workflow details |
| `POST /checklist/workflow/{id}/respond` | Respond to workflow prompt |
| `POST /checklist/workflow/{id}/cancel` | Cancel workflow |

---

## 9. DDEX Distribution (`/ddex`)

Digital Data Exchange standard support for release distribution. Requires `addonsAccess` feature + `ddex` addon.

**ERN (Electronic Release Notification):**

| Endpoint | Role | Description |
|----------|------|-------------|
| `POST /ddex/ern/generate` | admin | Generate ERN message for a release |
| `POST /ddex/ern/generate-batch` | admin | Generate multiple ERN messages |

**MEAD (Music Enrichment and Description):**

| Endpoint | Role | Description |
|----------|------|-------------|
| `POST /ddex/mead/generate` | admin | Generate MEAD message |
| `PUT /ddex/mead/{entityId}` | admin | Update MEAD metadata |

**Message Management:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /ddex/messages` | user | List all DDEX messages |
| `GET /ddex/messages/{messageId}` | user | Get message details |
| `POST /ddex/messages/{messageId}/validate` | admin | Validate message |
| `GET /ddex/messages/{messageId}/download` | admin | Download message XML |

**Delivery:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `POST /ddex/delivery/deliver/{messageId}` | admin | Deliver message to provider |
| `POST /ddex/delivery/deliver-batch` | admin | Batch delivery |
| `POST /ddex/delivery/retry/{messageId}` | admin | Retry failed delivery |
| `GET /ddex/delivery/status/{messageId}` | user | Get delivery status |
| `GET /ddex/delivery/logs/{messageId}` | admin | Get delivery logs |
| `POST /ddex/delivery/test-connection` | owner | Test DSP connection |
| `POST /ddex/delivery/test-all-connections` | owner | Test all provider connections |

**Provider Management:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /ddex/providers` | user | List available DSP providers |
| `GET /ddex/providers/{providerId}` | user | Get provider details |
| `GET /ddex/providers/{providerId}/stats` | user | Get provider statistics |

**Tenant Provider Configuration:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /ddex/tenant-providers` | admin | List tenant's configured providers |
| `POST /ddex/tenant-providers` | owner | Configure new provider |
| `PUT /ddex/tenant-providers/{id}` | owner | Update provider config |
| `DELETE /ddex/tenant-providers/{id}` | owner | Remove provider config |

**Queue & Monitoring:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /ddex/queue/jobs` | admin | List queue jobs |
| `GET /ddex/queue/jobs/{jobId}` | admin | Get job details |
| `GET /ddex/queue/jobs/{jobId}/logs` | admin | Get job logs |
| `GET /ddex/monitoring/dashboard` | admin | Monitoring dashboard |

**Usage:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /ddex/usage` | admin | Get DDEX usage stats |
| `GET /ddex/usage/dashboard` | admin | Usage dashboard |

### DDEX Distribution Flow

```
1. POST /ddex/tenant-providers                    → Configure DSP provider (one-time)
2. POST /ddex/delivery/test-connection            → Verify connection
3. POST /ddex/ern/generate { releaseId }          → Generate ERN message
4. POST /ddex/messages/{messageId}/validate       → Validate message
5. POST /ddex/delivery/deliver/{messageId}        → Deliver to DSP
6. GET  /ddex/delivery/status/{messageId}         → Monitor delivery status
   If failed: POST /ddex/delivery/retry/{messageId}
```

---

## 10. AI Chat Agent (`/ai`)

Conversational AI assistant with workspace context. Requires `aiAgent` feature. Supports Vercel AI SDK streaming.

**Conversations:**

| Endpoint | Description |
|----------|-------------|
| `POST /ai/conversations` | Create conversation |
| `GET /ai/conversations` | List conversations |
| `GET /ai/conversations/{conversationId}` | Get conversation |
| `PUT /ai/conversations/{conversationId}` | Update conversation |
| `DELETE /ai/conversations/{conversationId}` | Archive conversation |

**Messages:**

| Endpoint | Description |
|----------|-------------|
| `GET /ai/conversations/{conversationId}/messages` | Get messages |
| `POST /ai/conversations/{conversationId}/messages` | Send message (rate limited) |
| `POST /ai/chat` | Vercel AI SDK streaming chat |

**Status & Configuration:**

| Endpoint | Description |
|----------|-------------|
| `GET /ai/health` | Health check (public) |
| `GET /ai/rate-limit` | Check rate limit status |
| `GET /ai/budget-status` | Check cost budget status |
| `GET /ai/suggestions` | Get context-aware follow-up suggestions |
| `GET /ai/config` | Get AI configuration |
| `POST /ai/feedback` | Submit conversation feedback |
| `GET /ai/conversations/{conversationId}/stats` | Conversation stats |

**Retention Config (admin):**

| Endpoint | Description |
|----------|-------------|
| `GET /ai/retention-config` | Get retention policy |
| `PUT /ai/retention-config` | Update retention policy |
| `POST /ai/retention/apply-now` | Apply retention immediately |

### AI Chat Streaming

The `/ai/chat` endpoint supports Vercel AI SDK streaming format:

```bash
POST /ai/chat
Content-Type: application/json

{
  "messages": [
    { "role": "user", "content": "What are my top performing artists this quarter?" }
  ],
  "conversationId": "optional-conversation-uuid"
}
```

The response is a server-sent event stream compatible with `useChat()` from the Vercel AI SDK.

---

## 11. Merlin Addon (`/merlin`)

Automated royalty file import via FTP with approval workflows. Requires `addonsAccess` feature + `merlin` addon.

**Configuration:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `POST /merlin/config` | owner | Create or update Merlin config |
| `GET /merlin/config` | admin | Get Merlin configuration |
| `DELETE /merlin/config` | owner | Disable Merlin integration |

**Credentials & Connection:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `PUT /merlin/credentials` | owner | Update FTP credentials |
| `POST /merlin/test-connection` | owner | Test FTP connection |
| `GET /merlin/connection-status` | admin | Get connection status |
| `PUT /merlin/features` | admin | Update enabled features |

**Import Configuration** (requires `royaltyImport` addon feature):

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /merlin/import/config` | admin | Get import config |
| `PUT /merlin/import/config` | admin | Update import config |
| `PUT /merlin/import/schedule` | admin | Update import schedule |

**Import Operations:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `POST /merlin/import/trigger` | admin | Trigger manual import |
| `GET /merlin/import/batches` | user | List import batches |
| `GET /merlin/import/batch/{id}` | user | Get batch details |
| `POST /merlin/import/batch/{id}/cancel` | admin | Cancel batch |

**Pending Import Approval:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /merlin/pending` | user | List pending imports |
| `GET /merlin/pending/grouped` | user | Pending imports grouped by source/period |
| `GET /merlin/pending/{id}` | user | Get pending import details |
| `GET /merlin/pending/{id}/preview` | user | Preview file contents |
| `GET /merlin/pending/{id}/recommendation` | user | Get confidence recommendation |
| `POST /merlin/pending/{id}/approve` | admin | Approve pending import |
| `POST /merlin/pending/{id}/reject` | admin | Reject pending import |
| `POST /merlin/pending/bulk-approve` | admin | Bulk approve |
| `POST /merlin/pending/bulk-reject` | admin | Bulk reject |

**Auto-Approval:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /merlin/batches/{batchId}/auto-approvable` | user | Get auto-approvable candidates |
| `GET /merlin/imports/groupable` | user | Get groupable imports |

**History & Stats:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /merlin/sources` | user | List Merlin-compatible sources |
| `GET /merlin/history` | user | Import history |
| `GET /merlin/stats` | user | Import statistics |
| `GET /merlin/metrics` | user | Comprehensive metrics |

---

## 12. Data Shares (`/data-shares`)

Cross-tenant royalty data sharing for labels sharing sources.

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /data-shares` | admin | List data shares |
| `POST /data-shares` | owner | Create data share |
| `GET /data-shares/{id}` | admin | Get share details |
| `PUT /data-shares/{id}` | owner | Update share |
| `DELETE /data-shares/{id}` | owner | Delete share |

---

## 13. Music Publishing

Publishing management with CWR (Common Works Registration) export. Requires `publisher` addon.

### Publishers (`/publishers`)

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /publishers` | user | List publishers |
| `POST /publishers` | admin | Create publisher |
| `GET /publishers/{id}` | user | Get publisher |
| `PUT /publishers/{id}` | admin | Update publisher |
| `DELETE /publishers/{id}` | admin | Delete publisher |
| `GET /publishers-with-user-data` | user | Publishers with associated user data |

**Territory Management:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /publishers/{id}/territories` | user | List territories |
| `POST /publishers/{id}/territories` | admin | Add territory |
| `PUT /publishers/{id}/territories/{territoryId}` | admin | Update territory |
| `DELETE /publishers/{id}/territories/{territoryId}` | admin | Delete territory |

**Agreement Management:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /publishers/{id}/agreements` | user | List agreements |
| `POST /publishers/{id}/agreements` | admin | Create agreement |
| `PUT /publishers/{id}/agreements/{agreementId}` | admin | Update agreement |
| `DELETE /publishers/{id}/agreements/{agreementId}` | admin | Delete agreement |

**Sub-Publishing:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `POST /sub-publishing` | admin | Create sub-publishing agreement |
| `GET /sub-publishing` | user | List sub-publishing agreements |
| `GET /sub-publishing/{id}` | user | Get agreement details |
| `PUT /sub-publishing/{id}` | admin | Update agreement |
| `POST /sub-publishing/check-conflicts` | admin | Check territory conflicts |

### Writers (`/writers`)

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /writers` | user | List writers |
| `POST /writers` | admin | Create writer |
| `GET /writers/{id}` | user | Get writer |
| `PUT /writers/{id}` | admin | Update writer |
| `DELETE /writers/{id}` | admin | Delete writer |
| `GET /writers-with-user-data` | user | Writers with associated user data |
| `POST /writers/{writerId}/works/{workId}` | admin | Assign writer to work |
| `DELETE /writers/{writerId}/works/{workId}` | admin | Remove writer from work |

### Musical Works (`/works`)

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /works` | user | List works |
| `POST /works` | admin | Create work |
| `GET /works/{id}` | user | Get work |
| `PUT /works/{id}` | admin | Update work |
| `DELETE /works/{id}` | admin | Delete work |

**Work-Recording Links:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `POST /works/{workId}/recordings/{assetId}` | admin | Link work to recording |
| `GET /works/{workId}/recordings` | user | Get work's recordings |
| `POST /works/{workId}/recordings/{assetId}/primary` | admin | Set primary recording |
| `GET /works/{workId}/recordings/primary` | user | Get primary recording |
| `GET /works/recordings/{assetId}/works` | user | Get recording's works |

**Work Registrations:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `POST /works/registrations` | admin | Create/update registration |
| `GET /works/registrations` | user | List all registrations |
| `GET /works/{workId}/registrations` | user | Get work's registrations |
| `GET /works/registrations/summary` | user | Registration summary |
| `GET /works/registrations/{id}` | user | Get registration details |
| `DELETE /works/registrations/{id}` | admin | Delete registration |
| `PATCH /works/registrations/{id}/status` | admin | Update registration status |

**Work-Writer Relationships:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /works/work-writers` | user | List work-writer relationships |

### CWR Export (`/cwr`)

| Endpoint | Role | Description |
|----------|------|-------------|
| `POST /cwr/export` | admin | Export CWR file |
| `GET /cwr/status/{publisherId}` | user | Get export status |
| `POST /cwr/cancel` | admin | Cancel export |
| `POST /cwr/acknowledgment` | admin | Process acknowledgment file (upload) |
| `GET /cwr/works/registration-status` | user | Get work registration statuses |
| `GET /cwr/works/{workId}/registration` | user | Get work's CWR registration |
| `PATCH /cwr/registrations/{registrationId}/status` | admin | Update registration status |

---

## 14. Currency Management (`/currencies`)

**Public Routes:**

| Endpoint | Description |
|----------|-------------|
| `GET /currencies` | List all supported currencies |
| `GET /currencies/{code}` | Get currency details |

**Tenant Routes:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /currencies/tenant` | user | Get tenant's enabled currencies |
| `GET /currencies/tenant/default` | user | Get tenant's default currency |
| `POST /currencies/tenant/{code}/enable` | admin | Enable currency |
| `POST /currencies/tenant/{code}/disable` | admin | Disable currency |
| `POST /currencies/tenant/{code}/default` | owner | Set default currency |

---

## 15. Billing & Subscriptions (`/billing`)

Subscription management with Stripe integration.

**Current State:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /billing/active` | user | Get active subscription |
| `GET /billing/sync-status` | user | Subscription sync status |
| `GET /billing/usage` | user | Usage summary |

**Plans:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /billing/plans` | user | List available plans |
| `GET /billing/plans/stripe` | user | Get Stripe plans |

**Subscription Management:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /billing/subscriptions` | admin | List subscriptions |
| `GET /billing/subscriptions/{id}` | admin | Get subscription |
| `POST /billing/subscriptions` | owner | Create subscription |
| `POST /billing/subscriptions/{id}/cancel` | owner | Cancel subscription |

**Plan Changes:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `POST /billing/upgrade/checkout-session` | owner | Create Stripe checkout for upgrade |
| `POST /billing/upgrade/{lookupKey}` | owner | Direct plan upgrade |
| `POST /billing/downgrade` | owner | Downgrade plan |

**Custom Invoices:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `POST /billing/invoices/custom` | owner | Create custom invoice |
| `PUT /billing/invoices/custom/{id}` | owner | Update custom invoice |
| `DELETE /billing/invoices/custom/{id}` | owner | Delete custom invoice |
| `POST /billing/invoices/custom/{id}/mark-paid` | owner | Mark invoice as paid |
| `GET /billing/invoices` | admin | List invoices |

**Stripe Integration:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `POST /billing/portal` | owner | Create Stripe customer portal session |
| `POST /billing/customer-session` | owner | Create Stripe customer session |
| `POST /billing/refresh` | owner | Force refresh subscription data |

---

## 16. Custom Domains (`/domains`)

Cloudflare SaaS custom domain management.

| Endpoint | Role | Description |
|----------|------|-------------|
| `POST /domains/setup` | admin | Setup custom domain |
| `GET /domains/status` | user | Get domain status |
| `GET /domains/instructions` | user | Get DNS setup instructions |
| `POST /domains/switch-validation` | admin | Switch validation method |
| `POST /domains/restart-validation` | admin | Restart domain validation |
| `DELETE /domains` | owner | Delete custom domain |
| `GET /domains/all` | admin | List all domains |

---

## 17. Admin Dashboard (`/admin/dashboard`)

Centralized admin dashboard for workspace management.

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /admin/dashboard/overview` | admin | Dashboard overview metrics |
| `GET /admin/dashboard/analytics` | admin | Release analytics |
| `GET /admin/dashboard/health` | admin | System health monitoring |
| `GET /admin/dashboard/users` | admin | User management data |
| `POST /admin/dashboard/releases/bulk-action` | owner | Bulk approve/reject releases |
| `GET /admin/dashboard/config` | admin | Get dashboard config |
| `PUT /admin/dashboard/config` | owner | Update dashboard config |
| `GET /admin/dashboard/config/export` | admin | Export config JSON |
| `POST /admin/dashboard/config/import` | owner | Import config JSON |
| `GET /admin/dashboard/workers/stats` | admin | Background worker statistics |
| `POST /admin/dashboard/workers/{workerName}/pause` | admin | Pause worker |
| `POST /admin/dashboard/workers/{workerName}/resume` | admin | Resume worker |

---

## 18. Audit Trail (`/api/audit`)

Audit logging for compliance and security monitoring. Requires admin role.

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /api/audit` | admin | List all audit trails |
| `GET /api/audit/entity/{entityType}/{entityId}` | admin | Get entity audit trail |
| `GET /api/audit/user/{userId}/activity` | admin/self | Get user activity (self-access allowed) |
| `GET /api/audit/high-risk` | admin | Get high-risk security events |

---

## 19. Monitoring (`/api/monitoring`)

System monitoring for delivery pipelines and integrations.

**FUGA Delivery Monitoring:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /api/monitoring/fuga/metrics` | user | FUGA delivery metrics |
| `GET /api/monitoring/fuga/health` | user | FUGA health status |
| `GET /api/monitoring/fuga/alerts` | user | FUGA alerts |
| `GET /api/monitoring/fuga/stuck-deliveries` | user | Stuck deliveries |
| `GET /api/monitoring/fuga/ftp-health` | user | FTP connection health |
| `PUT /api/monitoring/fuga/thresholds` | admin | Update alert thresholds |

**DDEX Registry Monitoring:**

| Endpoint | Role | Description |
|----------|------|-------------|
| `GET /api/monitoring/registries/health` | user | Registry health |
| `GET /api/monitoring/registries/adapters` | user | Adapter health |
| `GET /api/monitoring/registries/providers` | user | Registered providers |
| `GET /api/monitoring/registries/metrics` | user | Adapter metrics |

**Prometheus Metrics:**

| Endpoint | Description |
|----------|-------------|
| `GET /api/monitoring/metrics/fuga` | Prometheus-compatible metrics endpoint |

---

## 20. Webhooks

### Outbound Webhooks (Royalti → Your Endpoint)

Configure your webhook endpoint via tenant settings:

```bash
# Set webhook URL
PUT /tenant/settings/webhook-url
{ "webhookUrl": "https://yourapp.com/webhooks/royalti" }

# Enable/disable webhooks
PUT /tenant/settings/webhook-isActive
{ "isActive": true }

# Subscribe to event types
PUT /tenant/settings/webhook-enabledEvents
{ "enabledEvents": ["PAYMENT_COMPLETED", "ROYALTY_FILE_PROCESSED"] }
```

### Event Categories

**Financial Events:**
- `PAYMENT_COMPLETED`, `PAYMENT_PROCESSING`, `PAYMENT_MADE_FAILED`
- `PAYMENT_REQUEST_SENT`, `PAYMENT_REQUEST_APPROVED`, `PAYMENT_REQUEST_REJECTED`
- `PAYMENT_DELETED`
- `REVENUE_CREATED`, `REVENUE_UPDATED`, `REVENUE_DELETED`
- `EXPENSE_CREATED`, `EXPENSE_UPDATED`, `EXPENSE_DELETED`

**Catalog Events:**
- `ASSET_CREATED`, `ASSET_UPDATED`, `ASSET_DELETED`
- `PRODUCT_CREATED`, `PRODUCT_UPDATED`, `PRODUCT_DELETED`

**Roster Events:**
- `USER_CREATED`, `USER_UPDATED`, `USER_DELETED`
- `USER_INVITATION_SENT`
- `ARTIST_CREATED`, `ARTIST_UPDATED`, `ARTIST_DELETED`

**Royalty Events (opt-in):**
- `ROYALTY_FILE_UPLOADED`
- `ROYALTY_FILE_PROCESSED`
- `ROYALTY_FILE_PROCESSING_FAILED`

**Split Events:**
- `USER_ADDED_TO_SPLIT`
- `USER_REMOVED_FROM_SPLIT`

### Webhook Payload Structure

```json
{
  "id": "whd_{uuid}",
  "event": "PAYMENT_COMPLETED",
  "timestamp": "2025-01-15T10:30:00.000Z",
  "version": "1.0",
  "tenant": {
    "id": "tenant-uuid",
    "name": "My Label",
    "domain": "mylabel.royalti.io"
  },
  "source": {
    "service": "royalti-api",
    "environment": "production",
    "traceId": "trace-uuid"
  },
  "data": {
    "event": {
      "id": "evt-uuid",
      "type": "PAYMENT_COMPLETED",
      "category": "financial",
      "timestamp": "2025-01-15T10:30:00.000Z",
      "importance": "high"
    },
    "actor": {
      "id": "user-uuid",
      "type": "user",
      "name": "John Doe",
      "email": "john@label.com"
    },
    "resource": {
      "type": "payment",
      "id": "payment-uuid",
      "url": "https://app.royalti.io/payments/payment-uuid",
      "displayName": "Payment #1234"
    },
    "attributes": {
      "amount": 500.00,
      "currency": "USD",
      "recipientId": "user-uuid"
    },
    "previous": {}
  },
  "delivery": {
    "attempt": 1,
    "maxAttempts": 3,
    "nextRetryAt": "2025-01-15T10:35:00.000Z"
  }
}
```

- `previous` is only populated on `*_UPDATED` events (contains pre-update values)
- `delivery.maxAttempts` is 3 with exponential backoff
- Financial and split events include HMAC signature for verification

### HMAC Signature Validation

Financial and split webhook deliveries include an HMAC signature header for verification. Validate the signature before processing the payload.

### Webhook Delivery Management

| Endpoint | Description |
|----------|-------------|
| `GET /webhook-deliveries` | List deliveries (filterable by status, event type, date) |
| `GET /webhook-deliveries/summary` | Delivery stats |
| `GET /webhook-deliveries/{id}` | Delivery details |
| `POST /webhook-deliveries/{id}/retry` | Retry failed delivery |

Delivery statuses: `pending`, `success`, `failed`, `timeout`, `cancelled`

---

## 21. WebSocket Events (Socket.io)

Real-time events for file processing and workflow progress.

### Connection

```javascript
import { io } from "socket.io-client";

const socket = io("wss://api.royalti.io", {
  auth: { token: "<access_token>" }
});
```

Events are user-scoped — only the user who uploaded the file receives processing events. Workflow events are emitted to the tenant room.

### File Processing Events

| Event | When |
|-------|------|
| `file:processing:started` | File processing begins |
| `file:processing:progress` | Progress update (~10% intervals) |
| `file:processing:completed` | Processing finished successfully |
| `file:processing:failed` | Processing failed |

### Workflow Events

| Event | When |
|-------|------|
| `workflow:prompt` | Workflow requires user input |
| `workflow:step-started` | Workflow step begins |
| `workflow:step-complete` | Workflow step finishes |
| `workflow:completed` | Workflow finished |

### File Processing Event Payload

```json
{
  "fileId": "file-uuid",
  "fileName": "spotify-2025-01.csv",
  "status": "processing",
  "progress": 75,
  "message": "Processing row 750 of 1000",
  "error": null,
  "metadata": {
    "rowsProcessed": 750,
    "source": "Spotify",
    "accountingPeriod": "2025-01",
    "salePeriod": "2025-01",
    "processingTimeMs": 45000
  }
}
```

---

## 22. Key Data Models

### Tenant (Workspace)

```
id (integer), name, email, user (varchar — must be a TenantUser.id UUID),
status (active|inactive|suspended), plan, stripeCustomerId,
bigqueryDataset, domain, uid
```

**Important:** The `user` field on `Tenants` stores a `TenantUser.id`, not a `User.id`. This is used by API key auth resolution and accounting owner-exclusion. See "API Key Auth Resolution" in Section 1.

### User (Global)

```
id (UUID), email, isVerified, isAdmin, provider, googleId, linkedinId, facebookId
```

A User can belong to multiple workspaces via TenantUser records.

### TenantUser (Workspace-Scoped)

```
id (UUID), UserId (FK → User.id), TenantId (FK → Tenant.id),
firstName, lastName, email, nickName, profileImg,
role: main_super_admin | super_admin | owner | admin | user | guest,
userType, paymentSettings, permissions (JSONB),
ipi, externalId, country, phone, isActive
```

**Key distinction:** `TenantUser.id` is the workspace-scoped identity used throughout the API (splits, payments, accounting). `User.id` (`UserId`) is the global auth identity. API responses for `/user/` return TenantUser records, not User records.

### Artist

```
id (UUID), artistName, signDate, label, publisher, copyright,
externalId, artistImg, links {spotify, youtube, instagram, ...},
genres[], realName, pseudonyms, biography, influences,
instruments, activeYears, associatedActs, contributors
```

### Asset (Track)

```
id (UUID), title, ISRC, type (Audio|Video|Ringtone|YouTube),
version, displayArtist, mainArtist[], mainGenre[], subGenre[],
explicit, language, tempo, key, mood[], lyrics,
label, copyright, publisher, copyrightOwner,
recordingDate, recordingLocation, productionYear,
enableDDEX, focusTrack, ddexMetadata, resourceReference
```

### Product (Release)

```
id (UUID), title, UPC, format (Single|EP|Album|LP),
release_date, takedown_date, label, display_artist,
type (Audio|Video), catalog_number, version, explicit,
main_genre, sub_genre, status (active|inactive|pending|Live|Taken Down|Scheduled|Error),
distribution, external_id
```

### Split

```
id, entity_type (artist|product|asset), entity_id,
split_type (simple|conditional|temporal),
effective_date,
shares: [{ user: UUID, percentage: 0-100 }],
conditions: { territories[], mode, sources[], period_start, period_end, memo }
```

### Transaction

```
id (UUID), type (payment|royalty|expense|adjustment),
amount, currency, status (pending|processed|failed),
reference, metadata
```

### TenantRoyaltySource

```
id (UUID), name, displayName, type (dsp|distributor|custom),
salesDataQuery (BigQuery SQL), extractionQueries[],
periodConfig { type, format, startField, endField },
feeRate, currency, isActive, parentSourceId, version
```

### TenantDataShare

```
id (UUID), sourceTenantId, targetTenantId,
sourceId, status (active|inactive),
sharedColumns[], filters
```

### Publisher

```
id (UUID), name, ipiNumber, ipiNameNumber,
territories[], agreements[],
type (original|sub), parentPublisherId
```

### Writer

```
id (UUID), firstName, lastName, ipiNumber, ipiNameNumber,
prAffiliation, mrAffiliation, srAffiliation,
writerDesignationCode, citizenshipCountry
```

### Work (Musical Work)

```
id (UUID), title, iswc, alternativeTitles[],
writers[] (with shares), publishers[] (with shares),
recordings[] (linked assets), registrations[]
```

---

## 23. Common Integration Patterns

### Sync Catalog from External System

```
1. POST /artist/bulk          → Create artists
2. POST /product/bulk         → Create products
3. POST /asset/bulk           → Create assets/tracks
4. POST /split/               → Assign splits per entity
5. POST /accounting/refresh   → Recalculate accounting
```

### Upload and Process Royalty File

```
1. GET  /file/upload-url               → Get presigned upload URL
2. PUT  <presigned_url>                 → Upload file to cloud storage
3. POST /file/confirm-upload-completion → Notify API upload is done
4. GET  /file/detection/{sessionId}     → Poll auto-detection (or listen via WebSocket)
5. POST /file/confirm-detection/{sessionId} → Confirm detected format
   If unknown source:
   POST /file/session/{sessionId}/start-source-creator → Bridge to Source Creator
6. GET  /file/processing/{jobId}        → Poll processing status
   OR subscribe to WebSocket: file:processing:progress
7. POST /accounting/refresh             → Recalculate after processing
```

### Create a New Royalty Source (Source Creator)

```
1. POST /source-creator/analyze              → Upload & analyze file
2. POST /source-creator/ai-map-columns       → Get AI mapping suggestions
3. PUT  /source-creator/sessions/{id}/mappings → Confirm column mappings
4. PUT  /source-creator/sessions/{id}/periods  → Confirm periods
5. POST /source-creator/generate-queries      → Generate BigQuery SQL
6. POST /source-creator/test-queries          → Sandbox validation
7. POST /source-creator/save                  → Save as draft
```

### DDEX Release Distribution

```
1. POST /ddex/tenant-providers                → Configure DSP provider
2. POST /ddex/delivery/test-connection        → Verify connection
3. POST /ddex/ern/generate { releaseId }      → Generate ERN
4. POST /ddex/messages/{id}/validate          → Validate
5. POST /ddex/delivery/deliver/{id}           → Deliver to DSP
6. GET  /ddex/delivery/status/{id}            → Monitor
```

### Data Quality Checklist

```
1. GET /checklist/royaltyassets          → Find missing catalog items
2. POST /checklist/royaltyassets/import  → Import them
3. POST /checklist/assets/enrich         → Enrich with metadata
4. POST /checklist/enrichment/approve    → Approve enrichments
5. GET /checklist/missingroyaltysplits   → Find unsplit royalties
6. POST /checklist/workflow              → Start automated workflow
```

### Fetch Analytics Dashboard Data

```
1. GET /royalty/?start=2025-01-01&end=2025-12-31              → Overview
2. GET /royalty/month?start=2025-01-01&end=2025-12-31         → Monthly trend
3. GET /royalty/dsp?start=2025-01-01&end=2025-12-31           → Platform breakdown
4. GET /royalty/country?start=2025-01-01&end=2025-12-31       → Geographic breakdown
5. GET /royalty/asset?start=2025-01-01&end=2025-12-31&size=10 → Top tracks
```

### Set Up Webhook Listener

```
1. PUT /tenant/settings/webhook-url          → Set your endpoint
2. PUT /tenant/settings/webhook-enabledEvents → Choose event types
3. PUT /tenant/settings/webhook-isActive     → Enable
4. GET /webhook-deliveries                   → Monitor deliveries
5. POST /webhook-deliveries/{id}/retry       → Retry failures
```

### Release Lifecycle

```
1. POST /releases                          → Create draft release
2. POST /releases/{id}/media/files         → Upload artwork
3. POST /releases/{id}/tracks              → Add tracks
4. POST /releases/{id}/tracks/{trackId}/media/file → Upload audio
5. POST /releases/{id}/tracks/reorder      → Set track order
6. POST /releases/{id}/submit              → Submit for review
7. POST /releases/{id}/review              → Admin reviews
8. POST /releases/{id}/feedback            → Admin feedback (optional)
   OR POST /ddex/ern/generate              → Generate DDEX for distribution
```

---

## 24. Code Examples

Language-specific integration examples are available in the `references/` directory:

- `references/examples-javascript.md` — Node.js/TypeScript client, auth, CRUD, file upload, WebSocket, Express webhook receiver
- `references/examples-python.md` — Python client, auth, pagination, file upload, Flask webhook receiver, socketio
- `references/examples-php.md` — PHP client, auth, pagination, file upload, Laravel and plain PHP webhook receivers

Load these files when the developer is working in a specific language.

## 25. Troubleshooting

### Common Errors

| Error Message | HTTP Code | Cause | Fix |
|--------------|-----------|-------|-----|
| `"Workspace user not found"` | 404 | API key's workspace has `Tenants.user` pointing to wrong ID (UserId instead of TenantUserId), or no owner TenantUser exists | Verify `Tenants.user` matches a `TenantUser.id` where `role='owner'` for that workspace |
| `"Workspace not found"` | 404 | Tenant doesn't exist or `status != 'active'` | Check tenant status in admin panel |
| `"Authorization token is missing"` | 401 | No `Authorization` header or malformed token | Ensure `Authorization: Bearer <token>` header is present |
| `"Route does not exist"` | — | Wrong URL path (e.g., `/api/users` instead of `/user/`) | Check endpoint paths — no `/api` prefix, resource names are singular |
| `"Access denied"` | 403 | Token valid but user lacks required role for endpoint | Check RBAC requirements for the endpoint |

### Endpoint Path Gotchas

- Paths use **singular** nouns: `/user/`, `/artist/`, `/asset`, `/product/`
- Exceptions: `/labels/`, `/releases`, `/notifications/`, `/publishers`, `/writers`
- Most paths require a **trailing slash**: `/user/` not `/user`
- No `/api` prefix — endpoints are at the root: `https://api.royalti.io/artist/`
- Sources endpoint: `/file/sources` (nested under files, not standalone)

---

## 26. Further Reading

- **API Explorer:** [apidocs.royalti.io](https://apidocs.royalti.io)
- **MCP Server:** [royalti.io/mcp](https://royalti.io/mcp) — AI assistant integration for direct API interaction
- **MCP Setup Guide:** [royalti.io/help/setting-up-the-royalti-mcp-server](https://royalti.io/help/setting-up-the-royalti-mcp-server)
