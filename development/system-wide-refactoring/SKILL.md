---
name: system-wide-refactoring
description: 대화형 System-wide Refactoring — 변경 파일에서 Extract Method·Domain Logic 이동·Pull Up 등 클래스 경계를 넘는 구조 변경 후보를 찾아 승인 후 기법별 커밋으로 적용. "구조 리팩토링", "도메인 로직 이동", "클래스 분리", "system-wide", "/system-wide-refactoring" 요청 시 사용. 단, 메서드 내부 정돈(guard clause·extract variable 등)은 /tdd-tidy가 적합. /system-wide-refactoring [commit-ref]로 호출.
argument-hint: "[commit-ref]"
---

# System-wide Refactoring Skill

코드 분석 → 리팩토링 후보 제시 → 사용자 확인 → 기법별 커밋.

## GOAL

- **성공 = 사용자가 확인한 리팩토링이 기법별 커밋으로 완료됨**
- Extract Method / Extract Delegate / Domain Logic 이동 / SoC(Split Phase, Split by Abstraction Layer, Split by Unrelated Complexity) / 상속 계층(Pull Up Method, Push Down → Delegate) / 유사 기능 통합(Programming by Difference) 후보가 식별됨
- 사용자와 질의응답으로 방향이 확정됨
- 모든 테스트 통과

## CONSTRAINTS

### Hard Rules
- **동작 변경 금지** — 구조 개선만 수행
- **테스트 수정 금지** — 구조 변경이 테스트를 실패시키면 되돌리기
- **사용자 확인 없이 리팩토링 금지** — 모든 후보는 사용자 승인 후 실행
- **커밋 단위** — 1파일 x 1기법 = 1커밋 (논리적으로 연결된 파일은 함께)
- **git add -A 금지** — 변경된 파일만 명시적으로 추가

## OUTPUT FORMAT

### 실행 절차

공통 골격(대상 파일 수집 → 후보 제시(계열별 승인 규칙) → 적용 → 테스트 → 커밋/되돌리기, 브랜치·PR이
필요한 조건)은 이 스킬 디렉터리 기준 `../../references/refactoring-procedure.md`가 정본이다.
아래는 이 기법에 고유한 부분만 규정한다.

#### 적용 순서 — 후보 제시의 기본 순서

후보를 제시할 때 아래 순서를 기본으로 정렬한다. 사용자가 순서를 바꾸면 그에 따른다.

**A. TDD 직후(테스트에 로직이 모여 있는 상태) — 초기 리팩터링 7단계**:
1. **전제**: 모든 로직이 테스트에 구현되어 있다 (이 전제가 없으면 2~7의 순서가 성립하지 않는다)
2. AAA 구조의 테스트에서 Act 부분을 Extract Method한다
3. Act가 의존성 객체를 쓰면: ① Introduce Parameter로 의존성을 파라미터로 → ② Introduce
   Parameter Object로 파라미터들을 객체(Application Service)로 묶는다 (Application Service에
   그대로 전달될 파라미터는 제외) → ③ Move Instance Method to Application Service.
   의존성이 Application Service 생성자로 전달된다. 의존성 주입(DI)이 가능해진다
4. Act가 의존성 객체를 쓰지 않으면: Extract Delegate로 Application Service를 추출한다
5. Application Service에서 Slide Statements로 I/O → 계산 → I/O 구조(Functional Core /
   Imperative Shell)를 확보한다
6. Application Service에서 Extract Method로 도메인 로직을 메서드로 추출한다
7. 추출된 도메인 로직을 Extract Delegate·Move Instance Method로 domain 계층에 옮긴다

**B. 기존 트랜잭션 스크립트 → 도메인 모델 (Jimmy Bogard 9단계)**:
1. Composed Method — 긴 메서드를 같은 추상화 수준의 작은 메서드로 분해
2. Extract Methods — 주석 기준으로 블록 추출
3. Introduce Parameter — 의존성 명시화
4. Extract Class — seam 생성
5. Extract Interface — 테스트 용이성
6. Make Method Non-Static — Feature Envy 해소를 위한 인스턴스 메서드 전환
7. Move Method — 데이터를 가진 객체로 이동
8. Inline (Undo) — 이동 결과가 불균형하면 되돌리고 재추출한다. 리팩터링은 되돌릴 수 있어야 한다
9. Reduce Setter Scope — private setter로 캡슐화 강화

A와 B는 출발 상태가 다르다(A: 테스트에 로직 집중, B: 기존 서비스 코드). 둘을 섞지 않는다.

#### 코드 분석 — 리팩토링 후보 식별 (공통 절차 2단계)

대상 파일을 읽고 다음 패턴을 찾는다:

**Extract Method 후보**:
- 긴 메서드 (20줄 이상)에서 독립적인 로직 블록
- 여러 곳에서 반복되는 코드 패턴
- 서로 다른 추상화 수준이 섞인 메서드

**Extract Delegate 후보** (Fat Class 분리 3기준):
- **ISP 기준**: 클라이언트마다 사용하는 메서드 집합이 다르면 클라이언트별 인터페이스 단위로 분리한다
- **관련 필드·메서드 기준**: 함께 읽고 쓰는 필드와 메서드가 그룹을 이루면 그 그룹을 클래스로 추출한다
- **관련 협력자(collaborator) 기준**: 테스트 setUp에서 함께 mock되는 협력자 그룹이 있으면
  그 그룹을 사용하는 메서드들이 하나의 클래스 경계 후보다 (Split by Unrelated Complexity와 같은 신호)

**Domain Logic 이동 후보**:
- Feature Envy — Service에서 도메인 객체의 데이터를 직접 조작
- Tell, Don't Ask 위반 — getter 체이닝으로 로직 수행
- Hide Delegate — getter 체이닝으로 내부 객체를 노출 (디미터 법칙(Law of Demeter) 위반)
  - 징후: `obj.getA().getB().doSomething()` 형태의 체이닝
  - 해결: 중간 객체를 숨기고 위임 메서드 제공, 또는 로직 자체를 obj로 이동
  - Tell Don't Ask와의 관계: 둘 다 Feature Envy의 증상. 해결 방향 동일 — 로직을 데이터가 있는 곳으로 이동
- Domain Service, Value Object, First Class Collection 추출 가능
- **Train Wreck 제거** — `a.getB().getC().doSomething()` 연쇄 호출(Law of Demeter 위반)을
  2단계로 해소한다: ① 연쇄 호출을 포함한 로직을 Extract Method → ② 추출한 메서드를
  연쇄의 시작 객체(`a` 또는 `B`)로 Move Method. Hide Delegate가 위임 메서드를 추가하는 것과
  달리 로직 자체를 옮긴다
- **Remove Middle Man** (Hide Delegate의 역) — 단순 위임만 하는 메서드가 많아져 클라이언트가
  위임 객체를 직접 다루는 편이 자연스러우면 위임 메서드를 제거하고 위임 객체를 노출한다.
  Hide Delegate와 Remove Middle Man은 같은 축의 양 끝이며, 위임 메서드 수를 기준으로 판단한다

**Split by Abstraction Layer 후보**:
- High-level 비즈니스 로직과 Low-level 인프라 코드(DB, I/O)가 한 메서드에 혼재
- App 계층과 Domain 계층이 분리되지 않은 경우
- **낮은 수준 기능이 높은 수준 클래스에 섞였을 때의 절차** (Push Down → Delegate → 상속 제거):
  ① 낮은 수준 기능을 담을 새 클래스를 **임시로 원본 클래스의 하위 클래스**로 만든다
  ② 옮길 필드·메서드를 Push Members Down으로 하위 클래스에 내린다
  ③ 테스트가 통과하도록 원본 클래스가 하위 클래스 인스턴스에 위임(delegate)하게 바꾼다
  ④ 상속 관계를 제거해 합성(composition)으로 확정한다. 각 단계마다 테스트를 실행한다

**Split by Unrelated Complexity 후보**:
- 서로 관계없는 복잡성(예: 사용자 처리 로직과 상품 처리 로직)이 한 메서드/클래스에 혼재
- 서로 다른 변경 이유를 가진 코드가 결합된 경우

**Split Phase 후보** (Functional Core & Imperative Shell 포함):
- 서로 다른 계산 단계가 한 메서드에 혼재 (예: 파싱 → 처리 → 포매팅)
- 순수 로직과 부수효과(I/O)가 분리되지 않은 경우 (impure → pure → impure 구조)
  - 패턴: I/O(impure) → 비즈니스 로직(pure) → I/O(impure)
- 중간 데이터 구조(Intermediate Data Structure)로 단계를 연결

**Pull Up Method 후보** (서브클래스 간 중복):
- 여러 서브클래스가 같은 메서드를 동일하게 override한 경우. 절차(IDE 자동 리팩터링 활용):
  ① superclass의 abstract 메서드에서 `abstract`를 제거한다
  ② 각 서브클래스의 override 메서드를 같은 이름으로 rename하고 Pull Members Up한다.
     IDE가 다른 서브클래스의 중복도 바꾸겠느냐고 물으면 "Skip"을 선택한다 (서브클래스 간
     중복은 자동으로 제거되지 않으므로 모든 서브클래스에 대해 rename → pull up을 반복한다)
  ③ pull up된 메서드 하나를 골라 본문을 Extract Method하며 IDE의 "All"(전체 치환)을 선택해
     나머지 중복도 한 번에 치환한다
  ④ superclass 구현을 추출한 메서드 호출로 바꾼다
  ⑤ 사용되지 않는 서브클래스 메서드를 제거한다

**유사 기능 통합 후보** (Programming by Difference):
- 새 기능이 기존 기능과 대부분 같고 일부만 다를 때. 순서: ① 복사·붙여넣기로 동작시킨다 →
  ② 차이점만 남기고 공통 부분을 추출한다(Programming by Difference) → ③ Template Method
  패턴으로 수렴한다(상속 또는 위임). 세부 절차는 규정하지 않는다.
  후보 제시 시 차이점 목록을 사용자에게 먼저 확인한다

#### 후보 제시 예시 (공통 절차 3단계)

후보를 하나씩 제시하고 사용자 확인:

```
## 리팩토링 후보 1: Extract Method

**파일**: OrderService.java
**대상**: processOrder() 메서드 (45줄)

**현재 코드**:
[해당 코드 블록]

**제안 변경**:
- calculateDiscount() 메서드 추출 (라인 23-35)
- validateInventory() 메서드 추출 (라인 37-42)

**적용할까요?** (yes / no / 수정 요청)
```

```
## 리팩토링 후보 N: Split Phase (Functional Core & Imperative Shell)

**파일**: OrderService.java
**대상**: processOrder() 메서드 (35줄)

**현재 코드**:
[해당 코드 블록 — DB 조회, 비즈니스 로직, DB 저장이 혼재]

**제안 변경**:
1. DB 조회를 메서드 상단으로 모음 (Imperative Shell — 빵)
2. 순수 비즈니스 로직을 별도 메서드로 추출 (Functional Core — 속)
3. DB 저장을 메서드 하단으로 모음 (Imperative Shell — 빵)

**적용할까요?** (yes / no / 수정 요청)
```

```
## 리팩토링 후보 N: Hide Delegate (Domain Logic 이동)

**파일**: OrderService.java
**대상**: order.getCustomer().getAddress().getCity() (3단계 체이닝)

**현재 코드**:
String city = order.getCustomer().getAddress().getCity();
if (city.equals("Seoul")) { applyLocalDiscount(); }

**제안 변경**:
1. Order에 getCustomerCity() 위임 메서드 추가
   또는
2. 판단 로직 자체를 Order로 이동: order.isLocatedIn("Seoul")

**적용할까요?** (yes / no / 수정 요청)
```

```
## 리팩토링 후보 N: Pull Up Method (서브클래스 중복 제거)

**파일**: CardPayment.java, BankTransferPayment.java, PointPayment.java
**대상**: validate() — 3개 서브클래스가 동일 구현으로 override

**현재 코드**:
[각 서브클래스의 validate() 본문 — 동일]

**제안 변경**:
1. Payment.validate()의 abstract 제거
2. 각 서브클래스 validate()를 rename → Pull Members Up (Skip 선택), 3회 반복
3. pull up된 메서드 본문을 Extract Method(All) → 나머지 중복 치환
4. 사용되지 않는 서브클래스 메서드 제거

**적용할까요?** (yes / no / 수정 요청)
```

- 사용자가 **yes** → 실행 목록에 추가
- 사용자가 **no** → 스킵
- 사용자가 **수정 요청** → 요청 반영 후 재제시

모든 후보 확인 후 최종 실행 목록을 보여주고 진행 여부 확인.

#### 기법별 적용 실행 (공통 절차 4단계)

확정된 리팩토링을 하나씩 수행:

1. 리팩토링 적용

**대규모 범위 — Mikado Method 분기**: 하나의 후보를 적용했을 때 컴파일 오류·테스트 실패가
연쇄적으로 발생할 수 있다. 30분(타임박스) 안에 수습되지 않으면 강행하지 않는다. 다음 절차로 전환한다.
사용자와 대화형으로 진행하며 자동 실행하지 않는다.
M1. 변경을 되돌린다(`git checkout -- <파일>`). 컴파일이 깨진 상태에서는 IDE 자동 리팩터링이
   동작하지 않으므로 항상 컴파일 가능한 상태로 복귀한다
M2. 실패 원인을 "이 변경의 **전제 조건**"으로 기록한다 (예: "OrderService가 Repository를
   직접 생성함 → 생성자 주입으로 바꿔야 함")
M3. 전제 조건과 목표의 의존 관계를 목록 또는 그래프로 사용자에게 제시한다
M4. 전제 조건 중 안전하게 완료할 수 있는 것부터 하나씩 적용·커밋한다 (각각이 독립 후보가 된다)
M5. 전제 조건이 모두 해결되면 원래 후보로 돌아가 다시 적용한다. 다시 실패하면 M2로 돌아간다

**커밋 메시지 형식**:
- `refactor: extract method [메서드명] from [클래스명]`
- `refactor: extract delegate [클래스명] from [원본클래스명]`
- `refactor: move [설명] to [대상 클래스]`
- `refactor: split phase [설명] in [클래스명]`
- `refactor: split by abstraction layer [설명] in [클래스명]`
- `refactor: split unrelated complexity [설명] from [클래스명]`
- `refactor: pull up [메서드명] to [상위클래스명]`
- `refactor: push down [설명] to [하위클래스명] and delegate`
- `refactor: remove middle man [메서드명] in [클래스명]`
- `refactor: extract common part of [기능A]/[기능B] into [템플릿 메서드명]`

#### 결과 보고

사용자에게 보고:
- 적용된 리팩토링 목록

리팩토링 과정에서 발견된 추가 개선 기회를 제안:

```
추가로 발견된 개선 기회:
[발견 시에만 해당 항목 표시]
- /extract-method-object — [파일명]에서 지역 변수 얽힘으로 Extract Method 불가
- /replace-conditional-with-poly — [파일명]에 반복 switch/if-else [N]곳
- /introduce-parameter-object — [파일명]에 3개 이상 파라미터 그룹 반복
- /discover-value-object — [파일명]에 primitive 타입에 로직 집중
- /first-class-collection — [파일명]에 컬렉션+관련 로직 산재
- /lift-up-conditional — [파일명]에 동일 조건문 중복
- /separate-query-modifier — [파일명]에 값 반환과 부수효과 혼재
- /introduce-special-case — [파일명]에 동일 타입 null 검사가 [N]곳 반복
- /intent-revealing-names — [파일명]에 이름이 what만 나열하는 긴 메서드가 있어 이름 주도 관통 리팩토링(3단계 완전정직→extract→intent rename)이 유효합니다
적용할 기법을 선택하세요 (slash command 또는 skip)
```

## FAILURE CONDITIONS

공통 실패 조건(계열별 승인 규칙 위반, 테스트 실패 방치, 테스트 수정, 커밋 단위, `git add -A`, heredoc
한글 메시지)은 `../../references/refactoring-procedure.md`에 있다. 아래는 이 기법에 고유한 것만.

- Local Tidying 기법 수행 (Guard Clauses, Reorder 등은 tdd-tidy 전담)
- Split Phase 적용 시 중간 데이터 구조 없이 단계만 분리 (단계 간 결합 유발)
- Push Down → Delegate 절차에서 상속을 제거하지 않고 종료 (임시 상속이 영구화됨)
- Pull Up 시 IDE 중복 치환에 "Replace"를 선택해 서브클래스 본문이 superclass 호출로 바뀐 채 중복 확인을 건너뜀
- 시그니처·파라미터 순서 변경을 한 커밋에 Expand와 Contract를 함께 넣어 수행 (절차는 `../../references/parallel-change.md`)
