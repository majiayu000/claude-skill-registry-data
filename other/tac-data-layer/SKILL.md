---
name: tac-data-layer
description: "MANDATORY when writing services, database queries, hooks, or any data-fetching logic in TAC Express. Enforces the UI → packages/services → packages/database → Supabase architecture."
---

# TAC Express — Data Layer Authoring

Invoke this skill before writing any service, database query, or data-fetching hook. The architecture is inviolable: **components never touch the database.**

---

## Architecture (No Exceptions)

```
apps/web or apps/dashboard
  └── React Component (display only)
       ↓ calls hook / receives props
  packages/services/
    └── *.service.ts (business logic)
         ↓ calls database client
  packages/database/
    └── client.ts (Supabase client, initialized once)
         ↓ Supabase JS SDK
  Supabase Cloud
```

**Violations:**
- `@supabase/supabase-js` in `apps/` → LAW 8 violation → CI blocks
- DB query in component body → LAW 6 violation → PR rejected
- Business logic in component → LAW 7 violation → PR rejected

---

## File Locations

```
packages/
  types/
    src/
      shipment.types.ts     ← TypeScript types/interfaces
      user.types.ts
  database/
    src/
      client.ts             ← Supabase client (singleton)
      shipment.queries.ts   ← Raw Supabase queries
  services/
    src/
      shipment.service.ts   ← Business logic, data transformation
      user.service.ts
```

---

## Database Client Pattern

```ts
// Browser client (client components, sign-in handlers)
import { createBrowserClient } from "@workspace/database/client"

const db = createBrowserClient()

// Server client (RSC, route handlers, server actions)
import { createServerClient } from "@workspace/database/client"
import { cookies } from "next/headers"

const db = createServerClient(await cookies())

// Middleware client (proxy.ts ONLY — never in components)
import { createMiddlewareClient } from "@workspace/database/middleware"

const { supabase, response } = createMiddlewareClient(req)
```

> **NEVER** use `createClient` from `@supabase/supabase-js` directly.
> **NEVER** use a `getDbClient()` singleton — that pattern is removed.
> LAW 8: `@supabase/supabase-js` is only importable inside `packages/database`.

---

## Service Pattern

```ts
// packages/services/src/shipment.service.ts
import { createServerClient } from "@workspace/database/client"
import { cookies } from "next/headers"
import type { Shipment, CreateShipmentInput } from "@workspace/types"

export async function getShipments(userId: string): Promise<Shipment[]> {
  const db = createServerClient(await cookies())
  const { data, error } = await db
    .from("shipments")
    .select("*")
    .eq("user_id", userId)
    .order("created_at", { ascending: false })

  if (error) throw new Error(`Failed to fetch shipments: ${error.message}`)
  return data ?? []
}

export async function createShipment(
  input: CreateShipmentInput
): Promise<Shipment> {
  const db = createServerClient(await cookies())
  const { data, error } = await db
    .from("shipments")
    .insert(input)
    .select()
    .single()

  if (error) throw new Error(`Failed to create shipment: ${error.message}`)
  if (!data) throw new Error("No data returned from insert")
  return data
}
```

---

## Hook Pattern (Connecting Service to UI)

```ts
// packages/services/src/hooks/useShipments.ts
import { useState, useEffect } from "react"
import { getShipments } from "../shipment.service"
import type { Shipment } from "@workspace/types"

interface UseShipmentsResult {
  shipments: Shipment[]
  isLoading: boolean
  error: string | null
  refetch: () => void
}

export function useShipments(userId: string): UseShipmentsResult {
  const [shipments, setShipments] = useState<Shipment[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchShipments = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const data = await getShipments(userId)
      setShipments(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error")
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchShipments()
  }, [userId])

  return { shipments, isLoading, error, refetch: fetchShipments }
}
```

---

## Type Definitions Pattern

```ts
// packages/types/src/shipment.types.ts
export interface Shipment {
  id: string
  user_id: string
  tracking_number: string
  status: ShipmentStatus
  origin: string
  destination: string
  created_at: string
  updated_at: string
}

export type ShipmentStatus =
  | "pending"
  | "in_transit"
  | "customs"
  | "delivered"
  | "exception"

export interface CreateShipmentInput {
  user_id: string
  tracking_number: string
  origin: string
  destination: string
}
```

---

## Service Test Pattern

```ts
// packages/services/src/shipment.service.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest"
import * as dbClient from "@workspace/database/client"
import { getShipments } from "./shipment.service"

vi.mock("@workspace/database/client")
vi.mock("next/headers", () => ({ cookies: vi.fn().mockResolvedValue({}) }))

describe("shipment.service", () => {
  const mockClient = {
    from: vi.fn().mockReturnThis(),
    select: vi.fn().mockReturnThis(),
    eq: vi.fn().mockReturnThis(),
    order: vi.fn().mockResolvedValue({ data: [], error: null }),
  }

  beforeEach(() => {
    vi.mocked(dbClient.createServerClient).mockReturnValue(mockClient as any)
    vi.clearAllMocks()
  })

  it("returns empty array when no shipments exist", async () => {
    const result = await getShipments("user-1")
    expect(result).toEqual([])
  })

  it("throws on database error", async () => {
    mockClient.order.mockResolvedValue({
      data: null,
      error: { message: "Connection refused" },
    })
    await expect(getShipments("user-1")).rejects.toThrow(
      "Failed to fetch shipments: Connection refused"
    )
  })

  it("queries correct table and filters by userId", async () => {
    await getShipments("user-123")
    expect(mockClient.from).toHaveBeenCalledWith("shipments")
    expect(mockClient.eq).toHaveBeenCalledWith("user_id", "user-123")
  })
})
```

---

## Pre-Completion Checklist

```
[ ] Types in packages/types (not inline in service)
[ ] Service uses createServerClient() from @workspace/database/client (not getDbClient)
[ ] Service throws typed errors (not returns null/undefined on error)
[ ] Service function return type explicitly annotated
[ ] Service test file created alongside (tac-tdd)
[ ] Service mocked in component tests (not real DB)
[ ] Hook exported from packages/services/src/index.ts
[ ] No @supabase/supabase-js import outside packages/database
[ ] No business logic duplicated in components
```
