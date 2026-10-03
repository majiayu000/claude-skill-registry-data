---
name: deprecation-and-migration
description: >
  코드 부채 정리 + 안전한 마이그레이션 + 코드 최소화(reducing-entropy).
  레거시 코드 폐기 계획, API 버전 전환, 라이브러리 마이그레이션, 단계적 제거,
  Dead Code 탐지, LOC 측정. /deprecate로 실행.
license: MIT
metadata:
  version: "2.0.0"
  merged-from: "reducing-entropy"
---

# Deprecation & Migration — 코드 부채 정리 + 안전한 마이그레이션

> **코드는 자산이 아니라 부채다.** 유지보수할 코드가 적을수록 팀은 빠르게 움직인다.
> 삭제하지 못하는 코드는 미래의 버그이고, 마이그레이션하지 않는 레거시는 기술 부채의 이자다.

## Quick Start

```
/deprecate                          # 대화형 폐기/마이그레이션 계획 수립
/deprecate scan                     # 프로젝트 내 폐기 대상 스캔
/deprecate plan "jQuery → vanilla"  # 특정 마이그레이션 계획 생성
/deprecate api v1 → v2              # API 버전 전환 계획
/deprecate audit                    # 기술 부채 감사
```

**공식 호출명:** `/deprecate` (별칭: `마이그레이션`, `레거시 정리`, `코드 부채`)

## 적용 시점

| 상황 | 적용 |
|------|------|
| 라이브러리/프레임워크 메이저 버전 업그레이드 | O |
| API 버전 폐기 (v1 → v2) | O |
| 레거시 코드 단계적 제거 | O |
| 언어/런타임 마이그레이션 (JS → TS, Python 2 → 3) | O |
| DB 스키마 대규모 변경 | O |
| 인프라 전환 (온프렘 → 클라우드) | O |
| 단순 리팩토링 (이름 변경, 파일 이동) | X — 일반 리팩토링 |
| 새 기능 추가 | X |

---

## CRITICAL: First Actions

### 1. Print Intro

```
Deprecation & Migration — 코드 부채 정리
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
순서: Audit → Plan → Deprecate → Migrate → Verify → Cleanup
```

### 2. 현재 상태 스캔

```bash
# 1. @deprecated 어노테이션/주석 찾기
echo "=== @deprecated ==="
grep -rn "@deprecated\|@Deprecated\|# deprecated\|// deprecated\|DEPRECATED" \
  --include="*.{ts,tsx,js,jsx,py,java,go,rb,cs,kt,rs}" . 2>/dev/null | head -30

# 2. TODO/FIXME/HACK 찾기
echo "=== TODO/FIXME/HACK ==="
grep -rn "TODO\|FIXME\|HACK\|XXX\|WORKAROUND" \
  --include="*.{ts,tsx,js,jsx,py,java,go,rb,cs,kt,rs}" . 2>/dev/null | wc -l

# 3. 오래된 의존성 확인
echo "=== Outdated Dependencies ==="
npm outdated 2>/dev/null || pip list --outdated 2>/dev/null || \
  go list -m -u all 2>/dev/null | grep '\[' | head -20

# 4. Dead code 후보 (export되지만 import 안 되는 것)
echo "=== Unused Exports (sample) ==="
grep -rn "^export " --include="*.{ts,tsx,js,jsx}" . 2>/dev/null | head -10
```

---

## Step 1: 기술 부채 감사 (Audit)

### 부채 분류 매트릭스

| 카테고리 | 예시 | 리스크 | 우선순위 기준 |
|----------|------|--------|-------------|
| **보안 부채** | 패치 안 된 의존성, 취약한 암호화 | 높음 | 즉시 |
| **호환성 부채** | EOL 런타임, 폐기 예정 API | 높음 | 분기 내 |
| **성능 부채** | N+1 쿼리, 불필요한 번들 | 중간 | 다음 스프린트 |
| **가독성 부채** | 죽은 코드, 혼란스러운 네이밍 | 낮음 | 여유 시 |

### 감사 보고서 템플릿

```markdown
# Tech Debt Audit Report

**Date**: {YYYY-MM-DD}
**Scope**: {프로젝트/모듈}

## Summary
- 총 부채 항목: {N}개
- Critical: {N} | High: {N} | Medium: {N} | Low: {N}

## Critical Items
| # | 항목 | 위치 | 리스크 | 예상 작업량 |
|---|------|------|--------|-----------|
| 1 | {항목} | {파일:라인} | {리스크} | {시간/일} |

## Recommended Migration Order
1. {가장 먼저 해야 할 것} — 이유: {왜}
2. {두 번째} — 이유: {왜}
```

---

## Step 2: 폐기 계획 (Deprecation Plan)

### 2.1 API 폐기 패턴

```markdown
# API Deprecation Plan: {API 이름} v{old} → v{new}

## Timeline
| 단계 | 날짜 | 조치 |
|------|------|------|
| Announce | {D-day} | 폐기 공지 + v{new} 제공 |
| Sunset Warning | {+30일} | 응답 헤더에 Sunset 추가 |
| Usage Drop Gate | {+60일} | v{old} 사용률 < 5% 확인 |
| Soft Removal | {+90일} | v{old} 410 Gone 반환 |
| Hard Removal | {+120일} | v{old} 코드 삭제 |

## API Response Headers (Sunset 기간)
```http
Sunset: Sat, 01 Nov 2026 00:00:00 GMT
Deprecation: true
Link: <https://api.example.com/v2/docs>; rel="successor-version"
```

## Migration Guide for Consumers
| v1 Endpoint | v2 Endpoint | Breaking Changes |
|-------------|-------------|-----------------|
| GET /v1/users | GET /v2/users | 페이지네이션 변경 |
```

### 2.2 라이브러리 마이그레이션 패턴

```markdown
# Migration Plan: {old-lib} → {new-lib}

## Compatibility Layer (Strangler Fig 패턴)
1. new-lib를 설치하고 old-lib과 공존
2. 새 코드는 new-lib으로 작성
3. 기존 코드를 모듈 단위로 전환
4. old-lib 사용처가 0이 되면 제거

## File-by-File Migration Tracker
| 파일 | 상태 | old-lib 사용 | 비고 |
|------|------|-------------|------|
| src/components/Button.tsx | migrated | 0 | |
| src/utils/api.ts | pending | 3 | 복잡도 높음 |
| src/pages/Home.tsx | pending | 1 | |
```

### 2.3 코드 폐기 마킹

언어별 폐기 어노테이션:

```typescript
// TypeScript/JavaScript
/** @deprecated Use `newFunction()` instead. Will be removed in v3.0. */
export function oldFunction(): void { ... }
```

```python
# Python
import warnings
def old_function():
    """Deprecated: Use new_function() instead. Removed in v3.0."""
    warnings.warn("old_function is deprecated, use new_function", DeprecationWarning, stacklevel=2)
    return new_function()
```

```java
// Java
@Deprecated(since = "2.0", forRemoval = true)
public void oldMethod() { ... }
```

```csharp
// C#
[Obsolete("Use NewMethod() instead. Will be removed in v3.0.", false)]
public void OldMethod() { ... }
```

---

## Step 3: 마이그레이션 실행

### 3.1 Strangler Fig 패턴 (점진적 교체)

```
Phase 1: 공존 — old + new 모두 동작
  └─ new-lib 설치, adapter/bridge 작성
  └─ 새 코드는 무조건 new 사용

Phase 2: 전환 — 모듈 단위로 old → new 교체
  └─ 리스크 낮은 모듈부터 시작
  └─ 각 모듈 전환 후 테스트

Phase 3: 정리 — old 제거
  └─ old-lib 사용처 0 확인
  └─ old-lib 의존성 제거
  └─ adapter/bridge 코드 제거
```

### 3.2 Feature Flag 기반 전환

```typescript
// 피처 플래그로 old/new 전환
if (featureFlags.isEnabled('use-new-auth')) {
  return newAuthService.login(credentials);
} else {
  return legacyAuthService.login(credentials);  // @deprecated
}
```

### 3.3 마이그레이션 스크립트 (자동화 가능한 경우)

```bash
# codemod 예시 (jscodeshift)
npx jscodeshift -t transforms/old-to-new.ts src/**/*.tsx

# AST 기반 변환 (Python)
python -m libcst.tool codemod old_to_new.OldToNewTransform .

# sed 기반 단순 치환 (최후 수단)
find src -name "*.ts" -exec sed -i 's/oldImport/newImport/g' {} +
```

---

## Step 4: 검증

### 마이그레이션 완료 검증 체크리스트

| # | 항목 | 확인 방법 |
|---|------|-----------|
| 1 | old-lib 사용처 0 | `grep -rn "old-lib" src/` 결과 없음 |
| 2 | old-lib 의존성 제거 | `package.json` / `requirements.txt`에서 삭제 |
| 3 | 테스트 전체 통과 | CI 그린 |
| 4 | @deprecated 마킹 정리 | 제거 완료된 항목의 deprecated 주석 삭제 |
| 5 | adapter/bridge 코드 정리 | 호환 레이어 제거 |
| 6 | 문서 업데이트 | API 문서, README에서 old 참조 제거 |
| 7 | CHANGELOG 기록 | Breaking changes 명시 |

### 회귀 테스트 전략

```bash
# 전체 테스트 실행
npm test -- --coverage    # JS/TS
pytest --cov=src          # Python
go test -cover ./...      # Go

# 마이그레이션 전후 스냅샷 비교 (API 응답)
diff <(curl -s localhost:3000/api/v1/users) <(curl -s localhost:3000/api/v2/users)
```

---

## Step 5: 정리 + 문서화

### 마이그레이션 후 Dead Code 정리

마이그레이션 완료 후 old 코드 잔재물 정리는 `/hestia`(헤스티아)를 사용합니다:

```
/hestia scan    # 미사용 export, 의존성, 파일 스캔
/hestia clean   # 스캔 + 자동 삭제
```

### 마이그레이션 ADR 작성

마이그레이션 결정은 반드시 ADR로 기록:

```
/adr "jQuery를 제거하고 vanilla JS로 전환"
```

---

## 출력 형식

```
마이그레이션 계획 생성 완료
━━━━━━━━━━━━━━━━━━━━━━━━━━
  대상: moment.js → date-fns
  전략: Strangler Fig (점진적 교체)
  
  현재 상태:
    moment.js 사용처: 47개 파일
    예상 작업량: 3-5일
  
  생성된 산출물:
    - docs/migration-moment-to-datefns.md  (마이그레이션 계획)
    - docs/adr/0008-replace-moment.md      (ADR)
  
  권장 순서:
    1. date-fns 설치 + adapter 작성
    2. utils/ 모듈 먼저 전환 (리스크 낮음)
    3. components/ 전환
    4. moment.js 제거 + 테스트

다음 단계:
  - /adr로 결정 기록 (자동 생성됨)
  - 모듈별 PR 분리 권장
  - /launch로 배포 전 체크
```

---

## Red Flags — 위험한 마이그레이션 패턴

| 패턴 | 위험 | 대안 |
|------|------|------|
| 빅뱅 마이그레이션 (한 번에 전부) | 롤백 불가, 디버깅 불가 | Strangler Fig 패턴 |
| 마이그레이션 중 기능 추가 | 범위 폭발, 원인 혼동 | 마이그레이션과 기능을 분리 |
| "나중에 정리" 약속 | 영원히 안 함 | 마이그레이션 PR에 정리 포함 |
| 테스트 없이 전환 | 회귀 버그 | 전환 전 테스트부터 작성 |
| deprecated 마킹만 하고 제거 안 함 | 부채 누적 | 제거 일정 + 알림 설정 |
| adapter 코드 영구 유지 | 복잡도 증가 | 전환 완료 후 즉시 제거 |

---

## 파이프라인 위치

```
/deprecate audit → /deprecate plan → /agent-team (구현) → /code-reviewer → /launch
  부채 감사        마이그레이션 계획    병렬 구현          리뷰           출시
```

**독립 실행 가능** — `scan`, `audit`, `plan` 각각 단독 사용 가능.

---

## Related Files

| 파일 | 역할 |
|------|------|
| `docs/migration-*.md` | 마이그레이션 계획 |
| `docs/adr/*.md` | 관련 아키텍처 결정 |
| `skills/documentation-and-adrs/SKILL.md` | ADR 작성 |
| `skills/dependency-updater/SKILL.md` | 의존성 업데이트 |
| `skills/release-notes/SKILL.md` | Breaking changes 기록 |
