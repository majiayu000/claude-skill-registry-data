---
name: catch-up
description: Personal daily catch-up dashboard — gathers, for the configured sources, the Slack messages where you're involved in the last week plus your Slack "save for later" items, the Jira tickets assigned to you or open & unassigned, and the open PRs in your repos (open, or where you're mentioned), then distills them into one prioritized "do these first" list rather than dumping everything. On first run, if there's no config, it walks you through setup. Use when asked to "catch up", "what's on me", "my standup", "what needs my attention", "/catch-up", or any "what did I miss / what's waiting on me" request.
---

# /catch-up — what needs my attention

Aggregates three feeds and distills them into a single **prioritized** "do these first" list (not a
dump of everything):

1. **Slack** — messages from the last week where the user is involved (mentions, DMs, replies in their threads), plus their **"save for later" / Later** items, scoped to the configured channels.
2. **Jira** — tickets in the configured project(s) that are **assigned to the user** or **open with no assignee**.
3. **GitHub** — pull requests in the configured repos that are **still open**, or any PR (anywhere) where the user is **mentioned / requested as reviewer**.

The skill is **portable**: it reads everything it needs from a config file and uses whatever
integrations are available. Nothing about a specific employer or repo is baked in.

## Step 1 — Load config

The config file is `.claude/.config/catch-up.json`. **Walk up the directory tree** from the current
working directory looking for it, and stop at `$HOME` (inclusive):

```
<cwd>/.claude/.config/catch-up.json
<cwd>/../.claude/.config/catch-up.json
<cwd>/../../.claude/.config/catch-up.json
… (keep going up) …
$HOME/.claude/.config/catch-up.json
```

**First match wins** — so a project-local `.claude/.config/catch-up.json` overrides the one in
`$HOME`. Never search above `$HOME`. (`$CATCH_UP_CONFIG`, if set, takes precedence over the walk.)

Read the first one found. If it parses and has at least one source configured → go to **Step 3
(Run)**.

If the file is missing or empty → go to **Step 2 (Configure)**.

If the user invoked the skill with an argument like `configure`, `setup`, `reconfigure`, or
`--config` → go to **Step 2** regardless.

## Step 2 — Configure (first run)

Tell the user there's no config yet and you'll set one up. Collect the values below by **asking the
user** (conversationally, or with `AskUserQuestion` for the bounded choices). For each source you
include, you **must explicitly ask for that source's specifics** — never silently fall back to a
default. In particular:

- **Ask which Slack channels** to scope to. Don't assume "everywhere": present it as a real choice
  ("specific channels, or search everywhere you can see?") and only record `[]` if the user
  actively chooses unscoped. List the channel names back to them before writing.
- **Ask which Jira project keys** to include.
- **Ask which GitHub repos** (`owner/name`) to watch.

Only skip a source entirely if the user says they don't want it — in which case omit its key so it's
skipped at run time.

```jsonc
{
  "lookbackDays": 7,                      // Slack/PR recency window
  "identity": {
    "slackHandle": "jdoe",                // your Slack display name or @handle (for "mentions you")
    "githubLogin": "jdoe"                 // optional; gh defaults to @me if omitted
  },
  "slack": {
    "channels": ["#team", "#general"]     // ask the user; [] only if they choose unscoped search
  },
  "jira": {
    "projects": ["PROJ"]                  // one or more project keys
  },
  "github": {
    "repos": ["owner/repo-a", "owner/repo-b"]
  }
}
```

Notes when collecting:

- **Slack handle** — needed to find "messages that mention you". Confirm the exact display
  name/handle; if unsure, you can resolve it with `slack_search_users`.
- **Jira projects** — project keys (e.g. `PROJ`). The JQL uses `currentUser()`, so no account id
  is needed.
- **GitHub repos** — `owner/name` slugs. Reviewer/mention search uses `@me`, so login is optional.

Write the file to `$HOME/.claude/.config/catch-up.json` by default (so it applies in every project),
creating the `.claude/.config/` directory first. If the user wants this config to apply only to the
current project, write it to `<repo-root>/.claude/.config/catch-up.json` instead. Then continue to
**Step 3** with the values you just collected.

## Step 3 — Run

Compute the cutoff date once: `date -d "-${lookbackDays} days" +%Y-%m-%d` (GNU) — keep it as a
`YYYY-MM-DD` string for both Slack and GitHub queries.

Run the three source checks **in parallel** (independent — fire them in one batch). Skip any source
that isn't present in the config. If an integration/tool is unavailable, note it as "unavailable"
rather than failing the whole run.

**Fan out within each source too** — don't loop sequentially. Issue one query per configured
**Slack channel**, one per **Jira project**, and one per **GitHub repo**, all in the same parallel
batch, then merge the results. With N channels + M projects + K repos you should have ~N+M+K queries
in flight at once, not one-at-a-time.

### Slack — involved in the last week

Use the Slack search tools. Run, for the configured `channels` (or unscoped if `channels` is empty):

- Mentions of the user: query `@<slackHandle> after:<cutoff>` (add `in:#channel` per channel when scoped).
- Their own thread activity / DMs: query `from:@<slackHandle> after:<cutoff>` to catch threads they
  drove and conversations awaiting their reply.

Prefer `slack_search_public_and_private` if available, else `slack_search_public`. Collapse results
to the distinct threads/conversations; for each, capture channel, who, a one-line gist, and a link.

Also pull the user's **"save for later" / Later** items — messages they explicitly bookmarked to
come back to. These are high-signal by definition (the user chose them), so treat them as such when
ranking. There may be no dedicated MCP tool for this; if so, fetch them via the Slack Web API
`stars.list` / saved-items endpoint (e.g. through the `slack:slack-api` skill or a `curl` with the
workspace token). If no such access is available, note "Later items: unavailable" rather than
dropping the category silently.

**Read the thread before ranking any Slack item as blocked-on-you.** A single matched message is a
snippet, not a verdict — a mention that reads like an open question to the user is often already
answered by them further down the thread, or the whole incident is resolved. For every Slack item a
first pass would rank in tier 1 (directly blocked on you), pull the full thread with
`slack_read_thread` and check whether the user already replied and whether the ask still stands. Only
keep it in tier 1 if it's genuinely still waiting; otherwise demote it (already-replied → tier 3, or
drop it into the rolled-up tail). This costs a few extra reads but is what stops false "you owe a
reply" items. Do this for the tier-1 candidates, not the whole feed.

### Jira — assigned to me or open & unassigned

Run **one query per configured project, in parallel** (`searchJiraIssuesUsingJql`, Atlassian MCP):

```
project = <PROJECT>
AND statusCategory != Done
AND (assignee = currentUser() OR assignee IS EMPTY)
ORDER BY updated DESC
```

Merge the per-project results. For each issue capture key, summary, status, assignee (or
"unassigned"), and updated date.

### GitHub — open PRs in my repos + PRs that mention me

Use the `gh` CLI via Bash (most portable — no MCP dependency). Run these concurrently (separate
background Bash calls, or one batch), not in a sequential loop:

- Per configured repo, open PRs — **one `gh pr list` per repo, in parallel**:
  `gh pr list --repo <repo> --state open --json number,title,author,url,updatedAt,isDraft,reviewRequests`
- Mentioned / review-requested anywhere (cross-repo):
  `gh search prs --state open --involves @me --json number,title,repository,url,updatedAt`
  and `gh search prs --state open --review-requested @me --json number,title,repository,url,updatedAt`

Merge and de-duplicate by URL. Flag the ones awaiting the user's review distinctly from the ones
they authored.

## Step 4 — Prioritize, then present

**Don't dump every item.** Pull the raw results from all sources into one pool, then **rank** them
into a single priority list. The output is a short, ordered "do these first" list — not three full
feeds.

Score each item by how much it's **actively waiting on the user** and how urgent it is. Rough order,
highest first:

1. **Directly blocked on you** — a PR with your review requested, a Jira ticket assigned to you that's
   In Progress, a Slack mention that asks you a direct question and is unanswered (verify against the
   full thread — see the Slack section; a snippet that looks unanswered often isn't), an item you
   **saved for later** in Slack.
2. **Owned by you, in flight** — your open PRs (esp. non-draft, with changes requested or stale), your
   assigned tickets not yet started.
3. **Up for grabs / FYI** — unassigned open tickets, threads you were in but already replied to,
   draft PRs.

Apply judgment on top of the tier: bump items that are **older / going stale** (e.g. a review request
sitting for days), and **collapse noise** — group near-duplicates, and roll long tails into a single
"…and N more" line with a link rather than listing each. Aim for roughly the **top ~10 items**; the
rest is a count, not a wall of bullets.

Render as one ranked list (links so each item is one click away). Annotate each with its source, why
it's ranked there, and its age. Example shape:

```
🟢 Catch-up — last 7 days · 10 of 34 items shown

1. PR  owner/repo #123  Fix retry backoff       review requested · 4d, stale   <url>
2. Slack ⭐ saved  @alice "can you confirm the rollout window?"  · 2d           <url>
3. Jira PROJ-456  Flaky scanner test            assigned to you · In Progress  <url>
4. PR  owner/repo #119  Queue split             yours · changes requested      <url>
5. Slack #team  @bob pinged you on the migration plan (unanswered) · 1d        <url>
6. Jira PROJ-461  Tune cache TTL                open · unassigned              <url>
…
   + 24 more (8 Slack threads you've already replied to, 3 draft PRs, …)
```

If a source was skipped (not configured) or unavailable, say so in one line at the end rather than
silently omitting it.

## Re-configuring

`/catch-up configure` (or `setup` / `reconfigure`) re-runs Step 2 and overwrites the config file.
