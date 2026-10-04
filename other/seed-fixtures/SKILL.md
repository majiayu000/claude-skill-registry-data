---
name: seed-fixtures
description: Manage db/seed.ts for FixNow with realistic Vietnamese fixture data for services, parts, admin user, and sample appointments using Drizzle. Use when user says "seed data", "tạo dữ liệu mẫu", "reset demo data", "thêm linh kiện vào DB".
---

# seed-fixtures

Quản lý `db/seed.ts` với dữ liệu mẫu tiếng Việt thực tế.

## Nguyên tắc

- **Idempotent**: dùng `onConflictDoNothing` hoặc `onConflictDoUpdate`.
- **Realistic VN**: tên dịch vụ + giá theo SPEC, tiếng Việt có dấu (UTF-8).
- **Đủ demo**: ≥ 8 services, ≥ 4-5 parts mỗi loại, 1 admin, 2-3 sample appointments.
- **An toàn**: KHÔNG seed password plain text. Hash bằng bcrypt.

## Template

```ts
// db/seed.ts
import { db } from './index';
import { users, servicePrices, parts, appointments } from './schema';
import { eq } from 'drizzle-orm';
import bcrypt from 'bcryptjs';

async function main() {
  // 1. Admin
  await db.insert(users).values({
    fullName: 'Admin FixNow',
    phone: '0900000001',
    email: 'admin@fixnow.local',
    passwordHash: await bcrypt.hash('admin123', 10),
    role: 'ADMIN',
  }).onConflictDoNothing({ target: users.phone });

  // 2. Customer demo
  await db.insert(users).values({
    fullName: 'Nguyễn Văn A',
    phone: '0987654321',
    email: 'demo@example.com',
    passwordHash: await bcrypt.hash('demo1234', 10),
    role: 'CUSTOMER',
  }).onConflictDoNothing({ target: users.phone });

  // 3. Services
  const servicesData = [
    { serviceName: 'Kiểm tra & chẩn đoán máy', priceFrom: 'Miễn phí', note: 'Tận nơi trong 5km', sortOrder: 0 },
    { serviceName: 'Vệ sinh laptop / PC', priceFrom: 'Từ 150.000đ', note: 'Bao gồm tra keo tản nhiệt', sortOrder: 1 },
    { serviceName: 'Cài đặt Windows + phần mềm cơ bản', priceFrom: 'Từ 200.000đ', note: 'Windows bản quyền tính riêng', sortOrder: 2 },
    { serviceName: 'Diệt virus / mã độc', priceFrom: 'Từ 200.000đ', note: 'Giữ nguyên dữ liệu', sortOrder: 3 },
    { serviceName: 'Nâng cấp RAM / SSD', priceFrom: 'Theo linh kiện', note: 'Báo giá trước khi sửa', sortOrder: 4 },
    { serviceName: 'Thay pin laptop', priceFrom: 'Từ 500.000đ', note: 'Tùy dòng máy', sortOrder: 5 },
    { serviceName: 'Sửa lỗi phần cứng', priceFrom: 'Báo giá sau khi kiểm tra', note: 'Có thể mang về xưởng', sortOrder: 6 },
    { serviceName: 'Cài mạng / wifi / máy in', priceFrom: 'Từ 150.000đ', note: 'Hỗ trợ văn phòng nhỏ', sortOrder: 7 },
    { serviceName: 'Hỗ trợ từ xa (TeamViewer / AnyDesk)', priceFrom: 'Từ 100.000đ', note: 'Lỗi phần mềm nhẹ', sortOrder: 8 },
  ];
  for (const s of servicesData) {
    await db.insert(servicePrices).values({ ...s, isActive: true })
      .onConflictDoNothing({ target: servicePrices.serviceName });
  }

  // 4. Parts
  const partsData = [
    { type: 'RAM',       name: 'RAM Laptop DDR4 8GB 3200MHz',       price: '650.000đ',   warranty: '36 tháng' },
    { type: 'RAM',       name: 'RAM Laptop DDR4 16GB 3200MHz',      price: '1.250.000đ', warranty: '36 tháng' },
    { type: 'RAM',       name: 'RAM PC DDR4 16GB 3200MHz',          price: '1.100.000đ', warranty: '36 tháng' },
    { type: 'RAM',       name: 'RAM DDR5 16GB 4800MHz',             price: '1.850.000đ', warranty: '36 tháng' },
    { type: 'SSD',       name: 'SSD NVMe 256GB Samsung',            price: '850.000đ',   warranty: '36 tháng' },
    { type: 'SSD',       name: 'SSD NVMe 512GB Samsung',            price: '1.450.000đ', warranty: '36 tháng' },
    { type: 'SSD',       name: 'SSD NVMe 1TB Kingston',             price: '2.150.000đ', warranty: '36 tháng' },
    { type: 'SSD',       name: 'SSD SATA 480GB Kingston',           price: '850.000đ',   warranty: '36 tháng' },
    { type: 'HDD',       name: 'HDD Laptop 1TB Seagate',            price: '1.350.000đ', warranty: '24 tháng' },
    { type: 'HDD',       name: 'HDD PC 2TB WD Blue',                price: '1.650.000đ', warranty: '24 tháng' },
    { type: 'BATTERY',   name: 'Pin laptop Dell Inspiron 14 (zin)', price: '750.000đ',   warranty: '6 tháng' },
    { type: 'BATTERY',   name: 'Pin laptop HP Pavilion 15 (zin)',   price: '800.000đ',   warranty: '6 tháng' },
    { type: 'BATTERY',   name: 'Pin laptop Lenovo ThinkPad (zin)',  price: '950.000đ',   warranty: '6 tháng' },
    { type: 'ACCESSORY', name: 'Adapter sạc laptop Dell 65W',       price: '350.000đ',   warranty: '6 tháng' },
    { type: 'ACCESSORY', name: 'Bàn phím laptop HP (thay tại nhà)', price: '450.000đ',   warranty: '3 tháng' },
    { type: 'ACCESSORY', name: 'Keo tản nhiệt Thermalright TF7',    price: '120.000đ',   warranty: 'Không' },
    { type: 'ACCESSORY', name: 'Quạt tản nhiệt laptop (đôi)',       price: '350.000đ',   warranty: '3 tháng' },
  ] as const;
  for (const p of partsData) {
    await db.insert(parts).values({ ...p, isActive: true })
      .onConflictDoNothing({ target: parts.name });
  }

  // 5. Sample appointments
  const customer = await db.query.users.findFirst({ where: eq(users.phone, '0987654321') });
  if (customer) {
    await db.insert(appointments).values({
      appointmentCode: 'FN-2026-0001',
      userId: customer.id,
      customerName: customer.fullName,
      phone: customer.phone,
      address: '123 Nguyễn Trãi, Q.5, TP.HCM',
      deviceType: 'LAPTOP',
      serviceGroup: 'Sửa chữa phần mềm',
      issueDescription: 'Máy bị chậm, mở Chrome treo, nghi virus.',
      preferredTime: new Date(Date.now() + 86_400_000),
      status: 'RECEIVED',
    }).onConflictDoNothing({ target: appointments.appointmentCode });

    await db.insert(appointments).values({
      appointmentCode: 'FN-2026-0002',
      userId: null,
      customerName: 'Trần Thị B',
      phone: '0912345678',
      address: '45 Lê Lợi, Q.1, TP.HCM',
      deviceType: 'PC',
      serviceGroup: 'Nâng cấp linh kiện',
      issueDescription: 'Muốn nâng RAM 8GB lên 16GB, gắn thêm SSD.',
      preferredTime: new Date(Date.now() + 172_800_000),
      status: 'IN_PROGRESS',
    }).onConflictDoNothing({ target: appointments.appointmentCode });
  }

  console.log('Seed completed');
}

main()
  .catch((e) => { console.error(e); process.exit(1); })
  .finally(async () => { process.exit(0); });
```

## Đăng ký lệnh seed

Thêm vào `package.json`:

```json
{
  "scripts": {
    "db:seed": "tsx db/seed.ts"
  }
}
```

Cài tsx:
```bash
npm i -D tsx
```

## Chạy

```bash
npm run db:seed
```

## Verify

Mở Drizzle Studio:
```bash
npx drizzle-kit studio
```

Hoặc query trực tiếp qua psql.

## Checklist

- [ ] Tất cả seed dùng `onConflictDoNothing` hoặc `onConflictDoUpdate`.
- [ ] Password hash bcrypt cost ≥ 10.
- [ ] Admin user có role 'ADMIN'.
- [ ] ≥ 8 services + ≥ 16 parts + 2 sample appointments.
- [ ] Tiếng Việt có dấu, format giá VND.
- [ ] Đã chạy `npm run db:seed` và verify trong Studio.
