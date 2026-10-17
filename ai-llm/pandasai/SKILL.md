---

name: pandasai
description: >
  Conversational data analysis using natural language queries on pandas DataFrames.
  Use when you want to ask plain-English questions about data, generate charts, explain
  transformations, or build exploratory analysis interfaces — all powered by an LLM backend.
  Supports OpenAI, Anthropic, Google Gemini, Azure OpenAI, and local models. Handles single
  DataFrames (SmartDataframe) and multi-table joins (SmartDatalake).
version: 1.0.0
author: workspace-hub
category: ai-prompting
type: skill
trigger: manual
auto_execute: false
capabilities:
  - natural_language_queries
  - dataframe_conversations
  - chart_generation
  - code_explanation
  - multi_dataframe_analysis
  - custom_prompts
  - llm_backend_flexibility
  - data_privacy_modes
tools:
  - Read
  - Write
  - Bash
  - Grep
tags: [pandasai, llm, dataframe, natural-language, data-analysis, visualization, conversational-ai, pandas]
platforms: [python]
related_skills:
  - langchain
  - pandas-data-processing
  - plotly
  - streamlit
scripts_exempt: true
---

# PandasAI Skill

> Chat with your data using natural language. Ask questions about DataFrames and get
> insights, visualizations, and explanations powered by LLMs.

## When to Use

**USE when:**
- Exploring an unfamiliar dataset with open-ended natural language questions
- Generating quick visualizations from descriptive prompts
- Explaining complex data transformations to stakeholders
- Building conversational data exploration interfaces (Streamlit, Jupyter, FastAPI)
- Rapid prototyping of data analysis workflows

**DON'T USE when:**
- Production pipelines requiring deterministic, version-controlled outputs
- Processing highly sensitive PII without anonymization (use privacy mode)
- Performance-critical paths with very large DataFrames (>100K rows)
- Simple queries that direct pandas operations would handle faster

## Install

```bash
uv add pandasai                          # core
uv add pandasai openai                   # + OpenAI backend
uv add pandasai matplotlib seaborn plotly # + visualization

export OPENAI_API_KEY="sk-..."
# or ANTHROPIC_API_KEY / GOOGLE_API_KEY for other backends
```

## Quick Start

```python
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

df = pd.read_csv("data.csv")
smart_df = SmartDataframe(df, config={"llm": OpenAI(model="gpt-4", temperature=0)})

result = smart_df.chat("What is the total revenue by region?")
smart_df.chat("Plot a bar chart of monthly sales")   # saves chart to ./charts/
print(smart_df.last_code_generated)                  # inspect generated code
```

## Core Capabilities

| Capability | API | Notes |
|-----------|-----|-------|
| Natural language query | `smart_df.chat(question)` | Returns value, DataFrame, or chart |
| Multi-table queries | `SmartDatalake([df1, df2]).chat(q)` | Assign `df.name` before passing |
| Inspect code | `smart_df.last_code_generated` | Verify correctness |
| Enable caching | `config={"enable_cache": True}` | Avoids repeat LLM calls |
| Privacy mode | `config={"enforce_privacy": True}` | Anonymize sensitive columns first |
| Chart saving | `config={"save_charts": True, "save_charts_path": "./charts"}` | Auto-saves matplotlib figures |

## Supported LLM Backends

| Provider | Import class | Env var |
|----------|-------------|---------|
| OpenAI | `from pandasai.llm import OpenAI` | `OPENAI_API_KEY` |
| Anthropic | `from pandasai.llm import Anthropic` | `ANTHROPIC_API_KEY` |
| Google Gemini | `from pandasai.llm import GoogleGemini` | `GOOGLE_API_KEY` |
| Azure OpenAI | `from pandasai.llm import AzureOpenAI` | `AZURE_OPENAI_API_KEY` |
| Local (Ollama) | `from pandasai.llm import LocalLLM` | — |

Switch backends by passing a different `llm=` object to `config`. For fallback logic,
see `MultiBackendAnalyzer` in `references/api-reference.md`.

## Privacy Pattern (Quick)

```python
import hashlib

safe_df = df.copy()
for col in ["name", "email", "ssn"]:
    safe_df[col] = safe_df[col].apply(lambda x: hashlib.md5(str(x).encode()).hexdigest()[:8])

smart_df = SmartDataframe(safe_df, config={"llm": llm, "enforce_privacy": True, "enable_cache": False})
```

See `references/api-reference.md` for full `PrivacyAwareAnalyzer` with audit logging.

## Key Gotchas

- **Determinism**: Set `temperature=0` for reproducible results.
- **Large DataFrames**: Sample to ≤10K rows before wrapping to avoid context overflow.
- **Cache invalidation**: Cache keys are per-question string; data changes don't auto-invalidate.
- **Chart display**: In headless environments set matplotlib backend to `Agg` before import.
- **Multi-table**: Assign `df.name = "table_name"` before passing list to `SmartDatalake`.

## References

- Full code examples (all 6 capabilities): `references/api-reference.md`
- Integration patterns (Streamlit, FastAPI, Jupyter): `references/api-reference.md`
- Best practices, caching, cost management: `references/api-reference.md`
- Troubleshooting table: `references/api-reference.md`
- Upstream docs: https://docs.pandas-ai.com/
- GitHub: https://github.com/gventuri/pandas-ai

## Version History

- **1.0.0** (2026-01-17): Initial release — NL queries, chart generation, multi-backend, privacy modes
