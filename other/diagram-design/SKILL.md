---
name: diagram-design
description: >
  에디토리얼 품질 다이어그램 표현 계층. 파이프라인 .mmd(flowchart/sequence/state/ER) 또는
  자연어 설명을 브랜드 토큰 기반 self-contained HTML + inline SVG로 렌더링한다.
  PRD·기술문서·아키텍처 문서 등 사람에게 전달되는 산출물에 다이어그램이 필요할 때 사용.
  Mermaid 파이프라인을 대체하지 않음(.mmd가 정본, 이 모듈은 렌더링만).
  "다이어그램 예쁘게", "editorial diagram", "다이어그램 렌더링", "발표용 다이어그램" 요청에 실행.
  Credits: cathrynlavery/diagram-design v2.6 (MIT, pinned 648c2a5)
---

# Diagram Design (표현 계층)

> **정본은 `.mmd`, 렌더링은 여기.** Mermaid 자동 레이아웃 대신 에디토리얼 규칙으로
> 직접 배치한 inline SVG를 생성합니다. upstream cathrynlavery/diagram-design의 부분 vendoring입니다.

## 역할 경계 (필수 준수)

| 계층 | 소유자 | 산출물 | 용도 |
|------|--------|--------|------|
| 설계 도면 (정본) | mermaid-diagrams + flow-verifier + zephermine Step 18 | `.mmd` | 기계 대조(코드 흐름 검증), diff, 파이프라인 |
| **표현 (이 모듈)** | diagram-design | self-contained `.html` (+ 선택 `.png`) | 사람용 문서·발표·공유 |

- 이 모듈은 `.mmd`를 **읽기만** 하고 절대 수정하지 않습니다. flow-verifier 검증 체인의 입력을 바꾸지 않습니다.
- **Claude 네이티브 경계**: Claude에서 Artifact(웹 페이지)로 출력할 다이어그램은 네이티브
  `artifact-diagramming` 스킬이 우선입니다. 이 모듈은 (a) 파일 산출물이 필요할 때(clio 문서 삽입,
  PNG 내보내기), (b) Codex/Antigravity/Grok 등 네이티브가 없는 CLI에서 사용합니다.
- 데이터 차트(bar/line/scatter 등 통계 시각화)는 `data-visualization` 스킬 소관입니다.
  이 모듈은 구조·흐름·관계 다이어그램만 담당합니다.

## Vendored 구성 (부분 이식)

| 파일 | 내용 |
|------|------|
| `references/core-rules.md` | upstream SKILL.md 원문 — 철학, 커넥터 6규칙(§6), 4px 그리드·복잡도 예산(§7), 산출 전 체크리스트(§9). **그리기 전 반드시 로드** |
| `references/style-guide.md` | 색·타이포 토큰 정본 (paper/ink/muted/accent, Instrument Serif + Geist + Geist Mono) |
| `references/output-spec.md` | format × size × detail × audience 다이얼, viewBox 프리셋, 타입 램프 |
| `references/type-*.md` | 타입별 레이아웃 규칙 — architecture, flowchart, sequence, er, db-schema, layers (6종) |
| `references/import-mermaid.md` | Mermaid → IR → 재배치 절차 |
| `references/export.md` | HTML → SVG/PNG 내보내기 (Playwright) |
| `scripts/mermaid_extract.py` | `.mmd` → JSON IR 파서 (표준 라이브러리만, flowchart/sequence/state/ER 지원) |
| `assets/template.html`, `assets/template-dark.html` | 산출 스캐폴드 |
| `LICENSE.upstream` | upstream MIT 라이선스 원문 |

**미포함 upstream 자산**: 나머지 33개 type 레퍼런스, semantic-patterns, animation, primitive-*,
onboarding/profiles, example HTML. 미포함 타입이 필요하면
`https://raw.githubusercontent.com/cathrynlavery/diagram-design/main/skills/diagram-design/references/type-{이름}.md`
에서 가져와 사용하고, 네트워크가 없으면 해당 타입을 `NOT RUN`으로 보고합니다.
vendored 6종으로 억지 대체하지 않습니다(폴백 금지).

## 워크플로우

1. **입력 확보**
   - `.mmd` 파일: `python scripts/mermaid_extract.py <파일> --json` 으로 JSON IR 추출
     (노드·엣지·깊이·사이클 분석 포함). 이어서 `references/import-mermaid.md`의 재배치 절차 적용.
   - 자연어 설명: 노드·관계 목록을 먼저 텍스트로 확정한 뒤 진행.
2. **타입 선택** — 아래 매핑표에서 선택 후 해당 `references/type-*.md` 로드:

   | 내용 | 타입 | 비고 |
   |------|------|------|
   | 시스템 구성, 컴포넌트 연결 | `type-architecture.md` | C4 Container 수준 |
   | 프로세스·분기 (`.mmd flowchart`) | `type-flowchart.md` | flow-verifier 도면의 사람용 렌더링 |
   | API·시간 흐름 (`.mmd sequenceDiagram`) | `type-sequence.md` | |
   | 데이터 모델 개요 (`.mmd erDiagram`) | `type-er.md` | 관계 중심 |
   | 테이블 상세 스키마 | `type-db-schema.md` | 컬럼·키 포함 |
   | 계층 구조 (인프라 스택, 아키텍처 레이어) | `type-layers.md` | |

3. **규칙 로드** — `references/core-rules.md`(§1 철학, §6 커넥터, §7 그리드·예산, §9 체크리스트)와
   `references/style-guide.md`를 읽는다. 이 단계를 건너뛰고 그리지 않는다.
4. **토큰 결정** — 아래 "DESIGN.md 토큰 매핑" 적용.
5. **SVG 작성** — `assets/template.html` 스캐폴드에 inline SVG로 작성.
   viewBox·크기는 `references/output-spec.md` 프리셋(기본 `doc-inline` 960×600)을 따른다.
6. **검증** — core-rules.md §9 체크리스트 통과 확인. 가능하면 브라우저/Playwright로 실제 렌더를
   열어 레이블 겹침·잘림을 육안 확인한다("다 된 것 같다" ≠ "확인됐다").
7. **산출** — 단일 `.html` 저장. PNG가 필요하면 `references/export.md` 절차(Playwright 스크린샷).

## DESIGN.md 토큰 매핑 (upstream §0 대체)

upstream의 "첫 실행 시 사용자에게 브랜드 질문" 게이트는 **사용하지 않습니다**
(zeus 등 zero-interaction 파이프라인과 충돌). 대신:

1. 대상 프로젝트 루트에 `DESIGN.md`가 있으면 그 토큰을 매핑한다:
   `background → paper`, `text → ink`, `accent/primary → accent`, 본문 폰트 → node-name 폰트.
   매핑 후 accent 대비가 WCAG AA 미달이면 `style-guide.md`의 Inversion rule로 보정.
2. `DESIGN.md`가 없으면 기본 스킨(white-smoke + atomic-tangerine)을 그대로 쓰고,
   산출 보고에 "기본 스킨 사용"을 한 줄 명시한다. 질문하지 않는다.

## 복잡도 예산과 분할

- core-rules.md 기준: **노드 9개 이하, 화살표 12개 이하** (밀도 목표 4/10).
- 파이프라인 `.mmd`는 노드 20개까지 허용되므로(zephermine 규칙) 초과분은
  **개요 다이어그램 1장 + 상세 다이어그램 N장**으로 분할한다. 정본 `.mmd`는 분할하지 않는다.
- 액센트는 다이어그램당 1~2개 노드만. 그림자 금지, 4px 그리드 준수.

## Related Files

| 경로 | 역할 |
|------|------|
| `skills/diagram-design/references/core-rules.md` | 핵심 규칙 원문 (upstream SKILL.md v2.6) |
| `skills/diagram-design/references/style-guide.md` | 토큰 정본 |
| `skills/diagram-design/scripts/mermaid_extract.py` | .mmd → JSON IR |
| `skills/mermaid-diagrams/SKILL.md` | 정본 도면 문법 (상류 모듈) |
| `skills/flow-verifier/SKILL.md` | 도면 대비 코드 검증 (이 모듈과 무관하게 .mmd 사용) |
| `skills/clio/SKILL.md` | 주 소비자 — 문서 산출물 다이어그램 렌더링 |
