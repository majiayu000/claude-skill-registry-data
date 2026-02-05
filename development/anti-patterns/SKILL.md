---
name: anti-patterns
description: >
  Gentle reminder skill for common mistakes to avoid. Non-blocking suggestions.

  AUTO-ACTIVATE when user mentions (FR/EN):
  - erreur, error, bug, problème, problem
  - anti-pattern, mauvaise pratique, bad practice, avoid, éviter
  - pourquoi erreur, why error, comment éviter, how to avoid
  - any, undefined, null, timezone, siteId manquant

  This skill shows as a GENTLE reminder after code edits (non-blocking).
---

# Anti-Patterns - Don't Do This

**Purpose**: Gentle reminders of common mistakes
**Source**: DONT_DO.md (397 lines)
**Enforcement**: Suggest only (non-blocking)

---

## 🚫 TypeScript

```typescript
// ❌ any types
const data: any = response

// ✅ Explicit types
const data: User = response

// ❌ Non-null assertion without check
const user = getUser()!

// ✅ Proper check
const user = getUser();
if (!user) throw new Error('User not found');
```

---

## 🚫 React

```typescript
// ❌ useState for server data
const [users, setUsers] = useState([])

// ✅ React Query
const { data: users } = useQuery({ queryKey: ['users'], ... })

// ❌ useEffect without dependencies
useEffect(() => doSomething(prop))  // Missing []

// ✅ With dependencies
useEffect(() => doSomething(prop), [prop])

// ❌ Inline objects in props (causes re-renders)
<Component style={{ margin: 10 }} />

// ✅ Memoized or extracted
const style = useMemo(() => ({ margin: 10 }), []);
<Component style={style} />
```

---

## 🚫 Database (Prisma)

```typescript
// ❌ N+1 Queries
const users = await prisma.user.findMany()
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { userId: user.id } })
}

// ✅ Use include
const users = await prisma.user.findMany({
  include: { posts: true }
});

// ❌ Queries without pagination
const allUsers = await prisma.user.findMany()  // Can return millions

// ✅ Always paginate
const users = await prisma.user.findMany({
  take: 50,
  skip: page * 50
});
```

---

## 🚫 API Design

```typescript
// ❌ No validation
export async function POST(request: NextRequest) {
  const data = await request.json();  // No validation!
  return NextResponse.json(await createPlanning(data));
}

// ✅ Zod validation
const schema = z.object({ name: z.string().min(1) });
export async function POST(request: NextRequest) {
  const body = await request.json();
  const validation = schema.safeParse(body);

  if (!validation.success) {
    return NextResponse.json(
      { error: 'Validation failed', details: validation.error },
      { status: 400 }
    );
  }

  return NextResponse.json(await createPlanning(validation.data));
}

// ❌ Unhandled errors
export async function GET() {
  const data = await service.getData();  // Can throw
  return NextResponse.json(data);
}

// ✅ Try-catch
export async function GET() {
  try {
    const data = await service.getData();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

---

## 🚫 Dates & Timezone

```typescript
// ❌ Send yyyy-MM-dd without timezone
const payload = {
  startDate: format(date, 'yyyy-MM-dd'),  // "2025-10-28"
  // Parsed as midnight UTC → timezone bug!
};

// ✅ Always send ISO with explicit timezone
const payload = {
  startDate: startOfDay(date).toISOString(),  // 2025-10-27T23:00:00.000Z
  endDate: endOfDay(date).toISOString()
};
```

---

## 🚫 Critical Fields Missing

```typescript
// ❌ Forget siteId when creating assignments
const assignment = await prisma.assignment.create({
  data: {
    date: request.date,
    userId: request.userId,
    operatingRoomId: request.operatingRoomId,
    // ❌ siteId missing → null in DB!
  }
});

// ✅ Always include siteId
const assignment = await prisma.assignment.create({
  data: {
    date: request.date,
    userId: request.userId,
    operatingRoomId: request.operatingRoomId,
    siteId: request.siteId,  // ✅ Essential for filtering/deletion
  }
});
```

**Impact**: 55% of assignments had `siteId: null`, making bulk delete impossible.

---

## 🚫 UX & Accessibility

```tsx
// ❌ Insufficient contrast (gray on gray)
<div className="bg-gray-50 p-3">
  <Switch />  {/* OFF state invisible on light gray background */}
</div>

// ✅ Sufficient contrast with border or white bg
<div className="bg-white border-2 border-gray-200 hover:border-blue-300 p-4 rounded-lg">
  <Label htmlFor="active" className="text-sm font-medium cursor-pointer">Active</Label>
  <Switch id="active" />
</div>

// ❌ Touch zones too small (<44px - not WCAG AAA)
<button className="p-1 text-xs">Action</button>

// ✅ Minimum 44x44px
<button className="min-h-[44px] min-w-[44px] p-3">Action</button>

// ❌ Labels not connected (accessibility broken)
<Label>Active</Label>
<Switch />

// ✅ Connected for screen readers
<Label htmlFor="active">Active</Label>
<Switch id="active" />
```

---

## 🚫 Authentication

```typescript
// ❌ Read token from document.cookie (HttpOnly cookies inaccessible)
function getAuthToken() {
  const cookies = document.cookie.split(';');
  const token = cookies.find(c => c.includes('token='));  // Doesn't work if HttpOnly!
  return token;
}

// ✅ Use auth context
const { getAuthHeaders } = useAuth();
const headers = {
  'Content-Type': 'application/json',
  ...getAuthHeaders()  // Includes Authorization: Bearer <token>
};

// ❌ Forget credentials: 'include' in fetch
fetch('/api/endpoint', { method: 'POST' });  // Cookies not sent!

// ✅ Always include credentials for authenticated requests
fetch('/api/endpoint', {
  method: 'POST',
  credentials: 'include',
  headers: getAuthHeaders()
});
```

---

## 🎯 ABSOLUTE RULES

1. **❌ NEVER**: `any` types in TypeScript
2. **❌ NEVER**: `console.log` in production
3. **❌ NEVER**: Queries without pagination
4. **❌ NEVER**: Components >200 lines
5. **❌ NEVER**: Business logic in UI
6. **❌ NEVER**: Tests without cleanup
7. **❌ NEVER**: Import full libraries (use tree shaking)
8. **❌ NEVER**: APIs without Zod validation
9. **❌ NEVER**: `useEffect` without dependencies
10. **❌ NEVER**: Missing braces (syntax errors)
11. **❌ NEVER**: Gray on gray (contrast <3:1 WCAG)
12. **❌ NEVER**: Buttons/Switch <44px (WCAG AAA)

---

**Source**: DONT_DO.md
**Maintained by**: Mathildanesth Team
**Last Update**: 27 October 2025
