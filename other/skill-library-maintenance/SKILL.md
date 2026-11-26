---
name: skill-library-maintenance
description: "Audit, repair and merge an installed skill library."
version: 1.0.0
author: ponti-studios
license: MIT
metadata:
  author: ponti-studios
  version: "1.1.0"
  category: Engineering
  tags: [skills, library, provenance, merge, audit]
  hermes:
    tags: [skills, library, provenance, merge, audit]
    related_skills: []
---

# Skill library maintenance

Operating an installed library rather than authoring one file: proving every skill has provenance, folding
installed-only edits back into source, merging two skills into one, and reconciling the tiers of a merged
skill. Frontmatter, size and structure rules for a single SKILL.md live in the repo's AGENTS.md
and are enforced by `scripts/validate_skills.py`; this skill is the library-wide work.

## When to Use

- "what is in my skills directory", "where did this skill come from", "why is this skill out of date"
- a library that installs from git (`npx skills add <repo> --skill <name> -g`) feels stale or duplicates itself
- two skills enforce the same standards and should become one
- a merged or imported skill needs its laws checked against its references
- removing a retired skill from every agent on this Mac (Claude, Codex, Gemini, the shared
  store) — that is a multi-store delete, not a library edit; the store inventory and the sweep live in
  `app-configuration` under "Removing one"
- Don't use for: writing one new skill, or frontmatter details — see AGENTS.md

## Layout to reason about

Three layers, and every fault is a disagreement between two of them:

| Layer  | Path                               | What it proves                                        |
| ------ | ---------------------------------- | ----------------------------------------------------- |
| source | the library repo, `skills/<name>/` | git history, the only copy worth editing              |
| store  | `~/.agents/skills/<name>`          | what the loader actually reads; overwritten on update |
| loader | `<agent-home>/skills/<name>`          | symlink the installer creates; never hand-make it     |

`~/.agents/.skill-lock.json` is the only provenance record. A skill absent from it still loads and still
looks installed, while `skills list` prints `Source: local` — which means "no record", not "installed from
here".

## Procedure

### 1. Audit before touching anything

Run the library's own audit (`node scripts/skills_audit.mjs` in the kernel repo) and read four numbers:
unprovenanced installs, stale lock entries, name collisions, drift against the repo. Exit code is non-zero
on any finding, so it works as a gate; `--quiet` prints only when something is wrong, which is what a
weekly launchd job should run.

The drift check compares **logical** trees, so a vendored `references -> ../../data` symlink is not reported
as drift. A naive `diff -rq` reports that case as dozens of "Only in" lines and a reinstall never clears
it — compare the link's target instead.

### 2. Repair drift in the direction it exists

The store drifts both ways:

- **Source ahead** (repo edited, store stale): reinstall.
- **Store ahead** (an agent edited `~/.agents/skills/<name>` instead of the source): fold the change back
  into the repo, commit, push, _then_ reinstall. A blind reinstall silently deletes it.

Do the same when two copies of a skill exist (a loose directory plus an installed entry): diff first, and
merge rather than choose — the hand-maintained copy is often the richer one. Delete the loose copy last,
and prove the result with `diff -rq` plus a zero on the collision sweep.

### 3. Merge two skills into one

Merge when two skills enforce the same person's standards, or cover one class of task from two angles: an
agent then loads one thing instead of guessing which, and the pair can no longer drift apart.

1. **Pick the surviving name, sort what is unique.** Each rule in the loser already exists, restates one it
   overlaps (merge the wording into that rule), or is new (add it). In one real merge, ten of fourteen "top
   rules" were restatements.
2. **Keep the winner's frontmatter shape**, bump the version, carry every `references/` file across
   unchanged — they were already the depth tier behind both skills.
3. **Renumber and repair cross-references.** Rules get cited by number ("rule 32", "law 46") and a merge
   moves them. Build an old→new map, rewrite through it, then grep the file for `law \d+` / `rule \d+` and
   assert every target exists and still means the same thing.
4. **Find every pointer to the old names before deleting:** `related_skills` in other skills, the catalog
   manifest, the README catalogue, prose notes that say "copied from X". `search_files(pattern='<old1>|<old2>',
   path=<repo>)` must return only the deletion hits.
5. **One catalog entry replaces two**, then the library validator and its test suite, then `git rm -r` the
   old directories, commit, push.
6. **Uninstall, then install.** `npx skills remove -g -s <old> -y` once per name — `-s a,b` exits 0 and
   removes neither — then `npx skills add <repo> --skill <new> -g --yes`, then re-run the audit: zero drift,
   zero collisions.
7. **Run the contradiction pass** (section 4 below) before calling it done.

### 4. Contradiction pass on the merged skill

A skill with `SKILL.md` laws plus `references/` depth states the same rule twice, and the copies drift
after a merge or an import. Read the laws against their references and fix each disagreement by carrying
the reference's **qualifier** up into the law — never by softening the law into vagueness.

Cheap sweep: grep `never|always|only|nothing` in the laws and `except|unless|is fine|exempt|allowed` in the
references; every disagreeing pair needs a decision written into the law. Real examples of the pattern: a
law banning all ternaries against a reference allowing one short two-way; a law demanding red for real
failures against a reference where a particular surface reports failure by shape; a law claiming "apps
never touch a database" against a native-package architecture where on-device decisions are local.

Also state provenance honestly: which laws are the user's literal words, which were inferred from how they
review. A document that calls everything "law" when a third of it was inferred is a lie the next session
will cite as authority.

### 5. Keep the tiers apart when the user respecifies scope

"This skill should be about X, not Y" is a scoping instruction, not a deletion: move the Y laws into the
reference that owns Y, delete nothing, and say in the intro where that material now lives. Laws are one-line
rules a session applies from memory; anything about process — branches, PRs, merge gates, tickets, voice —
belongs in a reference, not in the laws that are meant to be craft.

### 6. Verify a surviving law against the live system

A law can be consistent with every reference, well worded, and still be false about the system it
describes. The failure mode is a law that states a protocol nobody implemented: it survives every
contradiction pass because nothing in the skill disagrees with it.

- **Count the objects before keeping the sentence.** A law saying every project carries a routing block,
  every ticket a template, or every repo a config key is testable in one command: query the real store and
  report `n of m`. Three of seventeen is a description of an intention, not a law.
- **Grep for the keys it names.** If a rule cites a `github:`/`local:` block or a `gitBranchName` field,
  search the codebase for a reader. A documented field with no reader is the same defect as no field.
- **Delete that law; do not correct it.** An agent that follows it looks for an artefact that does not
  exist, and the outcome — nothing picked up, nothing claimed — is indistinguishable from a healthy quiet
  system. The behaviour that _is_ implemented is the source of truth, wherever it actually lives.
- **Record the reason in the commit, not in the file.** A skill should read as rules, not as a changelog:
  the diff explains why a law went, and a future session should never meet "(removed because…)" mid-law.
- **A law that restates an implemented, tested check is a weaker duplicate of that check.** If deleting the
  sentence loses nothing because a gate catches the mistake, the gate is the lesson.

## Pitfalls

- **An installed copy is not where a law is edited.** `~/.agents/skills/<name>` (and the `<agent-home>` symlink
  through it) is overwritten by the next `skills add`/`update`; a scope change, a deletion or a fix belongs
  in the source repo, committed and pushed, then reinstalled. Editing the store looks like it worked until
  the next machine updates.
- **`local` is not a location.** It means the lock has no entry, so `skills update` skips the skill forever
  and nothing looks broken. Diff the store directory names against the lock keys.
- **The audit earns its keep on live defects.** Expect it to find a forward edit or a stale install on its
  first run against a real library; treat the finding as work, not as a false positive to be suppressed.
- **Reinstalling is not the same as reconciling.** `skills add` does not delete files the newer source
  dropped, and it cannot fix a materialised symlink; if the audit still reports `extra: …` after a reinstall,
  remove the skill first and add it again.
- **A merge is not finished until the pointers are gone.** A deleted skill name left in another skill's
  `related_skills` or the README is a validator failure at best and a dead link in a future session at worst.
- **Do not let the audit live only in someone's shell history.** Commit it to the library repo, point SKILL.md
  of the authoring skill at it, and schedule it weekly — a library that silently stops being updatable is
  exactly the failure nobody notices.

## Verification

- audit exits 0, and its four counters are: unprovenanced 0, stale 0, collisions 0, drift 0
- `diff -rq <repo>/skills/<name> ~/.agents/skills/<name>` clean for every skill touched
- library validator reports catalog parity, and the test suite passes
- for a merge: `search_files` for both old names returns nothing but the deletion commits
