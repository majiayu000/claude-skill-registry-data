---
name: triton-deploy
description: NVIDIA Triton Inference Server 배포 및 관리. "triton 서버", "triton 실행", "모델 서빙", "inference server" 요청 시 활성화됩니다.
---

# Triton Deploy 스킬

## Overview

NVIDIA Triton Inference Server 컨테이너 배포 및 관리를 자동화하는 스킬입니다.

**중요**: 이 스킬이 활성화되면 Claude가 자동으로 스크립트를 실행합니다. 사용자가 직접 명령어를 입력할 필요가 없습니다.

**핵심 기능:**
- **서버 실행**: GPU/메모리 설정이 포함된 docker 컨테이너 실행
- **모델 관리**: 모델 레포지토리 마운트 및 로드
- **상태 모니터링**: 서버 헬스체크 및 모델 상태 확인
- **포트 관리**: HTTP/gRPC/metrics 포트 자동 설정
- **프로파일 지원**: 개발/프로덕션 환경별 설정

## Script Location

```
SCRIPT: ./scripts/triton-deploy.sh
```

Claude는 이 스크립트를 Bash 도구로 직접 실행합니다.

## When to Use

이 스킬은 다음 상황에서 활성화됩니다:

**명시적 요청:**
- "triton 서버 실행해줘"
- "모델 서빙 시작해줘"
- "inference server 띄워줘"
- "triton 상태 확인해줘"
- "모델 로드해줘"

**자동 활성화:**
- Triton 관련 docker 명령 실행 시
- 모델 서빙 요청 시

## Prerequisites

```bash
# Docker 설치 확인
docker --version

# NVIDIA Container Toolkit 확인 (GPU 사용 시)
nvidia-container-cli --version

# 스크립트 실행 권한
chmod +x /path/to/agent-skills/ml/triton-deploy/scripts/triton-deploy.sh
```

## Workflow

### Claude 실행 절차

**Step 1**: 사용자 요청 분석
- 실행할 모델 또는 모델 레포지토리 경로 파악
- GPU 설정 확인 (기본: GPU 0)
- 포트 설정 확인 (기본: 8000/8001/8002)

**Step 2**: 스크립트 실행
```bash
# 스크립트 경로
SCRIPT=./scripts/triton-deploy.sh

# 서버 시작
$SCRIPT start --model-repo <path> [--gpu <devices>] [--port <port>] [--profile <name>]

# 상태 확인
$SCRIPT status

# 모델 목록
$SCRIPT models

# 서버 중지
$SCRIPT stop

# 로그 확인
$SCRIPT logs [--follow]
```

**Step 3**: 결과 보고
- 서버 시작 성공 여부
- 로드된 모델 목록
- 접속 URL 안내

### 명령어 레퍼런스

| 작업 | 명령어 |
|------|--------|
| 기본 시작 | `$SCRIPT start --model-repo /path/to/models` |
| GPU 지정 | `$SCRIPT start --model-repo /path --gpu 0,1` |
| 프로파일 사용 | `$SCRIPT start --profile langdetector` |
| 상태 확인 | `$SCRIPT status` |
| 모델 목록 | `$SCRIPT models` |
| 서버 중지 | `$SCRIPT stop` |
| 로그 확인 | `$SCRIPT logs --follow` |

### 자주 사용하는 설정

| 용도 | 명령어 |
|------|--------|
| 개발 (단일 GPU) | `triton-deploy.sh start --model-repo ./models --gpu 0` |
| 프로덕션 (멀티 GPU) | `triton-deploy.sh start --model-repo ./models --gpu all --shm 8g` |
| 디버그 모드 | `triton-deploy.sh start --model-repo ./models --verbose` |
| 특정 모델만 | `triton-deploy.sh start --model-repo ./models --load-model my_model` |

---

## Examples

### 예시 1: 기본 서버 실행

```
사용자: langdetector 모델로 triton 서버 띄워줘

Claude: Triton 서버를 실행합니다.

$ triton-deploy.sh start --profile langdetector

Starting Triton Server...
- Image: nvcr.io/nvidia/tritonserver:24.01-py3
- GPU: device=0
- Model Repo: /nfs/train/langdetector/models/triton
- Ports: 8000 (HTTP), 8001 (gRPC), 8002 (metrics)

Container ID: abc123def456

Waiting for server ready...
Server is READY

## Status

| Property | Value |
|----------|-------|
| Container | triton-langdetector |
| Status | Running |
| HTTP | http://localhost:8000 |
| gRPC | localhost:8001 |
```

### 예시 2: 멀티 GPU 프로덕션 배포

```
사용자: GPU 0,1번으로 triton 띄워줘. 메모리 8GB로

Claude: 멀티 GPU 설정으로 Triton을 실행합니다.

$ triton-deploy.sh start \
    --model-repo /mnt/models \
    --gpu 0,1 \
    --shm 8g \
    --port 16000

Starting Triton Server...
- GPU: device=0,1
- Shared Memory: 8GB
- Ports: 16000, 16001, 16002

Server is READY

## Loaded Models

| Model | Version | Status |
|-------|---------|--------|
| langdetector_ensemble | 1 | READY |
| features | 1 | READY |
| classifier | 1 | READY |
```

### 예시 3: 서버 상태 확인

```
사용자: triton 상태 확인해줘

Claude: Triton 서버 상태를 확인합니다.

$ triton-deploy.sh status

## Server Status

| Property | Value |
|----------|-------|
| Container | triton-server |
| Status | Running |
| Uptime | 2h 35m |
| HTTP | healthy |
| gRPC | healthy |

## Resource Usage

| Metric | Value |
|--------|-------|
| GPU Memory | 4.2GB / 24GB |
| CPU | 15% |
| Memory | 2.1GB |
```

### 예시 4: 모델 상태 확인

```
사용자: 로드된 모델 확인해줘

Claude: 모델 상태를 확인합니다.

$ triton-deploy.sh models

## Loaded Models

| Model | Version | Status | Backend |
|-------|---------|--------|---------|
| langdetector_ensemble | 1 | READY | ensemble |
| langdetector_features | 1 | READY | onnxruntime |
| langdetector_classifier | 1 | READY | tensorrt |

Total: 3 models loaded
```

---

## Configuration

### 프로파일 설정

`~/.triton-profiles.yaml` 파일로 프로파일 정의:

```yaml
profiles:
  langdetector:
    image: hub.rtzr.ai/rtzr/tritonserver:25.01-rtzr-py3
    model_repo: /nfs/train/langdetector/models/triton
    gpu: "0"
    shm_size: 4g
    ports:
      http: 15000
      grpc: 15001
      metrics: 15002

  asr:
    image: nvcr.io/nvidia/tritonserver:24.01-py3
    model_repo: /nfs/train/asr/models
    gpu: "0,1"
    shm_size: 8g
```

### 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `TRITON_IMAGE` | Docker 이미지 | nvcr.io/nvidia/tritonserver:24.01-py3 |
| `TRITON_SHM_SIZE` | 공유 메모리 크기 | 4g |
| `TRITON_PINNED_MEMORY` | Pinned 메모리 | 2073741824 |

---

## Best Practices

**DO:**
- 프로파일 사용으로 설정 재사용
- 헬스체크로 서버 준비 확인 후 요청
- 적절한 공유 메모리 크기 설정
- 모델별 최적 백엔드 선택 (TensorRT > ONNX > PyTorch)

**DON'T:**
- 포트 충돌 무시하고 실행
- 공유 메모리 부족 상태로 운영
- GPU 메모리 초과 모델 로드
- 프로덕션에서 verbose 모드 사용

---

## Troubleshooting

### 서버 시작 실패

```bash
# 포트 사용 확인
triton-deploy.sh check-port 8000

# GPU 가용성 확인
nvidia-smi

# 컨테이너 로그 확인
triton-deploy.sh logs
```

### 모델 로드 실패

```bash
# 모델 설정 검증
triton-deploy.sh validate --model-repo /path/to/models

# 특정 모델 로그
triton-deploy.sh logs --model my_model
```

### GPU 메모리 부족

```bash
# GPU 메모리 확인
nvidia-smi

# 다른 컨테이너 정리
docker ps -a | grep triton
docker rm -f <container_id>
```

---

## Resources

| 파일 | 설명 |
|------|------|
| `scripts/triton-deploy.sh` | Triton 서버 배포 통합 스크립트 |
| `~/.triton-profiles.yaml` | 프로파일 설정 파일 (사용자 정의) |
