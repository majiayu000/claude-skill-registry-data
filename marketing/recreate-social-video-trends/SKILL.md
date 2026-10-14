---
name: recreate-social-video-trends
description: Research relevant short-form videos for a brand or its competitors, analyze an Instagram or Facebook reference video, and recreate its editing language as an original, reusable Remotion template. Use for social-video trend research, competitor video discovery, lyric videos with supplied lyrics or timing data, transition breakdowns, reference-video imitation, editable clip-replacement templates, and export-ready Remotion compositions.
---

# Recreate Social Video Trends

Turn a trend or reference into an editable Remotion system, not a one-off hard-coded clone.

## Establish the brief

Collect or infer:

- brand, product, audience, platform, competitors, region, and campaign goal;
- reference URL or local video, target aspect ratio, duration, and frame rate;
- user-owned clips, music, lyrics, logos, fonts, colors, and export requirements;
- the supplied lyric and timing format, including its units and cue boundaries. Do not guess an undocumented format.

Ask only for information that materially changes the result. Never request credentials in chat.

When the task includes message strategy, content planning, or script development, read [references/content-and-script-frameworks.md](references/content-and-script-frameworks.md). Use the minimum framework that improves the decision, distinguish research-grounded models from practitioner heuristics, and state unverified audience assumptions as hypotheses.

## Research relevant videos

When asked to find trends or competitor examples, use an available browser/search connector to inspect public, accessible sources. Prefer recent posts from the brand, named competitors, adjacent category leaders, and platform trend pages. Record the URL, account, post date when visible, hook, duration, shot rhythm, text treatment, transitions, audio pattern, engagement signals, and why it fits the brief.

Do not bypass logins, paywalls, bot protection, or platform download restrictions. If the link cannot be accessed, ask for an uploaded or otherwise authorized local copy. Treat engagement counts as directional and timestamp the observation.

Shortlist three to five patterns by relevance and repeatability. Score whether each pattern serves the audience's job, positioning, content role, and desired response—not only its visual novelty. Separate observations from inferences. Do not claim that a trend is current without live evidence.

## Analyze the reference

Read [references/analysis-and-rights.md](references/analysis-and-rights.md) before analyzing a linked or uploaded reference. Produce a beat sheet with timecodes for hook, shots, lyric or caption changes, motion, transitions, effects, audio cues, and outro. Describe the underlying technique rather than copying protected assets or distinctive branding.

When writing or revising the script, name the chosen narrative structure and why it fits the audience need and available proof. Hooks must earn attention by delivering the promised value; do not withhold essential context, fabricate social proof, or reproduce false scarcity, shame, fear, or other manipulative elements from the reference.

For lyric videos, preserve the supplied lyric text exactly unless asked to edit it. Convert the supplied timing source into deterministic cue data. If timings are absent, derive provisional cues from the authorized audio and label them for review.

## Build the Remotion template

Use installed Remotion skills when available, especially `remotion-create`, `remotion-markup`, `remotion-multimedia`, `remotion-captions`, `remotion-best-practices`, and `remotion-render`. Read their instructions before relying on them.

Read [references/template-contract.md](references/template-contract.md), then:

1. Implement the reference's pacing and transition grammar with original code and user-authorized assets.
2. Drive animation from `useCurrentFrame()` and `useVideoConfig()`; keep rendering deterministic.
3. Expose clips, crop/focal position, text or lyrics, colors, fonts, audio, transition style, timing, and output format through a typed props schema.
4. Keep transition duration bounded by adjacent scenes. Prefer purposeful combinations of masks, wipes, match cuts, parallax, blur, light sweeps, displacement-like layers, and typography motion over random effect stacking.
5. Preserve safe areas and legibility for the target platform. Provide sensible fallbacks for missing optional assets.
6. Add or update a registered composition and include example props that can be replaced without editing component internals.

## Verify and hand off

- Run typecheck, lint, and relevant tests available in the project.
- Inspect representative frames at the hook, every transition boundary, dense lyric sections, and the outro.
- Preview the composition. Render only when the user explicitly asks for an export.
- Report the composition ID, dimensions, FPS, duration, editable props, asset locations, preview command, and export command.
- Identify any approximation caused by unavailable source media, fonts, plugins, or unclear timing.
- When strategy is in scope, report the audience and positioning hypothesis, content-system role, script structure, evidence used, ethical guardrail, and measurement plan.

Do not upload, publish, or post the result unless the user explicitly asks and authorizes that external action.

## Creator

Created for and maintained by [Brownsmith Dynamics](https://brownsmithdynamics.com).
