---
name: finops-ai
description: "AI 워크로드 비용 관리 — LLM 비용 구조, token economics·귀속, GPU 최적화, Shift-Left FinOps, model routing. Use when LLM API·GPU 비용이 늘어 토큰 단위로 추적하고 모델 라우팅으로 줄일 때."
---

# FinOps for AI — AI 워크로드 비용 관리

AI/LLM 비용 구조, Token Economics, GPU 비용 최적화, Shift-Left FinOps, Model Routing

## Quick Reference (결정 트리)

```
AI 비용 유형?
    │
    ├─ LLM API 호출 (Token 기반) ──────> Token Economics & Attribution
    │       │
    │       ├─ 비용 급증 ─────> Model Routing (경량↔Frontier)
    │       ├─ 비용 추적 불가 ─> 워크플로우별 Attribution
    │       └─ 예산 초과 ─────> Rate Limiting + Budget Alert
    │
    ├─ GPU 인스턴스 (Training/Inference) ──> GPU 비용 최적화
    │       │
    │       ├─ Training ──────> Spot + Checkpointing
    │       ├─ Inference (안정) ──> Reserved Instance
    │       └─ Inference (가변) ──> Autoscaling + Spot
    │
    └─ 벡터 DB / 스토리지 ─────────────> 임베딩 비용 관리
            │
            └─ 인덱스 크기 최적화, 캐싱

비용 관리 시점?
    │
    ├─ 설계 단계 ──────> Shift-Left (비용 = 설계 제약조건)
    ├─ PR 단계 ────────> Infracost + GPU cost estimation
    ├─ 런타임 ─────────> 실시간 모니터링 + 이상 탐지
    └─ 월간 리뷰 ──────> Attribution 분석 + 최적화
```

---

## AI 비용 구조

### Token 기반 과금 (LLM API)

```
┌────────────────────────────────────────────────┐
│              LLM API 비용 구조                   │
├────────────────────────────────────────────────┤
│                                                  │
│  Input Tokens  ──> 프롬프트 길이에 비례           │
│  Output Tokens ──> 응답 길이에 비례 (보통 3-5x)   │
│  Cached Tokens ──> 90% 할인 (반복 프롬프트)       │
│                                                  │
│  비용 = (input × $/1K) + (output × $/1K)        │
│                                                  │
│  ※ 모델 간 단가 차이 최대 100배                  │
│  ※ Output이 Input보다 단가 높음 (보통 3-5x)      │
└────────────────────────────────────────────────┘
```

| 모델 계층 | Input ($/1M tokens) | Output ($/1M tokens) | 용도 |
|----------|-------------------|---------------------|------|
| Economy (Haiku 5.5) | $0.10 | $0.50 | 분류, 추출, 포맷팅 |
| Standard (Sonnet 5.5) | $2 | $10 | 코드 생성, 분석 |
| Frontier (Opus 5.5) | $4 | $20 | 복잡한 추론, 아키텍처 |
| Top (Fable 5.2) | $8 | $40 | 측정으로 효과를 확인한 작업 |

> Claude 공시가, 2026-11-04 확인 (Fable 5.2 행은 2026-11-11 보강). 가격은 자주 바뀌므로 [공식 표](https://platform.claude.com/docs/en/about-claude/pricing)로 다시 확인한다. Haiku 5.5 는 100k 토큰 초과 프롬프트에 더 높은 단가가 붙는다.

### GPU 인스턴스 비용

| 작업 유형 | 인스턴스 패턴 | 비용 최적화 |
|----------|------------|-----------|
| Training | 대규모, 일시적 | Spot (60-90% 절감) + 체크포인트 |
| Fine-tuning | 중규모, 간헐적 | Spot + 스케줄링 |
| Inference (안정) | 소규모, 상시 | Reserved (40-72% 절감) |
| Inference (가변) | 가변, 스파이크 | Autoscaling + Spot mix |

### AI 비용 변동성 요인

```
비용 스파이크 원인:
├─ 모델 drift → 재시도 증가 → 토큰 2-3배
├─ 프롬프트 비효율 → 불필요하게 긴 context
├─ Agent 루프 → MAX_ITERATIONS 미설정
├─ RAG 과잉 검색 → 대량 embedding 호출
└─ 사용자 급증 → inference 스케일링
```

---

## Shift-Left FinOps for AI

### 비용을 설계 제약조건으로

```
기존 설계 검토:   Latency  ×  Resilience  ×  Compliance
                                    ↓
2026 설계 검토:   Latency  ×  Resilience  ×  Compliance  ×  AI Cost
```

### PR 단위 비용 영향 분석

```yaml
# .github/workflows/ai-cost-check.yaml
name: AI Cost Impact Check
on: [pull_request]
jobs:
  cost-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # 전통 인프라 비용
      - uses: infracost/actions/setup@v3
      - run: infracost diff --path . --format json --out-file /tmp/infracost.json

      # AI 워크로드 비용 추정 (커스텀)
      - name: Estimate AI cost impact
        run: |
          # 모델 변경 감지
          if git diff --name-only origin/main | grep -q "model_config\|llm_config"; then
            echo "::warning::AI 모델 설정 변경 감지 - 비용 영향 검토 필요"
          fi
          # GPU 리소스 변경 감지
          if git diff origin/main -- '*.yaml' | grep -q "gpu\|nvidia"; then
            echo "::warning::GPU 리소스 변경 감지 - 비용 영향 검토 필요"
          fi
```

### Pre-deployment Cost Gating

```
PR 제출 → 비용 추정 → 임계값 체크 → 승인/거부
                          │
                   ├─ < $100/월 증가 → 자동 승인
                   ├─ $100-500/월 → 팀 리드 승인
                   └─ > $500/월 → FinOps 팀 리뷰
```

---

## Token Economics & Attribution

### 비용 Attribution 모델

```
┌─────────────────────────────────────────────────┐
│            AI Cost Attribution                    │
├─────────────────────────────────────────────────┤
│                                                   │
│  Level 1: 모델별     → 어떤 모델이 비용 주도?     │
│  Level 2: 워크플로우별 → 어떤 기능이 비용 주도?    │
│  Level 3: 사용자별   → 누가 비용 주도?            │
│  Level 4: 프롬프트별 → 어떤 프롬프트가 비효율?     │
│                                                   │
│  핵심: 모든 token/request/GPU를                   │
│        제품 메트릭에 매핑                          │
│        → 비용 = Product Telemetry                 │
└─────────────────────────────────────────────────┘
```

### OTel GenAI Metrics → FinOps 연동

```yaml
# OTel Collector pipeline — GenAI metrics → cost calculation
processors:
  transform/ai-cost:
    metric_statements:
      - context: datapoint
        statements:
          # token 사용량을 비용으로 변환
          - set(attributes["cost.usd"],
              attributes["gen_ai.usage.input_tokens"] * 0.000003 +
              attributes["gen_ai.usage.output_tokens"] * 0.000015)
          # 모델별 단가 매핑 (실제로는 lookup table 사용)

exporters:
  prometheus:
    namespace: ai_finops
```

### Grafana 대시보드 쿼리 예시

```promql
# 일별 AI 비용 (모델별)
sum(increase(ai_finops_cost_usd_total[1d])) by (model)

# 워크플로우별 토큰 사용량
sum(rate(gen_ai_client_token_usage_total[1h])) by (workflow, token_type)

# 비용 이상 탐지 (전일 대비 200% 초과)
ai_finops_cost_usd_total
  / (ai_finops_cost_usd_total offset 1d) > 2
```

---

## Model Routing 전략

### 라우팅 규칙 설계

```python
# 개념적 라우팅 로직
def route_request(task: AITask) -> ModelConfig:
    if task.complexity == "simple":
        # 분류, 포맷팅, 추출
        return ModelConfig(model="haiku", max_tokens=1000)

    elif task.complexity == "moderate":
        # 코드 생성, 요약, 번역
        return ModelConfig(model="sonnet", max_tokens=4000)

    elif task.requires_deep_reasoning:
        # 아키텍처, 복잡한 디버깅
        return ModelConfig(model="opus", max_tokens=8000)

    # Fallback: 비용 효율 기본값
    return ModelConfig(model="sonnet", max_tokens=2000)
```

### 라우팅 효과

| 전략 | 월 비용 (예시) | 품질 영향 |
|------|-------------|---------|
| 모든 요청 → Frontier | $10,000 | 최고 (과잉) |
| 모든 요청 → Economy | $500 | 복잡 작업 품질↓ |
| **Smart Routing** | **$2,000-3,000** | **작업별 최적** |

---

## 도구 & 대시보드

| 도구 | 용도 | AI 지원 |
|------|------|---------|
| Kubecost | K8s 비용 분석 | GPU 워크로드 분석 |
| OpenCost | 오픈소스 K8s 비용 | GPU 메트릭 확장 |
| Infracost | IaC 비용 예측 | AI 워크로드 추정 |
| Cast AI | 자동 최적화 | GPU 인스턴스 자동 선택 |
| Vantage | 멀티 클라우드 비용 | AI API 비용 추적 |

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 총 API 비용만 추적 | 최적화 대상 불명 | 워크플로우별 Attribution |
| 모든 요청에 Frontier 모델 | 10-50배 비용 | Model routing |
| GPU 인스턴스 상시 가동 | 유휴 GPU 비용 | 스케줄링 + Spot |
| 프롬프트 캐싱 미적용 | 반복 비용 | Prompt caching (90% 절감) |
| 비용 사후 검토만 | 설계 단계 비효율 | Shift-Left cost gating |
| MAX_ITERATIONS 미설정 | Agent 루프 → 비용 폭증 | 8회 제한 + timeout |

---

## 체크리스트

### Shift-Left
- [ ] PR 비용 영향 분석 파이프라인
- [ ] Pre-deployment cost gating 임계값 설정
- [ ] AI 비용을 설계 리뷰 항목에 포함

### Attribution
- [ ] OTel GenAI metrics 수집
- [ ] 모델별/워크플로우별 비용 대시보드
- [ ] 비용 이상 탐지 알림

### 최적화
- [ ] Model routing 규칙 정의
- [ ] Prompt caching 활성화
- [ ] GPU 인스턴스 Spot/Reserved 전략
- [ ] 유휴 리소스 자동 정리

---

## 참조 스킬

- `finops.md` — 전통 클라우드 FinOps 프레임워크
- `finops-tools.md` — Kubecost, OpenCost, Infracost 도구 상세
- `finops-greenops.md` — GreenOps 탄소 발자국 + 비용 동시 최적화
- `agentic-coding.md` — Model routing, Agent 루프 비용 제어
- `observability-genai.md` — OTel GenAI metrics → FinOps 연동

---

## Sources

- [FinOps Foundation: FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)
- [State of FinOps 2026](https://data.finops.org/)
- [FinOps Shifts Left and Up](https://thecuberesearch.com/finops-2026-shift-left-and-up-as-ai-drives-technology-value/)
- [Zylos: AI Agent Cost Optimization](https://zylos.ai/research/2026-02-19-ai-agent-cost-optimization-token-economics)
- [OpsLyft: FinOps for AI Tokens & GPU](https://opslyft.com/blog/finops-ai-token-gpu-costs)
