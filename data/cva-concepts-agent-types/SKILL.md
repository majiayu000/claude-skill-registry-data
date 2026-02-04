---
name: cva-concepts-agent-types
description: Agent system taxonomy (A/B/C/D) based on capabilities - Type A (pure AI), Type B (AI+database context), Type C (AI+web grounding), Type D (AI+database+web). Includes latency/cost analysis, decision tree, healthcare pipeline mapping, and ROI optimization. Use when designing agent architecture, selecting agent type, optimizing costs, or implementing multi-agent workflows.
allowed-tools: Read,Bash,Edit,Write
---

# Agent System Types (A/B/C/D Taxonomy)

> **Core Concept:** Taxonomy of AI agent systems based on their **capabilities** (data sources)
> **Origin:** Validated architecture from FluSisTip project (healthcare production system)
> **Applicability:** Generic for any regulated domain or rich-context requirements

---

## 🎯 Overview

In production AI agent development, especially in regulated domains (healthcare, legal, finance), not all agents need the same **capabilities**. The A/B/C/D typology classifies agents by **type of data they access**, enabling cost, performance, and complexity optimization.

### Complexity Hierarchy

```
Type A (Pure AI)
  ↓ +Database Context
Type B (AI + CAG)
  ↓ +Web Grounding
Type C (AI + Web)
  ↓ +Database Context
Type D (AI + CAG + Web)
```

---

## 📊 Quick Comparison

| Type | Capabilities | Cost | Latency | Use Cases | Vertex AI Feature |
|------|--------------|------|---------|-----------|-------------------|
| **A** | Pure AI | $ | ~3s | Analysis, classification, extraction | Standard prompting |
| **B** | AI + CAG | $$ | ~5s | Personalization, compliance | Context injection |
| **C** | AI + Web | $$$ | ~12s | Research, external validation | Grounding API |
| **D** | AI + CAG + Web | $$$$ | ~17s | Maximum context consolidation | Context + Grounding |

**Cost Legend:**
- $ = $0.001 - $0.05
- $$ = $0.05 - $0.15
- $$$ = $0.15 - $0.30
- $$$$ = $0.30 - $0.50

---

## 🔷 Type A: Pure AI

### Definition

**Direct input → LLM → Structured output**

Agent processes **only** data provided in input (by user or previous system in workflow). No database access, external APIs, or web search.

### Characteristics

- ✅ **Fastest**: ~3s average time
- ✅ **Cheapest**: ~$0.02 per execution
- ✅ **Deterministic**: Same input = same output
- ✅ **Stateless**: No state between calls
- ❌ **Limited context**: Only what's in the prompt

### When to Use

1. **Analysis & Extraction**: Identify entities, extract structured data
2. **Classification**: Categorize content, detect sentiment
3. **Transformation**: Convert formats, restructure data
4. **Syntactic Validation**: Check format, data completeness
5. **Query Generation**: Create search strategies

### Healthcare Example: S.1.2 - Claims Identification

**Function:** Identify medical claims in raw text requiring scientific validation

**Implementation Pattern (Clojure):**

```clojure
(ns lab.agents.claims-identifier
  "Type A: Pure AI - Medical claims identification"
  (:require [lab.config.google-cloud :as gc])
  (:import [com.google.cloud.vertexai VertexAI]
           [com.google.cloud.vertexai.generativeai GenerativeModel]))

(defn create-claims-agent
  "Creates Type A agent for medical claims identification."
  [{:keys [project-id location model]
    :or {model "gemini-1.5-flash"}}]
  (let [vertex-ai (VertexAI. project-id location)
        generation-config (-> (GenerationConfig/newBuilder)
                              (.setTemperature 0.2)  ; Low for technical analysis
                              (.setMaxOutputTokens 2000)
                              (.build))
        model-instance (.getGenerativeModel vertex-ai model)]
    (.withGenerationConfig model-instance generation-config)))

(defn identify-claims
  "Identifies medical claims in content."
  [agent content specialty]
  (let [prompt (format
                 "Analyze this %s content and extract ALL scientific claims
                 that require validation. Return JSON with 'claims' array."
                 specialty content)
        response (.generateContent agent prompt)
        text (-> response .getText)]
    (cheshire.core/parse-string text true)))
```

**Real Metrics (Healthcare Pipeline):**
- Average time: 3.2s
- Average cost: $0.018
- Success rate: 96.1%
- Average tokens: 520 total

---

## 🔶 Type B: AI + CAG (Context-Aware Generation)

### Definition

**Input + Database Context → LLM → Personalized output**

Agent **enriches prompt** with data from tenant database (Context-Aware Generation). Enables personalization based on history, profile, stored business rules.

### Characteristics

- ✅ **Rich context**: Access tenant data (regulations, profiles, history)
- ✅ **Personalized**: Adapts output to specific context
- ✅ **Compliance**: Incorporates stored business rules
- ⚠️ **Query overhead**: +2s to fetch contexts
- ⚠️ **Cache important**: Contexts should be cached (TTL 1h+)

### When to Use

1. **Output Personalization**: Adapt tone, style, language to profile
2. **Dynamic Compliance**: Apply tenant-specific rules
3. **History**: Consider previous interactions/decisions
4. **Custom Configuration**: Client-specific guidelines
5. **Rule Validation**: Check conformance with stored policies

### Healthcare Example: S.3-2 - SEO + Professional Profile

**Function:** Optimize content for SEO considering professional profile and specialized keywords

**Implementation Pattern (Clojure):**

```clojure
(ns lab.agents.seo-optimizer
  "Type B: AI + CAG - SEO optimization with tenant context"
  (:require [lab.config.google-cloud :as gc]
            [next.jdbc :as jdbc]))

(defn fetch-professional-profile
  "Fetches complete professional profile (Context 1)."
  [db-spec prof-id]
  (jdbc/execute-one!
    (jdbc/get-datasource db-spec)
    ["SELECT nome_completo, crm, especialidade, anos_experiencia,
             tom_voz, cidade_atuacao
      FROM profissionais
      WHERE id = ?::uuid"
     (str prof-id)]
    {:builder-fn rs/as-unqualified-lower-maps}))

(defn fetch-seo-keywords
  "Fetches specialized SEO keywords (Context 2)."
  [db-spec specialty city]
  (jdbc/execute!
    (jdbc/get-datasource db-spec)
    ["SELECT keyword, tipo, search_volume
      FROM seo_keywords
      WHERE especialidade = ? AND cidade = ?
      ORDER BY relevancia DESC LIMIT 10"
     specialty city]
    {:builder-fn rs/as-unqualified-lower-maps}))

(defn optimize-seo
  "Optimizes content for SEO with professional context."
  [agent db-spec content prof-id]
  (let [profile (fetch-professional-profile db-spec prof-id)
        keywords (fetch-seo-keywords db-spec
                                     (:especialidade profile)
                                     (:cidade_atuacao profile))
        prompt (build-enriched-prompt content profile keywords)
        response (.generateContent agent prompt)]
    (parse-response response)))
```

**Real Metrics:**
- Average time: 5.2s (3.1s LLM + 2.1s queries)
- Average cost: $0.078
- Success rate: 94.7%
- **Cache critical**: Reduces queries by 85% with 1h TTL

---

## 🔷 Type C: AI + Web (Grounding)

### Definition

**Input + Web Search/Grounding → LLM → Validated output**

Agent performs **real-time external searches** (web, scientific databases, public APIs) to enrich context and validate information. Uses Vertex AI Grounding API or custom tools.

### Characteristics

- ✅ **External updated data**: Doesn't depend on model knowledge
- ✅ **Real-time validation**: Search evidence, prices, availability
- ✅ **Trusted sources**: PubMed, Google Scholar, specialized APIs
- ⚠️ **High latency**: +8-12s for complete grounding
- ⚠️ **High cost**: $0.15-0.30 per execution
- ⚠️ **Rate limits**: External APIs may limit requests

### When to Use

1. **Scientific Research**: Search papers, studies, guidelines
2. **Fact Validation**: Verify claims against authoritative sources
3. **Prices/Availability**: Query real-time information
4. **External Compliance**: Check published regulations
5. **Public Data Enrichment**: Government APIs, datasets

### Healthcare Example: S.2-1.2 - Scientific Reference Search

**Function:** Find scientific references to validate medical claims

**Implementation Pattern (Clojure):**

```clojure
(ns lab.agents.scientific-search
  "Type C: AI + Web Grounding - Scientific reference search"
  (:require [lab.config.google-cloud :as gc])
  (:import [com.google.cloud.vertexai.api Tool GroundingMetadata]))

(defn create-grounded-agent
  "Creates Type C agent with grounding enabled."
  [{:keys [project-id location grounding-sources]
    :or {grounding-sources ["google_search" "google_scholar"]}}]
  (let [vertex-ai (VertexAI. project-id location)
        grounding-tool (-> (Tool/newBuilder)
                           (.setGoogleSearchRetrieval
                             (-> (GoogleSearchRetrieval/newBuilder)
                                 (.build)))
                           (.build))
        model-instance (-> (.getGenerativeModel vertex-ai "gemini-1.5-pro")
                           (.withTools [grounding-tool]))]
    model-instance))

(defn search-scientific-references
  "Searches scientific references with grounding."
  [agent claims]
  (let [prompt (format
                 "For each medical claim, search reliable scientific references.
                 Minimum 2 primary sources, 1 systematic review if available.
                 Sources: PubMed, Google Scholar, SciELO. Return JSON."
                 (json/generate-string claims))
        response (.generateContent agent prompt)
        text (-> response .getText)
        grounding-metadata (.getGroundingMetadata response)]
    (assoc (json/parse-string text true)
           :grounding-sources (-> grounding-metadata .getSearchQueries vec)
           :grounding-confidence (-> grounding-metadata .getConfidence))))
```

**Real Metrics:**
- Average time: 12.1s (8.2s grounding + 3.9s LLM)
- Average cost: $0.175
- Success rate: 91.7%
- References/claim: 4.3 average
- **Important**: Rate limiting on public APIs (PubMed: 3 req/s)

---

## 🔶 Type D: AI + CAG + Web (Maximum Context)

### Definition

**Input + Database Context + Web Grounding → LLM → Consolidated output**

Agent combines **all capabilities**: accesses tenant DB AND performs external searches. Maximum possible context, used for final consolidation or complex decisions.

### Characteristics

- ✅ **Maximum context**: Tenant DB + web + input
- ✅ **Complex decisions**: Multiple sources of truth
- ✅ **Total compliance**: Internal rules + external regulations
- ⚠️ **Maximum latency**: 15-20s total
- ⚠️ **Maximum cost**: $0.30-0.50 per execution
- ⚠️ **High complexity**: Orchestration of multiple sources

### When to Use

1. **Final Consolidation**: Aggregate data from multiple sources
2. **Critical Decisions**: Require complete context
3. **Multi-Source Validation**: Check against DB + web
4. **Executive Reports**: Insights from internal + external data
5. **Total Compliance**: Validate against internal rules + public regulations

### Healthcare Example: S.4-1.1-3 - Final Text Consolidation

**Function:** Consolidate all previous outputs (LGPD data, validated claims, references, SEO) into final professional text ready for publication

**Real Metrics:**
- Average time: 16.8s (4.2s queries + 9.5s grounding + 3.1s LLM)
- Average cost: $0.42
- Success rate: 89.3%
- **Trade-off**: Maximum quality vs cost/latency

> 📘 **Complete implementation:** See [`cva-healthcare-pipeline`](../cva-healthcare-pipeline/SKILL.md) skill, System S.4.

---

## 📊 Selection Strategy (Decision Tree)

```
┌─────────────────────────────────────────┐
│ Need external data (web/APIs)?         │
└─────────────┬───────────────────────────┘
              │
        ┌─────┴─────┐
        │           │
       NO          YES
        │           │
        v           v
┌───────────┐  ┌─────────────────────────────┐
│ Need      │  │ Need tenant DB also?        │
│ tenant DB?│  └──────────┬──────────────────┘
└─────┬─────┘             │
      │             ┌─────┴─────┐
  ┌───┴───┐         │           │
  │       │        NO          YES
 NO      YES        │           │
  │       │         v           v
  v       v    ┌────────┐  ┌────────┐
┌───┐  ┌───┐  │ TYPE C │  │ TYPE D │
│ A │  │ B │  │        │  │        │
└───┘  └───┘  └────────┘  └────────┘
```

### Mapping Examples

| Task | Need DB? | Need Web? | Type | Justification |
|------|----------|-----------|------|---------------|
| Extract entities from text | ❌ | ❌ | **A** | Direct input sufficient |
| Classify sentiment | ❌ | ❌ | **A** | Pure text analysis |
| Generate personalized text | ✅ | ❌ | **B** | Need profile/history |
| Validate tenant compliance | ✅ | ❌ | **B** | Rules in DB |
| Search scientific papers | ❌ | ✅ | **C** | External sources |
| Check real-time prices | ❌ | ✅ | **C** | Public APIs |
| Consolidate executive report | ✅ | ✅ | **D** | Internal + market data |
| Total regulatory validation | ✅ | ✅ | **D** | Internal + CFM/CRP rules |

---

## 💡 Best Practices

### 1. Always Start with Type A

> "Premature optimization is the root of all evil" - Donald Knuth

Implement first as Type A. If output is unsatisfactory, consider B/C/D. Often, a well-structured Type A prompt is sufficient.

### 2. Context Caching (Type B)

DB contexts rarely change. Aggressive caching:
- Professional profiles: TTL 1h
- Regulations: TTL 24h
- SEO keywords: TTL 7 days

**Observed savings:** 85% query reduction

### 3. Batch for Type C

Grounding is expensive. Group multiple claims in a single call:

```clojure
;; ❌ Inefficient: 5 calls
(doseq [claim claims]
  (search-references agent [claim]))

;; ✅ Efficient: 1 call
(search-references agent claims)
```

**Savings:** ~70% cost and latency

### 4. Conditional Grounding (Type D)

Not always need web grounding. Use conditional logic:

```clojure
(defn consolidate-content
  [agent inputs]
  (let [db-contexts (fetch-all-contexts inputs)
        needs-grounding? (requires-external-validation? inputs)
        web-data (when needs-grounding?
                   (perform-grounding inputs))]
    (generate-final-content agent db-contexts web-data)))
```

### 5. Fallback Strategy

Grounding can fail (rate limits, timeout). Have fallback to Type B:

```clojure
(defn robust-consolidation
  [agent inputs]
  (try
    (consolidate-tipo-d agent inputs)  ; Try with grounding
    (catch Exception e
      (log/warn "Grounding failed, falling back to Type B" e)
      (consolidate-tipo-b agent inputs))))  ; Fallback without web
```

---

## 🎯 Executive Summary

| Aspect | Type A | Type B | Type C | Type D |
|---------|--------|--------|--------|--------|
| **Primary use** | Analysis, extraction | Personalization | Research, validation | Consolidation |
| **Latency** | ~3s | ~5s | ~12s | ~17s |
| **Cost** | $0.02 | $0.08 | $0.18 | $0.42 |
| **Complexity** | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Success rate** | 96% | 95% | 92% | 89% |
| **When to use** | Default | Tenant context | External data | Critical decisions |

**Recommended Distribution in Pipeline (Healthcare):**
- Type A: 40% of systems (extraction, classification)
- Type B: 40% (personalization, compliance)
- Type C: 15% (scientific validation)
- Type D: 5% (final consolidation)

**ROI Multi-Model + Typing:**
- Savings vs "Type D everywhere": 67%
- Savings vs "Claude-only": 41%
- Average pipeline time: 34.2s (vs 87s all Type D)

---

## 🔗 Related Skills

- [`cva-healthcare-pipeline`](../cva-healthcare-pipeline/SKILL.md) - Practical application of all 4 types ⭐
- [`cva-patterns-cost`](../cva-patterns-cost/SKILL.md) - Cost optimization strategies
- [`cva-patterns-context`](../cva-patterns-context/SKILL.md) - Context management (CAG) implementation
- [`cva-patterns-workflows`](../cva-patterns-workflows/SKILL.md) - Multi-agent orchestration

---

## 📘 Additional Documentation

For detailed examples by type, see:
- [Type A Examples](examples-type-a.md) - Pure AI implementations
- [Type B Examples](examples-type-b.md) - CAG patterns
- [Type C Examples](examples-type-c.md) - Grounding strategies
- [Type D Examples](examples-type-d.md) - Maximum context consolidation
- [Decision Tree](decision-tree.md) - Visual selection guide

---

*This taxonomy is validated in production with proven ROI. Use it to make systematic architecture decisions and optimize costs.*
