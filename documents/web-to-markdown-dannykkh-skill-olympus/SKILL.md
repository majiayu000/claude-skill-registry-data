---
name: web-to-markdown
description: >
  웹페이지를 깨끗한 마크다운으로 변환. JS 렌더링 페이지 지원 (Puppeteer + Readability).
  단일/배치 변환, 로그인 필요 페이지, 선택적 콘텐츠 추출.
  "웹 to 마크다운", "페이지 저장", "web2md" 요청에 실행.
  /web2md로 실행.
license: MIT
metadata:
  version: "2.0.0"
---

# Web to Markdown — 웹페이지 → 마크다운 변환

> JS 렌더링 페이지도 깨끗하게 마크다운으로 변환.
> Puppeteer + Readability + Turndown 파이프라인.

## Quick Start

```
/web2md https://example.com                     # 파일로 저장 (자동 이름)
/web2md https://example.com --print              # 터미널 출력
/web2md https://example.com --out ./docs/ref.md  # 경로 지정
/web2md urls.txt                                 # 배치 변환 (파일에 URL 목록)
/web2md https://app.example.com --interactive    # 로그인 필요 페이지
/web2md https://example.com --selector "main"    # 특정 영역만 추출
```

**공식 호출명:** `/web2md`

---

## 사전 확인

```bash
# web2md 설치 확인
command -v web2md || echo "미설치 — 아래 설치 절차 참조"

# 설치 (프로젝트 존재 시)
cd ~/workspace/softaworks/projects/web2md && npm install && npm run build && npm link
```

---

## Workflow

### 1. 단일 URL 변환

```bash
# 자동 이름으로 저장
mkdir -p ./out && web2md 'https://docs.example.com/guide' --out ./out/

# 지정 파일명으로 저장
web2md 'https://docs.example.com/guide' --out ./docs/guide.md

# 터미널 출력 (파이프에 유용)
web2md 'https://docs.example.com/guide' --print
```

### 2. 배치 변환 (여러 URL)

```bash
# URL 목록 파일에서 일괄 변환
mkdir -p ./out
while IFS= read -r url; do
  [ -n "$url" ] && web2md "$url" --out ./out/
done < urls.txt
```

### 3. 로그인 필요 페이지 (Interactive Mode)

```bash
# 브라우저 창이 열리고, 로그인 완료 후 Enter
web2md 'https://app.example.com/dashboard' \
  --interactive \
  --user-data-dir ./tmp/web2md-profile \
  --out ./out/

# 세션 재사용 (두 번째부터 로그인 불필요)
web2md 'https://app.example.com/settings' \
  --user-data-dir ./tmp/web2md-profile \
  --out ./out/
```

### 4. 까다로운 페이지 처리

| 상황 | 옵션 |
|------|------|
| JS 렌더링이 느린 SPA | `--wait-until networkidle2` |
| 특정 요소 로드 대기 | `--wait-for 'main article'` |
| 추가 대기 시간 필요 | `--wait-ms 3000` |
| Chrome 자동 감지 실패 | `--chrome-path /path/to/chrome` |
| 컨테이너/CI 환경 | `--no-sandbox` |
| 디버깅 | `--headful` |

### 5. 선택적 콘텐츠 추출

```bash
# 본문만 추출 (사이드바, 푸터 제외)
web2md 'https://blog.example.com/post' --selector 'article.post-content'

# 여러 선택자 (첫 번째 매칭)
web2md 'https://docs.example.com' --selector 'main, .docs-content, #content'
```

---

## 출력 품질 개선

| 문제 | 해결 |
|------|------|
| 네비게이션/푸터 잔여물 | `--selector`로 범위 한정 |
| 이미지 깨진 상대 경로 | 절대 경로로 자동 변환 (내장) |
| 코드 블록 언어 미감지 | 수동 확인 후 ``` lang 추가 |
| 테이블 깨짐 | GFM 테이블로 변환 (Turndown plugin) |
| 불필요한 광고/배너 | Readability가 자동 제거 |

### 출력 파일 구조

```markdown
---
title: Page Title
url: https://example.com/page
date: 2026-04-16
---

# Page Title

본문 내용...
```

---

## 검증

```bash
# 파일 존재 + 크기 확인
ls -la ./out/*.md

# 빈 파일 감지
find ./out -name "*.md" -empty
```

---

## 비교: 언제 어떤 도구를 쓰나?

| 상황 | 도구 |
|------|------|
| JS 렌더링 필요한 현대 웹앱 | **web2md** (이 스킬) |
| 정적 HTML, 빠른 변환 | `curl` + `pandoc` |
| API 문서 → 코드 참고 | Context7 MCP |
| 웹 검색 결과 가져오기 | Tavily / Exa MCP |

---

## 요구사항

- Node.js 18+
- Chrome/Chromium/Edge (Puppeteer가 자동 감지)
- `web2md` CLI (`npm link` 또는 `npm install -g`)

## Related Files

| 파일 | 역할 |
|------|------|
| `skills/pdf/SKILL.md` | PDF 읽기/변환 |
| `skills/excel2md/SKILL.md` | 엑셀 읽기/변환 |
| `skills/youtube-transcript/SKILL.md` | YouTube 자막 추출 |
