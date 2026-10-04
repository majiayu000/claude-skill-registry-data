---
name: activity-roundup
description: "Builds a time-boxed roundup of what happened across chat, email, documents, work trackers, code hosting, calendars, and CRM, sorts every item into priority tiers, and puts the user's action items at the very top with requester, source link, deadline, and waiting time. Use when the user asks what they missed, wants a daily or weekly digest, is catching up after time off, or wants a summary of recent activity for a team, project, or selected sources."
---

# Activity Roundup

You help the user catch up. Pull together everything that happened in a given time window across their connected tools and sources, decide what actually needs them, and deliver a digest that opens with their to-dos and ends with the nice-to-know. Every line you write must point back to where it came from.

## Sources to draw on

Work with whichever tools and sources are connected. What each kind typically yields for a roundup:

- **Chat** (Slack, Microsoft Teams): activity in channels, direct messages, thread discussions, decisions shared in conversation
- **Email** (Gmail, Outlook): incoming mail, threads that need an action, FYI updates
- **Documents and wikis** (Google Drive, SharePoint, OneDrive, Confluence, Notion): documents that are new or changed, comments people shared, page edits
- **Work tracking** (Jira, Linear, Asana, Monday.com): ticket status moves, new assignments, finished work, sprint updates
- **CRM** (Salesforce, HubSpot): deals changing stage, new activities, account updates
- **Code hosting** (GitHub, GitLab, Bitbucket): merged PRs, newly opened issues, release notes, CI/CD status
- **Calendars** (Google Calendar, Outlook Calendar): meetings that took place (as context) and meetings coming up (so the user can prepare)
- **Knowledge bases** (Confluence, Notion, internal wikis): changed policies, fresh articles, revised procedures

When a source isn't connected, say so in the digest header so the reader knows the picture is partial.

## Method

### Phase 1 — Pin down the scope

Settle these four parameters before you collect anything. Use the default unless the user says otherwise.

| Parameter | What you assume by default | How users typically override it |
|---|---|---|
| **Time window** | Daily: since the previous business day. Weekly: since last Monday | "Cover the last 3 days", "Everything since my holiday started on March 20" |
| **Sources** | Every connected source | "Just Slack and Jira", "Leave out email" |
| **Team or project** | All teams the user is a member of | "Only the platform team", "Just Project Atlas" |
| **Depth** | A summary plus action items | "Give me the detailed version", "Headlines only" |

A loose request such as "what did I miss?" gets a daily digest across all sources. Only ask a clarifying question — and just one — when the time window is genuinely unclear, for example because the user was away but hasn't said for how long.

### Phase 2 — Collect the activity

Query every connected source for the chosen window and pull out these kinds of items:

| Item type | Where it shows up | Capture |
|---|---|---|
| **Action items aimed at the user** | Email where they are in to/cc, chat @mentions, tickets assigned to them | The ask, who made it, any urgency signals, the deadline if one is given |
| **Decisions** | Chat threads that reached a resolution, email approval chains, meeting notes in documents | The decision, who made it, what it touches |
| **Status changes** | Project tracker, CRM, CI/CD | Tickets finished, blocked, or reopened; deals moved forward or lost; builds broken or repaired |
| **New content** | Documents, knowledge base, code | Documents that are new or substantially reworked, new wiki pages, merged PRs |
| **Discussions that need the user's input** | Open chat threads, unanswered email questions, PR review requests | The question or request, and how long it has been waiting |
| **FYI updates** | Channel announcements in chat, newsletters and broadcasts by email, shared comments in documents | Informational items with no action attached |

### Phase 3 — Sort into tiers

Place every item in one of three tiers:

1. **Tier 1 — Action required.** Addressed to the user and needs a reply, a decision, or some other action from them. These lead the digest.
2. **Tier 2 — Decisions and changes.** Decisions that affect the user's work, status changes on things they follow, and changes to policy or process. The user needs to know, but doesn't need to act right now.
3. **Tier 3 — Context and FYI.** Broader updates, ongoing conversations, and freshly published content that keep the user in the loop. Not urgent, still worth having.

Inside each tier, order items by:

1. **Urgency** — anything with an explicit deadline or escalation signal goes first
2. **Recency** — among items of equal urgency, newest first
3. **Source authority** — official decisions and tracker updates come before passing mentions in chat

### Phase 4 — Turn Tier 1 into action items

Each Tier 1 item becomes one discrete action item with these fields:

- **Action** — the concrete, specific thing to do
- **Requester** — the person who asked or assigned it
- **Source** — where the ask came from, with a link
- **Deadline** — the deadline as stated, or "No deadline stated"
- **Waiting since** — the length of time the ask has gone unanswered

If one ask surfaces in several places (say, a Slack message and a matching Jira ticket), merge it into a single action item and keep both links.

### Phase 5 — Assemble the digest

Fill in the template below with the sorted, prioritized material.

## Digest template

```markdown
# Activity Roundup — [Date range]

**Period**: [Start date] to [End date]
**Sources checked**: [Sources you searched]
**Not connected**: [Unavailable sources, if any]

---

## Your Action Items ([count])

| # | Action | Requester | Source | Deadline | Waiting since |
|---|--------|-----------|--------|----------|---------------|
| 1 | [Concrete action] | [Name] | [Source + link] | [Date or "None"] | [Duration] |
| 2 | ... | | | | |

---

## Decisions and Changes

### [Grouping — e.g., Project Atlas, Platform Team, Company-wide]
- **[Decision or change]**: [What happened] — [Who decided] — [Source + link]

---

## Where things stand

### Tickets and tasks
- [count] completed | [count] in progress | [count] blocked
- Worth noting: [Unexpected status moves or items that just became blocked]

### Code and deployments
- [count] PRs merged | [count] waiting for review | [count] builds broken/fixed
- Worth noting: [Releases, incidents, significant merges]

### Deals and accounts (only if a CRM is connected)
- [count] deals advanced | [count] deals at risk
- Worth noting: [Significant stage changes]

---

## Discussions Waiting on You
- **[Topic]**: [Question or context] — [Channel/thread + link] — waiting [duration]

---

## FYI — New Content and Announcements
- [Document or announcement title] — [Source + link] — [One-line summary]

---

## How Complete Is This Roundup
- Sources checked: [list]
- Sources unavailable: [list, if any]
- Items left out: [count of low-relevance items filtered out, if significant]
```

## Adjusting the roundup

The user can tune the digest along these dimensions:

- **Cadence** — daily, weekly, or a custom interval. Shifts the default time window and how much detail you include.
- **Sources** — include or exclude particular sources, to cut noise from ones the user doesn't want in the digest.
- **Scope** — a single team, a single project, or the whole organization. Narrows activity to that context.
- **Detail level** — *Headlines* means action items plus one-liners; *Summary* is the standard template above; *Detailed* adds excerpts from the discussions.
- **Delivery** — a chat post, an email, or a document. Reformat the output to suit where it will be read.

## Ground rules

- Never invent activity or make up action items. Each item in the digest has to trace back to a connected source or to something the user told you.
- Never guess at urgency. Mark a deadline only when the source states it explicitly.
- Never summarize content you haven't actually retrieved. Show the metadata and the link instead of guessing at what it says.
- Label every item `[From: source name]`, and list in the digest header which sources you searched and which you did not.
