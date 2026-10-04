---
name: content-ops
description: >-
  Auto-assembles a domain-specific expert panel (7–10 experts), scores any
  content or strategy artifact against a typed rubric, and iterates until the
  aggregate hits 90+ (max 3 rounds). Use as a quality gate on copy, email
  sequences, landing-page drafts, strategy docs, charts, titles, or recruiting
  evaluations — or when another skill needs a final review gate on its output.
  Triggers on "expert panel this", "score this", "rate these variants", "quality
  check this", "panel review", "expert score", "evaluate this copy/strategy/page".
  For variant generation and multi-round conversion optimization see autoresearch;
  for live-URL CRO auditing see conversion-ops; for the scripted content-production
  pipeline see content-pipeline.
when_to_use: |
  Use when any single content or strategy artifact needs a quality gate before publishing or handoff — scoring copy, landing-page drafts, email sequences, strategy docs, charts, or candidate evaluations against an assembled panel of domain experts. Triggers on "expert panel this", "score this", "rate these variants", "quality check this", or when another skill (e.g. outbound-engine) needs a final review gate.

  Not when: the goal is pre-launch variant generation and multi-round optimization of conversion copy — use `autoresearch`. Not when the focus is CRO auditing of a live URL (fetch + conversion-dimension scoring) — use `conversion-ops`; use content-ops when the artifact is a draft landing page being quality-gated before publish. Not when the job is running the content-production pipeline as scripts (RSS quote mining, video-clip discovery, repurposing, batch draft gating) — use `content-pipeline`.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Expert Panel

General-purpose scoring and iterative improvement engine. Auto-assembles the right experts for whatever is being evaluated, scores it, and loops until 90+.

## Core rules

1. Intake: collect content, content type, offer context, variants, and source skill — full procedure in `references/procedure-steps.md` Step 1.
2. Auto-assemble 7–10 experts: start from `experts/` pre-built panels, add 1–3 domain experts, always include AI Writing Detector (1.5x weight) and Brand Voice Match.
3. Select scoring rubric from `scoring-rubrics/` by content type; read the file for criteria.
4. Score recursively until 90+ aggregate (max 3 rounds). Humanizer weighted 1.5x. Show all rounds in output — the iteration trail is the value.
5. Check `references/patterns.md` at every round start and dock points for known-bad patterns before expert scoring.
6. When scoring another skill's output, generate a Source Improvement Brief (Step 6).
7. On user rejection of 90+ content, capture the reason and append to `references/patterns.md`.

## References

- [references/procedure-steps.md](references/procedure-steps.md) — full 7-step procedure: intake, panel assembly, rubric selection, scoring loop, output format, feedback-to-source, pattern learning
- [references/expert-assembly.md](references/expert-assembly.md) — domain-expert examples for auto-assembly of unfamiliar panels
- [references/patterns.md](references/patterns.md) — learned rejection patterns; read every run
- [experts/humanizer.md](experts/humanizer.md) — AI writing detection rubric (24 patterns); always run
- [experts/](experts/) — pre-built panels: humanizer, instagram, linkedin, newsletter, podcast-quotes, recruiting, seo-strategy, x-articles, youtube-shorts
- [scoring-rubrics/](scoring-rubrics/) — content-quality, conversion-quality, evaluation-quality, strategic-quality, visual-quality

## Related skills

- [autoresearch](../autoresearch/SKILL.md) — pre-launch variant generation + multi-round optimization of conversion copy; run before content-ops's final gate
- [conversion-ops](../conversion-ops/SKILL.md) — post-publish conversion layer; run after content-ops quality gate
- [adversarial-claims-reviewer](../adversarial-claims-reviewer/SKILL.md) — judges whether formal/technical claims are true; content-ops judges whether the prose is good
- [content-pipeline](../content-pipeline/SKILL.md) — script-driven content production (RSS quote mining, video-clip discovery, repurposing, batch draft gating); reuses this skill's `experts/` panels in its transform stage
