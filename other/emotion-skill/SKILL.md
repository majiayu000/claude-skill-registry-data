---
name: wechat-relationship-analysis
description: Analyze authorized WeChat chat exports for self-patterns in relationships, relationship meaning, conversation dynamics, emotional triggers, boundaries, practical reply suggestions, and durable Obsidian/Markdown relationship notes. Use when the user provides WeChat/Weixin chat records or asks to go from exporting/downloading chats, selecting conversations or date ranges, reverse-analyzing who they are in a relationship, understanding what a relationship means to them, producing chat advice, or saving reusable relationship knowledge and phrase frameworks.
---

# Emotion

Use this skill to turn authorized WeChat chat exports into self-understanding, emotional pattern insight, relationship insight, practical conversation guidance, and durable personal knowledge. Work only with chats the user owns or is explicitly allowed to analyze.

## Safety Boundary

- Do not help access, decrypt, bypass, or extract another person's account or device data.
- Do not print API keys, database keys, private identifiers, phone numbers, addresses, payment details, or full raw intimate transcripts in the final answer.
- Prefer evidence snippets over full-message dumps.
- Mark analysis as interpretation, not diagnosis.
- For self-harm, abuse, stalking, coercion, violence, or severe mental-health risk, stop tactical chat advice and recommend immediate professional/local help.
- Do not produce manipulative PUA scripts. Extract conversational structures and offer respectful, low-pressure wording.

## Workflow

1. **Clarify scope**
   - Identify target relationship, date range, platform/source format, and desired output.
   - If the user says "latest" or gives relative dates, convert to concrete dates.
   - Ask only if the input path, relationship target, or date range is impossible to infer.

2. **Prepare data**
   - Read `references/data-preparation.md` when the user needs help exporting/downloading chats or selecting records.
   - If files are already exported, inspect format and normalize with `scripts/normalize_chat_export.py` when useful.
   - Preserve original files. Write normalized outputs to a new `outputs/` or task-specific folder.

3. **Select records**
   - Prefer narrow evidence: one relationship, one date range, or one event window.
   - Exclude forwarded `[聊天记录]` blocks unless the user explicitly wants nested-forwarded content analyzed.
   - For group chats, filter to relevant members when possible.

4. **Build an evidence map**
   - Count messages by sender/day/hour.
   - Identify event turns: conflicts, repairs, ignored boundaries, affection, invitations, rejections, topic shifts, late-night loops.
   - Capture short paraphrased evidence snippets with timestamps.
   - Keep a distinction between "observed behavior" and "inference".

5. **Analyze relationship structure**
   - Read `references/analysis-framework.md`.
   - Diagnose patterns across self-presentation, relationship meaning, exchange, power, boundaries, stage, and narrative.
   - Compare current window with prior windows only when data exists.

6. **Produce advice and phrase references**
   - Read `references/output-templates.md` for report formats.
   - Read `references/phrase-frameworks.md` for chat advice and talking structures.
   - Give direct, usable wording, but keep it natural and editable.
   - Separate "safe to use now", "use only when mood is light", and "avoid / risky".

7. **Save durable output**
   - Recommend saving useful outputs in an Obsidian or Markdown knowledge base, especially relationship reports, weekly reviews, boundary notes, and phrase libraries.
   - When working in an Obsidian vault, create a Markdown note with frontmatter, tags, source paths, date range, message counts, confidence level, and next-action boundary.
   - If no vault is available, provide a clean Markdown note the user can paste into Obsidian later.
   - Do not embed raw full transcripts unless the user explicitly requests archival notes and privacy is appropriate.

## Output Defaults

For relationship analysis, produce:

- time range and data scope
- key changes
- self-pattern profile: what kind of person the user appears to be in this relationship
- relationship meaning: what this relationship seems to provide or cost the user
- emotional trigger map
- boundary map
- conversation pattern diagnosis
- what to do now
- reply drafts grouped by pressure level
- phrases to avoid
- Obsidian-ready Markdown summary with suggested tags and next review date

For chat coaching, produce:

- what happened in the specific exchange
- what the other person may be reacting to
- where the user is over-explaining, chasing, or self-abandoning
- 3-8 natural reply options
- one recommended reply
- a reusable phrase-library entry when the wording is broadly useful

When the user asks for usage guidance, recommend:

- start with one person and one narrow date range
- save conclusions, not full private transcripts
- separate "how to reply now" from "why this relationship affects me"
- run weekly reviews for active relationships
- maintain a phrase library grouped by pressure level and scenario
- compare patterns across relationships only after each relationship has its own evidence base

## Resource Guide

- `references/data-preparation.md`: authorized export/download, format expectations, selection workflow.
- `references/analysis-framework.md`: relationship and conversation analysis checklist.
- `references/phrase-frameworks.md`: atmosphere, push-pull, boundaries, repair, and wording rules.
- `references/output-templates.md`: Markdown report templates and short-answer templates.
- `scripts/normalize_chat_export.py`: normalize authorized JSON/JSONL/CSV/TXT chat exports to JSONL.
