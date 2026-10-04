---
name: icaire-comms-lead-plan-social-content
description: Plan the next weekly ICAIRE social-content batch from recent Brain updates and public-interest evidence. Use when the user asks what ICAIRE should post next or wants a source-grounded social-content plan.
---

Plan the next ICAIRE social-content batch by filtering recent updates and ranking the surviving public-interest ideas.

## Contract Checklist

- Run `check-for-public-facing-achievements` as the required recent-update filter.
- Run `icaire-social-content-planning` on the filtered evidence when its live Brain and analytics sources are available.
- Read every source page used for a shortlisted idea and preserve its Brain slug.
- Keep internal progress, plans, approvals, and unresolved work out of the public shortlist.
- Stop at a source-grounded plan: do not draft copy, create visuals, publish, schedule, or write Brain pages.
- Carry missing facts, rights, consent, partner review, and pillar-leader approval as explicit dependencies.

## Workflow

1. Define the weekly planning window.
   - Use the date range supplied by the user; otherwise review the latest 14 days of ICAIRE updates and state the exact dates used.
   - Confirm the requested batch size, channels, language, and whether the output is for internal review or later production.
   - Anti-patterns: silently changing the date range, treating a previous batch as current source evidence, assuming publication approval.

2. Filter recent updates through the source skill.
   - Run `check-for-public-facing-achievements` against the relevant recent stand-up reports, initiative pages, deliverables, and other canonical Brain sources.
   - Keep the skill's categories separate: public-facing, public-facing with confirmation needed, and internal-only.
   - Preserve a one-line factual basis and source slug for every candidate that survives.
   - Anti-patterns: mining search snippets, turning a plan into an achievement, converting operational work into public impact, dropping caveats.

3. Rank the public-interest ideas.
   - Run `icaire-social-content-planning` using the filtered source pages, not the raw update list alone.
   - Apply its audience, mission, consequence, source, safety, and originality gates before scoring.
   - If the analytics basis is missing or weak, label the limitation and use it only for bounded format or experiment guidance.
   - Anti-patterns: ranking by institutional excitement, using internal metrics as the topic, treating visual appeal as topic value, inventing claims.

4. Build the production handoff.
   - Select the requested number of ideas, or a practical default of 4 to 8 when no number is given.
   - For each idea provide the public hook, audience, public value, source slugs, confirmed facts, confirmation-needed facts, suggested channel, CTA direction, visual direction, and relevant pillar owner.
   - Flag podcast items that need real guest photos, episode details, public links, or guest approval rather than generating substitute claims or portraits.
   - Anti-patterns: drafting final post copy, creating a publication calendar without dates, treating a proposed CTA or asset as confirmed.

5. Verify the handoff.
   - Check that every selected idea has a readable Brain source, an external audience, a public consequence or question, and an approval path.
   - Include rejected candidates and the gate they failed when this prevents overclaiming.
   - State explicitly that no copy, asset, publication, schedule, or Brain write was performed.
   - Anti-patterns: hiding missing evidence, claiming production readiness, publishing or updating campaign state.

## Anti-Patterns

- Do not draft or publish from this planning skill.
- Do not use completion, attendance, certification, satisfaction, email, poll, task, or operational metrics as the public topic unless an approved accountability report explicitly requires them.
- Do not claim a launch, approval, publication, partner endorsement, event date, guest detail, or public URL without evidence.
- Do not replace the live ICAIRE Brain with remembered context or a local summary.

## Output

Return:

- `Planning Frame`: dates, batch size, channels, audience, language, and objective.
- `Source Filter`: the `check-for-public-facing-achievements` result with source slugs.
- `Ranked Batch`: selected ideas with public hook, audience, public value, source basis, facts, dependencies, channel, CTA direction, visual direction, and pillar owner.
- `Rejected Or Held`: candidates excluded or held and the reason.
- `Production Handoff`: the exact inputs required by `icaire-comms-lead-produce-social-content-batch`.
- `Non-Actions`: copy, visuals, files, publication, scheduling, and Brain writes not performed.
