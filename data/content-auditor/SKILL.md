---
name: content-auditor
description: This skill should be used when users need to evaluate course content, workshop materials, or training programs against a set of evaluation criteria (such as ICP-BAF learning outcomes). The skill audits content comprehensively, identifies gaps, and provides actionable recommendations.
---

# Content Auditor Skill

## Purpose

Systematically evaluate educational content (courses, workshops, training materials) against predefined evaluation criteria. The skill analyzes content artifacts, identifies where criteria are met or missing, and generates an annotated evaluation report with evidence and recommendations.

## When to Use This Skill

Use this skill when:
- Evaluating course content against certification standards (e.g., ICP-BAF, ICP-ACC)
- Auditing workshop materials for completeness against learning outcomes
- Assessing training programs for compliance with frameworks
- Identifying gaps in curriculum coverage
- Generating evidence-based evaluation reports for stakeholders

## Core Capabilities

### 1. Multi-Artifact Content Analysis

Analyze diverse content types:
- Slide decks (Slidev, PowerPoint, Keynote)
- Facilitator scripts and guides
- Workshop plans and constitutions
- Specifications and task lists
- Student materials and handouts
- Assessment instruments

### 2. Criteria-Based Evaluation

Support multiple evaluation criteria formats:
- YAML-based rubrics (primary format)
- JSON-based criteria
- Markdown checklists
- Custom evaluation frameworks

### 3. Evidence Mapping

For each criterion:
- Search content for evidence of coverage
- Extract specific quotes/references (with file:line citations)
- Assess depth of coverage (Awareness / Working Knowledge / Mastery)
- Identify partial vs. complete coverage
- Flag gaps and missing elements

### 4. Gap Analysis & Recommendations

For missing or partial coverage:
- Suggest specific content to add
- Reference similar patterns from existing content
- Recommend artifacts to create (slides, exercises, assessments)
- Prioritize gaps (Critical / Important / Nice-to-have)
- Estimate effort to close gaps

### 5. Annotated Report Generation

Generate comprehensive audit reports:
- Original criteria with `where_the_course_covers` field populated
- Evidence citations with file paths and line numbers
- Coverage percentages and statistics
- Gap analysis summary
- Actionable recommendations
- YAML output format (preserves original structure)

---

## Workflow

### Stage 1: Gather Inputs

Ask clarifying questions to understand the audit scope:

1. **Evaluation Criteria Source**
   - "Where is your evaluation criteria file? (YAML, JSON, or other format)"
   - "What framework are you evaluating against? (e.g., ICP-BAF, ICP-ACC, custom)"

2. **Content to Audit**
   - "What content should I audit? (specific files, directories, or patterns)"
   - "Should I include all artifacts (slides, scripts, plans, etc.) or specific types?"

3. **Audit Depth**
   - "What level of rigor? (Quick scan / Standard / Deep dive)"
     - Quick scan: Check for presence/absence only
     - Standard: Assess depth + provide quotes
     - Deep dive: Full analysis + gap recommendations

4. **Output Format**
   - "Do you want the annotated YAML file, or also a summary report?"
   - "Should I include recommendations for closing gaps?"

### Stage 2: Load and Parse Criteria

**Action**: Read the evaluation criteria file

**YAML Criteria Format** (Standard):
```yaml
- evaluation:
    expectation: "What participants should be able to do"
    purpose: "Why this learning outcome matters"
    context: "Background/setting for the learning outcome"
    learning_outcome: "1.1.1. Specific LO Number and Name"
    where_the_course_covers: ""  # <-- FILL THIS IN
```

**Parsing Strategy**:
- Extract all `evaluation` items into a list
- For each item, note:
  - `learning_outcome` (the criterion ID/name)
  - `expectation` (what to look for in content)
  - `where_the_course_covers` (initially empty—to be populated)

### Stage 3: Discover Content Artifacts

**Action**: Identify all content files to audit

**Search Patterns** (use Glob tool):
- Slide decks: `**/*.md` (Slidev), `**/*.pptx`, `**/*.key`
- Scripts: `**/facilitator-script.md`, `**/module*-script.md`
- Plans: `**/plan.md`, `**/specification.md`, `**/constitution.md`
- Tasks: `**/tasks.md`
- Other: `**/README.md`, `**/handouts/*.md`

**Cataloging**:
- Create a list of all discovered files
- For each file, note:
  - File path
  - File type (slide deck, script, plan, etc.)
  - Estimated purpose (Module 1 slides, Module 2 script, etc.)

### Stage 4: Content Analysis (Criterion-by-Criterion)

For each evaluation criterion:

#### 4.1 Extract Search Keywords

From the `expectation` field, extract key concepts to search for:

**Example**:
```yaml
expectation: "Demonstrate high-performance questions. Participants should have the opportunity to practice using these techniques in a safe environment."
```

**Keywords**: `high-performance questions`, `HPQ`, `practice`, `techniques`

#### 4.2 Search Content Artifacts

Use Grep tool to search for keywords across all content files:

```bash
# Example grep searches
grep -i "high-performance questions" **/*.md
grep -i "HPQ" **/*.md
grep -i "evidence-seeking" **/*.md  # Related concept
```

**Record**:
- File paths where keywords found
- Line numbers
- Surrounding context (±3 lines)

#### 4.3 Assess Coverage Depth

For each match found, assess depth:

**Levels**:
- **Awareness** (Mentioned): Criterion mentioned but not explained
  - Example: "We'll cover HPQs in Module 4"
- **Working Knowledge** (Explained + Example): Criterion explained with examples
  - Example: Slide showing 4 HPQ categories with examples
- **Mastery** (Practice + Assessment): Includes hands-on practice and assessment
  - Example: Participants practice HPQs + facilitator evaluates quality

**Coverage Assessment**:
- No coverage: 0%
- Awareness only: 33%
- Working knowledge: 66%
- Mastery (practice + assessment): 100%

#### 4.4 Extract Evidence

For coverage ≥33%, extract specific evidence:

**Evidence Format**:
```
Module 4 (1:05-1:40): HPQ Round (Slide 14, module4-facilitator-script.md:132-135)
- Participants practice 4 HPQ types: Evidence-seeking, Assumption-testing, Boundary-probing, Reflection-prompting
- Chat exercise: "What evidence would change your mind?" (90 seconds)
- Facilitator highlights 2-3 strong HPQ examples from chat

Coverage: 66% (Working Knowledge - explained + practiced, but no formal assessment)
```

#### 4.5 Identify Gaps (Coverage <100%)

For partial or missing coverage, identify specific gaps:

**Gap Categories**:
- **Mention Only** (33%): No explanation or examples provided
- **No Practice** (66%): Explained but no hands-on activity
- **No Assessment** (66-100%): Practice exists but no quality check or rubric
- **Missing Entirely** (0%): No evidence found

**Recommendations**:
- Suggest specific content to add (slides, exercises, assessment rubrics)
- Reference similar existing content as a template
- Estimate effort (minutes to create)

### Stage 5: Populate `where_the_course_covers` Field

For each criterion, fill in the `where_the_course_covers` field:

**If Coverage ≥33%**:
```yaml
where_the_course_covers: |
  Module 4 (1:05-1:40): HPQ Round
  - **Evidence**: Slide 14 (module4-facilitator-script.md:132-135)
  - **Practice**: Participants type HPQ responses in chat (90 sec exercise)
  - **Depth**: Working Knowledge (66%) - Explained + practiced, but no formal assessment rubric
  - **Gap**: Add HPQ quality rubric to assess participant responses (Acceptable vs. Stretch)
```

**If Coverage = 0%**:
```yaml
where_the_course_covers: |
  **NOT COVERED** ❌
  - **Gap**: No content found for "Design Thinking Approaches" (LO 3.1.3)
  - **Recommendation**: Add 10-minute Module 2.5 segment:
    - Slide: Design Thinking 5 Steps (Empathize, Define, Ideate, Prototype, Test)
    - Activity: Participants sketch one customer journey map for their initiative (Empathize step)
    - Reference: Use Module 1 O-I-S exercise as template structure
  - **Effort**: ~30 minutes (1 slide + 1 facilitator script section + Miro template)
```

### Stage 6: Generate Coverage Statistics

Calculate overall coverage metrics:

**Metrics**:
- Total criteria: `X`
- Fully covered (100%): `Y` (`Y/X %`)
- Partially covered (33-99%): `Z` (`Z/X %`)
- Not covered (0%): `W` (`W/X %`)
- Average coverage: `(sum of all coverage %) / X`

**Breakdown by Category** (if applicable):
- Group criteria by `learning_outcome` prefix (e.g., "1.1.", "1.2.", "2.1.")
- Calculate coverage % for each category
- Identify weakest categories for prioritization

### Stage 7: Generate Annotated Output

**Primary Output**: YAML file with populated `where_the_course_covers` fields

**File Structure**:
```yaml
# Content Audit Report
# Generated: 2025-11-09
# Course: 120-Minute Business Agility Primer
# Framework: ICP-BAF (ICAgile Business Agility Foundations)
#
# Coverage Summary:
# - Total Criteria: 31
# - Fully Covered (100%): 8 (26%)
# - Partially Covered (33-99%): 18 (58%)
# - Not Covered (0%): 5 (16%)
# - Average Coverage: 64%

- evaluation:
    expectation: "Demonstrate high-performance questions..."
    purpose: "To define high-performance questions..."
    context: "High Performance Questions are an effective tool..."
    learning_outcome: "2.2.1. Ask vs. Tell: High-Performance Questions"
    where_the_course_covers: |
      Module 4 (1:05-1:40): HPQ Round
      - **Evidence**: Slide 14 + Facilitator Script (lines 132-170)
      - **Practice**: Chat exercise (90 sec), participants answer "What evidence would change your mind?"
      - **Depth**: Working Knowledge (66%)
      - **Gap**: Add HPQ rubric to assess quality (Acceptable: Specific threshold defined; Stretch: Instrumented + kill criterion)

# ... (remaining criteria)
```

**Secondary Output** (Optional): Summary Report

Generate markdown summary if requested:

**Summary Report Sections**:
1. **Executive Summary**: Overall coverage %, key findings
2. **Coverage by Category**: Table showing % coverage for each LO category
3. **Top Gaps** (Critical): List of missing/low coverage criteria sorted by priority
4. **Recommendations**: Actionable steps to close gaps (effort-estimated)
5. **Full Details**: Link to annotated YAML file

---

## Bundled Resources

### References

**`references/icp-baf-framework.md`** (Optional):
- Full ICP-BAF learning outcomes reference (31 LOs from pages 6-11)
- Use when evaluating against ICP-BAF specifically
- Grep pattern: Search for specific LO numbers (e.g., "1.1.1", "2.2.3")

**`references/depth-levels.md`**:
- Definitions for coverage depth assessment
- Awareness vs. Working Knowledge vs. Mastery
- Assessment rubrics for each level

### Scripts

None required (skill is search/analysis-based, not code-generation)

### Assets

None required (generates YAML and markdown output)

---

## Best Practices

### Search Strategy

1. **Use Multiple Keyword Variants**:
   - Search for both full terms and abbreviations (e.g., "high-performance questions" AND "HPQ")
   - Include related concepts (e.g., "evidence-seeking", "assumption-testing" when searching for HPQs)

2. **Contextual Relevance**:
   - Not every keyword match is evidence (e.g., "practice" in "best practice" vs. "participants practice")
   - Read ±5 lines of context to verify relevance

3. **Cross-Reference Artifacts**:
   - If slides mention a topic, check facilitator scripts for practice activity
   - If script includes practice, check for assessment rubric in quality gate sections

### Evidence Quality

**Strong Evidence** (cite this):
- Specific slide numbers or script line numbers (e.g., "Slide 14, lines 200-210")
- Direct quotes showing practice activities (e.g., "Participants type HPQ in chat for 90 seconds")
- Assessment rubrics or quality gates (e.g., "RYG self-check: Green = meets Acceptable")

**Weak Evidence** (flag as partial):
- Vague mentions without details (e.g., "We'll cover this later")
- Tangential references (e.g., keyword appears in unrelated context)
- No practice or assessment (awareness only)

### Gap Recommendations

**Prioritization**:
- **Critical**: Core learning outcomes central to certification (e.g., ICP-BAF 1.1.x, 2.2.x)
- **Important**: Supporting outcomes that enhance credibility
- **Nice-to-have**: Advanced topics or bonus content

**Actionability**:
- Suggest SPECIFIC artifacts to create (e.g., "Add Slide 15: Design Thinking 5 Steps")
- Estimate effort (e.g., "~20 minutes to create slide + facilitator notes")
- Reference existing content as template (e.g., "Use Module 1 O-I-S structure")

### Output Formatting

**YAML Formatting**:
- Preserve original criteria structure exactly
- Use `|` (pipe) for multi-line `where_the_course_covers` fields
- Include markdown formatting (bold, lists, code) for readability
- Add inline comments for coverage % and gaps

**File References**:
- Use relative paths (e.g., `module1-facilitator-script.md:132`)
- Include line numbers when referencing scripts
- Use descriptive artifact names (e.g., "Slide 14" instead of "slides.md line 400")

---

## Usage Example

### Input

**Evaluation Criteria** (`baf_evaluation.yaml`):
```yaml
- evaluation:
    expectation: "Demonstrate high-performance questions..."
    learning_outcome: "2.2.1. Ask vs. Tell: High-Performance Questions"
    where_the_course_covers: ""
```

**Content Artifacts**:
- `workshop-slides.md` (15 slides)
- `module4-facilitator-script.md` (Module 4 script)

### Audit Process

1. **Extract keywords**: "high-performance questions", "HPQ", "evidence-seeking"
2. **Search content**:
   - Found in `workshop-slides.md` line 200 (Slide 14)
   - Found in `module4-facilitator-script.md` lines 132-170 (HPQ Round section)
3. **Assess depth**:
   - Slide 14 shows 4 HPQ categories with examples (explained)
   - Script includes chat practice exercise (practiced)
   - No quality rubric found (not assessed)
   - **Coverage: 66% (Working Knowledge)**
4. **Identify gap**: Missing HPQ quality assessment rubric

### Output

```yaml
- evaluation:
    expectation: "Demonstrate high-performance questions..."
    learning_outcome: "2.2.1. Ask vs. Tell: High-Performance Questions"
    where_the_course_covers: |
      Module 4 (1:05-1:40): HPQ Round ✅ PARTIAL (66%)

      **Evidence**:
      - Slide 14 (workshop-slides.md:200-250): 4 HPQ categories defined
        - Evidence-seeking: "What evidence would change your mind?"
        - Assumption-testing: "What would have to be true?"
        - Boundary-probing: "At what point would you kill this?"
        - Reflection-prompting: "What surprised you most?"
      - Facilitator script (module4-facilitator-script.md:132-170):
        - Practice activity: Participants type HPQ answer in chat (90 sec)
        - Facilitator models 2-3 HPQs
        - Participants read aloud 2-3 strong HPQ examples

      **Coverage Level**: Working Knowledge (66%)
      - ✅ Awareness: HPQs defined with examples
      - ✅ Practice: Chat exercise + verbal share
      - ❌ Assessment: No quality rubric (what makes an HPQ "good"?)

      **Gap**: Add HPQ Quality Rubric
      - **Where**: Module 4 Facilitator Script (after line 170)
      - **Content**:
        - Acceptable: HPQ is specific (not vague like "Why?")
        - Stretch: HPQ surfaces hidden assumptions or defines kill criteria
      - **Effort**: ~10 minutes (add rubric + spot-check protocol)
```

---

## Integration with Other Skills

**Skill Sequencing**:
1. **content-auditor** (this skill) → Evaluate content against criteria, identify gaps
2. **implementation-coach** → Generate missing artifacts to close gaps
3. **slidev-skill** → Create specific slides for gap areas
4. **content-auditor** (re-run) → Verify gaps closed, update coverage report

**Example Workflow**:
```
User: "Audit my workshop against ICP-BAF"
→ content-auditor runs → Identifies 5 critical gaps
→ User: "Create slides for gap #2 (Design Thinking)"
→ slidev-skill runs → Generates Design Thinking slides
→ User: "Re-audit to confirm gap closed"
→ content-auditor re-runs → Updates YAML (gap #2 now 100%)
```

---

## Quality Patterns

### Comprehensive Search

- Search ALL content artifacts (don't skip facilitator scripts—they often contain practice details)
- Use case-insensitive search (`grep -i`)
- Search for acronyms AND full terms (e.g., "O-I-S" AND "Outcome-Indicator-Slice")

### Depth Assessment Rigor

**Checklist for Each Criterion**:
- [ ] **Mentioned?** (keyword found in content)
- [ ] **Explained?** (concept defined with examples)
- [ ] **Practiced?** (hands-on activity for participants)
- [ ] **Assessed?** (quality rubric or facilitator evaluation)

Only mark 100% if all 4 checkboxes are true.

### Actionable Recommendations

**Bad Recommendation** (too vague):
```
Gap: Design Thinking not covered. Add content about Design Thinking.
```

**Good Recommendation** (specific + actionable):
```
Gap: Design Thinking (LO 3.1.3) not covered (0%)

Recommendation:
- **Add Module 2.5** (5 minutes, after Flow mapping at minute 45)
  - Slide 8.5: Design Thinking 5 Steps visual (Empathize → Define → Ideate → Prototype → Test)
  - Activity: Participants sketch 1-minute customer journey map for their O-I-S outcome (Empathize step)
  - Use Miro Frame 9 (new frame): "Customer Journey Map" template
- **Facilitator Script Addition** (module2-facilitator-script.md, after line 120):
  - Script: "Design Thinking starts with empathy. Sketch your customer's journey—what do they experience before/during/after your outcome?"
  - Spot-check: Visit 1 triad, ensure journey maps show customer perspective (not internal process)
- **Effort**: ~30 minutes total
  - 15 min: Create Slide 8.5
  - 10 min: Write facilitator script section
  - 5 min: Design Miro template
- **Template**: Use Module 1 O-I-S structure (10-min build, 3-min peer review)
```

---

Generated: 2025-11-09
Purpose: Evaluate course content against certification frameworks (ICP-BAF, etc.)
Integration: Works with implementation-coach, slidev-skill for gap remediation
