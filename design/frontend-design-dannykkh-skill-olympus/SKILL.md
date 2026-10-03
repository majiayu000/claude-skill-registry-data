---
name: frontend-design
description: 아프로디테(design-plan) 파이프라인의 Experience Contract와 DESIGN.md를 실제 렌더로 구현하고 비평하는 미학 실행 스킬. 레시피/CSV/anatomy/스캐폴드와 공식 플러그인이 없는 CLI(Codex/Antigravity)의 디자인 폴백을 제공한다. Claude Code의 일반 UI 요청은 공식 frontend-design 플러그인이 담당한다.
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

**프레이밍**: 템플릿 같은 시안을 이미 거절해 본 클라이언트를 받은 소규모 스튜디오의 디자인 리드로 작업한다. 이 브리프에 고유한 팔레트·타이포·레이아웃을 의도적으로 결정하고, **근거를 댈 수 있는 미학적 리스크를 정확히 하나** 감수한다.

**주제에 뿌리내리기 (Ground it in the subject)**: 브리프가 제품/주제를 못 박지 않았다면 디자인 전에 스스로 못 박는다 — 구체적 주제 1개, 오디언스, 페이지의 단일 임무를 선언. **고유한 선택은 주제의 세계(그 세계의 실물, 도구, 유물, 어휘)에서 나온다** — 색·폰트·구조·카피 전부에 해당하는 일반 원칙이다 (색상 유도는 Design Database 사용법 4번이 상세 절차). 사용자의 취향 기록·이전 디자인 정보가 있으면 힌트로 쓴다.

> 이식 출처: Claude 공식 frontend-design 플러그인 최신본 (2026-08-05, A/B/C 실험에서 승리한 조건 B의 코어 — docs/research/2026-08-05-deep-research-impeccable.md)

## Source-only internal module resolution (mandatory)

이 스킬은 `design-plan` 하네스의 하위 모듈 또는 standalone 원본으로 실행될 수 있습니다. 관련
스킬 이름을 활성 slash command로 가정하지 말고 다음 계약을 따릅니다.

1. 상위 하네스가 `MODULE_SKILL[name]`과 `MODULE_ROOT[name]`을 전달했으면 그 정확한 경로를
   사용하고 다시 탐색하거나 호출하지 않습니다.
2. standalone이면 실제로 필요한 모듈만 프로젝트의 `skills/<name>/SKILL.md` exact
   frontmatter → 현재 CLI 활성 루트(active skills root) → 전역 `SKILLS-CATALOG.md` exact row의 `읽을 경로`
   순서로 해석합니다.
3. 해석한 `SKILL.md` 전체를 읽고, 그 모듈의 참조·스크립트는 `MODULE_ROOT[name]` 기준으로
   찾습니다. 이름만 언급하거나 레지스트리에 등록됐다고 가정하는 것은 실행으로 치지 않습니다.

- `design-system-starter`는 사용자가 디자인 시스템 scaffold를 명시적으로 요청했을 때만
  조건부로 읽습니다. 찾지 못하면 기존 `DESIGN.md`와 프로젝트 토큰만 사용하는 bounded
  fallback으로 진행하고 `design-system-starter: NOT RUN`을 남깁니다.
- `ui-ux-auditor`와 `web-design-guidelines` 검증을 상위 하네스가 소유하면 구현물과 증거를
  반환합니다. standalone이면 위 순서로 직접 읽어 실행합니다. 찾지 못하면 네이티브
  접근성·반응형·테마 점검만 수행하고 해당 모듈을 `NOT RUN`으로 기록하며 `PASS`로 간주하지
  않습니다.
- Stitch 작업은 상위 `design-plan`이 해석한 `stitch` 어댑터가 소유합니다. 이 모듈은 Stitch
  명령을 자체 라우팅하지 않습니다.

## Design System First

Before making aesthetic choices, check if the project already has a design system:

1. `DESIGN.md` — 디자인 정본(YAML 토큰 + 산문 근거), 색상·타이포·간격·컴포넌트 규칙
2. `design-system.md` / `design-tokens.json` — 레거시 또는 파생 디자인 자산
3. `tailwind.config.*` / `theme.ts` / CSS `@theme`·변수 — 기존 테마 설정 (Tailwind v4는 CSS-first `@import "tailwindcss"`+`@theme`이라 config 파일이 없을 수 있음; v3 JS config를 쓰면 `@config`로 명시 로드)

**있으면**: 토큰(색상, 폰트, 간격)만 뽑아 쓰지 말고 **DESIGN.md 전체를 Read** — 산문 계약(Spatial
Model, State Contracts, Motion, Component Anatomy, Copy Rules 등)이 구도·상태·카피의 스펙입니다.
`docs/design-refs/`가 있으면 최신 Experience Contract, direction·critique, benchmark 증거,
레이아웃 청사진도 함께 Read해서 구현 계약으로 사용합니다. 우선순위는 사용자 과업·접근성 >
Experience Contract > DESIGN.md 시각 토큰 > Layout Blueprint > benchmark 증거입니다.
**후속 수정 세션에도 동일 적용** — "버튼 하나 고치는" 세션이 산문 계약을
안 읽으면 수정이 누적될수록 원래 디자인 의도에서 드리프트합니다. 토큰은 그대로, 산문 계약 위반 금지.
**없으면**: 아래 Design Thinking으로 자유롭게 방향을 결정.

## Interface-Type Gate

스타일 프리셋보다 먼저 화면의 주 행동을 분류합니다. 랭킹·모니터링, 검색 디렉터리,
agent IDE, 로딩 상태, 효과 문서라면
[`references/coder-interface-pattern-playbook.md`](references/coder-interface-pattern-playbook.md)를
읽고 다음 중 하나를 고릅니다.

- `Data Instrument`
- `Faceted Directory`
- `Agent Workbench`
- `Waiting State`
- `Effect Stage`

기능형 UI의 기본 장식 효과 수는 `0`입니다. 정보 위계, 상태 전달, 입력 피드백을 먼저 설계하고
남는 예산에만 signature effect를 둡니다. React Bits 같은 컴포넌트 라이브러리는 디자인 방향이
정해진 뒤 채택 게이트를 통과한 효과만 사용합니다.

## Design Style Presets

프론트엔드 생성/재디자인 시 **사용자에게 디자인 스타일을 질문**합니다.

현재 CLI의 질문 방식:

```
question: "어떤 느낌으로 만들까요?"
header: "디자인 스타일"
options:
  - label: "깔끔하게"
    description: "정돈된 기업 사이트, 안정적인 레이아웃"
  - label: "럭셔리하게"
    description: "여백 많고 프리미엄한 느낌, 고급 브랜드"
  - label: "대담하게"
    description: "비대칭, 애니메이션, 눈에 띄는 디자인"
  - label: "미니멀하게"
    description: "차분하고 절제된, 군더더기 없는"
  - label: "대시보드"
    description: "데이터 중심, 빽빽하고 효율적"
  - label: "매거진"
    description: "에디토리얼, 사진 중심, 읽는 재미"
  - label: "직접 설정"
    description: "VARIANCE/MOTION/DENSITY 숫자로 직접 조정"
```

### 프리셋 → 파라미터 매핑

| 프리셋 | VARIANCE | MOTION | DENSITY | 느낌 |
|--------|----------|--------|---------|------|
| **깔끔하게** | 3 | 3 | 5 | 정돈된 그리드, 최소 애니메이션 |
| **럭셔리하게** | 5 | 5 | 2 | 넉넉한 여백, 프리미엄 타이포 |
| **대담하게** | 8 | 7 | 5 | 비대칭 레이아웃, 스크롤 트리거 |
| **미니멀하게** | 4 | 2 | 3 | 절제된 색상, 여유 있는 간격 |
| **대시보드** | 2 | 3 | 8 | 촘촘한 데이터, 모노스페이스 |
| **매거진** | 7 | 5 | 3 | 오프셋 이미지, 타이포 중심 |

### Tunable Parameters (직접 설정 시)

```
DESIGN_VARIANCE: 1~10  (1=완벽한 대칭 ↔ 10=비대칭 실험적)
MOTION_INTENSITY: 1~10  (1=정적 ↔ 10=시네마틱 물리)
VISUAL_DENSITY: 1~10    (1=갤러리/여유 ↔ 10=대시보드/빽빽)
```

| 파라미터 | 1~3 | 4~7 | 8~10 |
|----------|-----|-----|------|
| **DESIGN_VARIANCE** | 센터 정렬, 대칭 그리드, 균일 패딩 | 오프셋 마진, 비대칭 비율, 좌측 정렬 헤더 | 매소닉, CSS Grid fr, 거대한 빈 공간 |
| **MOTION_INTENSITY** | CSS `:hover`/`:active`만 | `transition: all 0.3s cubic-bezier(0.16,1,0.3,1)`, 캐스케이드 | Framer Motion, 스크롤 트리거, 패럴랙스 |
| **VISUAL_DENSITY** | 여유 여백, 큰 섹션 간격, 럭셔리 | 일반 웹앱 간격 | 촘촘한 패딩, 1px 구분선, 숫자엔 모노스페이스 |

> Credits: Tunable parameters inspired by [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT)

## Design Database (참조 데이터)

프리셋 선택 후 또는 직접 디자인 시, 아래 DB에서 프로젝트에 맞는 팔레트/폰트/스타일을 검색합니다.

| DB | 파일 | 항목 수 | 내용 |
|----|------|---------|------|
| **스타일 레시피** | [references/style-recipes/index.md](references/style-recipes/index.md) | 12종 | 완결된 미학 캡슐 — 경계 선언 + hex 토큰 + 한·영 폰트 스택 + 패턴 + Avoid. **프리셋보다 구체적인 시작점** |
| **Motion-first 프롬프트** | [references/motion-first-prompt-playbook.md](references/motion-first-prompt-playbook.md) | 방향 8종 | 공개 무료 프롬프트에서 합성한 구현 문법 + 색상 레인 + 초록/주황 편향 차단 |
| **코더 UI 패턴** | [references/coder-interface-pattern-playbook.md](references/coder-interface-pattern-playbook.md) | 유형 5종 | 데이터 도구·디렉터리·agent workbench·로딩·효과 stage의 정보 구조, 밀도, 상태, 모션 예산 |
| **블록 해부 카탈로그** | [references/layout-block-anatomy.md](references/layout-block-anatomy.md) | 블록 30종 | Marketing/App/Ecommerce 블록별 구조 계약(요소 순서·잉크 위계·강조 규칙) + 페이지 시퀀스 템플릿 + 와이어프레임-퍼스트 청사진 절차 |
| **코드 스캐폴드** | [references/scaffolds/](references/scaffolds/) | 블록 4종 | Hero/Navbar/Footer/Pricing의 렌더 검증된 시작 코드(HTML+CSS, DESIGN.md 토큰 바인딩) — anatomy를 산문이 아니라 실제 마크업으로 강제 |
| **색상 후보 도구** | [scripts/select-diverse-palettes.js](scripts/select-diverse-palettes.js) | JSON | CSV/playbook을 hue family로 분산. 기본 초록/주황 0개 + 과사용 스톡 accent(Tailwind 기본 hex 등) 기본 제외(`--allow-stock`으로 해제) |
| **테크닉 레시피** | [references/technique-recipes.md](references/technique-recipes.md) | 10종 | 그림자/blur/보더 그라데이션/텍스트 리빌/마퀴/GSAP+Lenis/접근 가능한 로딩 상태 — 복붙 가능한 검증 값 |
| **색상 팔레트** | [references/color-palettes.csv](references/color-palettes.csv) | 9개 | 산업별 색상 세트 (Primary~Border 18컬럼). 원 161행 중 과사용 스톡 accent 152행 삭제(2026-08-05) — 폴백은 플레이북 레인이 주력 |
| **폰트 페어링** | [references/font-pairings.csv](references/font-pairings.csv) | 47개 | Heading+Body 조합, Google Fonts URL 포함. 비한글 과사용 37행 삭제(2026-08-05), 한글 페어링 #74~84 전부 보존 |
| **디자인 스타일** | [references/design-styles.csv](references/design-styles.csv) | 84개 | Glassmorphism, Brutalism 등 스타일별 색상/효과/호환성/체크리스트 |

**사용법:**

1. 먼저 `Interface-Type Gate`로 주 유형을 정합니다. 기능형 유형이면 `coder-interface-pattern-playbook.md`의 정보 구조와 모션 예산을 고정합니다.
2. 방향이 모호하거나 결과 반복 불만이 있으면 `motion-first-prompt-playbook.md`를 읽고 구성·색·모션이 다른 방향 카드 3개를 만듭니다.
2-1. 페이지/섹션을 새로 만들 때는 `layout-block-anatomy.md`에서 블록 시퀀스와 해당 블록의 anatomy 계약(필수 요소·강조 1개 규칙·CTA 문법)을 확인하고 마크업 구조를 먼저 고정합니다 — 레퍼런스가 없을 때 즉흥 구조 금지. Hero/Navbar/Footer/Pricing이면 `scaffolds/`의 렌더 검증된 코드부터 시작(처음부터 새로 짜지 않음).
3. **레시피 우선**: 선택된 방향과 맞는 스타일 레시피가 있으면 그 레시피 1개 파일만 Read → 토큰/패턴을 시작점으로 (두 레시피 혼합 금지). 액센트는 색상 레인/CSV 팔레트로 변주 가능
4. **색은 유도가 기본, DB는 폴백**: 제품의 세계에서 재료(실물·도메인 어휘 3~5개)를 뽑아 지배색+액센트를 유도하고 대비를 실측하는 것이 1차 경로입니다(카탈로그 선택은 "인터넷의 평균"으로 수렴 — 과사용 스톡 152행은 삭제 완료). 유도 재료가 없을 때만 `node "<이 스킬 디렉터리>/scripts/select-diverse-palettes.js" --type "{타입}" --seed "{slug}"` shortlist를 폴백으로 사용합니다(잔여 9행 + 플레이북 레인). 초록/주황이 필요하다는 근거가 있을 때만 `--max-signal 1`을 추가합니다.
5. 색상 CSV의 잔여 행에 해당 산업이 있으면 참조 가능하나, 대부분 삭제됐으므로 유도(4번)와 플레이북 레인이 실질 경로입니다
6. 프리셋 "럭셔리" → `design-styles.csv`에서 Minimalism, Neumorphism 참조 — 무드·체크리스트·기술 키워드만 참조하고 **Colors 컬럼의 hex는 복사 금지**(순수 #000000/#FFFFFF·보라 지정 행 존재 — 색 정본은 유도 값/DESIGN.md 토큰)
7. 사용자가 "세련된 느낌" → `font-pairings.csv`에서 "elegant, luxury" 키워드 검색 — 비한글 과사용 행은 삭제됨(47행 잔존). 한글 UI는 한글 행 #74~84 우선(전부 보존, 한글 커버리지 정보 보유) — 과사용 폰트(IBM Plex 계열) 포함 2건만 `ai-slop-blacklist.md` 교차 확인
8. 구현 중 그림자/blur/리빌/로딩 디테일 필요 시 → `technique-recipes.md` 해당 §만 참조

> Credits: Design databases from [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (MIT),
> style/technique recipes adapted from [MengTo/Skills](https://github.com/MengTo/Skills) (MIT),
> block anatomy translated from [anelkabag/bag-ui](https://github.com/anelkabag/bag-ui) (MIT) block wireframes,
> code scaffolds (Hero/Navbar/Footer/Pricing) freshly written after reading bag-ui's production components —
> structure verified against them, brand copy/motion/external URLs not carried over

## Motion-first Prompt Compiler

사용자가 원하는 인상을 명확히 설명하지 못하거나 이전 출력이 비슷하게 반복됐으면 코딩 전에
`references/motion-first-prompt-playbook.md`를 읽습니다.

1. Experience Contract가 있으면 그 `Prompt Contract`를 정본으로 사용합니다. 없으면 INTERFACE MODE,
   PRIMARY ACTION, INFORMATION+STATE, DENSITY+EFFECT BUDGET을 먼저 채운 뒤 GOAL, AUDIENCE, TASK,
   FLOW, HEADER, MESSAGE, SECTION_ORDER, CTA, TRUST, COMPOSITION, TYPE, COLOR, MATERIAL, MOTION,
   MEDIA, RESPONSIVE, STATES, PERFORMANCE, ACCESSIBILITY, PRESERVE, EXCLUDE, SUCCESS를 채웁니다.
2. 후보 3개는 베이스 명도, 색상 계열, 레이아웃, 모션 중 최소 4개가 달라야 합니다.
3. 초록·주황은 합쳐서 후보 3개 중 최대 1개이며, 브랜드/도메인 근거가 없으면 제외합니다.
4. 공개 레퍼런스에서는 구조와 결정 문법만 배우고 프롬프트 문구, 카피, 에셋 URL을 복제하지 않습니다.
5. 기능형 UI에서는 장식 효과보다 상태·밀도·비교 가능성을 먼저 검증합니다.
6. 방향 선택 후 DESIGN.md에 값을 고정하고, 구현 단계에서는 전체 재생성 대신 변수 1~2개만 바꿉니다.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Interface mode first**: In functional UI, "bold" means decisive hierarchy, density, and state semantics—not decorative motion.
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?
- **Direction fingerprint**: Base mode, layout axis, type contrast, hue family, material, and motion mechanism. If two candidates share four or more of these six, they are the same direction.

- **Hero는 논지(thesis)다**: 주제의 세계에서 가장 특징적인 것으로 연다 — 헤드라인, 이미지, 애니메이션, 라이브 데모, 인터랙티브 순간 중 주제에 맞는 형태로. "큰 숫자 + 작은 라벨 + 그라데이션 액센트"는 템플릿 답안이다.
- **구조는 정보다**: 번호(01/02/03)·아이브로우·구분선·라벨 같은 구조 장치는 내용의 사실을 부호화할 때만 쓴다 — 실제 순서·실제 타임라인이 아니면 번호를 붙이지 않는다. 장식용 구조 장치는 제거.

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

### 2-Pass 프로세스: 계획 → 제네릭 자기검사 → 구현

**캘리브레이션 — 현재 AI 디자인은 3개 클러스터로 수렴한다**: ① 웜 크림 지면(#F4F1EA 근방) + 고대비 세리프 디스플레이 + 테라코타/시그널레드 액센트, ② 니어블랙 + 애시드그린·버밀리언 단일 액센트, ③ 브로드시트 헤어라인 + 라운드 0 + 신문형 밀집 칼럼. 셋 다 어떤 브리프엔 정당하지만 **선택이 아니라 기본값이며 주제와 무관하게 나타난다** (2026-08-04 실험에서 세 조건 모두 ①에 착지). 브리프가 방향을 못 박으면 브리프가 이긴다 — 이 룩을 요구할 때 포함. 브리프가 축을 비워뒀으면 그 자유를 이 기본값들에 쓰지 않는다.

1. **Pass 1 — 계획**: 콤팩트 토큰 계획을 만든다 — Color: 이름 붙인 hex 4~6개 / Type: 역할 2개 이상(절제해 쓰는 개성 디스플레이 + 보완 본문 + 필요시 유틸리티) / Layout: Experience Contract와 Layout Blueprint에서 인용 / **Signature: 이 페이지가 기억될 단 하나의 고유 요소**
2. **제네릭 자기검사**: 구현 전에 계획을 브리프와 대조한다 — "비슷한 브리프를 스스로 시뮬레이션했을 때 같은 곳에 도달하는 부분"이 있으면 그 부분은 이 브리프를 위한 선택이 아니라 기본값이다. 수정하고 무엇을 왜 바꿨는지 말한다
3. **Pass 2 — 구현**: 수정된 계획을 정확히 따르며 모든 색·타이포 결정을 계획에서 파생. **대담함은 한 곳에 쓴다** — Signature가 유일한 기억 장치, 주변은 조용하고 규율 있게. 품질 바닥(모바일 반응형·키보드 포커스·reduced-motion)은 선언 없이 갖춘다
4. **CSS 특이도 주의**: `.section a` 같은 타입+요소 셀렉터가 `.btn` 같은 클래스를 이기며 서로 상쇄되기 쉽다(특히 섹션 간 패딩/마진, 내비 안 버튼) — 실험 조건 B가 실제로 이 버그를 렌더 검증에서 잡았다

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font. 2026 경향: serif 헤드라인 + sans 본문 페어링, 표현적 이탤릭. **한글 프로젝트는 Pretendard를 안전한 기본**으로, 더 개성 있는 한글 폰트는 [눈누(noonnu.cc)](https://noonnu.cc)에서 상업용 무료 라이선스(웹폰트/임베딩 허용)로 탐색.
  - **한·영 페어링은 한 시스템으로(중요)**: 한글+라틴이 섞일 때 따로 놀지 않으려면 둘을 같은 시각 논리로 묶어라 — (1) 한 패밀리가 한·영을 모두 커버하거나(Pretendard/Wanted Sans/IBM Plex Sans KR 등), (2) 한글 폰트와 라틴 폰트의 **무게축·획 대비(contrast) DNA·x-height를 맞춰** 같은 목소리로. 검증된 조합 예: 송명(고대비 명조)×Fraunces(고대비 모던 세리프), 검은고딕(초헤비)×Space Grotesk(헤비 그로테스크), Gothic A1×Space Mono(기능적/모노). 한글엔 진짜 이탤릭이 거의 없으니 **한글 강조는 라틴 이탤릭에 의존하지 말고** 한글 serif·색·굵기·의도된 슬랜트(skewX)로 — 라틴 전용 이탤릭(Instrument Serif/Fraunces 등)에 한글을 넣으면 시스템 serif로 폴백해 의도가 깨진다.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. **신규 색은 `oklch()`로 작성** (2026 권장 기본) — 지각 균일(equal L = 동일 밝기)이라 톤 스케일·대비 예측·접근성이 HEX/HSL보다 유리, HEX는 레거시 폴백으로. 광색역은 chroma ≤0.15면 sRGB 안전, 0.2+는 Display P3 영역(더 선명).
  - **초록/주황 자동 수렴 금지**: 현재 팔레트 DB의 Accent는 두 계열 비중이 높습니다. CSV 첫 행이나 익숙한 성공 사례를 추천 순위로 쓰지 말고 hue family를 먼저 분산합니다. 후보 3개에는 서로 다른 색상 계열을 쓰며, 초록·주황은 합쳐 최대 1개만 허용합니다.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise. **스크롤 연동 모션은 2026 주류** — 네이티브 CSS 스크롤 타임라인(`animation-timeline: view()` / `scroll()`)을 1순위로(컴포지터 스레드 실행 → 메인스레드 jank 제로, 약 80% 케이스 커버). 핀(pin)·스크롤 스냅·복잡한 시퀀스·WebGL/스크롤리텔링만 GSAP ScrollTrigger(부드러운 스크롤은 Lenis, `gsap.ticker`와 동기화). JS 스크롤 효과는 모바일 LCP/CLS·SEO를 해치므로 남용 금지, 모든 스크롤 모션에 `prefers-reduced-motion` 폴백 필수. **페이지/뷰 전환은 View Transitions API** — SPA는 `document.startViewTransition()`(baseline), MPA는 `@view-transition { navigation: auto }`(동일 출처 양쪽 페이지, Chromium+Safari). 미지원 브라우저에선 애니 없이 정상 동작하는 점진적 향상이므로 지금 도입 OK, cross-document는 Speculation Rules로 목적지 프리로드.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density. **컴포넌트 반응형은 뷰포트 미디어쿼리가 아니라 컨테이너 쿼리**(`container-type: inline-size` + `@container`, 2024~ baseline widely available) — 카드가 사이드바/본문 어디 놓이든 자기 컨테이너 폭에 적응하므로 재사용 컴포넌트에 1순위. 미디어쿼리는 페이지 전역 레이아웃(내비 데스크톱→모바일, 전역 타이포·간격, print)에만. JS `ResizeObserver` 대체 → 메인스레드 부담↓. **상태/내용 기반 스타일은 `:has()`**(첫 부모 셀렉터, 2023~ baseline) — "에러 input 있는 폼 섹션 강조", "특정 자식 가진 카드만 변형" 같은 걸 JS DOM 검사 없이. 단 성능상 `.container`/`.gallery`처럼 구체적 앵커에만 걸고(`body`/`:root`/`*` 금지), 내부 셀렉터엔 `>`/`+` 조합자로 탐색 범위 한정. 미지원 대비 `@supports (selector(:has(*)))`.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays. **구현 값**: `technique-recipes.md` §11(그레인/메시/강조 이탈/지속 비대칭) — 지시만 읽고 넘어가지 말 것. flat 패널 + 완벽히 균일한 반복 그리드는 규칙(색·폰트·대비)을 다 지켜도 "딱딱한 AI적 느낌"의 가장 흔한 원인.

## Banned Patterns (AI Slop 방지)

> 공유 블랙리스트: [references/ai-slop-blacklist.md](references/ai-slop-blacklist.md) — 10항목 블랙리스트 + Hard Rejection 7개 + 폰트 블랙리스트/대안

**Typography:**
- `Inter`/시스템 폰트를 기본값으로 쓰지 말 것 (= AI 슬롭 신호) → `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`, `General Sans` 등. **한글: Pretendard 기본 + [눈누](https://noonnu.cc)에서 탐색**
- 한글 강조에 라틴 전용 이탤릭 폰트(Instrument Serif·Fraunces 등) 직접 적용 금지 → 한글이 시스템 serif로 폴백해 의도가 깨짐. 한글 강조는 한글 serif(송명·마루부리·고운바탕 등) + 색/굵기로
- 한글 디스플레이를 Pretendard 볼드로만 때우지 말 것(= 개성 없는 기본값) → 헤드라인은 눈누/구글의 개성 있는 한글 디스플레이(검은고딕·송명·Gothic A1 900 등)로
- 대시보드/소프트웨어 UI에 Serif 금지
- 과도한 H1 크기 금지

**Color:**
- **기본값**으로 끌려간 "AI Purple/Blue"(보라 글로우, 디폴트 보라→파랑 그라데이션) 금지 — 단 2026은 **컨셉으로 선택한 대담·고채도(도파민/레트로퓨처)는 유효**. "무심코"는 금지, "의도적"은 OK
- **DB 기본값**으로 끌려간 초록/주황 액센트 금지 — 환경·상태·산업 신호·브랜드색처럼 명시적 이유가 있을 때만 사용
- 순수 검정(#000000) 금지 → Zinc-950 또는 Charcoal 사용
- 채도 80% 초과는 **컨셉상 의도된 경우에만**(도파민/브랜드 강조) — 무심코 디폴트로 쓰는 건 금지
- 그라데이션 텍스트 남용 금지
- 액센트 색상은 **최대 1개**, 나머지는 Zinc/Slate 뉴트럴

**Layout:**
- `DESIGN_VARIANCE > 4`일 때 센터 정렬 Hero 섹션 금지 → 비대칭 강제
- **비대칭을 히어로 1곳에서만 쓰고 이후 섹션이 전부 균등 그리드로 복귀 금지** → 히어로 그리드 비율을 최소 1개 후속 섹션에서 재사용(technique-recipes §11-D 지속 비대칭). 한 번 쓰고 포기한 비대칭은 "시도했다 안 했다"로 읽힘
- 3열 카드 레이아웃 반복 금지 → 지그재그, 비대칭 그리드, 가로 스크롤 활용
- 반복 블록(카드/행) 3개 이상이면 정확히 1개를 근거 있는 이유로 강조 이탈(technique-recipes §11-C) → 완전 균일 반복은 예산 지켜도 딱딱해 보임
- `h-screen` 금지 → `min-h-[100dvh]` 사용 (모바일 레이아웃 점프 방지)
- `VISUAL_DENSITY > 7`일 때 카드 남용 금지 → `border-t`, `divide-y`, 여백으로 대체
- **지루함 테스트(Boring Test, §11-E)**: 제품명만 바꿔도 다른 SaaS에 그대로 쓰이는 구조면 팔레트·폰트와 무관하게 제네릭. 구현 완료 직후 자가 점검 필수

**Motion:**
- `transform`과 `opacity`만 애니메이트 — `top`, `left`, `width`, `height` 애니메이트 금지
- Spring Physics 기본: `type: "spring", stiffness: 100, damping: 20`
- 스크롤 효과에 메인스레드 `scroll` 이벤트 리스너 직접 사용 금지 → CSS `animation-timeline`(우선) 또는 `IntersectionObserver`/GSAP ScrollTrigger로
- 스크롤 컨테이너에 grain/noise 필터 금지 (성능)
- `z-index` 남발 금지 — 시스템 레이어(navbar, modal, overlay)에만

**Content (스타트업 슬럽 방지):**
- "John Doe", "Sarah Chan" 같은 제네릭 이름 금지
- 99.99%, 50% 같은 예측 가능한 숫자 금지
- "Elevate", "Seamless", "Unleash", "Next-Gen" 같은 AI 카피 금지
- 이모지 금지 → Radix Icons, Phosphor Icons, 또는 커스텀 SVG 사용

**Output 완성도:**
- placeholder 코드 금지 (`// TODO`, `...`, `/* implement later */`)
- 모든 상태 필수 구현: Loading, Empty, Error, 성공
- `:active` 상태에 `-translate-y-[1px]` 또는 `scale-[0.98]`로 촉각 피드백
- `shadcn/ui`는 커스터마이징 후에만 사용 (기본 상태 그대로 사용 금지)

NEVER use generic AI-generated aesthetics. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code. Minimalist designs need restraint and precision. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back.

## Writing in Design (카피 원칙)

카피는 장식이 아니라 **디자인 재료**다 — 이해를 돕고, 그래서 쓰기 쉽게 만들기 위해 존재한다. 간격과 색에 쏟는 의도를 카피에도 쏟는다.

- **사용자 쪽에서 쓴다**: 시스템 구조가 아니라 사람이 인지·조작하는 대상으로 명명 — "웹훅 설정"이 아니라 "알림 관리". 팔지 말고 무엇을 하는지 평이하게. 영리함보다 구체성
- **능동태 + 정확한 동사**: 컨트롤은 눌렀을 때 일어나는 일을 그대로 말한다 — "Submit"이 아니라 "변경사항 저장". 같은 행동은 흐름 내내 같은 이름("게시" 버튼 → "게시됨" 토스트) — 어휘 일관성이 길찾기 표지판
- **실패와 빈 화면은 방향 제시의 순간**: 에러는 사과하지 않고 무엇이 잘못됐고 어떻게 고치는지 명확히. 빈 화면은 행동으로의 초대
- **요소당 임무 하나**: 라벨은 라벨하고, 예시는 시연한다 — 몰래 두 역할을 겸하는 요소 금지. 어조는 브랜드·오디언스에 맞춘 평문, sentence case, 필러 없음

## Design Module Workflow (디자인 모듈 조합)

```
설계 단계 ──────────────────────────────────────────────
  design-plan 하네스         → 화면 유형·방향·토큰을 DESIGN.md로 고정
  design-system-starter 원본 → 명시적 scaffold 요청일 때만 세부 토큰 파생
  stitch 어댑터              → 상위 하네스가 원격 디자인 작업과 역추출을 소유

구현 단계 ──────────────────────────────────────────────
  frontend-design            → 공식 플러그인이 없는 CLI는 이 원본을 직접 읽어 구현
  stitch 어댑터              → DESIGN.md·청사진 기반 생성·수정·변형·멀티페이지·React 반영

리뷰 단계 ──────────────────────────────────────────────
  네이티브 시각 비평       → render-critique-loop 계약으로 실제 렌더의 미학·메시지·신뢰·모바일 평가
  ui-ux-auditor 원본        → 다크모드, 반응형, 접근성 등 9영역 감사
  web-design-guidelines 원본 → Web Interface Guidelines 준수 체크
```

**조합 예시:**
1. `design-plan` 하네스가 Interface Mode + DESIGN.md 생성
2. 이 스킬이 DESIGN.md와 관련 playbook을 읽어 구조·토큰·미학 적용
3. 구현 완료 후 상위 하네스 또는 직접 해석한 `ui-ux-auditor` 원본이 9영역 감사 수행

## Usage Patterns (3단계 활용법)

### 0단계: Unknown Known 끌어내기 (조건부 필수)
사용자가 "봐야 알 것 같다", "디자인 취향을 설명하기 어렵다", "방향을 모르겠다", "항상 비슷하다"고
하거나 브랜드 가이드 없이 대표 화면을 만들거나 벤치마크를 크게 변환할 때 구현 전에 가벼운
프로토타입을 만듭니다. 자세한 선택·비평·수정 규율은
`../design-plan/references/render-critique-loop.md`를 따릅니다.

- 백엔드/API 연결 없이 동일한 실제 카피·데이터·상태의 HTML 또는 React 정적 화면 3개를 서로 다른 방향으로 만든다
- 기능형 UI면 먼저 `references/coder-interface-pattern-playbook.md`로 화면 유형과 효과 예산을 고정한다
- 각 방향은 색/타이포/밀도/레이아웃이 분명히 달라야 하며, 같은 카드 그리드의 변주로 만들지 않는다 — `references/motion-first-prompt-playbook.md`의 서로 다른 3안 규칙으로 방향을 벌린 뒤 `references/style-recipes/`에서 레시피를 매칭한다
- 데스크톱 대표 화면과 모바일 핵심 화면을 함께 렌더하고, 설명을 읽기 전에 스크린샷만 보고 비평한다
- 사용자가 고른 방향에서 "좋은 점/싫은 점"을 추출해 `DESIGN.md` 또는 구현 지시로 고정한다
- 확정 전 프로토타입은 throwaway로 취급하고, 실제 구현에 그대로 복붙하지 않는다

**방향 확정 후 반복 규율 (variants > rerolls):**
- 첫 결과에서 바로 고정하지 않고 `render-critique-loop.md`의 Baseline-worthiness gate를 통과시킨다.
- 구조·메시지·모바일 흐름이 실패하면 레이아웃·섹션 순서·카피·CTA·신뢰 위치까지 다시 설계한다.
- gate를 통과한 뒤에만 **레이아웃 + 위계 + 카피를 보존 영역으로 고정**한다.
- 이후 반복은 전체 재생성(reroll)이 아니라 **한 번에 변수 1~2개만** 바꾸는 변형(variant)으로: 액센트 색 / 배경 톤 / 카드 배치 / 크롭·앵글.
- 수정 지시에 "다른 건 바꾸지 마", "히어로는 유지"를 명시해 이미 잘 된 부분의 파괴를 방지한다.
- 같은 취향을 반복 설명하지 말고 파일로 고정한다 — 레퍼런스는 `docs/design-refs/`(아프로디테 Phase 1 슈퍼프롬프트), 토큰은 DESIGN.md.

### 1단계: 기본 생성
먼저 primary action, 정보 위계, 상태 모델, 반응형 순서를 확정합니다. 기능형 UI에서는 장식보다
스캔·비교·조작 가능성을 먼저 검증하고, 표현형 UI에서는 첫 화면의 기억 장치 1개를 고정합니다.

### 2단계: 스킬 적용 (레퍼런스 없이)
"use the frontend design skill to improve the design" — 이 스킬의 미학 가이드라인만으로 재디자인.

### 3단계: 레퍼런스 참조 재디자인 (최고 품질)
Dribbble, Behance, Awwwards 등에서 원하는 스타일의 스크린샷을 찾아 첨부:
"use the frontend design skill to improve the design following the attached screenshot"

> **3단계가 가장 효과적.** 레퍼런스 이미지가 있으면 톤/색상/레이아웃을 정확하게 매칭할 수 있다.
