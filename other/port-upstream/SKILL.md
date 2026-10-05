---
name: port-upstream
description: "Analyzes upstream fork PR changes and ports selected items into the local branch. Use when checking upstream PRs, porting upstream changes, or planning selective upstream integration."
when_to_use: "port upstream, upstream PR, check upstream, upstream changes, upstream fork, bring changes from upstream"
user-invocable: true
argument-hint: "[release_tag | compare_url | pr_url]"
allowed-tools: ["Agent", "Bash", "Read", "Glob", "Grep"]
---

## Step 1. Derive the canonical diff (do this BEFORE spawning any agent)

The input to analysis must be a **git diff between two tags** (or two commits) — not release-notes prose. Release notes are summaries; the diff is ground truth.

### 1a. Resolve the tag range

From the user's input, identify the upstream repo and the two endpoints:
- **HEAD tag** — the release/PR being evaluated (e.g. `v4.4.0`)
- **BASE tag** — the previous release tag on the same upstream branch (e.g. `v4.3.0`), or whatever tag we last successfully ported up to

If only a release URL is given, infer BASE from the upstream's tag list (`gh release list --repo <upstream> --limit 5`) — the immediately preceding semver tag.

### 1b. Fetch the diff via one of these (cheapest first)

```bash
# Option A — GitHub compare endpoint (no local fetch needed; works for any public fork)
gh api repos/<owner>/<repo>/compare/<BASE>...<HEAD> \
  --jq '.files[] | {filename, status, additions, deletions, patch}' > /tmp/upstream-diff.json

# Option B — local git (if upstream is wired as a git remote)
git fetch upstream --tags
git diff upstream/<BASE>..upstream/<HEAD> -- ':!*.lock' ':!bin/' ':!*.min.*'
```

Exclude generated artifacts (`bin/`, lock files, minified output) — they're noise.

### 1c. Spawn the Explore agent on the diff

Pass the diff file path (not the release URL) as the agent's primary input. Brief:
- Classify each changed hunk: new feature / bug fix / doc / generated artifact.
- For each substantive change, produce a one-line summary plus the file:line citation **from the upstream diff**.
- For every item the agent classifies as **"already in local"**, it must produce one of the evidence forms in Verification Rules below. A bare commit-hash citation is not sufficient and must be rejected.
- Translate any non-English content to English (see Rules).

### Why a diff, not release notes

Release notes are prose summaries written by the upstream author. They invite subject-line matching — "upstream said X, local commit says X, must be the same." That heuristic produces false-positive merge claims. Diffs eliminate the abstraction: the hunks either are or are not in the working tree, no interpretation needed.

## Step 2. Build the harness plan from the finding

- Based on what we found in Step 1, write a plan through `/harness-plan`
- If there is nothing worth porting, just tell user.


## Verification Rules — "is this change already in local?"

This skill exists in a fork of an upstream repo. After `git fetch upstream`, every commit upstream pushes is reachable **by hash** from the local repo, even if no local branch points at it. This makes hash-based "proof" unreliable.

### Forbidden checks (do not use as proof of local presence)

- `git show <hash>` — works on any fetched object, including unmerged upstream commits.
- `git log --oneline | grep <hash>` — same problem; the hash is in the object DB, not necessarily on `master`.
- Subject-line matching ("upstream commit says X, local commit says X" → "we have it") — heuristic only, never proof.

### Required checks (use one — pick the cheapest)

1. **Working-tree symbol grep** (preferred). Pick a unique symbol the upstream change introduces — a function name, variable name, regex literal, error string — and grep the working tree:
   ```bash
   grep -rn 'headingTaskRe' .   # if it's missing, the change is not present, full stop
   ```
2. **Branch reachability** (when only a hash is available). Confirm the cited commit is reachable from `master`:
   ```bash
   git branch --contains <hash>   # empty output = not merged, ignore the citation
   ```

### Default question

When verifying "is this in local?", default the framing to **"what would prove this is *missing*?"** — not "what would prove it's present?". Confirmation bias is the recurring failure mode in port reviews; refutation-first framing is the cheapest counter.

## Rules

- If changes are in Japanese or non English, translate to English
- One verifier, not chained reviewers. Layered second-opinions amplify bad evidence — if the first agent's check is wrong, a reviewer checking the same way will reach the same wrong conclusion.
