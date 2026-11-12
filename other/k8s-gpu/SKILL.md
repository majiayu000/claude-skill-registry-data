---
name: k8s-gpu
description: "Kubernetes GPU 기본 구성 — NVIDIA GPU Operator, MIG 파티셔닝, GPU 공유 전략. Use when 클러스터에 GPU 노드를 도입하거나 MIG·time-slicing 으로 GPU 를 나눠 쓸 때."
---

# Kubernetes GPU 가이드

NVIDIA GPU Operator, MIG 파티셔닝, GPU 공유 전략

## Quick Reference (결정 트리)

```
GPU 워크로드 유형?
    │
    ├─ 분산 학습 (Multi-GPU)
    │       │
    │       ├─ Gang 스케줄링 필요 ───> Volcano
    │       └─ 큐 관리 필요 ────────> Kueue
    │
    ├─ 단일 GPU 학습
    │       │
    │       └─ 기본 스케줄링 ───────> NVIDIA Device Plugin
    │
    ├─ GPU 공유 (소형 워크로드)
    │       │
    │       ├─ 격리 필요 ──────────> MIG (A100/H100)
    │       └─ 처리량 우선 ────────> MPS (시분할)
    │
    └─ 추론
            │
            ├─ 소형 모델 ──────────> MIG / Time-slicing
            └─ 대형 LLM ───────────> 전용 GPU
```

---

## CRITICAL: GPU 스케줄링 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                 Kubernetes GPU Scheduling Stack                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Application Layer                            │   │
│  │  PyTorch Job, TensorFlow Job, KServe, Custom Pod         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Scheduling Layer                             │   │
│  │  Kueue (Queue/Quota) | Volcano (Gang Scheduling)         │   │
│  │                      │                                    │   │
│  │  Default K8s Scheduler                                    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Device Layer                                 │   │
│  │  NVIDIA Device Plugin | MIG Manager | MPS | DCGM         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Hardware Layer                               │   │
│  │  A100 (80GB) | H100 (80GB) | T4 (16GB) | L4 (24GB)       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## NVIDIA GPU Operator

### 설치

```bash
# Helm repo 추가
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update

# GPU Operator 설치
helm install gpu-operator nvidia/gpu-operator \
  --namespace gpu-operator \
  --create-namespace \
  --set driver.enabled=true \
  --set toolkit.enabled=true \
  --set devicePlugin.enabled=true \
  --set dcgmExporter.enabled=true \
  --set mig.strategy=mixed  # MIG 지원
```

### 설정 옵션

```yaml
# gpu-operator-values.yaml
driver:
  enabled: true
  version: "535.104.12"  # CUDA 12.2

toolkit:
  enabled: true

devicePlugin:
  enabled: true
  config:
    name: time-slicing-config
    default: any

dcgmExporter:
  enabled: true
  serviceMonitor:
    enabled: true

mig:
  strategy: mixed  # none, single, mixed

validator:
  enabled: true
```

### GPU 노드 확인

```bash
# GPU 노드 레이블 확인
kubectl get nodes -l nvidia.com/gpu.present=true

# GPU 리소스 확인
kubectl describe node <gpu-node> | grep -A 10 "Allocatable"

# 할당된 GPU 확인
kubectl get pods -A -o custom-columns=\
"POD:.metadata.name,GPU:.spec.containers[*].resources.limits.nvidia\.com/gpu"
```

---

## GPU 공유 전략

### MIG (Multi-Instance GPU)

**지원 GPU**: A100, A30, H100

```yaml
# MIG 파티션 설정
apiVersion: v1
kind: ConfigMap
metadata:
  name: mig-parted-config
  namespace: gpu-operator
data:
  config.yaml: |
    version: v1
    mig-configs:
      # A100-40GB 파티션 예시
      all-1g.5gb:
        - devices: all
          mig-enabled: true
          mig-devices:
            "1g.5gb": 7     # 7개의 소형 인스턴스

      all-balanced:
        - devices: all
          mig-enabled: true
          mig-devices:
            "3g.20gb": 2    # 중형 2개
            "1g.5gb": 1     # 소형 1개

      # H100-80GB 파티션 예시
      h100-inference:
        - devices: all
          mig-enabled: true
          mig-devices:
            "1g.10gb": 7    # 추론용 소형 7개
```

### MIG 사용 Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mig-inference-pod
spec:
  containers:
    - name: inference
      image: nvcr.io/nvidia/tritonserver:latest
      resources:
        limits:
          nvidia.com/mig-1g.5gb: 1  # MIG 슬라이스 요청
```

### Time-Slicing (시분할)

**모든 GPU 지원**

```yaml
# Time-slicing 설정
apiVersion: v1
kind: ConfigMap
metadata:
  name: time-slicing-config
  namespace: gpu-operator
data:
  any: |
    version: v1
    sharing:
      timeSlicing:
        renameByDefault: false
        resources:
          - name: nvidia.com/gpu
            replicas: 4  # 1 GPU를 4개로 분할
```

```yaml
# Time-slicing 사용 Pod
apiVersion: v1
kind: Pod
metadata:
  name: shared-gpu-pod
spec:
  containers:
    - name: app
      image: cuda-app:latest
      resources:
        limits:
          nvidia.com/gpu: 1  # 1/4 GPU 사용
```

### MPS (Multi-Process Service)

```yaml
# MPS 활성화
apiVersion: v1
kind: ConfigMap
metadata:
  name: mps-config
  namespace: gpu-operator
data:
  config.yaml: |
    version: v1
    sharing:
      mps:
        renameByDefault: false
        resources:
          - name: nvidia.com/gpu
            replicas: 10  # 최대 10개 프로세스 공유
```

### 공유 전략 비교

| 전략 | 격리 | 성능 | 적합 워크로드 |
|------|------|------|---------------|
| **MIG** | 하드웨어 | 최고 | 안정적 추론, 학습 |
| **Time-slicing** | 없음 | 중간 | 개발, CI/CD |
| **MPS** | 소프트웨어 | 높음 | 추론, 배치 |

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 전체 GPU 요청 | 리소스 낭비 | MIG/Time-slicing |
| Gang 스케줄링 미사용 | 분산 학습 실패 | Volcano 사용 |
| 쿼터 미설정 | 팀간 경합 | Kueue ClusterQueue |
| 모니터링 부재 | 사용률 불명 | DCGM Exporter |
| 단일 노드 풀 | 스케일링 어려움 | 워크로드별 노드 풀 |

---

## 체크리스트

### 인프라 설정
- [ ] NVIDIA GPU Operator 설치
- [ ] DCGM Exporter 활성화
- [ ] GPU 노드 레이블링
- [ ] Karpenter/CA GPU 풀 설정

### 공유 전략
- [ ] MIG 프로필 설정 (A100/H100)
- [ ] Time-slicing 또는 MPS 설정
- [ ] ResourceFlavor 정의

**관련 agent**: `mlops-expert`
**관련 skill**: `/k8s:k8s-gpu-scheduling` (Kueue, Volcano, 모니터링), `/ai:ml-serving`, `/k8s:k8s-autoscaling`
