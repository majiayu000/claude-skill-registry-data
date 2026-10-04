---
name: ato-review
version: 1.1.0
description: |
  Before committing any non-trivial change, dispatch the diff to a reviewer
  runtime via ATO (`ato dispatch <reviewer> --session <id>`), parse the
  numbered/severity-tagged findings, apply or defer each one with a
  recorded justification, then commit. Fights the "build passes therefore
  ship it" failure mode — what Garry Tan calls the AI agent complexity
  ratchet.

  Place in the v2.16 stack: this skill is the LAST gate. `ato-warroom`
  decides the design; `ato-mission` runs the multi-step work and
  produces the diff; `ato-review` checks the diff before commit. When
  the review is part of a Mission, dispatch the review with
  `--require-tools read_file,grep,git_diff,git_log` so the reviewer can
  walk the source itself instead of reasoning from a paraphrase
  (PR-1.5 tool surface). Receipts land in `execution_logs` and the
  Mission narrative.

  Fires automatically before commits touching public surface
  (CLI subcommands, Tauri commands, MCP tools, schema migrations, security
  boundaries) or whenever a diff exceeds ~50 LOC of behavior change.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
---

## When this skill fires

Before `git commit`, check whether any of these apply to the staged diff:

- Adds or changes a **public surface**: CLI subcommand or flag, Tauri command, MCP tool, REST endpoint, exported function signature, schema migration (`ALTER TABLE`, `CREATE TABLE`), `tauri.conf.json`, `package.json` `bin` entries.
- Touches a **security boundary**: shell-out / `Command::new` / IPC allowlist / authentication code / file-system writes outside the repo.
- Is **>50 lines of behavior change** (not counting test fixtures, snapshots, or pure formatting).
- Adds a **new module / file** that's larger than ~30 LOC.
- Changes an existing **schema** or **persistence shape**.

If none apply (small typo fix, comment-only change, doc-only edit, dependency bump with no code change), skip this skill and commit normally. Note the reason in your turn message so the next reader sees you decided rather than forgot.

If any apply, run the procedure below.

## Procedure

### 1. Capture the diff

```bash
# Capture both staged and unstaged so the review sees what the commit will look like.
git diff HEAD > /tmp/ato-review-$$.patch
```

The "When this skill fires" section above is authoritative. The `wc -l`
heuristic is *only* a final tie-breaker for diffs that match none of the
public-surface / security-boundary / new-file / schema triggers:

```bash
if [ $(wc -l < /tmp/ato-review-$$.patch) -lt 10 ] \
   && ! grep -qE '#\[tauri::command\]|server\.tool\(|CREATE TABLE|ALTER TABLE|Command::new|spawn\(' /tmp/ato-review-$$.patch; then
    rm /tmp/ato-review-$$.patch
    exit 0  # genuinely trivial
fi
```

A 9-line diff that adds a Tauri command or runs `Command::new` is not
trivial. Trust the triggers over the line count.

### 2. Open or reuse a review session

The session keeps reviewer context across multiple turns of one feature, so the reviewer doesn't re-derive the codebase each commit.

```bash
# Try to find an existing review session for the active branch.
# Pass $BRANCH as a python argv to avoid nesting shell quotes inside a
# Python f-string (review-of-the-skill caught this — the earlier version
# had mismatched quotes that silently SyntaxError'd, so every commit
# opened a fresh session instead of reusing one).
BRANCH=$(git branch --show-current)
SID=$(ato sessions list --limit 20 2>/dev/null | python3 -c '
import sys, json
branch = sys.argv[1]
sessions = json.load(sys.stdin)
for s in sessions:
    if s.get("title", "").startswith("review/" + branch):
        print(s["id"]); break
' "$BRANCH" 2>/dev/null)

# If none, open one. Default reviewer is minimax; allow user to override
# via $ATO_REVIEWER env var.
REVIEWER="${ATO_REVIEWER:-minimax}"
if [ -z "$SID" ]; then
    SID=$(ato sessions new --runtime "$REVIEWER" --title "review/$BRANCH" 2>/dev/null \
          | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
fi
echo "Review session: $SID  reviewer: $REVIEWER"
```

ATO's `sessions new` and `sessions list` commands emit pure JSON to stdout
(diagnostics on stderr) — that's a stable contract, so direct piping into
`json.load` is safe.

If `ato` isn't on PATH or the user has no `$ATO_REVIEWER` configured and no MiniMax / Grok / DeepSeek / Qwen / OpenRouter key, tell the user once and skip — don't block the commit on infrastructure they don't have.

### 3. Dispatch the diff for review

The prompt is the most load-bearing part. The reviewer needs to know:

- The change is a real diff being committed today
- What categories of issues to look for (calibrated to the diff)
- The expected output format (numbered, severity-tagged, with concrete fixes)

```bash
DIFF=$(cat /tmp/ato-review-$$.patch)
PROMPT="You are a senior reviewer for a multi-runtime AI agent ops platform written in
Rust + TypeScript. This diff is about to be committed to main. Critique it.

Look specifically for:
1. **Security**: shell injection, IPC trust boundaries, SQL injection, path traversal,
   unbounded user input passed to Command::new / spawn / fs writes.
2. **Race conditions / cache invalidation**: any concurrent writers, stale reads, UI
   that re-renders before the backend confirms.
3. **Validation gaps**: input ranges, regex shapes, empty / null handling at edges.
4. **Contract drift**: a flag rename, a Tauri command shape change, a CLI argv shift —
   anything that would break a wrapper or earlier caller silently.
5. **Bugs you can spot from the diff alone**, especially around error handling and
   resource cleanup.

Reply with a numbered list. For each finding:
  N. **SEVERITY — short title** (HIGH / MEDIUM / LOW / INFO)
     Brief description.
     **Fix:** one concrete diff or sentence.

Be brief — 3–8 findings, not a wall of text. Skip the obvious. If a category has
nothing wrong, don't enumerate it. If a candidate finding is wrong on closer look,
say so explicitly. Do NOT invent findings to pad the list.

DIFF:
\`\`\`
$DIFF
\`\`\`"

# Bound the dispatch so a hung reviewer doesn't block the commit forever.
# Coreutils `timeout` is available on Linux; on macOS install via
# `brew install coreutils` (gtimeout) or fall back to running without.
TIMEOUT=${ATO_REVIEW_TIMEOUT:-180}
TIMEOUT_CMD=""
if command -v timeout >/dev/null 2>&1; then
    TIMEOUT_CMD="timeout $TIMEOUT"
elif command -v gtimeout >/dev/null 2>&1; then
    TIMEOUT_CMD="gtimeout $TIMEOUT"
fi
$TIMEOUT_CMD ato dispatch "$REVIEWER" "$PROMPT" --session "$SID" --human \
    | tee /tmp/ato-review-findings-$$.txt
DISPATCH_RC=${PIPESTATUS[0]}
if [ "$DISPATCH_RC" = "124" ]; then
    echo "Review timed out after ${TIMEOUT}s. Proceeding without review — note in commit."
fi
```

If the dispatch fails (network, quota, key missing), surface the error to the user but do NOT auto-retry — they may want to skip the review for this commit.

After the dispatch returns, verify the response actually contains review
findings before triaging:

```bash
# Findings should be numbered + severity-tagged. If grep finds none, the
# reviewer probably returned prose or freeform text — surface that as a
# warning so we don't silently advance to commit thinking the review
# was clean.
if ! grep -qE '^\s*[0-9]+\.\s+\*\*[A-Z]+' /tmp/ato-review-findings-$$.txt; then
    echo "WARN: review output did not match the expected numbered+severity format."
    echo "      Eyeball /tmp/ato-review-findings-$$.txt before committing."
fi
```

### 4. Triage findings

For each numbered finding in the response:

- **HIGH** → must apply before committing. Edit the code, rebuild, re-stage.
- **MEDIUM** → apply unless there's a specific reason not to. Document the reason in the commit message under a `Deferred from review:` line.
- **LOW / INFO** → judgment call. Apply if cheap (<5 LOC, no design implication). Defer otherwise.

Verify findings against the actual diff before applying. The reviewer can hallucinate — refer to the v2.3.38 dogfood pass which caught a real inline-code-fence bug AND surfaced multiple non-bugs that didn't apply to the actual code. Grep + read the cited file/line before committing the fix.

Anti-pattern: applying every finding mechanically. The signal-to-noise on these reviews is real but imperfect; you're the human-in-the-loop even when no human is in the loop.

### 5. Re-build + re-test

After applying findings:

```bash
# Match the project's QA §0:
cargo build --manifest-path apps/cli/Cargo.toml -p ato
cargo build --manifest-path apps/desktop/src-tauri/Cargo.toml
cargo test --manifest-path apps/cli/Cargo.toml -p ato
cd apps/desktop && npx vite build && cd -
```

If any step fails, fix the failure before committing. The pre-commit hook will catch this anyway, but catching it now means one fewer round-trip.

### 6. Commit with the review note

Include a `### Dogfood + review process` section in the commit body listing:

- Which reviewer ran (`minimax` / `grok` / etc.)
- What the headline findings were
- Which ones were applied vs deferred with justification

Example:

```
### Dogfood + review process

MiniMax-reviewed the diff before commit. Findings:
- MEDIUM: IPC validation on days/threshold → applied (bounds check in lock_ratchet)
- LOW: agent slug regex → applied (frontend regex guard)
- LOW: ato-binary fallback could be clearer → deferred (intentional graceful
  fallback so a post-startup ato install still works)
- INFO: targetKey computed in 3 sites → applied (extracted helper)
```

This commits the *audit trail* of the review, not just the code. A future reader can see why a finding wasn't applied without spelunking through chat history.

### 7. Cleanup

```bash
rm -f /tmp/ato-review-$$.patch /tmp/ato-review-findings-$$.txt
```

The session itself stays open — next commit on this branch reuses it via the `review/<branch>` title lookup in step 2.

## Override / skip

There are legitimate reasons to skip review on a specific commit:

- **WIP commit you'll squash later** — note `[wip]` in the subject.
- **Reviewer unreachable** (no network, no key configured) — proceed with a `Review skipped: <reason>` line in the commit body.
- **Trivial / mechanical change** the trigger heuristics caught as a false positive — note "trivial" in the commit body.

Don't skip silently. The point of the skill is to make "did I review?" a yes-or-no question with a recorded answer.

## Why this skill exists

Tan's "AI Agent Complexity Ratchet" (May 2026) argues that AI agents make 90% test
coverage free — agents don't experience effort writing the fourteenth edge-case
test. The same principle applies to code review: dispatching a diff to a second
runtime costs cents and seconds, but humans (and Claude in flow) routinely skip it
because "build passes." Build passing isn't a review. Tests passing isn't a review.
A second runtime reading the actual diff with a fresh prior is a review.

ATO's Phase 6 cluster (sessions, bridge, ratchet) was built to make this loop
cheap and ergonomic. This skill makes "use it" the default rather than something
to remember.

## Pairs well with

- **`ato ratchet check`** as a pre-deploy CI gate — quality floors complement
  per-commit review.
- **`ato dispatch <runtime> --tag-bridge`** when a single reviewer's pass leaves
  you uncertain; bridge into a second runtime for a second opinion.
- **Activity feed (`ato posts list --kind approval_request`)** to surface review
  spinning to a human when the bridge can't converge.
