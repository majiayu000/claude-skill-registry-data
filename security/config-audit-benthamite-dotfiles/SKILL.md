---
name: config-audit
description: Audit agent configuration for redundancy, conflicts, dead weight, staleness, and instruction drift across CLAUDE.md or AGENTS.md, skills, memory, hooks, settings, and docs.
---

# Audit agent configuration

Perform a comprehensive audit of all agent instruction sources to find redundancy, conflicts, staleness, dead weight, and documentation drift.

## Scope and safety

- Use this for agent configuration audits, not ordinary app config linting, code review, repo architecture review, or general security scans unless the question is specifically about agent instructions or automation behavior.
- Honor the requested subset. A skills-only audit may read governing instructions
  and relevant hooks for context, but does not authorize rewriting unrelated
  settings, memory, or global instructions. When the user asks for full skill
  audits, read procedural bodies and required resources too; the ordinary
  instruction-overlap limits below do not narrow that request.
- Treat settings, MCP configuration, memory, and hook payload examples as potentially sensitive. Read them locally, but do not quote secrets, OAuth tokens, API keys, credential helper output, or unnecessary account identifiers in the report. Redact values and report only the setting names or rule effects needed for the audit.
- If the audit runs inside this dotfiles repo and secret material may be involved, follow the repo secret-handling instructions before inspecting credential-related files.
- If an expected source is missing, unreadable, generated, or intentionally absent, record that explicitly instead of inferring its contents.
- If the user supplied `--accept` or explicitly asked you to apply the cleanup, treat that as confirmation to apply high-confidence, scope-preserving edits after the audit. Otherwise, present the audit and ask before changing files.

## Phase 1: Discovery

Create an inventory first, then read every instruction source in the requested
scope. For each source, record the resolved path, symlink target when relevant,
whether it is tracked, and what role it plays. Use parallel investigation only
when compatible with the user's requested order. For a one-by-one audit,
complete and verify the current item before advancing; parallel help may
independently check that same item.

### Instruction files

- `~/.claude/CLAUDE.md or ~/.codex/AGENTS.md or AGENTS.md` (global instructions — may be a symlink)
- Every `CLAUDE.md or AGENTS.md` in the project directory ancestry (project-level instructions)
- Resolve `@` includes in any CLAUDE.md or AGENTS.md and read the referenced files

### Skills

- Every `SKILL.md` in `~/.claude/skills/ or ~/.codex/skills/` and the project's skill directories
- Distinguish discovery metadata from loaded instructions. Claude's
  `user-invocable: false` hides a skill from direct user invocation; it does
  not preload the body. Check actual loading and invocation policy for each
  runtime before classifying a skill as always-loaded context.
- For user-invocable skills, check only the frontmatter and any top-level rules outside procedural sections — the procedural body is loaded on demand and doesn't compete for attention with CLAUDE.md or AGENTS.md

### Memory

- `MEMORY.md` index and every linked memory file in the project memory directory
- `global or project memory files, when present` (global memory) and its files
- Pay special attention to `type: feedback` memories — these are the most likely to duplicate rules that have since been promoted to CLAUDE.md or AGENTS.md or enforced by hooks

### Hooks

- Read `settings.json` to find all hook definitions
- Read each hook script to understand what it enforces mechanically
- Compare a hook's actual runtime and tool coverage with the instruction.
  Enforcement overlap alone does not prove the instruction is redundant.

### Settings

- `settings.json` and `settings.local.json` for any behavioral configuration
- `tool configuration files` for MCP server definitions (referenced by instructions?)
- Redact sensitive values. The audit needs behavioral meaning, configured paths, and rule effects, not raw credentials.

### Documentation

- Read `claude/README.org or codex/README.org` (if present in the project) — this documents the claude/ subdirectory (skills, hooks, settings) and serves as a cross-reference for the audit
- Flag any discrepancies between README.org and the actual configuration (missing skills, outdated hook descriptions, etc.)

### Third-party skills

- Check `.agents/skills/` or any other non-standard skill locations

## Phase 2: Extraction

For each source, extract every discrete rule, instruction, or preference, while respecting the Phase 1 limits for user-invocable procedural skill bodies. A "rule" is any statement that constrains or directs behavior. Examples:

- "Use sentence case instead of title case" — a rule
- "After editing config.org, tangle with init-build-profile" — a rule
- Step 3 of a 10-step procedure in a release skill — NOT a rule (it's a procedural step, only loaded when that skill runs)

Assign each rule a short ID and note which file it came from.

## Phase 3: Analysis

Evaluate every extracted rule on five criteria. Present the results in a table grouped by source file.

### Criterion 1: Default behavior

"Is this something I already do by default without being told?"

The active agent system prompt and training already establish many behaviors. Instructions that merely restate defaults consume tokens without changing anything. To evaluate this, consider what you would do if the instruction were absent — if the answer is "the same thing," it's dead weight.

**Examples of likely defaults**: don't mix unrelated changes in a commit, use descriptive variable names, don't introduce security vulnerabilities.

**Examples of likely NOT defaults**: commit all changes immediately, use `trash` instead of `rm`, use the most capable available model for subagents. Check the active runtime's instructions; do not assume another model or tool has the same defaults. A predicted default alone is not sufficient evidence to remove a useful user preference.

### Criterion 2: Conflicts

"Does this contradict or conflict with another rule somewhere else in the setup?"

Check for:
- Direct contradictions (one rule says X, another says not-X)
- **Global vs. project CLAUDE.md or AGENTS.md conflicts**: a project file can intentionally narrow or override a global rule (e.g., global says "commit immediately" but a project says "don't commit without PR review"). Flag these and ask whether the override is intentional. If intentional, the project file should say so explicitly. If accidental, one of them needs to change.
- **Project CLAUDE.md or AGENTS.md shadowing**: a project file that restates a global rule with slightly different wording creates ambiguity about which version governs. These are repetition bugs, not conflicts — resolve by removing the project-level copy or adding an explicit "overrides global" note.
- Tension between a blanket prohibition and a skill that needs to do the prohibited thing (e.g., "never kill Emacs" vs. a skill that sends SIGUSR2 with safeguards)
- Instructions that intentionally override system prompt defaults — flag these as intentional overrides, not bugs
- Rules that give different guidance for the same situation depending on which file is loaded

### Criterion 3: Repetition

"Does this repeat something already covered by a different rule or file?"

Check for:
- Exact duplicates across files (same rule, same words)
- Semantic duplicates (different words, same effect)
- Subset rules (rule A says "commit everything immediately"; rule B says "commit skills immediately" — B is a strict subset of A)
- Rules also enforced by a hook; treat these as candidate overlap until runtime
  coverage and the instruction's remaining guidance have been checked

When a rule appears in N places, identify the **canonical location** (usually CLAUDE.md or AGENTS.md or the most general file) and flag the others as duplicates.

### Criterion 4: Reactive one-off fixes

"Does this read like it was added to fix one specific bad output rather than improve outputs overall?"

Telltale signs:
- The rule's `Why` section names a single incident ("missed during the whisperx rewrite")
- The rule bans a specific word or pattern rather than addressing the underlying behavior ("never say 'should'")
- The rule is a `type: feedback` memory whose content is a strict subset of a CLAUDE.md or AGENTS.md rule that was added later
- The rule has been superseded by a hook that now enforces it mechanically

Not all reactive rules are bad — some capture genuinely useful corrections. The question is whether the underlying principle is already covered elsewhere. If so, the reactive rule is redundant.

### Criterion 5: Vagueness

"Is this so vague that it would be interpreted differently every time?"

Telltale signs:
- Subjective adjectives without calibration ("be more natural", "use a good tone", "write clean code")
- No examples or criteria for what counts as compliance
- The rule could justify opposite actions depending on interpretation

Note: most well-written rules with examples or specific constraints will pass this criterion. It mainly catches hastily written preferences.

## Phase 4: Output

Keep the user-facing report proportional to the findings. For comprehensive
audits, preserve detailed per-source analysis in an audit artifact and lead
with actionable findings. Use the sections below only where they apply to
the requested scope.

### 1. Per-rule analysis table

For each source file, a table with columns: Rule (short description), Default?, Conflicts?, Repeats?, Reactive?, Vague?. Use checkmarks or short notes in each cell.

### 2. Cut list

A flat table of every rule recommended for removal, with:
- The rule (short description)
- The source file
- One-line reason for cutting

### 3. Conflict list

Every conflict found, with:
- The two (or more) conflicting rules and their source files
- Whether the conflict is intentional (override) or a bug
- Suggested resolution

### 4. Cleaned-up CLAUDE.md or AGENTS.md

When global instructions are in scope and need changes, a rewritten version
of the global CLAUDE.md or AGENTS.md with:
- Dead weight removed
- Overlapping rules merged
- Conflicts resolved
- No new rules added — only consolidation

Show a clear summary of what changed and why.

### 5. Other file changes

For each non-CLAUDE.md or AGENTS.md file that needs changes (skills, memory), list the specific edits:
- Which rules to remove from which files
- Which memory files to delete
- Which MEMORY.md entries to remove

## Applying changes

If applying changes after confirmation or `--accept`:

1. Apply only high-confidence edits that preserve the intended scope of the user's configuration.
2. Prefer consolidation, wording tightening, and removal of confirmed duplicates over broad rewrites.
3. Do not delete memory files or other user-authored records destructively; use the repo's deletion policy and make the deletion explicit in the summary.
4. Keep paired Claude/Codex configuration artifacts synchronized when the repo defines a sync relationship.
5. Commit each logical change when working in a git repo, unless the user explicitly asked not to commit.

## Verification

Before calling the audit complete:

- Re-read every changed file and check for internal contradictions, broken references, and accidental scope changes.
- Run any available repo-specific checks, especially sync checks for paired Claude/Codex artifacts.
- Review the final diff and staged files so unrelated user changes are not included.
- In the final response, list files changed, verification performed, and unresolved issues or sources that could not be checked.

## Guidelines

- **Do not remove rules that are working.** If a rule changes behavior in a useful way and isn't duplicated elsewhere, it stays — even if it was reactive in origin.
- **Canonical location principle.** Keep general preferences in global
  instructions and task-specific constraints in the skill that needs them.
  Remove a duplicate only when the canonical rule is available in every
  supported context; preserve standalone portability and useful local context.
- **Check enforcement coverage.** A hook may prevent an action without teaching
  the agent the intended workflow, and it may cover only one runtime or tool.
  Remove an overlapping instruction only after checking coverage and confirming
  that no useful guidance or user preference would be lost.
- **Distinguish procedure from always-loaded rules.** In an ordinary config
  audit, do not cut useful procedural steps merely to reduce context. In an
  explicitly requested skill audit, inspect the full workflow for defects,
  authorization errors, broken references, and verification gaps.
- **Respect the confirmation boundary.** `--accept` or an explicit apply request authorizes high-confidence cleanup; otherwise, present the full analysis and wait for confirmation before changing files.
