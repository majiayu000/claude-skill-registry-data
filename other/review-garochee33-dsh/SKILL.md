---
name: review
description: >-
  Run a reviewer subagent against uncommitted local changes, a named branch,
  or a GitHub PR. Local and branch modes write a review file plus a summary to disk.
  PR mode posts the findings as a PENDING GitHub review for the user to inspect and
  submit through the UI.
when-to-use: "Use when asked to 'review', 'code review', 'review my changes', 'review this PR', or '/review'."
argument-hint: "[--local | --branch <name> | --pr <number-or-url> | <auto-detect>]"
---

# Review Skill

You are an orchestrator that runs a reviewer subagent against one of three review targets. You coordinate only — **all** review findings are authored by a subagent whose prompt is seeded with the `reviewer` persona instructions, never by the orchestrator directly.

## Persona Injection

This skill uses the **reviewer** persona. The persona instructions are defined at:

```
<dirname of this SKILL.md>/../shared/personas/reviewer.md
```

Resolve this path once at the start of the run (the system context gives you the absolute path to this SKILL.md). Read the file with `read_file` and store its contents as `reviewer_persona_instructions`.

When launching the reviewer subagent, **prepend** the persona instructions to the prompt. Do NOT pass a `persona` parameter to `spawn_subagent` — that parameter is not supported.

1. **Local mode (default)** -- uncommitted local changes (staged + unstaged + untracked).
2. **Branch mode** -- the diff between a named branch and its merge-base with the default base branch.
3. **PR mode** -- a GitHub pull request. Findings are posted as a PENDING review for the user to inspect and submit through GitHub.

The reviewer subagent is read-only -- it never modifies code. The orchestrator never edits source either; the only artifacts produced are a review file, a summary file, and (in PR mode) a pending GitHub review.

## Invocation

The user runs:

```
/review                                  # local mode (default)
/review --local                          # local mode (explicit)
/review --branch <name>                  # branch mode (explicit)
/review --pr <number-or-url>             # PR mode (explicit)
/review <plain-arg>                      # auto-detect; see disambiguation below
```

### Argument parsing

Parse the argument string with these deterministic rules, applied in order. The first rule that matches wins; do not fall through.

1. **Empty / whitespace-only**: `MODE=local`, no target.
2. **Starts with `--local`**: `MODE=local`. Reject any extra positional argument with an error.
3. **Starts with `--branch <name>`**: `MODE=branch`, `TARGET=<name>`. The branch name is required -- if the flag appears with no following token (or only with another `--`-prefixed token), reject with `Flag --branch requires an argument: <branch-name>` and stop.
4. **Starts with `--pr <id-or-url>`**: `MODE=pr`, `TARGET=<id-or-url>`. The id or URL is required -- if the flag appears with no following token (or only with another `--`-prefixed token), reject with `Flag --pr requires an argument: <number-or-url>` and stop.
5. **Starts with `--` but does not match any of the above**: reject with `Unknown flag: <flag>. Valid flags: --local, --branch <name>, --pr <number-or-url>.` and stop. Do NOT fall through to auto-detect.
6. **Plain argument given (no flag prefix)**: auto-detect against the rules below, also applied in order:
   1. Matches the regex `^https?://github\.com/[^/]+/[^/]+/pull/\d+(?:[/?#].*)?$` -- treat as PR URL. `MODE=pr`, `TARGET=<url>`.
   2. Matches `^#?\d+$` (optional leading `#`, then pure digits) -- treat as PR number. `MODE=pr`, `TARGET=<digits without leading #>`.
   3. Resolves to a local or remote branch via `git rev-parse --verify --quiet <arg>` or `git rev-parse --verify --quiet origin/<arg>` -- treat as branch. `MODE=branch`, `TARGET=<arg>` (use the bare name, not `origin/<arg>`).
   4. None of the above -- ask the user whether the argument is a PR identifier or a branch name (use the appropriate ask/question tool if available). Provide three options: "PR (treat as PR identifier)", "Branch (treat as branch name)", and "Cancel". On Cancel, stop.

If the user passes both a flag and a positional argument (e.g., `/review --local somebranch`), reject with a clear error message and stop. The flags are mutually exclusive.

## Setup

Generate a unique ID for this run's artifact files. Execute this via `run_terminal_cmd` and capture stdout:

```bash
python3 -c "import uuid; print(uuid.uuid4().hex[:8])"
```

This matches the pattern used by `implement/SKILL.md`. The previous draft of this skill chained two fallbacks (`/proc/sys/kernel/random/uuid` and `date +%s`), but the `/proc` path is missing on macOS and the `date` fallback's `tail -c 9` kept a trailing newline -- both bugs. `python3` is reliably present in the supported environments; if it is genuinely absent, the validation step below catches it with a clear error.

**Validate** that the command produced a non-empty 8-character string. If `REVIEW_ID` is empty or the command failed, report the error to the user (with the suggestion to install Python 3) and stop -- do not proceed with empty/malformed file paths.

Store the output as `REVIEW_ID`. Set a restrictive umask first so all subsequent artifact writes land at mode 0600 -- the diff and review files can capture `.env` snippets or other secrets and the default 0644 leaks them to other users on shared hosts:

```bash
umask 077
```

Then define the file paths used throughout the run:

- `summary_file`: `/tmp/grok-review-summary-${REVIEW_ID}.md` (orchestrator-written; used in local and branch modes only -- not written or read in PR mode)
- `review_file`: `/tmp/grok-review-${REVIEW_ID}.md` (reviewer subagent writes here; produced in all modes)
- `diff_file`: `/tmp/grok-review-diff-${REVIEW_ID}.diff` (collected diff fed to the reviewer; produced in all modes)
- `pending_review_payload`: `/tmp/grok-review-pending-${REVIEW_ID}.json` (PR mode only -- not written or read in local/branch modes, so cleanup of this path is a no-op outside PR mode)

Initialize state variables:

- `mode`: one of `local`, `branch`, `pr` (set by argument parsing).
- `target`: the branch name, PR number, or PR URL (empty in local mode).
- `head_sha`, `base_sha`, `owner`, `repo`, `pr_number`, `pr_url`, `pr_title` (populated in PR mode by Step 1).
- `changed_files`: list of file paths in the diff (populated by Step 1).

## Step 1: Resolve target & collect diff

The diff collection commands differ per mode.

### Local mode

1. Detect changes:

   ```bash
   git status --porcelain
   ```

   If the output is empty, print "No local changes to review (working tree clean)." Skip directly to Step 4 (Cleanup -- use the local/branch sub-case; both `<diff_file>` and the helper file list will be no-op `rm -f` since neither was written yet) and then Step 5 (Final report). The Final report should use the "Local / branch (empty-diff exit)" bullet. Do NOT launch the reviewer.

2. Build a unified diff covering staged + unstaged tracked changes AND untracked files:

   ```bash
   # Staged + unstaged tracked changes (includes deletions and modifications).
   # Guard against fresh `git init` repos with no commits -- `git diff HEAD`
   # fails there with "ambiguous argument 'HEAD'". In that case, leave the
   # tracked-change portion empty and let the untracked loop populate the file.
   # `core.quotepath=false` keeps non-ASCII / space-bearing paths unquoted so
   # the parser in Step 3 PR mode sees literal paths.
   if git rev-parse --verify --quiet HEAD >/dev/null; then
       git -c core.quotepath=false diff HEAD > "${diff_file}"
   else
       : > "${diff_file}"
   fi

   # Append each untracked file as an added-file diff (skip ignored files)
   git ls-files --others --exclude-standard -z | while IFS= read -r -d '' f; do
       git -c core.quotepath=false diff --no-index -- /dev/null "$f" >> "${diff_file}" || true
   done

   # Size check: print the byte count so the orchestrator can gate continuation.
   # See the executable size check handling immediately below.
   wc -c "${diff_file}"
   ```

   Trade-off note: `git diff --no-index` exits with status 1 when differences are present (which is always, here), so we suppress its exit with `|| true`. The alternative -- `git add -N <untracked> && git diff HEAD && git rm --cached <untracked>` -- mutates the index and risks leaving the user in an unexpected state if interrupted; the `--no-index` approach is non-mutating, which is why this block uses it.

   **Fresh-repo guard**: on a brand-new `git init` with zero commits there is no `HEAD` to diff against, so the `if git rev-parse --verify --quiet HEAD` branch above falls through to the `else` and `${diff_file}` starts empty. Everything in the working tree at that point is untracked from git's perspective, so the subsequent `git ls-files --others` loop captures it correctly. The rest of the local-mode flow is unchanged.

   **Size gate (orchestrator-side)**: read the byte count emitted by `wc -c` and act on it:
   - **> 10 MB**: abort with an error telling the user to add the offending paths to `.gitignore` (point them at `git status --porcelain` plus `du -sh` to find the worst offenders -- typical culprits are an untracked `node_modules/`, `.cache/`, `target/`, or a stray dataset). Do NOT launch the reviewer; run cleanup and stop.
   - **> 1 MB**: ask the user to confirm before continuing (use the appropriate ask/question tool if available). On decline, run cleanup and stop. The reviewer subagent has a context limit and a multi-MB diff will saturate it.
   - **otherwise**: proceed silently.

   Edge cases to be aware of (these do not break the workflow, but the user should be told if they apply):
   - **Very large untracked files** (binary blobs, generated artifacts that were never `.gitignore`-d) get appended to `${diff_file}` in full. The size gate above handles this -- the prose here is just a pointer to the executable check above.
   - **Symlinks** surfaced by `git ls-files --others` produce a single `Symbolic link` line in the diff rather than file content; the reviewer can still report on the symlink itself but cannot inspect its target.

3. Capture the changed-files list (same fresh-repo guard as in step 2 -- if there is no `HEAD`, skip the tracked-name listing and rely entirely on `git ls-files --others`):

   ```bash
   {
       if git rev-parse --verify --quiet HEAD >/dev/null; then
           git -c core.quotepath=false diff --name-only HEAD
       fi
       git ls-files --others --exclude-standard
   } | sort -u > /tmp/grok-review-files-${REVIEW_ID}.txt
   ```

   Read this into `changed_files`.

### Branch mode

1. Determine the base branch. Try in order:

   ```bash
   if git rev-parse --verify --quiet origin/main >/dev/null; then
       BASE=origin/main
   elif git rev-parse --verify --quiet origin/master >/dev/null; then
       BASE=origin/master
   else
       BASE=""
   fi
   ```

   Use an explicit `if/elif/else` (not two unconditional `&&` lines) so that `origin/master` does not overwrite `origin/main` when both exist (which happens during master-to-main migrations and on mirror repos). The `>/dev/null` redirect prevents the SHA emitted by `git rev-parse` from leaking into the orchestrator's captured output.

   If `BASE` is empty (neither ref exists), ask the user which base ref to compare against (use the appropriate ask/question tool if available) (offer the local default branch name(s) you can detect via `git symbolic-ref refs/remotes/origin/HEAD`, plus an "Other" option).

2. Verify the target branch exists:

   ```bash
   git rev-parse --verify --quiet "${target}" || git rev-parse --verify --quiet "origin/${target}"
   ```

   If neither resolves, report the error and stop.

3. Compute the merge base and collect the diff (`core.quotepath=false` prevents C-style path quoting so the parser in Step 3 PR mode sees literal paths -- `gh pr diff` does not quote paths, so PR mode is unaffected):

   ```bash
   MERGE_BASE=$(git merge-base "${BASE}" "${target}")
   git -c core.quotepath=false diff "${MERGE_BASE}".."${target}" > "${diff_file}"
   git -c core.quotepath=false diff --name-only "${MERGE_BASE}".."${target}" > /tmp/grok-review-files-${REVIEW_ID}.txt
   ```

4. **Empty-diff handling**: if `${diff_file}` is empty (or contains only whitespace), print "Branch `${target}` has no changes vs `${BASE}`." Skip directly to Step 4 (Cleanup -- use the local/branch sub-case) and then Step 5 (Final report). The Final report should use the "Local / branch (empty-diff exit)" bullet to note that the branch has no changes vs its base. Do NOT launch the reviewer.

   Read `changed_files` from the names file.

### PR mode

1. Verify `gh` authentication:

   ```bash
   gh auth status
   ```

   If this exits non-zero, warn the user that the PR cannot be fetched without `gh` auth, then stop with instructions to run `gh auth login`.

2. Fetch PR metadata in a single round trip (works for both numeric IDs and full URLs). Note that `gh pr view --json` does NOT expose a `baseRepository` field (verified: `gh pr view 1 --json baseRepository` returns `Unknown JSON field: "baseRepository"`. The available repo fields are `headRepository`, `headRepositoryOwner`, and `isCrossRepository`). The owner/repo for the upstream where the PR lives must therefore be derived from the `url` field instead. The `files` field is also requested here so we do not need a second round trip:

   ```bash
   gh pr view "${target}" --json number,title,body,headRefOid,baseRefOid,headRefName,baseRefName,url,headRepository,headRepositoryOwner,isCrossRepository,files \
       > /tmp/grok-review-prmeta-${REVIEW_ID}.json
   ```

   Parse the JSON and populate:
   - `pr_number` from `.number`
   - `pr_title` from `.title`
   - `pr_url` from `.url`
   - `head_sha` from `.headRefOid`
   - `base_sha` from `.baseRefOid`
   - `owner`, `repo` -- parse from `pr_url` using the regex `^https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/pull/\d+`. The URL always points at the upstream where the PR lives, even for cross-repo PRs (`isCrossRepository: true`), so this is the correct source for the review-posting endpoint.
   - `changed_files` -- extract via `jq -r '.files[].path' /tmp/grok-review-prmeta-${REVIEW_ID}.json > /tmp/grok-review-files-${REVIEW_ID}.txt`, then read the file.

   **Validate** that all required fields are non-empty: `pr_number`, `head_sha`, `base_sha`, `owner`, `repo`. If any is missing or empty (which can happen for very old PRs, PRs in unusual states, or partial responses), surface the parsed JSON to the user and stop -- do not proceed to build a payload with `null` fields.

3. Fetch the diff:

   ```bash
   gh pr diff "${target}" > "${diff_file}"
   ```

4. **Empty-diff handling**: if `${diff_file}` is empty, print "PR #${pr_number} has no changes." Skip directly to Step 4 (Cleanup -- use the "PR mode, no reviewer output" sub-case, which removes `<diff_file>`, the prmeta JSON, the files list, and is a no-op on `<review_file>` / `<pending_review_payload>` because neither was written) and then Step 5 (Final report). The Final report should use the "PR (empty-diff exit)" bullet to note that the PR has no changes. Do NOT launch the reviewer.

After Step 1, report progress: "Collected diff for <mode> target <summary>. Launching reviewer..."

## Step 2: Launch reviewer subagent

Launch a single reviewer subagent using the `task` tool.

Task tool parameters:

- `subagent_type`: `"general-purpose"`
- `description`: `"Review: <mode> <target-summary>"` (e.g., `"Review: pr #4221"` or `"Review: branch feature/foo"` or `"Review: local changes"`)

Build the prompt with the mode-specific context. **Prepend the reviewer persona instructions** (loaded during setup) to the prompt. Use this template:

```
<reviewer_persona_instructions>

---

You are reviewing code changes. Mode: <mode>.

Target: <target-summary-line>
<if PR mode: PR URL: <pr_url>>
<if PR mode: head SHA: <head_sha>, base SHA: <base_sha>>
<if branch mode: base: <BASE>, merge-base: <MERGE_BASE>, head: <target>>

The unified diff is at: <diff_file>
The list of changed files is at: /tmp/grok-review-files-${REVIEW_ID}.txt

Read the diff first to understand the scope. The diff alone is often not enough
context, so you should also `read_file` the source files referenced in the diff
to understand call sites, types, and surrounding logic before flagging issues.

Write your structured findings to: <review_file>

Format:

## Summary

<2 to 4 sentence overall assessment of the changes -- what they do, whether
they look correct, the dominant risk areas. This goes at the very top of the
file, before any individual issues.>

## Issues

### Issue 1 -- Severity: bug
- File: path/to/file.ext:LINE
- Description: <what is wrong>
- Suggestion: <how to fix>
- Status: open

### Issue 2 -- Severity: suggestion
- File: path/to/file.ext:LINE
- Description: ...
- Suggestion: ...
- Status: open

Severity must be one of: bug, suggestion, nit. Each issue's Status field must be set to "open" (as shown in the example above).

<if PR mode, include this paragraph verbatim:>
IMPORTANT: For each issue, the File line MUST reference a single line number on
the RIGHT side of the diff (the line number in the new/post-change file, not
the pre-change file). If a finding spans a range, pick the most representative
single line on the RIGHT side. This requirement is mandatory because the
orchestrator will post these findings as inline comments on the GitHub PR, and
the GitHub API rejects comments that do not target a line present in the diff.
<end if>

If the diff is genuinely fine and you have no issues, write the Summary and an
empty `## Issues` section (or omit the Issues section entirely). Do not invent
issues to fill space.
```

Wait for the subagent to complete. If it fails, report the error to the user and stop.

After it completes, verify that `<review_file>` exists and is non-empty. If it does not, report the error and stop.

Save the returned `subagent_id` for the report. The reviewer is not resumed; this is a one-shot review.

Report progress: "Review complete. Processing findings..."

## Step 3: Handle output based on mode

The post-processing differs between local/branch mode (write summary to disk) and PR mode (post pending review to GitHub).

### Local / Branch mode

1. Read `<review_file>` via `read_file`.
2. Count issues by counting heading lines that match the regex `^### Issue \d+ -- Severity: (bug|suggestion|nit)$` and bucket them by the captured severity. Issues whose heading does not match this pattern (typo'd severity, missing severity field, malformed heading) are malformed -- log a one-line warning to the user listing the heading line and treat them as uncounted. Do not attempt to re-parse the body for a `Severity:` field; the heading is the canonical source. The same regex governs the parsing in Step 3 PR mode below.
3. Compute diff stats:

   ```bash
   git diff --shortstat ...     # local: HEAD; branch: MERGE_BASE..target
   ```

   For local mode, run `git diff --shortstat HEAD` and also count untracked files separately. For branch mode, run `git diff --shortstat "${MERGE_BASE}".."${target}"`.

4. Use the `write` tool to create `<summary_file>` with this structure:

   ```markdown
   # Review Summary

   - **Mode**: <mode>
   - **Target**: <target-summary>
   - **Files reviewed**: <count> (<list, truncated to 10 if longer>)
   - **Diff stats**: <shortstat-line>
   - **Issue counts**: <X> bugs, <Y> suggestions, <Z> nits

   ## Top issues

   <First 5 issue titles, one per line, in the form "[severity] file:line -- description (truncated to ~100 chars)">

   See the full review at: <review_file>
   ```

5. Print to the user:
   - Inline issue counts and the file paths to `<review_file>` and `<summary_file>`.

Do NOT delete `<review_file>` or `<summary_file>` in local/branch modes -- those files ARE the deliverable.

### PR mode

1. Read `<review_file>` via `read_file` and parse it into a structured representation:
   - Extract the `## Summary` section -- everything after the `## Summary` heading and before the next `## ` heading.
   - Extract each issue by matching heading lines against `^### Issue \d+ -- Severity: (bug|suggestion|nit)$` (same regex as Step 3 Local/Branch mode). For each matched block, capture:
     - `severity` -- the captured group from the heading regex
     - `file` and `line` -- parsed from the `- File: path:line` field. If `:line` is missing, the issue cannot become an inline comment; it must be promoted to the body.
     - `description` -- from the `- Description:` field
     - `suggestion` -- from the `- Suggestion:` field (may be empty)

   **Early-exit on zero issues**: if the parsed issue list is empty, do NOT walk the diff, do NOT build a payload, and do NOT post anything to GitHub. Posting an empty PENDING review is wasteful, looks spammy on the PR, and gives the user a "submit your review" reminder for a review with nothing in it. Instead:
   - Print: "Reviewer found no issues on PR #${pr_number}. No PENDING review created."
   - Skip directly to Step 4 (Cleanup) and then Step 5 (Final report). The Final report should note that no PENDING review was posted.

2. Read `<diff_file>` via `read_file` and walk it to determine which `(file, line)` pairs are present on the RIGHT side of any hunk. The line is on the RIGHT side when:
   - It is an added line (prefix `+`, but not the `+++ b/...` header line), OR
   - It is a context line (prefix ` `).

   Walk the diff file by file:
   - Each file section starts with `+++ b/<path>` (treat `+++ /dev/null` as a deletion -- skip).
   - Within a file, each hunk starts with `@@ -<old>[,<oldcount>] +<new>[,<newcount>] @@`. The `,<count>` parts are optional and default to `1` when omitted (so `@@ -42 +42 @@` is a valid single-line hunk that `git diff` and `gh pr diff` both emit). A regex like `^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@` matches both forms; capture `<new>` from the second group. Reset the right-side line counter to `<new>`. (The regex is intentionally unanchored at the end -- real diffs frequently carry trailing context after the second `@@`, e.g. `@@ -10,5 +15,3 @@ def my_function():`, and `re.match` succeeds on the prefix without a `$` anchor. Do NOT add `$`; it would reject every hunk header that includes a function/class hint.)
   - Walk the hunk body. For ` ` (context) and `+` lines (excluding `+++` headers), record the current right-side line and increment the counter. For `-` lines (excluding `---` headers), do not increment the right-side counter.
   - Lines starting with `\ ` (a literal backslash followed by a space) are diff metadata, not file content -- e.g., `\ No newline at end of file`. Skip them: do not increment the right-side counter, and do not contribute a `(file, line)` pair.

   Build a set of `(file, line)` pairs.

3. Partition the parsed issues into two groups:
   - **Inline comments**: issues whose `(file, line)` is in the diff set.
   - **Promoted to body**: issues whose `(file, line)` is missing or not in the diff set.

4. Build the JSON payload via the `write` tool, saving to `<pending_review_payload>`:

   ```json
   {
     "commit_id": "<head_sha>",
     "body": "<assembled body, see below>",
     "comments": [
       {
         "path": "src/foo.rs",
         "line": 42,
         "side": "RIGHT",
         "body": "**[bug]** description text\n\n**Suggestion:** suggestion text"
       }
     ]
   }
   ```

   **Do NOT include the `event` field.** Omitting `event` causes the GitHub API to create the review in PENDING state, which is exactly what we want -- the user reviews and submits it through the GitHub UI.

   The top-level `body` is constructed as:

   ```
   ## Summary

   <verbatim text of the ## Summary section from the review_file>

   ## Issue counts by severity

   - bugs: <X>
   - suggestions: <Y>
   - nits: <Z>

   <if any promoted issues exist, append:>
   ## Issues outside the diff

   These findings reference lines that are not present in the diff and could not be posted as inline comments:

   - **[severity]** file:line -- description
     - **Suggestion:** suggestion text
   <repeat for each promoted issue>
   <end if>
   ```

   Each inline comment body has the form `**[severity]** description\n\n**Suggestion:** suggestion`. If the suggestion is empty, drop the suggestion line.

   **Construct the payload as a Python dict, then serialize via `json.dumps`.** Do NOT concatenate JSON strings by hand: review text routinely contains `"`, `\`, or embedded newlines, and naive concatenation produces invalid JSON which `gh api` rejects with 400/422. Run a short `python3` heredoc to materialize the JSON string and persist it to `<pending_review_payload>` through the `write` tool:

   ```bash
   python3 <<'PY'
   import json
   payload = {
       "commit_id": "<head_sha>",
       "body": "<assembled body>",
       "comments": [
           {
               "path": "src/foo.rs",
               "line": 42,
               "side": "RIGHT",
               "body": "**[bug]** description text\n\n**Suggestion:** suggestion text",
           },
           # ... one entry per inline comment
       ],
   }
   print(json.dumps(payload, ensure_ascii=False, indent=2))
   PY
   ```

   `json.dumps(payload, ensure_ascii=False, indent=2)` handles all quote, backslash, and newline escaping automatically. Capture the printed JSON and pass it as the `content` argument to the `write` tool with `<pending_review_payload>` as the file path.

5. Post the review:

   ```bash
   gh api "repos/${owner}/${repo}/pulls/${pr_number}/reviews" \
       -X POST \
       --input "${pending_review_payload}" \
       > /tmp/grok-review-post-${REVIEW_ID}.json 2> /tmp/grok-review-post-${REVIEW_ID}.err
   ```

   Capture both stdout and stderr.

6. **Error handling**: if the `gh api` call exits non-zero, surface the captured stderr verbatim to the user along with the HTTP status code (parseable from `gh api`'s stderr message). Do not retry. Common cases by status:
   - **422 Unprocessable Entity**: comments reference lines outside the diff (the diff-line filter missed something, e.g., the reviewer hallucinated a file path), `commit_id` is stale (the PR was force-pushed between Step 1 and now), or the `side` value was rejected.
   - **403 Forbidden**: authenticated user lacks permission to comment on the PR (read-only collaborator on the repo, archived repo).
   - **404 Not Found**: PR does not exist (the user passed a wrong number, or the URL is in a private repo the user cannot see).
   - **5xx**: GitHub-side outage or transient failure.

   On any error, also keep `<review_file>` on disk (skip the PR-mode review_file deletion in Step 4) so the user can see what would have been posted and either re-run with corrected inputs or submit the notes through some other channel. Mention the preserved path in the error message.

7. On success, the user-facing pending-review URL is the PR Files tab, where pending reviews surface and where the "Finish your review" / "Submit review" button lives:

   ```
   https://github.com/<owner>/<repo>/pull/<pr_number>/files
   ```

   Construct this URL from the already-validated `owner`, `repo`, and `pr_number` -- do NOT use the `html_url` field from the GitHub response. The response's `html_url` points at a deep link to the review object that does not surface the submit button as cleanly as the Files tab. (The response is still parsed for the review `id`, which is recorded in the Final report; the `html_url` field is not used.)

   Print to the user as a structured block (not a wall of text):

   ```
   A PENDING review has been created on PR #<pr_number>.
   - Inline comments: <N>
   - Body findings (outside the diff): <M>
   - Submit at: https://github.com/<owner>/<repo>/pull/<pr_number>/files
     (scroll to "Finish your review" -> click "Submit review").
   Until you submit, the comments are visible only to you.
   ```

## Step 4: Cleanup

The cleanup behavior is **asymmetric** by mode and by outcome:

- **Local and branch modes**: keep `<review_file>` and `<summary_file>` -- they are the deliverable. Remove only `<diff_file>` and the `/tmp/grok-review-files-${REVIEW_ID}.txt` helper file.
- **PR mode, successful post**: remove `<review_file>`, `<diff_file>`, `<pending_review_payload>`, `/tmp/grok-review-prmeta-${REVIEW_ID}.json`, `/tmp/grok-review-files-${REVIEW_ID}.txt`, and the post stdout/stderr capture files. The pending review on GitHub is the deliverable; the local files are no longer needed. `<summary_file>` was never written in PR mode, so no action there.
- **PR mode, failed post (any non-zero `gh api` exit)**: keep `<review_file>` so the user can see what would have been posted and submit it through some other channel. Remove the rest as in the success path. The Final report must mention the preserved path.
- **PR mode, no reviewer output (covers both zero-issue early-exit AND PR-with-empty-diff exit)**: remove all of `<diff_file>`, `<pending_review_payload>` (never created -- `rm -f` is a no-op), `/tmp/grok-review-prmeta-${REVIEW_ID}.json`, `/tmp/grok-review-files-${REVIEW_ID}.txt`, and `<review_file>` (which is a no-op in the empty-diff case where the reviewer never ran, and removes the empty-of-actionable-content file in the zero-issue case). This sub-case is the catch-all for any PR-mode exit that did not POST to GitHub.

Cleanup commands:

```bash
# Local / branch mode (always -- covers both successful-review and empty-diff-exit cases;
# the empty-diff exit happens before <diff_file> contains anything useful, but rm -f is a no-op
# on a non-existent or already-empty file)
rm -f "${diff_file}" /tmp/grok-review-files-${REVIEW_ID}.txt

# PR mode, successful post
rm -f "${review_file}" "${diff_file}" "${pending_review_payload}" \
      /tmp/grok-review-prmeta-${REVIEW_ID}.json \
      /tmp/grok-review-files-${REVIEW_ID}.txt \
      /tmp/grok-review-post-${REVIEW_ID}.json \
      /tmp/grok-review-post-${REVIEW_ID}.err

# PR mode, failed post -- omit "${review_file}" from the rm command
rm -f "${diff_file}" "${pending_review_payload}" \
      /tmp/grok-review-prmeta-${REVIEW_ID}.json \
      /tmp/grok-review-files-${REVIEW_ID}.txt \
      /tmp/grok-review-post-${REVIEW_ID}.json \
      /tmp/grok-review-post-${REVIEW_ID}.err

# PR mode, no reviewer output (zero-issue early-exit OR empty-diff exit)
rm -f "${review_file}" "${diff_file}" "${pending_review_payload}" \
      /tmp/grok-review-prmeta-${REVIEW_ID}.json \
      /tmp/grok-review-files-${REVIEW_ID}.txt
```

## Step 5: Final report

Present a final report to the user. Item 1 is always included; item 2 is omitted on empty-diff exits; item 3 is omitted on empty-diff exits and on PR zero-issue early-exits; item 4 is always included.

1. **Mode + target** -- e.g., "Local changes" or "Branch feature/foo vs origin/main" or "PR #4221: <pr_title>".
2. **Files reviewed** -- count and (if 10 or fewer) the list. Omit on empty-diff exits.
3. **Issues by severity** -- the bug/suggestion/nit counts. Omit on empty-diff exits and on PR zero-issue early-exits (counts are all zero by construction; the mode-specific bullet says so).
4. **Mode-specific output**:
   - Local / branch (successful review): full paths to `<review_file>` and `<summary_file>`, plus a one-line copy of the summary's top-issues list.
   - Local / branch (empty-diff exit): "No changes to review." (local mode) or "Branch <target> has no changes vs <BASE>." (branch mode). No file paths -- nothing was written.
   - PR (successful post): the structured submit block from Step 3 PR mode item 7 (PR number, inline-comment count, body-findings count, Files-tab URL, submit reminder), plus the review `id` from the response (for traceability).
   - PR (zero-issue early-exit): "Reviewer found no issues on PR #<pr_number>. No PENDING review created."
   - PR (empty-diff exit): "PR #<pr_number> has no changes. Nothing to review."
   - PR (failed post): the verbatim stderr from `gh api` plus the HTTP status code, plus the preserved path to `<review_file>` so the user can recover the findings.

## In-Progress Reporting

Give the user a brief status update after each phase:

- After argument parsing: "Reviewing <mode> target: <target-summary>." (omit target for local mode -- "Reviewing local changes.")
- After Step 1 (diff collection): "Collected diff (<N> files, <M> changed lines). Launching reviewer..."
- After Step 1 (empty diff): "No changes to review. Proceeding to final report."
- After Step 2 (reviewer complete): "Review complete. Processing findings..."
- After Step 3 (local / branch): "Found N issues (X bugs, Y suggestions, Z nits). Wrote <review_file> and <summary_file>."
- After Step 3 (PR, zero issues): "Reviewer found no issues on PR #<pr_number>. No PENDING review created."
- After Step 3 (PR, success): "Posted PENDING review with N inline comments and M body findings. Visit <url> to submit."
- After Step 3 (PR, error -- 422 or any other non-zero exit): "Failed to post pending review. HTTP <status>. GitHub returned: <verbatim stderr>. Review notes preserved at <review_file>."

## Rules

- **Reviewer is read-only** -- the reviewer subagent must never modify files. The orchestrator must never modify source files either. The only writes are to `<review_file>`, `<summary_file>`, `<diff_file>`, `<pending_review_payload>`, and the GitHub PENDING review.
- **Inject the reviewer persona into the prompt** -- always prepend the `reviewer` persona instructions (from the shared personas file) to the subagent prompt. Do NOT pass a `persona` parameter to `spawn_subagent`.
- **Include context in the reviewer prompt** -- the reviewer needs the conversation context (the user's framing, any constraints, etc.) passed through the task prompt.
- **One reviewer per run** -- this skill runs a single reviewer. Multi-reviewer runs are the job of `/implement` with `--effort N`.
- **Disambiguation is deterministic** -- the auto-detect rules in argument parsing are applied in order. Do not second-guess them. If the rules do not match, ask the user; do not guess.
- **Empty diffs short-circuit** -- never launch the reviewer with an empty diff. Report "no changes", run cleanup, and produce a Final report (using the appropriate "empty-diff exit" bullet).
- **Zero issues short-circuits PR mode** -- if the reviewer finds nothing on a PR, do not post an empty PENDING review. Print a "no issues found" message, clean up, and stop.
- **PR mode requires `gh` auth** -- if `gh auth status` fails, stop with a clear instruction to run `gh auth login`. Do not try to work around it.
- **PENDING reviews are the user's to submit** -- the orchestrator never sets the `event` field on the review payload. The user reviews and submits via the GitHub UI. Always print the URL plus the submit-via-UI reminder.
- **Filter inline comments to lines actually in the diff** -- GitHub returns 422 for comments on lines outside the diff. The orchestrator parses the diff itself to validate `(file, line)` pairs and promotes any out-of-diff issues to the top-level body as bullet points.
- **Surface every `gh api` error verbatim** -- if the GitHub API call exits non-zero (422, 403, 404, 5xx, anything else), do not retry. Show the user the raw stderr plus the HTTP status code so they can debug, and preserve `<review_file>` on disk so the findings are not lost.
- **No helper script** -- the orchestrator does the diff parsing and JSON building inline.
- **Cleanup is asymmetric by mode and outcome** -- local/branch modes keep `<review_file>` and `<summary_file>` (they are the deliverable). PR mode removes `<review_file>` on a successful post (the pending GitHub review is the deliverable) and on a no-reviewer-output exit (zero issues OR empty diff -- nothing actionable to preserve), but preserves it on a failed post so the user can recover the findings.
- **Thread the same file paths** across all steps -- never regenerate paths between steps. The `REVIEW_ID` is fixed for the run.
- **Error handling** -- if the reviewer subagent fails, the diff collection fails, or the GitHub API call fails, report the error to the user and stop. Do not silently continue with missing results.
- **No emojis in output** -- match the conventions of the `reviewer` persona instructions and the surrounding skills.

## Design notes

These are background notes that explain the rationale behind some of the choices above. They are NOT rules; they are pointers for future maintainers.

- **No helper script.** The markdown parsing of `<review_file>` and the unified-diff hunk walk are well-defined and small enough to do directly in the orchestrator (using `read_file` to load the inputs and `write` to create the JSON payload). This follows the same self-contained pattern as `xai-pr-comments`. If a future maintainer finds the inline approach genuinely intractable -- e.g., the parser is consistently miscounting hunks across many real-world PRs -- a helper at `.grok/skills/review/scripts/build_pending_review.py` could be added with a clear justification. As of this writing, no such helper exists.
- **Owner/repo are derived from the PR `url`, not from a `baseRepository` field.** `gh pr view --json baseRepository` returns `Unknown JSON field: "baseRepository"` -- only `headRepository`, `headRepositoryOwner`, and `isCrossRepository` are exposed. Parsing the URL is the simplest universal approach and works correctly for cross-repo PRs.
- **The constructed `/files` URL is used in user output, not the response's `html_url`.** The Files tab is where the "Finish your review" / "Submit review" button surfaces in the GitHub UI; that is what the user actually needs to interact with. The response's `html_url` deep-links to the review object and is less useful for this workflow.
