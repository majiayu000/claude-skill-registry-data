---
name: learning-memory
description: Use when capturing or restoring a learner's persistent profile to personalize teaching across sessions.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [memory, personalization, cross-session, learner-profile]
status: stable
---

# Purpose

Maintain a structured learner profile across sessions so agents start at the right depth, avoid re-teaching covered material, and prioritize known weak areas.

# Activation

- New session begins and prior context may exist. Learner references prior sessions or covered topics. Session ends and state should be preserved. Agent needs to personalize without re-asking onboarding questions.
- **Skip if**: one-off session with no continuity desired, no persistent storage available, or narrow stateless task.
- **Routing**: run at session start (restore) and end (save). Feed weak areas to `weak-area-tracker`. Profile drives `find-your-level` for returning learners with uncertain level.

# Inputs

- Prior session summary/profile, current session transcript, concepts + outcomes, learner self-reports, error patterns from assessment skills.

# Profile Schema (compact)

```yaml
learner_profile:
  level: beginner | intermediate | advanced
  stated_goal: "<goal>"
  learning_style: code-first | concept-first | mixed
  weak_areas: [{topic, type, last_seen, correction_attempted}]
  covered_topics: [{topic, confidence: low|medium|high, last_confirmed}]
  active_checkpoint: "<last concept/milestone in progress>"
  session_count: N
  last_session: "<ISO date>"
```

# Workflow

## Session Start (Restore)
1. **Retrieve** — Check for prior profile. If exists: summarize and confirm accuracy with learner. If none: run `find-your-level`.
2. **Staleness Check** — Last session 2+ weeks ago → flag for light review. Goal changed → update target.
3. **Inject** — Feed relevant profile data (level, weak areas, last checkpoint) into current session. Don't re-explain confirmed material unless requested.

## Session End (Save)
4. **Extract** — Record: concepts covered, understanding outcomes, new weak areas, self-reported confidence.
5. **Update** — Merge into profile. Promote "in-progress" → "covered" when confirmed. Add new weak areas.
6. **Handoff** — Output compact summary: where to resume, what to skip, top 1–2 priorities for next session.

# Rules

- DO: confirm profile accuracy with learner at session start — never assume stale data is current.
- DO: base profile updates on observable evidence, not assumptions.
- DO: cap weak-area list at 5 active items.
- DO: frame all profile data as "what we'll focus on" not "what went wrong."
- DON'T: re-teach confirmed topics without request or regression evidence.
- DON'T: skip the session-end save — always output the handoff note.
- DON'T: treat "covered" as "fully mastered" — watch for regression signals.

# Output

Session start: restored profile summary + confirmation prompt. Session end: concepts covered with outcomes, new/resolved weak areas, and handoff note (resume point + priorities + skip list). Format naturally.

# Checklist

- [ ] Profile confirmed with learner at session start.
- [ ] Staleness check performed if 2+ week gap.
- [ ] Session outcomes logged with evidence.
- [ ] Handoff note produced at session end.
