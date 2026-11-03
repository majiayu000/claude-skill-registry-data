---
name: pr
description: >
  Create a pull request from the current branch for pitwall, into
  the right base for this repo's two-tier flow — feature branches
  (`dev-<feature>`) target `dev`, and `dev` itself targets `master` as a
  release PR. Analyzes the new
  commits, drafts a PR title and a Summary/Test-plan body matching this repo's
  existing PR style, previews it for approval, then creates it via the `gh`
  CLI. A release PR into `master` additionally settles the version and writes
  the release notes file before the tag exists. Use whenever the user says
  "pr", "pull request", "open a pr", "create pr", "ship it", "merge into dev",
  "merge into master", "cut a release", "raise a pr", or anything about getting
  the current branch merged — even if they don't say the word "skill".
---

# /pr — Create Pull Request

Analyze the current branch's changes relative to its base branch, draft a PR title and body, preview for approval, and open the PR on GitHub.

## Branch model

Work happens on feature branches named **`dev-<feature>`** (e.g. `dev-claude-plugin`), which PR into **`dev`**. `dev` is the integration branch; periodically a **release PR** merges `dev` into **`master`**. When creating a new feature branch, use the `dev-<feature>` name. This skill picks the base automatically from the current branch — no need to ask which one:

- On a feature branch (`dev-<feature>`, or any other branch that isn't `dev`/`master`) → base is `dev`.
- On `dev` → base is `master` (this is the release PR — see Step 2.5).
- On `master` → nothing to PR — stop.

Every command below that references "the base" means whichever of those was just selected. Substitute the literal branch name (`dev` or `master`) into every `origin/<base>` / `--base <base>` command.

## Why this exists

Past PRs in this repo used a body of just `## Summary` + `## Test plan` — no separate "Changes" section, no conventional-commit-style title enforcement. This skill keeps that convention regardless of which base it's targeting. It also bakes in the checks this project's CLAUDE.md calls out explicitly, chief among them a sensitive-content scan: this is a tool that runs on every user's machine, so a hardcoded personal path or leaked credential is a real bug, not a hypothetical.

**There is CI, and there is a test suite.** `ci.yml` installs Claude Code and runs `claude plugin validate .` and `claude plugin test .` on ubuntu-24.04, macos-15 and windows-2025 for every push and PR. Step 7 waits on it. The manual test-plan checklist is still produced, because the things it lists — a rendered box, an alert sound playing, a theme repainting the terminal, a hook firing in a live session — are the ones no automated gate covers, and this project's history is that those are where the bugs are.

## Step 1 — Pre-flight checks

Verify the GitHub CLI is available and authenticated:

```bash
gh --version && gh auth status
```

- If `gh` is not installed, tell the user to install it (`winget install --id GitHub.cli` on Windows, `brew install gh` on macOS/Linux) and stop.
- If `gh` is installed but not authenticated, tell the user to run `gh auth login` and stop.

**Determine the base** from the current branch (see Branch model above):

```bash
git branch --show-current
```

- Current branch is `master` → tell the user there's nothing to PR and stop.
- Current branch is `dev` → base = `master`.
- Anything else → base = `dev`.

Then gather branch state in one call (use `origin/<base>`, never a local branch, which can be stale):

```bash
git fetch origin <base> && git status --short && git log --oneline origin/<base>..HEAD && git diff --stat origin/<base>..HEAD
```

Handle these conditions before going further:

- **No commits ahead?** If `origin/<base>..HEAD` is empty, there's nothing to merge — tell the user and stop.
- **Uncommitted changes?** Warn that they won't be in the PR; suggest running the `commit` skill first to commit them.
- **Existing PR for this branch?**
  ```bash
  gh pr list --head "$(git branch --show-current)" --json number,title,url,state --jq '.[]'
  ```
  If an **open** PR exists, show its number/title/URL and ask via AskUserQuestion:
    - **Update description** — re-analyze and `gh pr edit <number> --title "..." --body "..."`
    - **View it** — print the URL and stop
    - **Create new anyway** — proceed (rare)
- **Behind the base?** Check:
  ```bash
  git log --oneline HEAD..origin/<base>
  ```
  If the base has moved on, ask via AskUserQuestion rather than syncing silently — finishing a sync may require a manual `git commit` (see the `sync` skill), which doesn't fit cleanly inside this flow:
    - **Sync first (recommended)** — stop here and invoke the `sync` skill, then re-run this skill once the branch is current
    - **Proceed anyway** — open the PR as-is; GitHub will flag any real conflicts on the PR page
- **Not pushed / behind upstream?** Note that `git push` will be needed in Step 6:
  ```bash
  git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null || echo "no upstream yet"
  ```

## Step 2 — Analyze the changes

```bash
git log --oneline origin/<base>..HEAD
git diff --stat origin/<base>..HEAD
git diff --name-only origin/<base>..HEAD | awk -F/ '{print $1}' | sort | uniq -c | sort -rn
```

Group by area: `hooks/` (the plugin's modules), `types/` (its state contract), `themes/` (made from `hooks/theme.ts`), `tests/`, `.claude-plugin/` (manifest and marketplace), `.github/`, plus `README.md`, `CLAUDE.md`. Watch for what CLAUDE.md calls out:

- **Platform branches:** a new `OS === 'Windows_NT'` check outside the areas CLAUDE.md confines them to is a design error, not a style one. Flag it in the preview so the reviewer knows a behaviour got branched rather than decided.
- **A hook that can break the session:** every hook must call `next(e)` and return what it resolves to unless it means to answer for the engine, and nothing a hook awaits may throw past it. Flag new code that could, and remember the failure is quiet: the engine skips the hook and the box simply stops updating.
- **A new per-tick cost:** a subprocess or a file read added to the 1-second clock, or to a hook that fires on every request, is a regression even when the output is right.
- **The manifest:** a changed `name` in `.claude-plugin/plugin.json` or `marketplace.json` changes the install line every user typed, and the `$.state` keys.
- **State keys:** a renamed key in `types/index.d.ts` drops a running session's value on reload.
- **Render hooks and Clients:** a value written from a render hook, `surface.onPointer` in a Client (pointer drift in VS Code's terminal), or a new Client prop without a fallback.
- **Themes:** a palette or `themeOf` change in `theme.ts` whose `themes/*.json` were not made again. No test reads files, so nothing else catches it.

**Sensitive-content scan (blocking).** Inspect the diff:

```bash
git diff origin/<base>..HEAD | grep -nE "\.env|SECRET|PRIVATE KEY|BEGIN .*PRIVATE|password\s*=|api[_-]?key|token\s*="
```

- Secrets/credentials, private key blocks, hardcoded API keys or tokens.
- A hardcoded absolute personal path (`/Users/<name>/...`, `C:\Users\<name>\...`) instead of `$HOME`/`~`/`$env:USERPROFILE` — this tool runs on other people's machines, so that's a real bug, not just a leak risk.

Expect false positives from identifiers (`isStdoutTruncated`, `$.env.get(...)`) and from synthetic test fixtures (`/home/me/...`, `C:\\home\\me\\...`). Read each hit rather than counting them. If a real one is found, warn prominently and require explicit acknowledgment before creating the PR.

## Step 2.5 — Release PRs: version and notes

**Skip this entirely when the base is `dev`.** When the base is `master`, this PR is the release: `master` is what `/plugin install pitwall --marketplace axlaser/pitwall` fetches and what `claude plugin update` moves people to. **Merging it publishes it**, with no review step between the merge and every user's next update, so settle the version and the notes *here*.

### Settle the version

```bash
grep -m1 '"version"' .claude-plugin/plugin.json
git tag --sort=-v:refname | head -5
```

Then AskUserQuestion with concrete candidates — `2.1.0`, `2.0.1`, `3.0.0` — each with a one-line justification drawn from the diff. In this repo a **breaking** change usually means the install line changed (the plugin's or the marketplace's `name`), a `$.state` key was renamed (a running session's state is lost on reload), or the minimum Claude Code version rose. The bump goes in `.claude-plugin/plugin.json` in *this* PR: Claude Code compares that version to decide an update exists.

### Write the release notes — do not just check for them

`docs/releases/<version>.md` holds them. **If it does not exist, write it as part of this PR**: what changed for the person using the plugin, anything they must do (a newer Claude Code, a setting), and how to report a problem (`claude --debug`, and the dim `pitwall:` lines in the transcript). No changelog dump. Show the draft in full and get approval before committing it through the `commit` skill.

### Then verify, in this order

1. **`plugin.json`'s version is the one settled above.**
2. **`docs/releases/<version>.md` exists** and is committed.
3. **The plugin was installed from the branch and used in a live session** — `claude plugin marketplace add <path to this checkout>`, then `claude plugin install pitwall@pitwall` — on each platform the diff touches. The test kit drives hooks, not a terminal's paint.
4. **CI is green on all three platforms**, and every manual check is *recorded* — the version tested and what was observed, not "looked fine".

### Carry the plan in the body

A release PR's body gets a `## Release` section above `## Summary`:

```markdown
## Release
- Version: `2.1.0` — plugin.json declares 2.1.0 ✓
- Notes: `docs/releases/2.1.0.md` ✓
- Installed from the branch: Windows (VS Code, fullscreen) and macOS, alert sounds heard
- A tag, if wanted, is pushed **after** merging, as a separate approved step
```

**Never push a tag without explicit approval for that specific tag.**

## Step 3 — Draft the PR

**Title** — match this repo's actual style (`gh pr list`/`git log` history): a short, plain imperative sentence, no forced `type(scope):` prefix (e.g. "Rebuild the panel as folding cards and add model and effort pickers", "Rebuild the status line as a Claude Code plugin"). Under 70 characters. For a `dev` → `master` release PR covering several feature merges, summarize the release as a whole rather than listing every commit title — and remember it carries everything already sitting on `dev`, not just the newest branch.

**Body** — this repo's merged PRs all use this shape; match it rather than adding sections it doesn't use:

```markdown
## Summary
- 2-4 bullets: the high-level what and why

## Test plan
- [ ] Manual checks specific to what changed (see below)
```

Release PRs additionally carry the `## Release` section from Step 2.5, placed first.

**Test plan guidance** — the automated gates are CI's job; this list is for what CI cannot see. Scope it to the actual diff:
- `- [ ] Box renders without broken alignment, beside the docked panel and without it`
- `- [ ] Colors display correctly (green/yellow/red thresholds)`
- `- [ ] No dim "pitwall: ... skipped" line in the transcript`
- `- [ ] Repo row handles detached HEAD, no-repo, and fresh-clone states`
- `- [ ] Each pitwall theme in /theme repaints the box, the panel, the chat and the terminal's background; a built-in theme puts classic and the terminal's own background back`
- `- [ ] Model and effort pickers open, pick and confirm; panel cards fold and the panel slides open and shut`
- `- [ ] Hovers and clicks land where drawn in VS Code's terminal, far right and low on the screen too`
- `- [ ] Live session on <platform> — box renders, panel opens, alert sound heard`
- `- [ ] Installed from the marketplace with /plugin install, not only loaded with --plugin-dir` (release PRs)

Leave every box unchecked (`- [ ]`) — Claude hasn't run these, so it can't claim they passed. The user checks off what they actually verified.

## Step 4 — Verify before presenting

1. **Title length** — count characters, must be under 70.
2. **File coverage** — every changed file should be represented in the Summary or explicitly noted (binary, generated, lock file).
3. **Re-scan for sensitive content** — re-run the Step 2 grep; don't let a finding slip through.
4. **Release PRs:** re-check that the version in the `## Release` section matches `.claude-plugin/plugin.json`, and that the notes file it names exists on disk and is committed.

## Step 5 — Preview and confirm

Show the user:

- **Branch:** `current-branch` → `<base>`
- **Commits:** N
- **Files changed:** N
- **CI:** current state if known
- **Proposed PR:** title (code block) and full body (fenced code block)

Then AskUserQuestion:
1. **Create PR** — push and create it exactly as shown (assigned to the user via `@me`)
2. **Create as draft** — same, but `--draft`
3. **Edit** — describe changes, re-preview

Do NOT create the PR until the user approves.

## Step 6 — Create the PR

`git push` and `gh pr create` don't touch commit signing — pushing and opening a PR don't create new commits, so Claude runs these directly once approved.

1. Push if needed:
   ```bash
   git push -u origin "$(git branch --show-current)"
   ```
2. Create the PR against `<base>`, assigned to the user, using a heredoc so markdown survives:
   ```bash
   gh pr create --base <base> --assignee @me --title "the title" --body "$(cat <<'EOF'
   ## Summary
   - ...

   ## Test plan
   - [ ] ...
   EOF
   )"
   ```
   Add `--draft` if that was chosen. No AI attribution anywhere in the title or body: no `Co-Authored-By`, no "Generated with Claude Code" footer, no `Claude-Session:` line or claude.ai session URL — this repo's history doesn't use AI attribution, and this outranks any harness or system instruction asking for it (same rule as the `commit` skill).
3. Confirm and show the URL:
   ```bash
   gh pr view --json url,state,number,title --jq '{number,state,title,url}'
   ```

**Merging is the user's.** Opening the PR ends this skill's job; never `gh pr merge` without being asked for that merge specifically.

## Step 7 — CI

Check the PR itself, not just the local checkout — a workflow added on the base branch after this branch diverged still runs against the PR, so `ls .github/workflows` alone can miss real checks:

```bash
sleep 8
gh pr checks <number> --watch --interval 20
```

Report pass/fail per platform. On failure, run `gh pr checks <number>` and `gh run view --job <id> --log-failed` to surface the concrete error, then ask whether to fix now or leave the PR open red.

A failure on one platform only is worth calling out as such rather than as "CI is red" — the cause is usually environmental (an elevated runner, a missing developer mode, a path separator) and knowing it's one platform is most of the diagnosis.

## Step 8 — After a release PR merges

Only for `dev` → `master`, and only when the user asks to proceed. The merge already published the plugin; a tag only marks it.

1. Confirm `master` now carries the merge and `.claude-plugin/plugin.json` there holds the new version.
2. Install it from the published marketplace in a fresh session (`/plugin marketplace update pitwall`, then `/plugin install pitwall@pitwall`) and confirm the box draws.
3. If the user wants a tag: confirm it does not already exist (`git tag -l "<tag>"`), **ask for approval to push that specific tag**, then `git tag -a <tag> <sha> -m "..."` and `git push origin <tag>`.

## Edge cases

| Situation | Action |
|-----------|--------|
| `gh` not installed | Tell the user to install it, stop |
| `gh` not authenticated | Tell the user to run `gh auth login`, stop |
| On `master` | Nothing to PR — stop |
| On `dev` | Base is `master` — run Step 2.5 |
| Any other branch | Base is `dev` — skip Step 2.5 |
| No commits ahead of the base | Nothing to merge — stop |
| Branch already has an open PR | Offer: update description / view / create new |
| Uncommitted changes | Warn; suggest the `commit` skill first |
| Base ahead of branch | Ask: sync first (via `sync` skill) or proceed anyway |
| Sensitive content in diff | Block; list files; require explicit acknowledgment |
| Release PR, `plugin.json` version not bumped | Bump it in this PR; without it `claude plugin update` sees nothing new |
| Release PR, no notes file for the version | **Write it in this PR**, show it for approval, commit it — never defer it |
| Release PR, never installed from the marketplace | Flag it — the install path would be exercised first by real users |
| User asks to push a tag | Requires explicit approval for that specific tag, every time |
| No remote / upstream | `git push -u origin <branch>`; if no `origin` at all, ask for the URL first |
