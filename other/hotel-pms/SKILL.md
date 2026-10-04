---
name: hotel-pms
description: >
  Build a Hotel Property Management System (PMS) in Laravel or Next.js/Prisma.
  Covers: room management, guest accounts, hotel packages with meal plans (RO/BB/HB/FB/AI),
  meal window quotas with real-time deduction, reservation validation, refund policy engine,
  multi-hotel support, and Filament admin dashboard. Triggers when user asks to build
  a hotel management system, PMS, guest management, room management, hotel packages,
  meal plan system, or quota tracking.
---

# Hotel PMS Agent

## Core Entities

```
Hotel (property) → has many Rooms, Packages, Restaurants, Reservations
Room → belongs to Hotel (types: STANDARD/DELUXE/SUITE/PENTHOUSE)
Guest → has Reservations
HotelPackage → belongs to Hotel (codes: RO/BB/HB/FB/AI)
MealQuota → belongs to Guest + Restaurant + Date + Window
Restaurant → belongs to Hotel (linked to package outlet access)
Reservation → belongs to Hotel + Guest + Room (+ optional Package)
```

## Step 1 — Design Schema (Next.js/Prisma/PostgreSQL)

```typescript
// prisma/schema.prisma

model Hotel {
  id        String   @id @default(cuid())
  name      String
  slug      String   @unique
  address   String?
  timezone  String   @default("Africa/Cairo")
  rooms     Room[]
  packages  HotelPackage[]
  restaurants Restaurant[]
  reservations Reservation[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Room {
  id        String   @id @default(cuid())
  hotelId   String
  hotel     Hotel    @relation(fields: [hotelId], references: [id])
  number    String
  floor     Int?
  type      RoomType
  status    RoomStatus @default(AVAILABLE)
  amenities String[]
  pricePerNight Decimal
  createdAt DateTime @default(now())
  @@unique([hotelId, number])
}

enum RoomType { STANDARD DELUXE SUITE PENTHOUSE }
enum RoomStatus { AVAILABLE OCCUPIED MAINTENANCE OUT_OF_SERVICE }

model Guest {
  id           String   @id @default(cuid())
  name         String
  email        String?  @unique
  phone        String
  idDocType    String?
  idDocNumber  String?
  passportExpiry DateTime?
  notes        String?
  reservations Reservation[]
  mealQuotas   MealQuota[]
  createdAt    DateTime @default(now())
  updatedAt    DateTime @updatedAt
}

model HotelPackage {
  id        String       @id @default(cuid())
  hotelId   String
  hotel     Hotel        @relation(fields: [hotelId], references: [id])
  name      String
  code      PackageCode
  mealsPerDay Int        @default(1)  // RO=0, BB=1, HB=2, FB=3, AI=3+snacks
  outlets   String[]     // ["main-restaurant", "pool-bar"]
  pricePerNight Decimal
  cancellationHours Int  @default(48)
  isActive  Boolean      @default(true)
  createdAt DateTime @default(now())
}

enum PackageCode { RO BB HB FB AI }

model Restaurant {
  id        String   @id @default(cuid())
  hotelId   String
  hotel     Hotel    @relation(fields: [hotelId], references: [id])
  name      String
  code      String
  mealWindows MealWindow[]
  createdAt DateTime @default(now())
}

model MealWindow {
  id          String     @id @default(cuid())
  restaurantId String
  restaurant  Restaurant @relation(fields: [restaurantId], references: [id])
  name        String
  timeStart   String
  timeEnd     String
  dailyQuota  Int
  isActive    Boolean    @default(true)
  allocations MealQuota[]
  createdAt   DateTime   @default(now())
}

model MealQuota {
  id            String     @id @default(cuid())
  guestId       String
  guest         Guest      @relation(fields: [guestId], references: [id])
  mealWindowId  String
  mealWindow    MealWindow @relation(fields: [mealWindowId], references: [id])
  date          DateTime   @db.Date
  window        MealWindowType
  used          Int        @default(0)
  entitled      Int
  @@unique([guestId, mealWindowId, date, window])
}

enum MealWindowType { BREAKFAST LUNCH DINNER SNACK }

model Reservation {
  id             String             @id @default(cuid())
  hotelId        String
  hotel          Hotel              @relation(fields: [hotelId], references: [id])
  guestId        String
  guest          Guest              @relation(fields: [guestId], references: [id])
  roomId         String
  checkIn        DateTime
  checkOut       DateTime
  packageId      String?
  package        HotelPackage?      @relation(fields: [packageId], references: [id])
  status         ReservationStatus   @default(CONFIRMED)
  totalAmount    Decimal
  depositPaid    Decimal            @default(0)
  paymobOrderId  String?
  paymobTxId     String?
  refundEligible Boolean            @default(true)
  notes          String?
  createdAt      DateTime           @default(now())
  updatedAt      DateTime           @updatedAt
}

enum ReservationStatus { CONFIRMED CHECKED_IN CHECKED_OUT CANCELLED NO_SHOW }
```

## Step 2 — Reservation Validation

```typescript
// lib/reservation-validator.ts

export async function validateReservation(params: {
  hotelId: string;
  roomId: string;
  checkIn: Date;
  checkOut: Date;
  guestId?: string;
  packageId?: string;
}): Promise<{ valid: boolean; errors: string[] }> {
  const errors: string[] = [];

  // 1. Check room availability (no overlapping confirmed bookings)
  const overlap = await prisma.reservation.findFirst({
    where: {
      roomId: params.roomId,
      status: { in: ['CONFIRMED', 'CHECKED_IN'] },
      OR: [
        { checkIn: { lt: params.checkOut }, checkOut: { gt: params.checkIn } }
      ]
    }
  });
  if (overlap) errors.push('Room is not available for selected dates');

  // 2. Check minimum stay
  const nights = differenceInDays(params.checkOut, params.checkIn);
  if (nights < 1) errors.push('Minimum stay is 1 night');

  // 3. Check-in must be in the future
  if (params.checkIn < new Date()) errors.push('Check-in date must be in the future');

  // 4. Package eligibility
  if (params.packageId) {
    const pkg = await prisma.hotelPackage.findUnique({ where: { id: params.packageId } });
    if (!pkg?.isActive) errors.push('Selected package is not available');
  }

  return { valid: errors.length === 0, errors };
}
```

## Step 3 — Meal Quota Enforcer

```typescript
// lib/quota-enforcer.ts

export async function useMealQuota(params: {
  guestId: string;
  mealWindowId: string;
  date: Date;
  window: 'BREAKFAST' | 'LUNCH' | 'DINNER' | 'SNACK';
  count: number;
}): Promise<{ allowed: boolean; message: string }> {
  // 1. Get guest's reservation + package
  const guestReservations = await prisma.reservation.findMany({
    where: { guestId: params.guestId, status: 'CHECKED_IN' },
    include: { package: true }
  });

  const activePkg = guestReservations[0]?.package;
  if (!activePkg) return { allowed: false, message: 'No active package' };

  // 2. Check restaurant is in package outlets
  const window = await prisma.mealWindow.findUnique({
    where: { id: params.mealWindowId },
    include: { restaurant: true }
  });
  if (!activePkg.outlets.includes(window!.restaurant.code)) {
    return { allowed: false, message: `${window!.name} not included in ${activePkg.name}` };
  }

  // 3. Check current usage vs entitlement
  const quota = await prisma.mealQuota.findUnique({
    where: {
      guestId_mealWindowId_date_window: {
        guestId: params.guestId,
        mealWindowId: params.mealWindowId,
        date: params.date,
        window: params.window
      }
    }
  });

  const remaining = (quota?.entitled ?? 0) - (quota?.used ?? 0);
  if (remaining < params.count) {
    return { allowed: false, message: `Only ${remaining} slots remaining` };
  }

  // 4. Increment usage
  await prisma.mealQuota.upsert({
    where: { id: quota?.id ?? 'tmp' },
    create: { guestId: params.guestId, mealWindowId: params.mealWindowId, date: params.date, window: params.window, entitled: activePkg.mealsPerDay, used: params.count },
    update: { used: { increment: params.count } }
  });

  return { allowed: true, message: 'OK' };
}
```

## Step 4 — Refund Policy Engine

```typescript
// lib/refund-calculator.ts

export function calculateRefund(params: {
  totalAmount: number;
  depositPaid: number;
  cancellationHoursBefore: number;
  checkIn: Date;
}): { refundAmount: number; isEligible: boolean; reason: string } {
  const hoursUntilCheckIn = differenceInHours(params.checkIn, new Date());

  if (hoursUntilCheckIn >= params.cancellationHoursBefore) {
    return {
      refundAmount: params.depositPaid,
      isEligible: true,
      reason: `Cancelled ${params.cancellationHoursBefore}h+ before check-in — full refund`
    };
  }

  if (hoursUntilCheckIn >= 24) {
    return {
      refundAmount: Math.floor(params.depositPaid * 0.5),
      isEligible: true,
      reason: 'Cancelled 24-48h before check-in — 50% refund'
    };
  }

  return {
    refundAmount: 0,
    isEligible: false,
    reason: 'Cancelled <24h before check-in — no refund eligible'
  };
}
```

## Step 5 — Filament Admin Resources (Laravel)

```bash
php artisan make:filament-resource Guest --generate
php artisan make:filament-resource Room --generate
php artisan make:filament-resource Reservation --generate
php artisan make:filament-resource HotelPackage --generate
php artisan make:filament-resource MealWindow --generate
```

## Step 6 — Multi-Hotel Property Context

```typescript
// Property context: switch via subdomain or route prefix
// /cairo/admin/rooms  vs  /luxor/admin/rooms

export function PropertyProvider({ children }: { children: React.ReactNode }) {
  const [hotelSlug, setHotelSlug] = useState<string | null>(null);

  useEffect(() => {
    const hostname = window.location.hostname;
    const slug = hostname.split('.')[0];
    setHotelSlug(slug === 'app' ? null : slug);
  }, []);

  return <PropertyContext.Provider value={{ hotelSlug }}>{children}</PropertyContext.Provider>;
}
```

## Package Meal Tier Quick Reference

| Code | Name | Meals per day | Outlets included |
|------|------|--------------|-----------------|
| RO | Room Only | 0 | None |
| BB | Bed & Breakfast | 1 | Breakfast only |
| HB | Half Board | 2 | Breakfast + dinner |
| FB | Full Board | 3 | Breakfast + lunch + dinner |
| AI | All Inclusive | 3+snacks | All outlets, all day |
