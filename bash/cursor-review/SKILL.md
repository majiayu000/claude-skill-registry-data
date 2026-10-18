---
name: cursor-review
description: "Run a Cursor Composer review as an advisory second opinion while keeping the primary review verdict on the host brain. Use when user invokes cursor:review, asks Cursor to review, or wants composer to sanity-check a diff. Cursor never owns APPROVE/REQUEST_CHANGES."
description-en: "Run a Cursor Composer review as an advisory second opinion while keeping the primary review verdict on the host brain. Use when user invokes cursor:review, asks Cursor to review, or wants composer to sanity-check a diff. Cursor never owns APPROVE/REQUEST_CHANGES."
description-ja: "Cursor Composer に advisory second opinion としてレビューさせるスキル。cursor:review、Cursor にレビューして、composer で差分を sanity check して、という時に使う。primary verdict は常に host brain が持ち、Cursor は APPROVE/REQUEST_CHANGES を所有しない。"
allowed-tools: ["Read", "Bash", "Grep"]
argument-hint: "[--base <ref>] [review-scope]"
user-invocable: true
---

# cursor:review - Advisory Cursor Review

Cursor Composer (`composer-2.5-fast`) を read-only second opinion として使う review skill。primary verdict は host brain (Opus / Claude role) が出す。

## Quick Reference

```bash
cursor:review --base origin/main
cursor:review "Phase 88.5 command namespace diff"
```

## Rules

- Cursor review is advisory. The final verdict must come from the host reviewer.
- Do not pass `--write` to `cursor-companion.sh`.
- Use resolver/model routing, not direct env checks:

  ```bash
  bash scripts/resolve-impl-backend.sh --backend cursor --role reviewer
  bash scripts/model-routing.sh --host cursor --role worker --field model
  ```

- Prefer the existing `harness-review` contract when a full review is requested. This command exists for users who explicitly ask for the Cursor lane.

## Flow

1. Resolve the Harness helper root:

   ```bash
   HARNESS_PLUGIN_ROOT="${HARNESS_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT:-}}"
   if [ -z "$HARNESS_PLUGIN_ROOT" ] && [ -n "${CLAUDE_SKILL_DIR:-}" ]; then
     probe="$(cd "${CLAUDE_SKILL_DIR}" && pwd)"
     while [ "$probe" != "/" ] && [ ! -d "$probe/scripts" ]; do
       probe="$(cd "$probe/.." && pwd)"
     done
     [ -d "$probe/scripts" ] && HARNESS_PLUGIN_ROOT="$probe"
   fi
   if [ -z "$HARNESS_PLUGIN_ROOT" ]; then
     echo "ERROR: HARNESS_PLUGIN_ROOT is not set and could not be derived from CLAUDE_PLUGIN_ROOT or CLAUDE_SKILL_DIR" >&2
     exit 2
   fi
   ```

2. Determine review scope:

   ```bash
   BASE_REF="${TASK_BASE_REF:-origin/main}"
   REVIEW_SCOPE="${ARGUMENTS:-}"
   if [ -n "${REVIEW_SCOPE}" ]; then
     set -- ${REVIEW_SCOPE}
     while [ "$#" -gt 0 ]; do
       case "$1" in
         --base)
           BASE_REF="${2:?--base requires a ref}"
           shift 2
           ;;
         --base=*)
           BASE_REF="${1#--base=}"
           shift
           ;;
         *)
           shift
           ;;
       esac
     done
   fi
   DIFF_STAT="$(git diff --stat "${BASE_REF}..HEAD")"
   DIFF_TEXT="$(git diff "${BASE_REF}..HEAD")"
   ```

3. Ask Cursor in read-only mode:

   ```bash
   PROMPT="$(cat <<EOF
Review this diff as an advisory second opinion.
Base ref: ${BASE_REF}
Requested scope: ${ARGUMENTS:-full diff}

Focus on bugs, regressions, missing tests, and unsafe assumptions. Do not propose broad refactors.

Diff stat:
${DIFF_STAT}

Diff:
${DIFF_TEXT}
EOF
)"
   bash "${HARNESS_PLUGIN_ROOT}/scripts/cursor-companion.sh" task "${PROMPT}"
   ```

4. Host reads Cursor's output and performs the primary review:

   - Findings first, ordered by severity.
   - Mark Cursor-originated points as advisory when used.
   - `APPROVE` / `REQUEST_CHANGES` must be the host decision, not a copied Cursor verdict.

## Output

Use the standard review shape:

- findings
- open questions
- validation run
- final host verdict
