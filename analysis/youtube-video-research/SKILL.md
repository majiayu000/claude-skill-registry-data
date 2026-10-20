---
name: youtube-video-research
description: "Enhance any deep research task with first-hand YouTube video evidence via manus-analyze-video. Highly recommended whenever the task involves deep research, investigation, report writing, industry analysis, competitive intelligence, market research, technology trends, cultural analysis, policy research, or any information-gathering task that would benefit from expert talks, interviews, keynotes, panels, documentaries, product demos, vlogs, or conference presentations on YouTube. Also use when the user explicitly mentions YouTube, video sources, or asks for first-hand evidence. YouTube contains unfiltered first-person insights (CEO interviews, expert panels, practitioner vlogs, conference talks, earnings calls) unavailable in text articles, making it a critical primary source for virtually any research topic."
compatibility: opencode
---

# YouTube Video Research

Leverage YouTube as a **primary source of first-hand information** for research tasks. YouTube hosts CEO interviews, founder keynotes, earnings calls, expert panels, conference talks, product demos, practitioner vlogs, cultural documentaries, policy discussions, technical deep-dives, and educational content that contain unfiltered, first-person insights unavailable in text articles. This skill orchestrates video discovery, analysis, and synthesis into a structured research workflow.

## Trigger Guidance

This skill is **highly recommended for deep research tasks**, not just travel, company, or person research. 

**Explicit trigger** — the user mentions YouTube, video sources, interviews, keynotes, vlogs, podcasts, conference talks, or asks for first-hand evidence.

**Implicit trigger** — any research, investigation, or report-writing task where YouTube videos would materially improve the answer by providing first-hand evidence. This includes but is not limited to:

| Research category | Why YouTube adds value | Example topics |
|---|---|---|
| Industry / market analysis | Expert panels, analyst deep-dives, conference talks | AI chip market, fintech trends, SaaS landscape |
| Company research / due diligence | CEO interviews, earnings calls, product demos | Startup investigation, competitor analysis |
| Technology trends | Conference presentations, developer talks, demos | AI models, database comparisons, dev tools |
| Policy / regulatory research | Panel discussions, government hearings, legal podcasts | EU AI Act, export controls, central bank policy |
| Person / public-figure profiling | Interviews, podcast appearances, keynotes | Founder profiles, researcher tracking |
| Travel / destination research | Vlogs, local guides, cost breakdowns | City guides, accommodation reviews |
| Cultural / entertainment analysis | Documentaries, reviews, fan analysis, creator content | Anime impact, music history, game design |
| Financial / economic research | Economist talks, earnings calls, market analysis | Stock valuation, capital flows, real estate |
| Science / academic topics | Lectures, conference presentations, lab tours | Protein design, climate research |
| Product / tool comparison | Review videos, hands-on demos, user testimonials | Software tools, hardware, consumer products |

If the research topic exists, there are almost certainly relevant YouTube videos. **Default to using this skill** for comprehensive research rather than defaulting to skip it.

## Core Tools

| Tool | Purpose | When to use |
|---|---|---|
| `search` (type: `info` or `news`) | Discover YouTube videos and gather web context | Always; first step in every research task |
| `manus-analyze-video` | Analyze YouTube video content with multimodal LLM | After discovering relevant videos; the core analytical tool |
| `search` (type: `research`) | Find academic papers, industry reports for cross-validation | When rigorous sourcing is needed |
| `webpage_extract` or browser | Read articles, transcripts, show notes linked from videos | When supplementary text context is needed |

## Core Workflow

Every research task follows this five-step loop. Repeat steps 2-4 for each relevant video.

### Step 1: Theme-Based Video Discovery

Before searching, decompose the research goal into **distinct research themes**. Each theme becomes a separate search-and-analysis unit. This ensures broad coverage and prevents tunnel vision on a single angle.

**Theme decomposition process:**

1. Identify 4-6 research themes from the user's request (e.g., for a company investment analysis: "industry background", "business model & technology", "financial data & valuation", "customer & partnerships", "bull case & growth catalysts", "bear case & risk factors").
2. For each theme, run 1-2 targeted YouTube search calls.
3. Select **2-3 videos per theme** to ensure multiple perspectives on each dimension.
4. Total target: **12-20 videos** for deep research, **8-12** for standard research. The power of this workflow lies in **high video volume** across diverse themes.

**Theme decomposition examples:**

| Research goal | Themes | Videos per theme |
|---|---|---|
| Company investment analysis | Industry context, Business model, Financials, Customers, Bull case, Bear case | 2-3 each = 12-18 total |
| Technology comparison | Architecture, Performance benchmarks, Developer experience, Production use cases, Cost analysis | 2-3 each = 10-15 total |
| Market entry research | Market size, Competitors, Regulatory landscape, Customer needs, Distribution channels | 2-3 each = 10-15 total |
| Person profile | Career history, Leadership style, Public controversies, Vision & philosophy, Peer assessments | 2-3 each = 10-15 total |

**Query construction rules:**

- Always include `YouTube` in at least one query variant.
- Include the content type: `interview`, `talk`, `panel`, `keynote`, `vlog`, `earnings call`, `podcast`, `review`, `documentary`, `demo`, `conference`, `lecture`, `analysis`, `deep dive`.
- Include the entity name: person, company, destination, product, topic.
- Use 2-3 query variants per search call to maximize coverage.
- **Vary query angles per theme**: e.g., for "bear case" theme, search for `[company] risks concerns analysis YouTube`, `[company] stock bearish case YouTube`, `[company] problems criticism YouTube`.

**Examples across research types:**

| Research goal | Query variants |
|---|---|
| Company research on Stripe | `Stripe CEO Patrick Collison interview YouTube`, `Stripe company culture keynote YouTube`, `Stripe product demo YouTube` |
| AI industry trends | `AI industry trends 2025 expert panel YouTube`, `AI market analysis conference talk YouTube`, `AI startup landscape deep dive YouTube` |
| Policy research on EU AI Act | `EU AI Act impact analysis YouTube`, `EU AI regulation panel discussion YouTube`, `AI compliance legal expert talk YouTube` |

For **company research**, prioritize videos featuring the **top leader (CEO/founder/principal executive)**. Search patterns:

- `[CEO name] interview YouTube`
- `[CEO name] [company] keynote YouTube`
- `[company] earnings call YouTube`
- `[CEO name] podcast appearance YouTube`

### Step 2: Select and Prioritize Videos

From search results, select videos based on these criteria:

| Priority | Signal | Example |
|---|---|---|
| Highest | First-person: subject/expert speaking directly | Keynote, interview, podcast guest appearance, conference talk |
| High | Expert or insider perspective | Industry analyst, practitioner, local guide, researcher |
| Medium | Third-party quality coverage | Documentary, in-depth review channel, news feature |
| Lower | Aggregated or secondhand content | Compilation, reaction video, news summary |

Select **2-3 videos per theme** to ensure each research dimension has multiple perspectives. For deep research, total video count should reach **12-20 videos**. Prioritize recency unless historical context is specifically needed.

**Balance requirement**: Actively seek opposing viewpoints. For investment/company research, ensure at least 30% of videos present bearish/critical perspectives to avoid confirmation bias.

### Step 3: Analyze Videos with manus-analyze-video

Use `manus-analyze-video` to extract insights from the selected videos. 

**Syntax for manus-analyze-video:**

```bash
manus-analyze-video "<youtube_url>" "<analysis_prompt>"
```

#### Critical: High-Density Prompt Engineering

`manus-analyze-video` performs AI-based visual and audio analysis. Its output quality is **entirely determined by prompt design**. A/B testing shows that a structured, quote-demanding prompt yields **2.4x more content, 12 direct quotes vs 0, and 18 precise data points vs 6 vague mentions** compared to a generic "summarize" prompt — on the exact same video.

**Mandatory prompt rules:**

1. **NEVER use generic prompts** like "summarize this video" or "what are the key points". These produce thin, quote-free summaries.
2. **ALWAYS demand direct quotes**: Include explicit instructions like "Extract at least 8-10 near-exact quotes from the speaker, preserving their original wording in quotation marks."
3. **ALWAYS demand exhaustive data extraction**: "List ALL numbers, dollar amounts, percentages, dates, deadlines, company names, person names, and metrics mentioned."
4. **ALWAYS request structured sections**: Use labeled sections (A/B/C/D/E/F) so output is organized and parseable.
5. **ALWAYS include a sentiment/stance rating request**: "Rate the speaker's overall stance and note where they express uncertainty vs conviction."
6. **State that length is not a concern**: "Be exhaustive. Length is not a concern — information density is. Do not summarize when you can quote directly."

**Mandatory general-purpose prompt template:**

```
Extract MAXIMUM detail from this video about [topic/company]. For every claim
the speaker makes, capture their near-exact wording as a direct quote in
quotation marks. Include ALL numbers, dates, dollar amounts, percentages,
company names, and person names mentioned.

Structure output as:
(A) SPEAKER PROFILE: Name, credentials, disclaimers, sponsors.
(B) DIRECT QUOTES: At least 8 verbatim or near-verbatim quotes with topic labels.
(C) ALL DATA POINTS: Every number, metric, date, name as a numbered list.
(D) KEY ARGUMENTS: Main thesis broken into sub-arguments with supporting quotes.
(E) COUNTER-ARGUMENTS / RISKS: Every risk, caveat, or opposing view with quotes.
(F) SENTIMENT: Overall stance rating and confidence level.

Be exhaustive. Length is not a concern — information density is.
Do not summarize when you can quote directly.
```

See [references/prompt-templates.md](references/prompt-templates.md) for domain-specific high-density prompt templates.

#### Optional: Two-Pass Strategy for Maximum Fidelity

For critical videos where verbatim accuracy is essential (e.g., earnings calls, legal testimony, policy hearings), use a two-pass approach:

1. **Pass 1 — Raw transcript**: Run `manus-speech-to-text` on the video to get a verbatim text transcript.
2. **Pass 2 — Structured analysis**: Run `manus-analyze-video` with the high-density prompt for visual context, speaker identification, and structured extraction.
3. **Merge**: Cross-reference the raw transcript with the structured analysis to get both exact quotes and organized insights.

This is optional for most research but recommended when the user specifically needs exact wording or when the video contains dense financial data.

### Step 4: Cross-Validate with Web Search

After analyzing videos, use `search` tool (type: `info` or `news`) to:

- Verify factual claims made in videos.
- Fill gaps: dates, statistics, context not covered in videos.
- Find contradicting or supporting evidence from other sources.
- Get the latest updates if videos are older.

Do not treat video content as ground truth. Speakers may exaggerate, misremember, or present biased views. Cross-validation is mandatory for factual claims.

### Step 5: Synthesize into a Quote-Rich, Detail-Dense Report

Combine video analysis results and web research into a coherent deliverable. The final report MUST follow these **mandatory output rules**:

#### Rule 1: Direct Quotes Are Mandatory

Every major section of the report MUST include at least 2-3 **blockquote citations** of speakers' original words or closely paraphrased statements. Use Markdown blockquote syntax:

```markdown
> "The exact or closely paraphrased words from the speaker go here. This is what
> makes the report credible and vivid." [3]
```

Each blockquote MUST be attributed with a numeric citation linking to the source video in the References section. Acceptable attribution patterns:

- `> "Quote text here." [3]` — citation at end of quote
- Preceding paragraph names the speaker: `CEO Jake DeWitte explained in his NYSE interview:` followed by blockquote

**Minimum quote density**: At least **1 blockquote per 300 words** of report body. A 3,000-word report needs at least 10 blockquotes.

#### Rule 2: Detail Expansion Is Mandatory

Do NOT summarize video insights into single-sentence bullet points. Every key finding MUST be expanded into a full paragraph (3-5 sentences minimum) that includes:

- **Context**: Who said it, in what setting, and why it matters
- **Specifics**: Numbers, dates, names, technical details mentioned
- **Quote**: The speaker's own words as a blockquote
- **Implication**: What this means for the research question

**Bad example** (too brief):
> Oklo has a 14 GW customer pipeline.

**Good example** (properly expanded):
> At the 2025 KPMG Tech and Innovation Symposium, CEO Jacob DeWitte revealed that Oklo's customer pipeline has grown dramatically over the past 18 months, reaching 14,100 MW (14.1 GW). This figure is anchored by a 12 GW non-binding Master Power Agreement with Switch — one of the largest corporate clean energy agreements ever signed — along with a 1.2 GW prepayment-backed agreement with Meta and a 500 MW letter of intent from Equinix that included a $25 million prepayment. DeWitte emphasized the structural nature of this demand:
>
> > "Tech giants are looking for baseload power to fuel AI training and inference. Intermittent renewables simply cannot meet the 24/7 steady-state demands of data centers." [2]
>
> However, independent analysts caution that the vast majority of this pipeline consists of non-binding letters of intent that carry no legal obligation. [3]

#### Rule 3: Multi-Source Triangulation

When multiple videos address the same topic, present them as a dialogue — showing agreement, disagreement, or complementary perspectives. Do not just list each video's view sequentially; weave them into a narrative.

#### Rule 4: Structured Source Attribution

Always include:
- **Inline numeric citations** `[1]` `[2]` linking to the References section
- **Speaker identification** before quotes (name, title, credibility note)
- A **Source Videos Analyzed** table listing all videos

#### Output Structure

```markdown
# [Research Title]

## Executive Summary
[2-3 paragraphs with key findings, including at least 2 blockquotes from different sources]

## [Theme 1 Title]
[3-5 paragraphs per theme, each with blockquotes, specific data, and source attribution]

## [Theme 2 Title]
[Same depth as above]

## [Additional themes...]

## Source Videos Analyzed
| # | Title | Speaker/Creator | Stance | URL | Key Contribution |
|---|---|---|---|---|---|

## References
[1]: [Video/source title and URL]
[2]: [Video/source title and URL]
...
```

Adapt this structure based on the specific research type. See reference files for domain-specific output templates:
- [references/company-research.md](references/company-research.md)
- [references/person-research.md](references/person-research.md)
- [references/travel-research.md](references/travel-research.md)

## Multi-Video Synthesis Strategy

When analyzing multiple videos on the same topic, synthesize rather than list sequentially:

| Approach | When to use |
|---|---|
| Thematic synthesis | Group insights by theme across videos (e.g., "Strategy", "Culture", "Challenges") |
| Chronological narrative | Track evolution over time (e.g., founder's changing vision across interviews) |
| Comparative analysis | Videos present different perspectives on the same topic |
| Evidence triangulation | Build a factual picture from multiple partial sources |
| **Bull-bear dialogue** | Present opposing views as a structured debate with quotes from each side |

## Quality Safeguards

| Mistake | Correct behavior |
|---|---|
| Analyzing too few videos (< 8 for deep research) | Target 12-20 videos for deep research, 2-3 per theme. **High volume is the core value of this skill.** |
| Using generic "summarize" prompts | Use the mandatory high-density prompt template; MUST request 8+ direct quotes, ALL data points, and structured sections (A-F) |
| Writing a report without blockquote citations | MUST include ≥1 blockquote per 300 words of report body |
| Summarizing findings as brief bullet points | Expand every finding into 3-5 sentence paragraphs with context, data, quote, implication |
| Treating speaker claims as facts | Cross-validate with web search; label opinions vs. facts |
| Only including bullish/positive videos | Ensure ≥30% of videos present critical/bearish perspectives |
| Dumping raw analysis without synthesis | Weave multi-source insights into thematic narratives with quote dialogues |
| Forgetting to include video links | Always provide YouTube URLs in the Source Videos table and References |
| **Analysis Failure (e.g., video deleted, no transcript, too long)** | **Fallback:** Use `search` to find text summaries, articles, or alternative videos on the same topic. Do not halt the research process. |
