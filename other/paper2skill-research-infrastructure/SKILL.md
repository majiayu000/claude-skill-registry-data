---
name: paper2skill-research-infrastructure
description: "Convert research infrastructure papers into design pattern guides. Extracts capability gaps addressed, API design decisions, performance/usability trade-offs, and integration patterns. Use this skill when extracting skills from Category 7 (Research Infrastructure) papers — PyTorch-style framework papers, evaluation harness tooling, or any paper where the tool itself is the contribution."
---

# Paper2Skill: Research Infrastructure Edition

This skill specializes in converting research infrastructure papers (frameworks, libraries, tools, evaluation systems) into structured agent skills that teach design patterns and integration strategies.

Infrastructure papers are fundamentally different from algorithmic or theoretical papers. They address capability gaps by introducing new tools or frameworks that others build on. The extractable knowledge isn't a single algorithm — it's a collection of design decisions, API patterns, performance/usability trade-offs, and integration guidance that practitioners need to make informed choices.

## What Counts as Research Infrastructure

**Infrastructure papers** introduce tools, frameworks, or systems designed to enable other research:

- **Frameworks:** PyTorch, JAX, TensorFlow, Hugging Face Transformers
- **Libraries & Tooling:** PyTorch Geometric, Ray Tune, Weights & Biases
- **Evaluation Systems:** HELM, LM-Eval-Harness, or custom benchmarking frameworks
- **Data Pipelines:** Apache Spark for ML, Hugging Face Datasets
- **Experiment Management:** Weights & Biases, CometML, MLflow
- **Development Infrastructure:** Docker-based training systems, distributed frameworks

**Not infrastructure:** Papers with a single core algorithm (MAML, Adam, GPT), theoretical analyses, or empirical studies that don't introduce a reusable tool.

## Phase 1: Identifying Extractable Infrastructure Knowledge

### Four Key Questions

Ask these before extracting:

1. **Capability Gap:** What was broken or missing before this tool? What problem does it solve? (e.g., "PyTorch filled the gap between NumPy simplicity and CUDA complexity")

2. **Design Decisions:** What architectural choices does the paper document? API design? Modularity tradeoffs? Why these choices over alternatives?

3. **Performance/Usability Trade-offs:** What does this tool optimize for? What does it sacrifice? (e.g., "Simplicity over raw performance", "Automatic differentiation convenience vs memory overhead")

4. **Integration Patterns:** How does this tool fit with the ecosystem? Requires specific dependencies? Interoperable with alternatives?

### Skill Focus by Infrastructure Type

| Infrastructure Type | Extractable Knowledge | Output Skill Teaches |
|-------------------|----------------------|---------------------|
| Framework | Core abstractions, plugin architecture, module lifecycle | Architecture patterns, when to extend vs when to fork, API design decisions |
| Library | Algorithm library design, dependency strategy, caching patterns | Which library functions to use when, performance profiles, integration challenges |
| Evaluation System | Benchmark design, metric computation, infrastructure for fairness | How to design robust evaluations, avoiding benchmark gaming, extensibility patterns |
| Data Pipeline | Data loading abstractions, preprocessing stages, parallelization | Composing pipelines, handling distributed I/O, data validation strategies |
| Experiment Management | Logging patterns, hyperparameter management, result aggregation | Tracking experiment metadata, avoiding common pitfalls, reproducibility practices |

## Phase 2: Paper Reading Strategy for Infrastructure

### Pass 1: Architecture & Positioning (3 min)

Read the introduction and any architecture diagrams. Ask:
- What problem existed before? Why is the solution non-obvious?
- What are the main system components?
- What design constraints drove the architecture? (Ease of use? Performance? Extensibility?)

### Pass 2: Core Design (7 min)

Read the design/implementation section carefully:
- What are the primary abstractions? (e.g., DataLoader, Module, Optimizer in PyTorch)
- How does the tool handle key challenges? (Distributed computation? Custom operators? Memory management?)
- What API decisions were made? Why? (Static vs dynamic graphs? Eager vs lazy evaluation?)
- What trade-offs are explicitly discussed?

### Pass 3: Case Studies & Integration (5 min)

Look for:
- Example use cases showing how to combine this tool with others
- Documented limitations or when NOT to use this tool
- Ecosystem integration patterns (plugins, extensions, third-party tools)
- Performance/memory profiles under different workloads

### Pass 4: Lessons Learned (2 min)

- Did the authors retrospectively discuss what worked well vs poorly?
- What surprised them in building this tool?
- What do they recommend for similar infrastructure projects?

## Phase 3: Extraction Template for Infrastructure Papers

Fill this before writing the skill:

```
PAPER: [title]
ARXIV: [verified arXiv ID]
URL: [full verified arXiv URL]

CAPABILITY GAP:
  What was missing or broken before?
  What user problem does this solve?

CORE ABSTRACTIONS:
  Main classes/concepts (e.g., Module, Tensor, DataLoader)
  How they compose together
  Key lifecycle events (init, forward, cleanup)

DESIGN DECISIONS & RATIONALE:
  Decision 1: [choice] because [reasoning]
  Decision 2: [choice] because [reasoning]
  (typically 3-5 major decisions)

PERFORMANCE vs USABILITY TRADE-OFFS:
  Optimization axis 1: [what was prioritized] at cost of [what was sacrificed]
  Optimization axis 2: [what was prioritized] at cost of [what was sacrificed]

API PATTERNS:
  Key method signatures and their usage
  Configuration patterns
  Extension points (how to customize)

INTEGRATION CHALLENGES:
  Known incompatibilities or awkward integrations with other tools
  When to prefer alternative tools
  Dependency management gotchas

CODE AVAILABLE: [yes/no, URL]
KEYWORDS: [5-10 infrastructure-focused keywords]
```

## Phase 4: Writing the Infrastructure Skill

### SKILL.md Structure for Infrastructure

**Title section:**
```
# [Tool/Framework Name]: [Outcome — what users can accomplish with it]
```

Example: "PyTorch: Express ML Models in Python and Execute on Any Device"

**Problem Statement (1-2 paragraphs):**
Ground in what existed before this tool and why it was insufficient. Use concrete pain points.

Example: "Before PyTorch, ML practitioners faced a stark choice: use NumPy and hand-code GPU kernels (painful), or use static-graph frameworks like TensorFlow 1.x (inflexible). PyTorch solved this by making dynamic computation graphs the default, so researchers could debug and iterate like Python code, while still compiling to efficient GPU operations."

**Core Abstractions section:**
Explain the 2-3 main concepts users interact with. Use bullet points, not ASCII diagrams.

Example for PyTorch:
- **Tensor:** Multi-dimensional arrays that track computation history and support automatic differentiation
- **Module:** Reusable, composable neural network components with learnable parameters
- **Optimizer:** Updates model parameters based on gradients computed via backprop
- **DataLoader:** Batches and parallelizes data loading, decoupling I/O from training loops

**Design Decisions section:**
Cover 3-5 architectural choices. For each, explain the alternative they rejected and why.

Example structure:
- **Dynamic vs static graphs:** PyTorch chose dynamic (eager execution) over static because it matches Python semantics. Trade-off: easier debugging, harder ahead-of-time optimization.
- **Imperative vs declarative API:** Chose imperative ("tell me step-by-step what to do") over declarative ("describe what you want"). Trade-off: more intuitive for Python programmers, less room for automatic optimization.

**Integration Patterns section:**
How does this tool fit with others? When to use vs alternatives?

- When to use: Rapid prototyping, complex models, research workflows
- When NOT to use: Inference-only (consider ONNX), mobile deployment (consider TFLite/Core ML)
- Common integrations: Hugging Face Transformers on top, ONNX export for inference, Ray for distributed training

**Performance/Usability Trade-offs:**
Create a table or list of key decisions and their costs:

| Decision | What You Get | What You Sacrifice |
|----------|------------|-------------------|
| Dynamic graphs | Easy debugging, Pythonic API | Ahead-of-time graph optimization |
| Automatic differentiation built-in | No manual backprop code | Slightly higher memory overhead |
| GPU-agnostic API | Write once, run on CPU/GPU/TPU | Small abstraction overhead |

**Implementation Considerations (if applicable):**
If the skill focuses on a specific design pattern (e.g., "how to build a custom Module"), show 1-2 concrete examples of ~20-30 lines each.

Example: "Creating a Custom Module with Gradient Checkpointing"

```python
import torch
import torch.nn as nn

class GradCheckpointedModule(nn.Module):
    """Trade memory for compute by recomputing activations during backprop.
    Useful for large models where activation storage is the bottleneck."""

    def __init__(self, layer):
        super().__init__()
        self.layer = layer

    def forward(self, x):
        # During backward, this recomputes layer(x) instead of storing activations.
        return torch.utils.checkpoint.checkpoint(self.layer, x, use_reentrant=False)
```

**Ecosystem & Extensions:**
Document how users typically extend or integrate this tool:

- Plugin system (if applicable): Document hook points
- Common third-party integrations: Lightning, Hugging Face, PyTorch Geometric
- When to fork vs contribute: Guidance on the customization boundary

**Common Pitfalls & Anti-patterns:**
From the paper and experience, document what practitioners get wrong:

- Not releasing GPU memory in loops (forgotten .detach() or .no_grad())
- Building models too dynamically (harder to save/load)
- Forgetting distributed training gotchas (all_reduce synchronization)

**Reference:**
```
Paper: https://arxiv.org/abs/XXXX.XXXXX
Code: https://github.com/pytorch/pytorch
```

## Key Rules for Infrastructure Skills

1. **Focus on design, not just features.** Don't enumerate all the modules in PyTorch. Explain the design philosophy and why each core abstraction exists.

2. **Include performance numbers.** Infrastructure papers typically benchmark their tool. Include concrete speedup claims or memory profiles.

3. **Document the ecosystem.** Practitioners want to know what builds on top of this tool and how to combine them.

4. **Explain trade-offs explicitly.** Infrastructure always trades something off. Be honest about what this tool prioritizes vs sacrifices.

5. **Give "when NOT to use" guidance.** No tool is universally best. State clearly when alternatives are better.

6. **Keep code examples focused on design patterns.** Show how the tool's abstractions are meant to be used, not basic tutorials.

## Phase 5: Quality Checks for Infrastructure Skills

- [ ] **Gap clarity:** Would someone unfamiliar with the problem understand why this tool was needed?
- [ ] **Abstraction understanding:** Can a reader explain the 2-3 core concepts to someone else?
- [ ] **Trade-off documentation:** Are the performance/usability decisions clear and justified?
- [ ] **Ecosystem context:** Does it explain how this fits with related tools?
- [ ] **Decision rationale:** For each major design choice, does it explain the alternative and why it was rejected?
- [ ] **Integration guidance:** Does it clearly state when to use vs when to prefer alternatives?
- [ ] **No feature dump:** Does it explain *why* each feature exists, or just list that it exists?

## Batch Processing Infrastructure Papers

When triaging multiple infrastructure papers:

1. **Identify infrastructure vs algorithm papers:** Infrastructure = tool/framework. Algorithm = single technique.
2. **Assess maturity:** Mature (widely adopted, extensive ecosystem) vs emerging (novel but not yet proven). Prioritize mature.
3. **Diversity:** Aim for mix of frameworks, libraries, evaluation systems.
4. **Coverage:** Extract papers that would genuinely help practitioners understand the ML infrastructure landscape.

## Reference

Infrastructure skill extraction adapted from Anthropic's skills guide and patterns in the Orchestra-Research repository. Infrastructure papers demand different extraction templates than algorithmic or theoretical papers because they teach architecture and design patterns, not step-by-step procedures.
