---
license: Apache-2.0
name: khattab-2023-dspy
description: Declarative programming framework for optimizing LLM prompts through compilation and automatic tuning
category: Research & Academic
tags:
  - dspy
  - prompt-optimization
  - llm-programming
  - compilation
  - declarative
---

# DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines

## Decision Points

### When to Choose Optimization Strategy

```
Input: LLM pipeline with N modules, training data size T, target metric M
├── T < 50 examples AND N ≤ 2 modules
│   └── Use manual prompt engineering → DSPy overhead not justified
├── T ≥ 50 examples AND no labeled intermediate steps
│   ├── N ≤ 3 modules → Use BootstrapFewShot teleprompter
│   └── N > 3 modules → Use BootstrapFewShotWithRandomSearch
├── T ≥ 200 examples AND have some labeled intermediates
│   ├── Simple accuracy metric → Use MIPRO (optimizes instructions + demos)
│   └── Complex composite metric → Use BootstrapFinetune if budget allows
└── T ≥ 1000 examples AND production system
    └── Use ensemble of compiled programs → vote/rank outputs
```

### Module Design Decision Tree

```
Need: Transform input X to output Y
├── Single reasoning step (X → Y)
│   └── Use Predict(signature="X -> Y") 
├── Multi-step reasoning required
│   ├── Steps are sequential (A→B→C→Y) → Use ChainOfThought("X -> reasoning, Y")
│   ├── Steps need external tools → Use ReAct("X -> thought, action, observation, Y")
│   └── Need confidence estimation → Use majority vote ensemble
├── Retrieval + generation needed
│   ├── Simple QA → Use Retrieve(k=3) + Generate("context, question -> answer")
│   └── Complex reasoning over docs → Use ColBERTv2 + ChainOfThought
└── Multiple valid approaches exist
    └── Use ProgramOfThought for mathematical reasoning
```

### Signature Complexity Guidelines

```
Field count in signature:
├── 1-2 fields → Start here, expand only if metrics plateau
├── 3-4 fields → Acceptable for complex tasks, monitor token usage
├── 5+ fields → Likely over-specified, consider decomposition
└── If adding fields doesn't improve validation metrics → Remove them
```

## Failure Modes

### 1. **Metric Misalignment Trap**
**Symptom**: High training accuracy, poor real-world performance  
**Detection**: `training_metric >> validation_metric OR users report "system gives perfect but useless answers"`  
**Root cause**: Metric optimizes for wrong objective (exact string match vs semantic correctness)  
**Fix**: Redesign metric to capture actual user success criteria, recompile with composite metrics

### 2. **Bootstrapping Collapse** 
**Symptom**: Compiler generates repetitive or nonsensical demonstrations  
**Detection**: `len(set(demonstrations)) < 0.3 * len(demonstrations) OR average_demo_length < 5 tokens`  
**Root cause**: Training set too narrow, causing trace filtering to select degenerate examples  
**Fix**: Expand training diversity, lower trace filtering threshold, or add minimum quality constraints

### 3. **Signature Explosion**
**Symptom**: Modules produce malformed outputs, compilation time increases exponentially  
**Detection**: `signature_fields > 5 OR parsing_errors > 20% OR compilation_time > 2x baseline`  
**Root cause**: Over-specified signatures make reliable generation harder  
**Fix**: Decompose into simpler modules or merge related fields (reasoning_step_1, reasoning_step_2 → reasoning)

### 4. **Manual Prompt Injection**
**Symptom**: Performance doesn't improve with compilation, prompts contain hard-coded instructions  
**Detection**: `str("Let's think step by step") in module.forward() OR instructions manually set in __init__`  
**Root cause**: Bypassing DSPy abstraction by injecting imperative prompts  
**Fix**: Remove hard-coded strings, let compiler optimize instructions, trust the abstraction

### 5. **Validation Leak**
**Symptom**: Perfect compiled performance that doesn't generalize to deployment  
**Detection**: `compiled_accuracy = 100% OR validation_set overlaps training_set`  
**Root cause**: Compiler overfit to training traces, no held-out validation  
**Fix**: Create true validation split, use cross-validation during compilation, monitor test metrics

## Worked Examples

### Example 1: Multi-Hop QA System

**Scenario**: Build a system that answers questions requiring 2-3 reasoning hops over a knowledge base.

**Initial Manual Approach** (what novices do):
```python
# Brittle manual prompting
prompt = f"Given context: {context}\nQuestion: {question}\nLet's think step by step:\n1. First, I need to..."
```

**DSPy Expert Approach**:
```python
# 1. Define signature (interface, not implementation)
class MultiHopQA(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=5)
        self.reason = dspy.ChainOfThought("context, question -> reasoning, answer")
    
    def forward(self, question):
        contexts = self.retrieve(question)
        return self.reason(context=contexts, question=question)

# 2. Set up compilation
train_set = [...] # 100 question/answer pairs
metric = lambda example, prediction: example.answer.lower() in prediction.answer.lower()

# 3. Compile (this is where the magic happens)
teleprompter = BootstrapFewShot(metric=metric, max_bootstrapped_demos=8)
compiled_qa = teleprompter.compile(MultiHopQA(), trainset=train_set)
```

**Key Decision Points Navigated**:
- Used ChainOfThought signature because multi-hop requires explicit reasoning
- Chose BootstrapFewShot because no intermediate reasoning labels available
- Simple contains-answer metric appropriate for factual QA

**What Expert Catches** vs **Novice Misses**:
- Expert: Signature drives both training and inference behavior consistently
- Novice: Manually writes "step 1, step 2" prompts that vary by hand
- Expert: Bootstrapping finds task-specific demonstrations from successful traces
- Novice: Uses generic few-shot examples that may not match pipeline context

### Example 2: Document Summarization with Constraints

**Scenario**: Summarize technical papers with length/style constraints while preserving key findings.

**DSPy Implementation with Trade-offs**:
```python
class ConstrainedSummarizer(dspy.Module):
    def __init__(self):
        # Trade-off: More fields = better control but harder optimization
        self.summarize = dspy.ChainOfThought(
            "document, style_guide, max_words -> key_findings, summary"
        )
    
    def forward(self, document, style_guide="academic", max_words=150):
        result = self.summarize(
            document=document, 
            style_guide=style_guide,
            max_words=max_words
        )
        return result

# Composite metric balancing multiple objectives
def summary_quality(example, prediction):
    word_count = len(prediction.summary.split())
    length_ok = word_count <= example.max_words * 1.1  # 10% tolerance
    
    # Trade-off: More sophisticated metrics = better quality but slower compilation
    key_present = any(finding in prediction.summary for finding in example.key_findings)
    
    return length_ok and key_present

# Compilation decision: MIPRO optimizes both demonstrations AND instructions
teleprompter = MIPRO(metric=summary_quality, num_candidates=10)
```

**Trade-offs Shown**:
- 3-field signature enables fine control but may slow compilation
- Composite metric ensures length constraints but adds complexity
- MIPRO teleprompter improves quality but requires more compute than BootstrapFewShot

## Quality Gates

Validation checklist for DSPy pipeline deployment:

- [ ] **Signature validation**: All module signatures parse correctly on 100% of validation inputs
- [ ] **Metric plateau detection**: Compilation metric improvement < 2% over last 3 iterations
- [ ] **Cross-model consistency**: Compiled program achieves >80% of best performance when swapped to different LM
- [ ] **Demonstration quality**: Manual inspection shows ≥80% of bootstrapped examples are sensible
- [ ] **Validation holdout**: Validation set completely separate from compilation training data
- [ ] **Latency constraint**: 95th percentile response time meets production SLA requirements
- [ ] **Cost constraint**: Token usage per request within acceptable budget limits
- [ ] **Failure graceful**: Pipeline handles malformed inputs without crashing (try 10 edge cases)
- [ ] **Metric alignment**: Manual evaluation of 50 outputs confirms metric captures real quality
- [ ] **Overfit detection**: Validation performance within 10% of training performance

## NOT-FOR Boundaries

**Do NOT use DSPy for**:
- Single LM calls with abundant labeled examples → Use standard fine-tuning instead
- Real-time systems requiring <100ms response → Use cached/pre-computed approaches 
- Tasks where prompt content is legally regulated → Use verified manual prompts instead
- Simple classification with clear training data → Use traditional ML classifiers instead
- One-off queries or prototypes → Use manual prompting, DSPy overhead not justified

**Delegate to other skills**:
- For training custom models → Use `model-fine-tuning` skill instead
- For retrieval system design → Use `rag-architecture` skill instead  
- For LM serving optimization → Use `inference-optimization` skill instead
- For prompt security → Use `prompt-injection-defense` skill instead
- For LM evaluation methodology → Use `llm-evaluation-frameworks` skill instead

**DSPy is for**: Multi-module pipelines, automatic optimization, model-agnostic systems, compositional reasoning chains, and when you need programs that improve from their own execution traces.