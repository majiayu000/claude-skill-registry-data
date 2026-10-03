---
name: shipping-and-launch
description: >
  프리런치 체크리스트 + 단계적 롤아웃 전략. 배포 전 품질 게이트, 모니터링 설정,
  롤백 계획을 체계적으로 점검. "런치", "배포 준비", "출시 체크리스트", "go-live" 요청에 실행.
  /launch로 실행.
license: MIT
metadata:
  version: "1.0.0"
  benchmarked_from: "addyosmani/agent-skills"
---

# Shipping & Launch — 출시 체크리스트 + 단계적 롤아웃

> "빨리 배포하되, 안전하게 배포하라."
> 배포는 코드 완성이 아니라 **사용자에게 가치가 전달되는 순간**이다.

## Quick Start

```
/launch                       # 전체 프리런치 체크리스트 실행
/launch --scope backend       # 백엔드만 체크
/launch --scope frontend      # 프론트엔드만 체크
/launch --rollout              # 단계적 롤아웃 계획 생성
/launch --rollback             # 롤백 플레이북 생성
/launch --dry-run              # 체크만 (변경 없음)
```

**공식 호출명:** `/launch` (별칭: `런치`, `출시`, `go-live`, `배포 준비`)

## 적용 시점

| 상황 | 적용 |
|------|------|
| 새 기능/서비스 첫 배포 | O |
| 대규모 마이그레이션 후 go-live | O |
| API 버전 전환 | O |
| 인프라 변경 (DB, 캐시, CDN) | O |
| 일상적인 버그 수정 배포 | X — `/release`로 충분 |
| 개발 환경 변경 | X |

---

## CRITICAL: First Actions

### 1. Print Intro

```
Shipping & Launch — 출시 체크리스트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
순서: Scope → Pre-Launch → Launch Plan → Rollback → Post-Launch
```

### 2. 배포 스코프 감지

```bash
# 변경 범위 파악
_BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||' || echo "main")
_CHANGED=$(git diff origin/$_BASE --name-only 2>/dev/null || git diff HEAD~10 --name-only)

# 영역 분류
_HAS_BACKEND=false; _HAS_FRONTEND=false; _HAS_INFRA=false
_HAS_DB=false; _HAS_API=false; _HAS_AUTH=false; _HAS_DEPS=false

echo "$_CHANGED" | grep -qiE '\.(py|rb|java|go|cs|rs|kt|php)$' && _HAS_BACKEND=true
echo "$_CHANGED" | grep -qiE '\.(tsx?|jsx?|vue|svelte|css|scss)$' && _HAS_FRONTEND=true
echo "$_CHANGED" | grep -qiE '(docker|k8s|terraform|helm|nginx|Caddyfile)' && _HAS_INFRA=true
echo "$_CHANGED" | grep -qiE '(migrat|schema|alembic|flyway|prisma)' && _HAS_DB=true
echo "$_CHANGED" | grep -qiE '(openapi|swagger|\.proto|graphql)' && _HAS_API=true
echo "$_CHANGED" | grep -qiE '(auth|login|session|token|oauth|jwt)' && _HAS_AUTH=true
echo "$_CHANGED" | grep -qiE '(package\.json|requirements|go\.mod|Cargo|\.csproj)' && _HAS_DEPS=true

echo "SCOPE: backend=$_HAS_BACKEND frontend=$_HAS_FRONTEND infra=$_HAS_INFRA"
echo "       db=$_HAS_DB api=$_HAS_API auth=$_HAS_AUTH deps=$_HAS_DEPS"
```

---

## Step 1: Pre-Launch 체크리스트

### 1.1 코드 품질 게이트

| # | 항목 | 확인 방법 | 필수 |
|---|------|-----------|------|
| 1 | 모든 테스트 통과 | `npm test` / `pytest` / `go test` | **필수** |
| 2 | 타입 체크 통과 | `tsc --noEmit` / mypy / etc. | **필수** |
| 3 | 린트 통과 | `eslint` / `ruff` / `golangci-lint` | **필수** |
| 4 | 코드 리뷰 완료 | PR approved | **필수** |
| 5 | 보안 스캔 | `npm audit` / `pip audit` / SAST | 권장 |
| 6 | 번들 사이즈 확인 | 이전 대비 증가량 | 프론트엔드 |
| 7 | 성능 테스트 | 부하 테스트 / 벤치마크 | 대규모 변경 시 |

### 1.2 인프라/환경 체크

| # | 항목 | 확인 사항 |
|---|------|-----------|
| 1 | 환경 변수 | 새 env var가 프로덕션에 설정되었는가? |
| 2 | 시크릿 | 새 시크릿이 시크릿 매니저에 등록되었는가? |
| 3 | DB 마이그레이션 | 마이그레이션이 롤백 가능한가? |
| 4 | 외부 의존성 | 새 API 키, 서드파티 서비스 준비 완료? |
| 5 | DNS/도메인 | 새 도메인/서브도메인 설정 완료? |
| 6 | SSL/TLS | 인증서 유효? 자동 갱신 설정? |
| 7 | CDN/캐시 | 캐시 무효화 계획? |

### 1.3 모니터링/관측성 체크

| # | 항목 | 확인 사항 |
|---|------|-----------|
| 1 | 로깅 | 핵심 경로에 로그 있는가? |
| 2 | 메트릭 | 비즈니스 메트릭 대시보드 준비? |
| 3 | 알림 | 에러율/지연시간 알림 설정? |
| 4 | 헬스체크 | `/health` 엔드포인트 존재? |
| 5 | APM | 트레이싱 설정 (Datadog, Sentry 등)? |

### 1.4 사용자 경험 체크 (프론트엔드)

| # | 항목 | 확인 사항 |
|---|------|-----------|
| 1 | 크로스 브라우저 | Chrome, Firefox, Safari, Edge |
| 2 | 모바일 반응형 | 320px ~ 1440px |
| 3 | 접근성 | 키보드 네비게이션, 스크린 리더 |
| 4 | 에러 상태 | 네트워크 오류, 빈 상태, 로딩 상태 |
| 5 | SEO | 메타 태그, OG 태그, sitemap |

---

## Step 2: 단계적 롤아웃 계획

### 롤아웃 단계 템플릿

```markdown
# Rollout Plan: {기능/서비스명}

## Phase 1: Internal (Day 0)
- **대상**: 내부 팀 / 스테이징
- **비율**: 0% 외부 트래픽
- **기간**: 1-2일
- **성공 기준**: 에러율 < 0.1%, 지연시간 기존 대비 ±10%
- **모니터링**: 15분 간격 대시보드 확인

## Phase 2: Canary (Day 1-3)
- **대상**: 1-5% 프로덕션 트래픽
- **기간**: 1-3일
- **성공 기준**: 에러율 < 0.5%, P99 지연시간 < {N}ms
- **자동 롤백**: 에러율 > 1% 시 자동 롤백
- **모니터링**: 5분 간격

## Phase 3: Gradual (Day 3-7)
- **대상**: 10% → 25% → 50% 순차 확대
- **기간**: 3-5일
- **성공 기준**: 비즈니스 메트릭 이상 없음
- **확대 조건**: 24시간 안정 시 다음 단계

## Phase 4: Full (Day 7+)
- **대상**: 100% 트래픽
- **조건**: Phase 3 성공 기준 48시간 유지
- **이후**: 피처 플래그 정리, 레거시 코드 제거 계획
```

### 피처 플래그 체크

```bash
# 피처 플래그 사용 확인
grep -rn "feature_flag\|featureFlag\|FEATURE_\|isEnabled\|unleash\|launchdarkly\|growthbook" \
  --include="*.{ts,tsx,js,jsx,py,java,go,rb}" . 2>/dev/null | head -20
```

---

## Step 3: 롤백 플레이북

### 롤백 플레이북 템플릿

```markdown
# Rollback Playbook: {기능/서비스명}

## 롤백 트리거 조건
- [ ] 에러율 > {N}% (5분 이상 지속)
- [ ] P99 지연시간 > {N}ms (10분 이상 지속)
- [ ] 핵심 비즈니스 흐름 실패 (결제, 로그인 등)
- [ ] 데이터 무결성 이슈 발견

## 즉시 롤백 절차

### 애플리케이션 롤백
```sh
# 이전 버전으로 롤백
git revert HEAD                              # git
kubectl rollout undo deployment/{name}       # k8s
aws ecs update-service --force-new-deployment # ECS
```

### DB 마이그레이션 롤백
```sh
# 마이그레이션 되돌리기 (가능한 경우)
npx prisma migrate resolve --rolled-back {migration}  # Prisma
alembic downgrade -1                                   # Alembic
flyway undo                                            # Flyway
```

### 피처 플래그 킬스위치
```sh
# 피처 플래그로 즉시 비활성화 (코드 롤백 불필요)
curl -X PATCH {flag-service}/api/flags/{flag-name} \
  -d '{"enabled": false}'
```

## 롤백 후 확인
- [ ] 에러율 정상 복귀
- [ ] 지연시간 정상 복귀
- [ ] 사용자 신고 없음
- [ ] 포스트모텀 일정 잡기
```

---

## Step 4: Post-Launch 체크리스트

| 시점 | 항목 | 확인 사항 |
|------|------|-----------|
| **+1시간** | 에러율 | 정상 범위 내 |
| | 지연시간 | P50, P99 확인 |
| | 로그 | 새로운 에러 패턴 없음 |
| **+24시간** | 비즈니스 메트릭 | 전환율, 이탈률 이상 없음 |
| | 사용자 피드백 | CS 문의 증가 여부 |
| | 리소스 사용량 | CPU, 메모리, 디스크 |
| **+1주** | 안정성 확인 | 에러 트렌드 분석 |
| | 피처 플래그 정리 | 불필요한 플래그 제거 |
| | 문서 업데이트 | 운영 문서, API 문서 |
| | 포스트모텀 | 이슈 있었으면 회고 작성 |

---

## Step 5: 최종 출력

```
Launch 체크리스트 완료
━━━━━━━━━━━━━━━━━━━━━━
  스코프: backend + frontend + db-migration
  
  Pre-Launch:
    [PASS] 코드 품질 게이트     (8/8 통과)
    [PASS] 인프라/환경 체크      (7/7 확인)
    [WARN] 모니터링 체크         (4/5 — APM 미설정)
    [PASS] 사용자 경험 체크      (5/5 확인)
  
  생성된 산출물:
    - docs/rollout-plan-{feature}.md    (롤아웃 계획)
    - docs/rollback-playbook-{feature}.md (롤백 플레이북)
  
  판정: GO (경고 1건 — APM 설정 권장)
  
  다음 단계:
    1. APM 설정 (권장)
    2. /release로 버전 태그
    3. 배포 실행
    4. Post-Launch +1시간 체크
```

---

## Red Flags — 위험한 배포 패턴

| 패턴 | 위험 | 대안 |
|------|------|------|
| 금요일 오후 배포 | 주말 장애 대응 불가 | 월-목 오전 배포 |
| 롤백 계획 없이 배포 | 장애 시 복구 지연 | 항상 롤백 플레이북 작성 |
| 모니터링 없이 배포 | 장애 인지 지연 | 최소 헬스체크 + 알림 |
| 빅뱅 배포 (100% 즉시) | 전체 사용자 영향 | 카나리 → 점진적 확대 |
| DB 스키마 + 앱 동시 배포 | 롤백 복잡도 급증 | 스키마 먼저, 앱 따로 |
| 수동 배포 스크립트 | 실수 가능성 | CI/CD 파이프라인 |

---

## 파이프라인 위치

```
/zephermine → /agent-team → /code-reviewer → /release → /launch
  설계          구현           리뷰           버전      출시 체크
```

**독립 실행 가능** — 파이프라인 밖에서 단독 사용.

---

## Related Files

| 파일 | 역할 |
|------|------|
| `docs/rollout-plan-*.md` | 롤아웃 계획 |
| `docs/rollback-playbook-*.md` | 롤백 플레이북 |
| `skills/release-notes/SKILL.md` | 버전 + CHANGELOG 생성 |
| `skills/deploymonitor/SKILL.md` | 배포 모니터링 |
| `skills/argos/SKILL.md` | 구현 검증 (감리) |
