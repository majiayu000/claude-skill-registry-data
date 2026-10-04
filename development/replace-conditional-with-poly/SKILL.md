---
name: replace-conditional-with-poly
description: 타입·상태별로 반복되는 switch/if-else 분기를 다형성(인터페이스 + 구현 클래스)으로 치환. "switch를 다형성으로", "타입 분기를 클래스로", "strategy 패턴", "/replace-conditional-with-poly" 요청 시 사용. 단, null 분기만이면 /introduce-special-case, 조건식 가독성만이면 /decompose-conditional이 적합. /replace-conditional-with-poly [commit-ref]로 호출.
argument-hint: "[commit-ref]"
---

# Replace Conditional with Polymorphism Skill

반복되는 switch/if-else 조건문을 다형성으로 치환하여 Open-Closed Principle 적용.

## GOAL

- **성공 = 반복 조건문이 다형성으로 치환되어 커밋 완료됨**
- 동일한 switch/if-else가 2곳 이상에서 반복됨
- Type Code 기반 분기가 식별됨
- 사용자 확인 후 다형성 패턴 적용
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

Replace Conditional with Polymorphism 리팩토링 경로:

1. **Replace Type Code with Subclasses**
   - Type code (String, enum 등)를 서브클래스로 변환
   - 각 타입별 서브클래스 생성

2. **Replace Constructor with Factory**
   - 직접 생성자 호출을 Factory Method로 치환
   - Type code에 따라 적절한 서브클래스 반환

3. **Replace Conditional with Polymorphism**
   - switch/if-else를 추상 메서드로 치환
   - 각 서브클래스에서 구체적 구현

### Before/After 예시

```java
// Before: 반복되는 조건문 (2곳 이상)
public class Performance {
    private Play play;
    private int audience;
    
    public int amount() {
        switch (play.type) {
            case "tragedy":
                int result = 40000;
                if (audience > 30) {
                    result += 1000 * (audience - 30);
                }
                return result;
            case "comedy":
                int result = 30000;
                if (audience > 20) {
                    result += 10000 + 500 * (audience - 20);
                }
                result += 300 * audience;
                return result;
            default:
                throw new IllegalArgumentException("unknown type: " + play.type);
        }
    }
    
    public int volumeCredits() {
        int result = Math.max(audience - 30, 0);
        // 동일한 조건문 반복
        if ("comedy".equals(play.type)) {
            result += Math.floor(audience / 5);
        }
        return result;
    }
}

// After: 다형성으로 치환
abstract class PerformanceCalculator {
    protected Play play;
    protected int audience;
    
    static PerformanceCalculator create(Play play, int audience) {
        switch (play.type) {
            case "tragedy": return new TragedyCalculator(play, audience);
            case "comedy": return new ComedyCalculator(play, audience);
            default: throw new IllegalArgumentException("unknown type: " + play.type);
        }
    }
    
    PerformanceCalculator(Play play, int audience) {
        this.play = play;
        this.audience = audience;
    }
    
    abstract int amount();
    
    int volumeCredits() {
        return Math.max(audience - 30, 0);
    }
}

class TragedyCalculator extends PerformanceCalculator {
    TragedyCalculator(Play play, int audience) {
        super(play, audience);
    }
    
    @Override
    int amount() {
        int result = 40000;
        if (audience > 30) {
            result += 1000 * (audience - 30);
        }
        return result;
    }
}

class ComedyCalculator extends PerformanceCalculator {
    ComedyCalculator(Play play, int audience) {
        super(play, audience);
    }
    
    @Override
    int amount() {
        int result = 30000;
        if (audience > 20) {
            result += 10000 + 500 * (audience - 20);
        }
        result += 300 * audience;
        return result;
    }
    
    @Override
    int volumeCredits() {
        return super.volumeCredits() + (int) Math.floor(audience / 5);
    }
}

// 사용
public class Performance {
    private PerformanceCalculator calculator;
    
    public Performance(Play play, int audience) {
        this.calculator = PerformanceCalculator.create(play, audience);
    }
    
    public int amount() {
        return calculator.amount();
    }
    
    public int volumeCredits() {
        return calculator.volumeCredits();
    }
}
```

## 적용 기준

Replace Conditional with Polymorphism을 적용해야 하는 경우:

1. **조건문 반복**: 동일한 switch/if-else가 2곳 이상에서 반복
2. **Type Code 기반**: String, enum 등의 타입 코드로 분기
3. **새 타입 추가 빈번**: 새로운 케이스가 자주 추가됨
4. **분산된 로직**: 타입별 로직이 여러 메서드에 분산
5. **OCP 위반**: 새 타입 추가 시 기존 코드 수정 필요

## OUTPUT FORMAT

### 실행 절차

공통 골격(대상 파일 수집 → 후보 제시(계열별 승인 규칙) → 적용 → 테스트 → 커밋/되돌리기, 브랜치·PR이
필요한 조건)은 이 스킬 디렉터리 기준 `../../references/refactoring-procedure.md`가 정본이다.
아래는 이 기법에 고유한 부분만 규정한다.

#### 반복 조건문 후보 식별 (공통 절차 2단계)

대상 파일에서 다음 패턴을 찾는다:

- 동일한 조건 변수로 분기하는 switch/if-else가 2곳 이상
- Type code (String, enum)로 분기
- 3개 이상의 case/branch
- 각 branch가 5줄 이상의 로직 포함

#### 후보 제시 예시 (공통 절차 3단계)

후보를 하나씩 제시하고 사용자 확인:

```
## 리팩토링 후보 1: Replace Conditional with Polymorphism

**파일**: Performance.java
**대상**: play.type 기반 조건문 (2곳에서 반복)

**반복 위치**:
1. amount() 메서드 (라인 15-30)
2. volumeCredits() 메서드 (라인 35-40)

**현재 코드**:
[조건문이 반복되는 코드 블록]

**제안 변경**:
1. PerformanceCalculator 추상 클래스 생성
2. TragedyCalculator, ComedyCalculator 서브클래스 생성
3. Factory Method로 적절한 서브클래스 생성
4. switch 문을 추상 메서드 호출로 치환
5. 각 서브클래스에서 타입별 로직 구현

**적용할까요?** (yes / no / 수정 요청)
```

- 사용자가 **yes** → 실행 목록에 추가
- 사용자가 **no** → 스킵
- 사용자가 **수정 요청** → 요청 반영 후 재제시

모든 후보 확인 후 최종 실행 목록을 보여주고 진행 여부 확인.

#### 다형성 치환 실행 (공통 절차 4단계)

확정된 리팩토링을 하나씩 수행:

1. 추상 클래스 생성 및 공통 로직 이동
2. Type code별 서브클래스 생성
3. Factory Method 추가
4. 조건문을 추상 메서드 호출로 치환
5. 각 서브클래스에서 구체적 구현

**커밋 메시지 형식**:
```
refactor: replace conditional with polymorphism in [클래스명]
```

#### 결과 보고

사용자에게 보고:
- 적용된 다형성 치환 목록

## FAILURE CONDITIONS

공통 실패 조건(계열별 승인 규칙 위반, 테스트 실패 방치, 테스트 수정, 커밋 단위, `git add -A`, heredoc
한글 메시지)은 `../../references/refactoring-procedure.md`에 있다. 아래는 이 기법에 고유한 것만.

- 1곳에만 있는 단순 조건문에 적용 (불필요한 복잡도 증가)
- Factory Method 없이 직접 서브클래스 생성자 노출
- 모든 조건문을 다형성으로 치환 (간단한 조건문은 유지하는 것이 나음)
