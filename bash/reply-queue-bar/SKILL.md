---
name: reply-queue-bar
description: A menu-bar reply queue for capturing copied comments or inbox snippets, sorting what deserves a response, and handing the next reply draft forward without reopening every tab.
---

# Reply Queue Bar

Use this skill when the user wants a local, Mac-first reply triage lane for copied comments, inbox snippets, or feedback fragments without pretending to be a full inbox client.

Default product shapes:
- a menu-bar popover that keeps the next reply, draft, and archive action one click away
- a deterministic local helper that stores reply items in a small JSON queue and renders a brief for prompts, notes, or clipboard handoff

## Quick Start

1. Confirm whether the user needs a one-off reply queue snapshot, a local helper workflow, or a real menu-bar utility shell.
2. Use `python skills/reply-queue-bar/scripts/reply_queue_bar.py capture --clipboard --source "X comment" --bucket urgent --urgency high --tag launch` to save the current copied snippet into the local queue.
3. Use `python skills/reply-queue-bar/scripts/reply_queue_bar.py brief --format prompt` when the next step is deciding which reply deserves attention now.
4. Use `python skills/reply-queue-bar/scripts/reply_queue_bar.py draft --id <item-id> --text "..." --copy-draft` when the answer is ready to paste back into the destination app.
5. Use `python skills/reply-queue-bar/scripts/reply_queue_bar.py archive --id <item-id> --move-to-archive-bucket` after the response is handled.
6. Use the SwiftUI starter in `prototype/` when the user wants a real menu-bar shell instead of only the local queue helper.

## Accepted Inputs

- copied comments, DMs, support replies, feedback snippets, or short email fragments
- a source label such as `Telegram`, `X`, `Gmail`, `Linear`, or `Support inbox`
- a queue bucket: `urgent`, `reusable`, or `archive`
- urgency level, tags, and an optional draft
- whether the output should print, render as markdown or prompt text, or copy back to the clipboard
- whether the user wants a one-off summary or a reusable macOS utility concept

## Workflow

### Keep the queue local and deterministic

- Store the queue in a local JSON file instead of inventing a cloud inbox, analytics pipeline, or unsupported background listener.
- Capture from explicit text, a file, stdin, or `pbpaste`; do not imply live inbox access when the source app has not been connected.
- Treat the queue as a handoff tool for the next response, not a full CRM or comment dashboard.

### Lead with the next reply that matters

- Show urgent and reusable items before archive material.
- Keep the source, bucket, urgency, and current draft visible without forcing the user back through tabs.
- Prefer one short draft that is ready to copy out over a long thread-management surface.

### Keep the Mac utility shape narrow

- Prefer a menu-bar popover or compact panel over a large multi-window app.
- Use one primary reply action and a few supporting actions like capture, copy draft, and archive.
- If the queue grows, make the summary scannable first and push deeper detail into a secondary view.

## Local Helper

Use `scripts/reply_queue_bar.py` when a deterministic local queue is useful:

```bash
python skills/reply-queue-bar/scripts/reply_queue_bar.py capture --clipboard --source "Telegram DM" --bucket urgent --urgency high --tag support
python skills/reply-queue-bar/scripts/reply_queue_bar.py capture --text "Can you pin the latest meeting note link?" --source "X reply" --bucket reusable --tag faq
python skills/reply-queue-bar/scripts/reply_queue_bar.py brief --format prompt
python skills/reply-queue-bar/scripts/reply_queue_bar.py list --format markdown --limit 8
python skills/reply-queue-bar/scripts/reply_queue_bar.py draft --id rqb-20260413-000001 --text "Pinned in the latest update thread. I’ll keep the note linked there." --copy-draft
python skills/reply-queue-bar/scripts/reply_queue_bar.py archive --id rqb-20260413-000001 --move-to-archive-bucket
```

The helper keeps a local queue at `~/.codex/reply-queue-bar/queue.json` by default, ranks urgent and reusable items ahead of archive material, supports `plain`, `markdown`, `prompt`, or `json` output, and can copy a rendered brief or saved draft with `pbcopy`.

## Prototype

- SwiftUI starter files live in `prototype/`.
- The prototype sketches a menu-bar shell with queue counts, bucket switching, the current reply card, and a draft handoff area.

## Example Prompts

- `Use $reply-queue-bar to design a compact macOS menu-bar utility that turns copied comments into an urgent-versus-reusable reply lane with one ready draft.`
- `Use $reply-queue-bar to keep the workflow local: capture from clipboard, rank the queue, and copy the next draft without inventing inbox APIs.`
- `Use $reply-queue-bar to create a menu-bar shell for community replies with explicit capture, copy, and archive actions instead of a full social dashboard.`

## Resources

- `scripts/reply_queue_bar.py`: local queue helper for capture, summary, drafting, and archive actions
- `prototype/`: menu-bar-first SwiftUI starter for the reply triage surface

## When extending

- Add more depth only when it improves the short reply handoff loop.
- If the skill grows, keep the queue summary and next reply readable at a glance.
