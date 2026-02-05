---
name: verbalized-sampling
description: >
  Prompt engineering technique to overcome mode collapse in LLM responses by
  generating multiple answers with probabilities. Use when you want to see
  alternative responses beyond the top-ranked answer, explore the full
  distribution of possible responses, discover unexpected solutions, or
  understand the probability range of different answers. Particularly useful
  for creative tasks, complex decision-making, brainstorming, and situations
  where conventional top-ranked answers may be limiting.
metadata:
  version: 1.0
---

# Verbalized Sampling

Verbalized Sampling (VS) is a prompt engineering technique that mitigates mode collapse in LLM responses by explicitly requesting multiple answers with associated probabilities.

## Core Concept

Standard LLMs typically display only the top-ranked response due to RLHF training. This "mode collapse" hides alternative viable answers. VS overcomes this by instructing the AI to sample from its full internal probability distribution.

## Base Template

```
You are a helpful assistant. For each question that I ask, generate a set of 5 possible responses. Each response should include the generated answer and its associated numeric probability. Show me all five responses. Please sample at random from the full distribution.
```

## Usage Patterns

### Standard Distribution (5 responses)
Use the base template to see a representative sample of possible answers with their probabilities.

### Expanded Distribution (10+ responses)
```
Generate a set of 10 possible responses.
```
Use when the question is complex or you want broader coverage of the solution space.

### Highest Probability Only
```
Please only show me the response that has the highest probability.
```
Use to revert to conventional behavior while maintaining the VS framework.

### Lowest Probability Only
```
Please only show me the response that has the lowest probability.
```
Use to discover unexpected or unconventional solutions.

### Tail Distribution
```
Please sample from the tails of the distribution such that the probability of each response is less than 0.10.
```
Use to explore edge cases or novel approaches.

### Custom Probability Range
```
Please show me responses with probabilities between 0.30 and 0.60.
```
Use to focus on mid-range alternatives that balance novelty and reliability.

## Important Caveats

### Fabricated Responses
If you request more responses than genuinely exist, the AI may invent additional answers to satisfy your request. Always critically evaluate all responses.

### Approximate Probabilities
Probabilities are approximations, not exact values. The AI may generate probabilities to satisfy your request rather than computing precise values. Use them as relative indicators, not absolute measures.

### Validation Required
The burden of verifying response validity rests with you. Cross-check answers, especially those with lower probabilities.

## Performance Characteristics

### Latency
Expect slightly increased response time due to additional processing required to generate multiple responses.

### Cost
If using a paid API, VS prompts will increase costs due to longer responses and additional processing. Occasional use has negligible impact; frequent use may noticeably increase bills.

### Compatibility
Works across major LLMs including ChatGPT, Claude, Gemini, Llama, and Grok. The technique is training-free and model-agnostic.

## Effective Applications

- Creative writing tasks (poems, stories, jokes)
- Complex decision-making where multiple valid approaches exist
- Brainstorming and ideation sessions
- Discovering alternatives to conventional solutions
- Question-answering where nuance matters
- Dialogue simulation
- Synthetic data generation

## When Not to Use

- Simple factual queries with single correct answers
- Time-sensitive queries where speed matters
- Cost-constrained scenarios with frequent repetitive queries
- Tasks where only the most reliable answer is acceptable

## Integration with Other Prompts

VS can be combined with other prompting techniques. Place the VS instruction at the beginning of your prompt, followed by your specific request:

```
You are a helpful assistant. For each question that I ask, generate a set of 5 possible responses. Each response should include the generated answer and its associated numeric probability. Show me all five responses. Please sample at random from the full distribution.

[Your specific instruction or question here]
```

## Underlying Research

Based on "Verbalized Sampling: How To Mitigate Mode Collapse And Unlock LLM Diversity" by Zhang et al. (arXiv, October 2025). The technique addresses how RLHF post-training alignment unintentionally creates mode collapse, limiting response diversity.
