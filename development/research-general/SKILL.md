---
name: research-general
description: Research a non-technical topic online (science, history, news, policy, regional/regulatory, consumer purchases, personal decisions, fact-check). The default for research in non-code repos (e.g. a notes vault). For technical/developer topics — libraries, errors, tooling, and even choosing/evaluating dev tools or products — use `research-tech`.
argument-hint: <topic, question, or claim to verify>
effort: medium
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Research General

Research a general (non-programming) topic from multiple angles using parallel sub-agents, with critical evaluation of source credibility.

## Usage

```
research-general <question or topic>
research-general "<exact claim to verify>"
research-general what does the evidence say about screen time and adolescent sleep
research-general causes of the 2008 financial crisis
research-general nuclear vs solar economics for grid power
```

## Gotchas
- "Recent" doesn't mean "correct". For historical, philosophical, or settled empirical topics, a 30-year-old peer-reviewed paper can outweigh a recent op-ed. Weigh authority and topic-stability before recency.
- Wikipedia is **grounding, not authority** — follow its citations to primary sources before stating something as fact.
- Advocacy organizations and think tanks have a stance. Cite them as evidence of *what that side says*, not as neutral fact.
- **Affiliate-driven and SEO listicle sites** ("Top 10 Best X", coupon-hosting comparison sites) are biased toward whatever pays them. Weight independent test institutions and regulators above them.
- Quick mode may miss nuance. If a "simple" question turns out contested ("Is X healthy?" — depends on dose, population, endpoint), note it and suggest re-running in Standard.

## Workflow

### Step 1: Resolve the Research Brief

Extract: **topic**, **purpose** (understand, decide, or verify), **sub-questions / claims**,
**date scope**, **comparison targets and outcomes**, **region/locale**, **personal context**
when relevant, and **topic stability** (current / active research / established / historical).
Use the conversation, relevant supplied documents, and any brief from a calling workflow
to fill these in. These are context to consider, not a questionnaire to complete.

If an unresolved decision would materially change the investigation, invoke
`blind-spots` on the brief before answering or dispatching researchers. For example,
"research home batteries" may need a choice between an explanation and a purchase
comparison; region and priorities matter for the latter. A short direct lookup can
establish unfamiliar options before asking. Keep prices, capabilities, and empirical
claims as research questions, even when their answers are unknown.

Use the returned purpose, scope, constraints, and priorities to focus the research.
Clear lookups, explicit requests for an overview, and settled briefs proceed without
an interview or confirmation. A lookup assigned during an active `blind-spots`
interview answers its narrow question and returns evidence or a scope blocker to the
caller; it does not open another interview.

### Step 2: Check Existing Knowledge

Before spawning any agents, assess whether you can already answer well from training data:

- **High confidence** (well-established facts, stable domain): answer directly, note you didn't search, offer to research if the user wants verification.
- **Medium confidence** (good answer but maybe outdated, regionally wrong, or incomplete): proceed in **Quick mode** to verify and supplement.
- **Low confidence** (unfamiliar, rapidly changing, contested, or regulatory/regional specifics): proceed in **Standard mode**.

When in doubt, lean toward searching — but only if searching can plausibly improve the answer.

### Step 3: Classify Query Depth

| Mode | When | Behavior |
|------|------|----------|
| **Quick** | Well-known fact, one-shot lookup, or verifying medium-confidence existing knowledge | Encyclopedic + General only. Skip follow-up loop and critique. |
| **Standard** | Empirical, contested, comparisons, fact-checking, regional/regulatory, consumer research | Full workflow including follow-up loop and adversarial critique. |

When in doubt, use Standard. **Stop at diminishing returns** — if three agents return the same finding, broaden don't deepen.

### Step 4: Spawn Agents in Parallel

Pick the relevant agents from the table below and launch each batch together as runtime capacity allows. Include the settled brief and each worker's factual question in every prompt. Workers return new scope blockers to you instead of interviewing the user. Each agent captures source metadata: URL, date, source type, author/publisher, and (where it applies) sample/methodology, primary-vs-secondary, and **affiliate or sponsorship disclosure**.

**Dispatch research workers with read/search/fetch tools and no file edits.** Disable delegation tools for ordinary workers where supported; read-only access alone does not prevent delegation, and available tools vary by harness. If a branch needs a coordinator, its brief must name the subtasks, bound all descendants, and define when to stop. Include those descendants in the main agent's allocation.

**One focused assignment per worker.** Give it a concrete question and a stopping condition. Coordinators receive an explicit decomposition; workers do the assigned research themselves.

**The table is a menu.** Pick the smallest useful set of complementary perspectives. Briefly state a larger decomposition, including any nesting, and queue work within the runtime concurrency limit. Additional agents do not require approval solely because of their count.

| Agent | Spawn when | Search strategy |
|-------|------------|-----------------|
| **Encyclopedic** | Almost always | `site:en.wikipedia.org {topic}`, then `mcp__jina__read_url` top 1-2. Note cited sources as leads. |
| **Academic** | Scientific, scholarly, social-science, economic | `mcp__jina__parallel_search_arxiv` (STEM) or `parallel_search_ssrn` (econ/finance/law/social). Fall back to `{topic} systematic review meta-analysis`. |
| **News** | Current events, contemporaneous reporting | WebSearch filtered to NYT, BBC, Reuters, AP, Guardian, Economist, FT. Then `mcp__jina__read_url` top 2-3. |
| **Primary** | Statistics, regulatory, official positions | `{topic} site:.gov` / `site:.int` / `{org} report {topic}`. WebFetch for plain HTML/PDF. |
| **General** | Always | `{topic}` plain — explainers, longreads, expert blogs. |
| **Forum** | Opinion-heavy, lived experience, unsettled | `site:reddit.com {topic}`, then `mcp__jina__read_url` top 2-3 (Reddit is JS-heavy). |
| **Comparison** | "vs", "or", "compare", "which is better" | `{A} vs {B} {context}`. Flag affiliate / "Top 10" sites. |
| **Specific** | Exact claim/quote to verify (in quotes) | `"{claim}"` plus `"{claim}" fact check` and `"{claim}" debunked`. |
| **Historical** | Topic is historical | `{topic} primary sources` / `archive` / `declassified`. Try news archives. |
| **Regional** | Country/city/locale-specific (regulations, prices, services) | `{topic} site:{country_TLD}` plus locale-specific authority sites. **Search in the local language** for non-English locales. |

**Fetching**: prefer `mcp__jina__read_url` for JS-heavy pages; `WebFetch` for plain HTML, government PDFs, `.gov`/`.int`. See "Web Fetching" in CLAUDE.md. `WebSearch`/`WebFetch` are Claude Code's tool names — on another harness, use its equivalent search and fetch tools.

For full agent prompts including the Regional locale playbook (DE/FR/UK/US/AU), see `references/agent-prompts.md`.

### Step 5: Deduplicate and Note Convergence

Wait for agents, deduplicate by URL (keep richest metadata), and note when independent agents found the same source — convergence raises authority. **Watch for false convergence**: three blogs citing one tweet are *one* source, not three.

### Step 6: Critical Evaluation

**Authority:**

| Source Type | Score |
|-------------|-------|
| Peer-reviewed (esp. systematic reviews / meta-analyses), government statistics, primary documents, well-cited encyclopedia entries | High |
| Established outlets (NYT, BBC, Reuters, AP, Economist, FT), reputable books, official organization reports, established test institutions (Stiftung Warentest, Consumer Reports, Which?) | High |
| Working papers / preprints, named-expert blogs, Wikipedia (no dispute markers), think-tanks, recognized domain sites (Finanztip, Verbraucherzentrale) | Medium |
| Secondary outlets, op-eds by named experts | Medium |
| Reddit threads (>100 upvotes, substantive replies) | Medium-Low |
| Op-eds without expertise, advocacy-org claims about own cause, content marketing | Low |
| **"Top 10 Best X" affiliate listicles, SEO content farms**, low-engagement forums, social media | Very Low |

**Recency** (depends on topic):

| Topic Type | Threshold |
|-----------|-----------|
| Current events, market data, prices, active policy | < 1 month |
| Active research, contested empirical, public health, regulations | < 5 years preferred |
| Established science, well-settled history, mathematics | Mostly irrelevant |
| Historical / biographical / classical | **Primary sources beat recent commentary** |

**Conflicts:** First check if it's a real conflict or different scopes/populations/regions. Otherwise prefer higher authority, then more recent, then primary over secondary. A meta-analysis disagreeing with mainstream news usually wins on the empirical question — but news may correctly capture *what people believe*.

### Step 7: Follow-Up Loop (Standard only)

If a topic area has fewer than 2 sources or the core question is unanswered: identify the gap, generate 1-2 delta queries (alternative terminology, narrower/broader scope, primary-source angle, local-language variant), spawn 1-2 follow-up agents (read-only, same as Step 4), merge.

**Max 1 cycle.** If the gap persists, mark as low confidence in the synthesis.

**Reuse the allocation.** Reuse a worker when practical, and keep follow-ups focused on the named gap. Include descendants and advisor calls in the same task accounting; a new round does not reset a spending limit. Stop when further sources only repeat the findings.

### Step 8: Adversarial Critique (Standard only)

Brief self-challenge:
- What would a disagreer cite? Did the search find that?
- Over-weighting one source type? (all news, no academic — or vice versa)
- "Independent" sources tracing to a single origin? (3 articles citing one study = 1 source)
- Mistaking *what people say is true* for *what is true*?
- **Affiliate, sponsorship, or commercial COI** in any cited source?
- **Assuming a specific country / culture / population**? Verify regional applicability.
- **Survivorship bias** — only hearing from people who succeeded?
- Population/scope/endpoint mismatch between the question and the evidence?

If the critique reveals a blind spot, adjust and lower confidence.

### Step 9: Present Results

**Lead with the answer**, not the research process. Use **inline source counts** ("(3 sources)", "(1 source, low confidence)") instead of a separate Confidence block.

Structure:
1. **Direct answer** with inline source counts
2. **Key references** (1-3) — sources that most shaped the conclusion
3. **Supporting Details** — only sections that add value beyond the answer

Available detail sections (use only those that add value): Background · Evidence · News & Reporting · Comparison · Regional details · Claim Verification · Historical Context · Conflicts · Open Questions.

For the full output template, see `references/output-format.md`.

## Examples

"Research home batteries" with no established purpose goes through `blind-spots`.
"Explain how home batteries work" proceeds with an overview. A purchase comparison
with the location, budget, and priorities already supplied uses that brief directly;
product prices and availability are research tasks.

| # | Query | Spawns |
|---|-------|--------|
| 1 | `research-general what does the evidence say about screen time and adolescent sleep` | Encyclopedic, Academic, News, Forum, General |
| 2 | `research-general causes of the 2008 financial crisis` | Encyclopedic, Academic, News (archived), Primary (Fed/SEC), Comparison |
| 3 | `research-general nuclear vs solar economics for grid power` | Academic, Primary (gov energy data), Comparison, News, Encyclopedic |
| 4 | `research-general history of the Suez Canal crisis` | Encyclopedic, Historical, News (archived), Primary (declassified) |
| 5 | `research-general "humans only use 10% of their brain"` | Specific, Academic, Encyclopedic, General |
| 6 | `research-general best mattress brands in Germany price tiers` | Regional (DE), Comparison, Forum, General — flag affiliate listicles |
| 7 | `research-general options for risk-free investments in Germany` | Regional (DE), Primary (BaFin), Authority (Finanztip, Verbraucherzentrale) |
| 8 | `research-general what's the capital of Mongolia` | **Likely answered from existing knowledge.** If searching: Encyclopedic + General only. |

## Troubleshooting

**Agent fails or times out** — Continue with remaining agents. Note the gap in the synthesis.

**No academic sources found** — Try alternative terms (medical/scientific terminology often differs from lay language). If still nothing, note the empirical evidence base is thin.

**Sources disagree along ideological lines** — Separate the empirical claim from the value judgment. Find the underlying primary source. Present what each side argues, then what primary evidence supports — and note where disagreement is genuinely values-based.

**Topic is current and unsettled** — Flag explicitly ("active situation as of {date}; details may shift"). Prefer wire services (Reuters, AP) over editorial outlets.

**All consumer sources are affiliate-driven** — Search for independent test institutions for the locale (Stiftung Warentest, Consumer Reports, Which?, Choice). If none, note that available sources are commercial.
