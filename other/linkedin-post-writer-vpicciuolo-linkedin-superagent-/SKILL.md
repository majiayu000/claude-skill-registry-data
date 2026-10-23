---
name: linkedin-post-writer
description: Draft, revise, or review a LinkedIn feed post in the user's voice. Use for text posts, post ideas, launch posts, founder updates, educational posts, opinions, stories, offers, or a pasted draft that needs improvement.
license: MIT
metadata:
  version: "2.2.0"
  copyright: "VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD"
---

# LinkedIn post writer

Read `../../references/session-and-safety.md` and
`../../references/content-system.md`. Use the approved voice profile and
strategy when present.

Before drafting, obtain one concrete idea, intended reader, goal, and proof.
If any required fact is missing, ask one compact question or use an explicit
`{{NEEDS INPUT}}` marker.

Workflow:

1. Write a one-sentence brief.
2. Use `linkedin-hook-lab` or `../../references/hook-library.md` to develop
   three openings with different promises.
3. Choose one and draft a post that fully pays it off.
4. Keep one main idea. Use specific examples, honest caveats, and a natural
   ending. Add a CTA only when it helps the stated goal.
5. Apply Humanizer as an editorial check, preserving facts and voice.
6. Run the local linter when available:
   `python <plugin-root>/scripts/oyyo_linkedin.py lint <draft-file>`.

Return the recommended hook, the final copy-ready post, and a receipt with
goal, character count, unresolved facts, and one optional alternate ending.
Never publish or log the post without the user's explicit request.
