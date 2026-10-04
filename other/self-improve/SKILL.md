---
name: self-improve
description: Crystallize a wasteful thinking/behavioral loop into the cheapest durable artifact so it never recurs — routes a friction event to a CLAUDE.md rule, a deterministic shortcut script, a memory fact, a new skill, or a settings.json hook, picking artifact + scope by friction type. Use when the user invokes /self-improve, says "never again" / "remember this for next time" / "automate this away", OR proactively when you notice you just re-derived something, looped, or got corrected on a thing that prior knowledge would have prevented — then suggest running it.
---

# Self-Improve

Turn effort you just wasted into knowledge you'll never re-derive. One friction event → one durable artifact in the right scope, as small as possible.

## When to fire

- **Manual**: user runs `/self-improve` or says "never again", "remember this", "automate this".
- **Proactive**: you just (a) re-derived a fact/path/command, (b) looped or backtracked, (c) got corrected on a preference, or (d) hand-wrote code you'd write again. Stop and offer: *"That was avoidable — want me to /self-improve it into a [artifact]?"* Don't just silently continue.

## Flow

1. **Name the friction** in one sentence: *what* was wasted and *what prior knowledge* would have prevented it. This is the root cause — fix that, not the symptom.
2. **Run the target map** to resolve scope paths for this environment (don't re-derive them):
   ```
   bash scripts/targets.sh
   ```
3. **Route** friction type → artifact using the table below. If the type is **not 100% obvious from the user's prompt**, disambiguate with a *targeted Q&A* (§Disambiguation) — do **not** guess.
4. **Create the smallest artifact** that closes the loop. Prefer a one-line rule over prose, a script over regenerated code, a fact over a paragraph.
5. **Confirm** in one line: `✓ <artifact type> @ <path/scope> — <what it prevents>`.

## Routing table

| Friction type | Artifact | Where |
|---|---|---|
| Non-obvious **fact** re-discovered (path, command, env quirk, decision) | **Memory file** | memory dir (per target map) — follow the memory format in global CLAUDE.md |
| **Rule / preference** about *how to work* that was violated or corrected | **CLAUDE.md rule** | project CLAUDE.md (project-specific) or global `~/.claude/CLAUDE.md` (cross-project) |
| **Deterministic multi-step operation** re-derived from scratch | **Shortcut script** | project `scripts/` (project op) or skill `scripts/` (reusable) — keep output terse |
| **Reusable capability / workflow** worth triggering by description | **New skill** → delegate to `write-a-skill` | `~/.claude/skills/` |
| **Automated** before/after/each-time/on-event behavior, permission, or env var | **settings.json hook** → delegate to `update-config` | settings.json (harness runs it, not you) |

Tie-breakers: **a fact** is data you forgot; **a rule** is behavior you should change; **a script** is steps you'd repeat; **a skill** is a script + judgment worth auto-loading; **a hook** is a thing that must run *every* time without you remembering. When two fit, pick the cheaper/more-automatic one (hook > rule for "every time"; script > skill for "no judgment needed").

Scope rule: project-specific → project tree. About the user, your general workflow, or any tool across projects → global.

## Disambiguation (targeted Q&A)

Only when the route or scope isn't obvious. Use `AskUserQuestion`: terse, multiple-choice, **each option carries a concrete example of the resulting artifact**, recommended option first. Apply the interview discipline — ask only the forks that actually change the build (usually just *artifact type* and/or *scope*), resolve dependencies between them, prefer answering a fork yourself from the codebase over asking. One or two questions, then act. See [ROUTING.md](ROUTING.md) for the question bank and worked examples.

## Token-conservation principle

This skill exists to *spend tokens once* so future runs spend none. Every artifact must be the leanest form that works: rules are one line, scripts print terse output, memory files hold one fact. If your artifact is longer than the loop it prevents, you chose the wrong artifact.
