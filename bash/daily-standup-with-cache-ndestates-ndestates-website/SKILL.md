---
name: daily-standup-with-cache
description: >
  Start a daily working session on ndestates-io using the local cache + today's TODO + open concerns.
  This is the recommended prompt/skill for almost every normal development or review session.
argument-hint: "Optional focus, e.g. 'Frontend', 'Users', 'Filament work', 'schema', 'tests', 'valuations'"
user-invocable: true
disable-model-invocation: false
---

# Daily Standup With Cache (Recommended Default Session Start)

**This is the skill you should invoke at the beginning of most sessions.**

## Step 1: Load Core Cache (do not skip)

Honor `token_policy.max_cache_files_default` (default **2** extra docs after spine).

**Spine (does not count toward cap):**
1. `.claude/project-manifest.yaml` — read `token_policy`
2. `docs/codebase/README.md`
3. `docs/codebase/.codebase-scan.txt`
4. Current daily TODO from `TODO/` (latest date file)
5. `.copilot/memories/INDEX.md`

**Pick ≤2 additional** (grep sections first; do not full-read registry/skills):
- `docs/codebase/CONCERNS.md` (default first pick)
- One of: `ARCHITECTURE.md`, task-specific cache doc, or one INDEX memory

## Step 2: Remote branch resume (mandatory — never skip)

**Hard rule:** `.github/skills/chain/SKILL.md session-start`, `.github/prompts/daily-standup-with-cache.prompt.md`, and standup aliases **always** resolve the **latest remote branch worked on** (`origin/*` by committer date after `git fetch`) and **offer the user a switch** to it. Never auto-checkout.

Run from project root **before** synthesis:

```bash
git fetch origin --prune
git branch --show-current
git status -sb
# Latest remote branches (primary resume signal)
git for-each-ref refs/remotes/origin/ --sort=-committerdate \
  --format='%(refname:short)|%(committerdate:short)|%(authorname)|%(subject)' \
  | grep -vE 'origin/HEAD|origin/develop$|origin/master$' | head -8
# Local branches (secondary — may be behind or unpushed)
git for-each-ref refs/heads/ --sort=-committerdate \
  --format='%(refname:short)|%(committerdate:short)|%(subject)' | head -5
# Optional: recent pushes / open PRs
gh pr list --author @me --limit 5 2>/dev/null || true
```

Also read **Branch:** in the latest `TODO/*_TODO.md`.

**Pick `remote-last` (required):**
1. After fetch, newest `origin/<branch>` by **committer date** on the remote-tracking ref.
2. Prefer user work branches: `feature/*`, `fix/*`, `chore/*`, `docs/*`.
3. Exclude `origin/develop` and `origin/master` unless they are genuinely the newest remote activity (rare for day-to-day work).
4. If the newest remote is a merged/deleted branch, take the next newest that still exists on `origin`.

**Also note:** `local-last` (newest local branch), `current`, `todo-branch`.

**If `current` ≠ `remote-last`:** you **must** offer switching to `remote-last` — this is non-optional for session-start.

| | Branch | Last activity | Role |
|---|--------|---------------|------|
| **Remote last** | … | … | **primary resume target** |
| Current | … | … | where you are now |
| Local last | … | … | may differ if unpushed or stale checkout |
| TODO says | … | … | from latest TODO file |

End Step 2 with an explicit prompt (always include **remote-last**):

> **Branch resume:** Latest remote branch worked on: **`<remote-last>`** (`<date>` — `<subject>`).
> You're on **`<current>`**. Local last: `<local-last>`. TODO: `<todo-branch>`.
> Switch to **`<remote-last>`**? Reply **`yes`** / branch name / **`stay`** on `<current>` / **`no`** to skip.

- **`yes`** or matching branch name → `git checkout <branch>` then `git pull --ff-only origin <branch>` when tracking exists.
- **`stay`** / **`no`** → continue on `current`; say why remote-last was not chosen if it differs from TODO.

Then: branch purpose vs TODO scope; flag detached HEAD (always offer `remote-last`).

## Step 3: Synthesise
Produce a short briefing for the user:
- What the cache says the current priorities/risks are
- What today's TODO file says is in scope
- Any numbered CONCERNS items that are relevant
- **Shell/script discipline:** if CONCERNS §6 applies or last session had heredoc/syntax shell errors, remind user of `.github/skills/script-not-shell/SKILL.md` (write `scripts/` or `/tmp/agent-*`, never retry complex one-liners)
- Whether DDEV is running (if relevant to the task)
- AI engineering maturity indicators (per the 8-stages model in .github/skills/ai-engineering-maturity/SKILL.md and copilot-instructions §11): e.g. shared .github/ context adoption vs. drift, guardrail/MCP usage, evals/standards encoded in system, any "islands" in workflows. Note center of gravity and one concrete advancement opportunity.

## Step 4: Ask for Direction
End with a numbered list of suggested next actions based on the above.

**Token rule**: Do not read source files yet. Only read source after the user confirms the direction and you have absorbed the cache + TODO.

Cite every cache file you used in your response.

Full details in `.github/prompts.github/prompts/daily-standup-with-cache.prompt.md.md`. Follow `.github/copilot-instructions.md`. Always consider AI maturity when the work involves Grok skills/agents/prompts or code generation.
