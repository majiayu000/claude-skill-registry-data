---
name: argos
description: 준공검사 감리 스킬. 설계 산출물(spec, api-spec, qa-scenarios, flow-diagrams) 대비 구현을 정적·런타임·API·QA·도면·보안 관점으로 검증한다. 일반 diff 품질은 가용한 CLI 네이티브 리뷰에 위임하고 spec 대비 감리는 직접 소유한다. /argos로 실행한다.
---

# Argos (아르고스) — 100개의 눈으로 검증하는 감리

> **아르고스 판옵테스(Argus Panoptes)**: 100개의 눈을 가진 그리스 신화의 감시자.
> 설계 도면과 스펙 대비 구현 상태를 빠짐없이 검증합니다.

## GS 작업을 전달받은 경우에만

GS 인증 사전점검에서 등급·기관 기준·run_dir을 전달받으면 `gs-certification` 모듈을
프로젝트 실제 경로 → 현재 CLI 활성 루트 → SKILLS-CATALOG.md의 정확한 source-only 경로로 해석한다.
그 SKILL.md를 읽고 부모 디렉터리의 `references/argos-gs-audit.md`를 적용한다.
GS 입력이 없는 일반 실행은 기존 절차를 따른다. 필수 참조 누락은 NOT RUN으로 반환한다.
사용자의 점검/수정 권한과 GS 출력 경로를 우선하고 기존 latest 보고서를 덮어쓰지 않는다.

## Quick Start

```
/argos                              # planning_dir 자동 탐색
/argos docs/plan/my-feature         # 특정 계획 디렉토리 지정
/argos --phase 5                    # 특정 Phase만 실행
```

**공식 호출명:** `/argos` (별칭: `아르고스`, `감리`)

## 내부 소스 모듈 해석 계약 (필수)

`code-reviewer`, `flow-verifier`, `frontend-design`, `ui-ux-auditor`는 Argos 안에서
호출하는 등록 스킬이 아니라, 절차와 기준을 직접 읽는 source-only 내부 모듈입니다. 각 이름에 대해
해석된 `SKILL.md` 절대경로를 `MODULE_SKILL[name]`, 그 부모 디렉터리를
`MODULE_ROOT[name]`으로 기록합니다.

각 모듈을 처음 쓰기 전에 다음 순서로 해석합니다.

1. 프로젝트 루트의 `skills/<name>/SKILL.md`가 **실제 파일로 존재하고 frontmatter의 `name`이
   정확히 `<name>`일 때만** 그 절대경로를 사용합니다. 없거나 이름이 다르면 프로젝트의 다른
   경로를 추측하지 않고 2번으로 갑니다.
2. 없으면 현재 런타임의 활성 루트에서 정확한 `skills/<name>/SKILL.md`를 확인합니다. Codex는
   `$CODEX_HOME/skills`(미설정이면 `~/.codex/skills`), Claude와 Grok 호환 표면은
   `~/.claude/skills`, Antigravity는 `~/.gemini/antigravity-cli/skills`입니다. 파일 존재와 frontmatter 이름이
   모두 일치할 때만 사용하고, 아니면 3번으로 갑니다.
3. 없으면 현재 런타임의 전역 `SKILLS-CATALOG.md`를 읽습니다. Codex는
   `$CODEX_HOME/SKILLS-CATALOG.md`(미설정이면 `~/.codex/SKILLS-CATALOG.md`), Claude와
   Grok 호환 표면은 `~/.claude/SKILLS-CATALOG.md`, Antigravity는
   `~/.gemini/antigravity-cli/SKILLS-CATALOG.md`입니다. 첫 번째 셀이 정확히 `<name>`인 행
   (`| <name> | ... | ... | <읽을 경로> |`) 하나를 찾아 `읽을 경로`의 절대 `SKILL.md`를
   그대로 사용합니다. 정확한 이름의 행이 0개이거나 2개 이상이면 해석 실패이며 다른 행이나
   레지스트리 경로를 추측하지 않습니다.
4. 해석한 파일의 존재를 확인하고 `SKILL.md` 전체를 읽은 뒤에만 그 모듈의 기준을 적용합니다.
   참조 파일은 `MODULE_ROOT[name]/references/...`, 스크립트는
   `MODULE_ROOT[name]/scripts/...`로부터 절대경로를 만듭니다.

이 과정은 모듈 읽기이지 스킬 호출이 아닙니다. `/code-reviewer`, `/flow-verifier`,
`/frontend-design`, `/ui-ux-auditor`를 호출하거나 스킬 레지스트리에 등록됐다고 가정하지 않습니다.
프로젝트·활성 루트 파일도 없고 카탈로그의 정확한 행·`읽을 경로`·필수 참조 중 하나라도 없으면 보고서의
`Module Coverage`에 경로와 이유를 기록하고 아래의 한정된 native fallback을 사용합니다. fallback도
실행할 수 없는 검사는 `NOT RUN` 또는 `UNVERIFIED`로 남기며 PASS로 바꾸지 않습니다.

| 모듈 | 한정된 native fallback |
|------|------------------------|
| `flow-verifier` | Phase 5의 노드·분기·순서·오류·코드에만 있는 경로 대조를 직접 수행하고 `source: native-fallback` 표기 |
| `frontend-design` | 이 문서와 verify-protocol에 적힌 축약 블랙리스트만 검사하고 전체 블랙리스트 커버리지는 `UNVERIFIED` |
| `ui-ux-auditor` | Phase 6의 9영역을 실제 렌더 우선으로 점검. 렌더 불가 시 `static-only`와 미관찰 영역을 명시 |
| `code-reviewer` | Phase 7에서 신뢰 경계, 마스킹된 시크릿 위치, 설치된 감사 도구, 입력·권한 경계, STRIDE만 점검하고 빠진 영역은 `NOT RUN` |

## 파이프라인 위치

```
/zephermine (설계사)  →  /agent-team (포세이돈)  →  /argos (감리)  →  /minos (실사)
     도면 생성               섹션 기반 구현           준공검사          런타임 테스트
```

## CRITICAL: First Actions

### 1. Print Intro

```
아르고스(Argos) — 100개의 눈으로 감리 시작
순서: Detect → Phase 0 (CPS 추적) → Phase 1 (정적) → Phase 2 (런타임) → Phase 3 (API) → Phase 4 (QA) → Phase 5 (도면) → Phase 6 (디자인) → Phase 7 (보안) → Phase 8 (도메인사전) → Report
```

### 2. Resolve Planning Directory

계획 산출물 디렉토리를 찾습니다:

1. `$ARGUMENTS`로 전달된 경로
2. `docs/plan/*/spec.md` 패턴으로 자동 탐색 (Glob) — **archive/ 경로 제외** (결과에서 `archive` 포함된 경로 필터링)
3. 못 찾으면 → 현재 CLI의 질문 방식으로 경로 요청

### 3. Scan Artifacts

`<planning_dir>/`에서 검증 대상 파일을 확인:

```
필수:
  spec.md              → Phase 0 (CPS 추적, Context Map/Problem Statement 있을 때)
                       → Phase 1 (정적 검증)

선택 (있으면 해당 Phase 실행):
  sections/index.md    → Phase 0-2, 0-3 (없으면 해당 서브체크 건너뜀)
  api-spec.md          → Phase 3 (API 일치)
  qa-scenarios.md      → Phase 4 (QA 시나리오)
  checklist.md (+ checklist-status.md) → Phase 4A (완료 기준 이행)
  flow-diagrams/index.md      → Phase 5 (도면 대조)
  docs/domain-dictionary.md   → Phase 8 (도메인사전 감리)
```

**spec.md조차 없으면:** 에러 메시지 출력 후 종료.
```
❌ 검증 대상 없음: spec.md를 찾을 수 없습니다.
   /zephermine으로 설계를 먼저 완료하세요.
```

상태 출력:
```
📋 검증 대상:
  ✅ spec.md (CPS)     → Phase 0 (Context Map + Problem Statement 감지됨)
  ✅ spec.md           → Phase 1, 2
  ✅ sections/index.md → Phase 0 (에코시스템 커버리지)
  ✅ api-spec.md       → Phase 3
  ✅ qa-scenarios.md   → Phase 4
  ✅ checklist.md      → Phase 4A (장부: checklist-status.md 있음/없음)
  ✅ flow-diagrams/ (3개)     → Phase 5
```

---

## 검증 프로세스 (9 Phase: 0~8)

### Phase 0: CPS 추적성 검증

spec.md에 `## Context Map`과 `## Problem Statement`가 **모두 있는 경우만** 실행합니다.
없으면 아래 메시지 출력 후 Phase 1로 바로 진행:
```
ℹ️ CPS 섹션 미감지 — 레거시 계획, Phase 0 건너뜀
```

See [verify-protocol.md](references/verify-protocol.md) — Phase 0

#### 0-1. Problem → Solution 추적
Problem Statement의 각 문제(P1, P2, P3...)에 대해:
- spec.md Requirements에 대응하는 솔루션이 기술되어 있는가?
- 결과: ✅ 추적됨 / ❌ 솔루션 없음

#### 0-2. 에코시스템 → 섹션 커버리지
Context Map의 에코시스템 맵 각 시스템에 대해:
- `sections/index.md`에서 대응 섹션이 있는가?
- ⏭️ 제외 사유가 문서화되어 있는가?
- 결과: ✅ 커버됨 / ⏭️ 명시적 제외 / ❌ 누락

#### 0-3. Problem → 섹션 매핑
Problem Statement의 '해결 섹션' 열이 가리키는 섹션 파일이 실제로 존재하는가?
- 결과: ✅ 존재 / ❌ 파일 없음

#### 등급 영향
- Phase 0 전체 통과 → 다음 Phase로 진행
- Phase 0 일부 실패 → **CONDITIONAL** 등급 (FAIL이 아님 — 문서 수정으로 해결 가능)
- Healer 분류: "manual fix required" (자동 수정 불가, 설계 문서 수정 필요)

---

### Phase 1: 정적 검증

See [verify-protocol.md](references/verify-protocol.md) — Phase 1

서로 독립적인 **읽기 전용 검증 작업** 2개를 실행합니다. 이 이름은 의미 계약입니다.
현재 CLI가 제공하는 내장 탐색·검토 기능을 사용하되 특정 에이전트 이름이나 호출 인자 형식을
요구하지 않습니다. 각 작업은 spec과 코드를 읽고 근거가 있는 발견만 반환하며, 소스·계획 산출물·
`verify-report.md`를 수정하지 않습니다. 네이티브 병렬 위임이 가능하면 동시에 실행하고, 위임이
없거나 실패하면 메인 컨텍스트에서 아래 두 작업을 순차 수행합니다.

1. **기능 검증 작업**: spec.md의 기능적 요구사항 vs 실제 코드
   - 각 요구사항별 구현 여부 (✅/❌)
   - 누락된 기능 구체적 명시
   - 엣지 케이스 처리 확인

2. **품질 검증 작업**: 비기능 요구사항 + 코드 품질
   - 성능/보안/접근성 요구사항 충족 여부
   - 테스트 커버리지
   - 타입 안전성
   - 문서화 상태

**일반 코드 품질 층 — 네이티브 리뷰 엔진 위임 (native-first, code-reviewer 모듈과 동일 경로):**

품질 검증 중 spec과 무관한 일반 코드 품질(버그·타입 안전성·중복)은 자체 스캔을 중복하지 않고 네이티브 결과를 재사용합니다:

- **같은 세션에 code-reviewer 보고서가 이미 있으면** 그 발견을 그대로 병합 — 재실행 금지
- Claude: Skill 목록에 `code-review`가 있으면 호출 (⚠️ `ultra` 호출 금지 — 클라우드 과금, 사용자 트리거 전용)
- Codex: `codex review --uncommitted` 또는 `--base <브랜치>`
- 네이티브 부재, 또는 감리 대상이 diff가 아니라 전체 코드베이스인 경우 → 위 품질 검증 체크리스트를 읽기 전용 작업자나 메인 컨텍스트에서 실행

병합 발견은 verify-report.md Phase 1에 `source: native`로 표기합니다.
**spec 대비 기능 검증(1번 작업)은 네이티브 diff 리뷰로 대체 불가** — diff 엔진은 spec을 모릅니다.

메인 컨텍스트만 두 축(기능 검증 + 품질 검증/네이티브 병합)의 결과를 정규화·중복 제거하고
정적 검증 보고서에 반영합니다. 위임된 작업은 보고서나 공유 상태를 직접 쓰지 않습니다.

### Phase 2: 런타임 검증

See [verify-protocol.md](references/verify-protocol.md) — Phase 2

빌드, 테스트, E2E를 실행하여 검증합니다.

> 네이티브 `/run`·`/verify`와의 관계: 둘은 단발 동작 확인용이고, 이 Phase는 감리 보고서에 들어갈
> 구조화된 검증 결과(빌드/테스트/E2E 파싱)를 만들기 위한 자체 절차입니다 — 의도된 설계.

1. **프로젝트 감지**: package.json, pom.xml, pyproject.toml 등에서 기술 스택 자동 감지
2. **빌드 검증**: `npm run build`, `mvn compile` 등 실행
3. **단위 테스트**: `npm test`, `pytest` 등 실행 + 결과 파싱 (통과/실패/스킵)
4. **E2E 테스트**: Playwright/Cypress 감지 시 실행 (미감지 시 건너뜀)

### Phase 3: API 일치 검증

`api-spec.md`가 있는 경우만 실행.

See [verify-protocol.md](references/verify-protocol.md) — Phase 3

1. 코드에서 실제 API 라우트 추출 (Express/Next.js/Spring/FastAPI 패턴 감지)
2. API Spec 문서와 대조:
   - spec에 있고 코드에 있음 → ✅ 일치
   - spec에 있지만 코드에 없음 → ❌ 미구현
   - 코드에 있지만 spec에 없음 → ⚠️ 미등록
3. 중복 API 탐지 (단수/복수, 동사 중복)

### Phase 4: QA 시나리오 검증

`qa-scenarios.md`가 있는 경우만 실행.

See [verify-protocol.md](references/verify-protocol.md) — Phase 4

1. 각 테스트 케이스를 코드/테스트 결과 기반으로 판정
2. `qa-scenarios.md`의 체크박스를 ✅/❌ 마킹
3. 통과율 집계 (정상/에러/엣지 케이스별)

### Phase 4A: 완료 기준 이행 감리

`checklist.md`가 있는 경우만 실행. 형식·상태·증거 규칙은 젭마인 `references/acceptance-checklist-guide.md`입니다.

1. `checklist-status.md` 장부가 있으면 `proved` 행의 증거를 다시 실행·확인합니다(인용된 테스트·명령 재실행, 관찰 재현).
   다시 실행해 실패하면 `contradicted`, 다시 실행할 수 없으면 `weak`로 기록합니다(가이드의 '다시 확인했을 때' 규칙).
   `proved`가 아닌 행도 검증 열이나 장부의 증거로 지금 만족하는지 확인해 감리 판정을 적습니다. 검증 열 밖의 실행 증거도 인정합니다.
2. 장부가 없으면 `checklist.md`의 검증 열을 기준으로 각 AC를 직접 확인하고 "이행 장부 없음"을 경고합니다.
3. 감리는 구현 장부를 고치지 않습니다. 감리 판정은 보고서에만 적습니다.
4. 집계: AC별 감리 판정(proved/weak/missing/contradicted), 장부 상태와 다른 행, 미이행 AC(감리 판정이 `proved`가 아닌 행).
5. 원인을 나눕니다: 두 AC가 서로 모순되면(가이드의 '계약 모순') **설계 결함 — 계약 변경 필요**, 그 밖은 **구현 미이행**.

**등급 영향:** `missing`·`contradicted`가 1개라도 있으면 FAIL, `weak`만 남으면 CONDITIONAL. FAIL 사유에 원인 구분을 적어 재시공(구현 미이행)과 계약 변경(설계 결함)을 섞지 않습니다.

### Phase 5: 프로세스 도면 검증

`flow-diagrams/`가 있는 경우만 실행.

See [verify-protocol.md](references/verify-protocol.md) — Phase 5

`MODULE_SKILL[flow-verifier]`에서 직접 읽은 verify 모드를 참조하여 검증합니다. 모듈 해석에
실패하면 위 native fallback을 쓰고 보고서에서 모듈 적용으로 표기하지 않습니다.

1. `flow-diagrams/index.md`에서 프로세스 다이어그램 목록 추출
2. 각 `.mmd` 파일의 노드와 실제 코드를 대조:
   - **노드 존재**: 다이어그램 노드에 대응하는 코드가 있는가
   - **분기 완전성**: 모든 분기(if/else, switch)가 구현되었는가
   - **경로 순서**: 코드 실행 순서가 화살표 방향과 일치하는가
   - **에러 처리**: 에러 경로 노드에 예외 처리가 있는가
   - **누락 경로**: 코드에만 있는 경로 (다이어그램 업데이트 필요)

### Phase 6: 디자인 준수 검증

`design-system.md`가 있는 경우만 실행. UI/프론트엔드가 없는 프로젝트는 자동 건너뜀.

See [verify-protocol.md](references/verify-protocol.md) — Phase 6

#### 6-1. 디자인 토큰 준수
`design-system.md`의 디자인 토큰(색상, 폰트, 간격, 라운딩)이 실제 코드에 적용되었는지 확인:
- CSS 변수 / Tailwind config에 토큰이 정의되어 있는가
- 하드코딩된 색상/폰트가 토큰을 우회하고 있지 않은가
- 결과: ✅ 준수 / ⚠️ 일부 우회 / ❌ 미적용

#### 6-2. AI Slop 탐지
`MODULE_ROOT[frontend-design]/references/ai-slop-blacklist.md`를 직접 읽어 검사합니다. 참조가
없으면 축약 native fallback만 실행하고 전체 블랙리스트 커버리지를 `UNVERIFIED`로 남깁니다.
- 10항목 블랙리스트 grep/시각 확인
- Hard Rejection 7개 확인 → 발견 시 FAIL
- 과사용 폰트(Inter, Roboto 등) 프라이머리 사용 여부

#### 6-3. UI/UX 9영역 채점
`MODULE_SKILL[ui-ux-auditor]`에서 직접 읽은 채점 방법론을 적용합니다. 해석 실패 시 위
native fallback을 사용하고 `source: native-fallback`을 표시합니다.
- 9영역 각각 0-10 채점
- 가중 총점 → A~F 등급
- 5.0 미만 → CONDITIONAL, Hard Rejection 발견 → FAIL

#### 등급 영향
- Phase 6 등급 A~B → 다음 Phase로 진행
- Phase 6 등급 C → **CONDITIONAL** (디자인 개선 권장)
- Phase 6 등급 D~F 또는 Hard Rejection → **FAIL** (디자인 재작업 필요)
- design-system.md 미감지 → 건너뜀 (등급에 영향 없음)

### Phase 7: 보안 검증

**항상 실행.** `MODULE_ROOT[code-reviewer]/references/security-audit.md`를 직접 읽고 인프라 우선
감사 계약을 적용합니다. 모듈 또는 참조가 없으면 위 한정된 보안 fallback을 실행하며, 실행하지
못한 영역을 `NOT RUN`으로 남깁니다.

> 런타임의 보안 change review와의 관계: change review는 현재 변경 집합을 보강할 뿐입니다.
> 이 Phase는 전체 코드베이스 + 안전하게 마스킹된 이력 검사 + 의존성 감사라 대체되지 않습니다.
> 같은 세션의 change-review 발견이 있으면 7-3에 병합하고 동일 diff는 다시 스캔하지 않습니다.

See [verify-protocol.md](references/verify-protocol.md) — Phase 7

#### 7-1. 시크릿 탐지 (Secret Archaeology)
- 현재 코드와 이력에서 하드코딩 시크릿 후보의 **경로·줄·마스킹된 지문만** 수집
- 비밀값 원문을 출력하는 raw grep과 `git log -p` 금지
- .env 파일 커밋 이력 확인
- scanner 부재나 미실행 범위는 `NOT RUN`/`UNVERIFIED`로 기록

#### 7-2. 의존성 공급망 (Supply Chain)
- `npm audit` / `pip-audit` / `trivy` 실행 (설치된 도구 사용)
- Critical/High CVE 탐지
- Lock 파일 커밋 여부
- 결과: 🔴 Critical CVE 수 / 🟠 High CVE 수

#### 7-3. OWASP Top 10 코드 스캔
- SQL Injection, XSS, Command Injection, Path Traversal, SSRF, CSRF 패턴 Grep
- `validate-code` 훅보다 넓은 범위 (훅은 3개 패턴, 여기서는 전체 OWASP)
- 인증/권한 체계 확인 (미인증 엔드포인트 탐지)
- Rate Limiting 존재 여부

#### 7-3a. API 직접 호출·서버 검증 (런타임 감리)

`MODULE_ROOT[code-reviewer]/references/security-audit.md`의 `API 직접 호출·서버 검증 계약`을
대상 API에 매핑한다. Phase 3/4 및 api-tester/Minos의 같은 버전·환경·조건 실행 증거를 재사용하고,
누락 사례는 기존 API 테스트 하네스로 실행한다. 정적 패턴 검색·인증 여부·UI 테스트만으로 통과시키지 않는다.
계약 ID별 정상 대조군, 계정 간 접근, 변조 요청, 거부 응답, 저장/상태/부수 효과 증거를 보고서에 포함한다.
우회 또는 금지된 저장/효과 재현은 이 게이트 `FAIL`이며 최종 PASS를 금지한다. 미실행은 `NOT RUN`으로
남겨 최종 결과를 최대 `CONDITIONAL`로 제한한다(다른 FAIL은 유지). 해당 API가 없으면 근거 있는 `N/A`다.
이 제한은 점수 합산 및 Healer 재검증 후에도 적용한다. 참조 누락은 기존 fallback으로 확인 가능한
증거만 수집하고 계약 전체를 검증했다고 주장하지 않는다.

#### 7-4. STRIDE 위협 요약
- Spoofing / Tampering / Repudiation / Info Disclosure / DoS / Elevation
- 각 위협별 현재 대응 상태: ✅ 대응 / ⚠️ 부분 / ❌ 미대응
- 미대응 위협에 대한 권고 1줄씩

#### 등급 영향
- 🔴 Critical 1건 이상 → **FAIL** (보안 수정 필수)
- 🟠 High만 있고 Critical 없음 → **CONDITIONAL**
- 🟡 Medium 이하만 → PASS에 영향 없음 (권고만)

### Phase 8: 도메인사전 감리

`docs/domain-dictionary.md`가 있는 경우만 실행. 없으면 자동 건너뜀.

> 도메인사전(Ubiquitous Language)이 코드/문서에 일관되게 적용됐는지 검증합니다.
> Phase 1 정적 검증과 다른 점: Phase 1은 "기능 구현" 중심, Phase 8은 "용어 일관성" 중심.

#### 8-1. 영문 식별자 준수

사전의 각 핵심 용어가 코드의 식별자(클래스/함수/변수/타입명)에서 정확히 사용되는지:
- 사전: `Cart` (영문 식별자: `cart`)
- 코드: `class Cart`, `const cart`, `cartService` → ✅
- 코드: `class Basket`, `const bag` → ❌ 금지 표현 사용
- 결과: ✅ 준수 / ⚠️ 일부 위반 (N건) / ❌ 다수 위반

#### 8-2. 금지 표현 검출

사전의 "금지 표현" 섹션에 등재된 용어가 코드/문서/주석에 사용되었는지 Grep:
- 금지: `~~basket~~`, `~~bag~~` (Cart로 통일)
- 검출 시 보고: 파일:라인, 권장 대체 용어
- 결과: ✅ 클린 / ❌ N건 검출

#### 8-3. UI 한글 표기 일치

사전이 정의한 한글 표기와 UI 라벨/메뉴/메시지가 일치하는지:
- 사전: `Cart = 장바구니`
- UI: `"장바구니에 담기"` → ✅
- UI: `"쇼핑백 추가"` → ❌ 사전 위반
- 검출 도구: i18n 파일, JSX/TSX 문자열 리터럴 Grep
- 결과: ✅ 일치 / ⚠️ 일부 불일치 (N건)

#### 8-4. 사전 미등재 신규 식별자

코드에 새로 등장한 도메인 식별자가 사전에 등재되어 있는지:
- 코드: `class Voucher` (사전에 없음)
- 결과: ⚠️ 신규 식별자 N개 — 사전 갱신 권장 (또는 도메인 외 기술 용어로 분류)

#### 등급 영향
- Phase 8 8-1, 8-2, 8-3 모두 통과 → 다음 단계로 진행
- 8-2 (금지 표현 검출) 5건 이상 → **CONDITIONAL** (용어 통일 작업 필요)
- 8-1, 8-3 다수 위반 (전체 코어 용어의 30% 이상) → **CONDITIONAL**
- 사전 자체가 없음 → 건너뜀 (등급에 영향 없음)
- Healer 분류: 대부분 자동 수정 가능 (rename), 단 의미 변경은 사람 판단 필요

---

## 검증 보고서

**Archive 기존 보고서:** `<planning_dir>/verify-report.md`가 이미 존재하면:
```
1. <planning_dir>/archive/ 디렉토리 생성 (없으면)
2. 기존 파일 → <planning_dir>/archive/verify-report-{YYYY-MM-DD-HHMM}.md 로 이동
```

메인 컨텍스트만 기존 보고서를 archive하고 Phase 0~7 결과를 합쳐
`<planning_dir>/verify-report.md`를 작성합니다. 읽기 전용 작업자는 이 경로를 수정하지 않습니다.

### 보고서 구조

```markdown
# Argos 검증 보고서

## 요약
- CPS 추적성: ✅/⚠️ CONDITIONAL/ℹ️ 건너뜀
- 전체 충족률: {N}%
- 빌드: ✅/❌
- 테스트: {passed}/{total}
- API 일치: {matched}/{total}
- QA 통과: {passed}/{total}
- 완료 기준: {proved}/{total} proved (장부 불일치 {n}건) 또는 건너뜀
- 도면 매칭: {matched}/{total} 노드
- 디자인 준수: {등급} ({총점}/10) 또는 건너뜀
- 보안: 🔴{N} 🟠{N} 🟡{N}; 미실행 영역이 있으면 NOT RUN/UNVERIFIED

## Module Coverage
| 모듈 | 해석 경로 | 적용 상태 | 미실행·fallback 범위 |
|------|-----------|-----------|----------------------|
| {name} | {absolute path 또는 없음} | module/native-fallback/NOT RUN | {coverage gap} |

## Phase 0: CPS 추적성 검증
{Problem→Solution 추적 + 에코시스템→섹션 커버리지 + Problem→섹션 매핑 결과}
(CPS 섹션 미감지 시: "레거시 계획 — 건너뜀")

## Phase 1: 정적 검증
{기능 검증 + 품질 검증 결과 테이블}

## Phase 2: 런타임 검증
{빌드/테스트/E2E 결과 테이블}

## Phase 3: API 일치 검증
{endpoint 대조 테이블}

## Phase 4: QA 시나리오 검증
{통과율 테이블 + 실패 항목}

## Phase 4A: 완료 기준 이행 감리
{AC별 감리 판정 + 장부와 다른 행 + 미이행 AC 목록}

## Phase 5: 프로세스 도면 검증
{노드 매칭 테이블 + 누락 노드}

## Phase 6: 디자인 준수 검증
{디자인 토큰 준수율 + AI Slop 탐지 결과 + 9영역 스코어카드}
(design-system.md 미감지 시: "UI 없음 — 건너뜀")

## Phase 7: 보안 검증
{시크릿 탐지 + 의존성 CVE + OWASP 스캔 + STRIDE 요약}

## 누락 항목 목록
{전체 Phase에서 ❌인 항목 통합}
```

### 판정 기준

| Grade | 조건 | 판정 |
|-------|------|------|
| **PASS** | 전체 Phase 통과, 누락 0 | 준공 승인 |
| **CONDITIONAL** | 필수 기능 통과, 일부 경고 | 조건부 승인 |
| **FAIL** | 필수 기능 미구현 또는 빌드 실패 | 재시공 필요 |

필수 모듈을 해석하지 못했는데 fallback도 실행하지 않은 Phase는 PASS 근거가 될 수 없습니다.

---

## 결과 보고 및 자동 수정

검증 결과를 사용자에게 표시한 후:

- **PASS**: 준공 승인, 다음 단계 안내
- **CONDITIONAL/FAIL**: 누락 항목을 **확인 없이 바로 수정** 시도 → 수정 후 해당 Phase만 재검증
  - 수정-재검증은 항목당 **최대 2라운드**까지만. 2라운드 내 미해결이면 자동 수정을 멈추고 "수동 확인 필요"로 강등한다 (무한 수정 루프 방지)
  - 자동 수정 불가능한 항목, 그리고 라운드 소진으로 강등된 항목을 리스트로 보고 ("수동 확인 필요")
  - 라운드 소진 미해결 항목이 남으면 최종 판정을 PASS로 올리지 않는다 (소진=미완, 통과 아님)

---

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--phase N` | 특정 Phase만 실행 (0~7) | 전체 |
| `--skip-build` | Phase 2 빌드 건너뜀 | false |
| `--skip-e2e` | Phase 2 E2E 건너뜀 | false |
| `--report-only` | 기존 보고서 표시만 | false |

---

## 연관 스킬

| 스킬 | 역할 | 연결 |
|------|------|------|
| zephermine | 설계 산출물 생성 | 검증 대상 (spec, api-spec, qa-scenarios, flow-diagrams) |
| flow-verifier (source-only module) | 프로세스 도면 검증 | Phase 5에서 `MODULE_SKILL` 직접 읽기 |
| agent-team (포세이돈) | 구현 수행 | 검증 전 선행 단계 (젭마인 산출물 기반) |
| daedalus (다이달로스) | 구현 수행 | 검증 전 선행 단계 (젭마인 없이 직접 진행) |
| minos | Playwright 실사 테스트 | 검증 후 후행 단계 |
| code-reviewer (source-only module) | 코드 품질·보안 감사 계약 | Phase 7에서 `MODULE_ROOT` 참조 직접 읽기. 별도 보고서가 이미 있으면 발견만 병합 |

---

## 다음 단계 안내

```
✅ 아르고스 감리 완료! (결과: {PASS/CONDITIONAL/FAIL})

👉 다음 단계 (선택):
  /minos          → Playwright 실사 테스트 (아직 안 했다면)
  /commit              → 변경사항 커밋
  /wrap-up             → 세션 요약 + MEMORY.md 업데이트
```
