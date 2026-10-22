---
name: review-skill-links
description: >-
  Repo-only review of how this devkit's skills and agents fit together after a skill is
  added, renamed, split, or substantially changed: runs the mechanical checks, then reads
  for routing gaps, conflicting advice, duplicated rules, and missing two-way pointers
  between related skills. Use when the user asks to review cross-references, check skill
  wiring, or make sure everything still fits after a skill change. Not shipped with the
  plugin.
---

# Review skill links

The scripts catch what can be matched by text. This review catches what needs reading:
a skill nobody routes to in the one place it matters, two skills giving opposite advice,
the same rule in two places. Follow the "Skill boundary discipline" section of `CLAUDE.md`
throughout.

## 1. Run the checks

```bash
scripts/check-skill-refs.sh
scripts/check-skill-wiring.sh
scripts/check-version.sh
scripts/check-frontmatter.sh
scripts/check-skill-callers.sh
scripts/check-evals.sh
```

Fix or report every failure before reading further. A failure here is a finding, not
background.

## 2. Pick the scope

Find what changed since the main branch:

```bash
git diff --name-only "$(git merge-base HEAD origin/main)" -- plugins/
```

If the user names skills, start there. Otherwise start with the changed and new skills.
Either way, read each one's frontmatter `description` and section headings, then find its
neighbors: skills that cover nearby ground (`umbraco-backoffice-conventions` next to
`umbraco-backoffice-ux`, `umbraco-performance` next to `umbraco-extensibility`, and so on).

## 3. Read for these problems

For each skill in scope and each neighbor:

- **Routing gaps.** Every list that routes work to skills should name the skill when its
  territory comes up: `agents/builder.md`, `agents/reviewer.md`, `feature-design`'s skill
  list, `quick-fix` step 3, `feature-build`'s builder brief, `investigate-bug`'s suspects,
  and the README tables. Check each list against the skill's description, not just whether
  the name appears somewhere.
- **Conflicting advice.** Two skills telling the reader to do opposite things in the same
  situation. Read the rules on shared topics (caching, background work, handlers, file
  access, versioning) side by side.
- **Duplicated rules.** The same rule stated in two skills. Keep it in the skill whose
  description it fits; replace the other copy with a one-line pointer.
- **One-way pointers.** If skill A says "for X, see B", check whether B's matching section
  needs "for Y, see A". Not every pointer needs a return one; add it when a reader of B
  would otherwise miss A.
- **Stale facts after a move.** A rule that moved to a new skill but is still described
  in its old place, or a catalogue entry that now contradicts the new skill.
- **Caller checks.** A skill that describes its caller or acts differently depending on
  which skill started it, in wording the script didn't catch. Per `CLAUDE.md`'s "Skills
  calling skills", the fix is an input (an argument, a file section, a value passed in);
  the standard Hand off line is the one exception.
- **Scope drift.** A section that no longer fits its skill's `description`.

## 4. Fix and report

- Make the fixes on a branch, following `CLAUDE.md`'s committing rules. Ask before
  committing.
- Bump the patch version if any shipped file changed, then rerun step 1.
- Report what you fixed, one line each, and what you checked and left alone.
