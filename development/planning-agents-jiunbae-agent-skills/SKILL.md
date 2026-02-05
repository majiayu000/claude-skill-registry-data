---
name: planning-agents
description: 여러 AI 에이전트(Claude, Codex)가 동일한 주제에 대해 병렬로 기획을 수행하고, 각 결과를 보여준 후 최종 머지된 기획안을 제시합니다. "3명이 기획해주세요"처럼 에이전트 수를 지정할 수 있으며, Claude와 Codex가 랜덤하게 분배됩니다.
---

# Planning Agents (멀티 에이전트 기획)

## Overview

여러 AI 에이전트가 동일한 주제에 대해 독립적으로 기획을 수행하고, 각 아이디어를 병합하여 최종 기획안을 제시하는 스킬입니다.

**지원 에이전트:**
- Claude (현재 세션 또는 별도 호출)
- OpenAI Codex CLI (`codex` 명령어)

**핵심 기능:**
- N명의 에이전트가 병렬로 기획 수행
- 각 에이전트 결과를 개별적으로 표시
- 결과를 머지하여 통합 기획안 생성
- 터미널 출력 + 마크다운 파일 저장

## When to Use

이 스킬은 다음 상황에서 활성화됩니다:
- "기획해주세요", "기획 해줘", "N명이 기획" 등의 키워드가 포함된 요청
- 다양한 관점의 아이디어가 필요할 때
- 브레인스토밍, 기능 기획, 프로젝트 기획 등

**예시 요청:**
- "로그인 기능을 3명이 기획해주세요"
- "2명의 에이전트가 새로운 앱 기능을 기획해줘"
- "5명이서 마케팅 캠페인 기획해주세요"

## Prerequisites

### OpenAI Codex CLI 설치

```bash
# npm으로 설치
npm install -g @openai/codex

# 또는 직접 설치 확인
codex --version
```

### 환경 변수 설정

```bash
# Codex CLI용 OpenAI API 키
export OPENAI_API_KEY="sk-..."

# Claude는 현재 세션을 사용하거나 API 호출 시 필요
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Workflow

### Step 1: 요청 파싱

사용자의 요청에서 다음을 추출합니다:
- **기획 주제**: 무엇을 기획할 것인지
- **에이전트 수**: 몇 명이 기획할 것인지 (기본값: 2명)

```
예: "로그인 기능을 3명이 기획해주세요"
→ 주제: "로그인 기능"
→ 에이전트 수: 3
```

### Step 2: 에이전트 랜덤 분배

에이전트 수에 따라 Claude와 Codex를 랜덤하게 분배합니다:

```python
import random

def assign_agents(count):
    agents = []
    for i in range(count):
        agent_type = random.choice(["claude", "codex"])
        agents.append({
            "id": i + 1,
            "type": agent_type,
            "name": f"Agent {i + 1} ({agent_type.capitalize()})"
        })
    return agents

# 예: 3명 → [claude, codex, claude] 또는 [codex, codex, claude] 등
```

### Step 3: 병렬 기획 실행

각 에이전트에게 동일한 기획 프롬프트를 전달합니다:

**Claude 호출:**
```bash
# Claude API 또는 현재 세션에서 처리
```

**Codex CLI 호출:**
```bash
# 비대화형 실행 (exec 서브커맨드 사용)
codex exec "다음 주제에 대해 상세한 기획안을 작성해주세요: [주제]

기획안에는 다음을 포함해주세요:
1. 핵심 아이디어 및 목표
2. 주요 기능/구성 요소
3. 구현 접근 방식
4. 예상 도전과제 및 해결책
5. 성공 지표"
```

### Step 4: 개별 결과 출력

각 에이전트의 기획 결과를 순서대로 표시합니다:

```markdown
---
## Agent 1 (Claude) 기획안

[Claude의 기획 내용]

---
## Agent 2 (Codex) 기획안

[Codex의 기획 내용]

---
## Agent 3 (Claude) 기획안

[Claude의 기획 내용]
```

### Step 5: 결과 머지

모든 기획안을 분석하여 통합 기획안을 생성합니다:

```markdown
---
# 통합 기획안

## 공통 아이디어
- 여러 에이전트가 동의한 핵심 요소들

## 고유 아이디어
- Agent 1만 제안: ...
- Agent 2만 제안: ...

## 최종 권장 기획안
[머지된 최종 기획안]

## 의사결정 포인트
- [ ] 선택 1: A 방식 vs B 방식
- [ ] 선택 2: ...
```

### Step 6: 결과 저장

터미널 출력과 함께 마크다운 파일로 저장합니다:

```bash
# 저장 위치
./planning_output/[주제]_[timestamp].md
```

## Examples

### 예시 1: 기본 사용

```
사용자: 사용자 인증 기능을 2명이 기획해주세요
```

**실행 과정:**
1. 주제 파싱: "사용자 인증 기능"
2. 에이전트 분배: [Claude, Codex]
3. 병렬 실행
4. 개별 결과 출력
5. 머지 결과 출력
6. 파일 저장

### 예시 2: 다수 에이전트

```
사용자: 모바일 앱 온보딩 플로우를 5명이 기획해주세요
```

**실행 과정:**
1. 5개 에이전트 랜덤 분배: 예) [Claude, Codex, Codex, Claude, Claude]
2. 5개 병렬 기획 실행
3. 5개 개별 결과 표시
4. 통합 머지 기획안 생성

### 예시 3: 상세 주제

```
사용자: "실시간 채팅 기능 (WebSocket 기반, 읽음 확인, 타이핑 표시 포함)"을 3명이 기획해주세요
```

## Scripts

### 메인 실행 스크립트

```bash
python scripts/planner.py \
  --topic "기획 주제" \
  --agents 3 \
  --output ./planning_output
```

### 스크립트 구조

```
planning-agents/
├── SKILL.md
├── scripts/
│   ├── planner.py          # 메인 오케스트레이터
│   ├── agent_runner.py     # 에이전트 실행 모듈
│   └── merger.py           # 결과 머지 모듈
└── templates/
    └── planning_prompt.md  # 기획 프롬프트 템플릿
```

## Configuration

### 기본 설정

```yaml
defaults:
  agent_count: 2
  timeout: 120  # 각 에이전트 타임아웃 (초)
  output_dir: "./planning_output"

codex:
  model: "o4-mini"  # 또는 gpt-4o

claude:
  use_current_session: true  # 현재 세션 사용 여부
```

## Best Practices

**DO:**
- 명확하고 구체적인 기획 주제 제시
- 에이전트 수는 2-5명 권장 (너무 많으면 비용/시간 증가)
- 결과물을 검토하고 필요시 추가 기획 요청

**DON'T:**
- 너무 광범위한 주제 (예: "앱 전체를 기획해주세요")
- 10명 이상의 에이전트 사용 (비효율적)
- 결과를 검토 없이 그대로 사용

## Output Format

### 터미널 출력

```
========================================
  멀티 에이전트 기획 시작
  주제: [주제명]
  에이전트 수: [N]명
  분배: Claude(2) / Codex(1)
========================================

[Agent 1 - Claude] 기획 중...
✓ Agent 1 완료

[Agent 2 - Codex] 기획 중...
✓ Agent 2 완료

[Agent 3 - Claude] 기획 중...
✓ Agent 3 완료

========================================
  개별 기획안
========================================

--- Agent 1 (Claude) ---
[내용]

--- Agent 2 (Codex) ---
[내용]

--- Agent 3 (Claude) ---
[내용]

========================================
  통합 기획안
========================================

[머지된 내용]

========================================
  결과 저장됨: ./planning_output/[파일명].md
========================================
```

### 저장 파일 형식

```markdown
# 멀티 에이전트 기획: [주제]

- 생성일시: 2024-12-09 10:30:00
- 에이전트 수: 3 (Claude: 2, Codex: 1)

---

## Agent 1 (Claude) 기획안
[내용]

---

## Agent 2 (Codex) 기획안
[내용]

---

## Agent 3 (Claude) 기획안
[내용]

---

# 통합 기획안

## 공통 아이디어
...

## 고유 아이디어
...

## 최종 권장안
...

## 의사결정 체크리스트
- [ ] ...
```

## Troubleshooting

### Codex CLI 오류

```bash
# 설치 확인
codex --version

# API 키 확인
echo $OPENAI_API_KEY

# 직접 테스트 (비대화형)
codex exec "Hello"
```

### 타임아웃 발생

- 타임아웃 값 증가: `--timeout 180`
- 에이전트 수 줄이기

### 결과가 너무 짧음

- 프롬프트를 더 구체적으로 작성
- 기획 범위를 명확히 지정
