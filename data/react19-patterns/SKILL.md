---
name: react19-patterns
description: React 19 최신 패턴과 Best Practices 가이드. 컴포넌트 작성, 상태관리, 메모이제이션 최적화 시 참고. "React 19 패턴", "최신 React", "use hook", "Server Actions" 관련 질문에 사용.
---

# React 19 패턴 가이드

이 프로젝트는 **React 19**를 사용합니다. 최신 패턴을 적용해주세요.

---

## 1. forwardRef 제거

React 19부터 `forwardRef` 없이 ref를 prop으로 직접 전달합니다.

```tsx
// ❌ 이전 방식 (React 18)
import { forwardRef } from "react";

const Input = forwardRef<HTMLInputElement, InputProps>((props, ref) => {
  return <input ref={ref} {...props} />;
});

// ✅ React 19 방식
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  ref?: React.Ref<HTMLInputElement>;
}

function Input({ ref, ...props }: InputProps) {
  return <input ref={ref} {...props} />;
}
```

### useImperativeHandle도 간단해짐

```tsx
function TextInput({ ref }: { ref?: React.Ref<TextInputHandle> }) {
  const inputRef = useRef<HTMLInputElement>(null);

  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current?.focus(),
    clear: () => { if (inputRef.current) inputRef.current.value = ""; },
  }));

  return <input ref={inputRef} />;
}
```

---

## 2. 메모이제이션은 필요한 경우만

React Compiler가 자동으로 최적화합니다. **불필요한 메모이제이션은 오히려 성능 저하**를 유발할 수 있습니다.

### 왜 불필요한 메모이제이션이 나쁜가?

1. **오버헤드**: 의존성 배열 비교 + 메모리에 이전 값 저장
2. **버그 위험**: 의존성 배열 누락 시 stale closure 문제
3. **코드 복잡도**: 가독성 저하

```tsx
// ❌ 불필요 - 단순 값은 그냥 새로 만드는 게 더 빠름
const memoizedData = useMemo(() => data, [data]);

// ❌ 불필요 - 간단한 콜백
const handleClick = useCallback(() => {
  setCount(c => c + 1);
}, []);

// ❌ 불필요 - 가벼운 컴포넌트
const MemoizedItem = memo(({ name }) => <span>{name}</span>);
```

### 언제 사용해야 하나?

| 상황 | 권장 |
|------|------|
| 단순 값/함수 | 그냥 쓰기 |
| 복잡한 계산 (O(n²) 이상) | `useMemo` ✅ |
| 외부 라이브러리에 전달하는 객체 | `useMemo` ✅ |
| 수천 개 항목 렌더링하는 컴포넌트 | `memo` ✅ |
| 확실하지 않으면 | **일단 안 쓰고, 성능 문제 생기면 추가** |

```tsx
// ✅ 필요 - 복잡한 계산 (O(n log n) 이상)
const sortedAndFilteredItems = useMemo(() => {
  return items
    .filter(item => item.active)
    .sort((a, b) => complexSort(a, b))
    .map(item => transformItem(item));
}, [items]);

// ✅ 필요 - 참조 동등성이 중요 (Cesium, Three.js 등 외부 라이브러리)
// 객체가 바뀌면 전체 재초기화되는 경우
const mapOptions = useMemo(() => ({
  center: [lat, lng],
  zoom: 10,
}), [lat, lng]);

// ✅ 필요 - 정말 무거운 컴포넌트 (수천 행 테이블, 복잡한 차트)
const HeavyChart = memo(function HeavyChart({ data }) {
  // 수천 개의 데이터 포인트 렌더링
  return <canvas>{/* ... */}</canvas>;
});
```

### 실수하기 쉬운 패턴

```tsx
// ❌ 버그: count가 항상 0 (stale closure)
const handleClick = useCallback(() => {
  setCount(count + 1);  // count가 의존성 배열에 없음!
}, []);

// ✅ 그냥 이렇게 쓰면 버그 없음
const handleClick = () => {
  setCount(c => c + 1);
};
```

---

## 3. 새로운 Hooks

### use() - Promise/Context 읽기

```tsx
import { use, Suspense } from "react";

// Context를 조건부로 읽기 (useContext는 불가능)
function ConditionalTheme({ showTheme }: { showTheme: boolean }) {
  if (showTheme) {
    const theme = use(ThemeContext); // ✅ 조건부 사용 가능
    return <div className={theme}>Themed content</div>;
  }
  return <div>Default content</div>;
}

// Promise 읽기 (Suspense와 함께)
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise); // Suspense가 로딩 처리
  return <div>{user.name}</div>;
}

// 사용
<Suspense fallback={<Skeleton />}>
  <UserProfile userPromise={fetchUser(id)} />
</Suspense>
```

### useOptimistic() - 낙관적 업데이트

```tsx
import { useOptimistic, startTransition } from "react";

function TodoList({ initialTodos }: { initialTodos: Todo[] }) {
  const [todos, setTodos] = useState(initialTodos);

  const [optimisticTodos, addOptimistic] = useOptimistic(
    todos,
    (state, newTodo: string) => [
      ...state,
      { id: "temp-" + Date.now(), title: newTodo, pending: true },
    ]
  );

  async function handleAdd(title: string) {
    // 1. 즉시 UI 업데이트
    addOptimistic(title);

    // 2. 서버 요청 (실패 시 자동 롤백)
    startTransition(async () => {
      const newTodo = await createTodo(title);
      setTodos((prev) => [...prev, newTodo]);
    });
  }

  return (
    <ul>
      {optimisticTodos.map((todo) => (
        <li key={todo.id} style={{ opacity: todo.pending ? 0.5 : 1 }}>
          {todo.title}
          {todo.pending && " (저장 중...)"}
        </li>
      ))}
    </ul>
  );
}
```

### useActionState() - 폼 상태 관리

```tsx
import { useActionState } from "react";

async function updateProfile(prevState: State, formData: FormData) {
  const name = formData.get("name") as string;

  if (!name.trim()) {
    return { error: "이름을 입력해주세요", success: false };
  }

  try {
    await api.updateProfile({ name });
    return { error: null, success: true };
  } catch {
    return { error: "업데이트 실패", success: false };
  }
}

function ProfileForm() {
  const [state, formAction, isPending] = useActionState(updateProfile, {
    error: null,
    success: false,
  });

  return (
    <form action={formAction}>
      <input name="name" disabled={isPending} />
      <button type="submit" disabled={isPending}>
        {isPending ? "저장 중..." : "저장"}
      </button>
      {state.error && <p className="error">{state.error}</p>}
      {state.success && <p className="success">저장되었습니다!</p>}
    </form>
  );
}
```

### useFormStatus() - 폼 제출 상태

```tsx
import { useFormStatus } from "react-dom";

// 재사용 가능한 Submit 버튼
function SubmitButton({ children }: { children: React.ReactNode }) {
  const { pending } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? "처리 중..." : children}
    </button>
  );
}

// 사용 - 부모 폼의 상태 자동 감지
function Form() {
  return (
    <form action={submitAction}>
      <input name="email" type="email" required />
      <SubmitButton>제출</SubmitButton>
    </form>
  );
}
```

---

## 4. Suspense 적극 활용

```tsx
import { Suspense } from "react";

// 페이지 레벨 Suspense
function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* 각 섹션 독립적 로딩 */}
      <Suspense fallback={<ChartSkeleton />}>
        <RevenueChart />
      </Suspense>

      <Suspense fallback={<TableSkeleton />}>
        <RecentOrders />
      </Suspense>

      <Suspense fallback={<ListSkeleton />}>
        <TopProducts />
      </Suspense>
    </div>
  );
}

// 중첩 Suspense로 세밀한 로딩 제어
function UserProfile({ userId }: { userId: string }) {
  return (
    <Suspense fallback={<ProfileSkeleton />}>
      <UserInfo userId={userId} />

      <Suspense fallback={<p>게시물 로딩 중...</p>}>
        <UserPosts userId={userId} />
      </Suspense>
    </Suspense>
  );
}
```

---

## 5. Document Metadata

컴포넌트에서 직접 메타데이터 설정 가능:

```tsx
function BlogPost({ post }: { post: Post }) {
  return (
    <article>
      {/* head로 자동 이동 */}
      <title>{post.title} | My Blog</title>
      <meta name="description" content={post.excerpt} />
      <meta property="og:title" content={post.title} />
      <meta property="og:image" content={post.thumbnail} />

      {/* 실제 콘텐츠 */}
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  );
}
```

---

## 6. 권장 패턴 요약

| 상황 | 권장 패턴 |
|------|----------|
| ref 전달 | prop으로 직접 전달 (forwardRef 제거) |
| 간단한 상태 | useState (그대로) |
| 폼 상태 | useActionState + useFormStatus |
| 낙관적 업데이트 | useOptimistic |
| 비동기 데이터 | use() + Suspense |
| 메모이제이션 | 필요한 경우만 (복잡한 계산, 무거운 컴포넌트) |
| Context 읽기 | use() (조건부 가능) 또는 useContext |
| 로딩 상태 | Suspense (isPending 보다 선호) |

---

## 7. 마이그레이션 체크리스트

- [ ] `forwardRef` → ref를 prop으로 변경
- [ ] 불필요한 `useMemo`/`useCallback`/`memo` 제거
- [ ] 폼 처리 → `useActionState` 검토
- [ ] 낙관적 UI → `useOptimistic` 검토
- [ ] 조건부 Context → `use()` 검토
- [ ] 로딩 UI → `Suspense` 검토
