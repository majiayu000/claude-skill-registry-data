---
name: reddit-seo-response
description: Combine GSC, GA4, SEO growth-plan data, Reddit thread discovery, and the Humanizer skill to produce ranked Reddit reply opportunities for lifting blog clicks, impressions, and qualified organic traffic. Use when deciding which Reddit threads to answer, what URL or blog post to support, and what humanized reply to post.
version: 2.1.0
---

# Reddit SEO Response

Use this skill to generate referral traffic and support SEO signals for blog posts. The default behavior is fully automatic: fetch SEO data, pick the best low-hanging-fruit blog posts, discover/score Reddit threads, and return exact ready-to-post replies. Do not ask the user which blog posts to target unless the repo has no usable GSC/GA/SEO data.

The job is not "drop links on Reddit." The job is to find threads where people are already asking about problems a target blog post answers, then give a useful custom response and only include the blog link when it fits the thread and subreddit rules.

## Hard Linked-Target Contract

- The linked candidate must use a relevant existing `https://myimageupscaler.com/blog/...` URL selected from fresh GSC query/page evidence.
- Never use the homepage, dashboard, `/tools/`, `/free/`, or another product surface as the Reddit self-link. The campaign exists to distribute blog pages that already have measurable search demand.
- Record the fresh GSC date range, exact target query, target page, impressions, clicks, and average position in the action-sheet metadata.
- The public reply must contain exactly the same blog URL declared in `Target page` and no second MIU URL.
- If fresh GSC cannot be fetched, fail the linked-candidate step. Do not guess a target from topical similarity and do not fall back to the homepage.
- Run generate → project-validator → error-guided correction for at most 3 attempts. Never weaken the validator; after attempt 3, report failure instead of delivering a partial or invalid sheet.
- A linked page is worth a Reddit bump only when the exact matching GSC query is in the striking-distance band: **position 4-20, at least 50 impressions in the fresh 28-day window, and CTR below 5%**. Positions 4-10 are weak-capture first-page pushes; positions 11-20 are credible top-10 candidates. Do not use aggregate page position as a substitute for the matching query's metrics.
- The Reddit question and selected GSC query must share a concrete problem term, and the action sheet must state the semantic mapping in `Relevance evidence`. A high-opportunity page that does not answer that exact question is not a valid bump target.

## Regression Lock — Version-Controlled Contract

This project skill is the canonical MIU Reddit SEO contract. The installed Hermes shared skill may orchestrate it, but must not weaken or replace it.

- Canonical validator: `.claude/skills/reddit-seo-response/scripts/verify_action_sheet.py`
- Behavioral tests: `.claude/skills/reddit-seo-response/scripts/test_verify_action_sheet.py`
- Canonical action-sheet template: `.claude/skills/reddit-seo-response/templates/miu-action-sheet.md`
- Contract test: `tests/unit/seo/reddit-seo-contract.unit.spec.ts`

Any change to batch shape, GSC targeting, bump-worthiness thresholds, question relevance, permitted link paths, disclosure, dedupe, or retry behavior must update the relevant tests in the same commit. The cron must invoke this project validator with `--gsc`; do not point it back to an unversioned copy under `~/.hermes/skills`.

This skill is reusable across projects. It can run from this repo's `seo-growth-plan` output, or from a standalone target JSON when another project does not have the same GSC/GA scripts.

When this skill activates: `Reddit SEO Response: combining GSC, GA4, SEO plan, Reddit discovery, and Humanizer...`

## Default Auto-Campaign Behavior

When the user says `use reddit-seo-response`, `run reddit-seo-response`, or asks for Reddit replies/traffic bumps without giving target URLs, do this automatically:

1. Read the Reddit post log at `docs/seo/reddit-post-log.md` if it exists. Use it to avoid duplicate threads, maintain the 9:1 participation ratio, and account for recently posted links.
2. Run `gsc-analysis` for the current site.
3. Run `ga-analysis` for the current site.
4. Run `seo-growth-plan` to produce a joined SEO opportunity file.
5. Filter to blog/content URLs by default (`/blog` when present).
6. Select low-hanging-fruit posts automatically:
   - Position 4-10 first.
   - Position 11-20 second.
   - Position 21-40 only if Reddit relevance is very strong.
   - Position 1-3 only if CTR is weak.
7. Run Reddit discovery/scoring for those targets.
8. If Reddit native JSON search is blocked, rate-limited, or slow, immediately switch to RSS + old Reddit fallback before giving up:
   - Keep any candidates already found by the Reddit script.
   - Use Reddit Atom feeds for discovery: `https://www.reddit.com/r/<subreddit>/search.rss?q=<query>&restrict_sr=1&sort=relevance&t=year`, `https://www.reddit.com/search.rss?q=<query>&sort=relevance&t=year`, and subreddit `.rss` feeds when fresh community posts matter.
   - Use `old.reddit.com` thread HTML and thread `.rss` feeds for context inspection when `.json` endpoints return 403.
   - Run web searches such as `site:reddit.com/r/ "[target query]" reddit`, `site:reddit.com/r/ "[pain point]"`, and `site:reddit.com/r/ "[tool category]"`.
   - Prefer exact problem threads over generic keyword matches.
   - Feed manually found/RSS candidates into scoring when practical, or manually score the top 5-10 threads.
9. Inspect the top candidate threads for relevance and obvious rule/link risk.
10. Draft custom replies for the best opportunities.
11. Apply the `humanizer` skill to the final reply text.
12. Write a Markdown action sheet to disk and return the file path. The `.md` must start with exact posting instructions: what thread to target, what order to post in, and the ready-to-paste comment.
13. Append recommended actions to `docs/seo/reddit-post-log.md` with status `recommended`. If the user confirms they posted replies, update those rows to `posted`.

Do not stop after loading the skill. Do not ask for target posts as the first response. Only ask the user for input if credentials are missing, the site cannot be inferred, or Reddit discovery is blocked and no candidate source is available.

## Related Skills

Call these in order when data is not already available:

1. `gsc-analysis` - fetch Search Console query/page demand.
2. `ga-analysis` - fetch GA4 organic landing-page behavior and conversion data.
3. `seo-growth-plan` - join GSC + GA4 into `/tmp/seo-plan-miu.json`.
4. `humanizer` - rewrite only the final suggested replies so they sound like a real practitioner.

If the user gives a specific URL or topic, use it as a constraint, but still use GSC/GA when available to decide whether that URL deserves the push.

If the user gives specific blog posts, treat those as the campaign targets. Do not replace them with unrelated higher-scoring URLs unless the data shows the post is a bad match for the requested intent.

## Auto-Campaign Commands

```bash
# 1. Produce the joined SEO dataset
node ./.claude/skills/gsc-analysis/scripts/gsc-fetch.cjs --site=example.com --days=28 --output=/tmp/gsc.json
node ./.claude/skills/ga-analysis/scripts/ga-fetch.cjs --site=example.com --days=28 --output=/tmp/ga.json
node ./.claude/skills/seo-growth-plan/scripts/seo-synthesize.cjs \
  --gsc=/tmp/gsc.json \
  --ga=/tmp/ga.json \
  --site=example.com \
  --output=/tmp/seo-plan.json

# 2. Discover Reddit candidates from auto-selected blog opportunities
node ./.claude/skills/reddit-seo-response/scripts/reddit-discover.cjs \
  --seo-plan=/tmp/seo-plan.json \
  --page-prefix=/blog \
  --site=example.com \
  --max-pages=8 \
  --queries-per-target=2 \
  --threads-per-query=5 \
  --delay-ms=2000 \
  --output=/tmp/reddit-seo-opportunities.json
```

### Standalone Target Mode

Use this when another project does not have the same SEO synthesis script:

```json
{
  "targets": [
    {
      "page": "/blog/example-post",
      "queries": ["best free image upscaler", "upscale image without losing quality"],
      "position": 8.4,
      "impressions": 12000,
      "clicks": 35,
      "priority": "high",
      "notes": "Good low-hanging-fruit page. Push referral traffic and query engagement."
    }
  ]
}
```

```bash
node ./.claude/skills/reddit-seo-response/scripts/reddit-discover.cjs \
  --targets=/tmp/reddit-targets.json \
  --site=example.com \
  --page-prefix=/blog \
  --queries-per-target=2 \
  --threads-per-query=5 \
  --delay-ms=2000 \
  --output=/tmp/reddit-seo-opportunities.json
```

### Candidate Scoring Mode

Use this when Reddit public search is rate-limited or when another tool fetched the threads:

```json
{
  "threads": [
    {
      "title": "Best free image upscaler?",
      "url": "https://www.reddit.com/r/example/comments/abc/thread/",
      "subreddit": "r/example",
      "score": 42,
      "comments": 18,
      "createdUtc": 1760000000,
      "selftext": "Looking for a free tool that does not add a watermark."
    }
  ]
}
```

```bash
node ./.claude/skills/reddit-seo-response/scripts/reddit-discover.cjs \
  --targets=/tmp/reddit-targets.json \
  --candidates=/tmp/reddit-candidates.json \
  --output=/tmp/reddit-scored.json
```

## Strategy

Use Reddit for two use cases:

- **Traffic bump:** answer fresh threads with active comments where the page solves the exact problem.
- **SERP/LLM support:** answer older high-ranking Reddit threads that appear for the same GSC queries and can send long-tail referral traffic over time.

Do not treat Reddit as a replacement for on-page SEO. If GSC shows a page has impressions but bad CTR, fix title/meta first. If GA4 shows bad engagement or conversion, fix the page before pushing more traffic to it.

## Execution Efficiency

Optimize for getting to a usable posting plan quickly.

- Do not let Reddit 429s dominate the run. If two or more searches get rate-limited, switch to hybrid discovery with web search.
- Search fewer, better queries: use the top 1-2 GSC queries plus one plain-language pain-point query per target page.
- Cap discovery at 5-10 promising threads per target, then manually qualify. More raw candidates are usually noise.
- Deduplicate by Reddit thread URL before drafting.
- Reject false positives early: meme/news threads, competitor-owned subreddits, broad AI debates, and threads where the OP is not asking for help.
- Prefer threads where the reply can be useful even without a link.
- If a page has severe GA4 bounce/engagement problems, still allow a no-link participation reply, but mark linked posting as "fix page first."
- The user needs a copyable `.md` with posting instructions, not a research diary. Keep process notes after the post-ready replies.

## Opportunity Selection

Start from the joined SEO plan:

1. Filter to blog/content URLs first. Use `/blog` when present; otherwise infer the content section from the URL inventory.
2. Prioritize low-hanging-fruit rankings:
   - Position 4-10: primary targets.
   - Position 11-20: secondary targets.
   - Position 21-40: only if thread relevance is unusually strong.
   - Position 1-3: only if CTR is weak or the goal is defense.
3. Prefer posts with GSC impressions, low/moderate clicks, and queries that map cleanly to Reddit questions.
4. Prefer posts with GA4 engagement good enough that referral visitors will not instantly bounce.
5. Include CTR/content opportunities only when the post already matches intent.
6. Deprioritize posts with severe GA4 bounce or conversion problems unless the Reddit answer can route users to a better-matching page.

For each chosen page, build Reddit searches from:

- Top GSC queries for the page.
- Pain-point versions of the query, e.g. `how to fix blurry image`, `best ai image upscaler`, `upscale image without watermark`.
- Competitor/alternative intent, e.g. `alternative to [competitor]`, only when the target page is a genuine alternative.

## Reusable Script Controls

- `--seo-plan`: use a `seo-growth-plan` style JSON.
- `--targets`: use a standalone target JSON with `page`, `queries`, `position`, `impressions`, and `clicks`.
- `--candidates`: score a pre-fetched Reddit thread export instead of calling Reddit search.
- `--pages`: force specific URLs.
- `--page-prefix`: restrict to a section such as `/blog`.
- `--subreddits`: only search specific communities.
- `--exclude-subreddits`: deny noisy communities.
- `--queries-per-target`: reduce query volume to avoid Reddit rate limits.
- `--delay-ms` and `--max-retries`: pace Reddit search requests.
- `--min-relevance`: raise this when generic words are creating junk matches.
- `--dry-run`: validate selected targets and generated queries without calling Reddit.

## Reddit Qualification

Before writing a reply, inspect the thread and subreddit:

- Subreddit rules allow helpful links, or the reply can stand without a link.
- Thread is relevant to the target page and not just vaguely keyword-matched.
- Thread has real user intent: question, comparison, complaint, workflow problem, or tool request.
- Existing replies do not already answer the question completely.
- Account fit is plausible. Do not recommend posting from a new or brand-only account into strict communities.

If direct Reddit JSON search returns 403s or rate limits, do not abandon the task. Use these fallback paths in order:

- Run the bundled `reddit-discover.cjs` script first; it falls back from blocked JSON search to Reddit RSS automatically.
- If manually discovering, use Reddit Atom feeds: subreddit search RSS, global `search.rss`, and subreddit `.rss` feeds.
- Use `old.reddit.com` thread HTML and thread `.rss` feeds to inspect candidate context when `*.json` thread endpoints are blocked.
- Score any existing candidate export with `--candidates=...`.
- Use web search to find Reddit threads for the selected queries, then feed them as candidates.
- Return the selected target posts and exact Reddit search queries as a blocked discovery report only if JSON, RSS, old Reddit HTML, and web-search candidate sources are all inaccessible or inadequate.

Reject the thread if:

- Rules ban self-promotion, tool links, or external links.
- The answer would require pretending to be an unrelated happy customer.
- The page is not genuinely useful for the OP.
- The reply would be mostly a link with filler around it.

## Reply Construction

For every approved thread:

1. Address the OP's exact wording or situation.
2. Give away most of the answer in the comment. The reader should get value without clicking.
3. Mention tradeoffs, failure cases, or a practical caveat.
4. Add the link only when it is natural and allowed.
5. Run the final draft through the `humanizer` skill.

Keep the voice practical, specific, and non-corporate. Avoid fake enthusiasm, perfectly symmetric bullets, marketing phrases, and AI-sounding transitions.

## Link Guardrail

Default to a 9:1 participation ratio:

- After one self-link, the next nine Reddit actions should be non-promotional community participation.
- Track the target domain, subreddit, thread URL, date, and whether a link was used.
- If rules ban links, produce a no-link answer. Do not add a "DM me" workaround unless the user explicitly asks and the subreddit allows it.

## Post Log Memory

Use `docs/seo/reddit-post-log.md` as durable campaign memory.

At the start of every run:

- Read the log before selecting threads.
- Exclude threads already marked `posted`.
- Treat threads marked `recommended` as pending unless the user says they were skipped or posted.
- Count recent linked posts vs no-link participation posts before recommending another self-link.
- Avoid recommending the same subreddit repeatedly unless the new thread is clearly high intent.

After every run:

- Append each generated recommendation with status `recommended`.
- Include `date`, `status`, `subreddit`, `thread URL`, `thread title`, `target page`, `link decision`, `link used`, and a short note.
- When the user says they posted a reply, update the matching row to `posted` and set `posted date`.
- When the user says they skipped one, update the row to `skipped`.
- Keep the latest 100 rows in the main log. When it grows past 100 rows, move older rows into `docs/seo/reddit-post-log-archive.md` or summarize them by month, preserving linked-post counts.

## Output Format

Create a Markdown file and return its path. The default path should be `/tmp/reddit-seo-response-[site]-[YYYY-MM-DD].md` unless the user gives another path. Also include the same high-level posting list in the chat response, but the `.md` is the source of truth.

The Markdown file must start with exact posting instructions. The first section must answer "what do I post, and where?" before any analysis.

````markdown
## Post These Reddit Replies

### 1. Post first: r/subreddit - thread title

Thread: [URL]
Target page: [URL or "none"]
Link decision: [include link / no link / skip]

Reply:

```text
[Humanized ready-to-paste Reddit reply.]
```

### 2. Post second: r/subreddit - thread title

Thread: [URL]
Target page: [URL or "none"]
Link decision: [include link / no link / skip]

Reply:

```text
[Humanized ready-to-paste Reddit reply.]
```

### 3. Post third: r/subreddit - thread title

Thread: [URL]
Target page: [URL or "none"]
Link decision: [include link / no link / skip]

Reply:

```text
[Humanized ready-to-paste Reddit reply.]
```

## Why These Threads

**Data used:** GSC [date range], GA4 [date range], SEO plan path, Reddit discovery path
**Campaign goal:** referral traffic + SEO signal bump for [target blog posts]
**Best use now:** [traffic bump / SERP support / skip until page fixed]

### 1. [Priority] r/subreddit - thread title

- **Thread:** [URL]
- **Target page:** [URL]
- **Target query:** [GSC query this should support]
- **Why this thread:** [GSC query + GA4/page evidence + Reddit intent]
- **Link decision:** [include link / no link / skip]
- **Risk:** [low/medium/high and why]

**Suggested reply:**

[Humanized custom reply ready for manual posting.]

### Backlog

| Priority | Thread | Page | Query Match | Link? | Reason |
| -------- | ------ | ---- | ----------- | ----- | ------ |
````

Rules for the posting section:

- Always include at least one post-ready reply if any qualified thread exists.
- Always write the final action sheet to a `.md` file.
- Return the `.md` file path prominently in the chat response.
- Put the best action first, even if it is a no-link reply.
- Use plain labels: "Post first", "Post second", "Post third".
- Include the thread URL directly under each instruction.
- Put each reply in a `text` code block inside the `.md` so the user can paste it.
- Keep the ready-to-paste reply free of meta commentary like "Suggested reply:" inside the code block.
- If linking to the user's site, disclose affiliation plainly in the reply.
- If no link should be used, write the strongest no-link community reply instead of explaining that a reply could be written.
- Put skipped/backlog threads after the posting instructions, not before.

## Manual Review Checklist

Before telling the user to post:

- The comment is custom to that thread.
- The page solves the problem better than a generic answer alone.
- The link is optional, late in the reply, and framed as a convenience.
- The reply does not claim affiliation dishonestly.
- The subreddit rules were checked.

## Files

| Item                    | Path                                                               |
| ----------------------- | ------------------------------------------------------------------ |
| Skill Doc               | `./.claude/skills/reddit-seo-response/SKILL.md`                    |
| Reddit Discovery Script | `./.claude/skills/reddit-seo-response/scripts/reddit-discover.cjs` |
| Default Markdown Output | `/tmp/reddit-seo-response-[site]-[YYYY-MM-DD].md`                  |
| Reddit Post Log         | `docs/seo/reddit-post-log.md`                                      |
