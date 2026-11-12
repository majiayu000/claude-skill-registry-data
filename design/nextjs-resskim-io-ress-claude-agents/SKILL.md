---
name: nextjs
description: "Next.js App Router — React Server Components, Data Fetching, ISR, Route Handlers, Middleware, Parallel·Intercepting Routes, Server Actions, 캐싱. Use when Next.js 앱의 라우팅·데이터 패칭·캐싱을 설계하거나 구현할 때."
---

# Next.js 가이드

Next.js 15 App Router, React Server Components, ISR, Middleware, 라우팅 전략 종합 가이드.

## Quick Reference

```
Next.js 라우팅 선택
    │
    ├─ 신규 프로젝트 ─────────> App Router (app/)
    ├─ 레거시 유지보수 ───────> Pages Router (pages/)
    │
    렌더링 전략
    │
    ├─ 정적 콘텐츠 ──────────> SSG (generateStaticParams)
    ├─ 주기적 갱신 ──────────> ISR (revalidate)
    ├─ 요청마다 다른 데이터 ─> Dynamic Rendering
    ├─ 사용자 인터랙션 ──────> Client Component + API
    │
    데이터 변경
    │
    ├─ 폼 제출 ──────────────> Server Actions
    ├─ REST API 제공 ────────> Route Handlers
    └─ 실시간 데이터 ────────> Server-Sent Events / WebSocket
```

---

## App Router 디렉토리 구조

### 파일 규칙

| 파일 | 용도 | 렌더링 |
|------|------|--------|
| `layout.tsx` | 공유 레이아웃 (상태 유지) | Server |
| `page.tsx` | 라우트 고유 UI | Server |
| `loading.tsx` | Suspense fallback (자동 적용) | Server |
| `error.tsx` | Error Boundary (자동 적용) | Client |
| `not-found.tsx` | 404 UI | Server |
| `template.tsx` | 재마운트 레이아웃 | Server |
| `default.tsx` | Parallel Route 기본값 | Server |
| `route.ts` | API 엔드포인트 | Server |

### 권장 프로젝트 구조

```
app/
├── (auth)/                    # Route Group (URL에 미포함)
│   ├── login/page.tsx
│   └── register/page.tsx
├── (dashboard)/
│   ├── layout.tsx             # 대시보드 공통 레이아웃
│   ├── page.tsx               # /dashboard
│   ├── settings/page.tsx      # /dashboard/settings
│   └── orders/
│       ├── page.tsx           # /dashboard/orders
│       └── [id]/page.tsx      # /dashboard/orders/:id
├── api/
│   └── webhooks/route.ts      # API Route Handler
├── layout.tsx                 # Root Layout
├── page.tsx                   # Home page
├── loading.tsx                # Global loading
├── error.tsx                  # Global error
├── not-found.tsx              # 404 page
└── globals.css
```

---

## Data Fetching 전략

### Server Component에서 직접 fetch

```tsx
// app/products/page.tsx (Server Component)
async function ProductsPage() {
  // 서버에서 직접 데이터 fetch — 클라이언트 JS 불필요
  const products = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 }, // 1시간 ISR
  }).then((res) => res.json());

  return (
    <ul>
      {products.map((p: Product) => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  );
}

export default ProductsPage;
```

### generateStaticParams (SSG)

```tsx
// app/products/[id]/page.tsx
export async function generateStaticParams() {
  const products = await getProducts();
  return products.map((p) => ({ id: p.id.toString() }));
}

export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const product = await getProduct(id);

  if (!product) notFound();

  return <ProductDetail product={product} />;
}
```

### Dynamic Rendering (요청 시 렌더링)

```tsx
import { cookies, headers } from 'next/headers';

// cookies() 또는 headers() 사용 시 자동으로 Dynamic Rendering
async function UserDashboard() {
  const cookieStore = await cookies();
  const token = cookieStore.get('session')?.value;
  const user = await getUserByToken(token);

  return <Dashboard user={user} />;
}
```

---

## ISR (Incremental Static Regeneration)

### Time-based Revalidation

```tsx
// 60초마다 백그라운드 재생성
async function BlogPage() {
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 60 },
  }).then((res) => res.json());

  return <PostList posts={posts} />;
}
```

### On-demand Revalidation

```tsx
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const { secret, path, tag } = await request.json();

  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ error: 'Invalid secret' }, { status: 401 });
  }

  if (path) {
    revalidatePath(path);
  }
  if (tag) {
    revalidateTag(tag);
  }

  return NextResponse.json({ revalidated: true });
}

// 데이터 fetch 시 tag 지정
const products = await fetch('https://api.example.com/products', {
  next: { tags: ['products'] },
}).then((res) => res.json());
```

---

## Route Handlers

```tsx
// app/api/products/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const category = searchParams.get('category');

  const products = await getProducts({ category });
  return NextResponse.json(products);
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  // Zod 검증
  const result = productSchema.safeParse(body);
  if (!result.success) {
    return NextResponse.json(
      { error: result.error.flatten() },
      { status: 400 }
    );
  }

  const product = await createProduct(result.data);
  return NextResponse.json(product, { status: 201 });
}
```

---

## Middleware

```tsx
// middleware.ts (프로젝트 루트)
import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // 인증 체크
  const token = request.cookies.get('session')?.value;
  if (pathname.startsWith('/dashboard') && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // i18n 리다이렉트
  const locale = request.headers.get('accept-language')?.split(',')[0] ?? 'ko';
  if (pathname === '/') {
    return NextResponse.redirect(new URL(`/${locale}`, request.url));
  }

  // Rate Limiting 헤더 추가
  const response = NextResponse.next();
  response.headers.set('X-Request-Id', crypto.randomUUID());
  return response;
}

export const config = {
  matcher: [
    // 정적 파일 및 API Route 제외
    '/((?!_next/static|_next/image|favicon.ico|api/).*)',
  ],
};
```

---

## Parallel Routes & Intercepting Routes

### Parallel Routes

`@슬롯명/` 디렉토리로 같은 레이아웃 내에서 독립적인 영역 렌더링.

```tsx
// app/layout.tsx — @dashboard, @analytics 슬롯
export default function Layout({ children, dashboard, analytics }) {
  return (
    <div className="grid grid-cols-2">
      <div>{dashboard}</div>
      <div>{analytics}</div>
      {children}
    </div>
  );
}
```

### Intercepting Routes (모달 패턴)

`(..)` 접두사로 다른 세그먼트를 인터셉트하여 모달로 표시. 직접 접근 시 전체 페이지.

```
app/feed/(..)photo/[id]/page.tsx  → 피드에서 클릭 시 모달
app/photo/[id]/page.tsx           → 직접 접근 시 전체 페이지
```

---

## Server Actions

```tsx
// app/actions/product.ts
'use server';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export async function createProduct(prevState: any, formData: FormData) {
  const raw = {
    name: formData.get('name'),
    price: Number(formData.get('price')),
  };

  const result = createProductSchema.safeParse(raw);
  if (!result.success) {
    return { error: result.error.flatten().fieldErrors };
  }

  await db.product.create({ data: result.data });
  revalidatePath('/products');
  redirect('/products');
}
```

---

## Caching 전략

### 4가지 캐시 레이어

| 레이어 | 위치 | 용도 | 무효화 |
|--------|------|------|--------|
| Request Memoization | 서버 (요청 단위) | 동일 요청 내 중복 fetch 제거 | 요청 완료 시 자동 |
| Data Cache | 서버 (영구) | fetch 결과 캐싱 | revalidate, revalidateTag |
| Full Route Cache | 서버 (영구) | 정적 페이지 HTML/RSC 캐싱 | revalidatePath |
| Router Cache | 클라이언트 (세션) | RSC Payload 캐싱 | router.refresh() |

### 캐시 무효화 예시

```tsx
// Tag 기반 무효화 (권장)
const data = await fetch(url, { next: { tags: ['products'] } });
// 무효화: revalidateTag('products')

// Path 기반 무효화
// revalidatePath('/products')        — 특정 경로
// revalidatePath('/products', 'layout') — 레이아웃 포함

// 캐시 비활성화 (Dynamic Rendering 강제)
const data = await fetch(url, { cache: 'no-store' });
```

---

## Image & Font 최적화

### next/image

```tsx
import Image from 'next/image';

function ProductImage({ product }: { product: Product }) {
  return (
    <Image
      src={product.imageUrl}
      alt={product.name}
      width={400}
      height={300}
      placeholder="blur"
      blurDataURL={product.blurHash}
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
      priority={false} // LCP 이미지는 true
    />
  );
}
```

### next/font

```tsx
// app/layout.tsx
import { Noto_Sans_KR } from 'next/font/google';

const notoSansKR = Noto_Sans_KR({
  subsets: ['latin'],
  weight: ['400', '700'],
  display: 'swap',
  variable: '--font-noto-sans',
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko" className={notoSansKR.variable}>
      <body className="font-sans">{children}</body>
    </html>
  );
}
```

---

## next.config.ts 주요 설정

```ts
// next.config.ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // 실험적 기능
  experimental: {
    ppr: true,           // Partial Prerendering
    typedRoutes: true,   // 타입 안전 라우팅
  },

  // 이미지 도메인 허용
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'cdn.example.com' },
    ],
  },

  // 리다이렉트
  async redirects() {
    return [
      { source: '/old-path', destination: '/new-path', permanent: true },
    ];
  },

  // 헤더
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'X-Content-Type-Options', value: 'nosniff' },
        ],
      },
    ];
  },
};

export default nextConfig;
```

---

## Anti-Patterns

### 1. 불필요한 Client Component

```tsx
// Bad: 정적 콘텐츠에 'use client'
'use client';
export function Footer() {
  return <footer>Copyright 2026</footer>;
}

// Good: Server Component로 유지
export function Footer() {
  return <footer>Copyright 2026</footer>;
}
```

### 2. Layout에서 무거운 Data Fetch

```tsx
// Bad: 모든 하위 페이지에서 불필요한 데이터 로딩
// app/layout.tsx
export default async function Layout({ children }) {
  const allProducts = await getAllProducts(); // 모든 페이지에서 실행
  return <ProductContext value={allProducts}>{children}</ProductContext>;
}

// Good: 필요한 page에서만 fetch
// app/products/page.tsx
export default async function ProductsPage() {
  const products = await getProducts();
  return <ProductList products={products} />;
}
```

### 3. 캐시 전략 미설정

```tsx
// Bad: 캐시 설정 없이 매 요청마다 fetch
const data = await fetch(url); // 기본값이 Next.js 버전마다 다름

// Good: 명시적 캐시 전략
const data = await fetch(url, {
  next: { revalidate: 3600, tags: ['products'] },
});
```

### 4. Waterfall Data Fetching

```tsx
// Bad: 순차적 fetch (waterfall)
async function Page() {
  const user = await getUser();          // 1초
  const orders = await getOrders(user.id); // 1초 → 총 2초
}

// Good: 병렬 fetch
async function Page() {
  const userPromise = getUser();
  const ordersPromise = getOrders(userId);
  const [user, orders] = await Promise.all([userPromise, ordersPromise]); // 총 1초
}
```

---

## Sources

- Next.js 15 공식 문서: nextjs.org/docs
- Vercel Blog — App Router Best Practices
- Next.js GitHub Discussions
- Lee Robinson — Caching in Next.js
