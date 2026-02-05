---
name: tsh-stock
description: |
  TSH stock and warehouse logic for Main WareHouse. Use when:
  (1) Displaying stock levels on product pages
  (2) Understanding warehouse configuration
  (3) Debugging stock display issues (showing 0 when shouldn't)
  (4) Working with "In Stock" / "Out of Stock" badges
  (5) Implementing stock-based filtering
  (6) Understanding stock sync architecture (webhooks, cron, manual)
  (7) Understanding the difference between list and detail page stock
---

# TSH Stock Rules

## Warehouse Configuration

| Setting | Value |
|---------|-------|
| **Warehouse Name** | `Main WareHouse` |
| **Warehouse ID** | `2646610000000077024` |
| **Business Location** | Main TSH Business |
| **Stock Type** | Accounting Stock (Available for Sale) |
| **Field** | `location_available_for_sale_stock` |
| **Array** | `locations` (NOT `warehouses`) |

## Stock Formula

```
Available for Sale = Stock on Hand - Committed Stock
```

- **Stock on Hand**: Physical stock in warehouse
- **Committed Stock**: Reserved for pending orders
- **Available for Sale**: What can actually be sold

## Critical: Correct Field Names

```typescript
// CORRECT - Use these
const WHOLESALE_LOCATION_NAME = 'Main WareHouse';

const location = item.locations?.find(
  loc => loc.location_name === WHOLESALE_LOCATION_NAME
);
const stock = location?.location_available_for_sale_stock;

// WRONG - Never use
item.warehouses                    // Wrong array name
warehouse_available_stock          // Wrong field name
stock_on_hand                      // Includes committed stock
item.available_stock               // Combines ALL warehouses
```

## Code Implementation

### Constants
```typescript
// src/lib/zoho/stock-cache.ts & src/lib/zoho/products.ts
const WHOLESALE_LOCATION_NAME = 'Main WareHouse';
const WHOLESALE_WAREHOUSE_ID = '2646610000000077024';
```

### Stock Extraction Function
```typescript
function getWholesaleAvailableStock(item: ZohoItemWithLocations): number {
  if (item.locations && item.locations.length > 0) {
    const wholesaleLocation = item.locations.find(
      (loc) => loc.location_name === WHOLESALE_LOCATION_NAME
    );

    if (wholesaleLocation) {
      return wholesaleLocation.location_available_for_sale_stock || 0;
    }
  }
  // NEVER fall back to item.available_stock (combines all warehouses)
  return 0;
}
```

### Unified Stock Functions (ALWAYS USE)
```typescript
// For single item (detail page)
const { stock, source } = await getUnifiedStock(itemId, {
  fetchOnMiss: true,
  context: 'product-detail',
});

// For multiple items (list page)
const stockMap = await getUnifiedStockBulk(itemIds, {
  context: 'shop-list',
});
```

### Type Definition
```typescript
interface ZohoItem {
  item_id: string;
  name: string;
  available_stock: number;
  locations?: Array<{
    location_id: string;
    location_name: string;
    location_stock_on_hand: number;
    location_available_for_sale_stock: number;
  }>;
}
```

## List vs Detail Page

### Detail Page (Accurate Stock)
- Endpoint: `GET /inventory/v1/items/{item_id}`
- Returns: Full item with `locations` array
- Stock: Accurate per-warehouse breakdown

```typescript
export async function getProduct(itemId: string) {
  const response = await zohoFetch(`/inventory/v1/items/${itemId}`, {
    params: { organization_id: process.env.ZOHO_ORGANIZATION_ID },
  });

  const item = response.item;
  const stock = getWholesaleAvailableStock(item);
  return { ...item, stock };
}
```

### List Page (Filtered Stock)
- Endpoint: `GET /inventory/v1/items`
- Note: Does NOT return `locations` array
- Use `warehouse_id` parameter to filter

```typescript
export async function getAllProductsComplete() {
  const response = await zohoFetch('/inventory/v1/items', {
    params: {
      organization_id: process.env.ZOHO_ORGANIZATION_ID,
      warehouse_id: WHOLESALE_WAREHOUSE_ID,
      status: 'active',
    },
  });

  return response.items.map(item => ({
    ...item,
    stock: item.available_stock ?? 0,
  }));
}
```

## Stock Badge Component

```typescript
'use client';
import { Badge } from '@/components/ui/badge';
import { useTranslations } from 'next-intl';

export function StockBadge({ stock }: { stock: number }) {
  const t = useTranslations('products');

  if (stock > 10) {
    return <Badge variant="default">{t('inStock')}</Badge>;
  }

  if (stock > 0) {
    return (
      <Badge variant="warning">
        {t('lowStock', { count: stock })}
      </Badge>
    );
  }

  return <Badge variant="secondary">{t('outOfStock')}</Badge>;
}
```

## Translations

```json
// en.json
{
  "products": {
    "inStock": "In Stock",
    "outOfStock": "Out of Stock",
    "lowStock": "Only {count} left",
    "available": "available"
  }
}

// ar.json
{
  "products": {
    "inStock": "متوفر",
    "outOfStock": "غير متوفر",
    "lowStock": "متبقي {count} فقط",
    "available": "متاح"
  }
}
```

## Product Card with Stock

```typescript
export function ProductCard({ product }) {
  const t = useTranslations('products');

  return (
    <Card>
      <CardContent>
        <h3>{product.name}</h3>
        <div className="flex items-center gap-2 mt-2">
          {product.stock > 0 ? (
            <>
              <span className="text-green-600">{t('inStock')}</span>
              <span className="text-sm text-muted-foreground">
                ({product.stock} {t('available')})
              </span>
            </>
          ) : (
            <span className="text-red-600">{t('outOfStock')}</span>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Stock shows 0 | Wrong field | Use `location_available_for_sale_stock` |
| Stock shows 0 | Wrong array | Use `locations` not `warehouses` |
| Stock shows 0 | Wrong warehouse | Use ID `2646610000000077024` |
| Stock shows 0 | All committed | Stock reserved for orders |
| Not updating | Cache stale | Revalidate products cache |
| Different list/detail | List lacks locations | Expected - use warehouse_id filter |

## Debug Commands

```bash
# Check stock data
curl "https://www.tsh.sale/api/debug/stock"

# Revalidate product cache
curl "https://www.tsh.sale/api/revalidate?tag=products&secret=tsh-revalidate-2024"
```

## Other Locations (DO NOT USE FOR THIS CONSOLE)

| Location | Type | Purpose | Use |
|----------|------|---------|-----|
| **Main WareHouse** | Warehouse | B2B wholesale | ✅ THIS CONSOLE |
| Dora Store | Warehouse | Retail shop | ❌ EndUser Console |
| inactive 1/2 | Warehouse | Inactive | ❌ Delete |

Only use **Main WareHouse** (`2646610000000077024`) for this B2B console.

## Stock Sync Commands

```bash
# Check cache status
curl "https://www.tsh.sale/api/sync/stock?action=status"

# Force full sync
curl "https://www.tsh.sale/api/sync/stock?action=sync&secret=tsh-stock-sync-2024&force=true"
```

## Checklist

- [ ] Use `getUnifiedStock()` or `getUnifiedStockBulk()` for stock retrieval
- [ ] NEVER use `item.available_stock` directly
- [ ] Handle 0 stock with "Out of Stock" badge
- [ ] Add stock translations (en.json, ar.json)
- [ ] Verify list/detail stock consistency after changes
