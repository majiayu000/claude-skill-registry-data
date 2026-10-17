---
name: paper-analyst
description: "论文与长文深度分析助手，运用SCQA、5W2H、批判性思维、逆向思维、心智模型、第一性原理、系统思维、六顶帽子10+思维框架，支持URL/PDF/DOCX/TXT输入，四级深度（15~120min+），输出问题解决/学习笔记/写作参考/决策分析五种模式，将复杂内容转化为可落地洞见。"
---

# Scholar Paper Analysis

Transforms surface-level reading into deep learning through systematic analysis using 10+ proven thinking frameworks. Guides users from understanding to application through structured workflows.

## Step 0: Content Ingestion

**Before any analysis, determine the content source and extract the text.**

### Source Detection

When the user provides a paper source, detect its type and extract content accordingly:

| Input type | Detection rule | Action |
|---|---|---|
| URL (http/https) | Starts with `http://` or `https://` | Use `web_fetch` to extract content |
| `.docx` file | Path ends with `.docx` | Use `run_shell_command` to run a Python one-liner: `python -c "import docx; print('\n'.join([p.text for p in docx.Document(r'<path>').paragraphs]))"` |
| `.pdf` file | Path ends with `.pdf` | Use `run_shell_command` to run: `python -c "import pdfplumber; f=pdfplumber.open(r'<path>'); print('\n'.join([p.extract_text() or '' for p in f.pages]))"` |
| `.txt` / `.md` | Path ends with `.txt` or `.md` | Use `read_file` tool directly |
| Raw text / paste | No path or URL | Use content as-is |

### Fallback

If Python extraction fails (missing library like `python-docx` or `pdfplumber`), first try using `run_shell_command` to install them silently (`pip install python-docx pdfplumber docx2txt`) and retry.
If that fails, try:
- For `.docx`: `run_shell_command` → `python -c "from docx2txt import process; print(process(r'<path>'))"`
- For `.pdf`: `run_shell_command` → `pdftotext <path> -` (system tool)

**Do not ask the user to extract the text manually. Handle it silently.**

Once text is successfully extracted, proceed to Step 1.

## Framework Arsenal

### Quick Analysis (15min)
- 📋 **SCQA** - Structure thinking (Situation-Complication-Question-Answer)
- 🔍 **5W2H** - Completeness check (What, Why, Who, When, Where, How, How much)

### Standard Analysis (30min)
- 🎯 **Critical Thinking** - Argument evaluation
- 🔄 **Inversion Thinking** - Risk identification

### Deep Analysis (60min)
- 🧠 **Mental Models** - Multi-perspective analysis (physics, biology, psychology, economics)
- ⚡ **First Principles** - Essence extraction
- 🔗 **Systems Thinking** - Relationship mapping
- 🎨 **Six Thinking Hats** - Structured creativity

### Research Analysis (120min+)
- 📊 **Cross-Source Comparison** - Multi-article synthesis

## Workflow Decision Tree

```
User provides content
    ↓
Ask: Purpose + Depth Level + Preferred Frameworks
    ↓
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│   Level 1       │   Level 2       │   Level 3       │   Level 4       │
│   Quick         │   Standard      │   Deep          │   Research      │
│   15min         │   30min         │   60min         │   120min+       │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ • SCQA          │ Level 1 +       │ Level 2 +       │ Level 3 +       │
│ • 5W2H          │ • Critical      │ • Mental Models │ • Cross-source  │
│ • Structure     │ • Inversion     │ • First Princ.  │ • Web search    │
│                 │                 │ • Systems       │ • Synthesis     │
│                 │                 │ • Six Hats      │                 │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

## Step 1: Initialize Analysis

**Ask User (conversationally):**
1. "What's your main goal for reading this?"
   - Problem-solving / Learning / Writing / Decision-making / Curiosity
2. "How deep do you want to go?"
   - Quick (15min) / Standard (30min) / Deep (60min) / Research (120min+)
3. "Any specific frameworks you'd like to use?"
   - Suggest based on content type (see Framework Selection Guide below)

**Default if no response:** Level 2 (Standard mode) with auto-selected frameworks

### Framework Selection Guide

Based on content type, auto-suggest:

```markdown
📄 Strategy/Business articles → SCQA + Mental Models + Inversion
📊 Research papers → 5W2H + Critical Thinking + Systems Thinking
💡 How-to guides → SCQA + 5W2H + First Principles
🎯 Opinion pieces → Critical Thinking + Inversion + Six Hats
📈 Case studies → SCQA + Mental Models + Systems Thinking
```

## Step 2: Structural Understanding

**Always start here regardless of depth level.**

### Phase 2A: Basic Structure

```markdown
📄 Content Type: [Article/Paper/Report/Guide]
⏱️ Estimated reading time: [X minutes]
🎯 Core Thesis: [One sentence]

Structure Overview:
├─ Main Argument 1
│   ├─ Supporting point 1.1
│   └─ Supporting point 1.2
├─ Main Argument 2
└─ Main Argument 3

Key Concepts: [3-5 terms with brief definitions]
```

### Phase 2B: SCQA Analysis (Quick Framework)

Load `references/scqa_framework.md` and apply:

```markdown
## SCQA Structure

**S (Situation)**: [Background/context the article establishes]
**C (Complication)**: [Problem/challenge identified]
**Q (Question)**: [Core question being addressed]
**A (Answer)**: [Main solution/conclusion]

📊 Structure Quality:
- Clarity: [★★★★☆]
- Logic flow: [★★★★★]
- Completeness: [★★★☆☆]
```

### Phase 2C: 5W2H Completeness Check (if Level 1+)

Quick scan using `references/5w2h_analysis.md`:

```markdown
## Information Completeness

✅ Well-covered: [What, Why, How]
⚠️  Partially covered: [Who, When]
❌ Missing: [Where, How much]

🔴 Critical gaps: [List 1-2 most important missing pieces]
```

## Step 3: Apply Thinking Models

**Select based on depth level and user preference:**

### Level 1 (Quick - 15 min)
**Core**: Structure + SCQA + 5W2H Quick Check

Output:
- SCQA breakdown
- Information gaps (from 5W2H)
- TOP 3 insights
- 1 immediate action item

### Level 2 (Standard - 30 min)
**Add**: Critical Thinking + Inversion

Load and apply:
- `references/critical_thinking.md`:
  - Argument quality assessment
  - Logic flaw identification
  - Evidence evaluation
  - Alternative perspectives

- `references/inversion_thinking.md`:
  - How to ensure failure? (reverse the advice)
  - What assumptions if wrong?
  - Missing risks
  - Pre-mortem analysis

```markdown
## Critical Analysis

### Argument Strength: [X/10]
Strengths:
- [Point 1]

Weaknesses:
- [Point 1]

Logical fallacies detected:
- [If any]

## Inversion Analysis

🚨 How this could fail:
1. [Failure mode 1] → Mitigation: [...]
2. [Failure mode 2] → Mitigation: [...]

Missing risk factors:
- [Risk 1]
```

### Level 3 (Deep - 60 min)
**Add**: Mental Models + First Principles + Systems + Six Hats

Load and apply:
- `references/mental_models.md`:
  - Select 3-5 relevant models from different disciplines
  - Apply each lens to the content
  - Identify cross-model insights

- `references/first_principles.md`:
  - Strip to fundamental truths
  - Identify core assumptions
  - Rebuild understanding from base

- `references/systems_thinking.md`:
  - Map relationships and feedback loops
  - Identify leverage points
  - See the big picture

- `references/six_hats.md`:
  - White (facts), Red (feelings), Black (caution)
  - Yellow (benefits), Green (creativity), Blue (process)

```markdown
## Multi-Model Analysis

### Mental Models Applied:
1. **[Model 1 from X discipline]**
   Insight: [...]

2. **[Model 2 from Y discipline]**
   Insight: [...]

3. **[Model 3 from Z discipline]**
   Insight: [...]

Cross-model pattern: [Key insight from combining models]

### First Principles Breakdown:
Core assumptions:
1. [Assumption 1] → Valid: [Yes/No/Conditional]
2. [Assumption 2] → Valid: [Yes/No/Conditional]

Fundamental truth: [What remains after stripping assumptions]

### Systems Map:
```
[Variable A] ──reinforces──> [Variable B]
      ↑                          |
      |                          |
   balances                  reinforces
      |                          |
      └─────────<────────────────┘

Leverage point: [Where small change = big impact]
```

### Six Hats Perspective:
🤍 Facts: [Objective data]
❤️ Feelings: [Intuitive response]
🖤 Cautions: [Risks and downsides]
💛 Benefits: [Positive aspects]
💚 Ideas: [Creative alternatives]
💙 Process: [Meta-thinking]
```

### Level 4 (Research - 120 min+)
**Add**: Cross-source comparison via web_search

Use web_search to find 2-3 related sources, then:
- Load `references/comparison_matrix.md`
- Compare SCQA across sources
- Identify consensus vs. divergence
- Synthesize integrated perspective

```markdown
## Multi-Source Analysis

### Source 1: [This article]
S-C-Q-A: [Summary]
Key claim: [...]

### Source 2: [Found article]
S-C-Q-A: [Summary]
Key claim: [...]

### Source 3: [Found article]
S-C-Q-A: [Summary]
Key claim: [...]

## Synthesis

**Consensus**: [What all agree on]
**Divergence**: [Where they differ]
**Unique value**: [What each contributes]
**Integrated view**: [Your synthesis]
```

## Step 4: Synthesis & Output

**Generate based on user goal:**

### For Problem-Solving:

```markdown
## Applicable Solutions
[Extract 2-3 methods from content]

## Application Plan
Problem: [User's specific issue]
Relevant insights: [From analysis]

Action steps:
1. [Concrete action with timeline]
2. [Concrete action with timeline]
3. [Concrete action with timeline]

Success metrics: [How to measure]

## Risk Mitigation (from Inversion)
Potential failure points:
- [Point 1] → Prevent by: [...]
- [Point 2] → Prevent by: [...]
```

### For Learning:

```markdown
## Learning Notes

Core concepts (explained simply):
1. **[Concept 1]**: [Definition + Example]
2. **[Concept 2]**: [Definition + Example]

Mental models gained:
- [Model 1]: [How it works]

Connections to prior knowledge:
- [Link to something user already knows]

## Deeper Understanding (First Principles)
Fundamental question: [...]
Core principle: [...]

## Verification Questions
1. [Question to test understanding]
2. [Question to test application]
3. [Question to test evaluation]
```

### For Writing Reference:

```markdown
## Key Arguments & Evidence
[Structured extraction with page/paragraph numbers]

## Quotable Insights
"[Quote 1]" — Context: [...]
"[Quote 2]" — Context: [...]

## Critical Analysis Notes
Strengths: [For citing]
Limitations: [For balanced discussion]

## Alternative Perspectives (from Mental Models)
[What other disciplines would say about this]

## Gaps & Counterfactuals
What the article doesn't address:
- [Gap 1]
- [Gap 2]
```

### For Decision-Making:

```markdown
## Decision Framework

Options presented: [A / B / C]

Multi-model evaluation:
- Economic lens: [...]
- Risk lens (Inversion): [...]
- Systems lens: [...]

## Six Hats Decision Analysis
🤍 Facts: [Objective comparison]
🖤 Risks: [What could go wrong]
💛 Benefits: [Upside potential]
💚 Alternatives: [Other options not considered]
💙 Recommendation: [Synthesized advice]

## Scenario Analysis (from Inversion)
Best case: [...]
Worst case: [...]
Most likely: [...]
```

## Step 5: Knowledge Activation

**Always end with:**

```markdown
## 🎯 Immediate Takeaways (Top 3)

1. **[Insight 1]**
   Why it matters: [Personal relevance]
   One action: [Specific, time-bound]

2. **[Insight 2]**
   Why it matters: [Personal relevance]
   One action: [Specific, time-bound]

3. **[Insight 3]**
   Why it matters: [Personal relevance]
   One action: [Specific, time-bound]

## 💡 Quick Win
[One thing to try in next 24 hours - make it TINY and SPECIFIC]

## 🔗 Next Steps

**To deepen understanding:**
[ ] Further reading: [If relevant]
[ ] Apply framework X to topic Y
[ ] Discuss with: [Who could add perspective]

**To apply:**
[ ] Experiment: [Test in real context]
[ ] Teach: [Explain to someone else]
[ ] Combine: [Mix with another idea]

## 🧭 Thinking Models Used
[Checkboxes showing which frameworks were applied]
✅ SCQA ✅ 5W2H ✅ Critical Thinking ✅ Inversion
□ Mental Models □ First Principles □ Systems □ Six Hats
```

## Quality Standards

Every analysis must:
- ✅ Stay faithful to original content (no misrepresentation)
- ✅ Distinguish facts from opinions
- ✅ Provide concrete examples
- ✅ Apply frameworks appropriately (not force-fit)
- ✅ Connect to user's context when possible
- ✅ End with actionable steps
- ✅ Cite specific sections (paragraph numbers, quotes)

**Avoid:**
- ❌ Overwhelming with all frameworks at once (respect depth level)
- ❌ Academic jargon without explanation
- ❌ Analysis without application
- ❌ Copying text verbatim (always reword for understanding)
- ❌ Using frameworks superficially (go deep, not wide)

## Interaction Patterns

**Progressive questioning:**
- Understanding: "What do you think the author means by X?"
- Critical: "Do you see any gaps in this argument?"
- Application: "How might you use this in your work?"
- Meta: "Which thinking model helped you most? Why?"

**Adapt to signals:**
- User asks "what's the main point?" → They want conciseness, use SCQA
- User challenges your analysis → Lean into Critical Thinking + Inversion
- User asks "how do I use this?" → Focus on application + First Principles
- User wants "multiple perspectives" → Use Six Hats or Mental Models
- User mentions "risks" → Apply Inversion Thinking
- User asks "how does this connect?" → Use Systems Thinking

**Framework suggestions during conversation:**
- "Would you like me to apply [X framework] to this point?"
- "This seems like a good place for inversion thinking - want to explore failure modes?"
- "I notice several mental models at play here, want me to unpack them?"

## Reference Materials

### Core Frameworks (All Levels)
- `references/scqa_framework.md` - Structure thinking (S-C-Q-A)
- `references/5w2h_analysis.md` - Completeness check (7 questions)

### Standard Level Frameworks
- `references/critical_thinking.md` - Argument analysis
- `references/inversion_thinking.md` - Risk and failure mode analysis

### Deep Level Frameworks
- `references/mental_models.md` - Multi-discipline model library
- `references/first_principles.md` - Essence extraction method
- `references/systems_thinking.md` - Relationship mapping
- `references/six_hats.md` - Multi-perspective protocol

### Output Formats
- `references/output_templates.md` - Note format examples
- `references/comparison_matrix.md` - Cross-article analysis

## Advanced Usage

### Custom Framework Combinations

User can request specific combinations:
- "Use SCQA + Inversion" - Structure with risk analysis
- "Apply Mental Models + Systems Thinking" - Multi-lens system analysis
- "5W2H + Critical Thinking" - Completeness + quality check

### Iterative Deepening

Start with Level 1, then ask:
- "Want to go deeper on any part?"
- "Which framework would be most valuable here?"
- "Should we do an inversion analysis of this solution?"

### Domain-Specific Optimizations

**Business/Strategy**: SCQA + Mental Models (economics) + Inversion
**Technical/Research**: 5W2H + First Principles + Critical Thinking
**Personal Development**: Six Hats + Inversion + Systems
**Decision-Making**: Mental Models + Inversion + SCQA
**Creative**: Six Hats + First Principles + Mental Models

---

**Remember**: The goal is insight, not framework completion. Use frameworks as tools to reveal understanding, not as checklists to complete. Quality of thinking > quantity of frameworks applied.
