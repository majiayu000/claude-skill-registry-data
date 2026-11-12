---
name: ml-serving
description: "K8s 기반 ML·LLM 모델 서빙 — 서빙 엔진 비교, KServe, vLLM, TensorRT-LLM, llm-d, KEDA 오토스케일링, 최적화. Use when 모델을 클러스터에 배포하고 추론 지연·처리량을 튜닝할 때."
---

# ML Model Serving 가이드

Kubernetes 기반 ML/LLM 모델 서빙, KServe, vLLM, TensorRT-LLM 최적화

## Quick Reference (결정 트리)

```
서빙 엔진 선택?
    │
    ├─ 범용 ML 모델 ─────────> KServe + Triton
    │       │
    │       ├─ SKLearn/XGBoost ──> Built-in Runtime
    │       ├─ PyTorch/TensorFlow > ModelMesh
    │       └─ Custom ───────────> Custom Predictor
    │
    └─ LLM 추론 ──────────────> KServe + vLLM/TRT-LLM
            │
            ├─ 유연성 우선 ────────> vLLM
            ├─ NVIDIA 최적화 ─────> TensorRT-LLM
            └─ 대규모 분산 ────────> llm-d
```

---

## CRITICAL: 서빙 엔진 비교

| 엔진 | 장점 | 단점 | 최적 사용 |
|------|------|------|----------|
| **vLLM** | HuggingFace 호환, PagedAttention | NVIDIA 전용 최적화 부족 | 빠른 프로토타이핑 |
| **TensorRT-LLM** | NVIDIA 최고 성능, FP8 지원 | 빌드 복잡, NVIDIA 종속 | 프로덕션 최대 처리량 |
| **llm-d** | 분산 추론, KV-cache 최적화 | 복잡한 설정 | 대규모 LLM |
| **Triton** | 멀티 프레임워크, 배치 최적화 | LLM 특화 기능 부족 | 범용 ML |

### 성능 벤치마크 (H100 FP8)

| 엔진 | 최대 처리량 | TTFT | 비고 |
|------|------------|------|------|
| TensorRT-LLM | 10,000+ tok/s | ~100ms | 64 concurrent |
| vLLM | ~8,000 tok/s | ~150ms | PagedAttention |
| HF TGI | ~3,000 tok/s | ~400ms | baseline 대비 |

---

## KServe 설치 및 설정

### Quick Install

```bash
# Knative + KServe 설치
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.15.0/kserve.yaml
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.15.0/kserve-cluster-resources.yaml

# Runtime 설치
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.15.0/kserve-runtimes.yaml
```

### InferenceService 기본

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: sklearn-iris
spec:
  predictor:
    model:
      modelFormat:
        name: sklearn
      storageUri: "s3://models/sklearn/iris"
      resources:
        requests:
          cpu: "1"
          memory: "2Gi"
```

---

## vLLM 배포

### vLLM ServingRuntime

```yaml
apiVersion: serving.kserve.io/v1alpha1
kind: ServingRuntime
metadata:
  name: vllm-runtime
spec:
  annotations:
    prometheus.kserve.io/port: "8000"
    prometheus.kserve.io/path: "/metrics"
  supportedModelFormats:
    - name: vllm
      autoSelect: true
  containers:
    - name: kserve-container
      image: vllm/vllm-openai:latest
      command: ["python", "-m", "vllm.entrypoints.openai.api_server"]
      args:
        - --port=8000
        - --model=/mnt/models
        - --gpu-memory-utilization=0.9
        - --max-model-len=4096
      resources:
        limits:
          nvidia.com/gpu: 1
```

### LLM InferenceService (vLLM)

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: llama-7b
  annotations:
    serving.kserve.io/deploymentMode: RawDeployment
spec:
  predictor:
    model:
      modelFormat:
        name: vllm
      runtime: vllm-runtime
      args:
        - --model=meta-llama/Llama-2-7b-chat-hf
        - --tensor-parallel-size=1
        - --gpu-memory-utilization=0.9
        - --max-model-len=4096
      storageUri: "pvc://model-storage"
      resources:
        limits:
          nvidia.com/gpu: 1
          memory: 24Gi
```

### vLLM 핵심 파라미터

| 파라미터 | 설명 | 권장값 |
|----------|------|--------|
| `--gpu-memory-utilization` | GPU 메모리 사용률 | 0.85-0.95 |
| `--max-model-len` | 최대 컨텍스트 길이 | 모델별 상이 |
| `--tensor-parallel-size` | GPU 병렬화 | GPU 수 |
| `--max-num-seqs` | 최대 동시 시퀀스 | 256 |
| `--enforce-eager` | CUDA Graph 비활성화 | 디버깅 시 |

---

## TensorRT-LLM 배포

### TRT-LLM 엔진 빌드

```bash
# 모델 변환 (Llama-7B 예시)
python convert_checkpoint.py \
  --model_dir ./llama-7b-hf \
  --output_dir ./llama-7b-ckpt \
  --dtype float16

# 엔진 빌드
trtllm-build \
  --checkpoint_dir ./llama-7b-ckpt \
  --output_dir ./llama-7b-engine \
  --gemm_plugin float16 \
  --max_batch_size 64 \
  --max_input_len 2048 \
  --max_output_len 512
```

### TRT-LLM ServingRuntime

```yaml
apiVersion: serving.kserve.io/v1alpha1
kind: ServingRuntime
metadata:
  name: tensorrt-llm-runtime
spec:
  supportedModelFormats:
    - name: tensorrt-llm
  containers:
    - name: kserve-container
      image: nvcr.io/nvidia/tritonserver:24.04-trtllm-python-py3
      resources:
        limits:
          nvidia.com/gpu: 1
```

---

## 대규모 LLM 배포 (llm-d)

### llm-d 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                      llm-d Architecture                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────┐    ┌─────────────────────────────────────┐  │
│  │  Gateway   │───>│        Inference Gateway            │  │
│  │  (Ingress) │    │  - Request Routing                  │  │
│  └────────────┘    │  - KV-Cache Aware Scheduling        │  │
│                    └─────────────────────────────────────┘  │
│                              │                               │
│              ┌───────────────┼───────────────┐              │
│              ▼               ▼               ▼              │
│      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐    │
│      │   Prefill    │ │   Decode     │ │   Decode     │    │
│      │   Instance   │ │   Instance   │ │   Instance   │    │
│      │   (H100)     │ │   (H100)     │ │   (H100)     │    │
│      └──────────────┘ └──────────────┘ └──────────────┘    │
│              │               │               │              │
│              └───────────────┼───────────────┘              │
│                              ▼                               │
│                    ┌─────────────────┐                      │
│                    │   KV Cache      │                      │
│                    │   Transfer      │                      │
│                    │   (RDMA/ICI)    │                      │
│                    └─────────────────┘                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### llm-d 설치

```bash
# Helm 설치
helm repo add llm-d https://llm-d.github.io/llm-d
helm install llm-d llm-d/llm-d \
  --namespace llm-d \
  --create-namespace \
  --set vllm.enabled=true \
  --set gateway.replicas=2
```

### 분산 추론 설정

```yaml
# Disaggregated Prefill-Decode
apiVersion: llm-d.io/v1
kind: LLMDeployment
metadata:
  name: deepseek-v3
spec:
  model: deepseek-ai/DeepSeek-V3
  prefill:
    replicas: 2
    resources:
      nvidia.com/gpu: 8
  decode:
    replicas: 4
    resources:
      nvidia.com/gpu: 8
  kvCache:
    transfer: rdma
    compression: true
```

---

## 오토스케일링 (KEDA)

### KEDA 기반 LLM 스케일링

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: vllm-scaler
spec:
  scaleTargetRef:
    name: llama-7b-predictor
  minReplicaCount: 1
  maxReplicaCount: 10
  triggers:
    # KV Cache 사용률 기반
    - type: prometheus
      metadata:
        serverAddress: http://prometheus:9090
        metricName: vllm_gpu_cache_usage_perc
        threshold: "80"
        query: |
          avg(vllm_gpu_cache_usage_perc{
            namespace="default",
            pod=~"llama-7b.*"
          })
    # 대기 중인 요청 수 기반
    - type: prometheus
      metadata:
        metricName: vllm_num_requests_waiting
        threshold: "10"
        query: |
          sum(vllm_num_requests_waiting{
            namespace="default"
          })
```

### 스케일 투 제로

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: vllm-scale-to-zero
spec:
  scaleTargetRef:
    name: llama-7b-predictor
  minReplicaCount: 0  # Scale to zero
  maxReplicaCount: 5
  cooldownPeriod: 300  # 5분 유휴 후 스케일 다운
  triggers:
    - type: prometheus
      metadata:
        metricName: vllm_requests_total
        threshold: "1"
```

---

## 최적화 기법

### Quantization (양자화)

| 방식 | 메모리 절감 | 성능 영향 | 지원 |
|------|------------|----------|------|
| FP16 | 50% | 무시 | vLLM, TRT |
| INT8 (SmoothQuant) | 50% | 1-3% 저하 | TRT-LLM |
| FP8 | 50% | 무시 | TRT-LLM (H100+) |
| INT4 (AWQ/GPTQ) | 75% | 3-5% 저하 | vLLM, TRT |

```yaml
# vLLM AWQ 양자화
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
spec:
  predictor:
    model:
      args:
        - --model=TheBloke/Llama-2-7B-AWQ
        - --quantization=awq
        - --dtype=half
```

### Speculative Decoding

```yaml
# Draft 모델로 추론 가속
spec:
  predictor:
    model:
      args:
        - --model=meta-llama/Llama-2-70b
        - --speculative-model=meta-llama/Llama-2-7b
        - --num-speculative-tokens=5
```

### Continuous Batching

```yaml
# 동적 배칭 설정
args:
  - --max-num-seqs=256
  - --max-paddings=256
  - --disable-frontend-multiprocessing=false
```

---

## 모니터링

### vLLM 핵심 메트릭

```promql
# 처리량 (tokens/sec)
rate(vllm_generation_tokens_total[5m])

# KV Cache 사용률
vllm_gpu_cache_usage_perc

# 대기 중인 요청
vllm_num_requests_waiting

# 실행 중인 요청
vllm_num_requests_running

# TTFT (Time To First Token)
histogram_quantile(0.99,
  rate(vllm_time_to_first_token_seconds_bucket[5m])
)
```

### 알림 규칙

```yaml
groups:
  - name: llm-serving
    rules:
      - alert: HighKVCacheUsage
        expr: vllm_gpu_cache_usage_perc > 95
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "KV Cache 사용률 95% 초과"

      - alert: HighRequestLatency
        expr: |
          histogram_quantile(0.99,
            rate(vllm_e2e_request_latency_seconds_bucket[5m])
          ) > 10
        for: 5m
        labels:
          severity: critical
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Warm-up 미적용 | 콜드 스타트 지연 | preload 설정 |
| GPU 메모리 과다 할당 | OOM 발생 | 0.85-0.9 사용률 |
| 단일 레플리카 | 가용성 저하 | 최소 2개 레플리카 |
| 고정 배치 크기 | 비효율적 처리 | Continuous Batching |
| 모니터링 부재 | 병목 미파악 | DCGM + vLLM 메트릭 |

---

## 체크리스트

### 배포 전
- [ ] 모델 크기 대비 GPU 메모리 확인
- [ ] 양자화 필요 여부 검토
- [ ] 스토리지 (PVC/S3) 준비
- [ ] ServingRuntime 생성

### 프로덕션
- [ ] 오토스케일링 (KEDA) 설정
- [ ] Warm-up 활성화
- [ ] 모니터링 대시보드 구성
- [ ] 알림 규칙 설정
- [ ] 부하 테스트 완료

**관련 agent**: `mlops-expert`
**관련 skill**: `/k8s:k8s-gpu`

---

## Sources

- [KServe v0.15 Release](https://www.cncf.io/blog/2025/06/18/announcing-kserve-v0-15-advancing-generative-ai-model-serving/)
- [vLLM + KServe Guide](https://developer.ibm.com/articles/llms-inference-scaling-vllm-kserve/)
- [llm-d Project](https://github.com/llm-d/llm-d)
- [KEDA Autoscaling for vLLM](https://developers.redhat.com/articles/2025/09/23/how-set-kserve-autoscaling-vllm-keda)
- [vLLM vs TensorRT-LLM](https://northflank.com/blog/vllm-vs-tensorrt-llm-and-how-to-run-them)
- [GKE LLM Optimization](https://docs.cloud.google.com/kubernetes-engine/docs/best-practices/machine-learning/inference/llm-optimization)
