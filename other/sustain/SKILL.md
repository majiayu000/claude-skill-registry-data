---
description: Establish ongoing leadership rituals — 1:1s, retros, feedback cadence
---

# Sustain

Establish the ongoing leadership rituals for "$ARGUMENTS". Define the recurring processes that keep the team healthy, aligned, and growing.

## Prerequisites

Read all prior artifacts. If `.metapowers/leadership/$ARGUMENTS/04-develop.md` does not exist, tell the user:

> Phase 4 (Develop) has not been completed for "$ARGUMENTS". Run `/leadership:develop $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/leadership/$ARGUMENTS/skip-log.md`.

## Process

1. **Read all prior artifacts:**
   - Read `.metapowers/leadership/$ARGUMENTS/01-assess.md` through `04-develop.md`
   - Read `plugins/leadership/shared/one-on-one-template.md`
   - Read `plugins/leadership/shared/cfr-model.md`

2. **Define recurring rituals:**
   - **Weekly:** 1:1s (using template), team standup/sync
   - **Biweekly:** Team retrospective
   - **Monthly:** CFR review, skip-level meetings
   - **Quarterly:** OKR review and reset, team health check
   - For each ritual: purpose, format, duration, participants

3. **Create a leader's playbook:**
   - How to handle common situations: underperformance, conflict, burnout, new hire onboarding
   - When to escalate vs. handle yourself
   - How to maintain your own energy and avoid burnout

4. **Define health metrics:**
   - How will you know the team is healthy? (engagement, velocity, retention, satisfaction)
   - Warning signs to watch for
   - When to revisit earlier phases (re-assess, update vision)

5. **Write the artifact** to `.metapowers/leadership/$ARGUMENTS/05-sustain.md` with sections:
   - **Ritual Calendar** — all recurring meetings with cadence and format
   - **Leader's Playbook** — common situations and responses
   - **Health Metrics** — what to monitor and warning signs
   - **Renewal Triggers** — when to revisit assess/vision/build/develop

## Output

The sustainability plan written to `.metapowers/leadership/$ARGUMENTS/05-sustain.md`. Present a summary highlighting:
- Ritual calendar overview
- Key health metrics
- Top playbook entries
