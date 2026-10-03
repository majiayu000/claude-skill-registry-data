---
name: prompt-leakage
description: >
  Remove conversation dependencies from issues, PR descriptions, handoffs,
  comments, READMEs, and commit bodies. Use when drafting these artifacts,
  reviewing your own diff, the user says slop / leakage / prompt leakage, or
  before push. Always-on for any comment you are about to add.
---

# Prompt leakage

**Transcript residue** is content that serves the originating conversation
rather than the intended reader. It includes conversational justification and
artifacts that require access to a chat to understand the problem or action.
Apply this to drafts in chat as well as files: an issue draft is already a
handoff artifact.

Different from ceremonial *code* (yagni-anti-ceremonial) and generic extra
comments (deslop).

## Comments and incidental asides

Delete the line if any of these is true:

1. **Chat-motive** — names a user request, slash command, or "so Codex gets X".
2. **Restatement** — the next line's identifiers already say it.
3. **Theater** — parenthetical written to justify the change to the previous turn.

Keep it only if a stranger cannot recover the fact from names, types, or the
next line.

## Delete these

Chat-motive:

```sh
# Added because the reviewer asked for a defensive fallback.
run_with_fallback
```

The comment records the conversation, not a runtime fact.

Theater:

```md
- Retry through the legacy path. (This satisfies the original request.)
```

Restatement:

```sh
# Increment the retry count.
retry_count=$((retry_count + 1))
```

## Keep these

```md
The folder is named `agent-skills` because a global gitignore drops any `agents/` directory.
```

```sh
# fee_limit caps Energy burn. It is not ETH gas and does not pay bandwidth.
```

A stranger cannot get those facts from the identifiers alone.

## Do not

- Narrate ("now we link Codex so the two skills resolve").
- Paste the last message's acceptance criterion into a comment.
- Treat a comment you just wrote as documentation when you review your own diff.

## Issues, PR descriptions, and handoffs

Write for the destination audience, not the people in the source conversation.
State the problem, observed behavior, requested outcome, and material evidence
limits directly. Preserve necessary rationale; remove who asked for the work
unless that attribution establishes relevant ownership or policy authority.

Before retaining a source link, check both its purpose and its audience:

- Keep links that support a claim, establish authority, or let readers inspect
  relevant evidence. A link is not useful merely because it was used in research.
- Do not assume destination readers can open a private chat, group, local file,
  or authenticated service because the researcher can. When access is unknown,
  omit private conversation links from ordinary issue/PR drafts and include the
  necessary, authorized facts directly. Do not ask about access when omission
  leaves the artifact complete.
- If the user explicitly requests provenance, retain appropriate references and
  state access limits. Never invent a public replacement or disclose private
  material beyond the authorized audience.
- The essential problem and requested action must remain understandable with
  links unopened. Supporting evidence may remain linked; do not paste an entire
  transcript or strip uncertainty to make an artifact appear self-contained.

For example, replace “Increase the limit as discussed in the group” with the
observed limit and proposed outcome. If the new limit is only a suggestion,
label it as a proposal rather than an approved requirement.

## Final artifact check

Read only the artifact, without the conversation. Can its intended reader tell
what is true, what remains uncertain, and what action is requested? Check links,
attribution, and headings as well as prose; conversational phrasing is only one
form of leakage.

Remove `chat-motive`, `restatement`, and `theater`. Repair `conversation-dependency`
by retaining the necessary fact or rationale in concise standalone language.
Do not delete useful evidence just because it originated in a conversation.
Run this check on the final draft after revisions, not just the initial wording.
