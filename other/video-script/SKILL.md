---
name: video-script
description: Draft a scene-by-scene video script with timing, visual direction, narration, and source attribution from upstream creator-media artifacts
type: planning
version: v0.2
required_conventions: [alignment-page]
argument-hint: "<topic or slug> [--type launch|explainer|demo|testimonial] [--duration short|medium|long] [--series <series-slug>]"
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Video Script

Invoke as `$video-script`.

Read upstream research and spec artifacts, interview on video goal and audience, then produce a scene-by-scene script with narration text, visual direction, timing, and source attribution.

## Prerequisites

At least one of these artifacts must exist:

- `research/youtube/product-led-media-map-<slug>.md`
- `specs/youtube/series-<slug>.md`
- `research/youtube/creator-positioning-<slug>.md`

Enhancement tiers based on available artifacts:

- **Tier 1:** Creator positioning only — voice but thin proof.
- **Tier 2:** + product-led-media-map — product-grounded claims.
- **Tier 3:** + series-spec — format-consistent episode.
- **Tier 4:** + journey-map + gtm — full-funnel narrative with aha moments and GTM messaging.

## Inputs

- `research/youtube/product-led-media-map-<slug>.md`
- `specs/youtube/series-<slug>.md`
- `research/youtube/creator-positioning-<slug>.md`
- `research/youtube/content-programming-<slug>.md`
- `research/journey-map.md` (or `research/{app}/journey-map.md`)
- `research/gtm.md` (or `research/{app}/gtm.md`)

## Process

0. Resolve arguments: topic/slug, video type (`launch`, `explainer`, `demo`, `testimonial`), duration (`short`, `medium`, `long`), optional series slug.
1. Load all available upstream artifacts. Determine enhancement tier.
2. Text-based checkpoint: confirm video goal, target audience, narrative approach, tone, production constraints with the user before proceeding.
3. Draft narrative arc using the type-specific template. Present for approval before proceeding.
4. Write scene-by-scene script: narration text, visual direction, on-screen text, music cues, timing, source attribution.
5. Text-based checkpoint: present complete script with duration estimate, asset requirements, and ungrounded claims. Validate with user.
6. Write output only after user confirmation.

### Narrative Arc Templates

- **Launch:** Hook → Context → Reveal → Proof/Demo → Transformation (aha moment) → CTA → Outro
- **Explainer:** Hook → Problem → Concept → Application → Summary → CTA → Outro
- **Demo:** End result first → Setup → Walkthrough → Result → CTA → Outro
- **Testimonial:** Strongest quote → Problem framing → Discovery → Experience → Results → CTA → Outro

## Output

Create the `specs/youtube/` directory if it does not exist.

Write `specs/youtube/video-script-<slug>.md` with:

- **Video Brief:** type, audience, goal, duration target, series context, enhancement tier.
- **Narrative Arc:** high-level structure with per-section timing.
- **Scene Breakdown:** per scene — narration text, visual direction, on-screen text/graphics, music/mood, duration, source attribution via `<!-- Source: path — claim -->` comments.
- **CTA Strategy:** primary CTA, placement timing, end-screen plan.
- **Asset Requirements:** footage, screen recordings, graphics, music, b-roll — checklist with status.
- **Source Attribution Summary:** table mapping claim → upstream artifact → section.
- **Ungrounded Claims:** claims without research backing, marked `<!-- UNGROUNDED -->`.
- **Next Steps.**

Write `specs/youtube/video-script-<slug>-interview.md` with the interview log.

## Approved Artifact Handoff

After an approved synthesized write, explicit write/update mode, or any direct artifact mutation:

- List every created or updated synthesized artifact path in the final response.
- State the verification performed, such as readback, schema/check command, or why no executable verification applies for a Markdown-only strategy artifact.
- Check and report the relevant git status for intended artifacts when the project is a git repository. If intended artifacts are modified or untracked, make the next action shipping, committing, or an explicit dirty-artifact handoff before recommending downstream strategy work.
- Do not imply the research workflow is complete while approved artifacts remain untracked or uncommitted unless the user explicitly asked not to ship.
- If stopping for approval before writing, the approval request remains the next action; do not include downstream routing.

## Intent-Aware Routing

Before applying the default `## Next-Skill Routing` sequence, classify the user's immediate intent and route to the missing action that best serves that intent:

- Strategy refresh: recommend the missing or stale positioning, programming, portfolio, metrics, or product-media artifact.
- Recording prep: recommend the missing series spec, script, build proof, walkthrough guide, or validation artifact needed before recording.
- Upload prep: recommend packaging, title/thumbnail, description, chapters, or final metadata work before broader strategy work.
- Performance review: recommend metrics, cadence, portfolio, peer benchmark, or owner-analytics export work before new content planning.
- Owner analytics or private/manual platform evidence: route to an explicit manual/guide handoff instead of inventing unavailable metrics.
- Dirty intended artifacts: route to shipping/commit/handoff first, not another creator strategy skill.

Use the default next-skill sequence only when no stronger user intent, missing artifact, manual blocker, or dirty-artifact handoff applies.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/video-script-{topic}.html`.

## Constraints

- Source-attribute every factual claim with inline `<!-- Source: path — claim -->` comments.
- Mark ungrounded claims with `<!-- UNGROUNDED -->`.
- Respect series format when `--series` is provided.
- Respect anti-positioning from creator-positioning.
- Present the script before writing — never write until the user confirms.
- Do not prescribe thumbnail design or editing cuts.
- Do not expose secrets, private customer data, or unreleased commitments.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

