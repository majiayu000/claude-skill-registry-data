---
name: thesmarthost-context
description: Business context and backend API reference for TheSmartHost/HostMetrics platform. Auto-loads when starting any task.
---

# TheSmartHost Context

> **Essential business context and backend API reference for the HostMetrics platform**

**Auto-loaded for all tasks** - This provides the foundational context you need to work effectively on this project.

---

## Project Overview

**HostMetrics** is a property management reporting platform for short-term rental (STR) managers.

### Business Problem
Property managers spend **2-4 hours per client per month** manually creating financial reports from CSV exports (Airbnb, VRBO, etc.). HostMetrics automates this process down to **~10 minutes**.

### Client
- **Company:** TheSmartHost Co. Inc
- **Owner:** Luis Torres (Calgary property manager)
- **Team:** Mark Cena (Calgary) + Hussein Saab (Toronto)

### Timeline
- **Duration:** Oct 7 - Dec 20, 2025 (10 weeks)
- **Current Status:** Sprint 2, Week 4 (Infrastructure Setup - ~90% complete)

---

## Core Business Entities

### 1. **Profiles** (Users)
Property managers who use the platform. Linked to Supabase Auth.
- **Roles:** ADMIN, PROPERTY-MANAGER, CLIENT
- **Relationship:** One profile has many clients

### 2. **Clients** (Property Owners)
Individuals or companies who own rental properties.
- **Relationship:** One client can own many properties (via many-to-many)
- **Key Fields:** name, email, phone, status, company_name, PMS (property management system)

### 3. **Properties** (Rental Units)
Individual rental properties (houses, condos, etc.)
- **Types:** STR (Short-Term Rental), LTR (Long-Term Rental)
- **Relationship:** Many-to-many with clients (co-ownership support)
- **Key Fields:** name, address, province, commission_rate, hostaway_listing_id

### 4. **Client-Properties Junction** ⭐ CRITICAL
Links properties to their owners (supports co-ownership).
- **Key Fields:** is_primary (one owner must be primary), commission_rate_override
- **Business Rule:** Property MUST have ≥1 owner at all times

### 5. **Bookings**
Individual reservation records from CSV uploads.
- **Relationship:** Belongs to property, belongs to csv_upload
- **Key Fields:** guest_name, check_in_date, platform, nightly_rate, fees, payouts

### 6. **CSV Uploads**
Uploaded financial data files from PMS platforms.
- **Relationship:** Belongs to property, has many bookings
- **Status:** pending, processing, completed, failed

### 7. **Reports**
Generated PDF financial reports for clients.
- **Relationship:** Belongs to client and property
- **Key Fields:** reporting_period, pdf_file_path, status

---

## Tech Stack

### Frontend (This Repository)
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State Management:** Zustand
- **Authentication:** Supabase Auth
- **API Client:** Custom fetch wrapper (no axios)

### Backend (Separate Repository)
- **Framework:** Express.js 5.1.0
- **Language:** JavaScript (NOT TypeScript)
- **Database:** PostgreSQL via Supabase
- **Database Client:** node-pg (raw SQL queries, NOT Supabase SDK)
- **Authentication:** Supabase Auth (service role key)
- **Base URL:** `http://localhost:4000` (dev), `process.env.NEXT_PUBLIC_BASE_URL` (prod)

---

## Backend API Reference

**Base URL:** `process.env.NEXT_PUBLIC_BASE_URL` (configured in frontend `.env.local`)

### Standard Response Format

**Success:**
```json
{
  "status": "success",
  "message": "Optional success message",
  "data": { ... }
}
```

**Error:**
```json
{
  "status": "failed",
  "message": "Human-readable error message"
}
```

### HTTP Status Codes
- **200:** Success (GET, PUT, PATCH, DELETE)
- **201:** Created (POST)
- **400:** Validation error
- **404:** Resource not found
- **409:** Conflict (duplicate entry)
- **500:** Server error

---

## Available API Routes

### Authentication
| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/auth/me` | GET | Validate session | ✅ Complete |

### Users & Profiles
| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/users` | GET | List Supabase Auth users | ✅ Complete |
| `/api/profile` | GET, POST, PUT, DELETE | User profiles | ✅ Complete |

### Clients
| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/client` | GET | Get all clients (supports `?parentId=uuid` filter) | ✅ Complete |
| `/api/client` | POST | Create client | ✅ Complete |
| `/api/client/:id` | PUT | Update client | ✅ Complete |
| `/api/client/:id` | DELETE | Soft delete client | ✅ Complete |

### Properties ⭐ FULLY IMPLEMENTED
| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/api/properties` | GET | List all active properties with owners | Query: `?parentId=uuid` | `{ status, data: Property[] }` |
| `/api/properties/:id` | GET | Single property with details | - | `{ status, data: PropertyDetails }` |
| `/api/properties` | POST | Create property + junction entry | `CreatePropertyPayload` | `{ status, data: Property }` |
| `/api/properties/:id` | PUT | Update property + manage owners | `UpdatePropertyPayload` | `{ status, data: Property }` |
| `/api/properties/:id` | DELETE | Soft delete property | - | `{ status, message }` |
| `/api/properties/:id/status` | PATCH | Toggle active status | `{ isActive: boolean }` | `{ status, data: Property }` |

**Property Payloads:**
```typescript
// Create Property
{
  clientId: string          // Initial owner (marked as primary)
  name: string
  address: string
  province: string
  propertyType: 'STR' | 'LTR'
  hostawayListingId: string
  commissionRate: number    // 0-100
  commissionRateOverride?: number  // Optional per-owner override
}

// Update Property (all fields optional except what you want to update)
{
  name?: string
  address?: string
  province?: string
  propertyType?: 'STR' | 'LTR'
  commissionRate?: number
  hostawayListingId?: string
  owners?: Array<{
    clientId: string
    isPrimary: boolean
    commissionRateOverride: number | null
  }>
}
```

### Client Status Codes
| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/client-status` | GET, POST, PUT, DELETE | Custom status codes | ✅ Complete |

### Client Agreements
| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/client-agreements` | GET, POST, PUT, DELETE | Contract files | ✅ Complete |

### PMS Credentials
| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/pms-credentials` | GET, POST, PUT, DELETE | Encrypted credentials | ✅ Complete |

### Bookings
| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/bookings` | - | Not yet implemented | ⏳ Pending |

### Reports
| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/reports` | - | Not yet implemented | ⏳ Pending |

---

## Data Transformation Rules

**Backend uses snake_case, Frontend uses camelCase**

When receiving data from API:
```typescript
// Backend returns:
{
  client_id: "uuid",
  property_type: "STR",
  is_active: true,
  created_at: "2025-11-04T..."
}

// Frontend expects:
{
  clientId: "uuid",
  propertyType: "STR",
  isActive: true,
  createdAt: "2025-11-04T..."
}
```

**The backend already handles this transformation** - API responses are in camelCase, so frontend doesn't need to transform.

---

## Key Business Rules

### Property Ownership (Critical!)
1. **Every property MUST have ≥1 owner** at all times
2. **Exactly one owner must be marked as primary** (`is_primary = true`)
3. **Co-ownership is supported** (multiple clients can own one property)
4. **Commission hierarchy:** owner override > property default

### Commission Rates
- Stored as numbers (e.g., `15.5` for 15.5%)
- Range: 0-100
- Per-owner overrides supported via `commission_rate_override` in junction table

### Soft Deletes
- Properties and clients use soft deletes (`is_active = false`)
- Data is preserved for historical reporting
- Can be reactivated via PATCH status endpoint

---

## Need More Detail?

- **Database schema:** See `database-schema.md` in this skill folder
- **Backend implementation details:** See backend repo CLAUDE.md
- **Frontend patterns:** Use the `add-frontend-feature` skill
- **API integration:** Use the `connect-to-backend-api` skill

---

**Last Updated:** November 4, 2025
