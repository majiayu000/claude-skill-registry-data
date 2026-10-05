---
name: research-tech
description: Research any technical / developer topic online — libraries, errors, best-practice/how-to, tool·library·model comparisons, product capabilities, and ecosystem/community signal. Use when you'll act on the answer as a developer (write code, debug, choose a tool). For non-technical topics (science, history, consumer, personal, fact-check) use `research-general`.
argument-hint: <topic, error message, or "X vs Y">
effort: medium
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Research Tech

Research any technical topic from multiple angles using parallel sub-agents, with critical evaluation of source credibility. Covers the full developer surface: implementation and debugging, best practices, **comparing/choosing tools, libraries, models, or services**, checking what a product or platform can do, and reading ecosystem sentiment — not just code and errors.

For a genuinely non-technical question (science, history, news, policy, consumer purchases, personal decisions, fact-checking a claim), use `research-general` instead — it leads with encyclopedic/academic/news/primary sources rather than docs and StackOverflow.

## Usage

```
research-tech <library> <what you want to do>
research-tech "<error message>" <library>
research-tech how to implement auth in react-navigation v7
research-tech Redux vs Zustand for large app
research-tech does Airship support transactional emails
research-tech best open-weight coding models on OpenRouter by cost/quality
```

## Gotchas
- Context7 docs may lag behind a recent major release. Check which version is documented before citing it as authoritative.
- "Prefer recent, then higher authority" can be wrong: an authoritative maintainer comment from 18 months ago may be more correct than a popular blog post from last month. Weigh authority first for stable libraries.
- Quick mode may miss nuance. If a "simple" question turns out complex (e.g., "default port" depends on framework integration), note it and suggest re-running in Standard mode.
- GitHub star counts are trivially inflated (~6M suspected fake stars as of 2024) — never cite a star count as evidence of quality, adoption, or trust without vetting it. See `references/fake-stars.md`.

## Workflow

### Step 1: Parse Input

Extract: **library/framework**, **error message** (if any, usually quoted), **version**, **goal/intent**, **problem description** (debugging), **comparison targets** (if "X vs Y").

### Step 2: Classify Query Depth

| Mode | When | Behavior |
|------|------|----------|
| **Quick** | Simple factual lookup, single API question, "what version supports X", "how to do X" with well-known library | Skip internal docs check. Spawn only Docs + General. Skip follow-up loop and critique. |
| **Standard** | Comparisons, best practices, errors, complex implementation, "real world experience", debugging | Full workflow including follow-up loop and adversarial critique |
| **Product/Market** | Choosing/evaluating a tool, service, platform, or model; "does X support Y" capability lookups; pricing/ROI; benchmarks; ecosystem sentiment | Full workflow, but lead with **Product/Market**, **Comparison**, **Reddit**, and **News** — skip Docs/StackOverflow-first instinct; official docs here are for capability confirmation, not implementation. |

When in doubt, use Standard. When the question is "which should I use / can it do X / is it any good" rather than "how do I build/fix it", use Product/Market.

### Step 3: Check Context and Resolve Scope

For Standard and Product/Market work tied to a project, read relevant `docs/`, manifests,
and conversation context before external research. Reuse a brief already supplied by
`evaluate-tech`, `longshot`, or another caller.

If an unresolved decision would materially change the investigation, invoke
`blind-spots` on the research brief before dispatching researchers. Supply the context
already gathered and distinguish the intended outcome (learn, compare, implement, or
debug) from the facts to establish. For example, "research authentication" may need a
purpose and target environment; "does this provider support passkeys?" is a factual
lookup. A short direct lookup may be needed to frame unfamiliar options first.

Use the returned purpose, scope, constraints, and priorities to focus the research.
Clear lookups and settled briefs proceed without an interview or confirmation. A
lookup assigned during an active `blind-spots` interview answers its narrow question
and returns evidence or a scope blocker to the caller; it does not open another interview.

### Step 4: Spawn Agents in Parallel

Pick the relevant agents and launch each batch together as runtime capacity allows. Include the settled brief and each worker's factual question in every prompt. Workers return new scope blockers to you instead of interviewing the user. Each captures source metadata: URL, date, source type, and (for community sources) engagement signals.

**Dispatch research workers with read/search/fetch tools and no file edits.** Disable delegation tools for ordinary workers where supported; read-only access alone does not prevent delegation, and available tools vary by harness. If a branch needs a coordinator, its brief must name the subtasks, bound all descendants, and define when to stop. Include those descendants in the main agent's allocation.

**One focused assignment per worker.** Give it a concrete question and a stopping condition. Coordinators receive an explicit decomposition; workers do the assigned research themselves.

**The table is a menu.** Pick the smallest useful set of complementary perspectives. Briefly state a larger decomposition, including any nesting, and queue work within the runtime concurrency limit. Additional agents do not require approval solely because of their count.

| Agent | Spawn when | Search strategy |
|-------|------------|-----------------|
| **Docs** | Library/framework mentioned | Context7 `resolve-library-id` then `query-docs`. Fall back to `{lib} official documentation {goal}`. |
| **GitHub** | Library with known repo | `site:github.com {lib} "{terms}"`, then WebFetch top 2-3 (github.com works fine with WebFetch). |
| **General** | Always | `how to {goal} {lib}`. |
| **Specific** | Error message provided | `"{exact_error_message}" {lib}`. |
| **StackOverflow** | Common problem/implementation pattern | `site:stackoverflow.com {lib} {keywords}`, then `mcp__jina__read_url` top answers (SO is JS-heavy). |
| **Changelog** | Version mentioned OR "stopped working" / "after upgrade" | `{lib} {version} changelog breaking changes migration`. |
| **Best Practices** | Feature implementation (no error) | `{lib} best practices {goal}` + `{lib} recommended architecture {goal}`. |
| **Reddit** | Comparison, best practices, "real world experience", ecosystem sentiment | `site:reddit.com {lib} {keywords}`, then `mcp__jina__read_url` top 2-3 (Reddit is JS-heavy). |
| **Comparison** | "vs", "or", "compare", "which", "best library" | `{A} vs {B} {context}`. |
| **Product/Market** | Evaluating/choosing a product, platform, tool, or model; capability lookup ("does X support Y"); pricing/ROI; benchmarks | `{product} {capability} documentation`, `{product} pricing`, `{A} vs {B} {year}`, independent benchmark sites, plus News for launches/deprecations. Confirm capabilities against official product pages/changelogs; weight independent benchmarks and community threads over vendor claims. |
| **News** | Launches, deprecations, funding/acquisition, "is X still maintained" | WebSearch recent + `{product} news {year}`, then `mcp__jina__read_url` top 2-3. |

**Fetching**: prefer `mcp__jina__read_url` for JS-heavy pages (modern docs, SPAs); `WebFetch` for plain HTML and github.com. See "Web Fetching" in CLAUDE.md. `WebSearch`/`WebFetch` are Claude Code's tool names — on another harness, use its equivalent search and fetch tools.

For full agent prompts, see `references/agent-prompts.md`.

### Step 5: Deduplicate and Note Convergence

Wait for agents, deduplicate by URL/issue (keep richest metadata). Note when independent agents found the same source — convergence raises confidence.

### Step 6: Critical Evaluation

**Recency** (adjust by library velocity):

| Age | Fast-moving (React, Next.js) | Stable (Express, lodash) |
|-----|------------------------------|--------------------------|
| < 6 months | High | High |
| 6-18 months | Medium | High |
| 18-36 months | Low | Medium |
| > 3 years | Very Low | Low |

**Authority:**

| Source Type | Score |
|-------------|-------|
| Official docs, changelogs, core team posts, GitHub issues with maintainer response | High |
| GitHub issues (community), recent blogs (named author), SO answers (accepted + >10 votes), comparison articles | Medium |
| Reddit threads (>50 upvotes or multiple experienced replies) | Medium |
| SO answers (not accepted, <10 votes), old blogs, old comparisons | Low |
| Reddit threads (<10 upvotes), random forums | Very Low |

**Popularity signals (don't trust raw star counts):** if a recommendation leans on a library being "popular"/"the standard"/"most-starred" — especially in comparisons or "is this repo trustworthy" questions — a GitHub star count is a vanity metric that is trivially bought and is not evidence of quality or adoption. Cross-check with harder-to-fake signals (fork-to-star ratio, external contributors, production dependents) before weighting it. Quick tell: **>10k stars with a fork-to-star ratio under ~5% is suspicious.** Full checklist and tools in `references/fake-stars.md`.

**Conflicts:** Prefer more recent, then higher authority. If official docs conflict with recent issues, the issue may reveal a bug or undocumented behavior.

### Step 7: Follow-Up Loop (Standard only)

If a topic area has fewer than 2 sources or the core question is unanswered: identify the gap, generate 1-2 delta queries (more specific terms, alternative terminology, broader scope), spawn 1-2 follow-up agents (read-only, same as Step 4), merge.

**Max 1 cycle.** If the gap persists, mark as low confidence.

**Reuse the allocation.** Reuse a worker when practical, and keep follow-ups focused on the named gap. Include descendants and advisor calls in the same task accounting; a new round does not reset a spending limit. Stop when further sources only repeat the findings.

### Step 8: Adversarial Critique (Standard only)

Brief self-challenge:
- What would a disagreer cite?
- Over-weighting one source type? (all blogs, no official docs)
- "Independent" sources tracing to one origin? (3 blogs citing one tweet = 1 source)
- Is the recommended approach the simplest, or are we over-engineering?

If the critique reveals a blind spot, adjust and lower confidence.

### Step 9: Present Results

**Lead with the synthesis**, not the raw data. Structure:

1. **Synthesis** — goal, recommended approach, key findings weighted by credibility, **1-3 most influential references** with URLs.
2. **Supporting Details** — only sections relevant and not already covered in the synthesis.

Available detail sections (include only relevant): Documentation · GitHub Issues & Discussions · Reddit · Comparison · Specific Error Matches · Version/Changelog · Conflicts.

For the full output template, see `references/output-format.md`.

## Examples

"Research authentication" with no established goal first goes through `blind-spots`
to settle the purpose and target environment. "Does this provider support passkeys?"
proceeds directly to capability research. An implementation brief already settled by
`longshot` proceeds with that scope.

| # | Query | Spawns |
|---|-------|--------|
| 1 | `research-tech how to implement authentication in Next.js 14` | Docs, GitHub, General, Best Practices, StackOverflow |
| 2 | `research-tech Redux vs Zustand for large React app` | Docs (both), General, Comparison, Reddit, StackOverflow |
| 3 | `research-tech "Cannot read property 'navigate' of undefined" react-navigation` | Docs, GitHub, General, Specific, StackOverflow |
| 4 | `research-tech auth navigation not working in react-navigation v7` | Docs, GitHub, General, Changelog, StackOverflow |
| 5 | `research-tech best practices for folder structure in Express API` | Docs, General, Best Practices, Reddit, StackOverflow |
| 6 | `research-tech what's the default port for Vite dev server` | Quick mode: Docs + General only |
| 7 | `research-tech does Airship support transactional emails` | Product/Market mode: Product/Market, News, General (capability lookup — not implementation) |
| 8 | `research-tech best open-weight coding models on OpenRouter by cost/quality` | Product/Market mode: Product/Market, Comparison, Reddit, News (benchmark/ROI) |

## Troubleshooting

**Agent fails or times out** — Continue with remaining agents. Note the gap in the synthesis.

**No results found** — Widen search terms: try without the library name, use alternative terminology, or search for the underlying concept.

**All sources are outdated** — Flag explicitly. Note dates and recommend verifying against current docs.

**Sources conflict** — Weight by recency and authority. Note the conflict and resolution explaining which to trust and why.
