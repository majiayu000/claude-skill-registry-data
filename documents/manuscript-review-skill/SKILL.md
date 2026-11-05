---
name: manuscript-review
description: "Multi-agent academic manuscript review that generates bilingual annotated docx. Use when the user wants to review a manuscript, create a multi-agent review document, generate bilingual annotated review, or improve a paper before journal submission. Also trigger on: '审稿', '多Agent审稿', '文稿审阅', '学术文稿评审', 'agent team review', 'manuscript critique', 'paper review panel', '投稿前审阅', '逐段审稿'."
license: MIT
---

# Multi-Agent Academic Manuscript Review

Generate a bilingual (English-Chinese) annotated docx with 6 expert Agent review panels for any academic manuscript. Each Agent provides role-specific critique with scoring, producing a comprehensive pre-submission review document.

## When to Use

- User wants a multi-agent review of an academic manuscript
- User asks to generate a bilingual annotated review document
- User wants to improve a paper before journal submission
- User mentions "审稿", "agent team review", "manuscript review", "投稿前审阅"
- User provides a manuscript (docx, PDF, or text) and wants expert critique

## 6 Core Agents

| Agent | Role | Color | Background | Review Focus |
|-------|------|-------|------------|--------------|
| A | Architecture Strategist 架构军师 | #660066 | #F5F0F8 | Structure, logic chain, causal reasoning, storyline, hypothesis-data alignment |
| B | Theory Mentor 理论导师 | #003399 | #F0F4FA | Theory gaps, novelty, significance, literature positioning |
| C | Methods & Stats Reviewer 方法统计审稿人 | #990000 | #FAF0F0 | Data, formulas, models, statistical rigor, sample size, effect size, ML necessity/feasibility |
| D | Application Advisor 应用保护顾问 | #006600 | #F0FAF0 | Application value, management implications, policy relevance |
| E | Journal Editor 期刊主编 | #CC6600 | #FFF8F0 | Journal fit, formatting, word limits, impact, competitive positioning |
| F | Senior Collaborator 资深合作者 | #006666 | #F0FAFA | Strategic positioning, future directions, collaboration, career value |

Optional: **Agent ML** (ML/Statistics Specialist, #8B008B / #FFF0F5) for quantitative-heavy papers.

## Workflow

### Phase 1: Read the Manuscript

**Option A — From docx file:**
```bash
pandoc input.docx -o manuscript.md
```
Then read `manuscript.md` to extract the full text and identify structure.

**Option B — From PDF:**
Use the `pdf` skill to extract text, or ask the user to paste content.

**Option C — User pastes text directly.**

After reading, identify the manuscript structure:
- Title, Authors
- Significance Statement (if applicable)
- Abstract
- Introduction (count paragraphs)
- Materials and Methods (count subsections)
- Results (count subsections + figures + tables)
- Discussion (count subsections)
- References
- Supplementary Materials (SI methods, SI figures, SI tables)

Also identify image files if the user provides them (e.g., from unpacked docx media/).

### Phase 2: Configure Review Parameters

Ask the user (via AskUserQuestion) to confirm:

1. **Target journal** — e.g., PNAS, Nature, Science, Ecology Letters, etc. This affects Agent E's review standards (word limits, format requirements, scope fit).
2. **Review depth**:
   - **Quick review** — 2-3 sentences per Agent per section (at least 1 specific problem + 1 fix), overall scoring only
   - **Deep review** (default) — 4-6 sentences per Agent per section with specific suggestions + scoring (see "Review Depth Requirements" below)
3. **Additional Agents** — Whether to add Agent ML or other custom agents
4. **Language pair** — Default: English-Chinese. Can be changed.
5. **Output file name and directory**

### Phase 3: Generate the Review Script

#### Step 1: Read the scaffold template

**MANDATORY**: Read the scaffold template at [`template/scaffold.js`](template/scaffold.js) to get all helper functions and document infrastructure. Never recreate these from memory.

Also read the docx API reference at [`references/docx-js-api.md`](references/docx-js-api.md) for correct API usage and common pitfalls.

#### Step 2: Build the script

Create a new JS file (e.g., `create_bilingual_agents.js`) in the user's working directory:

1. **Copy the scaffold template** as the file header (everything before `// === INSERT CONTENT HERE ===`)
2. **Set configuration variables** at the top:
   - `MEDIA` path (if images are available)
   - `OUTPUT_FILE` path
   - `HEADER_TEXT` (customize per paper + journal)
3. **For each manuscript section**, generate content entries:

```javascript
// Pattern for each section:
content.push(...sectionHead(1, "Section Title", "中文标题"));
content.push(
  eng("Original English text of the paragraph..."),
  chn("中文翻译..."),
  separator()
);

// Agent review panel for this section
content.push(panelHeader("▶ Agent Team Review: Section Name 中文标签"));
content.push(
  agentA("审稿评语... [Score: 8/10]"),
  agentB("审稿评语... [Score: 7/10]"),
  agentC("审稿评语... [Score: 6/10]"),
  agentD("审稿评语... [Score: 7/10]"),
  agentE("审稿评语... [Score: 8/10]"),
  agentF("审稿评语... [Score: 9/10]"),
  separator()
);
```

4. **Generate scoring matrix table** at the end (see "Scoring System" below)
5. **Generate priority improvement list** after the scoring table
6. **Copy the scaffold template footer** (Document creation + Packer output)

#### Step 3: Handle long scripts

Since the generated file will be 1000+ lines, write it in batches:
1. Write file header (helpers + Title/Significance/Abstract) with the Write tool
2. Append Introduction section with Bash heredoc (`cat >> file << 'SECTION_EOF'`)
3. Append Materials and Methods section with Bash heredoc
4. Append Results + Discussion + Supplementary + Summary + Document assembly with Bash heredoc

### Phase 4: Run and Verify

```bash
cd <working_directory> && node create_bilingual_agents.js
```

Verify:
- Check that the output docx file exists and has reasonable size (>100KB typically)
- Optionally convert to PDF/images for visual inspection:
  ```bash
  soffice --headless --convert-to pdf output.docx
  pdftoppm -jpeg -r 150 output.pdf preview
  ```

## Scoring System — Stringent Calibration

**Calibration principle: Scores reflect the standard of the target journal's top 10% of accepted papers. Most first-draft manuscripts should score 5-7. A score of 8 means "minor revision only." A score of 9-10 is virtually never given on first review.**

Each Agent scores each major section on a 1-10 scale. At the document end, generate:

### 1. Scoring Matrix Table

Use docx `Table`, `TableRow`, `TableCell` to create a formatted table:

```javascript
// Helper for table cells
function makeCell(text, isHeader = false) {
  return new TableCell({
    width: { size: isHeader ? 1500 : 1000, type: WidthType.DXA },
    shading: isHeader ? { fill: "E8E8E8", type: ShadingType.CLEAR } : undefined,
    children: [new Paragraph({ spacing: { before: 30, after: 30 },
      children: [new TextRun({ text: String(text), font: "Arial", size: 15,
        bold: isHeader, color: "333333" })] })]
  });
}

// Build header row
const headerRow = new TableRow({ children: [
  makeCell("Section", true), makeCell("A 架构", true), makeCell("B 理论", true),
  makeCell("C 方法", true), makeCell("D 应用", true), makeCell("E 主编", true),
  makeCell("F 合作", true), makeCell("Avg", true)
]});
// ... data rows + overall average row with bold formatting
```

### 2. Priority Improvement List

After the table, add categorized improvements:

```javascript
content.push(panelHeader("▶ Priority Improvements 优先改进清单"));
content.push(
  eng("CRITICAL (must fix before submission):"),
  agentC("1. [Issue]..."),  // Use the relevant agent's color
  agentA("2. [Issue]..."),
  separator(),
  eng("MAJOR (strongly recommended):"),
  agentB("3. [Issue]..."),
  agentE("4. [Issue]..."),
  separator(),
  eng("MINOR (nice to have):"),
  agentF("5. [Suggestion]..."),
  separator()
);
```

## Agent Review Guidelines — Ultra-Critical Mode

**Core Philosophy: Simulate the harshest yet most constructive reviewers at the target journal. Assume the manuscript has serious problems until proven otherwise. Every sentence must earn its place; every claim must be interrogated.**

### Mandatory Review Principles

1. **Assume nothing is proven** — Treat every claim as a hypothesis to be challenged. Ask: "Is there an alternative explanation the authors haven't considered?" For EVERY major claim, explicitly state whether it is supported, partially supported, or unsupported by the presented evidence.

2. **Quote and cite precisely** — Reference exact phrases from the manuscript (e.g., "The claim in Results P3: 'X was significantly associated with Y' is problematic because..."). Never give vague feedback like "the analysis seems weak." Point to the exact location and exact problem.

3. **Diagnose AND prescribe** — Every critique MUST be paired with a concrete, actionable fix. Bad: "The statistics are questionable." Good: "The permutation test on line X does not account for spatial non-independence; recommend restructuring as a mixed-effects model with watershed as a random effect, or at minimum adding a spatial block bootstrap (see Legendre & Fortin 1989)."

4. **Challenge the logic chain explicitly** — For each section, map out the implicit argument chain (Premise A → Premise B → Conclusion C) and identify where links are weak, missing, or circular. Flag any instance of: correlation → causation conflation, post-hoc rationalization, unstated assumptions, circular reasoning, or cherry-picking.

5. **Score with extreme discipline** — The default assumption is that a section scores 5-6 (adequate but needs significant work). Scores of 8+ should be rare and reserved for genuinely exceptional work. Scores of 9-10 mean "I would not change a single word." NEVER inflate scores to be polite. An average manuscript should score 5-7 overall.

6. **Write in Chinese** — All Agent review text is in Chinese, with technical terms in English where standard.

7. **Include score** — End each comment with `[Score: X/10]`

8. **Stay in character** — Each Agent focuses on their domain but can flag cross-domain concerns for other agents. Agent C does NOT comment on journal fit; Agent E does NOT critique statistical methods.

### Review Depth Requirements

**Per section, per Agent (Deep Review mode):**
- Minimum 4-6 sentences of substantive critique
- At least 2 specific problems identified with exact locations
- At least 1 concrete rewrite suggestion (provide the actual improved sentence/paragraph)
- At least 1 question the authors must answer
- Score with brief justification for why this score and not higher

**Quick Review mode:** 2-3 sentences per Agent, but still with at least 1 specific problem and 1 fix.

### Red Flags to Always Catch

Every Agent should flag these if encountered, regardless of their domain:
- Internal contradictions between sections (Abstract says X, Results say Y)
- Overclaiming (e.g., "demonstrates" for observational data, "proves" for correlative evidence)
- Missing uncertainty quantification (no confidence intervals, no error propagation)
- Selective reporting (only favorable results shown, unfavorable ones buried in SI)
- Vague hedging that hides the true contribution ("may potentially contribute to partially explaining...")
- Tautological reasoning ("X is important because X matters")
- Orphan claims (statements with no citation and no data support)

### Section-Specific Review Focus

| Section | Primary Agents | Key Questions — MUST be explicitly answered |
|---------|---------------|----------------------------------------------|
| Title | A, B, E | Does every word earn its place? Does it overclaim or underclaim? Is it findable by keyword search? Does it accurately reflect the actual (not aspirational) contribution? |
| Significance | A, D, E | Would a non-specialist understand why they should care within 2 sentences? Does it stay within the word limit? Does it contain any jargon that excludes readers? Is the "so what?" crystal clear? |
| Abstract | All | Can someone reproduce the study from the abstract alone? Are all three of "what/why/how" answered? Is there any claim in the abstract not supported in the main text? Are numbers internally consistent with the main text? |
| Introduction | A, B | Is the gap statement falsifiable? Is the literature review balanced (not just citing supportive work)? Are hypotheses stated explicitly or merely implied? Is there a clear transition from "what is known" to "what is unknown" to "what we do"? |
| Methods | C | Could a competent researcher reproduce this study with only the Methods section? Are all arbitrary choices justified (e.g., why this distance threshold? why this sample size cutoff?)? Are assumptions of statistical tests explicitly verified? |
| Results | A, C | Does every result directly address a stated hypothesis? Are effect sizes reported alongside p-values? Is there cherry-picking of results? Do figures match the text exactly (same numbers, same patterns)? Are non-significant results reported honestly? |
| Discussion | B, D, F | Does it add genuine interpretation beyond restating Results? Are limitations honest or strategically minimized? Are alternative explanations seriously engaged (not just mentioned and dismissed)? Is speculation clearly labeled as such? |
| Figures | C, E | Is each figure necessary (could the information be conveyed more efficiently)? Are axes labeled with units? Are color choices accessible? Is the caption self-explanatory without reading the text? Do panels have consistent formatting? |
| Tables | C, E | Is a table the best format (vs. text or figure)? Are all columns/rows necessary? Are units in headers? Are significant digits consistent? Does the caption fully explain abbreviations and statistical notations? Do values match the text exactly? |
| Supplementary Methods | C | Are SI methods truly supplementary (not essential for reproducibility)? Could a reader reproduce the study without reading SI? Are cross-references to main text correct? Are SI-only analytical choices justified? |
| Supplementary Figures & Tables | A, C, E | Is each SI item referenced in the main text? Could any SI item strengthen the main text if promoted? Are SI figures/tables of publication quality (not draft-quality dumps)? Do SI results contradict or qualify main text claims? Is numbering sequential and cross-referenced correctly? |

For detailed agent role descriptions and review dimensions, see [`references/agent-profiles.md`](references/agent-profiles.md).

## Dependencies

```bash
# Check docx package
node -e "require('docx')" 2>/dev/null && echo "OK" || npm install docx
# Check pandoc (if needed for docx input)
which pandoc || brew install pandoc
```
