---
name: paper2skill-scaling-efficiency
description: "Convert scaling and efficiency papers into practical resource planning guides. Extracts empirical scaling laws, compute-optimal allocation rules, and budget-performance trade-offs. Use this skill when extracting skills from Category 11 (Scaling and Efficiency) papers — Chinchilla-style scaling law papers, Flash Attention efficiency papers, or knowledge distillation studies."
---

## When to Use

Apply this skill when you encounter arXiv papers that:
- Establish scaling laws or empirical relationships (GPT-3 scaling, Chinchilla compute-optimal training, scaling laws for vision models)
- Study compute efficiency, parameter efficiency, or memory efficiency (Flash Attention, model compression, knowledge distillation, quantization)
- Compare resource-performance tradeoffs (training with fewer parameters, inference latency optimization, energy consumption analysis)
- Provide specific empirical numbers from large-scale experiments (hours of compute, number of parameters, tokens seen, final accuracy)
- Discuss budget constraints and how to optimize performance within them
- Study diminishing returns, saturation points, or scaling frontiers

Examples: "Training Compute-Optimal Large Language Models", "Flash Attention: Fast and Memory-Efficient Exact Attention", "Scaling Laws for Neural Language Models", "Chinchilla Scaling Laws", "LoRA: Low-Rank Adaptation", papers on pruning, distillation, quantization.

## When NOT to Use

Do not use this skill for:
- Papers that propose a method without establishing resource-performance relationships
- Papers with only anecdotal performance numbers (no systematic sweep or scaling study)
- Purely algorithmic improvements without explicit compute/memory/latency analysis
- Papers that discuss efficiency but don't quantify tradeoffs
- Optimization papers that optimize a single component without resource-outcome mapping
- Survey papers that discuss efficiency without contributing new empirical laws

---

## Extraction Template

### For Scaling Law Papers

#### Step 1: Resource Definition
Extract what resource(s) are being studied.

```markdown
**Primary Resource:** What is being measured? (compute [FLOPs, GPU-hours, wall-clock time], data [tokens, examples], parameters [model size], or hardware [memory, batch size])
**Secondary Resources:** What other resources are tracked or discussed?
**Measurement Units:** How are resources quantified? (e.g., FLOPs, GPUs × hours, number of parameters in billions)
**Hardware Specification:** What hardware was used? (GPU type, number of GPUs, mixed precision settings)
```

#### Step 2: Empirical Laws
Document discovered relationships between resources and outcomes.

```markdown
**Primary Law:** L = a * N^b or equivalent mathematical form (e.g., loss decreases as N^-0.07 where N is parameter count)
**Exponent & Coefficient:** Specific numerical values from the paper (e.g., b = -0.07, a = 0.45)
**Validity Range:** Over what resource range does this law hold? (e.g., from 1M to 100B parameters)
**Assumptions:** What conditions must be met for the law to apply? (e.g., compute-optimal scaling, no architectural changes)
**Functional Form:** Is it power law? Logarithmic? Sigmoidal? Saturation?
```

#### Step 3: Specific Numbers & Benchmarks
Extract concrete performance points from experiments.

```markdown
**Training Configuration:**
- N parameters: {value}
- D tokens (or training examples): {value}
- Compute budget: {value} GPU-hours (or FLOPs)
- Final loss (or benchmark score): {value}
- Time to convergence: {wall-clock time}

**Inference Configuration:**
- Model size: {value}
- Latency per token: {milliseconds}
- Throughput: {tokens/second}
- Memory footprint: {GB}
```

#### Step 4: Compute-Optimal Allocation
Extract how to allocate compute optimally.

```markdown
**Budget Constraint:** Given X GPU-hours, how should compute be split between:
- Training tokens vs. parameters (data-parameter tradeoff)?
- Number of training runs vs. model size?
- Batch size vs. learning rate?

**Chinchilla-like Trade-offs:** For a fixed compute budget:
- If you increase parameters by 2x, how should you scale training data?
- Typical optimal ratio: (training tokens) = k × (parameters)

**Sensitivity:** Which allocation decisions matter most? (parameter count > token count > batch size?)
```

### For Efficiency Papers

#### Step 1: Efficiency Dimension
Extract what aspect of efficiency is being optimized.

```markdown
**Target Efficiency:** What is being reduced? (memory, latency, FLOPs, energy, parameter count)
**Baseline:** What standard approach is being compared against?
**Improvement Metric:** How is improvement measured? (speedup factor, memory reduction %, FLOPs saved)
**Hardware Context:** What hardware is this optimized for? (A100 GPUs, TPUs, mobile devices, CPUs)
```

#### Step 2: Performance-Efficiency Tradeoff
Document what is gained and lost.

```markdown
**Accuracy Preservation:** How much accuracy is retained compared to the baseline?
- At zero efficiency cost: {baseline accuracy}
- At 2x speedup: {accuracy}
- At 10x speedup: {accuracy}
- At maximum efficiency: {accuracy drop %}

**Latency Improvement:**
- Baseline latency: {ms}
- With technique: {ms}
- Speedup factor: {x}

**Memory Savings:**
- Baseline memory: {GB}
- With technique: {GB}
- Reduction: {%}
```

#### Step 3: Practical Integration
Extract how to implement the efficiency gain.

```markdown
**Prerequisites:** What is required to use this technique? (specific hardware, software framework, model architecture)
**Hyperparameter Sensitivity:** Which choices most affect the accuracy-efficiency tradeoff?
**Implementation Complexity:** How complex is this to implement? (simple replace, moderate refactoring, major rewrite)
**Reproducibility:** What do you need to reproduce the claimed efficiency gains?
```

#### Step 4: Diminishing Returns Analysis
Document where efficiency gains saturate.

```markdown
**Efficiency Curve:** As the technique is pushed harder, what happens?
- At moderate application: {tradeoff point}
- At aggressive application: {tradeoff point}
- At maximum application: {tradeoff point}

**Saturation Point:** Beyond what parameter does further optimization yield little benefit?
**Bottleneck Shift:** What becomes the new bottleneck after this optimization?
```

### For Compute Budget & Allocation Papers

#### Step 1: Budget Constraints
Extract how different resource budgets change the problem.

```markdown
**Budget Scenarios:**
- Ultra-low (< 1 GPU-day): What is achievable?
- Low (1-100 GPU-days): What methods become viable?
- Medium (100-10K GPU-days): What is state-of-the-art?
- High (10K+ GPU-days): What frontiers can be explored?

**Resource Dimensions:** How do tradeoffs change across:
- Wall-clock time constraint (days vs weeks vs months)
- Total compute constraint (GPU-hours)
- Parameter budget (model size)
- Data availability
```

#### Step 2: Allocation Strategy
Document how to spend a budget optimally.

```markdown
**Allocation Rule:** Given a budget of X:
- How much goes to model size? (percentage or parameter count)
- How much goes to training compute? (tokens or GPU-hours)
- How much goes to data collection/preprocessing?
- How much goes to experimental iteration?

**Optimization Surface:** What allocation strategy is Pareto-optimal across multiple objectives? (speed, accuracy, cost)
```

---

## Output Skill Format

Generate a new SKILL.md with the following structure:

**Frontmatter:**
```yaml
---
name: [kebab-case-scaling-or-efficiency-technique]
title: [Technique Name]: Resource-Optimal Training & Deployment
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: [verified arxiv link to source paper]
keywords: [scaling-laws, resource-optimization, efficiency, compute-optimal, or domain-specific technique name]
description: Optimize {resource} by understanding {empirical law or efficiency principle}. Extracts {scaling law OR efficiency tradeoff}, providing specific performance numbers at known {costs OR hardware constraints}. Enables practitioners to {allocate compute optimally OR achieve X speedup with Y accuracy loss OR train within a budget}. Use when planning training budgets, choosing model sizes for inference, understanding compute-performance tradeoffs, or maximizing efficiency within resource constraints.
---
```

**Skill Body Structure:**

1. **Core Principle** (1 paragraph): What resource-outcome relationship does this paper establish? Why does it matter?
2. **Empirical Law or Scaling Relationship** (1 paragraph + equation form): Specific mathematical relationship discovered. What are the exponents/coefficients from experiments?
3. **Concrete Numbers Table** (bullet points or table): Specific performance points: (parameter count, training tokens, GPU-hours) → (final loss/accuracy, inference latency, memory)
4. **Budget Calculator** (1 paragraph + decision tree): Given a compute budget, what should practitioners do? Parameter allocation rules.
5. **Practical Guidance** (3-5 bullet points): Implementation details, hyperparameter sensitivity, what decisions matter most
6. **Diminishing Returns & Saturation** (1 paragraph): Where does this technique stop working? What are the limits?
7. **When to Use This Skill** (1-2 sentences): What decision-making scenarios apply this resource-outcome relationship?

**Length:** 150-250 lines

---

## Processing Instructions

1. **Identify resource type:** What resource is being studied? (compute, data, parameters, memory, latency, energy)
2. **Obtain the paper:** Fetch HTML from arxiv.org/html/{arxiv_id}, fallback to PDF
3. **Extract empirical laws:** What mathematical relationships are discovered? Specific exponents and coefficients.
4. **Tabulate specific numbers:** Create (resource) → (outcome) mappings from experiments
5. **Identify allocation strategy:** How should budget be split between model size, training data, and compute?
6. **Find tradeoff curves:** Where is the Pareto frontier? What is the accuracy-latency-memory space?
7. **Determine saturation:** At what point do further gains become diminishing?
8. **Build budget calculator:** Create a practical tool practitioners can use to plan their own allocations
9. **Validate against real experiments:** Confirm the extracted laws and numbers match the paper's reported results

---

## Quality Checks

- [ ] Paper establishes quantitative resource-outcome relationships (not just qualitative discussion)
- [ ] Specific empirical numbers are extracted (parameter counts, token counts, GPU-hours, final metrics)
- [ ] Scaling law or efficiency curve is expressed in mathematical form with numerical coefficients
- [ ] Assumptions for the empirical law are explicitly stated (e.g., compute-optimal regime, specific hardware)
- [ ] Hardware specifications are documented (GPU type, precision, batch size) so results can be contextualized
- [ ] Tradeoff curves show accuracy loss at different efficiency levels
- [ ] Budget allocation rules are specified (e.g., optimal parameter-to-token ratio)
- [ ] Saturation points or limits are identified
- [ ] Output skill provides actionable guidance for practitioners with specific budgets
- [ ] Keywords (5-10) include "scaling", "efficiency", "compute-optimal", "resource", or domain-specific terms
- [ ] Description is under 1024 characters
- [ ] Engine tag matches skillxiv-v0.0.2-claude-opus-4.6

---

## Common Pitfalls

- **Confusing this category with Component Innovation (Category 5):** Scaling & Efficiency papers focus on resource-PERFORMANCE RELATIONSHIPS across many configurations. Component papers optimize one component (e.g., replacing one attention variant with another) without systematic resource study.
- **Extracting qualitative efficiency discussion instead of quantitative laws:** Paper must provide specific numbers and curves. Skip if it's only "technique X is more efficient" without data.
- **Missing the specific hardware context:** Efficiency gains are hardware-specific. Flash Attention has different speedups on different GPUs. Document this.
- **Assuming one scaling law applies everywhere:** Laws often only hold in certain regimes (e.g., compute-optimal regime, or above a certain model size). Capture boundary conditions.
- **Overlooking data-parameter tradeoff:** In scaling papers, both tokens and parameters scale. Capture both and their relationship.
- **Ignoring practical integration challenges:** A technique may be theoretically efficient but hard to implement in practice. Extract both the theoretical efficiency and practical gotchas.
- **Missing diminishing returns:** Many efficiency techniques have saturation points. Document where gains stop.
- **Extracting without wall-clock validation:** FLOPs reduction doesn't always mean wall-clock speedup. Verify what the paper actually measures.
