---
name: sms-template-review
description: Review Chinese SMS drafts and templates before delivery for language, logic, unresolved variables, recipient fit, factual consistency, links, privacy, safety, compliance, and send readiness. Use when a user provides an SMS text or image, asks whether it can be sent, wants a corrected final version, or needs a template checked against their own source material.
---

# SMS Template Review

Decide whether an SMS is ready to send, needs revision, or must wait for fact verification. Fluent language alone never proves send readiness.

## Read first

Read `references/review-rules.md` before reviewing. It defines the verdict levels and blocking conditions.

## Workflow

1. Preserve the original text, spacing, punctuation, URL, numbers, and variables. For an image, transcribe then visually recheck ambiguous characters; do not guess unreadable text.
2. Determine whether this is a template or a final recipient-facing message. Identify the intended audience, channel, send time, and source of critical facts.
3. Run the mechanical checker without leaking personal text in command history:

   Resolve the installed skill directory first, then invoke the bundled script by its absolute path (do not assume the current project directory contains `scripts/`):

   ```bash
   python3 /absolute/path/to/sms-template-review/scripts/lint_sms.py --stdin
   ```

   Use `--file <path>` when appropriate. Use `--text` only after confirming the body contains no personal or sensitive information. The script redacts unresolved-variable contents, but its output is still diagnostic data: do not paste the original text or private file path into public logs. It is evidence for formatting and placeholders, not proof of business facts.
4. Check sender identity, audience fit, dates, locations, status, action instructions, links, privacy, safety, marketing authorization, and channel restrictions against the user's current authoritative source.
5. Give the verdict first, then blocking problems, fact gaps, a corrected copy-ready draft where safe, and a short final checklist.

## Constraints

- Never repeat or export phone numbers, names, health details, workbook rows, internal links, or secret data from the source material.
- Do not invent a date, venue, status, URL, phone number, refund policy, weather instruction, emergency contact, unsubscribe wording, or legal requirement.
- A final message with unresolved variables is blocked. A template with legal variables can be approved only for library use after field mapping, missing-value policy, and rendered examples are verified.
- If critical facts lack a source, the best possible verdict is `待事实核验`, not `可发送`.
