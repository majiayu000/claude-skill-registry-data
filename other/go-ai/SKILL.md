---
name: go-ai
description: "Go 백엔드 AI 통합 — Genkit·LangChainGo·Eino 비교, Tool Calling, RAG(PgVector), mcp-go 로 MCP 서버 구현. Use when Go 서비스에 LLM 기능을 붙이거나 RAG·MCP 서버를 만들 때."
---

# Go AI Integration Patterns

Go 백엔드에서 LLM 통합, 프레임워크 선택 (Genkit/LangChainGo/Eino), Tool Calling, RAG, MCP 서버 구현

## Quick Reference (결정 트리)

```
Go AI 프레임워크 선택?
    │
    ├─ 빠른 프로토타입 → 프로덕션 ──> Genkit Go 1.0 (Google)
    │       └─ 플러그인 아키텍처, MCP 호스트, 트레이싱 내장
    │
    ├─ 최대 유연성, 커뮤니티 ────────> LangChainGo
    │       └─ 20+ 프로바이더, 가장 큰 에코시스템
    │
    ├─ 대규모 트래픽, ByteDance 검증 ──> Eino (CloudWeGo)
    │       └─ Go-first 설계, goroutine 네이티브
    │
    ├─ 엔터프라이즈 멀티에이전트 ────> Google ADK Go 1.0
    │       └─ A2A 프로토콜, Visual Agent Designer
    │
    └─ Claude MCP 서버만 필요 ───────> mcp-go (공식 SDK)
            └─ MCP 서버/클라이언트 구현

AI 기능 선택?
    │
    ├─ 단순 LLM 호출 ──────> 직접 API 호출 (net/http)
    ├─ Tool Calling ───────> Genkit / LangChainGo
    ├─ Structured Output ──> Genkit (스키마 검증) / JSON 파싱
    ├─ RAG 파이프라인 ─────> LangChainGo + PgVector
    ├─ MCP 서버 구현 ──────> mcp-go SDK
    └─ Agent 워크플로우 ───> Genkit / ADK (멀티에이전트)
```

---

## 프레임워크 비교

| 항목 | Genkit Go 1.0 | LangChainGo | Eino | ADK Go 1.0 | mcp-go |
|------|-------------|------------|------|----------|--------|
| 주체 | Google | 커뮤니티 | ByteDance | Google | MCP 공식 |
| 성숙도 | **GA** | Stable | Stable | **GA** | Stable |
| MCP 지원 | 호스트 내장 | - | - | 내장 | **네이티브** |
| Tool Calling | O | O | O | O | - |
| Structured Output | O | O | O | O | - |
| RAG | O | O | O | - | - |
| 트레이싱 | OTel 내장 | 수동 | O | OTel | - |
| 에이전트 | 기본 | 기본 | 고급 | **멀티에이전트** | - |
| 프로바이더 수 | 10+ | **20+** | 10+ | Google 중심 | - |

### 선택 기준

```
Spring AI 대응? → Genkit Go (가장 유사한 포지션)
LangChain 경험? → LangChainGo (익숙한 API)
성능 극한?     → Eino (ByteDance 대규모 검증)
MCP 서버?      → mcp-go (Claude Code 연동)
```

---

## Genkit Go 기본 사용

### 설치 & 설정

```bash
go get github.com/firebase/genkit/go
go get github.com/firebase/genkit/go/plugins/googlegenai  # Google AI
# 또는
go get github.com/firebase/genkit/go/plugins/ollama       # 로컬 Ollama
```

### 기본 LLM 호출

```go
package main

import (
    "context"
    "fmt"

    "github.com/firebase/genkit/go/ai"
    "github.com/firebase/genkit/go/genkit"
    "github.com/firebase/genkit/go/plugins/googlegenai"
)

func main() {
    ctx := context.Background()
    g, err := genkit.Init(ctx, genkit.WithPlugins(&googlegenai.GoogleAI{}))
    if err != nil {
        panic(err)
    }

    // 모델 참조
    model := googlegenai.GoogleAIModel(g, "gemini-2.0-flash")

    // 단순 호출
    resp, err := ai.Generate(ctx, g, ai.WithModel(model),
        ai.WithTextPrompt("Go 언어의 장점 3가지를 알려주세요"))
    if err != nil {
        panic(err)
    }
    fmt.Println(resp.Text())
}
```

### Structured Output

```go
type CodeReview struct {
    Summary string  `json:"summary"`
    Score   int     `json:"score"`
    Issues  []Issue `json:"issues"`
}

type Issue struct {
    Severity    string `json:"severity"`
    File        string `json:"file"`
    Line        int    `json:"line"`
    Description string `json:"description"`
}

// Genkit Structured Output
resp, err := ai.Generate(ctx, g,
    ai.WithModel(model),
    ai.WithTextPrompt("다음 코드를 리뷰해주세요:\n"+code),
    ai.WithOutputType(ai.DefineType[CodeReview](g, "CodeReview")),
)
var review CodeReview
resp.Output(&review) // 자동 JSON → Go struct 변환
```

### Tool Calling

```go
// Go 함수를 AI 도구로 등록
getPodsTool := ai.DefineTool(g, "get_pods",
    "쿠버네티스 Pod 상태를 조회합니다",
    func(ctx context.Context, input struct {
        Namespace string `json:"namespace" jsonschema:"description=네임스페이스"`
    }) ([]PodStatus, error) {
        return k8sClient.ListPods(ctx, input.Namespace)
    },
)

searchLogsTool := ai.DefineTool(g, "search_logs",
    "에러 로그를 검색합니다",
    func(ctx context.Context, input struct {
        Service string `json:"service"`
        Minutes int    `json:"minutes"`
    }) ([]LogEntry, error) {
        return lokiClient.SearchErrors(ctx, input.Service, input.Minutes)
    },
)

// AI가 필요에 따라 도구를 자동 선택/호출
resp, err := ai.Generate(ctx, g,
    ai.WithModel(model),
    ai.WithTextPrompt("payment-service에서 최근 에러가 있나요?"),
    ai.WithTools(getPodsTool, searchLogsTool),
)
```

---

## MCP 서버 구현 (mcp-go)

Claude Code / Claude Desktop과 연동할 Go MCP 서버 구현.

```go
package main

import (
    "context"
    "fmt"

    "github.com/modelcontextprotocol/go-sdk/mcp"
    "github.com/modelcontextprotocol/go-sdk/server"
)

func main() {
    s := server.NewMCPServer("go-devops-tools", "1.0.0")

    // MCP 도구 등록
    s.AddTool(mcp.Tool{
        Name:        "get_pod_status",
        Description: "K8s Pod 상태를 조회합니다",
        InputSchema: mcp.ToolInputSchema{
            Type: "object",
            Properties: map[string]any{
                "namespace": map[string]any{
                    "type":        "string",
                    "description": "쿠버네티스 네임스페이스",
                },
            },
            Required: []string{"namespace"},
        },
    }, handleGetPodStatus)

    s.AddTool(mcp.Tool{
        Name:        "run_go_test",
        Description: "Go 테스트를 실행합니다",
        InputSchema: mcp.ToolInputSchema{
            Type: "object",
            Properties: map[string]any{
                "package": map[string]any{
                    "type":        "string",
                    "description": "테스트할 패키지 경로",
                },
            },
        },
    }, handleRunGoTest)

    // stdio 전송으로 실행 (Claude Code 연동)
    if err := server.ServeStdio(s); err != nil {
        panic(err)
    }
}

func handleGetPodStatus(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
    ns := req.Params.Arguments["namespace"].(string)
    pods, err := k8sClient.ListPods(ctx, ns)
    if err != nil {
        return mcp.NewToolResultError(err.Error()), nil
    }
    return mcp.NewToolResultText(fmt.Sprintf("%+v", pods)), nil
}
```

### Claude Code에 MCP 서버 등록

```json
// .claude/settings.json
{
  "mcpServers": {
    "go-devops": {
      "command": "./bin/go-devops-mcp",
      "args": []
    }
  }
}
```

---

## RAG 패턴 (LangChainGo + PgVector)

```go
import (
    "github.com/tmc/langchaingo/embeddings"
    "github.com/tmc/langchaingo/llms/anthropic"
    "github.com/tmc/langchaingo/vectorstores/pgvector"
    "github.com/tmc/langchaingo/schema"
)

func setupRAG(ctx context.Context) error {
    // 1. Embeddings 모델
    embedder, _ := embeddings.NewEmbedder(
        embeddings.WithModel("text-embedding-3-small"),
    )

    // 2. Vector Store (PgVector)
    store, _ := pgvector.New(ctx,
        pgvector.WithConnectionURL("postgres://localhost/aidb"),
        pgvector.WithEmbedder(embedder),
    )

    // 3. 문서 추가
    docs := []schema.Document{
        {PageContent: "Go에서 goroutine은 경량 스레드입니다..."},
        {PageContent: "channel은 goroutine 간 통신 수단입니다..."},
    }
    store.AddDocuments(ctx, docs)

    // 4. 유사 검색 + LLM 응답
    results, _ := store.SimilaritySearch(ctx, "Go 동시성", 3)

    llm, _ := anthropic.New(anthropic.WithModel("claude-sonnet-5-5"))
    // results를 컨텍스트로 주입하여 LLM 호출
    // ...
    return nil
}
```

---

## Go의 AI 강점 활용

### goroutine 병렬 LLM 호출

```go
func parallelLLMCalls(ctx context.Context, tasks []string) []string {
    results := make([]string, len(tasks))
    var wg sync.WaitGroup

    // 동시성 제한 (API rate limit 고려)
    sem := make(chan struct{}, 5)

    for i, task := range tasks {
        wg.Add(1)
        go func(idx int, t string) {
            defer wg.Done()
            sem <- struct{}{}        // 세마포어 획득
            defer func() { <-sem }() // 세마포어 반환

            resp, err := ai.Generate(ctx, g,
                ai.WithModel(model),
                ai.WithTextPrompt(t),
            )
            if err == nil {
                results[idx] = resp.Text()
            }
        }(i, task)
    }

    wg.Wait()
    return results
}
```

### Model Routing (비용 최적화)

```go
type ModelRouter struct {
    economy  ai.Model // Haiku — 분류, 포맷팅
    standard ai.Model // Sonnet — 코드 생성
    premium  ai.Model // Opus — 아키텍처, 복잡한 추론
}

func (r *ModelRouter) Route(ctx context.Context, task Task) (string, error) {
    var model ai.Model
    switch task.Complexity {
    case Simple:
        model = r.economy
    case Moderate:
        model = r.standard
    case Complex:
        model = r.premium
    }

    resp, err := ai.Generate(ctx, g,
        ai.WithModel(model),
        ai.WithTextPrompt(task.Prompt),
    )
    if err != nil {
        return "", err
    }
    return resp.Text(), nil
}
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| API 키 하드코딩 | 보안 취약점 | `os.Getenv()` 또는 Secret Manager |
| goroutine 무제한 LLM 호출 | API rate limit 초과, OOM | 세마포어로 동시성 제한 |
| 에러 무시 (`_ = err`) | LLM 실패 미감지 | 에러 전파 + OTel span 기록 |
| 프레임워크 과잉 | 단순 호출에 무거운 프레임워크 | 단순 작업은 직접 API 호출 |
| Structured Output 미사용 | JSON 수동 파싱 에러 | Genkit/LangChainGo 스키마 검증 |

---

## 체크리스트

### 프레임워크 선택
- [ ] 프로젝트 요구사항에 맞는 프레임워크 선택 (비교표 참조)
- [ ] API 키 환경변수 설정
- [ ] OTel 트레이싱 연동

### 구현
- [ ] Structured Output 스키마 정의
- [ ] Tool Calling 도구 등록
- [ ] 동시성 제한 (세마포어)
- [ ] Model Routing 설정

### MCP 서버 (Claude 연동)
- [ ] mcp-go로 MCP 서버 구현
- [ ] `.claude/settings.json`에 등록
- [ ] 도구 테스트

---

## 참조 스킬

- `effective-go.md` — Go 패턴 결정 가이드
- `go-microservice.md` — Go MSA 프로젝트 구조
- `concurrency-go.md` — Go 동시성 패턴
- `agentic-coding.md` — Agentic Coding 모드, Model Routing
- `observability-genai.md` — GenAI 관측성, LLM Tracing
- `finops-ai.md` — AI 비용 관리

---

## Sources

- [Go Blog: Building LLM-powered applications in Go](https://go.dev/blog/llmpowered)
- [Genkit Go 1.0 Announcement](https://developers.googleblog.com/en/announcing-genkit-go-10-and-enhanced-ai-assisted-development/)
- [Top 7 Go AI Agent Frameworks 2026](https://reliasoftware.com/blog/golang-ai-agent-frameworks)
- [mcp-go SDK](https://github.com/modelcontextprotocol/go-sdk)
- [Eino (CloudWeGo)](https://github.com/cloudwego/eino)
- [LangChainGo](https://github.com/tmc/langchaingo)
