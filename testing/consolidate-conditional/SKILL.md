---
name: consolidate-conditional
description: 동일한 결과를 내는 여러 조건문(OR 나열·중첩 AND)을 하나로 통합하고 의미 있는 boolean 메서드로 추출. "조건문 합쳐", "같은 결과 반환하는 if 정리", "중첩 if 평탄화", "/consolidate-conditional" 요청 시 사용. 단, 여러 메서드에 흩어진 동일 조건을 호출자 쪽으로 올리는 것은 /lift-up-conditional, 복잡한 조건식·분기를 메서드로 쪼개는 것은 /decompose-conditional이 적합. /consolidate-conditional [commit-ref]로 호출.
argument-hint: "[commit-ref]"
---

# Consolidate Conditional Expression

## GOAL

동일한 결과를 내는 여러 조건문을 하나로 통합하여:
- 흩어진 조건들의 관계를 명확히 표현
- 통합된 조건을 의미 있는 메서드로 추출
- 코드 의도 파악 용이

decompose-conditional과 상호 보완:
- **Consolidate**: 흩어진 조건을 **통합하는** 방향 (여러 if → 하나의 if)
- **Decompose**: 복잡한 조건을 **분해하는** 방향 (하나의 복잡한 if → 여러 메서드)
- 실전: Consolidate → Decompose 순서로 적용하는 경우가 많음

## CONSTRAINTS

- **계열**: Tidy — 후보 보고 후 **승인 없이 적용** (`../../references/refactoring-procedure.md` §0·§3-A)
- **동작 변경 금지**: 구조 개선만 수행 (기능 변경 없음)
- **테스트 수정 금지**: 구조 변경이 테스트를 실패시키면 되돌리기
- **명시적 git add**: `git add -A` 금지, 변경된 파일만 명시
- **Extract Method 포함**: 단일 클래스 내 완결 시에만 적용

## 적용 패턴

### Before: OR 패턴 — 동일 결과를 내는 조건들이 분산
```java
if (employee.getSeniority() < 2) return 0;
if (employee.getMonthsDisabled() > 12) return 0;
if (employee.isPartTime()) return 0;
```

### After: 조건 통합 + 메서드 추출
```java
if (isNotEligibleForDisability(employee)) return 0;

private boolean isNotEligibleForDisability(Employee employee) {
    return employee.getSeniority() < 2
        || employee.getMonthsDisabled() > 12
        || employee.isPartTime();
}
```

### 추가 예시: AND 패턴 — 중첩 조건 통합
```java
// Before
if (employee.onVacation()) {
    if (employee.getSeniority() > 10) {
        return 1;
    }
}

// After
if (employee.onVacation() && employee.getSeniority() > 10) {
    return 1;
}
```

### 추가 예시: 삼항 연산자 통합
```java
// Before
if (isSpecialDeal()) {
    total = price * 0.95;
} else {
    total = price * 0.98;
}
if (isLoyalCustomer()) {
    total = price * 0.95;
}

// After (동일 결과를 내는 조건 통합)
if (isSpecialDeal() || isLoyalCustomer()) {
    total = price * 0.95;
} else {
    total = price * 0.98;
}
```

## 적용 기준

### 적용 대상
- 2개 이상의 조건문이 동일한 결과(return/throw/assign)를 냄
- 조건들이 논리적으로 OR 또는 AND로 결합 가능
- 각 조건이 독립적 (부수효과 없음)
- 통합 후 의미 있는 이름을 부여할 수 있음

### 적용 제외
- **다른 결과**: 조건들이 서로 다른 결과를 냄
- **부수효과 사이**: 조건 사이에 부수효과 코드가 있음
- **의도적 분리**: 각 조건이 서로 다른 비즈니스 규칙을 표현 (분리가 의도적)
- **단일 조건**: 통합할 조건이 1개뿐

## OUTPUT FORMAT

### 실행 절차

공통 골격(대상 파일 수집 → 후보 제시(계열별 승인 규칙) → 적용 → 테스트 → 커밋/되돌리기, 브랜치·PR이
필요한 조건)은 이 스킬 디렉터리 기준 `../../references/refactoring-procedure.md`가 정본이다.
아래는 이 기법에 고유한 부분만 규정한다.

#### 후보 식별 (공통 절차 2단계)

- 동일 결과(return/throw/assign)를 내는 연속 조건문 탐지
- 동일 결과를 내는 중첩 조건문 탐지 (AND 패턴)
- 각 후보에 대해:
  - 파일명 및 라인 번호
  - Before/After 코드 미리보기
  - 통합 유형 (OR / AND)

#### 후보 제시 예시 (공통 절차 3단계)

```
발견된 후보 2개:

1. DisabilityService.java:15-17
   OR 패턴: 3개 조건 → 동일 return 0
   → isNotEligibleForDisability() 메서드 추출

2. VacationPolicy.java:30-34
   AND 패턴: 중첩 if 2단계
   → 단일 조건으로 플래트닝

→ 승인 없이 적용 (Tidy 계열)
```

#### 리팩토링 적용 (공통 절차 4단계)

- 조건문을 OR 또는 AND로 통합
- 통합된 조건을 boolean 반환 메서드로 추출
- (선택) 통합 후 복잡하면 decompose-conditional 제안

커밋 메시지: `refactor: consolidate conditional in <클래스명>` (공통 절차 6단계)

### 출력 예시
```
완료: Consolidate Conditional Expression

변경 내용:
- DisabilityService.java:15-17
  OR 통합: 3개 조건 → isNotEligibleForDisability() 메서드 추출

- VacationPolicy.java:30-34
  AND 통합: 중첩 if → 단일 조건으로 플래트닝

테스트: 모든 테스트 통과 (23 tests)
커밋: refactor: consolidate conditional in DisabilityService, VacationPolicy

제안: DisabilityService.java의 통합된 조건이 복잡합니다.
   /decompose-conditional 적용을 고려해보세요.
```

## FAILURE CONDITIONS

공통 실패 조건(계열별 승인 규칙 위반, 테스트 실패 방치, 테스트 수정, 커밋 단위, `git add -A`, heredoc
한글 메시지)은 `../../references/refactoring-procedure.md`에 있다. 아래는 이 기법에 고유한 것만.

- [ ] 다른 결과를 내는 조건들을 통합함
- [ ] 부수효과가 있는 조건 사이의 코드를 무시함
