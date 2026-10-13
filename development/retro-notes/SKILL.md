---
name: retro-notes
description: "Capture AI-readable postmortems after a dev attempt resolves into a project-scoped lessons file that future /big-plan runs can read. Use when: (1) User says 'retro-notes', 'retro', 'capture lessons', 'fail-notes', 'postmortem', (2) A dev session wrapped up that took longer than expected, changed approach mid-way, or had non-obvious gotchas. Reader is a future planning agent."
---

# Retro Notes

## Purpose

Convert lessons from a just-resolved dev attempt into a structured, project-scoped lessons file (`/l-lessons-{area}` skill) that future planning runs (e.g. `/big-plan`) can consume. Goal: turn one-time pain into permanent leverage so the next attempt in the same area is faster.

## Pre-flight check (mandatory)

Before writing, confirm two things:

1. **Is the work actually wrapped up?** If the user is still mid-struggle, ask them to confirm. Mid-struggle notes record symptoms, not root causes — they crystallize the wrong lesson. If unresolved, suggest they invoke this skill again after the fix lands.
2. **What's the project area?** Look at the current working directory, recently touched files, and conversation topic. Propose a project-area name (kebab-case, e.g. `canvas-tools`, `tauri-window-mgmt`, `react-form-state`). Confirm with the user before writing.

## Locate or create the lessons file

The output is a project-scope skill at `.claude/skills/l-lessons-{area}/SKILL.md`.

**One growing file per problem-area, NOT one file per attempt.**

1. Check `.claude/skills/` for any existing `l-lessons-*` skill that matches the area. If a relevant one exists, **append** a new dated section to its `SKILL.md`.
2. If none exists, scaffold a new skill at `.claude/skills/l-lessons-{area}/SKILL.md` with the frontmatter shown below.

### Frontmatter for new lessons files

```yaml
---
name: l-lessons-{area}
description: Project lessons learned for {area}. Read PROACTIVELY before planning or implementing work touching {area} — contains traps, root causes, and "watch for next time" notes from previous attempts.
---
```

Keep `description` short but concrete enough that planning agents pick it up automatically.

## Note template

Append (or create) a section using exactly this structure:

```markdown
## {YYYY-MM-DD} — {short topic}

### What we set out to do
{1–2 sentences. The original goal, not the implementation.}

### Approach we tried first
{The wrong path. Be specific about the abstraction or structural choice — not the symptom.}

### Why it went wrong (root cause)
{The structural cause, not the symptom. See "Symptom vs root cause" below.}

### What worked instead
{The right abstraction or approach.}

### Watch for next time
- {Concrete trap, ideally in "if you see X, you're probably Y" form.}
- {Another trap. Aim for 2–5 bullets, not narrative.}

### Would-skip-if-redoing
{Things that wasted time and are now provably unnecessary. One short paragraph or bullet list.}
```

The **Watch for next time** section is the highest-leverage part. Future planning agents will scan it first. Keep bullets concrete and trap-shaped.

## Symptom vs root cause

When the user offers a symptom-shaped description, probe for the structural cause before writing.

| Symptom (what the user says first) | Root cause (what to actually record) |
|---|---|
| "zoom was buggy" | "transform threaded through every function instead of inverted at input boundary" |
| "form kept losing state" | "state owned by child instead of lifted to parent that survives re-mount" |
| "the build was flaky" | "test relied on filesystem ordering not guaranteed by the runtime" |
| "performance was bad" | "N+1 query in the render loop, hidden behind an inner abstraction" |

If the user gives a symptom, ask: "What was the actual structural reason that made the symptom show up — what was wrong about the shape of the code, not the bug itself?" Record the structural answer. The symptom can stay as one phrase in **What we set out to do** or **Approach we tried first** for context.

## Writing style

- **Terse.** The reader is a future LLM scanning for relevant patterns, not a human reading prose. Cut adjectives, cut narrative.
- **Specific over general.** "Coordinate transforms must invert at input boundary" beats "be careful with coordinates."
- **Past tense, no apology.** "We threaded the transform through every function" — not "I made a mistake by..."
- **No grep-able blame.** Don't name people or PRs; the lesson is structural.

## After writing

Briefly tell the user:

1. The lessons file is at `.claude/skills/l-lessons-{area}/SKILL.md`. `/big-plan` auto-reads matching `l-lessons-*` skills in its Step 1c before planning, so future planning runs in this area pick it up automatically.
2. Suggest a periodic `/retro-notes-refactor` pass (e.g. once the lessons file accumulates 5+ entries): merge overlapping notes, delete advice for code that no longer exists, promote repeated lessons into broader wisdom.
3. If the retro produced "nothing surprising, plan matched reality," that's signal too — the area is now well-mapped, future planning in this area can be lighter.

## When NOT to invoke this skill

- The work is still in progress or stuck.
- The dev was trivial and went exactly as planned (no lesson to extract).
- The lesson is universal CSS/JS knowledge that belongs in a global wisdom skill (e.g. `/css-wisdom`), not a project-scoped one.
