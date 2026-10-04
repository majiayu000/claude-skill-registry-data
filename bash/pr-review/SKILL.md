---
name: "PR: Review"
description: "Review a pull request and post it as a GitHub review"
when_to_use: "When the user explicitly asks for a review posted to GitHub (inline comments + verdict), or when next-task-ship's Step 7 self-review runs. Posts to the PR immediately; for a read-only review printed to the terminal use pr-review-dry_run instead, and never invoke this speculatively."
model: opus
effort: high
metadata:
  glyph: ᛟ
  family: pr
disable-model-invocation: false # invocable so next-task-ship's Step 7 self-review can call it; it posts to GitHub, so never invoke without an explicit ask or that orchestration
allowed-tools: ["Bash(git:*)", "Bash(gh:*)", "Bash(node:*)", "Bash(jq:*)"]
disallowed-tools: ["Edit", "Write", "NotebookEdit"] # reviews and posts, never fixes
arguments: ["mode", "pr"]
argument-hint: "[loose|strict] [PR number | URL]"
---

# PR Review with Comment

Thin wrapper around `pr-review-dry_run`: all methodology (foci, taxonomy, matrix, verdict logic, writing rules) lives there, including the loose/strict mode split. This skill only parses the mode keyword out of `$ARGUMENTS` and forwards it; it turns the resulting findings into a single GitHub review, using `partition-findings.mjs` (in this skill's folder) to do the deterministic diff-matching and payload assembly. Everything stays in context and in a single shell pipeline: no scratch files are read or written at any point.

```xml
<pull-request-review-and-comment>
  <task>Review the pull request identified within `$ARGUMENTS` (an optional loose/strict mode keyword plus the PR number/URL, in either order; see step 1) and post the findings as one GitHub review. If this skill has reviewed this PR before, build on that prior review instead of starting cold.</task>
  <steps>
    <step num="1">Before resolving the PR, split `$ARGUMENTS` into the mode keyword (`loose` or `strict`, if present, case-insensitive, order-agnostic) and the PR identifier. Pass only the identifier onward: `gh pr view <identifier> --json number,url,author --jq '{number, url, author: .author.login}'`, then take `owner`, `repo` and `pull_number` from the `url` (`https://github.com/{owner}/{repo}/pull/{n}`). The URL always names the base repository, where the review must be posted; `headRepository` would name the fork on a cross-repository PR. Keep `author` for step 2.</step>
    <step num="2">Resolve the authenticated login via `gh api user --jq .login`, then make two checks. **Self-review**: when `author` equals the login, GitHub refuses `APPROVE` and `REQUEST_CHANGES` at step 6 (422, "Can not approve your own pull request" / "Can not request changes on your own pull request"), so set `selfReview: true` in step 4's JSON and submit as `COMMENT` at step 6. This is the normal case in Jason's own repos and in every next-task-ship run; the derived verdict still reaches the PR as the first line of the review body. **Prior reviews from this skill**: `gh api repos/{owner}/{repo}/pulls/{pull_number}/reviews --jq '[.[] | select(.user.login == "<login>" and (.body | contains("&lt;!-- pr-review --&gt;")))]'`. Only reviews carrying that marker count: `partition-findings.mjs` stamps it into every body this skill posts, and a review by the same login without it is something else (a hand-written review, or the empty `COMMENTED` review GitHub creates for each pr-handle_review thread reply). If any match, this is a re-review: fetch each one's inline comments with `gh api repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/comments` and enter <follow-up-mode/>. Otherwise proceed cold.</step>
    <step num="3">Load the pr-review-dry_run skill and run it against the resolved PR identifier, forwarding the resolved mode (loose applies when no keyword was given), to produce structured findings, a summary, and a derived verdict. In follow-up mode, pass the prior findings in as context per <follow-up-mode/>. Do not skip or duplicate pr-review-dry_run's methodology here. Keep the findings, summary, and verdict in context; nothing gets written to disk at any point in this skill.</step>
    <step num="4">Assemble one JSON object in context (never on disk): `{ "verdict": ..., "selfReview": true|false, "findings": [...], "diff": "<verbatim gh pr diff output for the resolved PR identifier>", "summary": "<verbatim review summary prose>" }`. `verdict` is the exact string pr-review-dry_run derived (`Request Changes`, `Comment` or `Approve`); when `selfReview` is true the script opens the body with a bold verdict line built from it, so do not write one into the summary yourself. The summary prose (and every comment body inside `findings[].body`) must contain **no em-dashes, en-dashes, or other dash-family separators**; use a semicolon, colon, or parentheses instead. `partition-findings.mjs` hard-fails the run if it finds one, so getting this right up front avoids a wasted round-trip.</step>
    <step num="5">Feed that JSON straight into a single pipeline, with `partition-findings.mjs` reading it from stdin and `gh api` reading the resulting payload from stdin in turn; nothing touches disk at any point. **Set `pipefail` first** (`set -o pipefail;` at the start of the same shell call, or run the pipeline inside `bash -o pipefail -c '...'`): without it, a non-zero exit from the node step is swallowed, its empty/partial stdout still flows into `gh api`, and `gh` happily creates an empty pending review from nothing. Never omit the flag.
      <code>
set -o pipefail
node ${CLAUDE_SKILL_DIR}/partition-findings.mjs <<'JSON_EOF' | gh api --method POST repos/{owner}/{repo}/pulls/{pull_number}/reviews --input -
{ "verdict": "...", "selfReview": false, "findings": [...], "diff": "...", "summary": "..." }
JSON_EOF
      </code>
      `${CLAUDE_SKILL_DIR}` resolves to this skill's directory wherever it is installed. The script partitions findings per <mapping/>, composes the review body (verdict line first under self-review, then the summary, the folded sections and finally the `&lt;!-- pr-review --&gt;` marker step 2 looks for), **validates the summary and every comment body** (dash-family ban + a banned-emoji check on the summary; see <api-constraints/>), and writes the ready-to-POST payload to stdout; stats `{inline, folded, offDiffDemoted}` go to stderr so stdout stays pure JSON for `gh api` to consume. Omitting `event` on the `gh api` call is what keeps the review **pending** (author-only) rather than publishing immediately. Capture the returned `review_id` from the response.

      If the pipeline still fails (`gh api` prints a non-2xx response, or exits non-zero under `pipefail`), check whether it nonetheless created an empty or partial pending review: `gh api repos/{owner}/{repo}/pulls/{pull_number}/reviews --jq '[.[] | select(.state == "PENDING")]'`. Delete any such stray review (`gh api --method DELETE repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`) before re-running, so a retry never leaves two pending reviews on the same PR. On non-zero exit from the node step specifically, treat stderr as a hard failure: read the message, fix the offending prose or the finding shape in the heredoc, and re-run the whole pipeline. Do not attempt to hand-build the payload as a fallback, and do not split this into separate write-then-read steps through a file.</step>
    <step num="6">Auto-submit immediately: `gh api --method POST repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/events -f event="$EVENT"`, where `$EVENT` comes from <verdict-map/>: `APPROVE` / `REQUEST_CHANGES` / `COMMENT`, or always `COMMENT` under self-review. If this call fails (non-2xx), the review is still `PENDING` and visible only to the author: resubmit the same `review_id` with `event=COMMENT` rather than leaving it stranded or re-running step 5, which would create a second pending review.</step>
  </steps>
  <api-constraints>
    <!-- Verified against GitHub REST docs (2022-11-28). State these plainly so the model never re-derives them live. -->
    <fact>The review-create endpoint's `comments[]` array accepts ONLY line-anchored entries (path, body, line, side, start_line, start_side). It does NOT accept `subject_type`; that field is response-only on this endpoint, not a request field. File-level comments therefore CANNOT be batched into a pending review. This is why file-level, cross-file, off-diff, and admiration findings all fold into the top-level review `body` instead; see <mapping/>.</fact>
    <fact>This endpoint is REST, not GraphQL. `gh api` calls it directly as REST. Don't chase a GraphQL explanation if a payload is rejected; check the payload shape against this block first.</fact>
    <fact>Omitting `event` on review-create leaves the review PENDING. `POST .../reviews/{review_id}/events` with an `event` value submits it.</fact>
    <fact>There is no endpoint to append file-level comments to an existing pending review after creation. Get the body right in the initial POST.</fact>
    <fact>A PR's author cannot submit `APPROVE` or `REQUEST_CHANGES` on it: the events endpoint returns 422 for both. Only `COMMENT` is accepted from the author, which is why self-review carries the verdict as the body's first line instead.</fact>
    <fact>`partition-findings.mjs` ends every body with `&lt;!-- pr-review --&gt;`. GitHub hides HTML comments when rendering, and step 2 filters on it to tell this skill's reviews apart from other reviews by the same login. Never strip it.</fact>
    <fact>`partition-findings.mjs` validates prose before writing the payload: the summary and every comment body are rejected if they contain an em-dash, en-dash, horizontal bar, or figure dash; the summary is additionally rejected if it contains 🆕, ✅, or ⚠️ (superseded vocabulary; 🆕 in particular renders as a GitHub `:new:` badge, not a plain glyph). This is a ban-list, not an allow-list; the summary can otherwise carry any emoji. See <follow-up-mode/> for the correct vocabulary on a follow-up delta.</fact>
    <fact>Every `findings[].type` value in the JSON payload MUST be the literal emoji (`🔴`, `🟠`, `🟡`, or `🟣`), never the English word. `partition-findings.mjs` checks `finding.type` against exactly those four glyphs and throws `Unknown finding type` on anything else, `"admiration"` included, even though <mapping/> below uses `type="admiration"` as an XML attribute for readability. That attribute names the row; it is not the value to put in the payload. Get the emoji into the JSON directly rather than a word pr-review-dry_run's own <taxonomy/> emoji-to-name mapping might tempt you to write.</fact>
  </api-constraints>
  <mapping>
    <!-- What partition-findings.mjs does: documentation of its behaviour, not instructions for the model to reimplement. -->
    <rule scope="line" condition="in-diff">→ `comments[]` entry: { path, line (or start_line+line for a range), side: "RIGHT", body: type-emoji-prefixed, + suggestion block if present }</rule>
    <rule scope="line" condition="off-diff">a finding whose target line isn't inside a diff hunk is demoted into the body's "Off-diff notes" section; never dropped, never misrouted into comments[]</rule>
    <rule scope="file">folds into the body's "File-scoped notes" section</rule>
    <rule scope="cross-file">folds into the body's "Cross-file notes" section</rule>
    <rule type="admiration">🟣 always folds into the body's "Accolades" section, one bullet per finding, each individually prefixed with 🟣; never an inline comment, never a single umbrella heading absorbing the emoji, even when the finding is line-scoped</rule>
  </mapping>
  <follow-up-mode>
    <guide>Triggered when step 2 finds a prior review on this PR from the authenticated user whose body carries the `&lt;!-- pr-review --&gt;` marker. This means the skill has reviewed this PR before; treat it as a continuation, not a fresh review. Reviews by the same login without the marker are ignored for this purpose.</guide>
    <guide>Pass the prior findings (path, line, body, submitted_at) into the pr-review-dry_run run as context. pr-review-dry_run should evaluate whether each prior finding was addressed in the current diff, not re-flag it from scratch as if seeing the code for the first time.</guide>
    <guide>The composed summary leads with a short "Since my last review" delta before the current findings: one line each for what's now fixed (⚪), what's still open (⚫), and what's newly introduced (🟢). This is the only emoji vocabulary the delta may use: never 🆕 (renders as a GitHub `:new:` badge, not a plain glyph) and never ✅/⚠️ (superseded, off-palette next to the circle set). `partition-findings.mjs` hard-fails the run if it sees the banned set, so use the circles from the start. This is a brief acknowledgement, not a full changelog: a sentence per item, not a status table with links back to original threads.</guide>
    <guide>The verdict reflects the PR's current state, not a mechanical re-scan. A prior 🔴 that's now fixed should not resurface; a prior 🟡 left unaddressed can be repeated, but say so explicitly ("still open from last review") rather than presenting it as newly discovered.</guide>
  </follow-up-mode>
  <verdict-map>
    <guide>Mode selection happens in pr-review-dry_run. This map is mode-agnostic: it translates the derived verdict, whichever rule set produced it.</guide>
    <rule>pr-review-dry_run verdict "Request Changes" → event `REQUEST_CHANGES`</rule>
    <rule>pr-review-dry_run verdict "Comment" → event `COMMENT`</rule>
    <rule>pr-review-dry_run verdict "Approve" → event `APPROVE`</rule>
    <rule>Self-review (PR author is the authenticated login) → event `COMMENT` whatever the verdict; the verdict words open the review body instead</rule>
  </verdict-map>
  <toggle>
    <guide>To switch to manual submission (review pending in the GitHub UI until a human submits it): skip step 6 entirely and stop after step 5. One-line change; do not add complexity beyond deleting the step.</guide>
  </toggle>
</pull-request-review-and-comment>
```
