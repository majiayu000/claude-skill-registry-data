---
name: cva-patterns-cost
description: Cost optimization strategies for production AI pipelines in Clojure+Vertex AI. Covers multi-model routing (70% Gemini/20% Haiku/10% Sonnet), token optimization (prompt engineering, output constraints), aggressive caching (58% cost reduction), batch processing, and real-time monitoring. Includes production metrics showing $0.391 to $0.162 per pipeline (-58%). Use when optimizing production costs, implementing multi-model strategies, designing budget controls, or scaling to high volume.
allowed-tools: Read,Bash,Edit,Write,Glob
---

# Cost Optimization

> **Pattern Type:** Optimization
> **Complexity:** Medium
> **Best For:** Production systems with >100 requests/day, budget-constrained projects, multi-agent pipelines

## 🎯 Overview

Cost optimization patterns reduce AI model API costs without sacrificing quality. This pattern addresses three optimization vectors:

1. **Model Selection**: Route requests to cheapest model that meets quality requirements
2. **Token Reduction**: Minimize input/output tokens via prompt engineering
3. **Caching**: Avoid redundant API calls for stable/repeated data

**When to Use:**
- Production pipeline with predictable volume (>100 requests/day)
- Multi-agent system with varying complexity per agent
- Budget constraints requiring cost predictability
- Scaling from prototype to production

**Trade-offs:**
- **Complexity**: Multi-model routing adds +15% code complexity
- **Quality**: Careful testing required to ensure cheaper models maintain quality
- **Latency**: Caching reduces latency by 33% as side benefit

**Production ROI:** Healthcare pipeline achieved 58% cost reduction ($0.391 → $0.162 per pipeline) via multi-model routing (22% savings), token optimization (3% savings), and aggressive caching (29% savings). Annual savings: $2,748 for 12,000 pipelines/year.

## 📊 Pattern Explanation

### Core Concept

Cost optimization follows a layered strategy:

```
COST OPTIMIZATION LAYERS

Layer 1: MULTI-MODEL ROUTING (22% savings)
- Gemini Flash:  $0.075/1M tokens (fast, good JSON, medium precision)
- Claude Haiku:  $0.020/1M tokens (very cheap, long text, good comprehension)
- Claude Sonnet: $0.090/1M tokens (expensive, max precision, complex reasoning)

Decision tree:
- Critical compliance/medical? → Sonnet
- Long text (>2K tokens) + cost-sensitive? → Haiku
- JSON output + fast? → Gemini Flash
- Complex reasoning? → Sonnet
- Default → Gemini Flash

Layer 2: TOKEN OPTIMIZATION (3% savings)
- Concise prompts (avoid verbosity)
- Output constraints (max words, brevity)
- Context trimming (remove examples, compress lists)

Layer 3: CACHING (29% savings)
- Static contexts: 100% hit rate (permanent)
- Query contexts: 85% hit rate (1h TTL)
- API contexts: 73% hit rate (24h TTL)

TOTAL: 58% cost reduction ($0.391 → $0.162)
```

### Implementation Approach

**Step 1**: Baseline costs
- Measure current cost per pipeline execution
- Break down by agent (which agents are most expensive?)
- Identify optimization opportunities (75% of cost in 2 agents)

**Step 2**: Implement multi-model routing
- Define quality requirements per agent (critical vs standard)
- Choose model based on complexity, input size, output format
- A/B test quality before full rollout

**Step 3**: Optimize tokens
- Trim prompt templates (remove verbosity)
- Add output constraints (max words, JSON-only)
- Compress static contexts (remove examples)

**Step 4**: Enable aggressive caching
- Static contexts: Preload at startup
- Query contexts: 1h TTL for DB data
- API contexts: 24h TTL for external data

**Step 5**: Monitor and iterate
- Track cost per agent, per model
- Alert on budget thresholds
- Monthly cost prediction based on trend

## 💻 Clojure Implementation

### Basic Example: Multi-Model Routing Decision Tree

```clojure
(ns lab.optimization.model-selection
  "Intelligent model routing based on task requirements")

(defrecord ModelRequirements
  [complexity       ; :low, :medium, :high
   precision-level  ; :standard, :high, :critical
   input-size       ; :small (<1K tokens), :medium (<5K), :large (>5K)
   output-format    ; :text, :json, :structured
   cost-sensitivity ; :high, :medium, :low
   latency-req])    ; :fast (<3s), :medium (<10s), :slow (>10s)

(def model-capabilities
  "Model characteristics for decision tree.

  Cost: Per 1M input tokens
  Latency: Average response time (seconds)
  Strengths/Weaknesses: Qualitative assessment"
  {:gemini-flash
   {:cost 0.075
    :latency 2.5
    :best-for [:json :structured :medium-text]
    :strengths ["Fast" "Cheap" "Reliable JSON" "Good latency"]
    :weaknesses ["Medium precision for long text" "Limited complex reasoning"]}

   :claude-haiku
   {:cost 0.020
    :latency 1.8
    :best-for [:large-text :simple-analysis :summarization]
    :strengths ["VERY cheap" "Fast" "Excellent long text" "Good comprehension"]
    :weaknesses ["Less reliable JSON" "Limited complex reasoning"]}

   :claude-sonnet
   {:cost 0.090
    :latency 4.2
    :best-for [:complex-reasoning :critical-precision :compliance]
    :strengths ["Maximum precision" "Complex reasoning" "Critical compliance"]
    :weaknesses ["Expensive" "Higher latency"]}})

(defn select-optimal-model
  "Select optimal model using decision tree.

  Decision logic (priority order):
  1. Critical precision → Sonnet (compliance, medical)
  2. Large text + cost-sensitive → Haiku (>2K tokens, high cost sensitivity)
  3. JSON output + fast → Gemini Flash (structured output, latency requirement)
  4. Complex reasoning → Sonnet (multi-step logic, analysis)
  5. Default → Gemini Flash (best general-purpose cost/benefit)

  Args:
    requirements - ModelRequirements record

  Returns:
    {:model keyword
     :rationale string
     :estimated-cost float}

  Example:
    (select-optimal-model
      (map->ModelRequirements
        {:complexity :high
         :precision-level :critical
         :input-size :medium
         :output-format :json
         :cost-sensitivity :low
         :latency-req :medium}))
    ;; => {:model :claude-sonnet
    ;;     :rationale 'Critical precision required (compliance/medical)'
    ;;     :estimated-cost 0.09}"
  [requirements]
  (cond
    ;; Rule 1: Critical precision → Sonnet
    (= (:precision-level requirements) :critical)
    {:model :claude-sonnet
     :rationale "Critical precision required (compliance, medical, financial)"
     :estimated-cost 0.09}

    ;; Rule 2: Large text + cost-sensitive → Haiku
    (and (= (:input-size requirements) :large)
         (= (:cost-sensitivity requirements) :high))
    {:model :claude-haiku
     :rationale "Large text (>2K tokens) + high cost sensitivity"
     :estimated-cost 0.020}

    ;; Rule 3: JSON output + latency requirement → Gemini Flash
    (and (= (:output-format requirements) :json)
         (#{:fast :medium} (:latency-req requirements)))
    {:model :gemini-flash
     :rationale "JSON output + latency requirement (<10s)"
     :estimated-cost 0.075}

    ;; Rule 4: Complex reasoning → Sonnet
    (= (:complexity requirements) :high)
    {:model :claude-sonnet
     :rationale "High complexity requires advanced reasoning"
     :estimated-cost 0.09}

    ;; Rule 5: Default → Gemini Flash
    :else
    {:model :gemini-flash
     :rationale "Default - best general-purpose cost/benefit ratio"
     :estimated-cost 0.075}))

(defn get-model-for-system
  "Apply decision tree to healthcare pipeline agents.

  Agent-specific routing:
  - S.1.1 (extraction): Gemini Flash (JSON, LGPD precision, fast)
  - S.1.2 (claims): Gemini Flash (simple task, JSON, cheap)
  - S.2-1.2 (references): Haiku (long text analysis, cost-sensitive)
  - S.3-2 (SEO): Gemini Flash (standard precision, JSON)
  - S.4 (consolidation): Sonnet 10% (sensitive data), Gemini Flash 90%

  Args:
    system-id - :s11, :s12, :s212, :s32, :s4
    context   - Execution context (for dynamic routing)

  Returns:
    {:model keyword, :rationale string}

  Example:
    (get-model-for-system :s4 {:s11 {:dados_sensiveis_detectados ['saude_mental']}})
    ;; => {:model :claude-sonnet
    ;;     :rationale 'Complex case: sensitive data detected'}"
  [system-id context]
  (case system-id
    :s11  ; Data extraction + LGPD detection
    (select-optimal-model
      (map->ModelRequirements
        {:complexity :medium
         :precision-level :high  ; LGPD detection is critical
         :input-size :small
         :output-format :json
         :cost-sensitivity :medium
         :latency-req :fast}))
    ;; => Gemini Flash (good JSON, sufficient precision, fast)

    :s12  ; Claims identification
    (select-optimal-model
      (map->ModelRequirements
        {:complexity :low
         :precision-level :standard
         :input-size :small
         :output-format :json
         :cost-sensitivity :high
         :latency-req :fast}))
    ;; => Gemini Flash (simple task, very cheap)

    :s212  ; Scientific reference search
    (let [input-length (count (str (:claims context)))]
      (select-optimal-model
        (map->ModelRequirements
          {:complexity :medium
           :precision-level :high
           :input-size (if (> input-length 2000) :large :medium)
           :output-format :json
           :cost-sensitivity :high
           :latency-req :medium})))
    ;; => Haiku (long text, cheap, good precision)

    :s32  ; SEO optimization
    (select-optimal-model
      (map->ModelRequirements
        {:complexity :medium
         :precision-level :standard
         :input-size :small
         :output-format :json
         :cost-sensitivity :medium
         :latency-req :fast}))
    ;; => Gemini Flash (SEO is standard task)

    :s4  ; Final consolidation
    (let [has-sensitive-data? (get-in context [:s11 :dados_sensiveis_detectados])
          many-references? (> (count (get-in context [:s212 :references])) 10)]
      (if (or has-sensitive-data? many-references?)
        {:model :claude-sonnet
         :rationale "Complex case: sensitive data OR many references (>10)"}
        {:model :gemini-flash
         :rationale "Standard case: no complexity triggers"}))
    ;; => Sonnet 10%, Gemini Flash 90% (production distribution)
    ))

(comment
  ;; Usage in pipeline
  (def s4-model (get-model-for-system :s4 pipeline-context))

  (def agent (if (= (:model s4-model) :claude-sonnet)
              (create-claude-agent "claude-3.5-sonnet")
              (create-gemini-agent "gemini-2.0-flash")))

  ;; Production metrics (multi-model routing):
  ;; - Distribution: 72% Gemini, 18% Haiku, 10% Sonnet
  ;; - Cost per pipeline: $0.304 (vs $0.391 single-model)
  ;; - Savings: 22%
  ;; - Quality: 87.8% success rate (unchanged)
  )
```

### Production Example: Comprehensive Cost Optimization

```clojure
(ns lab.optimization.cost-tracking
  "Production cost monitoring and optimization"
  (:require [next.jdbc :as jdbc]
            [next.jdbc.result-set :as rs]
            [cheshire.core :as json]
            [clojure.core.cache :as cache]
            [lab.optimization.model-selection :as model-sel]))

(defn count-tokens-estimate
  "Fast token estimation (1 token ≈ 4 characters).

  Production systems should use model-specific tokenizers
  (tiktoken for GPT, cl100k_base, etc.). This is a reasonable
  approximation for cost estimation.

  Args:
    text - String to estimate

  Returns:
    Estimated token count (integer)"
  [text]
  (int (/ (count text) 4.0)))

(defn trim-context
  "Remove excessive whitespace from context.

  Optimizations:
  - Max 2 consecutive newlines (not 3+)
  - Single spaces only (not multiple)
  - Trim leading/trailing whitespace

  Args:
    context - String context

  Returns:
    Trimmed string

  Example:
    (trim-context 'Line 1\n\n\n\nLine 2   extra  spaces')
    ;; => 'Line 1\n\nLine 2 extra spaces'"
  [context]
  (-> context
      (clojure.string/replace #"\n{3,}" "\n\n")  ; Max 2 newlines
      (clojure.string/replace #" {2,}" " ")      ; Single spaces
      clojure.string/trim))

(defn add-output-constraints
  "Add output size/format constraints to prompt.

  Reduces output tokens by guiding model to be concise.
  Production data shows 15-20% token reduction in outputs.

  Args:
    base-prompt - Original prompt string
    constraints - {:max-words int, :format :json/:markdown, :brevity :high/:medium}

  Returns:
    Prompt with constraints appended

  Example:
    (add-output-constraints
      base-prompt
      {:max-words 500, :format :json, :brevity :high})
    ;; Appends: '**OUTPUT CONSTRAINTS:**
    ;;           - Maximum 500 words
    ;;           - Format: JSON only, no additional text
    ;;           - Brevity: Concise responses, no unnecessary explanations'"
  [base-prompt constraints]
  (let [constraint-text
        (str "\n\n**OUTPUT CONSTRAINTS:**\n"
             (when-let [max-words (:max-words constraints)]
               (str "- Maximum " max-words " words\n"))
             (when (= (:format constraints) :json)
               "- Format: JSON only, no additional text\n")
             (when (= (:brevity constraints) :high)
               "- Brevity: Concise responses, no unnecessary explanations\n")
             "- No repetitions or redundancy\n")]

    (str base-prompt constraint-text)))

(defn track-system-cost!
  "Record agent execution cost to database.

  Enables:
  - Historical cost analysis
  - Per-agent cost breakdown
  - Budget alerting
  - Monthly cost prediction

  Args:
    db-spec     - Database connection spec
    pipeline-id - UUID of pipeline execution
    system-id   - Agent identifier (:s11, :s12, etc.)
    cost        - Cost in USD (float)
    model       - Model name string
    metadata    - Additional metadata map

  Returns:
    Inserted row ID

  Example:
    (track-system-cost!
      db-spec
      pipeline-id
      :s212
      0.067
      'claude-3-haiku'
      {:tokens 3350, :latency-ms 8400})"
  [db-spec pipeline-id system-id cost model metadata]
  (jdbc/execute-one!
    (jdbc/get-datasource db-spec)
    ["INSERT INTO pipeline_costs
      (pipeline_id, system_id, cost_usd, model, metadata_json, created_at)
      VALUES (?::uuid, ?, ?, ?, ?::jsonb, NOW())
      RETURNING id"
     (str pipeline-id)
     (name system-id)
     cost
     model
     (json/generate-string metadata)]))

(defn get-daily-costs
  "Aggregate costs for a specific date.

  Returns:
    {:total-cost float
     :request-count int
     :avg-cost-per-request float
     :by-system {:s11 float, :s12 float, ...}
     :by-model {:gemini-flash float, :claude-haiku float, ...}}

  Example:
    (get-daily-costs db-spec (java.time.LocalDate/now))
    ;; => {:total-cost 12.47
    ;;     :request-count 78
    ;;     :avg-cost-per-request 0.16
    ;;     :by-system {:s11 2.34, :s12 1.09, :s212 3.12, :s32 2.03, :s4 3.89}
    ;;     :by-model {:gemini-flash 8.93, :claude-haiku 2.11, :claude-sonnet 1.43}}"
  [db-spec date]
  (let [daily-data (jdbc/execute!
                     (jdbc/get-datasource db-spec)
                     ["SELECT system_id, model, SUM(cost_usd) as total_cost, COUNT(*) as count
                       FROM pipeline_costs
                       WHERE DATE(created_at) = ?::date
                       GROUP BY system_id, model"
                      (str date)]
                     {:builder-fn rs/as-unqualified-lower-maps})

        total-cost (reduce + (map :total_cost daily-data))
        request-count (count (distinct (map :pipeline_id daily-data)))

        by-system (reduce
                   (fn [acc row]
                     (update acc (keyword (:system_id row))
                            (fnil + 0) (:total_cost row)))
                   {}
                   daily-data)

        by-model (reduce
                  (fn [acc row]
                    (update acc (keyword (:model row))
                           (fnil + 0) (:total_cost row)))
                  {}
                  daily-data)]

    {:total-cost total-cost
     :request-count request-count
     :avg-cost-per-request (if (pos? request-count)
                            (/ total-cost request-count)
                            0.0)
     :by-system by-system
     :by-model by-model}))

(defn check-budget-alert!
  "Check if daily budget threshold is exceeded.

  Alerting thresholds:
  - 80%: Warning (print alert)
  - 100%: Critical (print alert + consider blocking)

  Args:
    db-spec      - Database spec
    date         - Date to check (default: today)
    budget-limit - Daily budget in USD (default: $50)

  Returns:
    {:alert? boolean
     :current-cost float
     :budget-limit float
     :percent-used float}

  Example:
    (check-budget-alert! db-spec :budget-limit 50.0)
    ;; If at $42:
    ;; Prints: '⚠️ ALERT: Daily budget at 84.0%'
    ;; => {:alert? true, :current-cost 42.0, :budget-limit 50.0, :percent-used 84.0}"
  [db-spec & {:keys [date budget-limit]}]
  (let [date (or date (java.time.LocalDate/now))
        budget-limit (or budget-limit 50.0)
        daily-costs (get-daily-costs db-spec date)
        current-cost (:total-cost daily-costs)
        percent-used (* 100 (/ current-cost budget-limit))]

    (when (> percent-used 80.0)
      (println "⚠️ ALERT: Daily budget at" (format "%.1f%%" percent-used))
      (when (> percent-used 100.0)
        (println "🚨 CRITICAL: Daily budget EXCEEDED!")))

    {:alert? (> percent-used 80.0)
     :current-cost current-cost
     :budget-limit budget-limit
     :percent-used percent-used}))

(defn predict-monthly-cost
  "Predict monthly cost based on recent trend.

  Uses last N days to calculate daily average, then
  extrapolates to 30 days. Calculates confidence based
  on coefficient of variation (std dev / mean).

  Args:
    db-spec         - Database spec
    days-to-analyze - Lookback period (default: 7)

  Returns:
    {:daily-avg float
     :monthly-prediction float
     :confidence :high/:medium/:low
     :std-dev float}

  Confidence levels:
  - High: CV < 0.2 (stable, predictable)
  - Medium: CV < 0.5 (moderate variation)
  - Low: CV >= 0.5 (high variation, unpredictable)

  Example:
    (predict-monthly-cost db-spec 14)
    ;; => {:daily-avg 11.23
    ;;     :monthly-prediction 336.90
    ;;     :confidence :high
    ;;     :std-dev 1.87}"
  [db-spec & [days-to-analyze]]
  (let [days (or days-to-analyze 7)
        daily-costs (map
                      #(get-daily-costs db-spec %)
                      (take days (iterate #(.minusDays % 1) (java.time.LocalDate/now))))

        daily-avg (/ (reduce + (map :total-cost daily-costs)) days)
        monthly-prediction (* daily-avg 30)

        ;; Calculate variance for confidence
        variance (/ (reduce + (map #(Math/pow (- (:total-cost %) daily-avg) 2) daily-costs))
                   days)
        std-dev (Math/sqrt variance)
        coefficient-of-variation (/ std-dev daily-avg)

        confidence (cond
                    (< coefficient-of-variation 0.2) :high
                    (< coefficient-of-variation 0.5) :medium
                    :else :low)]

    {:daily-avg daily-avg
     :monthly-prediction monthly-prediction
     :confidence confidence
     :std-dev std-dev}))

(comment
  ;; Daily cost monitoring
  (def today-costs (get-daily-costs db-spec (java.time.LocalDate/now)))
  ;; => {:total-cost 12.47
  ;;     :request-count 78
  ;;     :avg-cost-per-request 0.16
  ;;     :by-system {:s11 2.34, :s12 1.09, :s212 3.12, :s32 2.03, :s4 3.89}
  ;;     :by-model {:gemini-flash 8.93, :claude-haiku 2.11, :claude-sonnet 1.43}}

  ;; Budget alerting
  (check-budget-alert! db-spec :budget-limit 50.0)
  ;; => {:alert? false, :current-cost 12.47, :budget-limit 50.0, :percent-used 24.9}

  ;; Monthly cost prediction
  (def prediction (predict-monthly-cost db-spec 14))
  ;; => {:daily-avg 11.23
  ;;     :monthly-prediction 336.90
  ;;     :confidence :high
  ;;     :std-dev 1.87}

  ;; Production case: Healthcare pipeline
  ;; - 20 posts/month × $0.162 = $3.24/month (after optimization)
  ;; - vs manual: 20 posts × 4.25h × R$ 45/h = R$ 3,825/month
  ;; - ROI: +180% (R$ 3,094 savings, or ~$620 USD)
  )
```

## 💡 Best Practices

1. **Measure Before Optimizing**
   - **Rationale**: Optimization without data is guesswork. Measure baseline to quantify improvements.
   - **Example**: Healthcare pipeline measured $0.391 baseline. After optimization, $0.162 (-58%). Without baseline, no way to prove ROI.

2. **Start with High-Impact Optimizations**
   - **Rationale**: 80/20 rule applies. Caching (29% savings) and multi-model (22% savings) are quick wins. Token optimization (3% savings) is lower priority.
   - **Example**: Implemented caching first (2h effort, 29% savings). Then multi-model routing (6h effort, 22% savings). Total: 51% savings in 8h.

3. **A/B Test Model Changes**
   - **Rationale**: Cheaper models may reduce quality. A/B test 10% of traffic before full rollout.
   - **Example**: Tested Haiku vs Gemini Flash for S.2-1.2. Haiku was 73% cheaper, but 2% lower quality (acceptable). Rolled out to 100%.

4. **Set Budget Alerts**
   - **Rationale**: Cost overruns are invisible without monitoring. Alert at 80% of daily budget.
   - **Example**: Set $50/day budget. Alert at $40 triggers review. Prevented $200 overrun when batch job doubled volume.

5. **Cache Aggressively for Stable Data**
   - **Rationale**: API contexts (PubMed, SEO keywords) change slowly. 24h TTL achieves 73% hit rate with no quality impact.
   - **Example**: PubMed cache saves $0.049/request × 73% hit rate = $0.036/request. Annual: $0.036 × 12000 = $432 savings.

6. **Optimize Expensive Agents First**
   - **Rationale**: Pareto principle - 75% of cost in 2 agents (S.2-1.2, S.4). Optimize those first.
   - **Example**: S.4 was 46% of total cost ($0.18/$0.391). Multi-model routing reduced to $0.14 (-22%). Bigger impact than optimizing S.1.2 (5% of cost).

## 🔗 Related Skills

- [`cva-concepts-agent-types`](../cva-concepts-agent-types/SKILL.md) - Different agent types have different cost profiles ⭐
- [`cva-healthcare-pipeline`](../cva-healthcare-pipeline/SKILL.md) - Real cost optimization case study ⭐
- [`cva-patterns-workflows`](../cva-patterns-workflows/SKILL.md) - Parallelization for cost-neutral latency reduction
- [`cva-patterns-context`](../cva-patterns-context/SKILL.md) - Caching strategies for context management
- [`cva-basics-models`](../cva-basics-models/SKILL.md) - Model capabilities and pricing
- [`cva-basics-prompts`](../cva-basics-prompts/SKILL.md) - Prompt engineering for token efficiency

## 📘 Additional Resources

### Advanced Optimization Techniques

**Batch Processing**: Process multiple requests in single API call (where supported). Gemini Batch API offers 50% discount for async processing (24h latency acceptable).

**Prompt Caching** (Anthropic): Cache prompt prefixes across requests. Healthcare pipeline could cache LGPD guidelines (50% of prompt) → 50% cost reduction on input tokens.

**Speculative Decoding**: Use small model to draft, large model to verify. Can reduce cost by 30-40% with 10% latency increase. Not yet supported in Vertex AI (as of 2025-01).

### Model Selection Decision Matrix

| Use Case | Recommended Model | Cost (1M in/out) | Rationale |
|----------|-------------------|------------------|-----------|
| JSON extraction | Gemini Flash | $0.075 / $0.30 | Reliable JSON, fast |
| Long text analysis | Claude Haiku | $0.02 / $0.10 | VERY cheap, good comprehension |
| Critical compliance | Claude Sonnet | $0.09 / $0.45 | Maximum precision |
| Complex reasoning | Claude Sonnet | $0.09 / $0.45 | Multi-step logic |
| SEO/Marketing | Gemini Flash | $0.075 / $0.30 | Creative, fast |
| Code generation | Gemini Flash | $0.075 / $0.30 | Good code, cheap |

### Cost Benchmarks (Healthcare Pipeline)

| Optimization Layer | Cost Before | Cost After | Savings | Effort (hours) |
|--------------------|-------------|------------|---------|----------------|
| Baseline (Sonnet-only) | $0.450 | - | - | - |
| Single model (Gemini) | $0.450 | $0.391 | 13% | 0 |
| + Multi-model routing | $0.391 | $0.304 | 22% | 6 |
| + Token optimization | $0.304 | $0.295 | 3% | 2 |
| + Caching | $0.295 | $0.162 | 45% | 4 |
| **TOTAL** | $0.450 | $0.162 | **64%** | **12** |

**ROI**: 64% cost reduction in 12 hours of engineering effort. For 12,000 pipelines/year, saves $3,456 annually. Payback period: <1 week of production usage.

### Monitoring Dashboard Metrics

**Key Metrics to Track:**
1. Cost per pipeline (daily average)
2. Cost breakdown by agent (identify expensive agents)
3. Cost breakdown by model (track multi-model distribution)
4. Cache hit rates (static/query/API contexts)
5. Daily budget % used (alert threshold)
6. Monthly cost prediction (with confidence interval)

**Alerting Rules:**
- Daily budget >80%: Warning (review usage)
- Daily budget >100%: Critical (investigate spike)
- Cost per pipeline >$0.25: Warning (should be $0.162 average)
- Cache hit rate <50%: Warning (cache misconfiguration)
- Model distribution skew >20%: Info (expected 70/20/10, alert if 50/50/0)

### Scaling Considerations

**High Volume (>10,000 requests/day):**
- Implement batch processing (50% discount)
- Use Vertex AI quotas/rate limits
- Consider dedicated model deployments (reserved capacity)

**Multi-Tenant:**
- Track costs per tenant (separate billing)
- Implement per-tenant budget limits
- Fair queuing to prevent tenant starvation

**Global Deployment:**
- Regional pricing differences (e.g., us-central1 vs europe-west4)
- Network egress costs for cross-region API calls
- Cache replication strategy (Redis multi-region)
