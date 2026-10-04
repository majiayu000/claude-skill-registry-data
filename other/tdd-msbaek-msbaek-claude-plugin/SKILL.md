---
name: tdd
description: TDD 오케스트레이터 — 대상 클래스(FQCN)의 템플릿 문서·테스트 클래스를 생성하고 tdd-plan→tdd-rgb 워크플로우를 안내. "TDD 시작", "TDD로 새 클래스 만들자", "테스트 주도로 시작", "/tdd" 요청 시 사용. 단, 템플릿이 이미 있는 상태에서 사이클만 돌리는 것은 /tdd-rgb, 요구사항 정리부터는 /tdd-plan-input이 적합. /tdd <general|web-app> <FQCN>으로 호출.
argument-hint: "<general|web-app> <FQCN>"
---

# TDD 오케스트레이터

TDD 프로젝트 생성 및 진행 상황을 관리하는 진입점입니다.

## GOAL

- **성공 = TDD 유형에 맞는 템플릿 문서가 생성되거나, 기존 프로젝트의 진행 상황이 분석되어 다음 단계가 안내됨**
- 프로젝트 생성: 템플릿 문서 + 빈 테스트 클래스 생성 후 "/tdd-plan 실행하세요" 안내
- 진행 상황 분석: 체크박스 기반 현재 단계 파악 후 적절한 다음 명령어 안내

## CONSTRAINTS

### Hard Rules

#### Ground Rule

- 모르는 정보면 모른다고 확실히 대답
- 요청에 답변하기 위해 필요한 정보가 있으면 먼저 질문
- 코드는 최신 Java, Spring Boot 기준으로 작성
- 요청하지 않는 한 리팩터링하지 않고, 절차적/명령형 스타일로 하나의 메소드로 직관적이게 작성
- 메소드 추출(extract method)이나 변수 추출(extract variable/field) 최소화
- 금액, 거리, 무게 등은 대한민국 기준
- getter/setter는 lombok 활용, 최대한 record 활용
- 마크다운 문서는 한글로 작성
- Class 파일에서 중요한 public method가 먼저, private 메소드가 나중에

#### 피드백 규칙

- 한 단계에서 관련된 코드를 생성한 후에는 반드시 사용자에게 피드백을 요청
- 사용자가 명시적으로 다음 단계로 진행하는 것을 결정해야만 다음 단계로 진행
- 피드백이 필요할 때마다 다음 형식으로 질문:

```
[피드백 요청]

- 대상: [테스트/구현/설계/리팩토링]
- 초점: [특정 관심 영역]
- 맥락: [현재까지의 작업 요약]
- 구체적 질문: [구체적인 피드백 요청 사항]
```

## OUTPUT FORMAT

### 호출 형식

```
/tdd $1 $2
```

- `$1` = `general` | `web-app` (TDD 유형)
- `$2` = FQCN (예: `com.example.bowling.BowlingGame`)

FQCN에서 패키지명과 클래스명을 자동 파싱합니다.
패키지명 없이 입력 시 예시를 보여주며 재입력 요청합니다.

```
예: /tdd general com.example.bowling.BowlingGame
예: /tdd web-app com.example.basket.CreateShoppingBasket
```

---

### 프로젝트 탐색 로직

#### 1. 빌드 시스템 탐색
- 현재 디렉토리에서 Gradle(`build.gradle`, `build.gradle.kts`) 또는 Maven(`pom.xml`) 프로젝트 루트 탐색
- 프로젝트 루트를 기준으로 경로 결정

#### 2. FQCN 기반 경로 결정

FQCN을 기반으로 다음 경로를 결정합니다:

- **템플릿 문서**: `src/test/java/{package_path}/{ClassName}.md`
- **테스트 클래스**: `src/test/java/{package_path}/{ClassName}Test.java`

예: `com.example.bowling.BowlingGame` →
- 문서: `src/test/java/com/example/bowling/BowlingGame.md`
- 테스트: `src/test/java/com/example/bowling/BowlingGameTest.java`

---

### 상태 판단

#### Case A: 템플릿 없음 → 프로젝트 생성

1. TDD 유형에 따라 템플릿 문서 생성
2. 빈 테스트 클래스 생성 — 주석 언어와 빌드 파일 UTF-8 인코딩 명시는
   `../../references/code-comment-style.md`를 따른다
3. 산출물 커밋 1회 — 템플릿 문서 + 빈 테스트 클래스(+ 새로 만든 빌드 골격이 있으면 함께).
   메시지 형식·한글 안전 방식은 `../../references/commit-style.md`를 따른다
4. **"/tdd-plan 실행하세요"** 안내

#### Case B: 템플릿 있음 → 진행 상황 분석

1. 체크박스 분석으로 현재 단계 파악
2. 진행 기록의 기어 상태 확인 — 있으면 현재 기어와 전환 이력을 함께 안내, 없으면 low로 간주
3. 완료된 단계와 다음 단계 안내
4. 적절한 다음 명령어 안내:
   - 앵커(규칙·예제·미확정) 미완성 → **"/tdd-plan 실행하세요"** (high-stakes·대형 작업이면 `/tdd-plan --full`로 3 에이전트 + critic 풀 플로우를 안내)
   - 테스트 구현 단계 → 아래 "구현 스킬 라우팅" 표로 기어에 맞는 호출을 안내
   - 대상이 테스트 없는 기존 코드(레거시)라면 이 템플릿 흐름 대신 → **"/tdd-legacy로 안전망부터 구축하세요"**

#### 구현 스킬 라우팅 — 기어로 고른다

기어(검토 밀도)는 이론에 대한 확신이 정한다. 확신이 낮으면 low, 상용구 수준으로 명확하면
high다(상세는 tdd-rgb의 "기어(Gears)" 섹션).

| 상황 | 기어 | 호출 |
|---|---|---|
| 낯선 도메인·기술, 학습 목적, 설계 미확정 | low | `/tdd-rgb --gear=low` (매 R/G/B 검토) |
| 유사 문제 경험 있음, 설계가 안정되어 감 | mid | `/tdd-rgb --gear=mid` (테스트 1개 사이클마다 검토) |
| 이론이 명확, 테스트 목록 전체를 자율로 | high | `/tdd-rgb --gear=high` (완료 + 적대적 리뷰 후 최종 검토) |
| 이론이 명확, feature 하나를 plan 합의 후 자율로 | high | `/tdd-feature` (Phase B = feature 범위 high) |

폭발 반경(blast radius)이 큰 영역(인증·인가, 결제·금액 계산, 데이터 삭제·변경, 외부 API, 동시성)은
기어와 무관하게 완료 시 적대적 리뷰를 1회 실행한다
(`../tdd-rgb/references/gears.md`의 "폭발 반경(blast radius)" 참조).

- 진행 기록에 기어가 남아 있으면 `--gear` 없이 `/tdd-rgb`만 호출해도 그 기어로 복원된다
- `/tdd-feature`는 `--gear`를 받지 않는다 — Phase B 자율 진행이 곧 high다
- 폭발 반경(blast radius)이 큰 영역(인증·결제·데이터 삭제·외부 API·동시성)은 확신이 높아도 한 단
  낮은 기어를 권장한다 — 두 스킬 모두 시작 시 이 점검을 수행한다

---

### General TDD 템플릿 (2단계)

```markdown
# {ClassName} TDD 구현

## 절차
- [ ] 1. 앵커 작성 (규칙 + 예제 검산표 + 미확정)
- [ ] 2. 테스트 구현 (RGB 사이클)

## 규칙

## 예제 (검산표)

## 미확정

## 진행 기록

기어: low

## 배움 로그
```

---

### Web App TDD 템플릿 (8단계)

```markdown
# AI와 Pair로 {ClassName}을 TDD로 구현하기 (Web App)

## 전체적인 절차
- [ ] 1. 앵커 작성 (규칙 + 예제 검산표 + 미확정)
- [ ] 2. 인수 테스트 셋업 (.feature + Runner, 미구현은 @pending — .feature가 시나리오의 실행되는 정본)
- [ ] 3. Walking Skeleton 구현
- [ ] 4. 테스트 구현 (RGB 사이클 — 각 Green이 자기 시나리오 @pending 해제)
- [ ] 5. JPA Repository 완성 (계약 테스트로 InMemory와 동등성 검증)
- [ ] 6. DSL 개선 (Steps·Protocol Driver·Test Data Builder)
- [ ] 7. 적대적 리뷰 (high 기어 또는 폭발 반경(blast radius) high-stakes 시 — 5·6을 마친 뒤 실행, diff가 전체 구현을 포함해야 함)
- [ ] 8. 하드닝 게이트 (① CRAP·DRY 분석 → ② /system-wide-refactoring → ③ mutation 대표 파일 1개 — 제안만, 실행은 사용자 결정)

## 규칙

## 예제 (검산표)

## 미확정

## 진행 기록

기어: low

## 배움 로그
```

> Web App은 `/cucumber-acceptance`가 **필수**다 — 1단계 앵커 작성에서 승인된 Gherkin이
> 2단계에서 `.feature`로 실행되어 인수 계층을 담당한다. 별도 High Level Test(JUnit)를 두지 않는다(같은 검증이
> 두 계층에 중복되면 안 됨). 프로젝트 제약으로 Cucumber를 도입할 수 없는 경우에만
> 대표 시나리오 1개를 JUnit 인수 테스트로 작성해 대체한다.

## FAILURE CONDITIONS

- [ ] Case A 산출물(템플릿 문서·테스트 클래스·빌드 골격)을 커밋하지 않은 채 다음 단계를 안내하지 않았는가?

### 에러 대처

1. **요구사항 이해 실패** → "요구사항에 대해 제가 이해한 것이 맞는지 확인해주세요."
2. **컨텍스트 혼란** → "지금까지의 작업을 요약해주세요."
3. **구현 방향성 혼란** → "더 단순한 방법으로 목표를 달성할 수 있을까요?"
4. **테스트 실패 원인 파악 어려움** → "가능한 원인을 모두 나열해주세요."
5. **테스트 품질 저하** → Programmer Test 규칙 기준으로 품질 평가
