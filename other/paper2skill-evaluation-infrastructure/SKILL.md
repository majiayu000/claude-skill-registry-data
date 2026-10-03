---
name: paper2skill-evaluation-infrastructure
description: "Convert dataset and benchmark papers into evaluation infrastructure skills. For datasets: extracts collection protocol, annotation design, quality control. For benchmarks: extracts task definition, metric selection, leaderboard design. Use this skill when extracting skills from Category 2 (Evaluation Infrastructure) papers — ImageNet-style dataset papers, SWE-bench-style benchmark papers, or any paper whose primary contribution is evaluation methodology."
---

## When to Use
Apply this skill when you encounter arXiv papers that:
- Introduce a new dataset with annotation/collection procedures (ImageNet, COCO, GLUE, SWE-bench)
- Define a new benchmark or evaluation protocol with metrics justification
- Describe annotation schema, inter-annotator agreement, or quality assurance procedures
- Discuss scale considerations or data curation decisions
- Analyze what a benchmark actually measures versus assumptions people make about it

Examples: COCO dataset design, GLUE benchmark construction, SWE-bench evaluation framework, SafetyBench methodology.

## When NOT to Use
Do not use this skill for:
- Papers that only USE a dataset without describing its construction
- Purely methodological papers (even if they include evaluation)
- Papers that evaluate on benchmarks without describing benchmark design
- Survey papers that analyze existing benchmarks
- Papers about data augmentation without collection/annotation focus

---

## Extraction Template

### For Dataset Papers

#### Step 1: Collection Methodology
Extract how the raw data was gathered and organized.

```markdown
**Collection Source:** Where does the raw data come from?
**Collection Scale:** How much data was collected? By whom?
**Collection Process:**
- Sampling strategy (random, stratified, targeted)
- Data preparation steps
- Format standardization
**Scale Considerations:** Storage, accessibility, versioning
```

#### Step 2: Annotation Design
Document the human annotation or labeling process.

```markdown
**Annotation Schema:** What exactly is being annotated?
**Annotation Protocol:**
- Step-by-step instructions for annotators
- Definitions and edge cases
- Examples (prototypical and boundary cases)
**Quality Control:**
- Inter-annotator agreement metrics
- Agreement resolution procedure
- Crowd-worker vetting/training
**Annotation Cost:** Time and resource estimates
```

#### Step 3: Data Format & Specs
Extract data structure and usage specifications.

```markdown
**Data Format:** JSON/CSV/HDF5 structure
**Splits:** Train/val/test reasoning and sizes
**Metadata:** What additional information is provided?
**Access & Licensing:** How is the dataset distributed?
```

### For Benchmark Papers

#### Step 1: Task Definition
Extract what the benchmark actually measures.

```markdown
**Task Definition:** What is the benchmark asking models to do?
**Input/Output Spec:**
- Input format and constraints
- Output format and constraints
- Assumptions about model architecture or training
**Task Motivation:** Why is this task important?
**Gap from Real World:** What simplifications are made?
```

#### Step 2: Evaluation Metrics
Document metric selection and interpretation.

```markdown
**Primary Metrics:** [Metric name, formula, range]
**Why These Metrics:** What capability does each metric isolate?
**Metric Limitations:** What does each metric NOT measure?
**Secondary Metrics:** [How they provide additional insight]
**Baseline Selection:** What baselines are included and why?
```

#### Step 3: Benchmark Analysis
Extract what the benchmark reveals.

```markdown
**What It Measures:** Core capabilities tested
**What People Think It Measures:** Common misconceptions
**Failure Modes:** What types of errors does it NOT catch?
**Correlation with Real Performance:** If studied, how well does benchmark performance predict real-world success?
**Known Saturation:** Is the benchmark being saturated? What's next?
```

#### Step 4: Leaderboard Design
For competitive benchmarks, extract evaluation infrastructure.

```markdown
**Leaderboard Mechanics:** How is performance tracked?
**Submission Process:** Frequency, format, evaluation turnaround
**Evaluation Server:** How are answers checked?
**Cheating Prevention:** How is overfitting to eval set prevented?
**Reporting Standards:** What metadata must submissions include?
```

---

## Output Skill Format

Generate a new SKILL.md with:

**Frontmatter:**
```yaml
---
name: [kebab-case-dataset-or-benchmark-name]
title: [Dataset/Benchmark: {Name} Evaluation Infrastructure]
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: [verified arxiv link to source paper]
keywords: [evaluation, infrastructure, metric-selection, annotation-protocol, or data-curation]
description: Build evaluation infrastructure for {domain} by replicating {benchmark/dataset} methodology. Includes {annotation protocol OR task definition}, {quality control OR metric selection}, enabling {outcome} for {use case}.
---
```

**For Dataset Skills, include:**
1. **Collection Methodology** (1 paragraph): How raw data is gathered
2. **Annotation Protocol** (3-4 bullet points): Step-by-step labeling procedure
3. **Quality Control** (2-3 bullet points): Inter-annotator agreement and resolution
4. **Data Format** (1 paragraph): Structure and splits
5. **When to Use** (1-2 sentences): What research uses this dataset type

**For Benchmark Skills, include:**
1. **Task Definition** (1 paragraph): What the benchmark measures
2. **Evaluation Metrics** (3-5 bullet points): Metric selection rationale
3. **What It Actually Measures** (1 paragraph): Reality vs perception
4. **Baseline Strategy** (2-3 bullet points): How to select and interpret baselines
5. **When to Use** (1-2 sentences): What research questions this benchmark answers

**Length:** 150-250 lines

---

## Processing Instructions

1. **Obtain the paper:** Fetch HTML from arxiv.org/html/{arxiv_id}, fallback to PDF
2. **Classify:** Determine if this is a dataset paper (annotation focus) or benchmark paper (task/metric focus)
3. **Extract methodology:** For datasets, extract collection and annotation details. For benchmarks, extract task and metric definitions.
4. **Analyze depth:** Determine if paper provides sufficient methodological detail (some papers lack specifics)
5. **Identify gaps:** What assumptions does the benchmark/dataset make? What real-world aspects are simplified?
6. **Validate:** Confirm the paper contains original evaluation infrastructure (not just application)
7. **Generate skill:** Write output skill following the appropriate format above

---

## Quality Checks

- [ ] Paper clearly describes collection/annotation OR task/metric methodology
- [ ] Specific procedures are documented (not just high-level overview)
- [ ] Quality control or metric selection rationale is explained
- [ ] Output skill identifies what the benchmark actually measures vs common assumptions
- [ ] For datasets: annotation protocol is detailed enough to replicate
- [ ] For benchmarks: metrics are justified, not arbitrary
- [ ] Keywords (5-10) include "evaluation", "infrastructure", and domain-specific terms
- [ ] Description is under 1024 characters
- [ ] Engine tag matches skillxiv-v0.0.2-claude-opus-4.6

---

## Common Pitfalls

- **Assuming all dataset papers are extractable:** Skip papers that only distribute existing data
- **Mistaking metric innovation for benchmark innovation:** Paper may introduce a metric without designing the benchmark itself
- **Missing the gap:** If the paper doesn't explain WHY these design choices, extract them anyway with domain reasoning
- **Oversimplifying complexity:** Real annotation protocols are complex; preserve the details
- **Ignoring leaderboard design:** Leaderboard mechanics are part of the benchmark infrastructure
