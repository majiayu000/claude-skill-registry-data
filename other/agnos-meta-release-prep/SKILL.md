---
name: agnos-meta-release-prep
description: "AGNOS maintainer skill. Prepares a release of this repository before agnos-meta-release: checks the working tree and the index, syncs the documents with agnos-meta-docs-sync, shows the diff, the changelog's unreleased entries and a proposed SemVer 2.0.0 version, records the version the maintainer approves and commits it, then states the steps left. USE FOR: before rehearsing a release to publish. It publishes nothing: no merge, no tag, no push."
argument-hint: "(no arguments)"
---

<!-- FTR-PLG-005; RQ-PLG-027 to RQ-PLG-030, RQ-PLG-032 / ADR-PLG-005 (DEC-PLG-022, DEC-PLG-023, DEC-PLG-025) -->
# AGNOS Release Preparation

Canonical procedure, shared by GitHub Copilot (`.github/skills/agnos-meta-release-prep/`) and Claude Code
(`.claude/skills/agnos-meta-release-prep/`, which points here). It is a **maintainer tool**, not delivered. The script does
what needs no model; this file orders it around what needs an agent or a person. Run every command from the repository root.

## Procedure

1. **Check.** Run:

   ```
   python .github/skills/agnos-meta-release-prep/scripts/release_prep.py check
   ```

   - Exit `1`: STOP. Give the maintainer the `changed:` lines or the duplicate IDs printed; nothing was edited.
   - Exit `0`: give the maintainer the `open:` lines (tasks not Done) and ask whether to continue with them open.
2. **Sync the documents.** Run the `agnos-meta-docs-sync` sub-agent and wait for it. It edits `CHANGELOG.md`, `AGENTS.md`,
   `CLAUDE.md` and the user's guide, and never commits.
3. **Review.** Run:

   ```
   python .github/skills/agnos-meta-release-prep/scripts/release_prep.py review
   ```

   Show the maintainer its output as printed: the changed files (`unexpected` names one outside docs-sync's four), the diff, the
   `## [Unreleased]` content, `current:` and `proposed:`. If it says `nothing to release`, STOP: nothing is to be prepared.
4. **Approval.** Ask the maintainer with the user-question tool (`askQuestion` on GitHub Copilot, `AskUserQuestion` on Claude
   Code) whether they approve the diff, and which version: the proposed one first, or another they give.
   If they do not approve, STOP and commit nothing: the working tree stays as docs-sync left it.
5. **Record the version.** Run, with the approved version:

   ```
   python .github/skills/agnos-meta-release-prep/scripts/release_prep.py set-version <X.Y.Z>
   ```

   It writes `VERSION.txt` and renames `## [Unreleased]` to `## [<X.Y.Z>]`. Exit `1` (not SemVer 2.0.0, not above the current
   version, no `[Unreleased]`): nothing changed; give the reason and ask again.
6. **Commit.** Invoke the `agnos-git-workflow` skill's `commit-task` sub-command with the task the maintainer names, so that
   the documents and the version are one commit. Read its short SHA with `git rev-parse --short HEAD`.

## Next steps

Print these four steps, in this order, with the short SHA of step 6, and run none of them: publishing is the maintainer's.

1. `agnos-meta-release` from `<sha>` into an empty folder outside the repository.
2. `agnos-meta-plugin-proof` on that folder.
3. Regenerate the marketplace folder (`agnos-marketplace`) from the proved output.
4. The merge, tag and push, by the maintainer.

## Tests

`python -m unittest discover -s .github/skills/agnos-meta-release-prep/tests -v` from the repository root.
