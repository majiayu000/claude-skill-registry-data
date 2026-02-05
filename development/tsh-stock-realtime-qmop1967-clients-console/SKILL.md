---
name: tsh-stock-realtime
description: |
  Real-time stock synchronization for TSH Clients Console. Use when:
  (1) Debugging stock sync issues (webhooks not firing, stock not updating)
  (2) Understanding webhook event handling
  (3) Implementing stock-affecting features
  (4) Troubleshooting stock discrepancies between Zoho and app
  (5) Adding new stock-affecting transaction handlers
  (6) Monitoring stock sync health
  (7) Understanding the multi-layer sync architecture
---

# TSH Stock Real-Time Synchronization

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                   TSH STOCK SYNC ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  LAYER 1: WEBHOOKS (Instant, < 5 seconds)                          │
│  ├── Zoho transaction occurs                                        │
│  ├── POST /api/webhooks/zoho                                        │
│  ├── quickSyncStock(itemIds)                                        │
│  └── Update Redis + Revalidate ISR                                  │
│                                                                     │
│  LAYER 2: PERIODIC SYNC (Every 15 minutes)                         │
│  ├── Vercel Cron job                                                │
│  ├── POST /api/sync/stock                                           │
│  ├── syncStockFromBooks()                                           │
│  └── Full cache refresh                                             │
│                                                                     │
│  LAYER 3: ON-DEMAND SYNC (Manual trigger)                          │
│  ├── Admin triggers via API                                         │
│  ├── GET /api/sync/stock?action=sync&force=true                     │
│  └── Immediate full refresh                                         │
│                                                                     │
│  LAYER 4: HEALTH MONITORING (Continuous)                           │
│  ├── GET /api/sync/stock?action=status                              │
│  ├── Check: itemCount > 400                                         │
│  ├── Check: cache age < 4 hours                                     │
│  └── Alert if unhealthy                                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Webhook Event Reference

### Stock-Affecting Transactions

| Transaction | Stock Effect | Webhook Event | Handler |
|-------------|--------------|---------------|---------|
| **Invoice Created** | Decreases | `invoice.created` | `revalidateProducts()` |
| **Invoice Updated** | May change | `invoice.updated` | `revalidateProducts()` |
| **Bill Created** | Increases | `bill.created` | `revalidateProducts()` |
| **Bill Updated** | May change | `bill.updated` | `revalidateProducts()` |
| **Sales Order Created** | Commits stock | `salesorder.created` | `revalidateProducts()` |
| **Sales Order Updated** | May release | `salesorder.updated` | `revalidateProducts()` |
| **Credit Note Created** | May increase | `creditnote.created` | `revalidateProducts()` |
| **Inventory Adjustment** | Changes | `inventoryadjustment.created` | `revalidateProducts()` |
| **Sales Return Received** | Increases | `salesreturnreceive.created` | `revalidateProducts()` |
| **Package Shipped** | Physical decrease | `package.shipped` | `revalidateProducts()` |
| **Item Updated** | May change | `item.updated` | `revalidateProducts()` |

### Webhook Handler Location

```typescript
// src/app/api/webhooks/zoho/route.ts

export async function POST(request: Request) {
  const payload = await request.json();
  const { event_type, resource_name, resource_id } = payload;

  // Extract affected item IDs from payload
  const itemIds = extractItemIds(payload);

  switch (resource_name) {
    case "invoice":
    case "bill":
    case "salesorder":
    case "creditnote":
    case "inventoryadjustment":
    case "salesreturnreceive":
    case "package":
      // Sync stock for affected items
      await quickSyncStock(itemIds);
      await revalidateTag('products');
      break;

    case "item":
      // Direct item update
      await quickSyncStock([resource_id]);
      await revalidateTag('products');
      break;
  }
}
```

## Quick Sync Function

```typescript
// src/lib/zoho/stock-cache.ts

export async function quickSyncStock(
  itemIds: string[],
  reason: string
): Promise<void> {
  const WHOLESALE_LOCATION_NAME = 'Main WareHouse';

  for (const itemId of itemIds) {
    try {
      // Fetch item with locations from Zoho Books
      const item = await getItemWithLocations(itemId);

      // Extract warehouse-specific stock
      const location = item.locations?.find(
        loc => loc.location_name === WHOLESALE_LOCATION_NAME
      );
      const stock = location?.location_available_for_sale_stock || 0;

      // Update Redis cache
      await redis.set(`stock:${itemId}`, stock, { ex: STOCK_CACHE_TTL });

      console.log(`[quickSyncStock] ${itemId}: ${stock} (${reason})`);
    } catch (error) {
      console.error(`[quickSyncStock] Failed for ${itemId}:`, error);
    }
  }
}
```

## Unified Stock Functions

### ALWAYS Use These Functions

```typescript
// For single item (product detail page)
import { getUnifiedStock } from '@/lib/zoho/stock-cache';

const { stock, source } = await getUnifiedStock(itemId, {
  fetchOnMiss: true,      // Fetch from API if not in cache
  context: 'product-detail',
});

// source: 'cache' | 'api' | 'unavailable'
```

```typescript
// For multiple items (shop list page)
import { getUnifiedStockBulk } from '@/lib/zoho/stock-cache';

const stockMap = await getUnifiedStockBulk(itemIds, {
  context: 'shop-list',
});

// Returns: Map<itemId, stock>
```

### Why Unified Functions?

```yaml
PROBLEM SOLVED:
  - Shop list showed different stock than product detail page
  - Root cause: Different fallback sources when Redis cache missed
  - List fell back to Books API (total across ALL warehouses)
  - Detail fell back to Inventory API (warehouse-specific)

SOLUTION:
  - Unified functions use ONLY Redis cache as stock source
  - On cache miss, detail page fetches from API and caches result
  - Next list page load sees the cached value
  - NEVER fall back to Books item.available_stock
```

## Stock Data Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                     STOCK DATA FLOW                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ZOHO BOOKS/INVENTORY                                            │
│  │                                                               │
│  ├── Transaction occurs (Invoice, Bill, etc.)                    │
│  │   │                                                           │
│  │   └──► Webhook fires to /api/webhooks/zoho                    │
│  │        │                                                      │
│  │        ├── Extract item IDs from payload                      │
│  │        │                                                      │
│  │        └──► quickSyncStock(itemIds)                           │
│  │             │                                                 │
│  │             ├── Fetch item with locations from API            │
│  │             │                                                 │
│  │             ├── Extract Main WareHouse stock                  │
│  │             │   └── location_available_for_sale_stock         │
│  │             │                                                 │
│  │             └──► Update Redis cache                           │
│  │                  │                                            │
│  │                  └──► Revalidate Next.js ISR cache            │
│  │                                                               │
│  └── Periodic sync (every 15 min)                                │
│      │                                                           │
│      └──► Full cache refresh from Books API                      │
│                                                                  │
│  REDIS CACHE (Upstash)                                           │
│  │                                                               │
│  ├── Key: stock:{itemId}                                         │
│  ├── Value: number (warehouse-specific stock)                    │
│  ├── TTL: 4 hours (14400 seconds)                                │
│  │                                                               │
│  └──► Read by: getUnifiedStock(), getUnifiedStockBulk()          │
│                                                                  │
│  NEXT.JS APPLICATION                                             │
│  │                                                               │
│  ├── Shop List Page                                              │
│  │   └── getUnifiedStockBulk(itemIds) → Redis                    │
│  │                                                               │
│  └── Product Detail Page                                         │
│      └── getUnifiedStock(itemId) → Redis → API (if miss)         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Cache Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| **Stock Cache TTL** | 4 hours (14400s) | Reduced from 24h for freshness |
| **Redis Provider** | Upstash | https://fine-mole-41883.upstash.io |
| **Key Pattern** | `stock:{itemId}` | One key per item |
| **Freshness Check** | 10 minutes | For periodic sync trigger |
| **Sync Frequency** | Every 15 minutes | Vercel Cron |

## Debugging Stock Sync

### Check Cache Status

```bash
# Check cache health
curl "https://www.tsh.sale/api/sync/stock?action=status"

# Expected response:
{
  "status": "healthy",
  "itemCount": 450,
  "lastSync": "2025-12-11T10:30:00Z",
  "cacheAge": "2 hours"
}
```

### Force Full Sync

```bash
# Trigger full sync
curl "https://www.tsh.sale/api/sync/stock?action=sync&secret=tsh-stock-sync-2024&force=true"

# Expected response:
{
  "success": true,
  "itemsSynced": 450,
  "duration": "45s"
}
```

### Revalidate Caches

```bash
# Revalidate all caches
curl "https://www.tsh.sale/api/revalidate?tag=all&secret=tsh-revalidate-2024"

# Revalidate products only
curl "https://www.tsh.sale/api/revalidate?tag=products&secret=tsh-revalidate-2024"
```

### Check Specific Item Stock

```bash
# Debug specific item
curl "https://www.tsh.sale/api/debug/stock?itemId=2646610000109854052"

# Expected response:
{
  "itemId": "2646610000109854052",
  "cachedStock": 15,
  "apiStock": 15,
  "source": "cache",
  "warehouse": "Main WareHouse"
}
```

## Troubleshooting

### Stock Shows 0 When It Shouldn't

| Check | Command | Fix |
|-------|---------|-----|
| Cache empty? | `?action=status` | Run full sync |
| Wrong warehouse? | Check `location_name` | Must be "Main WareHouse" |
| Stale cache? | Check `lastSync` | Force sync if > 4h old |
| Webhook not firing? | Check Zoho webhook logs | Reconfigure webhook |

### Stock Discrepancy Between List/Detail

| Cause | Symptoms | Fix |
|-------|----------|-----|
| Cache miss | Detail shows different | Run sync, check TTL |
| Wrong function | Using deprecated fn | Use `getUnifiedStock()` |
| Books fallback | List shows ALL warehouse | Never use `item.available_stock` |

### Webhook Not Updating Stock

1. **Check Zoho Webhook Configuration**
   - Go to Zoho Settings → Webhooks
   - Verify URL: `https://www.tsh.sale/api/webhooks/zoho`
   - Verify events are enabled

2. **Check Vercel Logs**
   ```bash
   vercel logs --follow | grep webhook
   ```

3. **Verify Webhook Payload**
   - Add logging to webhook handler
   - Check if `resource_name` matches expected

4. **Test Webhook Manually**
   ```bash
   curl -X POST https://www.tsh.sale/api/webhooks/zoho \
     -H "Content-Type: application/json" \
     -d '{"resource_name":"item","event_type":"updated","resource_id":"123"}'
   ```

## Adding New Stock-Affecting Feature

When adding features that affect stock:

### 1. Identify Webhook Events

```yaml
Example: Adding "Stock Transfer" feature
Events needed:
  - inventorytransfer.created
  - inventorytransfer.updated
```

### 2. Update Webhook Handler

```typescript
// src/app/api/webhooks/zoho/route.ts

case "inventorytransfer":
  const itemIds = extractItemIdsFromTransfer(payload);
  await quickSyncStock(itemIds, `stock transfer: ${eventType}`);
  await revalidateProducts(`stock transfer: ${eventType}`);
  break;
```

### 3. Test the Flow

```bash
# 1. Create test transaction in Zoho
# 2. Check webhook received
curl "https://www.tsh.sale/api/debug/webhook-log"

# 3. Verify stock updated
curl "https://www.tsh.sale/api/debug/stock?itemId=<ITEM_ID>"
```

## Golden Rules

1. **Single Source of Truth**: ALWAYS use `getUnifiedStock()` or `getUnifiedStockBulk()`

2. **Never Use Books Fallback**: NEVER use `item.available_stock` (combines ALL warehouses)

3. **Warehouse Isolation**: ONLY show stock from "Main WareHouse" (ID: 2646610000000077024)

4. **Cache Before Display**: Ensure Redis cache is populated before displaying stock

5. **Graceful Degradation**: Show "Check availability" if stock unavailable, NOT zero

6. **Sync Before Deploy**: Run full stock sync before deploying stock-related changes

## Related Files

| File | Purpose |
|------|---------|
| `src/lib/zoho/stock-cache.ts` | Stock caching, unified functions |
| `src/lib/zoho/products.ts` | Product fetching, stock extraction |
| `src/app/api/webhooks/zoho/route.ts` | Webhook handler |
| `src/app/api/sync/stock/route.ts` | Sync endpoint |
| `.claude/STOCK_RULES.md` | Stock display rules |
| `.claude/skills/tsh-stock/SKILL.md` | Basic stock skill |

## Checklist for Stock Changes

Before modifying stock-related code:

- [ ] Read `.claude/STOCK_RULES.md`
- [ ] Check Redis cache status
- [ ] Understand which webhook events affect the change
- [ ] Use unified stock functions
- [ ] Test on staging first
- [ ] Run full sync after deploy
- [ ] Verify list/detail stock consistency
