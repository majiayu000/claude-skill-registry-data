---
name: replace-temp-with-query
description: 임시 변수를 메서드 호출(query)로 치환하여 중복 제거·추출 용이성 확보. "임시 변수 메서드로", "temp 제거", "지역 변수를 쿼리로", "/replace-temp-with-query" 요청 시 사용. 단, 임시 변수가 서로 얽혀 치환 불가면 /extract-method-object가 적합. /replace-temp-with-query [commit-ref]로 호출.
argument-hint: "[commit-ref]"
---

# Replace Temp with Query

## GOAL

한 번만 대입되고 여러 곳에서 사용되는 임시 변수를 의미 있는 이름의 메서드로 추출하여:
- 중복된 계산 로직 제거
- 표현식의 의미를 명확한 메서드명으로 전달
- Extract Method의 전제 조건 충족 (임시 변수 제거)

## CONSTRAINTS

- **계열**: Tidy — 후보 보고 후 **승인 없이 적용** (`../../references/refactoring-procedure.md` §0·§3-A)
- **동작 변경 금지**: 구조 개선만 수행 (기능 변경 없음)
- **테스트 수정 금지**: 구조 변경이 테스트를 실패시키면 되돌리기
- **명시적 git add**: `git add -A` 금지, 변경된 파일만 명시

## 적용 패턴

### Before
```java
double basePrice = quantity * itemPrice;
if (basePrice > 1000) {
    return basePrice * 0.95;
} else {
    return basePrice * 0.98;
}
```

### After
```java
if (basePrice() > 1000) {
    return basePrice() * 0.95;
} else {
    return basePrice() * 0.98;
}

private double basePrice() {
    return quantity * itemPrice;
}
```

### 추가 예시: 복잡한 조건식
```java
// Before
double tax = order.getTotal() * 0.1;
double shipping = order.getTotal() > 100 ? 0 : 10;
return order.getTotal() + tax + shipping;

// After
return order.getTotal() + tax() + shipping();

private double tax() { return order.getTotal() * 0.1; }
private double shipping() { return order.getTotal() > 100 ? 0 : 10; }
```

## 적용 기준

### 적용 대상
- 한 번만 대입되는 임시 변수
- 여러 곳에서 참조되는 변수
- 복잡한 표현식을 담은 변수 (의미 부여 가치 높음)
- Extract Method 전 단계로 사용

### 적용 제외
- **루프 내 누적 변수** (accumulator): `sum += value;`
- **부수효과 있는 표현식**: 메서드 호출이 상태 변경하는 경우
- **여러 번 대입되는 변수**: 값이 변경되는 경우
- **성능 크리티컬 구간**: 측정된 성능 문제가 있는 경우만

## OUTPUT FORMAT

### 실행 절차

공통 골격(대상 파일 수집 → 후보 제시(계열별 승인 규칙) → 적용 → 테스트 → 커밋/되돌리기, 브랜치·PR이
필요한 조건)은 이 스킬 디렉터리 기준 `../../references/refactoring-procedure.md`가 정본이다.
아래는 이 기법에 고유한 부분만 규정한다.

#### 후보 식별 (공통 절차 2단계)

- 임시 변수 패턴 탐지 (한 번 대입, 여러 번 참조)
- 적용 제외 조건 필터링
- 각 후보에 대해:
  - 파일명 및 라인 번호
  - Before/After 코드 미리보기
  - 적용 근거 (참조 횟수, 표현식 복잡도)

#### 후보 제시 예시 (공통 절차 3단계)

```
발견된 후보 3개:

1. OrderService.java:45
   basePrice = quantity * itemPrice
   → private double basePrice() { return quantity * itemPrice; }
   (참조 3회, 복잡도 낮음)

→ 승인 없이 적용 (Tidy 계열)
```

#### 리팩토링 적용 (공통 절차 4단계)

- 메서드 추출 (private, 원본 표현식)
- 임시 변수 참조를 메서드 호출로 치환
- 임시 변수 선언 제거

커밋 메시지: `refactor: replace temp with query in <클래스명>` (공통 절차 6단계)

### 출력 예시
```
완료: Replace Temp with Query

변경 내용:
- OrderService.java: basePrice 변수 → basePrice() 메서드
- InvoiceCalculator.java: discount 변수 → discount() 메서드

테스트: 모든 테스트 통과 (23 tests)
커밋: refactor: replace temp with query in OrderService, InvoiceCalculator
```

## FAILURE CONDITIONS

공통 실패 조건(계열별 승인 규칙 위반, 테스트 실패 방치, 테스트 수정, 커밋 단위, `git add -A`, heredoc
한글 메시지)은 `../../references/refactoring-procedure.md`에 있다. 아래는 이 기법에 고유한 것만.

- [ ] 부수효과 있는 표현식을 메서드로 추출함
- [ ] 누적 변수를 메서드로 치환함
