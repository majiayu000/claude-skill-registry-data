---
name: typst-korean
description: Typst 문서 작성을 도와줍니다. 프리텐다드(Pretendard) 폰트를 기본으로 설정하고 한글 문서에 적합한 설정을 안내합니다. Typst 문법, 폰트 설정, 페이지 레이아웃 관련 질문에 사용합니다.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Typst Korean - 한글 문서 작성 지원

Typst로 한글 문서를 작성할 때 도움을 제공합니다.

## 기본 폰트 설정 (프리텐다드)

사용자가 Typst 문서를 새로 만들 때, 다음 기본 설정을 권장합니다:

```typst
#set text(
  font: "Pretendard",
  lang: "ko",
  region: "KR",
)
```

### 프리텐다드 폰트 설치

프리텐다드 폰트가 시스템에 없는 경우:

1. **다운로드**: https://github.com/orioncactus/pretendard/releases
2. **Typst에서 사용**: `--font-path` 옵션으로 폰트 경로 지정

```bash
typst compile --font-path ./fonts document.typ
```

### 폰트 확인

```bash
typst fonts | grep -i pretendard
```

## Typst 문법 참조

자세한 문법 정보는 [reference.md](reference.md)를 참조하세요.

## 주의사항

- 사용자가 특별히 요청하지 않는 한 문서 구조나 서식을 강제하지 마세요
- 사용자의 기존 스타일을 존중하고, 필요한 부분만 수정하세요
- 프리텐다드 외의 폰트를 원하면 그에 맞춰 안내하세요
