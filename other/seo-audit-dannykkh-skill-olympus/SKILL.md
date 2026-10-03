---
name: seo-audit
description: "웹 프로젝트 SEO + AEO + GEO 종합 감사. 코드베이스를 정적 분석해 10개 영역을 점검하고, 검색 SEO 점수와 AI 가시성 점수를 따로 산출한다. 근거 계측은 스크립트가, 판정은 리포트가 담당. /seo-audit로 실행."
license: MIT
metadata:
  version: "3.0.0"
---

# SEO + AEO + GEO Audit — 웹 프로젝트 검색 종합 감사

웹 프로젝트 **코드베이스**를 정적 분석해 검색 최적화 상태를 **10개 영역**에서 점검합니다.
라이브 URL 크롤러가 아니라, 배포 전 소스에서 문제를 잡는 것이 목적입니다.

Next.js, Nuxt, Astro, Remix, SvelteKit, 정적 HTML 등 모든 웹 프레임워크에 대응합니다.

## 두 개의 점수

**검색 SEO 점수와 AI 가시성 점수를 따로 냅니다. 평균내지 않습니다.**
순위는 좋은데 AI가 인용하지 못하는 사이트가 실제로 존재하며, 하나로 뭉개면 그 사실이 사라집니다.

| 구분 | SEO (영역 1~7) | AEO (영역 9) | GEO (영역 10) |
|------|---------------|-------------|--------------|
| **대상** | Google/Bing 검색 결과 | Featured Snippet, 음성 비서 | ChatGPT, Perplexity, Gemini, Claude |
| **목표** | 검색 순위 상위 노출 | "하나의 답변"으로 선택됨 | AI가 출처로 인용 |
| **점수 축** | 검색 SEO | AI 가시성 | AI 가시성 |

> AEO/GEO는 별개 분야가 아니라 **AI 검색 표면에 적용된 SEO 기본기**입니다.
> 소견도 그렇게 서술하세요. 상세 근거는 [scoring-model.md](references/scoring-model.md#배점-근거가-바뀐-항목).

## 적용 시점

- `/seo-audit` 명시적 실행
- 웹 프로젝트 배포 전 점검
- "SEO 점검해줘", "검색 최적화 확인", "AI 검색 최적화", "AEO/GEO 점검" 요청 시

---

## Step 1: 프로젝트 정찰

기술 스택과 **사이트 유형**을 파악합니다. 유형 판정이 뒤에서 `na` 처리의 근거가 됩니다.

**필수 확인:**
```
- package.json → 프레임워크 종류, SEO 관련 패키지
- 프레임워크 설정 파일 (next.config.*, nuxt.config.*, astro.config.* 등)
- 라우팅 디렉토리 구조 (src/app/, src/pages/, src/routes/ 등)
- public/ 또는 static/ 디렉토리 내 정적 파일
- middleware 파일 존재 여부
```

**프레임워크 자동 감지:**

| 감지 패턴 | 프레임워크 | 메타데이터 방식 |
|-----------|-----------|---------------|
| `next` in package.json | Next.js | `metadata` export / `<Head>` |
| `nuxt` in package.json | Nuxt | `useHead()` / `nuxt.config` SEO |
| `astro` in package.json | Astro | frontmatter / `<BaseHead>` |
| `@remix-run` in package.json | Remix | `meta()` function |
| `@sveltejs/kit` in package.json | SvelteKit | `<svelte:head>` |
| `gatsby` in package.json | Gatsby | `gatsby-plugin-react-helmet` |
| `*.html` in root/public | 정적 HTML | `<meta>` 태그 직접 확인 |

**사이트 유형 판정 (na 처리의 근거):**

| 신호 | 유형 | 결과 |
|------|------|------|
| 콘텐츠 파일(md/mdx) 없음, 인증 라우트 위주 | 앱/대시보드 | 영역 9 전체 na |
| md/mdx 다수, 블로그 라우트 | 콘텐츠 사이트 | 영역 4의 Product na |
| Product/cart/checkout 라우트 | 커머스 | 영역 4 Product 활성 |
| i18n 설정·locale 라우트 없음 | 단일 언어 | hreflang 항목 na |
| 사내/비공개 배포 | 비공개 | 영역 8 전체 na |

판정 근거를 리포트에 한 줄로 남기세요. [na 규칙 상세 → scoring-model.md](references/scoring-model.md#na-제외와-재정규화-중요)

---

## Step 2: 10개 영역 감사

각 영역을 점검하고 **findings 배열**을 만듭니다. 등급(P0~P3)과 축(`search`/`ai`)을 함께 붙입니다.

| 카테고리 | 영역 | 한 줄 설명 | 주 축 |
|---------|------|-----------|-------|
| **SEO** | 1. robots.txt | 크롤러 접근 정책 및 sitemap 참조 | 검색 |
| **SEO** | 2. Sitemap | 모든 공개 라우트 등록 및 유효성 | 검색 |
| **SEO** | 3. 메타태그 | title, description, OG, canonical, viewport | 검색 |
| **SEO** | 4. 구조화 데이터 | JSON-LD @type 적절성 및 필수 필드 | 양쪽 |
| **SEO** | 5. 이미지 | alt 속성, 최적화 컴포넌트, lazy loading | 검색 |
| **SEO** | 6. 링크 & 내비게이션 | 404, rel, 앵커 텍스트 | 검색 |
| **SEO** | 7. 성능 | Core Web Vitals, SSR/SSG 여부 | 양쪽 |
| **AEO/GEO** | 8. AI 크롤러 접근성 | GPTBot/ClaudeBot 허용, 렌더링 | **AI** |
| **AEO/GEO** | 9. AEO (답변 엔진) | 질문형 헤딩, 40단어 규칙, Q&A 구조 | **AI** |
| **AEO/GEO** | 10. GEO (생성형 AI) | 팩트 밀도, E-E-A-T, 인용 가능성 | **AI** |

[영역별 상세 체크리스트 및 탐색 방법 → references/10-areas-checklist.md](references/10-areas-checklist.md)

[구현 코드 예시 → references/seo-patterns.md](references/seo-patterns.md)

[등급 판정 기준 → references/severity-guide.md](references/severity-guide.md)

### 판정 원칙 (반드시 지킬 것)

- **`evidence` 없이 `fail`을 쓰지 마세요.** `file:line` 근거를 못 찾았으면 `fail`이 아니라 `unknown`입니다.
- 정적 분석으로 확인 불가한 항목(런타임 헤더, 실제 렌더 결과)은 `unknown`으로 두고 리포트에 이유를 적습니다.
- 해당 없는 항목은 `na`. 억지로 `fail`을 만들지 마세요.

---

## Step 3: 계측 스크립트 실행

**판단하기 전에 세십시오.** 스크립트는 결정론적 수치만 내고, 해석은 리포트가 합니다.

### 3-1. 팩트 밀도 계측 (영역 9~10 근거)

한국어·영어 콘텐츠를 함께 처리합니다.

```bash
python scripts/fact_density.py <콘텐츠 경로> --json
python scripts/fact_density.py ./src/content --json
```

출력 항목과 대응 점검:

| 출력 | 대응 영역·항목 |
|------|--------------|
| `numeric_density_per_100w` | 영역 10-1 팩트 밀도 |
| `original_data_signal` | 영역 10-6 고유 데이터 |
| `citation_markers` | 영역 10-2 출처 표기 |
| `superlative_or_vague_authority` | 영역 10-1 역신호 (과장) |
| `authoritative_outbound_links` | 영역 10-3 권위 신호 |
| `question_headings` | 영역 9-2 질문형 헤딩 |
| `answer_leads_over_40w` | 영역 9-3 40단어 규칙 |

> 스크립트는 **세기만** 합니다. "이 주장이 출처를 필요로 하는가"는 리포트의 판단입니다.
> 카운트를 채우려고 통계나 출처를 지어내지 마세요.

### 3-2. Lighthouse (영역 7 성능)

```bash
npx lighthouse --version 2>/dev/null || echo "미설치 — npm install -g lighthouse"
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 || echo "서버 미실행"

npx lighthouse http://localhost:3000 \
  --output=json --output-path=./lighthouse-report.json \
  --chrome-flags="--headless --no-sandbox" \
  --only-categories=performance,accessibility,best-practices,seo
```

| Lighthouse 점수 | 등급 | 조치 |
|----------------|------|------|
| 90-100 | 녹색 | 양호 |
| 50-89 | 주황 | P1~P2 |
| 0-49 | 빨강 | P0 |

Core Web Vitals 기준: LCP < 2.5s, CLS < 0.1, INP < 200ms, FCP < 1.8s, TTFB < 800ms

**실행 불가 시**: dev server 미실행이면 사용자에게 안내, Chrome 미설치면 영역 7 항목을
`unknown`으로 두고 사유를 명시합니다. **점수를 추측으로 채우지 마세요.**

---

## Step 4: 두 축 점수 계산

findings를 JSON으로 만들어 스코어러에 넘깁니다.

```bash
python scripts/score.py findings.json
python scripts/score.py findings.json --json
```

스코어러가 자동 처리하는 것:
- `na`/`unknown` 항목을 분자·분모에서 제외하고 **재정규화**
- 축별 P0 `fail` 발생 시 **40점 상한** + `capped: true`
- 두 축 조합 해석 문장

[점수 모델 상세 → references/scoring-model.md](references/scoring-model.md)

---

## Step 5: 감사 리포트 생성

```
# SEO 감사 리포트

프로젝트: {프로젝트명}  |  프레임워크: {감지}  |  유형: {사이트 유형}  |  점검일: {날짜}

검색 SEO 점수:   {N}/100 [{밴드}]{ 상한 표시}
AI 가시성 점수:  {N}/100 [{밴드}]{ 상한 표시}
해석: {두 축 조합 해석}
제외 항목: 해당 없음 {n}건 / 판정 불가 {n}건

이슈: P0 {n}건 / P1 {n}건 / P2 {n}건 / P3 {n}건

Lighthouse: Performance {N} · Accessibility {N} · Best Practices {N} · SEO {N}
```

- **P0** (즉시 수정): 현재 상태 → 영향 → 수정 코드 (`file:line` 근거 필수)
- **P1** (빠른 수정): 현재 상태 → 영향 → 수정 방법
- **P2 / P3**: 항목 설명
- **판정 불가 항목**: 무엇을 왜 확인 못 했는지 명시
- **통과 항목**: 체크리스트
- **권장 액션 플랜**: 상한이 걸린 축의 P0부터

[전체 리포트 형식 → references/severity-guide.md](references/severity-guide.md)

---

## 다음 단계 안내

```
SEO + AEO + GEO 감사 완료

  검색 SEO 점수:  {N}/100 [{밴드}]
  AI 가시성 점수: {N}/100 [{밴드}]
  {해석 한 줄}

다음 단계 (선택):
  /code-reviewer 보안 감사 → 보안 점검
  /minos               → Playwright 자동 테스트
  /commit              → 변경사항 커밋
```

---

## Related Files

| 파일 | 용도 |
|------|------|
| `references/scoring-model.md` | 점수 모델 정본 (가중치, na 규칙, 상한) |
| `references/10-areas-checklist.md` | 영역별 점검 항목·탐색 방법 |
| `references/severity-guide.md` | P0~P3 판정 기준·리포트 형식 |
| `references/seo-patterns.md` | 프레임워크별 구현 코드 예시 |
| `scripts/fact_density.py` | 팩트 밀도 계측 (한국어·영어) |
| `scripts/score.py` | 두 축 점수 계산 |
| `scripts/test_fact_density.py` | 계측기 검증 |
| `scripts/test_score.py` | 점수 모델 규칙 검증 |
