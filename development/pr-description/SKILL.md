---
name: pr-description
description: GitHub PR 템플릿(.github/PULL_REQUEST_TEMPLATE.md)을 사용해서 한국어로 Pull Request 설명을 작성합니다. 사용자가 PR을 생성하거나 PR 설명을 추가/업데이트하도록 요청할 때 사용하세요.
---

# PR Description Generator

이 스킬은 프로젝트의 GitHub PR 템플릿을 기반으로 한국어로 Pull Request 설명을 자동 생성합니다.

## Overview

Git 변경사항을 분석하고 `.github/PULL_REQUEST_TEMPLATE.md` 템플릿의 각 섹션을 채워서 완전한 PR 설명을 작성합니다. bityoungjae.nvim 프로젝트(Lua 기반 Neovim 컬러스킴 플러그인)의 구조와 특성을 이해하고 적절한 내용을 생성합니다.

## Instructions

### Step 1: 사용자 의도 파악

변경사항을 종합적으로 분석하여 사용자의 의도를 명확히 파악하세요:

- 커밋 메시지, 변경된 파일, 코드 diff를 종합 분석
- 변경의 주요 목적이 무엇인지 추론
- 비즈니스 임팩트나 기술적 개선점 파악

**의도가 모호한 경우 AskUserQuestion 도구를 사용하여 질문하세요:**

다음과 같은 상황에서 질문이 필요합니다:

- 여러 가지 해석이 가능한 변경사항
- 변경 이유가 불명확한 경우
- 비즈니스 컨텍스트가 필요한 경우
- 리팩토링인지 버그 수정인지 애매한 경우

질문 예시:

```
AskUserQuestion({
  questions: [{
    question: "이번 변경의 주요 목적은 무엇인가요?",
    header: "변경 목적",
    multiSelect: false,
    options: [
      {
        label: "새로운 기능 추가",
        description: "사용자에게 새로운 기능을 제공"
      },
      {
        label: "버그 수정",
        description: "기존 버그나 오류를 수정"
      },
      {
        label: "성능 개선",
        description: "코드 성능이나 사용자 경험 향상"
      },
      {
        label: "코드 품질 개선",
        description: "리팩토링, 코드 정리 등"
      }
    ]
  }]
})
```

**중요**: 사용자 답변을 받은 후 그 의도에 맞춰 PR 설명을 작성하세요.

### Step 2: PR 템플릿 이해

**Read 도구로** `.github/PULL_REQUEST_TEMPLATE.md` 파일을 읽으세요.

템플릿 구조:

- **관련 이슈**: 이슈 번호 연결
- **변경 사항**: 무엇을 변경했는지
- **변경 이유**: 왜 필요한지
- **추가 컨텍스트**: 리뷰어에게 도움될 정보

### Step 3: 각 섹션 작성

#### 관련 이슈

- Jira, GitHub 이슈, Linear 티켓 등이 있으면 링크
- 없으면 "N/A" 또는 섹션 삭제

#### 변경 사항

- **1-2문단**, 간결하고 명확하게
- 무엇을 변경했는지 (What)
- 비전문가도 이해할 수 있도록

#### 변경 이유

- **왜** 이 변경이 필요한가? (Why)
- 어떤 문제를 해결하는가?
- 비즈니스 또는 기술적 배경

#### 추가 컨텍스트

- 스크린샷이나 데모가 필요한 경우 사용자에게 요청
- 성능 영향, 보안 고려사항 등
- Breaking changes가 있으면 명시

### Step 4: PR 설명 생성 규칙

1. **한국어로 전문적으로 작성**

   - 존댓말 사용 (예: "추가했습니다", "개선했습니다")
   - 기술 용어는 영어 그대로 (예: Component, atom, namespace)

2. **코드와 경로는 백틱으로 감싸기**

   - 파일 경로: `lua/bityoungjae/palette.lua`
   - 함수명: `setup`, `load`, `set_hl`
   - 색상명: `Void`, `Platinum`, `Pale Emerald`

3. **Neovim/Lua 컨텍스트 고려**

   - 하이라이트 그룹 구조 (editor, syntax, treesitter, plugins)
   - 팔레트 색상 참조 방식
   - Neovim API 호출 (`vim.api.nvim_set_hl` 등)
   - 모듈 구조 (`lua/bityoungjae/`)

4. **절대 추가하지 말 것**
   - "🤖 Generated with Claude Code" 같은 푸터
   - "Co-Authored-By: Claude" 같은 서명
   - AI가 작성했다는 언급

### Step 5: PR 생성 또는 업데이트

사용자 요청에 따라:

**PR 생성** (사용자가 요청 시):

```bash
gh pr create --title "feat: 적절한 PR 제목" --body "$(cat <<'EOF'
[생성된 PR 설명]
EOF
)"
```

**PR 설명만 출력** (기본):

- 생성된 PR 설명을 사용자에게 보여주기
- 사용자가 GitHub UI에 붙여넣을 수 있도록

## Examples

### Example 1: 플러그인 하이라이트 추가

**Git 변경사항**:

```
A  lua/bityoungjae/groups/plugins/telescope.lua
M  lua/bityoungjae/groups/init.lua
M  README.md
```

**커밋 메시지**:

```
feat: telescope.nvim 하이라이트 그룹 추가
```

**생성된 PR 설명**:

```markdown
## 관련 이슈

- Closes #12

## 변경 사항

telescope.nvim 플러그인을 위한 하이라이트 그룹을 추가했습니다. 프롬프트, 결과 목록, 프리뷰 영역에 대해 테마와 일관된 색상을 적용했습니다.

## 변경 이유

telescope.nvim은 Neovim에서 가장 많이 사용되는 퍼지 파인더 플러그인입니다. 기본 하이라이트가 bityoungjae 테마와 조화롭지 않아 전용 하이라이트 그룹을 추가했습니다.

## 추가 컨텍스트

Neovim에서 `:Telescope find_files`를 실행하여 새로운 하이라이트를 확인할 수 있습니다.
```

### Example 2: 팔레트 색상 조정

**Git 변경사항**:

```
M  lua/bityoungjae/palette.lua
M  docs/palette.md
```

**커밋 메시지**:

```
fix: Muted Rose 색상 대비 향상
```

**생성된 PR 설명**:

```markdown
## 관련 이슈

N/A

## 변경 사항

`Muted Rose` 색상의 명도를 조정하여 어두운 배경에서의 가독성을 향상시켰습니다.

## 변경 이유

기존 `Muted Rose` (#E08A8A) 색상이 `Void` 배경 (#09090B)에서 WCAG AA 기준 대비율을 충족하지 못했습니다. 에러 메시지와 경고 표시의 가독성 개선이 필요했습니다.

## 추가 컨텍스트

대비율: 기존 4.2:1 → 변경 후 4.8:1 (WCAG AA 기준 4.5:1 충족)
```

## Best Practices

### 1. 명확하고 간결하게

**DO**:

- "telescope.nvim 플러그인을 위한 하이라이트 그룹을 추가했습니다"
- "`palette.lua`의 `Muted Rose` 색상값 조정"

**DON'T**:

- "색상을 개선했습니다"
- "일부 파일 수정"

### 2. 리뷰어 관점

- **무엇을** 테스트할지 구체적으로
- Breaking changes 명확히

## Important Notes

### 절대 하지 말 것

❌ "🤖 Generated with Claude Code" 푸터
❌ "Co-Authored-By: Claude" 서명
❌ AI 작성 언급

### PR 제목 규칙

커밋 메시지 컨벤션 따르기:

- `feat: 새로운 기능 추가`
- `fix: 버그 수정`
- `refactor: 코드 리팩토링`
- `style: 스타일/UI 변경`
- `chore: 빌드/설정 변경`

### 프로젝트별 참고사항

- **CLAUDE.md**: 코드 스타일, 네이밍 규칙, 아키텍처
- **main 브랜치**: 기본 브랜치로 main 사용
- **테스트**: Neovim에서 `:colorscheme bityoungjae`로 테마 적용 확인
- **프로젝트 구조**:
  - `lua/bityoungjae/palette.lua`: 색상 팔레트 정의
  - `lua/bityoungjae/groups/`: 하이라이트 그룹 (editor, syntax, plugins 등)
  - `lua/lualine/themes/bityoungjae.lua`: Lualine 테마
