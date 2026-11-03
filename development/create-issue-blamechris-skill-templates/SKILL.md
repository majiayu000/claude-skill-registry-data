---
description: "Create a standardized GitHub issue with labels and traceability."
---

# /create-issue

Create a standardized GitHub issue with labels and traceability.

## Arguments

- `$ARGUMENTS` - Issue title (required). Optionally followed by flags:
  - `--from-pr N` — Link to source PR
  - `--from-issue N` — Link to source issue (e.g. a decomposition parent)
  - `--comment-url URL` — Link to specific review comment
  - `--complexity low|medium|high` — Set complexity label
  - `--label NAME` — Additional label (repeatable)
  - `--standalone` — This issue genuinely has no source; if nothing else resolves one, forces `Filed from: none` instead of the refusal below

## Instructions

### 1. Parse Arguments and Gather Context

Extract the title and any flags from `$ARGUMENTS`. **Resolve `FILED_FROM` — the source for the required `Filed from:` line (#268) — in this order, first match wins:**

1. `--from-pr N` or `--from-issue N` (explicit flag) → `#N`, plus `--comment-url` in parentheses if given
2. Not explicit, but the current branch has an **open** PR → that PR, auto-detected. `gh pr view` also returns a branch's closed or merged PR, which is not the source of work being filed now, so only an open one counts (#363). To file from a closed or merged PR, such as a follow-up from the review of a PR that has since merged, pass `--from-pr N`
3. Not explicit, no open PR on this branch, but a session id is available → `session ${CLAUDE_CODE_SESSION_ID}`
4. `--standalone` → `none`; nothing resolved (no flag, no PR, no session, no `--standalone`) → REFUSE and ask the user rather than silently defaulting to `none` — the whole point of Critical Rule 7 is that `none` is a deliberate choice, never a fallback for "didn't figure it out"

```bash
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)

# Auto-detect the source PR from the current branch, OPEN only (#363): `gh pr view` returns
# the branch's PR in any state. A detached HEAD, or a branch with no PR, reads as none.
CURRENT_PR=$(gh pr view --json number,state -q 'select(.state == "OPEN") | .number' 2>/dev/null || echo "")

# Flag values from $ARGUMENTS, empty if the flag was not given:
FROM_PR="${FROM_PR:-}"           # --from-pr N
FROM_ISSUE="${FROM_ISSUE:-}"     # --from-issue N
COMMENT_URL="${COMMENT_URL:-}"   # --comment-url URL
STANDALONE="${STANDALONE:-}"     # --standalone
COMPLEXITY="${COMPLEXITY:-}"     # --complexity low|medium|high
EXTRA_LABELS="${EXTRA_LABELS:-}" # --label NAME, comma-joined when repeated

# FILED_FROM per the resolution order above. SOURCE_PR is the PR it names, if any: it (or
# --comment-url) selects §3's From-Review form and §4's from-review label.
SOURCE_PR=""
if [ -n "$FROM_PR" ]; then
  FILED_FROM="#${FROM_PR}"; SOURCE_PR="$FROM_PR"
elif [ -n "$FROM_ISSUE" ]; then
  FILED_FROM="#${FROM_ISSUE}"
elif [ -n "$CURRENT_PR" ]; then
  FILED_FROM="#${CURRENT_PR}"; SOURCE_PR="$CURRENT_PR"
elif [ -n "${CLAUDE_CODE_SESSION_ID:-}" ]; then
  FILED_FROM="session ${CLAUDE_CODE_SESSION_ID}"
elif [ -n "$STANDALONE" ]; then
  FILED_FROM="none"
else
  echo "REFUSE: no source resolved — pass --from-pr N, --from-issue N, or --standalone" >&2
  exit 1
fi
if [ -n "$COMMENT_URL" ] && [[ "$FILED_FROM" == \#* ]]; then
  FILED_FROM="${FILED_FROM} (${COMMENT_URL})"
fi
```

### 2. Check for Duplicates

Before creating, scan for existing issues with similar titles:

```bash
# Search open issues for potential duplicates
gh issue list --state open --search "${ISSUE_TITLE}" --json number,title --limit 5
```

If a close match exists, show it to the user and ask whether to proceed or reference the existing issue instead.

### 3. Build Issue Body

Construct the issue body based on available context.

#### From-Review Issue (has source PR or comment URL)

```markdown
## Context

Filed from: ${FILED_FROM}

Identified during review of PR #${SOURCE_PR}.

{{If comment URL provided and not already folded into Filed from: above:}}
**Review comment:** ${COMMENT_URL}

{{If file/line can be extracted from comment:}}
**Location:** \`${FILE_PATH}:${LINE_NUMBER}\`

## Description

What needs to be done and why. Be specific — another developer should be able to pick this up without reading the original review thread.

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
```

#### Standalone Issue (no review context)

```markdown
## Context

Filed from: ${FILED_FROM}

## Description

What needs to be done and why.

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
```

The `## Context` section, and its `Filed from:` first line, is present in **every** issue this
skill files — including the standalone template. `${FILED_FROM}` is never left as a
placeholder: it is one of the four resolved forms from step 1 (`#N`, `#N (<url>)`,
`session <id>`, or the literal `none`).

### 4. Determine Labels

Build the label set:

```bash
: "${FILED_FROM:?run the block in §1 first, in the same shell}"
LABELS="enhancement"

# Always add from-review if this came from a PR review
if [ -n "$SOURCE_PR" ] || [ -n "$COMMENT_URL" ]; then
  LABELS="$LABELS,from-review"
fi

# Add complexity label if specified
# No complexity label family exists here; leave COMPLEXITY empty.
if [ -n "$COMPLEXITY" ]; then
  LABELS="$LABELS,complexity:$COMPLEXITY"
fi

# Add any extra --label flags
if [ -n "$EXTRA_LABELS" ]; then
  LABELS="$LABELS,$EXTRA_LABELS"
fi
```

**Verify labels exist** before using them. If a label doesn't exist in the repo, skip it with a warning rather than failing. List the labels once, with `--limit 500`: `gh label list` returns only 30 by default, oldest first, so without it every label past the 30th reads as missing and is dropped (#357). Match names case-insensitively, as GitHub does:

```bash
: "${LABELS:?run the label-building block above first, in the same shell}" "${REPO:?run the block in §1 first, in the same shell}"
# A failed listing stops here: reading it as "no labels exist" would file the issue unlabeled.
REPO_LABELS=$(gh label list --limit 500 --json name -q '.[].name') \
  || { echo "REFUSE: could not list labels in ${REPO}" >&2; exit 1; }
KEPT=""
while IFS= read -r LABEL; do
  [ -n "$LABEL" ] || continue
  if grep -qixF -- "$LABEL" <<< "$REPO_LABELS"; then
    KEPT="${KEPT:+$KEPT,}$LABEL"
  else
    echo "Warning: '${LABEL}' label not found in ${REPO}; filing without it" >&2
  fi
done <<< "$(printf '%s\n' "$LABELS" | tr ',' '\n')"
LABELS="$KEPT"
```

### 5. Create the Issue

```bash
ISSUE_URL=$(gh issue create \
  --title "${ISSUE_TITLE}" \
  --label "${LABELS}" \
  --body "$(cat <<'EOF'
${ISSUE_BODY}
EOF
)")
```

### 6. Extract Issue Number

```bash
ISSUE_NUM=$(echo "$ISSUE_URL" | grep -oE '[0-9]+$')
```

### 7. Report to User

Output a **summary table** — this is the PRIMARY output:

```markdown
| Issue | Title | Labels | Source |
|-------|-------|--------|--------|
| #${ISSUE_NUM} | ${ISSUE_TITLE} | from-review, complexity:low | PR #${SOURCE_PR} |
```

Then below the table:
- Issue URL (clickable)
- Labels applied
- Source PR link (if applicable)
- Review comment link (if applicable)

## Critical Rules

1. **NO attribution** — Follow Zero Attribution Policy.
2. **Check for duplicates** — Always search before creating. Don't create duplicate issues.
3. **Labels must exist** — Verify labels exist in the repo, listing them with `--limit 500` (§4): gh's default of 30 reads every newer label as missing. Skip missing labels gracefully.
4. **Be specific** — The issue description must be self-contained. Another developer should understand it without reading the review thread.
5. **Always include acceptance criteria** — Even if just one checkbox. Issues without criteria are hard to close confidently.
6. **Link to source** — If from a review, always include the PR number and comment URL in the body.
7. **The `Filed from:` line is required and machine-read — the four forms, and never omitted** (#268). Every issue this skill files opens `## Context` with exactly one of: `Filed from: #NNN`, `Filed from: #NNN (<url>)`, `Filed from: session <id>`, or `Filed from: none`. It is what `assets/scripts/filed-from.py check` and `chain` read to compute whether a PR spawned follow-on work and to walk a rework chain without a human re-reading every body — an issue filed without it is invisible to both. `none` is a real, deliberate choice for a genuinely standalone issue, never a default reached by skipping the resolution order in step 1.
