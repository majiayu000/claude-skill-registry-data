---
name: rabbitmq
description: "RabbitMQ — Quorum Queues, AMQP 1.0, Exchange 패턴, Publisher Confirms, Dead Letter Exchange, Go·Spring AMQP, KEDA. Use when RabbitMQ 큐 신뢰성 설정이나 DLX 재처리, 클러스터 운영을 구성할 때."
---

# RabbitMQ 가이드

RabbitMQ v4.1 Quorum Queues, AMQP 1.0, Exchange 패턴, Publisher Confirms, DLX, K8s 운영

## Quick Reference (결정 트리)

```
큐 타입 선택?
    ├─ 데이터 안전성 우선 ──────> Quorum Queue (v3.8+, 권장)
    ├─ 극한 저지연 필요 ────────> Classic Queue (미러링 비권장)
    └─ 대용량 스트림 처리 ──────> Stream (Kafka-like, v3.9+)

Exchange 타입?
    ├─ 정확한 라우팅 키 매칭 ──> Direct Exchange
    ├─ 패턴 기반 라우팅 ────────> Topic Exchange (order.*.created)
    ├─ 모든 큐에 브로드캐스트 ──> Fanout Exchange
    └─ 헤더 속성 기반 라우팅 ──> Headers Exchange

프로토콜 선택?
    ├─ 기존 호환성 ─────────────> AMQP 0-9-1 (기본)
    └─ 2x 성능 향상 필요 ──────> AMQP 1.0 (v4.0+, 권장)

K8s 배포?
    ├─ 프로덕션 클러스터 ──────> RabbitMQ Cluster Operator
    └─ Consumer 오토스케일링 ──> KEDA rabbitmq-queue-trigger
```

---

## CRITICAL: RabbitMQ 아키텍처

```
┌──────────────────────────────────────────────────────────────┐
│  Publisher ──> Exchange ──┬── Binding(key)     ──> Queue A   │
│                           ├── Binding(pattern) ──> Queue B   │
│                           └── Binding(#)       ──> Queue C   │
│                                                   │  │  │    │
│                                                   Consumers  │
│  Publisher Confirm  <──────────────────  Broker Ack          │
│  실패 메시지 → DLX → Dead Letter Queue → 재처리/알림        │
└──────────────────────────────────────────────────────────────┘
```

### Quorum Queue vs Classic Queue (v4.1)

| 항목 | Quorum Queue | Classic Queue |
|------|-------------|---------------|
| **복제** | Raft 기반 합의 (자동) | 미러링 (deprecated) |
| **데이터 안전성** | 디스크 우선 저장 | 메모리 우선 |
| **Poison Message** | 자동 감지 (delivery-limit) | 수동 처리 필요 |
| **권장 여부** | **프로덕션 권장** | 임시 큐/저지연 전용 |

### Exchange 타입별 용도

| Exchange | 라우팅 방식 | 용도 | 예시 |
|----------|-----------|------|------|
| **Direct** | routing_key 정확 매칭 | 작업 분배, RPC | `order.payment` |
| **Topic** | 패턴 매칭 (*, #) | 이벤트 라우팅 | `order.*.created` |
| **Fanout** | 모든 바인딩 큐에 전달 | 브로드캐스트/알림 | 시스템 공지 |
| **Headers** | 헤더 속성 매칭 | 복합 조건 라우팅 | `x-match: all` |

### AMQP 1.0 (v4.0+)

```
성능 향상 (vs AMQP 0-9-1): 퍼블리싱/컨슈밍 ~2x 처리량
프로토콜 레벨 flow control 내장, 멀티 프로토콜 상호운용
```

---

## CRITICAL: Publisher Confirms

```
1. channel.confirmSelect()       (Confirm 모드 활성화)
2. channel.basicPublish()        (메시지 발행)
3. basic.ack / basic.nack        (Broker 확인/거부 응답)
동기: waitForConfirms() ← 단순하지만 느림
비동기: addConfirmListener() ← 고처리량 권장
```

## CRITICAL: Dead Letter Exchange (DLX)

```
Main Queue → 실패 시 DLX로 이동:
  - Consumer nack (requeue=false) / TTL 만료 / 최대 길이 초과
  - delivery-limit 초과 (Quorum Queue)
  → DLX → Dead Letter Queue → 재처리/알림
```

---

## Go 구현 (amqp091-go)

### Publisher (Confirm + Quorum Queue + DLX)

```go
package rabbitmq

import (
	"context"
	"encoding/json"
	"fmt"
	"sync"
	"time"
	amqp "github.com/rabbitmq/amqp091-go"
)

type Publisher struct {
	conn     *amqp.Connection
	ch       *amqp.Channel
	confirms chan amqp.Confirmation
	mu       sync.Mutex
}

func NewPublisher(url string) (*Publisher, error) {
	conn, err := amqp.Dial(url)
	if err != nil { return nil, fmt.Errorf("연결 실패: %w", err) }
	ch, err := conn.Channel()
	if err != nil { return nil, fmt.Errorf("채널 생성 실패: %w", err) }
	if err := ch.Confirm(false); err != nil {
		return nil, fmt.Errorf("confirm 모드 활성화 실패: %w", err)
	}
	confirms := ch.NotifyPublish(make(chan amqp.Confirmation, 256))
	// DLX 토폴로지
	ch.ExchangeDeclare("orders.dlx", "direct", true, false, false, false, nil)
	ch.QueueDeclare("orders.dead-letter", true, false, false, false, nil)
	ch.QueueBind("orders.dead-letter", "orders.failed", "orders.dlx", false, nil)
	// 메인 Exchange + Quorum Queue
	ch.ExchangeDeclare("orders", "topic", true, false, false, false, nil)
	ch.QueueDeclare("orders.processing", true, false, false, false, amqp.Table{
		"x-queue-type": "quorum", "x-delivery-limit": int32(3),
		"x-dead-letter-exchange": "orders.dlx", "x-dead-letter-routing-key": "orders.failed",
	})
	ch.QueueBind("orders.processing", "order.#", "orders", false, nil)
	return &Publisher{conn: conn, ch: ch, confirms: confirms}, nil
}

func (p *Publisher) PublishWithConfirm(ctx context.Context, routingKey string, payload any) error {
	p.mu.Lock()
	defer p.mu.Unlock()
	body, _ := json.Marshal(payload)
	if err := p.ch.PublishWithContext(ctx, "orders", routingKey, true, false,
		amqp.Publishing{
			DeliveryMode: amqp.Persistent, ContentType: "application/json",
			Body: body, Timestamp: time.Now(),
			MessageId: fmt.Sprintf("%d", time.Now().UnixNano()),
		}); err != nil {
		return fmt.Errorf("발행 실패: %w", err)
	}
	select {
	case c := <-p.confirms:
		if !c.Ack { return fmt.Errorf("broker 거부: tag=%d", c.DeliveryTag) }
		return nil
	case <-ctx.Done():
		return ctx.Err()
	}
}

func (p *Publisher) Close() { p.ch.Close(); p.conn.Close() }
```

### Consumer (수동 Ack, Graceful Shutdown)

```go
package rabbitmq

import (
	"context"
	"fmt"
	"log"
	amqp "github.com/rabbitmq/amqp091-go"
)

type MessageHandler func(body []byte) error

type Consumer struct {
	conn *amqp.Connection
	ch   *amqp.Channel
}

func NewConsumer(url string, prefetch int) (*Consumer, error) {
	conn, err := amqp.Dial(url)
	if err != nil { return nil, fmt.Errorf("연결 실패: %w", err) }
	ch, err := conn.Channel()
	if err != nil { return nil, fmt.Errorf("채널 생성 실패: %w", err) }
	ch.Qos(prefetch, 0, false)
	return &Consumer{conn: conn, ch: ch}, nil
}

func (c *Consumer) Consume(ctx context.Context, queue string, handler MessageHandler) error {
	msgs, err := c.ch.Consume(queue, "", false, false, false, false, nil)
	if err != nil { return fmt.Errorf("consume 실패: %w", err) }
	for {
		select {
		case <-ctx.Done():
			return nil
		case msg, ok := <-msgs:
			if !ok { return fmt.Errorf("채널 종료") }
			if err := handler(msg.Body); err != nil {
				msg.Nack(false, false) // DLX로 이동
			} else {
				msg.Ack(false)
			}
		}
	}
}

func (c *Consumer) Close() { c.ch.Close(); c.conn.Close() }
```

---

## Spring AMQP 구현

### 설정 (application.yml)

```yaml
spring:
  rabbitmq:
    host: rabbitmq.default
    port: 5672
    username: ${RABBITMQ_USERNAME:guest}
    password: ${RABBITMQ_PASSWORD:guest}
    publisher-confirm-type: correlated
    publisher-returns: true
    listener:
      simple:
        acknowledge-mode: manual
        prefetch: 10
        concurrency: 3
        max-concurrency: 10
        retry: { enabled: true, max-attempts: 3, initial-interval: 1000, multiplier: 2.0 }
```

### Config (Quorum Queue + DLX + Publisher Confirm)

```java
@Configuration
public class RabbitConfig {
    @Bean public TopicExchange orderExchange() { return new TopicExchange("orders"); }
    @Bean public DirectExchange deadLetterExchange() { return new DirectExchange("orders.dlx"); }

    @Bean
    public Queue orderQueue() {
        return QueueBuilder.durable("orders.processing").quorum()
            .deadLetterExchange("orders.dlx").deadLetterRoutingKey("orders.failed")
            .deliveryLimit(3).build();
    }
    @Bean public Queue deadLetterQueue() { return QueueBuilder.durable("orders.dead-letter").build(); }

    @Bean public Binding orderBinding(Queue orderQueue, TopicExchange orderExchange) {
        return BindingBuilder.bind(orderQueue).to(orderExchange).with("order.#");
    }
    @Bean public Binding dlqBinding(Queue deadLetterQueue, DirectExchange dlx) {
        return BindingBuilder.bind(deadLetterQueue).to(dlx).with("orders.failed");
    }

    @Bean
    public RabbitTemplate rabbitTemplate(ConnectionFactory cf) {
        RabbitTemplate t = new RabbitTemplate(cf);
        t.setExchange("orders");
        t.setConfirmCallback((cd, ack, cause) -> { if (!ack) log.error("발행 실패: {}", cause); });
        t.setReturnsCallback(r -> log.warn("메시지 반환: {}", r.getMessage()));
        return t;
    }
    @Bean public Jackson2JsonMessageConverter messageConverter() { return new Jackson2JsonMessageConverter(); }
}
```

### Publisher + Consumer

```java
@Service @RequiredArgsConstructor
public class OrderPublisher {
    private final RabbitTemplate rabbitTemplate;
    public void publishOrderCreated(OrderEvent event) {
        rabbitTemplate.convertAndSend("orders", "order.created", event,
            new CorrelationData(event.getOrderId()));
    }
}

@Service @Slf4j
public class OrderConsumer {
    @RabbitListener(queues = "orders.processing")
    public void handleOrder(OrderEvent event, Channel channel,
                            @Header(AmqpHeaders.DELIVERY_TAG) long tag) {
        try {
            processOrder(event);
            channel.basicAck(tag, false);
        } catch (Exception e) {
            log.error("처리 실패: {}", event.getOrderId(), e);
            channel.basicNack(tag, false, false); // DLX로 이동
        }
    }

    @RabbitListener(queues = "orders.dead-letter")
    public void handleDeadLetter(Message message) {
        log.error("DLQ 메시지: {}", new String(message.getBody()));
    }
}
```

---

## K8s 배포 (RabbitMQ Cluster Operator)

```bash
kubectl apply -f https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml
```

### RabbitmqCluster + Policy

```yaml
apiVersion: rabbitmq.com/v1beta1
kind: RabbitmqCluster
metadata:
  name: rabbitmq-prod
  namespace: rabbitmq
spec:
  replicas: 3
  image: rabbitmq:4.1-management
  resources:
    requests: { cpu: "500m", memory: 1Gi }
    limits: { cpu: "2", memory: 4Gi }
  persistence: { storageClassName: gp3, storage: 50Gi }
  rabbitmq:
    additionalConfig: |
      default_queue_type = quorum
      vm_memory_high_watermark.relative = 0.4
      disk_free_limit.absolute = 2GB
      publisher_confirm_timeout = 30000
      consumer_timeout = 1800000
  tls: { secretName: rabbitmq-tls }
  override:
    statefulSet:
      spec:
        template:
          spec:
            topologySpreadConstraints:
              - maxSkew: 1
                topologyKey: topology.kubernetes.io/zone
                whenUnsatisfiable: DoNotSchedule
                labelSelector:
                  matchLabels: { app.kubernetes.io/name: rabbitmq-prod }
---
apiVersion: rabbitmq.com/v1beta1
kind: Policy
metadata: { name: quorum-queue-policy, namespace: rabbitmq }
spec:
  name: quorum-queue-policy
  vhost: "/"
  pattern: "^orders\\."
  applyTo: queues
  definition: { dead-letter-exchange: orders.dlx, delivery-limit: 3 }
  rabbitmqClusterReference: { name: rabbitmq-prod }
```

---

## KEDA RabbitMQ 오토스케일링

### ScaledObject + TriggerAuthentication

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: order-consumer-scaler
spec:
  scaleTargetRef: { name: order-consumer }
  pollingInterval: 15
  cooldownPeriod: 60
  minReplicaCount: 1
  maxReplicaCount: 10
  advanced:
    restoreToOriginalReplicaCount: true
    horizontalPodAutoscalerConfig:
      behavior:
        scaleDown: { stabilizationWindowSeconds: 120 }
  triggers:
    - type: rabbitmq
      metadata:
        protocol: amqp
        mode: QueueLength
        queueName: orders.processing
        value: "50"  # 큐 길이 50 초과 시 스케일업
      authenticationRef: { name: rabbitmq-trigger-auth }
---
apiVersion: keda.sh/v1alpha1
kind: TriggerAuthentication
metadata: { name: rabbitmq-trigger-auth }
spec:
  secretTargetRef:
    - parameter: host
      name: rabbitmq-secret
      key: connection-string
```

### Consumer Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: order-consumer }
spec:
  replicas: 1
  selector: { matchLabels: { app: order-consumer } }
  template:
    metadata: { labels: { app: order-consumer } }
    spec:
      containers:
        - name: consumer
          image: order-consumer:latest
          env:
            - name: RABBITMQ_URL
              valueFrom: { secretKeyRef: { name: rabbitmq-secret, key: connection-string } }
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits: { cpu: 500m, memory: 512Mi }
          livenessProbe: { httpGet: { path: /healthz, port: 8080 } }
          readinessProbe: { httpGet: { path: /readyz, port: 8080 } }
```

### KEDA 설정 가이드

| 설정 | 권장값 | 이유 |
|------|--------|------|
| **mode** | QueueLength | 큐 길이 기반이 가장 직관적 |
| **value** | 50-100 | 워크로드 처리 속도 기반 |
| **cooldownPeriod** | 60-120초 | 급격한 스케일다운 방지 |
| **minReplicaCount** | 1+ | 0이면 콜드스타트 지연 |

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| auto-ack 사용 | 메시지 유실 위험 | 수동 Ack + prefetch |
| Classic Queue 미러링 | v4.x에서 deprecated | Quorum Queue 사용 |
| Publisher Confirm 미사용 | 발행 실패 감지 불가 | Confirm 모드 활성화 |
| DLX 미설정 | 실패 메시지 무한 재시도 | DLX + delivery-limit |
| prefetch=1 | Consumer 처리량 저하 | prefetch 10-50 |
| 단일 커넥션 다중 쓰레드 | 채널 경합 | 쓰레드당 채널 또는 풀 |
| 큐 이름 하드코딩 | 환경별 관리 어려움 | 설정/CRD로 관리 |
| TTL 없는 큐 | 메모리 폭증 | TTL + max-length |

---

## 체크리스트

### 클러스터
- [ ] Quorum Queue 기본 타입으로 설정
- [ ] 3+ 노드 클러스터 구성
- [ ] 메모리 워터마크 (0.4) + 디스크 최소치 설정
- [ ] TLS 활성화 + topology spread AZ 분산

### Publisher
- [ ] Publisher Confirm 활성화
- [ ] Persistent 메시지 (deliveryMode=2)
- [ ] mandatory 플래그 (라우팅 실패 감지)
- [ ] 재시도 로직 구현

### Consumer
- [ ] 수동 Ack (auto-ack 비활성화)
- [ ] prefetch 적절히 설정 (10-50)
- [ ] Graceful shutdown + 멱등성 보장

### DLX / KEDA
- [ ] DLX + delivery-limit + DLQ 모니터링
- [ ] TriggerAuthentication으로 인증 관리
- [ ] cooldownPeriod + stabilizationWindow 설정
- [ ] minReplicaCount >= 1 (콜드스타트 방지)

**관련 skill**: `/messaging:kafka` (대용량 스트리밍 비교), `/architecture:msa-event-driven` (이벤트 기반 설계), `/k8s:k8s-autoscaling` (KEDA 고급 설정)
