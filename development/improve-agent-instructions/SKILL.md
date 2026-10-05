---
name: improve-agent-instructions
description: Audit and improve the always-loaded agent instruction files (AGENTS.md, CLAUDE.md, GEMINI.md). Triggers "check/audit/update/improve/fix/revise CLAUDE.md or AGENTS.md", "project memory optimization", "trim my instruction file". Not for general docs.
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Instruction-File Improver

Audit, evaluate, and improve the instruction files that load into **every** agent session —
`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and their package-level equivalents. Can also capture
session learnings into them.

**The governing idea:** this file is a permanent, per-session token cost paid by every agent
that reads it. Keep it lightweight, spend most of its budget on **gotchas**, and push depth
behind pointers (skills, `docs/`) that load only when relevant. Restating what the agent can
see for itself — the directory tree, the dependency list, the catalog of available skills —
costs tokens in every session and buys nothing.

## Gotchas
- In this repo, `~/.claude/` is symlinked — changes to the global instruction file here affect all projects. Warn about cross-project impact before proposing changes to a committed, shared file.
- The cross-referencing step is easy to do superficially, producing a high score that misses stale paths. Actually resolve the references.
- **Multi-harness repos:** `AGENTS.md` is read by Codex, Pi and OpenCode; `CLAUDE.md` by Claude Code. Advice that leans on one tool's specific mechanisms doesn't belong in the shared file. Prefer `AGENTS.md` as canonical with `CLAUDE.md` a one-line `@AGENTS.md` bridge.

## Instructions

### Step 1: Discovery

Find all instruction files:

```bash
find . \( -name "AGENTS.md" -o -name "CLAUDE.md" -o -name "GEMINI.md" -o -name ".claude.local.md" \) 2>/dev/null | head -50
```

Also check `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` for global defaults — they matter
because **project rules that merely repeat a global rule are pure duplication**.

| Type | Location | Purpose |
|------|----------|---------|
| Project root (canonical) | `./AGENTS.md` | Primary context, read by every harness |
| Claude bridge | `./CLAUDE.md` | Ideally one line: `@AGENTS.md` (+ Claude-only overrides) |
| Local overrides | `./.claude.local.md` | Personal settings (gitignored) |
| Global defaults | `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md` | User-wide defaults |
| Package-specific | `./packages/*/AGENTS.md` | Module-level context in monorepos |

### Step 2: Quality Assessment

Evaluate each file against six criteria (see `references/quality-criteria.md` for detailed rubrics):

| Criterion | Weight | What to check |
|-----------|--------|---------------|
| Gotchas & non-obvious knowledge | 25pts | Quirks, footguns, invariants — what can't be read off the repo? |
| Commands & divergent conventions | 20pts | Build/test/deploy present? Conventions that actually differ from tool defaults? |
| Non-derivable & non-duplicated | 20pts | Directory trees, dependency lists, skill/tool catalogs, rules repeated from the global file? |
| Progressive disclosure | 15pts | Are long procedures extracted into skills/`docs/` and referenced, or inlined? |
| Currency | 10pts | Reflects current codebase? |
| Internal consistency | 10pts | Any rule contradicting another rule or the tool's own defaults? |

Grades: A (90-100), B (70-89), C (50-69), D (30-49), F (0-29).

Cross-reference with the actual codebase: check that referenced files exist, that commands
would work, and that described behavior matches the code.

Also record the **line count** — the target is roughly <200 lines. Over that, the finding is
usually "extract into skills/docs", not "write more tersely".

### Step 3: Output Quality Report

**Always output the report BEFORE making changes.** Format:

```
## CLAUDE.md Quality Report

### Summary
- Files found: X
- Average score: X/100
- Files needing update: X

### File-by-File Assessment

#### 1. ./AGENTS.md (Project Root) — NNN lines
**Score: XX/100 (Grade: X)**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Gotchas & non-obvious knowledge | X/25 | ... |
| ... | ... | ... |

**Issues:** [specific problems]
**Recommended additions:** [what should be added]
**Recommended removals:** [derivable / duplicated / extractable content, with where it should go instead]
**Conflicts:** [rules that contradict each other or the tool's defaults — both sides named]
```

### Step 4: Propose Targeted Updates

After the report, ask for user confirmation before editing.

Follow `references/update-guidelines.md` strictly. Auditing is **not only additive** — a
good audit usually proposes cuts as well as additions:
- **Add** only genuinely useful info: gotchas, discovered commands, divergent conventions,
  cross-module knowledge, config quirks
- **Remove** what's derivable from the repo, what the harness already injects, what repeats
  the global file, and long procedures that belong in a skill (say where they should go)
- **Surface conflicts** rather than resolving them silently: name both rules and ask which wins
- **Leave the user's preferences alone.** House style, commit format, review policy and
  similar taste rules are exactly what this file is for — propose removing a rule only when
  it is a guardrail against a failure mode, not an expression of preference, and even then
  the user decides
- Show diffs for each proposed change with a brief "why this helps"

Use `references/templates.md` for section formatting guidance.

### Step 5: Apply Updates

After user approval, apply changes with the Edit tool. Preserve existing content structure.

### Alternative: Session Learnings Mode

If invoked at end of session or with "revise AGENTS.md" / "revise CLAUDE.md":

1. **Reflect** on session: what context was missing? Commands discovered? Gotchas encountered? Code style patterns?
2. **Filter hard.** A learning belongs in the instruction file only if it is durable, project-specific, non-derivable, and broadly relevant. A one-session detail is not; a recurring footgun is
3. **Decide placement**: `AGENTS.md` for team-shared info, `.claude.local.md` for personal
   preferences, a skill or `docs/` file when the learning is a procedure rather than a fact
4. **Draft additions** — one line per concept, concise
5. **Show proposed diffs** with "why" for each
6. **Apply with approval** only

### User Tips to Share

- Prefer `AGENTS.md` as the canonical file with `CLAUDE.md` as a `@AGENTS.md` bridge — every harness reads the former
- Use `.claude.local.md` for personal preferences (add to `.gitignore`)
- Global defaults go in `~/.claude/CLAUDE.md` / `~/.codex/AGENTS.md`
- Keep it lightweight — this file is part of every prompt. Depth belongs in a skill or `docs/`, referenced from here
- Claude Code saves relevant memories automatically; the instruction file is for durable project rules, not a session scratchpad

## Examples

### Example 1: Auditing a project

User says: "Check if my CLAUDE.md is up to date"

Actions:
1. Find all instruction files in the repo (plus the global ones, to spot duplication)
2. Read each and cross-reference with the codebase (check package.json for commands, verify file paths exist, etc.)
3. Score each file against the quality criteria; record line counts
4. Output the report: 45/100 (Grade D), 310 lines — missing build commands; a 60-line directory tree the agent can see for itself; an "Architecture" section referencing a deleted `src/legacy/` dir; the git policy repeated verbatim from `~/.claude/CLAUDE.md`
5. Propose **both** directions: add the commands table from package.json and a gotcha about required Node 20+; remove the directory tree and the duplicated git policy; extract the 40-line release checklist into a skill and leave a one-line pointer
6. After user approves, apply edits

### Example 2: Trimming an over-constrained file

User says: "audit AGENTS.md"

Actions:
1. Score the file; note two rules that fight each other — "always add JSDoc to exported functions" in one section and "no comments unless non-obvious" in another
2. Report the conflict with both line numbers, explaining that an agent must burn reasoning deciding which wins and may pick wrong
3. Ask which rule the user wants to keep, rather than picking one
4. Apply the user's choice; leave the rest of their house style untouched

### Example 3: Capturing session learnings

User says: "/improve-agent-instructions" or "revise AGENTS.md" at end of session

Actions:
1. Reflect on session — discovered that `npm test -- --runInBand` is needed, found that `src/config.ts` must be imported before any DB calls
2. Filter: both are durable, project-specific, and non-derivable — they qualify. A one-off flaky-test rerun from this session does not
3. Draft two additions: testing command note, initialization order gotcha
4. Show diffs targeting `./AGENTS.md`
5. Apply after approval

## Troubleshooting

### No instruction files found
**Cause:** New project, or none created yet.
**Solution:** Offer to create one using the minimal template from `references/templates.md`. Ask about project type (standard, monorepo, package) to pick the right template.

### Score seems wrong
**Cause:** Assessment may not have cross-referenced enough of the codebase.
**Solution:** Read key files (package.json, main config, CI config) to verify commands and described behavior before scoring. Re-run assessment with deeper codebase analysis.

### The audit only proposed additions
**Cause:** Treating the file as a place to accumulate rather than curate — the most common failure mode of this skill.
**Solution:** Re-run the Non-derivable, Progressive-disclosure, and Internal-consistency criteria specifically. A file over ~200 lines that produced zero removal candidates was not really audited.

### User rejects proposed changes
**Cause:** Changes may be too generic, not project-specific, or the audit proposed cutting a rule the user holds deliberately.
**Solution:** Ask what specific areas the user wants improved. Preferences stay; only derivable, duplicated, or extractable content is on the table.
