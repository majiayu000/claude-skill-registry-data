---
name: decompose-conditional
description: 복잡한 if/then/else의 조건식과 각 분기를 의미 있는 메서드로 추출하여 가독성 향상. "조건문 분해", "if 가독성", "복잡한 조건식에 이름 붙여", "/decompose-conditional" 요청 시 사용. 단, 같은 결과를 내는 조건문들을 하나로 합치는 것은 /consolidate-conditional, 타입별 분기를 클래스로 바꾸는 것은 /replace-conditional-with-poly가 적합. /decompose-conditional [commit-ref]로 호출.
argument-hint: "[commit-ref]"
---

# Decompose Conditional

## GOAL

복잡한 조건문(if/then/else)을 의미 있는 이름의 메서드로 분해하여:
- 조건식의 의도를 명확한 메서드명으로 표현
- 분기별 로직을 독립적 메서드로 분리
- 가독성 및 재사용성 향상

Guard Clauses와 상호 보완:
- **Guard Clauses**: 중첩 해결 (early return)
- **Decompose Conditional**: 조건식 복잡성 해결 (의미 부여)

## CONSTRAINTS

- **계열**: Tidy — 후보 보고 후 **승인 없이 적용** (`../../references/refactoring-procedure.md` §0·§3-A)
- **동작 변경 금지**: 구조 개선만 수행 (기능 변경 없음)
- **테스트 수정 금지**: 구조 변경이 테스트를 실패시키면 되돌리기
- **명시적 git add**: `git add -A` 금지, 변경된 파일만 명시
- **Extract Method 포함**: 단일 클래스 내 완결 시에만 적용

## 적용 패턴

### Before: 복잡한 조건식
```java
if (date.isBefore(SUMMER_START) || date.isAfter(SUMMER_END)) {
    charge = quantity * winterRate + winterServiceCharge;
} else {
    charge = quantity * summerRate;
}
```

### After: 조건식과 분기 모두 추출
```java
if (isWinter(date)) {
    charge = winterCharge(quantity);
} else {
    charge = summerCharge(quantity);
}

private boolean isWinter(LocalDate date) {
    return date.isBefore(SUMMER_START) || date.isAfter(SUMMER_END);
}

private double winterCharge(int quantity) {
    return quantity * winterRate + winterServiceCharge;
}

private double summerCharge(int quantity) {
    return quantity * summerRate;
}
```

### 추가 예시: 복합 조건
```java
// Before
if (customer.isPremium() && order.getTotal() > 1000 || 
    customer.isVip() && order.getTotal() > 500) {
    applySpecialDiscount();
} else {
    applyStandardDiscount();
}

// After
if (eligibleForSpecialDiscount(customer, order)) {
    applySpecialDiscount();
} else {
    applyStandardDiscount();
}

private boolean eligibleForSpecialDiscount(Customer customer, Order order) {
    return customer.isPremium() && order.getTotal() > 1000 ||
           customer.isVip() && order.getTotal() > 500;
}
```

### 추가 예시: 중첩 조건 + Guard Clause 병행
```java
// Before
if (isActive) {
    if (hasPermission) {
        if (isValidDate) {
            processRequest();
        }
    }
}

// After (Guard Clause + Decompose Conditional)
if (!isActive) return;
if (!hasPermission) return;
if (!isValidDate) return;
processRequest();
```

## 적용 기준

### 적용 대상
- 복잡한 boolean 표현식 (AND/OR 2개 이상)
- 분기 로직이 의미 있는 단위로 추출 가능
- 여러 곳에서 유사한 조건 사용
- 삼항 연산자가 중첩된 경우

### 적용 제외
- **단순 조건**: `if (x > 0)` 같은 간단한 표현식
- **단일 분기**: else가 없고 분기 로직이 1줄
- **다른 클래스 의존**: 추출한 메서드가 다른 클래스를 요구하는 경우
- **테스트 전용 조건**: 프로덕션 코드에 없는 테스트 케이스

### 주의사항
- Guard Clause와 함께 사용하면 효과 극대화
- Extract Method가 단일 클래스 내 완결되지 않으면 적용 보류
- 조건식만 추출하거나 분기만 추출하는 부분 적용도 가능

## OUTPUT FORMAT

### 실행 절차

공통 골격(대상 파일 수집 → 후보 제시(계열별 승인 규칙) → 적용 → 테스트 → 커밋/되돌리기, 브랜치·PR이
필요한 조건)은 이 스킬 디렉터리 기준 `../../references/refactoring-procedure.md`가 정본이다.
아래는 이 기법에 고유한 부분만 규정한다.

#### 후보 식별 (공통 절차 2단계)

- 복잡한 boolean 표현식 탐지 (AND/OR 연산자 다수)
- 분기 로직이 2줄 이상인 if/else
- 각 후보에 대해:
  - 파일명 및 라인 번호
  - Before/After 코드 미리보기
  - 추출 범위 (조건만 / 분기만 / 둘 다)

#### 후보 제시 예시 (공통 절차 3단계)

```
발견된 후보 3개:

1. PricingService.java:30
   조건: date.isBefore(SUMMER_START) || date.isAfter(SUMMER_END)
   분기: charge = quantity * winterRate + winterServiceCharge
   → isWinter(date) 메서드 + winterCharge(quantity) 메서드

2. AuthService.java:45
   조건: customer.isPremium() && order.getTotal() > 1000 || ...
   분기: 간단 (1줄씩)
   → eligibleForSpecialDiscount(customer, order) 메서드만 추출

→ 승인 없이 적용 (Tidy 계열)
```

#### 리팩토링 적용 (공통 절차 4단계)

- 조건식을 boolean 반환 메서드로 추출
- 분기 로직을 독립 메서드로 추출
- 원본 if/else를 메서드 호출로 간소화
- (선택) Guard Clause 병행 적용 제안

커밋 메시지: `refactor: decompose conditional in <클래스명>` (공통 절차 6단계)

### 출력 예시
```
완료: Decompose Conditional

변경 내용:
- PricingService.java:30
  조건: isWinter(date) 메서드 추출
  분기: winterCharge(), summerCharge() 메서드 추출
  
- AuthService.java:45
  조건: eligibleForSpecialDiscount() 메서드 추출
  분기: 그대로 유지 (간단)

테스트: 모든 테스트 통과 (23 tests)
커밋: refactor: decompose conditional in PricingService, AuthService

제안: AuthService.java:52에 중첩 조건이 남아 있습니다.
   Guard Clause 적용을 고려해보세요.
```

## FAILURE CONDITIONS

공통 실패 조건(계열별 승인 규칙 위반, 테스트 실패 방치, 테스트 수정, 커밋 단위, `git add -A`, heredoc
한글 메시지)은 `../../references/refactoring-procedure.md`에 있다. 아래는 이 기법에 고유한 것만.

- [ ] Extract Method가 다른 클래스를 요구함 (단일 클래스 내 완결 실패)
- [ ] 단순 조건(`if (x > 0)`)을 불필요하게 추출함
