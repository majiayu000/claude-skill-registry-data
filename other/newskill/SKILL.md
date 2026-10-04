---
name: newskill
description: >-
  Scaffold a new skillhub skill, or repair one that drifted, across all four
  registration surfaces in one motion — folder, README table row, marketplace
  plugin, and trigger evals — then prove it with validate-skills.py. User-invoked.
disable-model-invocation: true
---

# newskill — add a skill without drift

`/newskill scaffold <name> "<description>" <category>` — create a new skill, registered
`/newskill fix [<name>]` — complete a skill that exists in some surfaces but not others

A skillhub skill lives in **four surfaces**, and it is only really "added" when
all four agree:

1. **Folder** — `.claude/skills/<name>/SKILL.md` with valid frontmatter.
2. **README table row** — a row in the right category table (a prose mention
   does *not* count; the validator checks for a table row specifically).
3. **Marketplace** — `<name>` listed in one plugin's `skills[]` in
   `.claude-plugin/marketplace.json`.
4. **Trigger evals** — cases in `evals/triggers.json` (model-invoked skills
   only; user-invoked skills are exempt).

**Drift** is these four disagreeing — the default failure of hand-adding a
skill. The oracle for drift is `python3 scripts/validate-skills.py`: it already
reports which surfaces are missing. This skill's whole job is to make the four
agree and leave the validator green.

## The loop (both modes end here)

Run `python3 scripts/validate-skills.py` → read each FAIL/WARN → fix that exact
surface → re-run. Repeat until **no FAIL**. Never assert done from memory; the
validator is cheap and authoritative.

## Mode: scaffold

Adding a brand-new skill from a name + description + category.

1. **Guard.** If `.claude/skills/<name>/` already exists, **stop** — this is a
   `fix`, not a scaffold; never overwrite an existing `SKILL.md`. Also reject a
   `<name>` that collides with a harness built-in (the validator's `BUILTINS`
   set) or an existing skill.
2. **Folder.** Write `.claude/skills/<name>/SKILL.md` with frontmatter (`name`
   = folder name) and a `description`. If `out/tune/principles.md` exists, read
   it before writing the body — each line is an authoring rule distilled from
   accepted past fixes. Keep the description **≤ 950 chars**
   (soft limit; hard wall is 1024) — front-load the leading word, one trigger
   per branch. For a user-invoked tool add `disable-model-invocation: true` and
   write a human-facing one-line description (no trigger list).
3. **Category → plugin + table.** `<category>` is one of `coding-loop` /
   `research` / `daily`. Add `./.claude/skills/<name>` to that plugin's
   `skills[]` in `marketplace.json`, and add one row to the matching README
   category table.
4. **Trigger evals (model-invoked only).** Add ≥2 cases to
   `evals/triggers.json`, including a routing pair against the nearest
   neighbour skill. Skip for user-invoked skills.
5. **Pre-flight the body's snippets.** Every snippet the new `SKILL.md` embeds
   is tried once against real data before the skill ships, output quoted
   in-session: execute each bash line (placeholders filled with real values),
   fetch each API endpoint, read each referenced path. A snippet that fails as
   written is a bug in the skill, not a formatting nit. Two honest outs, both
   flagged **unverified** and never skipped silently: one that can't run here
   (external account, missing binary, a file that exists only mid-run), and one
   that would mutate real state — never run something destructive just to
   prove it. This is tune's prove-the-rules-bite extended from config to
   authoring. (Fix mode is exempt — it never writes a body.)
6. **Run the loop** above until green.

**Completion criterion:** validator prints no FAIL; the new `<name>` appears in
all four surfaces it's required in; every embedded snippet has run clean or is
flagged unverified.

## Mode: fix

Completing a skill that already drifted (e.g. a folder with no registration).

1. **Diagnose.** Run the validator; it lists exactly which surfaces `<name>`
   (or every skill, if `<name>` omitted) is missing from.
2. **Register only — never rewrite the body.** Fill each missing surface:
   marketplace entry, README table row, trigger cases. Touch `SKILL.md` **only**
   if the validator flags the frontmatter itself (e.g. description over the
   1024-char limit) — and then edit the frontmatter alone, leaving the body
   unchanged.
3. **Run the loop** until green.

**Completion criterion:** validator prints no FAIL; the previously-missing
surfaces now list `<name>`, and its `SKILL.md` body is unchanged.

## After a description change — run the eval

Adding or rewording a **model-invoked** description changes the skill's only
trigger surface, so a green validator is necessary but not sufficient. Re-run
the trigger eval per `evals/README.md` (a fresh judge sub-agent over
`evals/triggers.json` using `validate-skills.py --descriptions`): confirm the
skill wins its own prompts and doesn't steal a neighbour's. User-invoked skills
carry no description reach, so this step doesn't apply to them.
