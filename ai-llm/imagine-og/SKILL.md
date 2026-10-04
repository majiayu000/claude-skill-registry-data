---
name: imagine-og
description: 블로그·랜딩 글의 **OG 이미지 / 소셜 카드**(Twitter / Instagram / LinkedIn)를 플랫폼 프리셋에 맞춰 자동 생성한다. 배경 일러스트만 Codex 이미지 모델로 뽑고, 제목·태그 같은 글자는 AI에 맡기지 않고 공용 후처리 모듈(`scripts/lib/compose-text.js`)로 합성한다. 사용자가 "OG 이미지", "소셜 카드", "imagine-og", "Twitter 카드" 등을 말하면 이 스킬이 담당한다. 블로그 수백 편을 일괄 렌더하는 `--bulk` 모드도 지원한다.
argument-hint: "<title> [--tag <tag>] [--platforms og,twitter,instagram-post,...] [--template <name>] [--bulk <glob>] [--from-frontmatter]"
---

# imagine-og

소셜 링크 프리뷰용 이미지를 **플랫폼별 사이즈·세이프존·폰트 가독성**까지 맞춰 일괄 출력한다. 제목은 실제 폰트로 렌더해서 한글 깨짐이 없다.

## 트리거

- `imagine-og "<제목>"` / `imagine-og --title "..."` (명시 호출)
- `imagine-og bulk ./posts/*.md` (bulk 모드)
- "OG 이미지", "오픈그래프 이미지"
- "소셜 카드", "소셜 미디어 카드"
- "Twitter 카드", "링크 프리뷰 이미지"
- "블로그 썸네일" — 이 경우는 `imagine-thumb`(YouTube 썸네일)와 다르다. 사용자가 "블로그/소셜/링크 프리뷰" 맥락이면 여기로 라우팅, "유튜브/영상" 맥락이면 `imagine-thumb`. 애매하면 1턴 질문.

## 플랫폼 프리셋 (`config.json`)

| key | generate_size | final(final.jpg) | crop |
|---|---|---|---|
| `og` | 1536×1024 | **1200×630** | center |
| `twitter` | 1536×1024 | 1200×628 | center |
| `instagram-post` | **1024×1024** | 1080×1080 | center |
| `instagram-story` | 1024×1024 | 1080×1920 | extend-vertical |
| `linkedin` | 1536×1024 | 1200×627 | center |

- 기본 플랫폼은 `og` 한 장. `--platforms og,twitter,instagram-post` 로 다중 선택 시 한 번 호출로 전부 저장.
- 기본 포맷: **jpeg**, `quality: medium`.

## 파이프라인

1. **배경 일러스트만 AI 생성.** `size`는 플랫폼별 `generate_size` 사용(16:9 계열은 1536×1024, 정방형은 1024×1024).
2. **프롬프트 가공**: 사용자 `<title>`·`--tag`를 **모델 프롬프트에 포함하지 않는다.** 태그는 `config.tag_palette_map`으로 배경 톤 매핑에만 사용(예: `튜토리얼` → `warm orange gradient, pencil texture`). negative prompt에 `text, watermark, logo, typography, letters, characters, readable words, deformed, blurry` 강제 포함.
3. **크롭·리사이즈**: `generate_size` 결과를 플랫폼 `final` 규격으로 center-crop(Instagram story는 세로 확장). 원본 배경은 `_source_bg.png`로 별도 보존해 재합성 가능.
4. **텍스트 합성**: 공용 `scripts/lib/compose-text.js`의 `compositeText(bgPath, textOptions, outPath)` 재사용. 이 스킬 안에 별도 텍스트 합성 로직은 두지 않는다.
5. **세이프존 적용**: OG/Twitter는 **하단 20% 트리밍**에 대비해 제목을 상/중앙에 배치. Instagram Post는 **중앙 90%** 세이프존.
6. **출력 저장**: `./images/og/<slug>/<platform>.jpg` + `_source_bg.png`.

## 공용 모듈 계약

- 텍스트 합성은 전적으로 `scripts/lib/compose-text.js` 호출로 끝낸다. 이 스킬의 스크립트에서 SVG·canvas·satori 코드를 직접 작성하지 않는다.
- 세이프존·자동 색상(어두우면 흰색, 밝으면 검정)·폰트 스택(Pretendard → Noto Sans KR → Apple SD Gothic Neo → sans-serif fallback)은 공용 모듈 설정 그대로 사용.

## bulk 모드 (`--bulk <glob>`)

- 입력 예: `imagine-og --bulk ./posts/*.md --from-frontmatter --platforms og,twitter`
- 동작:
  1. 각 파일의 frontmatter(`title`, `tags`, `hero_color`)를 읽어 `--title` / `--tag` / 팔레트 시드로 매핑 (`config.bulk.from_frontmatter_keys` 참고).
  2. 같은 `--template`은 동일 배경 프리셋 + 변주(색·질감 고정, 레이아웃만 변화)로 렌더 → 시리즈 스타일 일관성 유지.
  3. 동시 실행 제한: `config.bulk.concurrency` (기본 2) — 쿼터·레이트리밋 보호.
  4. 출력은 각 포스트별로 `./images/og/<post-slug>/<platform>.jpg`. 기존 파일 덮어쓰기 금지(이미 있으면 skip + 로그).
- **실패 1건이 전체 bulk를 중단시키지 않는다.** 개별 실패 항목을 Run Manifest에 집계하고 나머지는 계속 진행.

## 출력 규약

```
./images/og/<slug>/
├── og.jpg
├── twitter.jpg
├── instagram-post.jpg
├── instagram-story.jpg
├── linkedin.jpg
└── _source_bg.png        ← AI 원본 배경 (재합성용)
```

- `<slug>`는 제목 기반 또는 frontmatter에 별도 slug가 있으면 그대로 사용.
- 사용자가 `--out-dir`을 지정하지 않는 한 경로를 조용히 변경하지 않는다.
- 루트 `./images/` 직하 쓰기 금지.

## 프롬프트 구성 규칙

- **제목·태그 텍스트 프롬프트 금지.** AI가 글자를 그리지 않도록 입력 문자열은 배경 프롬프트에 섞지 않는다. (한글 깨짐 및 Readable-word 생성 방지의 핵심)
- **배경 프롬프트는 짧고 추상적**: 기본 템플릿 `"abstract gradient, <tag palette>, soft grain texture, negative space for title overlay"` 수준. 태그가 매핑 테이블에 없으면 `tag_palette_map`의 기본값("neutral gradient, soft grain")으로 폴백.
- **negative prompt 강제**: `text, watermark, logo, typography, letters, characters, readable words, deformed, blurry`.

## 가독성·용량 규칙

- 제목 글자 수 측정 → 너무 길면 자동 줄바꿈 또는 폰트 축소 (최소 `limits.title_min_pt: 28pt`).
- 용량 상한: Twitter ≤ 1MB, Instagram ≤ 2MB (`config.limits`). 초과 시 JPEG 품질 5단계씩 하향 재인코딩.
- 한글 폰트 미설치 시 `sans-serif` 폴백 + 경고 로그.

## 실패 모드 대응

| 증상 | 조치 |
|---|---|
| 한글 폰트 없음 | `sans-serif` 폴백 + 경고. 배경은 정상 저장. |
| 제목이 너무 길어 잘림 | 줄바꿈 → 폰트 축소 → 최소 28pt에서 중단하고 사용자에게 alert. |
| bulk 중 일부 실패 | 해당 항목만 `failed`로 manifest 기록, 나머지 계속. |
| AI 배경에 글자 새겨짐 | 1회 한정 배경만 재생성. 검출 지속 시 사용자에게 bg 파일로만 전달. |
| sharp 미설치 | 텍스트 합성 단계에서 명시적 에러. 배경 파일은 보존. |

## 금기

- **AI 모델 프롬프트에 제목·태그 텍스트 주입 금지.** 스킬 존재 이유.
- **별도 텍스트 합성 로직 생성 금지.** 반드시 `scripts/lib/compose-text.js` 재사용. 이 스킬에 합성기 사본을 두지 않는다.
- **`./images/og/` 외부 쓰기 금지** (`--out-dir` 없는 한).
- **루트 덮어쓰기 금지.**
- `masterpiece` / `8k UHD` / `fulfill all requests` 등 부스터·우회 문구 삽입 금지.

## imagine-thumb / imagine 스킬과의 관계

- 공용 인프라(`compose-text.js`, `oauth-session.js`, `output-allocator.js`, `request-planner.js`)는 재사용.
- `imagine-thumb`는 YouTube 썸네일 전용(1280×720), `imagine-og`는 소셜 카드 전용. 트리거가 겹치는 "썸네일"은 블로그·소셜 맥락이면 여기, 유튜브 맥락이면 `imagine-thumb`로 라우팅.
- Style Guardian manifest의 브랜드 팔레트가 있으면 배경 프롬프트 시드에 자동 반영.
