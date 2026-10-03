---
name: paper2skill-field-foundation
description: "Convert foundational papers that create new subfields into conceptual framework skills. Extracts problem definitions, vocabulary, founding experiments, and opened research directions. Use this skill when extracting skills from Category 8 (Field Foundation) papers — MAML-style paradigm-creating papers or 'Deep Learning' review-style papers that define entire research communities."
---

# Paper2Skill: Field Foundation Edition

This skill specializes in converting foundational papers — those that establish new fields, paradigms, or problem definitions — into structured agent skills that convey conceptual frameworks, vocabulary, and the empirical foundations of a research direction.

Foundational papers are the hardest category to extract skills from because they don't have a single "algorithm" to implement. Instead, they define a landscape: new vocabulary, new problem formulations, new ways of thinking about old problems, and opening moves in what becomes a field.

## Understanding Field Foundation Papers

A **field foundation paper** does one or more of these:

1. **Creates a new problem class.** E.g., MAML introduced "meta-learning" as a distinct problem; before MAML, people did transfer learning or few-shot learning ad-hoc.

2. **Introduces foundational vocabulary and concepts.** The LeCun/Bengio/Hinton "Deep Learning" review established the vocabulary and conceptual framework the entire field uses.

3. **Proposes a new paradigm over existing approaches.** E.g., "Attention Is All You Need" (Transformers) didn't just introduce an architecture — it fundamentally changed how we think about sequence modeling.

4. **Runs founding experiments that validate a new direction.** E.g., GPT papers showed that scaling language model pretraining was a viable path forward (enabling the current era).

5. **Opens multiple future research directions.** A field foundation paper is one where you can point to dozens of follow-on papers and trace their lineage back.

### Infrastructure vs Field Foundation

A **distinction:** Infrastructure papers (PyTorch, HELM) introduce tools. Field foundation papers introduce ideas and problem definitions. Both can create new research areas, but in different ways.

- **Infrastructure:** "Here's a tool that makes X easier." (Derivative: thousands of papers using the tool)
- **Field Foundation:** "Here's a problem worth studying / Here's a new way to think about this problem." (Derivative: hundreds of papers exploring the problem space)

## Identifying What to Extract

### Three Paper Types in Category 8

**Type 8A: Algorithmic Founding Papers**
Examples: MAML, Transformers, Vision Transformers
These have a **clear algorithm** at their core, BUT they also define a problem class or paradigm.

Extraction: Do both — extract the algorithm (like you would for a technique paper), BUT also extract the paradigm they establish. What new problem do they define that didn't exist before?

**Type 8B: Conceptual/Survey Founding Papers**
Examples: "Deep Learning" review (LeCun et al.), "A Primer on Neural Network Architectures"
These have **no single algorithm**. Instead they establish vocabulary, categorize problems, and set the research agenda.

Extraction: This is purely conceptual. Extract vocabulary, problem taxonomy, opening directions, and founding experiments.

**Type 8C: Paradigm-Shift Papers**
Examples: "Attention Is All You Need" (shifted from RNNs to Transformers), "Scaling Laws for Neural Language Models"
These **reframe how we think** about a problem.

Extraction: What old assumptions did this paper invalidate? What new assumptions did it establish? What experiments prove the new paradigm works?

### Assessment Rubric

Does this paper... | Points | Notes
---|---|---
Introduce new terminology that becomes field-standard? | 1 | Check citations and follow-on papers
Define a new problem class (not previously studied this way)? | 1 | Is there a clear "before and after" shift?
Propose a new paradigm or alternative to existing approaches? | 1 | Does it reframe the problem?
Run founding experiments validating the direction? | 1 | Are these canonical/replicated often?
Open multiple subsequent research directions? | 1 | Do you see 10+ papers building on this idea?

**Threshold:** Need 3+ points to extract as a field foundation paper.

## Phase 2: Reading a Field Foundation Paper

### Pass 1: Positioning & Contribution (5 min)

- What is this paper claiming is wrong or missing in the status quo?
- What new term, problem, or paradigm is it introducing?
- Is there a clear moment in the paper where they say "X is not the right way to think about this; instead, Y"?

Read: intro, abstract, key figures

### Pass 2: Conceptual Core (10 min)

- What are the 2-3 foundational concepts this paper introduces?
- What does the paper define (formally or informally) that didn't have a clear definition before?
- What is the opening set of experiments that validate this new direction?
- What is the "aha moment" — the insight that makes this direction worth pursuing?

Read: method section (if there is one), early experiments

### Pass 3: Taxonomy & Problem Formulation (5 min)

- Does the paper organize a problem space into categories?
- What are the dimensions along which problems in this field vary?
- Are there clear sub-problems or follow-up questions the paper raises but doesn't answer?

Read: related work (reframed through new vocabulary), discussion

### Pass 4: Empirical Foundations (5 min)

- What are the canonical experiments that prove this paradigm works?
- What are the baselines? What do they fail at? What does the new paradigm do better?
- What are the key experimental findings (beyond raw accuracy numbers)?

Read: results, ablations, qualitative analysis

### Pass 5: Opening Directions (2 min)

- What does the paper explicitly list as future work?
- What implicit questions does the paradigm open? ("If this works, what about...?")

Read: conclusion, future work

## Phase 3: Extraction Template

### For Type 8A (Algorithmic Founding Papers)

```
PAPER: [title]
ARXIV: [verified ID]
URL: [full URL]

PROBLEM STATEMENT:
  What is the problem this paper addresses?
  Why is this an important problem?
  What existing approaches are inadequate? (and why)

NEW PARADIGM OR PROBLEM CLASS:
  What new way of thinking about this problem does it introduce?
  What terminology becomes field-standard?
  How does this reframe the problem?

CORE ALGORITHM/APPROACH:
  High-level pseudocode or conceptual description (2-3 sentences)
  Key innovation (what's novel vs prior work)

FOUNDING EXPERIMENTS:
  What are the canonical experiments that validate this direction?
  Key results (qualitative + quantitative)
  Ablations: what matters, what doesn't

OPENED RESEARCH DIRECTIONS:
  What follow-up questions does this paper raise?
  What sub-problems or extensions are obvious next steps?
  (List 3-5 obvious directions)

VOCABULARY INTRODUCED:
  New terms or concepts that become standard (3-5 terms)
  Brief definition for each

KEYWORDS: [5-10 foundational keywords]
```

### For Type 8B (Conceptual/Survey Founding Papers)

```
PAPER: [title]
ARXIV: [verified ID]
URL: [full URL]

FIELD/PARADIGM BEING DEFINED:
  What is the research area or way of thinking about a problem?
  What makes this a coherent field/paradigm vs scattered topics?

PROBLEM TAXONOMY:
  How does the paper categorize problems in this area?
  Key axes of variation (e.g., supervised vs unsupervised, offline vs online)
  Sub-problem classes with examples

FOUNDATIONAL CONCEPTS:
  Core ideas that define how researchers in this field think (5-7 concepts)
  For each: definition, why it's essential, relation to other concepts

VOCABULARY STANDARDIZED:
  Terms that become field-standard after this paper (5-8 terms)
  Brief definition for each, why the term matters

FOUNDING EXPERIMENTS & EVIDENCE:
  What are the canonical experiments validating this paradigm?
  Key empirical findings
  What was surprising or counter-intuitive?

RESEARCH LANDSCAPE (BEFORE/AFTER):
  How did people study this problem before?
  What changed after this paper?
  What became possible that wasn't before?

OPENED RESEARCH DIRECTIONS:
  Explicit (listed in paper)
  Implicit (obvious extensions of the framework)
  Sub-fields this spawned (if applicable)

KEYWORDS: [5-10 vocabulary/paradigm keywords]
```

## Phase 4: Writing the Field Foundation Skill

### Skill Structure for Type 8A (Algorithmic Founding)

**Title:**
```
# [Technique/Paradigm Name]: [Outcome — what it lets you do]
```

Example: "Meta-Learning (MAML): Learn New Tasks From Few Examples"

**Section 1: The Problem (2-3 paragraphs)**
- Describe what problem existed before this paper
- Why was it hard? What existing approaches failed?
- Use concrete examples, not abstractions

Example: "Before MAML, the field of learning from small datasets was scattered. Transfer learning worked via fine-tuning — but required many labeled examples. Few-shot learning was studied ad-hoc in specific domains (vision, NLP) with hand-engineered features. No one had a principled algorithm to learn *how* to learn from small datasets across different tasks."

**Section 2: The Paradigm Shift**
- What new way of thinking did this paper introduce?
- What question does it ask that nobody asked before?
- What becomes a "discipline" after this paper?

Example: "MAML reframed the problem. Instead of asking 'How do I fine-tune on small data?', it asked 'What initial parameters would let any model learn new tasks quickly with few examples?' This transformed learning-from-small-data into 'meta-learning' — a subfield with its own problem class, metrics, and benchmark tasks."

**Section 3: The Core Idea (1-2 paragraphs)**
- Explain the algorithm or approach in plain language
- What is the key insight?
- How is this different from what came before?

For MAML: "The key insight: You don't need to learn the final model — you need to learn parameters that are positioned in loss landscape such that a few gradient steps land in a good solution. MAML optimizes the initial parameters to minimize loss after 1-5 fine-tuning steps on a new task."

**Section 4: Founding Experiments (2-3 paragraphs)**
- What are the canonical experiments that prove this works?
- What were people surprised by?
- Quantitative results (if applicable)
- Qualitative insights

Example table for MAML:

| Benchmark | MAML | Transfer Learning | Few-Shot Baseline |
|-----------|------|------------------|-------------------|
| Omniglot (1-shot) | 98.7% | 94.5% | 89.2% |
| miniImageNet (5-shot) | 63.2% | 61.4% | 52.1% |

Also include: MAML worked across diverse domains (vision, RL, NLP) without modification — showing the paradigm was general.

**Section 5: Vocabulary & Concepts**
- List the 4-6 core concepts this paper establishes
- For each, 1-2 sentences explaining why it matters

Example for MAML:
- **Task Distribution:** Meta-learning requires defining what counts as a "new task." MAML assumes a distribution of tasks and optimizes for fast adaptation across all of them.
- **Inner Loop:** The few gradient steps on a new task. MAML differentiates through this inner loop to optimize initial parameters.
- **Outer Loop:** The meta-training step that updates initial parameters based on inner loop performance across task distribution.
- **Few-Shot Adaptation:** Learning a new task with k examples. MAML's metric is: how fast can you adapt?

**Section 6: Opened Research Directions**
- List 5-8 follow-up questions or extensions the paradigm opens
- For each, 1-2 sentences on why it's natural/obvious

Example for MAML:
- How to meta-learn when task distribution is unknown? (Unsupervised meta-learning)
- Can meta-learning work in continuous control (RL)? (Led to MAML-RL, and entire meta-RL subfield)
- What if inner loop is too expensive? (Led to fast adaptation variants: Prototypical Networks, Matching Networks)
- How do you design task distributions? (Led to research on task sampling, task diversity)

**Section 7: When to Use This Paradigm**
When this direction is appropriate:
- Few examples available for each task
- Task distribution is well-defined
- You want a general learning algorithm, not per-task tuning

When NOT:
- Plenty of data for target task (standard supervised learning is better)
- No clear task distribution
- Computational cost of inner loop is prohibitive

**Reference:**
```
Paper: https://arxiv.org/abs/XXXX.XXXXX
Code: [URL if available]
Related subfield: Meta-Learning
```

---

### Skill Structure for Type 8B (Conceptual/Survey Founding Papers)

**Title:**
```
# [Field/Paradigm Name]: [Outcome — what thinking this enables]
```

Example: "Deep Learning: Representation Learning for AI and Massive Data"

**Section 1: What is This Field? (2-3 paragraphs)**
- What is the field studying?
- Why is it distinct from related areas?
- What makes it a "field" vs scattered techniques?

Example: "Deep Learning is the study of learning hierarchical representations from raw data. Unlike traditional machine learning (hand-engineered features + shallow learning), deep learning learns feature hierarchies automatically. The field emerged because: (1) neural networks are fundamentally scalable, (2) massive datasets changed what was tractable, (3) GPUs made large-scale training feasible."

**Section 2: Problem Taxonomy**
- Break down problems in this field by key dimensions
- Use a table or clear categories

Example table for Deep Learning:

| Dimension | Variants | Examples |
|-----------|----------|----------|
| **Architecture** | CNNs, RNNs, Transformers | Image (CNN), Sequence (RNN/Transformer) |
| **Task** | Supervised, Unsupervised, RL | Classification, Clustering, Policy Learning |
| **Scale** | Small models, Medium, Large | ResNet-50, BERT, GPT |
| **Data Regime** | Lots of labels, Few labels, No labels | ImageNet, Few-shot, Self-supervised |

**Section 3: Foundational Concepts (3-5 paragraphs)**
- For each core concept: definition + why it matters + how it changed thinking

Example concepts for Deep Learning:
- **Hierarchical Representations:** Deep networks automatically learn multi-level features. Low layers learn edges; mid layers learn shapes; high layers learn objects. This is more efficient than hand-engineering all features.
- **Backpropagation at Scale:** Backprop + modern hardware (GPUs) + large datasets made end-to-end training of deep networks feasible.
- **Non-convex Optimization in High Dimensions:** Traditional optimization theory says this shouldn't work (local minima). In practice, overparameterized networks with gradient descent find good solutions. Why? Still partially mysterious, but empirically very reliable.
- **Transfer Learning & Pre-training:** Learning useful representations on massive datasets (ImageNet, Wikipedia text) then fine-tuning on downstream tasks. This is the canonical deep learning workflow.

**Section 4: Vocabulary & Terminology**
- List 6-10 terms that became standard in this field
- For each: definition + context for when you use it

Example for Deep Learning:

| Term | Definition | Used When |
|------|-----------|-----------|
| **Activation Function** | Element-wise nonlinearity (ReLU, tanh, sigmoid) that enables networks to learn nonlinear representations | Defining any neural network architecture |
| **Backpropagation** | Algorithm to compute gradients of loss w.r.t. all parameters by reverse-mode AD | Training any supervised model |
| **Convolutional Layer** | Parameter-efficient layer exploiting spatial structure via weight sharing and local receptive fields | Processing images, sequences, or grid-structured data |
| **Batch Normalization** | Normalizing layer inputs to accelerate training and stabilize learning | Standard in modern deep nets for stability/speed |
| **Fine-tuning** | Adapting a pre-trained model to a downstream task via continued training | Transfer learning workflow |

**Section 5: Founding Experiments & Empirical Evidence**
- What are the canonical experiments that established this field?
- What surprising results validated the approach?
- Quantitative + qualitative insights

Example for Deep Learning:
- **AlexNet (2012):** Deep CNNs crushed traditional vision methods on ImageNet. This was the moment deep learning became undeniable.
- **ImageNet Scaling:** Each year, deeper networks won. This empirical observation drove the "scaling hypothesis" — a core belief of modern AI.
- **Transfer Learning Breakthrough:** Features learned on ImageNet transferred to other visual domains. This showed learned representations are general, not specific to training distribution.
- **Language Model Scaling:** GPT/BERT showed the same scaling laws apply to language. Models trained on billions of tokens transfer to any downstream NLP task. This opened the LLM era.

**Section 6: Pre vs. Post This Paper**

Before this field/paradigm:
- What was the dominant approach?
- What was hard or impossible?

After this field/paradigm:
- What changed?
- What became possible?
- What metrics became standard?

Example:

Before Deep Learning:
- Computer vision relied on hand-crafted features (SIFT, HOG)
- Getting >95% on ImageNet was state-of-the-art
- Scaling the model meant more features to hand-engineer

After Deep Learning:
- End-to-end learning from raw pixels
- >99% on ImageNet is routine
- Scaling means bigger networks, more data, more compute — all automatable
- Transfer learning became the standard workflow
- Emergent capabilities (in large LLMs) became possible

**Section 7: Opened Research Directions & Subfields**
- Explicit directions listed in the paper
- Implicit questions the paradigm raises
- Sub-disciplines that emerged

Example for Deep Learning:
- **Architecture design:** What structure of network is best for X task? (CNNs, RNNs, Transformers, Diffusion, ...)
- **Scaling laws:** How do performance and efficiency scale with model size, data, compute? (Led to foundational scaling laws research)
- **Interpretability:** How do we understand what deep networks learn? (Entire subfield)
- **Adversarial robustness:** Why are deep networks so vulnerable to tiny input perturbations? How to make them robust?
- **Few-shot learning:** Can deep networks learn new tasks from tiny datasets? (Led to meta-learning)
- **Self-supervised learning:** Can we learn useful representations without labels? (Led to contrastive learning, diffusion models, LLMs)
- **Alignment & safety:** How do we ensure large models are safe and aligned? (Increasingly urgent as models scale)

**Section 8: Scope & Limitations**
- Where does this field/paradigm apply well?
- Where does it struggle or fail?
- Are there problems this approach is fundamentally ill-suited for?

Example for Deep Learning:
- Works well: Unstructured data (vision, language, audio), large-scale learning, transfer learning scenarios
- Struggles: Small data regimes (overfits), interpretability (black boxes), data efficiency (requires lots of examples), adversarial robustness
- Fundamentally limited for: Symbolic reasoning, causal inference, systems requiring hard constraints, few-shot learning (some progress but not solved)

**Reference:**
```
Paper: https://arxiv.org/abs/XXXX.XXXXX
Related field: [Domain]
Survey/Review: [Yes/No, and if yes, what does it survey]
```

## Key Rules for Field Foundation Skills

1. **Don't oversimplify to a single algorithm.** If the paper doesn't have one, say so. Foundational papers often define a landscape, not a technique.

2. **Vocabulary matters.** What terms does this paper introduce that become field-standard? These are the core extractable knowledge.

3. **Reframe before/after.** What changed about how people think about this problem after this paper?

4. **Mine for opened directions.** Field foundation papers are valuable because they open future research. Explicitly list what they make possible.

5. **Include founding experiments.** What are the canonical benchmarks or results that made this direction credible?

6. **Be honest about limitations.** No paradigm is universal. State where this field applies and where it fails.

## Phase 5: Quality Checks for Field Foundation Skills

- [ ] **Clarity of paradigm shift:** Without reading the paper, can someone understand what new way of thinking this introduces?
- [ ] **Vocabulary utility:** Are the defined terms actually what researchers in this field use?
- [ ] **Founding experiments concrete:** Are the canonical experiments specific enough to find and replicate?
- [ ] **Opened directions plausible:** Do the listed research directions feel like natural follow-ups?
- [ ] **Before/after comparison:** Is the contrast between old thinking and new thinking explicit?
- [ ] **Scope honesty:** Does it acknowledge where this paradigm is limited?
- [ ] **Not a summary:** Does it teach the framework, not just paraphrase the abstract?

## Batch Processing Field Foundation Papers

When triaging foundational papers:

1. **Assess maturity:** Is this a mature field (decades old) or an emerging paradigm (2-3 years)?
2. **Check impact:** Do follow-on papers cite this foundationally? Is it in textbooks?
3. **Coverage balance:** Aim for mix of old paradigms (established fields), recent paradigms (5-10 years), and emerging (1-3 years).
4. **Avoid commodity techniques:** A well-executed technique paper that didn't spawn a field should be extracted as Category 3, not Category 8.

## Reference

Field foundation extraction adapted from Anthropic's skills guide. Unlike algorithm or infrastructure extraction, foundational papers require distilling concepts, vocabulary, and paradigms. The output skill teaches frameworks and problem formulations, not procedures.
