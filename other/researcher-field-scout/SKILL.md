---
name: researcher-field-scout
description: Orchestrate public-source scouting for a representative researcher, builder, professor, lab, or technical thought leader to infer field structure, current mainline, branches, historical lines, public artifacts, reading route, watch plan, and minimal-test opportunities. Use when Codex is asked to "follow" a person, trace how someone reached their current work, learn a field by looking at key people, compare public researcher/builders, design a person-centered field map, or turn public posts, papers, talks, repos, courses, students/collaborators, and projects into an evidence-backed scouting report. Route collection through existing search/crawler/source-intel skills instead of inventing a new crawler.
---

# Researcher Field Scout

Map a public person or lab into a decision-useful field scouting report. This skill is not a biography writer. Its job is to turn public artifacts into:

- current mainline / branches / historical lines,
- trajectory and public action trace,
- source ledger and confidence labels,
- reading / watch / minimal-test route,
- reusable workflow signals.

## Core Rule

Watch public actions before commentary. Prefer original artifacts: official pages, personal/lab pages, papers, repos, courses, talks, blog posts, project pages, datasets, benchmarks, and direct posts. Use secondary media and community discussion for discovery or corroboration, not as the final basis when originals exist.

## Workflow

1. Establish scope.
   - Identify the target person/lab, field, user's purpose, time window, output language, and whether the result is public-safe or private.
   - If the target is an academic professor/lab and the user mainly wants advisor/RA fit, route through `professor-direction-mapper` or `professor-fit-analyzer` first, then add this skill's broader public-trace layers.
   - If the user asks for several people, use a small candidate table and scout only enough to rank or choose deeper lanes.

2. Build a route plan before crawling.
   - Read `references/tool-routing.md` when selecting collection tools.
   - Choose only needed lanes: web/source discovery, academic profile, papers, code/projects, talks/posts, community signal, Chinese platforms, career/JD signals, or watchlist.
   - Do not install new crawlers until local tools and official/public sources are insufficient.

3. Source-lock the identity.
   - Find canonical homepages, official profiles, GitHub/HF/ORCID/OpenAlex/DBLP/Semantic Scholar pages, lab pages, and verified direct-post accounts.
   - Resolve name ambiguity before interpreting works.
   - Record source type, URL, fetched date, what it proves, and caveat.

4. Collect public artifact lanes.
   - Self-positioning: homepage, bio, lab mission, research statement, pinned projects, course pages, selected works.
   - Papers: recent 3-4 years plus older highlighted or field-shaping works.
   - Code/projects: repositories, releases, READMEs, demos, datasets, evals, leaderboards, scripts.
   - Posts/talks: blogs, interviews, videos, transcripts, slides, direct posts.
   - Network: students, collaborators, coauthors, organizations, labs, conferences, communities.
   - Early signals: HN, alphaXiv, RSS/lab blogs, Zhihu/XHS/Nowcoder only when relevant to the user's question and safety rules allow.

5. Classify the trace.
   - Current mainline: self-positioning plus repeated recent artifacts, current projects, recent papers, public talks, recruiting language, or active repos.
   - Branch: real but narrower or less repeated line.
   - Historical line: older important work with weak current continuation.
   - Emerging pivot: fresh but still sparse signal.
   - Open question: plausible but insufficiently sourced.

6. Extract field structure.
   - Convert person trace into field map: core problems, method families, datasets/benchmarks, venues, collaborators, canonical readings, adjacent communities, and practical entry route.
   - Separate the person's taste/workflow from field-wide consensus.
   - Avoid personality worship: every claimed pattern should point to public artifacts.

7. Produce the report.
   - Use `references/output-template.md` for durable reports.
   - Include source IDs in major claims.
   - For public repositories, keep local paths, private tasks, secrets, cookies, paid content, and personal sensitive context out of the report.
   - End with a watch plan and minimal-test plan, not only conclusions.

8. QA before finalizing.
   - Ask: did I confuse current with historical?
   - Ask: is each strong claim source-backed?
   - Ask: did I label secondary/community evidence?
   - Ask: did I expose private or local-only context in a public output?
   - Ask: is there an action route: what to read, watch, reproduce, or test next?

## Output Contract

For substantial tasks, produce or update:

- `source-ledger.md` or a source table,
- `timeline.md` or public action trace,
- `projects.md` / `papers.md` / `posts-talks.md` when evidence volume justifies it,
- one human-facing synthesis report,
- one watchlist or refresh plan,
- optional application-alignment note when the user wants to connect findings to their own work.

For quick tasks, return a compact version with:

- verdict,
- evidence layers,
- current mainline / branches / historical line,
- what to follow next,
- caveats.

## Routing With Other Skills

- Use `anysearch` for current web discovery, official pages, direct posts, and batch search.
- Use `google-scholar-profile-intel`, `paper-review-source-intel`, or `professor-direction-mapper` for academic profiles, publication evidence, and advisor/lab direction mapping.
- Use `code-model-benchmark-intel` for GitHub, Hugging Face, datasets, benchmark, and implementation evidence.
- Use `early-signal-intel` for HN, alphaXiv, RSS/lab blogs, Bluesky/Reddit-style discussion signals.
- Use `zhihu-public-intel`, `xhs-explore`, `nowcoder-public-intel`, `chinese-ai-signal-crawler`, or career/salary tools only when those public/community channels are relevant and their safety rules permit.
- Use `evidence-synthesis-docs` after collection to turn raw ledgers into reports.
- Use `assumption-auditor` or an adversarial QA pass when the output will guide a high-stakes decision.

## Guardrails

- Do not infer private motives, personality, ideology, or life details from technical artifacts.
- Do not treat high citation, media fame, or social engagement as current mainline evidence by itself.
- Do not use Google Scholar scraping as canonical evidence; prefer official pages, OpenAlex, Semantic Scholar, DBLP, ORCID, proceedings, arXiv, and direct sources.
- Do not bypass paywalls, CAPTCHAs, login gates, rate limits, platform controls, or deleted/removed content.
- Do not save API keys, tokens, cookies, browser profiles, private chats, or personal sensitive details into Git-tracked outputs.
- Do not claim completeness unless the run explicitly covered all declared source lanes and recorded failures.
