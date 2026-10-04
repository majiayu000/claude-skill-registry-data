---
name: pm-changelog
description: Generate or update CHANGELOG.md from git history — group commits by Conventional-Commits prefix (feat/fix/refactor/docs/test/chore/breaking), translate raw subject lines into human-readable entries, link to PRs/issues, prepend a new versioned section. Reads the range from `$ARGUMENTS` (since tag/SHA), the last CHANGELOG entry, or last tag fallback. Distinct from `pm-status-report` (now-state outward report) and `pm-retrospective` (reflective, not log-driven). Loads when the operator says "changelog", "release notes", "what shipped", "summarize commits since X", "update CHANGELOG".
argument-hint: [since: tag, commit hash, or date]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# pm-changelog

The git-log-to-CHANGELOG translation skill. Reads commits in a range, groups by Conventional-Commits type, rewrites raw subjects into human-readable entries, links PRs/issues, and prepends a new versioned section to `CHANGELOG.md`. Distinct from `pm-status-report` (cadence-driven outward state) and `pm-retrospective` (reflective look-back, not log-driven).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "changelog", "release notes", "what shipped", "summarize commits since X", "update CHANGELOG", "draft the release notes".
- **Pre-release context**: about to tag a version; CHANGELOG needs to be brought up to that tag.
- **Sister-project ask**: a fleet/sister project (openfleet, dspd, nnrt) is releasing — generate their changelog from their git history with the same skill.

Do NOT load when:

- Operator wants a status report, not a log dump — load `pm-status-report`.
- Operator wants the why behind decisions — load `pm-retrospective` or read `wiki/decisions/`.
- Operator wants the next-up plan — load `pm-plan`.
- Operator wants per-task narrative — that's `wiki/backlog/tasks/T*.md`, not changelog.

## Operations

This skill has 3 named operations. Execute in order.

### Operation 1: Determine the range and gather raw commits

**Trigger**: skill loaded; operator may have provided `$ARGUMENTS` (since tag/SHA/date).

**Process**:

1. Resolve the range start:
   - If `$ARGUMENTS` provided: use it (`v1.2.3`, SHA, or `2026-04-15`).
   - Else: read first version header in `CHANGELOG.md` (regex `^##\s*\[?\d`), use the date or referenced tag.
   - Else: most recent git tag (`git describe --tags --abbrev=0`).
   - Else: last 30 days (`--since="30 days ago"`).
2. Pull commits in the range:
   ```bash
   git log <range>..HEAD --no-merges --pretty="%H%x09%s%x09%b" > /tmp/commits.tsv
   wc -l /tmp/commits.tsv   # commit count
   ```
3. Identify the version-to-write:
   - If operator named a version (`$ARGUMENTS=v1.3.0`): use it.
   - Else: derive from semver based on prefixes seen (`feat:` → minor; `fix:` → patch; `BREAKING CHANGE` or `!` → major).
   - Else: leave as `Unreleased` and let operator decide.
4. Detect linked artifacts:
   - PR refs in commit body: `(#123)` patterns.
   - Issue refs: `closes #X`, `fixes #Y`, `T<NNN>` task IDs (AICP/fleet convention).
5. Sanity-check the range:
   - 0 commits: nothing to write — tell operator the range is empty.
   - >200 commits: range is too wide — confirm with operator before writing 100+ entries.
   - Merge commits stripped (`--no-merges`) — confirm this matches operator's preferred style.

**Quality bar (Operation 1 done when)**:

- [ ] Range start identified with explicit source (operator arg / CHANGELOG header / tag / date fallback).
- [ ] Commit list captured with hashes, subjects, bodies.
- [ ] Version-to-write decided (specific version OR `Unreleased`).
- [ ] Linked PRs/issues/tasks extracted from commit bodies.
- [ ] Range size acknowledged: 0 → bail; large → confirm.

### Operation 2: Group, translate, and author the new section

**Trigger**: Operation 1 commit set assembled.

**Process**:

1. Group by Conventional-Commits type. Standard buckets:
   - **Breaking changes** (`!:` suffix, `BREAKING CHANGE` in body) — always first.
   - **Features** (`feat:`)
   - **Fixes** (`fix:`)
   - **Performance** (`perf:`)
   - **Refactor** (`refactor:`) — include only if user-visible or migration-relevant.
   - **Docs** (`docs:`) — include only structural docs (architecture, public API), not internal notes.
   - **Tests / Chores / Style** — usually omitted from user-facing changelog; include in operator-internal changelog if applicable.
2. Translate each subject line into a human-readable entry:
   - ❌ `refactor: update benchmark model argument from hermes to qwen3-8b for consistency`
   - ✅ `Benchmark target now uses qwen3-8b (formerly hermes); update local CI scripts that pinned the model name.`
   - Goal: a reader who didn't write the code understands what changed and what they need to do.
3. Preserve facts; rewrite only narration:
   - Don't merge two distinct commits into one entry just because subjects look similar.
   - Don't drop a commit because the subject is terse — read the body for context.
4. Author the new CHANGELOG section in this shape (Keep-A-Changelog style):
   ```markdown
   ## [<version>] — <YYYY-MM-DD>

   ### Breaking changes
   - <entry>. (#PR or T<NNN> ref)

   ### Added
   - <entry>. (ref)

   ### Fixed
   - <entry>. (ref)

   ### Changed
   - <entry>. (ref)

   ### Security
   - <entry>. (ref)
   ```
   Empty subsections are omitted.
5. Cross-link to deeper sources where they exist:
   - Architecture changes → `docs/architecture/<area>.md`
   - Decisions → `wiki/decisions/<file>.md`
   - Incidents that drove fixes → `docs/incidents/INC-*.md`

**Quality bar (Operation 2 done when)**:

- [ ] Commits grouped by Conventional-Commits type with correct precedence (Breaking first).
- [ ] Each entry rewritten human-readably; no raw `feat: blah` lines.
- [ ] No commit dropped silently — if it didn't make the changelog (chore/test/style), explicit category exclusion noted.
- [ ] PR/issue/task refs preserved per entry.
- [ ] Cross-links to architecture/decisions/incidents added where they exist.

### Operation 3: Prepend to CHANGELOG.md and verify

**Trigger**: Operation 2 new section authored.

**Process**:

1. Locate (or create) `CHANGELOG.md`:
   - If exists: read first 20 lines to find insertion point (after the header / between `## [Unreleased]` and the first prior version).
   - If not exists: create with Keep-A-Changelog skeleton:
     ```markdown
     # Changelog

     All notable changes to this project will be documented in this file.

     The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
     and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
     ```
2. Insert the new section in chronological order (newest at top), beneath the header but above any existing version sections.
3. If `## [Unreleased]` had pending entries: merge them into the new released version's appropriate buckets (don't lose them).
4. Validate:
   - Markdown lints clean (`tools/lint.py CHANGELOG.md` if applicable, or visual check).
   - All version dates are ISO-8601.
   - Version numbers are semver-valid.
5. Optional cross-doc updates:
   - Bump version references in `pyproject.toml` / `package.json` if releasing.
   - Add a `wiki/log/` entry for the release (per second-brain convention).
6. Hand off the next step to operator:
   - "Changelog updated. Ready for `git tag <version>` and `ops-deploy` if releasing now, OR review-and-edit if you want to tweak."

**Quality bar (Operation 3 done when)**:

- [ ] CHANGELOG.md exists with Keep-A-Changelog structure.
- [ ] New section inserted at correct position (newest-on-top).
- [ ] No unreleased entries lost (merged into release if appropriate).
- [ ] Dates ISO-8601, versions semver-valid.
- [ ] Operator told the immediate next step (tag / deploy / review).

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Treating raw commit subjects as entries

Commit subject reads `fix: F841 in stream_batch_sampling`. Skill copies it into the changelog. Reader has no idea what F841 is or whether they need to do anything. The changelog is technically populated but functionally useless.

**The rule**: Operation 2 step 2 rewrites every entry. The test is: a reader who didn't write the code understands the change and any action they need to take. If a commit is too internal to translate that way, demote it to a chore/internal section or omit it.

### Gotcha 2: Range silently includes the wrong commits

Operator says "changelog since v1.2.0". Skill resolves `v1.2.0` to the tag — but there's also a `v1.2.0-rc1` tag that `git describe` would have used as the more recent starting point. The range either over-includes (back to rc1's predecessor) or under-includes (only post-rc1 commits, missing what was in v1.2.0 itself).

**The rule**: Operation 1 step 1 — when the range start is ambiguous, surface to operator. Resolve `v1.2.0` to its full SHA (`git rev-parse v1.2.0`), show the operator the resolved start commit, and confirm before pulling the commit list. Don't silently pick a tag pattern.

### Gotcha 3: Merging distinct commits into one entry

Two commits both touch the routing logic — one fixes a fail-fast bug, the other adds a new band. Skill merges both into "router improvements" because the subjects rhyme. Reader doesn't see the bug fix or the new band specifically.

**The rule**: Operation 2 step 3 preserves distinct commits as distinct entries. Merging is allowed only when commits genuinely describe the same change broken across N commits (e.g., "feat: add X" + "fix: typo in feat: add X" — the typo commit folds into the feature). Different topics → different entries.

### Gotcha 4: Refactor flood drowning user-visible changes

Two months of refactoring produces 80 `refactor:` commits. Skill dumps all 80 into the changelog. Real users skim past 80 lines of refactor-noise looking for the 3 features and 2 fixes that actually affect them.

**The rule**: Operation 2 step 1 — `refactor:` entries are included in user-facing changelog ONLY if user-visible (API change, performance change, observable behavior shift). Internal refactors that are pure code-shape changes go into an "Internal" section or get omitted from the user-facing changelog. The user changelog summarizes 80 refactors as one line: "Internal refactoring across X areas. No user-visible changes."

### Gotcha 5: Losing pending Unreleased entries on release

`## [Unreleased]` had three entries that operator added by hand last month. Skill writes a new `## [v1.3.0]` section ABOVE Unreleased — but the three pending entries are now stranded under Unreleased and not in the released version where they belong. Reader doesn't see them as part of v1.3.0.

**The rule**: Operation 3 step 3 — if `## [Unreleased]` exists with content, MERGE its content into the new release section before writing. Then the empty `## [Unreleased]` shell is preserved (or recreated) for the next cycle. Don't strand entries that were added in advance.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP commit history follows Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, etc.); the recent log shows mostly `refactor:` and `feat:` commits. Task IDs use the `T<NNN>` convention. There is no per-tag CHANGELOG yet for AICP itself (mission-driven phase work has been the unit of release rather than versioned tags) — this skill helps add one when the project moves to versioned releases. Sister projects (openfleet, dspd, nnrt) may already have CHANGELOGs; the skill works there with their tag/version conventions.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| pm-status-report | Cadence-driven outward state report | Now-state with metrics; this skill is log-driven release notes |
| pm-retrospective | Reflective look-back on a slice | Reflective; this skill is log-driven |
| pm-handoff | Cross-session continuity context | Continuity; this skill is release-facing |
| pm-assess | Internal project state synthesis | Internal; this skill is outward release notes |
| ops-deploy | Forward action shipping the release | Action; this skill is the documentation of the release |
| evolve-api-version | Coordinating an API version bump | Coordinated change; this skill is the changelog OUTPUT of such a change |
