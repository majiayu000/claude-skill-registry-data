---
name: lift-up-conditional
description: 여러 메서드·분기에 중복된 동일 조건문을 상위(호출자 또는 메서드 시작)로 끌어올려 중복 제거. "조건 위로 올려", "같은 if가 여러 메서드에", "lift up", "/lift-up-conditional" 요청 시 사용. 단, 한 메서드 안에서 동일 결과를 내는 조건문 통합은 /consolidate-conditional이 적합. /lift-up-conditional [commit-ref]로 호출.
argument-hint: "[commit-ref]"
---

# Lift Up Conditional Skill

여러 곳에 중복된 조건문을 상위로 끌어올려 중복을 제거하고 코드 의도를 명확히 한다.

## GOAL

- **성공 = 중복 조건문이 상위로 끌어올려져 커밋 완료됨**
- 동일한 조건문이 여러 메서드/블록에서 반복됨
- 조건에 따라 다른 처리가 필요한 패턴 식별됨
- 후보 보고 후 조건문 끌어올리기 적용 (Tidy 계열 — 승인 없이)
- 모든 테스트 통과

## CONSTRAINTS

- **계열**: Tidy — 후보 보고 후 **승인 없이 적용** (`../../references/refactoring-procedure.md` §0·§3-A)
### Hard Rules
- **동작 변경 금지** — 구조 개선만 수행
- **테스트 수정 금지** — 구조 변경이 테스트를 실패시키면 되돌리기
- **커밋 단위** — 1파일 x 1기법 = 1커밋 (논리적으로 연결된 파일은 함께)
- **git add -A 금지** — 변경된 파일만 명시적으로 추가

## 적용 패턴

Lift Up Conditional 리팩토링 단계:

1. **중복 조건문 식별**
   - 동일한 조건식이 여러 곳에서 반복
   - 조건에 따라 다른 동작 수행

2. **조건을 변수로 추출**
   - 중복된 조건식을 boolean 변수로 추출
   - 의미 있는 변수명으로 조건 의도 명확히

3. **조건을 메서드로 추출 (선택적)**
   - 복잡한 조건은 별도 메서드로
   - 메서드명으로 조건의 비즈니스 의미 표현

4. **조건을 상위로 끌어올림**
   - Surround with if-else로 조건을 한 곳으로 모음
   - 조건 내부에서 각 메서드 호출
   - 불필요한 중간 변수 제거 (inline)

### Before/After 예시

```java
// Before: 동일 조건 중복
public class ProductService {
    public double calculatePrice(Product product) {
        if (product.isOnSale()) {
            return product.getPrice() * 0.9;  // 10% 할인
        }
        return product.getPrice();
    }
    
    public String formatLabel(Product product) {
        if (product.isOnSale()) {
            return "SALE: " + product.getName();
        }
        return product.getName();
    }
    
    public String getBadgeColor(Product product) {
        if (product.isOnSale()) {
            return "red";
        }
        return "blue";
    }
}

// After: 조건을 상위로 끌어올림
public class ProductService {
    public ProductDisplay createDisplay(Product product) {
        if (product.isOnSale()) {
            return createSaleDisplay(product);
        }
        return createNormalDisplay(product);
    }
    
    private ProductDisplay createSaleDisplay(Product product) {
        double price = product.getPrice() * 0.9;
        String label = "SALE: " + product.getName();
        String badgeColor = "red";
        return new ProductDisplay(price, label, badgeColor);
    }
    
    private ProductDisplay createNormalDisplay(Product product) {
        double price = product.getPrice();
        String label = product.getName();
        String badgeColor = "blue";
        return new ProductDisplay(price, label, badgeColor);
    }
}
```

### 단계별 리팩토링 과정

```java
// Step 1: 조건을 변수로 추출
boolean isOnSale = product.isOnSale();
if (isOnSale) { ... }

// Step 2: 조건을 메서드로 추출 (복잡한 경우)
private boolean isEligibleForDiscount(Product product) {
    return product.isOnSale() && product.getPrice() > 1000;
}

// Step 3: Surround with if-else로 조건 끌어올림
if (isEligibleForDiscount(product)) {
    double price = calculateSalePrice(product);
    String label = formatSaleLabel(product);
    String badge = getSaleBadgeColor();
} else {
    double price = calculateNormalPrice(product);
    String label = formatNormalLabel(product);
    String badge = getNormalBadgeColor();
}

// Step 4: 각 분기를 메서드로 추출 + inline
if (isEligibleForDiscount(product)) {
    return createSaleDisplay(product);
}
return createNormalDisplay(product);
```

## 적용 기준

Lift Up Conditional을 적용해야 하는 경우:

1. **조건 중복**: 동일한 조건문이 2곳 이상에서 반복
2. **논리적 연관**: 중복된 조건들이 같은 비즈니스 규칙을 나타냄
3. **일관성**: 조건이 참/거짓일 때의 처리가 여러 곳에서 일관됨
4. **복잡도**: 조건이 복잡하여 의도가 불명확함
5. **변경 빈도**: 조건이 자주 변경되어 여러 곳 수정 필요

## OUTPUT FORMAT

### 실행 절차

공통 골격(대상 파일 수집 → 후보 제시(계열별 승인 규칙) → 적용 → 테스트 → 커밋/되돌리기, 브랜치·PR이
필요한 조건)은 이 스킬 디렉터리 기준 `../../references/refactoring-procedure.md`가 정본이다.
아래는 이 기법에 고유한 부분만 규정한다.

#### 중복 조건문 후보 식별 (공통 절차 2단계)

대상 파일에서 다음 패턴을 찾는다:

- 동일한 조건식이 2곳 이상에서 반복
- 조건식이 같은 변수/메서드를 참조
- 조건 분기에서 서로 다른 메서드 호출
- 논리적으로 같은 비즈니스 규칙

#### 후보 제시 예시 (공통 절차 3단계)

후보를 보고하고 즉시 적용한다(Tidy 계열 — 정본 §3-A):

```
## 리팩토링 후보 1: Lift Up Conditional

**파일**: ProductService.java
**중복 조건**: product.isOnSale()

**반복 위치** (3곳):
1. calculatePrice() 메서드
2. formatLabel() 메서드
3. getBadgeColor() 메서드

**현재 코드**:
[조건이 반복되는 메서드들]

**제안 변경**:
1. 조건을 변수로 추출: boolean isOnSale = product.isOnSale()
2. createDisplay() 메서드 생성
3. 조건을 상위로 끌어올림 (surround with if-else)
4. 각 분기를 메서드로 추출
   - createSaleDisplay(product)
   - createNormalDisplay(product)
5. ProductDisplay 객체로 결과 통합

→ 승인 없이 적용 (Tidy 계열)
```



#### 조건문 끌어올리기 실행 (공통 절차 4단계)

확정된 리팩토링을 하나씩 수행:

1. 조건을 변수로 추출
2. 조건을 메서드로 추출 (복잡한 경우)
3. Surround with if-else로 조건 끌어올림
4. 각 분기를 메서드로 추출
5. 불필요한 중간 변수 제거 (inline)

**커밋 메시지 형식**:
```
refactor: lift up conditional [조건 설명] in [클래스명]
```

#### 결과 보고

사용자에게 보고:
- 적용된 조건문 끌어올리기 목록

## FAILURE CONDITIONS

공통 실패 조건(계열별 승인 규칙 위반, 테스트 실패 방치, 테스트 수정, 커밋 단위, `git add -A`, heredoc
한글 메시지)은 `../../references/refactoring-procedure.md`에 있다. 아래는 이 기법에 고유한 것만.

- 논리적으로 다른 조건을 동일하다고 판단 (조건식은 같아도 의미가 다를 수 있음)
- 조건 평가 순서 변경으로 부수효과 발생 (short-circuit 주의)
- 단순히 조건만 이동하고 메서드 추출 없음 (가독성 개선 부족)
