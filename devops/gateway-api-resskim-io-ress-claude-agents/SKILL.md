---
name: gateway-api
description: "Kubernetes Gateway API 개념과 리소스, Envoy Gateway·Kong 설정, Ingress NGINX EOL 대응 결정 트리. Use when Ingress NGINX 종료에 대비해 Gateway API 구현체를 고르고 구성할 때."
---

# Kubernetes Gateway API 가이드

Ingress NGINX 지원 종료 대응: Gateway API, Envoy Gateway, Kong 마이그레이션

## Quick Reference (결정 트리)

```
Gateway API 구현체 선택?
    |
    +-- Envoy 기반 원하는 경우 ------> Envoy Gateway
    |       |
    |       +-- 순수 Gateway API ----> Envoy Gateway (권장)
    |       +-- Istio 연동 ----------> Istio Gateway API mode
    |
    +-- Kong 기존 사용자 ------------> Kong Gateway (KIC 3.x)
    |       |
    |       +-- 플러그인 필요 -------> Kong + Gateway API
    |       +-- 엔터프라이즈 --------> Kong Konnect
    |
    +-- Cilium CNI 사용 중 ----------> Cilium Gateway
    |
    +-- 멀티클러스터 -----------------> NGINX Gateway Fabric
            |
            +-- F5 엔터프라이즈 -----> NGF Commercial

마이그레이션 우선순위?
    |
    +-- Ingress NGINX 사용 중 -------> 2026년 EOL 전 전환 필수!
    +-- Istio Gateway 사용 중 -------> Gateway API 점진적 전환
    +-- 신규 프로젝트 ----------------> Gateway API 직접 시작
```

---

## CRITICAL: Ingress NGINX EOL 타임라인

```
2024 Q4 -----> Ingress NGINX Community 지원 감소
    |
2025 Q1-Q2 --> Gateway API v1.2 GA (핵심 기능 안정화)
    |
2025 H2 -----> 마이그레이션 권장 기간
    |
2026 --------> Ingress NGINX 지원 종료 (CVE만 패치)
    |
    +-- 권장: 2025년 내 Gateway API 전환 완료
```

### Ingress vs Gateway API 비교

| 항목 | Ingress | Gateway API |
|------|---------|-------------|
| **상태** | 레거시 (1.19~) | 표준 (GA 2023~) |
| **역할 분리** | 없음 | 인프라/앱 분리 |
| **프로토콜** | HTTP(S) 위주 | HTTP, gRPC, TCP, UDP |
| **확장성** | Annotations | Policy Attachment |
| **TLS** | 기본 | mTLS, TLS Passthrough |
| **트래픽 관리** | 제한적 | 가중치, 미러링, 헤더 |
| **CNCF** | - | CNCF 공식 표준 |

---

## Gateway API 핵심 개념

### 리소스 계층 구조

```
+------------------------------------------------------------------+
|                     Infrastructure Provider                        |
|                     (GatewayClass)                                |
+------------------------------------------------------------------+
                               |
                               v
+------------------------------------------------------------------+
|                     Cluster Operator                               |
|                     (Gateway)                                      |
+------------------------------------------------------------------+
                               |
          +--------------------+--------------------+
          |                    |                    |
          v                    v                    v
+------------------+  +------------------+  +------------------+
| Application Dev  |  | Application Dev  |  | Application Dev  |
| (HTTPRoute)      |  | (GRPCRoute)      |  | (TCPRoute)       |
+------------------+  +------------------+  +------------------+
```

### 역할 분리

| 역할 | 담당 | 리소스 |
|------|------|--------|
| **인프라 제공자** | 게이트웨이 구현 | GatewayClass |
| **클러스터 관리자** | 게이트웨이 배포 | Gateway |
| **애플리케이션 개발자** | 라우팅 정의 | HTTPRoute, GRPCRoute |

---

## Gateway API 리소스

### GatewayClass

```yaml
# 인프라 제공자가 정의
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: envoy-gateway
spec:
  controllerName: gateway.envoyproxy.io/gatewayclass-controller
  description: "Envoy Gateway for production workloads"
```

### Gateway

```yaml
# 클러스터 관리자가 정의
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: production-gateway
  namespace: gateway-system
spec:
  gatewayClassName: envoy-gateway

  listeners:
    # HTTPS
    - name: https
      protocol: HTTPS
      port: 443
      hostname: "*.example.com"
      tls:
        mode: Terminate
        certificateRefs:
          - name: wildcard-tls
            kind: Secret
      allowedRoutes:
        namespaces:
          from: Selector
          selector:
            matchLabels:
              gateway-access: "true"
        kinds:
          - kind: HTTPRoute

    # HTTP -> HTTPS 리다이렉트
    - name: http-redirect
      protocol: HTTP
      port: 80
      hostname: "*.example.com"
      allowedRoutes:
        namespaces:
          from: Same
```

### HTTPRoute

```yaml
# 애플리케이션 개발자가 정의
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-app-route
  namespace: production
spec:
  parentRefs:
    - name: production-gateway
      namespace: gateway-system
      sectionName: https

  hostnames:
    - "api.example.com"

  rules:
    # 버전별 라우팅
    - matches:
        - path:
            type: PathPrefix
            value: /api/v2
          headers:
            - name: X-API-Version
              value: "v2"
      backendRefs:
        - name: api-v2
          port: 8080

    # 가중치 기반 트래픽 분할
    - matches:
        - path:
            type: PathPrefix
            value: /api
      backendRefs:
        - name: api-v1
          port: 8080
          weight: 90
        - name: api-v2
          port: 8080
          weight: 10

    # 요청 수정
    - matches:
        - path:
            type: PathPrefix
            value: /legacy
      filters:
        - type: URLRewrite
          urlRewrite:
            path:
              type: ReplacePrefixMatch
              replacePrefixMatch: /api/v1
        - type: RequestHeaderModifier
          requestHeaderModifier:
            add:
              - name: X-Legacy-Redirect
                value: "true"
      backendRefs:
        - name: api-v1
          port: 8080
```

### GRPCRoute

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GRPCRoute
metadata:
  name: grpc-route
  namespace: production
spec:
  parentRefs:
    - name: production-gateway
      namespace: gateway-system

  hostnames:
    - "grpc.example.com"

  rules:
    - matches:
        - method:
            service: myapp.UserService
            method: GetUser
      backendRefs:
        - name: user-service
          port: 9090

    - matches:
        - method:
            service: myapp.OrderService
      backendRefs:
        - name: order-service
          port: 9090
```

---

## Envoy Gateway 설정

### 설치

```bash
# Helm 설치
helm repo add envoy-gateway https://envoyproxy.github.io/gateway-helm
helm install envoy-gateway envoy-gateway/gateway-helm \
  --namespace envoy-gateway-system \
  --create-namespace

# GatewayClass 자동 생성 확인
kubectl get gatewayclass
```

### EnvoyProxy 커스터마이징

```yaml
apiVersion: gateway.envoyproxy.io/v1alpha1
kind: EnvoyProxy
metadata:
  name: custom-proxy
  namespace: envoy-gateway-system
spec:
  provider:
    type: Kubernetes
    kubernetes:
      envoyDeployment:
        replicas: 3
        container:
          resources:
            requests:
              cpu: 100m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi
      envoyService:
        type: LoadBalancer
        annotations:
          service.beta.kubernetes.io/aws-load-balancer-type: "nlb"

  telemetry:
    accessLog:
      settings:
        - format:
            type: JSON
            json:
              start_time: "%START_TIME%"
              method: "%REQ(:METHOD)%"
              path: "%REQ(:PATH)%"
              response_code: "%RESPONSE_CODE%"
              duration: "%DURATION%"
    metrics:
      prometheus: {}
```

### mTLS 설정

```yaml
apiVersion: gateway.envoyproxy.io/v1alpha1
kind: ClientTrafficPolicy
metadata:
  name: mtls-policy
  namespace: gateway-system
spec:
  targetRefs:
    - group: gateway.networking.k8s.io
      kind: Gateway
      name: production-gateway
  tls:
    clientValidation:
      caCertificateRefs:
        - name: client-ca
          kind: ConfigMap
      optional: false
```

### Rate Limiting

```yaml
apiVersion: gateway.envoyproxy.io/v1alpha1
kind: BackendTrafficPolicy
metadata:
  name: rate-limit
  namespace: production
spec:
  targetRefs:
    - group: gateway.networking.k8s.io
      kind: HTTPRoute
      name: my-app-route
  rateLimit:
    type: Global
    global:
      rules:
        - clientSelectors:
            - headers:
                - name: x-user-id
                  type: Distinct
          limit:
            requests: 100
            unit: Minute
```

### JWT 인증

```yaml
apiVersion: gateway.envoyproxy.io/v1alpha1
kind: SecurityPolicy
metadata:
  name: jwt-auth
  namespace: production
spec:
  targetRefs:
    - group: gateway.networking.k8s.io
      kind: HTTPRoute
      name: my-app-route
  jwt:
    providers:
      - name: auth0
        issuer: https://myapp.auth0.com/
        audiences:
          - "api.example.com"
        remoteJWKS:
          uri: https://myapp.auth0.com/.well-known/jwks.json
```

---

## Kong Gateway API 모드

### 설치 (KIC 3.x)

```bash
# Gateway API CRDs 설치
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.0/standard-install.yaml

# Kong Ingress Controller 3.x
helm repo add kong https://charts.konghq.com
helm install kong kong/ingress \
  --namespace kong \
  --create-namespace \
  --set gateway.enabled=true \
  --set controller.ingressController.gatewayDiscovery.enabled=true
```

### Kong GatewayClass

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: kong
  annotations:
    konghq.com/gatewayclass-unmanaged: "true"
spec:
  controllerName: konghq.com/kic-gateway-controller
```

### Kong 플러그인 with Gateway API

```yaml
# Kong 플러그인을 HTTPRoute에 적용
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: rate-limiting
  namespace: production
plugin: rate-limiting
config:
  minute: 100
  policy: local
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-app
  namespace: production
  annotations:
    konghq.com/plugins: rate-limiting
spec:
  parentRefs:
    - name: kong-gateway
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api
      backendRefs:
        - name: my-app
          port: 8080
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Ingress EOL 무시 | 보안 패치 누락 | 2025년 내 마이그레이션 |
| GatewayClass 미확인 | 잘못된 구현체 | 구현체별 GatewayClass 확인 |
| 모든 NS에서 Route 허용 | 보안 위험 | allowedRoutes.namespaces 제한 |
| Annotation 의존 | Gateway API 비호환 | Policy CRD 활용 |
| 단일 Gateway | SPOF | 환경별 Gateway 분리 |

---

## 체크리스트

### 사전 준비
- [ ] Kubernetes 1.26+ 확인
- [ ] Gateway API CRDs 설치 (v1.2+)
- [ ] 구현체 선택 (Envoy/Kong/Istio)

### Gateway 설정
- [ ] GatewayClass 생성
- [ ] Gateway 리소스 정의
- [ ] TLS 인증서 설정
- [ ] allowedRoutes 범위 제한

### Route 설정
- [ ] HTTPRoute/GRPCRoute 정의
- [ ] 트래픽 분할 (Canary)
- [ ] 필터 설정 (Rewrite, Headers)

### 보안
- [ ] mTLS 설정
- [ ] Rate Limiting
- [ ] JWT/OAuth2 인증

## 참조 스킬

- `/k8s:gateway-api-migration` - Ingress NGINX 마이그레이션, Istio Gateway API 통합
- `/service-mesh:istio-gateway` - Istio Gateway 설정
