---
name: minos
description: QA 시나리오 수집·현장 생성 → Playwright 코드 생성 → 실행·수정 반복을 수행한다. /minos, 미노스, /qpassenger, 큐패신저, QA 통과할 때까지, 테스트 통과까지, playwright test until pass 요청에 사용한다.
---

# Minos (미노스)

> **미노스(Minos)**: 그리스 신화의 저승 심판자. 죽은 자의 영혼을 심판해 합격/불합격을 가립니다.
> 코드를 심판대에 세워 모든 테스트가 통과할 때까지 fix 루프를 반복하는 이 스킬의 본성과 일치합니다.

QA 시나리오를 Playwright 테스트 코드로 변환하고, 모든 테스트가 통과할 때까지 자동으로 수정을 반복합니다.

## Quick Start

```
/minos                           # 자동 감지 (qa-scenarios.md 또는 docs/qa/)
/minos @qa-scenarios.md          # 특정 QA 문서 지정
/minos --api-only                # API 테스트만
/minos --ui-only                 # UI 테스트만
```

**공식 호출명:** `/minos` (별칭: `미노스`, 레거시: `/qpassenger`, `큐패신저`)

## 워크플로우 (7단계)

```
Step 1: 시나리오 수집
  ↓
Step 2: Playwright 코드 생성
  ↓
Step 3: 서버 준비 (자동 감지 + 실행)
  ↓
Step 4: 테스트 실행
  ↓
Step 5: 브라우저 탐색 QA (탐색 스크립트 생성·실행 → 이슈 회수)
  ↓
Step 6: Healer Loop (실패 → 수정 → 재실행, max 5회)
  ↓
Step 7: 결과 보고 + 서버 정리
```

---

## Step 1: 시나리오 수집

QA 시나리오를 수집합니다. 우선순위 순으로 탐색:

1. `$ARGUMENTS`로 전달된 QA 문서 경로
2. `qa-scenarios.md` (zephermine 산출물)
3. `docs/qa/*.md` (기존 QA 문서)
4. 위 모두 없으면 → Minos Step 1 계약으로 현장 생성

### API 직접 호출·서버 검증 시나리오

상세 기준은 `skills/code-reviewer/references/security-audit.md`의 `API 직접 호출·서버 검증 계약`이다.
프로젝트에 없으면 현재 CLI 활성 루트, 이어서 `SKILLS-CATALOG.md`의 code-reviewer 원본 경로로
해석하고 그 모듈의 참조를 직접 읽는다. source-only를 slash 호출하거나 전역 활성화하지 않는다.
참조 누락은 `NOT RUN`으로 남긴다. 대상 API에 계약 ID별 사례를 매핑하고 기존 QA의 누락을 보충한다.
UI 입력만으로 끝내지 않고 독립 계정의 직접 HTTP 요청(기존 API 테스트 또는 Playwright request)을 실행한다.
정상 대조군·거부 응답·저장/상태/부수 효과의 전후 비교와 실행 증거를 계약 형식으로 남긴다.
기존 증거는 대상 버전·환경·조건이 같을 때 재사용한다. 서버·계정·관찰 수단 부족은 `NOT RUN`이며,
필수 사례 미실행을 전체 PASS로 표시하지 않는다. 명시적 UI-only 범위에서는 API 시험을 확장하지 않고
API 보안 검증 제외를 보고한다. 테스트를 통과시키려고 검증을 제거하거나 거부 기대값을 완화하지 않는다.

### 시나리오 파싱 규칙

QA 문서에서 테스트 케이스 테이블을 추출합니다:

```markdown
<!-- 이 형식을 인식 -->
| TC-ID | 시나리오 | 입력 | 기대 결과 | 우선순위 |
|-------|---------|------|----------|---------|
| TC-001 | 로그인 성공 | valid@email.com / Pass123! | 대시보드 이동 | P0 |
| TC-002 | 로그인 실패 | invalid@email.com / wrong | 에러 메시지 | P0 |
```

### 보충 시나리오 소스

`qa-scenarios.md`의 테스트 케이스가 부족하면 추가 소스를 참조합니다:

1. `operation-scenarios.md` (운영 시나리오) — qa-scenarios의 근거 문서. 메뉴별/업무별 흐름에서 누락된 테스트 케이스를 보충
2. `api-spec.md` — API 엔드포인트 중 qa-scenarios에 없는 것을 추가

### 시나리오 없을 때 현장 생성

qa-scenarios.md가 전혀 없으면 미노스가 직접 시나리오를 생성합니다:

**1단계: 프로젝트 분석 (자동)**

```bash
# 라우트/API 엔드포인트 탐색
grep -rn "router\.\|@Get\|@Post\|@app\.\|app\.get\|app\.post" --include="*.{ts,tsx,js,py,java}" src/ app/ 2>/dev/null | head -30

# 페이지/컴포넌트 탐색
find src -name "*.tsx" -path "*/pages/*" -o -name "*.tsx" -path "*/app/*" 2>/dev/null
```

**2단계: 시나리오 생성 (CRUD + 엣지 케이스)**

| 입력 소스 | 생성 전략 |
|-----------|----------|
| `operation-scenarios.md` 있음 | 업무 흐름 기반 TC 작성 (우선) |
| `api-spec.md` 있음 | API 엔드포인트별 정상/에러 케이스 |
| 둘 다 없음 | 코드 분석으로 라우트/페이지 자동 감지 → TC 생성 |

**3단계: TC 테이블 작성**

각 기능에 대해 아래 형식으로 테스트 케이스를 작성합니다:

```markdown
| TC-ID | 시나리오 | 유형 | 입력 | 기대 결과 | 우선순위 | 전제조건 |
|-------|---------|------|------|----------|---------|---------|
| TC-001 | 정상 로그인 | 정상 | valid@test.com / Pass123! | 대시보드 이동 | P0 | 회원 가입 완료 |
| TC-002 | 잘못된 비밀번호 | 에러 | valid@test.com / wrong | "비밀번호 오류" 표시 | P0 | - |
| TC-003 | 빈 이메일 제출 | 엣지 | (빈값) / Pass123! | "이메일 필수" 검증 | P1 | - |
```

**TC 유형별 필수 포함:**

| 유형 | 최소 케이스 | 예시 |
|------|-----------|------|
| 정상 (Happy path) | 기능당 1~2개 | 로그인 성공, 주문 완료 |
| 에러 (Error) | 기능당 2~3개 | 잘못된 입력, 권한 없음, 404 |
| 엣지 (Edge) | 주요 기능당 1~2개 | 빈값, 특수문자, 최대길이, 동시 요청 |
| 회귀 (Regression) | 변경 영역당 1개 | 기존 기능이 깨지지 않았는지 |

**4단계: 저장**

생성된 시나리오를 `qa-scenarios.md`로 저장 → Step 2로 진행

### 도메인사전 컨텍스트 로드

Step 1 끝에 `docs/domain-dictionary.md` 존재 여부를 확인하고, 있으면 메모리에 로드하여 Step 2~6 전체에서 참조합니다.

**용도:**
- 시나리오 텍스트의 도메인 용어를 사전 한글 표기와 일치시킴 (예: 사전 `Cart=장바구니`인데 시나리오에 "쇼핑백"이면 정정)
- Step 2 코드 생성 시 `describe`/`it` 블록에 사전 영문 식별자 사용
- 사전 위반 발견 시 Step 6 Healer Loop의 수정 후보로 분류

사전이 없으면 이 컨텍스트 단계 건너뜀.

---

## Step 2: Playwright 코드 생성

시나리오 → Playwright TypeScript 테스트 코드로 변환합니다.

> 상세 변환 규칙: [references/playwright-codegen.md](references/playwright-codegen.md)

### 프로젝트 감지

```
# 테스트 프레임워크 자동 감지
playwright.config.ts 존재 → Playwright 설정 재사용
package.json "playwright" → 버전 확인
없으면 → npx playwright install 안내
```

파일 구조: `tests/e2e/{feature}.spec.ts` + `tests/api/{feature}-api.spec.ts` (기능 단위 분리)

### 코드 생성 원칙

- 각 기능별 `describe` 블록, TC-ID 주석 포함
- Role-based selector 우선, 하드코딩 URL 금지, `beforeEach`로 상태 초기화
- **도메인사전 준수** (사전 있을 때): `describe('Cart')`, `it('adds item to 장바구니')` 같이 영문 식별자(클래스/함수명) + 한글 표기(테스트 설명/UI 라벨 매칭) 모두 사전 따름. 사전 금지 표현(예: `basket`)은 코드/주석에 절대 사용 금지

---

## Step 3: 서버 준비 (자동 감지 + 실행)

테스트 전에 앱 서버를 자동으로 준비합니다. 사용자 개입 없이 진행합니다.

감지 순서: docker-compose.yml → Dev Server → Django → 사용자 안내

> 네이티브 `/run`과의 관계: /run은 단발 실행·확인용이고, 이 Step은 테스트 수명주기에 묶인 서버 준비
> (포트 정리·헬스체크·종료)라 자체 절차가 기본입니다. 자체 감지가 모두 실패하면 /run의 실행 패턴을 참고.

환경별 서버 실행, 포트 정리, 헬스체크 상세: See [server-setup.md](references/server-setup.md)

---

## Step 4: 테스트 실행

### Worker 수 제한 (CPU 보호)

**기본값: CPU 논리코어의 50%** (`--workers=50%`)
사용자가 `--workers` 옵션으로 오버라이드 가능합니다.

```bash
# 기본 실행 (CPU 50% 제한)
npx playwright test --reporter=list --workers=50%

# 사용자가 --workers 지정 시 해당 값 사용
npx playwright test --reporter=list --workers=3      # 고정 3개
npx playwright test --reporter=list --workers=25%    # CPU 25%
npx playwright test --reporter=list --workers=1      # 직렬 (디버깅)

# headed 모드 (디버깅 필요 시)
npx playwright test --headed --workers=50%

# 특정 파일만
npx playwright test tests/e2e/auth.spec.ts --workers=50%
```

### 사전 조건 확인

테스트 실행 전 머신 상태(CPU 코어, workers 수, 예상 RAM)를 감지하여 사용자에게 보여줍니다.

CPU 감지 명령어 및 출력 형식: See [server-setup.md](references/server-setup.md)

추가 사전 조건: 서버 실행(Step 3 완료), DB 시드, `.env.test`, Playwright 브라우저 설치

---

## Step 5: 브라우저 탐색 QA (코드화 방식)

자동화 테스트(Step 4) 이후, **탐색용 Playwright 스크립트를 생성·실행**하여 실제 브라우저에서
탐색적 QA를 수행합니다. 자동화 테스트가 잡지 못하는 콘솔 에러, 네트워크 실패, 레이아웃 깨짐을 발견합니다.

Antigravity에서 사용자가 `/browser`를 명시적으로 열었거나 현재 세션에 browser capability가 노출돼
있으면 초기 탐색과 재현 후보 수집에 사용할 수 있습니다. 이 스킬이 slash command를 프로그램적으로
호출한다고 가정하지 않습니다. 네이티브 browser에서 발견한 이슈는 반복 가능한 Playwright 테스트나
`tests/explore/*.spec.ts`로 재현한 뒤에만 자동 PASS/FAIL 증거로 승격하며, 코드화하지 못한 관찰은
`exploratory-only`로 보고합니다. `/browser`는 Step 2~5의 Playwright 산출물과 Healer 재실행을 대체하지 않습니다.

> 상세 프로토콜: [references/browser-explorer.md](references/browser-explorer.md)

### 설계 원칙 (gstack browser 차용)

Step 2에서 이미 Playwright 코드를 생성하므로, 탐색 QA도 동일하게 **코드화**하여 일관성과 효율을 확보합니다.

| 원칙 | 의미 | 효과 |
|------|------|------|
| 코드화 | 페이지 순회·수집을 단일 Playwright 스크립트로 생성·실행 | Healer 반복 시 재탐색 비용 0 (스크립트 재실행) |
| 토큰 효율 | 수집 결과를 `report.json`으로 덤프, 컨텍스트엔 이슈만 적재 | 페이지 수에 무관하게 컨텍스트 안정 |
| MCP 비의존 | Playwright 이벤트 리스너로 console/network/error를 한 번에 수집 | Playwright MCP 설치 불필요 |

### 실행 조건

- **Playwright만 설치되어 있으면 기본 실행** (MCP 불필요)
- `--no-explore` 옵션으로 스킵 가능
- `--explore-only` 옵션으로 Step 2~4를 건너뛰고 이 단계만 실행 가능
- `--explore-mcp` 옵션으로 기존 Playwright MCP 방식 fallback (페이지마다 도구 직접 호출)

### 체크 항목

| 체크 | 수집 방법 (Playwright 이벤트) | 감지 대상 |
|------|------------------------------|----------|
| JS 에러 | `page.on('pageerror')` | `Uncaught TypeError`, unhandled rejection |
| 콘솔 에러 | `page.on('console')` (type=error) | React warnings, deprecated API |
| 네트워크 실패 | `page.on('response')` (status>=400) | 4xx/5xx, CORS, 404 리소스 |
| 구조 검증 | `page.accessibility.snapshot()` | 빈 페이지, 접근성 누락 |
| 시각적 확인 | `page.screenshot({fullPage})` | 레이아웃 깨짐, overflow, 빈 화면 |
| 인터랙션 | 생성된 `interact.spec.ts` (Phase 4) | 버튼 미반응, 폼 제출 실패 |

### 실행 흐름

```
1. 라우트 수집 (소스/qa-scenarios에서)
2. 탐색 스크립트 생성 → tests/explore/explore.spec.ts
   (ROUTES 순회 + console/pageerror/response 리스너 + screenshot + snapshot 덤프)
3. npx playwright test tests/explore/explore.spec.ts 실행
4. test-results/explorer/report.json 생성
5. jq/grep으로 이슈 항목만 추출 (전체를 컨텍스트에 올리지 않음)
6. (선택) snapshot.json 읽고 interact.spec.ts 생성·실행 (액티브 인터랙션)
```

### 발견 이슈 처리

- **P0/P1 코드 수정 가능** (JS 에러, API 실패) → Healer Loop(Step 6)에 전달
- **수동 확인 필요** (레이아웃, UX) → 결과 보고서(Step 7)에만 기록

---

## Step 6: Healer Loop

테스트 실패(Step 4) + 브라우저 탐색 QA 발견 이슈(Step 5)를 자동으로 분석하고 수정을 반복합니다.

> 상세 프로토콜: [references/healer-loop.md](references/healer-loop.md)

### 루프 구조

```
max_retries = 5
retry = 0

WHILE (실패한 테스트 존재) AND (retry < max_retries):
  1. 실패 로그 분석 (에러 메시지, 스택 트레이스)
  2. 원인 분류 → 수정 대상 결정
  3. 수정 적용 (현재 런타임의 직접 편집 기능)
  4. 재실행 (실패한 테스트만)
  5. retry++

IF retry >= max_retries:
  남은 실패 → test.fixme() 표시 + exhausted(미해결, ≠통과)로 라벨 + 사용자 보고
  → Healer 소진은 PASS가 아니다. "조건부 통과"로 둔갑시키지 않는다 (아래 판정 기준 참조)
```

### 원인 분류 체계

| 원인 | 수정 대상 | 예시 |
|------|----------|------|
| 셀렉터 변경 | 테스트 코드 | `button[name]` → `getByRole('button')` |
| API 응답 불일치 | 구현 코드 | 404 → 엔드포인트 경로 오류 |
| 타이밍 이슈 | 테스트 코드 | `waitForResponse`, `waitForSelector` 추가 |
| 비즈니스 로직 버그 | 구현 코드 | 유효성 검증 누락 |
| 테스트 데이터 문제 | 테스트 코드 | fixture/seed 데이터 수정 |
| 콘솔 JS 에러 | 구현 코드 | `TypeError`, `Unhandled Rejection` (Step 5 발견) |
| 404 리소스 | 구현 코드 | 이미지/폰트/API 경로 오류 (Step 5 발견) |
| 인프라 문제 | 사용자 안내 | DB 연결, 포트 충돌 |

### 수정 원칙

- **테스트 코드 수정 우선**: 구현이 정확하면 테스트를 맞춤
- **구현 코드 수정은 신중하게**: 명백한 버그만 수정
- **수정 범위 최소화**: 실패한 부분만 정확히 수정
- **인프라 문제는 수정하지 않음**: 사용자에게 보고

---

## Step 7: 결과 보고 + 서버 정리

### 결과 보고서 생성

요약·수정 이력·미통과 항목·브라우저 탐색 발견 이슈 4섹션으로 구성합니다.
보고서 마크다운 템플릿 및 QA 문서 업데이트 형식: See [result-report.md](references/result-report.md)

### 판정 기준 (Minos 실행 증거 기준)

| Grade | 조건 | 판정 |
|-------|------|------|
| **PASS** | 자동 테스트 + 탐색 QA 전체 통과 | 배포 가능 |
| **CONDITIONAL** | P0/P1 통과, P2/P3 일부 fixme 또는 탐색 QA 경고만 | 조건부 진행 |
| **FAIL** | P0 또는 P1 실패 존재 (자동 테스트 또는 탐색 QA) | 수정 필수 |

> **완료 계약 (028 — 거짓 완료 방지):** 각 시나리오의 "통과"는 그 시나리오의 Playwright assertion이 실제 green인 것을 증거로 한다.
> Healer 소진으로 `test.fixme()` 처리된 항목은 통과가 아니라 `exhausted`(미해결)로 집계한다.
> P0/P1에 `exhausted`가 하나라도 있으면 PASS/CONDITIONAL로 올리지 않고 **FAIL**로 판정한다 — 반복 소진을 조건부 통과로 둔갑시키지 않는다.

### QA 문서 업데이트

원본 시나리오 문서에 `✅ / ⚠️ fixme` 결과를 반영합니다.

---

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--workers N` | Playwright worker 수 (숫자 또는 퍼센트) | 50% |
| `--api-only` | API 테스트만 생성/실행 | false |
| `--ui-only` | UI E2E 테스트만 생성/실행 | false |
| `--max-retries N` | Healer 최대 반복 횟수 | 5 |
| `--headed` | 브라우저 화면 표시 | false |
| `--skip-generate` | 기존 테스트 코드 사용 (Step 2 건너뜀) | false |
| `--no-explore` | 브라우저 탐색 QA 스킵 (Step 5 건너뜀) | false |
| `--explore-only` | 브라우저 탐색 QA만 실행 (Step 2~4 건너뜀) | false |
| `--explore-mcp` | 탐색 QA를 Playwright MCP 방식으로 실행 (코드화 대신 fallback) | false |
| `--no-explore-active` | 액티브 인터랙션 탐색(Phase 4) 스킵, 패시브 수집만 | false |
| `--fix-code` | 구현 코드 수정도 허용 | true |
| `--fix-test-only` | 테스트 코드만 수정 (구현 코드 수정 금지) | false |

---

## 연관 실행 경로

| 경로 | 역할 | 연결 |
|------|------|------|
| Minos Step 1 (내장) | 프로젝트 근거 기반 시나리오 현장 생성 | Step 1 입력 |
| 네이티브 테스트 작업자 | 실제 테스트 설정·인접 테스트·빌드 명령 기반 코드 작성 | Step 2 구현 |
| zephermine (스킬) | qa-scenarios.md + operation-scenarios.md 생성 | Step 1 입력 |
| argos (스킬) | 설계 산출물 대비 준공 검증 | 별도 감리 |

---

### 서버 정리

테스트 완료 후 Step 3에서 실행한 서버를 정리합니다.

서버 정리 명령어 상세: See [server-setup.md](references/server-setup.md)

---

## 주의사항

- Playwright 미설치 시 `npx playwright install` 필요
- 브라우저 탐색 QA(Step 5)는 탐색 스크립트를 생성·실행하므로 Playwright만 있으면 동작 (MCP 불필요). `--explore-mcp`로 MCP 방식 fallback 가능
- 탐색 결과(`report.json`)는 전체를 컨텍스트에 올리지 말고 jq/grep으로 이슈 항목만 추출 (토큰 절약)
- Healer가 구현 코드를 수정하므로, 커밋되지 않은 변경사항이 있으면 주의
- 외부 의존성(메일, 결제 등) 테스트는 mock 대체 권장

---

## 다음 단계 안내

QA가 완료되면 사용자에게 다음 단계를 안내합니다:

```
✅ Minos 완료! (결과: {PASS/CONDITIONAL/FAIL})

👉 다음 단계 (선택):
  Docker 배포 환경 생성 → 카탈로그의 source-only docker-deploy 모듈을 직접 읽어 실행
  코드 리뷰             → 현재 CLI의 네이티브 리뷰 사용
  API 문서 생성          → 프로젝트 계약과 코드 근거로 작성
  변경사항 커밋          → 현재 CLI의 네이티브 Git 흐름 사용
  세션 핸드오프          → mnemo 핸드오프 계약 사용

📎 참고: docs/workflow-guide.md
```
