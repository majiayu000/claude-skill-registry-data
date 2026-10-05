---
name: tutorial-qa-to-prod
description: Use when a tutorial author has previewed a tutorial in the QA channel (/tutorials-qa/) and wants to promote it to PROD — copies the tutorial markdown from the private sap-tutorials/<product>-Contribution repo (QA source) to the canonical public sap-tutorials/Tutorials repo (PROD source) and opens a PR in each, cross-linked. Triggers on "promote this tutorial to prod", "copy from QA to PROD", "publish my QA tutorial", "move <slug> from Contribution to Tutorials".
---

# Promote a tutorial from QA (Contribution) to PROD (canonical Tutorials)

An author edits and previews a tutorial in its product-specific
**`sap-tutorials/<product>-Contribution`** repo, served on the platform's QA
channel at `/tutorials-qa/<slug>`. Promoting it to PROD means landing the same
markdown in the **canonical public repo `sap-tutorials/Tutorials`** at the same
`tutorials/<slug>/<slug>.md` path. Merging the `Tutorials` PR is what the PROD
content rebuild consumes — the platform auto-discovers `Tutorials` content and
republishes to the PROD HANA BLOBs.

The two repos share **no git fork network**, so one cross-repo PR is impossible.
This skill copies the file once and opens **one PR in each repo**, cross-linked.

## Non-negotiable facts (verified 2026-09-15)

- **Host is `github.com`, NOT `github.tools.sap`.** Always `export GH_HOST=github.com`.
- **Default branches DIFFER per repo — never hardcode.**
  - Canonical `sap-tutorials/Tutorials` (PROD) → **`master`**.
  - `sap-tutorials/<product>-Contribution` (QA) → **`main`**.
  - Resolve each repo's default with the API (Step 0); do not assume.
- **`*-Contribution` repos are private** → `raw.githubusercontent.com` 404s.
  Verify pushed content via the authenticated contents API, not raw curl.
- **Path parity.** Both repos use `tutorials/<slug>/<slug>.md`. Same slug → same path.
- **First promotion is a CREATE, not an update.** A QA-only tutorial does NOT
  exist in `Tutorials` yet (contents API returns 404). Handle create vs update.
- **No `tutorials-ims` code change is needed.** The platform auto-discovers any
  org repo with a `tutorials/` folder; merging the `Tutorials` PR triggers PROD.

## Workflow

Work through the GitHub contents API (`gh api`) — do NOT clone `Tutorials`; it is
huge. Use `$CLAUDE_JOB_DIR/tmp` or a scratch dir for the file. Set
`export GH_HOST=github.com` first.

### Step 0 — Resolve inputs and per-repo default branches

Identify the QA repo (`sap-tutorials/<product>-Contribution`), the slug, and the
path `tutorials/<slug>/<slug>.md`. Then resolve BOTH default branches — do not
assume:

```bash
export GH_HOST=github.com
CONTRIB=sap-tutorials/<product>-Contribution
MAIN=sap-tutorials/Tutorials
PATHREL="tutorials/<slug>/<slug>.md"

CONTRIB_DEF=$(gh api "repos/$CONTRIB" --jq '.default_branch')   # expect: main
MAIN_DEF=$(gh api "repos/$MAIN"    --jq '.default_branch')      # expect: master
```

### Step 1 — Fetch the QA source (source of truth for the copy)

The QA file is what the author previewed and approved — it is authoritative.

```bash
CONTRIB_SHA=$(gh api "repos/$CONTRIB/contents/$PATHREL?ref=$CONTRIB_DEF" --jq '.sha')
gh api "repos/$CONTRIB/contents/$PATHREL?ref=$CONTRIB_DEF" --jq '.content' | base64 -d > file.md
```

If this 404s, the slug/path is wrong — re-confirm with the author. Do NOT invent content.

### Step 2 — Determine PROD state: CREATE or UPDATE (+ drift guard)

```bash
if MAIN_SHA=$(gh api "repos/$MAIN/contents/$PATHREL?ref=$MAIN_DEF" --jq '.sha' 2>/dev/null); then
  MODE=update
else
  MODE=create   # QA-only tutorial, first promotion — no sha, no drift check
fi
```

- **MODE=create** → nothing in PROD to clobber. Proceed; the contents PUT omits `sha`.
- **MODE=update** → PROD already has this tutorial. **DRIFT GUARD:** diff the
  current PROD file against the QA file you fetched. If PROD has content the QA
  copy would silently discard (someone edited PROD directly, or the repos have
  drifted), **STOP and show the author the diff** before overwriting:

  ```bash
  gh api "repos/$MAIN/contents/$PATHREL?ref=$MAIN_DEF" --jq '.content' | base64 -d > prod-current.md
  diff prod-current.md file.md && echo "IN SYNC (no-op)" || echo "DRIFT — review below before promoting"
  ```

  If `diff` is empty, the promotion is a no-op — tell the author PROD already
  matches QA; don't open an empty PR. If it differs, that's the expected
  promotion delta — but confirm the diff is only the author's intended change,
  not an unrelated PROD edit being reverted.

### Step 3 — For EACH repo, branch + commit the copied file

Same branch name in both (e.g. `promote/<slug>-to-prod`). QA repo commits the
same content back to itself on a branch (so the promotion is auditable there
too); PROD repo receives the copy. Use each repo's OWN default branch as base
and each repo's OWN current file sha.

```bash
promote_to() {   # $1=repo  $2=default-branch  $3=current-file-sha-or-empty
  local REPO="$1" DEF="$2" CUR_SHA="$3" BR="promote/<slug>-to-prod"
  local BASE_SHA; BASE_SHA=$(gh api "repos/$REPO/git/ref/heads/$DEF" --jq '.object.sha')
  gh api "repos/$REPO/git/refs" -f ref="refs/heads/$BR" -f sha="$BASE_SHA" >/dev/null

  local B64; B64=$(base64 -w0 file.md)
  if [ -n "$CUR_SHA" ]; then
    printf '{"message":"docs(%s): promote to PROD","branch":"%s","sha":"%s","content":"%s"}' \
      "<slug>" "$BR" "$CUR_SHA" "$B64" > payload.json
  else
    printf '{"message":"docs(%s): promote to PROD","branch":"%s","content":"%s"}' \
      "<slug>" "$BR" "$B64" > payload.json
  fi
  gh api -X PUT "repos/$REPO/contents/$PATHREL" --input payload.json --jq '.commit.sha'

  # verify byte-for-byte (works on private repos)
  gh api "repos/$REPO/contents/$PATHREL?ref=$BR" --jq '.content' | base64 -d > pushed.md
  diff file.md pushed.md && echo "MATCH ($REPO)" || { echo "MISMATCH ($REPO) — STOP"; return 1; }
}

promote_to "$CONTRIB" "$CONTRIB_DEF" "$CONTRIB_SHA"           # QA branch (audit)
promote_to "$MAIN"    "$MAIN_DEF"    "${MAIN_SHA:-}"          # PROD copy (empty sha => create)
```

Do not open a PR for a repo until its `promote_to` printed `MATCH`.

### Step 4 — Open a PR in each repo, cross-linked

```bash
# PROD first (the one that matters), base = its OWN default branch
PROD_PR=$(gh pr create --repo "$MAIN" --base "$MAIN_DEF" --head promote/<slug>-to-prod \
  --title "Promote <slug> to PROD" \
  --body "Promotes QA-previewed tutorial \`<slug>\` to PROD. Paired QA PR: <fill after>. Merging this triggers the PROD content rebuild." )

QA_PR=$(gh pr create --repo "$CONTRIB" --base "$CONTRIB_DEF" --head promote/<slug>-to-prod \
  --title "Promote <slug> to PROD (QA-side record)" \
  --body "QA-side record of promoting \`<slug>\`. Paired PROD PR: $PROD_PR" )

gh pr edit "$PROD_PR" --body "Promotes QA-previewed tutorial \`<slug>\` to PROD. Paired QA PR: $QA_PR. Merging this triggers the PROD content rebuild."
```

### Step 5 — Report

Report **both PR URLs**, whether it was a CREATE or UPDATE, and that content was
verified identical in both. Remind the author: **merging the `Tutorials` (PROD)
PR is what publishes to PROD** — the QA-side PR is an audit record.

## Guardrails

- **Never hardcode a base branch.** Resolve each repo's default (Step 0);
  `Tutorials`=`master`, `-Contribution`=`main` today, but always resolve live.
- **Never open one PR expecting it to span both repos** — always two.
- **UPDATE mode: run the drift guard before overwriting PROD.** An empty diff is
  a no-op (don't open a PR); a diff must be confirmed as only the intended change.
- **Before adding a follow-up commit to an existing PR branch, check PR state**
  (`gh pr view <n> --repo <r> --json state,mergedAt`). If MERGED/CLOSED, branch
  fresh and open a NEW PR — a PUT to a merged PR's branch SUCCEEDS but never
  reaches the default branch. Confirm changes landed by reading the file at the
  default-branch ref.
- **Never `git push`/force-push; never target a non-default base branch.**
- **QA is the source of truth for the copy** — the author previewed it there.
  Do not hand-edit content during promotion; if the content is wrong, fix it in
  the Contribution repo first (see `sap-tutorial-dual-pr` for editing flows),
  then promote.
- This skill promotes ONE tutorial (one slug) per run. For a batch, loop the
  slug and open one PR pair per slug, or ask the author to confirm a multi-slug
  scope explicitly.

## Relationship to `sap-tutorial-dual-pr`

`sap-tutorial-dual-pr` **edits** a tutorial and mirrors the edit to both repos in
lockstep (keeping QA and PROD identical after an edit). This skill **promotes** a
QA-previewed tutorial to PROD (the QA→PROD direction, create-or-update, with a
drift guard for the first-promotion 404 case). Use dual-pr to change content;
use this to ship a QA-approved tutorial to PROD.
