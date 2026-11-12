---
name: dx-ai-agents
description: "AI 코딩 에이전트 거버넌스 — 엔지니어 역할 변화, 성숙도 모델, Copilot·Claude Code 통합, 권한 범위, 금지 사항, 작업 완료 기준. Use when 조직의 AI 에이전트 사용 정책과 규칙을 정할 때, 협업 구성은 dx-ai-agents-orchestration 을 쓴다."
---

# AI Agents 플랫폼 통합 가이드

AI 코딩 에이전트 거버넌스, Copilot/Claude 통합, 엔터프라이즈 AI 정책

## Quick Reference (결정 트리)

```
AI 에이전트 유형?
    │
    ├─ Copilot (보조) ────────> 실시간 코드 제안, 인간 입력 필수
    │       │
    │       └─ GitHub Copilot, Cursor, Codeium
    │
    ├─ Agent (자율) ──────────> 이슈 → PR 자동 생성, 비동기 작업
    │       │
    │       └─ Copilot Coding Agent, Claude Code, Devin
    │
    └─ 하이브리드 ────────────> 일부 자율 + 인간 검토
            │
            └─ 권장: PR 자동 생성 + 인간 머지

2026 엔지니어 역할 전환?
    │
    ├─ 기존: 코드 작성자 (Implementer)
    │
    └─ 2026: Agent 오케스트레이터 (Supervisor)
            ├─ 시스템 설계 & 아키텍처
            ├─ Agent 지시 & 조율
            ├─ 출력 품질 평가
            └─ 전략적 문제 분해
```

---

## CRITICAL: 2026 엔지니어 역할 변화

코딩의 전술적 작업(작성, 디버깅, 유지보수)이 AI로 이동.
엔지니어 가치는 **설계, 조율, 평가, 전략적 분해**에 집중.

| 영역 | 기존 역할 | 2026 역할 |
|------|---------|---------|
| 코드 작성 | 직접 구현 | Agent에 지시, 결과 검증 |
| 코드 리뷰 | 동료 코드 리뷰 | **Agent 코드 리뷰** (인지 부하↑) |
| 아키텍처 | 설계 + 구현 | 설계 (구현은 Agent) |
| 테스트 | 직접 작성 | TDD 계약 정의, Agent가 작성 |
| 디버깅 | 직접 분석 | Agent에 진단 지시, 근본 원인 판단 |

### Context Engineering (Agent 품질의 핵심)

Agent 출력 품질 = 주입된 컨텍스트 품질. **CLAUDE.md / Rules를 사람과 AI 모두 읽을 수 있게** 작성.

- "좋은 코드를 작성하라" (X) → "Guard Clause, 메서드 50줄 이내, p99 < 500ms" (O)
- BAD/GOOD 예시 코드 포함
- 금지 패턴 명시 (anti-patterns)

### TDD with Agents

```
1. 인간: 요구사항 + 수용 기준 정의
2. Agent: 테스트 작성 (수용 기준 기반)
3. 인간: 테스트 검토 & 승인 ← 계약 확정
4. Agent: 테스트 통과하는 코드 구현
5. 규칙: Agent는 테스트 수정 불가 (테스트 = 계약)
```

---

## CRITICAL: AI Agent 성숙도 모델

```
┌─────────────────────────────────────────────────────────────────┐
│                AI Agent Maturity Model (2026)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Level 1: Assisted       Level 2: Automated      Level 3: Autonomous │
│  ────────────────       ─────────────────       ─────────────────    │
│  - 코드 자동완성         - PR 자동 생성          - 이슈 할당 → 완료    │
│  - 인라인 제안          - 테스트 자동 작성       - 자체 코드 리뷰      │
│  - 문서 생성 보조        - 리팩토링 제안         - 배포 결정           │
│                                                                  │
│  인간 개입: 항상         인간 개입: 검토/승인     인간 개입: 예외만     │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 2026 권장: Level 2 (Automated) + 엄격한 거버넌스         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Copilot vs Agent 비교

| 특성 | Copilot (보조) | Agent (자율) |
|------|---------------|--------------|
| 작동 방식 | 실시간 제안 | 비동기 작업 |
| 인간 개입 | 매 줄마다 | 작업 완료 후 |
| 컨텍스트 | 현재 파일 | 전체 저장소 |
| 출력물 | 코드 스니펫 | PR, 커밋 |
| 리스크 | 낮음 | 중간~높음 |
| 거버넌스 | 기본 | **필수** |

---

## AI 에이전트 거버넌스

### CRITICAL: 엔터프라이즈 정책 프레임워크

```yaml
# ai-governance-policy.yaml
apiVersion: platform.company.io/v1
kind: AIAgentPolicy
metadata:
  name: enterprise-ai-policy
spec:
  # 1. 접근 제어
  access:
    allowedRepositories:
      - "org/*"                    # 전체 조직
      - "!org/secrets-*"           # 시크릿 저장소 제외
      - "!org/compliance-*"        # 컴플라이언스 저장소 제외

    allowedBranches:
      - "feature/*"
      - "fix/*"
      - "ai/*"                     # AI 전용 브랜치
    deniedBranches:
      - "main"
      - "release/*"
      - "hotfix/*"

  # 2. 권한 수준
  permissions:
    codeGeneration: true
    codeModification: true
    prCreation: true
    prMerge: false                 # 인간만 머지 가능
    issueCreation: true
    issueClose: false

  # 3. 리소스 제한
  resourceLimits:
    maxTokensPerRequest: 100000
    maxRequestsPerHour: 100
    maxConcurrentTasks: 5
    budgetPerMonth: 500            # USD

  # 4. 콘텐츠 정책
  contentPolicy:
    scanForSecrets: true
    scanForPII: true
    requireCodeReview: true
    minReviewers: 1

  # 5. 감사 로깅
  audit:
    logAllRequests: true
    logResponses: true
    retentionDays: 90
```

### RBAC for AI Agents

```yaml
# ai-agent-rbac.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ai-agent-developer
rules:
  # 읽기 권한
  - apiGroups: [""]
    resources: ["configmaps", "services", "pods"]
    verbs: ["get", "list", "watch"]

  # 제한된 쓰기 권한
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "patch"]
    # 삭제, 생성 권한 없음

  # Secret 접근 금지 (명시적)
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: []                      # 모든 동작 금지
```

---

## GitHub Copilot 통합

### 조직 설정

```yaml
# .github/copilot-config.yml
copilot:
  features:
    code_completion: true
    chat: true
    cli: true
    coding_agent: true

  content_exclusions:
    - "**/.env*"
    - "**/secrets/**"
    - "**/*credentials*"
    - "**/private/**"

  code_references:
    enable_suggestions_matching_public_code: false
```

### Copilot Coding Agent 워크플로우

```yaml
# .github/workflows/copilot-agent.yaml
name: Copilot Agent Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  detect-ai-pr:
    runs-on: ubuntu-latest
    outputs:
      is_ai_generated: ${{ steps.check.outputs.is_ai }}
    steps:
      - name: Check if AI-generated
        id: check
        run: |
          if [[ "${{ github.event.pull_request.user.login }}" == *"[bot]"* ]] || \
             [[ "${{ github.event.pull_request.head.ref }}" == "copilot/"* ]]; then
            echo "is_ai=true" >> $GITHUB_OUTPUT
          else
            echo "is_ai=false" >> $GITHUB_OUTPUT
          fi

  ai-pr-validation:
    needs: detect-ai-pr
    if: needs.detect-ai-pr.outputs.is_ai_generated == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Assign Human Reviewers
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.pulls.requestReviewers({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.payload.pull_request.number,
              reviewers: ['senior-dev-1', 'senior-dev-2']
            });

      - name: Add AI Label
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.payload.pull_request.number,
              labels: ['ai-generated', 'needs-human-review']
            });
```

---

## Claude Code 통합

### 프로젝트 설정 (CLAUDE.md)

```markdown
# CLAUDE.md - AI 에이전트 가이드라인

## 권한 범위
- 코드 생성: 허용
- 테스트 작성: 허용
- 리팩토링: 허용 (기존 동작 유지)
- 설정 파일 수정: 검토 필요
- 시크릿/인증 관련: 금지

## 코드 스타일
- 기존 패턴 준수
- 새 의존성 추가 전 확인 요청
- 주석은 복잡한 로직에만

## 금지 사항
- .env 파일 수정/생성 금지
- credentials, secrets 관련 코드 금지
- 프로덕션 데이터베이스 직접 접근 금지
- 외부 API 키 하드코딩 금지

## 작업 완료 기준
- 모든 테스트 통과
- 린트 에러 없음
- 기존 기능 회귀 없음
```

### MCP (Model Context Protocol) 서버 설정

```json
// .mcp.json (프로젝트 루트)
{
  "mcpServers": {
    "github": {
      "command": "mcp-server-github",
      "args": ["--repo", "org/repo"]
    },
    "kubernetes": {
      "command": "mcp-server-kubernetes",
      "args": ["--context", "development"]
    },
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": ["--root", "/workspace"]
    }
  }
}
```

> `.mcp.json` 에는 서버별 권한 필드가 없다. 접근 범위는 서버 인자(`--context development`, `--root /workspace`)와 토큰 스코프로 좁히고, 도구 호출 허용 여부는 Claude Code settings 의 `permissions` 규칙으로 정한다 ([MCP docs](https://code.claude.com/docs/en/mcp)).

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| AI에게 프로덕션 접근 허용 | 심각한 보안 리스크 | 개발 환경만 허용 |
| AI PR 무검토 머지 | 품질/보안 문제 | 인간 리뷰 필수 |
| 토큰 예산 미설정 | 비용 폭증 | 팀별 예산 할당 |
| AI 생성 코드 구분 안함 | 품질 추적 불가 | 라벨링 필수 |
| 시크릿 필터링 미적용 | 키 노출 | 콘텐츠 필터 설정 |
| AI 메트릭 미수집 | ROI 증명 불가 | 사용량/품질 추적 |

---

## 체크리스트

### 거버넌스
- [ ] AI 에이전트 정책 문서화
- [ ] RBAC 설정 (저장소/브랜치 제한)
- [ ] 콘텐츠 필터링 (시크릿, PII)
- [ ] 감사 로깅 활성화

### 통합
- [ ] Copilot 조직 설정
- [ ] Claude CLAUDE.md 작성
- [ ] MCP 서버 설정
- [ ] CI/CD 파이프라인 연동

---

## 참조 스킬

- `dx-ai-agents-orchestration.md` — 멀티 에이전트 협업, 가드레일, Self-Healing, 메트릭
- `agentic-coding.md` — Agentic Coding 4가지 모드, Agent Supervision, Code Review 변화
- `spring-ai.md` — Spring AI 기반 LLM 통합, MCP, Advisors
- `finops-ai.md` — AI 비용 관리, Model Routing 비용 최적화
- `/ai:dx-ai-security` — 보안/품질
- `/dx:dx-metrics` — 메트릭 수집

---

## Sources

- [GitHub Copilot](https://docs.github.com/en/copilot)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [MCP Protocol](https://modelcontextprotocol.io/)
