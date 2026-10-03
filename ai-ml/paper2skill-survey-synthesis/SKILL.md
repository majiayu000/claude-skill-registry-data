---
name: paper2skill-survey-synthesis
description: "Convert survey and synthesis papers into field navigation guides. Extracts taxonomies, method selection decision trees, literature navigation heuristics, and open problems. Use this skill when extracting skills from Category 10 (Survey and Synthesis) papers — comprehensive reviews, position papers, tutorials, or roadmaps that organize a research landscape."
---

## When to Use

Apply this skill when you encounter arXiv papers that:
- Provide a comprehensive review of a field with explicit taxonomy or organization scheme (surveys of LLMs, transformers, diffusion models, reinforcement learning)
- Present a new perspective or position on existing research directions (position papers on safety, interpretability, scalability)
- Teach a research methodology through structured walkthrough (tutorials on prompt engineering, training techniques, evaluation)
- Articulate research roadmaps or community consensus on open problems (future of AI, scaling paradigms, unsolved challenges in NLP)
- Compare and contrast multiple approaches to the same problem with decision criteria
- Discuss why certain design choices succeeded or failed across a research lineage

Examples: "A Survey of Large Language Models", "Attention is All You Need" (foundational review sections), "Challenges and Opportunities in Open-Ended Learning", roadmap papers from conferences or workshops.

## When NOT to Use

Do not use this skill for:
- Papers that implement a single technique with minimal comparative analysis
- Purely experimental papers (even comprehensive ones) without conceptual synthesis
- Literature reviews that are just lists of papers without organization or taxonomy
- Papers that discuss existing methods but don't help readers navigate or choose between them
- Narrow domain papers that only survey variations of one specific approach
- Papers without clear structure, decision points, or organizing principles

---

## Extraction Template

### For Comprehensive Surveys

#### Step 1: Field Definition & Scope
Extract what the survey bounds and covers.

```markdown
**Field/Topic:** What research area is being surveyed?
**Scope Boundaries:** What is IN scope? What is OUT of scope?
**Temporal Coverage:** When was this field established? What time period does the survey cover?
**Key Assumption:** What foundational concept unites this field?
**Motivation:** Why survey this now? What triggered the need for synthesis?
```

#### Step 2: Taxonomy Construction
Document the organizing principle the survey uses.

```markdown
**Top-Level Categories:** What are the main buckets for organizing research?
**Organizing Principle:** Is it grouped by problem, solution, time, application, or some other dimension?
**Decision Points:** What factors determine which category a paper falls into?
**Key Distinctions:** What are the critical differences between categories?
**Relationship Map:** How do categories relate to each other? Orthogonal? Hierarchical? Overlapping?
```

#### Step 3: Method Comparison Matrix
Extract decision criteria for choosing between approaches.

```markdown
**Method A:** [name, core idea, when to use, pros, cons, required resources]
**Method B:** [name, core idea, when to use, pros, cons, required resources]
**Method C:** [name, core idea, when to use, pros, cons, required resources]
**Decision Criteria:** What factors determine which method is best?
**Common Pitfalls:** What mistakes do practitioners make when choosing between methods?
```

#### Step 4: Literature Navigation
Extract heuristics for reading the field strategically.

```markdown
**Essential Foundation Papers:** Must-read foundational works to understand the field
**Landmark Shifts:** Papers that changed how the field thinks
**Domain-Specific Tracks:** Different research threads within the field (e.g., scaling track, alignment track, efficiency track)
**For Practitioners:** Key papers if you're implementing something in this domain
**For Theorists:** Key papers if you're advancing fundamental understanding
```

#### Step 5: Open Problems & Research Directions
Document unresolved questions and suggested next steps.

```markdown
**Identified Gaps:** What does current research NOT address?
**Open Questions:** Specific unsolved problems the survey identifies
**Scaling Frontiers:** How should the field scale in future? (scale, compute, data, human effort)
**Bottlenecks:** What is preventing progress on key challenges?
**Suggested Directions:** What research avenues does the survey recommend?
```

### For Position Papers

#### Step 1: Core Thesis
Extract the argued perspective.

```markdown
**Central Claim:** What is the paper arguing?
**Target Audience:** Who needs to hear this argument? (researchers, practitioners, policymakers)
**Problem Statement:** What is the status quo getting wrong?
**Proposed Direction:** What should the field do instead?
```

#### Step 2: Evidence Structure
Document how the argument is supported.

```markdown
**Key Evidence:** What empirical or conceptual evidence supports the thesis?
**Counterarguments:** What objections might be raised? How does the paper address them?
**Analogies & Examples:** What real-world cases demonstrate the thesis?
**Failure Case:** What would disprove the thesis?
```

#### Step 3: Implementation Implications
Extract what changes if the position is adopted.

```markdown
**If Right:** How should research directions change?
**If Wrong:** What would we learn from the contradiction?
**Research Priorities:** What work becomes more important if this position is true?
**Evaluation Strategy:** How should the community test this position?
```

### For Tutorials & Pedagogical Papers

#### Step 1: Learning Progression
Extract the teaching structure.

```markdown
**Prerequisite Knowledge:** What must readers know first?
**Pedagogical Order:** In what sequence are concepts introduced?
**Key Inflection Points:** Where does understanding suddenly click?
**Common Misconceptions:** What do learners typically misunderstand?
```

#### Step 2: Worked Examples
Document the teaching methodology.

```markdown
**Simplest Case:** Minimal example showing the core idea
**Elaborated Case:** Medium-complexity example with important variations
**Edge Case:** Complex example revealing limitations or subtleties
**Anti-pattern:** Example of what NOT to do and why
```

#### Step 3: Practice Guidance
Extract learning scaffolding.

```markdown
**Concept Checks:** Self-test questions at each stage
**Implementation Milestones:** Checkpoints for hands-on practice
**Common Errors & Debugging:** What goes wrong during practice and how to fix it
**Next Steps:** How to extend understanding beyond the tutorial
```

### For Research Roadmaps

#### Step 1: Current State Assessment
Document what has been achieved.

```markdown
**Accomplished:** What has the field solved well?
**Mature Techniques:** What approaches have been thoroughly validated?
**Standard Benchmarks:** What evaluation practices are established?
**Known Tradeoffs:** What design choices are well-understood?
```

#### Step 2: Barriers & Bottlenecks
Extract what is preventing progress.

```markdown
**Technical Bottlenecks:** What fundamental limits are known? (e.g., scaling limits, memory constraints)
**Resource Constraints:** What bottlenecks are resource-dependent? (compute, data, human effort)
**Conceptual Gaps:** What fundamental understanding is missing?
**Measurement Challenges:** What is hard to measure or evaluate?
```

#### Step 3: Proposed Next Frontiers
Document the suggested research path forward.

```markdown
**Near-term (1-2 years):** What should the field tackle immediately?
**Medium-term (3-5 years):** What are the next big goals?
**Long-term (5+ years):** What are moonshot ambitious directions?
**Key Milestones:** How will we know we are making progress?
**Required Investments:** What resources (compute, data, talent) are needed?
```

---

## Output Skill Format

Generate a new SKILL.md with the following structure:

**Frontmatter:**
```yaml
---
name: [kebab-case-field-or-topic-name]
title: [Survey/Position/Roadmap: {Title} — Field Guide]
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: [verified arxiv link to source paper]
keywords: [taxonomy, survey, research-directions, field-navigation, or domain-specific terms]
description: Navigate {field/topic} by understanding {taxonomy/position/roadmap}. Extracts {taxonomy structure OR decision tree OR open problems}, enabling practitioners to {choose approaches OR understand landscape OR guide next research}. Use when selecting methods in {field}, understanding how {domain} has evolved, identifying unresolved challenges, or planning research directions.
---
```

**Skill Body Structure:**

1. **Field Overview** (1 paragraph): What is the scope, timeline, and unifying concept?
2. **Taxonomy or Organizing Principle** (1-2 paragraphs + visual text-based breakdown): How is the field organized? What are the main categories?
3. **Method Comparison or Position Framework** (3-5 bullet points): Key decision criteria for choosing between approaches OR core thesis and implications
4. **Literature Navigation or Learning Path** (3-5 bullet points): Essential papers, conceptual tracks, or learning progression
5. **Open Questions & Research Directions** (1 paragraph + 4-6 bullet points): What does the field need next?
6. **When to Use This Skill** (1-2 sentences): What research or decision-making scenarios apply this framework?

**Length:** 150-250 lines

---

## Processing Instructions

1. **Identify paper type:** Determine if this is a comprehensive survey, position paper, tutorial, or roadmap
2. **Obtain the paper:** Fetch HTML from arxiv.org/html/{arxiv_id}, fallback to PDF
3. **Extract taxonomy:** For surveys, identify the organizing principle and major categories
4. **Map decision points:** What factors determine how papers or methods are grouped?
5. **Identify open problems:** What does the paper identify as unresolved questions?
6. **Extract literature heuristics:** What papers should practitioners know? In what order?
7. **Build field guide:** Synthesize the extraction into a practical navigation tool
8. **Validate comprehensiveness:** Confirm the output skill helps practitioners or researchers navigate the field

---

## Quality Checks

- [ ] Paper is clearly a survey, position paper, tutorial, or roadmap (not a single-technique paper)
- [ ] Taxonomy or organizing principle is explicit and can be explained in 2-3 sentences
- [ ] Decision criteria for method selection are identifiable
- [ ] At least 3-5 open questions or future research directions are extracted
- [ ] Literature navigation heuristics help readers prioritize what to read
- [ ] For tutorials: learning progression and common misconceptions are documented
- [ ] For position papers: thesis and counterarguments are clear
- [ ] For roadmaps: current achievements, bottlenecks, and next steps are distinguished
- [ ] Output skill functions as a field guide/decision tree, not a summary
- [ ] Keywords (5-10) include domain terms and "survey", "taxonomy", "navigation", or "directions"
- [ ] Description is under 1024 characters
- [ ] Engine tag matches skillxiv-v0.0.2-claude-opus-4.6

---

## Common Pitfalls

- **Mistaking a single-technique paper for a survey:** Papers with "survey" in the title may still focus on one method. Check if it truly compares multiple approaches and provides a taxonomy.
- **Extracting raw paper lists instead of structure:** A skill should teach HOW to navigate the field, not just list all papers. Focus on organizing principles and decision criteria.
- **Missing the conceptual synthesis:** The valuable part of surveys is the organizing principle. Don't just paraphrase paper titles — extract the taxonomy that explains them.
- **Ignoring open problems:** The most useful part of a survey is often what it says the field still needs to solve. Prioritize this section.
- **Treating tutorials as data transfer:** A good tutorial skill extracts the pedagogical order and common misconceptions, not just the technical content.
- **Ignoring position/perspective:** Position papers are valuable specifically because they argue a perspective. Capture the thesis and evidence, not just the content.
- **Missing decision heuristics:** For practitioners, the most useful extraction is: given these constraints/goals, which approach should I use?
