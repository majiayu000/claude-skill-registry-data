---
name: explicit-parameters
description: 암묵적 의존성(전역 변수·클래스 필드·싱글턴 접근)을 명시적 파라미터로 전환하여 메서드 투명성 향상. "숨은 의존성 드러내", "필드 대신 파라미터로", "전역 참조 제거", "/explicit-parameters" 요청 시 사용. 단, 파라미터가 많아져 묶어야 하면 /introduce-parameter-object, I/O와 계산 분리는 /segregate-functional-core가 적합. /explicit-parameters [commit-ref]로 호출.
argument-hint: "[commit-ref]"
---

# Explicit Parameters

## GOAL

암묵적 의존성(전역변수, 클래스 필드, Singleton)을 명시적 파라미터로 전환하여:
- 함수 시그니처로 의존성을 명확히 표현
- 테스트 용이성 향상 (의존성 주입 가능)
- 숨겨진 결합도 제거

## CONSTRAINTS

- **계열**: System-wide — 후보 제시 후 **승인 받고 적용** (`../../references/refactoring-procedure.md` §0·§3-B)
- **동작 변경 금지**: 구조 개선만 수행 (기능 변경 없음)
- **테스트 수정 금지**: 구조 변경이 테스트를 실패시키면 되돌리기
- **사용자 확인 필수**: 자동 적용 금지
- **명시적 git add**: `git add -A` 금지, 변경된 파일만 명시

## 적용 패턴

### Before: 필드에 암묵적 의존
```java
class OrderService {
    private DiscountPolicy discountPolicy;
    private TaxCalculator taxCalculator;
    
    double calculateTotal(Order order) {
        double discount = discountPolicy.calculate(order.getSubtotal());
        double tax = taxCalculator.calculate(order.getSubtotal() - discount);
        return order.getSubtotal() - discount + tax;
    }
}
```

### After: 명시적 파라미터
```java
class OrderService {
    double calculateTotal(Order order, DiscountPolicy discountPolicy, TaxCalculator taxCalculator) {
        double discount = discountPolicy.calculate(order.getSubtotal());
        double tax = taxCalculator.calculate(order.getSubtotal() - discount);
        return order.getSubtotal() - discount + tax;
    }
}
```

### 추가 예시: Singleton 의존성 제거
```java
// Before: 전역 상태 참조
double applyRate() {
    return amount * CurrencyConverter.getInstance().getRate("USD");
}

// After: 명시적 파라미터
double applyRate(CurrencyConverter converter) {
    return amount * converter.getRate("USD");
}
```

### 파라미터 과다 시: Introduce Parameter Object
```java
// 파라미터 3개 이상 시
class OrderService {
    double calculateTotal(Order order, PricingContext context) {
        double discount = context.getDiscountPolicy().calculate(order.getSubtotal());
        double tax = context.getTaxCalculator().calculate(order.getSubtotal() - discount);
        return order.getSubtotal() - discount + tax;
    }
}

class PricingContext {
    private final DiscountPolicy discountPolicy;
    private final TaxCalculator taxCalculator;
    // constructor, getters...
}
```

## 적용 기준

### 적용 대상
- 클래스 필드를 메서드 내에서만 참조
- Singleton 패턴으로 전역 접근하는 의존성
- 테스트 시 Mocking이 필요한 의존성
- 순수 함수로 전환 가능한 메서드

### 적용 제외
- **생성자 주입으로 관리되는 필드**: DI 컨테이너 관리 대상
- **도메인 상태 필드**: 객체의 본질적 상태 (e.g., `Customer.name`)
- **불변 상수**: `private static final` 값
- **파라미터 수 과다**: 3개 이상이면 Parameter Object 고려
- **Method Object의 입력·계산 상태 필드**: 인자 전달 최소화가 그 객체의 존재 이유 — 이 스킬의 대상은 협력 객체 의존성이지 계산 상태가 아니다 (extract-method-object의 "추출 후 데이터 결정" 참조)

### 주의사항
- 파라미터 개수 증가는 신중히 판단
- 호출부 모두 업데이트 필요 (IDE 리팩터링 활용)
- 순수 함수화가 목적이라면 필드 제거까지 진행

## OUTPUT FORMAT

### 실행 절차

공통 골격(대상 파일 수집 → 후보 제시(계열별 승인 규칙) → 적용 → 테스트 → 커밋/되돌리기, 브랜치·PR이
필요한 조건)은 이 스킬 디렉터리 기준 `../../references/refactoring-procedure.md`가 정본이다.
아래는 이 기법에 고유한 부분만 규정한다.

#### 후보 식별 (공통 절차 2단계)

- 메서드 내에서만 참조되는 필드 탐지
- Singleton 패턴 호출 탐지
- 전역 변수 참조 탐지
- 각 후보에 대해:
  - 파일명 및 라인 번호
  - Before/After 코드 미리보기
  - 영향받는 호출부 수 (Change Impact)

#### 후보 제시 예시 (공통 절차 3단계)

```
발견된 후보 2개:

1. OrderService.java:25 calculateTotal()
   필드 의존: discountPolicy, taxCalculator
   → 파라미터로 전환 (영향받는 호출부 5곳)

2. PaymentProcessor.java:40 processPayment()
   Singleton 의존: Logger.getInstance()
   → 파라미터로 전환 (영향받는 호출부 3곳)

적용하시겠습니까? (yes / no / 수정)
파라미터 3개 이상이면 Parameter Object 생성을 제안합니다.
```

#### 리팩토링 적용 (공통 절차 4단계)

- 메서드 시그니처에 파라미터 추가
- 필드 참조를 파라미터 참조로 치환
- 모든 호출부에서 인자 전달
- (선택) 필드가 다른 곳에서 사용 안 되면 제거
- (선택) 파라미터 3개 이상 시 Parameter Object 생성

커밋 메시지: `refactor: explicit parameters in <클래스명>` (공통 절차 6단계)

### 출력 예시
```
완료: Explicit Parameters

변경 내용:
- OrderService.java: calculateTotal() 파라미터 추가 (2개)
  → discountPolicy, taxCalculator
- PaymentProcessor.java: processPayment() Singleton 제거
  → logger 파라미터 추가

영향받는 호출부: 8곳 자동 업데이트

테스트: 모든 테스트 통과 (23 tests)
커밋: refactor: explicit parameters in OrderService, PaymentProcessor

제안: OrderService.calculateTotal()은 파라미터 3개 이상입니다.
   Introduce Parameter Object를 고려해보세요.
```

## FAILURE CONDITIONS

공통 실패 조건(계열별 승인 규칙 위반, 테스트 실패 방치, 테스트 수정, 커밋 단위, `git add -A`, heredoc
한글 메시지)은 `../../references/refactoring-procedure.md`에 있다. 아래는 이 기법에 고유한 것만.

- [ ] 도메인 상태 필드를 파라미터로 전환함
- [ ] 생성자 주입 필드를 파라미터로 전환함 (DI 컨테이너 방해)
- [ ] 파라미터 5개 이상으로 증가 (Parameter Object 미적용)
