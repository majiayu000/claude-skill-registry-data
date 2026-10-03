---
name: brag-doc
description: Generate a comprehensive, impact-framed brag-doc entry for a chosen time window (day, week, biweek, month, or custom). Pulls authored PRs, reviews given, commits, deploys, and linked tickets across GitHub, local git, and configured MCPs, then synthesises a themed narrative, leading with outcomes, quantifying impact, owning the work in first-person past tense, separating IC contributions from amplification, and naming the judgment exercised. Output is designed to drop straight into a developer journal, a personal bragging sheet, or a performance-review packet. Accepts a mode argument, `/flagrare:brag-doc resumancer` renders the output as ready-to-paste Resumancer CLI commands (`resumancer impact "..." --branch ...`) instead of markdown. Use whenever the user says "brag doc", "brag sheet", "what did I do this week", "weekly recap", "monthly recap", "performance review prep", "what should I tell my manager", "summarise my impact", "career log entry", "give me my wins", "biweekly recap", or any variant about looking back over a longer window than a single day's standup. Also trigger near review season ("self-review", "perf packet", "evaluation prep"), and on phrases like "log my wins to resumancer" or "make resumancer entries for this week" (which should pass the `resumancer` mode). For windows longer than about a month, a tenure retrospective, a departure record, or "everything I did at this company", hand off to `/flagrare:impact-timeline` instead; this skill's window tops out at a month.
---

# Brag Doc

> **No em-dashes.** Nothing this skill writes may contain an em-dash; use a comma, colon, or parentheses instead. Enforced by a repo hook that flags em-dashes in generated `.md`. See `/flagrare:write-docs`.

Produce a comprehensive retrospective of the user's code work over a chosen time window, written in **brag-doc voice**: themed by impact, quantified where possible, owned in first-person, and structured to be re-read months later in a performance review or copied into a dev journal.

This skill is the long-arc counterpart to `/flagrare:standup-report`. Same data pipeline (GitHub, local git, deploys, tickets, optional MCPs), inverted output:

|  | standup-report | brag-doc |
|---|---|---|
| Window | last working day | day → month (user picks) |
| Audience | team, in Slack | future-me, in a journal or review packet |
| Tense | conversational past ("most of the day went to...") | accomplishment-framed past ("I shipped X, which reduced Y by Z%") |
| Order | chronological / time-of-day | thematic / impact-area |
| Goal | "what's the team status?" | "what's worth remembering and re-telling?" |

The single rule that shapes the synthesis: **lead with what got better, by how much, for whom.** Not "I worked on X." That framing, owned, quantified, outcome-first, is what separates a brag doc from a glorified changelog.

## Modes

The skill accepts a mode argument that controls output rendering. The synthesis pipeline is identical across modes, only the final render differs.

| Invocation | Mode | Output |
|---|---|---|
| `/flagrare:brag-doc` | **default** | Brag-doc markdown (headline, themed sections, refs). Suitable for a dev journal, a personal brag sheet, or a performance-review packet. |
| `/flagrare:brag-doc resumancer` | **resumancer** | Ready-to-paste `resumancer` CLI commands (`resumancer impact "..." --branch ... --commit ...`), one per theme/unblock/reflection. Skips markdown rendering, the commands are the output. |

Parse the trailing argument on invocation:

- No arg, empty arg, or unrecognised arg → default mode (mention "rendering as brag-doc markdown; pass `resumancer` to emit CLI commands instead" once in the report header, so the user discovers the option organically).
- `resumancer` (case-insensitive) → resumancer mode.

Both modes run the same data-collection, theme-clustering, and impact-framing logic, they diverge only at the render step. If a user wants both outputs in one invocation, they can ask after the fact ("now give me the same thing as Resumancer entries").

Other repurposings (performance-review packet grouped by competency, append to an existing brag sheet, dev-journal append at a known path) stay as natural-language follow-ups, they don't change the fundamental shape of the output the way Resumancer mode does.

## Setup (first run only)

Config lives at **`~/.claude/skills/flagrare/config.json`**: a single file shared across all flagrare skills, outside the plugin tree so it survives plugin updates and reinstalls. Skill-agnostic keys (GitHub login, display name, repo scope, local roots) sit at the top level; brag-doc-specific keys nest under `skills["brag-doc"]`.

In Bash, expand `~` explicitly: `"$HOME/.claude/skills/flagrare/config.json"`. The directory may not exist yet, `mkdir -p "$HOME/.claude/skills/flagrare"` before writing.

### Step 1: Migrate legacy config (one-time)

If the new path doesn't exist but a legacy per-skill config does, migrate it:

```bash
LEGACY="{skill_directory}/config.json"   # old location, lost on plugin reinstall
NEW="$HOME/.claude/skills/flagrare/config.json"
if [ ! -f "$NEW" ] && [ -f "$LEGACY" ]; then
  mkdir -p "$(dirname "$NEW")"
  # Brag-doc had no skill-specific keys in the old shape; carry over top-level only.
  jq '{
    github_login, display_name, first_person, repo_scope, local_repo_roots, tracker_mcp
  } | with_entries(select(.value != null))' "$LEGACY" > "$NEW"
fi
```

Tell the user once: "Migrated your config from the old per-plugin location to `~/.claude/skills/flagrare/config.json` so it survives plugin updates."

### Step 2: First-time setup (if no config exists at the new path)

If the file already exists from another flagrare skill (e.g. `standup-report`), reuse the top-level keys silently, no re-prompting. Otherwise collect via `AskUserQuestion`:

1. **GitHub login**: for `author:`, `commenter:`, `reviewed-by:` searches. Run `gh api user --jq '.login'` to detect and confirm.
2. **Display name**: how to refer to the user. Default to first-person ("I").
3. **Repo scope**: `org:<name>`, `user:<login>`, or explicit `owner/repo` list.
4. **Local repo roots**: directories to scan for commits (e.g., `~/Dev`, `~/work`).
5. **Tracker MCP**: detect Linear / Jira / Notion / Asana / Shortcut / Trello in the session; ask which is in use.
6. **Optional extra MCPs**: Slack, calendar, etc., for narrative context (a meeting that produced a decision, a thread that explained a regression).

Brag-doc may also carry skill-specific keys under `skills["brag-doc"]`:

- `journal_path`, where to append the rendered brag doc (set on first save)
- `resumancer_branches`, a map of theme → branch name to avoid re-guessing in Resumancer mode

These are written lazily as the user answers follow-up prompts (e.g. "save to `~/notes/brag.md`" → persist `journal_path`); don't ask up front.

Save shape:

```json
{
  "github_login": "aturing",
  "display_name": "Alan",
  "first_person": true,
  "repo_scope": { "type": "org", "value": "acme-corp" },
  "local_repo_roots": ["~/Dev", "~/work"],
  "tracker_mcp": "linear",
  "skills": {
    "brag-doc": {
      "journal_path": "~/notes/brag.md",
      "resumancer_branches": { "reliability": "reliability", "reviews": "reviews" }
    }
  }
}
```

Confirm with the user before saving. Preserve any pre-existing `skills.*` blocks from other flagrare skills, merge, don't overwrite.

If the user says "reconfigure" or "edit setup", re-run, but only rewrite the `skills["brag-doc"]` block plus any top-level keys the user changes.

## Resolve the time window

At every invocation, ask `AskUserQuestion` what window to cover. The user explicitly opted for no default, the question runs every time so the answer is always fresh.

Offer these preset options (the tool auto-adds an "Other" free-form field for custom ranges):

| Option | Meaning |
|---|---|
| **Today** | 00:00 today → now |
| **This week** | Monday 00:00 this week → now |
| **Last week** | Monday 00:00 last week → Sunday 23:59 last week |
| **Last 2 weeks (biweek)** | 14 days ago → now |
| **This month** | 1st of this month 00:00 → now |
| **Last month** | 1st of last month → last day of last month |

If the user picks "Other", they can type ranges like:

- `since 2026-05-01`
- `2026-05-01 to 2026-05-15`
- `last 10 days`
- `Q1 2026`
- `since my last brag doc`, if a prior brag doc exists in the configured journal path, use its end date as the start

Parse and resolve the custom range into concrete ISO dates before collecting data.

If the user passed a window in the original invocation prompt ("brag doc for the last month", "brag doc since May"), skip the `AskUserQuestion` and use that, but state the resolved window in the report header so they can verify.

## Data collection

Run in parallel (independent queries, slow if serialised). Same shape as `standup-report` but the window is wider, so be ready for more results.

### 1. GitHub: your authored PR activity

```bash
gh api "search/issues?q={SCOPE}+is:pr+author:{LOGIN}+updated:{FROM}..{TO}&per_page=100" \
  --jq '.items[] | {number, title, html_url, state, draft, merged_at, created_at, updated_at, body, repo: (.repository_url | split("/") | last), labels: [.labels[].name]}'
```

Page through results if the window is long enough that 100 may not cover it.

For each PR returned, fetch:

- **Your commits on the PR**: subject + body (carries the "why")
- **Reviews on the PR**: who approved, who requested changes, what they said
- **Linked issues / tickets** from body (extract `[A-Z]{2,5}-\d+`, `#\d+`, Notion URLs)

### 2. GitHub: reviews you gave

```bash
gh api "search/issues?q={SCOPE}+is:pr+reviewed-by:{LOGIN}+updated:{FROM}..{TO}&per_page=100"
```

For each, fetch your specific reviews, state (`APPROVED` / `CHANGES_REQUESTED` / `COMMENTED`), and the body text. **The review body matters most for brag-doc** because that's where your judgment shows up.

### 3. GitHub: comment-only contributions

PRs where you commented but didn't author or formally review. Often: pull request comments where you flagged a concern, design discussions, RFC threads.

### 4. Local git commits

For each configured local repo root, enumerate `*/.git/` and run:

```bash
git -C {repo} log --author="{LOGIN_OR_EMAIL}" \
  --since="{FROM}" --until="{TO} 23:59:59" \
  --pretty=format:'%H|%ai|%s|%b%n---'
```

Dedupe against PR commits already collected.

### 5. Deploys / releases

For each merged PR, check whether a release workflow fired and what its outcome was:

```bash
gh api "repos/{OWNER}/{REPO}/actions/runs?created=>={MERGE_DATE}&per_page=20" \
  --jq '.workflow_runs[] | select(.name | test("release|deploy|publish"; "i"))'
```

Match by `head_sha` or time proximity. A merged PR that did NOT deploy successfully is a separate beat in the brag doc, surface it explicitly.

### 6. Linked tickets

For each ticket reference in PR bodies/titles, fetch the ticket's title and current status from the configured tracker MCP. The **title is the human name of the work**: use it in the prose, not the ticket ID.

### 7. Optional MCP context

Slack threads, calendar events, anything else the user opted into. Treat as narrative seasoning, not primary data, they add *why* and *who else cared*, but the brag doc still works without them.

### 8. Contributions log

Run `python3 <plugin root>/lib/career/career_state.py contributions --home "$HOME"` (the plugin root is two directories above this skill's base directory). It returns the entries of the career contributions log that `/flagrare:impact-scan` keeps, from both `~/.claude/skills/flagrare/career/contributions.log.md` and the older `senior-scan/` copy, without duplicates. Keep the entries dated inside the window. Each one is a contribution the user already chose to make and post (a review that changed a decision, a question answered with evidence, a problem found and handed to the right team), with its link and one sentence on what it changed: this is first-class evidence, not seasoning. It feeds **What I unblocked** for answers and reviews, and **What I shipped** when the entry is work the user drove. When an entry carries `| row: <id>`, it names the promotion rubric row it demonstrates; keep that tie when the output is for a review packet. If the command returns nothing, skip this source.

### 8b. Measured results

Run `python3 <plugin root>/lib/career/measurements.py show --home "$HOME"`. For work in the window that has a measurement (match by `work.link` against the PRs, tickets and log entries you collected), lead with its result sentence (action, measured result, impact) and keep its confidence level and source next to it. Work without a measurement is described as what was done, never given a number it does not have; when it matters for a review packet, suggest `/flagrare:measure-impact` past for it.

### 9. Recognition from peers

When `~/.claude/skills/flagrare/career/recognition.json` exists (a peer-recognition tool such as Bonusly is set up; see `/flagrare:promotion`), read the bonuses received in the window with `python3 <plugin root>/lib/career/recognition.py summary --home "$HOME" --today <date>` or straight from the file. Each is a peer saying what the user did, with a link: use the `text` (the thanks, cleaned) as supporting evidence for the work it names, never as a headline on its own, and quote only what is about the user.

## Naming work in human terms

Same priority order as `standup-report`:

1. **Linked ticket title**, lowercased, trimmed of leading verbs ("Fix image cache eviction" → "the image cache eviction")
2. **PR title with conventional-commit prefix stripped**
3. **Commit message subject**
4. **First meaningful file path** as a last resort

The phrase goes in prose. PR numbers, ticket IDs, commit SHAs go in the `Refs` footnote.

## Synthesis: the brag-doc voice

This is where the skill earns its keep. A weekly window might contain 15 commits across 6 PRs plus 4 reviews and 2 tickets closed. The naive output enumerates all of that. The brag-doc output **clusters those events into 3-5 impact themes** and writes each theme with the principles below.

### The seven shifts

1. **Cluster into themes, not chronology.** Group by impact area, not by what shipped first. Same files touched repeatedly = same thread. Same ticket area = same thread. Same problem domain = same thread. A theme is "the image-cache stability work", not "Tuesday's PRs".

2. **Lead each theme with the outcome.** The first sentence of each theme states **what got better, by how much, for whom**. Not "I worked on the image cache", *"The image-cache regression that was paging the on-call rotation for a week is fixed; error rates on the hot path dropped from 4.2% to 0.1%."* Outcome first, then the *how*.

3. **Quantify ruthlessly.** Numbers, percentages, durations, scale, count of affected users. Mine them from commit messages, PR bodies, ticket scopes, deploy metrics. *"Reduced p99 latency from 800ms to 480ms"* beats *"improved latency"*. If no numbers are available, use scale qualifiers, *"the entire admin API surface"*, *"the on-call rotation for two weeks"*, *"every job-application form in the product"*. Vague impact reads as inflated impact.

4. **Own the work in active voice, first-person.** *"I designed and shipped"*, *"I caught"*, *"I pushed back on"*, *"I unblocked"*. Never passive, *"the auth refactor was completed"* is the construction of someone who doesn't want to claim it. The brag doc is exactly the place to claim it.

5. **Separate IC contributions from amplification.** Things you built yourself are IC work. Things you unblocked others to ship, reviews that changed direction, mentoring, design feedback that prevented a wrong turn, are amplification. Both matter. A staff/senior brag doc has both, named distinctly. Don't list every review; surface only the ones where your input *materially shifted* what someone else did.

6. **Highlight judgment, not just shipping.** What did you *decide*? What tradeoff did you make? What did you push back on? What edge case did you catch that nobody else flagged? What future risk did you surface? This is the layer that separates a junior brag doc (lists artifacts) from a staff one (names decisions). If a theme has no judgment visible, dig back into the PR review threads and commit bodies, it's almost always there, just unsurfaced.

7. **Acknowledge growth and learning.** New systems you understood for the first time, hard debugs that taught something, decisions made under uncertainty. Including this prevents the brag doc from reading as pure trophy display, it becomes a development record too. Skip the section if nothing meaningful belongs in it; don't fabricate.

### Vocabulary that signals seniority

Use these verbs liberally, they communicate ownership and craft:

> designed, shipped, owned, unblocked, flagged, pushed back, caught, mitigated, instrumented, profiled, refactored toward, deprecated, simplified, prevented

Avoid these, they hedge or hide:

> worked on, looked at, addressed, fixed (without object), helped with, contributed to, was involved in

### Before / after

Same five events, two ways. Both accurate, only one is brag-doc material.

**❌ Bland enumeration:**

> This week I fixed the image cache eviction bug, reviewed Daniel's auth refactor, requested changes on Carol's cache benchmarks, addressed feedback on my queue refactor, and spiked queue sharding.

**✅ Brag-doc voice:**

> **Image-cache stability.** The week's headline was killing a regression that was paging the on-call rotation daily, root cause was the LRU admitting entries faster than it could evict under burst load, amplified by our retry policy. I shipped the fix Wednesday; error rate on the hot path dropped from 4.2% to 0.1%, the pages stopped, and a follow-up post-mortem documenting the failure mode landed Friday.
>
> **Unblocking the auth refactor.** Daniel had been blocked on the auth-service migration for two days waiting on review of a 1200-line PR. I reviewed it Tuesday, agreed on the rollback path inline, and surfaced one race condition in the token-refresh handler that would have failed silently in staging. He shipped it Thursday on schedule.
>
> **Pushing back on cache-benchmark methodology.** Carol's PR proposed shipping cache-eviction tuning based on a synthetic workload that didn't reflect production access patterns. I requested changes with a one-page write-up of what production looks like and why the proposed thresholds would have driven the wrong tuning decisions next quarter. We're aligned on a new benchmark approach.
>
> **Queue refactor back in review** after addressing the back-pressure concerns from last sprint, should land early next week.
>
> **Parked queue-sharding** after a half-day spike showed the bottleneck is upstream in the producer side, not the queue itself. Saved a week of misdirected work; refocusing on the producer next sprint.

Notice what changed: each theme leads with the *consequence*, names the *root cause* or judgment call, and quantifies where possible. The reader walks away knowing what's better about the system, not what tickets moved columns.

## Output format

```markdown
# Brag Doc: {window_human}
> {N PRs merged} | {M reviews given} | {K commits} | {J tickets closed} | {covering: from → to}

## Headline

{2-3 sentences. The single most consequential thing this period made
better. The elevator pitch for the whole window. If the window had no
single headline, name the two or three biggest themes in one sentence
each, joined by impact framing.}

## What I shipped

### {Theme 1 name}
{Lead with outcome (what got better, by how much, for whom). Then a
paragraph: how I did it, what was hard, what judgment was involved.
2-5 sentences. Concrete numbers where available; scale qualifiers
otherwise.}

### {Theme 2 name}
...

{3-6 themes is typical. If a window has fewer than 3, that's fine, 
don't pad. If more than 6, you're probably under-clustering; group
harder.}

## What I unblocked

{IC amplification. Reviews that changed direction, mentoring, design
feedback that prevented a wrong turn. Don't list every review, only
ones where your input materially shifted what someone else did.
Format: paragraph or themed bullets, your choice based on volume.}

## What I learned

{Optional. New systems, hard debugs, decisions under uncertainty.
Including this turns the brag doc into a development record, not just
a trophy case. Omit if there's nothing genuine to put here, never
fabricate.}

## Open threads

{What's in flight, parked, or still tricky going into the next period.
Forward-looking context that helps future-you remember the state of
play. 2-4 bullets max.}

## Refs

{Compact footnote, one line per theme with the actual PR / ticket /
commit / deploy identifiers, so the brag doc can be re-grounded in
the underlying artifacts.}

- image-cache stability, acme/api#481, ENG-142, deployed 2026-05-22
- auth refactor (Daniel), acme/api#478 (reviewed)
- cache-benchmark methodology, acme/api#479 (changes requested)
- queue refactor, acme/api#476 (in review)
- queue-sharding spike, local commits in acme/queue-svc
```

### Length rules of thumb

| Window | Target word count |
|---|---|
| Day | 200-400 |
| Week | 400-800 |
| Biweek | 600-1200 |
| Month | 1000-1800 |
| Quarter+ | 1500-3000; consider summarising into 3-5 mega-themes |

Long enough to capture nuance. Short enough that future-you will actually re-read it. If you're approaching the upper bound, group harder, fewer, deeper themes beat more, thinner ones.

## Rendering by mode

### Default mode: brag-doc markdown

Use the report template above (`# Brag Doc: {window} / ## Headline / ## What I shipped / ## What I unblocked / ## What I learned / ## Open threads / ## Refs`). This is the format that works as-is for a dev journal, a personal brag sheet, or a performance-review packet.

After rendering, two natural follow-ups the user might ask for:

- **Append to journal / running brag sheet.** If the user has a configured journal or brag-sheet path under `skills["brag-doc"].journal_path` in `~/.claude/skills/flagrare/config.json`, offer to append under a dated heading. If they request a save without a path, default to `./brag-{YYYY-MM-DD}.md` and offer to persist that choice under `journal_path` so the next run defaults to it.
- **Performance-review packet framing.** Same content, regrouped by competency axes (ownership, technical depth, collaboration, growth) instead of by chronology. If the user provides their company's review rubric, map themes to the rubric's axes; otherwise default to the standard four.

### Resumancer mode: CLI commands

Triggered by `/flagrare:brag-doc resumancer` or by trigger phrases like "log my wins to resumancer", "make resumancer entries for this week".

Run the same synthesis (theme clustering, impact framing, vocabulary discipline), but emit the output as a bash code block of `resumancer` CLI commands the user can paste into their terminal. Skip the markdown brag-doc rendering entirely, the commands are the output.

Map themes to Resumancer command types:

| Source | Command | Why |
|---|---|---|
| **Shipped theme with a quantified outcome** | `impact` | The numbers are the point; `impact` is for "what got better, by how much" |
| **Shipped theme that's primarily a new capability** | `build` | `build` is for "I shipped X" without a numeric outcome to anchor |
| **Unblock / amplification** | `impact` | Your judgment moved someone else's work forward, that's impact, not a build |
| **Learning / reflection** | `reflection` | Pattern noticed, hard debug, decision under uncertainty |
| **Open thread (in flight or parked)** | `goal` | Forward-looking; what you're aiming at next |

For each entry, populate:

- **Message**: the impact-framed sentence (use the same outcome-first vocabulary as the markdown mode). One concrete claim per entry, not a paragraph.
- **`--commit <sha>`**: when a single commit anchors the work, surface it. For multi-commit themes, pick the most representative (usually the merge commit or the final fix).
- **`--branch <name>`**: use the configured Resumancer branch if known (the shared config may carry one under `skills["brag-doc"].resumancer_branches`). Otherwise default to a plausible name based on the theme (e.g. `reliability`, `reviews`, `reflections`) and tell the user to swap if it doesn't match their setup.
- **`--public`**: add for headline-worthy shipped impact (likely to surface in a profile / portfolio). Omit for reflections and internal-only work.

Example output for the same five-event week shown in the before/after:

```bash
resumancer impact "killed the image-cache regression that was paging on-call rotation daily — error rate on the hot path dropped 4.2% → 0.1% after fixing the LRU admission/eviction balance under burst load" --commit 8b36fb5 --branch reliability --public
resumancer impact "unblocked Daniel on the auth-service migration: reviewed the 1200-line PR Tuesday, agreed on the rollback path inline, caught a race in token-refresh that would have failed silently in staging — shipped Thursday on schedule" --branch reviews
resumancer impact "pushed back on Carol's cache-benchmark methodology with a one-page writeup of why the synthetic workload didn't match production — prevented shipping eviction tuning that would have driven the wrong decisions next quarter" --branch reviews
resumancer build "queue refactor back in review after addressing back-pressure concerns from last sprint" --branch queue
resumancer reflection "half-day spike on queue-sharding revealed the bottleneck is upstream in the producer side, not the queue itself — saved a week of misdirected work" --branch queue
```

Map themes to entries thoughtfully. One theme may produce two entries (the `build` + the `impact`), or one `impact` that subsumes both. Resist the urge to emit one entry per PR, that's the bland-enumeration trap the markdown mode also warns against.

When `skills["brag-doc"].resumancer_branches` is missing from the shared config, output reasonable defaults and add a one-line note at the top of the code block: `# Branches are guesses, swap to your own if they don't match.` After the user confirms the branches they actually use, offer to persist them.

## Edge cases

- **Empty window** (PTO, sick, all-meetings): render a short doc that says so explicitly. *"Quiet period, no code shipped between {from} and {to}. {If MCPs surface meeting context, mention it: 'most of the week was the Q3 planning offsite.'} Resuming next period."* Don't fabricate beats.
- **Single-day window**: shape is similar to `standup-report` but framed as durable. If the user really wants a same-day-as-standup retrospective, point out the overlap and offer to invoke standup-report instead.
- **Very long window (3+ months)**: warn that the data volume may require aggressive clustering and that fine-grained detail will be lost. Offer to break it into monthly sub-docs.
- **Mostly review work, no authored PRs**: the brag doc shape inverts, "What I unblocked" becomes the dominant section, "What I shipped" might be a single short paragraph. That's a valid shape; don't force a fake "shipped" section.
- **MCP unavailable**: skip silently for tracker/Slack; warn explicitly if `gh` is unauthenticated since GitHub is the primary source.
- **Window before the user joined the GitHub org**: report what's there but note the gap.

## Output

Render the full brag doc inline in the conversation.

If the user asks to save it, default to `./brag-{YYYY-MM-DD}.md` in the current working directory, with the date being the *end* of the window.

If the user has a configured journal/brag-doc path (in `~/.claude/skills/flagrare/config.json` under `skills["brag-doc"].journal_path`), offer to append there instead.
