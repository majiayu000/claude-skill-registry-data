---
name: screenpipe-meeting-follow-up
description: "Capture decisions and commitments after a meeting and draft a concise follow-up."
---

# meeting follow up

Identify the exact meeting and inspect its note or bounded transcript using screenpipe-api. Keep stated intent, agreed work, and completed work separate.

Never infer who spoke from the wording of a transcript. Speaker separation is an audio problem, not a text one, and guessing it is how commitments get assigned to the wrong person. Get attribution from the deterministic layer instead: `python ~/.claude/scripts/_shared/speaker_truth.py --timeline --hours N` (add `--jsonl` for machine use, `--llm-contract` for what you may and may not change). Lines it marks at confidence 1.00 come from the recording device and are not yours to reassign; `ГОСТЬ-<id>` may be given a name from context; `ГОСТЬ-?` stays unknown. A desk microphone hears the whole room, so on one it proves whose machine is recording, not whose voice it is.

Write the outcome, decisions, owners, due dates explicitly mentioned, and open questions. Do not invent owners or dates. Include a source link and flag gaps in recording.
Draft a short follow-up when requested. Check the user’s current casing and punctuation preferences. Sending, updating external systems, or creating calendar events requires the user’s explicit request.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
