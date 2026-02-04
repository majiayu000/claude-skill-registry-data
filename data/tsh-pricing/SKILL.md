---
name: tsh-pricing
description: |
  TSH pricing logic with Zoho Inventory pricebooks. Use when:
  (1) Displaying product prices on any page
  (2) Working with different price lists (Consumer, Wholesale, Technical, Retail)
  (3) Implementing price display for public vs authenticated users
  (4) Debugging "Contact for price" issues
  (5) Adding pricing to new components
  (6) Understanding customer price list assignment
---

# TSH Pricing Rules

## Golden Rule

```
NEVER display item.rate (base sell price from Zoho)
ALWAYS fetch price from the appropriate pricebook
If item NOT in pricebook → show "Contact for price"
```

## Price List IDs (MEMORIZE)

| ID | Name | Currency | Use Case |
|-----|------|----------|----------|
| `2646610000049149103` | Consumer | IQD | Public visitors (DEFAULT) |
| `2646610000004453985` | Retailor | USD | Retail shops |
| `2646610000057419683` | Technical IQD | IQD | Technicians (IQD) |
| `2646610000045742089` | Technical USD | USD | Technicians (USD) |
| `2646610000004152175` | Wholesale A | USD | Cash wholesale (نقدي) |
| `2646610000004453961` | Wholesale B | USD | Credit wholesale (اجل) |

## Code Constants

```typescript
// src/lib/zoho/price-lists.ts
import { PRICE_LIST_IDS, PRICE_LIST_INFO } from '@/lib/zoho/price-lists';

PRICE_LIST_IDS.CONSUMER       // '2646610000049149103'
PRICE_LIST_IDS.RETAILOR       // '2646610000004453985'
PRICE_LIST_IDS.TECHNICAL_IQD  // '2646610000057419683'
PRICE_LIST_IDS.TECHNICAL_USD  // '2646610000045742089'
PRICE_LIST_IDS.WHOLESALE_A    // '2646610000004152175'
PRICE_LIST_IDS.WHOLESALE_B    // '2646610000004453961'
```

## Price Selection Logic

### Public Visitors (Not Logged In)
```typescript
const priceListId = PRICE_LIST_IDS.CONSUMER; // Always IQD
```

### Authenticated Users
```typescript
import { getZohoCustomerByEmail } from '@/lib/zoho/customers';

const customer = await getZohoCustomerByEmail(session.user.email);
const priceListId = customer?.price_list_id || PRICE_LIST_IDS.CONSUMER;
```

## Fetching Prices

### Get Full Pricebook
```typescript
import { getPriceList } from '@/lib/zoho/price-lists';

const pricebook = await getPriceList(PRICE_LIST_IDS.CONSUMER);
// Returns: { pricebook_id, name, currency_code, pricebook_items: [...] }
```

### Get Price for Single Item
```typescript
import { getPriceForItem } from '@/lib/zoho/price-lists';

const { price, currency, inPriceList } = await getPriceForItem(
  itemId,
  PRICE_LIST_IDS.CONSUMER
);

if (!inPriceList) {
  // Show "Contact for price"
}
```

## Display Component

```typescript
'use client';
import { useTranslations } from 'next-intl';

interface PriceDisplayProps {
  price: number;
  currency: string;
  inPriceList: boolean;
}

export function PriceDisplay({ price, currency, inPriceList }: PriceDisplayProps) {
  const t = useTranslations('products');

  if (!inPriceList) {
    return (
      <span className="text-muted-foreground">
        {t('contactForPrice')}
      </span>
    );
  }

  return (
    <span className="text-lg font-bold">
      {price.toLocaleString()} {currency}
    </span>
  );
}
```

## Product Card with Pricing

```typescript
interface Product {
  id: string;
  name: string;
  price: number;
  currency: string;
  inPriceList: boolean;
}

export function ProductCard({ product }: { product: Product }) {
  const t = useTranslations('products');

  return (
    <Card>
      <CardContent>
        <h3>{product.name}</h3>
        {product.inPriceList ? (
          <span className="text-lg font-bold">
            {product.price.toLocaleString()} {product.currency}
          </span>
        ) : (
          <span className="text-muted-foreground">
            {t('contactForPrice')}
          </span>
        )}
      </CardContent>
    </Card>
  );
}
```

## Shop Page Pattern

```typescript
// src/app/[locale]/(public)/shop/page.tsx
import { PRICE_LIST_IDS, getPriceList } from '@/lib/zoho/price-lists';
import { getAllProductsComplete } from '@/lib/zoho/products';

export default async function ShopPage() {
  const [products, pricebook] = await Promise.all([
    getAllProductsComplete(),
    getPriceList(PRICE_LIST_IDS.CONSUMER),
  ]);

  // Create price lookup map
  const priceMap = new Map();
  pricebook.pricebook_items?.forEach((item: any) => {
    priceMap.set(item.item_id, {
      price: item.pricebook_rate,
      currency: pricebook.currency_code,
    });
  });

  // Enrich products
  const productsWithPrices = products.map(p => ({
    ...p,
    price: priceMap.get(p.item_id)?.price || 0,
    currency: priceMap.get(p.item_id)?.currency || 'IQD',
    inPriceList: priceMap.has(p.item_id),
  }));

  return <ProductsContent products={productsWithPrices} />;
}
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| All "Contact for price" | Token rate limited | Check Upstash Redis env vars |
| Wrong prices | Wrong pricebook ID | Verify `priceListId` |
| Missing items | Not in pricebook | Add in Zoho Inventory |
| Wrong currency | Wrong pricebook | Check PRICE_LIST_IDS |

## Debug Commands

```bash
# Check if prices fetch correctly
curl "https://www.tsh.sale/api/debug/prices"

# Revalidate price cache
curl "https://www.tsh.sale/api/revalidate?tag=price-lists&secret=tsh-revalidate-2024"
```

## Checklist for Pricing Features

- [ ] Import `PRICE_LIST_IDS` from `@/lib/zoho/price-lists`
- [ ] Determine correct price list (public vs authenticated)
- [ ] Fetch pricebook with `getPriceList()`
- [ ] Handle `inPriceList: false` case
- [ ] Display "Contact for price" translation
- [ ] Show correct currency (IQD or USD)
