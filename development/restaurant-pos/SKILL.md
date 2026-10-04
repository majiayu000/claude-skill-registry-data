---
name: restaurant-pos
description: >
  Build a Restaurant Point of Sale (POS) system — menu CRUD, table management,
  floor plan, order flow, Kitchen Display System (KDS), tip tracking, and multi-outlet support.
  Triggers when user asks to build a restaurant POS, restaurant management,
  menu management, restaurant ordering, kitchen display, or table management.
---

# Restaurant POS Agent

## Schema

```typescript
// prisma/schema.prisma
model Outlet {
  id       String  @id @default(cuid())
  name     String
  code     String  @unique
  tables   Table[]
  categories Category[]
  orders   Order[]
  createdAt DateTime @default(now())
}

model Table {
  id       String     @id @default(cuid())
  outletId String
  outlet   Outlet     @relation(fields: [outletId], references: [id])
  number   Int
  capacity Int        @default(4)
  status   TableStatus @default(OPEN)
  orders   Order[]
  createdAt DateTime @default(now())
  @@unique([outletId, number])
}

enum TableStatus { OPEN OCCUPIED RESERVED CLEANING }

model Category {
  id       String     @id @default(cuid())
  outletId String
  outlet   Outlet     @relation(fields: [outletId], references: [id])
  name     String
  sortOrder Int       @default(0)
  items    MenuItem[]
}

model MenuItem {
  id         String   @id @default(cuid())
  categoryId String
  category   Category @relation(fields: [categoryId], references: [id])
  name       String
  price      Decimal
  cost       Decimal?
  variants   MenuVariant[]
  isAvailable Boolean @default(true)
  imageUrl   String?
  orderItems OrderItem[]
  createdAt  DateTime @default(now())
}

model MenuVariant {
  id      String  @id @default(cuid())
  itemId  String
  item    MenuItem @relation(fields: [itemId], references: [id])
  name    String
  price   Decimal
}

model Order {
  id        String      @id @default(cuid())
  tableId   String
  table     Table       @relation(fields: [tableId], references: [id])
  outletId  String
  outlet    Outlet      @relation(fields: [outletId], references: [id])
  serverName String
  status    OrderStatus @default(OPEN)
  items     OrderItem[]
  payments  Payment[]
  subtotal   Decimal    @default(0)
  tax        Decimal    @default(0)
  tip        Decimal    @default(0)
  total     Decimal    @default(0)
  notes     String?
  openedAt  DateTime   @default(now())
  closedAt  DateTime?
}

enum OrderStatus { OPEN SUBMITTED IN_PROGRESS READY SERVED PAID SPLIT }

model OrderItem {
  id         String     @id @default(cuid())
  orderId    String
  order      Order      @relation(fields: [orderId], references: [id])
  menuItemId String
  menuItem   MenuItem   @relation(fields: [menuItemId], references: [id])
  variantId  String?
  quantity   Int        @default(1)
  unitPrice  Decimal
  status     ItemStatus @default(PENDING)
  notes      String?
  sentAt     DateTime?
  doneAt     DateTime?
}

enum ItemStatus { PENDING COOKING DONE }

model Payment {
  id          String        @id @default(cuid())
  orderId     String
  order       Order         @relation(fields: [orderId], references: [id])
  method      PaymentMethod
  amount      Decimal
  tip         Decimal       @default(0)
  serverName  String?
  processedAt DateTime      @default(now())
}

enum PaymentMethod { CASH CARD QR }
```

## Floor Plan View

```tsx
// pages/pos/index.tsx
export function FloorPlan() {
  const { data: tables } = trpc.table.list.useQuery();

  const statusColor: Record<TableStatus, string> = {
    OPEN: 'bg-green-100 border-green-400',
    OCCUPIED: 'bg-orange-100 border-orange-400',
    RESERVED: 'bg-blue-100 border-blue-400',
    CLEANING: 'bg-yellow-100 border-yellow-400',
  };

  return (
    <div className="grid grid-cols-4 gap-4 p-4">
      {tables.map(table => (
        <button key={table.id}
          onClick={() => router.push(`/pos/table/${table.id}`)}
          className={`p-4 rounded-lg border-2 text-center ${statusColor[table.status]}`}>
          <div className="text-lg font-bold">T{table.number}</div>
          <div className="text-xs">{table.status}</div>
          <div className="text-xs text-gray-500">{table.capacity} seats</div>
        </button>
      ))}
    </div>
  );
}
```

## Kitchen Display System (KDS)

```tsx
// pages/kitchen/index.tsx
// Real-time via polling or WebSocket

export function KitchenDisplay() {
  const { data: items } = trpc.kitchen.pendingItems.useQuery(undefined, {
    refetchInterval: 10000,
  });

  const byStation = groupBy(items ?? [], item => item.station);

  return (
    <div className="flex gap-4 p-4 overflow-x-auto">
      {Object.entries(byStation).map(([station, stationItems]) => (
        <div key={station} className="flex-1 min-w-64">
          <h2 className="text-xl font-bold mb-4 bg-gray-800 text-white p-2 rounded">{station}</h2>
          {stationItems.map(item => (
            <KDSItem key={item.id} item={item} />
          ))}
        </div>
      ))}
    </div>
  );
}

function KDSItem({ item }: { item: KitchenItem }) {
  const [age, setAge] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setAge(Math.floor((Date.now() - new Date(item.sentAt).getTime()) / 60000));
    }, 10000);
    return () => clearInterval(interval);
  }, []);

  const urgencyColor = age > 15 ? 'bg-red-500 text-white' : age > 8 ? 'bg-orange-400' : 'bg-white';

  return (
    <div className={`rounded p-3 mb-2 shadow border ${urgencyColor}`}>
      <div className="font-bold">#{item.orderId.slice(-4)} — Table {item.tableNumber}</div>
      <div className="text-2xl font-bold">{item.quantity}x {item.menuItemName}</div>
      {item.variant && <div className="text-sm">{item.variant}</div>}
      {item.notes && <div className="text-sm italic mt-1">{item.notes}</div>}
      <button onClick={() => markDone(item.id)}
        className="mt-2 px-3 py-1 bg-green-600 text-white rounded text-sm w-full">
        DONE {age > 0 && `(${age}m)`}
      </button>
    </div>
  );
}
```

## Tip Allocation

```typescript
// lib/tip-allocation.ts
export function allocateTips(shifts: ShiftRecord[]): TipAllocation[] {
  const totalSales = shifts.reduce((sum, s) => sum + s.sales, 0);
  return shifts.map(s => ({
    serverName: s.serverName,
    sales: s.sales,
    tipPct: s.sales / totalSales,
    tipAmount: s.tips * (s.sales / totalSales),
  }));
}
```

## Bill Split

```typescript
// lib/bill-split.ts
type SplitType = 'equal' | 'by-item' | 'by-person';

export function splitBill(order: Order, splitType: SplitType, params: SplitParams) {
  switch (splitType) {
    case 'equal': {
      const perPerson = Number(order.total) / params.personCount;
      return Array(params.personCount).fill({ amount: perPerson });
    }
    case 'by-item': {
      return params.assignments.map(a => ({
        personId: a.personId,
        items: a.items,
        amount: a.items.reduce((sum, i) => sum + Number(i.unitPrice) * i.quantity, 0),
      }));
    }
    case 'by-person': {
      return params.personTotals;
    }
  }
}
```
