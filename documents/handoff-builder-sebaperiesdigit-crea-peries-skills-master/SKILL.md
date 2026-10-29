---
name: handoff-builder
description: "Use when the user asks to hand off, transfer, or continue this chat/project elsewhere — a new Codex chat, a different Codex project, or a separate AI tool like ChatGPT or Codex — or runs /handoff."
---

# Handoff Builder

Generates a markdown handoff document that lets work continue in a new destination — another Codex chat, another Codex project, or a different AI tool (ChatGPT, Codex, etc.) — with minimal loss of context. Triggers on `/handoff` and on natural-language requests like "hand this off", "prep this for a new chat", "create a handoff doc", "continue this in a new project".

This skill is written to work the same way on any AI platform — see Step 6 for how delivery adapts to whatever's actually available, rather than assuming a specific file/doc API.

## Known limitation — state this up front

This skill can only read what's actually accessible to it: the current conversation, plus any files or docs this platform lets it read. It cannot see other conversations that were never shared or written into something readable here. A full-project handoff is therefore only as complete as whatever's actually visible — if progress/status docs aren't being kept current (by `task-progress-tracker`, `progress-status`, manual notes, or anything else), other conversations' work will be invisible to this skill. Say this plainly if the visible material looks thin or old relative to what the user describes.

## Step 1: Ask destination + scope in one prompt

Always ask — via `AskUserQuestion` where that tool is available, otherwise a plain numbered list with a free-text fallback — never guess silently:

**Destination** (pick one):
1. Same project, new Codex chat
2. A different/new Codex project
3. A new chat for ChatGPT, Codex, or another AI tool ("cross-tool")

**Scope** (pick one):
1. This chat — the current conversation plus anything it referenced or touched
2. Everything visible — sourced from whatever project docs, files, or prior tracking material this platform can actually show it

If the user already stated destination/scope in their invocation (e.g. "/handoff to codex", "handoff the whole project"), skip asking for that part and only ask what's missing.

## Step 2: Gather the source content

Depending on scope:

- **This chat**: summarize the current conversation directly — decisions made, code/files changed, open questions, next steps. Also pull in any docs or files this chat explicitly referenced or touched.
- **Everything visible**: gather whatever progress or status information is already available — a doc discussed earlier, a file this platform can read, notes pasted into this conversation. Don't assume a particular skill or tool produced it; just use what's actually there. If nothing beyond the current chat is accessible, fall back to summarizing just the current chat and say so.

## Step 3: Draft the handoff using one shared template

Use the same structure for every destination (see Template below). Do not fork the template per destination.

## Step 4: Verify before finalizing

Run all three checks, in order:

1. **Internal consistency** — check the draft itself: no empty/placeholder sections, no contradictions between sections (e.g. "status: done" next to an open blocker for the same item).
2. **Reconcile against other visible material (staleness check)** — there's no reliable "last updated" signal to lean on, so instead diff what the current chat/draft claims is done or in-progress against whatever other visible docs/notes say. Flag any contradiction or gap explicitly in the draft as "⚠️ possibly stale — chat says X, other notes say Y" rather than silently picking one.
3. **User confirmation** — before finalizing, show the user a short summary of what's about to be included (key facts, decisions, open items, any staleness flags from step 2) and ask them to confirm or correct it. Only proceed to Step 6 after confirmation.

## Step 5: Cross-tool adjustments (destination = ChatGPT/Codex/other)

Only for the cross-tool destination, apply both:

- **Glossary section**: append a short "Terms used in this doc" section translating Codex-specific concepts referenced in the handoff (e.g. "project" = a shared workspace of related chats/docs; "skill" = a reusable Codex procedure) so the doc reads correctly with zero Codex context. Do not otherwise rewrite the template — same structure as any other destination.
- **Secret scan**: before finalizing, scan the draft for obvious secrets — API keys, tokens, passwords, connection strings, credential-looking values, and any personal data (emails, phone numbers) pulled in from the chat/docs. Redact anything found (replace with `[REDACTED]`) and list what was redacted at the top of the doc so the user can double check. If something looks sensitive but ambiguous, ask the user rather than guessing.

For same-tool Codex destinations (same project or new project), skip the glossary and secret scan.

## Step 6: Deliver the output

There's no platform-specific "project doc API" or "file card" this skill assumes exists. Instead:

1. **Always print the full handoff document directly in the reply**, as plain markdown. This is the one delivery method guaranteed to work on every platform, and it's what the user copies/pastes into the new destination regardless of what that destination is.
2. **If a file-write tool actually exists in this session**, additionally save the handoff to a local file named `handoff-<YYYY-MM-DD>.md` (don't overwrite a prior day's handoff — dated files preserve history) and tell the user where it was saved.
3. If the destination is "a different/new Codex project" (or any separate workspace/tool), note plainly in the reply that content doesn't move automatically between separate conversations, projects, or tools — the user needs to paste or upload the delivered content into the new destination themselves.

## Template

```markdown
# Handoff: <short title>

**Generated:** <date>
**From:** <this chat/project name if known>
**Destination:** <same-project chat / new project / cross-tool>
**Scope:** <this chat / everything visible>

## Summary
<2-4 sentence plain-language summary of what this work is and where it stands>

## What's done
<bulleted-in-prose or short list of completed items>

## In progress / current state
<what's actively being worked on right now, with enough detail to resume>

## Open questions / decisions needed
<anything unresolved that the next chat/tool needs to address>

## Key facts & context
<file paths, names, IDs, constraints, prior decisions and why they were made — enough for a cold start>

## Next steps
<concrete next actions, in order>

## ⚠️ Flags
<any staleness contradictions from Step 4, or redacted-secret notices from Step 5 — omit this section if empty>

<!-- Cross-tool destinations only, appended: -->
## Terms used in this doc
<glossary of Codex-specific terms used above>
```

## Notes / Guardrails

- This skill is intentionally self-contained: it doesn't call or require `task-progress-tracker` or `progress-status` to have run. If their output happens to be visible in the conversation or in a readable file, that's just one possible source of material for Step 2 — not a dependency.
- Never invent progress, decisions, or facts that aren't actually visible somewhere accessible to this skill — an incomplete handoff that says so honestly is far more useful than a confident one that guesses.
