---
name: conversation-memo
description: Archive complete agent conversations and derive structured memo outputs for strategy discussions, architecture debates, execution-direction sessions, or other discussions that should be preserved before turning into formal artifacts. Use when the user wants to save a full discussion, extract the key points into a memo, or identify what formal outputs should come next. Do not use for writing the final formal document itself unless the user explicitly asks for that separate step.
metadata:
  runtime_support_files: true
---

# Conversation Memo

## Overview

Use this skill to preserve a discussion in two stages:

1. save the complete raw conversation first
2. derive a structured memo that can later feed formal documents, index files, or code changes

The memo is not the final formal output. Its job is to preserve context, decisions, and possible next artifacts without collapsing them prematurely into canonical documents.

## Workflow

### 1. Confirm that the discussion is memo-worthy

Use this skill when the conversation is creating direction, framing architecture, clarifying workflow policy, or producing durable reasoning that should not stay only in chat history.

Typical triggers:

- "整理這段討論"
- "做成 memo"
- "保存完整對話"
- "歸納重點"
- "把討論變成後續執行方向"
- strategy / architecture / workflow discussions that are likely to influence later implementation

If the user only wants a final polished document and does not care about preserving the raw discussion chain, another writing or document skill may be a better fit.

### 2. Write the raw archive first

Before summarizing, preserve the full discussion transcript.

Default raw archive root:

- `C:\Users\<user>\.agents\.little_talks`

Unless the user explicitly names a better location, keep using that root for complete raw discussion storage.

Use a stable filename such as:

- `YYYY-MM-DD_<topic-slug>.md`

Requirements for the raw archive:

- keep the complete discussion in chronological order
- do not rewrite or compress the archive before saving it
- if the available transcript is partial, say so explicitly
- treat the raw archive as the evidence source for later memo and formalization work

Read [references/memo-lifecycle.md](references/memo-lifecycle.md) for naming, path, and content expectations.

### 3. Produce the summary memo

After the raw archive exists, create a memo in the appropriate location for the project or workspace.

The memo must always contain a direct path or link back to the raw archive file.

The memo should usually include:

- discussion background
- distilled key points
- decision tendencies or preferred direction
- unresolved questions
- candidate formal outputs

The memo is an intermediate artifact. It should preserve reasoning and next-step clarity without pretending to be canonical policy or final implementation.

Read [references/memo-lifecycle.md](references/memo-lifecycle.md) when you need the memo shape.

### 3.5. Emit a structured handoff when downstream indexing or automation needs it

If the discussion will feed downstream automation such as `obsidian-index-adapter`, emit a structured handoff artifact in addition to the prose memo.

The handoff should capture:

- raw archive path
- summary memo path
- topic or project metadata
- candidate formal outputs

The handoff does not replace the memo. It exists so downstream adapters can consume stable structured inputs without scraping narrative prose.

Read [references/conversation-memo-handoff-schema.md](references/conversation-memo-handoff-schema.md) when you need the canonical schema shape for that handoff artifact.

### 4. Separate memo from formal outputs

Do not treat the memo as the final formal artifact by default.

Formal outputs may take different forms:

- one standalone reference or index document
- several distributed reference or index documents
- direct implementation in code

When the user wants to continue from memo into formalization, make that transition explicit as a separate step.

Read [references/formalization-patterns.md](references/formalization-patterns.md) for the common output shapes.

### 5. Keep Obsidian as a downstream integration unless explicitly activated

Do not write to an Obsidian vault by default.

Until the user explicitly enables Obsidian integration and provides a clear vault target, treat Obsidian as a later indexing or adapter layer rather than the primary memo store.

Read [references/obsidian-boundary.md](references/obsidian-boundary.md) when the user wants Obsidian integration or asks whether Obsidian should replace the memo stack.

## Output Rules

- Preserve the raw discussion before abstracting it.
- Make the memo point back to the raw archive.
- When downstream automation is expected, produce or preserve a structured handoff artifact.
- Keep memo and formal document states distinct.
- If the formal output is not yet created, say that clearly.
- If the discussion implies multiple possible formal outputs, list them instead of forcing one too early.
- If a project already has document-placement policy, follow it for the memo location.
- If no better placement exists yet, keep the memo in an authoring or working-notes layer rather than forcing it into canonical docs.
