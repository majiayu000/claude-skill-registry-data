---
name: harness-lessons
description: >
  Measures what this `.claude/` costs in context — every session and per skill, agent, rule
  and hook — through `ArchHook.jar footprint`, reads the audit trail's spend, failures and
  peaks when the project records one, judges both against a curated baseline of Claude Code
  and Anthropic best practices, and writes `harness-NNN.md` — under `docs/lessons-learned/` in
  a generated project, `.claude/lessons-learned/` here: each finding with its evidence, the
  practice it breaks, the file that owns the fix and the expected saving.
  Ends with `/report-issue` in a generated project, `/claude-code-architect-designer` here.
  Explicit invocation only.
argument-hint: "[empty for the whole harness | <skill or agent name> to focus on one piece]"
disable-model-invocation: true
allowed-tools: Read, Write, Glob, Grep, Bash(java:*), Bash(ls:*), WebFetch(domain:code.claude.com), WebFetch(domain:platform.claude.com), WebFetch(domain:www.anthropic.com)
model: opus
effort: high
---

# Harness Lessons

Turns the cost and behavior of this `.claude/` into a lesson its owner can act on. A skill
that loads 16k tokens, a rule with no `paths`, a hook that spawns on every tool call, an
agent that re-reads what its caller had: each one is paid in every session or every run, and
each one has exactly one owning file. This skill finds the owner, names the change and
estimates what it saves. It changes nothing in `.claude/` itself.

## Target

$ARGUMENTS

Empty: the whole harness. A skill or agent name: § 3 judges only that piece, § 1 and § 2 stay
whole — the numbers of one piece only mean something next to the others.

## Measured

!`java -jar "${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/ArchHook.jar" footprint 2>&1`

## Spent

!`java -jar "${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/ArchHook.jar" audit summary 2>&1`

---

**Never recompute a number the two blocks printed**, and never read every `SKILL.md` to
re-derive one: the arithmetic is Java on purpose (`references/best-practices.md` BP-12). Open a
file only to judge a finding the numbers already point at.

## Why this is a skill (Form 2)

Form 2 because writing a lessons file is a side effect the user decides, and the analysis runs
a few times a month, never every session — axes 2 and 3 of the design interview. The closest
rejected form was extending `audit-usage`: its `observer` class writes nothing, runs on
`sonnet` and stays out of the trail, while judging which piece of `.claude/` to cut needs
`opus` and a file. Measuring stays in `ArchHook.jar footprint` so the numbers repeat from run to
run. Record: `@.claude/decisions/0188-harness-lessons-and-footprint-mode.md`.

## Procedure

### 1 · Where am I

- `.claude/.arch-provenance.json` exists → **generated project**: § Measured and § Spent
  both count; the lessons folder is `docs/lessons-learned/` — gitignored there, and where
  `/report-issue` reads — and the handoff is `/report-issue`.
- No stamp and a `decisions/` folder sits under `.claude/` → **the Nerviz repository**: the trail is off here
  by design, so § Spent is empty and only § Measured counts; the lessons folder is
  `.claude/lessons-learned/`, beside the run reports — `docs/` is the public documentation —
  and the handoff is `/claude-code-architect-designer`.
- § Measured starts with `❌` → stop, quote it, write nothing.
- § Spent empty in a generated project → the trail is off; say so, judge § Measured alone,
  and name in the lessons file what the trail would have added.

### 2 · Baseline — read, revalidate when stale

Read `references/best-practices.md` whole. Its `Verified on` date older than **90 days** →
WebFetch each URL of its `Sources` table, asking whether each practice citing that key still
holds and whether a threshold changed. Use what the sources say now for this run. List every
practice that changed or vanished in the lessons file's `## Baseline` section — never edit the
reference here: in a generated project `/arch-adopt` overwrites it, and in this repository it
is `/claude-code-architect-designer`'s to change. Within the window: no fetch.

### 3 · Findings

Walk the four lenses in order. A finding needs a number from § Measured or § Spent, a
practice id (`BP-NN` or `AP-NN`), and one owning file. No number → it is an opinion, leave it
out.

| Lens | Where the evidence comes from |
|---|---|
| **Every-session cost** | § Measured › Every session — `CLAUDE.md` past its limit, an import, a rule without `paths`, a long listing, a server whose CLI exists |
| **Per-invocation cost** | § Measured › Skills, Agents — a body past its limit or large next to its peers, files with no contents list, a `sonnet`-shaped procedure pinned to `opus` or the reverse, an agent re-loading what its caller had · § Spent › own tokens, Peak, dominant tool |
| **Behavior** | § Spent › failure ratio, compaction incidents, permissions granted, repeated tool failures — open the one report the block names for the worst piece |
| **Guarantees** | § Measured › Hooks — an entry spawning on every tool call; prose that keeps being missed (AP-01) and belongs in a hook; a hook for a mere preference (BP-20) |

For each finding decide:

1. **Owner** — the one file whose change removes it, as a path in `.claude/`. A norm stated in
   two places is itself the finding (`@CLAUDE.md` invariant 2).
2. **Change** — concrete: what moves where, what gets cut, which field changes. "Shorten the
   skill" is not a change; "move § 5's 200-line decision table to `references/x.md` and cite
   it" is.
3. **Saving** — tokens per session (every-session lens) or per run (the rest), from the
   block's own numbers, labelled as an estimate. Behavior and guarantee findings say what
   stops happening instead.
4. **Priority** — saving × how often it is paid: every session beats every `/new-feature`,
   which beats a manual skill run once a month.

Then check each candidate against the `decisions/` folder under `.claude/` when it exists: a size or a pin
decided on purpose (`0080`, `0081`) is reported with its record, never as a defect.

### 4 · Write `<lessons folder>/harness-NNN.md`

The lessons folder is the one § 1 named. `NNN` is the highest existing `harness-*.md` there plus one, `001` when there is none. Fill
`templates/lessons-learned.md.example`. When `harness-<NNN-1>.md` exists, fill its *Previous*
and *Δ* columns and mark each finding *new*, *recurring* or — in a closing list — *gone*. A
recurring finding whose previous file already named the change says so: it has not reached
this project, or not been made.

### 5 · Hand off — print the command, invoke nothing

Write the `## Next` line at the end of the file and end the report with it:

- Generated project: `/report-issue docs/lessons-learned/harness-NNN.md`
- This repository: `/claude-code-architect-designer` followed by the highest-priority finding
  in one sentence, with the path of the lessons file

## Failure modes

**Jar missing or older than the source** (`Unknown mode: footprint`):
```
❌ ArchHook.jar has no `footprint` mode. Here: java .claude/hooks/ArchHook.java build.
   In a generated project: /arch-adopt pulls the current jar. Nothing written.
```

**No network past the window:**
```
⚠️ Baseline verified on <date>, past 90 days, and <url> did not answer. Judging against it
   as is — the lessons file says so in ## Baseline.
```

**Focus names no piece:**
```
❌ <name> is no skill under .claude/skills/ nor agent under .claude/agents/. Nothing written.
```

## Report

```
✅ Harness lessons — every session ~<n> tokens · <F> findings (<s> session, <i> invocation, <b> behavior, <g> guarantee)

Lessons ... <lessons folder>/harness-NNN.md
Top ....... <owner path> — <change> — saves ~<n> tokens per <session | run>
Baseline .. verified on <date> <| revalidated now: <k> practices changed>
Next ...... <the ## Next line>
```

## Contract

**Class:** report — the territory is `skill_classes.report` in
`@.claude/schemas/extensions.json`, with this skill's own override:
`docs/lessons-learned/**` and `.claude/lessons-learned/harness-*.md`, nothing else.
`ArchHook.java guard` enforces it.

**Reads** the output of `ArchHook.jar footprint` and `audit summary`,
`references/best-practices.md`, `.claude/audit-usage/*.md` for the report § Spent names,
`.claude/.arch-provenance.json`, the `decisions/` folder under `.claude/` when present, and the files a finding
points at. WebFetch only the URLs of the reference's `Sources` table.

**Writes** `docs/lessons-learned/harness-NNN.md` in a generated project,
`.claude/lessons-learned/harness-NNN.md` in the Nerviz repository.

**Never writes** any other path under `.claude/` — the change belongs to the owner's skill, here or upstream —
and never `references/best-practices.md`, whose owner is `claude-code-architect-designer`.

**Handoff** — prints `/report-issue` or `/claude-code-architect-designer`; invokes neither.
