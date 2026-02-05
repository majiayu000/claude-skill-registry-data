---
name: commit-helper
description: git 변경사항을 분석하고 Conventional Commits 패턴에 따라 한국어로 커밋 메시지를 작성하여 커밋을 생성합니다. 사용자가 커밋을 만들어달라고 요청하거나, 변경사항을 커밋해야 할 때 사용합니다.
model: claude-haiku-4-5
---

# Commit Helper

## Overview

이 스킬은 git 저장소의 변경사항을 분석하여 Conventional Commits 패턴에 따라 한국어로 커밋 메시지를 작성하고 커밋을 생성합니다. 변경사항이 여러 유형에 걸쳐 있는 경우 논리적으로 분류하여 여러 개의 커밋으로 나눕니다.

## Instructions

### Step 1: 사용자 의도 파악

변경사항을 종합적으로 분석하여 사용자의 의도를 명확히 파악하세요:

- git diff, 변경된 파일, 코드 내용을 종합 분석
- 변경의 주요 목적이 무엇인지 추론
- 적절한 커밋 타입 (feat/fix/refactor 등) 판단
- 프로젝트의 기존 커밋 메시지 스타일 참고

**의도가 모호한 경우 AskUserQuestion 도구를 사용하여 질문하세요:**

다음과 같은 상황에서 질문이 필요합니다:

- 여러 가지 해석이 가능한 변경사항
- 변경 이유가 불명확한 경우
- 기능 추가인지 버그 수정인지 애매한 경우
- 리팩토링인지 기능 개선인지 구분이 어려운 경우

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
        label: "리팩토링",
        description: "동작은 유지하면서 코드 개선"
      },
      {
        label: "문서/설정 변경",
        description: "문서 업데이트, 빌드 설정 등"
      }
    ]
  }]
})
```

**중요**: 사용자 답변을 받은 후 그 의도에 맞춰 커밋 타입과 메시지를 작성하세요.

### Step 2: 변경사항 분류

변경사항을 다음 기준으로 논리적 그룹으로 분류:

1. **변경 타입별 분류** (Conventional Commits 타입 기준)
2. **기능/모듈별 분류** (연관된 변경사항끼리 그룹화)
3. **파일 종류별 분류** (문서, 소스코드, 설정 파일 등)

각 그룹은 하나의 독립적인 커밋이 될 수 있어야 합니다.

### Step 3: Conventional Commits 타입 결정

각 그룹에 적합한 타입 선택:

- **feat**: 새로운 기능 추가
- **fix**: 버그 수정
- **docs**: 문서만 변경 (코드 변경 없음)
- **style**: 코드 의미에 영향 없는 변경 (공백, 포맷팅, 세미콜론 등)
- **refactor**: 버그 수정이나 기능 추가 없는 코드 개선
- **test**: 테스트 추가, 테스트 리팩토링
- **chore**: 빌드 업무, 패키지 매니저 설정 등
- **perf**: 성능 개선

### Step 4: 한국어 커밋 메시지 작성

각 그룹에 대해 다음 형식으로 메시지 작성:

```
<type>: <제목>

<본문>
```

**제목 작성 규칙**:

- 50자 이내로 간결하게
- 명령형 현재 시제 사용 (예: "추가", "수정", "제거")
- 마침표 없이 작성
- 무엇을 변경했는지 명확히 표현

**본문 작성 규칙** (선택사항, 복잡한 변경사항인 경우):

- 제목과 본문 사이 빈 줄 추가
- 각 줄은 72자 이내
- 변경 이유와 변경 전/후 동작 차이 설명
- 여러 변경사항이 있으면 불릿 포인트 사용

**중요: 다음 규칙을 반드시 준수**:

- 순수 한국어로만 작성
- Claude Code, Claude, AI 등 도구 관련 언급 절대 금지
- Co-Authored-By 라인 추가 금지
- emoji 사용 금지
- 개발자가 직접 작성한 것처럼 자연스럽게 작성

### Step 5: 커밋 실행

각 그룹에 대해 순차적으로:

1. **Bash tool로 해당 파일들 스테이징**

   ```bash
   git add <file1> <file2> ...
   ```

2. **Bash tool로 커밋 실행**

   ```bash
   git commit -m "$(cat <<'EOF'
   <type>: <제목>

   <본문>
   EOF
   )"
   ```

3. **Bash tool로 커밋 결과 확인**

   ```bash
   git log -1 --stat
   ```

4. 다음 그룹으로 이동하여 반복

### Step 6: 완료 보고

모든 커밋 완료 후:

1. 생성된 커밋 목록 요약
2. 각 커밋의 타입과 제목 표시
3. 추가 작업 필요 여부 확인

## Examples

### Example 1: 플러그인 하이라이트 추가

**변경사항**:

- `lua/bityoungjae/groups/plugins/telescope.lua` 추가
- `lua/bityoungjae/groups/init.lua`에 telescope 그룹 등록

**커밋 메시지**:

```
feat: telescope.nvim 하이라이트 그룹 추가

- TelescopeNormal, TelescopeBorder 등 기본 하이라이트 정의
- 프롬프트, 결과, 프리뷰 영역별 색상 설정
- 선택 항목 강조 스타일 적용
```

### Example 2: 여러 타입의 변경사항

**변경사항**:

- `README.md` 업데이트 (문서)
- `lua/bityoungjae/palette.lua` 색상값 수정 (버그)
- `lua/bityoungjae/groups/plugins/neo-tree.lua` 추가 (기능)

**커밋 1**:

```
docs: README에 지원 플러그인 목록 추가
```

**커밋 2**:

```
fix: Muted Rose 색상 대비 부족 문제 수정

에러 메시지 가독성 향상을 위해 명도 조정
```

**커밋 3**:

```
feat: neo-tree.nvim 하이라이트 그룹 추가

- NeoTreeNormal, NeoTreeFloatBorder 정의
- 디렉토리, 파일, git 상태별 색상 설정
- 선택 및 포커스 상태 스타일 적용
```

### Example 3: 리팩토링

**변경사항**:

- `lua/bityoungjae/groups/editor.lua`의 중복 색상 참조 제거
- `lua/bityoungjae/groups/syntax.lua`의 중복 색상 참조 제거
- `lua/bityoungjae/util.lua`에 공통 함수 추출

**커밋 메시지**:

```
refactor: 하이라이트 그룹 공통 유틸 함수 추출

- blend_colors 헬퍼 함수 추가
- 중복된 색상 계산 로직 통합
- editor, syntax 그룹에서 재사용
```

## Best Practices

1. **원자적 커밋**: 각 커밋은 하나의 논리적 변경사항만 포함
2. **의미 있는 제목**: 커밋 로그만 봐도 변경 내용 파악 가능하게
3. **일관된 형식**: Conventional Commits 패턴 엄격히 준수
4. **적절한 분류**: 변경사항이 많으면 여러 커밋으로 분할
5. **자연스러운 메시지**: 개발자가 직접 작성한 것처럼 자연스럽게

## Common Pitfalls

❌ **피해야 할 것**:

- "Claude Code로 생성", "AI 작성" 등의 언급
- Co-Authored-By: Claude 라인 추가
- 너무 많은 변경사항을 하나의 커밋에 포함

✅ **올바른 예**:

- 순수 한국어 커밋 메시지
- 명확한 타입 분류
- 적절한 커밋 단위 분할
- 개발자의 자연스러운 어투
