---
name: multi-llm-agent
description: 여러 LLM(OpenAI, Gemini, Ollama 등)을 통합하여 멀티 에이전트 협업을 수행합니다. 역할 분담, 토론/합의, 체인 파이프라인, 병렬 처리 등 다양한 협업 패턴을 지원하며, 사용 시점에 시나리오를 동적으로 구성할 수 있습니다. 복잡한 작업을 여러 LLM에게 분산하여 더 나은 결과를 얻고 싶을 때 사용하세요.
---

# Multi-LLM Agent

## Overview

여러 LLM을 오케스트레이션하여 복잡한 작업을 협업으로 수행하는 스킬입니다.

**지원 LLM 프로바이더:**
- OpenAI (GPT-4, GPT-4o, o1, o3)
- Google Gemini (gemini-pro, gemini-2.0-flash)
- Anthropic Claude (API 직접 호출 시)
- Ollama (로컬 LLM)
- 기타 OpenAI 호환 API

**지원 협업 패턴:**
- **역할 분담**: 각 LLM이 전문 역할을 맡아 협업
- **토론/합의**: 여러 LLM이 의견을 교환하고 합의 도출
- **체인 파이프라인**: 순차적으로 결과를 전달하며 처리
- **병렬 + 종합**: 동시에 작업 후 결과를 종합

## When to Use

이 스킬은 다음 상황에서 활성화됩니다:
- "여러 LLM으로", "멀티 에이전트", "LLM 협업" 등의 키워드가 포함된 요청
- 복잡한 작업을 여러 관점에서 처리해야 할 때
- 코드 리뷰, 문서 분석, 아이디어 브레인스토밍 등 협업이 유용한 작업

## Prerequisites

### 환경 변수 설정

사용할 LLM 프로바이더에 맞는 API 키를 환경 변수로 설정하세요:

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Google Gemini
export GOOGLE_API_KEY="..."

# Anthropic (선택적)
export ANTHROPIC_API_KEY="sk-ant-..."

# Ollama는 로컬 실행으로 API 키 불필요
# 기본 URL: http://localhost:11434
```

### 의존성 설치

```bash
pip install openai google-generativeai requests pyyaml
```

## Workflow

### Step 1: 작업 분석 및 패턴 선택

사용자의 요청을 분석하여 적합한 협업 패턴을 선택합니다:

| 작업 유형 | 권장 패턴 | 예시 |
|-----------|-----------|------|
| 코드 작성 + 리뷰 | 역할 분담 | GPT가 코드 작성 → Gemini가 리뷰 |
| 의사결정, 설계 | 토론/합의 | 여러 LLM이 장단점 토론 |
| 문서 처리 파이프라인 | 체인 | 요약 → 번역 → 포맷팅 |
| 다양한 관점 필요 | 병렬 + 종합 | 여러 LLM이 각자 분석 후 종합 |

### Step 2: 에이전트 구성

`scripts/orchestrator.py`를 사용하여 에이전트를 구성합니다:

```bash
python scripts/orchestrator.py \
  --pattern "role_based" \
  --agents '[
    {"name": "coder", "provider": "openai", "model": "gpt-4o", "role": "코드 작성"},
    {"name": "reviewer", "provider": "gemini", "model": "gemini-2.0-flash", "role": "코드 리뷰"},
    {"name": "tester", "provider": "ollama", "model": "codellama", "role": "테스트 생성"}
  ]' \
  --task "사용자 인증 기능 구현"
```

### Step 3: 협업 실행

선택한 패턴에 따라 협업이 실행됩니다:

**역할 분담 (Role-Based):**
```python
# scripts/patterns/role_based.py 사용
result = execute_role_based(
    agents=configured_agents,
    task="사용자 인증 기능 구현",
    workflow=[
        {"agent": "coder", "action": "implement"},
        {"agent": "reviewer", "action": "review", "input_from": "coder"},
        {"agent": "tester", "action": "generate_tests", "input_from": "coder"}
    ]
)
```

**토론/합의 (Discussion):**
```python
# scripts/patterns/discussion.py 사용
result = execute_discussion(
    agents=configured_agents,
    topic="마이크로서비스 vs 모놀리식 아키텍처 선택",
    rounds=3,  # 토론 라운드 수
    consensus_threshold=0.7  # 합의 임계값
)
```

**체인 파이프라인 (Chain):**
```python
# scripts/patterns/chain.py 사용
result = execute_chain(
    pipeline=[
        {"agent": "analyzer", "prompt": "문서 분석 및 핵심 추출"},
        {"agent": "translator", "prompt": "한국어로 번역"},
        {"agent": "formatter", "prompt": "마크다운 포맷팅"}
    ],
    input_data=document_content
)
```

**병렬 + 종합 (Parallel):**
```python
# scripts/patterns/parallel.py 사용
result = execute_parallel(
    agents=configured_agents,
    task="이 코드의 보안 취약점 분석",
    aggregation="synthesize"  # 또는 "vote", "best_of"
)
```

### Step 4: 결과 처리

각 패턴은 다음 형태의 결과를 반환합니다:

```python
{
    "pattern": "role_based",
    "agents_used": ["coder", "reviewer", "tester"],
    "execution_log": [...],
    "final_result": "...",
    "metadata": {
        "total_tokens": 15000,
        "execution_time": 45.2,
        "cost_estimate": "$0.12"
    }
}
```

## Examples

### 예시 1: 코드 리뷰 파이프라인

```bash
python scripts/orchestrator.py \
  --pattern "role_based" \
  --config config/code_review.yaml \
  --input "path/to/code.py"
```

**config/code_review.yaml:**
```yaml
agents:
  - name: reviewer_security
    provider: openai
    model: gpt-4o
    role: 보안 관점 리뷰
    system_prompt: "보안 전문가로서 코드를 검토하세요."

  - name: reviewer_performance
    provider: gemini
    model: gemini-2.0-flash
    role: 성능 관점 리뷰
    system_prompt: "성능 최적화 전문가로서 코드를 검토하세요."

  - name: reviewer_clean_code
    provider: ollama
    model: llama3.2
    role: 클린 코드 관점 리뷰
    system_prompt: "클린 코드 원칙에 따라 코드를 검토하세요."

workflow:
  pattern: parallel
  aggregation: synthesize
```

### 예시 2: 브레인스토밍 토론

```bash
python scripts/orchestrator.py \
  --pattern "discussion" \
  --topic "새로운 모바일 앱 기능 아이디어" \
  --agents '[
    {"name": "innovator", "provider": "openai", "model": "gpt-4o"},
    {"name": "critic", "provider": "gemini", "model": "gemini-2.0-flash"},
    {"name": "pragmatist", "provider": "ollama", "model": "llama3.2"}
  ]' \
  --rounds 3
```

### 예시 3: 문서 처리 체인

```bash
python scripts/orchestrator.py \
  --pattern "chain" \
  --pipeline '[
    {"agent": "extractor", "task": "핵심 정보 추출"},
    {"agent": "analyzer", "task": "SWOT 분석"},
    {"agent": "writer", "task": "경영진 요약 보고서 작성"}
  ]' \
  --input "path/to/document.pdf"
```

## Configuration

### 전역 설정 (config/settings.yaml)

```yaml
defaults:
  timeout: 120  # 각 LLM 호출 타임아웃 (초)
  max_retries: 3
  temperature: 0.7

providers:
  openai:
    base_url: "https://api.openai.com/v1"
    default_model: "gpt-4o"

  gemini:
    default_model: "gemini-2.0-flash"

  ollama:
    base_url: "http://localhost:11434"
    default_model: "llama3.2"

logging:
  level: "INFO"
  save_conversations: true
  output_dir: "./logs"
```

### 에이전트 프리셋 (config/agents.yaml)

```yaml
presets:
  code_team:
    - name: architect
      provider: openai
      model: gpt-4o
      role: 시스템 설계
    - name: developer
      provider: gemini
      model: gemini-2.0-flash
      role: 구현
    - name: reviewer
      provider: ollama
      model: codellama
      role: 코드 리뷰

  analysis_team:
    - name: researcher
      provider: openai
      model: gpt-4o
      role: 조사 및 분석
    - name: critic
      provider: gemini
      model: gemini-2.0-flash
      role: 비판적 검토
    - name: synthesizer
      provider: openai
      model: gpt-4o
      role: 종합 및 결론
```

## Best Practices

**DO:**
- 작업에 맞는 협업 패턴 선택
- 각 에이전트에 명확한 역할과 시스템 프롬프트 부여
- 비용 효율을 위해 간단한 작업은 로컬 LLM(Ollama) 활용
- 결과 로깅으로 협업 과정 추적

**DON'T:**
- 단순 작업에 불필요하게 여러 LLM 사용
- API 키를 코드에 하드코딩
- 토론 라운드를 과도하게 설정 (비용 증가)
- 타임아웃 없이 실행 (무한 대기 방지)

## Troubleshooting

### API 키 오류
```bash
# 환경 변수 확인
echo $OPENAI_API_KEY
echo $GOOGLE_API_KEY
```

### Ollama 연결 실패
```bash
# Ollama 실행 확인
ollama list
curl http://localhost:11434/api/tags
```

### 타임아웃 발생
- 타임아웃 값 증가: `--timeout 180`
- 모델 변경: 더 빠른 모델 사용 (gpt-4o-mini, gemini-flash)

## Resources

- `scripts/llm_client.py`: 통합 LLM 클라이언트
- `scripts/orchestrator.py`: 멀티 에이전트 오케스트레이터
- `scripts/patterns/`: 협업 패턴 구현
- `references/llm_providers.md`: LLM 프로바이더 상세 가이드
- `config/`: 설정 파일 예시
