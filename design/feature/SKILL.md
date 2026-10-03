---
name: feature
description: Creating a new feature module in the React web frontend. Triggers when adding a new page, creating a feature folder under src/features/, implementing a new domain area (auth, admin, manager, staff), or adding components, hooks, services, or types for a frontend feature.
---

## Nguyên tắc bắt buộc

1. **Tuân thủ tuyệt đối** cấu trúc folder, naming convention, và code pattern được định nghĩa trong skill này — không tự ý thêm layer, đổi tên file, hay gọi API trực tiếp trong component.
2. **Hỏi trước khi code** nếu bất kỳ yêu cầu nào chưa rõ (feature thuộc domain nào, data shape từ API, role nào được truy cập). Không đoán mò — một câu hỏi ngắn tốt hơn một giờ implement sai hướng.

---

# FE Feature Pattern

## Feature folder structure

```
src/features/{domain}/
├── pages/
│   └── {Name}Page.tsx
├── components/
│   └── {Name}.tsx
├── hooks/
│   └── use{Name}.ts
├── services/
│   └── {name}.service.ts
├── schemas/
│   └── {name}.schema.ts
└── types/
    └── {name}.types.ts
```

## Page component

```tsx
const BatteryListPage: React.FC = () => {
  const { data, isLoading, error } = useBatteries();

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorBoundary error={error} />;

  return (
    <div>
      {data?.items.map(b => <BatteryCard key={b.id} battery={b} />)}
    </div>
  );
};

export default BatteryListPage;
```

## Service layer

```ts
// src/features/admin/services/battery.service.ts
import { axiosInstance } from '@/shared/lib/axios';
import type { Battery, BatteryCreatePayload } from '../types/battery.types';
import type { PaginationResponse } from '@/shared/types/api.types';

const BASE = '/api/batteries';

export const batteryService = {
  getList: (params: BatteryGetListParams) =>
    axiosInstance.get<PaginationResponse<Battery>>(BASE, { params }).then(r => r.data),

  getById: (id: string) =>
    axiosInstance.get<Battery>(`${BASE}/${id}`).then(r => r.data),

  create: (payload: BatteryCreatePayload) =>
    axiosInstance.post<Battery>(BASE, payload).then(r => r.data),

  update: (id: string, payload: Partial<BatteryCreatePayload>) =>
    axiosInstance.put<Battery>(`${BASE}/${id}`, payload).then(r => r.data),

  delete: (id: string) =>
    axiosInstance.delete(`${BASE}/${id}`).then(r => r.data),
};
```

## Naming

| Type | Pattern | Example |
|------|---------|---------|
| Page | `{Name}Page.tsx` | `BatteryListPage.tsx` |
| Component | `{Name}.tsx` | `BatteryCard.tsx` |
| Hook | `use{Name}.ts` | `useBatteries.ts` |
| Service | `{name}.service.ts` | `battery.service.ts` |
| Schema | `{name}.schema.ts` | `battery.schema.ts` |
| Types | `{name}.types.ts` | `battery.types.ts` |

## Zod schema (form validation)

```ts
// src/features/admin/schemas/battery.schema.ts
import { z } from 'zod';

export const batteryCreateSchema = z.object({
  name: z.string().min(1, 'Required').max(100, 'Max 100 chars'),
  locationId: z.string().uuid('Invalid ID').optional(),
});

export type BatteryCreateFormValues = z.infer<typeof batteryCreateSchema>;
```

```tsx
// trong component form — kết hợp react-hook-form + zod
const form = useForm<BatteryCreateFormValues>({
  resolver: zodResolver(batteryCreateSchema),
});
```

## Rules

- Never call API in component — always through `services/` → TanStack Query hook
- `useState` only for UI state (modal, tab, toggle)
- Zustand only for auth session — not server state
- Features must NOT import from other features — only from `shared/`
- Never hardcode URLs — use `env.VITE_API_BASE_URL`
- Never create a new Axios instance — use `shared/lib/axios.ts`
- Never store token in localStorage — use `js-cookie`
