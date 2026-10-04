---
name: tdd-tidy
description: git diff 기준 변경 파일을 자동 탐지해 Composed Method 지향 Tidying Process를 TDD 사이클 없이 독립 실행. 완료 후 선택 기법 제안. "변경 파일 정리", "tidying만", "방금 바꾼 코드 정돈", "tidy first", "/tdd-tidy" 요청 시 사용. 단, 다른 클래스로 로직을 옮기는 구조 변경은 /system-wide-refactoring이 적합. /tdd-tidy [commit-ref]로 호출.
argument-hint: "[commit-ref]"
---

# Tidying Skill — Composed Method 지향 독립 리팩토링

git diff로 최근 변경된 Java 파일을 자동 탐지하여, tdd-blue agent의 Local Tidying Process를 TDD 사이클 없이 독립 실행합니다.

## GOAL

- **성공 = 변경된 파일의 코드 냄새가 안전하게 제거되고, 모든 테스트가 통과하며, `refactor:` 커밋 완료됨**
- git diff 기준으로 대상 파일이 정확히 식별됨
- Local Tidying Process가 적용됨 (단계·순서는 `../../agents/references/tidying-process.md` 정본)
- 모든 기존 테스트가 통과함
- 하나의 `refactor:` 커밋으로 완료됨 (변경이 있는 경우)

## CONSTRAINTS

### Hard Rules
- **동작 변경 금지** — 구조 개선만 수행
- **테스트 수정 금지** — 구조 변경이 테스트를 실패시키면 되돌리기
- **80% 규칙** — 지금 할 수 있는 수준에서 80% 이하로 리팩토링
- **git add -A 금지** — 변경된 파일만 명시적으로 추가

## OUTPUT FORMAT

### 실행 절차

#### 1. 대상 파일 수집

인자가 전달된 경우 해당 commit ref와 비교, 없으면 unstaged + staged 변경 파일 수집:

```bash
# 인자 없음: unstaged + staged 변경 파일
git diff --name-only -- '*.java'
git diff --cached --name-only -- '*.java'

# 인자 있음: 특정 commit과 비교
git diff --name-only <commit-ref> -- '*.java'
```

- 테스트 파일(`*Test.java`, `*Tests.java`, `*Spec.java`)은 **제외**
- 변경 파일이 없으면: "tidying 대상 Java 파일이 없습니다." 안내 후 종료

#### 2. 대상 파일 확인

수집된 파일 목록을 사용자에게 보여주고 확인:

```
다음 파일에 Tidying Process를 적용합니다:
- src/main/java/com/example/OrderService.java
- src/main/java/com/example/PaymentProcessor.java

진행할까요?
```

#### 3. tdd-blue agent 호출

사용자 확인 후 tdd-blue agent를 **standalone 모드**로 호출:

```
[standalone] 다음 파일에 Local Tidying Process를 적용해주세요:
- src/main/java/com/example/OrderService.java
- src/main/java/com/example/PaymentProcessor.java

Local Tidying Process(단계·순서는 `../../agents/references/tidying-process.md` 정본)를 순서대로 적용하고,
One Pile 적용 시에는 항상 별도 커밋(refactor: one-pile [대상])으로 먼저 분리하고, 나머지 tidying은 별도 refactor: 커밋으로 완료해주세요.
Extract Method는 같은 클래스 내부(private 메서드 추출)로 한정한다. 다른 클래스로 옮기는 Domain Logic 이동(새 클래스가 생기는 분리 포함)은 수행하지 않는다 (system-wide-refactoring 스킬 전담).
```

#### 4. 결과 보고

tdd-blue agent 완료 후 사용자에게 결과 보고:
- 적용된 tidying 단계
- 변경된 파일과 주요 개선 사항
- 커밋 해시 (변경이 있는 경우)

tidying 과정에서 발견된 징후에 따라 선택 기법 제안:

```
추가로 적용 가능한 기법이 발견되었습니다:
[발견 시에만 해당 항목 표시]
- /decompose-conditional — [파일명]의 if/then/else가 복잡합니다
- /replace-temp-with-query — [파일명]에서 임시 변수가 반복 계산됩니다
- /explicit-parameters — [파일명]에서 암묵적 필드 의존이 발견되었습니다
- /naming-process — 의도가 불분명한 이름이 [N]건 있습니다
- /intent-revealing-names — [파일명]에 긴 메서드가 남아 이름 주도 관통 리팩토링(grouping→comment→extract→6단계 rename)이 필요합니다
- /encapsulate-collection — [파일명]에서 컬렉션이 직접 노출됩니다
- /consolidate-conditional — [파일명]에서 동일 결과 조건문이 분산됩니다
- /introduce-assertion — [파일명]에서 암묵적 가정이 발견되었습니다
- /replace-loop-with-pipeline — [파일명]에서 명령형 루프를 Stream으로 변환 가능합니다
적용할 기법을 선택하세요 (slash command 또는 skip)
```

## FAILURE CONDITIONS

- 테스트 파일을 tidying 대상에 포함
- 동작이 변경되어 테스트가 실패
- 사용자 확인 없이 tidying 진행
- git add -A로 전체 파일 추가
