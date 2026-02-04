---
name: ml-benchmark
description: ML 모델 벤치마크 및 평가 실행. "벤치마크", "모델 평가", "성능 테스트", "inference 속도" 요청 시 활성화됩니다.
---

# ML Benchmark 스킬

## Overview

ML 모델의 성능 벤치마크 및 평가를 자동화하는 스킬입니다.

**중요**: 이 스킬이 활성화되면 Claude가 자동으로 스크립트를 실행합니다. 사용자가 직접 명령어를 입력할 필요가 없습니다.

**핵심 기능:**
- **벤치마크 실행**: 지연시간, 처리량, 정확도 측정
- **결과 비교**: 여러 모델/버전 간 성능 비교
- **리포트 생성**: 마크다운/JSON 형식 결과 저장
- **프로파일 지원**: 사전 정의된 벤치마크 시나리오
- **다국어 평가**: 언어별 성능 분석

## Script Location

```
SCRIPT: ./scripts/ml-benchmark.sh
```

Claude는 이 스크립트를 Bash 도구로 직접 실행합니다.

## When to Use

이 스킬은 다음 상황에서 활성화됩니다:

**명시적 요청:**
- "벤치마크 실행해줘"
- "모델 평가해줘"
- "성능 테스트해줘"
- "inference 속도 측정해줘"
- "결과 비교해줘"

**자동 활성화:**
- 모델 성능 측정 요청 시
- 평가 스크립트 실행 요청 시

## Prerequisites

```bash
# Python 환경 확인
python --version
uv --version  # 또는 pip

# 필요 패키지
pip install numpy pandas matplotlib

# 스크립트 실행 권한
chmod +x /path/to/agent-skills/ml/ml-benchmark/scripts/ml-benchmark.sh
```

## Workflow

### Claude 실행 절차

**Step 1**: 사용자 요청 분석
- 벤치마크 대상 모델 확인
- 서버 URL 확인 (기본: localhost:8001)
- 실행 횟수 및 옵션 파악

**Step 2**: 스크립트 실행
```bash
# 스크립트 경로
SCRIPT=./scripts/ml-benchmark.sh

# 벤치마크 실행
$SCRIPT run --url <endpoint> --model <name> [--runs <n>] [--save <file>]

# 정확도 평가
$SCRIPT evaluate --url <endpoint> --model <name> --languages <langs> [--samples-per-lang <n>]

# 결과 비교
$SCRIPT compare <result1.json> <result2.json>

# 히스토리 조회
$SCRIPT history <model_name>
```

**Step 3**: 결과 보고
- 지연시간 (P50/P95/P99)
- 처리량 (req/s)
- GPU 메모리 사용량
- 정확도 (평가 시)

### 명령어 레퍼런스

| 작업 | 명령어 |
|------|--------|
| 기본 벤치마크 | `$SCRIPT run --url localhost:8001 --model langdetector` |
| 100회 실행 | `$SCRIPT run --url localhost:8001 --model langdetector --runs 100` |
| 결과 저장 | `$SCRIPT run --url localhost:8001 --model langdetector --save results/bench.json` |
| 정확도 평가 | `$SCRIPT evaluate --url localhost:8001 --model langdetector --languages en,ja,ko` |
| 결과 비교 | `$SCRIPT compare results/v1.json results/v2.json` |
| 프로파일 사용 | `$SCRIPT run --profile langdetector-prod` |

### 측정 항목

| 항목 | 설명 | 단위 |
|------|------|------|
| Latency P50 | 50번째 백분위 지연시간 | ms |
| Latency P95 | 95번째 백분위 지연시간 | ms |
| Latency P99 | 99번째 백분위 지연시간 | ms |
| Throughput | 초당 처리량 | req/s |
| GPU Memory | GPU 메모리 사용량 | MB |
| Accuracy | 정확도 (평가 시) | % |

---

## Examples

### 예시 1: 기본 벤치마크

```
사용자: langdetector 벤치마크 100회 돌려줘

Claude: langdetector 벤치마크를 실행합니다.

$ ml-benchmark.sh run \
    --url localhost:15001 \
    --model langdetector_ensemble \
    --runs 100

Running benchmark...
- Model: langdetector_ensemble
- Endpoint: localhost:15001
- Runs: 100

Warming up... (5 runs)
Benchmarking... [████████████████████] 100/100

## Benchmark Results

| Metric | Value |
|--------|-------|
| Model | langdetector_ensemble |
| Runs | 100 |
| Latency P50 | 12.3ms |
| Latency P95 | 15.8ms |
| Latency P99 | 18.2ms |
| Throughput | 78.5 req/s |
| GPU Memory | 1.2GB |
```

### 예시 2: 결과 비교

```
사용자: rt vs mms 평가 결과 비교해줘

Claude: 두 모델의 결과를 비교합니다.

$ ml-benchmark.sh compare results/rt_eval.json results/mms_eval.json

## Model Comparison

| Metric | RT | MMS | Diff |
|--------|-----|-----|------|
| Latency P50 | 12.3ms | 45.6ms | -73% |
| Latency P95 | 15.8ms | 52.1ms | -70% |
| Throughput | 78.5/s | 21.2/s | +270% |
| Accuracy (en) | 98.2% | 97.8% | +0.4% |
| Accuracy (ja) | 96.5% | 95.2% | +1.3% |
| Accuracy (ko) | 97.1% | 96.8% | +0.3% |

Winner: RT (faster with similar accuracy)
```

### 예시 3: 다국어 평가

```
사용자: langdetector 영어, 일본어, 한국어 정확도 평가해줘

Claude: 다국어 정확도 평가를 실행합니다.

$ ml-benchmark.sh evaluate \
    --url localhost:15001 \
    --model langdetector_ensemble \
    --languages en,ja,ko \
    --samples-per-lang 100

Evaluating accuracy...
- Languages: en, ja, ko
- Samples per language: 100

## Evaluation Results

| Language | Samples | Correct | Accuracy |
|----------|---------|---------|----------|
| en | 100 | 98 | 98.0% |
| ja | 100 | 96 | 96.0% |
| ko | 100 | 97 | 97.0% |

**Overall: 97.0%**
```

### 예시 4: 결과 저장 및 추적

```
사용자: 벤치마크 결과 저장해서 추적할 수 있게 해줘

Claude: 결과를 JSON으로 저장합니다.

$ ml-benchmark.sh run \
    --url localhost:15001 \
    --model langdetector_ensemble \
    --runs 100 \
    --save results/langdetector_$(date +%Y%m%d).json \
    --label "v2.1 release"

## Saved Result

File: results/langdetector_20251211.json

{
  "metadata": {
    "model": "langdetector_ensemble",
    "label": "v2.1 release",
    "timestamp": "2025-12-11T10:30:00Z",
    "runs": 100
  },
  "latency": {
    "p50": 12.3,
    "p95": 15.8,
    "p99": 18.2
  },
  "throughput": 78.5,
  "gpu_memory_mb": 1200
}

History: 5 previous results found
Use 'ml-benchmark.sh history langdetector' to view trends
```

---

## Configuration

### 프로파일 설정

`~/.ml-benchmark.yaml`:

```yaml
profiles:
  langdetector-prod:
    url: localhost:15001
    model: langdetector_ensemble
    runs: 100
    warmup: 10
    languages: en,ja,ko,zh
    save_dir: ~/benchmark-results/langdetector

  asr-dev:
    url: localhost:8001
    model: asr_ensemble
    runs: 50
    warmup: 5

defaults:
  runs: 100
  warmup: 5
  timeout: 30
```

### 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `BENCHMARK_RUNS` | 기본 실행 횟수 | 100 |
| `BENCHMARK_WARMUP` | 워밍업 횟수 | 5 |
| `BENCHMARK_TIMEOUT` | 요청 타임아웃 (초) | 30 |

---

## Best Practices

**DO:**
- 워밍업 후 측정 (첫 몇 회는 캐시 미스로 느림)
- 충분한 반복 횟수로 통계적 유의성 확보 (최소 50회)
- 동일 조건에서 비교 (같은 입력, 같은 하드웨어)
- 결과를 JSON으로 저장하여 추적

**DON'T:**
- 워밍업 없이 측정 (불정확한 결과)
- 너무 적은 횟수로 결론 도출
- 다른 워크로드 실행 중 벤치마크
- GPU 온도 높을 때 측정 (스로틀링 영향)

---

## Troubleshooting

### 서버 연결 실패

```bash
# 서버 상태 확인
curl http://localhost:8001/v2/health/ready

# 포트 확인
lsof -i:8001
```

### 높은 지연시간 변동

```bash
# GPU 상태 확인
nvidia-smi

# 다른 프로세스 확인
nvidia-smi --query-compute-apps=pid,name,used_memory --format=csv
```

### 메모리 부족

```bash
# 배치 크기 줄이기
ml-benchmark.sh run --batch-size 1

# GPU 메모리 모니터링
watch -n 1 nvidia-smi
```

### 결과 파일 손상

```bash
# JSON 검증
python -m json.tool results/bench.json

# 백업에서 복구
ls -la results/*.json.bak
```

---

## Resources

| 파일 | 설명 |
|------|------|
| `scripts/ml-benchmark.sh` | 벤치마크 실행 통합 스크립트 |
| `~/.ml-benchmark.yaml` | 프로파일 설정 파일 (사용자 정의) |
