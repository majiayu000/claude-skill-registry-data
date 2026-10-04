---
name: intent-revealing-names
description: 하나의 긴 메서드를 grouping(Reorder/Chunk)·comment로 정돈해 책임을 드러낸 뒤 Arlo Belshee 6단계 네이밍(완전정직 이름 → Extract Method → Intent Revealing → Domain Abstraction)을 하나의 연속 흐름으로 관통하는 self-contained 워크플로우. "이 긴 메서드 이름이 하는 일을 안 드러낸다", "메서드 이름부터 정직하게 만들어서 쪼개줘", "이름 주도로 이 메서드 리팩토링" 요청 시 사용. 단, 여러 파일에 흩어진 개별 이름 스멜의 배치 교체는 /naming-process, 클래스 분리·도메인 이동 같은 대규모 구조 변경은 /system-wide-refactoring이 적합. /intent-revealing-names로 호출.
argument-hint: "[파일:메서드 | commit-ref]"
---

# Intent-Revealing Names — 이름 주도 관통 리팩토링

이름 없는 긴 메서드 하나를 대상으로, **grouping → comment → 정직한 이름 → extract → 의도 드러내는 이름 → 도메인 추상화**를 하나의 연속 흐름으로 관통한다.

> 이름을 신뢰한다면 어떨까요? 이름을 읽어도 메서드를 읽을 필요가 없는 세상을 상상해 보세요.
> — Arlo Belshee

## 핵심 명제

- **intent(의도) = why(왜)**. 좋은 이름은 코드가 *무엇을 하는가(what)*가 아니라 *왜 부르는가(why)*를 드러낸다.
- **이름은 리팩터링의 결과가 아니라 진단 수단이다.** 이름을 정직하게 만들려는 시도 자체가 구조적 문제(SRP 위반, 원시 집착)를 드러내고, 그 진단이 Extract Method·값 객체 도입으로 이어진다.
- **comment는 extract될 메서드 이름의 초안이다** (Kent Beck: "좋은 이름이 떠오르지 않으면 먼저 주석으로 의도를 표현하라 — Extract Method의 전 단계").
- **전환점은 3 → 5단계**: 3단계까지 "무엇을(what)"을 정직하게 누적하고, 5단계에서 "왜(why)"로 전환한다. 이 전환이 있어야 "이름만 읽으면 본문을 읽을 필요가 없는" 상태가 된다.

## GOAL

- **성공 = 대상 긴 메서드가 목차(table of contents)로 축약되고, 각 이름이 why를 드러내며, 모든 테스트가 통과하고, 되돌리기 쉬운 단위 커밋으로 남는다.**
- 상위 메서드의 이름이 what 나열이 아니라 why(호출 이유)를 드러냄
- 추출된 각 private helper가 하나의 식별 가능한 책임만 수행 (Composed Method)
- 남은 원시 집착(Primitive Obsession)이 식별되어 후속 스킬로 인계됨 (승격 자체는 이 스킬 밖)
- 동작 변경 없이 구조만 개선됨

## CONSTRAINTS

- **계열**: Tidy — 후보 보고 후 **승인 없이 적용** (`../../references/refactoring-procedure.md` §0·§3-A)
### Hard Rules (공유)

- **동작 변경 금지** — 구조·이름만 개선, 기능 변경 없음
- **테스트 수정 금지** — 변경이 테스트를 실패시키면 즉시 되돌리기
- **작은 단계 + 매 단계 테스트** — 한 번에 하나의 변형만 적용하고 green 확인
- **명시적 git add** — `git add -A` 금지, 변경 파일만 명시
- **사용자 확인** — 대상 메서드 확정과 5·6단계 진입은 사용자와 합의

### 이 스킬 고유 규칙

- **대상은 하나의 긴 메서드** — 파일 전체 검토가 아니라, 지정된(또는 가장 냄새나는) 긴 메서드 하나에 집중
- **rename을 마지막에 일괄 수행하지 않는다** — 이름 진화(3단계)가 extract(4단계)를 **유발**하고, extract 후 다시 rename(5단계)한다. 이 인터리빙이 이 스킬의 본질이다
- **Extract는 국소(local)에 한정** — 대상 메서드를 **같은 클래스 내 private helper**로 분할하는 것까지. 클래스 분리·도메인 이동 등 대규모 구조 변경은 `/system-wide-refactoring` 전담 (이 스킬은 self-contained 연속 흐름)
- **6단계는 가르치되 인계** — 운영상 이 스킬은 **5단계(Intent Revealing)까지 실행**하고, 6단계(Domain Abstraction)는 방향만 보여준 뒤 원시 집착을 지목해 값 객체·도메인 이동을 후속 스킬(`/discover-value-object` 등)로 **인계**한다. 승격을 이 스킬 흐름 안에서 실행하지 않는다

## 6단계 관통 프로세스 — "주문 처리" 예제

e-commerce "주문 처리" 예제로 6단계를 처음부터 끝까지 진행한다. 각 단계는 **목적 + 코드 상태 + 다음 단계로 넘어가게 만드는 트리거(냄새)** 로 구성된다.

### 출발점 — 이름 없는 긴 메서드

`OrderHelper.process(cart)`가 재고 확인 → 재고 차감 → 결제 → 확정 메일을 한 메서드에서 처리한다. `-Helper` 접미사와 `process`는 정보가 없으면서 정보가 있는 것처럼 보이는, 가장 위험한 종류의 이름이다.

```java
public class OrderHelper {
    public void process(Cart cart) {
        for (CartItem item : cart.getItems()) {
            int stock = stockDao.getStock(item.getProductId());
            if (stock < item.getQuantity()) throw new RuntimeException("out of stock");
        }
        for (CartItem item : cart.getItems())
            stockDao.decrease(item.getProductId(), item.getQuantity());
        BigDecimal total = BigDecimal.ZERO;
        for (CartItem item : cart.getItems())
            total = total.add(item.getPrice().multiply(BigDecimal.valueOf(item.getQuantity())));
        paymentGateway.charge(cart.getUserId(), total);
        emailSender.send(cart.getUserEmail(), "주문이 완료되었습니다");
    }
}
```

### 단계 A — 본문 정돈으로 책임 가시화 (grouping + comment)

> 사용자 요청 1·2번. 기법 정의는 `/tdd-tidy`(tdd-blue의 Local Tidying)에서 인용 — 여기서는 대상 메서드에 국소 적용한다.

**A-1. Reorder (Reading/Cohesion Order)**: 변수 선언을 사용 위치 가까이로(Reading Order), 관련 로직끼리 인접하게(Cohesion Order, Step Down Rule).
**A-2. Chunk**: 빈 줄로 논리 블록을 분리한다.
**A-3. Explaining Comment**: 각 블록에 "무엇을/왜"를 한 줄로 붙인다. **이 주석이 곧 추출될 메서드 이름의 초안**이다.

```java
public void process(Cart cart) {
    // 재고 확인 — 부족하면 주문 거절
    for (CartItem item : cart.getItems()) {
        int stock = stockDao.getStock(item.getProductId());
        if (stock < item.getQuantity()) throw new RuntimeException("out of stock");
    }

    // 재고 차감
    for (CartItem item : cart.getItems())
        stockDao.decrease(item.getProductId(), item.getQuantity());

    // 결제 — 합계 계산 후 청구
    BigDecimal total = BigDecimal.ZERO;
    for (CartItem item : cart.getItems())
        total = total.add(item.getPrice().multiply(BigDecimal.valueOf(item.getQuantity())));
    paymentGateway.charge(cart.getUserId(), total);

    // 확정 메일 발송
    emailSender.send(cart.getUserEmail(), "주문이 완료되었습니다");
}
```

**트리거**: 주석 붙은 책임 블록이 4개다 — 이 메서드가 여러 일을 한다는 사실이 이제 눈에 보인다.

### 단계 B — 상위 메서드 이름을 정직하게 진화 (6단계 1→2→3)

이름 축을 정직하게 단계적으로 바꿔, 이름 스스로가 SRP 위반을 드러내게 만든다.

**1. Obvious Nonsense**: `process()` → `applesauce()`. 그럴듯하지만 비어 있는 이름을, 일부러 명백히 틀린 이름으로 바꿔 "여기 이름이 필요하다"를 코드가 명시하게 한다. `-er`/`-Utils`/라이프사이클(`onCreate`) 이름을 제거하는 단계이기도 하다.

**2. Honest**: `applesauce()` → `probably_updateStockAndCharge_andStuff()`. 3부 규칙 — `probably_`(불확실) + 파악한 동작 + `_andStuff`(아직 못 파악). 완벽함이 아니라 **오해를 주지 않는 것**이 목표.

**3. Completely Honest**: `checkStockAndDeductStockAndChargePaymentAndSendConfirmationEmail()`. 단계 A의 comment들을 그대로 이어 붙인 이름. `probably_`·`_andStuff`를 모두 제거하고 하는 일 **전부**(what)를 담는다. 길고 어색해도 상관없다.

**트리거**: 이름에 `And`가 네 번 등장한다 — 책임이 네 개, 즉 **SRP 위반을 이름이 드러낸다**. 이것이 다음 단계(extract)의 근거다.

> **팀 합의 노트**: `applesauce`·`probably_..._andStuff` 같은 중간 이름을 실제 커밋할지는 팀 합의 사항이다. "아직 이해하지 못했다"를 정직하게 남기는 편이 그럴듯한 거짓 이름보다 낫다는 입장(Emily Bache 데모)이 있으나, 개인 작업이면 3단계에서 한 번에 커밋해도 된다.

### 단계 C — 드러난 책임대로 Extract (6단계 4: Does the Right Thing, composed method)

완전정직 이름의 각 `And` 조각 = 단계 A의 각 comment 블록. 그 블록들을 **comment를 이름으로 승격**하여 private helper로 추출한다. 상위 메서드는 4줄짜리 목차가 된다. (Arlo Belshee 정본 4단계 "Does the Right Thing"을 여기서 Extract로 흡수한다 — 각 조각이 비로소 제 일만 하게 되므로.)

```java
public void checkStockAndDeductStockAndChargePaymentAndSendConfirmationEmail(Cart cart) {
    ensureStockAvailable(cart);
    deductStock(cart);
    chargePayment(cart);
    sendConfirmationEmail(cart);
}

private void ensureStockAvailable(Cart cart) { /* 재고 확인 블록 */ }
private void deductStock(Cart cart) { /* 재고 차감 블록 */ }
private void chargePayment(Cart cart) { /* 결제 블록 */ }
private void sendConfirmationEmail(Cart cart) { /* 확정 메일 블록 */ }
```

지역 변수가 상호 의존해 추출이 불가능하면 먼저 `/replace-temp-with-query`·`/extract-method-object`를 적용한다(이름으로 인용).

**트리거**: 구조는 정직해졌지만 상위 이름은 여전히 "무엇을 하는지"의 나열이다. "왜 이 메서드를 부르는지"는 아직 드러나지 않는다.

### 단계 D — 의도를 드러내기 (6단계 5) ★핵심 전환점

호출하는 쪽(예: `CheckoutController`의 "주문하기" 버튼 처리)을 살펴보면, 이 메서드의 진짜 목적은 "고객이 주문을 낸다"임을 알 수 있다. what이 아니라 why로 이름을 바꾼다.

```java
// 호출부: checkStockAndDeductStockAndChargePaymentAndSendConfirmationEmail(cart);
//      ↓
//         placeOrder(cart);

public class OrderService {          // OrderHelper → OrderService
    public void placeOrder(Cart cart) {
        ensureStockAvailable(cart);
        deductStock(cart);
        chargePayment(cart);
        sendConfirmationEmail(cart);
    }
}
```

이것이 "**intent = why**"의 실체다. 이름은 더 짧아지고, 호출 코드를 읽을 때 자연스럽게 이해된다.

**트리거**: 이름은 좋아졌지만 내부에 `String productId`, `int quantity`, `BigDecimal total` 같은 원시 타입이 분산되어 있다 — 원시 집착(Primitive Obsession).

### 단계 E — 도메인 추상화 (6단계 6)

> 여기서부터는 무거운 구조 변경이라 **이 스킬의 범위를 벗어난다** — 이 스킬은 5단계까지 실행하고 6단계는 인계한다. 값 객체·First Class Collection·Functional Core 분리는 각각 `/discover-value-object`, `/introduce-parameter-object`, `/first-class-collection`, `/segregate-functional-core`로 인계한다.
>
> **아래 코드는 후속 스킬들로 도달하는 목표 end-state(aspirational)이며, 이 스킬에서 전부 실행하지 않는다.** 이 스킬의 역할은 5단계까지 완성한 뒤 원시 집착을 _가리키고_, 실제 승격은 인용된 후속 스킬로 넘기는 것이다 (클래스 분리·도메인 이동은 이 스킬 범위 밖 — FAILURE CONDITIONS 참조).

```java
public Order placeOrder(Cart cart) {
    Order order = cart.toOrder();          // Order 애그리거트
    inventory.reserve(order.lines());      // 재고 확인+차감 → Inventory 도메인
    payment.charge(order.total());         // total() → Money 값 객체
    notifier.notifyOrderPlaced(order);
    return order;
}
```

| 이전 (원시 집착) | 이후 (도메인 개념) |
| --- | --- |
| `String productId` + `int quantity` 반복 | `OrderLine` 값 객체 |
| `BigDecimal total` 산재 | `Money` 값 객체 (`order.total()`) |
| `stockDao.getStock()`/`decrease()` 절차 호출 | `Inventory.reserve(lines)` |
| `Cart`를 절차적으로 순회·변환 | `Order` 애그리거트 (`cart.toOrder()`) |

이제 `placeOrder`의 본문은 하나의 유비쿼터스 언어 안에서 비즈니스 규칙을 읽는 산문이 된다.

### 6단계 요약

| 단계 | 이 스킬의 활동 | 초점 | 예제 이름 |
| --- | --- | --- | --- |
| A. Tidy-prep (6단계 이전 준비) | Reorder + Chunk + Comment | 책임 가시화 | `// 재고 확인` 등 4개 블록 |
| B1. Obvious Nonsense | 나쁜 이름 제거 | — | `applesauce()` |
| B2. Honest | 파악한 사실만 정직하게 | what(부분) | `probably_updateStockAndCharge_andStuff()` |
| B3. Completely Honest | 하는 일 전부 | what(전부) | `checkStock...AndSendConfirmationEmail()` |
| C. Extract | SRP 위반대로 분리 | Composed Method | `ensureStockAvailable()` + 3개 |
| D. Intent Revealing ★ | 무엇이 아니라 **왜** | why | `placeOrder(cart)` |
| E. Domain Abstraction (범위 밖 — 인계) | 원시 집착 → 도메인 언어 | 도메인 | 후속 스킬로 인계 (`Order`, `Money`, `Inventory`) |

## 다른 스킬과의 경계

이 스킬은 self-contained하지만, 각 기법의 **정의는 재기술하지 않고 이름으로 인용**한다.

- **grouping/comment 기법 상세** → `/tdd-tidy`(tdd-blue): Reorder, Chunk, Explaining Comment, Normalize Symmetries, Split Loop 등
- **대규모 Extract / 클래스 분리 / 도메인 이동** → `/system-wide-refactoring`. 이 스킬은 국소 private helper 추출까지만
- **개별 이름 rename 카탈로그(Naming Smells 탐지)** → `/naming-process`. 이 스킬은 "하나의 메서드를 6단계로 관통"이 목적 (개별 이름 스캔이 아님)
- **값 객체/컬렉션/함수형 코어 승격 상세** → `/discover-value-object`, `/introduce-parameter-object`, `/first-class-collection`, `/segregate-functional-core`

## OUTPUT FORMAT

### 실행 절차

#### 1. 대상 메서드 확정

- 인자로 `파일:메서드`가 오면 그 메서드를, `commit-ref`가 오면 그 diff의 Java 파일에서 가장 긴/냄새나는 메서드를 후보로 제시
- 인자가 없으면 `git diff --name-only -- '*.java'`(+`--cached`)의 변경 파일에서 20줄 이상 메서드를 찾아 후보 제시
- 테스트 파일(`*Test.java` 등)은 제외
- 후보를 보여주고 **대상 하나를 사용자와 확정**

```
관통 리팩토링 대상 후보:
- OrderHelper.process(Cart) — 15줄, 책임 4개 추정 (재고확인/차감/결제/메일)
이 메서드로 진행할까요?
```

#### 2. 단계 A~E를 순서대로, 작은 단계로 적용

- **A**: Reorder → Chunk → Comment (책임 블록 가시화)
- **B**: 상위 메서드 이름을 1→2→3단계로 진화 (완전정직까지)
- **C**: comment 블록을 이름으로 승격해 private helper 추출 (IDE Extract Method)
- **D**: 호출부를 근거로 상위 메서드를 intent-revealing rename (IDE Rename — 참조 자동 갱신). 클래스명 `-Helper`/`-er`도 이때 함께
- **E**: (실행 안 함 — 인계) 5단계 완성 후 남은 원시 집착을 지목하고, 값 객체·도메인 이동을 후속 스킬(`/discover-value-object` 등)로 제안한다. 승격은 이 스킬에서 수행하지 않는다

**각 단계마다**: 변경 → 테스트 실행(`./gradlew test` 또는 `mvn test`) → green이면 진행, red면 즉시 되돌리기.

#### 3. 커밋 — 되돌리기 쉬운 단위로

의미 단위로 나눠 커밋하는 것을 권장한다 (각 단계가 독립적으로 되돌려짐):

- `refactor: tidy-prep OrderHelper.process — group & comment responsibilities` (단계 A)
- `refactor: extract composed methods from OrderHelper.process` (단계 C, B의 이름 진화 포함)
- `refactor: reveal intent — process → placeOrder` (단계 D)

(단계 E의 도메인 승격은 이 스킬에서 커밋하지 않는다 — 후속 스킬로 인계.)

- 커밋 메시지는 `docs/reviewable-commits.md`(없으면 `${CLAUDE_PLUGIN_ROOT}/references/reviewable-commits.md`) 표준을 따른다. subject는 `refactor:` 접두사, body에 Why(이름이 무엇을 드러냈고 왜 이렇게 분리/명명했는지)를 담는다. 형식은 그 표준이 유일한 출처이므로 여기서 재기술하지 않는다. 길이는 `../../references/commit-style.md`의 간결성 규칙(제목 + 핵심 bullet 2~4줄)을 따른다.
- 한글 메시지는 임시 파일 + `git commit -F` (`-m "한글"` 금지 — 깨짐).
- 최소 요건이 급하면 전체를 단일 `refactor:` 커밋으로 마무리해도 되나, 단계별 분리가 리뷰·롤백에 유리하다.

#### 4. 완료 보고

- 이름 진화 경로 요약 (`process` → `applesauce` → … → `placeOrder`)
- 추출된 helper 목록과 각 책임
- 테스트 결과
- 남은 원시 집착과 인계할 후속 스킬 제안 (`/discover-value-object` 등)

## FAILURE CONDITIONS

이 중 하나라도 발생하면 작업 실패로 간주:

- [ ] 리팩토링 후 테스트가 실패함
- [ ] rename을 맨 마지막에 일괄 수행함 (3단계 완전정직 이름이 extract를 유발하는 인터리빙을 건너뜀)
- [ ] 3단계(Completely Honest)를 건너뛰고 곧장 intent-revealing 이름으로 건너뜀 (SRP 위반 진단 과정 생략)
- [ ] 별도 브랜치를 만들거나 PR을 생성함 (self-contained 위반 — 대규모는 `/system-wide-refactoring`)
- [ ] 클래스 분리·도메인 이동 같은 대규모 구조 변경을 이 스킬에서 수행 (경계 침범)
- [ ] 단계 E(도메인 승격)를 후속 스킬로 인계하지 않고 이 스킬 흐름 안에서 직접 실행 (5단계까지만 실행이 원칙)
- [ ] `git add -A` 사용 / 동작 변경 발생 / 사용자 확인 없이 5단계(Intent Revealing) 진입

## 더 읽을거리 (비-load-bearing)

이 스킬은 아래 vault 문서를 소스로 작성되었다. **런타임 의존성이 아니며**, 없어도 스킬은 완전하게 동작한다.

- vault: `Intent Revealing Names.md` — Arlo Belshee 6단계 프로세스를 "주문 처리" 예제로 관통한 원 노트
- Emily Bache, *Trustworthy Code with Naming as a Process* — Arlo Belshee 기법 라이브 데모
- Robert C. Martin, *Clean Code* Ch.4 Meaningful Names — Intention-Revealing Names 원개념
