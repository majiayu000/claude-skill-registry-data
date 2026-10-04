---
name: naming-process
description: Arlo Belshee의 6단계 네이밍 프로세스와 Clean Code 네이밍 규칙을 적용해, 여러 파일에 흩어진 개별 이름 스멜(타입 반복·-er/-Utils·불용어·축약어 등)을 탐지하고 배치 교체하여 코드 가독성 향상. 단, 하나의 긴 메서드를 통째로 관통(grouping→extract→rename)하는 것은 /intent-revealing-names가 적합. /naming-process로 호출.
argument-hint: "[commit-ref]"
---

# Naming as a Process

## GOAL

Arlo Belshee의 **6단계 네이밍 진화**와 **Clean Code 7가지 네이밍 원칙**을 적용하여:
- 코드의 의도(what이 아니라 **why**)를 이름으로 명확히 전달 — "이름을 신뢰하면 메서드 본문을 읽을 필요가 없는" 상태가 목표
- Naming Smells 제거
- 도메인 언어를 코드로 표현

## CONSTRAINTS

- **계열**: Tidy — 후보 보고 후 **승인 없이 적용** (`../../references/refactoring-procedure.md` §0·§3-A)
- **동작 변경 금지**: 구조 개선만 수행 (기능 변경 없음)
- **테스트 수정 금지**: 구조 변경이 테스트를 실패시키면 되돌리기
- **명시적 git add**: `git add -A` 금지, 변경된 파일만 명시

## 6단계 네이밍 프로세스

1. **Obvious Nonsense** → 2. **Honest** → 3. **Completely Honest** → 4. **Does the Right Thing** → 5. **Intent Revealing** → 6. **Domain Abstraction**

### 예시: 네이밍 진화
```java
// 1. Obvious Nonsense
int x;

// 2. Honest (타입 반복)
int intValue;

// 3. Completely Honest (맥락 포함)
int orderItemCount;

// 4. Does the Right Thing (역할 명확)
int itemsInCart;

// 5. Intent Revealing (의도 표현)
int pendingOrderItems;

// 6. Domain Abstraction (도메인 언어)
int itemsAwaitingFulfillment;
```

## Clean Code 7가지 네이밍 원칙

| # | 원칙 | 핵심 | 예시 |
|---|---|---|---|
| 1 | Reveal Your Intent | 동작이 아니라 목적을 담는다 | `process()` → `placeOrder()` |
| 2 | Describe the Problem | 매직 값 대신 도메인 언어 | `INCLUDE_FIRST` → `OPEN_LEFT`, `TWENTYFOURBITGROUP` → `BITS_PER_GROUP` |
| 3 | Avoid Disinformation | 타입/역할을 속이지 않는다 | `accountList`(실제 List 아님) → `accounts` |
| 4 | Pronounceable Names | 팀 대화에서 발음 가능해야 함 | `genymdhms` → `generationTimestamp` |
| 5 | Avoid Encodings | 헝가리안·타입/스코프 접두사 금지 | `IService` → `Service`, `m_memberName` → `memberName` |
| 6 | Parts of Speech | 클래스=명사, 메서드=동사, boolean=서술어 | 아래 상세 |
| 7 | The Scope Rule | scope에 따라 길이 조절 | 아래 상세 |

### The Scope Rule
- **변수**: scope ↑ → 이름 ↑ (**정비례**) — scope가 길수록 선언부-사용부 거리가 멀어져 문맥 상실 위험이 커진다. 20줄 떨어진 곳의 `d`는 의미가 불명확하다.
- **함수/클래스**: scope ↑ → 이름 ↓ (**반비례**) — public API는 자주 호출되므로 짧아야 하고, private 메서드는 호출처가 적어 긴 이름이 주석 역할을 대신한다.
- **Public=일반적(general), Private=구체적(detailed)**: public 인터페이스는 상위 추상화 계약이므로 짧고 일반적으로, private 구현은 하위 디테일이므로 길고 정확하게 서술한다.

```java
// Good: 변수 scope 규칙 (정비례)
for (int i = 0; i < 10; i++) { ... }  // 극히 짧은 scope → 짧은 이름
private Customer currentlyAuthenticatedCustomer;  // 클래스 필드 → 긴 이름
static final int WORK_DAYS_PER_WEEK = 5;  // 정적 필드 → 가장 긴 이름

// Good: 함수 scope 규칙 (반비례)
public void serve(Socket s) { ... }  // public, 자주 호출 → 짧게
private void closeEnclosingServiceInSeparateThread() { ... }  // private → 길게(자체 문서화)
```

클래스도 함수와 같은 방향: 기반 클래스(넓은 scope)는 짧게 `Employee`, 파생 클래스(좁은 scope)는 형용사를 더해 길게 `PartTimeHourlyEmployee`.

#### 한 글자 이름 허용 기준

| 상황 | 허용 여부 |
|---|---|
| 루프 변수 (`i`, `j`, `k` — 1~5줄) | 허용 |
| exception 핸들러 (`e` — 3줄 이내) | 허용 |
| 인스턴스 필드 | 불허 |
| 10줄 이상 지역변수 | 불허 |
| 도메인 의미 있는 파라미터 (`x` 대신 `sourceAmount`) | 불허 |

### Parts of Speech
- **클래스**: 명사 (Customer, Order, Invoice)
- **메서드**: 동사 (calculate, save, send)
- **Boolean**: 서술어 (isValid, hasPermission, canExecute)

```java
// Good
if (employee.isLate()) {
    employee.reprimand();
}

// Bad
if (employee.late()) {  // 서술어 아님
    employee.punishment();  // 명사
}
```

### System of Names
이름의 체계가 도메인을 전달해야 함. **한 개념에는 한 단어만** 사용한다 (`fetch` ≠ `retrieve` ≠ `get` — 같은 의미면 하나로 통일).

```java
// Good: 일관된 네이밍 체계
class OrderService {
    void placeOrder(Order order) { ... }
    void validateOrder(Order order) { ... }
    void fulfillOrder(Order order) { ... }
}

// Bad: 체계 없음 (do/check/execute가 같은 계열 동작에 뒤섞임)
class OrderHandler {
    void doOrder(Order order) { ... }
    void checkOrder(Order order) { ... }
    void executeOrder(Order order) { ... }
}
```

### 요소별 네이밍 패턴

- **메서드**: `from`(factory, 인자 1개) / `of`(factory, 인자 2개+) / `canXXX`(검증 boolean) / `validateXXX`(검증 exception) / `markXXX`(상태 변경) / 동사구(일반)
- **클래스**: 명사/명사구. `-er` 접미사(Manager/Helper) 지양, `-Utils` 금지
- **패키지**: 동사구 (`invoicing`, `invoice` 아님). Bounded Context 내부에서는 접두사 불필요 — `invoicing.Customer`이지 `InvoicingCustomer`가 아니다

### 문맥(Context) 추가하기

`name`, `street`, `state`를 단독으로 쓰면 의미가 불명확하다. 해결 우선순위:
1. **클래스로 그룹화** (최선) — `Address` 클래스에 `street`, `state` 필드를 담는다
2. **접두사** (최후 수단) — `addrState`

## Naming Smells

### 1. 라이프사이클 이벤트명 (Lifecycle Event Names)
```java
// Bad
void onCreate() { ... }
void onDestroy() { ... }

// Good
void initialize() { ... }
void cleanup() { ... }
```

### 2. 타입 반복 (Type Repetition)
```java
// Bad
String nameString;
List<Order> orderList;

// Good
String name;
List<Order> orders;
```

### 3. -er / -Utils 클래스
```java
// Bad
class OrderProcessor { ... }
class StringUtils { ... }

// Good
class OrderService { ... }  // 또는 구체적 역할명
class TextFormatter { ... }
```

### 4. 불용어 (Noise Words)
```java
// Bad
class OrderData { ... }
class CustomerInfo { ... }
void processData() { ... }

// Good
class Order { ... }
class Customer { ... }
void calculateTotal() { ... }
```

### 5. 축약어 (Abbreviations)
```java
// Bad
int qty;
String custNm;

// Good
int quantity;
String customerName;
```

### 6. 중요 정보 생략 (Missing Information)
정보가 없으면서 정보가 있는 것처럼 보이는 이름 — 가장 위험한 종류.
```java
// Bad
void process() { ... }
void handle() { ... }
void execute() { ... }

// Good
void placeOrder() { ... }
void refundPayment() { ... }
```

### 7. Junk Drawer 클래스
이름이 모호해서 온갖 책임이 계속 누적되는 클래스.
```java
// Bad: 계속 커지는 MemberService (등록·포인트·알림·통계...)

// Good: 책임별 분리
class MemberRegistration { ... }
class MemberPointsCalculator { ... }
```

## 적용 기준

### 적용 대상
- 단일 문자 변수명 (위 "한 글자 이름 허용 기준" 표의 허용 케이스 제외)
- 타입 반복 이름
- -er/-Utils 클래스
- 불용어 포함 이름
- 축약어 사용
- 중요 정보 생략 이름 (`process`, `handle`, `execute`)
- 한 개념에 여러 단어 혼용 (`fetch`/`retrieve`/`get` 혼재)
- Scope Rule 방향 위반 (public인데 장황, private인데 모호)
- 의도를 드러내지 않는 이름

### 적용 제외
- **루프 인덱스**: `i, j, k`는 관례상 허용 (1~5줄)
- **exception 핸들러**: `e`는 3줄 이내 핸들러에서 허용
- **수학 공식**: `x, y, z`는 맥락상 명확한 경우 허용
- **도메인 표준 용어**: 업계 표준 축약어 (HTTP, URL, ID)

## OUTPUT FORMAT

### 실행 절차

공통 골격(대상 파일 수집 → 후보 제시(계열별 승인 규칙) → 적용 → 테스트 → 커밋/되돌리기, 브랜치·PR이
필요한 조건)은 이 스킬 디렉터리 기준 `../../references/refactoring-procedure.md`가 정본이다.
아래는 이 기법에 고유한 부분만 규정한다.

#### 후보 식별 — Collapse All + Naming Smells 탐지 (공통 절차 2단계)

- IDE Collapse All (구조만 보기)
- Naming Smells 패턴 탐지:
  - 타입 반복 (orderList, nameString)
  - -er/-Utils 클래스
  - 불용어 (Data, Info, Manager)
  - 단일 문자 변수 (허용 기준 표 외)
  - 축약어 (qty, nm, addr)
  - 중요 정보 생략 (process, handle, execute)
  - Junk Drawer 클래스 (계속 커지는 XxxService)
  - 한 개념 여러 단어 (fetch/retrieve/get 혼재)
- 6단계 네이밍 프로세스로 현재 단계 평가
- 제안 이름 검증 체크리스트: 의도(why)가 드러나는가 / 발음·검색 가능한가 / 오해 소지가 없는가 / 품사가 올바른가 / scope에 맞는 길이인가 / 인코딩·접두사가 없는가 / 도메인 용어를 사용했는가

#### 후보 제시 예시 (공통 절차 3단계)

```
발견된 Naming Smells 5개:

1. OrderProcessor.java (클래스)
   현재: OrderProcessor
   단계: 2 (Honest) - -er 클래스
   제안: OrderService (단계 5: Intent Revealing)

2. OrderProcessor.java:15 (변수)
   현재: List<Order> orderList
   단계: 2 (Honest) - 타입 반복
   제안: List<Order> pendingOrders (단계 5: Intent Revealing)

3. Customer.java:30 (메서드)
   현재: void processData()
   단계: 2 (Honest) - 불용어
   제안: void calculateLoyaltyPoints() (단계 6: Domain Abstraction)

→ 승인 없이 적용 (Tidy 계열)
```

#### 리팩토링 적용 — IDE Rename (공통 절차 4단계)

- IDE의 Rename 리팩토리 사용 (모든 참조 자동 업데이트)
- 한 번에 하나씩 적용 (충돌 방지)

커밋 메시지: `refactor: improve naming in <클래스명>` (공통 절차 6단계)

### 출력 예시
```
완료: Naming Process

변경 내용:
- OrderProcessor.java → OrderService.java
  (단계 2 → 5: -er 제거)
  
- orderList → pendingOrders (단계 2 → 5: 타입 반복 제거)

- processData() → calculateLoyaltyPoints()
  (단계 2 → 6: 불용어 제거, 도메인 언어 사용)

테스트: 모든 테스트 통과 (23 tests)
커밋: refactor: improve naming in OrderService

제안: Customer.java에 축약어 3개가 남아 있음. 다음 리팩토링 대상에 포함한다.
```

## FAILURE CONDITIONS

공통 실패 조건(계열별 승인 규칙 위반, 테스트 실패 방치, 테스트 수정, 커밋 단위, `git add -A`, heredoc
한글 메시지)은 `../../references/refactoring-procedure.md`에 있다. 아래는 이 기법에 고유한 것만.

- [ ] 루프 인덱스(i, j, k)나 3줄 이내 exception 핸들러(e)를 불필요하게 변경함
- [ ] 도메인 표준 용어(HTTP, URL)를 축약어로 판단하여 변경함
- [ ] Parts of Speech 위반 (클래스가 동사, 메서드가 명사 등)
- [ ] Scope Rule 방향을 반대로 적용 (변수를 scope 클수록 짧게, public 함수를 길게)
- [ ] 같은 개념에 다른 단어를 새로 도입 (기존 `get` 계열인데 `fetch`로 rename)

## 더 읽을거리 (비-load-bearing)

이 스킬의 원칙·표는 아래 vault 문서를 소스로 보강되었다. **런타임 의존성이 아니며**, 없어도 스킬은 완전하게 동작한다.

- vault: `999-MOC/Clean-Code-2nd-Edition-Naming-원칙과-실천법.md` — 7가지 원칙, Scope Rule 심화(1판 vs 2판), 한 글자 허용 기준, 요소별 패턴의 원 노트
- Robert C. Martin, *Clean Code 2nd Edition* Ch.4 Meaningful Names
- Emily Bache, *Trustworthy Code with Naming as a Process* — Arlo Belshee 6단계 라이브 데모
