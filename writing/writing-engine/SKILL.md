---
name: writing-engine
description: >
  ALWAYS activate when the user writes, drafts, or revises any part of an academic paper.
  This is the core skill for overcoming writer's block and producing complete first drafts.
  Provides concrete sentence-level templates, paragraph formulas, and section blueprints 
  for IS/WI/BWL research papers. Works for journal papers (MISQ, BISE, EJIS), 
  conference papers (ICIS, ECIS, WI), and working papers.
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Writing Engine
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (writing-engine)
> **Input:** [brief description of what the user asked to write/draft/revise]
> **Output:** [brief description of what was produced — e.g., "Complete draft of Introduction (1,200 words)"]
> ```

# Writing Engine

## Core Principle
The biggest barrier to writing is the blank page. This skill eliminates it by providing 
fill-in-the-blank templates at every level: sentence, paragraph, section, and full paper.
Claude should NEVER give vague advice like "write a compelling introduction." Instead, 
Claude produces ACTUAL DRAFT TEXT that the researcher can edit.

## When the User Says "Help Me Write" — What to Do

1. **Ask what section** (if not clear)
2. **Ask what the key inputs are** (RQ, findings, theory — whatever that section needs)
3. **PRODUCE A COMPLETE DRAFT** — not an outline, not bullet points, actual paragraphs
4. **Mark placeholders** with [BRACKETS] where specific data is needed
5. **Include inline citation placeholders** as (Author, Year) or [CITE] where references go

---

## INTRODUCTION (Target: 1500-2000 words for journal, 800-1000 for conference)

### The 6-Paragraph Formula

**Paragraph 1 — The Hook (Practical Relevance)**
Open with a striking fact, trend, or problem from practice. Ground the reader immediately.

Template:
```
[Phenomenon] is transforming [domain/industry]. [Concrete statistic or trend, e.g., 
"By 2025, X% of organizations..."] (Source, Year). [Second sentence expanding scope]. 
This development raises fundamental questions about [broad challenge], particularly 
regarding [specific aspect your paper addresses].
```

Example for the GenAI/Agents paper:
```
Generative AI and autonomous AI agents are fundamentally reshaping how organizations 
operate, make decisions, and create value. According to [McKinsey/Gartner], [X]% of 
enterprises have initiated pilot projects with generative AI, while autonomous agents 
are projected to handle [Y]% of routine business processes by [year] (Source, Year). 
This rapid adoption raises pressing questions about how organizations can effectively 
implement these technologies while managing the profound organizational changes they entail.
```

**Paragraph 2 — Academic Context (What We Know)**
Briefly position the topic in the scholarly conversation. Name 3-5 key streams.

Template:
```
The academic community has begun to examine [topic] from multiple perspectives. 
Research on [stream 1] has investigated [aspect] (Author1, Year; Author2, Year). 
Studies in [stream 2] have explored [aspect] (Author3, Year; Author4, Year). 
More recently, [stream 3] has examined [emerging aspect] (Author5, Year). 
Together, these streams provide important foundations, yet [transition to gap].
```

**Paragraph 3 — The Gap (What We Don't Know)**
The most critical paragraph. Must be specific, non-trivial, and convincing.

Gap patterns (use ONE or combine):
- **Fragmented knowledge**: "While these streams provide valuable insights individually, they remain largely disconnected. No integrative framework exists that [combines X and Y]."
- **Missing context**: "Although [phenomenon] is well-understood in [context A], its dynamics in [context B] remain unexplored. This matters because [reason]."
- **Temporal gap**: "Much of the existing research predates the emergence of [new development]. Given that [what changed], updated investigation is needed."
- **Missing mechanism**: "Prior work establishes that [X influences Y], but the underlying mechanisms — specifically [what and how] — are insufficiently understood."
- **Methodological limitation**: "Existing studies rely predominantly on [method], which cannot capture [important dynamic]. A [different approach] is needed to [achieve what]."

Template:
```
However, several important gaps remain. First, [gap 1 — be specific]. Second, [gap 2]. 
Third, [gap 3 if applicable]. These gaps are consequential because [why it matters 
for theory AND practice]. Without [what's missing], [negative consequence for the field].
```

**Paragraph 4 — Research Objective & Questions**
State exactly what the paper does.

Template:
```
To address these gaps, this study [verb: investigates/develops/examines/proposes] 
[specific object of research]. Specifically, we ask:

RQ1: [First research question — most important]
RQ2: [Second research question — if applicable]
[RQ3: Optional third question]

To answer [these questions/this question], we [brief method description: 
conduct a systematic literature review / develop a DSR artifact / employ a 
multiple case study approach / survey N organizations].
```

**Paragraph 5 — Contribution Statement**
The make-or-break paragraph for reviewers.

Template (3-contribution pattern):
```
This study makes three contributions to [field/literature stream]. First, we 
[specific contribution 1 — what new knowledge]. While prior work has [what they did], 
we [what you do differently]. Second, we [contribution 2 — theoretical or methodological]. 
This extends [theory/framework] by [specific extension]. Third, we derive [contribution 3 — 
practical]. For practitioners, our findings provide [actionable insight: guidelines / 
framework / decision criteria / implementation roadmap].
```

**Paragraph 6 — Roadmap**
Keep it short.

Template:
```
The remainder of this paper is structured as follows. Section 2 reviews [theoretical 
foundations and related work]. Section 3 describes our [research methodology]. 
Section 4 presents [results/findings/the artifact]. Section 5 discusses [implications 
and limitations]. Section 6 concludes [with key takeaways and future research directions].
```

---

## THEORETICAL BACKGROUND / LITERATURE REVIEW (Target: 3000-5000 words journal, 1500-2500 conference)

### Structure Options

**Option A — By Concept (most common for empirical papers)**
```
2. Theoretical Background
   2.1 [Core Concept 1, e.g., "Generative AI in Organizational Contexts"]
   2.2 [Core Concept 2, e.g., "Autonomous AI Agents: Definitions and Capabilities"]
   2.3 [Theoretical Lens, e.g., "Socio-Technical Systems Theory"]
   2.4 [Integration, e.g., "Research Model / Conceptual Framework"]
```

**Option B — Funnel (broad to narrow)**
```
2. Related Work
   2.1 [Broad field, e.g., "AI Adoption in Organizations"]
   2.2 [Narrower, e.g., "From Automation to Augmentation: The Agent Paradigm"]
   2.3 [Your specific niche, e.g., "Implementation Strategies for GenAI Systems"]
   2.4 [Theoretical framing]
```

**Option C — For Systematic Literature Reviews**
```
2. Conceptual Background
   2.1 [Key concept definitions]
   2.2 [Prior reviews and their limitations]
```

### Subsection Writing Template

Each subsection should follow this pattern:

```
[Opening sentence: Define the concept or state the subsection's purpose]

[Body: 2-4 paragraphs reviewing key papers. For each paper or cluster of papers:]
  - What they studied
  - How they studied it (method)
  - What they found
  - How it relates to YOUR study

[Closing sentence: Transition to the next subsection or identify what's missing]
```

Concrete paragraph template for reviewing papers:
```
[Author] (Year) [examined/investigated/developed] [what] using [method] 
in [context]. Their findings [suggest/reveal/demonstrate] that [key finding]. 
[Optional: This is consistent with / contrasts with Author2 (Year) who found [X].] 
While this work provides important insights into [aspect], it does not address 
[what your paper addresses / the context your paper examines].
```

### Theory Application Paragraph Template

```
We draw on [Theory] (Originator, Year) to frame our investigation. [Theory] 
posits that [core argument in 2-3 sentences — the actual mechanism, not just 
the theory name]. This lens is particularly appropriate for studying [your topic] 
because [2-3 reasons: (1) fit with phenomenon, (2) gap in theory application, 
(3) prediction/explanation it enables]. Specifically, [theory concept A] 
corresponds to [your construct/phenomenon A], while [theory concept B] 
illuminates [your construct/phenomenon B]. By applying [Theory] to 
[your context], we extend its explanatory reach to [new domain].
```

---

## METHODOLOGY (Target: 2000-3000 words journal, 1000-1500 conference)

### Structure depends on method — see method-engine skill for details.

### Universal Opening Paragraph Template:
```
To address our research question(s), we [adopted/employed] a [method name] 
approach. This approach is appropriate because [2-3 reasons: nature of the 
phenomenon, state of existing knowledge, type of contribution intended] 
(Methodological reference, Year). [If applicable: Following the guidelines 
of Author (Year), we structured our research process in [N] phases: 
[list phases briefly].]
```

---

## RESULTS / FINDINGS (Target: 2000-4000 words)

### For Qualitative Studies:
Present findings organized by themes/categories. Each theme:
```
**[Theme Name]**

[Introduction sentence: what this theme captures]

[Evidence paragraph 1: Present data with representative quotes]
  "Direct quote from interview/document" (Participant ID / Document reference).
  [1-2 sentences interpreting the quote]

[Evidence paragraph 2: Additional evidence, potentially contrasting]

[Summary sentence: What this theme means for the overall picture]
```

### For Quantitative Studies:
```
[Descriptive statistics paragraph]
Table [N] presents descriptive statistics and correlations for all variables.
[Highlight notable patterns]

[Main analysis paragraph]
We tested our hypotheses using [method]. [H1: result]. [H2: result]. [H3: result].
Table [N+1] summarizes the results.

[Additional analyses paragraph]
To test the robustness of our findings, we [robustness check].
```

### For Systematic Literature Reviews:
```
[Descriptive results: N papers found, by year, by method, by venue, by topic]
[Thematic synthesis organized by your concept matrix categories]
[Visual: concept matrix table, temporal distribution chart]
```

### For DSR:
```
[Artifact description: architecture, components, design principles]
[Demonstration: usage scenario, walkthrough]
[Evaluation results: method applied, findings]
```

---

## DISCUSSION (Target: 2000-3000 words journal, 1000-1500 conference)

### The 5-Block Formula

**Block 1 — Summary (1 paragraph)**
```
This study set out to [restate purpose]. Through [method], we [key finding summary 
in 2-3 sentences]. Our results [confirm/challenge/extend] [prior understanding] and 
offer new insights into [specific aspect].
```

**Block 2 — Discussion of Key Findings (2-4 paragraphs)**
For EACH major finding:
```
[Finding statement]. This result [is consistent with / contradicts / extends] 
prior research by [Author(s)] (Year) who found [their finding]. A possible 
explanation for [your finding / the difference] is [your interpretation]. 
This suggests that [broader implication for the field].
```

**Block 3 — Theoretical Implications (1-2 paragraphs)**
```
Our findings have several implications for [theory/literature stream]. First, 
[specific theoretical implication — not just "we extend theory X" but HOW]. 
[2-3 sentences elaborating]. Second, [implication 2]. This [challenges/refines/
supports] the assumption in [Theory] that [specific assumption].
```

**Block 4 — Practical Implications (1-2 paragraphs)**
```
For practitioners, our findings suggest [actionable insight 1]. Specifically, 
[concrete recommendation]. Furthermore, [actionable insight 2]. Organizations 
seeking to [goal] should [specific guidance based on findings].
```

**Block 5 — Limitations & Future Research (1-2 paragraphs)**
```
This study is not without limitations. First, [limitation 1 — be honest and specific, 
not formulaic]. This constrains [what aspect of generalizability/validity]. Future 
research could address this by [specific suggestion]. Second, [limitation 2]. 
Additionally, our study opens several avenues for future investigation: [2-3 specific, 
non-obvious future research questions].
```

---

## ABSTRACT (150-250 words, write LAST)

### Why the Abstract Matters More Than You Think

AI research agents (Codex, Claude, Semantic Scholar recommender, Elicit, etc.) screen
papers by reading **abstracts only**. They rarely access full text — paywalls, token
limits, and API constraints mean the abstract is often *the* paper from an agent's
perspective. A vague or jargon-heavy abstract makes a paper invisible to automated
research workflows.

**Design principle:** Write the abstract so that a research agent can extract the
research question, method, domain, key finding, and contribution in a single pass
without reading anything else.

### Template (Structured for Agent Discoverability)

```
[1 sentence: Context/Motivation — name the domain explicitly]
[1 sentence: Problem/Gap — state what is unknown or unresolved]
[1 sentence: Purpose — "This study [verb]..." with concrete scope]
[1-2 sentences: Method — name the approach, data source, and sample]
[2-3 sentences: Key findings — include concrete results, numbers where available]
[1 sentence: Contribution/Implication — what changes because of this work]
```

### Agent-Readability Rules

1. **Name the domain in the first sentence.** Not "organizations face challenges"
   but "enterprise software teams face challenges." Agents match on domain terms.
2. **State the research question explicitly.** Not "we explore implications" but
   "we investigate whether X leads to Y." Agents filter on parseable RQs.
3. **Include the method and data source by name.** Not "qualitative methods" but
   "semi-structured interviews with 24 IT managers" or "fine-tuned LLaMA-3-8B on
   12,000 StackOverflow posts." Agents use method terms for screening queries.
4. **Report at least one concrete finding.** Not "results show significant effects"
   but "adoption increased task completion by 34% (p < .01)." Agents rank specificity.
5. **Avoid jargon without grounding.** If you must use a framework name, briefly
   explain it: "Drawing on affordance theory (the actionable properties technology
   offers users), we find..." — agents cannot resolve undefined acronyms or niche
   framework names.
6. **Front-load keywords.** The first 50 words carry disproportionate weight in
   semantic search. Put the topic, method, and domain there — not throat-clearing.
7. **Use structured abstract format when the venue permits.** Labeled sections
   (Objective / Method / Results / Conclusion) are trivially parseable by agents
   and increasingly common in IS, medical, and CS venues.

### Anti-Patterns (Agent Invisibility)

| Pattern | Problem | Fix |
|---------|---------|-----|
| "This paper contributes to the literature on..." | No searchable content | Lead with the finding |
| "Results are discussed in light of..." | Deferred meaning — abstract says nothing | State the result |
| "We use a mixed-methods approach" | Too vague for method-based filtering | Name the specific methods |
| "Implications for theory and practice are drawn" | No concrete takeaway | State the implication |
| "Drawing on [Framework], we explore..." | Explore ≠ finding; framework may be unknown | State what you found |

---

## STYLE RULES

### Always:
- Write in past tense for what was done, present tense for established facts
- Hedge appropriately: "suggests" not "proves", "indicates" not "shows conclusively"
- Use transitions between paragraphs: "Building on...", "In contrast...", "Furthermore..."
- Cite sources for ALL non-trivial claims
- One idea per paragraph

### Never:
- Start a sentence with "It is important to note that..."
- Use "In today's fast-paced world..."
- Write "Many scholars have studied..." without naming them
- Use bullet points in the actual paper text (prose only)
- Over-hedge: "It might possibly suggest that perhaps..."

### German-Language Papers:
- Wissenschaftlicher Schreibstil: sachlich, präzise, unpersönlich
- "Es wurde untersucht..." statt "Ich habe untersucht..."
- Gendern nach Vorgabe des Journals/der Konferenz
- Fachbegriffe bei Erstverwendung definieren

---

## STYLE ANALYSIS MODE

When activated via `/analyze-writing`, perform a **diagnostic analysis** (not a drafting task).
Read the paper and evaluate each section against these metrics:

### Metric 1: Passive Voice Ratio
- **Target:** < 30% of sentences per section
- **Detection:** Identify auxiliary + past participle patterns ("was conducted", "were analyzed", "has been shown")
- **Note:** Some passive is acceptable (method sections often 40-50%). Flag only when overused in Introduction/Discussion.

### Metric 2: Weak Openings
Flag sentences beginning with:
- "It is important to note that..."
- "There are several..."
- "In today's [fast-paced/digital/modern] world..."
- "It should be mentioned that..."
- "Many scholars have studied..."
- "As everyone knows..."
- "It goes without saying that..."
- **Fix pattern:** Rewrite with subject-verb-object structure. Lead with the actor or finding.

### Metric 3: Hedging Balance
- **Under-hedging** (too assertive): "This proves...", "This clearly demonstrates...", "This is the first study to..."
- **Over-hedging** (too timid): "It might possibly suggest that perhaps..."
- **Target:** Appropriate hedging — "suggests", "indicates", "our findings are consistent with"
- **Score:** Count hedge words per paragraph. < 1 = under-hedged, > 3 = over-hedged.

### Metric 4: Sentence Length Variation
- **Target:** Average 15-25 words per sentence, with variation (SD > 5 words)
- **Problem signs:** All sentences same length (monotonous), sentences > 40 words (hard to parse), sequences of 5+ short sentences (choppy)
- **Fix pattern:** Mix short declarative sentences with longer ones. Break sentences > 40 words.

### Metric 5: Word/Phrase Repetitions
- Flag the same non-trivial word used 3+ times in consecutive sentences
- Flag the same sentence opener pattern used 3+ times in a paragraph
- Exclude common academic terms (e.g., "study", "research", "findings")
- **Fix pattern:** Use synonyms or restructure sentences

### Metric 6: Paragraph Length
- **Target:** 4-8 sentences per paragraph
- **Problem signs:** Single-sentence paragraphs (underdeveloped), 10+ sentence paragraphs (needs splitting)
- **Exception:** Method sections may have shorter procedural paragraphs

### Metric 7: Transition Quality
Between paragraphs, check for:
- **Explicit transitions:** "Building on...", "In contrast...", "Furthermore...", "However..."
- **Logical flow:** Does each paragraph's opening connect to the previous paragraph's closing?
- **Section transitions:** Does each subsection end with a bridge to the next?
- **Score:** Count paragraphs without any transition. Target: < 20%

### Metric 8: Citation Integration Style
- **Parenthetical citations:** "(Author, Year)" at sentence end — factual support
- **Narrative citations:** "Author (Year) found that..." — when discussing a specific study
- **Target ratio:** 60-70% parenthetical, 30-40% narrative (varies by section)
- **Problem signs:** All parenthetical (reads like a list), all narrative (reads like a book report), citation clusters of 5+ references (reviewer may question if author read all)

### Output Format

```markdown
# Writing Quality Analysis

**Paper:** [filename]
**Analyzed:** [date]
**Total word count:** [N]

## Section Scores

| Section | Passive Voice | Weak Opens | Hedging | Sent. Length | Repetitions | Para. Length | Transitions | Citation Style | Overall |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Abstract | [%] | [n] | [score] | [avg±sd] | [n] | [avg] | — | [ratio] | [★/★★/★★★] |
| Introduction | [%] | [n] | [score] | [avg±sd] | [n] | [avg] | [%] | [ratio] | [★/★★/★★★] |
| Theory | [%] | [n] | [score] | [avg±sd] | [n] | [avg] | [%] | [ratio] | [★/★★/★★★] |
| Method | [%] | [n] | [score] | [avg±sd] | [n] | [avg] | [%] | [ratio] | [★/★★/★★★] |
| Results | [%] | [n] | [score] | [avg±sd] | [n] | [avg] | [%] | [ratio] | [★/★★/★★★] |
| Discussion | [%] | [n] | [score] | [avg±sd] | [n] | [avg] | [%] | [ratio] | [★/★★/★★★] |

★★★ = Strong | ★★ = Adequate | ★ = Needs Work

## Specific Improvements

### [Section Name] — [Overall Score]

**Issue 1: [Metric name]**
> "[Problematic text from the paper]"
→ Suggested rewrite: "[Improved version]"
Reason: [brief explanation]

**Issue 2: [Metric name]**
> "[Problematic text]"
→ Suggested rewrite: "[Improved version]"

[... repeat for each issue found ...]

## Summary

**Strengths:** [2-3 strengths across the paper]
**Priority improvements:** [top 3 issues to fix first]
**Estimated revision effort:** [light / moderate / substantial]
```
