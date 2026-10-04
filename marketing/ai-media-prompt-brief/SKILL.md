---
name: ai-media-prompt-brief
description: Prepare provider-neutral AI media prompt briefs for creator image, video, audio, voiceover, thumbnail, b-roll, and batch content workflows. Use when Codex is asked to turn a creator concept into AI media prompt packs with creative intent, format, source references, constraints, exclusions, rights/provenance notes, acceptance criteria, and human-review gates without using provider-specific syntax or executing generation.
license: MIT
---

# AI Media Prompt Brief

## Core Workflow

1. Identify creator goal, audience, platform, format, campaign, source assets,
   AI-assisted elements, deadline, review owner, and distribution context.
2. Define provider-neutral prompt briefs for image, video, audio, thumbnail,
   b-roll, or voiceover assets. Keep production operations in
   `creator-production-ops-brief` when scheduling, owners, contractors, or batch
   handoff details dominate. Use `ai-video-prompt-pack` when video generation
   needs platform/model constraints, timing maps, prompt variants, negative
   prompts, or regeneration notes.
3. Include creative intent, format, references, constraints, exclusions, source
   asset needs, acceptance criteria, and review gates.
4. Avoid copying protected styles, living artists, private likenesses, specific
   copyrighted works, distinctive voices, or confidential source assets.
5. Add provenance, consent, rights, AI disclosure, platform-policy, sponsor,
   brand-safety, and authenticity review gates.
6. Separate draft prompts, reviewer notes, missing assets, unresolved rights,
   and approval requirements.
7. Do not generate, publish, schedule, upload, or send assets unless the user
   explicitly asks for that action and the workflow supports it safely.

## Prompt Brief Fields

- Asset purpose
- Audience and platform
- Format, duration, aspect ratio, or placement
- Source assets required
- Visual/audio direction
- Negative constraints
- Accessibility notes
- Rights, consent, provenance, and disclosure checks
- Human review owner

## Safety Rules

- This is production planning support, not legal, copyright, platform-policy,
  or rights clearance.
- Do not claim that AI output is safe, original, licensable, platform-compliant,
  sponsor-approved, or disclosure-complete.
- Do not prompt for living artists, private people, protected characters,
  copyrighted works, voice clones, likeness replicas, logos, or confidential
  source assets without rights and review.
- Do not fabricate provenance, consent, model/tool settings, source assets,
  brand approvals, or audience reactions.
- Verify current official platform or provider rules when tactical generation,
  labeling, commercial-use, or distribution details matter.

## Deliverable Shape

For AI media prompt briefs, provide:

- Asset objective
- Asset and prompt brief table
- Source references and provenance needs
- Constraints and exclusions
- Acceptance criteria
- Review gates
- Rights, disclosure, and platform-policy questions
- Hold/revise/go notes

## References

- Read `references/ai-media-prompt-brief-checklist.md` when preparing
  provider-neutral AI media prompt packs.
