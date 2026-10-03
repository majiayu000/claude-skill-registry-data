---
name: reddit-researcher
description: "Reddit에서 잠재 고객과 수요를 찾아주는 시장 조사 스킬. 키워드 기반 포스트 수집, 리드 스코어링, Pain Point 분류, 경쟁사 언급 추적. /reddit-researcher로 실행."
license: MIT
metadata:
  version: "1.1.0"
---

# Reddit Researcher — 시장 조사 + 리드 스코어링

Reddit 공개 데이터를 수집하여 잠재 고객을 찾고, 리드를 스코어링하고, Pain Point를 분류합니다.
WebSearch와 WebFetch만으로 동작하며, 별도 API 키가 필요 없습니다.

## 적용 시점

- `/reddit-researcher` 명시적 실행
- "시장 조사해줘", "Reddit에서 고객 찾아줘", "수요 조사" 요청 시

---

## Setup (최초 1회)

이 스킬은 `config.json`에 설정이 필요합니다.

1. `config.json`을 읽는다 (`skills/reddit-researcher/config.json` 또는 현재 CLI의 글로벌 스킬 경로)
2. 빈 필드가 있으면 현재 CLI의 질문 방식으로 사용자에게 질문한다
3. 답변을 `config.json`에 저장한다
4. 이후 실행 시에는 `config.json`에서 자동으로 읽는다

| 항목 | 설명 | 예시 |
|------|------|------|
| `target_subreddits` | 기본으로 조사할 서브레딧 목록 | `["SaaS", "startups", "webdev"]` |
| `keywords` | 기본 검색 키워드 목록 | `["SaaS boilerplate", "starter kit"]` |
| `language` | 리포트 출력 언어 (`ko` / `en`) | `ko` |
| `max_posts_per_subreddit` | 서브레딧당 최대 수집 포스트 수 | `25` |

**Setup 로직:**

```
config.json 읽기
  ├─ target_subreddits 비어있음? → "기본으로 조사할 서브레딧을 입력해주세요 (쉼표 구분, 예: SaaS,startups,webdev)"
  │                                 → 입력 없으면 기본값(r/SaaS, r/startups 등) 사용
  ├─ keywords 비어있음? → "기본 검색 키워드를 입력해주세요 (쉼표 구분, 건너뛰려면 Enter)"
  ├─ language 확인 → "리포트 언어를 선택해주세요 (ko / en, 기본값: en)"
  └─ 답변 수집 후 config.json에 저장 → 이후 자동 사용
```

> **config.json 값은 Step 1에서 사용자 입력의 기본값으로 사용됩니다.** 사용자는 실행 시 항상 덮어쓸 수 있습니다.

---

## Step 1: 사용자 입력 수집

### 필수 입력

사용자에게 아래를 질문합니다. 이미 제공된 정보는 다시 묻지 않습니다.

**1. 타겟 키워드** (쉼표 구분)
```
예: "SaaS boilerplate, starter kit, landing page template"
```

**2. 서브레딧 목록** (기본값 제공, 사용자가 추가/변경 가능)
```
기본값:
  r/SaaS, r/startups, r/Entrepreneur, r/webdev,
  r/nextjs, r/reactjs, r/indiehackers, r/microsaas,
  r/smallbusiness, r/nocode
```

**3. ICP (Ideal Customer Profile)**
```
예: "비개발자 창업자, 1-5인 팀, MVP 빠르게 런칭하고 싶은 사람"
```

### 선택 입력

| 항목 | 기본값 |
|------|--------|
| 검색 기간 | 최근 30일 |
| 최소 upvote | 3 |
| 경쟁사 이름 | (없음) |

---

## Step 2: 데이터 수집

### 수집 방법 (우선순위 순)

> **2026-07 기준**: Reddit `.json` 엔드포인트(www/old/api.reddit.com 모두)는 비로그인 CLI 요청에 대부분 **403**을 반환합니다 (브라우저 User-Agent를 붙여도 차단). 반면 **old.reddit.com HTML 페이지는 정상(200)** 응답합니다. JSON API는 프로브 1회만 시도하고, 차단이면 즉시 HTML 경로로 전환하세요. 요청마다 재시도하면 대기 시간이 누적되어 스킬이 멈춘 것처럼 보입니다.

**방법 0: 차단 프로브 (필수, 최초 1회)**

수집 시작 전 JSON API에 딱 1회 테스트 요청:

```
https://www.reddit.com/r/{첫 subreddit}/search.json?q={첫 keyword}&restrict_sr=1&limit=1
```

- 200 → 방법 1 (JSON API) 사용
- 403/429/기타 실패 → **이번 실행 전체에서 JSON API를 건너뛰고** 방법 2로 전환 (요청별 재시도 금지)

**방법 1: Reddit JSON API (프로브 통과 시에만)**

```
URL: https://www.reddit.com/r/{subreddit}/search.json?q={keyword}&restrict_sr=1&sort=relevance&t=month&limit=25
```

WebFetch로 호출하여 JSON 파싱. 응답 구조:
```json
{
  "data": {
    "children": [
      {
        "data": {
          "title": "포스트 제목",
          "selftext": "본문",
          "subreddit": "서브레딧",
          "author": "작성자",
          "created_utc": 1234567890,
          "ups": 42,
          "num_comments": 15,
          "permalink": "/r/sub/comments/..."
        }
      }
    ]
  }
}
```

**방법 2: old.reddit.com HTML 검색 (기본 경로, 2026-07 동작 검증)**

```
URL: https://old.reddit.com/r/{subreddit}/search?q={keyword}&restrict_sr=1&sort=relevance&t=month
```

WebFetch로 호출하여 HTML에서 추출. 검색 결과 1건당 아래 마커가 포함됩니다:

| 필드 | HTML 마커 |
|------|-----------|
| title + permalink | `<a ... class="search-title ...">제목</a>` (href가 포스트 URL) |
| ups | `search-score">N points` |
| num_comments | `search-comments ...">N comments` |
| author | `class="author ..."` 링크 텍스트 |
| created_utc | `search-time">submitted` 옆 `<time datetime="...">` |
| subreddit | permalink URL의 `/r/{subreddit}/` 부분 |

- 페이지네이션: 결과 하단 next 링크의 `after=` 파라미터 (25건 단위)
- 본문(selftext)은 검색 결과 페이지에 없음 → **필터 통과 + 예비 점수 상위 후보만** permalink를 old.reddit.com 도메인으로 WebFetch하여 본문 확보 (전건 fetch 금지, 호출 수 절약)

**방법 3: 검색 엔진 폴백 (HTML까지 차단된 경우)**

Tavily MCP(`mcp__tavily__*`)가 연결되어 있으면 우선 사용하고, 없으면 WebSearch:

```
site:reddit.com/r/{subreddit} "{keyword}"
```

이 경로는 upvote/댓글 수를 얻지 못하는 경우가 많습니다 → Step 3의 데이터 결측 규칙으로 스코어링을 보정합니다.

### Rate Limiting 규칙

- 각 WebFetch 호출 사이 **최소 2초** 대기
- **Fast-fail**: 같은 방법에서 403/429가 2회 연속 발생 → 그 방법은 이번 실행에서 포기하고 다음 방법으로 전환 (요청별 10초 대기 재시도 금지 — 대기 누적으로 실행이 멈춘 것처럼 보이는 원인)
- 총 API 호출 100회 초과 시 수집 중단

### 수집 데이터 포인트

| 필드 | 설명 |
|------|------|
| title | 포스트 제목 |
| selftext | 본문 (500자까지) |
| subreddit | 서브레딧 |
| author | 작성자 (u/username) |
| created_utc | 작성 시간 |
| ups | Upvote 수 |
| num_comments | 댓글 수 |
| permalink | 포스트 URL |

---

## Step 3: 리드 스코어링

수집된 각 포스트에 대해 **10점 만점**으로 스코어링합니다.

### 스코어링 기준

| 카테고리 | 배점 | 기준 |
|---------|------|------|
| **ICP 적합도** | 0~4점 | 작성자가 ICP에 부합하는 정도 |
| **긴급도** | 0~2점 | "지금 당장", "급하게", "ASAP" 등 긴급 신호 |
| **최신성** | 0~2점 | 7일 이내 = 2점, 14일 이내 = 1점, 이후 = 0점 |
| **참여도** | 0~2점 | upvote + 댓글 수 기반 |

### ICP 적합도 세부 기준 (0~4점)

```
4점: ICP 완벽 매칭 + 구매 의사 표현 ("돈 내고라도", "유료 서비스 추천")
3점: ICP 매칭 + 명확한 니즈 표현 ("~하는 도구 있나요?", "~가 필요합니다")
2점: ICP 부분 매칭 + 관련 토론 참여
1점: 관련 주제 언급만
0점: ICP 미해당 또는 무관
```

### 긴급도 신호 키워드

```
높음 (2점): "urgent", "ASAP", "today", "this week", "급하게", "지금 당장"
중간 (1점): "soon", "looking for", "need", "찾고 있습니다", "필요합니다"
낮음 (0점): 단순 토론, 비교, 일반 질문
```

### 참여도 기준

```
2점: upvote ≥ 20 또는 댓글 ≥ 10
1점: upvote ≥ 5 또는 댓글 ≥ 3
0점: 그 외
```

> **데이터 결측 시 (검색 엔진 폴백 경로)**: upvote/댓글 수를 얻지 못한 포스트는 참여도 항목을 제외하고, `(획득 점수 / 8) × 10`을 반올림하여 10점 스케일로 정규화합니다. 리포트에 결측 여부를 표기합니다.

---

## Step 4: 거짓 양성 필터링

아래 패턴에 해당하면 **자동 제외**합니다:

| # | 패턴 | 제외 이유 |
|---|------|----------|
| 1 | 작성자가 [deleted] 또는 AutoModerator | 봇/삭제 계정 |
| 2 | 제목에 "[Hiring]", "[For Hire]" 포함 | 구인 게시물 |
| 3 | 본문에 자기 제품 URL 3개 이상 | 스팸/자기홍보 |
| 4 | upvote 0 이하 (downvote 많음) | 커뮤니티 거부 |
| 5 | "I built", "I made", "Show HN" 패턴 | 쇼케이스 (구매자 아님) |
| 6 | 본문 없이 링크만 있는 포스트 | 콘텐츠 없음 |
| 7 | 댓글 0개 + upvote 1 | 관심 없는 포스트 |
| 8 | 서브레딧 규칙 위반 Flair (Removed 등) | 삭제된 포스트 |
| 9 | 같은 작성자의 포스트가 3개 이상 | 스팸 계정 |
| 10 | "affiliate", "referral" 포함 | 어필리에이트 |
| 11 | 작성일이 검색 기간 밖 | 오래된 데이터 |
| 12 | 제목/본문이 키워드와 무관 (검색 엔진 노이즈) | 관련성 없음 |

---

## Step 5: Pain Point 분류

필터링 통과한 포스트들에서 Pain Point를 추출하고 분류합니다:

| 카테고리 | 설명 | 예시 키워드 |
|---------|------|-----------|
| **가격** | 비용 불만, 대안 요청 | "expensive", "free alternative", "비싸다" |
| **기능 부재** | 특정 기능 요청 | "wish it had", "doesn't support", "~기능이 없어" |
| **복잡성** | 사용 어려움 | "too complicated", "steep learning curve", "어렵다" |
| **성능** | 느림, 불안정 | "slow", "crashes", "downtime", "느리다" |
| **통합** | 연동 문제 | "integration", "API", "connect with", "연동" |
| **지원** | 고객 지원 불만 | "support", "no response", "답변이 없다" |

---

## Step 6: 경쟁사 분석 (선택)

사용자가 경쟁사 이름을 제공한 경우:

- 각 경쟁사 이름이 언급된 포스트 추적
- 언급 맥락 분류: 추천 / 불만 / 비교 / 대안 요청
- 경쟁사별 sentiment 요약 (긍정/부정/중립)

---

## Step 7: 리포트 출력

### 7-1. CSV 데이터 파일

`docs/reddit-research/leads-{날짜}.csv`에 저장:

```csv
score,title,subreddit,author,ups,comments,date,url,pain_points,icp_match
8,"Need a SaaS boilerplate urgently",SaaS,u/founder123,42,15,2026-03-10,https://reddit.com/...,가격;복잡성,높음
6,"Looking for starter kit recommendations",startups,u/indie_dev,12,8,2026-03-08,https://reddit.com/...,기능부재,중간
```

### 7-2. 마크다운 요약 리포트

`docs/reddit-research/report-{날짜}.md`에 저장:

```markdown
# Reddit 시장 조사 리포트

**조사일**: {날짜}
**키워드**: {키워드 목록}
**서브레딧**: {서브레딧 목록}
**수집 포스트**: {N}개 → 필터 후 {N}개

---

## 핫 리드 (8~10점)

| 점수 | 제목 | 서브레딧 | 작성자 | URL |
|------|------|---------|--------|-----|
| 9 | ... | r/SaaS | u/... | [링크](...) |

## 웜 리드 (5~7점)

| 점수 | 제목 | 서브레딧 | 작성자 | URL |
...

## 콜드 리드 (1~4점)

(요약만, 개별 목록 생략)

---

## Pain Point 분석

| 카테고리 | 언급 횟수 | 대표 포스트 |
|---------|---------|-----------|
| 가격 | 12건 | "Too expensive for a solo founder..." |
| 복잡성 | 8건 | "Spent 3 days just setting up auth..." |

## 경쟁사 언급 현황

| 경쟁사 | 언급 | 긍정 | 부정 | 대표 의견 |
|--------|------|------|------|----------|
| CompetitorA | 15건 | 8 | 7 | "Great but too expensive" |

---

## 액션 아이템

1. **즉시 접근 가능**: 핫 리드 {N}건에 DM/댓글로 접근
2. **콘텐츠 기회**: Pain Point "{가장 많은 카테고리}"를 다루는 블로그 포스트 작성
3. **기능 로드맵**: "{요청 많은 기능}" 우선 개발 고려
```

---

## 주의사항

- Reddit API rate limit을 반드시 준수합니다 (요청 간 2초)
- 개인정보(이메일, 연락처)를 수집하지 않습니다
- 공개 포스트만 수집합니다 (비공개 서브레딧 접근 불가)
- `.json` 엔드포인트는 비로그인 클라이언트에 403이 일반적입니다 → 프로브 1회 후 old.reddit.com HTML 경로 사용
- HTML 경로까지 차단되면 검색 엔진 폴백(Tavily 우선, 없으면 WebSearch)으로 대체합니다
- 차단 시 재시도 대기를 누적하지 않습니다 (fast-fail 후 다음 방법으로 전환)

---

## 다음 단계 안내

```
✅ Reddit 시장 조사 완료!

리포트: docs/reddit-research/report-{날짜}.md
데이터: docs/reddit-research/leads-{날짜}.csv

다음 단계 (선택):
  /planner    → 조사 결과 기반으로 PRD 작성
  /chronos    → 발견된 기능 요청 구현
```
