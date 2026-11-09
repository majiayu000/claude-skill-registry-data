---
name: yt-repurpose
description: Choose between a new opening, a visual restyle, or a themed mashup of existing social videos using analytics and visual evidence. Produces an edit brief, not rendered media.
---

Read the ranking and frame reports when available. Consider **new opening only first**,
especially if the user reports a drop around 0:02. Treat that as supplied evidence, not a
fact about every profile. Keep the rest of the clip fixed for that experiment.

Use `select.py evidence.json` for a baseline recommendation. Evidence keys:
`opening_drop_seconds`, `opening_untested`, `clear_subject`, `restyle_motion_suitable`,
`shared_theme`, `new_narrative_payoff`, `old_footage_fraction` (0..1),
`substantial_new_material` (boolean). Missing evidence stays unknown.
Assess the frames alongside narration: narration does not establish what is visible.

For mashups estimate reused screen time and explain what new story, commentary, or scenes
add value. Warn when mostly old footage has little new substance. The helper's 70% flag is
an editorial heuristic, not an official threshold. Do not promise rewards eligibility or
assert an automatic reach penalty. Check current platform rules if eligibility is relevant:
[TikTok](https://support.tiktok.com/en/business-and-creator/creator-rewards-program/creator-rewards-program)
and [YouTube](https://support.google.com/youtube/answer/1311392).

Return the treatment, supporting evidence, uncertainties, proposed opening/payoff, estimated
credits (only if known), and one changed variable. Log it with yt-experiments. Rendering,
paid generation, and posting require the corresponding user request and available tools.
