---
name: sync-workflow
description: Sync the pragma template repo so it stays consistent with a project's current conventions (build commands, branch strategy, agent conventions). Invoke manually after any change to those.
disable-model-invocation: true
---

# Sync Workflow Agent

Sync the pragma template repo so it stays consistent with your project's current conventions.

## Trigger
Run manually after any change to AGENTS.md/CLAUDE.md, branch strategy, build commands, or agent conventions: `/sync-workflow`

## Process

### 0. Sync pragma's local checkout and create the sync branch first
```bash
git -C <pragma path> checkout develop && git -C <pragma path> pull
git -C <pragma path> checkout -B sync/<YYYY-MM-DD>
```
Do this before making any edits below — pulling *after* step 4 has already staged
uncommitted changes risks a checkout/pull conflict against your own in-progress edits.
All edits in steps 3-5 happen on this branch, not on `develop` directly. `-B` (not `-b`)
resets the branch if a same-day sync attempt left one behind from an earlier aborted run.
If `checkout develop` itself fails (e.g. mid-rebase), resolve or abort that first — don't
work around it by editing on the wrong branch.

### 1. Read the source of truth
- Read `AGENTS.md` (or `CLAUDE.md` on the pre-AGENTS.md convention) from your project — branch strategy, build commands, simulator name, architecture rules
- Read all files in `.claude/skills/` — the project-specific versions

### 2. Read the template
- Read all files in the pragma template repo's `.claude/skills/`

### 3. Compare and update
Check for drift in these areas (keep `<AppName>` placeholders — pragma is a template):

| What to check | Source of truth |
|---|---|
| Branch strategy (`main` vs `develop`) | Your project's AGENTS.md/CLAUDE.md |
| Simulator name | Your project's AGENTS.md/CLAUDE.md |
| Build command structure | Your project's AGENTS.md/CLAUDE.md |
| Test framework (`import Testing` vs XCTest) | Your project's AGENTS.md/CLAUDE.md |
| Pre-flight check commands in `/release` | Your project's `/release` skill |
| Architecture rules checklist in `/review` | Your project's `/review` skill |
| New gates in `/gates` — **only if generalizable** | Your project's `/gates` skill |
| CI workflow flags (simulator selection, coverage, parallelism) | Your project's `.github/workflows/*.yml` vs. pragma's `scaffold/.github/workflows/*.yml` |

### 4. Apply updates
Edit only the lines that differ. Do not copy project-specific paths or app names into the template — use `<AppName>` placeholders.

For new gates in your project's `/gates`, judge each one individually — do not copy-paste:
- **Generalizable** (checks a pattern any iOS MVVM+Repository project would want — e.g. a layer-rule compliance gate): port it as a *templated* gate with `<placeholder>` values, matching the style of Gates 1/2/7. Do not hardcode your project's literal grep patterns (field names, concrete paths, etc.) into the template.
- **App-specific** (checks something only your project's domain or toolchain has — e.g. a concurrency-shape gate tied to one specific actor/service, or a visual-verification gate that depends on an MCP server the project installs itself): leave it out of pragma entirely. It has no equivalent in a template repo.

### 5. Self-review the diff before committing
Pragma has no `AGENTS.md`/`CLAUDE.md` and no `/review` of its own — this is the
only check that runs before a sync PR opens. Keep it lightweight: it exists to catch the
specific ways a *template* repo can drift, not to re-litigate content already reviewed once
in your project. Run against the staged diff, before `git commit` — stage first, since the
checks below read `git diff --cached`. Stage everything this sync touched, not just
`.claude/skills/` — a CI workflow flag change under `scaffold/.github/workflows/` is just
as much a sync output and must go through the same review:
```bash
git -C <pragma path> add .claude/skills/ scaffold/
```

**a. No project-specific literals leaked into template content (advisory — eyeball each hit):**
```bash
git -C <pragma path> diff --cached | grep -E '^\+' | grep -iE '<your real app name>|/Users/|iPhone [0-9]+|<a concrete ViewModel or Repository name>'
```
Fill in the alternation with your actual project's literal identifiers before running — e.g. FinanceTracker's own copy of this check greps for `FinanceTracker|/Users/akshaypimprikar|iPhone 17|AccountViewModel|SwiftData[A-Z]\w*Repository`. Searching for the placeholder text itself (`<AppName>` etc.) catches nothing; it's the literal values a leak would introduce that this check needs. A worked example in prose is fine (pragma's own files already do this, e.g. `/gates feature/recurring-transactions`). A hardcoded value standing in for what should be a `<placeholder>` is not — generalize it before committing.

**b. `<placeholder>` convention held where your project's source used a concrete name:**
For every newly templated section (an architecture rule, a gate), confirm it uses
`<placeholder>` tokens for anything project-specific — a type name, a file path, a field
name — matching the style already used throughout pragma's `gates/SKILL.md` Gate 9/10 examples.
Zero placeholders in a section that generalizes a project-specific check is the leak.

**c. Gate numbering and counts stay internally consistent (deterministic):**
`Gate 0` (the build-relevant change check) is intentionally excluded from both the sequence and
the count — the pattern below starts from Gate 1 on purpose, not an oversight. `deterministic-pr-gates/SKILL.md`
is excluded from the count-reference grep below: it's a standalone skill with its own independent
gate numbering (one fewer than `gates/SKILL.md`), not a second copy of the same list.
```bash
awk 'BEGIN{expected=1} {if($1!=expected) print "non-sequential: expected "expected" got "$1; expected=$1+1}' \
  <(grep -oE '^### Gate [1-9][0-9]*' <pragma path>/.claude/skills/gates/SKILL.md | grep -oE '[0-9]+' | sort -n)
MAX=$(grep -oE '^### Gate [1-9][0-9]*' <pragma path>/.claude/skills/gates/SKILL.md | grep -oE '[0-9]+' | sort -n | tail -1)
if [ -z "$MAX" ]; then echo "ERROR: no '### Gate N' headers found in gates/SKILL.md — check the file, not the count"; else
grep -rniE "all [0-9]+ gates" <pragma path>/.claude/skills/*/SKILL.md | grep -v "deterministic-pr-gates/SKILL.md" | grep -viE "all $MAX gates"
fi
```
Pass: the sequential check prints nothing, and the count-reference grep returns no lines
disagreeing with `$MAX`. Fail: fix the stale number before committing — a stale gate-count
reference is a real recurring bug class, not a hypothetical one. If `MAX` comes back empty,
`gates/SKILL.md`'s header format has changed or the file is missing gate sections entirely — investigate
that directly rather than trusting the count-reference grep (an empty `$MAX` would otherwise
match every "all N gates" line as "stale," which is noise, not the real problem).

### 6. Open a PR — never push directly to main
The branch was already created in step 0. Re-stage before committing regardless of step 5's
staging — if self-review in 5a/5b caught something and you fixed it, the fix is unstaged
until you add it again:
```bash
git -C <pragma path> add .claude/skills/ scaffold/
git -C <pragma path> commit -m "chore: sync skills from <AppName> — <brief summary>"
git -C <pragma path> push -u origin sync/<YYYY-MM-DD>
gh pr create --repo akshaypimprikar/pragma \
  --title "chore: sync skills from <AppName> — <brief summary>" \
  --body "## Changes\n<bullet list of what changed and why>\n\n<append your coding agent's own PR-attribution footer here, if it uses one — e.g. Claude Code appends \"🤖 Generated with [Claude Code](https://claude.com/claude-code)\">" \
  --base develop \
  --head sync/<YYYY-MM-DD>
```

If nothing changed, do not create a branch or PR — report "no changes needed" instead.

**Verify before trusting the PR:** `--repo` alone does not fix the head branch — the shell's current working directory can silently resolve to the wrong repo's branch. Always confirm with:
```bash
gh pr view <N> --repo akshaypimprikar/pragma --json headRefName,baseRefName,files
```

### 7. Report
List every file changed and what was updated, plus the PR URL. If nothing needed changing, say so explicitly.

## Done when
PR is open on pragma (or "no changes needed" confirmed), report delivered.
