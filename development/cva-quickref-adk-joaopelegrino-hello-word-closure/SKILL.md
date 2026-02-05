---
name: cva-quickref-adk
description: Quick reference cheatsheet for Google ADK in Clojure. Includes agent creation patterns, model configuration, tool building, execution patterns, and common workflows. Use when writing ADK code, looking up API syntax, building agents, or troubleshooting implementations.
allowed-tools: Read,Bash,Edit,Write
---

# Google ADK Quick Reference

> **Purpose:** Fast API reference and common patterns for Google Agent Development Kit
> **Target:** Developers actively coding with ADK in Clojure

## 🎯 Quick Start

```clojure
;; Most common operations - copy-paste ready

;; 1. Create basic LLM agent
(def agent
  (-> (LLMAgent/builder)
      (.setModel gemini-model)
      (.setSystemPrompt "You are helpful")
      (.build)))

;; 2. Execute agent
(def result (.execute agent "user input"))

;; 3. Get response text
(.getText result)

;; 4. Create simple tool
(def tool
  (-> (FunctionTool/builder)
      (.setName "tool_name")
      (.setDescription "What it does")
      (.setFunction
        (reify Function
          (apply [_ input]
            {"result" (process input)})))
      (.build)))

;; 5. Add tool to agent
(-> (LLMAgent/builder)
    (.setModel model)
    (.addTools [tool])
    (.build))
```

## 📚 Complete Reference

### Imports

```clojure
;; Core agent types
(import '[com.google.adk.agent LLMAgent
                               SequentialAgent
                               ParallelAgent
                               LoopAgent])

;; Model providers
(import '[com.google.adk.model GeminiModel
                               OpenAIModel])

;; Tool system
(import '[com.google.adk.tool FunctionTool
                              Tool])

;; Java utilities for callbacks
(import '[java.util.function Function
                            Predicate
                            Consumer])

;; REPL test:
;; (LLMAgent/builder) => should not error
```

### Agent Creation

**Basic LLM Agent:**
```clojure
(def agent
  (-> (LLMAgent/builder)
      (.setModel model)
      (.addTools tools)
      (.setSystemPrompt "You are helpful")
      (.build)))

;; REPL test:
;; (type agent) => com.google.adk.agent.LLMAgent
```

**Complete LLM Agent (all options):**
```clojure
(def agent
  (-> (LLMAgent/builder)
      (.setModel gemini-model)
      (.addTools [tool1 tool2 tool3])
      (.setSystemPrompt "Detailed instructions...")
      (.setTemperature 0.7)        ; Creativity level
      (.setMaxTokens 2048)         ; Response length limit
      (.build)))

;; See also: cva-quickref-adk#temperature-guide
;; REPL test:
;; (.getModel agent) => GeminiModel instance
;; (.getTools agent) => [tool1 tool2 tool3]
```

**Sequential Agent (pipeline):**
```clojure
(def seq-agent
  (-> (SequentialAgent/builder)
      (.addStep agent1)            ; Runs first
      (.addStep agent2)            ; Gets agent1 output
      (.addStep agent3)            ; Gets agent2 output
      (.build)))

;; REPL test:
;; (.execute seq-agent "input") => final agent3 output
;; See also: cva-patterns-sequential
```

**Parallel Agent (concurrent execution):**
```clojure
(def par-agent
  (-> (ParallelAgent/builder)
      (.addAgent agent1)           ; All run simultaneously
      (.addAgent agent2)
      (.setAggregationStrategy :merge)  ; How to combine results
      (.build)))

;; REPL test:
;; (.execute par-agent "input") => merged results
;; See also: cva-patterns-parallel
```

**Loop Agent (iterative):**
```clojure
(def loop-agent
  (-> (LoopAgent/builder)
      (.setAgent base-agent)
      (.setMaxIterations 5)        ; Safety limit
      (.setTerminationCondition
        (reify Predicate
          (test [_ result]
            (success? result))))   ; Custom success check
      (.build)))

;; REPL test:
;; (.execute loop-agent "solve step by step") => iterates until success
;; See also: cva-patterns-loop, cva-concepts-agent-types
```

### Model Configuration

**Gemini Model:**
```clojure
(def gemini-model
  (-> (GeminiModel/builder)
      (.setProjectId "your-project-id")
      (.setLocation "us-central1")
      (.setModelName "gemini-1.5-pro")
      (.setTemperature 0.7)
      (.setMaxOutputTokens 2048)
      (.setTopP 0.9)
      (.build)))

;; REPL test:
;; (type gemini-model) => com.google.adk.model.GeminiModel
;; See also: cva-setup-vertex#authentication
```

**Temperature Presets:**
```clojure
;; Deterministic (factual, consistent)
{:temperature 0.0 :top-p 1.0}    ; Same output every time

;; Consistent (slight variation)
{:temperature 0.3 :top-p 0.8}    ; Good for classification

;; Balanced (default)
{:temperature 0.7 :top-p 0.9}    ; General purpose

;; Creative (varied output)
{:temperature 0.9 :top-p 0.95}   ; Brainstorming

;; Very creative (unpredictable)
{:temperature 1.0 :top-p 1.0}    ; Experimental

;; REPL test:
;; (-> (GeminiModel/builder)
;;     (.setTemperature 0.0)
;;     (.build))
```

### Tool Building

**Simple Function Tool:**
```clojure
(def tool
  (-> (FunctionTool/builder)
      (.setName "tool_name")
      (.setDescription "What it does")  ; LLM sees this
      (.setFunction
        (reify Function
          (apply [_ input]
            {"result" (process input)})))
      (.build)))

;; REPL test:
;; (.getName tool) => "tool_name"
;; (.apply (.getFunction tool) "test") => {"result" ...}
```

**Tool with Input Schema:**
```clojure
(def calculator-tool
  (-> (FunctionTool/builder)
      (.setName "calculator")
      (.setDescription "Calculates math expressions")
      (.setInputSchema
        {"type" "object"
         "properties" {"expression" {"type" "string"}}
         "required" ["expression"]})  ; LLM must provide this
      (.setFunction
        (reify Function
          (apply [_ input]
            {"result" (eval-expr (get input "expression"))})))
      (.build)))

;; REPL test:
;; (.apply (.getFunction calculator-tool)
;;         {"expression" "2+2"}) => {"result" 4}
```

**Agent as Tool (composition):**
```clojure
(defn agent->tool
  "Wrap an agent as a tool for use in other agents"
  [agent name description]
  (-> (FunctionTool/builder)
      (.setName name)
      (.setDescription description)
      (.setFunction
        (reify Function
          (apply [_ input]
            (.execute agent input))))
      (.build)))

;; Usage:
(def specialist-tool
  (agent->tool specialist-agent
               "python_expert"
               "Expert in Python programming"))

;; REPL test:
;; (.getName specialist-tool) => "python_expert"
;; See also: cva-patterns-agent-composition
```

### Agent Execution

**Simple Execution:**
```clojure
(def result (.execute agent "user input"))

;; REPL test:
;; (.getText result) => "agent response..."
```

**With Runtime Configuration:**
```clojure
(def result
  (.execute agent
            "user input"
            {:max-tokens 1024        ; Override default
             :temperature 0.5}))     ; Override default

;; REPL test:
;; Useful for per-request customization
```

**Streaming (real-time output):**
```clojure
(def stream (.executeStream agent "input"))

(doseq [chunk stream]
  (println (.getText chunk)))

;; REPL test:
;; Watch output appear incrementally
;; See also: cva-patterns-streaming
```

**With Callback (async pattern):**
```clojure
(.execute agent
          "input"
          (reify Consumer
            (accept [_ result]
              (println "Result:" result))))

;; REPL test:
;; Callback fires when complete
;; See also: cva-patterns-async
```

### Result Processing

**Access Response Data:**
```clojure
;; Get text output
(.getText result)                    ; => "agent response..."

;; Get tool calls made by agent
(.getToolCalls result)               ; => [ToolCall(...), ...]

;; Get metadata
(.getMetadata result)                ; => {"finish_reason" "STOP", ...}

;; Get usage statistics
(.getUsage result)                   ; => Usage object
(.getTotalTokens (.getUsage result)) ; => 150

;; REPL test:
;; (keys (bean result)) => shows all available methods
```

**Extract to Clojure Map:**
```clojure
(defn extract-response
  "Convert Java result to Clojure data"
  [result]
  {:text (.getText result)
   :tools (vec (.getToolCalls result))
   :tokens (.getTotalTokens (.getUsage result))
   :finish-reason (get (.getMetadata result) "finish_reason")})

;; REPL test:
;; (extract-response result) => {:text "..." :tools [...] ...}
```

## 💡 Common Patterns

### Retry Pattern (exponential backoff)

```clojure
(defn execute-with-retry
  "Retry agent execution with exponential backoff"
  [agent input max-retries]
  (loop [n 0]
    (try
      (.execute agent input)
      (catch Exception e
        (if (< n max-retries)
          (do
            (Thread/sleep (* 1000 (Math/pow 2 n)))  ; 1s, 2s, 4s, ...
            (recur (inc n)))
          (throw e))))))

;; REPL test:
;; (execute-with-retry agent "test" 3)
;; See also: cva-patterns-resilience
```

### Fallback Pattern (multi-model)

```clojure
(defn execute-with-fallback
  "Try primary agent, fall back to secondary on failure"
  [primary-agent fallback-agent input]
  (try
    (.execute primary-agent input)
    (catch Exception e
      (println "Primary failed, using fallback")
      (.execute fallback-agent input))))

;; REPL test:
;; (execute-with-fallback expensive-agent cheap-agent "test")
;; See also: cva-patterns-fallback
```

### Chain Pattern (sequential processing)

```clojure
(defn chain-agents
  "Pass output of each agent to the next"
  [agents input]
  (reduce (fn [acc agent]
            (.execute agent (:text acc)))
          {:text input}
          agents))

;; REPL test:
;; (chain-agents [analyzer summarizer translator] "data")
;; See also: cva-patterns-sequential
```

### Router Pattern (intent-based)

```clojure
(defn route-to-agent
  "Select agent based on input classification"
  [input agents]
  (let [intent (classify-intent input)  ; Your classification logic
        agent (get agents intent)]
    (.execute agent input)))

;; Usage:
(route-to-agent
  "What's the weather?"
  {:weather weather-agent
   :news news-agent
   :chat chat-agent})

;; REPL test:
;; Create classifier function first
;; See also: cva-patterns-routing
```

### System Prompt Templates

```clojure
;; General assistant
"You are a helpful assistant."

;; Domain expert
"You are an expert in [domain]. Answer concisely and accurately.
Cite sources when possible."

;; Tool-using agent
"You have access to these tools: [list].
Use them when appropriate to answer user questions.
Always explain which tool you used and why."

;; Structured output
"Answer in JSON format: {\"answer\": \"...\", \"confidence\": 0-1}
Be concise but accurate."

;; Multi-step reasoning
"Think step by step. Show your reasoning process.
Use tools to verify information."

;; REPL test:
;; (-> (LLMAgent/builder)
;;     (.setSystemPrompt "You are...")
;;     (.build))
```

### Error Handling

**Catch Specific Exceptions:**
```clojure
(try
  (.execute agent input)
  (catch com.google.adk.exceptions.RateLimitException e
    (println "Rate limit hit, waiting...")
    (Thread/sleep 60000)  ; Wait 1 minute
    (.execute agent input))
  (catch com.google.adk.exceptions.InvalidRequestException e
    (println "Invalid request:" (.getMessage e)))
  (catch Exception e
    (println "General error:" (.getMessage e))))

;; REPL test:
;; Trigger errors intentionally to test handling
;; See also: cva-patterns-error-handling
```

**Safe Execute Wrapper:**
```clojure
(defn safe-execute
  "Execute agent and return success/error map"
  [agent input]
  (try
    {:success true
     :result (.execute agent input)}
    (catch Exception e
      {:success false
       :error (.getMessage e)
       :type (type e)})))

;; REPL test:
;; (safe-execute agent "test") => {:success true :result ...}
```

### Logging & Debugging

**Basic Logging:**
```clojure
(.setLogger agent
  (reify com.google.adk.observability.Logger
    (log [_ level message]
      (println (str "[" level "] " message)))))

;; REPL test:
;; Execute agent and watch log output
```

**Tool Call Logging:**
```clojure
(defn log-tool-calls
  "Debug which tools were called and with what input"
  [result]
  (doseq [tool-call (.getToolCalls result)]
    (println "Tool:" (.getToolName tool-call))
    (println "Input:" (.getInput tool-call))
    (println "Output:" (.getOutput tool-call))))

;; REPL test:
;; (log-tool-calls result)
```

**REPL Debug Helpers:**
```clojure
(comment
  ;; Inspect agent
  (type agent)                        ; => LLMAgent
  (.getModel agent)                   ; => GeminiModel
  (.getTools agent)                   ; => [tool1, tool2]

  ;; Inspect result
  (def r (.execute agent "test"))
  (.getText r)                        ; => response text
  (.getToolCalls r)                   ; => tool calls made
  (.getUsage r)                       ; => token usage

  ;; Inspect tool
  (.getName tool)                     ; => "tool_name"
  (.getDescription tool)              ; => description
  (.apply (.getFunction tool) "test") ; => test output
  )
```

## 🔧 Performance Tips

```clojure
;; 1. Reuse agents (thread-safe, stateless)
(defonce agent (create-agent))

;; 2. Lazy load heavy resources
(defonce model
  (delay
    (-> (GeminiModel/builder)
        (.setProjectId "project")
        (.build))))

;; 3. Cache deterministic results
(def cached-execute
  (memoize
    (fn [input]
      (.execute agent input))))

;; 4. Batch requests for efficiency
(defn batch-execute
  [agent inputs]
  (mapv #(.execute agent %) inputs))

;; 5. Use streaming for long responses
(defn stream-execute [agent input]
  (.executeStream agent input))

;; REPL test:
;; (time (batch-execute agent ["a" "b" "c"]))
;; See also: cva-patterns-performance
```

## 🔄 Data Conversions

**Java ↔ Clojure:**
```clojure
;; Java List → Clojure vector
(vec java-list)

;; Java Map → Clojure map
(into {} java-map)

;; Java Optional → Clojure value/nil
(.orElse java-optional nil)

;; Clojure vector → Java List
(java.util.ArrayList. clj-vec)

;; Clojure map → Java HashMap
(java.util.HashMap. clj-map)

;; Clojure nil → Java Optional
(java.util.Optional/ofNullable value)

;; REPL test:
;; (vec (java.util.ArrayList. [1 2 3])) => [1 2 3]
;; See also: cva-quickref-libpython for Python conversions
```

## 🔗 Related Skills

- [`cva-overview`](../cva-overview/SKILL.md) - High-level ADK concepts
- [`cva-concepts-agent-types`](../cva-concepts-agent-types/SKILL.md) - Agent type details
- [`cva-setup-vertex`](../cva-setup-vertex/SKILL.md) - Vertex AI setup
- [`cva-quickref-libpython`](../cva-quickref-libpython/SKILL.md) - Python interop reference

## 📘 Official Documentation

- **ADK Documentation:** https://google.github.io/adk-docs/
- **API Reference:** https://google.github.io/adk-docs/api-reference/
- **Examples:** https://github.com/google/adk-examples
- **Vertex AI Docs:** https://cloud.google.com/vertex-ai/docs
