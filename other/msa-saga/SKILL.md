---
name: msa-saga
description: "Saga 패턴 — Choreography vs Orchestration, 보상 트랜잭션, 실패 처리. Use when 여러 서비스에 걸친 분산 트랜잭션의 일관성과 롤백(compensation)을 설계할 때."
---

# Saga 패턴 가이드

분산 트랜잭션의 일관성을 보장하는 Saga 패턴 구현 전략 (Choreography, Orchestration, Compensation)

## Quick Reference (결정 트리)

```
분산 트랜잭션이 필요한가?
    │
    ├─ 서비스 2~3개, 단순 흐름 ──────> Choreography Saga
    │    └─ Kafka/RabbitMQ 이벤트 기반
    ├─ 서비스 4개+, 복잡한 흐름 ─────> Orchestration Saga
    │    ├─ 장기 실행 워크플로우 ─────> Temporal.io (권장)
    │    ├─ Spring 생태계 선호 ──────> Spring State Machine
    │    └─ 경량 프레임워크 ─────────> Axon Saga / Eventuate
    └─ 하이브리드 ──────────────────> 단순: Choreography + 복잡: Orchestration

보상 트랜잭션 유형?
    ├─ 되돌릴 수 있는 작업 ──────────> Compensable Transaction
    ├─ 되돌릴 수 없는 작업 ──────────> Pivot Transaction (no-return 지점)
    └─ 반드시 성공해야 하는 작업 ────> Retryable Transaction
```

---

## CRITICAL: Choreography vs Orchestration 비교

| 항목 | Choreography | Orchestration |
|------|-------------|---------------|
| **제어 방식** | 분산형 (이벤트 기반) | 중앙 집중형 (오케스트레이터) |
| **결합도** | 느슨한 결합 | 오케스트레이터에 의존 |
| **복잡성** | 참여자 증가 시 급격히 증가 | 중앙에서 관리 가능 |
| **확장성** | 높음 (병목 없음) | 오케스트레이터 성능에 의존 |
| **디버깅** | 어려움 (분산 추적 필요) | 용이 (중앙 로그/대시보드) |
| **SPOF** | 없음 | 오케스트레이터가 SPOF |
| **적합 사례** | 단순 흐름, 독립 팀 | 복잡 워크플로우, 롤백 필요 |
| **프레임워크** | Kafka + Spring Event | Temporal, Axon, Camunda |

---

## Choreography Saga

### 아키텍처

```
┌──────────┐  OrderCreated  ┌──────────┐  PaymentDone  ┌──────────┐
│  Order   │───────────────>│ Payment  │──────────────>│  Stock   │
│ Service  │<───────────────│ Service  │<──────────────│ Service  │
└──────────┘ PaymentFailed  └──────────┘  StockFailed  └──────────┘
  [Order DB]   (보상 트리거)  [Payment DB]  (보상 트리거)  [Stock DB]
  ※ Kafka Topic 기반 이벤트 발행/구독, 실패 시 역방향 보상 전파
```

### Spring Boot + Kafka 구현

```java
// === 이벤트 정의 ===
public sealed interface OrderEvent {
    record OrderCreated(String orderId, String customerId,
            List<OrderItem> items, BigDecimal totalAmount) implements OrderEvent {}
    record OrderCancelled(String orderId, String reason) implements OrderEvent {}
}
public sealed interface PaymentEvent {
    record PaymentCompleted(String orderId, String paymentId,
            BigDecimal amount) implements PaymentEvent {}
    record PaymentFailed(String orderId, String reason) implements PaymentEvent {}
    record PaymentRefunded(String orderId, String paymentId) implements PaymentEvent {}
}

// === Order Service - Saga 시작 + 보상 수신 ===
@Service
@RequiredArgsConstructor
public class OrderService {
    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;
    private final OrderRepository orderRepository;

    @Transactional
    public Order createOrder(CreateOrderRequest request) {
        Order order = Order.builder()
            .id(UUID.randomUUID().toString())
            .customerId(request.customerId())
            .status(OrderStatus.PENDING).build();
        orderRepository.save(order);
        // Saga 시작: 이벤트 발행
        kafkaTemplate.send("order-events", order.getId(),
            new OrderEvent.OrderCreated(order.getId(),
                order.getCustomerId(), request.items(), request.totalAmount()));
        return order;
    }

    @KafkaListener(topics = "payment-events", groupId = "order-service")
    public void handlePaymentEvent(ConsumerRecord<String, PaymentEvent> record) {
        switch (record.value()) {
            case PaymentEvent.PaymentCompleted e ->
                orderRepository.updateStatus(e.orderId(), OrderStatus.CONFIRMED);
            case PaymentEvent.PaymentFailed e -> {
                orderRepository.updateStatus(e.orderId(), OrderStatus.CANCELLED);
                log.warn("주문 {} 취소 - 사유: {}", e.orderId(), e.reason());
            }
            case PaymentEvent.PaymentRefunded e ->
                orderRepository.updateStatus(e.orderId(), OrderStatus.REFUNDED);
        }
    }
}

// === Payment Service - 이벤트 수신 + 보상 ===
@Service
@RequiredArgsConstructor
public class PaymentService {
    private final KafkaTemplate<String, PaymentEvent> kafkaTemplate;
    private final PaymentRepository paymentRepository;
    private final IdempotencyStore idempotencyStore;

    @KafkaListener(topics = "order-events", groupId = "payment-service")
    public void handleOrderCreated(ConsumerRecord<String, OrderEvent> record) {
        if (!(record.value() instanceof OrderEvent.OrderCreated evt)) return;
        // Idempotency: 중복 처리 방지
        if (idempotencyStore.exists("payment:" + evt.orderId())) return;
        try {
            Payment payment = processPayment(evt);
            idempotencyStore.save("payment:" + evt.orderId());
            kafkaTemplate.send("payment-events", evt.orderId(),
                new PaymentEvent.PaymentCompleted(evt.orderId(), payment.getId(), evt.totalAmount()));
        } catch (InsufficientFundsException e) {
            kafkaTemplate.send("payment-events", evt.orderId(),
                new PaymentEvent.PaymentFailed(evt.orderId(), e.getMessage()));
        }
    }

    // Stock 실패 시 보상: 결제 환불
    @KafkaListener(topics = "stock-events", groupId = "payment-service")
    public void handleStockFailed(ConsumerRecord<String, StockEvent> record) {
        if (!(record.value() instanceof StockEvent.StockReservationFailed evt)) return;
        Payment payment = paymentRepository.findByOrderId(evt.orderId());
        if (payment != null) {
            payment.refund();
            paymentRepository.save(payment);
            kafkaTemplate.send("payment-events", evt.orderId(),
                new PaymentEvent.PaymentRefunded(evt.orderId(), payment.getId()));
        }
    }
}
```

---

## Orchestration Saga

### 아키텍처

```
                ┌─────────────────────┐
                │   Saga Orchestrator  │
                │  (Temporal / Axon)   │
                └──────┬──────────────┘
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
 ┌──────────┐   ┌──────────┐   ┌──────────┐
 │  Order   │   │ Payment  │   │  Stock   │
 │ Service  │   │ Service  │   │ Service  │
 └──────────┘   └──────────┘   └──────────┘
 성공: Order 생성 → Payment → Stock → 완료
 실패: Stock X → Payment 환불 → Order 취소 (역순 보상)
```

### Temporal.io 구현 (권장)

```java
// === Workflow + Activity 인터페이스 ===
@WorkflowInterface
public interface OrderSagaWorkflow {
    @WorkflowMethod
    OrderResult processOrder(OrderRequest request);
}

@ActivityInterface
public interface OrderActivities {
    String createOrder(OrderRequest request);       // 정방향
    String processPayment(String orderId, BigDecimal amount);
    String reserveStock(String orderId, List<OrderItem> items);
    void cancelOrder(String orderId);               // 보상
    void refundPayment(String orderId, String paymentId);
    void releaseStock(String orderId, String reservationId);
}

// === Workflow 구현 (핵심: Saga 보상 로직) ===
public class OrderSagaWorkflowImpl implements OrderSagaWorkflow {
    private final OrderActivities activities = Workflow.newActivityStub(
        OrderActivities.class, ActivityOptions.newBuilder()
            .setStartToCloseTimeout(Duration.ofSeconds(30))
            .setRetryOptions(RetryOptions.newBuilder()
                .setInitialInterval(Duration.ofSeconds(1))
                .setBackoffCoefficient(2.0)
                .setMaximumAttempts(3).build())
            .build());

    @Override
    public OrderResult processOrder(OrderRequest request) {
        Saga saga = new Saga(new Saga.Options.Builder()
            .setParallelCompensation(false).build());
        try {
            // Step 1: 주문 생성 → 보상 등록
            String orderId = activities.createOrder(request);
            saga.addCompensation(activities::cancelOrder, orderId);
            // Step 2: 결제 → 보상 등록
            String paymentId = activities.processPayment(orderId, request.getTotalAmount());
            saga.addCompensation(activities::refundPayment, orderId, paymentId);
            // Step 3: 재고 예약 → 보상 등록
            String reservationId = activities.reserveStock(orderId, request.getItems());
            saga.addCompensation(activities::releaseStock, orderId, reservationId);
            return new OrderResult(orderId, "COMPLETED");
        } catch (ActivityFailure e) {
            saga.compensate(); // 실패 시 역순 보상 자동 실행
            return new OrderResult(null, "FAILED: " + e.getMessage());
        }
    }
}

// === Activity 구현 (모든 보상은 Idempotent) ===
@Component
public class OrderActivitiesImpl implements OrderActivities {
    @Override
    public void cancelOrder(String orderId) {
        orderRepository.findById(orderId).ifPresent(order -> {
            if (order.getStatus() != OrderStatus.CANCELLED) {
                order.setStatus(OrderStatus.CANCELLED);
                orderRepository.save(order);
            }
        });
    }
    @Override
    public void refundPayment(String orderId, String paymentId) {
        paymentGateway.refundIfNotAlreadyRefunded(paymentId); // Idempotent
    }
    // ... createOrder, processPayment, reserveStock, releaseStock 구현
}

// === Worker 등록 (Spring Boot) ===
@Configuration
public class TemporalConfig {
    @Bean
    public WorkerFactory workerFactory(WorkflowClient client, OrderActivities act) {
        WorkerFactory factory = WorkerFactory.newInstance(client);
        Worker worker = factory.newWorker("order-saga-queue");
        worker.registerWorkflowImplementationTypes(OrderSagaWorkflowImpl.class);
        worker.registerActivitiesImplementations(act);
        factory.start();
        return factory;
    }
}
```

### Temporal 결정성(Determinism) 제약

Workflow 코드는 재생(replay) 가능해야 한다. 아래를 쓰면 재생 시 다른 결과가 나와 워크플로가 깨진다.

```
금지: time.Now()          -> 대안: workflow.Now()
금지: rand.Int()          -> 대안: workflow.SideEffect()
금지: go func()           -> 대안: workflow.Go()
금지: 네트워크/파일 I/O    -> 대안: Activity 로 위임
금지: uuid.New()          -> 대안: workflow.SideEffect()
```

### Temporal Retry Policy

```go
activityOpts := workflow.ActivityOptions{
    StartToCloseTimeout: 30 * time.Second,
    RetryPolicy: &temporal.RetryPolicy{
        InitialInterval:    1 * time.Second,
        BackoffCoefficient: 2.0,
        MaximumInterval:    120 * time.Second,
        MaximumAttempts:    50,
        NonRetryableErrorTypes: []string{"InvalidInputError", "FraudDetectedError"},
    },
}
ctx = workflow.WithActivityOptions(ctx, activityOpts)
```

| 파라미터 | 권장 값 | 설명 |
|---------|--------|------|
| `InitialInterval` | 1s | 첫 재시도 대기 |
| `BackoffCoefficient` | 2.0 | 지수 백오프 계수 |
| `MaximumInterval` | 60~120s | 대기 상한 |
| `MaximumAttempts` | 0(무제한) 또는 50+ | 관대하게 설정 |

### Workflow Versioning

실행 중인 워크플로가 있는 상태에서 코드를 바꾸면 결정성이 깨진다. 반드시 버전 분기를 넣는다.

```go
func OrderWorkflow(ctx workflow.Context, order Order) error {
    v := workflow.GetVersion(ctx, "add-fraud-check", workflow.DefaultVersion, 1)
    if v == 1 {
        // 새 버전: 사기 탐지 Activity 추가
        err := workflow.ExecuteActivity(ctx, FraudCheckActivity, order).Get(ctx, nil)
        if err != nil { return err }
    }
    return workflow.ExecuteActivity(ctx, ProcessPaymentActivity, order).Get(ctx, nil)
}
```

| 방법 | 적합 시점 |
|------|----------|
| `GetVersion` / Patching | 소규모 변경, 점진적 마이그레이션 |
| Worker Versioning | 대규모 변경, 완전 분리 필요 |
| Task Queue 분리 | 완전 격리, A/B 테스트 |

> ⚠️ 실험적 Worker Versioning(2025 이전 API)은 Temporal Server 2026-03 제거 예정 — 신규 도입 금지. ⚠️ unverified: 2026-08-24 시점 재확인 안 함, Temporal 공식 릴리스 노트로 검증 필요.


### Spring State Machine 예시 (간단)

```java
public enum SagaState { ORDER_CREATED, PAYMENT_PROCESSING, STOCK_RESERVING, COMPLETED, COMPENSATING, FAILED }
public enum SagaEvent { PROCESS_PAYMENT, PAYMENT_SUCCESS, PAYMENT_FAIL, STOCK_SUCCESS, STOCK_FAIL }

@Configuration @EnableStateMachineFactory
public class OrderSagaSMConfig extends StateMachineConfigurerAdapter<SagaState, SagaEvent> {
    @Override
    public void configure(StateMachineTransitionConfigurer<SagaState, SagaEvent> t) throws Exception {
        t.withExternal().source(SagaState.ORDER_CREATED).target(SagaState.PAYMENT_PROCESSING).event(SagaEvent.PROCESS_PAYMENT)
         .and().withExternal().source(SagaState.PAYMENT_PROCESSING).target(SagaState.STOCK_RESERVING).event(SagaEvent.PAYMENT_SUCCESS)
         .and().withExternal().source(SagaState.STOCK_RESERVING).target(SagaState.COMPLETED).event(SagaEvent.STOCK_SUCCESS)
         .and().withExternal().source(SagaState.PAYMENT_PROCESSING).target(SagaState.FAILED).event(SagaEvent.PAYMENT_FAIL)
         .and().withExternal().source(SagaState.STOCK_RESERVING).target(SagaState.COMPENSATING)
               .event(SagaEvent.STOCK_FAIL).action(ctx -> compensatePayment(ctx));
    }
}
```

---

## 보상 트랜잭션 (Compensation)

### 트랜잭션 유형 및 Isolation 대응책

| 유형 | 설명 | 예시 |
|------|------|------|
| **Compensable** | 되돌릴 수 있는 트랜잭션 | 주문 생성, 결제 승인 |
| **Pivot** | 되돌릴 수 없는 분기점 | 결제 확정 (capture) |
| **Retryable** | 반드시 성공해야 하는 트랜잭션 | 알림 발송, 로그 기록 |

| Countermeasure | 설명 | 예시 |
|----------------|------|------|
| **Semantic Lock** | 앱 레벨 잠금으로 진행 중 표시 | `status=APPROVAL_PENDING` |
| **Commutative Updates** | 순서 무관 동일 결과 보장 | 잔액을 절대값 대신 델타로 |
| **Pessimistic View** | Dirty Read 방지 위한 순서 조정 | compensable을 retryable 뒤로 |
| **Reread Value** | 업데이트 전 데이터 변경 재확인 | Optimistic Lock (version 필드) |
| **Version File** | 작업 기록으로 순서 재정렬 | 비순차 요청을 올바른 순서로 실행 |
| **By Value** | 비즈니스 위험도별 동시성 전략 | 고위험: 분산 트랜잭션, 저위험: Saga |

### 보상 흐름 예시: 주문 Saga

```
[정상] 주문생성(C) ──> 결제승인(C) ──> 재고예약(P) ──> 배송요청(R) ──> 완료

[재고예약 실패 시 - 역순 보상]
  재고예약 실패! → 결제환불(cancelPayment) → 주문취소(cancelOrder) → FAILED
  (C)=Compensable  (P)=Pivot  (R)=Retryable
```

---

## CRITICAL: Saga 실패 처리

### Dead Letter Queue + 재시도

```java
// Kafka DLQ 설정 - 3회 재시도 후 DLQ 전송
@Configuration
public class KafkaDlqConfig {
    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, Object>
            kafkaListenerContainerFactory(ConsumerFactory<String, Object> cf,
                                          KafkaTemplate<String, Object> template) {
        var factory = new ConcurrentKafkaListenerContainerFactory<String, Object>();
        factory.setConsumerFactory(cf);
        var recoverer = new DeadLetterPublishingRecoverer(template,
            (record, ex) -> new TopicPartition(record.topic() + ".DLQ", record.partition()));
        factory.setCommonErrorHandler(new DefaultErrorHandler(recoverer, new FixedBackOff(1000L, 3L)));
        return factory;
    }
}

// Exponential Backoff 재시도 (Spring Retry)
@Retryable(retryFor = TransientException.class, maxAttempts = 5,
    backoff = @Backoff(delay = 1000, multiplier = 2.0, maxDelay = 30000))
public void executeWithRetry(SagaStep step) { step.execute(); }

@Recover
public void handleMaxRetryExceeded(TransientException e, SagaStep step) {
    log.error("최대 재시도 초과 - step: {}", step.getName(), e);
    sagaStateStore.markAsFailed(step.getSagaId(), step.getName());
    dlqPublisher.publish(step);
}
```

### Idempotency 보장

```java
// Redis 기반 Idempotency Guard
@Component
public class IdempotencyGuard {
    private final RedisTemplate<String, String> redis;
    private static final Duration TTL = Duration.ofHours(24);

    public boolean executeOnce(String key, Runnable action) {
        Boolean isNew = redis.opsForValue().setIfAbsent(key, "PROCESSING", TTL);
        if (Boolean.FALSE.equals(isNew)) return false; // 중복 스킵
        try {
            action.run();
            redis.opsForValue().set(key, "COMPLETED", TTL);
            return true;
        } catch (Exception e) {
            redis.delete(key); // 실패 시 재시도 허용
            throw e;
        }
    }
}
```

#### 멱등성 키 생성 전략

| 전략 | 생성 방식 | 적합 시점 |
|------|----------|----------|
| Workflow ID + Activity | `order-123:process-payment` | Temporal 기본 전략 |
| 비즈니스 키 조합 | `order:{id}:payment:{attempt}` | 비즈니스 의미 명확 |
| 클라이언트 UUID | 클라이언트가 요청마다 UUID | API Gateway 레벨 |
| 해시 기반 | `SHA256(요청 본문)` | 동일 내용 기반 탐지 |

#### Deduplication 테이블 (영속 필요 시)

Redis Guard 는 TTL 만료·플러시로 유실될 수 있다. 결제처럼 재실행이 치명적인 경로는 DB 에 남긴다.

```sql
CREATE TABLE idempotency_keys (
    idempotency_key VARCHAR(255) PRIMARY KEY,
    response_body   JSONB NOT NULL,
    status          VARCHAR(20) NOT NULL,  -- processing / completed / failed
    created_at      TIMESTAMP DEFAULT NOW(),
    expires_at      TIMESTAMP DEFAULT NOW() + INTERVAL '24 hours'
);
CREATE INDEX idx_idempotency_expires ON idempotency_keys(expires_at);
```


### Temporal Search Attributes (운영 조회)

Saga 를 Order/Customer 단위로 찾으려면 Search Attribute 를 올려야 한다 — 안 올리면 Web UI 에서 workflow ID 로만 찾을 수 있다.

```go
func OrderSagaWorkflow(ctx workflow.Context, order Order) error {
    _ = workflow.UpsertSearchAttributes(ctx, map[string]interface{}{
        "OrderID": order.ID, "CustomerID": order.CustomerID, "SagaStatus": "STARTED",
    })
    // ... Saga 로직 ...
    _ = workflow.UpsertSearchAttributes(ctx, map[string]interface{}{"SagaStatus": "COMPLETED"})
    return nil
}
```

### Saga 상태 추적

```java
@Entity @Table(name = "saga_state")
public class SagaStateEntity {
    @Id private String sagaId;
    private String sagaType;           // e.g., "ORDER_SAGA"
    @Enumerated(EnumType.STRING)
    private SagaStatus status;         // STARTED, COMPENSATING, COMPLETED, FAILED
    private String currentStep;
    private int completedSteps;
    private String failureReason;
    @Column(columnDefinition = "JSON")
    private String stepHistory;        // 각 단계 실행 기록
    private Instant startedAt;
    private Instant completedAt;
}
```

---

## Kubernetes에서의 Saga

### Temporal on K8s (Helm)

```bash
helm repo add temporal https://go.temporal.io/helm-charts && helm repo update
helm install temporal temporal/temporal \
  --namespace temporal-system --create-namespace \
  --set server.replicaCount=3 \
  --set prometheus.enabled=true \
  --set grafana.enabled=true \
  --set web.enabled=true
# Web UI: kubectl port-forward svc/temporal-web 8080:8080 -n temporal-system
```

### KEDA + Saga Worker 오토스케일링

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: saga-worker-scaler
spec:
  scaleTargetRef:
    name: saga-worker-deployment
  minReplicaCount: 1
  maxReplicaCount: 10
  triggers:
    - type: kafka
      metadata:
        bootstrapServers: kafka:9092
        consumerGroup: saga-worker
        topic: order-events
        lagThreshold: "50"
```

### Prometheus Alert

```yaml
groups:
  - name: saga-alerts
    rules:
      - alert: SagaFailureRateHigh
        expr: rate(saga_executions_total{status="FAILED"}[5m]) / rate(saga_executions_total[5m]) > 0.05
        for: 3m
        annotations:
          summary: "Saga 실패율 5% 초과"
      - alert: SagaCompensationTimeout
        expr: saga_compensation_duration_seconds > 60
        for: 1m
        annotations:
          summary: "보상 트랜잭션 60초 초과"
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 보상 로직 누락 | 데이터 불일치 영구 발생 | 모든 Compensable 단계에 보상 필수 구현 |
| 비-Idempotent 보상 | 재시도 시 이중 환불 등 부작용 | 모든 보상은 Idempotent로 설계 |
| 보상 순서 무시 | 참조 무결성 위반 | 반드시 역순으로 보상 실행 |
| 되돌릴 수 없는 작업 간과 | 이메일/외부 API 보상 불가 | Pivot Transaction으로 분류 |
| 타임아웃 미설정 | Saga 무한 대기 | 각 단계 timeout + circuit breaker |
| Semantic Lock 미적용 | Dirty Read 데이터 오염 | PENDING/PROCESSING 중간 상태 활용 |
| 단일 DB에서 Saga 사용 | 불필요한 복잡성 | 단일 DB면 로컬 트랜잭션 사용 |
| 모니터링 없는 Saga | 실패 감지 불가 | 상태 추적 + DLQ 알림 필수 |

---

## 체크리스트

### 설계
- [ ] 서비스 간 데이터 일관성 요구사항 분석
- [ ] Choreography vs Orchestration 방식 결정
- [ ] 각 단계 트랜잭션 유형 분류 (Compensable / Pivot / Retryable)
- [ ] 모든 Compensable 단계에 보상 트랜잭션 설계
- [ ] Semantic Lock 등 isolation 대응책 선택

### 구현
- [ ] 모든 이벤트/명령에 Idempotency Key 적용
- [ ] 보상 트랜잭션 역순 실행 구현
- [ ] Dead Letter Queue 설정 + 모니터링
- [ ] Exponential Backoff 재시도 정책
- [ ] Saga 상태 추적 테이블 또는 워크플로우 엔진

### 운영
- [ ] Saga 실패율 Prometheus Alert 설정
- [ ] DLQ 수동 재처리 프로세스 정의
- [ ] Distributed Tracing (Jaeger/Zipkin) 연동
- [ ] 동시 Saga 실행 부하 테스트
- [ ] 장애 시뮬레이션 (Chaos Engineering)

## 참조 스킬

- `/messaging:kafka-patterns` - Kafka Producer/Consumer, Exactly-Once 처리
- `/architecture:distributed-lock` - 분산 락 (Semantic Lock 구현 시 참고)
- `/observability:observability-otel` - OpenTelemetry 기반 Saga 추적
- `/cicd:deployment-strategies` - 무중단 배포 (Saga Worker 배포)
- `/k8s:k8s-helm` - Helm Chart 관리 (Temporal 배포)
- `/java:spring-data` - Spring Data JPA (Saga 상태 테이블)

## 참고 레퍼런스

- [Saga_Pattern_with_NATS_Go](https://github.com/ChikenduHillary/Saga_Pattern_with_NATS_Go) -- Go + NATS JetStream Saga
- [saga-example](https://github.com/minghsu0107/saga-example) -- Go Orchestration Saga
- [eventuate-tram-sagas](https://github.com/eventuate-tram/eventuate-tram-sagas-examples-customers-and-orders) -- Spring Orchestration Saga
- [saga-orchestration](https://github.com/semotpan/saga-orchestration) -- Spring Outbox + CDC + Debezium
- [Temporal Saga Mastery](https://temporal.io/blog/mastering-saga-patterns-for-distributed-transactions-in-microservices)
