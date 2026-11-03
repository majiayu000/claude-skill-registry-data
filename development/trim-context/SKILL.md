---
name: trim-context
description: Audit and reduce always-on token costs in the project's instruction files. Invoke manually after completing any plan.
disable-model-invocation: true
---

# Trim Context Agent

## Trigger
Invoked manually after completing any plan: `/trim-context`.

## Process

Audit and reduce always-on token costs.

## What to audit

### 1. AGENTS.md (target: ≤50 lines)
Read `AGENTS.md` (or `CLAUDE.md` on the pre-AGENTS.md convention) and flag any content that violates these rules:

| Keep | Remove |
|---|---|
| Build commands + simulator name | Anything already in `.claude/skills/` |
| Layer rules (enforced in code decisions) | Model/service tables (readable from source) |
| Non-obvious domain constraints | Navigation structure (visible in source) |
| Test framework (import Testing, not XCTest) | ASCII diagrams |
| File inclusion note (PBXFileSystemSynchronizedRootGroup) | Verbose descriptions of obvious patterns |

If AGENTS.md exceeds 50 lines or contains removable content, edit it in place and report what was cut.

### 2. Memory index (~/.claude/projects/.../memory/MEMORY.md)
Read the index and each linked file. Flag entries that are:
- Stale (reference things that no longer exist or have changed)
- Redundant with current project state
- No longer actionable

Remove stale files and their index entries. Report what was removed.

### 3. Settings.json allow list (target: broad patterns only)
Read `.claude/settings.json`. Flag any `Bash(...)` entries that are:
- Specific file paths — replace with a broad `Bash(git -C <project path> *)` pattern
- Pointing to paths that no longer exist
- Duplicated by an existing broad pattern

Edit in place, report changes.

### 4. Skill files (~/.claude/skills/)
Read each skill file. Flag content that is:
- Outdated (wrong simulator name, wrong paths, obsolete commands)
- Duplicated verbatim in AGENTS.md/CLAUDE.md or a command file

Report findings. Only edit skills if clearly outdated — skills load on-demand so verbosity matters less than AGENTS.md/CLAUDE.md.

### 5. Runtime read/tool-output waste (diagnostic only, no proxy required)
If `headroom` is installed (`command -v headroom`), run:
```bash
headroom audit-reads --path ~/.claude/projects/"$(pwd | sed 's/[^A-Za-z0-9]/-/g')" --format json
```
`--path` scopes it to this project only — its default with no `--path` is `~/.claude/projects`, every tracked project's transcripts combined, not this one. The transcript directory's name is this project's absolute path with every non-alphanumeric character (not just `/`) replaced by `-`; compute it with the `sed` command above rather than by hand — a path containing a `.`, space, or other punctuation (e.g. `akshaypimprikar.dev`, a folder name with parens or commas) transforms those characters too, not only slashes. This assumes the session was started from the project root: if your sessions launch from a parent directory, derive the path from that launch directory instead, because that is where the live transcripts land. It streams the scoped transcripts read-only and sizes addressable waste by category (identical repeats, stale reads, line-number scaffolding) as structured fields (`dedup_identical_bytes`, `stale_bytes`, `linenum_overhead_bytes`, etc.) — read those directly rather than parsing text output. This is a diagnostic, not a compression layer: it doesn't touch anything, it just tells you where the waste actually is.

Report the top category by byte share for this run. `headroom` doesn't persist run history, and this command doesn't save one either, so there's no "last run" to compare against — report the current numbers as a point-in-time reading, not a trend. If a category is a large share of the total, that's a *behavioral* signal, not a config fix — flag it in prose (e.g. "a file was re-read N times this session where the content hadn't changed — read once and hold it in context instead") rather than editing anything automatically; this section never changes files, unlike sections 1–4.

If `headroom` isn't installed, or `audit-reads` exits non-zero or returns malformed output, report that as section 5's outcome ("headroom not installed" / "audit-reads failed, skipped") rather than omitting a line for it — this section is optional to adopt, but still reports like every other section below.

## Output
For each section, including section 5: what was found, what was changed (or "no changes needed").
End with the new line count for AGENTS.md/CLAUDE.md.

## Rules
- Do not remove content that is genuinely useful and not available elsewhere
- Do not add new content — this is a reduction pass only
- Commit any changes to AGENTS.md/CLAUDE.md and settings.json with message `chore: trim context after <plan-name>`

## Done when
AGENTS.md/CLAUDE.md is ≤50 lines, stale memory entries removed, settings.json allow list tightened, and changes committed.
