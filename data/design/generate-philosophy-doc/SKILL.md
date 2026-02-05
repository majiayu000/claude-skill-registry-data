---
name: generate-philosophy-doc
description: Generate comprehensive philosophy and standards documents for any domain (UX design, landing pages, email outbound, API design, etc.). Load when user says "create philosophy doc", "generate standards for [domain]", "build best practices guide", or "create benchmarking document". Conducts deep research, synthesizes findings, and produces structured philosophy documents with principles, frameworks, anti-patterns, checklists, case studies, and metrics.
---

# Generate Philosophy Document

Create comprehensive, research-backed philosophy and standards documents for any domain.

## What This Skill Does

This skill generates high-quality philosophy documents similar to [ux-onboarding-philosophy.md](../../00-system/documentation/ux-onboarding-philosophy.md) for any domain:

- **UX & Design**: Interface design, mobile UX, accessibility standards
- **Marketing**: Landing pages, email outbound, conversion optimization
- **Technical**: API design, architecture patterns, code standards
- **Business**: Sales processes, customer success, operations

Each document includes:
1. Foundational principles (research-backed)
2. Frameworks and methodologies
3. Anti-patterns dictionary
4. Design checklists
5. Case studies with metrics
6. Measurement frameworks
7. Academic and industry references

## Workflow

### Step 1: Define the Domain

Ask the user to specify:

1. **Domain name**: "What domain do you want to document?"
   - Examples: "Landing Page Design", "API Design Standards", "Email Outbound Best Practices"

2. **Target audience**: "Who will use this document?"
   - Examples: "UX designers", "Backend developers", "Marketing team"

3. **Focus areas** (optional): "Any specific areas to emphasize?"
   - Examples: "Conversion optimization", "Performance", "Accessibility"

**Clarify scope**: Ensure domain is specific enough to be actionable but broad enough to be useful.

---

### Step 2: Conduct Research

Use the WebSearch tool or Perplexity API to gather comprehensive research:

**Research Strategy**:

1. **Foundational Research** (principles and theory):
   - Search: "[domain] fundamental principles"
   - Search: "[domain] research studies"
   - Search: "[domain] psychology" or "[domain] user behavior"

2. **Framework Research** (methodologies):
   - Search: "[domain] frameworks"
   - Search: "[domain] best practices methodology"
   - Search: "[domain] process workflow"

3. **Anti-Pattern Research** (common mistakes):
   - Search: "[domain] common mistakes"
   - Search: "[domain] anti-patterns"
   - Search: "worst [domain] practices"

4. **Metrics Research** (measurement):
   - Search: "[domain] KPIs metrics"
   - Search: "[domain] benchmarking"
   - Search: "[domain] success metrics"

5. **Case Study Research** (real examples):
   - Search: "[domain] case studies"
   - Search: "[domain] before after"
   - Search: "[domain] success stories"

6. **Academic Research** (credible sources):
   - Search: "[domain] academic research"
   - Search: "[domain] peer reviewed studies"

**Execute 10-15 targeted searches** covering all research areas. Synthesize findings into structured notes organized by section.

**Optional**: Use `scripts/research_topic.py` to generate search queries:
```bash
python scripts/research_topic.py "Landing Page Design" "principles,frameworks,anti-patterns,metrics"
```

---

### Step 3: Generate Document Structure

Use the bundled template to create the document structure:

**Option A: Manual Creation**

Copy [assets/philosophy-template.md](assets/philosophy-template.md) and fill in sections with research findings.

**Option B: Script-Assisted**

```bash
python scripts/generate_structure.py "Landing Page Design" > output.md
```

Then fill in placeholders with researched content.

---

### Step 4: Fill in Sections

Work through each section systematically. See [references/document-template.md](references/document-template.md) for detailed guidance on each section.

#### 4.1 Executive Summary

- **Core philosophy**: Distill into 1 sentence
- **The problem**: What challenge does this solve?
- **The solution**: What approach does this recommend?
- **Proof**: Cite key research or metrics

**Length**: 100-200 words

---

#### 4.2 Foundational Principles

Create 5-8 principles. Each principle needs:

1. **Name**: Concise and memorable (e.g., "Mobile-First Design")
2. **Definition**: Clear 1-sentence explanation
3. **Why This Works**: Research-backed rationale
4. **Application**: Wrong vs. Right examples (concrete)
5. **Test**: How to verify adherence

**Format Pattern**:
```markdown
### Principle 1: [Name]

**Definition**: [One sentence]

**Why This Works**: [Research explanation with citation]

**Application**:
- WRONG: [Concrete bad example]
- RIGHT: [Concrete good example]

**Test**: [Verification method]
```

**Quality Check**:
- Examples must be concrete (not abstract)
- Research must be cited
- Tests must be practical

**Length**: 400-800 words total (80-160 per principle)

---

#### 4.3 Framework & Methodology

Create a named framework (e.g., "LIFT Framework", "AIDA Model"):

1. **Framework name**: Memorable and descriptive
2. **Visual diagram**: ASCII art or description
3. **3-5 phases**: Sequential steps
4. **Each phase includes**:
   - Purpose statement
   - Key activities (3-5 items)
   - Quality checklist (3-5 checkboxes)
   - Time budget (percentage)

**Example Structure**:
```markdown
### The CLEAR Framework

[ASCII diagram showing 5 phases]

#### Phase 1: Capture Attention

**Purpose**: Hook user in first 3 seconds

**Key Activities**:
- Design hero section with compelling headline
- Use high-contrast CTA button
- Optimize above-fold content

**Quality Checklist**:
- [ ] Headline clearly states value proposition
- [ ] CTA visible without scrolling
- [ ] Hero image supports message

**Time Budget**: 20% of design process
```

**Length**: 400-600 words

---

#### 4.4 Anti-Patterns Dictionary

Document 5-10 common mistakes:

1. **Name**: Memorable (e.g., "The Wall of Text")
2. **Symptom**: How to recognize
3. **Example**: Concrete wrong example
4. **Why It Fails**: Explanation with data
5. **Fix**: How to correct
6. **Metrics**: Impact data (if available)

**Format**:
```markdown
### Anti-Pattern 1: "The Wall of Text"

**Symptom**: Landing page with 500+ words above fold, no visual breaks

**Example**:
WRONG:
[Paste or describe actual bad example]

**Why It Fails**: Users scan, don't read. Average time on page: 8 seconds.
Wall of text = 90% bounce rate (Source: Nielsen Norman Group)

**Fix**: Break into scannable sections with headers, bullets, and whitespace

**Metrics**: Before: 90% bounce | After: 45% bounce (50% improvement)
```

**Length**: 400-600 words total (60-80 per anti-pattern)

---

#### 4.5 Design Checklists

Create 3 checklists:

1. **Pre-Design Checklist**: Before starting work
2. **Mid-Design Checklist**: During execution
3. **Post-Design Checklist**: Before launch

**Format**:
```markdown
### Pre-Design Checklist

**Define Success Criteria**:
- [ ] Primary conversion goal defined
- [ ] Target audience identified
- [ ] Success metrics established

**Audience Analysis**:
- [ ] User personas documented
- [ ] Pain points identified
- [ ] Value proposition clear
```

**Quality Standards**:
- All items binary (yes/no)
- Specific and measurable
- No ambiguous language
- 3-5 items per category
- Can complete in <10 minutes

**Length**: 200-400 words

---

#### 4.6 Case Studies

Include 2-3 real examples:

1. **Context**: Background and situation
2. **Challenge**: Problem to solve
3. **Approach**: How principles were applied
4. **Before metrics**: Quantified starting point
5. **After metrics**: Quantified results
6. **Improvement**: Percentage gains
7. **Key insights**: Learnings (3-5 bullets)

**Example**:
```markdown
### Case Study: Dropbox Homepage Redesign

**Context**: Dropbox needed to improve conversion on homepage (2017)

**Challenge**: 65% bounce rate, unclear value proposition

**Approach**: Applied "Show Don't Tell" principle - replaced feature list
with video demo showing product in action

**Before**:
- Bounce Rate: 65%
- Sign-up Conversion: 2.8%
- Time on Page: 12 seconds

**After**:
- Bounce Rate: 42% (35% improvement)
- Sign-up Conversion: 4.2% (50% improvement)
- Time on Page: 48 seconds (300% improvement)

**Key Insights**:
- Video demo increased engagement 4x
- Visual demonstration beats text explanation
- Clear CTA after video critical for conversion
```

**Length**: 300-500 words total (150-250 per case study)

---

#### 4.7 Measurement Framework

Create tiered metrics structure:

1. **Tier 1**: Critical metrics (make-or-break)
2. **Tier 2**: Important metrics (quality indicators)
3. **Tier 3**: Nice-to-have metrics (optimization)
4. **Red flags**: When to take immediate action
5. **Measurement methods**: How to collect data

**Format**:
```markdown
### Success Metrics Hierarchy

TIER 1: CRITICAL METRICS (Make or Break)
  - Conversion Rate: Primary goal completion
    Target: >5% | Baseline: 2-3%

  - Bounce Rate: User engagement
    Target: <40% | Baseline: 50-60%

### Red Flags

CRITICAL RED FLAGS:

1. Conversion Rate < 2%
   -> Poor value proposition - Redesign messaging

2. Bounce Rate > 70%
   -> No engagement - Rethink content strategy
```

**Length**: 300-400 words

---

#### 4.8 Research References

Organize sources by category:

1. **Academic Sources**: Peer-reviewed research
2. **Industry Research**: Authoritative reports
3. **Best Practice Documentation**: Standards and guides

**Format**:
```markdown
### Academic Sources

1. **Cognitive Psychology**:
   - Nielsen, J. (2006). "F-Shaped Pattern For Reading Web Content"
   - Kahneman, D. (2011). "Thinking, Fast and Slow"

### Industry Research

1. **ConversionXL**: Landing page optimization studies
2. **Baymard Institute**: UX research and benchmarks
```

**Quality Standards**:
- Sources are authoritative
- Citations are complete
- Mix of academic and practical
- Recent (within 5-10 years preferred)

**Length**: 100-200 words

---

### Step 5: Quality Validation

Use [references/quality-checklist.md](references/quality-checklist.md) to validate the document:

**Critical Checks**:
- [ ] All 8 core sections present
- [ ] No placeholder text remains ([TODO], [PLACEHOLDER])
- [ ] 5-8 principles included
- [ ] 5-10 anti-patterns documented
- [ ] 2-3 case studies with metrics
- [ ] Research references cited
- [ ] Total length: 1,500-3,000 words

**Content Quality**:
- [ ] Examples are concrete (not abstract)
- [ ] Research is cited properly
- [ ] Metrics are specific
- [ ] Checklists are actionable
- [ ] Language is clear and professional

**Formatting Quality**:
- [ ] Markdown formatting correct
- [ ] Links work (TOC, cross-references)
- [ ] Headers hierarchical
- [ ] Visual hierarchy clear

**Target Grade**: B (80%+) minimum, A (90%+) recommended

---

### Step 6: Iterate and Refine

After initial draft:

1. **Read full document** - Check flow and coherence
2. **Validate against checklist** - Ensure quality standards met
3. **Test with target audience** (if possible) - Get feedback
4. **Refine based on feedback** - Make improvements
5. **Final proofread** - Catch typos and errors

**Common Refinements**:
- Strengthen weak examples with more concrete details
- Add missing citations
- Improve clarity of complex explanations
- Enhance visual hierarchy with better formatting
- Cut redundant content

---

### Step 7: Deliver Document

**Output Format Options**:

1. **Standalone File**: Save as `[domain]-philosophy.md` in appropriate location
2. **System Documentation**: Place in `00-system/documentation/` if system-wide
3. **Project Documentation**: Place in project folder if project-specific
4. **External Sharing**: Package with any additional context needed

**Delivery Includes**:
- Complete philosophy document
- Brief usage guide (how to apply)
- Quality checklist for future updates
- Recommendation for review timeline

---

## Tips for Success

### Research Quality

**Do**:
- Search multiple sources (10-15 queries minimum)
- Prioritize authoritative sources (academic, industry leaders)
- Look for quantified data and metrics
- Find real case studies with numbers
- Cross-reference claims across sources

**Don't**:
- Rely on single source
- Accept claims without evidence
- Use outdated research (>10 years old) without noting
- Include speculation without labeling it
- Cite non-authoritative sources

---

### Writing Quality

**Do**:
- Use concrete examples (not abstract)
- Quantify whenever possible (X% improvement)
- Write in clear, professional tone
- Format for scannability (headers, lists, emphasis)
- Connect principles to research

**Don't**:
- Use jargon without definition
- Write long paragraphs (>4-5 lines)
- Make unsupported claims
- Use vague language ("might", "could", "maybe")
- Copy-paste without synthesis

---

### Common Pitfalls

1. **Too Broad**: Domain too general to be actionable
   - Fix: Narrow scope to specific subdomain

2. **Too Shallow**: Research insufficient for depth
   - Fix: Conduct more targeted searches, find academic sources

3. **No Metrics**: Principles lack quantified support
   - Fix: Search for benchmarking data, case study metrics

4. **Abstract Examples**: Examples too generic to be useful
   - Fix: Use real scenarios, specific companies/products

5. **Incomplete Sections**: Missing key components
   - Fix: Use quality checklist, ensure all sections complete

---

## Example Domains

**UX & Design**:
- Mobile App UX Design Philosophy
- Accessibility Standards Guide
- Visual Hierarchy Best Practices
- Micro-interaction Design Standards

**Marketing**:
- Landing Page Conversion Optimization
- Email Outbound Best Practices
- Cold Outreach Philosophy
- Content Marketing Standards

**Technical**:
- REST API Design Principles
- Microservices Architecture Standards
- Database Schema Design Philosophy
- Code Review Best Practices

**Business**:
- Sales Discovery Process Standards
- Customer Onboarding Philosophy
- Product Roadmap Planning Guide
- Remote Team Management Principles

---

## References

**Skill Resources**:
- [document-template.md](references/document-template.md) - Detailed section guidelines
- [quality-checklist.md](references/quality-checklist.md) - Validation checklist
- [philosophy-template.md](assets/philosophy-template.md) - Blank template

**Example Philosophy Document**:
- [ux-onboarding-philosophy.md](../../00-system/documentation/ux-onboarding-philosophy.md) - Reference example

**Scripts**:
- `scripts/research_topic.py` - Generate research queries
- `scripts/generate_structure.py` - Generate document structure

---

## Success Criteria

A successful philosophy document:

1. **Comprehensive**: Covers all 8 core sections with depth
2. **Research-Backed**: Claims supported by citations and data
3. **Actionable**: Readers can apply principles immediately
4. **Professional**: Publication-ready quality
5. **Measurable**: Success metrics clearly defined
6. **Validated**: Passes quality checklist (80%+ grade)

Target: Create documents that become authoritative references for the domain.
