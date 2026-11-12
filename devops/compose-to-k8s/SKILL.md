---
name: compose-to-k8s
description: "Docker Compose 에서 Kubernetes 매니페스트로 전환 — Kompose 자동 변환, 수동 패턴, StatefulSet. Use when Compose 로 돌던 서비스를 K8s 로 이전할 때."
---

# Docker Compose → Kubernetes 전환 가이드

Docker Compose에서 Kubernetes 매니페스트로의 전환 패턴. Kompose 활용 및 수동 전환 전략.

## Quick Reference (결정 트리)

```
Compose → K8s 전환 방법?
    │
    ├─ 빠른 시작 ──────────> Kompose (자동 변환)
    │     │
    │     └─ 변환 후 반드시 수동 검토/수정
    │
    ├─ 정교한 전환 ────────> 수동 매핑 (권장)
    │     │
    │     └─ 서비스별로 Deployment + Service 작성
    │
    └─ Helm Chart 생성 ───> 수동 매핑 + 변수화
          │
          └─ 환경별 values overlay 포함
```

---

## Compose ↔ K8s 개념 매핑

```
┌────────────────────┬────────────────────────────────────┐
│ Docker Compose     │ Kubernetes                         │
├────────────────────┼────────────────────────────────────┤
│ services:          │ Deployment + Service               │
│ image:             │ spec.containers[].image            │
│ ports:             │ Service (ClusterIP/NodePort)       │
│   "8080:80"        │   + Ingress                        │
│ environment:       │ ConfigMap + env/envFrom            │
│ env_file:          │ ConfigMap (from file)              │
│ volumes:           │ PersistentVolumeClaim (PVC)        │
│   named volumes    │   + PersistentVolume (PV)          │
│   bind mounts      │   hostPath (dev only)              │
│ networks:          │ NetworkPolicy (선택적)             │
│ depends_on:        │ initContainers / readinessProbe    │
│ healthcheck:       │ livenessProbe / readinessProbe     │
│ restart: always    │ restartPolicy: Always (기본값)     │
│ deploy.replicas    │ spec.replicas                      │
│ deploy.resources   │ resources.requests/limits          │
│ secrets:           │ Secret                             │
│ configs:           │ ConfigMap                          │
└────────────────────┴────────────────────────────────────┘
```

---

## Kompose (자동 변환)

### 설치

```bash
# macOS
brew install kompose

# Linux
curl -L https://github.com/kubernetes/kompose/releases/download/v1.34.0/kompose-linux-amd64 -o kompose
chmod +x kompose && sudo mv kompose /usr/local/bin/
```

### 기본 사용법

```bash
# docker-compose.yml → K8s 매니페스트
kompose convert

# Helm chart로 변환
kompose convert --chart

# 특정 파일 지정
kompose convert -f docker-compose.yml -f docker-compose.override.yml

# stdout으로 출력 (파일 생성하지 않음)
kompose convert --stdout
```

### Kompose 한계점 (반드시 수동 수정 필요)

```
1. depends_on → 변환되지 않음 → initContainers/readinessProbe로 수동 구현
2. build: → 무시됨 → 사전에 이미지 빌드/푸시 필요
3. volumes (bind mount) → hostPath로 변환 → PVC로 교체 필요
4. networks → 무시됨 → NetworkPolicy로 수동 구현
5. ports (host binding) → NodePort로 변환 → Ingress로 교체 필요
6. healthcheck → 부분 변환 → probe 세부 설정 수동 필요
7. 리소스 제한 → deploy.resources가 있어야 변환됨
```

---

## 수동 전환 패턴

### 전형적인 Compose 서비스

```yaml
# docker-compose.yml
version: "3.8"

services:
  api:
    build: ./api
    image: myapp-api:latest
    ports:
      - "8080:8080"
    environment:
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_NAME=myapp
      - REDIS_HOST=redis
      - LOG_LEVEL=debug
    env_file:
      - .env
    volumes:
      - api-data:/app/data
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 3
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: "1.0"
          memory: 512M

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    volumes:
      - pg-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U myuser"]
      interval: 5s
      timeout: 3s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  api-data:
  pg-data:
  redis-data:
```

### K8s 매니페스트로 전환

#### Deployment

```yaml
# api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  labels:
    app: api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      initContainers:
        # depends_on 대체 — DB 준비 대기
        - name: wait-for-db
          image: busybox:1.36
          command: ['sh', '-c', 'until nc -z postgres 5432; do sleep 2; done']
      containers:
        - name: api
          image: myapp-api:latest
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: api-config
          env:
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: password
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: "1"
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: api-data
              mountPath: /app/data
      volumes:
        - name: api-data
          persistentVolumeClaim:
            claimName: api-data-pvc
```

#### Service

```yaml
# api-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app: api
  ports:
    - port: 8080
      targetPort: 8080
  type: ClusterIP    # 외부 노출은 Ingress로
```

#### Ingress

```yaml
# api-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
  annotations: {}    # 환경별로 다른 annotation
spec:
  ingressClassName: nginx    # 변수화 대상
  rules:
    - host: api.dev.example.com    # 변수화 대상
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api
                port:
                  number: 8080
```

#### ConfigMap (environment → ConfigMap)

```yaml
# api-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
data:
  DB_HOST: postgres
  DB_PORT: "5432"
  DB_NAME: myapp
  REDIS_HOST: redis
  LOG_LEVEL: debug    # 환경별 override 대상
```

#### Secret (비밀번호 분리)

```yaml
# db-secret.yaml (실제로는 External Secrets 사용 권장)
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
stringData:
  password: mypassword    # 실환경에서는 절대 git에 커밋하지 않음
```

#### PVC

```yaml
# api-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: api-data-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard    # 변수화: standard(kind) / gp3(EKS) / pd-ssd(GKE)
  resources:
    requests:
      storage: 1Gi    # 변수화 대상
```

---

## StatefulSet (DB/Redis)

Compose의 DB 서비스는 K8s에서 StatefulSet으로 전환한다.

```yaml
# postgres-statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:16-alpine
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_DB
              value: myapp
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: username
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: password
          readinessProbe:
            exec:
              command: ["pg_isready", "-U", "myuser"]
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: pg-data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: pg-data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: standard    # 변수화
        resources:
          requests:
            storage: 10Gi
```

### Phase별 DB 전략

```
Phase 0 (compose):  postgres 컨테이너 (데이터 휘발 OK)
Phase 1 (kind):     StatefulSet + PVC (데이터 영속)
Phase 2 (staging):  StatefulSet + PVC (또는 외부 DB)
Phase 3 (prod):     RDS/Cloud SQL (Managed DB로 전환)
                    → DB_HOST만 변경하면 됨 (변수화 덕분)
```

---

## 단계별 전환 전략

### 권장 순서

```
1단계: Compose 정리 (K8s 전환 준비)
   - 모든 환경변수를 .env 파일로 분리
   - healthcheck 추가
   - 리소스 제한 (deploy.resources) 추가
   - bind mount → named volume 전환

2단계: 무상태(Stateless) 서비스 먼저 전환
   - API 서버, 웹 프론트엔드 등
   - Deployment + Service + Ingress

3단계: 유상태(Stateful) 서비스 전환
   - DB, Redis, Kafka 등
   - StatefulSet + PVC
   - 또는 Managed 서비스로 외부화 (Phase 3 대비)

4단계: 보조 서비스 전환
   - 모니터링 (Prometheus, Grafana)
   - 로깅 (Fluent Bit, Loki)
   - 이것들은 Helm chart로 설치 (수동 전환 불필요)

5단계: CI/CD 연동
   - 이미지 빌드 → 레지스트리 푸시 → ArgoCD 배포
   - docker-compose는 로컬 개발 전용으로 유지 가능
```

### docker-compose와 K8s 병행 운영

```
# 로컬 개발: docker-compose (유지)
# CI 테스트: kind + K8s manifests
# staging/prod: EKS/GKE + K8s manifests

# Makefile로 통합
make dev       # docker-compose up
make test-k8s  # kind create cluster + helm install
make deploy    # argocd sync
```

---

## 전환 체크리스트

```
[ ] 모든 서비스에 healthcheck/probe 정의됨
[ ] 환경변수가 ConfigMap/Secret으로 분리됨
[ ] 비밀번호/토큰이 Secret으로 관리됨
[ ] named volume이 PVC로 전환됨
[ ] depends_on이 initContainers/readinessProbe로 대체됨
[ ] 포트 매핑이 Service + Ingress로 전환됨
[ ] 리소스 requests/limits가 설정됨
[ ] 이미지가 레지스트리에서 pull 가능함 (build: 의존 제거)
[ ] StorageClass가 변수화됨 (kind/EKS/GKE)
[ ] IngressClass가 변수화됨
[ ] 로그가 stdout/stderr로 출력됨 (파일 로그 X)
```
