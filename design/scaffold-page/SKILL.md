---
name: scaffold-page
description: Scaffold a new Next.js App Router page following FixNow conventions — correct route group, Server vs Client component split, layout integration, mobile-first Tailwind. Use when user says "tạo trang X", "scaffold page /pricing", "thêm route /track".
---

# scaffold-page

Tạo trang Next.js mới theo pattern của FixNow.

## Hỏi user (nếu chưa rõ)

1. Tên route (vd: `/services`, `/admin/appointments`).
2. Trang public, customer (cần auth), hay admin?
3. Có cần data từ DB không? Nếu có thì model nào?
4. Có form không? Nếu có thì zod schema cần tạo?

## Workflow

### 1. Xác định route group

| Loại | Group | Path mẫu |
|------|-------|----------|
| Public | `(public)` | `app/(public)/services/page.tsx` |
| Auth (login/register) | `(auth)` | `app/(auth)/login/page.tsx` |
| Customer (cần auth) | `(customer)` | `app/(customer)/my-appointments/page.tsx` |
| Admin | `admin/` (no group) | `app/admin/appointments/page.tsx` |

### 2. Tạo file structure

Tối thiểu:
- `page.tsx` — Server Component, fetch data, render layout.
- `loading.tsx` — Suspense fallback (skeleton).
- `error.tsx` — Error boundary (Client Component required).

Optional:
- `_components/<name>.tsx` — Client components dùng riêng cho page này (prefix `_` để Next bỏ qua routing).

### 3. Server Component template (page.tsx)

```tsx
import { Metadata } from 'next';
import { db } from '@/db';
import { someTable } from '@/db/schema';

export const metadata: Metadata = {
  title: '<Tên trang> | FixNow',
  description: '<mô tả ngắn>',
};

export default async function <PageName>Page() {
  const data = await db.query.someTable.findMany({
    where: eq(someTable.isActive, true),
    orderBy: [asc(someTable.sortOrder)],
  });

  return (
    <main className="container mx-auto px-4 py-8 md:py-12">
      <h1 className="text-3xl md:text-4xl font-bold mb-6">
        <Title tiếng Việt>
      </h1>
      {/* sections */}
    </main>
  );
}
```

### 4. Client Component template (interactive)

```tsx
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';

interface Props {
  initialData: SomeType[];
}

export function <Name>({ initialData }: Props) {
  const [state, setState] = useState(initialData);
  return <div>{/* ... */}</div>;
}
```

### 5. Loading template

```tsx
export default function Loading() {
  return (
    <main className="container mx-auto px-4 py-8 md:py-12">
      <div className="h-10 w-64 bg-muted rounded animate-pulse mb-6" />
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="h-48 bg-muted rounded animate-pulse" />
        ))}
      </div>
    </main>
  );
}
```

### 6. Error template

```tsx
'use client';

import { Button } from '@/components/ui/button';

export default function Error({ reset }: { reset: () => void }) {
  return (
    <main className="container mx-auto px-4 py-12 text-center">
      <h2 className="text-2xl font-bold mb-2">Đã xảy ra lỗi</h2>
      <p className="text-muted-foreground mb-6">
        Vui lòng thử lại hoặc liên hệ hotline.
      </p>
      <Button onClick={reset}>Thử lại</Button>
    </main>
  );
}
```

## Checklist hoàn thành

- [ ] Route đặt đúng group (public/auth/customer/admin).
- [ ] `page.tsx` là Server Component (default), trừ khi cần interactivity ở root.
- [ ] Có `loading.tsx` với skeleton.
- [ ] Có `error.tsx` nếu page fetch data.
- [ ] Metadata tiếng Việt (title + description).
- [ ] Mobile 375px OK (test DevTools).
- [ ] Tailwind class theo `docs/ui-system.md`.
- [ ] Cập nhật `docs/routes.md` nếu route mới.
- [ ] Update CLAUDE.md "Trạng thái hiện tại" tick checkbox.

## Liên kết

- Khi cần UI components phức tạp → spawn agent `fixnow-ui-builder`.
- Khi cần API endpoint cho page → dùng skill `scaffold-api`.
