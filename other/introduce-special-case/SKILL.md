---
name: introduce-special-case
description: 반복되는 null 검사를 Special Case(Null Object) 클래스로 대체하여 다형성으로 처리. "null 객체 패턴", "null 체크 반복 제거", "특수 케이스 클래스", "/introduce-special-case" 요청 시 사용. 단, 단순 전제 조건 명시는 /introduce-assertion, 타입별 분기 전반은 /replace-conditional-with-poly가 적합. /introduce-special-case [commit-ref]로 호출.
argument-hint: "[commit-ref]"
---

# Introduce Special Case (Null Object)

## GOAL

- **성공 = 반복 null 검사가 Special Case 클래스로 대체되어 커밋 완료됨**
- 동일 타입에 대한 null 검사가 3곳 이상 반복됨
- null일 때의 기본 동작이 Special Case 클래스에 캡슐화됨
- 호출처의 null 검사가 제거됨
- 모든 테스트 통과

## CONSTRAINTS

- **계열**: System-wide — 후보 제시 후 **승인 받고 적용** (`../../references/refactoring-procedure.md` §0·§3-B)
### Hard Rules
- **동작 변경 금지** — 구조 개선만 수행
- **테스트 수정 금지** — 구조 변경이 테스트를 실패시키면 되돌리기
- **사용자 확인 없이 리팩토링 금지** — 모든 후보는 사용자 승인 후 실행
- **커밋 단위** — 단계별 커밋 (Special Case 생성 → 소스 수정 → 호출처 정리)
- **git add -A 금지** — 변경된 파일만 명시적으로 추가

## 적용 패턴

### Before: null 검사가 여러 곳에 산재
```java
public String getCustomerName(Site site) {
    Customer customer = site.getCustomer();
    if (customer == null) {
        return "occupant";
    }
    return customer.getName();
}

public BillingPlan getBillingPlan(Site site) {
    Customer customer = site.getCustomer();
    if (customer == null) {
        return BillingPlan.basic();
    }
    return customer.getBillingPlan();
}

public int getWeeksDelinquent(Site site) {
    Customer customer = site.getCustomer();
    if (customer == null) {
        return 0;
    }
    return customer.getPaymentHistory().getWeeksDelinquent();
}
```

### After: Special Case 객체 도입
```java
// Step 1: Special Case 클래스 생성
public class UnknownCustomer extends Customer {
    @Override
    public String getName() { return "occupant"; }

    @Override
    public BillingPlan getBillingPlan() { return BillingPlan.basic(); }

    @Override
    public PaymentHistory getPaymentHistory() {
        return PaymentHistory.empty();
    }

    @Override
    public boolean isUnknown() { return true; }
}

// Step 2: 소스에서 null 대신 Special Case 반환
public class Site {
    public Customer getCustomer() {
        return (customer == null) ? new UnknownCustomer() : customer;
    }
}

// Step 3: 호출처 — null 검사 제거
public String getCustomerName(Site site) {
    return site.getCustomer().getName();
}

public BillingPlan getBillingPlan(Site site) {
    return site.getCustomer().getBillingPlan();
}

public int getWeeksDelinquent(Site site) {
    return site.getCustomer().getPaymentHistory().getWeeksDelinquent();
}
```

### 추가 예시: 인터페이스 기반
```java
// 대상이 인터페이스인 경우
public interface PaymentMethod {
    String charge(int amount);
    String getDescription();
}

public class NullPaymentMethod implements PaymentMethod {
    @Override
    public String charge(int amount) { return "no-op"; }

    @Override
    public String getDescription() { return "No payment method on file"; }
}
```

## 적용 기준

### 적용 대상
- 동일 타입에 대한 null 검사가 **3곳 이상** 반복
- null일 때의 기본값/기본 동작이 **일관됨**
- 대상 타입이 **상속 또는 인터페이스 구현 가능** (final 아님)
- null 처리 로직이 흩어져 있어 일관성 유지가 어려운 경우

### 적용 제외
- **null 검사 1-2곳**: 과도한 추상화
- **동작이 호출처마다 다름**: 일관된 기본 동작이 없으면 Special Case 불가
- **외부 라이브러리 클래스**: 상속 불가
- **Optional로 충분**: Optional로 이미 처리되거나 Optional이 더 적합한 경우
- **final 클래스**: 상속 불가능

## OUTPUT FORMAT

### 실행 절차

공통 골격(대상 파일 수집 → 후보 제시(계열별 승인 규칙) → 적용 → 테스트 → 커밋/되돌리기, 브랜치·PR이
필요한 조건)은 이 스킬 디렉터리 기준 `../../references/refactoring-procedure.md`가 정본이다.
아래는 이 기법에 고유한 부분만 규정한다.

#### null 검사 반복 패턴 탐지 (공통 절차 2단계)

대상 파일에서 다음 패턴을 찾는다:

- 동일 타입에 대한 `== null` 또는 `!= null` 검사가 3곳 이상
- null일 때 반환하는 기본값이 일관됨
- 대상 타입이 상속/구현 가능

#### 후보 제시 예시 (공통 절차 3단계)

후보를 하나씩 제시하고 사용자 확인:

```
## 리팩토링 후보 1: Introduce Special Case

**대상 타입**: Customer
**null 검사 위치** (4곳):
1. OrderService.java:30 → null이면 "occupant" 반환
2. BillingService.java:45 → null이면 BillingPlan.basic() 반환
3. ReportService.java:20 → null이면 0 반환
4. NotificationService.java:55 → null이면 스킵

**기본 동작 일관성**: 일관됨 (1-3은 일관된 기본값, 4는 스킵)

**제안**:
1. UnknownCustomer extends Customer 생성
2. Site.getCustomer()에서 null 대신 UnknownCustomer 반환
3. 호출처 4곳의 null 검사 제거

**적용할까요?** (yes / no / 수정 요청)
```

#### Special Case 도입 실행 (공통 절차 4단계)

**커밋 1: Special Case 클래스 생성**
1. Special Case 클래스 작성 (상속 또는 인터페이스 구현)
2. 기본값을 반환하는 메서드 오버라이드
3. isUnknown() 메서드 추가
4. 커밋: `refactor: introduce special case <클래스명>`

**커밋 2: 소스에서 null 대신 Special Case 반환**
1. null을 반환하던 곳에서 Special Case 인스턴스 반환
2. 커밋: `refactor: return <Special Case> instead of null in <소스클래스>`

**커밋 3: 호출처 null 검사 제거**
1. null 검사 코드 제거
2. 직접 메서드 호출로 대체
3. 커밋: `refactor: remove null checks for <타입> in callers`

#### 결과 보고

사용자에게 보고:
- 생성된 Special Case 클래스
- 제거된 null 검사 위치

## FAILURE CONDITIONS

공통 실패 조건(계열별 승인 규칙 위반, 테스트 실패 방치, 테스트 수정, 커밋 단위, `git add -A`, heredoc
한글 메시지)은 `../../references/refactoring-procedure.md`에 있다. 아래는 이 기법에 고유한 것만.

- null일 때 동작이 호출처마다 다른데도 통합
- null 검사가 1-2곳뿐인데 적용 (과도한 추상화)
- final 클래스에 적용 시도
