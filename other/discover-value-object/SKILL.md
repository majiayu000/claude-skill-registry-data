---
name: discover-value-object
description: Primitive Obsession 제거 — 검증·연산이 따라다니는 primitive 필드(금액+통화, 이메일 문자열 등)를 도메인 개념을 담은 Value Object로 치환. "값 객체 도입", "primitive obsession", "Money 클래스로", "/discover-value-object" 요청 시 사용. 단, 함께 전달되는 파라미터 묶음을 객체로 바꾸는 것은 /introduce-parameter-object, 컬렉션을 감싸는 것은 /first-class-collection이 적합. /discover-value-object [commit-ref]로 호출.
argument-hint: "[commit-ref]"
---

# Discover Value Object Skill

Primitive Obsession을 제거하여 도메인 개념을 명시적으로 표현하는 Value Object 발견.

## GOAL

- **성공 = Primitive 타입이 Value Object로 치환되어 커밋 완료됨**
- Primitive 타입(int, String 등)에 도메인 로직이 산재함
- 반복되는 검증/변환/포맷팅 로직이 식별됨
- 사용자 확인 후 Value Object 추출
- 모든 테스트 통과

## CONSTRAINTS

- **계열**: System-wide — 후보 제시 후 **승인 받고 적용** (`../../references/refactoring-procedure.md` §0·§3-B)
### Hard Rules
- **동작 변경 금지** — 구조 개선만 수행
- **테스트 수정 금지** — 구조 변경이 테스트를 실패시키면 되돌리기
- **사용자 확인 없이 리팩토링 금지** — 모든 후보는 사용자 승인 후 실행
- **커밋 단위** — 1파일 x 1기법 = 1커밋 (논리적으로 연결된 파일은 함께)
- **git add -A 금지** — 변경된 파일만 명시적으로 추가

## 적용 패턴

Discover Value Object 리팩토링 단계:

1. **Primitive Obsession 패턴 식별**
   - Entity 필드가 primitive 타입
   - 해당 primitive에 대한 검증/변환/포맷팅 로직 산재
   - 동일한 검증/변환 로직 반복

2. **Value Object 클래스 생성**
   - 도메인 개념을 명시하는 이름 부여
   - Immutable record 또는 class 사용
   - 생성자에서 검증 수행

3. **관련 로직 이동**
   - 검증 로직을 생성자로 이동
   - 변환/포맷팅 로직을 메서드로 이동
   - 비즈니스 규칙을 메서드로 캡슐화

4. **사용처 변경**
   - Entity 필드 타입을 Value Object로 변경
   - 산재된 로직을 Value Object 메서드 호출로 치환

### Before/After 예시

```java
// Before: Primitive Obsession
public class Order {
    private int amount;        // primitive 타입
    private String currency;   // primitive 타입
    
    public Order(int amount, String currency) {
        // 검증 로직 산재
        if (amount < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
        if (currency == null || currency.isEmpty()) {
            throw new IllegalArgumentException("Currency is required");
        }
        this.amount = amount;
        this.currency = currency;
    }
    
    // 비즈니스 로직 산재
    public boolean isExpensive() {
        return amount > 1000;
    }
    
    public String formattedPrice() {
        return currency + " " + amount;
    }
    
    public double convertToUSD(double exchangeRate) {
        if ("USD".equals(currency)) {
            return amount;
        }
        return amount * exchangeRate;
    }
}

// After: Value Object 추출
record Money(int amount, String currency) {
    // 생성자에서 검증
    public Money {
        if (amount < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
        if (currency == null || currency.isEmpty()) {
            throw new IllegalArgumentException("Currency is required");
        }
    }
    
    // 비즈니스 로직을 Value Object로 이동
    public boolean isOver(int threshold) {
        return amount > threshold;
    }
    
    public String formatted() {
        return currency + " " + amount;
    }
    
    public Money convertTo(String targetCurrency, double exchangeRate) {
        if (currency.equals(targetCurrency)) {
            return this;
        }
        return new Money((int) (amount * exchangeRate), targetCurrency);
    }
    
    public Money add(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("Cannot add different currencies");
        }
        return new Money(amount + other.amount, currency);
    }
}

public class Order {
    private Money price;  // Value Object
    
    public Order(Money price) {
        this.price = price;
    }
    
    // 비즈니스 로직이 간결해짐
    public boolean isExpensive() {
        return price.isOver(1000);
    }
    
    public String formattedPrice() {
        return price.formatted();
    }
}
```

## 적용 기준

Discover Value Object를 적용해야 하는 경우:

1. **Entity 필드**: primitive 타입 필드가 도메인 개념을 나타냄
2. **로직 산재**: 해당 primitive에 대한 검증/변환/포맷팅 로직이 여러 곳에 분산
3. **반복 검증**: 동일한 검증 로직이 여러 곳에서 반복
4. **비즈니스 규칙**: primitive 값에 대한 비즈니스 규칙이 존재
5. **함께 사용**: 여러 primitive가 항상 함께 사용됨 (예: amount + currency)
6. **외부 라이브러리/API 타입 직접 노출**: 3rd-party 타입(`BigDecimal`, `LocalDate`, `UUID`, JDBC `ResultSet`, 외부 API 응답 DTO 등)이 도메인 개념을 그대로 대변
   - 해당 타입에 대한 검증/변환/계산 로직이 호출부에 산재
   - 수정/상속이 불가능해 **Wrapper(composition) 형태의 Local Extension**으로 감쌈 (Fowler: Introduce Local Extension)
   - 일회성 편의 메서드만 필요하면 Value Object 대신 **Introduce Foreign Method**를 검토

**발견 후보**:
- Entity의 필드 (예: amount, price, email, phoneNumber)
- 반복되는 파라미터 (Introduce Parameter Object와 연계)
- 기능이 많은 primitive (검증/변환/포맷팅 로직 다수)
- **외부 라이브러리 타입** (예: `BigDecimal` → `Money`, `LocalDate` → `BusinessDate`, `String` UUID → `OrderId`)
- **외부 API/프로토콜 타입** (예: `PaymentApiResponse` → `PaymentResult`, `HttpResponse<String>` → `AuthToken`)

## OUTPUT FORMAT

### 실행 절차

공통 골격(대상 파일 수집 → 후보 제시(계열별 승인 규칙) → 적용 → 테스트 → 커밋/되돌리기, 브랜치·PR이
필요한 조건)은 이 스킬 디렉터리 기준 `../../references/refactoring-procedure.md`가 정본이다.
아래는 이 기법에 고유한 부분만 규정한다.

#### Value Object 후보 식별 (공통 절차 2단계)

대상 파일에서 다음 패턴을 찾는다:

- primitive 타입 필드가 도메인 개념을 나타냄
- 해당 필드에 대한 검증 로직이 2곳 이상
- 해당 필드에 대한 변환/포맷팅 메서드가 존재
- 여러 primitive가 항상 함께 사용됨
- **외부 라이브러리 타입**(`BigDecimal`, `LocalDate`, `UUID` 등)이 필드/파라미터로 직접 노출되고, 관련 계산/검증 로직이 호출부에 산재
- **외부 API 응답/DTO 타입**이 도메인 경계를 넘어 내부 로직에서 그대로 사용됨

#### 후보 제시 예시 (공통 절차 3단계)

후보를 하나씩 제시하고 사용자 확인:

```
## 리팩토링 후보 1: Discover Value Object

**파일**: Order.java
**대상**: int amount, String currency

**현재 사용**:
- 필드: private int amount; private String currency;
- 검증: 생성자, setAmount() 등 3곳에서 검증 반복
- 로직: isExpensive(), formattedPrice(), convertToUSD() 등

**현재 코드**:
[관련 코드 블록]

**제안 변경**:
1. Money record 생성 (amount, currency)
2. 검증 로직을 Money 생성자로 이동
3. 비즈니스 로직을 Money 메서드로 이동
   - isOver(threshold)
   - formatted()
   - convertTo(currency, rate)
   - add(Money)
4. Order 필드를 Money 타입으로 변경

**적용할까요?** (yes / no / 수정 요청)
```

- 사용자가 **yes** → 실행 목록에 추가
- 사용자가 **no** → 스킵
- 사용자가 **수정 요청** → 요청 반영 후 재제시

모든 후보 확인 후 최종 실행 목록을 보여주고 진행 여부 확인.

#### Value Object 추출 실행 (공통 절차 4단계)

확정된 리팩토링을 하나씩 수행:

1. Value Object record 생성
2. 검증 로직을 생성자로 이동
3. 비즈니스 로직을 메서드로 이동
4. Entity 필드 타입 변경
5. 사용처 업데이트

**커밋 메시지 형식**:
```
refactor: discover value object [객체명] in [클래스명]
```

#### 결과 보고

사용자에게 보고:
- 적용된 Value Object 목록

## FAILURE CONDITIONS

공통 실패 조건(계열별 승인 규칙 위반, 테스트 실패 방치, 테스트 수정, 커밋 단위, `git add -A`, heredoc
한글 메시지)은 `../../references/refactoring-procedure.md`에 있다. 아래는 이 기법에 고유한 것만.

- 관련 로직 없는 모든 primitive를 객체로 감쌈 (불필요한 복잡도)
- 단순 getter/setter만 있는 Value Object 생성 (의미 없음)
- mutable Value Object 생성 (불변성 필수)
