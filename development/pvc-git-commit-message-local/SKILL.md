---
name: pvc-git-commit-message-local
description: Writes a git commit message in PVC format. First line is `vX.Y.Z - headline`, then `- one change per line` bullets. Bumps the semantic version from the most recent commit based on diff scope (PATCH for fixes, MINOR for new functionality, MAJOR for breaking changes). Reads `git status`, `git diff`, and `git log` so bullets describe real changes not hallucinated ones. In this variant Claude also EXECUTES the commit LOCALLY in the host project (see the Local Execution Steps); never pushes, never adds remotes. Use when asked to "commit this", "write a commit message", "make a commit", "git commit", "commit the session", or on situational phrasings like "wrap this up", "save my changes", "message for these changes", "what should I commit this as".
metadata:
  author: pvc
  version: "0.4.1"
  adapted-from: the print-only variant of this skill, reconciled for local execution (2026-07-15); public packaging added 2026-09-17
  sources: [semver-2.0.0, conventional-commits-1.0.0, tim-pope-git-commit-style, keep-a-changelog-1.1.0, pvc-voice-rules]
license: Apache-2.0
---

<!-- SPDX-License-Identifier: Apache-2.0 -->

# pvc-git-commit-message-local

Produces a commit message in the PVC house format, then commits it locally in the host project. This LOCAL variant stages the named paths for the work at hand and runs the commit itself. It never pushes, adds a remote, or sets an upstream.

## The Format

```
vX.Y.Z - Headline Summarizing the Main Change

- first concrete change
- second concrete change
- third concrete change
```

Rules:

1. First line is `vX.Y.Z - headline`. Semantic version, space, dash, space, short headline. **No quote characters anywhere.** The user supplies shell quoting around the whole message. **A blank line follows the headline before the bullets begin**, the git subject and body separator (Tim Pope); without it git treats the whole message as one subject line and log and graph views show the bullets run together.
2. Body lines start with `- ` (hyphen, single space) followed by one concrete change. One change per bullet, past-tense verbs (added, fixed, changed, removed, renamed, wired, refactored).
3. The message ends after the last bullet. No closing quote, no trailing newline, no extra punctuation.
4. 3 to 7 bullets is the target. Under 3 is acceptable when the diff contains fewer distinct changes (do not pad to hit 3). Over 7, group related changes into fewer bullets (see Example 7).
5. No em dashes anywhere. PVC voice rules apply to every word.
6. **No backtick characters anywhere in the message.** Backtick is PowerShell's escape character; on Windows it corrupts the commit whenever the message passes through a double-quoted context (`` `f `` becomes a form feed, `` `r `` a carriage return, `` `a `` a bell, `` `b `` a backspace, `` `v `` a vertical tab), eating the backtick plus the following letter. Write inline code references (function names, filenames, symbols) as PLAIN TEXT with no surrounding backticks. Quoted strings inside bullets use single quotes ('instal' to 'install'). Never use double quotes inside the body either; the outer shell quoting owns those.
7. **No GitHub autolink triggers.** GitHub renders commit messages and turns certain tokens into links: a token starting with `@` becomes a user/team mention (so `@font-face` links to github.com/font-face, a dead profile), and a bare `#123` becomes an issue/PR link. These do not corrupt the commit, only its display, but they read as mistakes. Drop the leading `@` from CSS at-rules and similar (write 'font-face rules', 'the keyframes at-rule', not '@font-face' / '@keyframes'), and avoid a lone `#` immediately followed by digits unless you genuinely mean to reference that issue.
8. **No attribution trailers.** Never append Co-Authored-By, Signed-off-by, Generated-with, or any other trailer or footer naming Claude, Anthropic, or a tool. The message ends at the last bullet even when a session note asks for an attribution line. A rule in a skill body does not always hold against that note, so the reliable fix is a Claude Code setting: put `"attribution": {"commit": "", "pr": ""}` in the repo's `.claude/settings.json`, or in the personal `~/.claude/settings.json` (`%USERPROFILE%\.claude\settings.json` on Windows). It takes effect straight away; the older `includeCoAuthoredBy` key is deprecated.

## Sources This Skill Is Grounded In

| Source | What it contributed |
|---|---|
| Semantic Versioning 2.0.0 (semver.org) | MAJOR / MINOR / PATCH bump rules and the 0.y.z initial-development phase |
| Conventional Commits 1.0.0 (conventionalcommits.org) | Change classification taxonomy (feat / fix / refactor / docs / chore) used internally to pick the bump |
| Tim Pope, "A Note About Git Commit Messages" (2008) | Imperative or past-tense subject under ~50 chars, blank line, body lines under ~72 chars |
| Keep a Changelog 1.1.0 (keepachangelog.com) | Categories used internally when grouping bullets: Added, Changed, Fixed, Removed, Deprecated, Security |
| PVC voice rules (the ban list in this file) | Banned phrases, no em dashes, no AI slop, no "ship" or "kill" or "leverage"-as-verb |

## When to Use

The user has changes in a working tree and wants them committed. Claude builds the message per the format below, then stages the named paths, runs the commit locally, and reports the short hash.

Three triggering shapes:

| User says | What to do |
|---|---|
| "commit this", "make a commit", "git commit" | Build the message from current diff |
| "what should I commit this as", "message for these changes" | Same as above, treat as message request |
| "ready to push", "wrap this up", "save my changes" | Situational. Confirm intent is a commit message, then build |

## What This Skill Does Not Do

- Does NOT push, add a remote, or set an upstream, ever. It stages named paths and commits locally, nothing further.
- Does NOT run `git add -A` blindly. It stages the specific paths for the work at hand (see the Local Execution Steps).
- Does NOT write CHANGELOG.md entries (a related but separate artifact). Use a changelog tool for that.
- Does NOT write release notes. Use a release-notes tool for that.
- Does NOT enforce Conventional Commits prefixes (`feat:`, `fix:`). The PVC format uses `vX.Y.Z` instead.
- Does NOT bump the version in `package.json`, `pyproject.toml`, or any source file. The version lives only in the commit message line.

## Trigger Examples

### Should trigger on

- "Commit this"
- "Write a commit message"
- "Make a commit for what I just changed"
- "Git commit"
- "/pvc-git-commit-message-local"
- "Ready to push, what's the message"
- "Wrap this up with a commit"
- "Save my changes"
- "What should I commit this as"

### Should NOT trigger on (let other tools handle)

- "Push my changes": user wants the push itself, not a message. Tell them to copy a prior message or rerun this skill.
- "Update the CHANGELOG": different artifact, recommend a changelog tool.
- "Write release notes": bigger scope, recommend a release-notes tool.
- "Squash my commits": git history rewrite, not a message generation.
- "Revert this commit": git operation, not a message.

## Workflow

### Step 1: Read the working tree

Run these read-only commands in parallel:

```bash
git status --short
git diff
git diff --staged
git log -10 --pretty=format:"%h %s"
```

Interpret:

- `git status --short` tells you what files moved (added / modified / deleted / renamed)
- `git diff` shows unstaged content changes
- `git diff --staged` shows staged content changes (this is what will be in the commit)
- `git log -10` gives the version history to bump from

### Step 1a: Decide what change set to capture

Four cases, in priority order:

1. `git status --short` is empty AND `git diff` AND `git diff --staged` are all empty: stop. Working tree is clean, nothing to commit. Print the refusal template (see "Refusal Template" below). Do not invent a message.
2. `git status` shows untracked files (`??` prefix) AND both diffs are empty: this is the **untracked-only** case (first commit, or fresh files not yet staged). Treat the untracked files as the change set. Infer bullet content from filenames and conventional file purpose (`package.json` means dependencies, `tsconfig.json` TypeScript config, `.gitignore` ignored paths, and so on). Add a one-line note above the rationale: `Files are untracked. Staging them by name, then committing.`
3. Only one of `git diff` / `git diff --staged` has content: use that one. No prompt needed.
4. Both `git diff` AND `git diff --staged` have content: in Auto-Mode, default to staged-only and state the choice in the rationale line. Otherwise ask once: `Both staged and unstaged changes exist. Capture STAGED only (suggested) or EVERYTHING?` Then proceed with the chosen set.

### Refusal Template (Step 1a case 1)

Print exactly this and stop. Do not produce a message, do not bump a version:

```
Nothing to commit. Working tree is clean.

Next steps:
- Stage changes: `git add <files>` and re-run.
- Or make edits in the working tree and re-run.
- Or stash exists and you meant to pop it: `git stash pop` and re-run.
```

### Step 2: Find the current version

Scan `git log` output for the most recent commit message matching the regex `^v(\d+)\.(\d+)\.(\d+)\b`.

- Found: that is the current version. Bump from it (Step 3).
- Not found and the repo has prior commits: this is the first PVC-format commit. Default the current version to `v0.0.0` and the new version to `v0.0.1` (treat the first PVC commit as a PATCH).
- Not found and the repo has NO prior commits (first commit ever): use `v0.0.1`.

### Step 3: Classify the change and pick a bump (User Choice Point)

Use SemVer 2.0.0 rules, adapted to a working tree where there is no public API contract to compare against. Read the diff and classify:

| Diff signal | Suggested bump |
|---|---|
| Only docs, comments, whitespace, config tweaks | PATCH |
| Bug fix in existing code, no new files, no signature changes | PATCH |
| New file added that adds new functionality, OR new function exposed | MINOR |
| New CLI flag, new public method, new exported symbol | MINOR |
| Removed file, removed function, renamed public symbol, breaking signature change | MAJOR |
| Repo still at 0.y.z AND change is what would be MAJOR at 1.0.0+ | MINOR (per SemVer rule: "Anything MAY change at any time" during 0.y.z; bumps stay below 1.0.0) |

**Internal vs public tiebreaker:** "New file" and "new exported symbol" sound MINOR, but if the new file is INTERNAL plumbing (not exported from the package root, not imported by anything outside the package, not part of the public API surface), prefer PATCH. Rule of thumb: if a downstream consumer of the package could USE the new symbol, it is MINOR. If only internal code uses it, it is PATCH.

Then ASK the user to confirm the bump before writing the message, unless the user already said "patch", "minor", or "major" in their request. Phrase the question short:

> "From v1.4.2. PATCH (suggested), MINOR, or MAJOR?"

Skip the question if any of these is true:
- User said "patch", "minor", "major", "bug fix", "new feature", or "breaking" in their original request
- Repo is at v0.0.0 and this would be the first commit (default to v0.0.1)

### Step 4: Write the headline

Pick ONE sentence, target 50 characters, hard cap 60 characters. **Past tense, always.** No imperative, no infinitive. Examples honor this.

Rules:
- Past tense verb start ("Added", "Fixed", "Renamed", "Wired", "Refactored", "Removed", "Documented")
- Title Case: capitalize the principal words, keep short words (a, an, the, and, or, of, to, in, on, for, with, into, onto) lowercase unless first. Preserve code identifiers and filenames as written (getUser, auth-callback.ts, OAuth, README)
- Concrete noun ("the lead-magnet form", "auth callback redirect", "Stripe webhook validator")
- No vague nouns ("things", "stuff", "updates", "tweaks", "improvements")
- No PVC-banned phrases (see voice rules below)
- If the headline would exceed 60 chars, trim with a comma: `"Removed getUser, renamed getCurrentUser to getViewer"` reads cleaner than running long.

### Step 5: Write the bullets

Target 3 to 7 bullets, each starting with `- ` (hyphen, single space). One concrete change per bullet.

Rules:
- Past-tense verb start (matches the headline)
- Specific subject ("the JWT validator", "checkout button styles", "the /api/leads route") not vague ("things", "code", "various")
- One change per bullet. If two ideas, split.
- If a bullet would only restate the headline, drop it.
- Order: most user-visible first, internal cleanup last.
- **Bullet count flex:** 3-7 is the target. Under 3 is acceptable when the diff genuinely contains fewer distinct changes (do not pad to hit 3). Over 7 forces grouping (see "Grouping" below).
- **Grouping for many-file pattern changes:** when 5+ files repeat the same change, list them by name in ONE bullet. See Example 7 below.
- **No backticks, no inner double quotes:** write inline code (function names, filenames, symbols) as PLAIN TEXT, e.g. parseInput not `` `parseInput` ``. Backticks are PowerShell's escape character and silently corrupt the commit on Windows (see format rule 6). Use single quotes only for quoted strings ('instal' to 'install').
- **No GitHub autolink triggers (rule 7):** drop the leading `@` from CSS at-rules and similar (write 'font-face rules', not '@font-face', since GitHub turns a leading `@` into a dead user-mention link), and avoid a lone `#` directly before digits unless you mean to reference that issue.
- **Filename grounding for binary-only changes:** when a binary has no companion text-diff context, ground it in filename semantics (`-dark` variant, `@2x` retina, `og-` social-share) and say so plainly.

### Step 6: Voice check

Before printing, grep your draft against the PVC ban list. If any match, rewrite the offending word:

| Banned | Replace with |
|---|---|
| em dash (U+2014) | comma, period, or rephrase |
| "ship", "ship it", "shipped" | published, released, delivered, finished, sent out |
| "kill", "killed" (re: business outcome) | stalled, dragged, hurt, broke, cost, ended |
| "leverage" (as verb) | use, lean on, take advantage of, build on |
| "land", "doesn't land" | works, fits, reads right, sounds natural |
| "move the needle", "shift the dial" | works, matters, pays off, produces results |
| "picture this" | (rewrite to start with the actual content) |
| "steal", "worth stealing" | adopt, worth adopting, adapt, take inspiration from |
| "operator", "founder" | business owner, owner, you |
| "X first, Y second" sequencing | "first ... then ...", "before ... after ..." |
| "does the heavy lifting" | (be specific about what the thing does) |
| "digging through" | looking for, searching, going through |
| "just", "simply", "really" (filler) | drop the word |
| "tedious", "delve" | (rewrite) |

### Step 7: Print the message, then commit

Print the version-bump rationale line, then the message in a fenced code block. Then EXECUTE the commit per the Local Execution Steps below: stage the named paths, commit through a heredoc so the multi-line message survives Windows shell quoting, and report the short hash. Never push, never add a remote.

## Output Rubric

Every message this skill produces must score pass on each dimension.

| Dimension | Pass criteria |
|---|---|
| format_exact | First line matches `^v\d+\.\d+\.\d+ - .+$` (no inner quote). A single blank line separates the headline from the first bullet. Body lines match `^- .+$`. Last bullet has no trailing quote, no trailing punctuation. Zero double-quote characters AND zero backtick characters anywhere in the message body (backticks break PowerShell paste). No token starts with `@` and no bare `#`-then-digits (GitHub autolinks both, see format rule 7). |
| version_bump_valid | Bump follows SemVer rules above. Repo at 0.y.z never jumps to 1.0.0 without user opt-in. |
| bullet_count | Target 3-7 bullets. Under 3 is acceptable when diff genuinely supports fewer (do not pad). Over 7 must be grouped using the Example 7 pattern. |
| concrete_subjects | Every bullet names a specific file, function, route, or feature. Zero vague nouns. |
| voice_consistency | Zero em dashes. Zero matches against the PVC ban list above. |
| grounded_in_diff | Every bullet maps to a real hunk in `git diff` or `git diff --staged`, OR (untracked-only case) to a real file in `git status --short`. Zero hallucinated changes. |
| local_commit_executed | The commit runs locally through a heredoc on named paths and the short hash is reported. Zero `git push`, zero remote or upstream changes. |
| edge_case_coverage | Handles: clean tree (refusal template, no message), first commit / untracked-only (default v0.0.1, ground in filenames, note the untracked files staged by name), no prior PVC-format version in log (default v0.0.0 baseline), staged + unstaged ambiguity (ask once or auto-default to staged in Auto-Mode), repo at 0.y.z (never auto-bump to 1.0.0), binary-only changes (filename-as-evidence with semantic inference like `-dark`, `@2x`), many-file pattern (group into one named bullet per Example 7). |
| internal_vs_public | New internal-only files default to PATCH, not MINOR. New publicly-exported symbols are MINOR. |
| headline_length | Headline target 50 chars, hard cap 60 chars. Past tense always. Title Case. |

## Worked Examples

### Example 1: Bug fix, PATCH bump

Diff signal: existing route handler had a wrong status code, fixed in one file. Last commit was `v1.4.2 - "..."`.

```
v1.4.3 - Fixed Wrong Status Code on /api/leads Validation Error

- Returned 422 instead of 500 when payload missing required fields
- Added regression test covering the missing-email case
- Updated error response shape to include the failed field name
```

Rationale line above the block: `PATCH from v1.4.2 to v1.4.3, behavior fix, no public API change.`

### Example 2: New feature, MINOR bump

Diff signal: new file `auth-callback.ts` exposes a new exported function, two existing files now import it. Last commit was `v0.4.7 - "..."`.

```
v0.5.0 - Added Supabase Auth Callback Handler for OAuth Redirects

- New auth-callback.ts module exporting handleOAuthRedirect
- Wired the handler into the /api/auth/callback route
- Login page now redirects to /dashboard after successful OAuth
- Added env var SUPABASE_REDIRECT_URL to .env.example
```

Rationale line: `MINOR from v0.4.7 to v0.5.0, new exported function, additive only.`

### Example 3: Breaking change, MAJOR bump (post-1.0.0 repo)

Diff signal: removed the deprecated `getUser()` function, renamed `getCurrentUser()` to `getViewer()`. Last commit was `v2.1.4 - "..."`.

```
v3.0.0 - Removed Deprecated getUser API and Renamed getCurrentUser

- Removed getUser function from the public exports
- Renamed getCurrentUser to getViewer across the SDK
- Updated all internal call sites to use getViewer
- Bumped TypeScript declarations to reflect the rename
- Added migration note in the README
```

Rationale line: `MAJOR from v2.1.4 to v3.0.0, public API removal and rename, callers must update.`

### Example 4: Docs-only, PATCH bump

Diff signal: only README.md and CLAUDE.md changed. Last commit was `v0.3.1 - "..."`.

```
v0.3.2 - Updated README Install Steps and CLAUDE.md Voice Rules

- Rewrote install section to cover the four placement paths
- Added the trigger-phrase variation test to the workflow
- Removed stale references to the old plugin cache location
- Tightened voice rules with the new ban list
```

Rationale line: `PATCH from v0.3.1 to v0.3.2, docs only.`

### Example 5: First commit in a brand-new repo

Diff signal: every file is new, no prior `git log` entries.

```
v0.0.1 - Scaffolded the Project with Initial Structure

- Added package.json with the base dependencies
- Created src/ with the entry point and main route
- Added .env.example and .gitignore
- Wrote the initial README with install steps
```

Rationale line: `Initial commit, defaulted to v0.0.1.`

### Example 6: Pre-1.0 repo with what would be a breaking change

Diff signal: removed a function from the public exports, but repo is at v0.4.x. Per SemVer 0.y.z phase: anything may change, stay below 1.0.0. Bump MINOR.

```
v0.5.0 - Removed Legacy parseInput Helper, Moved Logic into Validator

- Deleted parseInput from src/util/parse.ts
- Inlined the parsing into validateRequest
- Updated the two call sites to use validateRequest directly
- Pruned the now-unused regex helper from util/regex.ts
```

Rationale line: `MINOR from v0.4.6 to v0.5.0. Would be MAJOR at 1.0.0+, but repo is at 0.y.z so SemVer rule allows MINOR.`

### Example 7: Many-file pattern change (grouping)

Diff signal: 10 components migrated from a static `theme` import to a `useTheme()` hook. The hook itself is new and internal. Last commit was `v0.6.4 - "..."`.

Twelve files touched but the pattern repeats. Group the 10 component edits into one named bullet rather than ten near-duplicate bullets.

```
v0.6.5 - Refactored 10 Components onto a useTheme Hook

- Added useTheme hook in src/hooks/useTheme.ts wrapping ThemeContext
- Migrated Button, Input, Card, Modal, Toast, Avatar, Spinner, Tabs, Tooltip, and Badge to call useTheme() instead of importing theme directly
- Trimmed src/theme/tokens.ts since components no longer import it
- Confirmed no visual or behavior change, theme values render identically
```

Rationale line: `PATCH from v0.6.4 to v0.6.5, internal refactor, useTheme is internal plumbing not a public export.`

Note: PATCH (not MINOR) because `useTheme` is internal plumbing per the Step 3 internal-vs-public tiebreaker.

### Example 8: Untracked-only first commit (no diff to read)

Diff signal: brand-new repo, files exist but are untracked. `git diff` and `git diff --staged` both empty. `git status --short` shows `?? package.json`, `?? src/index.ts`, `?? tsconfig.json`, `?? .env.example`, `?? .gitignore`, `?? README.md`. `git log` errors with "does not have any commits yet."

Bullets ground in filenames since there is no diff to read.

```
v0.0.1 - Scaffolded the Project with Initial TypeScript Structure

- Added package.json with the base dependencies
- Created src/index.ts as the entry point
- Added tsconfig.json for TypeScript build config
- Added .env.example documenting required environment variables
- Added .gitignore to keep secrets and build output out of git
- Wrote the initial README
```

Two lines above the code block (not one), in this order:
1. `Files are untracked. Staging them by name, then committing.`
2. `Initial commit, defaulted to v0.0.1.`

Claude stages the six paths by name (package.json, src/index.ts, tsconfig.json, .env.example, .gitignore, README.md), runs the commit, then prints `committed <hash>` under the block, per Path B. No `git add .` hand-back: staging a whole folder in one go is what the named-paths rule exists to prevent.

## User Choice Points

Before writing the message, the skill MUST resolve the version bump. Three options:

| Option | When to pick |
|---|---|
| PATCH (x.y.Z+1) | Bug fix, docs, comments, internal refactor with no behavior change visible to callers |
| MINOR (x.Y+1.0) | New feature, new exported symbol, new CLI flag. Repo at 0.y.z also uses MINOR for what would be MAJOR at 1.0.0+ |
| MAJOR (X+1.0.0) | Removal of public API, rename of public symbol, signature change, behavior change callers must adapt to. Only at 1.0.0+ |

Skip the prompt if:
- The user said "patch", "minor", "major", "bug fix", "new feature", or "breaking" in their request
- This is the first commit ever (default to v0.0.1)

Otherwise ASK once: `From v<current>. PATCH (suggested), MINOR, or MAJOR?` Then write the message with the chosen bump.

## Auto-Mode Behavior

If Auto-Mode is active (the session runs unattended) or the user has signaled "do not stop for questions", skip the version-bump prompt and use the suggested bump. State the choice in the rationale line so the user can override on the next turn.

## What To Print

Three output paths, pick one based on Step 1a:

### Path A: Normal commit (happy path)

Three pieces, in this order:

1. One rationale line above the code block: `<BUMP> from v<old> to v<new>, <one-line reason>.`
2. The fenced code block containing the message. Plain triple-backtick fence, no language hint.
3. After executing the commit, the short hash on its own line: `committed <hash>`.

### Path B: Untracked-only first commit

Claude stages the named paths itself, then commits. Three pieces, in this order:

1. `Initial commit, defaulted to v0.0.1.` (or whatever the rationale is)
2. The fenced code block containing the message.
3. After executing the commit, the short hash on its own line: `committed <hash>`.

### Path C: Refusal (clean working tree)

Print the Refusal Template from Step 1a, nothing else. Do NOT produce a message. Do NOT bump a version. Do NOT print a code block.

### Universal rules

Do not print "Here is your commit message:". On a commit path, report the short hash as `committed <hash>` after the commit runs, then stop. Do not print "I have not run git commit"; the commit already ran. Do not print long summaries after. On the refusal path, print only the refusal template.

## How Claude Runs the Commit

Claude commits through a single-quoted heredoc so the multi-line message survives Windows shell quoting; the message body contains no quote characters, so the outer shell owns all quoting. The variants below are the exact mechanism Claude uses, and they double as copy-paste reference if the user ever runs a commit by hand.

### PowerShell (Windows default)

Use a single-quoted here-string. Single quotes prevent variable expansion, the `@'...'@` block preserves newlines, and the closing `'@` MUST sit at column 0:

```powershell
git commit -m @'
v1.4.3 - Fixed Wrong Status Code on /api/leads Validation Error

- Returned 422 instead of 500 when payload missing required fields
- Added regression test covering the missing-email case
- Updated error response shape to include the failed field name
'@
```

### Bash / zsh

Single-quote the whole message. Newlines pass through, no escaping needed:

```bash
git commit -m 'v1.4.3 - Fixed Wrong Status Code on /api/leads Validation Error

- Returned 422 instead of 500 when payload missing required fields
- Added regression test covering the missing-email case
- Updated error response shape to include the failed field name'
```

### Cmd.exe (Windows, not recommended)

Cmd does not handle multi-line `-m` arguments cleanly. Recommend the user switch to PowerShell or use `git commit` without `-m` to open the configured editor and paste there.

### Why this matters

The original PVC format spec wrapped the message body in `"..."`. That worked when typed at a shell prompt but broke on copy-paste because:

1. The inner `"` collided with the outer `git commit -m "..."` double-quote in PowerShell and bash, closing the outer string prematurely.
2. PowerShell parsed the old double-dash bullet lines as the unary decrement operator; the current single-dash bullets avoid that entirely.

The 2026-05-26 format change removed inner quotes from the body so the user controls all shell quoting at paste time.

### No paste block

Do NOT append a "paste with" block after the message. The fenced message block is the whole deliverable. Output ends at the closing fence of the message block. Print one of the shell wrapper variants above ONLY if the user explicitly asks how to paste or run the commit from their shell.

## Local Execution Steps

After producing the message per every rule above, Claude executes the commit
itself in the host project. Install this variant in the repos where the user wants Claude to run
the commit. The steps:

1. Stage NAMED paths for the work at hand. Avoid git add -A unless the
   repo is known-clean; if the repo holds gitignored private folders,
   confirm a private path is ignored before staging near it.
2. Commit via the Bash tool with a heredoc so the multi-line message
   survives Windows shell quoting (a PowerShell here-string works too;
   never single -m lines with embedded newlines).
3. LOCAL ONLY, absolute: never git push, never add a remote, never set an
   upstream. If the host project's CLAUDE.md allows pushing, that rule
   belongs to the project, not to this skill; this skill still never
   pushes on its own.
4. Version bump prompts: in Auto-Mode, use the suggested bump and
   state it in the rationale line (see Auto-Mode Behavior).
5. Report back Path A as usual PLUS the short hash per repo committed.

## Installation

Place this folder at `<repo>/.claude/skills/pvc-git-commit-message-local/` (project-level) or `~/.claude/skills/pvc-git-commit-message-local/` (personal). Restart Claude Code so the skill loads at startup. Verify by asking Claude "What skills are available?" and confirming `pvc-git-commit-message-local` appears with its description.
