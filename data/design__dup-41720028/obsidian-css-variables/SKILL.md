---
name: obsidian-css-variables
description: "Obsidian CSS variables 공식 문서를 참조하여 테마/플러그인 개발 시 올바른 CSS 변수 사용을 안내합니다. WebFetch 도구와 Jina Reader API를 사용하여 최신 문서를 마크다운으로 가져올 수 있습니다."
---

# Obsidian CSS Variables 참조 스킬

Obsidian 테마 및 플러그인 개발 시 CSS 변수를 올바르게 사용할 수 있도록 공식 문서를 참조하는 스킬입니다.

## 개요

Obsidian은 테마와 플러그인이 일관된 UI를 제공할 수 있도록 CSS 변수 시스템을 제공합니다. 이 스킬을 통해:

- 자주 사용하는 기본 CSS 변수를 빠르게 참조
- Jina Reader API로 최신 공식 문서를 마크다운 형식으로 가져오기
- 카테고리별 CSS 변수 문서 접근

## CSS 변수 카테고리

| 카테고리 | 설명 | 예시 |
|---------|------|------|
| **Foundations** | 색상, 간격, 타이포그래피 등 기본 추상화 | `--background-primary`, `--font-text` |
| **Components** | 버튼, 모달, 체크박스 등 UI 컴포넌트 | `--button-height`, `--modal-border-width` |
| **Editor** | 에디터 콘텐츠 스타일링 | `--h1-size`, `--link-color` |
| **Plugins** | 캔버스, 그래프 등 핵심 플러그인 | `--graph-line`, `--canvas-color` |
| **Window** | 앱 윈도우 프레임 관련 | `--ribbon-width`, `--status-bar-font-size` |

## Jina Reader API 사용법

최신 문서를 가져오려면 WebFetch 도구를 사용하여 다음 URL 패턴으로 요청합니다:

```
https://r.jina.ai/{원본_URL}
```

### 예시

```typescript
// 메인 CSS Variables 문서 가져오기
WebFetch("https://r.jina.ai/https://docs.obsidian.md/Reference/CSS+variables/CSS+variables")

// Foundations 카테고리 문서 가져오기
WebFetch("https://r.jina.ai/https://docs.obsidian.md/Reference/CSS+variables/Foundations/Colors")
```

## 참조 문서

- [common-variables.md](references/common-variables.md) - 자주 사용하는 기본 CSS 변수
- [jina-reader-urls.md](references/jina-reader-urls.md) - 카테고리별 WebFetch URL 목록

## 사용 예시

### 1. 빠른 색상 변수 참조
```css
/* Obsidian 테마 색상 변수 사용 */
.my-plugin-container {
  background-color: var(--background-primary);
  color: var(--text-normal);
  border: 1px solid var(--background-modifier-border);
}
```

### 2. 최신 문서 가져오기
CSS 변수에 대한 상세 정보가 필요할 때:
1. `references/jina-reader-urls.md`에서 해당 카테고리 URL 확인
2. WebFetch 도구로 해당 URL의 마크다운 문서 가져오기

### 3. 컴포넌트 스타일링
```css
/* 버튼 스타일 - Obsidian 기본 스타일과 일관성 유지 */
.my-button {
  height: var(--input-height);
  padding: var(--size-4-2) var(--size-4-4);
  border-radius: var(--radius-s);
  font-size: var(--font-ui-small);
}
```

## 주의사항

- CSS 변수는 Obsidian 버전에 따라 변경될 수 있으므로, 최신 문서를 확인하세요
- 플러그인에서는 Obsidian 기본 변수를 최대한 활용하여 테마 호환성을 유지하세요
- 커스텀 색상보다 `--text-*`, `--background-*` 계열 변수를 사용하는 것이 좋습니다
