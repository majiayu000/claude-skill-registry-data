---
name: scbe-marketing-outreach-runbook
description: Build safe, high-value B2B outreach campaigns for SCBE services (cold email, social, investor outreach) with strong hooks, high-signal targeting, and anti-spam controls.
---

# SCBE Marketing Outreach Runbook

Use this skill when a user requests campaign planning, strong-hook message drafts, follow-up design, or outbound strategy for leads/investors.

## Operating Contract

1. Prioritize signal density over volume; every message has one clear pain-point fit.
2. Never produce spam-style messaging or unverifiable guarantees.
3. Default to consent-first framing and explicit opt-out language when needed.
4. Always return a `send_plan` with readiness and risk level.
5. Keep hooks short, specific, and action-oriented.

## Scope

Use this for:

- cold email / social outreach drafts
- investor research handoff messages
- message templates for founder/operations/finance/AI-adjacent roles
- follow-up cadence and sequence design

## Inputs

- `audience`: ICP (industry, role, geography, business size)
- `offer`: one service statement (e.g., "AI workflow automation for client intake")
- `proof`: one concrete proof line (example, metric, or recent win)
- `cta`: one clear ask (audit call, workflow map, pilot offer)
- `channels`: `email`, `linkedin`, `voice`, `multi`
- `tone`: concise, practical, non-hype

## Execution Flow

1. Segment lock
   - define single segment and one pain wedge.
   - reject broad all-at-once outreach with mixed personas.

2. Hook generation
   - produce 3 hook variants:
     - pain-first
     - risk-first
     - speed-first
   - all hooks must include a measurable context.

3. Message drafting
   - generate subject + 3-6 line body.
   - include one proof microline.
   - close with one action and one option to decline.

4. Cadence design
   - D0 initial: hook
   - D2 follow-up: short clarification
   - D5 value-drop: one proof / use case
   - D8 close/exit: “no-pressure wrap”

5. Quality and compliance gate
   - remove unsupported revenue promises
   - remove deceptive urgency claims
   - mark any high-risk claim as `review_required`

6. Package for send
   - return `recipient, name, channel, subject, body, cta, next_step, risk_note`

## Output Format

- `target_profile`: JSON summary of segment and intent.
- `campaign`: draft set with hooks and final copy.
- `cadence`: table of day offsets and message text.
- `send_plan`:
  - `status`: ready | needs_verification | needs_credentials
  - `connector`: email | linkedin | manual | other
  - `risk`: low | medium | high
- `next_action`: single step to execute now.

## Core Templates

- Hook pattern: `[pain] + [specific relief] + [tiny next step]`
- Proof pattern: `I can map [N] repetitive tasks and remove [M] choke points in [timeframe].`
- CTA pattern: `If useful, I can walk you through one workflow this week.`

## References

- `references/marketing-runbook.md`

## Anti-Spam Guardrails

- max one contact per channel every 48 hours
- no guaranteed ROI language
- no fabricated case studies
- add `consent_verified: false` when source context is unknown
