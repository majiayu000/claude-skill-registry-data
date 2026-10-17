---
name: retention-report
description: Pull our own channel's retention curves and report where viewers drop off or rewatch, with quotes of what was said at each moment. Use when the user asks how their videos are performing, where people leave, what to cut, or wants lessons from their own analytics.
---

# Own-channel retention report

Details live in `channel-analytics/claude.md`.

## Steps
1. **Token:** if `channel-analytics/token.json` is missing or refresh fails, run `python channel-analytics/oauth_setup.py` in the background and ask the user to approve the browser consent (the one step that needs them).
2. **Run:** `python channel-analytics/retention.py` (newest 25), or `--video ID` for one video, or `--limit 50`. Add `--no-quotes` on big runs to save quota.
3. **Read** `channel-analytics/reports/retention_<date>.md` and summarise for the user: the best and worst hooks, recurring drop-off causes (from the quotes), rewatch moments worth reusing as shorts or thumbnails.
4. **Feed lessons forward:** recurring patterns go into the hook-research docs (`long-form-hook-research/`, `shorts-hook-research/`) so new scripts and edits use them.

## Gotchas (keep this list updated)
- Analytics lag about 2 to 3 days, so fresh uploads show "no data yet".
- Livestreams and test streams are filtered out on purpose.
