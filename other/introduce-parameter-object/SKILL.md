---
name: introduce-parameter-object
description: 반복되는 파라미터 그룹을 객체로 치환(IPO)하거나, 객체에서 꺼낸 값 대신 객체 자체를 전달(Preserve Whole Object). "파라미터 객체", "인자가 너무 많아", "start·end 대신 Range로", "/introduce-parameter-object" 요청 시 사용. 단, 결과 객체가 검증·연산을 가진 도메인 값이면 /discover-value-object가 적합. /introduce-parameter-object [commit-ref]로 호출.
argument-hint: "[commit-ref]"
---

# Introduce Parameter Object / Preserve Whole Object

상황에 따라 두 가지 기법 중 적합한 것을 선택:

- **Introduce Parameter Object (IPO)**: 파라미터에 행위를 추가해야 할 때 → 새 객체 생성 → 행위 이동 → Value Object 발견
- **Preserve Whole Object (PWO)**: 기존 객체에서 값을 꺼내 전달할 때 → 객체 자체를 전달하여 파라미터 수 감소

## GOAL

- **성공 = 반복 파라미터가 IPO 또는 PWO로 정리되어 커밋 완료됨**
- IPO: 파라미터 그룹이 Parameter Object로 치환되고 관련 행위가 이동됨
- PWO: 객체에서 꺼낸 값들이 객체 자체 전달로 대체됨
- 사용자 확인 후 적용
- 모든 테스트 통과

## 기법 선택 기준

| 상황 | 적용 기법 | 이유 |
|---|---|---|
| 파라미터들이 이미 하나의 객체에서 꺼내져 전달됨 | **Preserve Whole Object** | 객체가 이미 존재 — 꺼내지 말고 그대로 전달 |
| 파라미터에 대한 행위를 추가해야 하는 경우 | **Introduce Parameter Object** | 새 객체 생성 → 행위 이동 → Value Object 발견 |

### IPO의 진짜 목적

> "더 큰 혜택은 파라미터 그룹에 대해서 동작하는 행위들을 파라미터 객체로 이동시킬 수 있는 것" — Fowler, Ch10

IPO는 파라미터 묶기 자체가 목적이 아니라, **Value Object를 발견하는 시작점**:

```
Introduce Parameter Object
  → Move Instance Method (관련 로직을 Parameter Object로 이동)
    → Value Object 탄생 (데이터 + 행위를 가진 객체)
```

### 적용하면 안 되는 경우

| 상황 | 이유 |
|---|---|
| 파라미터 간에 논리적 관계가 없음 | 논리 관계 없이 그룹화하면 의미 없는 객체가 생성됨 |
| 한 메서드에서만 사용되는 파라미터 조합 | 반복이 없으면 추상화의 가치 없음 |
| 파라미터 객체에 이동할 행위가 없음 | 단순 DTO가 되어 Anemic Domain Model 유발 (이 경우 PWO가 더 적합할 수 있음) |

## CONSTRAINTS

- **계열**: System-wide — 후보 제시 후 **승인 받고 적용** (`../../references/refactoring-procedure.md` §0·§3-B)
### Hard Rules
- **동작 변경 금지** — 구조 개선만 수행
- **테스트 수정 금지** — 구조 변경이 테스트를 실패시키면 되돌리기
- **사용자 확인 없이 리팩토링 금지** — 모든 후보는 사용자 승인 후 실행
- **커밋 단위** — 1파일 x 1기법 = 1커밋 (논리적으로 연결된 파일은 함께)
- **git add -A 금지** — 변경된 파일만 명시적으로 추가

## 적용 패턴

Introduce Parameter Object 리팩토링 단계:

1. **반복 파라미터 그룹 식별**
   - 3개 이상의 파라미터가 함께 전달되는 패턴
   - 2곳 이상에서 동일한 파라미터 조합 반복

2. **Parameter Object 클래스 생성**
   - 논리적으로 관련된 파라미터를 하나의 클래스로
   - record 또는 immutable class 사용 (Java 14+)
   - 의미 있는 이름 부여

3. **메서드 시그니처 변경**
   - 개별 파라미터를 Parameter Object로 치환
   - 호출자 코드 업데이트

4. **관련 동작 이동 (선택적)**
   - Parameter Object와 관련된 로직을 객체 내부로 이동
   - Value Object로 발전 가능

### Before/After 예시

```java
// Before: 반복되는 파라미터 그룹
public class PriceService {
    public void processPrice(int originalPrice, int discountedPrice, String currency) {
        // 처리 로직
        validatePrice(originalPrice, discountedPrice, currency);
        formatPrice(originalPrice, discountedPrice, currency);
    }
    
    private void validatePrice(int originalPrice, int discountedPrice, String currency) {
        if (originalPrice < 0 || discountedPrice < 0) {
            throw new IllegalArgumentException("Price cannot be negative");
        }
        if (discountedPrice > originalPrice) {
            throw new IllegalArgumentException("Discounted price cannot exceed original");
        }
    }
    
    private String formatPrice(int originalPrice, int discountedPrice, String currency) {
        double discount = (originalPrice - discountedPrice) * 100.0 / originalPrice;
        return String.format("%s %.0f%% off: %d -> %d", 
            currency, discount, originalPrice, discountedPrice);
    }
}

// After: Parameter Object 적용
record Price(int original, int discounted, String currency) {
    // 생성자에서 검증
    public Price {
        if (original < 0 || discounted < 0) {
            throw new IllegalArgumentException("Price cannot be negative");
        }
        if (discounted > original) {
            throw new IllegalArgumentException("Discounted price cannot exceed original");
        }
    }
    
    // 관련 동작을 객체 내부로 이동
    public double discountPercentage() {
        return (original - discounted) * 100.0 / original;
    }
    
    public String formatted() {
        return String.format("%s %.0f%% off: %d -> %d", 
            currency, discountPercentage(), original, discounted);
    }
}

public class PriceService {
    public void processPrice(Price price) {
        // Parameter Object 하나만 전달
        // 검증은 Price 생성자에서 자동 수행
        String formatted = price.formatted();
    }
}
```

### Preserve Whole Object 패턴

```java
// Before: 객체에서 값을 꺼내서 전달
int low = temperatureRange.getLow();
int high = temperatureRange.getHigh();
boolean withinRange = plan.isWithinRange(low, high);

// After: 객체 자체를 전달
boolean withinRange = plan.isWithinRange(temperatureRange);
```

```java
// Before: DTO에서 여러 값을 꺼내서 전달
String name = request.getName();
String email = request.getEmail();
int age = request.getAge();
User user = createUser(name, email, age);

// After: 객체 자체를 전달
User user = createUser(request);
```

## 적용 기준

Introduce Parameter Object를 적용해야 하는 경우:

1. **파라미터 수**: 3개 이상의 파라미터가 함께 전달
2. **반복 패턴**: 동일한 파라미터 조합이 2회 이상 반복
3. **논리적 관계**: 파라미터들이 논리적으로 관련 있음
4. **함께 검증**: 파라미터들이 함께 검증되어야 함
5. **동시 변경**: 파라미터들이 함께 변경되는 경향

## OUTPUT FORMAT

### 실행 절차

공통 골격(대상 파일 수집 → 후보 제시(계열별 승인 규칙) → 적용 → 테스트 → 커밋/되돌리기, 브랜치·PR이
필요한 조건)은 이 스킬 디렉터리 기준 `../../references/refactoring-procedure.md`가 정본이다.
아래는 이 기법에 고유한 부분만 규정한다.

#### 반복 파라미터 그룹 후보 식별 (공통 절차 2단계)

대상 파일에서 다음 패턴을 찾는다:

**패턴 A: Introduce Parameter Object**
- 3개 이상의 파라미터를 받는 메서드
- 동일한 파라미터 조합이 2곳 이상에서 반복
- 파라미터들이 논리적으로 관련 있음 (같은 도메인 개념)
- 파라미터에 대한 계산/검증 로직이 여러 곳에서 중복
- Move Method의 전 단계로 파라미터를 묶어야 하는 경우

**패턴 B: Preserve Whole Object**
- 하나의 객체에서 여러 값을 꺼내어 다른 메서드에 전달
- `obj.getX()`, `obj.getY()`, `obj.getZ()`를 꺼낸 뒤 `method(x, y, z)` 호출
- 객체 자체를 전달하면 파라미터 수가 줄어드는 경우

#### 후보 제시 예시 (공통 절차 3단계)

후보를 하나씩 제시하고 사용자 확인:

```
## 리팩토링 후보 1: Introduce Parameter Object

**파일**: PriceService.java
**반복 파라미터**: (int originalPrice, int discountedPrice, String currency)

**반복 위치** (3곳):
1. processPrice() 메서드
2. validatePrice() 메서드
3. formatPrice() 메서드

**현재 시그니처**:
void processPrice(int originalPrice, int discountedPrice, String currency)
void validatePrice(int originalPrice, int discountedPrice, String currency)
String formatPrice(int originalPrice, int discountedPrice, String currency)

**제안 변경**:
1. Price record 생성 (original, discounted, currency)
2. 검증 로직을 Price 생성자로 이동
3. 포맷팅 로직을 Price.formatted()로 이동
4. 모든 메서드 시그니처를 Price로 변경

**적용할까요?** (yes / no / 수정 요청)
```

```
## 리팩토링 후보 2: Preserve Whole Object

**파일**: HeatingPlan.java
**현재**: temperatureRange에서 low, high를 꺼내어 isWithinRange(low, high) 호출
**제안**: isWithinRange(temperatureRange)로 변경

적용할까요? (yes / no / 수정 요청)
```

- 사용자가 **yes** → 실행 목록에 추가
- 사용자가 **no** → 스킵
- 사용자가 **수정 요청** → 요청 반영 후 재제시

모든 후보 확인 후 최종 실행 목록을 보여주고 진행 여부 확인.

#### Parameter Object 도입 실행 (공통 절차 4단계)

확정된 리팩토링을 하나씩 수행:

1. Parameter Object 클래스(record) 생성
2. 검증 로직을 생성자로 이동
3. 관련 동작을 객체 메서드로 이동
4. 메서드 시그니처 변경
5. 호출자 코드 업데이트

**커밋 메시지 형식**:
```
refactor: introduce parameter object [객체명] in [클래스명]
```

#### 결과 보고

사용자에게 보고:
- 적용된 Parameter Object 목록

## 실전 리팩토링 경로 (Vault 사례)

### 사례 1: SequenceKey
```
Extract Method → Introduce Parameter Object → Move Instance Method → Convert Record to Class
```
효과: sequenceKey가 String → Value Object로 승격. format, increase 로직이 Value Object로 이동.

### 사례 2: ProductPrice
```
Split Conditional → Extract Method → Introduce Parameter Object → Move Instance Method
```
효과: isDiscounted, getFinalPrice가 ProductPrice로 이동. 독립 테스트 가능.

### 사례 3: StockChecker (빵속빵 패턴)
```
빵속빵(FCIS) 구조 만들기 → DTO 의존성을 파라미터로 전환 → Parameter Object 생성 → 관련 메서드 이동
```
패턴: Move Method 전 단계로 파라미터를 먼저 묶음.

### 공통 패턴
```
IPO → Move Instance Method → Value Object 탄생
```

## FAILURE CONDITIONS

공통 실패 조건(계열별 승인 규칙 위반, 테스트 실패 방치, 테스트 수정, 커밋 단위, `git add -A`, heredoc
한글 메시지)은 `../../references/refactoring-procedure.md`에 있다. 아래는 이 기법에 고유한 것만.

- 논리적 관계 없는 파라미터를 억지로 묶음 (불필요한 결합)
- 1곳에만 사용되는 파라미터 그룹에 적용 (과도한 추상화)
- mutable Parameter Object 생성 (불변성 보장 필요)
