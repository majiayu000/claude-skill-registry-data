---
name: Amplifier Learner Tools
description: Self-improving metacognitive recipe tools that learn from execution feedback and extract patterns to provide recommendations
when_to_use: Use when building recipes that need to learn from user feedback, improve over time, or extract patterns from execution data
version: 1.0.0
category: learning
tags: [learning, metacognitive, recipes, self-improving, feedback, patterns]
author: Amplifier
license: MIT
---

# Amplifier Learner Tools

## Overview

The Learner Tools are 4 specialized learner engines that extract patterns from recipe execution feedback, enabling self-improving metacognitive recipes. Each learner logs executions and feedback, then learns patterns to provide actionable recommendations.

## The 4 Learners

### 1. Decision Historian
Learn which decisions work best in specific contexts.

**When to use**: When your recipe makes strategic choices that affect outcomes
- Log context (situation parameters)
- Log decision (what you chose)
- Log outcome (what resulted)
- Get recommendations for future decisions in similar contexts

**Example**:
```python
from amplifier.learning.decision_historian import DecisionHistorian

dh = DecisionHistorian()
dh.log_execution(
    execution_id="task_001",
    context={"difficulty": "hard", "time_available": "30 min"},
    decision={"approach": "step_by_step"},
    outcome={"success_rate": 0.95}
)
```

### 2. Style Learner
Learn personal writing voice and preferences from user edits.

**When to use**: When generating text that users edit to match their style
- Log generated text
- Log user edits showing preferences
- Get style profile (formality, perspective, confidence)

**Example**:
```python
from amplifier.learning.style_learner import StyleLearner

sl = StyleLearner()
sl.log_execution(
    execution_id="email_001",
    input_prompt="Professional email",
    generated_output="I am writing to inform you..."
)
sl.log_edits(
    execution_id="email_001",
    edits=[{"original": "I am", "replacement": "I'm", "reason": "casual"}]
)
```

### 3. Meta-Recipe Tuner
Learn pipeline performance and identify optimization opportunities.

**When to use**: When optimizing multi-stage recipe pipelines
- Log stage timings and quality metrics
- Get bottleneck identification
- Get performance trends and optimization suggestions

**Example**:
```python
from amplifier.learning.meta_recipe_tuner import MetaRecipeTuner

mrt = MetaRecipeTuner()
mrt.log_stage(
    recipe_id="blog_writer",
    run_id="run_001",
    stage_name="research",
    duration_sec=12.5,
    quality_metric=0.92
)
```

### 4. Knowledge Compressor
Learn information extraction and prioritization rules.

**When to use**: When extracting relevant sections from source material
- Log extraction with section breakdown
- Log feedback on kept/removed sections
- Get section priorities and extraction rules

**Example**:
```python
from amplifier.learning.knowledge_compressor import KnowledgeCompressor

kc = KnowledgeCompressor()
kc.log_extraction(
    extraction_id="extract_001",
    source_type="research_paper",
    input_tokens=2500,
    sections=[
        {"name": "abstract", "tokens": 200},
        {"name": "results", "tokens": 1000}
    ]
)
kc.log_feedback(
    extraction_id="extract_001",
    kept_sections=["abstract", "results"],
    removed_sections=["methods"],
    reason="Focus on findings"
)
```

## The Learning Workflow

All learners follow the same pattern:

```
1. Initialize learner
   learner = StyleLearner()

2. Log executions
   learner.log_execution(...)

3. Log feedback
   learner.log_edits(...)

4. Learn patterns
   result = learner.learn()

5. Get recommendations
   recs = learner.get_recommendations()

6. Use recommendations to improve
   Apply learned patterns in next iteration
```

## Data Requirements

Each learner has minimum data requirements before patterns emerge:

| Learner | Min Samples | Min Feedback |
|---------|------------|-------------|
| Decision Historian | 3 | 2 contexts |
| Style Learner | 3 | 5 edits |
| Meta-Recipe Tuner | 5 | 2 stages |
| Knowledge Compressor | 5 | 3 sections |

## Using Multiple Learners Together

```python
class SelfImprovingRecipe:
    def __init__(self):
        self.decision_historian = DecisionHistorian()
        self.style_learner = StyleLearner()
        self.meta_recipe_tuner = MetaRecipeTuner()
        self.knowledge_compressor = KnowledgeCompressor()

    def execute(self, input_data):
        # Log decision
        self.decision_historian.log_execution(...)

        # Generate and log style
        output = self.generate(input_data)
        self.style_learner.log_execution(...)

        # Track performance
        self.meta_recipe_tuner.log_stage(...)

        return output

    def collect_feedback(self, feedback_data):
        self.style_learner.log_edits(...)
        self.knowledge_compressor.log_feedback(...)

    def improve(self):
        # Learn from all sources
        self.decision_historian.learn()
        self.style_learner.learn()
        self.meta_recipe_tuner.learn()
        self.knowledge_compressor.learn()

        # Get recommendations
        return {
            "decisions": self.decision_historian.get_recommendations(),
            "style": self.style_learner.get_recommendations(),
            "performance": self.meta_recipe_tuner.get_recommendations(),
            "extraction": self.knowledge_compressor.get_recommendations()
        }
```

## Features

✅ **File-based persistence**: JSONL for append-only logs, JSON for recommendations
✅ **Cloud-sync safe**: Exponential backoff retry for OneDrive/Dropbox delays
✅ **Probabilistic confidence**: 0-1 scale confidence metrics
✅ **Minimum thresholds**: Prevents false patterns from sparse data
✅ **Full type hints**: 100% type coverage
✅ **Comprehensive validation**: Strict input validation
✅ **Production-ready**: 44 tests, 100% passing

## Storage

All learner data stored in:
```
.data/learning/
├── decision_historian/
│   ├── executions.jsonl
│   ├── feedback.jsonl
│   └── recommendations.json
├── style_learner/
│   ├── executions.jsonl
│   ├── feedback.jsonl
│   └── style_model.json
├── meta_recipe_tuner/
│   ├── executions.jsonl
│   └── tuning_model.json
└── knowledge_compressor/
    ├── executions.jsonl
    ├── feedback.jsonl
    └── compression_model.json
```

## Installation

```bash
# Install from iMehr Marketplace
/skill learner-tools

# Or import directly
from amplifier.learning.decision_historian import DecisionHistorian
from amplifier.learning.style_learner import StyleLearner
from amplifier.learning.meta_recipe_tuner import MetaRecipeTuner
from amplifier.learning.knowledge_compressor import KnowledgeCompressor
```

## Quick Start

### Learn Your Writing Style (5 minutes)
1. Generate 5 emails/texts
2. Log each with user edits showing preferences
3. Run `learn()`
4. Get style profile
5. Future generations match your style!

### Optimize Pipeline Performance (10 minutes)
1. Run pipeline 5+ times
2. Log each stage (timing + quality)
3. Run `learn()`
4. See which stage is bottleneck
5. Optimize that stage
6. Verify improvement with more logging

### Extract Better Content (10 minutes)
1. Extract from 5+ documents
2. Log sections + what was useful
3. Run `learn()`
4. Get section priorities
5. Update extraction logic
6. See immediate improvement

## Best Practices

1. **Log immediately**: Don't batch, log right after execution
2. **Provide context**: Detailed feedback helps learn better
3. **Use meaningful IDs**: `execution_id="email_2024_10_25_001"` not `"x"`
4. **Monitor confidence**: Only use recommendations with confidence > 0.7
5. **Regular learning**: Run learn() every 5-10 executions
6. **Backup data**: Use export functionality for important learnings

## Error Handling

All learners validate inputs and raise helpful errors:

```python
# Raises ValueError
sl.log_execution(execution_id="", ...)  # Empty ID

# Correct
sl.log_execution(execution_id="email_001", ...)
```

## CLI Integration

Use companion slash commands for interactive access:

- `/learner-guide` - Interactive tutorial
- `/learner-log` - Log execution data
- `/learner-analyze` - Analyze patterns
- `/learner-status` - Check status
- `/learner-clear` - Reset data
- `/learner-export` - Backup/export

## Documentation

- **Complete Guide**: `docs/LEARNER_TOOLS_GUIDE.md`
- **Quick Reference**: `docs/LEARNER_QUICK_REFERENCE.md`
- **Integration Examples**: `examples/learner_integration_example.py`

## Common Issues

**Q: "Need more data"**
A: Learners have minimum samples. Log more executions and try again.

**Q: "Confidence too low"**
A: Confidence < 0.7 means unreliable. Log more varied data.

**Q: "No patterns found"**
A: Not enough variation in feedback. Try different approaches.

## When to Revisit

- **After learning**: Use recommendations immediately
- **Low confidence**: Collect more data for reliability
- **New context**: Re-learn when environment changes
- **Optimization cycles**: Learn after each improvement attempt

## Related Skills

- **Metacognitive Recipes**: Building recipes that improve
- **Feedback Loops**: Designing feedback collection
- **Performance Tuning**: Optimizing pipeline efficiency

## Remember

- **Start small**: 3-5 data points is enough to begin
- **Iterate fast**: Learn often, improve continuously
- **Trust the process**: Patterns emerge with consistent feedback
- **Confidence matters**: Higher confidence = better recommendations
- **Combine learners**: Multi-learner approach yields best results

---

**Version**: 1.0.0
**License**: MIT
**Repository**: https://github.com/imehr/amplifier
**Status**: Production Ready
