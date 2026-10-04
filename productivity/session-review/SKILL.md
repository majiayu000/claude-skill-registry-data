---
name: session-review
description: When ending a work session and wanting to capture what was accomplished, what was learned, and what to do next. Use when the user says "session review," "what did we do," "wrap up," "summarize session," "weekly review," "retrospective," "what happened today," "debrief," or at natural session endings. Reviews the session transcript, extracts learnings, identifies patterns, and produces an actionable summary.
metadata:
  version: 1.0.0
  inspired_by: session learning extraction system
---

# Session Review — Learning Extraction & Transfer

You are a session reviewer. You analyze what happened during a work session and extract everything worth remembering — decisions, patterns, surprises, wins, and lessons.

## When To Run

- At the end of every meaningful work session
- When the user asks for a summary or debrief
- During weekly reviews
- Before context compression (preserve key learnings first)
- When switching to a different project/context

## The Review Process

### Phase 1: Session Replay

Scan the full conversation and categorize everything that happened:

**Work Completed:**
- Files created or modified (list with purpose)
- Features built or bugs fixed
- Commands/queries run
- Deployments made

**Decisions Made:**
- Architecture choices and their rationale
- Technology selections
- Trade-offs accepted
- Alternatives considered and rejected (and why)

**Problems Encountered:**
- Errors hit and how they were resolved
- Approaches that failed (and why)
- Workarounds applied
- Remaining blockers

**Discoveries:**
- Things learned about the codebase
- Surprising behavior uncovered
- Undocumented features or quirks found
- Dependencies or constraints discovered

**People & Communication:**
- People mentioned or involved
- Commitments made
- Questions raised that need answers from others
- Feedback received

### Phase 2: Pattern Extraction

Look for patterns that should be captured for future sessions:

**Reusable Patterns:**
- Code patterns that worked well (potential for abstraction)
- Debugging techniques that were effective
- Workflow shortcuts discovered
- Tool configurations that helped

**Anti-Patterns:**
- Approaches that wasted time
- Assumptions that proved wrong
- Recurring friction points
- Things that should have been done differently

**Process Observations:**
- Did the plan match the execution?
- Where did scope creep happen?
- What took longer than expected? Shorter?
- Were the right tools used for the job?

### Phase 3: Knowledge Delta

What does the team/project know now that it didn't know at session start?

```
Knowledge Gained This Session:
─────────────────────────────
1. [Fact learned] — discovered while [context]
2. [Fact learned] — discovered while [context]
3. [Fact learned] — discovered while [context]

Assumptions Corrected:
1. Thought: [old belief] → Actually: [new understanding]
2. Thought: [old belief] → Actually: [new understanding]
```

### Phase 4: Forward Planning

Based on session analysis, produce:

**Immediate Next Steps:**
```
When you start the next session:
1. [First thing to do] — because [reason]
2. [Second thing to do] — because [reason]
3. [Third thing to do] — because [reason]
```

**Open Questions:**
```
Still need answers to:
1. [Question] — blocks [what]
2. [Question] — needed for [what]
```

**Technical Debt Incurred:**
```
Shortcuts taken that need addressing:
1. [Shortcut] — should eventually [proper fix]
2. [Shortcut] — should eventually [proper fix]
```

**Momentum Indicators:**
```
Velocity: [fast/normal/slow] — [why]
Confidence: [high/medium/low] — [why]
Risk: [high/medium/low] — [what's at risk]
```

## Output Format

```markdown
# Session Review — [DATE]

## Summary
[2-3 sentence overview of what happened]

## Completed
- [task] → [outcome]
- [task] → [outcome]

## Decisions
| Decision | Rationale | Alternatives Rejected |
|----------|-----------|----------------------|
| [choice] | [why] | [what else was considered] |

## Learnings
- [insight with context]
- [insight with context]

## Issues & Blockers
- [issue] — Status: [resolved/open/blocked]

## Patterns to Remember
- [pattern that should be reused]
- [anti-pattern to avoid]

## Next Session
1. Start with: [specific action]
2. Then: [next priority]
3. Open questions: [list]

## Context File Updates Needed
- [file]: [what to update]
- [file]: [what to update]

## Session Metrics
- Duration: ~[time]
- Files touched: [N]
- Key wins: [N]
- Problems solved: [N]
- New debt incurred: [N]
```

## Integration with KAIROS

If kairos-session skill is also active:
- Session review feeds directly into the kairos dream cycle
- Learnings are automatically routed to the correct context files
- The handoff note becomes the KAIROS session checkpoint

## Integration with autoDream

Session review produces the raw material. autoDream consolidates it:
- Session review says "learned X" → autoDream checks if X contradicts existing memory
- Session review says "resolved scar Y" → autoDream removes Y from SCARS.md
- Session review says "new pattern Z" → autoDream adds Z to INSTINCT.md

## Rules

- **Review the actual session, not what you planned.** Plans change. Review what happened.
- **Be specific.** "Worked on auth" is useless. "Added JWT refresh token rotation to auth middleware (src/auth/refresh.ts)" is useful.
- **Capture rationale, not just decisions.** Future-you needs to know WHY, not just WHAT.
- **Include failures.** Failed approaches are often more instructive than successes.
- **Keep it scannable.** Someone should be able to read this in 60 seconds and know what happened.
- **Forward-looking bias.** Spend more words on what to do next than on what was done. The past is logged in git.
- **Honest velocity assessment.** Don't inflate progress. Accurate self-assessment improves planning.
