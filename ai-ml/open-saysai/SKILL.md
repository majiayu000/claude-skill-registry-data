---
name: open-saysai
description: Deeply audit and improve how websites are discovered, retrieved, cited, mentioned, and understood by AI search and answer systems. Use for technical multi-platform AI visibility audits, ChatGPT/Claude/Gemini/Copilot/Perplexity/Grok crawler or WAF diagnosis, robots.txt/sitemap implementation, citation-readiness audits, live prompt visibility testing, and ai_visibility_packet generation. Not for quick generic "how do I show up in ChatGPT?" tips when a lighter SEO/GEO skill is installed, or for general non-AI website QA.
---

# Open SaysAI

Treat AI visibility as a retrieval and source-selection problem, not a magic ranking system.

## Purpose

Every audit answers one question: **What information would an AI system need to cite from this domain because it originates here or is materially better here, and what stops that from happening?**

Technical checks (access, indexing, rendering) establish whether AI systems *can* use the site. They are the gate, not the goal. The audit's value is judging whether systems *would* select the site as a source, and what would change that. Technical findings are easy to prove; that is not a reason for them to dominate the report or the recommended first action.

## Non-negotiable rules

1. Separate **search/indexing**, **live retrieval/search crawlers**, **user-directed fetchers**, and **model-training crawlers**. Never imply that a training crawler controls search visibility unless current first-party documentation says so.
2. Verify platform-specific claims from first-party documentation when the cached verification in `references/platforms.md` is stale, missing, contradicted, or outside the requested scope.
3. Never guarantee ranking, citation, recommendation, inclusion, or traffic.
4. Mark unverifiable states **Unknown**, not failed.
5. Treat `llms.txt` as experimental unless a current platform source explicitly documents a visibility effect.
6. Treat standard structured data as machine-understanding support, not an AI ranking switch. Do not invent "AI schema."
7. Do not recommend cloaking, hidden crawler instructions, prompt injection, doorway pages, fake mentions/reviews/authors/studies, mass low-value AI content, or invisible schema claims.
8. Keep important facts in ordinary crawlable HTML whenever possible.
9. Distinguish observed evidence, documented platform behavior, and inference in every audit.
10. **Audit mode is read-only.** Inspect the site and repository as found. Do not `git pull`, edit files, regenerate content, install dependencies, run migrations, run formatters, or change production/CDN settings unless the user asked for implementation. If fresher state is needed, report the limitation instead. Changing what you audit contaminates the evidence.
11. Use the evidence language below. Claim only the link of the visibility chain you actually proved.

## Evidence language

The visibility chain is **reachable → indexed → retrieved → cited → recommended**. Each link needs its own evidence. Proving one link never proves the next.

- A synthetic-UA probe returning 200 ≠ the real crawler can access the site. The probe presented the crawler's name from this machine's IP; say "requests presenting the OAI-SearchBot UA received HTTP 200."
- Log requests claiming a crawler UA ≠ verified crawler traffic. Call them **UA-attributed** until matched to the vendor's published IP ranges or reverse/forward DNS. Fake crawler traffic is common.
- Crawlable ≠ indexed ≠ retrieved ≠ cited ≠ recommended.
- Indexed in Google Search = eligible for Google AI features, not evidence of being cited in them. Report search-index evidence and AI-citation evidence separately.
- No citation dashboard ≠ citations cannot be measured. Controlled prompt tests are a measurement method; Bing AI Performance covers Microsoft surfaces only. Say "measurement is incomplete" and name the gap.
- A fact missing from one page ≠ missing from the site. Name exactly what is missing and where you looked.

## Modes

Infer the mode from the request:

- **Full audit** -- technical access + source-selection fitness (retrieval, information gain, authority/entity, topic coverage) + freshness + measurement. Not finished until the completion gate passes.
- **Platform audit** -- one or more named AI/search systems.
- **Page audit** -- one URL/article as a potential cited source.
- **Implementation** -- exact robots, sitemap, IndexNow, schema, semantic HTML, accessibility, or content changes.
- **Content/source opportunity** -- identify facts, datasets, tools, comparisons, definitions, and pages worth citing.
- **Prompt visibility test** -- actually test important prompts when a suitable live-model connector is available.
- **General playbook** -- explain the system without auditing a site.

## Inputs

A URL/domain alone is sufficient to start a live audit. Use optional topics, markets, prompts, analytics, log files, webmaster exports, code, or existing audits when supplied. Do not stall waiting for keyword lists.

## Workflow

### 1. Define the visibility outcome

Translate the task into concrete outcomes such as:

- cited as a source
- mentioned as an entity/brand
- surfaced for topical or commercial prompts
- accessible to a named crawler/fetcher
- indexed by a search system that feeds AI answers
- selected for fresh/current information
- usable by AI agents for forms/tools/actions

Do not collapse these into one fake "AI ranking" score.

### 2. Resolve platform behavior efficiently

Read `references/platforms.md`.

- Reuse an entry whose **Verified** date is within 90 days unless current evidence conflicts or the user explicitly requests a fresh platform check.
- Reverify only platforms in scope or stale/unknown entries. Do not automatically research every vendor on every audit.
- Prefer vendor crawler/search/webmaster documentation over commentary.
- Record the verified date and source in the audit/packet.
- If the vendor does not publicly document a crawler or ranking mechanism, say **Unknown/undocumented** rather than guessing.

### 3. Gather technical evidence

For live domains, run `scripts/probe_site.py` when container execution is available. It checks:

- page status/redirects/meta robots/canonical/HTML headings/JSON-LD
- robots.txt with longest-rule matching, `*`, `$`, and Allow-tie behavior
- per-agent HTTP status/selected WAF headers for major crawlers/fetchers (synthetic UA)
- declared/common sitemaps and basic XML coverage/lastmod signals

Use the script as a first-pass probe, not a complete browser, IP-verification system, or index checker.

If every request in the probe fails with a network/DNS/connection error (including the page itself), the sandbox likely has no outbound internet. That says nothing about the site. Do not report the site as unreachable; fall back to the browsing tool for page content and mark HTTP/WAF rows **Unknown**.

Every per-agent result is `evidence_tier: synthetic_ua`. A `reachable` result shows how the site treats that UA from this machine, not that the real crawler gets in. If an agent shows a `spoofed_ua_caveat`, the block may be fake-bot protection that still admits the real crawler from its verified IP ranges. Report it as **Unverified**, not P0, until server/CDN logs or the platform's webmaster tools confirm it.

If server/CDN logs are available, report crawler request counts as UA-attributed unless IP/DNS-verified (see Access in `references/audit-framework.md`).

When sitemap, Search Console, crawl, and index counts disagree materially, reconcile the populations before computing any percentage or coverage summary (see Indexability in `references/audit-framework.md`). If the gap can't be explained, report both numbers and mark coverage **Unknown**.

Then use browser/webmaster/search evidence as needed to inspect rendering, index presence, CDN challenges, JavaScript-only content, and pages beyond the probe URL.

Read `references/audit-framework.md` for the detailed audit checklist and priority logic.

### 4. Audit source-selection fitness (the core of the audit)

Spend the most effort here. Use `references/audit-framework.md` to evaluate:

- passage-level retrieval fitness
- answer-first/self-contained sections
- entity clarity and independent corroboration
- trustworthy sourcing and authorship
- information gain/original facts
- topical/query-space coverage
- freshness
- agent usability
- measurement readiness

Review real pages, not the site in the abstract: run the **source-selection page review** in `references/audit-framework.md`. For each page, name the exact question that would make a retrieval system need it and which sources already answer that question.

Ask repeatedly: **What information would an AI need to cite from this domain because the information originates here or is materially better here?**

Fixes must make pages more worth citing: clearer, more specific, more original, better sourced. Do not propose mechanical keyword or location insertion; add a place or entity term only where the page is genuinely about it.

### 5. Run prompt visibility tests when requested

Create a representative prompt set across informational, comparison, commercial, troubleshooting, and entity queries.

Execute tests only through a clean channel: a connector or API that queries the target assistant in a fresh session, or results the user runs and pastes back. Do not answer the test prompts yourself inside this audit conversation. Your answers here are primed by the audit context and are not evidence of what real users see. Never simulate a platform you cannot actually query.

For each executed prompt record:

- model/product and test date
- exact prompt
- brand/entity mentioned?
- domain cited?
- cited URL(s)
- competing sources/entities
- answer attributes associated with the entity
- whether the result was direct model output, search-grounded, or unknown

If no clean channel is available, return the prompt suite and mark execution **Not run**.

### 6. Prioritize

Use these levels:

- **P0 -- Blocker:** verified crawl/index/retrieval obstacle.
- **P1 -- High leverage:** source-worthiness, retrieval structure, authority/entity, or index-coverage gap on important pages, likely to matter materially.
- **P2 -- Enhancement:** worthwhile but secondary. Measurement and freshness default here; raise measurement only when the user's stated outcome is reporting/tracking.
- **Experimental:** unproven tactics such as `llms.txt` unless current platform docs elevate them.

Every finding must include evidence, consequence (which link of the visibility chain it weakens), and an executable fix.

Findings are only issues that affect AI discovery, retrieval, or source selection. Other bugs found along the way (UI glitches, broken styling) go under **Incidental site issues**, not in the findings.

### 7. Pass the gates, then hand off

- **Completion gate (full audit):** every dimension in the audit-framework completion gate is evaluated with evidence or marked Unknown/Out of scope with the reason. An audit that stops after crawl/index checks is not finished. Content/source opportunities must be named, or their absence explained.
- **Priority gate:** the recommended first action is the highest-ranked finding by the audit-framework priority order. How easy, fast, or cheap a fix is never moves it up. Quick wins may be listed beside it, labeled "quick win (parallel)."
- **Evidence gate:** reread every claim against the evidence language above. Downgrade any claim that skips a link in the chain.

Use `references/output-templates.md` for the human-readable report and `references/ai-visibility-packet.md` for the portable `ai_visibility_packet`.

For a full/platform audit, always emit the packet in addition to the human-readable result. If file creation is available, save it as `ai_visibility_packet.json`; otherwise include it as fenced JSON.

## Tool discipline

- Browse current first-party docs only when the platform cache requires it or the user asks for fresh verification.
- Use search/webmaster evidence to prove index/citation state; crawlability alone does not prove indexing.
- When checking WAF behavior, compare per-agent responses. A generic 200 does not prove an AI crawler receives 200.
- Never infer crawler access from robots.txt alone if HTTP/WAF evidence contradicts it.
- Never treat a user-fetcher that ignores or conditionally applies robots rules as equivalent to an automatic search crawler.
- Audit mode is read-only (rule 10). In implementation mode, change only what the user asked for, with the tools the session permits.

## Resources

- `references/platforms.md` -- platform-specific roles, sources, and verification cache.
- `references/audit-framework.md` -- detailed technical/retrieval/authority checklist, page review, gates, and priority order.
- `references/output-templates.md` -- human-readable report formats.
- `references/ai-visibility-packet.md` -- machine-readable handoff schema.
- `scripts/probe_site.py` -- deterministic page/robots/synthetic-UA/sitemap probe.
