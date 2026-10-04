---
name: morning
description: Morning kickoff ritual — status check, daily brief review, top priorities, set intention for the day. Use when starting a work session or asked to "start the day", "morning", "kickoff", "what should I work on".
---

# Morning Kickoff

Start the day with clarity. Check status, review what's waiting, set one intention.

## Checklist

1. **Run `/z`** — get branch status, uncommitted changes, recent commits
2. **Check daily brief** — read latest file in `docs/daily-briefs/` (if the scheduled agent has run)
3. **Check inspiration** — read latest file in `research/inspiration/` (if available)
4. **Open issues** — run `gh issue list --state open --limit 5`
5. **Open PRs** — run `gh pr list --state open`. Watch for `claude/inbox-digest-YYYY-MM-DD` (overnight ZOE digest, see Doc 652).
6. **ZOE inbox check** — run `/inbox count`. If unread > 0, surface count in the brief and offer `/inbox research all` (require Zaal "yes" before firing — each item can become a research doc + PR, blast radius is real).
7. **Yesterday's reflection** — read latest file in `docs/reflections/` (if available)

## Present to User

After gathering everything, present a concise morning brief:

```
## Good morning

**Branch:** [current branch] | **Uncommitted:** [yes/no]
**Last commit:** [message] ([time ago])
**ZOE inbox:** [N unread] · [overnight digest: PR #M | none]

### Waiting for you
- [Open PRs needing review - call out claude/inbox-digest-* PRs first]
- [Open issues, sorted by priority]

### Yesterday's note to today
[Pull from reflection journal if it exists]

### Inspiration
[One-line from today's Steal Like an Artist entry if it exists]

### The question
What's the ONE thing that would make today a win?
```

Wait for the user's answer. Once they state their intention, acknowledge it and suggest which skill to start with (`/investigate` for bugs, `/brainstorm` for features, `/ship` for PRs, `/zao-research` for research).
