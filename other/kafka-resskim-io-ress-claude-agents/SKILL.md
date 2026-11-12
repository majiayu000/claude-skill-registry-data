---
name: kafka
description: "Apache Kafka 기초 — 클러스터 개념, 토픽·파티션 전략, Strimzi Operator 설치. Use when Kafka 를 처음 도입하거나 파티션 설계 등 기본 개념을 잡을 때, 고급·Connect·Streams 는 kafka- 접두 skill 사용."
---

# Apache Kafka 가이드

Kafka 클러스터, Strimzi Operator, 핵심 개념

## Quick Reference (결정 트리)

```
Kafka 배포 방식?
    │
    ├─ 관리형 서비스 ────> Amazon MSK / Confluent Cloud
    ├─ K8s 운영 ─────────> Strimzi Operator (추천)
    └─ VM 직접 운영 ────> Confluent Platform

Consumer 스케일링?
    │
    ├─ K8s 환경 ─────────> KEDA + Kafka Scaler
    └─ 일반 환경 ────────> Consumer Group 수동 관리

파티션 수?
    │
    ├─ 예상 처리량 / Consumer당 처리량
    └─ 최소: Consumer 수 이상
```

---

## CRITICAL: Kafka 개념

```
┌─────────────────────────────────────────────────────────────┐
│                    Kafka Architecture                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Producer ──────────────────────────────> Topic             │
│                                             │                │
│                                   ┌─────────┼─────────┐     │
│                                   │    Partitions     │     │
│                                   │  [P0] [P1] [P2]   │     │
│                                   └─────────┼─────────┘     │
│                                             │                │
│                                   ┌─────────┼─────────┐     │
│                                   │  Consumer Group   │     │
│                                   │  [C0] [C1] [C2]   │     │
│                                   └───────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘

파티션 : Consumer = 1:1 (최대 효율)
파티션 > Consumer: 일부 Consumer가 여러 파티션 처리
파티션 < Consumer: 일부 Consumer가 유휴 상태
```

### 핵심 개념

| 개념 | 설명 |
|------|------|
| **Topic** | 메시지 카테고리 |
| **Partition** | 토픽의 병렬 처리 단위 |
| **Offset** | 파티션 내 메시지 위치 |
| **Consumer Group** | 메시지를 분산 처리하는 Consumer 집합 |
| **Replication Factor** | 파티션 복제 수 (HA) |
| **ISR** | In-Sync Replicas (동기화된 복제본) |

---

## Strimzi (Kubernetes Operator)

### 설치

```bash
# Strimzi Operator 설치
kubectl create namespace kafka
kubectl apply -f https://strimzi.io/install/latest?namespace=kafka -n kafka
```

### Kafka 클러스터

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
  namespace: kafka
spec:
  kafka:
    version: 3.6.0
    replicas: 3
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      default.replication.factor: 3
      min.insync.replicas: 2
      inter.broker.protocol.version: "3.6"
    storage:
      type: jbod
      volumes:
        - id: 0
          type: persistent-claim
          size: 100Gi
          class: gp3
          deleteClaim: false
    resources:
      requests:
        memory: 4Gi
        cpu: "1"
      limits:
        memory: 8Gi
        cpu: "2"

  zookeeper:
    replicas: 3
    storage:
      type: persistent-claim
      size: 10Gi
      class: gp3
    resources:
      requests:
        memory: 1Gi
        cpu: "500m"

  entityOperator:
    topicOperator: {}
    userOperator: {}
```

### Topic 생성

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: orders
  namespace: kafka
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 12
  replicas: 3
  config:
    retention.ms: 604800000  # 7일
    segment.bytes: 1073741824
    min.insync.replicas: 2
```

---

## 파티션 전략

### 파티션 수 결정

```
파티션 수 = max(예상 처리량 / Consumer당 처리량, Consumer 수)

예시:
- 예상 처리량: 10,000 msg/s
- Consumer당 처리량: 1,000 msg/s
- 파티션 수 = 10,000 / 1,000 = 10 (최소)
- 여유분 포함: 12개 권장
```

### 파티션 키 전략

| 전략 | 용도 | 예시 |
|------|------|------|
| **사용자 ID** | 사용자별 순서 보장 | `key=user_123` |
| **주문 ID** | 주문별 순서 보장 | `key=order_456` |
| **Round Robin** | 균등 분산 (키 없음) | `key=null` |
| **지역 기반** | 지역별 처리 | `key=region_kr` |

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| auto.commit=true | 메시지 유실 | 수동 커밋 사용 |
| acks=0/1 | 메시지 유실 | acks=all |
| 파티션 < Consumer | 유휴 Consumer | 파티션 수 조정 |
| 단일 파티션 | 병렬 처리 불가 | 충분한 파티션 |
| 너무 많은 파티션 | 오버헤드 증가 | 적정 수 유지 |
| lag 무시 | 처리 지연 | KEDA + 모니터링 |

---

## 체크리스트

### 클러스터
- [ ] Replication Factor 3 이상
- [ ] min.insync.replicas 2 이상
- [ ] 충분한 파티션 수

### Producer
- [ ] acks=all 설정
- [ ] idempotence 활성화
- [ ] 적절한 배치/압축 설정

### Consumer
- [ ] 수동 오프셋 커밋
- [ ] Consumer Group 설정
- [ ] 에러 핸들링

**관련 skill**: `/messaging:kafka-patterns` (Producer/Consumer 패턴, KEDA), `/k8s:k8s-autoscaling`, `/observability:monitoring-metrics`
