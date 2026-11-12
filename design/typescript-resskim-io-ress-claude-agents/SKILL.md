---
name: typescript
description: "TypeScript 타입 시스템 — Generic, Utility Types, Discriminated Union, Type Narrowing, Branded Type, Zod 스키마 검증, tsconfig 설정. Use when 복잡한 타입을 설계하거나 타입 안전성을 높이고 tsconfig 를 정할 때."
---

# TypeScript 심화 가이드

TypeScript 5.x 타입 시스템 심화, 제네릭 패턴, Utility Types, 타입 안전성 종합 가이드.

## Quick Reference

```
타입 정의 선택
    │
    ├─ 객체 형태 정의 ────────> interface (extends로 확장)
    ├─ Union / 조합 타입 ────> type (|, &, 조건부)
    ├─ 열거값 ───────────────> const enum 또는 as const
    │
    타입 안전성 강화
    │
    ├─ 런타임 검증 ──────────> Zod + z.infer<typeof schema>
    ├─ 상태머신 ─────────────> Discriminated Union
    ├─ 식별 가능한 원시값 ──> Branded Types
    └─ 타입 좁히기 ──────────> type guards + in + instanceof
```

---

## TypeScript 5.x 주요 기능

### const Type Parameters

제네릭 인자를 리터럴 타입으로 추론.

```typescript
// const 없이: string[]으로 추론
function getRoutes<T extends readonly string[]>(routes: T) {
  return routes;
}
const r1 = getRoutes(['home', 'about']); // string[]

// const 사용: 리터럴 튜플로 추론
function getRoutes<const T extends readonly string[]>(routes: T) {
  return routes;
}
const r2 = getRoutes(['home', 'about']); // readonly ["home", "about"]
```

### satisfies 연산자

타입 호환성 검증 + 리터럴 타입 유지.

```typescript
type Color = 'red' | 'green' | 'blue';
type ColorMap = Record<Color, string | [number, number, number]>;

// satisfies: 타입 검증하면서 추론된 타입 유지
const palette = {
  red: [255, 0, 0],
  green: '#00ff00',
  blue: [0, 0, 255],
} satisfies ColorMap;

// palette.green은 string으로 추론 (toUpperCase 사용 가능)
palette.green.toUpperCase(); // OK

// 타입 어노테이션이었다면 string | [number, number, number]로 추론
// const palette: ColorMap = { ... };
// palette.green.toUpperCase(); // Error!
```

### Decorators (Stage 3)

```typescript
// ClassMethodDecoratorContext 기반 데코레이터
function logged(target: any, context: ClassMethodDecoratorContext) {
  return function(this: any, ...args: any[]) {
    console.log(`Calling ${String(context.name)} with`, args);
    return target.call(this, ...args);
  };
}

class Calculator { @logged add(a: number, b: number) { return a + b; } }
```

---

## type vs interface

| 특성 | interface | type |
|------|-----------|------|
| 객체 형태 | O | O |
| extends (상속) | O (빠름) | X (&로 교차) |
| implements | O | O |
| Declaration Merging | O | X |
| Union / Intersection | X | O |
| Mapped Types | X | O |
| Conditional Types | X | O |

```typescript
// interface: 객체 형태 정의, 확장이 필요할 때
interface User { id: string; name: string; email: string; }
interface AdminUser extends User { role: 'admin'; permissions: string[]; }

// type: Union, 조합, 유틸리티 타입
type Status = 'active' | 'inactive' | 'suspended';
type ApiResponse<T> = { data: T; error: null } | { data: null; error: string };
```

**권장**: 객체 형태는 `interface`, 나머지는 `type` 사용.

---

## 고급 타입

### Conditional Types

```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<'hello'>; // true
type B = IsString<42>;      // false

// 실용적 예시: API 응답 타입 추출
type ExtractData<T> = T extends { data: infer D } ? D : never;

type UserResponse = { data: User; status: number };
type Extracted = ExtractData<UserResponse>; // User

// Promise unwrap
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;
type Result = Awaited<Promise<Promise<string>>>; // string
```

### Mapped Types

```typescript
// 모든 프로퍼티를 선택적으로
type Optional<T> = { [K in keyof T]?: T[K] };

// 모든 프로퍼티를 읽기 전용으로
type Immutable<T> = { readonly [K in keyof T]: T[K] };

// 키 이름 변환 (Template Literal + Mapped)
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface Person { name: string; age: number; }
type PersonGetters = Getters<Person>;
// { getName: () => string; getAge: () => number; }
```

### Template Literal Types

```typescript
type EventName = 'click' | 'focus' | 'blur';
type EventHandler = `on${Capitalize<EventName>}`;
// 'onClick' | 'onFocus' | 'onBlur'

// API 경로 타입
type ApiVersion = 'v1' | 'v2';
type Resource = 'users' | 'products' | 'orders';
type ApiPath = `/api/${ApiVersion}/${Resource}`;
// '/api/v1/users' | '/api/v1/products' | ... (6개 조합)

// CSS 유닛 타입
type CSSUnit = 'px' | 'rem' | 'em' | '%';
type CSSValue = `${number}${CSSUnit}`;
const margin: CSSValue = '16px'; // OK
```

---

## Generic 패턴

### Factory 패턴

```typescript
interface Repository<T, ID = string> {
  findById(id: ID): Promise<T | null>;
  findAll(filter?: Partial<T>): Promise<T[]>;
  create(data: Omit<T, 'id' | 'createdAt'>): Promise<T>;
  update(id: ID, data: Partial<T>): Promise<T>;
  delete(id: ID): Promise<void>;
}

// 구현
class UserRepository implements Repository<User> {
  async findById(id: string): Promise<User | null> {
    return await db.user.findUnique({ where: { id } });
  }
  // ...
}
```

### Builder 패턴

```typescript
class QueryBuilder<T> {
  private filters: Record<string, unknown> = {};
  private sortField?: keyof T;

  where<K extends keyof T>(field: K, value: T[K]): this {
    this.filters[field as string] = value;
    return this;
  }

  orderBy(field: keyof T): this {
    this.sortField = field;
    return this;
  }
}

// 타입 안전한 쿼리 빌더
const query = new QueryBuilder<User>()
  .where('status', 'active')   // OK: 'status' is keyof User
  .where('age', 25)            // OK: age is number
  .orderBy('name');
```

### Generic Constraints

```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// 복합 제약: 여러 interface를 교차
function merge<T extends HasId & HasTimestamp>(entity: T, update: Partial<Omit<T, 'id'>>): T {
  return { ...entity, ...update, updatedAt: new Date() };
}
```

---

## Utility Types 심화

```typescript
type UpdateUser = Partial<User>;                // 모든 프로퍼티 선택적
type StrictConfig = Required<Config>;            // 모든 프로퍼티 필수
type UserSummary = Pick<User, 'id' | 'name'>;   // 특정 프로퍼티만 선택
type CreateUser = Omit<User, 'id' | 'createdAt'>; // 특정 프로퍼티 제외
type StatusMap = Record<Status, { label: string; color: string }>; // 키-값 매핑
type OnlyStrNum = Extract<string | number | boolean, string | number>; // string | number
type OnlyBool = Exclude<string | number | boolean, string | number>;  // boolean
type DefiniteUser = NonNullable<User | null | undefined>; // User
type FetchResult = ReturnType<typeof fetchUser>;   // Promise<User>
type FetchParams = Parameters<typeof fetchUser>;   // [id: string]
```

---

## Discriminated Unions

상태머신이나 다형성을 타입으로 안전하게 모델링.

```typescript
// 주문 상태를 Discriminated Union으로 모델링
type Order =
  | { status: 'pending'; createdAt: Date }
  | { status: 'confirmed'; confirmedAt: Date; estimatedDelivery: Date }
  | { status: 'shipped'; trackingNumber: string; shippedAt: Date }
  | { status: 'delivered'; deliveredAt: Date }
  | { status: 'cancelled'; reason: string; cancelledAt: Date };

function getOrderMessage(order: Order): string {
  switch (order.status) {
    case 'pending':
      return '주문이 접수되었습니다';
    case 'confirmed':
      return `배송 예정일: ${order.estimatedDelivery.toLocaleDateString()}`;
    case 'shipped':
      return `송장번호: ${order.trackingNumber}`;
    case 'delivered':
      return `배송 완료: ${order.deliveredAt.toLocaleDateString()}`;
    case 'cancelled':
      return `취소 사유: ${order.reason}`;
  }
  // exhaustive check: 새 status 추가 시 컴파일 에러 발생
  const _exhaustive: never = order;
  return _exhaustive;
}
```

### API 응답 패턴

```typescript
type ApiResult<T> =
  | { success: true; data: T }
  | { success: false; error: { code: string; message: string } };

// 사용 시 타입이 자동으로 좁혀짐
const result = await fetchUser('123');
if (result.success) {
  console.log(result.data.name); // User 타입 확정
} else {
  console.error(result.error.message); // Error 타입 확정
}
```

---

## Type Narrowing

```typescript
// Type Guard 함수
function isAdmin(user: User | AdminUser): user is AdminUser {
  return 'permissions' in user;
}

// in 연산자
function processResponse(res: SuccessResponse | ErrorResponse) {
  if ('data' in res) {
    return res.data; // SuccessResponse
  }
  return res.error;  // ErrorResponse
}

// instanceof
function handleError(err: unknown) {
  if (err instanceof ValidationError) {
    return { status: 400, message: err.details };
  }
  if (err instanceof NotFoundError) {
    return { status: 404, message: err.message };
  }
  return { status: 500, message: 'Internal error' };
}

// typeof
function format(value: string | number): string {
  if (typeof value === 'string') return value.trim();
  return value.toFixed(2);
}
```

---

## Branded Types / Nominal Types

런타임에는 같은 타입이지만 컴파일 타임에 구분.

```typescript
// Brand 타입 정의
type Brand<T, B extends string> = T & { readonly __brand: B };

type UserId = Brand<string, 'UserId'>;
type OrderId = Brand<string, 'OrderId'>;
type Email = Brand<string, 'Email'>;

// 생성 함수 (검증 포함)
function createUserId(id: string): UserId {
  if (!id.startsWith('usr_')) throw new Error('Invalid user ID');
  return id as UserId;
}

function createEmail(email: string): Email {
  if (!email.includes('@')) throw new Error('Invalid email');
  return email as Email;
}

// 사용: 서로 다른 ID 타입을 혼동할 수 없음
function getUser(id: UserId): Promise<User> { ... }
function getOrder(id: OrderId): Promise<Order> { ... }

const userId = createUserId('usr_123');
const orderId = 'ord_456' as OrderId;

getUser(userId);   // OK
getUser(orderId);  // Compile Error! OrderId는 UserId가 아님
```

---

## Zod + TypeScript 스키마 검증

```typescript
import { z } from 'zod';

const userSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  role: z.enum(['user', 'admin', 'moderator']),
});

type User = z.infer<typeof userSchema>; // 자동 타입 추론

// 런타임 검증
const result = userSchema.safeParse(input);
if (result.success) {
  console.log(result.data.name); // User 타입
} else {
  console.error(result.error.flatten());
}
```

---

## tsconfig.json 권장 설정

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalProperties": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "target": "ES2022",
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "paths": { "@/*": ["./src/*"] }
  }
}
```

---

## Anti-Patterns

### 1. any 남용

```typescript
// Bad: any는 타입 체크를 무력화
function process(data: any) {
  return data.foo.bar; // 런타임 에러 가능
}

// Good: unknown + 타입 가드
function process(data: unknown) {
  if (isValidData(data)) {
    return data.foo.bar; // 타입 안전
  }
  throw new Error('Invalid data');
}
```

### 2. Type Assertion 남용

```typescript
// Bad: as로 강제 캐스팅
const user = response.data as User; // 실제로 User가 아닐 수 있음

// Good: 런타임 검증
const user = userSchema.parse(response.data); // Zod 검증
```

### 3. 불필요한 제네릭

```typescript
// Bad: 의미 없는 제네릭
function getName<T extends { name: string }>(obj: T): string {
  return obj.name;
}

// Good: 단순하게
function getName(obj: { name: string }): string {
  return obj.name;
}
```

### 4. enum 대신 as const

```typescript
// Avoid: enum은 JS 런타임 코드 생성
enum Direction { Up, Down, Left, Right }

// Prefer: as const는 타입만 생성 (tree-shaking 유리)
const Direction = {
  Up: 'up',
  Down: 'down',
  Left: 'left',
  Right: 'right',
} as const;

type Direction = (typeof Direction)[keyof typeof Direction];
// 'up' | 'down' | 'left' | 'right'
```

---

## Sources

- TypeScript 5.x Handbook: typescriptlang.org/docs
- TypeScript Release Notes
- Total TypeScript — Matt Pocock
- Zod Documentation
- Effect-TS (타입 안전 함수형 프로그래밍)
