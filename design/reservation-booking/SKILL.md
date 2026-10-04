---
name: reservation-booking
description: >
  Build a complete reservation/booking system — slot management, calendar UI,
  booking CRUD, confirmation emails, and Stripe/Paymob deposit payments.
  Triggers when user asks to build a booking site, reservation system,
  appointment scheduler, appointment booking, slot booking, booking dashboard,
  or booking page with calendar.
---

# Reservation/Booking System Agent

## Schema

```typescript
// prisma/schema.prisma
model Service {
  id            String    @id @default(cuid())
  name          String
  slug          String    @unique
  description   String?
  price         Decimal
  currency      String    @default("USD")
  durationMins   Int       @default(60)
  capacity      Int       @default(1)
  bufferMins   Int       @default(15)
  isActive     Boolean   @default(true)
  slots        TimeSlot[]
  bookings     Booking[]
  createdAt    DateTime  @default(now())
  updatedAt    DateTime  @updatedAt
}

model TimeSlot {
  id        String   @id @default(cuid())
  serviceId String
  service   Service  @relation(fields: [serviceId], references: [id])
  dayOfWeek Int      // 0=Sunday, 6=Saturday
  startTime String
  endTime   String
  slotCount Int      @default(1)
}

model Booking {
  id           String         @id @default(cuid())
  serviceId    String
  service      Service        @relation(fields: [serviceId], references: [id])
  guestEmail   String
  guestName    String
  guestPhone   String?
  bookingDate  DateTime      @db.Date
  startTime   String
  endTime     String
  guestsCount Int            @default(1)
  status      BookingStatus   @default(PENDING)
  totalAmount Decimal
  depositPaid Decimal        @default(0)
  paymentProvider String?    // 'paymob' | 'stripe'
  paymobOrderId   String?
  stripePaymentId String?
  specialRequests String?
  confirmedAt  DateTime?
  cancelledAt DateTime?
  createdAt    DateTime      @default(now())
  updatedAt    DateTime      @updatedAt
  @@index([serviceId, bookingDate])
}

enum BookingStatus { PENDING CONFIRMED CANCELLED COMPLETED NO_SHOW }
```

## Slot Generation

```typescript
// lib/slots.ts
export function generateAvailableSlots(params: {
  serviceId: string;
  date: Date;
  durationMins: number;
  bufferMins: number;
}): TimeSlotOption[] {
  // 1. Get service's time windows for this day of week
  const windows = await prisma.timeSlot.findMany({
    where: { serviceId: params.serviceId, dayOfWeek: params.date.getDay() }
  });

  // 2. Get existing confirmed bookings for this date
  const existingBookings = await prisma.booking.findMany({
    where: { serviceId: params.serviceId, bookingDate: params.date, status: { in: ['CONFIRMED', 'PENDING'] } },
    select: { startTime: true, guestsCount: true }
  });

  // 3. Generate slots from time windows
  const slots: TimeSlotOption[] = [];
  for (const window of windows) {
    let current = parseTime(window.startTime);
    const end = parseTime(window.endTime);

    while (addMinutes(current, params.durationMins) <= end) {
      const slotStart = formatTime(current);
      const slotEnd = formatTime(addMinutes(current, params.durationMins + params.bufferMins));

      const conflicts = existingBookings.filter(b => timesOverlap(slotStart, slotEnd, b.startTime, b.startTime));

      slots.push({
        startTime: slotStart,
        endTime: formatTime(addMinutes(current, params.durationMins)),
        available: conflicts.length < 10,
        remaining: 10 - conflicts.length,
      });

      current = addMinutes(current, 30); // 30-min slot increments
    }
  }

  return slots;
}

export function timesOverlap(aStart: string, aEnd: string, bStart: string, bEnd: string): boolean {
  return aStart < bEnd && bStart < aEnd;
}
```

## Calendar UI (react-day-picker)

```tsx
// pages/book/[serviceSlug].tsx
import { DayPicker } from 'react-day-picker';
import 'react-day-picker/style.css';

export default function BookingPage() {
  const [selectedDate, setSelectedDate] = useState<Date | undefined>();
  const [selectedSlot, setSelectedSlot] = useState<TimeSlotOption | null>(null);

  const disabledDays = [{ before: new Date() }, { dayOfWeek: [0] }]; // no Sundays

  return (
    <div className="max-w-2xl mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">{service.name} — Book a Slot</h1>

      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <DayPicker mode="single" selected={selectedDate} onSelect={setSelectedDate}
            disabled={disabledDays} />

          {selectedDate && (
            <div className="mt-4">
              <h3 className="font-semibold mb-2">Available Times</h3>
              <div className="grid grid-cols-3 gap-2">
                {slots.map(slot => (
                  <button key={slot.startTime}
                    disabled={!slot.available}
                    onClick={() => setSelectedSlot(slot)}
                    className={`px-3 py-2 rounded text-sm ${
                      selectedSlot?.startTime === slot.startTime
                        ? 'bg-blue-600 text-white'
                        : slot.available ? 'bg-gray-100 hover:bg-gray-200' : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    }`}>
                    {slot.startTime}
                    {!slot.available && <span className="block text-xs text-red-400">Full</span>}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        <BookingForm service={service} date={selectedDate} slot={selectedSlot} />
      </div>
    </div>
  );
}
```

## Booking Flow

```
1. User selects date → slots fetched via API
2. User selects slot → booking form shown
3. User submits → create PENDING booking (no payment yet)
4. Redirect to payment (Paymob iframe or Stripe Elements)
5. Payment success → webhook updates booking to CONFIRMED
6. Send confirmation email via Resend
7. Show confirmation page
```

## Payment Integration (Paymob)

```typescript
// lib/paymob-booking.ts
export async function createBookingPayment(bookingId: string): Promise<string> {
  const booking = await prisma.booking.findUnique({ where: { id: bookingId } });

  const paymobService = new PaymobService();
  const amountCents = Number(booking.totalAmount) * 100;

  const order = await paymobService.createOrder(amountCents, `booking_${bookingId}`);
  const paymentKey = await paymobService.getPaymentKey(order.id, amountCents, {
    email: booking.guestEmail,
    name: booking.guestName,
    phone: booking.guestPhone,
  });

  await prisma.booking.update({
    where: { id: bookingId },
    data: { paymobOrderId: String(order.id) }
  });

  return `https://accept.paymob.com/v2/choose/payment-methods?token=${paymentKey}`;
}
```

## Admin Dashboard

```tsx
// pages/admin/bookings/index.tsx
// - List all bookings with filter by status/date/service
// - CSV export
// - Bulk status update
// - Click row → booking detail page
```

## Confirmation Email (Resend)

```tsx
// emails/BookingConfirmation.tsx
export function BookingConfirmationEmail({ booking }: { booking: Booking }) {
  return (
    <Email>
      <Text>Hi {booking.guestName},</Text>
      <Text>Your booking is confirmed!</Text>
      <Text>📅 {formatDate(booking.bookingDate)} at {booking.startTime}</Text>
      <Text>📍 {booking.service.name}</Text>
      <Text>Confirmation #: {booking.id.slice(-8).toUpperCase()}</Text>
    </Email>
  );
}
```
