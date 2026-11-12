---
name: clean-code
description: "Clean Code 실전 — Composed Method, Cognitive Complexity, Guard Clause, 네이밍, WHY 주석, Tell Don't Ask 를 BAD/GOOD 예시로 정리. Use when 읽기 어려운 긴 메서드·깊은 중첩을 정리하거나 코드 가독성을 리뷰할 때."
---

# Clean Code 실전 가이드

읽기 좋은 코드가 좋은 코드다. AI 시대에 가독성은 사람과 AI 모두의 생산성에 직결된다.

## Quick Reference

| 상황 | 원칙 | 참조 |
|------|------|------|
| 메서드가 50줄 초과 | Composed Method로 분할 | #composed-method |
| 중첩 if 3단 이상 | Guard Clause (Early Return) | #guard-clause |
| 코드 의미가 불명확 | 의도를 드러내는 이름 / WHY 주석 | #naming |
| 외부에서 상태 판단 | Tell, Don't Ask | #tell-dont-ask |
| 복잡도 수치화 필요 | Cognitive Complexity ≤ 15 | #cognitive-complexity |

---

## Composed Method Pattern

Kent Beck의 핵심 원칙: **한 메서드 안의 모든 호출은 같은 추상화 수준이어야 한다 (SLAP).**

### 분할 판단 기준

| 기준 | 행동 |
|------|------|
| 로직 블록 3줄 이상, 재사용 가능 | 의미 있는 이름으로 메서드 추출 |
| 로직 1-2줄, 의도가 명확 | 인라인 유지 + WHY 주석 |
| 메서드 20-50줄 | 정상 범위, 분할 불필요 |
| 메서드 50줄 초과 | 분할 검토 필수 |
| Cognitive Complexity > 15 | 반드시 리팩토링 |

### 균형점: Composed Method vs Deep Module

Kent Beck(Composed Method)과 John Ousterhout(Deep Module)의 균형:

```
✅ GOOD: 의미 있는 추출 — 각 메서드가 하나의 명확한 책임
  processOrder() → validateOrder() → calculateTotal() → saveOrder()

❌ BAD: 과도한 분해 — 15개 파일을 넘나들며 읽어야 이해 가능
  processOrder() → step1() → step1a() → step1a_i() → ...

💡 원칙: 추출된 메서드가 "깊은 모듈"이어야 한다
   — 단순한 인터페이스 뒤에 의미 있는 복잡성을 숨길 것
   — 1-2줄짜리 위임만 하는 얕은 메서드는 오히려 해로움
```

### Java 예시

```java
// ❌ BAD: 추상화 수준이 혼재
public OrderResult processOrder(OrderRequest request) {
    // 검증 로직 (저수준)
    if (request.getItems() == null || request.getItems().isEmpty()) {
        throw new InvalidOrderException("Items required");
    }
    if (request.getItems().size() > 100) {
        throw new InvalidOrderException("Too many items: " + request.getItems().size());
    }
    for (Item item : request.getItems()) {
        if (item.getQuantity() <= 0) {
            throw new InvalidOrderException("Invalid quantity for: " + item.getName());
        }
    }
    // 할인 계산 (저수준)
    BigDecimal total = BigDecimal.ZERO;
    for (Item item : request.getItems()) {
        BigDecimal price = item.getPrice().multiply(BigDecimal.valueOf(item.getQuantity()));
        if (item.hasDiscount()) {
            price = price.multiply(BigDecimal.ONE.subtract(item.getDiscountRate()));
        }
        total = total.add(price);
    }
    // 주문 생성 (고수준)
    Order order = Order.create(request.getUserId(), request.getItems(), total);
    orderRepository.save(order);
    eventPublisher.publish(new OrderCreated(order.getId()));
    return OrderResult.success(order.getId());
}

// ✅ GOOD: Composed Method — 같은 추상화 수준
public OrderResult processOrder(OrderRequest request) {
    validateOrder(request);
    BigDecimal total = calculateTotal(request.getItems());
    return createAndPublish(request.getUserId(), request.getItems(), total);
}
```

### Go 예시

```go
// ❌ BAD: 한 함수에 검증 + 계산 + 저장이 혼재
func (s *Service) ProcessOrder(ctx context.Context, req OrderRequest) (*OrderResult, error) {
    if len(req.Items) == 0 {
        return nil, ErrEmptyItems
    }
    if len(req.Items) > 100 {
        return nil, fmt.Errorf("too many items: %d", len(req.Items))
    }
    for _, item := range req.Items {
        if item.Quantity <= 0 {
            return nil, fmt.Errorf("invalid quantity for %s", item.Name)
        }
    }
    var total decimal.Decimal
    for _, item := range req.Items {
        price := item.Price.Mul(decimal.NewFromInt(int64(item.Quantity)))
        if item.DiscountRate.GreaterThan(decimal.Zero) {
            price = price.Mul(decimal.NewFromInt(1).Sub(item.DiscountRate))
        }
        total = total.Add(price)
    }
    order := NewOrder(req.UserID, req.Items, total)
    if err := s.repo.Save(ctx, order); err != nil {
        return nil, fmt.Errorf("saving order: %w", err)
    }
    return &OrderResult{ID: order.ID}, nil
}

// ✅ GOOD: Composed Method
func (s *Service) ProcessOrder(ctx context.Context, req OrderRequest) (*OrderResult, error) {
    if err := validateOrder(req); err != nil {
        return nil, err
    }
    total := calculateTotal(req.Items)
    return s.createOrder(ctx, req.UserID, req.Items, total)
}
```

---

## Cognitive Complexity

Cyclomatic Complexity(분기 수)보다 **인지 부하**를 정확히 측정하는 SonarQube 메트릭.

### Cyclomatic vs Cognitive

| 코드 | Cyclomatic | Cognitive | 실제 난이도 |
|------|-----------|-----------|-----------|
| 4-case switch | 4 | 1 | 쉬움 |
| 3단 중첩 if-for-if | 3 | 6+ | 어려움 |
| Guard clause 4개 | 4 | 4 | 쉬움 |
| 중첩 삼항 연산자 | 2 | 4+ | 어려움 |

### 계산 규칙 (핵심)

```
+1: if, else if, else, switch, for, while, catch, &&, ||, ?:
중첩 보너스: 중첩 깊이마다 +1 추가
break/continue to label: +1
재귀 호출: +1
```

### 리팩토링 전략

```java
// ❌ Cognitive Complexity = 12 (중첩 + 조건 체이닝)
public String evaluate(User user, Order order) {
    if (user != null) {                              // +1
        if (user.isVIP()) {                          // +2 (중첩)
            if (order.getTotal() > 1000) {           // +3 (중첩)
                return "GOLD";
            } else {                                 // +1
                return "SILVER";
            }
        } else {                                     // +1
            if (order.getTotal() > 500) {            // +2 (중첩)
                return "BRONZE";
            } else {                                 // +1
                return "STANDARD";
            }
        }
    }                                                // +1 (null check)
    return "NONE";
}

// ✅ Cognitive Complexity = 4 (Guard Clause + 단일 분기)
public String evaluate(User user, Order order) {
    if (user == null) return "NONE";                 // +1
    if (user.isVIP()) return evaluateVIP(order);     // +1
    return order.getTotal() > 500 ? "BRONZE" : "STANDARD"; // +2
}

private String evaluateVIP(Order order) {
    return order.getTotal() > 1000 ? "GOLD" : "SILVER"; // +1
}
```

---

## Guard Clause (Early Return)

### 핵심 원칙

1. 예외 상황을 먼저 걸러내고, happy path를 최외곽에 배치
2. 중첩 깊이를 줄여 Cognitive Complexity 감소
3. 각 guard는 하나의 검증 책임

### Java 패턴

```java
// ❌ BAD: 중첩 피라미드 (Arrow Anti-Pattern)
public Money calculateDiscount(Order order) {
    if (order != null) {
        if (order.hasItems()) {
            if (order.getCoupon() != null) {
                if (order.getCoupon().isValid()) {
                    return order.getCoupon().apply(order.getTotal());
                }
            }
        }
    }
    return Money.ZERO;
}

// ✅ GOOD: Guard Clause
public Money calculateDiscount(Order order) {
    if (order == null) return Money.ZERO;
    if (!order.hasItems()) return Money.ZERO;
    if (order.getCoupon() == null) return Money.ZERO;
    if (!order.getCoupon().isValid()) return Money.ZERO;

    return order.getCoupon().apply(order.getTotal());
}
```

### Go 패턴

```go
// ❌ BAD
func (s *Service) GetUser(ctx context.Context, id string) (*User, error) {
    if id != "" {
        user, err := s.repo.Find(ctx, id)
        if err == nil {
            if user.Active {
                return user, nil
            }
            return nil, ErrInactiveUser
        }
        return nil, fmt.Errorf("find user: %w", err)
    }
    return nil, ErrEmptyID
}

// ✅ GOOD
func (s *Service) GetUser(ctx context.Context, id string) (*User, error) {
    if id == "" {
        return nil, ErrEmptyID
    }
    user, err := s.repo.Find(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("find user: %w", err)
    }
    if !user.Active {
        return nil, ErrInactiveUser
    }
    return user, nil
}
```

---

## 네이밍 컨벤션

### 공통 원칙

| 규칙 | 예시 |
|------|------|
| 의도를 드러내는 이름 | `elapsedTimeInDays` not `d` |
| Boolean은 질문형 | `isValid`, `hasPermission`, `canWithdraw` |
| 매직 넘버 제거 | `MAX_RETRY_COUNT = 3` not `3` |
| 도메인 용어 사용 | `reservation` not `booking_data` |
| 대칭적 이름 | `open/close`, `start/stop`, `get/set` |

### Java 네이밍

```java
// ❌ BAD
int d;                              // 의미 불명
boolean flag;                       // 무슨 플래그?
List<String> list;                  // 무슨 리스트?
void process(Data data);            // 무슨 처리?

// ✅ GOOD
int elapsedDays;
boolean isEligibleForDiscount;
List<String> activeUserEmails;
void applyMembershipDiscount(Order order);
```

### Go 네이밍

```go
// Go는 스코프에 따라 길이가 달라짐
// 좁은 스코프: 짧게
for i, v := range items { ... }
if err != nil { ... }

// 넓은 스코프: 설명적
var maxRetryAttempts = 3
type OrderProcessor struct { ... }

// 패키지명이 컨텍스트 제공 — 중복 금지
http.Client      // ✅ (not http.HTTPClient)
user.Service     // ✅ (not user.UserService)
```

---

## 주석 철학: Comment the WHY

### 주석이 필요한 경우

```java
// ✅ 비즈니스 규칙 — 코드만으로는 "왜"를 알 수 없음
// 금융감독원 규정: 1일 이체 한도 5000만원 (2024.01 시행)
private static final long DAILY_TRANSFER_LIMIT = 50_000_000L;

// ✅ 비자명한 최적화 — 벤치마크 근거 명시
// StringBuilder 대신 + 사용: JDK 15+ invokedynamic으로 더 빠름 (benchmark: 2.3x)
String result = prefix + ":" + suffix;

// ✅ 외부 시스템 우회 — 맥락 없으면 "왜 이런 코드?"가 됨
// PG사 API가 간헐적으로 빈 응답을 보냄 (2024-03 이슈 PAYMENT-1234)
if (response.getBody() == null) {
    return retryPayment(request);
}
```

### 주석이 불필요한 경우

```java
// ❌ 코드 반복 (WHAT 주석)
// 사용자를 찾는다
User user = userRepository.findById(id);

// ❌ 당연한 getter
// 이름을 반환한다
public String getName() { return name; }

// ❌ 이력 주석 — git log로 대체
// 2024-01-15 김개발: 할인 로직 추가
// 2024-02-20 이개발: 쿠폰 검증 추가
```

---

## Tell, Don't Ask

### 핵심

객체의 상태를 꺼내서(Ask) 외부에서 판단하지 말고, 객체에게 행동을 시켜라(Tell).

### Java

```java
// ❌ ASK: 외부에서 상태를 꺼내 판단
if (account.getStatus() == AccountStatus.ACTIVE
    && account.getBalance().compareTo(amount) >= 0) {
    account.setBalance(account.getBalance().subtract(amount));
    transactionRepository.save(new Transaction(account.getId(), amount));
}

// ✅ TELL: 객체가 자신의 비즈니스 규칙을 수행
account.withdraw(amount);  // 내부에서 상태 검증 + 잔액 차감 + 이벤트 발행
```

### Go

```go
// ❌ ASK
if cart.Items != nil && len(cart.Items) > 0 {
    total := decimal.Zero
    for _, item := range cart.Items {
        total = total.Add(item.Price.Mul(decimal.NewFromInt(int64(item.Qty))))
    }
    cart.Total = total
}

// ✅ TELL
total := cart.CalculateTotal()  // Cart가 자신의 합계를 계산
```

---

## Anti-Patterns 카탈로그

| Anti-Pattern | 증상 | 해결 |
|-------------|------|------|
| **Arrow Code** | 중첩 3단+ 피라미드 | Guard Clause |
| **God Method** | 50줄+ 메서드 | Composed Method로 분할 |
| **Primitive Obsession** | `String email`, `int status` 남발 | Value Object (`Email`, `OrderStatus`) |
| **Magic Number** | `if (type == 3)` | Enum / Named Constant |
| **Feature Envy** | 다른 객체의 필드를 여러 개 꺼내 사용 | 로직을 해당 객체로 이동 (Tell, Don't Ask) |
| **Long Parameter List** | 파라미터 4개+ | Parameter Object / Builder |
| **Comment Rot** | 코드는 바뀌었는데 주석은 옛날 그대로 | WHY 주석만, WHAT 주석 삭제 |
| **Dead Code** | 주석 처리된 코드, 미사용 메서드 | 즉시 삭제 (git이 기억함) |

---

## 메서드 추출 판단 트리

```
메서드가 50줄 초과?
  ├─ YES → 반드시 분할
  └─ NO → Cognitive Complexity > 15?
      ├─ YES → Guard Clause 또는 메서드 추출로 중첩 감소
      └─ NO → 한 메서드에 추상화 수준이 섞여있나?
          ├─ YES → SLAP 위반 → 같은 수준으로 추출
          └─ NO → 현재 상태 유지 (과도한 분해 금지)
```

---

## 도구 추천

### Java

| 도구 | 용도 |
|------|------|
| SonarQube (S3776) | Cognitive Complexity 측정 (기본 ≤ 15) |
| Error Prone | 컴파일 타임 버그 탐지 (Google) |
| ArchUnit | 아키텍처 규칙을 테스트 코드로 강제 |
| Checkstyle | 스타일 일관성 (네이밍, 포맷) |

### Go

| 도구 | 용도 |
|------|------|
| golangci-lint | 메타 린터 (100+ 린터 통합 실행) |
| gocritic | 스타일/성능/버그 패턴 탐지 |
| revive | 커스텀 규칙 지원 린터 (golint 대체) |
| gocognit | Cognitive Complexity 측정 |

### 권장 golangci-lint 설정

```yaml
linters:
  enable:
    - gocritic
    - revive
    - gocognit
    - staticcheck
    - errcheck
    - gosimple
    - unused

linters-settings:
  gocognit:
    min-complexity: 15
  gocritic:
    enabled-tags: [diagnostic, style, performance]
  revive:
    rules:
      - name: var-naming
      - name: exported
```

---

## 핵심 원칙 요약

1. **20-50줄** — 메서드 길이의 실무 sweet spot
2. **Cognitive Complexity ≤ 15** — 줄 수보다 중요한 가독성 지표
3. **Guard Clause** — 중첩 대신 조기 반환, happy path를 최외곽에
4. **WHY만 주석** — 코드는 WHAT/HOW, 주석은 비즈니스 의도만
5. **Tell, Don't Ask** — 상태를 꺼내지 말고 행동을 위임
6. **SLAP** — 한 메서드 안에서 추상화 수준 통일
7. **Deep Module** — 추출된 메서드가 의미 있는 복잡성을 숨겨야 함 (과도한 분해 금지)
