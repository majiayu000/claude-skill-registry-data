---
name: pr-digest
description: "Generate the weekly PR digest, iterate on it with the user, post to Notion, then generate and post Slack blurb. Use when asked to 'write the digest', 'pr digest', 'weekly digest', 'infra update', or 'post the digest'."
argument-hint: "[--days N]"
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
  - ReadMcpResourceTool
  - mcp__notiongusto__notion-create-pages
  - mcp__notiongusto__notion-update-page
  - mcp__notiongusto__notion-fetch
  - mcp__slackgustoofficialmcp__slack_read_channel
  - mcp__slackgustoofficialmcp__slack_send_message
---

# PR Digest Skill

Generate the weekly engineering digest, collaborate with the user on wording, post to Notion, then generate and post the Slack announcement.

## Step 1: Fetch PR Data

Determine the `--days` value: use the user's argument if provided, otherwise default to 8 (one extra day beyond a full week to handle timezone edge cases).

Run the fetch script from the repo root:

```bash
scripts/pr_digest/generate --fetch-only --days {days}
```

If the script exits with an error or the output is empty, tell the user and stop.

Save the PR data output for use in the next step.

## Step 2: Gather Rollout Context

Rollout status, deprecations, and product renames often live in `#retirement-eng-announcements`, not in any PR body. Gather them so the digest frames the week correctly on the first draft.

1. **Read the announcements channel over the same window as `--days`.** `slack_read_channel` returns messages newest-first and caps `limit` at 100, so a single call can miss week-old posts in a busy channel. Paginate:
   - Compute `oldest` = unix timestamp for `today - {days}`.
   - Loop: call `slack_read_channel` with `channel_id: C09RE71FK52`, `oldest`, `limit: 100`; accumulate messages; follow `next_cursor` until the oldest returned message timestamp is `< oldest` or there is no cursor.
   - Cap the loop at 10 pages. If the cap is hit, warn the user that the window may be incompletely read.
   - **If `slack_read_channel` errors** (permissions, archived, rate-limit, MCP failure): tell the user and ask whether to proceed without context or retry. Do NOT silently treat an error like a quiet channel.
2. **Extract announcement-only facts:** rollout percentages, deprecations, product renames/lineage, "X replaces Y". Ignore ordinary chatter.
3. **Draft a `## Additional Context` block** — a short bulleted list of those facts.
4. **Confirm with the user** via `AskUserQuestion` (confirm / edit / add). Also ask whether any internal codename should be scrubbed from the digest and what to replace it with (feeds the scrub map in Step 3).

**Empty contract:** if no facts are found and the user adds none, produce NO context block. Do not pass an empty `## Additional Context` header into generation (the prompt treats that block as authoritative and would over-weight nothing).

## Step 3: Generate the Detailed Digest

First, read the prompt template at `scripts/pr_digest/prompts/weekly.md`. It contains the PR selection criteria, output format, output constraints, writing style rules, and an example. Follow ALL of those rules exactly when generating the digest.

Key adaptations from the prompt template (these override any conflicting instructions in weekly.md):

- Generate ONLY the detailed digest (Block 2 from the template). Ignore Block 1 entirely; the Slack blurb comes later in Step 6.
- Do NOT wrap the output in `---BEGIN/END DETAILED DIGEST---` delimiters. Do NOT output the `---BEGIN SLACK ANNOUNCEMENT---` block. Just output the raw digest content directly.
- Use today's date for the title.

**Feed the context in:** if Step 2 produced a context block, prepend it to the PR data using the literal `## Additional Context` header (the exact string the prompt keys on) immediately before the PR-data section. If Step 2 produced no block, feed the PR data alone.

Using the PR data from Step 1 (and the Additional Context block if present), generate the detailed digest.

**Scrub codenames (deterministic) before presenting.** After generating, run a literal, case-insensitive, whole-word search-and-replace over the draft using a substitution map:

- Seed the map with `Armadillo` → `Okta SSO login`.
- Add one entry per token the user flagged in Step 2.
- If a banned token appears but has no mapping, halt and ask the user for the replacement — never blind-delete the token (it leaves a dangling sentence).

Do NOT do this by re-prompting the model (that reintroduces the leak nondeterministically); it is a mechanical string replacement. Note in the review step which tokens were rewritten.

Present the (scrubbed) generated digest to the user.

## Step 4: Interactive Review of Detailed Digest

Ask the user for feedback on the digest using `AskUserQuestion`. Options:

- **Approve** — proceed to posting
- **Request changes** — user describes what to change

If the user requests changes, apply them and present the revised digest. Repeat until approved.

## Step 5: Post to Notion

Once the digest is approved:

1. **Fetch the Notion enhanced markdown spec** using `ReadMcpResourceTool` with server `notiongusto` and URI `notion://docs/enhanced-markdown-spec`. Use this to ensure the content is formatted correctly for Notion.

2. **Extract the title** from the first line of the digest (the `# YYYY-MM-DD: ...` line). Strip the `# ` prefix for the page title. The body content is everything after that first line.

3. **Create the new page** as a child of the parent page:
   - Parent page ID: `315ad673c6c2807d9df3f251e6a3b610`
   - Title: the extracted title (e.g., "2026-04-17: AI tooling, test runner updates")
   - Content: the digest body (everything after the title line)

4. **Extract the new page URL** from the creation response.

5. **Fetch the parent page** content using `mcp__notiongusto__notion-fetch` with the parent page ID.

6. **Prepend a link** to the new page at the very top of the parent page content (above all existing entries), so entries are always sorted descending by date. Match the format of existing entries on the index page. Use `mcp__notiongusto__notion-update-page` to update the content. If this update fails, continue to Step 6 anyway and note to the user that the index page was not updated.

7. **Report the new page URL** to the user. Keep this URL for the Slack blurb.

## Step 6: Generate the Slack Blurb

Generate a short Slack announcement using the same PR data and the Notion page URL from Step 5. Format:

```
:robot: hi gang, welcome to this week's update of infra stuff we've shipped that you might find useful for your teams adventures™.

<one paragraph summarizing the most important/useful changes, 2-4 sentences max>

- :books: [Full digest](<NOTION_PAGE_URL>)
- :notion: [Index](https://www.notion.so/Retirement-Platform-Engineering-Infra-Updates-315ad673c6c2807d9df3f251e6a3b610)
```

Rules (also see Block 1 rules in `scripts/pr_digest/prompts/weekly.md`):

- Highlight only the 2-3 most impactful changes
- Keep it concise enough to scan in Slack without expanding
- Same friendly, informal tone and writing style rules as the digest
- Use the real Notion page URL (not a placeholder)

Present the blurb to the user.

## Step 7: Interactive Review of Slack Blurb

Same as Step 4. Ask the user for feedback via `AskUserQuestion`:

- **Approve** — proceed to posting
- **Request changes** — revise and re-present

Repeat until approved.

## Step 8: Post to Slack

Post the approved blurb to `#retirement-eng-announcements`:

- Channel ID: `C09RE71FK52`
- Use `mcp__slackgustoofficialmcp__slack_send_message`

If the Slack post fails, report the error to the user and provide the approved blurb text so they can post it manually.

Share the Slack message permalink with the user.
