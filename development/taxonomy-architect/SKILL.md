---
name: taxonomy-architect
description: Design and maintain classification systems for jobs, skills, and companies. Use when defining categories, resolving edge cases, planning ontology structures, or preparing for semantic search capabilities.
---

# Taxonomy Architect

Design, maintain, and evolve classification systems that power job matching, skill analysis, and company categorization. Ensure taxonomies are precise, consistent, and extensible toward future semantic search capabilities.

## When to Use This Skill

Trigger when user asks to:
- Define or refine job role categories (families, subfamilies)
- Create or update skill taxonomies
- Classify ambiguous roles or edge cases
- Design company categorization schemes
- Plan ontology structures for semantic search
- Resolve classification conflicts or inconsistencies
- Evaluate taxonomy coverage and gaps
- Prepare embeddings or vector search strategies

## Core Principles

### 1. Mutually Exclusive, Collectively Exhaustive (MECE)

Categories at the same level should not overlap, and together should cover all cases.

```
BAD:                          GOOD:
├── Data Analyst              ├── Data Analyst
├── Business Analyst          ├── Analytics Engineer
├── Analytics (overlap!)      ├── Data Engineer
└── BI Developer (overlap!)   └── Data Scientist
```

### 2. User Mental Model Alignment

Categories should match how practitioners describe themselves, not internal corporate structures.

```
BAD (org-chart thinking):     GOOD (practitioner thinking):
├── Engineering               ├── Data Engineer
│   └── Data                  ├── ML Engineer
├── Analytics                 ├── Analytics Engineer
│   └── Data                  └── Data Analyst
└── Science
    └── Data
```

### 3. Stable Core, Flexible Edges

Core categories should be stable over time. Edge cases and emerging roles should be handled without restructuring the core.

```
STABLE CORE:                  EDGE HANDLING:
├── Data Engineer             "AI Engineer" → classify as:
├── ML Engineer               - ML Engineer (if model-focused)
├── Data Scientist            - out_of_scope (if API integration)
└── Analytics Engineer        Document decision, revisit quarterly
```

### 4. Evidence-Based Boundaries

Category boundaries should be defined by observable signals in job postings, not assumptions.

| Signal Type | Examples |
|-------------|----------|
| Title patterns | "Analytics Engineer" vs "Data Analyst" |
| Tool requirements | dbt, Airflow, Spark → Data/Analytics Engineer |
| Responsibility keywords | "build pipelines" vs "create dashboards" |
| Team placement | "Data Platform team" vs "Business Intelligence" |
| Seniority markers | "Principal", "Staff", "Lead", "Senior", "Junior" |

### 5. Semantic Readiness

Design with future embedding/vector search in mind. Categories should be describable in natural language that captures semantic meaning.

```
GOOD (embeddable description):
"Analytics Engineer: Builds and maintains data transformation 
pipelines using tools like dbt, creates metrics layers and 
semantic models, bridges raw data and analyst-ready datasets."

BAD (list of keywords):
"Analytics Engineer: dbt, SQL, data modeling, metrics"
```

---

## Current Taxonomy (v1.5)

### Job Families & Subfamilies

```yaml
job_families:
  product:
    description: "Roles focused on product strategy, discovery, and delivery"
    subfamilies:
      core_pm:
        label: "Core PM"
        description: "General product management for user-facing features"
        signals:
          titles: ["Product Manager", "PM", "Product Lead"]
          keywords: ["roadmap", "user stories", "stakeholders", "prioritization"]
          anti_signals: ["growth", "platform", "API", "ML", "AI"]
        
      growth_pm:
        label: "Growth PM"
        description: "Acquisition, retention, monetization, conversion optimization"
        signals:
          titles: ["Growth PM", "Growth Product Manager"]
          keywords: ["acquisition", "retention", "conversion", "funnel", "experimentation", "A/B testing"]
          
      platform_pm:
        label: "Platform PM"
        description: "Developer tools, APIs, infrastructure products"
        signals:
          titles: ["Platform PM", "API PM", "Developer Experience PM"]
          keywords: ["API", "SDK", "developer", "platform", "infrastructure", "internal tools"]
          
      technical_pm:
        label: "Technical PM"
        description: "Deep technical skills required, often ex-engineers"
        signals:
          titles: ["Technical Product Manager", "TPM"]
          keywords: ["technical requirements", "engineering background", "system design"]
          
      ai_ml_pm:
        label: "AI/ML PM"
        description: "AI/ML products, models, data products"
        signals:
          titles: ["AI PM", "ML PM", "AI Product Manager", "Data Product Manager"]
          keywords: ["machine learning", "AI", "model", "LLM", "GenAI", "data product"]

  data:
    description: "Roles focused on data infrastructure, analysis, and machine learning"
    subfamilies:
      product_analytics:
        label: "Product Analytics"
        description: "Product metrics, experiments, user behavior, growth analytics"
        signals:
          titles: ["Product Analyst", "Growth Analyst", "Product Data Analyst"]
          keywords: ["product metrics", "experimentation", "user behavior", "funnel analysis", "Amplitude", "Mixpanel"]
          anti_signals: ["pipeline", "infrastructure", "model training"]
          
      data_analyst:
        label: "Data Analyst"
        description: "Business reporting, dashboards, SQL analysis, BI tools"
        signals:
          titles: ["Data Analyst", "Business Analyst", "BI Analyst", "Reporting Analyst"]
          keywords: ["dashboards", "reporting", "Tableau", "Power BI", "Looker", "business intelligence"]
          anti_signals: ["dbt", "pipeline", "modeling layer"]
          
      analytics_engineer:
        label: "Analytics Engineer"
        description: "dbt, metrics layer, data modeling, semantic layer"
        signals:
          titles: ["Analytics Engineer", "Data Modeling Engineer"]
          keywords: ["dbt", "data modeling", "metrics layer", "semantic layer", "transformation"]
          disambiguate_from: ["data_analyst", "data_engineer"]
          
      data_engineer:
        label: "Data Engineer"
        description: "Pipelines, infrastructure, ETL/ELT, big data"
        signals:
          titles: ["Data Engineer", "ETL Developer", "Data Platform Engineer"]
          keywords: ["pipeline", "Airflow", "Spark", "ETL", "ELT", "data infrastructure", "Kafka"]
          
      ml_engineer:
        label: "ML Engineer"
        description: "Production ML systems, MLOps, includes LLM/GenAI implementation"
        signals:
          titles: ["ML Engineer", "Machine Learning Engineer", "MLOps Engineer", "AI Engineer"]
          keywords: ["model deployment", "MLOps", "feature store", "model serving", "LLM", "fine-tuning"]
          notes: "AI Engineer roles classify here if model-focused; out_of_scope if primarily API integration"
          
      data_scientist:
        label: "Data Scientist"
        description: "Statistical modeling, predictions, business insights"
        signals:
          titles: ["Data Scientist", "Senior Data Scientist", "Applied Scientist"]
          keywords: ["statistical modeling", "prediction", "regression", "classification", "causal inference"]
          disambiguate_from: ["ml_engineer", "research_scientist"]
          
      research_scientist:
        label: "Research Scientist (ML/AI)"
        description: "Novel ML research, publications, pushing state-of-the-art"
        signals:
          titles: ["Research Scientist", "ML Researcher", "AI Researcher"]
          keywords: ["publications", "novel", "state-of-the-art", "research", "PhD"]
          
      data_architect:
        label: "Data Architect"
        description: "Data strategy, governance, platform design"
        signals:
          titles: ["Data Architect", "Enterprise Data Architect", "Data Governance Lead"]
          keywords: ["data strategy", "governance", "data catalog", "metadata", "architecture"]
```

### Seniority Levels

```yaml
seniority:
  junior:
    label: "Junior"
    signals:
      titles: ["Junior", "Jr", "Associate", "Entry Level", "Graduate"]
      experience: ["0-2 years", "entry level", "new grad"]
      
  mid:
    label: "Mid-Level"
    signals:
      titles: ["Data Engineer", "Product Manager"] # No prefix = usually mid
      experience: ["2-5 years", "3+ years"]
      
  senior:
    label: "Senior"
    signals:
      titles: ["Senior", "Sr", "Lead"]
      experience: ["5+ years", "7+ years"]
      
  staff_plus:
    label: "Staff+"
    signals:
      titles: ["Staff", "Principal", "Distinguished", "Architect", "Director"]
      experience: ["10+ years", "extensive experience"]
```

### Working Arrangement

```yaml
working_arrangement:
  onsite:
    label: "Onsite"
    signals: ["on-site", "in-office", "office-based", "in-person"]
    
  hybrid:
    label: "Hybrid"
    signals: ["hybrid", "flexible", "2-3 days in office", "partial remote"]
    
  remote:
    label: "Remote"
    signals: ["remote", "work from home", "distributed", "anywhere"]
    qualifiers: ["remote (US only)", "remote (timezone restricted)"]
```

---

## Skills Taxonomy

### Structure

```yaml
skills:
  parent_categories:
    product:
      label: "Product Skills"
      families:
        - discovery_research
        - execution_delivery
        - experimentation
        - analytics_pm
        - stakeholder_mgmt
        
    data_ml:
      label: "Data/ML Skills"
      families:
        - programming
        - analytics_stats
        - classical_ml
        - deep_learning
        - llm_genai
        - big_data
        - pipelines_orchestration
        - data_modeling
        - warehouses_lakes
        - mlops
        - cloud
        - streaming
        - visualization
        
    platform_infra:
      label: "Platform/Infra Skills"
      families:
        - deployment
        - infrastructure_code
        - ci_cd
        - monitoring
```

### Skill Family Details

```yaml
data_ml:
  programming:
    label: "Programming Languages"
    skills: ["Python", "R", "SQL", "Scala", "Java", "Julia"]
    notes: "SQL is both a language and a skill; always extract"
    
  analytics_stats:
    label: "Analytics & Statistics"
    skills: ["Statistics", "Probability", "Regression", "Causal inference", 
             "Time series", "Hypothesis testing", "Bayesian analysis"]
             
  classical_ml:
    label: "Classical Machine Learning"
    skills: ["Scikit-learn", "XGBoost", "LightGBM", "Random Forest",
             "Logistic regression", "SVM", "Feature engineering"]
             
  deep_learning:
    label: "Deep Learning"
    skills: ["PyTorch", "TensorFlow", "Keras", "Neural networks",
             "CNNs", "RNNs", "Computer vision", "NLP"]
             
  llm_genai:
    label: "LLM/GenAI"
    skills: ["LLMs", "Transformers", "GPT", "BERT", "Claude",
             "Prompt engineering", "RAG", "Vector databases",
             "LangChain", "Embeddings", "Fine-tuning"]
    notes: "Fast-evolving category; review quarterly"
    
  big_data:
    label: "Big Data Processing"
    skills: ["Spark", "PySpark", "Hadoop", "Hive", "Presto", "Flink"]
    
  pipelines_orchestration:
    label: "Pipelines & Orchestration"
    skills: ["Airflow", "Dagster", "Prefect", "Luigi",
             "Data pipelines", "ETL", "ELT"]
             
  data_modeling:
    label: "Data Modeling"
    skills: ["dbt", "Data modeling", "Dimensional modeling",
             "Star schema", "Data warehouse design"]
             
  warehouses_lakes:
    label: "Warehouses & Lakes"
    skills: ["Snowflake", "BigQuery", "Redshift", "Databricks",
             "Athena", "Delta Lake", "Data lake"]
             
  mlops:
    label: "MLOps"
    skills: ["MLflow", "Kubeflow", "Model serving", "Model monitoring",
             "Feature stores", "Model registry", "Weights & Biases"]
             
  cloud:
    label: "Cloud Platforms"
    skills: ["AWS", "GCP", "Azure", "S3", "EC2", "Lambda", "Cloud Functions"]
    
  streaming:
    label: "Streaming"
    skills: ["Kafka", "Kinesis", "Pub/Sub", "Real-time processing"]
    
  visualization:
    label: "Data Visualization"
    skills: ["Tableau", "Power BI", "Looker", "Metabase",
             "Plotly", "Matplotlib", "Seaborn"]
```

---

## Company/Employer Taxonomy

**System of Record:** `docs/schema_taxonomy.yaml` (see `enums.employer_industry`)

### Employer Industry (20 Domain-Focused Categories)

**Design Decision:** These are industry VERTICALS, not business models. "B2B SaaS" was intentionally excluded - it's a business model that spans multiple industries. A company like Stripe is `fintech` even though it sells B2B SaaS.

| Code | Label | Examples |
|------|-------|----------|
| `fintech` | FinTech | Stripe, Monzo, Affirm, Plaid |
| `healthtech` | HealthTech | Flatiron, Omada, Oscar |
| `ecommerce` | E-commerce & Marketplace | Instacart, Deliveroo, Etsy |
| `ai_ml` | AI/ML | OpenAI, Anthropic, Harvey AI |
| `consumer` | Consumer Tech | Spotify, Reddit, Strava |
| `mobility` | Mobility & Logistics | Uber, Waymo, Zipline |
| `proptech` | PropTech | Airbnb, Zillow, CoStar |
| `edtech` | EdTech | Coursera, Duolingo |
| `climate` | Climate Tech | Watershed, Crusoe |
| `crypto` | Crypto & Web3 | Coinbase, Kraken |
| `devtools` | Developer Tools | GitHub, Vercel, Linear |
| `data_infra` | Data Infrastructure | Snowflake, Databricks, dbt Labs |
| `cybersecurity` | Cybersecurity | Okta, Vanta, 1Password |
| `hr_tech` | HR Tech | Rippling, Gusto, Deel |
| `martech` | Marketing Tech | Braze, Amplitude, HubSpot |
| `professional_services` | Professional Services | Deloitte, Accenture |
| `productivity` | Productivity & Collaboration | Notion, Asana, Airtable, Calendly |
| `hardware` | Hardware & Robotics | Apple, Gecko Robotics |
| `other` | Other | Catch-all |

### Employer Size

| Code | Label | Signals |
|------|-------|---------|
| `startup` | Startup (1-50) | seed, series A, early stage |
| `scaleup` | Scale-up (51-500) | series B/C, growth stage |
| `enterprise` | Enterprise (500+) | public, Fortune 500, established |

### Multi-Industry Companies

Some companies span multiple industries. Classification rules:

1. **Single primary industry** - Each company gets ONE `industry` value (MECE)
2. **Classify by core product/revenue** - Stripe is `fintech` (payments), not `devtools`
3. **For conglomerates** - Classify by the division most relevant to the job posting

| Company | Industry | Rationale |
|---------|----------|-----------|
| Stripe | `fintech` | Core is payments, even though they have dev tools |
| Uber | `mobility` | Core is transportation |
| Airbnb | `proptech` | Real estate marketplace |
| Amazon (AWS jobs) | `devtools` or `data_infra` | Depends on specific role |

---

## Edge Case Resolution

### Decision Framework

When encountering ambiguous roles:

```
1. Check title patterns against known signals
2. Analyze job description for disambiguating keywords
3. Look at team/department placement
4. Consider required tools/skills
5. Apply "where would the practitioner self-identify?" test
6. If still ambiguous, document and classify to best fit
7. Flag for quarterly taxonomy review
```

### Documented Edge Cases

| Role Pattern | Decision | Rationale |
|--------------|----------|-----------|
| "AI Engineer" | ML Engineer OR out_of_scope | If model-focused → ML Engineer; if API integration only → out_of_scope |
| "Data Analyst" with dbt | Analytics Engineer | dbt is strong signal for AE over DA |
| "Business Intelligence Engineer" | Data Analyst | Despite "engineer" title, typically dashboard/reporting focused |
| "Applied Scientist" | Data Scientist | Amazon-specific title; responsibilities align with DS |
| "Product Analyst" | Product Analytics | Distinct from generic Data Analyst by product focus |
| "Growth Engineer" | out_of_scope | Engineering role, not data/product |
| "Technical Program Manager" | out_of_scope | Program management, not product management |

### Geographic Variations

| Term | US Meaning | UK Meaning | Resolution |
|------|------------|------------|------------|
| "Data Scientist" | Often ML-heavy | Sometimes more analytics | Check for ML signals |
| "Analyst" | Entry-level connotation | Can be senior | Use seniority signals |

---

## Ontology Design (Future: Semantic Search)

### Current State: Taxonomy

```
Hierarchical classification
├── Fixed categories
├── Rule-based assignment
└── Exact match on signals
```

### Future State: Ontology

```
Semantic network
├── Entities with relationships
├── Embedding-based similarity
├── Natural language queries
└── Fuzzy matching with confidence
```

### Preparation Steps

**1. Rich Entity Descriptions**

Every category needs a natural language description suitable for embedding:

```yaml
analytics_engineer:
  embedding_description: |
    An Analytics Engineer builds and maintains the data transformation 
    layer between raw data sources and analyst-ready datasets. They 
    typically work with tools like dbt to create reusable data models, 
    define business metrics in a semantic layer, and ensure data quality 
    through testing. They bridge the gap between Data Engineers who 
    build pipelines and Data Analysts who consume clean data.
    
    Related roles: Data Analyst, Data Engineer, BI Developer
    Key differentiator: Focuses on transformation and modeling, not 
    pipeline infrastructure or end-user dashboards.
```

**2. Relationship Types**

```yaml
relationships:
  is_a:
    description: "Hierarchical parent-child"
    example: "Analytics Engineer IS_A Data Role"
    
  related_to:
    description: "Conceptually similar, often confused"
    example: "Analytics Engineer RELATED_TO Data Analyst"
    
  requires_skill:
    description: "Role typically requires this skill"
    example: "Analytics Engineer REQUIRES_SKILL dbt"
    
  collaborates_with:
    description: "Roles that frequently work together"
    example: "Analytics Engineer COLLABORATES_WITH Data Scientist"
    
  progression_to:
    description: "Common career progression"
    example: "Data Analyst PROGRESSION_TO Analytics Engineer"
```

**3. Embedding Strategy**

```yaml
embedding_approach:
  model: "text-embedding-3-small" # or similar
  
  what_to_embed:
    - role descriptions (paragraph form)
    - skill descriptions
    - job posting titles + first 500 chars
    
  similarity_thresholds:
    high_confidence: 0.85
    medium_confidence: 0.70
    needs_review: 0.50
    
  use_cases:
    - "Find roles similar to Analytics Engineer"
    - "What skills are adjacent to dbt?"
    - "Candidates with X skills might fit Y roles"
```

**4. Query Patterns (Future)**

```
Natural language queries the ontology should support:

"Show me roles that are like Data Scientist but more engineering-focused"
→ Returns: ML Engineer, Analytics Engineer

"What skills should a Data Analyst learn to become an Analytics Engineer?"
→ Returns: dbt, data modeling, SQL (advanced), Git

"Find companies where Analytics Engineers report to Engineering not Analytics"
→ Returns: [requires company org data]

"Which roles commonly transition to Product Management?"
→ Returns: Data Analyst, Product Analytics, Data Scientist
```

---

## Taxonomy Maintenance

### Review Cadence

| Review Type | Frequency | Focus |
|-------------|-----------|-------|
| Edge case log review | Weekly | Resolve accumulated ambiguities |
| Coverage analysis | Monthly | Identify gaps, new role patterns |
| Signal effectiveness | Monthly | Which signals are predictive? |
| Full taxonomy review | Quarterly | Add/remove/restructure categories |
| Skill taxonomy update | Quarterly | New tools, deprecated skills |

### Metrics to Track

| Metric | Target | Action if Below |
|--------|--------|-----------------|
| Classification confidence (avg) | >0.85 | Review low-confidence patterns |
| out_of_scope rate | <15% | Consider new categories |
| Edge case backlog | <20 unresolved | Schedule resolution session |
| Reclassification rate | <5% | Investigate unstable categories |

### Change Log Template

```markdown
## Taxonomy Change Log

### [Date] - v1.X.X

**Added:**
- [New category/skill] - Rationale: [why needed]

**Changed:**
- [Category] - [What changed] - Rationale: [why]

**Removed:**
- [Category/skill] - Rationale: [why deprecated]

**Edge Cases Resolved:**
- [Role pattern] → Now classifies as [category]

**Open Questions:**
- [Unresolved issue for next review]
```

---

## Output Formats

### Classification Decision

```markdown
## Classification: [Job Title]

**Input:** [Raw title and key description excerpts]

**Decision:**
- Family: [product/data]
- Subfamily: [specific category]
- Seniority: [level]
- Confidence: [high/medium/low]

**Signals Found:**
- Title: [matching patterns]
- Keywords: [matching terms]
- Tools: [specific tools mentioned]

**Disambiguation Notes:**
[If edge case, explain reasoning]

**Flags:**
- [ ] Needs human review
- [ ] New pattern for taxonomy consideration
```

### Taxonomy Gap Analysis

```markdown
## Gap Analysis: [Date]

**Coverage Summary:**
- Total roles analyzed: [N]
- Successfully classified: [N] ([%])
- Out of scope: [N] ([%])
- Low confidence: [N] ([%])

**Emerging Patterns:**
| Pattern | Frequency | Suggested Action |
|---------|-----------|------------------|
| [New title pattern] | [N] | [Add category / Add signal / Monitor] |

**Problem Categories:**
| Category | Issue | Recommendation |
|----------|-------|----------------|
| [Category] | [High confusion rate with X] | [Improve signals / Merge / Split] |

**Skill Gaps:**
- [New skills appearing frequently but not in taxonomy]

**Recommendations:**
1. [Specific change]
2. [Specific change]
```

---

## Integration Points

### With Classifier (Claude Haiku)

The taxonomy informs the classification prompt:

```python
TAXONOMY_CONTEXT = """
Valid subfamilies for Data roles:
- product_analytics: Product metrics, experiments, user behavior
- data_analyst: Business reporting, dashboards, BI tools
- analytics_engineer: dbt, metrics layer, data modeling
- data_engineer: Pipelines, ETL/ELT, data infrastructure
- ml_engineer: Production ML, MLOps, model deployment
- data_scientist: Statistical modeling, predictions
- research_scientist: Novel ML research, publications
- data_architect: Data strategy, governance

Classification rules:
- "AI Engineer" → ml_engineer if model-focused, else out_of_scope
- Presence of "dbt" strongly indicates analytics_engineer
- "Business Analyst" → data_analyst unless product-focused
"""
```

### With Job Feed (Filtering)

Taxonomy enables precise filtering:

```sql
-- User selects "Analytics Engineer" 
-- Only returns exact subfamily match, not "Data Analyst"
WHERE job_subfamily = 'analytics_engineer'

-- User selects "Data" family
-- Returns all data subfamilies
WHERE job_family = 'data'
```

### With Semantic Search (Future)

```python
# Current: exact match
results = db.query("subfamily = 'analytics_engineer'")

# Future: semantic similarity
query_embedding = embed("data transformation and metrics modeling role")
results = vector_search(query_embedding, threshold=0.8)
# Returns: analytics_engineer, data_engineer (lower score)
```
