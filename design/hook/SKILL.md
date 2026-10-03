---
name: hook
description: Creating a TanStack Query hook (useQuery or useMutation) in the React frontend. Triggers when implementing data fetching, server state management, cache configuration, SLA countdown polling, or any hook that calls a service function.
---

## Nguyên tắc bắt buộc

1. **Tuân thủ tuyệt đối** naming convention, cache strategy, và code pattern được định nghĩa trong skill này — không tự ý đặt `staleTime` tùy tiện hay dùng `refetchInterval` sai mục đích.
2. **Hỏi trước khi code** nếu bất kỳ yêu cầu nào chưa rõ (data type nào cần polling, mutation cần invalidate queryKey nào, hook dùng cho feature nào). Không đoán mò — một câu hỏi ngắn tốt hơn một giờ implement sai hướng.

---

# FE TanStack Query Hook Pattern

## Query Key — dùng `QUERY_KEY` + `KEY` từ `shared/utils/queryKeys.ts`

```ts
// useQuery — QUERY_KEY factory (có params)
queryKey: QUERY_KEY.batteries.list(params)
queryKey: QUERY_KEY.batteries.detail(id)

// invalidateQueries broad — KEY root (invalidate tất cả batteries queries)
queryClient.invalidateQueries({ queryKey: KEY.batteries })

// invalidateQueries narrow — chỉ invalidate 1 record
queryClient.invalidateQueries({ queryKey: QUERY_KEY.batteries.detail(id) })
```

Không dùng inline array `['batteries', params]` — luôn dùng factory từ `queryKeys.ts`.

---

## useQuery — list

```ts
import { QUERY_KEY } from '@/shared/utils/queryKeys';

export const useBatteries = (params: BatteryGetListParams) => {
  return useQuery({
    queryKey: QUERY_KEY.batteries.list(params),
    queryFn: () => batteryService.getList(params),
    staleTime: 1000 * 60 * 5,  // 5 min — xem bảng cache bên dưới
  });
};
```

## useQuery — detail

```ts
export const useBatteryDetail = (id: string) => {
  return useQuery({
    queryKey: QUERY_KEY.batteries.detail(id),
    queryFn: () => batteryService.getById(id),
    enabled: !!id,
  });
};
```

## useMutation — create/update/delete

Axios interceptor đã throw `EntityError` (listErrors) / `HttpError` (message) khi `isSuccess: false`.
Dùng `handleErrorApi` trong `onError` — không tự toast trong hook.

```ts
import { KEY } from '@/shared/utils/queryKeys';
import { handleErrorApi } from '@/shared/lib/errors';

export const useCreateBattery = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: BatteryCreatePayload) => batteryService.create(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: KEY.batteries });
      toast.success('Tạo pin thành công');
    },
    onError: (error) => handleErrorApi({ error }),
  });
};
```

## useMutation — form submit (try-catch + setError)

`onError` dùng cho non-form flows (delete, approve, cancel).
Form submit phải dùng `try-catch` + `setError` để map lỗi về đúng field:

```ts
// Trong component
const { handleSubmit, setError } = useForm<BatteryCreatePayload>();
const { mutateAsync } = useCreateBattery();

const onSubmit = async (data: BatteryCreatePayload) => {
  try {
    await mutateAsync(data);
  } catch (error) {
    handleErrorApi({ error, setError }); // EntityError → setError field, HttpError → toast
  }
};
```

## SLA countdown — polling pattern

```ts
// staleTime: 0 + refetchInterval: 30s syncs deadline from server every 30s
// setInterval only updates UI countdown display between fetches
export const useTicketDetail = (id: string) => {
  return useQuery({
    queryKey: QUERY_KEY.tickets.detail(id),
    queryFn: () => ticketService.getById(id),
    staleTime: 0,
    refetchInterval: 30_000,
  });
};

// In component — local countdown display
const [remaining, setRemaining] = useState(0);
useEffect(() => {
  if (!ticket?.slaDeadline) return;
  const update = () => setRemaining(new Date(ticket.slaDeadline).getTime() - Date.now());
  update();
  const id = setInterval(update, 1000);
  return () => clearInterval(id);
}, [ticket?.slaDeadline]);
```

## Cache staleTime per data type

| Data | staleTime | refetchInterval |
|------|-----------|-----------------|
| Ticket queue (manager) | `30_000` | — |
| SLA countdown | `0` | `30_000` |
| Battery list | `1000 * 60 * 5` | — |
| Battery config (threshold/settings) | `1000 * 60 * 10` | — |
| Dashboard stats | `1000 * 60` | — |
| User list (admin) | `1000 * 60 * 5` | — |

## QueryClient defaults (App.tsx)

```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 2,
      gcTime: 1000 * 60 * 10,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});
```

## Rules

- `staleTime: 0` does NOT auto-refetch — must pair with `refetchInterval` for true polling.
- Never use inline `queryKey: ['batteries', params]` — always use `QUERY_KEY` factory.
- `onError: handleErrorApi` for non-form mutations. Form submit → `try-catch` + `setError`.
- `invalidateQueries({ queryKey: KEY.batteries })` to invalidate all, `QUERY_KEY.batteries.detail(id)` to narrow.
