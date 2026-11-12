---
name: effective-java
description: "Effective Java 설계 결정 — 객체 생성 패턴, Modern Java(17·21) 기능, 제네릭·enum, Stream vs for loop, 예외 처리. Use when Java 클래스·API 를 설계하거나 코드 리뷰에서 관용적 Java 구현을 고를 때."
---

# Effective Java — 패턴 결정 가이드

Effective Java + Modern Java (17+, 21+) 기반 설계 결정 가이드.
"이 상황에서는 이 패턴을 써라" 형식의 실전 레퍼런스.

## Quick Reference — 객체 생성 결정 트리

```
객체 생성 어떻게?
    ├─ 파라미터 < 3개, 필수만 ────────> 생성자
    ├─ 파라미터 3개+, 선택 파라미터 ──> Builder (@Builder)
    ├─ 여러 생성 방법 / 캐싱 필요 ───> Static Factory Method
    ├─ 불변 데이터 컨테이너 ─────────> Record (Java 16+)
    └─ 외부 리소스 의존 ─────────────> DI (생성자 주입)
```

---

## CRITICAL: 설계 패턴 (Items 1–20)

### Item 1: Static Factory Method

**조건**: 동일 시그니처에 다른 의미, 캐싱, 서브타입 반환이 필요할 때

```java
// Bad: 생성자만으로는 의미 구분 불가
Color c1 = new Color(255, 0, 0);  // 빨강인지 즉시 알 수 없음

// Good: 이름으로 의도를 드러냄
public class Color {
    private final int r, g, b;
    private Color(int r, int g, int b) { this.r = r; this.g = g; this.b = b; }
    public static Color ofRgb(int r, int g, int b) { return new Color(r, g, b); }
    public static Color ofRed()  { return new Color(255, 0, 0); }
    public static Color ofBlue() { return new Color(0, 0, 255); }
}
```

**네이밍 컨벤션**:

| 메서드명 | 용도 | 예시 |
|---------|------|------|
| `of()` | 집합/경량 인스턴스 | `List.of(1, 2, 3)` |
| `from()` | 타입 변환 | `Instant.from(zonedDateTime)` |
| `valueOf()` | 같은 값 캐싱 | `Integer.valueOf(127)` |
| `create()` / `newInstance()` | 매번 새 인스턴스 | `Array.newInstance(...)` |

**이유**: 이름으로 의도 전달 + 캐싱/서브타입 유연성 확보

---

### Item 2: Builder Pattern

**조건**: 파라미터 3개 이상, 선택적 파라미터 존재, 불변 객체 생성

```java
// Bad: 텔레스코핑 생성자
public UserProfile(String name, String email) { ... }
public UserProfile(String name, String email, String phone) { ... }
public UserProfile(String name, String email, String phone, String addr) { ... }

// Good: Lombok @Builder
@Builder @Getter
public class UserProfile {
    private final String name;           // 필수
    private final String email;          // 필수
    @Builder.Default
    private final String phone = "";     // 선택
    @Builder.Default
    private final String address = "";   // 선택
}

UserProfile profile = UserProfile.builder()
    .name("Kim").email("kim@test.com").phone("010-1234-5678")
    .build();
```

**이유**: 가독성 + 불변 + 선택 파라미터 자유 조합

---

### Item 5: DI — 생성자 주입

**조건**: 외부 리소스(Repository, Service, Client)에 의존할 때

```java
// Bad: 필드 주입 → 테스트에서 교체 불가
@Service
public class OrderService {
    @Autowired private OrderRepository orderRepository;
    @Autowired private PaymentClient paymentClient;
}

// Good: 생성자 주입
@Service
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentClient paymentClient;
}
```

**이유**: 불변 보장 + 테스트 용이 + 순환 의존성 컴파일 타임 감지

---

### Item 17: 불변 객체 설계

**조건**: VO, DTO, 이벤트, API 응답 등 데이터 컨테이너

```java
// Bad: Setter로 변경 가능한 DTO
@Data  // getter + setter 모두 생성
public class OrderResponse {
    private Long orderId;
    private String status;
    private List<String> items;
}

// Good: Record (Java 16+)
public record OrderResponse(Long orderId, String status, List<String> items) {
    public OrderResponse {  // Compact constructor
        items = List.copyOf(items);  // 방어적 복사 → 불변
    }
}

// JPA Entity는 Record 불가 → private final + no setter
@Entity @Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Money {
    @Id @GeneratedValue private Long id;
    private final BigDecimal amount;
    private final String currency;
    public Money add(Money other) {
        return new Money(this.amount.add(other.amount), this.currency);
    }
}
```

**이유**: Thread-safe + 부작용 없음 + 안전한 Map key/Set 원소

---

### Item 18: Composition over Inheritance

**조건**: is-a 관계가 불명확하거나 외부 라이브러리 클래스 확장 시

```java
// Bad: 상속 → 캡슐화 깨짐 (addAll이 add 호출 시 이중 카운트)
public class InstrumentedSet<E> extends HashSet<E> {
    private int addCount = 0;
    @Override public boolean add(E e) { addCount++; return super.add(e); }
}

// Good: Composition + Forwarding
public class InstrumentedSet<E> implements Set<E> {
    private final Set<E> delegate;
    private int addCount = 0;
    public InstrumentedSet(Set<E> delegate) { this.delegate = delegate; }
    @Override public boolean add(E e) { addCount++; return delegate.add(e); }
    // 나머지 Set 메서드는 delegate에 위임
}
```

**이유**: 상위 클래스 내부 구현 변경에 안전

---

### Item 20: Interface > Abstract Class

**조건**: 타입 정의 시 기본 선택은 Interface

```java
// Good: 인터페이스 + default 메서드
public interface PaymentProcessor {
    PaymentResult process(Payment payment);
    default PaymentResult processWithRetry(Payment payment, int maxRetries) {
        for (int i = 0; i < maxRetries; i++) {
            try { return process(payment); }
            catch (TransientException e) { if (i == maxRetries - 1) throw e; }
        }
        throw new IllegalStateException("unreachable");
    }
}

// Sealed interface로 구현 제한 (Java 17+)
public sealed interface PaymentProcessor
    permits CardProcessor, BankTransferProcessor, VirtualAccountProcessor {
    PaymentResult process(Payment payment);
}
```

**이유**: 다중 구현 가능 + mixin 지원 + sealed로 계층 제어

---

## CRITICAL: Modern Java (17+, 21+)

### Record (Java 16+)

**사용 조건**: DTO, VO, 이벤트, 설정값 등 불변 데이터
**사용 불가**: JPA Entity (기본 생성자/setter 필요), 상속 필요 시

```java
// DTO — Bean Validation과 함께
public record CreateOrderRequest(
    @NotNull Long userId,
    @NotEmpty List<OrderItemRequest> items,
    @Size(max = 200) String memo
) {}

// VO — Compact constructor로 유효성 검증
public record Money(BigDecimal amount, Currency currency) {
    public Money {
        if (amount.compareTo(BigDecimal.ZERO) < 0)
            throw new IllegalArgumentException("음수 금액: " + amount);
    }
    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) throw new CurrencyMismatchException();
        return new Money(this.amount.add(other.amount), this.currency);
    }
}
```

### Sealed Class (Java 17+)

**조건**: 닫힌 타입 계층, switch exhaustiveness 보장

```java
public sealed interface ApiResult<T>
    permits ApiResult.Success, ApiResult.Failure {
    record Success<T>(T data) implements ApiResult<T> {}
    record Failure<T>(String code, String message) implements ApiResult<T> {}
}

// switch exhaustiveness (Java 21+) — 새 permits 추가 시 컴파일 에러
return switch (result) {
    case ApiResult.Success(var data) -> ResponseEntity.ok(data);
    case ApiResult.Failure(var code, var msg) -> ResponseEntity.badRequest().body(msg);
};
```

### Virtual Threads (Java 21+)

**사용**: I/O 바운드 작업 (DB 쿼리, HTTP 호출, 파일 읽기)
**금지**: CPU 바운드 연산, synchronized 블록 내 I/O (pinning 발생)

```java
// Spring Boot 3.2+ — application.yml
spring.threads.virtual.enabled=true

// 직접 사용 시
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<String>> futures = urls.stream()
        .map(url -> executor.submit(() -> httpClient.get(url)))
        .toList();
}

// 주의: synchronized → ReentrantLock 교체 (pinning 방지)
// Bad: synchronized (lock) { dbCall(); }
// Good:
private final ReentrantLock lock = new ReentrantLock();
lock.lock();
try { dbCall(); } finally { lock.unlock(); }
```

### Pattern Matching (Java 16+ / 21+)

```java
// Bad: instanceof + 캐스팅
if (shape instanceof Circle) {
    Circle c = (Circle) shape;
    return Math.PI * c.radius() * c.radius();
}

// Good: Pattern Matching for instanceof (Java 16+)
if (shape instanceof Circle c) {
    return Math.PI * c.radius() * c.radius();
}

// Good: switch Pattern Matching (Java 21+)
double area = switch (shape) {
    case Circle c    -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.width() * r.height();
    case Triangle t  -> 0.5 * t.base() * t.height();
};
```

---

## 제네릭 & 열거형

### Raw Type 금지 (Item 26)

```java
// Bad: 런타임까지 타입 오류 모름
List list = new ArrayList();
list.add("hello"); list.add(123);

// Good: 컴파일 타임 타입 체크
List<String> list = new ArrayList<>();
```

### PECS — Producer Extends, Consumer Super (Item 28)

```java
// Producer → extends, Consumer → super
public <T> void copy(List<? extends T> src, List<? super T> dest) {
    for (T item : src) { dest.add(item); }
}

// Comparable은 항상 Consumer → super
public static <T extends Comparable<? super T>> T max(Collection<? extends T> c) {
    return c.stream().max(Comparator.naturalOrder()).orElseThrow();
}
```

### int 상수 → Enum (Item 30)

```java
// Bad
public static final int STATUS_PENDING = 0;
public static final int STATUS_APPROVED = 1;

// Good: Enum + 동작 포함
public enum OrderStatus {
    PENDING  { public boolean canCancel() { return true; } },
    APPROVED { public boolean canCancel() { return false; } },
    SHIPPED  { public boolean canCancel() { return false; } };
    public abstract boolean canCancel();
}
```

---

## Stream vs For Loop 선택 기준

| 상황 | 선택 | 이유 |
|------|------|------|
| filter → map → collect 체인 | Stream | 선언적, 가독성 |
| flatMap (중첩 컬렉션 평탄화) | Stream | for 중첩보다 깔끔 |
| groupingBy / partitioningBy | Stream | Collectors 활용 |
| break / continue 필요 | For Loop | Stream은 조기 탈출 불가 |
| checked exception 발생 | For Loop | 람다에서 처리 불편 |
| 여러 변수 동시 수정 | For Loop | effectively final 제약 |
| 단순 변환 1단계 | 어느 쪽이든 | 팀 컨벤션 따름 |

```java
// Stream: groupingBy
Map<OrderStatus, List<Order>> grouped = orders.stream()
    .filter(o -> o.getCreatedAt().isAfter(weekAgo))
    .collect(Collectors.groupingBy(Order::getStatus));

// For Loop: checked exception + break
for (File file : files) {
    try {
        String content = Files.readString(file.toPath());
        if (content.contains("ERROR")) { break; }
    } catch (IOException e) { log.warn("파일 읽기 실패: {}", file, e); }
}
```

---

## 예외 처리 전략

### 비즈니스 예외는 RuntimeException 계열

```java
public abstract class BusinessException extends RuntimeException {
    private final ErrorCode errorCode;
    protected BusinessException(ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
    }
}
public class OrderNotFoundException extends BusinessException {
    public OrderNotFoundException(Long orderId) {
        super(ErrorCode.ORDER_NOT_FOUND);  // 실패 값 포함 → 디버깅 용이
    }
}
```

### 표준 예외 재활용 (Item 72)

| 예외 | 용도 |
|------|------|
| `IllegalArgumentException` | 잘못된 파라미터 값 |
| `IllegalStateException` | 객체 상태가 메서드 호출에 부적합 |
| `NullPointerException` | null이면 안 되는 곳에 null |
| `UnsupportedOperationException` | 지원하지 않는 연산 |

### 예외 메시지에 실패 값 포함 (Item 75)

```java
// Bad
throw new IllegalArgumentException("범위 초과");
// Good
throw new IllegalArgumentException(
    "주문 수량 범위 초과: quantity=%d, max=%d".formatted(quantity, maxQuantity));
```

---

## 동시성 (Items 78–84)

### Thread 직접 생성 금지 → Executor / Virtual Thread

```java
// Bad
new Thread(() -> sendEmail(user)).start();
// Good: Virtual Thread (Java 21+)
Thread.startVirtualThread(() -> sendEmail(user));
// Good: ExecutorService Bean
@Bean
public ExecutorService taskExecutor() {
    return Executors.newVirtualThreadPerTaskExecutor();
}
```

### 공유 가변 데이터 보호

| 상황 | 해결 |
|------|------|
| 단순 카운터/플래그 | `AtomicInteger`, `AtomicBoolean` |
| 복합 연산 보호 | `ReentrantLock` (Virtual Thread 호환) |
| 읽기 많고 쓰기 적음 | `ReadWriteLock` / `StampedLock` |
| 가변 데이터 자체 제거 | 불변 객체 + 새 인스턴스 반환 |

```java
// Atomic 카운터
private final AtomicLong requestCount = new AtomicLong(0);
public void handleRequest() { requestCount.incrementAndGet(); }

// 불변 객체: 가장 안전한 동시성 해법
public record Account(Long id, BigDecimal balance) {
    public Account deposit(BigDecimal amount) {
        return new Account(id, balance.add(amount));
    }
}
```

---

## Anti-Patterns 표

| 실수 | 해결 | Item |
|------|------|------|
| `new Boolean(true)` | `Boolean.valueOf(true)` | 1 |
| 텔레스코핑 생성자 (파라미터 4개+) | `@Builder` | 2 |
| `@Autowired` 필드 주입 | `@RequiredArgsConstructor` + `private final` | 5 |
| `@Data` on DTO (setter 노출) | Record 또는 `@Value` | 17 |
| 외부 클래스 상속 | Composition + Forwarding | 18 |
| Raw type `List` | `List<String>` | 26 |
| `catch (Exception e) {}` 빈 catch | 최소 log.error + 재throw 검토 | 77 |
| `new Thread().start()` | Virtual Thread / ExecutorService | 80 |
| `public static final int` 상수 | Enum | 30 |
| mutable DTO 공유 | Record / 불변 객체 | 17 |
| `synchronized` 내 I/O | `ReentrantLock` | 79 |
| 예외 메시지에 값 누락 | `"expected=%d, actual=%d".formatted(...)` | 75 |

---

## Checklist — 코드 리뷰 시 확인

```
□ 파라미터 3개+인 생성자 → Builder 검토
□ DTO/VO에 setter 있음 → Record 전환 검토
□ @Autowired 필드 주입 → 생성자 주입 전환
□ Raw type 사용 → 제네릭 추가
□ int 상수 그룹 → Enum 전환
□ catch (Exception e) {} → 로그 + 적절한 처리
□ new Thread() → Virtual Thread / Executor
□ 외부 클래스 상속 → Composition 검토
□ synchronized 내 I/O → ReentrantLock 전환
□ 예외 메시지에 실패 값 포함 여부
```

---

## 관련 스킬

- `/java:spring-data` — JPA Entity 설계, Repository 패턴
- `/java:spring-testing` — 불변 객체/Builder 테스트 전략
- `/java:concurrency-spring` — 낙관적/비관적 락, 분산 락
- `/java:refactoring-spring` — 레거시 코드 리팩토링 절차
