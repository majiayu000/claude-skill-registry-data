---
name: skill-hygiene
description: "Audit and maintain a skill bundle so every bundled asset is reachable from SKILL.md or its directory's INDEX.md. Use when a skill has accumulated content (references, examples, schemas, scripts, templates, agents, diagrams) that may not be discoverable, when adding new files to a skill, or before publishing a skill bundle. NOT for creating skills from scratch (that's skill-architect) or grading skill quality (that's skill-grader)."
license: Apache-2.0
allowed-tools: Read,Write,Edit,Bash,Grep,Glob
metadata:
  category: Productivity & Meta
  tags: [skill, hygiene, drift, progressive-disclosure, audit, maintenance]
  pairs-with: [skill-architect, skill-grader, skill-creator]
  provenance:
    kind: first-party
    owners: [port-daddy]
  authorship:
    maintainers: [port-daddy]
---

# Skill Hygiene

A skill bundle is a tree of files. Only the ones SKILL.md (or a SKILL-loaded
INDEX.md) names are actually discoverable by an agent at runtime. Files that
are not named are dead weight: they cost disk, they look like they're working,
and they're not.

This skill is for keeping a bundle's reachable surface in sync with what's on
disk — and for catching the drift before it ships.

## NOT For

- Creating new skills. That's `skill-architect`.
- Grading skill quality (clarity, expertise level, examples). That's `skill-grader`.
- Generic doc linting unrelated to skill-bundle structure.
- Fixing prose. The auditor checks reachability, not whether the prose is good.

## When To Use

- A skill has grown several subdirectories and you suspect not all of them are referenced from SKILL.md.
- You added a new file to an existing skill and want to confirm it's discoverable.
- You inherited a skill from another author and don't trust the surface area.
- You're about to publish or mirror a skill and want a clean reachability check first.
- A new INDEX.md was written by hand and may have drifted from the directory.

## The Drift Modes

A skill bundle drifts in four ways. The auditor catches all four. A fifth
issue type — broken links — surfaces typos and renames before they ship.

### 1. Orphaned files

A doc file exists in a subdirectory but no SKILL.md or INDEX.md mentions it.
Agents loading the skill at runtime will never find it. Asset files (`.svg`,
`.png`, fonts, etc.) are not audited as orphans — they're consumed by docs
that reference them, not loaded directly.

### 2. INDEX drift

An `INDEX.md` lists entries that don't match the directory:
- **missing_from_index**: doc files on disk the index doesn't mention (the
  orphan's mirror — same problem, viewed from the index side).
- **ghost_entries**: files in the index's table-row first column that aren't
  on disk anywhere in the bundle. Filename was changed or deleted; the
  index wasn't updated.

### 3. Broken links

A markdown link `[text](path)` or reference-style link from SKILL.md or any
INDEX.md points at a file that doesn't exist at the resolved path. The
auditor reports the source, target, and fuzzy-matched suggestions ("did you
mean: `respawn.md`?") for likely typos.

### 4. Missing INDEX

A subdirectory has multiple bundled doc files but no `INDEX.md`. Two
severities:

- **Failure**: at least one file in the directory is not named in SKILL.md.
  Without an INDEX hub, those files are unreachable.
- **Warning**: every file is named directly in SKILL.md. The skill works,
  but adding an INDEX would let SKILL.md route by trigger instead of listing
  files individually.

## The Audit Procedure

```bash
python3 skills/skill-hygiene/scripts/audit_skill_bundle.py <path-to-skill-bundle>
```

The script:

1. Walks the bundle, treating each top-level subdirectory as an audit unit.
2. Parses markdown links (inline `[text](path)`, reference-style, backtick
   code spans) from SKILL.md and every INDEX.md.
3. Resolves each link relative to its containing file. Classifies as
   `ok` / `broken` / `external` / `anchor` / `outside`.
4. Builds a "referenced" set from successfully resolved links plus basenames
   mentioned in prose anywhere reachable.
5. Any doc file not in that set → **orphan** (assets are exempt).
6. Any link with status `broken` → **broken_link** with typo suggestions.
7. For each existing INDEX.md, checks every same-directory doc file appears
   in the index → flags **missing_from_index**.
8. For each existing INDEX.md, scans pipe-table first-column entries for
   filenames not on disk anywhere → flags **ghost_entries**.
9. For each subdirectory with >1 doc file but no INDEX.md → flags
   **missing_index** (failure or warning depending on whether SKILL.md
   already names every file in the directory).

Exit code is `0` if clean, `1` if any failing issue, `2` if the bundle is
malformed (no SKILL.md). Use `--json` for CI integration, `--quiet` to set
exit code only.

## Fixing Drift

| Drift | Fix |
|---|---|
| Orphan in a directory that has an INDEX.md | Add the file to INDEX.md with a one-line "when to load" hook. |
| Orphan in a directory that has no INDEX.md | Either create an INDEX.md (preferred when the directory will keep growing) or mention the file directly in SKILL.md. |
| Missing-from-index | Same fix as orphan in directory with INDEX.md. |
| Ghost entry | Either the file should exist (restore it) or the entry is stale (delete the row). Check `git log` for the filename to decide. |
| Missing INDEX | Create one. Use the table format shown in `references/progressive-disclosure.md`. |

## Doctrine

- **SKILL.md is the entry point**, not the encyclopedia. Don't inline what
  belongs in a leaf doc; instead, point at the right INDEX.md with a one-line
  trigger ("when X, open Y").
- **Every subdirectory with more than one file needs an INDEX.md**. The cost
  is one short table; the benefit is discoverability.
- **An INDEX.md row is a contract**: "this file exists, here's when to load
  it." If the file moves, the contract breaks. Run the auditor to catch it.
- **Cross-references are fine**. An INDEX.md can mention a file in another
  directory (e.g. `agents/INDEX.md` mentioning `subagent-fork-template.yaml`).
  The auditor only flags ghost entries when the filename exists nowhere in
  the bundle.

See `references/progressive-disclosure.md` for the full SKILL.md → INDEX.md →
leaf pattern, and `references/drift-prevention.md` for hooking the auditor
into pre-commit and CI.

## Pairing With Other Skills

- After `skill-architect` produces a fresh bundle, run skill-hygiene to confirm
  every file the architect emitted is actually reachable.
- After `skill-grader` flags "this skill could use more examples" and you add
  them, run skill-hygiene to confirm the new examples are surfaced.
- Before mirroring a skill into other tool roots (`.codex/`, `.claude/`,
  `.gemini/extensions/`), audit the canonical bundle first — drift mirrors too.

## Self-Check

```bash
python3 skills/skill-hygiene/scripts/audit_skill_bundle.py skills/skill-hygiene
```

The hygiene skill audits itself. It should always pass; if it doesn't, fix
its own surface area before fixing anyone else's.

## Installing The Pre-Commit Guard

The pre-commit hook is the highest-leverage drift catcher: it runs the
auditor on every skill bundle touched by a commit and blocks the commit if
any bundle fails. Install once per checkout:

```bash
bash skills/skill-hygiene/scripts/install_hooks.sh
```

The installer is idempotent. It writes to the shared common-hooks dir
(`git rev-parse --git-common-dir`), so linked git worktrees pick it up
automatically. Bypass once with `git commit --no-verify` when the drift is
intentional and a follow-up fix is queued.

## Healing Drift In Bulk

For libraries with many drifted skills, see `scripts/heal_skill_bundle.py`.
It reads the audit findings, packages SKILL.md + every subdirectory's
content into a prompt, and dispatches to `claude` (haiku for one-orphan
quick wins, sonnet for content integration). The model emits a JSON write
plan; the script applies it and re-runs the auditor to verify. Use
`--apply` to mutate; default is dry-run.

**Healer auth requirements.** `heal_skill_bundle.py` shells out to the
`claude` CLI. That binary must be installed and authed on the operator's
machine — there's no API-key-only fallback today. Concretely: CI cannot
run the healer. CI catches drift via the auditor; the operator fixes drift
locally with the healer, commits, and pushes. If a contributor doesn't
have a working `claude` CLI, they hand-fix the failing bundle or wait for
someone with credits to run the healer.

```bash
python3 skills/skill-hygiene/scripts/heal_skill_bundle.py skills/<name> --model sonnet --apply
```

Mis-paired content (frontmatter says X, content is about Y) is out of
scope for the healer — that needs human review.
