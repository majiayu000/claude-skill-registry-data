---
name: supabase-fallback
description: |
  Supabase DB 직접 접근. Use when (1) "DB 조회/수정", "테이블 데이터",
  (2) 온프레미스 Supabase PostgREST API, (3) Spring 미가동 시 fallback.
tools: [Read, Write, Bash]
---

> **시스템 메시지**: `[SEMO] Skill: supabase-fallback 호출 - Supabase 직접 쿼리`

# Supabase Fallback Skill

## Purpose

1. Spring Boot 백엔드가 미가동 상태일 때 Supabase를 직접 쿼리
2. **온프레미스 Supabase 환경에서 PostgREST API로 DB 접근** (SSH 불가 환경)

## 온프레미스 Supabase PostgREST API

### 환경 구분

| 패턴 | 유형 | 특징 |
|------|------|------|
| `*.supabase.co` | 클라우드 | Supabase 공식 호스팅 |
| 기타 URL | **온프레미스** | Self-hosted, SSH 접근 불가능할 수 있음 |

### 환경변수 구조

```bash
# .env 파일
NEXT_PUBLIC_SUPABASE_URL=https://land-supabase-dev.semi-colon.space
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...        # 읽기 전용 (RLS 적용)
NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY=eyJ... # 읽기/쓰기 가능 (RLS 무시)
```

### 권한 매트릭스

| Key 유형 | SELECT | INSERT | UPDATE | DELETE |
|----------|--------|--------|--------|--------|
| Anon Key | O | X (RLS) | X (RLS) | X (RLS) |
| **Service Role Key** | **O** | **O** | **O** | **O** |

### PostgREST API 명령어

**1. SELECT (조회)**
```bash
curl -s "${SUPABASE_URL}/rest/v1/{table}?select=*" \
  -H "apikey: ${SERVICE_ROLE_KEY}" \
  -H "Authorization: Bearer ${SERVICE_ROLE_KEY}"
```

**2. INSERT (삽입)**
```bash
curl -s -X POST "${SUPABASE_URL}/rest/v1/{table}" \
  -H "apikey: ${SERVICE_ROLE_KEY}" \
  -H "Authorization: Bearer ${SERVICE_ROLE_KEY}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"key": "...", "value": ...}'
```

**3. UPDATE (수정)**
```bash
curl -s -X PATCH "${SUPABASE_URL}/rest/v1/{table}?key=eq.{value}" \
  -H "apikey: ${SERVICE_ROLE_KEY}" \
  -H "Authorization: Bearer ${SERVICE_ROLE_KEY}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"value": ...}'
```

**4. DELETE (삭제)**
```bash
curl -s -X DELETE "${SUPABASE_URL}/rest/v1/{table}?key=eq.{value}" \
  -H "apikey: ${SERVICE_ROLE_KEY}" \
  -H "Authorization: Bearer ${SERVICE_ROLE_KEY}"
```

**5. UPSERT (있으면 수정, 없으면 삽입)**
```bash
curl -s -X POST "${SUPABASE_URL}/rest/v1/{table}" \
  -H "apikey: ${SERVICE_ROLE_KEY}" \
  -H "Authorization: Bearer ${SERVICE_ROLE_KEY}" \
  -H "Content-Type: application/json" \
  -H "Prefer: resolution=merge-duplicates,return=representation" \
  -d '{"key": "...", "value": ...}'
```

### 실행 전 체크리스트

1. `.env` 파일에서 `SUPABASE_URL`, `SERVICE_ROLE_KEY` 확인
2. URL 패턴으로 온프레미스/클라우드 구분
3. 쓰기 작업은 반드시 `SERVICE_ROLE_KEY` 사용

---

## TypeScript 클라이언트 사용 (로컬 개발)

### 사용 시나리오

1. **로컬 개발 (Spring 미실행)**: Supabase JS 클라이언트로 직접 쿼리
2. **빠른 프로토타이핑**: API 구현 전 검증
3. **통합 테스트**: E2E 테스트에서 실제 데이터 사용

### 예시 코드

```typescript
const { data } = await supabase
  .from('posts')
  .select('*')
  .eq('metadata->>type', 'office');
```

### 환경별 전환

```typescript
// lib/api-factory.ts
export function createOfficeService() {
  const useSpring = process.env.NEXT_PUBLIC_USE_SPRING === 'true';
  return useSpring ? new SpringOfficeService() : new SupabaseOfficeService();
}
```

## References

- [Query Patterns](references/query-patterns.md) - 조회 패턴
- [Mutation Patterns](references/mutation-patterns.md) - 생성/수정/삭제 패턴
- [Client Setup](references/client-setup.md) - 클라이언트 설정 및 API Route
