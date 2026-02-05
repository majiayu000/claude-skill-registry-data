---
name: llm-rankings
description: Comprehensive LLM model evaluation and ranking system. Use when users ask to compare language models, find the best model for a specific task, understand model capabilities, get pricing information, or need help selecting between GPT-4, Claude, Gemini, Llama, or other LLMs. Provides benchmark-based rankings, cost analysis, and use-case-specific recommendations across reasoning, code generation, long context, multimodal, and other capabilities.
---

# LLM Rankings Skill

Comprehensive evaluation and ranking system for comparing language models across performance, cost, and technical dimensions.

## Core Capabilities

This skill provides four main ranking methodologies:

1. **Benchmark-Based Rankings** - Objective comparisons using MMLU, GSM8K, HumanEval scores
2. **Task-Specific Rankings** - Weighted recommendations for code generation, creative writing, reasoning, etc.
3. **Cost-Effectiveness Rankings** - Performance per dollar analysis
4. **Real-World Performance** - API reliability, documentation quality, ease of integration

## Standard Workflows

### Simple Comparison Request

When user asks "Which LLM is better for X?":

1. Load relevant benchmark data from `references/benchmarks.md`
2. Filter models matching requirements
3. Calculate rankings with appropriate weighting
4. Present top 3-5 recommendations with justification
5. Include pricing information from `references/pricing.md`

### Detailed Analysis Request

When user asks for comprehensive comparison:

1. Load model specifications from `references/model-details.md`
2. Generate side-by-side comparison table
3. Include benchmark scores across multiple tests
4. Calculate cost projections for expected usage
5. Provide deployment considerations

### Best Model for Task Query

When user describes a specific use case:

1. Parse task requirements (performance needs, budget, technical constraints)
2. Map to capability dimensions
3. Load task-specific rankings from `references/use-cases.md`
4. Return top 3 models with detailed reasoning
5. Include caveats and alternative suggestions

## Reference Resources

Load these files as needed to inform recommendations:

- **benchmarks.md** - Comprehensive benchmark scores (MMLU, GSM8K, HumanEval, MMMU, etc.)
- **model-details.md** - Technical specifications, context windows, API details, capabilities
- **use-cases.md** - Task-specific recommendations organised by common use cases
- **pricing.md** - Current pricing across all providers, cost optimisation strategies

## Output Formats

### Quick Recommendation
Present concise recommendations with model name, key strength, pricing snapshot, and one-sentence justification.

### Comparison Table
Use markdown tables comparing models across relevant dimensions (performance, context window, pricing, best use).

### Detailed Analysis
Structure as:
1. Executive summary (2-3 sentences)
2. Top recommendations (ranked with justification)
3. Performance comparison (benchmark scores)
4. Cost analysis (usage projections)
5. Implementation considerations
6. Alternative options

## Key Principles

1. **Evidence-Based** - Support all rankings with benchmark data or documented performance
2. **Context-Aware** - Consider user's specific requirements, budget, technical environment
3. **Transparent** - Explain weighting decisions and ranking criteria clearly
4. **Current Information** - Use web_search to verify latest releases, pricing changes, benchmark updates
5. **Practical Focus** - Prioritise real-world usage factors over pure benchmark scores
6. **Balanced** - Present strengths and weaknesses honestly for each model

## Important Considerations

- **Benchmark Limitations** - Benchmarks don't perfectly reflect real-world performance
- **Task Specificity** - A model's ranking varies significantly by use case
- **Pricing Volatility** - API pricing changes frequently; verify for important decisions
- **Access Availability** - Some models have waitlists or geographic restrictions
- **Trade-offs** - Larger context windows often mean slower processing

## Usage Notes

- Always verify current pricing and availability via web search for recent changes
- Consider user's deployment environment (API vs self-hosted)
- Account for additional costs (vision inputs, fine-tuning, enterprise features)
- Recommend testing on user's specific use case before committing
- Highlight when free tiers or trials are available

## Model Coverage

Provides comprehensive coverage of:
- **Anthropic:** Claude Opus 4.1/4, Sonnet 4.5/4, Haiku 4
- **OpenAI:** GPT-4 Turbo, GPT-4o, GPT-4o-mini, o1-preview, o1-mini
- **Google:** Gemini 1.5 Pro, Gemini 1.5 Flash
- **Meta:** Llama 3.1 (405B, 70B, 8B)
- **Mistral:** Large 2, Small
- **DeepSeek:** Coder V2
- **Other providers** as relevant to user queries
