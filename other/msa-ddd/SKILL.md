---
name: msa-ddd
description: "DDD 마이크로서비스 설계 — Bounded Context, Aggregate, Domain Event, Context Mapping, Event Storming, 서비스 분해 전략. Use when 도메인 기준으로 서비스 경계를 나누거나 Aggregate 를 설계할 때."
---

# DDD 마이크로서비스 설계 가이드

Bounded Context, Aggregate, Domain Event, Context Mapping, 서비스 경계 설계

## Quick Reference (결정 트리)

```
서비스 분리가 필요한가?
    |
    +-- 팀 1~2개, 도메인 단순 ---------> Modular Monolith
    |     └─ 패키지/모듈 경계로 분리 (단일 배포)
    +-- 팀 3개+, 독립 배포 필요 -------> Microservices (DDD 기반)
    |     └─ Bounded Context = 서비스 경계
    +-- 레거시 전환 중 ----------------> Strangler Fig + ACL
          └─ 점진적 추출 (Anti-Corruption Layer)

Bounded Context 식별 방법?
    |
    +-- 비즈니스 이벤트 중심 ----------> Event Storming (권장)
    +-- 기존 조직/팀 구조 기반 --------> Conway's Law 활용
    +-- 데이터 응집도 기반 ------------> Aggregate 클러스터링

Aggregate 크기 결정?
    |
    +-- 하나의 트랜잭션에서 일관성 필요 --> 같은 Aggregate
    +-- 결과적 일관성(Eventual) 허용 ----> 별도 Aggregate + Domain Event
    +-- 동시 수정 충돌 빈번 -----------> Aggregate 분리 (잠금 경합 감소)
```

---

## CRITICAL: 서비스 분해 전략 비교

| 항목 | 기술 분해 | 도메인 분해 (DDD) |
|------|-----------|-------------------|
| **기준** | 기술 레이어 (UI/API/DB) | 비즈니스 도메인 (주문/결제/배송) |
| **결합도** | 높음 (레이어 간 의존) | 낮음 (도메인 독립) |
| **팀 구조** | 기능별 팀 (프론트/백엔드/DBA) | 도메인별 크로스펑셔널 팀 |
| **확장성** | 전체 레이어 동시 확장 | 도메인 단위 독립 확장 |
| **DB 전략** | 공유 DB (모놀리스 유지) | Database per Service |
| **결과** | Distributed Monolith 위험 | 느슨한 결합, 독립 배포 |

```
Monolith vs Modular Monolith vs Microservices 결정:
  [팀 규모]     1~5명 → Monolith / 5~15명 → Modular Monolith / 15명+ → MSA
  [도메인 복잡도] 단순 CRUD → Monolith / 중간 → Modular / 복잡 → MSA + DDD
```

---

## Strategic Design (전략적 설계)

### Bounded Context

Bounded Context는 특정 도메인 모델이 일관되게 적용되는 명시적 경계이다.
경계 안에서는 Ubiquitous Language(보편 언어)가 통용되며, 같은 용어라도
경계 밖에서는 다른 의미를 가질 수 있다.

```
원칙: 하나의 Bounded Context = 하나의 마이크로서비스 (기본 규칙)
예외: 너무 큰 Context → 분리 / 너무 작은 Context → 합병

예시: E-Commerce 도메인 분해
┌─────────────────────────────────────────────────────────┐
│  ┌───────────┐  ┌───────────┐  ┌───────────┐           │
│  │   Order   │  │  Payment  │  │ Inventory │           │
│  │ - Order   │  │ - Payment │  │ - Stock   │           │
│  │ - LineItem│  │ - Invoice │  │ - Product │           │
│  └───────────┘  └───────────┘  └───────────┘           │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐           │
│  │ Customer  │  │ Shipping  │  │  Catalog  │           │
│  │ - Customer│  │ - Delivery│  │ - Product │           │
│  │ - Address │  │ - Carrier │  │ - Category│           │
│  └───────────┘  └───────────┘  └───────────┘           │
└─────────────────────────────────────────────────────────┘
※ "Product"는 Inventory와 Catalog에서 다른 의미 (재고 vs 전시)
```

### Context Mapping

Bounded Context 간 관계를 명시적으로 정의하는 전략적 패턴이다.
upstream/downstream 관계는 데이터 흐름이 아닌 모델 영향력의 방향이다.

```
관계 유형:
  Partnership       → 두 팀이 공동 목표로 모델을 함께 조정
  Shared Kernel     → 공유 모델/코드 사용 (높은 신뢰 필요)
  Customer-Supplier → 하류 팀이 상류 팀에 요구사항 전달
  Conformist        → 하류가 상류 모델을 그대로 수용
  ACL               → Anti-Corruption Layer로 번역 계층 구축
  Open Host Service → 공개 프로토콜(API)로 접근 제공
  Published Language→ 공유 언어(JSON Schema, Avro)로 통신
  Separate Ways     → 통합하지 않고 독립적으로 진화

Context Map 다이어그램 예시:
┌──────────┐  OHS/PL   ┌──────────┐  ACL    ┌──────────┐
│  Order   │ ────────> │ Payment  │ <────── │ External │
│ (Core)   │           │(Support) │         │ PG API   │
└────┬─────┘           └──────────┘         └──────────┘
     │ Customer-Supplier
     ▼
┌──────────┐  Partnership  ┌──────────┐
│Inventory │ <──────────── │ Shipping │
└──────────┘               └──────────┘

도메인 유형별 투자 전략:
  Core Domain    → 최고 인력 배치, DDD Tactical 패턴 집중 적용
  Supporting     → 외주 또는 패키지 솔루션 고려
  Generic        → 상용 서비스 사용 (결제 PG, 알림 SaaS 등)
```

---

## Tactical Design (전술적 설계)

### Aggregate

Aggregate는 데이터 변경의 트랜잭션 일관성 경계이다.
Aggregate Root는 외부에서 접근하는 유일한 진입점이다.

```
Aggregate Root 규칙:
  1. 외부에서는 Root를 통해서만 Aggregate 내부에 접근
  2. 하나의 트랜잭션 = 하나의 Aggregate 변경
  3. Aggregate 간 참조는 ID로만 (객체 참조 금지)
  4. Aggregate Root가 불변식(invariant)을 보장
  5. 작게 유지 (Large Aggregate = Lock 경합 증가)
```

```java
// === Aggregate Root ===
@Entity
@Table(name = "orders")
public class Order extends AbstractAggregateRoot<Order> {
    @Id
    private String id;
    @Column(nullable = false)
    private String customerId;  // 다른 Aggregate는 ID로만 참조
    @Enumerated(EnumType.STRING)
    private OrderStatus status;
    @Embedded
    private Money totalAmount;  // Value Object
    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "order_id")
    private List<OrderLineItem> lineItems = new ArrayList<>();

    // 팩토리 메서드 - 생성 시 도메인 이벤트 등록
    public static Order create(String customerId, List<OrderLineItem> items) {
        Order order = new Order();
        order.id = UUID.randomUUID().toString();
        order.customerId = customerId;
        order.status = OrderStatus.PENDING;
        order.lineItems.addAll(items);
        order.totalAmount = order.calculateTotal();
        // Spring Data AbstractAggregateRoot를 통해 이벤트 등록
        order.registerEvent(new OrderCreatedEvent(
            order.id, customerId, order.totalAmount));
        return order;
    }

    // 비즈니스 로직은 Aggregate Root가 캡슐화
    public void confirm() {
        if (this.status != OrderStatus.PENDING) {
            throw new IllegalStateException("PENDING 상태에서만 확정 가능");
        }
        this.status = OrderStatus.CONFIRMED;
        registerEvent(new OrderConfirmedEvent(this.id));
    }

    public void addLineItem(String productId, int quantity, Money unitPrice) {
        if (lineItems.size() >= 50) {
            throw new OrderLimitExceededException("최대 50개 아이템");
        }
        lineItems.add(new OrderLineItem(productId, quantity, unitPrice));
        this.totalAmount = calculateTotal();
    }

    private Money calculateTotal() {
        return lineItems.stream()
            .map(OrderLineItem::getSubtotal)
            .reduce(Money.ZERO, Money::add);
    }
}

// === Value Object (불변, 동등성은 속성 기반) ===
@Embeddable
public record Money(
    @Column(name = "amount") BigDecimal amount,
    @Column(name = "currency") String currency
) {
    public static final Money ZERO = new Money(BigDecimal.ZERO, "KRW");
    public Money {
        if (amount.compareTo(BigDecimal.ZERO) < 0)
            throw new IllegalArgumentException("금액은 0 이상이어야 합니다");
    }
    public Money add(Money other) {
        if (!this.currency.equals(other.currency))
            throw new IllegalArgumentException("통화 단위 불일치");
        return new Money(this.amount.add(other.amount), this.currency);
    }
}

// === Entity (Aggregate 내부, 식별자로 구분) ===
@Entity
@Table(name = "order_line_items")
public class OrderLineItem {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String productId;
    private int quantity;
    @Embedded
    @AttributeOverrides({
        @AttributeOverride(name = "amount", column = @Column(name = "unit_price")),
        @AttributeOverride(name = "currency", column = @Column(name = "unit_currency"))
    })
    private Money unitPrice;

    public Money getSubtotal() {
        return new Money(unitPrice.amount()
            .multiply(BigDecimal.valueOf(quantity)), unitPrice.currency());
    }
}
```

### Domain Event

Domain Event는 도메인에서 발생한 의미 있는 사건을 표현한다.
Aggregate 내부에서 생성되어 다른 Aggregate나 서비스에 전파된다.

```java
// === Domain Event 정의 ===
public record OrderCreatedEvent(String orderId, String customerId, Money totalAmount) {}
public record OrderConfirmedEvent(String orderId) {}

// === Spring ApplicationEvent로 내부 이벤트 처리 ===
@Component
@RequiredArgsConstructor
public class OrderEventHandler {
    private final InventoryService inventoryService;
    private final NotificationService notificationService;

    // 같은 트랜잭션 내에서 동기 처리
    @TransactionalEventListener(phase = TransactionPhase.BEFORE_COMMIT)
    public void onOrderCreated(OrderCreatedEvent event) {
        inventoryService.reserveStock(event.orderId());
    }
    // 트랜잭션 커밋 후 비동기 처리
    @Async
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void sendNotification(OrderConfirmedEvent event) {
        notificationService.sendOrderConfirmation(event.orderId());
    }
}

// === 외부 이벤트 발행 - Transactional Outbox 활용 ===
@Service
@RequiredArgsConstructor
public class OrderExternalEventPublisher {
    private final OutboxRepository outboxRepository;
    private final ObjectMapper objectMapper;

    // 커밋 전에 Outbox 테이블에 저장 (같은 트랜잭션)
    @TransactionalEventListener(phase = TransactionPhase.BEFORE_COMMIT)
    public void publishToOutbox(OrderCreatedEvent event) {
        outboxRepository.save(OutboxEvent.builder()
            .aggregateType("Order").aggregateId(event.orderId())
            .eventType("OrderCreated")
            .payload(objectMapper.writeValueAsString(event)).build());
    }
    // Outbox Relay 또는 Debezium CDC가 Kafka로 전달
}
```

### Repository Pattern

```java
// === Domain Repository 인터페이스 (domain 패키지) ===
public interface OrderRepository {
    Order findById(String id);
    Order save(Order order);
    void delete(Order order);
    List<Order> findByCustomerId(String customerId);
}

// === 인프라 구현 (infrastructure 패키지) ===
public interface JpaOrderRepository extends JpaRepository<Order, String> {
    List<Order> findByCustomerIdOrderByCreatedAtDesc(String customerId);
}

@Repository
@RequiredArgsConstructor
public class OrderRepositoryImpl implements OrderRepository {
    private final JpaOrderRepository jpaRepo;

    @Override
    public Order findById(String id) {
        return jpaRepo.findById(id)
            .orElseThrow(() -> new OrderNotFoundException(id));
    }
    @Override public Order save(Order order) { return jpaRepo.save(order); }
    @Override public void delete(Order order) { jpaRepo.delete(order); }
    @Override
    public List<Order> findByCustomerId(String customerId) {
        return jpaRepo.findByCustomerIdOrderByCreatedAtDesc(customerId);
    }
}
```

### Domain Service vs Application Service

```java
// === Domain Service: 여러 Aggregate에 걸친 비즈니스 로직 (상태 없음) ===
public class OrderPricingService {
    public Money calculateFinalPrice(Order order, Customer customer,
                                     List<Promotion> promotions) {
        Money basePrice = order.getTotalAmount();
        Money discount = promotions.stream()
            .filter(p -> p.isApplicable(order, customer))
            .map(p -> p.calculateDiscount(basePrice))
            .reduce(Money.ZERO, Money::add);
        return basePrice.subtract(discount);
    }
}

// === Application Service: 유스케이스 조율, 트랜잭션 관리 ===
@Service
@RequiredArgsConstructor
public class PlaceOrderUseCase {
    private final OrderRepository orderRepository;
    private final CustomerRepository customerRepository;
    private final OrderPricingService pricingService;

    @Transactional
    public OrderResult execute(PlaceOrderCommand cmd) {
        Customer customer = customerRepository.findById(cmd.customerId());
        List<Promotion> promotions = promotionRepository.findActive();
        Order order = Order.create(cmd.customerId(), cmd.items());
        Money finalPrice = pricingService.calculateFinalPrice(
            order, customer, promotions);
        order.applyFinalPrice(finalPrice);
        // 저장 시 AbstractAggregateRoot가 Domain Event 자동 발행
        return OrderResult.from(orderRepository.save(order));
    }
}
```

---

## Event Storming

Event Storming은 Alberto Brandolini가 고안한 워크숍 기법으로,
도메인 전문가와 개발자가 함께 비즈니스 프로세스를 탐색한다.

```
색상별 포스트잇 의미:
  [주황] Domain Event    - "주문이 생성되었다" (과거형)
  [파랑] Command         - "주문을 생성하라" (명령형)
  [노랑] Aggregate       - Command를 받아 Event를 발행하는 주체
  [보라] Policy/Rule     - "결제 완료되면 → 배송 시작" (자동 반응)
  [분홍] External System - 외부 시스템 (PG, 택배사 API)
  [빨강] Hotspot         - 의문/갈등/위험 요소
  [초록] Read Model      - 조회 화면/뷰

워크숍 흐름:
  1. Chaotic Exploration    → 도메인 이벤트를 자유롭게 나열
  2. Enforce Timeline       → 시간순으로 정렬, 누락 이벤트 발견
  3. Identify Pivotal Events→ 프로세스 전환점 식별 (경계 후보)
  4. Add Commands & Actors  → 이벤트를 트리거하는 명령과 행위자
  5. Identify Aggregates    → Command + Event 클러스터링
  6. Discover Bounded Contexts → Aggregate 그룹 → 서비스 경계

결과물 흐름:
  Event Storming 보드 → Bounded Context 도출 → Context Map → API 계약 → 구현
```

---

## 패키지 구조 (Hexagonal Architecture)

Hexagonal Architecture(Ports & Adapters)는 도메인 로직을
인프라/프레임워크로부터 격리하여 테스트 용이성과 유연성을 확보한다.

```
com.example.order/                     # Bounded Context: Order
├── domain/                            # 핵심 도메인 (프레임워크 무의존)
│   ├── model/                         # Aggregate Root, Entity, VO, Event
│   │   ├── Order.java                 # Aggregate Root
│   │   ├── OrderLineItem.java         # Entity
│   │   ├── Money.java                 # Value Object
│   │   └── OrderCreatedEvent.java     # Domain Event
│   ├── repository/
│   │   └── OrderRepository.java       # Port (인터페이스)
│   └── service/
│       └── OrderPricingService.java   # Domain Service
├── application/                       # 유스케이스 조율 계층
│   ├── port/
│   │   ├── in/                        # Inbound Port (유스케이스 인터페이스)
│   │   │   └── PlaceOrderUseCase.java
│   │   └── out/                       # Outbound Port
│   │       └── PaymentPort.java       # 외부 시스템 호출 포트
│   ├── service/
│   │   └── PlaceOrderService.java     # Inbound Port 구현
│   └── dto/
│       └── PlaceOrderCommand.java
├── infrastructure/                    # 인프라 어댑터 (프레임워크 의존)
│   ├── persistence/                   # Outbound Adapter (DB)
│   │   ├── JpaOrderRepository.java
│   │   └── OrderRepositoryImpl.java
│   ├── messaging/                     # Outbound Adapter (메시징)
│   │   └── KafkaOrderEventPublisher.java
│   └── external/                      # Outbound Adapter (외부 API)
│       └── PaymentGatewayAdapter.java
└── interfaces/                        # Inbound Adapter (외부 → 내부)
    ├── rest/
    │   └── OrderController.java
    └── consumer/
        └── PaymentEventConsumer.java  # Kafka Consumer

의존성 방향 (핵심 규칙):
  interfaces/ ──> application/ ──> domain/
  infrastructure/ ──> domain/
  domain은 어떤 외부 계층도 알지 못한다 (순수 Java)
  infrastructure가 Port를 구현한다 (DI로 주입)
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Anemic Domain Model | getter/setter만 보유, 로직이 Service에 분산 | 비즈니스 로직을 Aggregate Root에 캡슐화 |
| Distributed Monolith | 서비스 분리했지만 강결합, 동시 배포 필수 | Bounded Context 기반 재설계, ACL 적용 |
| 공유 DB 사용 | 서비스 간 스키마 결합, 독립 배포 불가 | Database per Service + Domain Event 동기화 |
| 과도한 서비스 분리 | 서비스 폭증, 통신 오버헤드 증가 | 작게 시작, 점진적 분리, Modular Monolith 우선 |
| Aggregate 간 객체 참조 | 트랜잭션 범위 확장, 잠금 경합 | ID 참조로 변경, Domain Event로 전파 |
| 도메인 전문가 배제 | 기술 중심 모델링, 비즈니스 요구 미반영 | Event Storming에 도메인 전문가 필수 참여 |
| Ubiquitous Language 무시 | 같은 용어가 다른 의미, 코드-비즈니스 괴리 | Context별 언어 사전 관리, 코드에 도메인 용어 반영 |
| Fat Aggregate | 하나의 Aggregate에 너무 많은 Entity | 불변식 단위로 분리, 결과적 일관성 활용 |
| CRUD 중심 Repository | findByXAndYAndZ 범람, 도메인 의미 부재 | 도메인 의미 담은 메서드명 (findPendingOrders) |
| Context Map 없이 통합 | 서비스 간 암묵적 결합, 장애 전파 | Context Map 작성 후 ACL/OHS 전략 선택 |

---

## 체크리스트

### 분석 단계
- [ ] 도메인 전문가와 Event Storming 워크숍을 수행했는가?
- [ ] Core / Supporting / Generic 도메인을 분류했는가?
- [ ] Bounded Context를 식별하고 Ubiquitous Language를 정의했는가?
- [ ] Context Map으로 서비스 간 관계를 명시했는가?
- [ ] 팀 구조가 서비스 경계와 정렬(Conway's Law)되어 있는가?

### 설계 단계
- [ ] Aggregate Root와 불변식(invariant)을 정의했는가?
- [ ] Aggregate 간 참조를 ID 기반으로 설계했는가?
- [ ] Entity와 Value Object를 명확히 구분했는가?
- [ ] Domain Event를 식별하고 발행/수신 흐름을 설계했는가?
- [ ] Application Service vs Domain Service 역할이 분리되었는가?
- [ ] Hexagonal Architecture 패키지 구조를 적용했는가?

### 구현 단계
- [ ] Domain 계층에 프레임워크 의존성이 없는가?
- [ ] Aggregate Root에 비즈니스 로직이 캡슐화되었는가?
- [ ] Repository는 도메인 인터페이스와 인프라 구현이 분리되었는가?
- [ ] Domain Event가 Transactional Outbox로 안전하게 발행되는가?
- [ ] @TransactionalEventListener로 내부/외부 이벤트를 구분하는가?
- [ ] Value Object가 불변(immutable)으로 구현되었는가?

## 참조 스킬

- `/architecture:msa-saga` - Saga 패턴 (Choreography/Orchestration)
- `/architecture:msa-cqrs-eventsourcing` - CQRS, Event Sourcing 패턴
- `/architecture:msa-event-driven` - 이벤트 드리븐 아키텍처, Outbox 패턴
- `/java:spring-data` - Spring Data JPA, Repository 패턴
- `/messaging:kafka-patterns` - Kafka Producer/Consumer 구현
- `/architecture:api-design` - API 설계 (Open Host Service 구현)
