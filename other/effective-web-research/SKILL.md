---
name: effective-web-research
version: "1.0.0"
user-invocable: true
description: "Effective web research discipline for AI agents — route first, then research with rigor. Step 0 triages whether a question needs external web lookup vs is answerable from the internal codebase/docs; when external, default mode auto-applies 4 maxims; on explicit 'strict/deep research' requests it runs a 7-dimension source-credibility evaluation (CRAAP + E-E-A-T) with an auditable report. When the static layer (WebSearch/WebFetch/curl) can't reach content (login-required / JS-rendered / anti-scraping like 小红书·公众号), it escalates to the real browser via the web-access skill (CDP, carries login state). Triggers: 「web 调研」「外部调研」「查资料」「有效调研」「严格调研」「深度调研」「严格查证」「登录态访问」「动态页面」「反爬」「这个库/框架怎么用」「有没有漏洞」「best practice 是什么」 / web research, look up, investigate, strict research, deep research, fact-check, login-state access, dynamic page, anti-scraping. Do NOT use for: searching the local codebase, reading repo files, grepping code."
---

# effective-web-research

Make every external web lookup **effective and credible**, and turn "deep research" requests into auditable, source-evaluated reports. Grounded in two established frameworks — **CRAAP** (decades of information-literacy science) and **Google E-E-A-T** (the web's dominant content-quality rubric) — so the rules are defensible, not opinionated.

This skill is about the **external web**. It does not compete with internal code-search tools.

## When to use / When NOT to use

**Use** when the agent is about to (or is asked to) gather information from the **external web** — official docs sites, third-party library docs, RFCs, reputable blogs, papers, real-world data.

**Do NOT use** for:
- Reading files inside the workspace/repo (`read`, `grep`, `ast-grep`)
- Navigating the local codebase (`LSP`, `goto_definition`, `explore` agent)
- Reading installed dependencies in `node_modules` / `venv` / `site-packages`
- Creating or editing documents

Those are internal search tasks with different tools and different quality bars.

---

## Step 0 — Triage: should this go external at all?

Before any web search, decide whether external research is even the right move. Many questions agents reflexively google are answerable faster and more reliably from the internal codebase. Going external when the answer is local wastes effort and introduces uncertainty.

| Task signal | Path | This skill's role |
|-------------|------|-------------------|
| Answer likely lives in the repo: our code logic, `AGENTS.md` conventions, existing skills, code comments, installed dependency source | **Internal first** — use `grep` / `read` / `LSP` / `explore`. Do not fire a web search. | Do not activate (a one-line "consider checking internal first" hint is fine) |
| About a third-party library / framework / external API / tool behavior / version-specific quirk | **External** — web research | Default mode (4 maxims) applies |
| Real-world information: news, market data, people, current events, papers | **External** | Default mode applies |
| Hybrid — external concept + internal application ("is the X library we use vulnerable to Y", "apply pattern X to our code") | **External-then-internal** — research the concept externally, then verify/apply internally | External stage uses default/strict; internal stage uses internal tools |
| Static layer can't reach the content (login required / JS-rendered / anti-scraping platform like 小红书·公众号) | **Escalate to CDP** via the `web-access` skill (runtime-checked; aborts with an install hint if web-access is absent) — real browser carries login state | web-access handles retrieval; this skill's credibility discipline still governs whatever is retrieved |

**Triage signals**:
- *Internal*: the question mentions "our / this project / this code / our convention", or the answer domain is clearly inside the repo.
- *External*: the question names a third-party lib/framework/API/tool with a version, or asks "how to use / how it works / best practice / is there a vulnerability" about an external thing.
- *Hybrid*: an external concept object + "our / apply to / check our" + an internal object.

> If unsure, prefer internal first — it's faster and authoritative for "our own" questions. Escalate to external only when internal search comes up empty.

---

## Escalation — when the static layer can't reach the content (CDP via web-access)

When WebSearch / WebFetch / curl / Jina return content that **lacks the target information** because the page refuses non-browser clients (login wall, JS-rendered shell, anti-scrape block on platforms like 小红书·公众号), load the **`web-access`** skill and follow its CDP guidance — it connects to the user's daily browser (login state native) and reaches the content via its curl HTTP API.

This is a **runtime-local** dependency, not a frontmatter `dependencies` entry: the core research discipline works without `web-access`, and upstream workflows (known-issue-research → solve-workflow family) stay free of any external-plugin requirement. Verify `web-access` only when you actually escalate; if missing, abort and tell the user how to install it (no silent fallback).

Retrieval is orthogonal to credibility — the 4 maxims / strict mode still evaluate whatever content CDP retrieves. For the escalation decision tree + curl API cheat sheet, see [reference.md · CDP upgrade](reference.md#cdp-upgrade).

---

## Default mode — 4 maxims (applied to every web search within an active task)

When this skill is active for a task, apply these to every web search / `webfetch` you perform during that task. (Skills activate per-task when their description matches — these maxims then govern every search inside that task, not searches in unrelated tasks.) No extra artifact is produced. They exist because the web is full of outdated, low-authority, copied, and AI-generated content — without discipline, agents amplify the noise.

### 1. Authority-first

**Source priority**: official docs/sites ＞ authoritative secondary (MDN, official blogs, RFC/spec) ＞ reputable community (high-vote StackOverflow answers, the official repo's issues/PRs) ＞ general web.

**Apply**: when web-search results come back, scan the **domain first** — is it the official site (`react.dev`, `developer.mozilla.org`, `nodejs.org`, `<lib>.<org>`)? Read those before generic blogs.
**Why it matters**: a 2019 blog's take on React Hooks is inferior to `react.dev`'s own documentation, yet search engines may rank the blog higher.

### 2. Currency check

For **fast-moving topics** (frameworks, APIs, tools, security), find the page's publish/update date before trusting it. Content older than ~2 years is "possibly stale" — verify the claim against the official current-version docs.

**Apply**: after `webfetch`, look for "Last updated" / article date / `<time>` tags. A page with no date at all is suspect — treat as stale until proven otherwise. **Exception**: official living-reference doc sites (`react.dev/reference/*`, `developer.mozilla.org`, the official docs of a framework) carry no per-page date but are kept evergreen-current by the vendor; treat them as authoritative for the current version. If you need to pin a specific minor version, check the page's version selector or the project changelog.
**Why it matters**: a 2021 Node.js article describes v16 behavior; on v22 the API may have changed.

### 3. Cross-validate non-trivial claims

Any **non-obvious claim** — a behavior assertion, a performance number, a security statement, a compatibility claim, a "best practice" opinion — needs **≥2 independent sources** before you relay it as fact.

**Sharper test**: if the claim will **influence a decision** (which library to install, how to architect something, whether an approach is safe), it is non-trivial — cross-validate. Trivial facts (syntax, parameter names, type signatures) need only one authoritative source.

**Apply**: when a single source makes a non-trivial claim, run a second search to corroborate. Two sites with near-identical wording do **not** count as independent (one likely copied the other); look for independent reasoning or primary evidence.
**Why it matters**: one wrong blog post, repeated across aggregators, becomes an "everyone says" myth.

### 4. Skip content farms

Recognize and deprioritize: aggregator/scraping sites, AI-generated SEO farms, pure-copy content, ad-saturated low-quality pages, no-author no-date filler.

**Apply**: when the top results are 10 near-identical low-substance pages on unknown domains, jump to the official source or a reputable English-language authority instead.
**Why it matters**: content farms are optimized for search ranking, not correctness, and increasingly pollute results.

### Corollary — citation hygiene

When you relay an external finding, attach the **source link + (date)** so the user can verify in one click:
> "React 19's `use` hook can be called in conditionals (react.dev, 2024-12)."

This is the natural output of the four maxims, not a fifth rule.

---

## Strict mode — 7-dimension source evaluation + report

Triggered when the user explicitly asks for rigor: 「严格调研」「深度调研」「严格查证」「严谨调研」/ "strict research", "deep research", "fact-check" — **and** the target is external (Step 0 confirms). Use this when the conclusion matters (technology selection, security decisions, claims that will be acted on).

If the user asks for strict research but the target is **internal code** (e.g.,「严格分析我们 auth 模块的实现」), this skill does not apply — internal deep analysis is a different task; hand off to `explore` / `debug-workflow` / code-review tools instead.

Strict mode **includes** default mode (the 4 maxims still govern the search phase) and adds a structured evaluation.

### The 7 dimensions (CRAAP + E-E-A-T merged)

Two frameworks overlap; merged they yield seven distinct dimensions. E-E-A-T's **Trust** is the synthesized verdict, not a separate axis.

| # | Dimension | Question |
|---|-----------|----------|
| 1 | Authority | Who published it? What is their standing? |
| 2 | Expertise | What are the author's credentials? |
| 3 | Experience | Does it show first-hand practical evidence? |
| 4 | Currency | When published/updated? Does it match the current version? |
| 5 | Accuracy | Verifiable? Cited? Cross-confirmed? |
| 6 | Purpose/Bias | Why created? Commercial/ideological tilt? |
| 7 | Relevance | Does it directly answer the question? |

Each dimension is scored **High / Med / Low** with concrete criteria — the full rubric lives in [reference.md](reference.md) so this file stays a lean decision document. The aggregate verdict is **Trustworthy / Cautious / Unreliable**.

### Workflow

1. **Decompose** the research question into verifiable sub-claims.
2. **Search** under the default-mode 4 maxims. Stop searching when you have enough — for security/safety-critical conclusions, that means **≥2 independent primary sources** agreeing; for ordinary claims, enough sources to cover the sub-claims without obvious gaps.
3. **Score each source** across the 7 dimensions; assign aggregate Trust.
4. **Synthesize at the claim level** — which claims are multi-source High, which are single-source, which conflict. **For security/safety-critical claims, require multi-source High on Authority + Accuracy before marking a claim "Strong/Trustworthy"** (the bar is higher than for ordinary claims).
5. **Emit the report** using the template below.
6. **Flag gaps** — what still needs checking, where sources disagree.

### Report template

```markdown
# Strict research report: <topic>

## Research question
<the specific question, including version/context>

## Source evaluation

### Source 1: <title> (<URL>, <date>)
- Authority: H/M/L — <basis>
- Expertise: ...
- Experience: ...
- Currency: ...
- Accuracy: ...
- Purpose/Bias: ...
- Relevance: ...
- **Verdict**: Trustworthy / Cautious / Unreliable

### Source 2: ...

## Claims & confidence
- <claim 1>: ✅ Strong (multi-source High) — Sources 1, 2
- <claim 2>: ⚠️ Moderate (single source or Med) — Source 3, suggest follow-up
- <claim 3>: ❌ Disputed (Low or sources conflict) — Source 4 vs 5 contradict

## Gaps & next steps
- Still needed: <what's missing>
- Unresolved conflicts: <where sources disagree>
```

A fully worked example (a sample strict-mode report on a real-ish question) is in [reference.md](reference.md#worked-example).

---

## Pitfalls (the non-obvious ones)

- **"Official" isn't always the vendor site.** For open-source, the canonical source may be the GitHub repo's README / docs folder, or an RFC, not a marketing `.com`. Match "official" to where the project itself publishes truth.
- **Version drift inside one page.** A single doc page can cover multiple major versions; make sure the snippet you cite describes the version the user is on, not a deprecated section. Check version selectors / banners on the page.
- **Dateless pages ≠ evergreen.** Some undated pages are timeless (specs, algorithms); most undated web content is just neglected. For fast-moving topics, treat undated as stale.
- **StackOverflow high-vote answers can be a decade old.** Vote count reflects historical usefulness, not current correctness. Always cross-check the date and test against the current version.
- **Two sources, one origin.** If blog B cites blog A, they are not independent. Independence requires separate reasoning or separate primary evidence.
- **AI-generated search summaries are aggregations, not sources.** Google AI Overviews, Perplexity, Bing Copilot, and similar synthesize from other pages — they are convenient starting points but secondary. Before relaying a claim sourced only to an AI summary, trace it to the underlying primary source the summary cites; if none, treat as single-source and cross-validate.
- **Same package name, different ecosystem.** Package names collide across ecosystems — `jsonwebtoken` (npm) vs `jsonwebtoken` (Rust crate, `Keats/jsonwebtoken`); `jwt-go` vs `golang-jwt`. When a search/advisory mentions a package, check the **ecosystem field** (npm/cargo/go/pypi) before matching it to your target. A CVE for the Rust crate is irrelevant to the npm user and vice versa.
- **Default mode is not a pre-flight checklist the user sees.** It is silent behavioral discipline. Don't narrate "applying maxim 2…" — just do it and cite well.

---

## Reference

The full material — complete 7-dimension High/Med/Low rubric, the strict-mode report template expanded, and a worked example — is in [reference.md](reference.md). Read it when you need the scoring criteria for strict mode, or when a dimension's judgment is ambiguous.
