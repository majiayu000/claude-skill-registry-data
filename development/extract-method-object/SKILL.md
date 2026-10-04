---
name: extract-method-object
description: 지역 변수가 서로 얽혀 Extract Method가 불가능한 거대 메서드를 별도 클래스(Method Object)로 추출. "긴 메서드를 클래스로", "지역 변수 때문에 추출 불가", "method object", "/extract-method-object" 요청 시 사용. 단, 지역 변수 얽힘 없이 잘라낼 수 있는 긴 메서드는 /intent-revealing-names(grouping→extract)가 적합. /extract-method-object [commit-ref]로 호출.
argument-hint: "[commit-ref]"
---

# Extract Method Object Skill

지역 변수가 상호 의존해 Extract Method가 어려운 거대 메서드를 별도 클래스로 추출.

## GOAL

- **성공 = 지역 변수가 상호 의존하는 긴 메서드가 Method Object로 추출되어 커밋 완료됨**
- 50줄 이상의 복잡한 메서드가 식별됨
- 지역 변수가 메서드 전역에 걸쳐 상호 의존해 Extract Method 불가
- 후보 보고 후 Method Object 패턴 적용 (Tidy 계열 — 승인 없이)
- 모든 테스트 통과

## CONSTRAINTS

- **계열**: Tidy — 후보 보고 후 **승인 없이 적용** (`../../references/refactoring-procedure.md` §0·§3-A)
### Hard Rules
- **동작 변경 금지** — 구조 개선만 수행
- **테스트 수정 금지** — 구조 변경이 테스트를 실패시키면 되돌리기
- **커밋 단위** — 1파일 x 1기법 = 1커밋 (논리적으로 연결된 파일은 함께)
- **git add -A 금지** — 변경된 파일만 명시적으로 추가

## 적용 패턴

Extract Method Object 리팩토링 단계:

1. **메서드를 클래스로 변환**
   - 새 클래스 생성 (메서드명 + "er" 또는 명사형)
   - 원본 메서드를 invoke() 또는 execute() 메서드로 이동

2. **지역 변수를 필드로 변환**
   - 메서드 내 지역 변수들을 클래스 필드로 변환
   - 읽기 전용 변수는 final 필드로

3. **외부 의존성을 생성자 파라미터로 전달**
   - 원본 클래스의 필드 참조를 생성자 파라미터로
   - 필요한 최소한의 의존성만 전달

4. **작은 메서드로 분해**
   - 큰 invoke() 메서드를 의미 있는 작은 private 메서드들로 분해
   - 각 메서드는 단일 책임 수행

### Before/After 예시

```java
// Before: 지역 변수가 상호 의존하는 거대 메서드 (50+ lines)
public class RefundService {
    public List<RefundDiff> refundDiff() {
        // 지역 변수 선언
        Map<String, Cost> costMap = new HashMap<>();
        Map<String, AcmeCost> acmeCostMap = new HashMap<>();
        List<RefundDiff> differences = new ArrayList<>();
        
        // 복잡한 로직이 50줄 이상...
        for (Cost cost : costs) {
            costMap.put(cost.getItemId(), cost);
        }
        
        for (AcmeCost acmeCost : acmeCosts) {
            acmeCostMap.put(acmeCost.getItemId(), acmeCost);
        }
        
        for (OrderItem item : orderItems) {
            Cost cost = costMap.get(item.getItemId());
            AcmeCost acmeCost = acmeCostMap.get(item.getItemId());
            
            if (cost != null && acmeCost != null) {
                double diff = cost.getAmount() - acmeCost.getAmount();
                if (Math.abs(diff) > 0.01) {
                    differences.add(new RefundDiff(item, diff));
                }
            }
        }
        
        return differences;
    }
}

// After: Method Object로 추출
public class RefundService {
    public List<RefundDiff> refundDiff() {
        return new RefundDifferenceCalculator(costs, acmeCosts).invoke(orderItems);
    }
}

class RefundDifferenceCalculator {
    private final List<Cost> costs;
    private final List<AcmeCost> acmeCosts;
    private Map<String, Cost> costMap;
    private Map<String, AcmeCost> acmeCostMap;
    private List<RefundDiff> differences;
    
    RefundDifferenceCalculator(List<Cost> costs, List<AcmeCost> acmeCosts) {
        this.costs = costs;
        this.acmeCosts = acmeCosts;
    }
    
    List<RefundDiff> invoke(List<OrderItem> orderItems) {
        buildCostMaps();
        calculateDifferences(orderItems);
        return differences;
    }
    
    private void buildCostMaps() {
        costMap = costs.stream()
            .collect(Collectors.toMap(Cost::getItemId, c -> c));
        acmeCostMap = acmeCosts.stream()
            .collect(Collectors.toMap(AcmeCost::getItemId, c -> c));
    }
    
    private void calculateDifferences(List<OrderItem> orderItems) {
        differences = new ArrayList<>();
        for (OrderItem item : orderItems) {
            findAndAddDifference(item);
        }
    }
    
    private void findAndAddDifference(OrderItem item) {
        Cost cost = costMap.get(item.getItemId());
        AcmeCost acmeCost = acmeCostMap.get(item.getItemId());
        
        if (cost != null && acmeCost != null) {
            addDifferenceIfSignificant(item, cost, acmeCost);
        }
    }
    
    private void addDifferenceIfSignificant(OrderItem item, Cost cost, AcmeCost acmeCost) {
        double diff = cost.getAmount() - acmeCost.getAmount();
        if (Math.abs(diff) > 0.01) {
            differences.add(new RefundDiff(item, diff));
        }
    }
}
```

## 적용 기준

Extract Method Object를 적용해야 하는 경우:

1. **메서드 길이**: 50줄 이상의 긴 메서드
2. **지역 변수 상호 의존(entanglement)**: 여러 지역 변수가 메서드 전체에 걸쳐 상호작용
3. **Extract Method 불가**: 파라미터가 너무 많아져 Extract Method로 분해 불가
4. **임시 변수 과다**: 중간 결과를 저장하는 임시 변수가 많음
5. **단계적 계산**: 여러 단계의 계산이 순차적으로 진행됨

### 신규 기능 추가 경로 — 계획된 목표 구조로서의 Method Object

Method Object는 레거시 개선용만이 아니다. **새 기능을 추가할 때 처음부터 목표 구조로 계획**하면
다음 3단계 경로가 효과적이다:

1. **검증 조건을 테스트로 먼저 확정** — 정확한 기대값을 가진 인수 테스트를 구현 전에 작성한다.
2. **새 클래스 하나에 절차적으로 구현** — WELC(Working Effectively with Legacy Code)의 Sprout Class처럼 정적 메서드 하나를 진입점으로
   노출해 기존 호출부 변경을 한 줄로 최소화한다. 이 단계는 절차적으로 구현한다 (make it work).
3. **절차를 Method Object로 변환** — 상태가 없는 순수 계산이라도, 메서드 간 인자 전달을
   최소화하기 위해 입력을 final 필드로 받는 객체로 전환한다. 정적 진입점은 유지한다:

```java
// public API는 처음부터 끝까지 정적 메서드 하나 — 내부가 절차→객체로 바뀌어도 호출부 불변
public static BigDecimal calculate(final Line[] lines) {
    return new TaxCalculator(List.of(lines)).total();
}
```

이 경로에서는 내부 구조 변화(절차 → 객체, 메서드 분해, 인자 제거)가 호출부에 전혀 전파되지 않아,
각 단계를 독립적인 작은 `refactor:` 커밋으로 안전하게 진행할 수 있다.

### 추출 후 데이터 결정 — 무엇을 필드로, 무엇을 파라미터로

Method Object 내부의 데이터는 세 종류로 나뉘고, 종류마다 답이 다르다:

| 데이터 종류 | 예 | 판정 |
|---|---|---|
| **입력** (생성자로 받는 본질적 상태) | 주문 라인 목록 | **final 필드** — 전체를 순회·합산하는 메서드들의 인자가 사라진다 |
| **파생값** (계산 도중의 중간 결과) | 과세표준, 세액 | **파라미터 유지**(데이터 흐름이 시그니처에 명시) 또는 **no-arg 질의로 전환**(replace-temp-with-query). 가변 필드에 저장하는 방식은 호출 순서 결합(temporal coupling)을 만들므로 피한다 |
| **loop 변수** (반복마다 다른 값) | 개별 라인 | **파라미터 필수** — 호출마다 값이 달라 필드화 불가능 |

**explicit-parameters 스킬과의 경계**: explicit-parameters는 협력 객체 의존성(Singleton·전역
상태·서비스)을 파라미터로 드러내는 기법이다. Method Object의 입력·계산 상태 필드는 그 스킬의
대상이 아니다 — 방향이 반대인 두 스킬은 적용 대상이 달라 충돌하지 않는다.

## OUTPUT FORMAT

### 실행 절차

공통 골격(대상 파일 수집 → 후보 제시(계열별 승인 규칙) → 적용 → 테스트 → 커밋/되돌리기, 브랜치·PR이
필요한 조건)은 이 스킬 디렉터리 기준 `../../references/refactoring-procedure.md`가 정본이다.
아래는 이 기법에 고유한 부분만 규정한다.

#### Method Object 후보 식별 (공통 절차 2단계)

대상 파일에서 다음 패턴을 찾는다:

- 50줄 이상의 긴 메서드
- 5개 이상의 지역 변수 선언
- 지역 변수가 메서드 전체에 걸쳐 읽기/쓰기됨
- Extract Method 시 파라미터가 4개 이상 필요
- 여러 단계의 계산이 순차적으로 진행

#### 후보 제시 예시 (공통 절차 3단계)

후보를 보고하고 즉시 적용한다(Tidy 계열 — 정본 §3-A):

```
## 리팩토링 후보 1: Extract Method Object

**파일**: RefundService.java
**대상**: refundDiff() 메서드 (68줄)

**현재 코드**:
[해당 메서드 전체]

**지역 변수 분석**:
- costMap, acmeCostMap, differences (메서드 전체에서 사용)
- 5개 이상의 지역 변수가 상호 의존함
- Extract Method 불가 (파라미터 6개 필요)

**제안 변경**:
1. RefundDifferenceCalculator 클래스 생성
2. 지역 변수를 필드로 변환
3. costs, acmeCosts를 생성자 파라미터로
4. invoke(orderItems) 메서드로 계산 수행
5. buildCostMaps(), calculateDifferences() 등으로 분해

→ 승인 없이 적용 (Tidy 계열)
```



#### Method Object 추출 실행 (공통 절차 4단계)

확정된 리팩토링을 하나씩 수행:

1. Method Object 클래스 생성 및 메서드 이동
2. 지역 변수를 필드로 변환
3. 외부 의존성을 생성자 파라미터로
4. 작은 메서드로 분해

**커밋 메시지 형식**:
```
refactor: extract method object [클래스명] from [원본클래스명].[메서드명]
```

#### 결과 보고

사용자에게 보고:
- 적용된 Method Object 목록

## FAILURE CONDITIONS

공통 실패 조건(계열별 승인 규칙 위반, 테스트 실패 방치, 테스트 수정, 커밋 단위, `git add -A`, heredoc
한글 메시지)은 `../../references/refactoring-procedure.md`에 있다. 아래는 이 기법에 고유한 것만.

- 지역 변수가 적은 (3개 이하) 단순 메서드에 적용 (Extract Method로 충분)
- Method Object 생성 후 작은 메서드로 분해하지 않음 (단순히 코드만 옮김)
- 필요 이상의 의존성을 생성자로 전달 (원본 클래스 전체 전달 등)
