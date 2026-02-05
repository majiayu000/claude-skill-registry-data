---
name: Slide Quality Assessment
description: This skill should be used when the user asks to "analyze slide quality", "review slide", "check slide design", "optimize slide", "improve slide content", "assess slide clarity", or needs evidence-based quality evaluation using the 12-point checklist for presentation slides.
version: 0.1.0
---

# Slide Quality Assessment

Evaluate presentation slides using evidence-based quality criteria grounded in cognitive load research, accessibility standards, and presentation best practices from TED, MIT Communication Lab, and technical conference guidelines.

**Research Foundation**: Quality assessment based on working memory limits (Miller's Law), David JP Phillips' cognitive load studies, WCAG accessibility standards, and analysis of effective technical presentations.

**IMPORTANT**: Before analyzing slides, use the Read tool to load the style guide from the plugin directory:
```
${CLAUDE_PLUGIN_ROOT}/references/presentation-best-practices.md
```
This contains the complete research-backed guidelines and validation criteria supporting the 12-point checklist.

## The 12-Point Quality Checklist

Use this systematic framework to evaluate any presentation slide:

### 1. ✓ One Idea Per Slide (CRITICAL)

**Criterion**: Does the slide communicate exactly ONE central idea, finding, or question?

**Why this matters**:
- Prevents cognitive overload
- Maintains audience focus during narration
- Enables clear narrative progression

**How to assess**:
- Can slide be explained in ~90 seconds?
- Does all content support only the title's assertion?
- Are there multiple unrelated concepts?

**Red flags**:
- ✗ Covering multiple independent topics
- ✗ Requires >2 minutes to explain
- ✗ Content diverges from title

**Fix**: Split into multiple slides, one concept each

---

### 2. ✓ Meaningful Title (CRITICAL)

**Criterion**: Is the title an assertion (subject + verb + finding) rather than a label?

**Why this matters**:
- Titles act as "topic sentences"
- Reading titles in sequence tells the story
- Helps distracted viewers catch up
- Audience should understand main point from title alone

**Good vs Bad**:
- ❌ Bad (labels): "Results", "Background", "Performance"
- ✅ Good (assertions): "Experiment X demonstrates 2x gain", "Current solutions fail at scale"

**How to assess**:
- Does title state a takeaway (not just a topic)?
- Subject + verb + finding format?
- Would titles in sequence tell a coherent story?

**Fix**: Convert labels to complete assertions

---

### 3. ✓ Element Count ≤6 (CRITICAL)

**Criterion**: Total distinct elements ≤6 (bullets + images + diagrams + charts + code blocks)

**Why this matters**:
- Working memory: 7±2 items (Miller's Law)
- >6 elements exponentially increases cognitive load (Phillips research)
- Audience cannot process >6 simultaneous information chunks

**What counts as elements**:
- Each bullet point = 1
- Each image/diagram = 1
- Each code block = 1
- Each chart/graph = 1
- Nested bullets count separately

**Exceptions**:
- Progressive builds (v-click) revealing elements incrementally = OK
- Diagrams with integrated labels (count as 1 if cohesive)

**How to assess**:
Count all visual and textual chunks the audience must process simultaneously

**Red flags**:
- ✗ 8+ bullet points
- ✗ Multiple diagrams + bullets
- ✗ Dense content without progressive disclosure

**Fix**: Reduce elements, split slides, or use v-click for progressive builds

---

### 4. ✓ Word Count <50 (CRITICAL)

**Criterion**: Body text <50 words (excluding title)

**Why this matters**:
- Audience cannot read and listen simultaneously
- >50 words = audience stops listening to speaker
- Slides support speaker, not replace them

**How to assess**:
- Count all words excluding title
- Include bullet text, captions, labels
- Exclude code (assess separately)

**Red flags**:
- ✗ Full sentences in bullets
- ✗ Paragraph text
- ✗ Long explanatory captions

**Fix**:
- Convert sentences to phrases (3-6 words per bullet)
- Move detailed explanations to presenter notes
- Split content across multiple slides

---

### 5. ✓ Visual Element Present

**Criterion**: At least one visual element (diagram, chart, image, code, or graphic)

**Why this matters**:
- Dual-channel processing (visual + audio) improves retention
- Visuals convey complex relationships better than text
- Almost never text-only slides

**Exceptions allowing text-only**:
- Quote slides
- Definition slides
- Bold statements for emphasis
- Section dividers

**How to assess**:
Is there a diagram, chart, image, code block, or other visual?

**Red flags**:
- ✗ Only title + bullets
- ✗ Dense text without supporting visual
- ✗ Missed opportunity for diagram

**Fix**: Add mermaid diagram, chart, image, or code example

---

### 6. ✓ Font Sizes (Body ≥18pt, Heading ≥24pt)

**Criterion**: Body text ≥18pt, headings ≥24pt (accessibility requirement)

**Why this matters**:
- WCAG accessibility standards
- Readability from back of room
- Accommodates vision impairments

**How to assess**:
- Check Slidev theme defaults
- Verify no custom CSS reducing sizes
- Test: Can text be read from 20 feet away?

**Red flags**:
- ✗ Tiny code fonts (<14pt)
- ✗ Compressed text to fit content
- ✗ Caption text <16pt

**Fix**: Use proper font sizes, split slides if content doesn't fit

---

### 7. ✓ Contrast Ratio (≥4.5:1)

**Criterion**: Text contrast ≥4.5:1 for normal text, ≥3:1 for large text (>24pt)

**Why this matters**:
- WCAG Level AA accessibility requirement
- Readability under projection conditions
- Accommodates vision impairments

**How to assess**:
- Check dark text on light backgrounds (or inverse)
- Avoid: gray-on-gray, yellow-on-white, light-blue-on-white
- Test: Is text clearly readable at a glance?

**Red flags**:
- ✗ Low-contrast color schemes
- ✗ Light text on light backgrounds
- ✗ Colored text without sufficient contrast

**Fix**: Use high-contrast color pairs, test with contrast checker

---

### 8. ✓ Colorblind-Safe (Not Color-Only)

**Criterion**: Meaning not conveyed by color alone (use patterns, labels, shapes)

**Why this matters**:
- ~8% of males have color vision deficiency
- Projected colors appear differently than on screen
- Print/grayscale versions must be understandable

**How to assess**:
- Can information be understood in grayscale?
- Are chart lines distinguished by style (solid/dashed) not just color?
- Do diagrams use labels, not just color coding?

**Red flags**:
- ✗ "Green = good, red = bad" without labels
- ✗ Chart with only color-differentiated lines
- ✗ Diagrams relying solely on color

**Fix**: Add patterns, labels, shapes, or text alongside color

---

### 9. ✓ Standalone Comprehension

**Criterion**: Can viewer grasp main point from title + visual alone (without narration)?

**Why this matters**:
- Distracted viewers can catch up mid-presentation
- Slides work for async review
- Conclusions highlighted, not buried

**How to assess**:
- 5-second test: Show slide without context - is point clear?
- Does visual reinforce the title's assertion?
- Could someone skimming slides get the story?

**Red flags**:
- ✗ Title + content don't align
- ✗ Visual unrelated to title
- ✗ Requires full narration to understand

**Fix**: Strengthen title-visual connection, add clarifying labels

---

### 10. ✓ Phrases Not Sentences

**Criterion**: Bullets are short phrases (3-6 words), not full sentences

**Why this matters**:
- Prevents audience from reading ahead
- Keeps focus on speaker
- Avoids reading-while-listening conflict
- Garr Reynolds principle: slides support, don't replace speaker

**Good vs Bad**:
- ❌ Bad: "Kubernetes orchestrates containerized applications across a cluster of machines"
- ✅ Good: "Container orchestration across clusters"

**How to assess**:
Are bullets short keyword phrases or full grammatical sentences?

**Red flags**:
- ✗ Bullets with periods at the end
- ✗ Multi-clause sentences
- ✗ Explanatory prose in bullets

**Fix**: Extract keywords, move details to presenter notes

---

### 11. ✓ White Space (≥10% Margins)

**Criterion**: Adequate white space around content (≥10% margins, well-distributed)

**Why this matters**:
- Prevents claustrophobic feeling
- Improves visual hierarchy
- Directs attention to content
- Professional appearance

**How to assess**:
- Is content distributed across slide?
- Breathing room around elements?
- Clear visual separation?

**Red flags**:
- ✗ Content edge-to-edge
- ✗ Cramped, dense appearance
- ✗ Elements overlapping or too close

**Fix**: Reduce content, increase padding, split slides

---

### 12. ✓ Explainable in ~90 Seconds

**Criterion**: Slide can be presented in approximately 90 seconds (configurable)

**Why this matters**:
- Maintains presentation pace
- Prevents overloaded slides
- Ensures depth without overwhelm
- Standard conference timing

**How to assess**:
- Can you explain all content in 90 seconds?
- Does slide require lengthy explanation?
- Would you rush through material?

**Red flags**:
- ✗ Requires >2 minutes to cover
- ✗ Dense content needing detailed explanation
- ✗ Multiple complex points

**Fix**: Split slides, simplify content, move details to notes

---

## Quality Scoring System

**Score calculation**: Count ✓ for each criterion met (max 12 points)

**Interpretation**:
- **12/12** - Excellent: Publication-ready
- **10-11/12** - Good: Minor tweaks needed
- **8-9/12** - Acceptable: Some improvements needed
- **6-7/12** - Poor: Significant revision required
- **<6/12** - Critical: Complete redesign needed

**Priority for fixes**:
1. **CRITICAL** violations (criteria 1-4): Must fix before presenting
2. **HIGH** violations (criteria 5-8): Should fix for quality presentation
3. **MEDIUM** violations (criteria 9-12): Nice to fix for polish

---

## Analysis Output Format

When assessing a slide, provide:

```markdown
## Slide [N]: [Current Title]

**Quality Score: [X/12]**

**Current State:**
- ✓/✗ One idea per slide
- ✓/✗ Meaningful title (assertion vs label)
- ✓/✗ Element count: [X] elements (target ≤6)
- ✓/✗ Word count: [Y] words (target <50)
- ✓/✗ Visual element present
- ✓/✗ Font sizes (body ≥18pt, heading ≥24pt)
- ✓/✗ Contrast ratio (≥4.5:1)
- ✓/✗ Colorblind-safe (not color-only)
- ✓/✗ Standalone comprehension (title + visual = point)
- ✓/✗ Phrases not sentences
- ✓/✗ White space (≥10% margins)
- ✓/✗ Explainable in ~90 seconds

**Critical Violations:** [List any CRITICAL criteria failures, or "None"]

**Recommendations (Priority Order):**

1. **[CRITICAL/HIGH/MEDIUM] - [Specific issue]**
   - Current: [What exists now with specific examples]
   - Suggested: [Concrete improvement with example]
   - Why: [Research basis from criteria above]
   - Impact: [Expected improvement]

2. **[Priority] - [Next issue]**
   [Same structure...]

**Quick Win:** [One simple change with biggest impact]
```

---

## Optimization Strategies by Issue

### Reducing Element Count (>6 elements)

**Tactics**:
- Merge related bullets into single points
- Move supporting details to presenter notes
- Split into 2-3 simpler slides
- Use progressive builds (v-click) to reveal incrementally

**Example**:
- Current: 8 bullets about microservices benefits
- Fix: Keep 4 key benefits, move implementation details to notes

---

### Reducing Word Count (>50 words)

**Tactics**:
- Convert full sentences to keyword phrases
- Remove articles (a, an, the)
- Use symbols/abbreviations where clear
- Move explanations to presenter notes

**Example**:
- Current: "Kubernetes provides automated deployment, scaling, and management of containerized applications"
- Fix: "Automated container deployment & scaling"

---

### Creating Meaningful Titles (Label → Assertion)

**Tactics**:
- Add verb + finding to label
- State the conclusion, not the category
- Make title reveal the "so what?"

**Examples**:
- "Results" → "Response time improved 3x with caching"
- "Background" → "Current solutions fail under high load"
- "Architecture" → "Microservices enable independent scaling"

---

### Adding Visual Elements

**When to add what**:
- **Process/workflow** → Mermaid flowchart
- **Architecture** → Mermaid component diagram
- **Data comparison** → Chart/graph
- **Concepts** → Icon or stock photo
- **Code behavior** → Code snippet with highlights

**Tip**: Use visual-design skill for diagram creation

---

### Converting Sentences to Phrases

**Pattern**:
- Identify the core noun phrase
- Remove helping verbs, articles
- Keep 3-6 words maximum

**Examples**:
- "The system automatically scales based on traffic" → "Auto-scaling based on traffic"
- "We implemented caching to improve performance" → "Caching improves performance"

---

## Edge Cases & Exceptions

### Slides That Don't Follow Standard Rules

**Title slides**:
- Skip word count limit
- Focus on visual impact
- Branding/conference info acceptable

**Code slides**:
- Check syntax highlighting
- Verify relevant line selection (not full files)
- Ensure <15 lines per block
- OK if text-heavy (code is visual)

**Data slides**:
- Chart clarity most important
- One insight per slide (even if data supports multiple)
- Label axes, provide legend

**Quote slides**:
- Attribution required
- Large readable font
- Can be text-only
- Keep quote <50 words

**Diagram-heavy slides**:
- Minimal text OK if diagram self-explanatory
- Ensure diagram elements ≤6
- Add title asserting diagram's point

**Reference slides** (appendix/backup):
- Mark as "reference" or "backup"
- Skip optimization
- Dense content acceptable

---

## When NOT to Optimize

**Don't optimize when**:
- Slide explicitly marked "detailed" or "reference"
- Mathematical proof requiring full derivation
- Code example needing complete context
- Intentional design choice with rationale

**Ask first if**:
- Unusual format seems intentional
- Content density might be presentation-specific requirement
- User indicates special constraints

---

## Interaction Guidelines

**When analyzing**:
- Be specific (not vague like "improve clarity")
- Explain reasoning with research basis
- Prioritize recommendations (most impactful first)
- Acknowledge good elements (not only criticism)
- Offer to apply changes or let user decide

**After analysis**:
- Ask if user wants to apply recommendations
- Allow selective application (not all-or-nothing)
- Offer to re-assess after changes
- Suggest next steps (optimize another slide, etc.)

---

## Working With This Skill

**To analyze a slide**:
1. Read the slide file
2. Apply each of the 12 criteria systematically
3. Count violations and score
4. Prioritize recommendations (CRITICAL → HIGH → MEDIUM)
5. Provide specific, actionable suggestions
6. Offer to implement approved changes

**Integration with other skills**:
- Use **presentation-design** skill for overall structure/flow
- Use **visual-design** skill to create diagrams/visuals
- Use **slidev-mastery** skill for technical Slidev syntax

**Tools available**:
- Read: Examine slide content
- Edit: Apply recommended improvements
- Grep: Search for patterns across slides

Apply this framework consistently to help create clear, accessible, evidence-based presentations.
