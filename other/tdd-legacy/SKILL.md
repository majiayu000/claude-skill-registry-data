---
name: tdd-legacy
description: 테스트 없는 기존 코드에 행위 보존 안전망(Characterization → Approval → Mutation)을 구축한 뒤 개선 스킬로 핸드오프. "레거시에 테스트 추가", "안전망 구축", "characterization test" 요청 시 사용. /tdd-legacy로 호출.
argument-hint: "<대상 클래스 FQCN 또는 파일 경로>"
---

# TDD Legacy — 레거시 코드 안전망 구축

테스트 없는 기존 코드의 현재 행위를 고정하는 안전망을 만들고, 개선은 기존 스킬로 넘깁니다.

## GOAL

- **성공 = 대상 코드의 현재 행위가 테스트로 고정되고, mutation 검증으로 안전망의
  실효성이 확인되며, 개선 스킬로 핸드오프됨**
- characterization 테스트가 현재 행위(옳은 행위가 아니라)를 기록함
- 모든 어설션이 sabotage 검증을 통과함 (동어반복 어설션 없음)
- mutation score가 합의된 임계값에 도달함 (기본: 대상 메소드 기준 100%)
- `/tdd-tidy` 또는 `/system-wide-refactoring` 핸드오프 안내로 종료

## CONSTRAINTS

### Hard Rules

- **현재 행위를 기록한다** — 버그로 보이는 동작도 일단 고정한다. 수정은 안전망
  완성 후 별도 작업 (발견한 의심 동작은 사용자에게 보고만).
- **프로덕션 코드를 변경하지 않는다** — 이 스킬의 산출물은 테스트뿐이다.
  sabotage로 일시 변경한 코드는 반드시 원복하고 커밋에 포함하지 않는다.
- 단계(1→2→3) 경계마다 사용자 검토 후 진행 (레거시는 확신이 낮은 상황 —
  기어 모델의 low 상당 밀도로 고정).
- 리팩토링·seam 생성·의존성 깨기(dependency breaking)는 범위 밖 — 필요하면 핸드오프 후 진행.

### Principles

- 테스트하기 어려운 의존성(DB·시간·랜덤)이 있으면 값을 고정할 수 있는 가장 얇은
  방법(고정 입력, 시스템 프로퍼티, 테스트 전용 설정)을 먼저 찾고, 불가능하면
  그 지점을 사용자에게 보고한다 — 의존성 깨기는 이 스킬이 하지 않는다.
- unit test vs approval test는 트레이드오프다: 설계가 매우 나쁠 때는 approval이
  효율적이고, 설계가 좋아지면 composable한 unit test가 낫다. 둘은 공존 가능하다.

## OUTPUT FORMAT

### 호출 형식

```
/tdd-legacy <대상 클래스 FQCN 또는 파일 경로>
```

### 1단계: Characterization — 현재 행위 고정

1. **대상 선정**: 인자의 클래스에서 변경 예정 지점(사용자에게 확인) 우선.
   public 메소드부터, 입력 조합이 단순한 것부터.
2. **golden master 작성**: 대표 입력으로 현재 출력을 그대로 어설션에 고정.
   기대값을 추측하지 말고 실제 실행 결과를 기록한다.
3. **어설션 정확성 검증 — SUT sabotage**: 통과하는 어설션마다
   - SUT를 일시적으로 변형해서(값 하나 변경 등) 테스트를 실행
   - 해당 어설션이 실제로 실패하는지 확인
   - 원복 후 다시 통과 확인
   - 실패하지 않는 어설션 = 동어반복 — 어설션을 고친다
4. **비결정 출력 정규화 — scrubber**: 타임스탬프·랜덤·해시·순서 등 실행마다
   변하는 부분은 정규화(치환) 후 비교한다.
5. 커밋: `test: <대상> characterization 테스트 추가`. 커밋 메시지는
   `docs/reviewable-commits.md`(없으면 `${CLAUDE_PLUGIN_ROOT}/references/reviewable-commits.md`)
   표준을 따른다 — body에 어떤 행위를 고정했고 sabotage 검증 결과를 기록.
   길이는 `../../references/commit-style.md`의 간결성 규칙(제목 + 핵심 bullet 2~4줄)을 따른다.
   커밋 직전 `git diff --stat`으로 테스트 외 파일 변경이 없는지 확인한다
   (sabotage 원복 누락 차단).
6. **사용자 검토 대기** — 고정한 행위 목록과 의심 동작 보고

### 2단계: Approval — 조합 커버리지 확장

1. 입력 조합이 많은 메소드는 `CombinationApprovals.verifyAllCombinations()`로
   조합 전체를 승인 파일에 고정 (approvaltests 의존성 필요 — 없으면 추가를
   사용자에게 확인).
2. 조합이 적거나 설계가 깨끗한 부분은 1단계의 unit 스타일을 유지 —
   전환은 트레이드오프 판단이며 전부 approval로 바꾸지 않는다.
3. 승인 파일(approved.txt)도 scrubber 적용.
4. 커밋: `test: <대상> combination approval 추가`
5. **사용자 검토 대기** — 커버한 조합 범위 보고

### 3단계: Mutation 검증 — 안전망 실효성 확인

1. **도구 선택**:
   - `mutate4java`가 있으면 그것을 사용 (1순위) — 에이전트 `mutate4java-runner` 또는 jar 직접
     실행. 설치·판정은 `../../references/hardening-tools.md`
   - 없으면 PIT를 직접 설정:
     - Gradle: `plugins { id "info.solidsoft.pitest" version "1.15.0" }` +
       `pitest { targetClasses = ["<대상 FQCN>"] }` → `./gradlew pitest`
     - Maven: `org.pitest:pitest-maven` 플러그인 `<targetClasses>` 설정 →
       `mvn test-compile org.pitest:pitest-maven:mutationCoverage`
2. 대상 클래스에 mutation 실행 → 살아남은 뮤턴트 = 안전망의 미검출 영역
3. 뮤턴트를 죽이는 테스트를 보강하고 재실행 (반복).
   죽일 수 없는 동등 뮤턴트(equivalent mutant)로 판정되면 사유와 함께
   사용자에게 보고하고 score 계산에서 제외를 합의한다 (무한 보강 루프 금지).
4. **DoD**: 대상 메소드 기준 mutation score 100% 또는 사용자가 합의한 임계값
5. 커밋: `test: <대상> 뮤턴트 킬 테스트 보강`
6. **사용자 검토 대기** — mutation score 전/후 보고

### 완료: 핸드오프

안전망 완료를 보고하고 종료한다:

> 안전망 완료 (characterization N개 + approval M개, mutation score X%).
> 이제 개선을 진행하세요: 코드 정리는 `/tdd-tidy`, 구조 개선은
> `/system-wide-refactoring`. 새 기능 추가는 `/tdd-feature`.

개선 실행은 이 스킬 범위 밖이다.

## FAILURE CONDITIONS

- [ ] characterization 어설션 중 sabotage 검증을 거치지 않은 것이 있다
- [ ] 프로덕션 코드 변경이 커밋에 포함됐다 (sabotage 원복 누락)
- [ ] "현재 행위"가 아니라 "옳다고 생각하는 행위"를 어설션에 넣었다
- [ ] mutation 검증 없이 안전망 완료를 선언했다
- [ ] 단계 경계에서 사용자 검토 없이 다음 단계로 진행했다
- [ ] 리팩토링/의존성 깨기를 이 스킬 안에서 수행했다
