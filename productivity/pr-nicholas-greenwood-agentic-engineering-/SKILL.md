---
name: pr
description: use before opening a PR or writing PR description
---

open a ready PR targeting `<base>`: the parent branch for a stacked PR, otherwise `develop`

for description-only requests, use the description rules below and leave packaging to an authorised PR flow

## workflow

1. inspect once

- in 1 tool call, run `git status --short --branch`, `git log --oneline origin/<base>..HEAD`, `git diff --stat origin/<base>...HEAD`, and `git diff --stat HEAD`
- use the actual diff and task evidence to describe the final change
- treat the working tree as intended; reuse the latest passing verification while its diff is unchanged
- complete when the branch action, commit message, PR title, and PR body draft are decided

2. package

- create a branch when detached or on `<base>`; stage/commit/push if needed
- run `gh pr create --base <base> --title "<pr title>" --body-file - <<'EOF'` with the body draft as the heredoc; keep file names as code paths until the PR URL exists; stdin needs no body file, so concurrent agents can't collide
- run `bin/pr-add-contributor` to add your thread to the PR's `contributors:` line
- after the PR URL exists, generate links using [file links](#file-links) and update it with `gh pr edit <pr-url> --body-file -` using the final body as a quoted heredoc, preserving existing content and contributor links
- complete when every published file/line link is generated per [file links](#file-links); return the PR URL

notes:

- use `/git` and `/repo-writing-style` skills
- if pre-commit or pre-push hooks fail, fix
- preserve third-party PR description content and existing contributor links when updating a body
- don't add labels, except `skip-backend-stress` when backend changes do not affect concurrency, async work, retries, locks, or test synchronisation; otherwise remove it
- invoking this skill to open a PR (directly or through another skill), or saying something like "open a PR", grants permission to push and open that PR
- commit and push authority ends when this PR flow completes; later requests need new permission

## description

- keep it short and skimmable, using UK english and ASD-STE100 simplified technical english; use `GLOSSARY.md` for domain terms when needed
- write 1-3 short summary bullets; combine related points to stay within 3
- keep prose at most 150 words by default, excluding headings, diagrams, image links, and contributors; small changes need less
- add detail beyond this only for a material risk, recovery step, or rollout requirement a reviewer needs to decide whether to merge
- give each fact 1 home; keep implementation detail or unchanged behaviour only when it explains the change, a tradeoff, or rollback
- describe the final diff for a reviewer without the chat history
- choose changed-file links using [file links](#file-links); prefer whole-file diff links for an overview and line/range links for a specific review point
- keep review links inside the PR; show unchanged files as code paths, and refresh affected links after file renames or line changes

use this body shape, omitting optional sections and replacing all placeholders:

```md
why and what changed:
- <problem or reason, then resulting behaviour>

merge danger:
- door: <1-way, 2-way, or unknown>, <rollback or recovery>
- blast radius: <affected users, tenants, workflows, or consumers>
- <high|medium|low>: <material remaining risk and why it was not verified>

verification:
- <manual check or smoke test and observed result>

visual verification:

| before | after |
| --- | --- |
| ![before](<uploaded URL>) | ![after](<uploaded URL>) |
```

### file links

- while implementation or PR description edits are still planned, keep links sparse: link only key files with whole-file diffs and use code paths for other references
- when reasonably confident no further implementation or description edits remain, add line/range links only where they help a specific review point; refresh or simplify affected links if work resumes
- resolve the intended PR URL from `gh pr create` output or `gh pr view --json url --jq .url`; for an explicitly requested PR, pass its URL/number to `gh pr view` in the commands below
- take exact repository-relative `filename` values from `gh api --paginate` for `repos/<owner>/<repo>/pulls/<number>/files?per_page=100`; derive the repository and number from the resolved PR URL; use the listed current path for renamed files and listed path for deleted files
- compare the returned file count with `gh pr view --json changedFiles --jq .changedFiles`; the API caps results at 3,000 files, so treat a count mismatch as an incomplete list; leave referenced paths missing from that list as code paths, report the lookup gap, and generate links only for listed paths
- generate `<pr-url>/changes#diff-<sha256(path)>` from the path's UTF-8 bytes, without URL-encoding or a trailing newline; replace the sample path below and pass further paths as separate quoted arguments

```bash
pr_url=$(gh pr view --json url --jq .url)
node - "$pr_url" 'path/to/changed-file.ts' <<'JS'
const { createHash } = require('node:crypto');
const [prUrl, ...paths] = process.argv.slice(2);
for (const path of paths) {
  const fileId = createHash('sha256').update(path, 'utf8').digest('hex');
  console.log(`${path}\t${prUrl}/changes#diff-${fileId}`);
}
JS
```

- for line links, append `L<line>` for the old side or `R<line>` for the new side; for ranges, append `L<start>-L<end>` or `R<start>-R<end>`, using actual PR diff line numbers

### why and what changed

- start with why, then the concrete change in behaviour
- for a complex change, use the smallest useful view: a mermaid workflow, pseudocode, a shallow call/file/component tree, or a short diff sketch
- place the visual next to the point it explains; use prose alone when it is clearer

### merge danger

- always state the door and actual blast radius; a small diff can affect every tenant
- use `2-way` when reverting the code restores the previous behaviour without data repair or undoing external effects
- use `1-way` for destructive data changes or hard-to-reverse effects; state the recovery needed, even if code can be reverted
- use `unknown` when reversibility is unresolved, and name the missing evidence
- name the affected surface, users/tenants, or consumers rather than a vague size label
- include material remaining risks as `high`, `medium`, or `low`, highest first; state the failure and why it was not verified
- omit the risk bullet when none remains; add required rollout or recovery steps here when needed


### verification

- show concrete before/after evidence when available: manual checks, smoke tests, API or console output, or measured behaviour
- report checks actually performed and their observed results; if the before state was not captured, say so when it matters
- keep unit tests, linting, formatting, type checks, builds, CI, and code review out of this section unless it was the goal of the PR
- skip this section when there is no manual or smoke-test evidence

### visual verification

- for all user-visible changes, or when visuals help review:
  - include browser evidence from our app or other sites, dashboards and prototypes when it helps explain or verify the change
  - use `/agent-browser` for screenshots of useful static states
  - use `/record-video` when full flow, motion, interaction or state persistence needs demonstrating
  - inspect screenshots, videos and visible URLs for private data before uploading; redact without hiding behaviour needed as proof
  - upload using `/github-image-upload` and include the result in the description
- for before/after comparisons, capture the base and changed versions in the same state, with matching viewport, data, and crop
- for before/after comparisons, use 1 2-column table per pair, as above; other visuals can use other formats
- when an element appears after an animation, wait for it to finish, ie add a 1s delay before capture
- if a before capture is unavailable, label the available visual accurately and explain the gap briefly
- skip this section when there are no visuals
- to save time, you can use a sub-agent for capture

### small PR example

```markdown
why and what changed:
- make file references open the review diff with before/after context and comment controls
- try the [demo file](https://github.com/meridian-labs/ops-console/pull/33042/changes#diff-b09335cb9e6aceea717e1b0e194589238d6c7af4973b68d9613b627ce07f928d) or [line 9](https://github.com/meridian-labs/ops-console/pull/33042/changes#diff-b09335cb9e6aceea717e1b0e194589238d6c7af4973b68d9613b627ce07f928dR9)

merge danger:
- door: 2-way, revert
- blast radius: PR descriptions and reviewer navigation
```
