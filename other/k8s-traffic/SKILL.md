---
name: k8s-traffic
description: "인프라 트래픽 제어 허브 — Rate Limiting, Circuit Breaker, Virtual Waiting Room 대기열, 티켓팅 권장 구성. Use when 급증 트래픽을 제어할 방식을 고르고 세부 skill 로 갈라 들어갈 때."
---

# Kubernetes Traffic Control Patterns

인프라 레벨 트래픽 제어 허브: Rate Limiting, Circuit Breaker, 대기열

## Quick Reference

```
트래픽 제어 선택
    │
    ├─ Service Mesh 있음 ───> Istio Rate Limiting
    │   └─ Global/Local 선택
    │
    ├─ Ingress만 사용 ──────> NGINX Ingress annotations
    │
    ├─ API Gateway ─────────> Kong / AWS API Gateway
    │
    └─ 대기열 필요 ─────────> Virtual Waiting Room 패턴
```

---

## 상세 가이드

| 인프라 | Skill | 내용 |
|--------|-------|------|
| Istio | `/service-mesh:k8s-traffic-istio` | Global/Local Rate Limit, Circuit Breaker |
| Ingress | `/k8s:k8s-traffic-ingress` | NGINX Ingress, Kong Rate Limiting |

---

## Virtual Waiting Room (대기열)

티켓팅 시스템의 핵심 패턴:

### 아키텍처

```
┌──────────┐     ┌──────────────┐     ┌──────────┐
│  Client  │────▶│ Waiting Room │────▶│  Ticket  │
└──────────┘     │   (Queue)    │     │   API    │
                 └──────┬───────┘     └──────────┘
                        │
                        ▼
                 ┌──────────────┐
                 │    Redis     │
                 │ Sorted Set   │
                 └──────────────┘
```

### Istio + Redis 기반 구현

```yaml
# 대기열 서비스
apiVersion: apps/v1
kind: Deployment
metadata:
  name: waiting-room
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: waiting-room
        image: waiting-room:latest
        env:
        - name: REDIS_URL
          value: redis:6379
        - name: MAX_CONCURRENT_USERS
          value: "5000"
        - name: TOKEN_TTL_SECONDS
          value: "300"
---
# VirtualService로 대기열 라우팅
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: ticket-with-queue
spec:
  hosts:
  - ticket.example.com
  http:
  # 대기열 토큰 있으면 바로 통과
  - match:
    - headers:
        x-queue-token:
          regex: ".+"
    route:
    - destination:
        host: ticket-api
  # 없으면 대기열로
  - route:
    - destination:
        host: waiting-room
```

### 대기열 상태 응답 헤더

```yaml
# 429 응답에 대기 정보 포함
X-Queue-Position: 1234
X-Queue-Wait-Time: 120s
Retry-After: 30
```

---

## 티켓팅 시스템 권장 구성

```yaml
# 1. Global Rate Limit (전체 시스템 보호)
전체 API: 10,000 req/s

# 2. Endpoint별 Rate Limit
/api/tickets/reserve: 1,000 req/s
/api/tickets/search: 5,000 req/s

# 3. User별 Rate Limit
일반 사용자: 10 req/s
VIP: 50 req/s

# 4. IP별 Rate Limit (봇 방어)
단일 IP: 20 req/s

# 5. Virtual Waiting Room
동시 접속: 5,000명
대기열 용량: 100,000명
토큰 TTL: 5분
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 앱 레벨만 Rate Limit | 인프라 부하 | Istio/Ingress 레벨 추가 |
| 단일 Redis | SPOF | Redis Cluster |
| 고정 Limit만 | 버스트 대응 불가 | Token Bucket 알고리즘 |
| 429만 응답 | UX 나쁨 | 대기열 + 예상 시간 제공 |
| Local만 사용 | 분산 환경 불일치 | Global Rate Limit |

---

## 체크리스트

### Rate Limiting
- [ ] Global Rate Limit 설정
- [ ] Endpoint별 차등 적용
- [ ] User/IP별 제한
- [ ] Redis HA 구성

### 대기열
- [ ] Virtual Waiting Room 구현
- [ ] 대기 순번/예상 시간 제공
- [ ] 토큰 기반 입장 제어

### Circuit Breaker
- [ ] 연결 풀 설정
- [ ] Outlier Detection 설정
- [ ] 장애 시 Fallback

**관련 skill**: `/service-mesh:k8s-traffic-istio`, `/k8s:k8s-traffic-ingress`, `/k8s:k8s-security`, `/k8s:k8s-helm`, `/architecture:distributed-lock`
