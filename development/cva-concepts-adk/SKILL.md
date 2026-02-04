---
name: cva-concepts-adk
description: Google ADK (Agent Development Kit) architecture and core concepts. Covers agent types (LLM, Sequential, Parallel, Loop, Multi-agent), tool ecosystem, execution flows, deployment options, and observability. Model-agnostic framework for production AI agents. Use when understanding ADK architecture, selecting agent patterns, designing agent systems, or deploying to Vertex AI.
allowed-tools: Read,Bash,Edit,Write,Glob
---

# Google ADK (Agent Development Kit) - Architecture

> **Framework:** Open-source by Google
> **Version:** 0.2.0+
> **Production:** Powers Google Agentspace and CES
> **Documentation:** https://google.github.io/adk-docs/

---

## 🎯 What is Google ADK?

**Agent Development Kit (ADK)** is Google's open-source framework for developing and deploying AI agents.

### Key Characteristics

- 🧠 **Model-agnostic** - Works with Gemini, OpenAI, Claude, Llama, etc.
- 🚀 **Deployment-agnostic** - Local, Vertex AI, Cloud Run, GKE, Kubernetes
- 🔧 **Framework-compatible** - Integrates with LangChain, CrewAI, custom tools
- 🏢 **Production-ready** - Battle-tested in Google products
- 🔄 **Interoperable** - Java and Python SDKs with identical APIs

---

## 🏗️ Core Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Your Application                    │
│            (Clojure via Java interop)               │
└─────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────┐
│                   Agent Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │   LLM    │  │ Workflow │  │  Multi-Agent     │ │
│  │  Agent   │  │  Agent   │  │    System        │ │
│  └──────────┘  └──────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────┐
│                   Tool Ecosystem                     │
│  ┌─────────┐ ┌─────────┐ ┌────────┐ ┌──────────┐  │
│  │Built-in │ │ Custom  │ │ OpenAPI│ │Third-party│  │
│  │ Tools   │ │Functions│ │  Tools │ │   (LC)    │  │
│  └─────────┘ └─────────┘ └────────┘ └──────────┘  │
└─────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────┐
│                    LLM Layer                         │
│        Gemini | Claude | GPT | Open Models          │
└─────────────────────────────────────────────────────┘
```

---

## 🤖 Agent Types

### 1. LLM Agent (Dynamic Routing)

**Concept:** Agent uses LLM to make decisions about which actions to execute.

**When to use:**
- ✅ Adaptive behavior based on context
- ✅ Multiple tools available
- ✅ Complex decisions required
- ✅ Unpredictable input patterns

**Clojure Example:**

```clojure
(ns lab.agents.llm-agent
  "LLM Agent with dynamic tool selection"
  (:import [com.google.adk.agent LLMAgent]
           [com.google.adk.model GeminiModel]
           [com.google.adk.tool Tool]))

(defn create-calculator-tool
  "Custom calculator tool"
  []
  (-> (Tool/builder)
      (.setName "calculator")
      (.setDescription "Performs basic arithmetic operations")
      (.setFunction
        (reify java.util.function.Function
          (apply [_ input]
            ;; Parse and execute calculation
            (str "Result: " (eval (read-string input))))))
      (.build)))

(defn create-llm-agent
  "Creates LLM agent with tools"
  [tools]
  (-> (LLMAgent/builder)
      (.setModel
        (-> (GeminiModel/builder)
            (.setModelName "gemini-1.5-flash")
            (.setTemperature 0.7)
            (.build)))
      (.addTools tools)
      (.setSystemPrompt "You are a helpful assistant with access to tools.")
      (.build)))

;; REPL Usage
(comment
  (def tools [(create-calculator-tool)])
  (def agent (create-llm-agent tools))

  (.execute agent "What is 25 * 4?")
  ;; Agent decides to use calculator tool
  ;; => "The result is 100"
  )
```

**Flow:**
```
Input → LLM decides → Selects Tool → Executes → LLM synthesizes → Output
```

---

### 2. Workflow Agents (Structured)

#### 2.1 Sequential Agent

**Concept:** Execute steps in predetermined order.

**When to use:**
- ✅ Fixed pipeline (ETL, data processing)
- ✅ Deterministic execution required
- ✅ Lower cost (no LLM routing overhead)

```clojure
(ns lab.agents.sequential
  (:import [com.google.adk.agent SequentialAgent]
           [com.google.adk.agent.step LLMStep]))

(defn create-sequential-pipeline
  "Sequential agent for data processing"
  []
  (-> (SequentialAgent/builder)
      (.addStep
        (-> (LLMStep/builder)
            (.setPrompt "Extract key entities from: {{input}}")
            (.setModel "gemini-1.5-flash")
            (.build)))
      (.addStep
        (-> (LLMStep/builder)
            (.setPrompt "Classify entities: {{previous_output}}")
            (.build)))
      (.addStep
        (-> (LLMStep/builder)
            (.setPrompt "Generate summary: {{previous_output}}")
            (.build)))
      (.build)))

;; REPL Usage
(comment
  (def pipeline (create-sequential-pipeline))
  (.execute pipeline "Process this medical text...")
  ;; Step 1: Extract entities
  ;; Step 2: Classify
  ;; Step 3: Summarize
  ;; => Final summary
  )
```

**Flow:**
```
Input → Step 1 → Step 2 → Step 3 → ... → Output
```

---

#### 2.2 Parallel Agent

**Concept:** Execute multiple agents concurrently.

**When to use:**
- ✅ Independent tasks can run simultaneously
- ✅ Need to reduce latency
- ✅ Aggregating results from multiple sources

```clojure
(ns lab.agents.parallel
  (:import [com.google.adk.agent ParallelAgent]))

(defn create-parallel-researcher
  "Parallel agent for multi-source research"
  []
  (-> (ParallelAgent/builder)
      (.addAgent "scholar" (create-scholar-agent))
      (.addAgent "pubmed" (create-pubmed-agent))
      (.addAgent "web" (create-web-search-agent))
      (.setAggregationStrategy :merge-all)
      (.build)))

;; REPL Usage
(comment
  (def researcher (create-parallel-researcher))
  (.execute researcher "Research: effectiveness of salicylic acid")
  ;; Executes 3 agents concurrently:
  ;; - Google Scholar search
  ;; - PubMed search
  ;; - Web search
  ;; => Aggregated results from all sources
  )
```

**Flow:**
```
Input → ┬─ Agent 1 ─┐
        ├─ Agent 2 ─┼─ Aggregate → Output
        └─ Agent 3 ─┘
```

---

#### 2.3 Loop Agent

**Concept:** Repeat execution until condition met.

**When to use:**
- ✅ Iterative refinement needed
- ✅ Quality threshold must be reached
- ✅ Self-correction workflows

```clojure
(ns lab.agents.loop
  (:import [com.google.adk.agent LoopAgent]))

(defn create-refining-agent
  "Loop agent that refines output until quality threshold"
  []
  (-> (LoopAgent/builder)
      (.setAgent (create-writer-agent))
      (.setMaxIterations 5)
      (.setCondition
        (reify java.util.function.Predicate
          (test [_ output]
            (>= (calculate-quality-score output) 0.8))))
      (.build)))

;; REPL Usage
(comment
  (def refiner (create-refining-agent))
  (.execute refiner "Write professional medical article")
  ;; Iteration 1: quality = 0.6
  ;; Iteration 2: quality = 0.75
  ;; Iteration 3: quality = 0.85 ✓
  ;; => Returns iteration 3 output
  )
```

**Flow:**
```
Input → Execute → Check condition ─No─┐
                         │            │
                        Yes           │
                         ↓            │
                      Output ←────────┘
```

---

### 3. Multi-Agent Systems

**Concept:** Coordinate multiple specialized agents.

**Patterns:**
- **Hierarchical:** Manager agent delegates to worker agents
- **Collaborative:** Agents negotiate and share information
- **Competitive:** Best result selected from multiple approaches

```clojure
(ns lab.agents.multi-agent
  (:import [com.google.adk.agent MultiAgentSystem]))

(defn create-healthcare-system
  "Multi-agent system for healthcare content generation"
  []
  (-> (MultiAgentSystem/builder)
      (.addAgent "extractor" (create-data-extraction-agent))
      (.addAgent "validator" (create-claims-validator-agent))
      (.addAgent "researcher" (create-reference-search-agent))
      (.addAgent "seo" (create-seo-optimizer-agent))
      (.addAgent "consolidator" (create-final-consolidator-agent))
      (.setOrchestrationStrategy :sequential-with-feedback)
      (.build)))
```

> 📘 **Complete implementation:** See [`cva-healthcare-pipeline`](../cva-healthcare-pipeline/SKILL.md) for production multi-agent system.

---

## 🔧 Tool Ecosystem

### Built-in Tools

**Available out-of-box:**
- Web search (Google Search, Google Scholar)
- Code execution (Python, JavaScript)
- Data retrieval (BigQuery, Cloud Storage)
- API calls (REST, GraphQL)

### Custom Tools (Clojure)

```clojure
(ns lab.tools.custom
  (:import [com.google.adk.tool Tool]))

(defn create-database-query-tool
  "Custom tool for database queries"
  [db-spec]
  (-> (Tool/builder)
      (.setName "query_database")
      (.setDescription "Queries PostgreSQL database for tenant data")
      (.setInputSchema
        {:type "object"
         :properties {:query {:type "string"
                              :description "SQL query to execute"}}
         :required ["query"]})
      (.setFunction
        (reify java.util.function.Function
          (apply [_ input]
            (let [query (get input "query")]
              (jdbc/execute! db-spec [query])))))
      (.build)))
```

### Tool Composition

**Combine tools from different sources:**

```clojure
(defn create-hybrid-agent
  "Agent with built-in + custom + third-party tools"
  []
  (let [built-in-search (GroundingTool/googleSearch)
        custom-db (create-database-query-tool db-spec)
        langchain-tool (from-langchain wikipedia-tool)]
    (create-llm-agent [built-in-search custom-db langchain-tool])))
```

---

## 🚀 Deployment Options

### 1. Local Development

```bash
# Run locally with Clojure CLI
clojure -M:dev -m lab.core
```

### 2. Vertex AI Agent Engine

```clojure
(ns lab.deployment.vertex
  (:import [com.google.cloud.vertexai.agent AgentEngine]))

(defn deploy-to-vertex
  "Deploy agent to Vertex AI Agent Engine"
  [agent project-id]
  (-> (AgentEngine/builder)
      (.setProjectId project-id)
      (.setLocation "us-central1")
      (.setAgent agent)
      (.deploy)))

;; REPL Usage
(comment
  (deploy-to-vertex my-agent "saas3-476116")
  ;; => Deployed to Vertex AI with endpoint URL
  )
```

### 3. Cloud Run (Container)

```dockerfile
FROM clojure:openjdk-17-tools-deps
COPY . /app
WORKDIR /app
RUN clojure -M:build
CMD ["clojure", "-M:prod"]
```

```bash
# Deploy to Cloud Run
gcloud run deploy agent-service \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 📊 Observability

### Logging

```clojure
(ns lab.observability.logging
  (:require [clojure.tools.logging :as log]))

(defn execute-with-logging
  "Execute agent with comprehensive logging"
  [agent input]
  (log/info "Agent execution started" {:input input})
  (let [start-time (System/currentTimeMillis)
        result (.execute agent input)
        duration (- (System/currentTimeMillis) start-time)]
    (log/info "Agent execution completed"
              {:duration-ms duration
               :output-length (count result)
               :success true})
    result))
```

### Metrics

**Track key metrics:**
- Execution time
- Token usage
- Tool invocations
- Error rates
- Cost per execution

```clojure
(defn track-metrics
  [agent input]
  (let [metrics (atom {})]
    (add-watch agent :metrics
               (fn [_ _ _ new-state]
                 (swap! metrics assoc
                        :tokens (:tokens-used new-state)
                        :tools-called (:tool-invocations new-state))))
    (.execute agent input)
    @metrics))
```

---

## 💡 Best Practices

### 1. Start Simple, Optimize Later

**Progression:**
```
LLM Agent → Sequential Agent → Parallel Agent → Multi-Agent System
(Day 1)     (Week 1)           (Month 1)        (Production)
```

**Rationale:** Build complexity incrementally based on actual requirements.

### 2. Choose the Right Agent Type

**Decision Matrix:**

| Need | Agent Type | Reason |
|------|-----------|--------|
| Simple task, one path | Sequential | Lowest cost, deterministic |
| Complex routing needed | LLM | Flexibility, adaptability |
| Independent parallel tasks | Parallel | Reduced latency |
| Iterative refinement | Loop | Quality improvement |
| Complex system | Multi-Agent | Specialized expertise per component |

> 📘 **Detailed guidance:** See [`cva-concepts-agent-types`](../cva-concepts-agent-types/SKILL.md) for A/B/C/D taxonomy.

### 3. Tool Design Principles

- **Single Responsibility:** One tool = one clear function
- **Descriptive Names:** `query_customer_database` not `db`
- **Rich Descriptions:** Help LLM understand when to use tool
- **Error Handling:** Return structured errors, not exceptions
- **Idempotent:** Safe to retry

### 4. Model Selection

**By task complexity:**
- **Simple** (extraction, classification): `gemini-1.5-flash`
- **Medium** (reasoning, personalization): `gemini-1.5-pro` or `claude-3-5-haiku`
- **Complex** (consolidation, critical decisions): `claude-3-5-sonnet` or `gemini-2.0-flash-thinking`

> 📘 **Cost optimization:** See [`cva-patterns-cost`](../cva-patterns-cost/SKILL.md) for multi-model routing.

### 5. Testing Strategy

```clojure
(ns lab.testing.agents
  (:require [clojure.test :refer :all]))

(deftest test-agent-execution
  (testing "Agent produces valid output"
    (let [agent (create-test-agent)
          result (.execute agent "test input")]
      (is (string? result))
      (is (> (count result) 0))
      (is (valid-json? result)))))

(deftest test-agent-tools
  (testing "Agent uses correct tools"
    (let [agent (create-test-agent-with-mock-tools)
          _ (.execute agent "calculate 2 + 2")
          tool-calls (get-tool-invocations agent)]
      (is (= 1 (count tool-calls)))
      (is (= "calculator" (:tool-name (first tool-calls)))))))
```

### 6. Error Handling

```clojure
(defn execute-with-retry
  "Execute agent with exponential backoff retry"
  [agent input max-retries]
  (loop [attempt 1]
    (try
      (.execute agent input)
      (catch Exception e
        (if (< attempt max-retries)
          (do
            (Thread/sleep (* 1000 (Math/pow 2 attempt)))
            (recur (inc attempt)))
          (throw e))))))
```

---

## 🔗 Related Skills

- [`cva-concepts-agent-types`](../cva-concepts-agent-types/SKILL.md) - A/B/C/D agent taxonomy ⭐
- [`cva-quickref-adk`](../cva-quickref-adk/SKILL.md) - ADK API quick reference ⭐
- [`cva-patterns-workflows`](../cva-patterns-workflows/SKILL.md) - Multi-agent workflow patterns
- [`cva-patterns-cost`](../cva-patterns-cost/SKILL.md) - Cost optimization strategies
- [`cva-healthcare-pipeline`](../cva-healthcare-pipeline/SKILL.md) - Production multi-agent system
- [`cva-setup-vertex`](../cva-setup-vertex/SKILL.md) - Vertex AI deployment setup

---

## 📘 Additional Resources

### Official Documentation
- [Google ADK Docs](https://google.github.io/adk-docs/)
- [ADK GitHub](https://github.com/google/adk-java)
- [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine)

### Advanced Topics
- [Custom Tool Development](https://google.github.io/adk-docs/tools/)
- [Multi-Agent Orchestration](https://google.github.io/adk-docs/agents/multi-agent/)
- [Production Deployment](https://google.github.io/adk-docs/deploy/)

---

*This skill provides foundational ADK knowledge. Combine with agent-types taxonomy and workflow patterns for complete understanding.*
