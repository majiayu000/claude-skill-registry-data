---
name: spring-ai
description: "Spring AI 통합 — ChatClient, Advisors API, Structured Output, Function·Tool Calling, MCP, RAG, 비용 최적화. Use when Spring Boot 앱에 LLM 챗·RAG·MCP 기능을 붙이거나 Spring AI 구조를 설계할 때."
---

# Spring AI Patterns

Spring AI 1.1 기반 LLM 통합, ChatClient, Advisors API, Structured Output, Function Calling, RAG, MCP

## Quick Reference (결정 트리)

```
Java LLM 통합 전략?
    │
    ├─ Spring Boot 팀 ──────────> Spring AI 1.1 (권장)
    │       └─ MCP 네이티브, Advisors, 20+ 모델, Auto-config
    │
    ├─ Spring 무관, 경량 ───────> LangChain4j
    │       └─ 독립 사용, 프레임워크 비의존
    │
    └─ 완전 제어 필요 ──────────> Direct API
            └─ 추상화 오버헤드 없음, 수동 관리

Spring AI 기능 선택?
    │
    ├─ 단순 대화 ───────────────> ChatClient API
    ├─ 구조화된 응답 필요 ──────> Structured Output
    ├─ 외부 데이터/도구 연동 ──> Function/Tool Calling
    ├─ RAG (검색 증강 생성) ───> Advisors + VectorStore
    ├─ 멀티스텝 워크플로우 ────> Recursive Advisors
    └─ 외부 AI 도구 서버 연동 ─> MCP Client

Vector DB 선택?
    │
    ├─ PostgreSQL 이미 사용 ───> PgVector (추가 인프라 불필요)
    ├─ 고성능 검색 필요 ───────> Elasticsearch / Redis
    ├─ 그래프 관계 중요 ───────> Neo4j
    └─ 실험/프로토타입 ────────> Chroma (인메모리)
```

---

## Spring AI 아키텍처

```
┌──────────────────────────────────────────────────────┐
│                    Spring AI 1.1                       │
├──────────────────────────────────────────────────────┤
│                                                        │
│  ┌─────────────┐   ┌──────────────┐   ┌───────────┐  │
│  │ ChatClient  │   │   Advisors   │   │   MCP     │  │
│  │ API         │   │   Pipeline   │   │   Client  │  │
│  └──────┬──────┘   └──────┬───────┘   └─────┬─────┘  │
│         │                  │                  │        │
│  ┌──────▼──────────────────▼──────────────────▼────┐  │
│  │              Model Abstraction Layer              │  │
│  │  OpenAI │ Anthropic │ Ollama │ Bedrock │ 20+    │  │
│  └─────────────────────────────────────────────────┘  │
│                                                        │
│  ┌─────────────┐   ┌──────────────┐   ┌───────────┐  │
│  │ Structured  │   │   Function   │   │  Vector   │  │
│  │ Output      │   │   Calling    │   │  Store    │  │
│  └─────────────┘   └──────────────┘   └───────────┘  │
│                                                        │
└──────────────────────────────────────────────────────┘
```

---

## ChatClient API

### 기본 사용

```java
@Service
public class AssistantService {

    private final ChatClient chatClient;

    // Spring Boot Auto-configuration으로 주입
    public AssistantService(ChatClient.Builder builder) {
        this.chatClient = builder
            .defaultSystem("당신은 Java 백엔드 전문가입니다.")
            .build();
    }

    public String ask(String question) {
        return chatClient.prompt()
            .user(question)
            .call()
            .content();  // String 응답
    }

    // 스트리밍 응답
    public Flux<String> askStream(String question) {
        return chatClient.prompt()
            .user(question)
            .stream()
            .content();
    }
}
```

### 모델 설정

```yaml
# application.yml
spring:
  ai:
    # Anthropic Claude
    anthropic:
      api-key: ${ANTHROPIC_API_KEY}
      chat:
        options:
          model: claude-sonnet-5-5
          # temperature 는 지정하지 않는다 — Sonnet 5.5 는 400 으로 거부한다
          max-tokens: 4096

    # 또는 OpenAI
    openai:
      api-key: ${OPENAI_API_KEY}
      chat:
        options:
          model: gpt-4o

    # 또는 Ollama (로컬)
    ollama:
      base-url: http://localhost:11434
      chat:
        options:
          model: llama3
```

---

## Advisors API (핵심 차별점)

Advisor = 모델 상호작용을 intercept/modify/enrich하는 미들웨어.

```
Request ──> Advisor 1 ──> Advisor 2 ──> Model ──> Advisor 2 ──> Advisor 1 ──> Response
              (RAG)       (Memory)                 (후처리)      (후처리)
```

### RAG Advisor

```java
@Configuration
public class RagConfig {

    @Bean
    public ChatClient ragChatClient(
            ChatClient.Builder builder,
            VectorStore vectorStore) {

        return builder
            .defaultAdvisors(
                // RAG: 질문과 관련된 문서를 자동으로 검색하여 컨텍스트에 추가
                new QuestionAnswerAdvisor(vectorStore,
                    SearchRequest.builder()
                        .topK(5)
                        .similarityThreshold(0.7)
                        .build()),

                // Memory: 대화 히스토리 유지
                new MessageChatMemoryAdvisor(
                    new InMemoryChatMemory(), 10)  // 최근 10턴
            )
            .build();
    }
}
```

### Recursive Advisors (멀티스텝)

```java
// Advisor 체인: 검증 → 보강 → 포맷팅
public class ValidationAdvisor implements CallAroundAdvisor {

    @Override
    public AdvisedResponse aroundCall(AdvisedRequest request,
            CallAroundAdvisorChain chain) {

        // 1. 입력 검증
        String userMessage = request.userText();
        if (containsSensitiveData(userMessage)) {
            return sanitizedResponse(request);
        }

        // 2. 다음 Advisor로 전달
        AdvisedResponse response = chain.nextAroundCall(request);

        // 3. 출력 검증
        String content = response.response().getResult().getOutput().getText();
        if (containsHallucination(content)) {
            // 재시도 또는 경고 추가
            return retryWithGrounding(request, chain);
        }

        return response;
    }
}
```

---

## Structured Output

LLM 응답을 Java 도메인 객체로 자동 변환.

```java
// 1. 도메인 객체 정의
public record CodeReview(
    String summary,
    List<Issue> issues,
    int score
) {
    public record Issue(
        String severity,   // BLOCKER, CRITICAL, MAJOR, MINOR
        String file,
        int line,
        String description,
        String suggestion
    ) {}
}

// 2. Structured Output으로 호출
public CodeReview reviewCode(String code) {
    return chatClient.prompt()
        .user("다음 코드를 리뷰해주세요:\n" + code)
        .call()
        .entity(CodeReview.class);  // 자동 JSON → Java 변환
}
```

---

## Function/Tool Calling

Spring Bean 메서드를 AI 도구로 노출.

```java
@Component
public class DevOpsTools {

    // AI가 호출할 수 있는 도구
    @Tool(description = "쿠버네티스 Pod 상태를 조회합니다")
    public List<PodStatus> getPodStatus(
            @ToolParam(description = "네임스페이스") String namespace) {
        // 실제 K8s API 호출
        return kubernetesClient.pods()
            .inNamespace(namespace)
            .list().getItems().stream()
            .map(pod -> new PodStatus(
                pod.getMetadata().getName(),
                pod.getStatus().getPhase()))
            .toList();
    }

    @Tool(description = "최근 에러 로그를 검색합니다")
    public List<LogEntry> searchErrors(
            @ToolParam(description = "서비스명") String service,
            @ToolParam(description = "최근 N분") int minutes) {
        return lokiClient.query(
            String.format("{service_name=\"%s\"} |= \"ERROR\"", service),
            Duration.ofMinutes(minutes));
    }
}

// AI가 자동으로 도구를 선택하여 호출
@Service
public class OpsAssistant {
    public String diagnose(String issue) {
        return chatClient.prompt()
            .user(issue)
            .tools(devOpsTools)  // 도구 등록
            .call()
            .content();
        // AI가 필요에 따라 getPodStatus(), searchErrors() 자동 호출
    }
}
```

---

## MCP 통합

### MCP Client 설정

```yaml
# application.yml
spring:
  ai:
    mcp:
      client:
        stdio:
          servers:
            github:
              command: mcp-server-github
              args: ["--repo", "org/repo"]
            filesystem:
              command: mcp-server-filesystem
              args: ["--root", "/workspace"]
```

### MCP Server 구현 (Spring Bean → MCP Tool)

```java
@Configuration
public class McpServerConfig {

    // Spring Bean의 @Tool 메서드가 자동으로 MCP tool로 노출
    @Bean
    public ToolCallbackProvider mcpTools(DevOpsTools tools) {
        return MethodToolCallbackProvider.builder()
            .toolObjects(tools)
            .build();
    }
}
```

---

## RAG 프로덕션 패턴

### ETL 파이프라인

```java
@Service
public class DocumentIngestionService {

    private final VectorStore vectorStore;

    // 문서 수집 → 변환 → 저장
    public void ingest(Resource document) {
        // 1. Read
        var reader = new TikaDocumentReader(document);
        List<Document> documents = reader.read();

        // 2. Transform (청킹)
        var splitter = new TokenTextSplitter(
            800,    // chunkSize (tokens)
            200,    // overlap
            5,      // minChunkSize
            10000,  // maxNumChunks
            true    // keepSeparator
        );
        List<Document> chunks = splitter.apply(documents);

        // 3. Store (임베딩 + 저장)
        vectorStore.add(chunks);
    }
}
```

### Vector Store 설정 (PgVector)

```yaml
spring:
  ai:
    vectorstore:
      pgvector:
        index-type: HNSW
        distance-type: COSINE_DISTANCE
        dimensions: 1536
  datasource:
    url: jdbc:postgresql://localhost:5432/aidb
```

---

## 비용 최적화

### Prompt Caching

```yaml
spring:
  ai:
    anthropic:
      chat:
        options:
          # 시스템 프롬프트 캐싱 (최대 90% 비용 절감)
          prompt-caching-enabled: true
          # TTL: ephemeral (5분) 또는 persistent (1시간)
```

### Model Routing (비용/성능 균형)

```java
@Service
public class SmartModelRouter {

    private final ChatClient economyClient;   // Haiku
    private final ChatClient standardClient;  // Sonnet
    private final ChatClient premiumClient;   // Opus

    public String route(String task, TaskComplexity complexity) {
        return switch (complexity) {
            case SIMPLE -> economyClient.prompt().user(task).call().content();
            case MODERATE -> standardClient.prompt().user(task).call().content();
            case COMPLEX -> premiumClient.prompt().user(task).call().content();
        };
    }
}
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| API 키 하드코딩 | 보안 취약점 | 환경변수 또는 Secret Manager |
| Advisor 없이 RAG 직접 구현 | 코드 중복, 유지보수↓ | QuestionAnswerAdvisor 사용 |
| 모든 요청에 같은 모델 | 비용 비효율 | Model routing |
| Structured Output 미사용 | 파싱 에러, 취약한 통합 | `.entity(Class)` 사용 |
| Memory 무제한 | 토큰 폭증 | 최근 N턴 제한 |
| Prompt caching 미설정 | 반복 비용 | caching 활성화 |

---

## 체크리스트

### 설정
- [ ] Spring AI 의존성 추가 (`spring-ai-bom`)
- [ ] 모델 프로바이더 설정 (API key 환경변수)
- [ ] Auto-configuration 확인

### 구현
- [ ] ChatClient Bean 설정
- [ ] Advisors 파이프라인 (RAG, Memory)
- [ ] Structured Output 도메인 객체 정의
- [ ] Function/Tool Calling 도구 등록
- [ ] MCP 서버/클라이언트 설정

### 운영
- [ ] Prompt caching 활성화
- [ ] Model routing 전략 설정
- [ ] OTel GenAI metrics 수집
- [ ] 비용 모니터링 대시보드

---

## 참조 스킬

- `spring-patterns.md` — Spring Boot 핵심 패턴
- `rag-patterns.md` — RAG 아키텍처 상세 (청킹, 검색 최적화)
- `vector-db.md` — Vector DB 비교, 인덱싱 전략
- `agentic-ai-architecture.md` — Agentic AI 시스템 설계
- `observability-genai.md` — GenAI 관측성, OTel 연동
- `finops-ai.md` — AI 비용 관리, Model routing 비용

---

## Sources

- [Spring AI 1.1 GA Release](https://spring.io/blog/2025/11/12/spring-ai-1-1-GA-released/)
- [Spring AI Reference Documentation](https://docs.spring.io/spring-ai/reference/)
- [Spring AI vs LangChain4j (2026)](https://www.javacodegeeks.com/2026/03/choosing-a-java-llm-integration-strategy-in-2026-spring-ai-1-1-vs-langchain4j-vs-direct-api-calls.html)
- [Spring AI Advisors Deep Dive](https://paradigma-digital.medium.com/deep-learning-about-spring-ai-advisors-structured-output-and-tool-calling-38abc6c1d97b)
- [Spring AI MCP Implementation](https://en.paradigmadigital.com/dev/deep-learning-spring-ai-mcp-implementation/)
