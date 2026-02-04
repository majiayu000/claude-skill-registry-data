---
name: run-deep-research
description: Toolkit for performing deep research on complex topics using multiple AI research providers (OpenAI, Falcon, Perplexity, Consensus). Emphasizes explicit speed vs depth trade-offs.
---

# run-deep-research

Toolkit for performing deep research on complex topics using multiple AI research providers including OpenAI Deep Research, FutureHouse Falcon, Perplexity AI, and Consensus AI.

## When to Use

Use this skill when:
- The user requests comprehensive research on a topic
- The user needs citations and sources for their research
- The user wants to explore scientific literature or academic papers
- The user needs structured markdown reports with metadata

## CRITICAL: Speed vs Depth Trade-offs

**ALWAYS** ask the user to be explicit about their approach preference:

### Fast/Light Approach (seconds to complete)
- **Provider**: Perplexity
- **Models**: `sonar`, `sonar-pro`, `sonar-reasoning`, `sonar-reasoning-pro`
- **Use when**: Quick answers, initial exploration, time-sensitive queries
- **Cost**: Lower API costs
- **Example**:
  ```bash
  uv run deep-research-client research "What is CRISPR?" --provider perplexity --model sonar-pro
  ```

### Comprehensive/Slow Approach (minutes to complete)
- **Provider**: Perplexity with deep research model, or OpenAI
- **Models**: `sonar-deep-research` (Perplexity), `o3-deep-research-2025-06-26` (OpenAI)
- **Use when**: Thorough analysis needed, critical decisions, comprehensive reports
- **Cost**: Higher API costs and longer wait times
- **Example**:
  ```bash
  uv run deep-research-client research "What is CRISPR?" --provider perplexity --model sonar-deep-research
  ```
  or
  ```bash
  uv run deep-research-client research "What is CRISPR?" --provider openai
  ```

### Specialized Approaches
- **Scientific Literature**: Use `falcon` provider for academic/scientific focus
- **Academic Papers**: Use `consensus` provider for peer-reviewed research (requires API approval)

## Features

- **Multiple Providers**: OpenAI Deep Research, FutureHouse Falcon, Perplexity AI, Consensus AI
- **Rich Output**: Comprehensive markdown reports with citations and YAML frontmatter metadata
- **Smart Caching**: File-based caching in `~/.deep_research_cache/` to avoid expensive re-queries
- **Auto-detection**: Automatically detects available providers from environment variables
- **Templates**: Support for reusable research queries with variable substitution
- **Citation Management**: Citations included by default or saved to separate file

## Required Environment Variables

```bash
# At least one of these is required:
export OPENAI_API_KEY="your-openai-key"           # For OpenAI Deep Research
export FUTUREHOUSE_API_KEY="your-futurehouse-key" # For Falcon
export PERPLEXITY_API_KEY="your-perplexity-key"   # For Perplexity AI
export CONSENSUS_API_KEY="your-consensus-key"     # For Consensus AI (requires approval)
```

## Basic Usage

### Simple Research Query
```bash
# Basic query (uses auto-detected provider)
uv run deep-research-client research "What is quantum computing?"

# With specific provider and model
uv run deep-research-client research "What is quantum computing?" --provider perplexity --model sonar-pro

# Save to file
uv run deep-research-client research "Machine learning trends 2024" --output report.md
```

### List Available Providers
```bash
uv run deep-research-client providers
```

### Using Templates
Templates allow reusable research queries with variable substitution:

```bash
# Use template with variables
uv run deep-research-client research \
  --template gene_research.md \
  --var "gene=TP53" \
  --var "organism=human" \
  --var "tissue=brain tissue" \
  --var "year=2020"
```

Template files use `{variable}` placeholders:
```markdown
Please research the gene {gene} in {organism}, focusing on:
1. Function and molecular mechanisms
2. Disease associations in {tissue} tissue
3. Recent discoveries since {year}
```

### Cache Management
```bash
# List cached research
uv run deep-research-client list-cache

# Clear all cache
uv run deep-research-client clear-cache

# Bypass cache for single query
uv run deep-research-client research "query" --no-cache
```

## Output Format

Research results are returned as markdown with YAML frontmatter:

```yaml
---
provider: perplexity
model: sonar-pro
cached: false
start_time: '2025-10-18T17:43:49.437056'
end_time: '2025-10-18T17:44:08.922200'
duration_seconds: 19.49
citation_count: 18
---

## Question

What is machine learning?

## Output

**Machine learning** is a branch of artificial intelligence...

## Citations

1. https://www.ibm.com/topics/machine-learning
2. https://www.coursera.org/articles/what-is-machine-learning
```

## Model Selection Guide

| Provider | Default Model | Alternative Models | Speed | Depth | Best For |
|----------|---------------|-------------------|-------|-------|----------|
| **Perplexity** | `sonar-deep-research` | `sonar`, `sonar-pro`, `sonar-reasoning`, `sonar-reasoning-pro` | Pro models: Fast | Deep Research: Comprehensive | Real-time web search |
| **OpenAI** | `o3-deep-research-2025-06-26` | - | Slow | Very Comprehensive | Thorough analysis |
| **Falcon** | Default API | - | Medium | Scientific | Academic/scientific literature |
| **Consensus** | Default API | - | Medium | Academic | Peer-reviewed papers |

## Workflow

1. **Ask user for speed preference**: Always clarify if they want fast/light or comprehensive/slow approach
2. **Check environment variables**: Ensure appropriate API keys are set
3. **Run research**: Use `uv run deep-research-client research` with appropriate provider and model
4. **Save output**: Use `--output` flag to save to file if needed
5. **Review results**: Check the markdown output, citations, and metadata
6. **Cache management**: Be aware that results are cached permanently unless cleared

## Important Notes

- **Cost awareness**: Deep research models can be expensive - always confirm with user before using
- **Time awareness**: Deep research can take several minutes - warn user about expected wait time
- **Caching**: Results are cached permanently in `~/.deep_research_cache/` - use `--no-cache` to bypass
- **Citations**: Always included by default; use `--separate-citations` to save to separate file
- **Templates**: Great for repeated research patterns (e.g., gene research, company analysis)
- **Metadata**: YAML frontmatter includes timing, provider info, and configuration details

## Common Patterns

### Quick exploratory research
```bash
uv run deep-research-client research "overview of topic X" --provider perplexity --model sonar-pro --output quick-research.md
```

### Comprehensive deep dive
```bash
uv run deep-research-client research "comprehensive analysis of topic X" --provider openai --output deep-research.md
```

### Scientific literature review
```bash
uv run deep-research-client research "scientific review of topic X" --provider falcon --output scientific-review.md
```

### Template-based gene research
```bash
uv run deep-research-client research --template gene_research.md --var "gene=BRCA1" --var "organism=human" --output brca1-research.md
```

## Python Library Usage

```python
from deep_research_client import DeepResearchClient

# Initialize client (auto-detects providers from env vars)
client = DeepResearchClient()

# Perform research
result = client.research(
    "What are the latest developments in AI?",
    provider="perplexity",
    model="sonar-pro"
)

print(result.markdown)  # Full markdown report
print(f"Provider: {result.provider}")
print(f"Model: {result.model}")
print(f"Duration: {result.duration_seconds:.2f}s")
print(f"Citations: {len(result.citations)}")
print(f"Cached: {result.cached}")
```
