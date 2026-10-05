---
name: skill-authoring-standard
description: >
  The bar a SKILL.md must clear before it ships in this lacquer — tight
  trigger-oriented frontmatter, single responsibility, no padding, companion
  files only when genuinely needed. Use when writing a new skill, reviewing
  an existing one, or auditing the skill set for quality.
---

# Skill Authoring Standard

A skill earns its place by being the thing someone reaches for at the right
moment, not by existing. Every line either helps a reader recognize when to
use it or tells them exactly what to do — nothing else survives review.

## Frontmatter

- **`name`** matches the directory name exactly (`core/skills/<name>/SKILL.md`,
  `name: <name>`). A mismatch (seen and fixed in this lacquer before) breaks
  discovery silently — the skill loads, but nothing points a reader at it by
  the name they'd search for.
- **`description`** is a trigger, not a summary. State *when* to reach for
  this skill — the scenarios, phrasings, or task shapes that should surface
  it — not just what it is. "Reviews code for style" tells a reader nothing
  actionable; "use before merging, when the user says 'is this safe', or when
  a change touches auth/secrets/exec" tells them exactly when to load it.
  Keep it to the trigger conditions — the body is where the how-to lives.
- **`disable-model-invocation: true`** for a skill with real side effects
  (it ships a release, pushes somewhere, deletes something) that should only
  ever run because a human explicitly typed `/<name>`, never because Claude's
  own judgment matched the description to a task. Without it, the description
  above is the only thing standing between an ambiguous prompt and an
  unintended side effect.

## Single responsibility

One skill, one job. If the body has an "and also" section that's really a
different concern (a distinct trigger, a distinct audience, a distinct
output), it's two skills wearing one name. Split it — a reader searching for
one of the two jobs shouldn't have to read past the other to find it.

## Body: instruction over exposition

Lead with the rubric or process, not throat-clearing about why the topic
matters. Cut anything a competent reader already knows (don't explain what a
git branch is; do explain the specific branching convention this lacquer
uses). If a sentence would be true of any skill on any topic, it's filler —
remove it.

Prefer concrete and checkable over abstract and aspirational: name specific
tools, specific commands, specific failure modes — not "follow best
practices" or "ensure high quality," which tell a reader nothing they can
act on or verify against.

## Companion files: only when they earn their keep

A skill is a single `SKILL.md` by default. Add a `references/` subdirectory
only when the reference material is long enough that inlining it would bury
the skill's core instructions (a large API surface, a big enumerated
checklist — see this profile's deeper stack-specific skills for the shape).
Add a runnable script only when the skill's value *is* the script — something
a reader executes, not just reads. If you're tempted to add a companion file
"for completeness," that's a sign the content belongs trimmed, not appended.

## Cross-referencing

Reference another skill by name in prose ("the same posture as the
security-review skill's verify-before-report principle") rather than
inventing a link syntax skills don't otherwise use — the reader who already
knows the referenced skill gets the connection; the reader who doesn't isn't
blocked by a dead link.

## Placement

Stack-agnostic guidance (applies regardless of iOS/web/supabase) belongs in
`core/skills/`. Anything that names a stack-specific tool, API, or convention
belongs in that profile's `skills/` — mixing the two either leaks
iOS-specific advice into a web project's synced skill set, or forces a
generalization vague enough to lose the concrete-and-checkable bar above.

Not every stack-specific rule belongs in a skill, though — a skill loads on
Claude's judgment (or `/<name>`), which is wrong for guidance that should load
automatically whenever a matching file is opened. For that shape, a project's
synced `CLAUDE.*.md` should point authors at `.claude/rules/` (path-scoped
files that load only when Claude touches matching paths) instead of growing
the profile body further. A profile `CLAUDE.*.md` pushing toward or past ~200
lines is the signal to split: move the parts that only matter for a specific
directory or file type into a rule, and reserve the profile body for what
every task in that stack needs regardless of which files it touches.

## Before shipping a skill

Read it back and ask: would a reader who's never seen this know from the
`description` alone whether to load it? Does every section either sharpen
that trigger or give an instruction they can act on? Is there a companion
file that exists because it seemed thorough rather than because it's used?
If any answer is no, cut, don't append.
