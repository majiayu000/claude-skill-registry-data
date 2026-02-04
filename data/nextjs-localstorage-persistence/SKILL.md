---
name: nextjs-localstorage-persistence
description: Implement localStorage persistence in Next.js 14 App Router with SSR-safe patterns. Use when storing data in localStorage, handling hydration errors, implementing state persistence, or creating type-safe storage utilities.
---

# Next.js LocalStorage Persistence

Next.js 14 App Router에서 SSR-안전한 localStorage 지속성 구현 스킬입니다.

## Quick Reference

### SSR-Safe 패턴
```tsx
// ❌ 잘못된 방법 - 하이드레이션 에러 발생
const data = localStorage.getItem('key');

// ✅ 올바른 방법 - useEffect 내에서 사용
useEffect(() => {
  const data = localStorage.getItem('key');
}, []);
```

### 하이드레이션 에러 방지
```tsx
const [hydrated, setHydrated] = useState(false);

useEffect(() => {
  setHydrated(true);
}, []);

if (!hydrated) return <Loading />;
```

## Contents

- [reference.md](reference.md) - SSR/CSR 라이프사이클 및 하이드레이션 가이드
- [guide.md](guide.md) - 타입-안전 스토리지 유틸리티 및 Zustand 통합
- [scripts/validate_storage_schema.py](scripts/validate_storage_schema.py) - 스토리지 스키마 검증

## When to Use

- Next.js에서 localStorage 사용 시 하이드레이션 에러 발생
- 세션 간 상태 지속성 구현 시
- 타입-안전한 스토리지 추상화 필요 시
- Zustand persist 미들웨어 설정 시
