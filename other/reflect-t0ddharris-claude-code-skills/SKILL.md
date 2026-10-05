---
name: reflect
version: 1.0.0
description: "Analyze the current conversation for corrections, approvals, and patterns, then propose updates to the skill files that were used. Trigger with /reflect or automatically at end of /brief. Use when the user says 'reflect,' 'learn from this,' 'update the skill,' or 'remember this for next time.'"
---

# Reflect: Self-Improving Skills

Scan the current conversation for signals (corrections, approvals, patterns) and propose updates to the skill files that were invoked during the session. Every correction should only need to happen once.

## Step 1: Identify Skills Used

Scan the conversation for skill invocations. Look for:
- Explicit `/skill-name` calls
- Skill tool invocations (the Skill tool being called)
- Agent delegations that loaded a skill

If no skills were used this session, check whether the corrections apply to:
- General behavior → suggest a CLAUDE.md or memory update instead
- A specific skill that *should* have been used → note the routing gap
- Neither → report "no learnings to extract" and stop

## Step 2: Extract Signals

Scan the full conversation for three signal types:

**HIGH confidence (explicit corrections):**
- User said "no," "don't," "never," "stop," "wrong," "not that"
- User rejected output and asked for a different approach
- User provided a specific rule ("always do X," "use Y not Z")
- User flagged an error, bad pattern, or bad output

**MEDIUM confidence (validated patterns):**
- User approved output without pushback ("yes," "perfect," "looks good," accepted without changes)
- A non-obvious approach worked and the user confirmed it
- User's positive reaction to a specific technique or format

**LOW confidence (observations):**
- Patterns that seemed to work but weren't explicitly validated
- Ambiguous signals worth reviewing later

**Not a signal, skip these:**
- One-time contextual decisions (e.g., "make this one shorter" doesn't mean all future outputs should be shorter)
- Task-specific details that don't generalize beyond this session
- Things already documented in the skill file, CLAUDE.md, or memory
- Corrections to factual or biographical content (those belong in a dedicated facts/context file, not skills)
- Preferences already captured in the session brief's carried-forward sections

## Step 3: Read the Target Skill Files

For each skill identified in Step 1, read its SKILL.md. Check:
- Does a `## Learnings` section exist at the bottom? If not, it will be created.
- Is this learning already captured? Don't duplicate.
- Does this learning contradict an existing learning or rule? Flag the conflict for the user to resolve.

## Step 4: Propose Updates

Present proposed changes in this format. **Always label each proposed update with a letter (A, B, C...) so the user can approve or reject individual items by letter.**

```
## Reflect: Session [N] Learnings

### Signals Detected
- **[HIGH]** [What happened] → [Proposed rule]
- **[MEDIUM]** [What happened] → [Proposed rule]

### Proposed Skill Updates

**[skill-name]:**
- **(A)** [HIGH] Add: "[actionable rule]"
- **(B)** [MEDIUM] Add: "[pattern description]"

**[other-skill-name]:**
- **(C)** [HIGH] Add: "[actionable rule]"

### Skipped (already captured)
- [Any signals that are already in the skill or CLAUDE.md]

### No Changes (if applicable)
- [Why no updates are warranted this session]
```

Letters run continuously across skills (A, B, C...) so the user can say "approve A and C, skip B" without ambiguity.

**STOP and wait for user approval before making any changes.**

The user can:
- Accept all proposed changes (Y / approve all)
- Accept some, reject others by letter ("A and C" / "skip B")
- Modify the wording of any proposed change
- Add learnings that weren't detected
- Reject everything (no changes made)

## Step 5: Apply Approved Changes

Append approved learnings to the skill's `## Learnings` section at the bottom of SKILL.md:

```markdown
## Learnings

<!-- Updated by /reflect. Promote stable patterns to the main skill body. -->

- **[HIGH]** Rule description here. *(Session N, YYYY-MM-DD)*
- **[MEDIUM]** Pattern description here. *(Session N, YYYY-MM-DD)*
```

Format rules:
- One line per learning, prefixed with confidence tag
- Include session number and date for traceability
- Write as actionable rules, not session logs ("Always X" not "Todd said to do X")
- Keep each entry to one sentence. If it needs more, it's too complex for a learning: promote it directly to the main skill body instead.

## Step 6: Graduation Check

After applying updates, scan the full `## Learnings` section. If any learning:
- Has been present for 5+ sessions without being contradicted
- Is HIGH confidence
- Applies broadly (not an edge case)

**Suggest promoting it** into the main skill body (the relevant framework, principles, or guidelines section). Once promoted, remove it from `## Learnings` to keep the section lean.

Tell the user which learnings are candidates for graduation and where in the skill body they'd go. Apply only with approval.

## When Called from /brief

When invoked as Step 2.5 of the `/brief` workflow:
- Run after the brief is written, before the git question
- Keep output concise: just the signals table and proposed changes
- Skill updates are committed together with the brief in one commit
- If no learnings were detected, say so in one line and move on

## When Called Standalone (/reflect)

When invoked directly:
- Run the full flow above
- Ask the user about git separately (commit the skill updates?)

## Scope Boundaries

This skill does NOT:
- Modify factual or biographical content files (those are managed separately, outside this skill)
- Modify `CLAUDE.md` (use `/revise-claude-md` for that; but DO suggest CLAUDE.md updates if a learning is cross-cutting)
- Modify memory files (the memory system is separate)
- Auto-commit without user approval
- Extract learnings when no skills were used (suggests alternatives instead)

## Quality Gate

Before proposing any learning, ask yourself:
1. **Is this generalizable?** Would this apply in the next 5 sessions, not just this one?
2. **Is this actionable?** Can a future session follow this rule without ambiguity?
3. **Is it already captured?** Check the skill file, CLAUDE.md, memory, and session brief.
4. **Is it the right home?** Skill-specific → skill file. Cross-cutting → suggest CLAUDE.md. Factual/biographical → suggest a dedicated facts/context file.

If a session produced no generalizable learnings, that's fine. Say "no new learnings detected" and move on. Not every session teaches something new. Forcing weak learnings into skills degrades them over time.

## Learnings

<!-- Updated by /reflect. Promote stable patterns to the main skill body. -->

- **[HIGH]** Each run, scan the memory directory for thematic clusters (3+ related feedback/gotcha memories): propose graduating the theme into a dedicated skill. *(Session 4 (Apexfall), 2026-07-06, per Todd)*
