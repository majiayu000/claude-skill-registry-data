---
name: ds-star
description: Multi-agent data science framework using DS-STAR (Data Science - Structured Thought and Action) architecture. Automates data analysis through collaborative AI agents with multi-model support (Haiku, Sonnet, Opus). Use for exploratory data analysis, automated insights, and iterative data science workflows.
metadata:
  version: 1.0.0
  category: ai-ml
  tags: [data-science, multi-agent, analysis, automation, claude-models, iterative-refinement]
  author: Jules Lescx (adapted by Claude)
  original_repo: https://github.com/JulesLscx/DS-Star
---

# DS-STAR: Multi-Agent Data Science Framework

## Overview

**DS-STAR** (Data Science - Structured Thought and Action) is an intelligent multi-agent framework adapted for Claude Code that automates data science workflows through specialized AI agents. Originally designed for Google's Gemini models, this skill adapts DS-STAR to leverage Claude's model family (Haiku, Sonnet, Opus) for cost-efficient, high-quality data analysis.

### What It Does

DS-STAR orchestrates **seven specialized agents** that work collaboratively to:
1. **Analyze** data files (structured/unstructured)
2. **Plan** analysis strategies iteratively
3. **Generate** Python code to execute plans
4. **Execute** code with automatic debugging
5. **Verify** results against the query
6. **Route** refinement decisions
7. **Finalize** formatted outputs

**Key Innovation**: Multi-model optimization - route exploration tasks to Haiku, complex reasoning to Sonnet, and critical analysis to Opus for optimal cost/performance balance.

### When to Use This Skill

- **Exploratory Data Analysis (EDA)**: Automated insights from CSV, JSON, or text files
- **Data Science Questions**: Answer factual questions from data programmatically
- **Iterative Analysis**: Refine analyses through multiple rounds of verification
- **Cost-Optimized Workflows**: Use cheaper models for simple tasks, powerful models for complex reasoning
- **Reproducible Research**: All artifacts (prompts, code, results) are saved for audit trails

### Performance Characteristics

| Agent | Default Model | Task Type | Cost Profile |
|-------|---------------|-----------|--------------|
| **Analyzer** | Haiku | Data inspection | $0.80/1M tokens |
| **Planner** | Sonnet | Strategy design | $15/1M tokens |
| **Coder** | Sonnet | Code generation | $15/1M tokens |
| **Verifier** | Sonnet | Result validation | $15/1M tokens |
| **Router** | Haiku | Decision routing | $0.80/1M tokens |
| **Debugger** | Sonnet | Error fixing | $15/1M tokens |
| **Finalyzer** | Sonnet | Output formatting | $15/1M tokens |

**Estimated Cost** (typical analysis):
- Traditional (all Sonnet): ~$0.50-1.00
- DS-STAR (mixed models): ~$0.20-0.40
- **Savings**: 50-60%

---

## How It Works

### Multi-Agent Pipeline

```
┌─────────────────────────────────────────────────────────┐
│  1. ANALYZER (Haiku)                                    │
│     Input: Data files                                   │
│     Output: Data descriptions, schemas, summaries       │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  2. PLANNER (Sonnet)                                    │
│     Input: Query + Data descriptions                    │
│     Output: Initial analysis step                       │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  3. CODER (Sonnet)                                      │
│     Input: Plan + Data descriptions                     │
│     Output: Python code to execute plan                 │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  4. DEBUGGER (Sonnet) [If needed]                       │
│     Input: Code + Error                                 │
│     Output: Fixed code                                  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  5. VERIFIER (Sonnet)                                   │
│     Input: Code + Results + Query                       │
│     Output: "Sufficient" or "Needs refinement"          │
└─────────────────────────────────────────────────────────┘
                         ↓
           ┌─────────────┴─────────────┐
           │    Sufficient?            │
           └─────────────┬─────────────┘
                 YES │   │ NO
                     │   └──────────────┐
                     │                  ↓
                     │    ┌──────────────────────────────┐
                     │    │  6. ROUTER (Haiku)           │
                     │    │     Decide: Fix step or Add  │
                     │    └──────────────────────────────┘
                     │                  │
                     │                  ↓
                     │         [Loop back to PLANNER]
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│  7. FINALYZER (Sonnet)                                  │
│     Input: Final code + Results + Query                 │
│     Output: Formatted answer (JSON/text)                │
└─────────────────────────────────────────────────────────┘
```

### Iterative Refinement

DS-STAR uses **up to 5 refinement rounds** (configurable):
- Each round can add a new analysis step or fix a previous step
- Automatic debugging retries failed code
- Verification gates ensure quality before finalization
- All artifacts saved in `runs/<run_id>/` for reproducibility

---

## Installation

### Quick Start

```bash
# Add the marketplace (if not already added)
/plugin marketplace add token-eater/skills-marketplace

# Install DS-STAR skill
/plugin install ds-star
```

### Manual Installation

```bash
# Clone the marketplace
git clone https://github.com/token-eater/skills-marketplace.git
cd skills-marketplace

# The skill is in skills/ds-star/
```

---

## Usage

### Basic Usage

```python
# In Claude Code, invoke the skill
/skill ds-star

# The skill will prompt you for:
# 1. Data files (CSV, JSON, TXT, etc.)
# 2. Your analysis query
# 3. Model configuration (optional)
```

### Example Queries

1. **Basic Statistics**:
   ```
   Query: "What is the average age and gender distribution in this dataset?"
   Data: customers.csv
   ```

2. **Time Series Analysis**:
   ```
   Query: "What are the monthly sales trends over the past year?"
   Data: sales_2024.csv
   ```

3. **Data Quality**:
   ```
   Query: "How many missing values are in each column, and what percentage of the total?"
   Data: survey_responses.csv
   ```

4. **Correlation Analysis**:
   ```
   Query: "Which features have the strongest correlation with customer churn?"
   Data: customer_features.csv
   ```

### Advanced Configuration

Configure which models to use for each agent:

```yaml
# In your query, you can specify:
agent_models:
  ANALYZER: haiku      # Fast data inspection
  PLANNER: sonnet      # Strategic planning
  CODER: sonnet        # Code generation
  VERIFIER: sonnet     # Result validation
  ROUTER: haiku        # Simple routing decisions
  DEBUGGER: opus       # Complex debugging (if needed)
  FINALYZER: sonnet    # Output formatting
```

Or use presets:
- **Fast** (70% cost savings): All Haiku except Coder/Debugger
- **Balanced** (50% cost savings): Haiku for simple, Sonnet for complex
- **Quality** (Highest accuracy): All Sonnet or Opus

---

## Output Structure

Every run creates a structured artifact directory:

```
runs/<run_id>/
├── steps/
│   ├── 001_analyzer/
│   │   ├── prompt.md       # Agent prompt
│   │   ├── code.py         # Generated code
│   │   ├── result.txt      # Execution output
│   │   └── metadata.json   # Step metadata
│   ├── 002_planner_init/
│   ├── 003_coder/
│   └── ...
├── exec_env/               # Executed scripts
├── logs/
│   ├── pipeline.log        # Structured logs
│   └── execution.log       # Code execution logs
├── final_output/
│   └── result.json         # Final answer
└── pipeline_state.json     # Resume state
```

### Resume Support

DS-STAR supports resuming interrupted runs:

```python
# Resume from a previous run ID
/skill ds-star --resume 20241123_143022_a1b2c3
```

---

## Multi-Model Optimization

### Cost Comparison (50K token analysis)

| Configuration | Input Cost | Output Cost | Total | Savings |
|---------------|-----------|-------------|-------|---------|
| **All Sonnet** | $0.75 | $0.75 | **$1.50** | 0% |
| **Balanced** | $0.30 | $0.30 | **$0.60** | 60% |
| **Fast** | $0.15 | $0.15 | **$0.30** | 80% |

### Model Selection Guidelines

**Use Haiku for**:
- Data file inspection (Analyzer)
- Simple routing decisions (Router)
- Basic extraction tasks

**Use Sonnet for**:
- Planning strategies (Planner)
- Code generation (Coder)
- Result verification (Verifier)
- Output formatting (Finalyzer)

**Use Opus for**:
- Complex debugging scenarios
- Critical analysis requiring highest accuracy
- Novel/ambiguous data formats

---

## Examples

### Example 1: Iris Dataset Analysis

**Data**: `iris.csv` (150 rows, 5 columns)

**Query**: "What is the average petal length for each species, and which species has the highest variance?"

**Result**:
```json
{
  "final_answer": {
    "averages": {
      "setosa": 1.46,
      "versicolor": 4.26,
      "virginica": 5.55
    },
    "highest_variance": "virginica",
    "variance_value": 0.304
  }
}
```

**Cost**: $0.18 (Balanced configuration)
**Time**: ~25 seconds
**Steps**: 3 (Analyze → Plan → Code → Verify → Finalize)

---

### Example 2: Sales Data Time Series

**Data**: `sales_2024.csv` (365 rows, daily sales)

**Query**: "Identify the top 3 months by total sales and calculate month-over-month growth rates."

**Result**:
```json
{
  "final_answer": {
    "top_3_months": [
      {"month": "December", "total_sales": 125000, "growth": "+15%"},
      {"month": "November", "total_sales": 108000, "growth": "+8%"},
      {"month": "July", "total_sales": 95000, "growth": "+12%"}
    ],
    "average_growth": "+8.3%"
  }
}
```

**Cost**: $0.22 (Balanced configuration)
**Time**: ~30 seconds
**Steps**: 4 (with 1 refinement round)

---

## Architecture

### Claude Provider Implementation

The skill includes a custom `ClaudeProvider` that integrates with the Claude Agent SDK:

```python
class ClaudeProvider(ModelProvider):
    """Provider for Claude models via Agent SDK."""

    def __init__(self, model_name: str = "sonnet"):
        self.model_name = model_name  # haiku, sonnet, or opus

    def generate_content(self, prompt: str) -> str:
        # Use SDK's subagent system for context efficiency
        # Automatically handles model routing
        # Returns generated content
```

### Integration with Claude Code

- **Context Efficient**: Uses subagents to avoid context bloat
- **Parallel Execution**: Independent agents can run concurrently
- **Artifact Persistence**: All outputs saved to project directory
- **Resume Support**: Can pause/resume long analyses

---

## Troubleshooting

### Common Issues

**1. "Missing data files" error**
- Ensure files are in the `data/` directory
- Use absolute paths or relative to project root
- Check file permissions

**2. Code execution timeout**
- Increase `execution_timeout` in config (default: 60s)
- Simplify the query or split into multiple queries
- Check for infinite loops in generated code

**3. "API key not found"**
- Claude Agent SDK handles auth automatically
- No API keys needed for built-in Claude models
- External models (OpenAI, Gemini) require env vars

**4. Verification always fails**
- Query may be too ambiguous - make it more specific
- Increase `max_refinement_rounds` (default: 5)
- Check intermediate results in `runs/<id>/steps/`

### Debug Mode

Enable detailed logging:

```python
# Run with interactive mode to pause at each step
/skill ds-star --interactive

# Or inspect artifacts manually
ls runs/<run_id>/steps/
cat runs/<run_id>/logs/pipeline.log
```

---

## Configuration

### Config Options

```yaml
# config.yaml (optional, in project root)
run_id: "my_experiment"           # Custom run ID
model_name: "sonnet"               # Default model
interactive: false                 # Pause between steps
max_refinement_rounds: 5           # Max iterations
execution_timeout: 60              # Code timeout (seconds)
preserve_artifacts: true           # Save all outputs
runs_dir: "runs"                   # Artifact directory
data_dir: "data"                   # Data file directory

# Agent-specific models
agent_models:
  ANALYZER: haiku
  PLANNER: sonnet
  CODER: sonnet
  VERIFIER: sonnet
  ROUTER: haiku
  DEBUGGER: opus
  FINALYZER: sonnet
```

---

## Comparison with Original

| Feature | Original DS-STAR | This Skill |
|---------|------------------|------------|
| **Models** | Gemini, OpenAI | Claude (Haiku/Sonnet/Opus) |
| **Context** | Full context per call | Subagent-optimized |
| **Cost** | $1-2 per analysis | $0.20-0.40 per analysis |
| **Integration** | Standalone CLI | Claude Code skill |
| **Resume** | ✅ Yes | ✅ Yes |
| **Interactive** | ✅ Yes | ✅ Yes |
| **Artifacts** | ✅ Saved | ✅ Saved |
| **Multi-model** | Basic | Advanced routing |

---

## Best Practices

### Query Design

✅ **Good Queries**:
- "Calculate the correlation between X and Y columns"
- "What percentage of users have more than 3 purchases?"
- "Identify outliers in the price column using IQR method"

❌ **Avoid**:
- "Tell me about this data" (too vague)
- "Do everything" (use multiple specific queries)
- Queries requiring external data not in files

### Data Preparation

✅ **Best Formats**:
- CSV with headers
- JSON with consistent structure
- Clean text files (UTF-8)

❌ **Problematic**:
- Excel files with multiple sheets (convert to CSV first)
- PDFs (extract text first)
- Binary formats (images, etc.)

### Model Selection

- Start with **Balanced** configuration (50% cost savings)
- Use **Fast** for large datasets (>100K rows)
- Use **Quality** (Opus) only for novel/complex analyses
- Override specific agents as needed (e.g., Opus for Debugger only)

---

## Limitations

- **Python-only execution**: Generated code is Python (pandas, numpy, etc.)
- **Local execution**: Code runs locally (be cautious with untrusted data)
- **No external APIs**: Agents can't call external services (by design)
- **Single-file outputs**: Finalyzer produces one result file
- **No interactive visualizations**: Text/JSON outputs only (no plots saved)

---

## Contributing

### Extending the Framework

Want to add new agents or capabilities?

1. **Add new agent type** in `scripts/dsstar.py`
2. **Create prompt template** in `scripts/prompts.py`
3. **Wire up in pipeline** in `run_pipeline()` method
4. **Test with sample data**
5. **Submit PR** with examples

### Ideas for Extensions

- **Visualization Agent**: Generate matplotlib/seaborn plots
- **Export Agent**: Save results to various formats (Excel, PDF, etc.)
- **Schema Agent**: Automatically detect and validate data schemas
- **Anomaly Agent**: Specialized outlier detection
- **ML Agent**: Train simple models (regression, classification)

---

## License

MIT License - Adapted from [DS-Star](https://github.com/JulesLscx/DS-Star) by Jules Lescx.

Original DS-STAR based on Google Research paper.

---

## Support & Resources

- 📖 **Original Paper**: [DS-STAR: Domain Adaptive Data Science via Large Language Models](https://arxiv.org/abs/2410.19016)
- 💾 **Original Repository**: [github.com/JulesLscx/DS-Star](https://github.com/JulesLscx/DS-Star)
- 🐛 **Report Issues**: [Skills Marketplace Issues](https://github.com/token-eater/skills-marketplace/issues)
- 💬 **Discussions**: [Skills Marketplace Discussions](https://github.com/token-eater/skills-marketplace/discussions)

---

**Ready to automate your data science workflows?** Install DS-STAR and let multi-agent AI handle the heavy lifting!
