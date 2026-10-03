---
name: paper-categorizer
description: >
  Categorize ML/AI research papers into 11 types based on their title and abstract.
  Returns structured JSON with a primary category, optional secondary categories,
  extractability rating, and rationale. Designed for the SkillXiv paper2skill pipeline
  as a triage step. Use this skill whenever the user wants to classify, categorize,
  sort, or triage research papers — whether a single paper or a batch. Also trigger
  when someone asks "what kind of paper is this?", wants to filter papers by type,
  or needs to decide which papers to prioritize for skill extraction.
---

# Paper Categorizer

Classify ML/AI research papers into one of 11 categories based on their title and abstract. The categories capture *what kind of contribution* the paper makes — not its topic or subfield — and what kind of *extractable skill* follows from that contribution.

## The 11 Categories

Each category reflects a distinct way a paper contributes to the field. When classifying, ask yourself: "What is this paper's *move*? What is it doing for the community? And what kind of skill can someone extract from it?"

### 1. Application Transfer *(was: "Meaningful Applications")*

The paper takes existing techniques and applies them to a real-world problem where the impact matters beyond ML itself. The key insight is not just "apply method X to domain Y" — it's knowing *why* the problem is hard enough to matter and *what had to change* to make the method work in a new context.

**Signals:** Solves a domain-specific problem (medicine, robotics, science, industry). The abstract talks about real-world deployment, practical impact, or domain experts. The novelty is in *what* they solved, not the method itself.

**Sub-types worth distinguishing:**
- *Domain transfer* — same method, new field
- *Real-world deployment* — lab → production constraints
- *Interdisciplinary crossing* — e.g., RL for protein folding

**Not this if:** The application is just a test bed for a new method (that's probably category 5 or 6).

**Extractable skill:** Problem formulation, the gap between existing methods and the requirement, and the adaptation decisions made.

**Examples:** AlphaGo, AlphaFold, Learning Quadrupedal Locomotion over Challenging Terrain.

### 2. Evaluation Infrastructure *(was: "Datasets & Benchmarks")*

The paper's primary contribution is a new dataset, benchmark suite, evaluation protocol, or competitive arena for the community. This category splits into two distinct extraction pipelines: a *dataset paper* yields skills around data collection protocol, annotation design, and quality control; a *benchmark paper* yields skills around task definition, metric selection, and leaderboard design. These are quite different — COCO teaches you annotation, SWE-bench teaches you evaluation design. Worth tagging which sub-type it is.

**Signals:** The abstract emphasizes scale of data, annotation effort, evaluation metrics, baselines, or community adoption. Words like "benchmark," "dataset," "evaluation suite," "leaderboard," "arena."

**Sub-types worth distinguishing:**
- *Dataset paper* — data collection protocol, annotation design, quality control
- *Benchmark paper* — task definition, metric selection, leaderboard design

**Not this if:** A new dataset is introduced only to validate a method — if the method is the star, categorize by the method's contribution type instead.

**Extractable skill:** Data collection protocol or evaluation design methodology.

**Examples:** ImageNet, COCO, GLUE, SWE-bench.

### 3. Paradigm Challenge *(was: "Challenge the Common Knowledge")*

The paper's main contribution is showing that something the community widely believes is wrong, incomplete, or more nuanced than assumed. The extraction skill here is: what was the prior belief, what controlled experiment falsifies it, and what revised principle replaces it.

This is close to Category 9, but the difference is *direction* — Category 3 is *adversarial* ("I'm proving you wrong"), Category 9 is *exploratory* ("I want to understand"). "Rethinking Generalization" is Category 3; "Network Dissection" is Category 9. Keep them separate.

**Signals:** The title or abstract contains words like "rethinking," "revisiting," "do we really need," "understanding why," "a closer look," "myth," "misconception." The paper presents surprising experimental results that contradict conventional wisdom. Often includes controlled experiments isolating one assumption.

**Not this if:** The paper just proposes a better alternative (that's category 5). The key here is the *insight* — revealing that something believed true is false or misleading.

**Extractable skill:** The prior belief, the falsifying experiment, and the revised principle.

**Examples:** "Understanding Deep Learning Requires Rethinking Generalization," "Rethinking Transformers in Solving POMDPs."

### 4. Systematic Empiricism *(was: "People Complain! I Experiment and Summarize Tricks")*

The paper addresses a pain point the community has been struggling with by systematically experimenting with implementation details, hyperparameters, or training tricks, and distilling the findings into actionable guidance. This is one of the highest-value categories for skill extraction because the output is already close to executable knowledge — ordered lists of decisions with performance impact.

**Signals:** The abstract mentions "implementation details," "tricks," "practical guide," "recipes," "best practices," "empirical study of X." Often includes ablation-heavy experimental sections. The paper might not propose anything new — it organizes what's already known but scattered or tribal.

**Sub-types:**
- *Implementation tricks* — e.g., "37 PPO details"
- *Hyperparameter studies* — e.g., "which regularizer to use"
- *Design choice ablations* — e.g., "does vision modality matter?"

**Not this if:** The paper proposes a new method that happens to include ablations (that's category 5). Category 4 papers are fundamentally about *systematizing existing knowledge* for practitioners.

**Extractable skill:** A ranked list of recommendations with conditions of applicability.

**Examples:** "The 37 Implementation Details of Proximal Policy Optimization," "Regularization Matters in Policy Optimization."

### 5. Component Innovation *(was: "I Change One Small Thing; But I Make a Big Difference")*

The paper introduces a relatively simple, elegant modification to an existing approach that yields surprisingly large improvements. Finer-grained than it looks — the "small thing" could be an architecture component (residual connection), a normalization choice (batch norm), a loss function, a data augmentation strategy, or an optimizer modification. Each implies a different extraction target.

The key skill to extract is: what component was swapped, what motivated the swap, what conditions determine when it helps, and what the performance delta is.

**Signals:** The core idea can be explained in one sentence. The abstract highlights a simple change with strong empirical gains. Often modifies a single component. The method section is short relative to the experiments.

**Critical distinction:** Always ask: *is this actually a small change, or does it reframe the whole problem?* — the latter is Category 8, not 5.

**Not this if:** The contribution is a large, complex system (that might be category 1 or 7). The hallmark of category 5 is *elegant simplicity*.

**Extractable skill:** What component was swapped, the motivation, conditions for when it helps, and the performance delta.

**Examples:** Batch Normalization, ResNet (skip connections), Transformers Without Normalization.

### 6. Insight-Driven Papers *(was: "Neat / Cute Papers! I Look Into Details")*

The paper is driven by a *single non-obvious observation* that unlocks a problem that seemed fundamentally hard, with a minimal implementation. "Learning to See in the Dark" works because of one data insight (raw sensor data instead of processed). The extraction template should identify: the key insight in one sentence, how it simplifies the problem, and the minimal recipe to reproduce the core result.

**Signals:** The problem is unusual, specific, or delightfully niche. The paper shows deep understanding of a narrow phenomenon. Often visually interesting results. The contribution is in the *thoroughness* and *craftsmanship* on a specific problem.

**Sub-types:**
- *Observation-driven* — you notice something about data
- *Formulation-driven* — you reframe the problem
- *Perspective-shift* — same equations, new interpretation

**Not this if:** The problem is a mainstream challenge (that's probably category 1 or 5). Category 6 papers stand out by their *unexpectedness* or *specificity*.

**Extractable skill:** The key insight, how it simplifies the problem, and the minimal recipe to reproduce it.

**Examples:** "Learning to See in the Dark," "Live Repetition Counting."

### 7. Research Infrastructure *(was: "Infrastructure. I Didn't Dig Gold; I Sell Water!")*

The paper's contribution is a tool, library, framework, or system that enables others to do research or build applications more effectively. Extraction here should focus on: what capability gap is being addressed, key API/design decisions and the reasoning behind them, and performance/usability trade-offs.

Worth splitting into *framework papers* (PyTorch, JAX) and *tooling papers* (evaluation harnesses, data pipelines, experiment management) — they produce different types of reusable skills.

**Signals:** The abstract talks about ease of use, scalability, API design, community adoption, supported models/tasks, integration. Words like "framework," "library," "toolkit," "platform," "system," "open-source."

**Sub-types:**
- *Framework papers* — PyTorch, JAX, general-purpose platforms
- *Tooling papers* — evaluation harnesses, data pipelines, experiment management

**Not this if:** The paper proposes a new method and just releases code (most papers do that). Category 7 is for papers where the *tool itself* is the contribution.

**Extractable skill:** Design decisions, API patterns, and performance/usability trade-offs.

**Examples:** PyTorch, Caffe, Hugging Face Transformers, PyTorch Geometric.

### 8. Field Foundation *(was: "I Create a (Sub)field")*

The paper is foundational — it defines a new problem space, introduces a new paradigm, or synthesizes ideas into a coherent framework that spawns a line of follow-up research. This is the hardest category to extract skills from, because foundational papers often don't have a clean algorithm — they define a vocabulary, a problem class, and a set of open questions. The extractable skill is more *conceptual*: what new problem is being named, what framework/vocabulary is introduced, what the founding experiments look like, and what directions are explicitly opened.

Note: MAML extracts differently than "Deep Learning" the review paper — both are Category 8 but one has a clear algorithm and the other has a conceptual framework.

**Signals:** Highly ambitious scope. Introduces new terminology that the field later adopts. The abstract frames a broad research direction rather than a specific result. Often surveys or unifies existing ideas into a new framework.

**Not this if:** The paper is a strong method paper that gets lots of citations (that might be category 5). Category 8 is about *paradigm creation*, not just impact.

**Extractable skill:** The new problem definition, vocabulary, founding experiments, and opened research directions.

**Examples:** "Deep Learning" (LeCun, Bengio, Hinton), "Deep Compression," "Model-Agnostic Meta-Learning (MAML)."

### 9. Mechanistic Analysis *(was: "I Analyze and Understand")*

The paper's primary goal is to understand *why* something works, *what* a model has learned, or *how* a phenomenon behaves. The extraction target here is the *analytical methodology*, not just the finding. "Network Dissection" teaches you a general method for probing what neurons represent. "Do Differentiable Simulators Give Better Policy Gradients?" teaches you an experimental design for comparing gradient estimators.

The skill is transferable if you extract: what question is being asked, what analytical instrument is used to answer it, what confounds are controlled for, and what the finding implies for practitioners.

**Signals:** The abstract frames questions rather than solutions. Words like "analyze," "understand," "interpret," "probe," "dissect," "theoretical analysis," "what does it mean to." Heavy on visualization, probing experiments, or mathematical analysis.

**Key distinction from Category 3:** Category 3 is *adversarial* ("I'm proving the community wrong"), Category 9 is *exploratory* ("I want to understand how this works"). If the paper's primary energy goes into dismantling a prior belief, it's Category 3. If it's investigating a phenomenon with curiosity, it's Category 9.

**Not this if:** The analysis leads to a new method that becomes the focus (that's category 5). Category 9 stays in the analytical mode — the understanding itself is the contribution.

**Extractable skill:** The analytical methodology — question, instrument, controls, and practitioner implications.

**Examples:** "Network Dissection," "Theoretical Analysis of Self-Training," "Do Differentiable Simulators Give Better Policy Gradients?"

### 10. Survey & Synthesis *(NEW)*

The paper is a survey, position paper, tutorial, or roadmap. Surveys and position papers are increasingly common and valuable — they produce a different kind of skill: taxonomy construction, literature navigation heuristics, and identification of open problems. Your current 9 categories are all primary research paper types, but this category captures the meta-level contributions.

**Signals:** The abstract mentions "survey," "review," "overview," "tutorial," "roadmap," "position paper," "landscape," "state of the art." The paper covers a broad range of existing work rather than presenting new experiments.

**Sub-types:**
- *Technical survey* — comprehensive coverage of methods
- *Position paper* — argued perspective
- *Tutorial* — pedagogical walkthrough
- *Roadmap* — community direction-setting

**Not this if:** The paper creates a new paradigm while surveying (that's category 8). Category 10 is for papers whose primary contribution is *organizing existing knowledge*, not creating new knowledge.

**Extractable skill:** A structured taxonomy and a list of unresolved questions.

**Examples:** "A Survey of Large Language Models," "Attention Is All You Need" (partially tutorial), comprehensive review papers.

### 11. Scaling & Efficiency *(NEW)*

The paper studies what happens as you add compute/data/parameters, or how to get the same result with less. Scaling papers and efficiency papers have a specific extractable pattern: what resource is being studied, what empirical laws emerge, what the practical implications are for someone with a given budget.

This deserves its own category separate from Component Innovation (Category 5). Scaling papers are about *resource-performance relationships*, not single component swaps.

**Signals:** The abstract mentions "scaling laws," "compute-optimal," "efficiency," "distillation," "compression," "pruning," "quantization," "speedup," "FLOPs," "inference cost." The paper studies how performance changes with resources or how to reduce resource requirements.

**Not this if:** The paper introduces a small architectural change that happens to be more efficient (that's category 5). Category 11 papers are fundamentally about *the relationship between resources and performance*.

**Extractable skill:** Resource-performance relationships, empirical laws, and practical budget implications.

**Examples:** GPT-3 (scaling), Chinchilla (compute-optimal training), Flash Attention (efficiency), knowledge distillation papers.

## Classification Process

When given a paper's title and abstract, follow this reasoning:

1. **Identify the core move.** What is this paper *doing* for the community? Is it building a tool? Sharing data? Proving something wrong? Solving a real problem? Explaining why something works? Scaling up? Surveying a field?

2. **Check category fit from the top.** Start with the most distinctive categories (8, 10, 11, 7, 2) since they have the clearest signals, then check the more nuanced ones (3 vs 9, 4, 6, 5, 1).

3. **Apply the key distinctions:**
   - Category 3 vs 9: Is the paper *adversarial* (proving something wrong → 3) or *exploratory* (investigating how something works → 9)?
   - Category 5 vs 8: Is it a *small component change* (→ 5) or does it *reframe the whole problem* (→ 8)?
   - Category 5 vs 11: Is it a *single component swap* (→ 5) or about *resource-performance relationships* (→ 11)?
   - Category 9 vs 10: Is it *analyzing a specific phenomenon* (→ 9) or *surveying/organizing a broad area* (→ 10)?

4. **Assign primary category.** Pick the single best fit — the category that captures the paper's *main* contribution.

5. **Consider secondary categories (0-2).** Some papers genuinely straddle categories. Only add secondaries when there's a real case for it — don't just pad the list.

6. **Tag the sub-type** if the category has sub-types defined above.

7. **Rate extractability.** How easily does this paper convert into an executable skill?
   - `high` — Categories 4, 5, 7 tend to produce highly executable skills
   - `medium` — Categories 1, 2, 3, 6, 11 produce moderately executable skills
   - `low` — Categories 8, 9, 10 tend to produce more conceptual/strategic skills

8. **Write a rationale.** One or two sentences explaining your reasoning — what made you pick this category over plausible alternatives.

## Output Format

Return a JSON object with this structure:

```json
{
  "paper_title": "The paper's title",
  "primary_category": {
    "id": 5,
    "name": "Component Innovation",
    "confidence": "high",
    "sub_type": "architecture component"
  },
  "secondary_categories": [
    {
      "id": 3,
      "name": "Paradigm Challenge",
      "confidence": "medium"
    }
  ],
  "extractability": "high",
  "rationale": "This paper introduces skip connections — a minimal architectural change — that enables training much deeper networks. The simplicity-to-impact ratio is the hallmark of category 5. It also mildly challenges the assumption that deeper networks are always harder to train (category 3), but the main contribution is the method, not the insight."
}
```

**Confidence levels:**
- `high` — clear fit, strong signals, little ambiguity
- `medium` — reasonable fit, some signals, but could plausibly be another category
- `low` — weak fit, assigned as secondary because there's a partial case

**Category names** (use these exact strings):
1. "Application Transfer"
2. "Evaluation Infrastructure"
3. "Paradigm Challenge"
4. "Systematic Empiricism"
5. "Component Innovation"
6. "Insight-Driven Papers"
7. "Research Infrastructure"
8. "Field Foundation"
9. "Mechanistic Analysis"
10. "Survey & Synthesis"
11. "Scaling & Efficiency"

## Batch Mode

When given multiple papers, return a JSON array of the above objects. Process each paper independently — don't let one paper's categorization influence another's.

## Edge Cases

- **Survey papers** that just summarize a field → category 10 (Survey & Synthesis), not category 8 or 9.
- **Papers introducing both a method and a dataset** → categorize by whichever is the *bigger* contribution. If the dataset is the lasting legacy (like ImageNet), it's category 2. If the method is, and the dataset is just validation, use the method's category.
- **Position papers / opinion pieces** → category 10 if they survey and synthesize, category 3 if they primarily challenge consensus, category 8 if they propose a new research agenda.
- **Reproduction studies** → category 4 (systematic empiricism) if they surface practical insights, category 9 (mechanistic analysis) if they're purely investigative.
- **System papers** that build an end-to-end pipeline → category 7 if the system is meant for community reuse, category 1 if it solves a specific application.
- **Scaling law papers** → category 11, not category 9, even though they involve analysis. The focus is on resource-performance relationships.
- **Distillation / compression papers** → category 11 if the focus is efficiency at scale, category 5 if it's a single technique change.
- **MAML vs "Deep Learning" review** → both category 8, but note that MAML has a clear algorithm (high extractability) while the review has a conceptual framework (low extractability). Use the sub_type field to distinguish.
