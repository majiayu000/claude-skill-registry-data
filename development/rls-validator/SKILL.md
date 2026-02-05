---
name: rls-validator
description: "Supabase RLS 정책 자동 검증 - 테넌트 격리, 권한 흐름, 정책 활성화 상태 확인"
allowed-tools: Read, Grep, Glob, Bash
---

# RLS Validator Skill

> Supabase Row Level Security 정책 자동 검증

## 트리거

- `/audit --rls` 실행 시
- `RLS`, `Row Level Security`, `정책 검증` 키워드
- 마이그레이션 파일 변경 시

---

## 검증 항목 (80점)

### 1. RLS 활성화 상태 (20점)

```sql
-- 모든 public 테이블에 RLS 활성화 확인
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public';

-- 검증 대상 테이블
- [ ] bids (공고)
- [ ] profiles (사용자 프로필)
- [ ] tenant_bid_state (테넌트별 공고 상태)
- [ ] products (제품 카탈로그)
- [ ] organizations (기관)
- [ ] audit_log (감사 로그)
```

### 2. 테넌트 격리 정책 (25점)

```sql
-- 필수 정책 패턴
CREATE POLICY "tenant_isolation" ON {table}
  FOR ALL
  USING (
    tenant_id = (auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid
  );

-- 검증 항목
- [ ] SELECT 격리
- [ ] INSERT 격리 (본인 tenant_id만 삽입)
- [ ] UPDATE 격리
- [ ] DELETE 격리
```

### 3. 역할 기반 접근 제어 (20점)

```sql
-- Admin 전용 작업
CREATE POLICY "admin_only" ON {table}
  FOR DELETE
  USING (
    (auth.jwt() -> 'app_metadata' ->> 'user_role') = 'admin'
  );

-- 검증 항목
- [ ] Admin 삭제 권한
- [ ] Member 읽기/쓰기 제한
- [ ] 민감 컬럼 접근 제어
```

### 4. Service Role 사용 검증 (15점)

```sql
-- Service Role 우회 최소화
-- auth.role() = 'service_role' 사용 시 로깅 필수

-- 검증 항목
- [ ] Service Role 사용 위치 파악
- [ ] 각 사용처 정당성 검토
- [ ] 감사 로그 기록 확인
```

---

## 검증 명령어

### 마이그레이션 파일 분석

```bash
# RLS 활성화 확인
grep -r "ALTER TABLE.*ENABLE ROW LEVEL SECURITY" supabase/migrations/

# 정책 정의 확인
grep -r "CREATE POLICY" supabase/migrations/

# tenant_id 조건 확인
grep -r "tenant_id.*auth.jwt" supabase/migrations/
```

### 테이블별 정책 확인

```bash
# profiles 테이블 정책
grep -A 10 "CREATE POLICY.*profiles" supabase/migrations/

# tenant_bid_state 테이블 정책
grep -A 10 "CREATE POLICY.*tenant_bid_state" supabase/migrations/
```

---

## 위험 패턴 탐지

### 위험 패턴 1: RLS 비활성화

```sql
-- BAD: RLS 없음
CREATE TABLE products (...);

-- GOOD: RLS 활성화
CREATE TABLE products (...);
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
```

### 위험 패턴 2: 너무 허용적인 정책

```sql
-- BAD: 모든 접근 허용
CREATE POLICY "allow_all" ON products
  FOR ALL USING (true);

-- GOOD: 테넌트 격리
CREATE POLICY "tenant_only" ON products
  FOR ALL USING (tenant_id = get_current_tenant_id());
```

### 위험 패턴 3: Service Role 남용

```sql
-- BAD: Service Role 무조건 허용
USING (auth.role() = 'service_role' OR ...)

-- GOOD: 특정 작업에만 제한
USING (
  CASE
    WHEN auth.role() = 'service_role'
    THEN current_setting('app.admin_action', true)::boolean
    ELSE tenant_id = get_current_tenant_id()
  END
)
```

---

## 검증 결과 형식

```
╔══════════════════════════════════════════════════════════════╗
║               RLS 정책 검증 보고서                             ║
╠══════════════════════════════════════════════════════════════╣
║  검증 시간: 2025-01-15 14:30:00                                ║
║  마이그레이션 파일: 12개                                        ║
║  검증 대상 테이블: 8개                                          ║
╚══════════════════════════════════════════════════════════════╝

┌─ 테이블별 RLS 상태 ──────────────────────────────────────────┐
│                                                               │
│  테이블             │ RLS │ 정책 수 │ tenant_id │ 상태       │
│  ──────────────────────────────────────────────────────────  │
│  bids              │ ✓   │ 2       │ N/A*      │ ✓ PASS     │
│  profiles          │ ✓   │ 3       │ ✓         │ ✓ PASS     │
│  tenant_bid_state  │ ✓   │ 4       │ ✓         │ ✓ PASS     │
│  products          │ ✓   │ 3       │ ✓         │ ✓ PASS     │
│  organizations     │ ✓   │ 2       │ N/A*      │ ✓ PASS     │
│  audit_log         │ ✓   │ 1       │ ✓         │ ⚠ CHECK    │
│                                                               │
│  * bids, organizations는 글로벌 테이블 (tenant 무관)           │
│                                                               │
└───────────────────────────────────────────────────────────────┘

┌─ 정책 세부 분석 ─────────────────────────────────────────────┐
│                                                               │
│  ✓ 테넌트 격리 정책: 5/5 테이블 적용                           │
│  ✓ Admin 전용 정책: 3개 정의                                   │
│  ✓ Service Role 사용: 2개소 (정당)                             │
│  ⚠ audit_log INSERT 정책 누락 → 추가 권장                      │
│                                                               │
└───────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════
                    총점: 75/80점 (A)
═══════════════════════════════════════════════════════════════

권장 조치:
  [MEDIUM] audit_log INSERT 정책 추가
    → CREATE POLICY "insert_own_tenant" ON audit_log
        FOR INSERT WITH CHECK (tenant_id = get_current_tenant_id());
```

---

## 자동화 스크립트

### RLS 상태 체크 스크립트

```bash
#!/bin/bash
# .claude/scripts/rls-check.sh

echo "=== RLS 정책 검증 ==="

# 1. RLS 활성화 확인
echo "\n[1] RLS 활성화 상태"
grep -c "ENABLE ROW LEVEL SECURITY" supabase/migrations/*.sql

# 2. 정책 수 확인
echo "\n[2] 정책 정의 수"
grep -c "CREATE POLICY" supabase/migrations/*.sql

# 3. tenant_id 조건 확인
echo "\n[3] tenant_id 격리 조건"
grep -c "tenant_id.*auth.jwt" supabase/migrations/*.sql

echo "\n=== 검증 완료 ==="
```

---

## 관련 파일

```
supabase/migrations/
├── 00001_init.sql              # 테이블 생성
├── 00002_rls_policies.sql      # RLS 정책 정의
├── 00003_tenant_isolation.sql  # 테넌트 격리
└── 00004_admin_policies.sql    # Admin 정책

src/lib/supabase/
├── client.ts                   # Supabase 클라이언트
├── admin.ts                    # Service Role 사용
└── rls-helpers.ts              # RLS 헬퍼 함수
```

---

## 사용법

```bash
# 전체 RLS 검증
/audit --rls

# 특정 테이블만
/audit --rls --table profiles

# 마이그레이션 검증
/audit --rls --migrations
```
