---
name: methodology-pattern-extractor
description: Extract recurring collaboration patterns from accumulated meeting logs (optionally session JSONL) and record them in docs/methodology.md with evidence of where each was sighted. Use when the user asks to update methodology, extract recurring patterns across the meeting logs, or consolidate recurring collaboration flows; or when five or more meeting logs have accumulated while §Patterns is still empty. Not for writing the meeting logs themselves (session-to-meeting-log) or for parking one-off ideas (backlog-routing-by-topic). Takes no arguments — the fork scans all of `meetings/*.md`.
context: fork
agent: general-purpose
---

# Methodology Pattern Extractor

Runs via [`context: fork`](https://code.claude.com/docs/en/skills#run-skills-in-a-subagent) — the fork has no memory of the invoking conversation, so it rescans `meetings/*.md` fresh each time.

## When to invoke

- The user says "update methodology", "extract a pattern", "I feel this flow has happened several times now".
- ≥ 5 meeting logs have accumulated but methodology.md §Patterns is still empty.
- After hitting an important milestone (end of spec phase, v1 release, major refactor close-out).

## Inputs

- All `meetings/*.md`
- Corresponding session JSONL (optional, for filling in details) — see
  `session-to-meeting-log`'s "Locating the session file" for finding the
  `.jsonl` by id (`ls ~/.claude/projects/*/<sessionId>.jsonl`) rather than
  computing the project directory; this skill has no `[session-id]` argument, so treat it as
  best-effort and skip it if the file isn't already known. [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
  only documents this transcript location for subagent transcripts specifically — treat the
  general-conversation case as unconfirmed.
- The existing `docs/methodology.md` (to avoid duplicate entries)

## Rule: ≥ 3 sightings or it's not a pattern

**Don't** turn a one-off behaviour into a pattern. Criteria:
- The same triggering situation appears in **≥ 3 different meeting logs**
- The response action each time is consistent or convergent
- There is an observable outcome

Items with fewer than 3 sightings can go into methodology.md §Backlog as "candidate patterns", annotated with the sighting count.

## Output format

One entry per pattern, five lines:

```markdown
### <Pattern name>

- **Trigger**: <what context activates this pattern>
- **Action**: <the observed response action>
- **Outcome**: <the resulting outcome>
- **Next-time adjust**: <what you'd improve next time, may be empty>
- **Sightings**: <one date per meeting log, comma-separated — ≥ 3 different logs, not ≥ 3 mentions in one log>
```

Example:

```markdown
### Section-by-section approval

- **Trigger**: User asks Leader to draft a document section (design.md / foundations.md / plan.md)
- **Action**: Leader advances one section at a time, waits for OK before moving on
- **Outcome**: Avoids the high cost of "whole-doc rejection and rewrite"
- **Next-time adjust**: Before dispatching a sub-agent, confirm all prerequisites for the section are Resolved
- **Sightings**: 2026-05-15, 2026-05-22, 2026-06-03
```

## Procedure

1. Grep meeting logs for frequently appearing verbs / triggers ("dispatch", "review round", "prerequisite", "rejected", ...).
2. For each high-frequency trigger, revisit its context — does the same action recur?
3. Filter to candidates with ≥ 3 sightings.
4. Extract Trigger / Action / Outcome / Next-time / Sightings.
5. **Append** to `methodology.md §Patterns`; never overwrite existing entries.
6. If a candidate has only 1–2 sightings, add it to methodology.md §Backlog as a "candidate pattern".

## Anti-patterns (also worth recording)

`docs/methodology.md` also carries a `§Anti-patterns` section (sibling of `§Patterns`) for
practices tried but found unsuitable. The three sections have different entry bars:

| Section | Entry bar |
|---|---|
| `§Patterns` | ≥ 3 sightings in different meeting logs |
| `§Anti-patterns` | 1 significant misstep with a clear lesson |
| `§Backlog` (candidate pattern) | 1–2 sightings, annotated with the count |

## Verification checklist

- Every pattern carries Sightings ≥ 3.
- No duplicates with existing entries (grep `methodology.md` first).
- Original meeting logs are never modified.
- Pattern names use kebab-case or short phrases, no more than 6 words.

## Deviation considerations

- **Solo project, single author**: "recurrence" includes the author's own habits; the ≥ 3 rule still applies.
- **Cross-project**: this skill's default scope is one repo; if extracting across repos, explicitly cite each origin.

## Related skills

- `session-to-meeting-log`: produces this skill's input.
- `backlog-routing-by-topic`: candidate patterns go into methodology.md §Backlog.
- `subagent-review-cycles` / `spec-phase-orchestration` / `leader-developer-handoff-contract`: codified forms of common patterns.
