---
name: paper2skill-application-transfer
description: "Convert arXiv papers that apply ML techniques to real-world domains into application-transfer skills. Extracts problem formulation, domain adaptation gaps, and deployment recipes. Use this skill when extracting skills from Category 1 (Application Transfer) papers — papers about AlphaFold-style domain applications, robotics deployment, interdisciplinary ML crossings, or any paper where the novelty is in what was solved rather than the method itself."
---

## When to Use
Apply this skill when you encounter arXiv papers that:
- Take an established ML method (transformer, reinforcement learning, diffusion, etc.) and apply it to a new domain
- Address real-world deployment challenges or domain-specific constraints
- Cross disciplinary boundaries (e.g., vision model applied to robotics, NLP technique applied to biology)
- Describe adaptation or modification of existing techniques to fit problem requirements
- Include lessons learned from deploying research to production

Examples: AlphaFold applying attention to protein structure, quadrupedal locomotion adapting RL to embodied agents, BLIP adapting vision-language models to multimodal tasks.

## When NOT to Use
Do not use this skill for:
- Pure methodological papers (novel architectures or algorithms without domain application)
- Purely exploratory papers (analyzing what works without solving a specific domain problem)
- Survey or review papers
- Papers that only benchmark existing methods
- Papers without clear domain-specific adaptation or constraints

---

## Extraction Template

### Step 1: Identify the Domain Problem
Extract what real-world or domain-specific problem the paper solves and why it matters.

```markdown
**Domain Problem:** What specific problem is being solved? Why is it important?
**Domain Context:** What makes this problem different from standard benchmarks?
**Existing Approaches:** What was the baseline approach before this work?
```

### Step 2: Analyze the Gap
Identify what existing methods lack and why naive application fails.

```markdown
**The Gap:** What specific limitations did existing methods have for this domain?
**Why It Matters:** How does this gap translate to real-world failure modes?
**Domain Constraints:** What domain-specific constraints forced adaptation?
- Hardware/computational limits
- Data availability or annotation cost
- Real-time requirements
- Physical/safety constraints
```

### Step 3: Extract the Source Method
Document the foundational technique being adapted.

```markdown
**Source Technique:** What is the core ML method (architecture, loss, training procedure)?
**Original Context:** Where did this method originate and what was it designed for?
**Key Properties:** What properties make it suitable for adaptation to this domain?
```

### Step 4: Extract Adaptation Decisions
Map the specific modifications made to fit the domain.

```markdown
**Key Adaptations:**
1. [Specific change]: Why this change was necessary
2. [Specific change]: Why this change was necessary
3. [Specific change]: Why this change was necessary

**Why These Work:** How do these adaptations address the domain gap?
```

### Step 5: Create the Adaptation Recipe
Synthesize a reusable template for similar transfers.

```markdown
**Recipe for Domain Transfer:**
1. Identify source technique that has property X, Y, Z
2. Analyze your domain problem for constraint A, B, C
3. Map constraints to required modifications:
   - For constraint A, modify [component]
   - For constraint B, modify [component]
4. Validate with domain-specific metrics
5. Deploy with [deployment considerations]
```

### Step 6: Extract Deployment Lessons
Document practical insights for real-world use.

```markdown
**Deployment Considerations:**
- Data pipeline: [how to prepare domain data]
- Integration points: [where the method fits in larger systems]
- Failure modes: [what goes wrong and how to detect it]
- Scaling considerations: [production deployment constraints]
- Monitoring: [metrics that indicate healthy operation]
```

---

## Output Skill Format

Generate a new SKILL.md with:

**Frontmatter:**
```yaml
---
name: [kebab-case-domain-method]
title: [Domain Transfer: Adapting {Method} to {Domain}]
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: [verified arxiv link to source paper]
keywords: [domain, method, constraint1, constraint2, outcome]
description: Apply {Method} to {Domain} by bridging the gap between {original context} and {domain requirements}. Focuses on {key adaptation}, enabling {outcome} when solving {problem class}.
---
```

**Content structure:**
1. **Domain Problem** (1 paragraph): What is being solved and why
2. **The Gap** (1 paragraph): Why existing methods don't work
3. **Source Technique** (1 paragraph): The foundational method
4. **Adaptation Recipe** (5-8 bullet points): Step-by-step how to port the method
5. **Deployment Guide** (3-4 bullet points): Production considerations
6. **When to Use** (1-2 sentences): Domain applicability
7. **When NOT to Use** (1-2 sentences): Boundary conditions

**Length:** 150-250 lines including code examples (if applicable)

---

## Processing Instructions

1. **Obtain the paper:** Fetch HTML from arxiv.org/html/{arxiv_id}, fallback to PDF
2. **Identify domain:** Extract the problem domain from abstract and introduction
3. **Find the source method:** Locate which existing technique is being adapted
4. **Map adaptations:** For each modification, determine what domain constraint required it
5. **Synthesize recipe:** Generalize the adaptation pattern to teach domain transfer
6. **Validate:** Confirm the paper contains real domain-specific adaptation (not just application)
7. **Generate skill:** Write output skill following the format above

---

## Quality Checks

- [ ] Paper clearly identifies a source technique and domain target
- [ ] Gap analysis explains why naive application would fail
- [ ] Specific adaptations are traceable to domain constraints
- [ ] Recipe is general enough to apply to similar domains
- [ ] Deployment section addresses production realities
- [ ] Output skill description is under 1024 characters
- [ ] Keywords (5-10) reflect both domain and method
- [ ] Engine tag matches skillxiv-v0.0.2-claude-opus-4.6
