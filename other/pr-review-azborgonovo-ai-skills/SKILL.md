---
name: pr-review
description: >
  Reviews a merge request or pull request against its linked work item, publishes the findings as
  inline comments on the diff, and records the verdict on the change. It fetches the change and the
  work-item context, isolates the change locally, hands the review itself to the review-changes
  skill, posts each finding, and then approves the change or requests changes according to that
  verdict. It ships with adapters for GitLab and GitHub as the code host, and Jira and GitHub Issues
  as the tracker. For any other host or tracker, it degrades to whatever tool discovery can reach.
  This skill is user-only: it runs only when the user invokes /pr-review <MR or PR URL>. When the
  user wants to review a GitLab MR or a GitHub PR, code-review a merge request or pull request, or
  evaluate the diff of a change against its linked work item, suggest this command instead of a
  manual review.
argument-hint: "<merge/pull request URL> [draft|comments-only]"
allowed-tools: [Read, Bash, Skill, Write, Glob, Grep, ToolSearch]
disable-model-invocation: true
---

# PR/MR Review

The review lands on the change itself. The author sees inline comments, and the host records the verdict as an approval or a request for changes.

## What this skill owns

The review itself belongs to the [review-changes](../review-changes/SKILL.md) skill. That skill reviews the diff between `HEAD` and a fixed point across the Code Review Pyramid. It checks the change against its spec, and against the repo's documented standards. It splits the findings into blocking and non-blocking, and it resolves them into one verdict. None of that judgment is repeated here. This skill supplies the four things that review-changes cannot reach from a URL alone:

- It resolves the change and its work item, through host and tracker adapters.
- It isolates the change locally, so the review reads real files at the exact head SHA of the change.
- It renders the findings as inline comments anchored to the diff.
- It turns the verdict into the host's approve action or request-changes action.

Two generic terms run through this skill. A "change" is what the host calls a merge request on GitLab, or a pull request on GitHub and Bitbucket. A "work item" is whatever the tracker holds, such as a Jira issue or a GitHub issue. The mechanics for a specific host or tracker live in adapter files under `references/`. Each one loads only when you reach the step that needs it, so the always-loaded body stays host-agnostic.

## Modes

The word after the URL chooses how much of the review lands on the change. With no word, both parts land.

| Invocation | Comments | Verdict |
|---|---|---|
| `/pr-review <url>` | published directly | Approved or Approved with suggestions, so **approve**. Request changes, so **request changes** |
| `/pr-review <url> comments-only` | published directly | reported in the conversation only |
| `/pr-review <url> draft` | drafts for the user to submit | reported in the conversation only |

**Self-authored changes**: both hosts reject a verdict from the author of the change. Step 2 compares the author against the authenticated user, and drops to `comments-only` when they match. Say so in the output of Step 8. The verdict is still worth reading, and the host cannot record it.

## Workflow

### Step 1: Identify the host and load its adapter

Determine which host holds the change, mainly from the shape of the URL:

- A URL that contains `…/-/merge_requests/<n>` is GitLab. Read `references/hosts/gitlab.md`.
- A URL that matches `github.com/<owner>/<repo>/pull/<n>` is GitHub. Read `references/hosts/github.md`.

The adapter file is the authority for the mechanics of that host. It covers URL parsing, the auth check, and the exact calls that fetch metadata and diffs. It covers the shape of the local clone path, how to post comments in either mode, and how to record a verdict. It also covers the gotchas of that host. Read it now, and follow it wherever a later step says "per the host adapter".

When no adapter file exists for the host in front of you, degrade instead of stopping. Discover the relevant tools with a keyword `ToolSearch`, or with the platform's CLI or API. Make sure that the fetch-metadata, fetch-diff, and post-comment operations you need exist. Then run in `comments-only` mode. Recording a verdict through an interface you have not verified is the one part that is not worth improvising. Tell the user that you are running without a dedicated adapter, so they know that host-specific behavior is best-effort.

### Step 2: Fetch change metadata

Use the metadata call from the host adapter. Fetch the title, the description, and the author of the change. Fetch its source branch and target branch, the SHAs that inline comment positions need, the checks or pipeline status, and the web URL.

Compare the author against the authenticated user. The adapter names both calls. On a match, the run is a self-review, so switch to `comments-only` for the rest of the workflow.

**If the metadata call fails with an auth error**, the CLI or tool that the host adapter names is not authenticated. An auth error is a 401, or a "not logged in" message. Stop and ask the user to authenticate, and quote the exact command from the adapter. Do not pre-check auth separately. A success here also proves that auth works for posting in Step 6, because both use the same credentials.

### Step 3: Resolve the work item and save it as the spec

Scan the title and the description for a work-item reference:

- A Jira key, which matches the regex `[A-Z][A-Z0-9]+-\d+`, bare or inside a full `…atlassian.net/browse/<KEY>` URL. Read `references/trackers/jira.md`.
- A GitHub issue reference. That is a full `github.com/<owner>/<repo>/issues/<n>` URL, a cross-repo `<owner>/<repo>#<n>` reference, or a bare `#<n>` when the change sits on GitHub in the same repo. Read `references/trackers/github.md`.

A full URL names its tracker without ambiguity, so prefer it over a bare key or number when both appear. The tracker is independent of the code host. A GitLab MR can reference a GitHub issue for its requirements, and the reverse also happens.

The tracker adapter is the authority for fetching that work item. It covers how to load or authenticate its tools, the exact call that fetches the item, and the fields to extract. Those fields are the summary, the description or acceptance criteria, and the issue type. Read it now, and follow it as "per the tracker adapter".

Write what you fetched to `${TMPDIR:-/tmp}/<change-id>-work-item.md`, word for word. Write the summary, the description, the acceptance criteria, and the URL of the work item. Step 5 hands that path to review-changes as the spec. A file keeps the requirements in the tracker's own words, and a paraphrase loses the exact wording that a conformance check needs.

When no adapter exists for the tracker in front of you, degrade the same way as in Step 1. When you find no work-item reference at all, or the fetch fails, continue with no spec file. review-changes then reports the review as spec-less, and the output of Step 8 carries the caveat that nobody assessed conformance.

### Step 4: Isolate the change in a review worktree

A checkout of the change in the user's main clone switches what is checked out under them. It disrupts the branch or the uncommitted work that they hold there. A disposable worktree, detached at the head SHA of the change, gives the review its own directory instead. A detached checkout also cannot collide with a branch that the user has checked out somewhere else.

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(readlink -f "<skill_dir>/SKILL.md")")")}"
python3 "$PLUGIN_ROOT/scripts/setup_workspace.py" \
  --repo-path <repo_path> --purpose review --change-id <mr_iid or pr_number> \
  --source-branch <source_branch> --target-branch <target_branch> --detach-sha <head_sha>
```

Use `python` in place of `python3` when `python3` is not on `PATH`. Some native Windows installs carry only one of the two.

The first line resolves the shared helper at the plugin root, in either install mode. `<repo_path>` is the relative shape that the host adapter states, which is the namespace for GitLab and `owner/repo` for GitHub. The script searches common project roots, and then searches by remote URL, because no single clone location is standard enough to assume. The `--target-branch` flag fetches the diff base too, which is what makes the fixed point in Step 5 resolvable locally.

On success the script prints `MODE: worktree`, then `WORKSPACE_PATH: <path>`. A review always detaches, so the mode is always `worktree` here. Use that path for every read, every `grep`, and every `git` call from here on. On a refusal, the script prints `STOP: <reason>` and exits non-zero. A refusal happens when a leftover worktree is dirty or unpushed, or when the script cannot find the clone. Never force past a refusal, and never fall back to a checkout of the change in the user's main clone. When the script cannot locate the clone, ask the user for the path, and re-run with `--repo-root <path>` in place of `--repo-path`.

With no worktree, the review is diff-only. Fetch the diff of every changed file per the host adapter, including its truncation check, and write it to `${TMPDIR:-/tmp}/<change-id>.diff`. Step 5 hands that file over in place of the worktree. Step 8 carries the limitation as a caveat, because with no working tree you cannot settle any claim by running the code.

### Step 5: Hand the review to review-changes, then come straight back

Invoke the `review-changes` skill through the Skill tool, with `skill: "review-changes"`. Pass these six things:

- **The worktree path**, with the instruction to run every git command as `git -C <worktree_path>`. The working directory of the shell is still the user's main clone. A review that silently diffs the wrong repo is the one failure mode here worth spelling out.
- **The fixed point**, which is the base SHA from Step 2. The target branch also works, because review-changes diffs with three dots, so either input resolves to the merge base. In diff-only mode there is no working tree to diff, so hand over `${TMPDIR:-/tmp}/<change-id>.diff` as the already-captured diff, and say that you did.
- **The spec**, which is the `${TMPDIR:-/tmp}/<change-id>-work-item.md` path from Step 3. When there is no spec, say that there is none.
- **The test signal**, which is the checks or pipeline status from Step 2, passed as the CI result to report. This is someone else's repo, freshly fetched, so report the host's verdict instead of building and running its suite unprompted.
- **Where the report goes**, which is `${TMPDIR:-/tmp}/<change-id>-review.md`, written as a file instead of printed in the conversation. The output of Step 8 is the only review that the user has to read. A report printed here says the same thing twice, and the second copy does not know what actually reached the author.
- **How long each finding can run**, which is the finding-length budget of review-changes, set here to 2 to 4 sentences of continuous prose per entry. Each entry names the symbol, states the concrete problem, and then gives the fix or the question. Step 6 posts those entries word for word as the inline comments. A requested change asserts the problem and prescribes the fix. A suggestion reads as something the author can decline, and it often works best as a direct question when the code can be deliberate. Go past one tight paragraph only when the failure mechanism needs the room. A concurrency race, a security hole, and a scope change that spans callers all need the room. Two things sit outside that budget. The first is a word-for-word quote of an unmet acceptance criterion. The second is a fenced code block that carries the corrected expression, when the fix is shorter to show than to describe.

**review-changes runs inside this workflow, not in place of it.** Its process is numbered independently of this one, and it ends in a step called "Report". Writing the file above satisfies that step, and it is not the end of the run. Read the file back and go straight into Step 6 in the same turn. Publishing is what this skill exists to do, and a review that stops at the report has produced nothing that the author can see.

That report is the review of record. It holds the verdict, the split between blocking and non-blocking, the spec accounting, and the list of what the review checked and found clean. Steps 6 through 8 turn that report into comments, a verdict action, and output. They do not review the change again.

### Step 6: Post the findings per the host adapter

Every finding that review-changes reported becomes one note object. Its text is **the entry as review-changes wrote it, word for word**, including the layer tag and the `file:line` citation. Do not re-draft, expand, re-explain, or trim it. The report and the change must say the same thing, and a rewrite here reliably comes out longer than the entry it replaced. Strip only the list number, which belongs to the report's ordering and means nothing on a standalone comment. Then promote a fenced code block into the host's suggestion syntax, where the rules below allow it.

Keep the citation even though the anchor points at the same line, because the anchor can fail to survive. When a host cannot resolve a position, it re-posts the same text with no position, through the `line_code` path of GitLab described in the adapter. A comment that lost its anchor is exactly the comment that has to name its own file and line.

So a report entry that reads

```
1. **[Impl. Semantics]** `svc/user.go:47` — `fetchUser` does not handle the case where the DB returns `null`, so the `.Name` access will panic at runtime. Add a nil check or return an early error.
```

posts as

```
**[Impl. Semantics]** `svc/user.go:47` — `fetchUser` does not handle the case where the DB returns `null`, so the `.Name` access will panic at runtime. Add a nil check or return an early error.
```

An entry too long to read as an inline comment is an entry to shorten in *both* places. Go back and tighten it in the report, instead of posting one length and reporting another.

**Anchors**: a finding cited as `file:line` becomes an inline note, with `new_path` plus `new_line`. A cross-cutting finding with no single site becomes `"general": true`, rather than a note pinned to a misleading line. `new_line` must be a line that this change added. Find it with `grep -n '<snippet>' <worktree_path>/<file>` instead of counting diff lines. Then make sure that it carries a `+` in `git -C <worktree_path> diff <base_sha>...HEAD -- <file>`. A finding that lands on an unchanged line anchors to the nearest added line, or it goes general. Both host scripts reject or downgrade an anchor that the diff does not contain.

**Suggested changes**: both hosts render a fenced `suggestion` block inside an inline comment as a patch that the author applies in one click. A finding whose fix is an exact replacement of the lines its comment anchors to belongs in one of those blocks. The adapter gives the syntax for that host. The block carries the whole replacement: the original indentation, code that is valid on its own, and nothing left for the author to fill in. Read the block word for word out of the worktree, instead of reconstructing it from the diff. Prose stays the right answer in four cases. The first is a fix that spans several files or non-contiguous lines. The second is a finding that the author has a genuine choice about. The third is anything that lands as a general comment, because the block is inert outside the diff. The fourth is diff-only mode, where no worktree exists to read the current line from.

**What stays out of the comments**: the summary paragraph, the "checked and clean" list, and the path to merge all belong to the Step 8 output in the conversation. Skip a suggestion that no author will act on, such as a style nit that automation must catch. Where the same finding recurs across files, post the clearest occurrence once.

**The verdict summary**: only a Request changes verdict in the default mode posts one. GitHub requires a body on that event, and GitLab has nowhere else to state the verdict. Write the one thing that the author needs to act on, and do not write a second copy of the review:

```
I did not approve this <merge request | pull request> yet because <the blocking finding, in one sentence>. <Why that blocks: the defect that will reach production, the contract broken for callers, or the acceptance criterion left unmet.> <Where the detail is: the inline comment on `<file>`, or "the N inline comments" when there are several.>
```

Write two or three sentences, with no headings and no lists. The inline comments carry the mechanism. The suggestions, the "checked and clean" list, and the path to merge stay in the Step 8 output. Write the summary to `${TMPDIR:-/tmp}/<change-id>-summary.md`, and pass it as `--summary-file`. The script marks it, so leave the 🤖 off.

Write the summary in short sentences and the active voice, define a term that the author can miss at its first use, and cut filler. Where that pulls against the two-sentence-to-three-sentence limit above, the limit wins. When a plain-English writing skill such as `simple-english` is available, invoke it and apply its rules to the summary. The findings need no pass here, because review-changes already wrote them in plain English and this step posts them word for word.

The host adapter names the bundled script that posts the notes, which is `scripts/post_review_notes_gitlab.py` or `scripts/post_review_notes_github.py`, relative to this SKILL.md. It also gives the exact invocation for the mode that Step 2 settled on. Both scripts read the same notes-file JSON shape, so the notes file does not change with the host. Both mark each comment and the verdict summary with a trailing 🤖. Both publish the comments before they touch the verdict, so an approval never lands without its reasoning. Both skip a finding that this account already published, instead of deleting it or duplicating it. Leave the marking to the script, because a mark you write yourself can land twice.

Read the script's tally afterward. It reports what was posted, what was skipped as already present, and what the verdict action did. Step 8 reports all three.

### Step 7: Remove the worktree

Remove the worktree that this run created, even when an earlier step failed partway, such as a posting error or an abandoned review. When Step 4 hit its STOP check, this run created no worktree, so leave the existing one untouched.

```bash
git -C <repo_path> worktree remove "<worktree_path>"
```

If git refuses the removal, leave the worktree in place. Tell the user exactly what git reported, so they can decide what to do with it.

### Step 8: Output the review

Output the full review in the conversation. The change carries the comments and the verdict, and it does not carry the reasoning around them. Step 5 kept the report of review-changes in a file, so this output is the only review that the user reads. It has to stand on its own. Lead with the verdict from review-changes, keep its lists as it wrote them, and add what only this skill knows: where the change and the work item live, what the author will see, and where the attention of a human is worth spending.

```markdown
## <Approved | Approved with suggestions | Request changes>

**Change**: [<title>](<web_url>)
**Work item**: [PROJ-123](<work_item_url>) — <work item summary>
*(or "No work item linked. Reviewed without requirements context.")*

<the summary paragraph from review-changes, plus any caveat this skill added: a diff-only review, a truncated diff, N of M files reviewed, or a diff too large to review at full depth>

### Requested changes
1. **[Impl. Semantics]** `svc/user.go:47` — <finding> *(posted inline)*

### Suggestions
1. **[Code Style]** `svc/user.go:12` — <finding>

### Checked and clean
<what review-changes checked, and how it established each result>

### Worth your own look
- `<file>`[, `<file>`, ...] — <one-clause reason. Group files that share a reason into one line.>

### Path to merge
1. <the requested changes, in the order worth addressing them>

### On the change
- <N comments published inline, M in the conversation, K skipped as already posted. In draft mode, N drafts awaiting submission.>
- <the verdict action taken, or why none was taken: comments-only mode, a self-authored change, or a 409 on a moved head>
- <the reversal or submit line from the closing lines of the host adapter>
```

**Marking posted findings**: tag each finding that reached the change with *(posted inline)* or *(posted to the conversation)*. Tag each finding that the script skipped with *(already on the change)*. That marking is the only way the reader can tell what the author sees from what stayed between the two of you.

**Worth your own look**: name the files where the independent judgment of a human pays off most, whatever the AI found there. Two kinds qualify. The first kind defines or changes a public contract that other code depends on. That contract is an interface, an exported type, or a signature that callers rely on. The second kind carries business-rule logic, such as a branch that encodes a business decision, a state transition, or orchestration across domain concerns. Judge by the role that a file plays, not by its path or its language. A controller with real branching of its own qualifies, and a "domain" file of pure boilerplate does not. Be selective. Let the criteria filter the list rather than a number, and omit the section when nothing rises to it.

## Hard constraints

The steps above carry their own reasoning. These four repeat because each one is either irreversible for the author once done, or leaves the run having delivered nothing.

- **Never** end the turn between the review and the posting. The report of review-changes is an intermediate artifact, and the run is not finished until Step 6 has posted and Step 8 has reported. If the user has to ask whether the comments went up, this skill failed.
- **Never** act on the verdict outside the default mode. `draft` and `comments-only` report the verdict in the conversation and leave the approval state of the change untouched, and so does a self-authored change.
- **Never** delete or overwrite a comment that is already published, on a rerun or at any other time. The author can have replied to it. A rerun skips what is already there.
- **Never** check out the change in the user's main clone. Always review from the isolated worktree that Step 4 created.
