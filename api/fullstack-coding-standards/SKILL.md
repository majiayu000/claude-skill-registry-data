---
name: fullstack-coding-standards
description: 명시적 `/fullstack-coding-standards` 호출 전용 풀스택 참고서. 일반 구현에는 자동 적용하지 않고 네이티브 코딩 능력과 프로젝트 규칙을 우선한다.
---

# Fullstack Coding Standards - 통합 패키지

## 포함 파일

```
fullstack-coding-standards/
├── SKILL.md                    # 이 파일 (상세 코드 예시)
├── references/                 # 핵심 규칙 (명시적 로드)
│   └── rules.md                # 스킬 호출 시 읽는 규칙 본문
└── templates/                  # 코드 템플릿
```

---

## 참조 로딩 규칙

1. 이 `SKILL.md`를 워크플로와 예시의 소유자로 사용합니다.
2. 스킬을 명시적으로 호출했을 때 `references/rules.md`를 읽고 현재 프로젝트에 필요한 규칙만 적용합니다.
3. Java/Spring Boot 또는 DB 연동 상세가 필요할 때만 해당 `templates/` 파일을 추가로 읽습니다.

이 규칙 본문은 스킬 안의 참조 문서이며 커스텀 에이전트로 등록되지 않습니다.

---

## 프론트엔드 코드 예시

### apiClient.ts (fetch 래퍼)

```typescript
// src/lib/apiClient.ts
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...this.getAuthHeaders(),
      },
      ...options,
    });

    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = '/login';
        throw new ApiError(401, 'Unauthorized');
      }
      throw new ApiError(response.status, await response.text());
    }

    return response.json();
  }

  private getAuthHeaders(): Record<string, string> {
    const token = localStorage.getItem('accessToken');
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  get<T>(endpoint: string) { return this.request<T>(endpoint); }
  post<T>(endpoint: string, data: unknown) {
    return this.request<T>(endpoint, { method: 'POST', body: JSON.stringify(data) });
  }
  put<T>(endpoint: string, data: unknown) {
    return this.request<T>(endpoint, { method: 'PUT', body: JSON.stringify(data) });
  }
  delete<T>(endpoint: string) {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
```

### TanStack Query 3계층 예시

```typescript
// [1] features/user/api/userService.ts
import { apiClient } from '@/lib/apiClient';
import type { User, CreateUserDto } from '../types/user';

export const userService = {
  getAll: () => apiClient.get<User[]>('/users'),
  getById: (id: string) => apiClient.get<User>(`/users/${id}`),
  create: (data: CreateUserDto) => apiClient.post<User>('/users', data),
  update: (id: string, data: Partial<User>) => apiClient.put<User>(`/users/${id}`, data),
  delete: (id: string) => apiClient.delete(`/users/${id}`),
};
```

```typescript
// [2] features/user/api/keys.ts — Query Key Factory
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
};
```

```typescript
// [3] features/user/api/queries.ts
import { useQuery } from '@tanstack/react-query';
import { userService } from './userService';
import { userKeys } from './keys';

export const useGetUsers = () =>
  useQuery({ queryKey: userKeys.lists(), queryFn: userService.getAll });

export const useGetUser = (id: string) =>
  useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => userService.getById(id),
    enabled: !!id,
  });
```

```typescript
// [3] features/user/api/mutations.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { userService } from './userService';
import { userKeys } from './keys';

export const useCreateUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: userService.create,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: userKeys.lists() }),
  });
};

export const useDeleteUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: userService.delete,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: userKeys.lists() }),
  });
};
```

### 공유 타입 예시

```typescript
// shared/types/user.ts
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user';
  createdAt: string;
}

export interface CreateUserDto {
  email: string;
  name: string;
  password: string;
}

// shared/types/common.ts
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: { code: string; message: string; fieldErrors?: FieldError[] };
}

export interface PaginatedResponse<T> {
  content: T[];
  page: number;
  size: number;
  totalElements: number;
  totalPages: number;
}

export interface FieldError {
  field: string;
  message: string;
}
```

---

## 백엔드 코드 예시

Java/Spring Boot 상세 코드 예시는 `templates/` 폴더 참조:

- **`templates/java-spring-boot.md`** — 4계층 구조, @Transactional, DTO 변환, 예외 처리, Validation, 테스트 패턴 전체 코드

---

## DB 연동 코드 예시

DB 설정 전체 코드는 `templates/db-integration.md` 참조.

### Spring Boot 필수 설정 (application.yml)

```yaml
spring:
  jpa:
    hibernate:
      # 기본값 — snake_case 자동 변환 (명시 안 해도 됨)
      naming:
        physical-strategy: org.hibernate.boot.model.naming.CamelCaseToUnderscoresNamingStrategy
      ddl-auto: validate          # 운영: validate, 개발: update
  jackson:
    serialization:
      write-dates-as-timestamps: false  # ISO 8601 문자열로 출력
    time-zone: UTC
  flyway:
    enabled: true
    locations: classpath:db/migration
```

### 자료형 매핑 예시

```java
// Entity - 올바른 타입 매핑
@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;                    // BIGINT → Long

    private BigDecimal totalAmount;     // DECIMAL → BigDecimal

    @Enumerated(EnumType.STRING)        // ENUM → STRING (ORDINAL 금지!)
    @Column(length = 20)
    private OrderStatus status;

    private Instant createdAt;          // TIMESTAMP WITH TIME ZONE → Instant

    private String firstName;           // → DB: first_name (자동 변환)
}
```

```java
// Response DTO - BIGINT/DECIMAL은 string으로 직렬화
public record OrderResponse(
    String id,                          // Long → String (JS 정밀도 보호)
    String totalAmount,                 // BigDecimal → String
    OrderStatus status,
    String createdAt                    // Instant → ISO 8601 String
) {
    public static OrderResponse from(Order order) {
        return new OrderResponse(
            String.valueOf(order.getId()),
            order.getTotalAmount().toPlainString(),
            order.getStatus(),
            order.getCreatedAt().toString()
        );
    }
}
```

### 프론트엔드 Zod 검증

```typescript
import { z } from 'zod';

const OrderSchema = z.object({
  id: z.string(),                                    // BIGINT → string
  totalAmount: z.string(),                           // DECIMAL → string
  status: z.enum(['PENDING', 'PROCESSING', 'COMPLETED', 'CANCELLED']),
  createdAt: z.string().datetime(),                  // ISO 8601
  deletedAt: z.string().datetime().nullable(),       // NULL 허용
});

type Order = z.infer<typeof OrderSchema>;            // 타입 자동 추론

// API 호출 시 검증
async function fetchOrder(id: string): Promise<Order> {
  const data = await apiClient.get(`/orders/${id}`);
  const result = OrderSchema.safeParse(data);
  if (!result.success) {
    console.error('API 응답 스키마 불일치:', result.error.flatten());
    throw new Error('Invalid API response');
  }
  return result.data;
}
```

### 날짜 로컬 변환 (프론트엔드)

```typescript
// UTC → 로컬 표시
function formatDateTime(utcString: string): string {
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit',
  }).format(new Date(utcString));
}

// 사용자 입력 → UTC로 변환 후 API 전송
function toUTCString(localDate: Date): string {
  return localDate.toISOString();  // 항상 UTC
}
```

---

## 리소스 안전 코드 예시

> 명시적으로 읽은 참고 규칙의 "리소스 안전" 상세 예시. 원칙: 리소스를 만드는 편집에서 해제를 같이 쓴다.

### React — useEffect cleanup (등록과 해제를 같은 자리에서)

```typescript
useEffect(() => {
  const onResize = () => setWidth(window.innerWidth);
  window.addEventListener('resize', onResize);      // 참조를 유지해야 제거 가능
  const timer = setInterval(refresh, 30_000);

  return () => {                                    // 등록한 것을 전부 해제
    window.removeEventListener('resize', onResize);
    clearInterval(timer);
  };
}, []);
```

### React — await 후 상태 갱신 가드

서버 상태는 TanStack Query 훅이 표준 (취소/캐시 자동 처리).
직접 비동기 효과가 불가피한 지점(SSE, 파일 다운로드, 비-Query 유틸)만 이 패턴 사용:

```typescript
useEffect(() => {
  let alive = true;                                 // 언마운트 후 setState 차단
  userService.getAll().then(users => {
    if (alive) setUsers(users);
  });
  return () => { alive = false; };
}, []);
```

### 상한 있는 캐시 (LRU)

```typescript
// 커스텀 캐시를 만들 때는 반드시 상한을 함께 만든다
class BoundedCache<K, V> {
  private map = new Map<K, V>();
  constructor(private maxSize = 100) {}

  get(key: K): V | undefined {
    const v = this.map.get(key);
    if (v !== undefined) { this.map.delete(key); this.map.set(key, v); } // 최근 사용으로 갱신
    return v;
  }

  set(key: K, value: V) {
    if (this.map.has(key)) this.map.delete(key);
    else if (this.map.size >= this.maxSize) {
      this.map.delete(this.map.keys().next().value!);                    // 가장 오래된 항목 제거
    }
    this.map.set(key, value);
  }
}
```

### Java — try-with-resources + ExecutorService 수명

```java
// 에러 경로에서도 해제가 보장된다
try (Connection conn = dataSource.getConnection();
     PreparedStatement ps = conn.prepareStatement(SQL)) {
    // ...
}

// ExecutorService는 빈 소멸 시점에 정리
@PreDestroy
void shutdownExecutor() {
    executor.shutdown();
}
```

### Python — 컨텍스트 매니저 + 태스크 취소

```python
# 파일/커넥션/락은 with로 — 예외가 나도 해제된다
async def export_csv(path: Path) -> None:
    async with aiofiles.open(path, "w") as f:
        await f.write(header)

# 백그라운드 태스크는 참조를 보관하고 종료 시 취소한다
class Poller:
    def start(self) -> None:
        self._task = asyncio.create_task(self._poll())

    async def stop(self) -> None:
        self._task.cancel()
```

---

## 환경 설정 예시

```
# .env.development
VITE_API_URL=http://localhost:8000/api

# .env.production
VITE_API_URL=/api

# .env.staging
VITE_API_URL=https://staging-api.example.com/api
```

- 환경별 `.env` 파일 분리
- `.env`는 `.gitignore`에 추가 (`.env.example`만 커밋)

---

## 잘못된 예시 (금지 패턴)

```typescript
// 금지 - URL 하드코딩
fetch('http://localhost:8000/api/users');

// 금지 - apiClient를 거치지 않는 직접 fetch
fetch('/api/users');

// 금지 - 컴포넌트에서 직접 API 호출
function UserList() {
  const [users, setUsers] = useState([]);
  useEffect(() => {
    fetch('/api/users').then(r => r.json()).then(setUsers); // 금지
  }, []);
}

// 올바른 예
function UserList() {
  const { data: users, isLoading } = useGetUsers();  // TanStack Query 훅
  if (isLoading) return <Loading />;
  return <ul>{users?.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```
