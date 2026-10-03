---
name: design-plan
description: >
  아프로디테 디자인 오케스트레이터. 사이트 벤치마크 해부, 사용자 과업·메시지·CTA·신뢰·모바일
  변환을 담은 Experience Contract, 실제 렌더 방향 탐색, DESIGN.md, 구현, 미학·UX·성능·접근성
  검증과 학습까지 프론트 디자인 전 과정을 수행합니다. /aphrodite, 아프로디테, 디자인 계획,
  프론트 디자인 요청에 사용합니다.
---

# Aphrodite — Experience-led Frontend Design

아프로디테는 색과 컴포넌트를 고르는 스킬이 아닙니다. 사용자가 이해하고 행동하고 신뢰하고
실패에서 회복하는 흐름을 아름다운 시각 언어로 구현하는 디자인 하네스입니다.

## Quick Start

```text
/aphrodite
/aphrodite --plan-only
/aphrodite --review-only
/aphrodite --benchmark <URL-or-file>
/aphrodite --product-design
/aphrodite --stitch
```

## 내부 소스 모듈 해석 계약 (필수)

`frontend-design`, `mermaid-diagrams`, `ui-ux-auditor`, `web-design-guidelines`는 모든 관련 실행에서
사용하는 핵심 source-only 내부 모듈입니다. `design-system-starter`, `stitch`, `skill-evolve`,
`autoresearch`도 등록 스킬을 호출하는 것이 아니라, 해당 선택 경로가 실제로 요청됐을 때만 직접
읽는 조건부 source-only 모듈입니다. 각 이름에 대해 해석된 `SKILL.md` 절대경로를
`MODULE_SKILL[name]`, 그 부모 디렉터리를 `MODULE_ROOT[name]`으로 기록합니다. 조건부 모듈은
다음 경계에서만 해석합니다.

- `design-system-starter`: 사용자가 상세 디자인 시스템 scaffold를 명시적으로 요청했을 때
- `stitch`: `--stitch` 또는 명시적인 Stitch 실행 요청이 있을 때, Phase 5 진입 직전
- `skill-evolve`: Phase 7에서 전역 규칙 변경을 사용자가 명시적으로 승인한 뒤
- `autoresearch`: 승인된 `skill-evolve` 절차가 대조 실험을 요구할 때

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

이 과정은 모듈 읽기이지 스킬 호출이 아닙니다. `/frontend-design`, `/mermaid-diagrams`,
`/ui-ux-auditor`, `/web-design-guidelines`, `/design-system-starter`, `/stitch`, `/skill-evolve`,
`/autoresearch`를 호출하거나 스킬 레지스트리에 등록됐다고 가정하지 않습니다. 프로젝트·활성 루트
파일도 없고 카탈로그의 정확한 행·`읽을 경로`·필수 참조 중 하나라도 없으면 완료 증거의
`Module Coverage`에 경로와 이유를 기록하고 다음 한정된 native fallback을 사용합니다.
fallback도 실행할 수 없는 검사는 `NOT RUN`,
`UNVERIFIED`, 또는 `BLOCKED`로 남기며 통과로 바꾸지 않습니다. 요청되지 않은 조건부 모듈은
`NOT REQUESTED`이며 완료 누락으로 계산하지 않습니다.

| 모듈 | 한정된 native fallback |
|------|------------------------|
| `frontend-design` | 루트 `DESIGN.md`, Experience Contract, 프로젝트 manifest와 기존 컴포넌트만 사용해 승인 범위를 구현. recipe·anatomy 의존 결정은 `UNVERIFIED` |
| `mermaid-diagrams` | `flowchart TD`, 안정적인 노드 ID, 인용된 label, 명시적 edge로 사이트맵을 작성. renderer가 없으면 문법 검증은 `NOT RUN` |
| `ui-ux-auditor` | Phase 6-4의 항목을 실제 스크린샷 우선으로 점검하고 점수 대신 관찰 근거와 미관찰 범위를 보고 |
| `web-design-guidelines` | 키보드·포커스·레이블·상태 알림·reduced-motion만 점검하고 전체 가이드라인 준수는 `NOT RUN` |
| `design-system-starter` | `DESIGN.md`에서 DTCG를 파생하고 scaffold 확장은 `NOT RUN`으로 기록. 정본은 계속 `DESIGN.md` |
| `stitch` | 명시 요청이면 Stitch 단계는 `BLOCKED` 또는 `NOT RUN`으로 보고하고 원격 산출물을 꾸며내지 않음. 사용자가 로컬 대체를 허용한 범위만 네이티브 구현 작업자로 계속 |
| `skill-evolve` | 전역 진화 단계만 `NOT RUN`으로 남기고 Phase 0~6 결과는 보존. 자체 판단으로 전역 파일을 수정하지 않음 |
| `autoresearch` | 비교 실험만 `NOT RUN`으로 남기며 단일 결과를 개선 증거로 승격하지 않음 |

## 성공 정의

다음 네 가지가 함께 통과해야 완료입니다.

1. **이해**: 첫 접촉에서 목적, 핵심 메시지, 다음 행동을 알 수 있음
2. **사용**: 주요 과업, 상태, 오류 회복, 모바일 흐름이 실제로 작동함
3. **아름다움**: 구도, 비례, 리듬, 타이포, 재질, 모션에 하나의 의도가 있음
4. **품질**: 접근성, 성능, 반응형, 구현 정합성이 기준을 충족함

금지 규칙을 지켰다는 사실만으로 아름답다고 판정하지 않습니다. 산출물을 모두 만들었다는 사실만으로
좋은 UX라고 판정하지 않습니다.

## 정본과 역할 경계

| 정본·담당 | 소유하는 결정 |
|---|---|
| `DESIGN.md` | 색, 타이포, 간격, 표면, 컴포넌트 외관, 모션 원칙 |
| Experience Contract | 과업, 메시지, CTA, 신뢰, 상태, 모바일 변환 |
| Layout Blueprint | 시각 탐색 전에 검증한 저충실도 와이어프레임, 페이지별 블록 순서, 그리드, anatomy, 첫 뷰포트 |
| Aphrodite | UX 행동 명세, 상태 표현, 시각 구현, 렌더 비평 |
| 앱 구현 파이프라인 | 라우팅, 상태 관리, 데이터, API, 비즈니스 로직 |
| Product Design | 승인된 계약을 인터랙티브 프로토타입으로 실행하는 선택적 Codex 어댑터 |
| Stitch | 승인된 계약을 실행하는 선택적 생성 백엔드와 원격 상태 |

아프로디테는 비즈니스 로직을 직접 소유하지 않지만, 사용자가 보는 loading·empty·error·success,
행동 피드백, 오류 회복의 설계 책임은 가집니다. 구현 담당자는 이 계약을 실제 기능에 연결합니다.

## Phase Map

```text
Phase 0  Route        입력·기존 자산·벤치마크 유무 판별
Phase 1  Discover     사용자·과업·근거·레퍼런스 확보
Phase 2  Architect    IA + 과업 흐름 + 메시지·CTA·신뢰 + 상태 + 와이어프레임 판단 게이트
Phase 3  Explore      실제 렌더 3방향 탐색 + 시각 시스템 확정
Phase 4  Contract     검증된 레이아웃 정교화·모바일 변환·Experience Contract 고정
Phase 5  Build        계약 컴파일 → 구현 → 렌더 비평 → 구조/변형 수정
Phase 6  Validate     미학·과업·벤치마크·접근성·성능 검증
Phase 7  Evolve       성공·실패 근거 적립과 검증된 원리 승격
```

## Phase 0: Route

### 0-0. Codex Product Design 추천 게이트

현재 요청이 실제 렌더 방향 탐색이나 프론트 구현을 포함하고 런타임이 Codex이면, 디자인 결정을
시작하기 전에 현재 세션이 노출한 플러그인·스킬·도구 메타데이터와 지원되는 Codex CLI의 다음
읽기 전용 조회를 교차 확인합니다.

```bash
codex plugin marketplace list --json
codex plugin list --json
codex plugin list --available --json
```

첫 명령은 구성된 marketplace, 두 번째는 설치된 plugin, 세 번째는 설치 가능한 marketplace 후보를
확인합니다. CLI가 해당 옵션을 지원하는지는 먼저 `--help`로 확인합니다. marketplace가 0개이거나
정확한 `PLUGIN@MARKETPLACE` selector가 확인되지 않으면 `ABSENT`가 아니라 `UNKNOWN`입니다.
`Product Design`이라는 표현은 exact selector가 검증되기 전까지 사용자가 원하는 capability label일
뿐, 공식·내장 plugin 이름이라고 단정하지 않습니다. 캐시 디렉터리나 검색 결과만으로 설치·활성을
판정하지 않습니다. 공식 OpenAI 문서상 IDE extension은 plugin을 지원하지 않으므로 그 표면은
`UNSUPPORTED`입니다. 지원되는 ChatGPT desktop 또는 Codex CLI에서는 Plugins tab이나 `/plugins`
browser를 사용할 수 있습니다. `--plan-only`, `--review-only`, 명시적인 `--stitch` 경로에서는 이
추천을 생략합니다.

상태는 다음 다섯 가지 중 하나로 기록합니다.

| 상태 | 동작 |
|---|---|
| `READY` | exact selector가 설치 목록에 있고 현재 세션에 capability가 노출됨. Phase 3·5의 선택 어댑터로 사용 |
| `ABSENT` | exact selector가 available 목록에 있지만 installed 목록에 없음. 같은 요청에서 정확히 한 번만 설치를 추천 |
| `RESTART_REQUIRED` | 설치는 됐지만 현재 세션에 노출되지 않았음을 한 번 알리고 새 세션 또는 로컬 계속 진행을 제안 |
| `UNKNOWN` | marketplace·selector·조회 결과 중 하나가 확인되지 않음. 미설치라고 단정하거나 설치를 묻지 않고 로컬 경로를 제안 |
| `UNSUPPORTED` | 현재 표면이 plugin을 지원하지 않음. 설치 추천 없이 로컬 경로를 사용 |

`ABSENT`이면 exact `PLUGIN@MARKETPLACE`, marketplace source, 확인된 snapshot/version, 설치로
생기는 skill·MCP·hook·설정 변경을 먼저 보여주고 “이 plugin을 설치할까요? 설치하지 않아도 로컬
경로로 계속할 수 있습니다.”처럼 이점과 폴백을 함께 제시합니다. 그 정확한 제안에 대한 직접 답변인
`설치해`, `좋아`, `알겠음`만 설치 동의로 인정합니다. exact selector를 보여주기 전의 일반적인
동의나 단순 확인 응답은 설치 권한이 아닙니다. 동의 전에는 plugin 설치, marketplace 추가·upgrade,
설정 변경, 다른 CLI나 전역 스킬 디렉터리로의 복사·동기화를 실행하지 않습니다. marketplace 추가가
필요하면 plugin 설치와 분리해 대상 source와 변경을 제시하고 별도 승인을 받습니다. 거절하거나 로컬
계속 진행을 선택하면 해당 요청에서는 다시 묻지 않고 로컬 어댑터로 진행합니다. 설치를 승인해도 실제
설치 성공과 새 세션의 노출을 각각 확인하기 전에는 `READY`나 사용 완료로 보고하지 않습니다.

`--product-design`은 가용성 확인과 어댑터 선호를 명시할 뿐 설치 동의로 간주하지 않습니다.
Product Design은 `DESIGN.md`, Experience Contract, Layout Blueprint를 소비하는 실행 엔진이며
시각 방향이나 UX 정책을 다시 결정하지 않습니다.

### 0-1. 기존 자산 확인

다음 순서로 확인합니다.

```text
DESIGN.md
docs/design-refs/*-experience-*.md
docs/design-refs/*-benchmark-*.md
docs/design-refs/*-direction-*.md
docs/design-refs/*-layout-*.md
design-system.md / design-tokens.json
tailwind.config.* / theme.* / CSS variables
docs/plan/*/spec.md                     (시스템 역할 표 = 역할 ID 정본)
docs/plan/*/operation-scenarios.md      (RBAC 매트릭스 + 거부 동작)
```

젭마인 산출물이 있으면 역할 ID와 거부 동작을 그대로 물려받고 여기서 새 역할명을 만들지 않습니다.
없으면 역할 구분 없는 단일 화면으로 진행하되, 화면에 관리 기능이 보이면 역할 존재 여부를 한 번 확인합니다.

`DESIGN.md`가 있다는 이유만으로 Phase 1~5를 건너뛰지 않습니다. 다음을 분류합니다.

- brief·과업·벤치마크·화면 구조가 같음: 변경 범위만 delta audit
- 위 항목 중 하나가 바뀜: 관련 Phase부터 재실행
- 기존 결과가 못생기거나 UX 문제가 있음: Phase 1의 가정과 Phase 3의 방향부터 재검토
- `--review-only`: Phase 6만 실행하되 필요한 정본이 없으면 신뢰도 제한을 보고

### 0-2. 입력 경로 선택

| 조건 | 경로 |
|---|---|
| URL·스크린샷·영상·HTML 벤치마크 있음 | reference-driven |
| 벤치마크 없음, 신규 디자인 | product-derived |
| 승인된 디자인의 국소 변경 | delta |
| Codex + Product Design `READY` | 위 경로로 설계 확정 후 Product Design adapter |
| Stitch 프로젝트 | 위 경로로 설계 확정 후 Stitch adapter |

벤치마크가 있으면 [site-benchmark-guide.md](references/site-benchmark-guide.md)의 Gate A~F를
통과하기 전 구현하지 않습니다. 모든 항목을 관찰하되 전부 복제하지 않고 Adopt·Adapt·Avoid로
판정합니다.

## Phase 1: Discover

### 1-1. 디자인 브리프

요구에 이미 있는 내용은 다시 묻지 않습니다. 빠진 것만 확인하고
`docs/design-refs/YYYY-MM-DD-brief-{slug}.md`에 저장합니다.

- 무엇을 만드는가
- 누가 어떤 상황에서 사용하는가
- 최우선 과업과 완료 조건은 무엇인가
- 사용자가 망설이거나 불신하는 지점은 어디인가
- 기술·콘텐츠·브랜드·접근성 제약은 무엇인가
- 관찰 가능한 성공 기준은 무엇인가

요구사항 자체가 불명확하면 `zephermine`에 인계합니다. 아프로디테는 디자인에 필요한 경험 가정을
확정합니다.

### 1-2. 벤치마크와 레퍼런스

레퍼런스가 있으면 다음 파일을 순서대로 읽습니다.

1. [reference-capture-guide.md](references/reference-capture-guide.md) — URL·스크린샷·영상·HTML 증거 확보
2. [site-benchmark-guide.md](references/site-benchmark-guide.md) — 구조·메시지·반응형·품질 해부

산출물은 `docs/design-refs/YYYY-MM-DD-benchmark-{slug}.md`입니다. 색·폰트만 기록한 분석은
실패입니다. 헤더, 핵심 메시지, 섹션 순서, CTA, 신뢰, 상태, 데스크톱→모바일 변환을 포함합니다.

레퍼런스가 없으면 제품 세계의 실물·도구·유물·어휘에서 색, 구조, 카피, 미디어의 근거를 유도합니다.
카테고리 클리셰를 제품 근거로 착각하지 않습니다.

## Phase 2: Architect the Experience

페이지보다 사용자 과업을 먼저 설계합니다.

### 2-1. 페이지·내비게이션

- 화면·페이지 목록과 각 페이지의 단일 임무
- 전역 내비게이션, 2차 내비게이션, 페이지 내 앵커
- primary action과 현재 위치 신호
- 페이지가 3개 이상이면 `MODULE_SKILL[mermaid-diagrams]`를 직접 읽은 문법으로 사이트맵 생성

산출물: `docs/design-refs/YYYY-MM-DD-sitemap-{slug}.md`

### 2-2. 과업·메시지 흐름

기능형 화면은 `입력→처리→진행 상태→결과→오류 회복`, 표현형 화면은
`약속→설명→증거→신뢰→행동` 순서를 설계합니다.

- 정상 경로만이 아니라 loading·empty·error·success·permission·stale 상태를 정의
- CTA의 정확한 문구, 목적지, 등장·반복 시점 정의
- 사용자의 불안 직전에 검증 가능한 신뢰 근거 배치
- 근거 없는 고객 수치·후기·배지 생성 금지

### 2-3. Experience Contract 초안

[experience-contract-guide.md](references/experience-contract-guide.md)의 필수 템플릿으로
`docs/design-refs/YYYY-MM-DD-experience-{slug}.md`를 작성합니다. 벤치마크 모드면 근거 파일과
Adopt·Adapt·Avoid를 포함합니다.

### 2-4. Interface Mode

핵심 행동을 기준으로 다음 중 하나를 고릅니다.

| Mode | 우선 설계 |
|---|---|
| Data Instrument | 검색·KPI·변화·표·anomaly |
| Faceted Directory | 검색·필터·비교·결과 |
| Agent Workbench | 지속 pane·task·terminal·review 상태 |
| Waiting State | 단계·진행·취소·복구 |
| Effect Stage | bounded preview·설정·코드 |
| Expressive Landing | 메시지·신뢰·전환·signature 장면 |

기능형 5종은
`MODULE_ROOT[frontend-design]/references/coder-interface-pattern-playbook.md`를
읽고 정보 구조와 효과 예산을 먼저 고정합니다.

### 2-5. 저충실도 와이어프레임 판단 게이트

새 화면을 설계하거나 주 과업·정보 구조를 바꿀 때, Phase 3의 색·이미지·그림자·재질·모션을 고르기 전에
`MODULE_ROOT[frontend-design]/references/layout-block-anatomy.md`를 읽고
`docs/design-refs/YYYY-MM-DD-layout-{slug}.md`에 블록 순서와 판단 근거를 남기고, 대표 화면의
데스크톱·모바일 와이어프레임을 **실제 볼 수 있는 파일**로 만듭니다. 정적 화면은 SVG,
상태·화면 전환을 확인할 때는 HTML/CSS로 그립니다. HTML이면 각 뷰포트의 스크린샷을 남기고,
캡처 도구가 없으면 직접 볼 수 있는 SVG를 산출합니다. ASCII는 빠른 초안으로 쓸 수 있지만
최종 와이어프레임을 대신하지 않습니다. 산출물 경로를 Layout Blueprint에 연결합니다.
브랜드 색·사진·그림자·장식으로 미완성 구조를 가리지 않습니다.
이미지 자리만 빈 상자로 표시할 수 있으며, 핵심 메시지·탐색 라벨·CTA·가격처럼 사용자의 판단에
필요한 내용은 실제 문구나 검증 가능한 샘플로 적습니다.
검색창·버튼·카드·내비게이션·미디어 자리 등은 텍스트와 단색 도형을 조합해 그립니다.
요소마다 별도 그림 파일을 준비하지 않습니다. 실제 사진과 브랜드 자산은 시각 디자인 단계에서
근거와 출처를 확인해 적용합니다.
이미 검증한 화면의 국소 변경은 영향받는 부분만 다시 판단하고 그 근거를 기존 Blueprint에 덧붙입니다.

와이어프레임은 보기 좋은 화면을 고르는 자료가 아니라 다음 결정을 내리는 자료입니다.

| 기준 | 통과 질문 |
|---|---|
| 위계 (Hierarchy) | 색 없이도 처음 볼 정보와 주 행동이 분명한가? |
| 구조 (Structure) | 묶음과 순서가 사용자의 과업·사고 순서와 맞는가? |
| 흐름 (Flow) | 진입→행동→완료와 실패→복구를 화면 사이에서 따라갈 수 있는가? |
| 일관성 (Consistency) | 같은 의미의 요소와 행동을 같은 방식으로 표현하는가? |
| 명료성 (Clarity) | 설명을 듣지 않아도 라벨, 상태, 다음 행동을 이해하는가? |

각 기준에 대해 화면에서 관찰한 근거와 수정할 결정을 Layout Blueprint에 남깁니다. 하나라도
불명확하면 과업 흐름·정보 순서·문구·CTA를 고쳐 다시 확인합니다. 시각 시안에서 주 행동이
처음 생겼다면 와이어프레임의 흐름이 아직 완성되지 않은 것입니다.
역할이 둘 이상이면 `spec.md` 시스템 역할 표의 `화면` 열에 따라 공용 화면의 권한 차이 또는 별도
역할 화면을 이 단계부터 그립니다. 주요 상태도 같은 구조 판단에 포함합니다. 이 게이트를 통과한
뒤에만 Phase 3의 시각 방향을 탐색합니다.

## Phase 3: Explore Direction and System

### 3-1. 실제 렌더 방향 탐색

[render-critique-loop.md](references/render-critique-loop.md)의 필수 조건에 해당하면 텍스트 카드만
제시하지 않고 서로 다른 실제 화면 3안을 렌더합니다.

후보는 통과한 와이어프레임의 과업·주 행동·정보 순서를 입력으로 사용합니다. 후보가 그 결정을
바꾸면 해당 후보의 와이어프레임을 다시 검토하고 Phase 2-5 게이트를 통과시킵니다.

- 동일한 실제 카피·데이터·상태 사용
- 구성·위계·명도·타입·재질·모션 중 최소 4축 차이
- 데스크톱 대표 화면 + 모바일 핵심 화면 포함
- 스크린샷만 먼저 보고 이해·구도·리듬·제품성·신뢰·모바일을 비평

선택 결과와 탈락 이유를 각각 `direction`과 `critique` 파일에 저장합니다. 실제 렌더를 만들지 않은
경우 생략 근거를 기록합니다.

### 3-2. 시각 시스템

`MODULE_SKILL[frontend-design]`을 직접 읽고 다음 순서로 확정합니다.

1. 선택된 방향과 제품 근거
2. 맞는 스타일 레시피 1개 또는 제품 유도 방향
3. 지배색 1 + 액센트 1, 실제 대비
4. 한글 글리프를 실제 로드하는 폰트 시스템
5. 밀도·간격·라운드·표면·모션 예산
6. 기억에 남을 signature 요소 정확히 1개

색·폰트 DB는 폴백이지 디자인의 출발점이 아닙니다. 값과 근거를
[design-md-guide.md](references/design-md-guide.md) 스키마의 루트 `DESIGN.md`에 저장합니다.

## Phase 4: Contract the Layout and Behavior

### 4-1. Layout Blueprint

Phase 2-5에서 검증한 Layout Blueprint를 선택된 시각 방향과 대조하고 페이지별로 다음을
정교화합니다. 구조·주 행동이 바뀌면 Phase 2-5 게이트를 다시 실행합니다.

- 블록 순서와 각 블록이 답하는 사용자 질문
- 필수 요소, 잉크 위계, 강조 1개, CTA 문법
- 첫 뷰포트와 스크롤 중 밀도 변화
- 기능형 화면의 pane·표·필터·상태 위치
- 사용 가능한 scaffold와 적용 범위

산출물: `docs/design-refs/YYYY-MM-DD-layout-{slug}.md`

### 4-1-1. 역할별 화면 (Role Variants)

역할이 둘 이상이면 Phase 2-5에서 결정한 화면 처리를 아래 형식으로 상세화합니다. `spec.md` 시스템 역할 표의 `화면` 열이 처리 방식을 결정합니다.

| `화면` 열 | 산출물 | 내용 |
|---|---|---|
| 공용 권한차등 | 기본 Blueprint + **역할별 변형표** | 같은 블록 순서 위에서 요소별로 역할에 따른 노출을 고정 |
| 별도 화면 | **역할 전용 Blueprint** 별도 파일 | `docs/design-refs/YYYY-MM-DD-layout-{slug}-{role}.md`. 블록 순서·첫 뷰포트·과업을 처음부터 다시 설계 |

역할별 변형표는 요소 x 역할 격자이며, 값은 `operation-scenarios.md` 거부 동작과 같은 어휘를 씁니다.

| 요소 | superadmin | admin | operator | user | guest |
|---|---|---|---|---|---|
| 주문 삭제 버튼 | 표시 | 표시 | 숨김 | 숨김 | 숨김 |
| 금액 입력란 | 표시 | 읽기전용 | 읽기전용 | 숨김 | 숨김 |
| 관리 메뉴 | 표시 | 표시 | 표시 | 숨김 | 숨김 |

규칙:

- 값은 `표시` / `숨김` / `비활성` / `읽기전용` 중 하나입니다. `403`·`404 위장`은 화면이 아니라 라우팅 결과이므로 진입 차단 항목에만 씁니다.
- **숨김과 비활성을 구분합니다.** 숨김은 권한이 있다는 사실 자체를 감추고, 비활성은 존재를 알리되 막습니다. 어느 쪽인지 정하지 않으면 구현자가 임의로 고릅니다.
- 전권 역할(superadmin)은 모든 요소가 `표시`인 기준 화면이며 별도 변형표를 만들지 않습니다.
- 역할을 지웠을 때 **화면이 텅 비거나 CTA가 사라지는 경우**를 확인합니다. 그 역할에는 다른 진입점이나 빈 상태 문안이 필요하다는 신호입니다.
- 역할이 1개이거나 인증이 없으면 `NOT APPLICABLE: single role`로 기록하고 이 절을 생략합니다.

Experience Contract에는 `## System Roles`와 `## Role Variants` 절로 옮겨 적어 Phase 4-4 검증이 잡을 수 있게 합니다.

### 4-2. Responsive Transformation

데스크톱 요소마다 `retain/reorder/compress/collapse/defer/replace/sticky/remove` 중 하나와 이유를
Experience Contract에 기록합니다. `모바일은 1열 stack`만 있으면 실패입니다.

### 4-3. Web Motion Contract

브라우저에서 실행되는 signature motion, 스크롤 연동, 레이아웃 전환, 텍스트·SVG 모션이 있으면
[web-motion-contract.md](references/web-motion-contract.md)를 읽고 각 장면의 목적, trigger, engine,
fallback, cleanup, 검증 방법을 기록합니다. CSS transition·View Transitions·Scroll-driven
Animations를 우선하고, pin·snap·복잡한 timeline·DOM 재배치·텍스트 분할·SVG path가 실제로 필요할
때만 GSAP core, ScrollTrigger, Flip, SplitText, SVG plugin을 선택합니다. 프로젝트 manifest에 없는
dependency를 자동으로 추가하지 않습니다.

이 계약은 실시간 웹 UI만 다룹니다. Remotion, HyperFrames, BGM·SFX, MP4 렌더링, 영상용 storyboard는
Aphrodite의 범위 밖이며 `video-maker`로 인계합니다.

### 4-4. 계약 검증

Experience Contract를 완성하고 다음을 실행합니다.

```bash
python <DESIGN_PLAN_SKILL_DIR>/scripts/validate_experience_contract.py \
  docs/design-refs/YYYY-MM-DD-experience-{slug}.md
```

검증 실패 시 구현으로 넘어가지 않습니다. 이 스크립트는 완성도를 검사하며 아름다움과 사용성은
Phase 5~6의 실제 렌더로 검증합니다. `## System Roles`가 있고 `NOT APPLICABLE`이 아니면
`## Role Variants`도 함께 요구하며, 변형표가 `표시/숨김/비활성/읽기전용` 어휘를 쓰지 않으면 실패합니다.

## Phase 5: Build and Critique

### 5-1. 구현 전 소비 게이트

코드를 쓰기 전에 존재하는 다음 파일을 모두 읽습니다.

1. 루트 `DESIGN.md` 전체
2. 최신 brief·benchmark·experience·sitemap·direction·critique·layout
3. 선택된 style recipe와 Interface Mode playbook

Experience Contract의 `Prompt Contract`를 구현 지시로 사용합니다. `예쁘게`, `모던하게` 같은
소원으로 대체하지 않습니다.

### 5-2. 구현 어댑터

- Product Design: Phase 0에서 `READY`로 확인됐거나 승인된 설치 뒤 새 세션에서 노출이 확인됐을 때만
  사용합니다. Experience Contract의 Prompt Contract와 `DESIGN.md`를 입력으로 실제 방향 렌더와
  인터랙티브 프로토타입을 만들고, 결과는 Phase 5-4와 Phase 6의 동일한 비평·품질 게이트를 통과시킵니다.
- 로컬: 네이티브 구현 작업자가 `MODULE_SKILL[frontend-design]`의 계약을 직접 적용하여 기존
  스택과 컴포넌트 규칙에 맞게 구현. Product Design이 없거나 거절·확인 불가·재시작 대기이면 이 경로로 진행
- Stitch: 명시 요청이 있을 때 `MODULE_SKILL[stitch]` 전체를 직접 읽고 그 preflight·상태·검증
  계약을 적용합니다. 사용자 의도를 generate·edit·variants·loop·react 중 하나로 분류한 뒤 현재
  노출된 Stitch MCP capability를 직접 사용하며 `/stitch` 등록이나 고정 도구 이름을 가정하지 않습니다.
- Stitch loop: 해석된 `MODULE_ROOT[stitch]` 기준으로 사이트맵을 `.stitch/SITE.md` 실행 상태로 파생
- Stitch react: Stitch 결과를 기존 React 구조에 반영하되 프로젝트 manifest와 테스트를 우선

Stitch는 디자인 정책을 다시 결정하지 않습니다. 루트 `DESIGN.md`와 `docs/design-refs/`가 정본이고
`.stitch/`는 원격 ID·다운로드·재개 상태만 소유합니다. Stitch MCP나 필수 capability가 없으면 해당
경로를 `BLOCKED` 또는 `NOT RUN`으로 보고하며 원격 결과를 생성했다고 주장하지 않습니다.

### 5-3. 구현 로그

페이지·작업당 하나의 `docs/design-refs/YYYY-MM-DD-impl-log-{slug}.md`에 실제 Prompt Contract,
변경 범위, 보존 영역, 구현 중 계약 변경을 누적합니다.

### 5-4. Baseline-worthiness gate

첫 결과에서 바로 레이아웃·위계·카피를 고정하지 않습니다.

- 구조·메시지·모바일 흐름이 좋음: 보존 영역 선언 후 변수 1~2개 variants
- 구조·메시지가 나쁨: 섹션 순서·레이아웃·카피·CTA·신뢰 위치까지 수정 후 재렌더

[render-critique-loop.md](references/render-critique-loop.md)를 따르고 실제 스크린샷을 봅니다.
HTML 정적 검사만으로 시각 충실도를 선언하지 않습니다.

### 5-5. Product Design 유무 대조

사용자가 유무 비교를 요청했거나 exact Product Design adapter를 처음 도입해 기준선이 없으면
[render-critique-loop.md](references/render-critique-loop.md)의 Adapter Comparison Contract를
실행합니다. 로컬과 Product Design 후보에 동일한 brief, Experience Contract, `DESIGN.md`, 실제
카피·데이터·상태, viewport·theme를 제공합니다. 과업 완수, 위계, 방향 차별성, 반응형 변환,
접근성, 성능, 기존 코드 적합성을 실제 렌더와 실행 증거로 비교합니다. plugin 결과라는 이유만으로
승자로 정하지 않습니다.

adapter가 `READY`가 아니면 가상 결과를 만들지 않고 비교를 `NOT RUN`으로 남기며 로컬 구현을
계속합니다. 결과는 `docs/design-refs/YYYY-MM-DD-adapter-comparison-{slug}.md`에 기록합니다.

## Phase 6: Validate the Experience

### 6-0. Antigravity `/browser` 실행 경계

Antigravity에서 사용자가 `/browser`를 명시적으로 열었거나 현재 세션에 네이티브 browser capability가
노출돼 있으면 URL 탐색, 실제 화면 관찰, 과업 경로 실행에 우선 사용합니다. 이 스킬이 slash command를
프로그램적으로 호출한다고 가정하지 않습니다. 관찰 결과는 동일한 viewport·theme·상태와 스크린샷 근거로
Experience Contract 및 아래 게이트에 연결합니다. 브라우저 capability가 없으면 사용 가능한 로컬 렌더·
스크린샷 경로로 축소하고, 관찰하지 못한 항목을 `PASS`로 처리하지 않습니다.

### 6-1. Benchmark conformance

벤치마크 모드면 [site-benchmark-guide.md](references/site-benchmark-guide.md)의 Gate E~F를 실행합니다.
픽셀 유사성이 아니라 Adopt·Adapt 결정, 데스크톱·모바일 변환, 제품 적용 근거를 대조합니다.

### 6-2. 미학 비평

네이티브 시각 비평 작업자가 [render-critique-loop.md](references/render-critique-loop.md)의
비평 계약을 사용해 다음을 실제 렌더로 평가합니다.

- 시각 논지와 제품 고유성
- 메시지·CTA·신뢰의 위계
- 구도·비례·여백·밀도·리듬
- 타이포·색·재질·모션의 일관성
- signature 장면과 주변 요소의 절제
- 모바일에서의 재구성 품질

AI Slop이 없다는 것만으로 통과시키지 않습니다.

### 6-3. 과업·상태 검증

주 과업을 시작→진행→완료와 실패→복구 두 경로로 실행합니다. 사이트맵, Experience Contract,
실제 내비게이션과 상태가 일치해야 합니다.

### 6-4. 품질 검증

1. `MODULE_SKILL[ui-ux-auditor]`를 직접 읽어 반응형, 다크모드, 접근성, 성능, 폼, 내비,
   타이포, 모션, AI Slop 감사
2. `MODULE_SKILL[web-design-guidelines]`를 직접 읽어 Web Interface Guidelines 감사
3. 데스크톱·모바일 × 지원 테마 스크린샷 관찰
4. 키보드·포커스·레이블·상태 알림·reduced-motion 확인
5. 실제 이미지·폰트·영상·스크립트로 성능 측정
6. `DESIGN.md` lint는 대화형일 때만 보조 신호로 사용. 헤드리스 무출력은 통과로 간주하지 않음

자동 수정→재검증은 최대 2라운드입니다. 남은 문제는 숨기지 않고 잔여 이슈로 보고합니다.

## Phase 7: Evolve

프로젝트 결과는 다음 실행의 근거가 되지만 한 번의 성공으로 전역 규칙을 바꾸지 않습니다.

1. `critique`와 구현 로그에 성공·실패·사용자 피드백·측정 결과 기록
2. 재사용 가능한 후보를 Adopt·Adapt·Avoid와 함께 분리
3. 서로 다른 과제에서 반복된 원리만 승격 후보로 표시
4. 전역 진화 후보가 있으면 `MODULE_SKILL[skill-evolve]`를 직접 읽어 3~6개 체크리스트를 먼저
   **대화에만** 제시합니다. 이 시점에는 체크리스트 파일·전역 스킬·실험 로그를 만들거나 수정하지 않습니다.
5. 사용자가 그 체크리스트와 정확한 수정 대상을 명시적으로 승인한 뒤에만 체크리스트를 저장합니다.
   승인된 진화 절차가 대조 실험을 요구하면 `MODULE_SKILL[autoresearch]`를 별도로 직접 읽어 한 번에
   변수 하나만 비교합니다. `/skill-evolve`나 `/autoresearch` 등록을 가정하지 않습니다.
6. 기준점보다 나빠지면 변경을 승격하지 않음

아프로디테가 자기 결과를 보고 즉시 자기 규칙을 수정하게 하지 않습니다. 관찰, 비교, 사용자 승인,
회귀 방지가 진화의 하네스입니다.

## Completion Evidence

완료를 보고하려면 적용 가능한 항목이 모두 있어야 합니다.

- brief와 Source Mode
- 벤치마크가 있으면 캡처 근거와 Adopt·Adapt·Avoid
- Experience Contract 검증 통과
- 새 화면·구조 변경이면 시각 탐색 전에 만든 데스크톱·모바일 와이어프레임 파일과 다섯 기준의 판단 근거
- 선택된 방향의 실제 렌더 또는 생략 근거
- `DESIGN.md`와 Layout Blueprint
- 데스크톱·모바일 구현 스크린샷
- 미학 비평과 주 과업 검증
- 접근성·성능·가이드라인 결과
- 잔여 이슈와 다음 진화 후보
- `Product Design Gate`: `READY`/`ABSENT`/`RESTART_REQUIRED`/`UNKNOWN`/`UNSUPPORTED`, exact selector,
  marketplace·설치·세션 노출 근거, 추천·동의 결과,
  실제 선택한 Product Design/local/Stitch 어댑터. 적용 대상이 아니면 `NOT APPLICABLE`
- Product Design 유무 대조가 요청됐거나 첫 도입이면 adapter comparison 결과 또는 `NOT RUN` 이유
- Web Motion Contract 적용 여부와 선택한 CSS/GSAP 경로. 영상 요청이면 `video-maker` 인계 근거
- `Module Coverage`: 각 내부 모듈의 절대 해석 경로, module/native-fallback/NOT RUN 상태,
  미실행 범위. 조건부 모듈은 NOT REQUESTED/requested를 구분하고, 요청된 경로의
  `NOT RUN`/`UNVERIFIED`/`BLOCKED` 항목은 완료 증거로 계산하지 않음

## Options

| 옵션 | 동작 |
|---|---|
| `--plan-only` | Phase 0~4 실행 |
| `--review-only` | Phase 6 실행 |
| `--benchmark <source>` | reference-driven 경로 강제 |
| `--product-design` | Codex Product Design 가용성을 확인하고 준비됐으면 프로토타입 어댑터로 우선 사용. 설치 동의는 별도 |
| `--stitch` | 승인된 계약을 Stitch adapter로 실행 |
| `--no-review` | Phase 6 생략. 결과에 검증 미완료 표시 |
| `--no-lint` | DESIGN.md 보조 lint만 생략 |
| `--export` | DESIGN.md를 Tailwind/DTCG로 파생 |
| `--skip-ia` | 단일 컴포넌트일 때 사이트맵만 생략. 과업·상태·계약은 유지 |

## Direct References

| 파일 | 읽는 시점 |
|---|---|
| [reference-capture-guide.md](references/reference-capture-guide.md) | URL·스크린샷·영상·HTML 증거 확보 |
| [site-benchmark-guide.md](references/site-benchmark-guide.md) | 벤치마크 사이트가 있을 때 필수 |
| [experience-contract-guide.md](references/experience-contract-guide.md) | 모든 신규·재설계 작업의 경험 계약 |
| [render-critique-loop.md](references/render-critique-loop.md) | 방향 탐색과 첫 구현 비평 |
| [web-motion-contract.md](references/web-motion-contract.md) | 브라우저 실시간 모션이 있을 때만 |
| [design-md-guide.md](references/design-md-guide.md) | DESIGN.md 생성·마이그레이션·export |
| `MODULE_SKILL[frontend-design]` | Phase 3·5 시각 방향과 구현 |
| `MODULE_ROOT[frontend-design]/references/layout-block-anatomy.md` | Phase 4 구조 계약 |
| `MODULE_ROOT[frontend-design]/references/coder-interface-pattern-playbook.md` | 기능형 Interface Mode |
| `MODULE_ROOT[frontend-design]/references/motion-first-prompt-playbook.md` | 표현형 방향과 모션 문법 |
| `MODULE_SKILL[design-system-starter]` | 명시적으로 요청된 상세 디자인 시스템 scaffold |
| `MODULE_SKILL[stitch]` | 명시적인 `--stitch` 실행의 MCP·상태·검증 계약 |
| `MODULE_SKILL[skill-evolve]` | 사용자 승인 뒤 전역 규칙 승격 후보를 만드는 선택 단계 |
| `MODULE_SKILL[autoresearch]` | 승인된 선택 단계의 단일 변수 대조 실험 |
