---
name: issue-draft-release-notes
category: business-product
codex-short-description: "Draft a customer-facing release note for a Jira ticket from ticket + MR context"
description: >
  Draft a customer-facing release note for a Jira ticket from its context and linked merge
  requests. Read-only unless the user opts in to publish. Use when the user says "draft
  release notes", "write a release note", "release note for [TICKET-KEY]", or invokes
  /issue-draft-release-notes.
allowed-tools:
  - Read
  - Bash
  - AskUserQuestion
  - Agent
  - Skill
  - mcp__atlassian__jira_get_issue
  - mcp__atlassian__jira_get_comments
  - mcp__atlassian__jira_get_remote_links
  - mcp__atlassian__jira_get_changelog
  - mcp__atlassian__jira_search
  - mcp__atlassian__jira_add_comment
  - mcp__atlassian__jira_update_issue
  - mcp__gitlab-mcp__list_merge_requests
  - mcp__gitlab-mcp__get_merge_request
  - mcp__gitlab-mcp__get_merge_request_diffs
  - mcp__gitlab-mcp__list_merge_request_changed_files
related-skills:
  - clarity-council
  - writing-humanize
loop-eligible: false
compatibility: claude-code codex opencode
---

# Issue — Draft Release Notes

Read-only drafting of a customer-facing release note for a Jira ticket. Gathers ticket context and related MR code changes, synthesizes a release note matched to the audience, runs a quality pass, and (only on opt-in) posts it back to the ticket.

**Read-only by default.** The skill never modifies code, MRs, Confluence, or Jira fields. The single permitted write is in Phase 6 — and only after explicit user opt-in: posting the note as a Jira comment, or setting a Release Notes field.

## Input

A Jira ticket key — pattern `[A-Z][A-Z0-9]+-\d+` (e.g. `PRJ-1234`). Extract from the user's message. If no key is present, ask for one. Default project key (if the user gives only a number) is read from memory (`reference_jira_default_project.md`).

## Workflow

```text
Release-Notes Progress:
- [ ] Phase 1: Gather ticket context
- [ ] Phase 2: Find & analyze related MRs / code changes
- [ ] Phase 3: Determine audience & note type
- [ ] Phase 4: Draft the release note
- [ ] Phase 5: Quality pass (clarity-council + writing-humanize)
- [ ] Phase 6: Optionally publish back to the ticket (user opt-in)
```

### Phase 1 — Gather ticket context

- `jira_get_issue` — summary, description, issue type, status, priority, components, labels, **fix version(s)**, affected version, resolution.
- `jira_get_comments` — capture what was actually implemented vs. originally scoped; watch for "done / shipped in" notes.
- `jira_get_remote_links` — capture linked GitLab MR URLs and Confluence pages.

The **issue type** and **fix version** strongly shape the note: a `Bug` reads as a fix, a `Story`/`Feature` as a capability, a `Task` may be internal-only (flag it). Compile a short **Context Summary** and present it.

### Phase 2 — Find & analyze related MRs / code changes

Locate merge requests tied to this ticket:

1. **From remote links** — any GitLab MR URLs captured in Phase 1; fetch each via `get_merge_request`.
2. **By search** — `list_merge_requests` filtered on the ticket key (MR titles and branch names usually embed it, e.g. `feature/PRJ-1234-...`). Limit to the most relevant 5.
3. For each relevant MR: read the **title, description, and changed-files list** (`list_merge_request_changed_files`). Pull diffs (`get_merge_request_diffs`) **only** when the description is thin and you need to infer user-visible behavior — release notes describe *what changed for the user*, not line-level detail. If a diff exceeds ~2000 lines, rely on the file list + MR description.

Resolve the GitLab project path from memory (`reference_gitlab_config.md`) — do not hardcode URLs. If no MRs are found, note that and draft from the ticket context alone.

Produce a one-line **"what actually changed"** takeaway per MR.

### Phase 3 — Determine audience & note type

Pick the note's framing from the ticket type and content. If genuinely ambiguous, ask the user once via `AskUserQuestion`:

- **Audience** — *Customer/end-user* (default), *Operator/admin*, or *Internal/developer*.
- **Type** — `New feature` · `Enhancement` · `Bug fix` · `Security fix` · `Deprecation` · `Breaking change` · `Internal (no customer-facing note)`.

If the change is purely internal (refactor, test, CI), recommend **Internal — no customer note** and confirm before drafting anyway.

### Phase 4 — Draft the release note

Write the note in the [RELEASE-NOTE-FORMAT.md](RELEASE-NOTE-FORMAT.md) structure. Core rules:

- **No icons or emoji.** Plain-text headline and body only.
- **Lead with user value**, not implementation. "You can now…" / "Fixed an issue where…" — not "Refactored the X handler."
- **Plain language.** No ticket jargon, no internal class/module names unless the audience is developers.
- **One note per ticket**, tight: a headline + 1–3 sentences. Add a "Details / Impact" line only when it changes user behavior (action required, defaults changed, migration needed).
- **State the fix version** if known.
- For **bug fixes**, describe the symptom the user saw, not the root cause.
- For **breaking changes / deprecations**, always include an **Action required** line.

### Phase 5 — Quality pass

1. Invoke `/clarity-council` (multi mode) with personas **Technical Writer**, **Product Owner**, and **Customer Advocate**:
   - **user_problem:** "Is this release note accurate, clear, and appropriately scoped for its audience?"
   - **context:** the draft note + Context Summary + per-MR "what changed" takeaways + chosen audience/type.
   - **desired_outcome:** "A release note that a {audience} reads in 10 seconds and understands what changed and whether they must act. Flag any claim not supported by the ticket/MR evidence, and any leaked internal jargon."
   - **depth:** standard.
   - **Technical Writer** owns clarity and scannability; **Product Owner** owns value framing and scope accuracy; **Customer Advocate** owns "does this answer the user's 'what's in it for me / do I need to do anything?'".
2. Incorporate the findings. Then run the note prose through the `/writing-humanize` skill to strip AI-tells (em-dash overuse, rule-of-three, inflated phrasing) so it reads naturally.
3. Present the final note in a fenced ```markdown block, plus a one-line note of the audience/type chosen and any claims that could **not** be evidenced (so the user can verify).

### Phase 6 — Optionally publish back to the ticket

Ask the user via `AskUserQuestion`:

> **Publish this release note to `{TICKET-KEY}`?**
> - **No** *(recommended default)* — end the skill, nothing posted.
> - **Post as a comment** — add it as a Jira comment.
> - **Set Release Notes field** — write it into a Release Notes field (only offer this if such a field exists on the ticket).

**If "No":** end with one sentence — *"Release note kept local. Nothing posted."*

**If "Post as a comment":**
1. Read [jira-comment-template.md](jira-comment-template.md) (sibling file).
2. Render the note in **Jira wiki markup** (headings `h2.`, bold `*text*`, code `{code}`, panels `{panel}`) per the template's mapping — not GitHub markdown.
3. Append the AI disclaimer panel from the template **verbatim**.
4. Post via `jira_add_comment` (`page_id` = ticket key, `body` = rendered note).
5. Confirm with the ticket key.

**If "Set Release Notes field":** only if Phase 1's `jira_get_issue` revealed a Release Notes custom field. Confirm the exact field name with the user, then `jira_update_issue` with that field set to the plain-text note (no disclaimer panel — fields are not comments). If no such field exists, fall back to the comment option.

If a write fails (permissions, network), surface the error and offer to retry or keep the note local — never swallow the failure.

## Constraints

- **Read-only across all systems, with one explicit exception.** The only permitted writes are `jira_add_comment` or `jira_update_issue` (Release Notes field), in Phase 6, after explicit opt-in. Never modify code, MRs, or Confluence.
- Never auto-publish. Phase 6 always goes through the explicit prompt, even if the user opted in during a prior session.
- The disclaimer panel is mandatory whenever a **comment** is posted. Do not edit, soften, or omit it.
- **Do not invent changes.** Every claim in the note must trace to the ticket or an MR. If evidence is thin, say so and draft conservatively rather than embellish.
- No internal jargon, ticket numbers, or class names in customer/operator notes (developer-audience notes may include them).
- **No icons or emoji** in the release note body or headline.
- Do not write files to disk unless the user explicitly asks to save the note.
- If no MRs are found and the ticket context is too thin to describe a user-visible change, stop and tell the user — a release note needs something concrete to describe.

## Quality Loop

Before returning, check the output against these criteria. If two or more fail, revise and re-check — at most two passes, then note what still falls short.

- Note is written for the target audience (customer-facing, not internal jargon)
- Content is grounded in the ticket + linked MR changes, not invented
- Fix version and issue type are reflected correctly
- Read-only respected — nothing posted unless the user opts in

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/issue-draft-release-notes.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
