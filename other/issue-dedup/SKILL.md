---
name: issue-dedup
layer: method
description: Before creating a GitHub issue or epic, search for an existing related one and force a reuse / replace / new decision — so the issue-first flow can't silently mint a duplicate. The create-time half of the dedup gate (the pickup-time half is /issue-sanity-check). Use whenever you're about to open an issue/epic, or run /issue-dedup. Backed by a hard PreToolUse hook on issue_write create.
allowed-tools: mcp__github__search_issues, mcp__github__list_issues, mcp__github__issue_read, mcp__github__issue_write, mcp__github__add_issue_comment, Read, Grep
---

# Issue Dedup — search before you create (HARD GATE)

The repo is **issue-first**: the first action for any initiative is opening the tracking
issue. The trap that creates is **duplicate / colliding issues** — a teammate (or a past
you, in an ephemeral session) already opened the epic, and a fresh agent dutifully opens a
second one. `github-tasks` already *says* "search before creating," but that was a soft,
skippable step. **This skill makes it a gate**, and a PreToolUse hook
(`require-issue-dedup.mjs`) backstops it so a `create` can't land without proof a search ran.

> Scope split: this is the **create-time** gate (don't mint a duplicate). The **pickup-time**
> gate — "should this issue even be done?" — is the sibling **`/issue-sanity-check`** skill.
> Both are sub-issues of epic #297.

## When this fires

Any time you're about to call `mcp__github__issue_write` with `method: create` — a new
epic, sub-issue, or standalone issue. Run the procedure below *first*.

## Procedure

### 1. Extract search terms

Pull 2–5 distinctive keywords from the intended title/body — the *nouns* of the work
(feature name, package/app, the thing being changed). Drop filler ("add", "fix", "the").

### 2. Auto-search open **and** recently-closed work

Stale-but-closed issues matter: the #257/#265 blog case duplicated *closed* epics. Search
both:

```
mcp__github__search_issues  query: "repo:FriendlyInternet/nuxt-crouton <keywords>"
mcp__github__search_issues  query: "repo:FriendlyInternet/nuxt-crouton in:title <keyword>"
mcp__github__list_issues    labels: ["epic"]      # scan epic titles for overlap
```

Run a couple of phrasings — exact-title and broad-body — and include `state:closed` in at
least one. **Keep results in-context:** these calls overflow easily (a bare `list_issues
labels:["epic"]` came back at ~140k chars), so pass **`minimal_output: true`**, a small
**`perPage` (5–10)**, and prefer **`in:title`** filters — only widen if a narrow query misses.
If output still overflows, narrow further rather than slicing the blob out-of-band.

### 3. Surface the matches to the human (number · state · why-similar)

Present a short table of candidates — **never** silently proceed:

| # | State | Title | Why it might be the same |
|---|-------|-------|--------------------------|
| #297 | open | Stale-epic dedup… | same feature — the dedup gate |
| #265 | closed (completed) | POC pipeline preview URL | adjacent, not the same |

If a candidate's closing comment cites artifacts (writeups, PRs) that **don't exist** in the
repo, flag it — that's the #297 smell (a stale close hiding undone work).

### 4. Force a **reuse / replace / new** decision — this is the hard stop

Do not create until one is chosen:

- **Reuse** — a match already covers this. **Stop. Don't create.** Continue *that* issue
  (assign yourself, `status:in-progress`). This is the whole point of the gate.
- **Replace** — a stale/closed issue should be superseded. Link it in the new body
  (`Supersedes #NN`) and, if it's open, close it `not_planned` referencing the replacement.
- **New** — genuinely nothing matches (or matches are only adjacent). Proceed to create.

**How to ask** (the on-match signal):
- **Interactive session** → ask in chat with `AskUserQuestion` (reuse / replace / new) and
  wait. This is the cheapest stop.
- **Autonomous / pipeline** (no human in the loop to block on) → you may create the issue,
  but **immediately post a reply comment** on it naming the suspected duplicate(s) and asking
  the owner to confirm reuse / replace / keep — assigned to them so it surfaces. A created
  issue with an unresolved dup question is honest; a silent duplicate is not.

### 5. Record the dedup result in the body (REQUIRED — the hook checks for it)

Every created issue body MUST end with a one-line **dedup attestation** — it's both the
audit trail and the token the backstop hook greps for. Format:

```
_Dedup-checked: searched «keyword, keyword» → no match_
```
or, when something related turned up:
```
_Dedup-checked: searched «dedup, issue» → related #297 (open), #800 (open); new because this is the create-time half_
```

The literal prefix `Dedup-checked:` is what the hook requires. Omit it and
`require-issue-dedup.mjs` blocks the `create` with a reminder to run this skill.

## The backstop hook

`.claude/hooks/require-issue-dedup.mjs` is a PreToolUse gate on `mcp__github__issue_write`:

- Only gates `method: create` — `update` and everything else pass untouched.
- Blocks (exit 2) when the `body` lacks a `Dedup-checked:` line.
- Mirrors `require-comment-provenance.mjs` exactly (body-content check, no state).

It's a *backstop*, not the brain — it can't tell whether you really searched, only that you
attested. Do the real search (steps 1–4); the marker is your signed receipt.

## What this is not

- Not the pickup gate — that's `/issue-sanity-check` (#800).
- Not a substitute for judgement — "related" ≠ "duplicate". Adjacent issues coexist; only a
  genuine same-scope overlap is a reuse/replace.
