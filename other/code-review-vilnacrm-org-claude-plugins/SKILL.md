---
name: code-review
description: Systematically retrieve, categorize, and address PR code review comments with an auditable evidence ledger — AI review loop, per-comment commits, suppression-free fixes, and pushed-head verification of required checks and approval. Use when handling code review feedback, addressing PR comments, or driving a reviewed React/TypeScript PR to merge-ready state.
---

# Code Review Workflow Skill

## Profile keys consumed

- `project.repo`
- `make.ci`, `make.ai_review_loop`, `make.pr_comments`, `make.format`, `make.lint`, `make.lint_eslint`, `make.lint_tsc`, `make.lint_md`, `make.lint_dup`, `make.lint_metrics`, `make.lint_deps`, `make.test_unit_client`, `make.test_unit_server`, `make.test_integration`, `make.test_e2e`, `make.test_visual`, `make.test_mutation`, `make.merge_mutation_reports`, `make.lighthouse_desktop`, `make.lighthouse_mobile`, `make.a11y`, `make.post_review_findings`
- `quality.coverage_statements`, `quality.coverage_branches`, `quality.coverage_functions`, `quality.coverage_lines`, `quality.mutation_msi`, `quality.jscpd_clones`, `quality.eslint_errors`, `quality.eslint_warnings`, `quality.tsc_errors`, `quality.markdownlint_errors`, `quality.depcruise_violations`, `quality.metrics_enforced`, `quality.visual_diffs`, `quality.lighthouse_desktop`, `quality.lighthouse_mobile`
- `capabilities.publish_pr_comments`, `capabilities.visual_testing`, `capabilities.lighthouse`, `capabilities.mutation_testing`, `capabilities.accessibility_audit`
- `ci.provider`, `ci.required_checks`
- `review.ai_review_agents`, `review.coderabbit`, `review.request_changes_blocking`

## Context (Input)

- PR has unresolved code review comments
- Need systematic approach to address feedback
- Ready to implement reviewer suggestions
- Need to maintain quality standards during review implementation
- Profile loaded from `.claude/react-sdlc.yml` (run `/fe-sdlc-setup` if missing).
  When `review.coderabbit` is `false`, the AI review loop is the primary
  comment source; review threads still go through the same evidence protocol.

## Task (Function)

Systematically retrieve, categorize, and address all PR code review comments
while maintaining quality standards and PR readiness.

**Success Criteria**:

- Direct GitHub GraphQL review-thread query shows 0 unresolved review comments,
  and the `PR_COMMENT_EVIDENCE` ledger records
  `SNAPSHOT_STARTED_AT=<auto-captured ISO time>`,
  `SNAPSHOT_CAPTURED_BY=code-review-skill`, `PR_HEAD=<sha>`, plus every
  review-thread, top-level PR issue, and review body comment from that
  snapshot as `COMMENT_META|url|updatedAt|body_sha256` and
  `COMMENT|url|commit|sha`, `COMMENT|url|reply|url`, or
  `COMMENT|url|decline|url`; reply/decline evidence comments must be posted by
  the PR author or a login in `PR_COMMENT_TRUSTED_EVIDENCE_ACTORS` and include
  structured `EVIDENCE_SOURCE`, `EVIDENCE_ACTION`, and decline
  `EVIDENCE_REASON`; non-evidence comments created or edited after the
  snapshot block completion until the snapshot and evidence are restarted,
  except an otherwise qualifying approval review on pushed `HEAD` whose body
  is empty or exactly `FINAL_APPROVAL_NO_ACTION: true`
- The target mapped by `make.ci` exits `0`
- A final AI review loop run (the target mapped by `make.ai_review_loop`, or
  `"${CLAUDE_PLUGIN_ROOT}/scripts/ai-review-loop.sh"` when that key is `null`)
  reports `AI_REVIEW_VERDICT: PASS` after the `make.ci` target, on the same
  commit; if it applies fixes, repeat CI and the loop until both pass without
  new changes
- Local `HEAD` is pushed and matches
  `gh pr view <number> --repo "$PR_REPO" --json headRefOid`
- Commit-scoped status/check rollup for local `HEAD` is queried from the base
  PR repository (`project.repo`), is non-empty, non-required contexts have
  only allowed terminal states (`SUCCESS`, `SKIPPED`, or `NEUTRAL`), and every
  check named in `ci.required_checks` plus every live base-branch protection
  required status/check is present with state `SUCCESS` on that pushed head;
  GitHub Actions check URLs must point at the base PR repository
- Final direct GitHub GraphQL review-thread query after the pushed-head
  verification still shows 0 unresolved review comments
- `gh pr view <number> --repo "$PR_REPO" --json state,mergeStateStatus,mergeable,reviewDecision,isDraft,reviewRequests`
  shows the PR is open, not draft, not conflicting, `reviewDecision` is
  `APPROVED`, `reviewRequests` is empty, and a direct review query shows an
  `APPROVED` review on the pushed `HEAD` submitted after the latest addressed
  comment evidence by a non-author reviewer with `OWNER`, `MEMBER`, or
  `COLLABORATOR` association. When `review.request_changes_blocking` is
  `true` (default), any `CHANGES_REQUESTED` review state blocks completion
  until re-reviewed.

**Degrade rule (NFR-4)**: when `ci.provider` is `null`, skip the check-waiting
and check-rollup steps with an explicit capability-absent note; all local
gates (CI target, AI review loop, evidence ledger, unresolved-thread queries)
still apply.

## Workflow Overview

```text
AI Review Loop → PR Comments (snapshot) → Categorize → Apply by Priority →
Verify → Run CI → Final AI Review Loop → Push → GitHub Readiness → Done
```

## Evidence Ledger Protocol

Every addressed comment leaves an auditable trace in a ledger file pointed to
by `PR_COMMENT_EVIDENCE`. The protocol prevents silently dropped feedback and
backdated "done" claims.

**Snapshot capture** — auto-capture the timestamp; never supply or backdate it
manually:

```bash
capture_review_comment_snapshot() {
  REVIEW_COMMENT_SNAPSHOT_STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  export REVIEW_COMMENT_SNAPSHOT_STARTED_AT
}
capture_review_comment_snapshot
printf 'SNAPSHOT_STARTED_AT=%s\nSNAPSHOT_CAPTURED_BY=code-review-skill\n' \
  "$REVIEW_COMMENT_SNAPSHOT_STARTED_AT" > "$PR_COMMENT_EVIDENCE"
```

**Ledger format** (one line each):

```text
SNAPSHOT_STARTED_AT=<ISO-8601 UTC>
SNAPSHOT_CAPTURED_BY=code-review-skill
PR_HEAD=<final local head sha>
COMMENT_META|<comment url>|<updatedAt>|<sha256 of bodyText>
COMMENT|<comment url>|commit|<sha>      # fixed by a commit
COMMENT|<comment url>|reply|<url>       # answered by a reply comment
COMMENT|<comment url>|decline|<url>     # declined with reasoned comment
```

The body hash comes from the comment's `bodyText`:

```bash
b64_decode() {
  if printf '' | base64 --decode >/dev/null 2>&1; then base64 --decode; else base64 -D; fi
}
sha256_hex() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum; else shasum -a 256; fi
}
body_hash_from_b64() {
  printf '%s' "$1" | b64_decode | sha256_hex | awk '{ print $1 }'
}
iso_time_epoch() {
  date -u -d "$1" +%s 2>/dev/null ||
    date -u -j -f '%Y-%m-%dT%H:%M:%SZ' "$1" +%s
}
```

**Validation rules** — each `COMMENT` line must satisfy, against the comment's
*effective time* (the later of `createdAt` and `updatedAt`):

- `commit` evidence: the sha resolves (`git rev-parse --verify <sha>^{commit}`),
  is an ancestor of local `HEAD`, is NOT an ancestor of the trusted base ref,
  its committer time is later than the comment's effective time, and its
  commit message references the source comment URL.
- `reply` evidence: a same-PR comment URL different from the source, with a
  later effective time, posted by the PR author or a login listed in the
  comma-separated `PR_COMMENT_TRUSTED_EVIDENCE_ACTORS`, whose body contains
  `EVIDENCE_SOURCE: <source URL>` and a positive
  `EVIDENCE_ACTION:` (`addressed|resolved|fixed|implemented|updated|changed|applied`).
- `decline` evidence: same actor and URL rules, body contains
  `EVIDENCE_SOURCE: <source URL>`, a no-change
  `EVIDENCE_ACTION:` (`declined|stale|duplicate|not applicable|not needed|won't fix|will not fix`),
  and a non-empty `EVIDENCE_REASON: <reason>`.
- Every `COMMENT_META` line must have a matching, valid `COMMENT` line, and
  the recorded `updatedAt`/hash must still match the live comment (an edited
  comment invalidates its evidence).

**Post-snapshot rule**: any non-evidence PR/review comment created or edited
after `SNAPSHOT_STARTED_AT` forces a restart of snapshot capture and evidence
collection. Allowed exceptions: validated reply/decline evidence URLs, and an
otherwise qualifying approval review on pushed `HEAD` whose body is empty or
exactly `FINAL_APPROVAL_NO_ACTION: true`.

**Comment enumeration** — three sources, each paginated with 100-node cursor
pages (`pageInfo{hasNextPage endCursor}`); never trust a single unpaginated
page:

1. Review-thread comments — `pullRequest.reviewThreads(first:100)` with nested
   `comments(first:100)`; threads whose inner `comments.pageInfo.hasNextPage`
   is true must be drained via
   `node(id:$threadId){... on PullRequestReviewThread{comments(first:100,after:$cursor)...}}`.
2. Top-level PR issue comments — `pullRequest.comments(first:100)`.
3. Review bodies — `pullRequest.reviews(first:100)`.

Each node yields `url`, `createdAt`, `updatedAt`, `bodyText`; skip empty
bodies; emit `url|createdAt|updatedAt|base64(bodyText)` items, deduplicate
with `sort -u`, and filter before/after the snapshot by effective time.

## Execution Steps

### Step 0: Run Autonomous AI Review Loop

Before addressing PR comments manually, fetch the PR base into a trusted ref
and run the autonomous review loop against that base:

```bash
set -euo pipefail
command -v jq >/dev/null || { echo "jq is required" >&2; exit 1; }

: "${PR:?Set PR to the pull request number}"
case "$PR" in
  ''|*[!0-9]*) echo "PR must be numeric" >&2; exit 1 ;;
esac
: "${PR_REPO:?Set PR_REPO=owner/repo for the base PR repository (profile project.repo)}"
PR_META="$(gh pr view "$PR" --repo "$PR_REPO" --json baseRefName,baseRefOid)"
BASE_REF="$(printf '%s\n' "$PR_META" | jq -r .baseRefName)"
BASE_OID="$(printf '%s\n' "$PR_META" | jq -r .baseRefOid)"
TRUSTED_BASE_REF="refs/remotes/pr-base/$PR"
git fetch "git@github.com:${PR_REPO}.git" "$BASE_REF:$TRUSTED_BASE_REF"
test "$(git rev-parse "$TRUSTED_BASE_REF")" = "$BASE_OID"
```

Then run the loop. If `make.ai_review_loop` is non-`null`, invoke that make
target with the trusted base as the diff base; when it is `null`, the plugin
substitutes its script:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/ai-review-loop.sh" --diff-base "$TRUSTED_BASE_REF"
```

The loop:

1. Runs the review agent(s) from `review.ai_review_agents` against the diff
   from the given base (v1 supports `claude` only; other entries warn+skip)
2. On a `FAIL` verdict, lets the reviewer apply safe fixes in the same
   iteration (the plugin script runs `claude` with
   `--permission-mode acceptEdits`)
3. Re-reviews until a `PASS` verdict or the iteration cap (plugin script:
   `--max-iterations`, default 5)

The plugin script runs no CI between iterations — verify the fixed tree with
the target mapped by `make.ci` afterwards (Step 6); a repo-mapped
`make.ai_review_loop` may run its own verification command per iteration
(commonly the CI target). The plugin script's default prompt covers
correctness, accessibility, FR/NFR coverage, and code health:
component/state design tradeoffs, appropriate React/MUI/Emotion and Zustand
pattern use, code smells, SOLID/DRY/KISS, bulletproof-react module
boundaries, tsyringe DI seams, and repository rules (no `static` / free
functions in `src/**/*.ts`, type-only files, no `data-testid`). Set the
`REVIEW_PROMPT` environment variable to override the scope. Review failures
must stay concrete and scoped to changed code or directly affected behavior.

**Success contract**: the loop exits `0` with a final
`AI_REVIEW_VERDICT: PASS` line (plugin script contract). Repo-provided loops
may print their own banner — treat exit status as the contract:

```bash # profile-example
AI_REVIEW_OUTPUT="$(AI_REVIEW_BASE="$TRUSTED_BASE_REF" make ai-review-loop 2>&1)"
printf '%s\n' "$AI_REVIEW_OUTPUT"
AI_REVIEW_LAST_LINE="$(printf '%s\n' "$AI_REVIEW_OUTPUT" | sed '/^[[:space:]]*$/d' | tail -n 1)"
test "$AI_REVIEW_LAST_LINE" = "AI review PASS."
```

**Configuration** — plugin script flags (canonical): `--agents LIST`
(overrides `review.ai_review_agents`), `--max-iterations N` (default 5),
`--diff-base REF` (default `main`). Repo-provided loops commonly accept
environment overrides instead:

```bash # profile-example
AI_REVIEW_BASE="$TRUSTED_BASE_REF" AI_REVIEW_AGENTS=claude make ai-review-loop
AI_REVIEW_BASE=develop AI_REVIEW_MAX_ITER=1 make ai-review-loop
```

### Step 1: Get PR Comments

Capture the snapshot and initialize the ledger (Evidence Ledger Protocol
above), then list comments through the target mapped by `make.pr_comments`;
when it is `null`, the plugin substitutes:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/get-pr-comments.sh" --pr "$PR"                   # all comments
"${CLAUDE_PLUGIN_ROOT}/scripts/get-pr-comments.sh" --pr "$PR" --unresolved-only # threads with resolution state
"${CLAUDE_PLUGIN_ROOT}/scripts/get-pr-comments.sh" --pr "$PR" --json            # machine-readable
```

**Output**: all unresolved comments with file/line, author, timestamp, URL.

### Step 2: Categorize Comments

| Type                   | Identifier                  | Priority | Action                               |
| ---------------------- | --------------------------- | -------- | ------------------------------------ |
| Committable Suggestion | Code block, "```suggestion" | Highest  | Apply immediately, commit separately |
| LLM Prompt             | "Prompt for AI Agents"      | High     | Execute prompt, implement changes    |
| Architecture Concern   | Placement, naming, boundary | High     | Invoke appropriate skill             |
| Accessibility Concern  | ARIA, focus, contrast, role | High     | Fix the component; re-audit a11y     |
| Question               | Ends with "?"               | Medium   | Answer inline or via code change     |
| General Feedback       | Discussion, recommendation  | Low      | Consider and improve                 |
| Resolved/Stale         | Outdated or already fixed   | None     | Do not change code; record reason    |

### Step 3: Verify Architecture & Organization

For code changes (suggestions, prompts, new files), invoke verification
skills:

| Concern Type                             | Skill to Invoke                                                                      |
| ---------------------------------------- | ------------------------------------------------------------------------------------ |
| Component/file placement or naming       | [code-organization](../code-organization/SKILL.md)                                   |
| Module boundary / DI / bulletproof-react | [architecture](../architecture/SKILL.md)                                             |
| Layer / import violations                | [architecture](../architecture/SKILL.md) (when the `make.lint_deps` target fails)    |
| Component / hook / form / MUI shape      | [frontend-component-development](../frontend-component-development/SKILL.md)         |
| Accessibility regression                 | [frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md) |

**Quick verification**: run the target mapped by `make.format`, then the
targets mapped by `make.lint_eslint`, `make.lint_tsc`, `make.lint_deps`, and
the narrowest relevant test target (`make.test_unit_client`,
`make.test_integration`, or `make.test_e2e`).

### Step 4: Apply Changes Systematically

#### For Committable Suggestions

1. Verify the suggestion still applies to current code
2. Apply the suggestion exactly when it is still valid and compatible with
   repository rules
3. If the suggestion is stale, implement the current equivalent fix or record
   why no change is needed (decline evidence)
4. Commit with reference:

   ```bash
   git commit -m "Apply review suggestion: [brief description]

   Ref: [comment URL]"
   ```

#### For LLM Prompts

1. Copy prompt from comment
2. Verify every finding against current code before changing files
3. Execute still-valid instructions
4. Skip stale, duplicate, or contradicted findings with a brief reason
5. Verify output meets requirements
6. Commit with reference

#### For Architecture/Organization Concerns

1. Invoke the appropriate skill ([code-organization](../code-organization/SKILL.md)
   or [architecture](../architecture/SKILL.md))
2. Implement recommended changes
3. Verify: the `make.format` target plus the `make.lint_eslint`,
   `make.lint_tsc`, `make.lint_deps`, and focused-test targets
4. Commit with reference

#### For Accessibility Concerns

1. Fix the component itself (semantic role, accessible name, focus order,
   contrast) — never reach for a `data-testid` or an `aria-*` band-aid that
   hides the defect
2. Re-run the accessibility lane (the target mapped by `make.a11y`, or the
   plugin's bundled axe-core / Playwright a11y lane when `null`); dispatch the
   `accessibility-auditor` agent when a live-browser re-audit is warranted
3. Commit with reference

#### For Questions

1. Determine if code change or reply needed
2. If code: implement + commit
3. If reply: respond on GitHub with `EVIDENCE_SOURCE`/`EVIDENCE_ACTION` fields

#### For General Feedback

1. Evaluate suggestion merit
2. Implement if beneficial
3. Document reasoning if declined (decline evidence with `EVIDENCE_REASON`)

One commit per comment — never batch unrelated review fixes.

### Step 5: Verify All Addressed

Query unresolved review threads directly (paginated; generic GraphQL):

```bash
set -euo pipefail
: "${PR:?Set PR to the pull request number}"
: "${PR_REPO:?Set PR_REPO=owner/repo for the base PR repository}"
owner="${PR_REPO%%/*}"
repo="${PR_REPO#*/}"
query='query($owner:String!,$repo:String!,$pr:Int!,$cursor:String){repository(owner:$owner,name:$repo){pullRequest(number:$pr){reviewThreads(first:100,after:$cursor){pageInfo{hasNextPage endCursor} nodes{isResolved comments(first:1){nodes{id}}}}}}}'
total_count=0
cursor=''
while :; do
  if [ -n "$cursor" ]; then
    page_json="$(gh api graphql -f owner="$owner" -f repo="$repo" -F pr="$PR" -f cursor="$cursor" -f query="$query")"
  else
    page_json="$(gh api graphql -f owner="$owner" -f repo="$repo" -F pr="$PR" -f query="$query")"
  fi
  page_count="$(printf '%s\n' "$page_json" | jq '[.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false and (.comments.nodes | length > 0))] | length')"
  total_count=$((total_count + page_count))
  has_next="$(printf '%s\n' "$page_json" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.hasNextPage')"
  [ "$has_next" = "true" ] || break
  cursor="$(printf '%s\n' "$page_json" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.endCursor')"
  test -n "$cursor" && test "$cursor" != "null"
done
test "$total_count" -eq 0
```

If unresolved comments remain, repeat categorization and implementation. If a
remaining thread is stale, duplicate, or answer-only, respond or resolve it
with reply/decline evidence before continuing. Then complete the ledger:
write `PR_HEAD=<sha>` plus a `COMMENT_META` line for every snapshotted
comment (all three sources), and one validated `COMMENT|url|commit|sha`,
`COMMENT|url|reply|url`, or `COMMENT|url|decline|url` line per `COMMENT_META`
line, following the Evidence Ledger Protocol exactly — including the
post-snapshot restart rule.

### Step 5b: Publish findings (gated)

When `capabilities.publish_pr_comments` is `true`, project the Step 2
priority/disposition categorization and the evidence-ledger dispositions
(`fixed` = commit, `dropped` = decline/stale) to the canonical ledger JSON
(schema in the poster header) at
`${SDLC_LEDGER_DIR:-.sdlc/review-ledgers}/code-review.json`, then publish ONE
consolidated, idempotent PR comment via the target mapped by
`make.post_review_findings`; when that key is `null`, the plugin substitutes
its script (the same null-substitution pattern as `make.pr_comments` →
`get-pr-comments.sh` in Step 1):

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/post-review-findings.sh" code-review \
  --file "${SDLC_LEDGER_DIR:-.sdlc/review-ledgers}/code-review.json" --pr "$PR"
```

The poster is idempotent (hidden `<!-- sdlc-review:code-review -->` marker — it
updates its prior comment, never spams), authorized (writes only to the resolved
repo's own PR), and DEGRADES (NFR-3): `capabilities.publish_pr_comments`
false/absent, `gh` absent, no PR, an empty ledger, a mismatched base repo, or a
`gh` write failure all skip-with-note and exit 0 — publishing NEVER fails this
workflow. When the flag is false/absent, skip this step with a note.

### Step 6: Run Quality Checks

**MANDATORY**: run the target mapped by `make.ci` after implementing all
changes; it must exit `0`. Many repositories print a success banner — treat
exit status as the contract, the banner as confirmation:

```bash # profile-example
CI_OUTPUT="$(make ci 2>&1)"
printf '%s\n' "$CI_OUTPUT"
CI_LAST_LINE="$(printf '%s\n' "$CI_OUTPUT" | sed '/^[[:space:]]*$/d' | tail -n 1)"
test "$CI_LAST_LINE" = "✅ CI checks successfully passed!"
```

**Suppression scan** — after CI, scan the PR diff for forbidden suppression
or ignore directives. Fix root causes; never silence tools:

```bash
command -v rg >/dev/null || { echo "rg is required for suppression scan" >&2; exit 1; }
set -o pipefail
diff_output="$(git diff --unified=0 "$TRUSTED_BASE_REF"...HEAD)" || {
  echo "Unable to compute PR diff for suppression scan" >&2
  exit 1
}

forbidden_suppression_pattern() {
  printf '%s\n' 'eslint-''disable|@ts-''ignore|@ts-''expect-error|@ts-''nocheck|prettier-''ignore|markdownlint-''disable|editorconfig-checker-''disable|editorconfig-''disable|jscpd:''ignore|istanbul ''ignore|Stryker ''disable|depcruise-''disable'
}

if printf '%s\n' "$diff_output" | rg '^\+[^+]' | rg -n "$(forbidden_suppression_pattern)"; then
  echo "Forbidden suppression/ignore directive found in PR diff" >&2
  exit 1
fi

# Gate-definition isolation: detect whether this is a dedicated
# gate-definition PR (only gate-definition files changed vs the trusted
# base). When so, the quality-config hard block is skipped — those changes
# are the legitimate subject of the PR and are reviewed on their own (see
# the Gate-definition isolation rule below). The forbidden-suppression line
# scan above still runs, and any threshold change must be raise-only.
GATE_DEFINITION_FILE_PATTERN='(^|/)(Makefile|\.github/|.*baseline.*|eslint\.config\.(mjs|js|cjs)|tsconfig.*\.json|\.jscpd\.json|\.?dependency-cruiser\.(js|cjs|mjs|json)|config/metrics-policy\.json|stryker(\.shard)?\.config\.mjs|jest\.config\.ts|playwright\.config\.ts|lighthouse/lighthouserc\..*\.js|\.markdownlint.*\.(json|ya?ml)|\.prettier.*|\.claude/skills/.*\.md)'
all_changes="$(git diff --name-only "$TRUSTED_BASE_REF"...HEAD)"
gate_definition_changes="$(printf '%s\n' "$all_changes" | rg "$GATE_DEFINITION_FILE_PATTERN" || true)"
non_gate_definition_changes="$(printf '%s\n' "$all_changes" | rg -v "$GATE_DEFINITION_FILE_PATTERN" || true)"
GATE_DEFINITION_CHANGES_PRESENT=false
if [ -n "$gate_definition_changes" ] && [ -z "$non_gate_definition_changes" ]; then
  GATE_DEFINITION_CHANGES_PRESENT=true
fi

quality_config_changes="$(git diff --name-only "$TRUSTED_BASE_REF"...HEAD | rg '(^|/)(.*baseline.*|eslint\.config\.(mjs|js|cjs)|tsconfig.*\.json|\.jscpd\.json|\.?dependency-cruiser\.(js|cjs|mjs|json)|config/metrics-policy\.json|stryker(\.shard)?\.config\.mjs|jest\.config\.ts|playwright\.config\.ts|lighthouse/lighthouserc\..*\.js|\.markdownlint.*\.(json|ya?ml)|\.prettier.*)$' || true)"
if [ -n "$quality_config_changes" ] && [ "$GATE_DEFINITION_CHANGES_PRESENT" != "true" ]; then
  printf '%s\n' "$quality_config_changes"
  echo "Quality tool suppression/baseline/config changes block completion; remove suppression/ignore changes instead" >&2
  exit 1
fi
```

On a dedicated gate-definition PR (`GATE_DEFINITION_CHANGES_PRESENT=true`,
i.e. only gate-definition files changed vs `$TRUSTED_BASE_REF`) the
quality-config hard block is skipped so the PR can legitimately tighten
quality-tool configs, while the forbidden-suppression line scan still runs
and any threshold change must be raise-only (see Thresholds below). A PR that
mixes gate-definition and product changes does not qualify and is blocked.

**Gate-definition isolation rule**: changes to CI/review gate definitions
(Makefile, CI workflow files, ESLint/TypeScript/jscpd/dependency-cruiser/rca
configs, `stryker.config.mjs`, the Lighthouse configs, the Jest/Playwright
configs, formatter configs, review scripts, agent skill files,
required-check declarations) must never piggyback on a product PR. They belong
in a dedicated gate-definition PR with no product, runtime, or unrelated
test-code changes, reviewed on its own. A product PR must not validate itself
against gate definitions it supplies.

**Thresholds** come from `quality.*` in the profile and are raise-only
(canonical floors: `quality.coverage_statements` 100,
`quality.coverage_branches` 100, `quality.coverage_functions` 100,
`quality.coverage_lines` 100, `quality.mutation_msi` seeded from
`stryker.config.mjs` `break`, `quality.lighthouse_desktop` 95,
`quality.lighthouse_mobile` 85; fixed ceilings: `quality.jscpd_clones` 0,
`quality.eslint_errors` 0, `quality.eslint_warnings` 0, `quality.tsc_errors` 0,
`quality.markdownlint_errors` 0, `quality.depcruise_violations` 0,
`quality.visual_diffs` 0; `quality.metrics_enforced` stays `true` — the rca
hard-fail policy lives in `config/metrics-policy.json`). A profile may tighten
these floors, never relax them. Fix the code, never the threshold.

**If CI fails**, invoke the appropriate skill:

| Failure Type                   | Re-run via                                                          | Skill to Use                                                                         |
| ------------------------------ | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Module boundary / import       | `make.lint_deps` target                                             | [architecture](../architecture/SKILL.md)                                             |
| Complexity / rca metrics       | `make.lint_metrics` target                                          | [complexity-management](../complexity-management/SKILL.md)                           |
| ESLint / TypeScript / markdown | `make.lint_eslint` / `make.lint_tsc` / `make.lint_md`               | [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md)                   |
| Duplication (jscpd)            | `make.lint_dup` target                                              | [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md)                   |
| Unit / integration / E2E tests | `make.test_unit_client` / `make.test_integration` / `make.test_e2e` | [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md)                   |
| Mutation testing               | `make.test_mutation` / `make.merge_mutation_reports`                | [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md)                   |
| Visual regression              | `make.test_visual` target                                           | [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md)                   |
| Lighthouse / accessibility     | `make.lighthouse_desktop` / `make.lighthouse_mobile` / `make.a11y`  | [frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md) |
| Component / hook / MUI shape   | -                                                                   | [frontend-component-development](../frontend-component-development/SKILL.md)         |
| Formatting                     | `make.format` target                                                | -                                                                                    |

**DO NOT** finish the task until the `make.ci` target exits `0`.

### Step 7: Run Final AI Review Loop

After the final successful CI run, capture `CI_HEAD="$(git rev-parse HEAD)"`
and run the AI review loop again (same invocation as Step 0, diff base
`$TRUSTED_BASE_REF`) before any push or ready-for-review action. Then assert:

```bash
test "$CI_HEAD" = "$(git rev-parse HEAD)"
test -z "$(git status --short)"
VERIFIED_HEAD="$CI_HEAD"
CURRENT_BASE_JSON="$(gh pr view "$PR" --repo "$PR_REPO" --json baseRefName,baseRefOid)"
test "$BASE_OID" = "$(printf '%s\n' "$CURRENT_BASE_JSON" | jq -r .baseRefOid)"
test "$BASE_REF" = "$(printf '%s\n' "$CURRENT_BASE_JSON" | jq -r .baseRefName)"
```

If the loop applies fixes or changes any tracked file, repeat:

1. Review `git status --short`
2. Commit intentional tracked changes with the relevant review or AI-loop
   reference
3. Re-run the `make.ci` target
4. Re-run the forbidden-suppression and quality-config scans
5. Re-capture `CI_HEAD="$(git rev-parse HEAD)"`
6. Re-run the loop and require `AI_REVIEW_VERDICT: PASS`

Before the final loop, write `PR_HEAD=<CI_HEAD>` plus generated
`COMMENT_META` lines into `PR_COMMENT_EVIDENCE`, then add one validated
`COMMENT|...` evidence line per `COMMENT_META` line. After the final loop,
`git rev-parse HEAD` must still equal the captured `CI_HEAD`,
`git status --short` must be empty, and the current PR `baseRefName` and
`baseRefOid` must still equal the `BASE_REF` and `BASE_OID` captured before
CI. Set `VERIFIED_HEAD="$CI_HEAD"` only after those checks pass. Step 8
reruns this local gate and recomputes `VERIFIED_HEAD` before pushing —
caller-supplied `VERIFIED_HEAD`/`BASE_OID` values are never trusted as proof.
Do not push, mark ready, or declare completion until the loop reports PASS on
the same commit and base that passed CI without leaving new uncommitted
changes. If the loop cannot be run at all, completion is blocked.

### Step 8: Push And Verify GitHub PR Readiness

**8a. Rerun the local readiness gate on a clean worktree** (recompute, don't
trust earlier variables): assert `git status --short` is empty → run the
`make.ci` target (exit `0`) → capture `LOCAL_HEAD` → rewrite ledger metadata
(`PR_HEAD`, fresh `COMMENT_META` lines from a fresh enumeration of all three
comment sources, preserving existing `COMMENT` lines) → validate every
evidence line → run the AI review loop (PASS) → assert `HEAD` unchanged,
worktree clean, and PR base (`baseRefName`/`baseRefOid`) unchanged. Set
`VERIFIED_HEAD="$LOCAL_HEAD"`.

**8b. Push to the actual PR head repository** (fork-aware):

```bash
test "$(git rev-parse HEAD)" = "$VERIFIED_HEAD"
LOCAL_HEAD="$VERIFIED_HEAD"
HEAD_REF="$(gh pr view "$PR" --repo "$PR_REPO" --json headRefName --jq .headRefName)"
PR_HEAD_REPO="$(gh pr view "$PR" --repo "$PR_REPO" --json headRepository --jq .headRepository.nameWithOwner)"
CURRENT_REPO="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"
if [ "$PR_HEAD_REPO" = "$CURRENT_REPO" ]; then
  git push origin HEAD:"$HEAD_REF"
else
  if git remote get-url pr-head >/dev/null 2>&1; then
    git remote set-url pr-head "git@github.com:${PR_HEAD_REPO}.git"
  else
    git remote add pr-head "git@github.com:${PR_HEAD_REPO}.git"
  fi
  git push pr-head HEAD:"$HEAD_REF"
fi
PR_HEAD="$(gh pr view "$PR" --repo "$PR_REPO" --json headRefOid --jq .headRefOid)"
test "$LOCAL_HEAD" = "$PR_HEAD"
```

**8c. Wait for checks** (skip with a degrade note when `ci.provider` is
`null`):

```bash
gh pr checks "$PR" --repo "$PR_REPO" --watch --interval 30
```

**8d. Verify the commit-scoped check rollup on the pushed head**, queried
from the base PR repository (never the fork). Paginate
`statusCheckRollup.contexts(first:100)` on the commit object:

```bash
query='query($owner:String!,$repo:String!,$oid:GitObjectID!,$cursor:String){repository(owner:$owner,name:$repo){object(oid:$oid){... on Commit{statusCheckRollup{contexts(first:100,after:$cursor){pageInfo{hasNextPage endCursor} nodes{__typename ... on CheckRun{name conclusion status detailsUrl checkSuite{app{slug}}} ... on StatusContext{context state targetUrl creator{login}}}}}}}}}'
```

Normalize each node to `{type, name, state, source, url}` (CheckRun →
`check_run` with `checkSuite.app.slug` as source; StatusContext →
`status_context` with `creator.login` as source), then assert:

- The rollup is non-empty; an empty or incomplete check list is a blocker
- Every context has an allowed terminal state:
  `jq -e 'length > 0 and all(.[]; .state | IN("SUCCESS", "SKIPPED", "NEUTRAL"))'`
- Every check named in the profile `ci.required_checks` list is present with
  state `SUCCESS` on this exact commit
- Every live base-branch protection required status/check is present with
  state `SUCCESS` — query the protection rule and compare:

  ```bash
  branch_query='query($owner:String!,$repo:String!,$baseRefName:String!){repository(owner:$owner,name:$repo){ref(qualifiedName:$baseRefName){branchProtectionRule{requiredStatusCheckContexts requiredStatusChecks{context app{slug}}}}}}'
  ```

- GitHub Actions check `detailsUrl` values start with
  `https://github.com/<PR_REPO>/actions/runs/` — checks pointing at another
  repository are not trusted

**8e. Verify a qualifying approval on the pushed head.** Paginate
`pullRequest.reviews(first:100)` selecting
`{url state submittedAt author{login} authorAssociation commit{oid}}` and
require at least one review where:

```text
state == "APPROVED"
commit.oid == LOCAL_HEAD
author.login != PR author
authorAssociation in (OWNER, MEMBER, COLLABORATOR)
submittedAt > latest addressed-comment/evidence event time
```

The "latest evidence event" is the maximum effective time across all ledger
source comments and their commit/reply/decline evidence.

**8f. Poll the final readiness predicate** (retry up to 30 times, 10s apart):

```bash
gh pr view "$PR" --repo "$PR_REPO" --json state,mergeStateStatus,mergeable,reviewDecision,isDraft,reviewRequests,headRefOid,baseRefOid,baseRefName |
jq -e --arg head "$LOCAL_HEAD" --arg base "$BASE_OID" --arg base_ref "$BASE_REF" '
  .headRefOid == $head and
  .baseRefOid == $base and
  .baseRefName == $base_ref and
  .state == "OPEN" and
  .isDraft == false and
  .mergeable == "MERGEABLE" and
  (.mergeStateStatus | IN("CLEAN", "HAS_HOOKS")) and
  .reviewDecision == "APPROVED" and
  ([.reviewRequests[]?] | length) == 0
'
```

**8g. Re-verify after the wait** — checks and reviews can change while
polling, so run the full set again on the same pushed head: unresolved-thread
query shows 0, ledger evidence still validates (review-thread and non-thread
sources), no unaccounted post-snapshot comments (only validated evidence URLs
and a qualifying empty/`FINAL_APPROVAL_NO_ACTION: true` approval are
allowed), required checks still `SUCCESS`, approval still present, readiness
predicate still true. If anything regressed, return to the failing step.

Required state:

- PR `headRefOid` equals local `HEAD` before and after waiting for checks
- PR `baseRefName` and `baseRefOid` still equal the `BASE_REF`/`BASE_OID`
  used for CI, the suppression scan, the final AI review loop, and the
  branch-protection query
- Commit-scoped status/check rollup queried from the base PR repository is
  non-empty; non-required contexts only `SUCCESS`, `SKIPPED`, or `NEUTRAL`
- Every `ci.required_checks` entry and every live base-branch protection
  required status/check is `SUCCESS` on the pushed head; GitHub Actions check
  URLs point at the base PR repository
- Final direct review-thread query after pushed-head verification shows 0
  unresolved review comments
- `PR_COMMENT_EVIDENCE` records the auto-captured snapshot, `PR_HEAD`,
  validated `COMMENT_META` lines, and validated `COMMENT|url|action|evidence`
  lines for every snapshotted comment from all three sources
- No non-evidence comments created/edited after the snapshot (or the
  snapshot/evidence loop was restarted), modulo the qualifying-approval
  exception
- `state` `OPEN`, `isDraft` `false`, `mergeable` `MERGEABLE`,
  `mergeStateStatus` `CLEAN`/`HAS_HOOKS`, `reviewDecision` `APPROVED`,
  `reviewRequests` empty
- Direct review query shows a qualifying `APPROVED` review per 8e

## Constraints (Parameters)

**NEVER**:

- Skip the autonomous AI review loop (`make.ai_review_loop` target or plugin
  script)
- Skip committable suggestions
- Batch unrelated changes in one commit
- Ignore LLM prompts from reviewers
- Apply stale or invalid review suggestions blindly
- Commit without running verification
- Leave questions unanswered
- Accept organizational violations (invoke
  [code-organization](../code-organization/SKILL.md))
- Accept architecture violations (invoke [architecture](../architecture/SKILL.md))
- Add suppression/ignore annotations (an ESLint disable, a TypeScript ignore,
  a Prettier/markdownlint/editorconfig disable, a jscpd or Stryker ignore
  marker, or a dependency-cruiser per-rule exclusion) to "fix" review comments
  or CI failures
- Weaken a TypeScript type, add a `data-testid`, or update a visual snapshot
  without inspecting the diff to make a finding disappear
- Lower any `quality.*` threshold or edit `eslint.config.mjs`,
  `config/metrics-policy.json`, `stryker.config.mjs`, `.jscpd.json`, or the
  dependency-cruiser config to make findings disappear — thresholds are
  raise-only, fix the code instead
- Finish before the `make.ci` target exits `0`
- Finish when the AI review loop was not run after the final CI run
- Finish while `git status --short` reports uncommitted changes after the
  final AI review loop
- Finish while local `HEAD` differs from the PR `headRefOid`
- Finish while GitHub reports failing checks, conflicts, draft status,
  requested changes (when `review.request_changes_blocking` is `true`),
  required review, or a blocking merge state

**ALWAYS**:

- Run the AI review loop before manually addressing PR comments and again
  after the final CI run, before push/ready
- Verify review findings against current code before applying them
- Commit each suggestion separately with URL reference
- Invoke [code-organization](../code-organization/SKILL.md) for structural
  issues and [architecture](../architecture/SKILL.md) for module-boundary / DI
  violations; route a confirmed code fix to the `react-implementer` agent
- Run the `make.ci` target after implementing all changes
- Scan the PR diff for forbidden suppression/ignore directives and blocked
  quality-config changes
- Push and verify PR `headRefOid` equals local `HEAD`
- Check `gh pr checks` and `gh pr view` after pushing
- Address ALL CI failures before finishing
- Mark conversations resolved after addressing

## Format (Output)

**Commit Message Template**:

```text
Apply review suggestion: [concise description]

[Optional: explanation if non-obvious]

Ref: https://github.com/<owner>/<repo>/pull/XX#discussion_rYYYYYYY
```

**Final Verification**:

```text
✅ direct GitHub GraphQL review-thread query shows 0 unresolved
✅ make.ci target exits 0
✅ final AI review loop reports AI_REVIEW_VERDICT: PASS after CI
✅ git status --short is empty after the final loop
✅ PR baseRefName/baseRefOid still match the base used for CI, the final loop, and the branch-protection query
✅ local HEAD matches the PR headRefOid
✅ base-repository check rollup: non-empty, no disallowed non-required states, every ci.required_checks entry and live branch-protection check SUCCESS, Actions URLs in the base repo
✅ final review-thread query after pushed-head verification shows 0 unresolved
✅ PR_COMMENT_EVIDENCE has auto-captured snapshot metadata, pushed HEAD, comment updatedAt/body hashes, and validated trusted-author action/evidence for every snapshotted comment URL
✅ no non-evidence comments created/edited after the snapshot (qualifying approval exception only)
✅ gh pr view shows OPEN, no conflicts, not draft, mergeStateStatus CLEAN/HAS_HOOKS, reviewDecision APPROVED, no reviewRequests
✅ direct review query shows an APPROVED review on the pushed HEAD, submitted after the latest evidence event, by a non-author OWNER/MEMBER/COLLABORATOR reviewer
```

## Verification Checklist

- [ ] Initial AI review loop run against the trusted PR base
- [ ] All PR comments retrieved (`make.pr_comments` target or plugin script)
- [ ] Snapshot captured automatically; ledger initialized
- [ ] Comments categorized by type (suggestion/prompt/architecture/a11y/question/feedback)
- [ ] Stale or duplicate comments recorded with concrete reasons (decline evidence)
- [ ] Architecture verified using appropriate skills
- [ ] `make.lint_deps` target passes (`quality.depcruise_violations` = 0)
- [ ] Committable suggestions applied and committed separately
- [ ] LLM prompts executed and implemented
- [ ] Accessibility concerns fixed in the component and re-audited (`make.a11y`)
- [ ] Questions answered (code or reply evidence)
- [ ] General feedback evaluated and addressed
- [ ] `make.ci` target exits `0`
- [ ] PR diff scanned for forbidden suppression/ignore directives and quality-config changes
- [ ] Final AI review loop reports PASS after CI, on the same commit
- [ ] `git status --short` empty after the final loop
- [ ] PR base unchanged since the gated CI run
- [ ] Direct review-thread query shows zero unresolved
- [ ] Ledger complete and validated for every snapshotted comment (all three sources)
- [ ] No unaccounted post-snapshot comments
- [ ] Local `HEAD` pushed and equal to PR `headRefOid`
- [ ] Check rollup verified on the pushed head (`ci.required_checks` + branch protection), or skipped with a degrade note when `ci.provider` is `null`
- [ ] Final post-wait re-verification passed (threads, evidence, checks, approval, readiness predicate)
- [ ] Qualifying `APPROVED` review present on the pushed `HEAD`
- [ ] All conversations marked resolved on GitHub

## Quick Reference: When to Use Related Skills

| Issue                                  | Skill to Use                                                                         |
| -------------------------------------- | ------------------------------------------------------------------------------------ |
| Component/file in wrong directory      | [code-organization](../code-organization/SKILL.md)                                   |
| Vague naming                           | [code-organization](../code-organization/SKILL.md)                                   |
| Module-boundary / DI violations        | [architecture](../architecture/SKILL.md)                                             |
| dependency-cruiser failures            | [architecture](../architecture/SKILL.md)                                             |
| Complexity / rca metrics too high      | [complexity-management](../complexity-management/SKILL.md)                           |
| Test or mutation failures              | [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md)                   |
| Lint / type / markdown / duplication   | [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md)                   |
| Component / hook / MUI shape           | [frontend-component-development](../frontend-component-development/SKILL.md)         |
| Lighthouse / accessibility regressions | [frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md) |
| Quality standards                      | [quality-standards](../quality-standards/SKILL.md)                                   |

## Related Skills

- [code-organization](../code-organization/SKILL.md) — directory/type and naming conventions (bulletproof-react placement, `UI*` prefix, type-only files)
- [architecture](../architecture/SKILL.md) — module boundaries, tsyringe DI seams, dependency-cruiser layers, path-alias rules
- [complexity-management](../complexity-management/SKILL.md) — reduces cyclomatic/cognitive complexity against the rust-code-analysis gate
- [frontend-component-development](../frontend-component-development/SKILL.md) — React components, hooks, forms, and MUI/Emotion shape
- [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md) — Jest/Testing Library, Playwright E2E/visual, and Stryker mutation coverage
- [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md) — formatting, ESLint, TypeScript, markdown, jscpd, and metrics
- [frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md) — Lighthouse, web-vitals, and accessibility
- [quality-standards](../quality-standards/SKILL.md) — overall quality metrics and thresholds
- [ci-workflow](../ci-workflow/SKILL.md) — comprehensive CI checks
