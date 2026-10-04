---
name: managing-branch-pr-workflow
description: Enforce branch-based workflow with meaningful Korean commits and PR creation for traceable decision history.
---

# 브랜치 + PR 기반 작업 워크플로우

## 설명

사용자의 요청(User Request)은 main 브랜치에 auto-commit으로 기록되어 생각의 흐름을 보존합니다.
Claude의 작업은 feature 브랜치에서 수행하며, 각 커밋에 WHY(의사결정 근거)를 포함하여 작업 이력을 추적할 수 있도록 합니다.
작업 완료 후 PR을 생성하여 전체 변경사항의 요약과 근거를 문서화합니다.

## 워크플로우

### 1. 계획 수립 후 브랜치 생성

```bash
git checkout -b feature/{작업-설명}
```

- 브랜치명은 영문 소문자, 하이픈 구분 (예: `feature/cqrs-refactor`, `feature/sqlite-persistence`)
- 계획(Plan)이 승인된 직후, 코드 변경 전에 생성

### 2. 첫 번째 커밋 (자동)

- Stop 훅(`auto-commit.mjs`)이 feature 브랜치에서 자동으로 빈 커밋 생성:
  ```
  [요구사항]
  {사용자가 요청한 내용}
  ```
- `.last_prompt` 파일에서 사용자 요청을 읽어 `--allow-empty` 커밋으로 기록
- 코드 변경 없이 요구사항만 기록하므로 이후 커밋과 분리됨

### 3. 작업 중 의미 있는 한글 커밋

```bash
git add {관련-파일들}
git commit -m "{타입}: {무엇} - {왜}"
```

- 논리적 단위마다 커밋 (하나의 커밋 = 하나의 논리적 변경)
- **커밋 메시지는 반드시 한글로 작성**
- 커밋 메시지에 반드시 WHY를 포함

### 4. 작업 완료 후 PR 생성

```bash
gh pr create --title "{제목}" --body "## 요약\n- ...\n\n## 의사결정 근거\n- ..."
```

- PR 본문에 의사결정 근거 섹션 포함
- 테스트 결과 포함

## 커밋 메시지 형식

```
{타입}: {무엇을 했는지} - {왜 이렇게 했는지}
```

### 타입 종류

| 타입 | 용도 |
|------|------|
| 기능 | 새 기능 추가 |
| 수정 | 버그 수정 |
| 리팩토링 | 코드 리팩토링 (동작 변경 없음) |
| 테스트 | 테스트 추가/수정 |
| 문서 | 문서 변경 |
| 기타 | 빌드, 설정 등 |

## 나쁜 예

```
# main에 직접 작업, 의사결정 근거 없음
[User Request] CQRS 패턴형태로 코드를 리펙토링 해야합니다...

# 모든 변경사항이 하나의 커밋에, WHY 없음
```

## 좋은 예

```
# main: 사용자 요청 기록
[User Request] CQRS 패턴형태로 코드를 리펙토링 해야합니다...

# feature/cqrs-refactor: Claude 작업 이력
[요구사항] CQRS 패턴형태로 코드를 리펙토링 해야합니다...     ← 자동 (auto-commit.mjs)
기능: Query/Command 요청 record 정의 - 읽기/쓰기 의도를 타입 시스템으로 명시
기능: Handler 인터페이스 분리 - DI를 통한 테스트 격리와 구현 교체 용이성 확보
리팩토링: Program.cs 엔드포인트를 Handler로 위임 - Minimal API 구조 유지하면서 비즈니스 로직 분리
테스트: Handler mock 테스트 추가 - 비즈니스 로직을 DB 없이 독립 검증

# PR #1: CQRS 패턴 적용
## 요약
- Query/Command 분리로 CQRS 구현
## 의사결정 근거
- Handler를 인터페이스로 분리한 이유: Moq 기반 단위 테스트 지원
- Request를 record로 정의한 이유: 불변성 보장 + 값 기반 동등성
```

## auto-commit 동작

- `auto-commit.mjs`는 브랜치 인식
  - **main**: 모든 변경사항을 `[User Request]` 커밋 (기존 동작)
  - **feature**: 코드 변경 없이 `[요구사항]` 빈 커밋만 자동 생성 → Claude가 코드 커밋 직접 관리
