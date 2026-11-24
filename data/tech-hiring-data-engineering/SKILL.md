---
name: "tech-hiring-data-engineering"
description: "Data engineers build and maintain the pipelines, infrastructure, and systems that make data available for analytics, ML, and business intelligence. They sit between the raw data sources (applications, APIs, third parties) and the consumers "
---

# Data Engineering — Hiring Guide

## How to Use This Guide

- **Sourcing:** Use the title synonyms and Boolean strings in each section
- **Screening:** Skill tiers: T1 = must-have, T2 = differentiator, T3 = rare upside
- **Interviewing:** Use the assessment approach to design your interview loop
- **Benchmarking:** Comp ranges are US market, growth-stage (Series B–D). Adjust for location, company stage, and current market

---

## Universal Seniority Framework

Applies across all disciplines. Use as a baseline — teams vary on exact year ranges.

| Level | Typical YoE | What they own | Mentorship | Scope |
|---|---|---|---|---|
| **Junior (L3 / IC1)** | 0–2 years | Defined tasks, bug fixes, small features | Needs daily guidance | Self |
| **Mid (L4 / IC2)** | 2–5 years | Features end-to-end, moderate ambiguity | Occasional junior support | Feature / component |
| **Senior (L5 / IC3)** | 5–8 years | Projects, technical decisions, cross-team coordination | Active mentorship | Team / project |
| **Staff (L6 / IC4)** | 8–12 years | Technical strategy, cross-team systems, org-wide standards | Multiplies teams | Org |
| **Principal / Distinguished** | 12+ years | Company-wide technical direction, external influence | Defines engineering culture | Company |

**Promotion-readiness signal:** Consistently operating at the *next* level before the title, not just meeting current-level expectations.

---

## Data Engineering

### What This Role Does
Data engineers build and maintain the pipelines, infrastructure, and systems that make data available for analytics, ML, and business intelligence. They sit between the raw data sources (applications, APIs, third parties) and the consumers (data scientists, analysts, dashboards). Poor data engineering is the primary reason ML projects fail.

### Titles & Synonyms

| Level | Common titles |
|---|---|
| Junior | Junior Data Engineer, Data Infrastructure Engineer, ETL Developer |
| Mid | Data Engineer, Analytics Engineer, Pipeline Engineer |
| Senior | Senior Data Engineer, Lead Data Engineer, Data Platform Engineer |
| Staff+ | Staff Data Engineer, Principal Data Engineer, Head of Data Platform |
| Specialist | Streaming Engineer (Kafka/Flink focus), Analytics Engineer (dbt focus) |

### Skill Tiers

**Tier 1 — Must-have:**
- Python for data pipelines: data manipulation, scripting, automation
- SQL: advanced queries, performance tuning, understanding of query plans
- At least one orchestration tool: Airflow, Prefect, Dagster, or similar
- Cloud data warehouse experience: BigQuery, Snowflake, or Redshift
- Data modelling: star schema, normalisation, slowly changing dimensions

**Tier 2 — Differentiator:**
- Batch processing: Apache Spark (PySpark) for large-scale transformations
- Streaming: Kafka, Flink, Kinesis — real-time pipeline experience
- dbt (data build tool) — increasingly standard for analytics engineering
- Data quality frameworks: Great Expectations, dbt tests, custom validation
- Data cataloguing and lineage: DataHub, OpenMetadata, Alation
- Infrastructure as Code: Terraform for cloud resource management

**Tier 3 — Bonus:**
- Apache Iceberg, Delta Lake, or Hudi (modern table formats)
- Custom Spark/Flink jobs in Scala or Java
- Cost optimisation at scale (query cost, storage tiering)
- Contributions to open source data tools

### Sourcing Strings

```bash
# LinkedIn X-Ray
site:linkedin.com/in/ ("data engineer" OR "analytics engineer" OR "pipeline engineer" OR "ETL developer") (Airflow OR Spark OR Kafka OR dbt OR Snowflake OR BigQuery) -recruiter -talent

# Streaming specialists
site:linkedin.com/in/ ("data engineer" OR "streaming engineer") (Kafka OR Flink OR Kinesis OR "real-time") -recruiter

# GitHub
language:python topic:data-engineering followers:>20 pushed:>2025-01-01
site:github.com "joined on" (Airflow OR dbt OR Kafka OR Spark OR "data pipeline") "data engineer"
```

### Seniority Signals

- **Junior → Mid:** Moves from "I build pipelines given a spec" to "I identify what data consumers need and design accordingly"
- **Mid → Senior:** Proactively raises data quality, schema evolution, and cost concerns; designs systems that other engineers can maintain
- **Senior → Staff:** Defines the data platform strategy; enables data scientists and analysts to self-serve; reduces pipeline toil company-wide

### Interview & Assessment Loop

| Stage | Format | What you're assessing |
|---|---|---|
| SQL screen | Complex multi-join query, window functions, explain plan | Fundamentals non-negotiable |
| Technical screen | Python coding + pipeline design | Code quality, data handling patterns |
| System design | Design a pipeline for [realistic scenario] | Scale thinking, failure handling, idempotency |
| Take-home (optional) | Build a small pipeline with dbt or Airflow | Practical skills, code organisation |
| Behavioural | STAR — working with data consumers, handling bad data | Data engineering is a service role |

**Critical question:** "What do you do when an upstream data source sends malformed data at 2am?" Tests failure handling philosophy, monitoring, alerting, and on-call readiness.

### Red Flags
- No understanding of idempotency in pipelines ("just re-run it")
- Can't explain the difference between batch and streaming at a technical level
- No experience with data testing or quality validation
- "I just write SQL in a notebook" — no pipeline engineering experience
- No awareness of schema evolution and how breaking changes propagate

### Compensation (2025, US, Growth-Stage)

| Level | Base salary range |
|---|---|
| Junior | $95k – $135k |
| Mid | $135k – $175k |
| Senior | $160k – $220k |
| Staff | $205k – $275k |
| Principal | $245k – $320k+ |
