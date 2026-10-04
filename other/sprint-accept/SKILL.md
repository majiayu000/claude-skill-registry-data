---
name: sprint-accept
description: Close out a sprint by reading sprint-plan.md, dev-report.md, all VP review files, and Phase 3 evals from a sprint directory. CTO synthesizes a final accept/reject decision and writes it to the sprint dir. Use when CEO is ready to formally accept or reject completed sprint work.
allowed-tools: Bash(*) Read Write
argument-hint: <sprint-dir-path>
---

# Sprint Accept: $ARGUMENTS

Reads the entire sprint dir, summarizes artifacts, and produces a CTO decision file.

## Inventory the sprint dir

```!
SPRINT_DIR="$ARGUMENTS"
# zsh aborts the whole script on an unmatched glob (e.g. cto-decision-*.md in a
# sprint dir that has none yet). no_nomatch makes an unmatched glob pass through
# literally, as bash does — the [ -f ] guards below then handle the no-match case.
[ -n "${ZSH_VERSION:-}" ] && setopt no_nomatch sh_word_split
# >>> CTO-HOME ANCHOR (canonical — sync with: bash scripts/cto/lint-skills.sh --apply) >>>
# Fleet state lives in the CTO home, and neither obvious anchor is reliable alone:
# `git rev-parse` returns whatever repo the SHELL sits in, so one lingering cd into a dev
# repo silently retargets the skill; and $CLAUDE_PROJECT_DIR was observed EMPTY in skill
# shells (2026-08-13) — /handoff then resolved the registry against a dev repo and refused
# with an error that blamed the registry rather than the anchoring. So: try every anchor,
# VALIDATE each candidate before accepting it, and when none holds either fail naming the
# real cause or fall back explicitly and say so.
# Skills that read the fleet registry set CTO_HOME_REQUIRED=1 before this block.
#
# NO POSITIONAL PARAMETERS IN THIS BLOCK — no dollar-1, no dollar-2, not even awk's dollar-1.
# (Spelled out rather than written literally, because the rewrite described next hits comments
#  too: a literal example here would itself be replaced with argument text.)
#
# This block is embedded in SKILL.md, and the skill runtime rewrites every dollar-followed-by-
# digits token in the FILE with the invocation's arguments before the shell ever sees it. The
# rewrite is document-wide: no awareness of code fences, no escape (a backslash before it does
# not protect it — it renders empty), and it applies inside comments and string literals alike.
# A shell function's own positional parameter is therefore replaced by argument text, and when
# the skill is invoked with no arguments it is replaced by nothing at all.
#
# The first version of this block used positional parameters and was consequently broken from
# the day it shipped: _cto_is_home tested a garbage path on every candidate, so the anchor
# NEVER matched, and every skill carrying it silently fell back to the cwd repo — precisely the
# confident wrong answer it was written to prevent. Found 2026-09-01, six weeks after it
# shipped, because the fallback usually landed on the right repo by luck.
#
# Candidates are passed in named variables instead. Brace-wrapped positionals happen to survive
# the rewrite; do not use them either — the next person to write the bare form reintroduces the
# bug, and it fails silently. Guarded by lint CHECK E.
_CTO_REJECTED=""
_CTO_CAND=""
_cto_is_home() {          # in: _CTO_CAND · appends to _CTO_REJECTED
  [ -n "$_CTO_CAND" ] && [ -f "$_CTO_CAND/.cto/projects.yaml" ] || return 1
  # The PUBLIC template ships a placeholder registry (/Users/yourname/repos/my-project).
  # Accepting it resolves cleanly and then reports a fleet of repos that do not exist —
  # a confident wrong answer, which is worse than the error it replaced. Observed live:
  # four dev repos still point .cto-path at the template, so this is the real path.
  if grep -q '/Users/yourname/' "$_CTO_CAND/.cto/projects.yaml" 2>/dev/null; then
    _CTO_REJECTED="$_CTO_REJECTED  $_CTO_CAND (placeholder registry — the unconfigured template)"
    return 1
  fi
  return 0
}
# Sets _CTO_FOUND rather than printing: a $(…) capture runs in a SUBSHELL, so the rejected-
# candidate diagnostics collected by _cto_is_home would be discarded exactly when they are
# needed — on the failure path.
_CTO_FOUND=""
_cto_walk() {             # in: _CTO_START · out: _CTO_FOUND
  _d="$_CTO_START"
  while [ -n "$_d" ] && [ "$_d" != "/" ]; do
    _CTO_CAND="$_d"; _cto_is_home && { _CTO_FOUND="$_d"; return 0; }
    if [ -f "$_d/.cto-path" ]; then
      _p="$(tr -d '[:space:]' < "$_d/.cto-path")"
      _CTO_CAND="$_p"; _cto_is_home && { _CTO_FOUND="$_p"; return 0; }
    fi
    # `--` because a mis-rendered candidate can begin with a dash, and `dirname --repos=x`
    # exits with "illegal option" instead of walking. That message was the only outward sign
    # of the rewrite bug above for two weeks, and it was read as cosmetic noise.
    _d="$(dirname -- "$_d")"
  done
  return 1
}
ROOT=""
for _c in "${CTO_HOME:-}" "${CTO_REPO:-}" "${CLAUDE_PROJECT_DIR:-}"; do
  [ -n "$_c" ] || continue
  _CTO_CAND="$_c"; _cto_is_home && { ROOT="$_c"; break; }
done
if [ -z "$ROOT" ]; then _CTO_START="$PWD"; if _cto_walk; then ROOT="$_CTO_FOUND"; fi; fi
if [ -z "$ROOT" ] && [ -f "$HOME/.cto/home" ]; then
  _p="$(tr -d '[:space:]' < "$HOME/.cto/home")"
  _CTO_CAND="$_p"; _cto_is_home && ROOT="$_p"
fi
if [ -z "$ROOT" ]; then
  if [ "${CTO_HOME_REQUIRED:-0}" = "1" ]; then
    echo "ERROR: no CTO home found — no directory containing .cto/projects.yaml." >&2
    echo "  \$CTO_HOME='${CTO_HOME:-}'  \$CTO_REPO='${CTO_REPO:-}'  \$CLAUDE_PROJECT_DIR='${CLAUDE_PROJECT_DIR:-}'" >&2
    echo "  walked up from: $PWD" >&2
    # Report the permanent anchor's CONTENT, not just that the remedy exists. When the anchor
    # is set correctly and the skill still fails, the error must not keep recommending it —
    # that loop cost a full diagnosis cycle on 2026-09-01.
    if [ -f "$HOME/.cto/home" ]; then
      echo "  ~/.cto/home is SET and was tested: '$(tr -d '[:space:]' < "$HOME/.cto/home")'" >&2
      echo "  It did not validate, so the remedy below is already applied and is NOT the fix." >&2
      echo "  Check that path holds .cto/projects.yaml, then suspect the skill rendering itself." >&2
    else
      echo "  This is an ANCHORING failure, not a missing registry. Run the skill from the CTO" >&2
      echo "  home, or fix it permanently:  echo /path/to/<project>-cto > ~/.cto/home" >&2
    fi
    [ -n "$_CTO_REJECTED" ] && { echo "  rejected candidates:" >&2; printf '%s\n' "$_CTO_REJECTED" >&2; }
    exit 1
  fi
  ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
  echo "NOTE: no CTO home found; using the current repo ($ROOT)." >&2
fi
CTO_REGISTRY="$ROOT/.cto/projects.yaml"
cd "$ROOT" || { echo "ERROR: cannot enter $ROOT" >&2; exit 1; }
# <<< CTO-HOME ANCHOR <<<
if [ -z "$SPRINT_DIR" ] || [ ! -d "$SPRINT_DIR" ]; then
  echo "ERROR: provide a path to a sprint directory"
  echo "Usage: /sprint-accept <path-to-sprint-XX/>"
  exit 1
fi

echo "Sprint directory: $SPRINT_DIR"
echo ""
echo "=== Files present ==="
ls -la "$SPRINT_DIR" | tail -n +2

echo ""
echo "=== Artifact summary ==="
for f in scope.md sprint-plan.md dev-report.md test-results.md demo-output.md conformance.md \
         qa-report.md product-review.md vp-eng-review.md security-review.md infra-review.md \
         vp-datascience-review.md test-eval.md cto-decision-*.md approval.md rejection.md; do
  for match in "$SPRINT_DIR"/$f; do
    if [ -f "$match" ]; then
      size=$(wc -c < "$match")
      lines=$(wc -l < "$match")
      printf "  [present] %-40s %6d bytes / %d lines\n" "$(basename $match)" "$size" "$lines"
    fi
  done
done

echo ""
echo "=== Missing canonical artifacts ==="
MISSING=0
for f in sprint-plan.md dev-report.md; do
  if [ ! -f "$SPRINT_DIR/$f" ]; then
    echo "  [missing] $f — required for accept"
    MISSING=$((MISSING + 1))
  fi
done

# CONFORMANCE GATE (process, not outcome): you cannot accept BLIND. conformance.md must
# EXIST (verification must have happened) — but it need NOT PASS. Accept stays a decision:
# shipping with NOT-MET/UNVERIFIED criteria as documented known-issues is a CTO/CEO call.
# This mirrors the QA-UX gate (report must exist + be reviewed; ship-with-defects is your call).
if [ ! -f "$SPRINT_DIR/conformance.md" ]; then
  echo "  [missing] conformance.md — REQUIRED for accept (objective verification precedes the decision)"
  echo "            Run:  /sprint-verify $SPRINT_DIR   (after tests + the QA drive), then re-run /sprint-accept."
  echo "            (Refusing only because verification is ABSENT — not because it failed. Accept never requires conformance to PASS.)"
  MISSING=$((MISSING + 1))
fi

if [ "$MISSING" -gt 0 ]; then
  echo ""
  echo "CANNOT ACCEPT: missing $MISSING canonical artifact(s). Sprint is not ready to decide on yet."
  exit 2
fi
```

## Synthesize the decision

```!
# >>> CTO-HOME ANCHOR (canonical — sync with: bash scripts/cto/lint-skills.sh --apply) >>>
# Fleet state lives in the CTO home, and neither obvious anchor is reliable alone:
# `git rev-parse` returns whatever repo the SHELL sits in, so one lingering cd into a dev
# repo silently retargets the skill; and $CLAUDE_PROJECT_DIR was observed EMPTY in skill
# shells (2026-08-13) — /handoff then resolved the registry against a dev repo and refused
# with an error that blamed the registry rather than the anchoring. So: try every anchor,
# VALIDATE each candidate before accepting it, and when none holds either fail naming the
# real cause or fall back explicitly and say so.
# Skills that read the fleet registry set CTO_HOME_REQUIRED=1 before this block.
#
# NO POSITIONAL PARAMETERS IN THIS BLOCK — no dollar-1, no dollar-2, not even awk's dollar-1.
# (Spelled out rather than written literally, because the rewrite described next hits comments
#  too: a literal example here would itself be replaced with argument text.)
#
# This block is embedded in SKILL.md, and the skill runtime rewrites every dollar-followed-by-
# digits token in the FILE with the invocation's arguments before the shell ever sees it. The
# rewrite is document-wide: no awareness of code fences, no escape (a backslash before it does
# not protect it — it renders empty), and it applies inside comments and string literals alike.
# A shell function's own positional parameter is therefore replaced by argument text, and when
# the skill is invoked with no arguments it is replaced by nothing at all.
#
# The first version of this block used positional parameters and was consequently broken from
# the day it shipped: _cto_is_home tested a garbage path on every candidate, so the anchor
# NEVER matched, and every skill carrying it silently fell back to the cwd repo — precisely the
# confident wrong answer it was written to prevent. Found 2026-09-01, six weeks after it
# shipped, because the fallback usually landed on the right repo by luck.
#
# Candidates are passed in named variables instead. Brace-wrapped positionals happen to survive
# the rewrite; do not use them either — the next person to write the bare form reintroduces the
# bug, and it fails silently. Guarded by lint CHECK E.
_CTO_REJECTED=""
_CTO_CAND=""
_cto_is_home() {          # in: _CTO_CAND · appends to _CTO_REJECTED
  [ -n "$_CTO_CAND" ] && [ -f "$_CTO_CAND/.cto/projects.yaml" ] || return 1
  # The PUBLIC template ships a placeholder registry (/Users/yourname/repos/my-project).
  # Accepting it resolves cleanly and then reports a fleet of repos that do not exist —
  # a confident wrong answer, which is worse than the error it replaced. Observed live:
  # four dev repos still point .cto-path at the template, so this is the real path.
  if grep -q '/Users/yourname/' "$_CTO_CAND/.cto/projects.yaml" 2>/dev/null; then
    _CTO_REJECTED="$_CTO_REJECTED  $_CTO_CAND (placeholder registry — the unconfigured template)"
    return 1
  fi
  return 0
}
# Sets _CTO_FOUND rather than printing: a $(…) capture runs in a SUBSHELL, so the rejected-
# candidate diagnostics collected by _cto_is_home would be discarded exactly when they are
# needed — on the failure path.
_CTO_FOUND=""
_cto_walk() {             # in: _CTO_START · out: _CTO_FOUND
  _d="$_CTO_START"
  while [ -n "$_d" ] && [ "$_d" != "/" ]; do
    _CTO_CAND="$_d"; _cto_is_home && { _CTO_FOUND="$_d"; return 0; }
    if [ -f "$_d/.cto-path" ]; then
      _p="$(tr -d '[:space:]' < "$_d/.cto-path")"
      _CTO_CAND="$_p"; _cto_is_home && { _CTO_FOUND="$_p"; return 0; }
    fi
    # `--` because a mis-rendered candidate can begin with a dash, and `dirname --repos=x`
    # exits with "illegal option" instead of walking. That message was the only outward sign
    # of the rewrite bug above for two weeks, and it was read as cosmetic noise.
    _d="$(dirname -- "$_d")"
  done
  return 1
}
ROOT=""
for _c in "${CTO_HOME:-}" "${CTO_REPO:-}" "${CLAUDE_PROJECT_DIR:-}"; do
  [ -n "$_c" ] || continue
  _CTO_CAND="$_c"; _cto_is_home && { ROOT="$_c"; break; }
done
if [ -z "$ROOT" ]; then _CTO_START="$PWD"; if _cto_walk; then ROOT="$_CTO_FOUND"; fi; fi
if [ -z "$ROOT" ] && [ -f "$HOME/.cto/home" ]; then
  _p="$(tr -d '[:space:]' < "$HOME/.cto/home")"
  _CTO_CAND="$_p"; _cto_is_home && ROOT="$_p"
fi
if [ -z "$ROOT" ]; then
  if [ "${CTO_HOME_REQUIRED:-0}" = "1" ]; then
    echo "ERROR: no CTO home found — no directory containing .cto/projects.yaml." >&2
    echo "  \$CTO_HOME='${CTO_HOME:-}'  \$CTO_REPO='${CTO_REPO:-}'  \$CLAUDE_PROJECT_DIR='${CLAUDE_PROJECT_DIR:-}'" >&2
    echo "  walked up from: $PWD" >&2
    # Report the permanent anchor's CONTENT, not just that the remedy exists. When the anchor
    # is set correctly and the skill still fails, the error must not keep recommending it —
    # that loop cost a full diagnosis cycle on 2026-09-01.
    if [ -f "$HOME/.cto/home" ]; then
      echo "  ~/.cto/home is SET and was tested: '$(tr -d '[:space:]' < "$HOME/.cto/home")'" >&2
      echo "  It did not validate, so the remedy below is already applied and is NOT the fix." >&2
      echo "  Check that path holds .cto/projects.yaml, then suspect the skill rendering itself." >&2
    else
      echo "  This is an ANCHORING failure, not a missing registry. Run the skill from the CTO" >&2
      echo "  home, or fix it permanently:  echo /path/to/<project>-cto > ~/.cto/home" >&2
    fi
    [ -n "$_CTO_REJECTED" ] && { echo "  rejected candidates:" >&2; printf '%s\n' "$_CTO_REJECTED" >&2; }
    exit 1
  fi
  ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
  echo "NOTE: no CTO home found; using the current repo ($ROOT)." >&2
fi
CTO_REGISTRY="$ROOT/.cto/projects.yaml"
cd "$ROOT" || { echo "ERROR: cannot enter $ROOT" >&2; exit 1; }
# <<< CTO-HOME ANCHOR <<<
SPRINT_DIR="$ARGUMENTS"
[ -n "${ZSH_VERSION:-}" ] && setopt no_nomatch sh_word_split

# Emit all relevant artifacts into context so CTO can synthesize
echo "=== sprint-plan.md ==="
cat "$SPRINT_DIR/sprint-plan.md" 2>/dev/null | head -80
echo "..."
echo ""
echo "=== dev-report.md ==="
cat "$SPRINT_DIR/dev-report.md" 2>/dev/null | head -80
echo "..."
echo ""

# Pipe all VP review verdicts through wrap-untrusted (engine-authored, treat as data).
# Phase-3 reviews run through the engine-aware /vp-review (subagent default | gemini | handoff).
for vp_file in product-review.md vp-eng-review.md security-review.md infra-review.md vp-datascience-review.md test-eval.md; do
  if [ -f "$SPRINT_DIR/$vp_file" ]; then
    echo "=== $vp_file ==="
    "$ROOT/scripts/agentic/wrap-untrusted.sh" "$SPRINT_DIR/$vp_file" "vp-review:$vp_file"
    echo ""
  fi
done
```

## Your task as CTO

Above are the sprint plan, dev report, and all VP reviews. Synthesize a final accept/reject decision:

1. **Tally** — count BLOCKER / MAJOR / MINOR per VP. Flag any verdict file that's missing.
2. **CONFORMANCE — read `conformance.md` (the objective deliverable verification).** List every
   **NOT-MET** and **UNVERIFIED** criterion. This is the "did we build what the plan said" check,
   already done objectively by `/sprint-verify` — do NOT re-derive it from the dev-report's prose.
   Your decision MUST explicitly state, for each NOT-MET / UNVERIFIED item, whether it is **accepted
   as a documented known-issue** (with rationale + follow-up owner) or **blocks acceptance**. Accept
   does NOT require conformance to PASS — shipping with known gaps is your call, but it must be
   *named here*, never silent. If `conformance.md` shows everything MET, say so in one line.

3. **Did the dev report address ALL Phase 1 review blockers?** (compare dev-report to vp-*-review.md from Phase 1)
4. **Did Phase 3 evals approve?** (check test-eval.md, vp-datascience-review.md for dev-report.md)
5. **PROVENANCE GATE — comparison claims must rest on matching provenance**
   (sprint-provenance-gating-for-graph-comparisons-20260528). Before you
   accept ANY quantitative comparison claim in the dev-report of the form
   "X improved/changed/drifted Y by Z" (deltas, %s, before/after, baseline-vs-
   perturbed, sensitivity), check that the underlying artifacts share a
   provenance triple `{code_sha, bundle_version, pipeline_version}`:
   - The harness records this under a `provenance_gate` block in
     `sensitivity_matrix.json` / `baseline_matrix.json`, and per-legend under
     `_provenance`. A `"mode": "strict"` with empty `refused` means the
     comparison is gate-clean.
   - **HARD-BLOCK rule (VP-DS mandate, sprint-provenance-gating-20260528):**
     a claim of *model or pipeline improvement* ("X improved Y by Z", "+N%
     recall", "precision lift", baseline-vs-treatment) is **REJECTED** if any
     contributing artifact (a) used the `--allow-cross-version` escape hatch,
     or (b) lacks a valid bundle **content hash** on the `bundle_version` axis
     (i.e. it ends in `@unhashed`). You cannot validate a lift when the
     baseline and treatment don't share a verifiable triple. Do not accept the
     sprint on the strength of such a claim; record it as REJECTED-FOR-REVISION
     or an explicit action item.
   - **Longitudinal/drift framing is the only legitimate use of the escape
     hatch:** "how did behavior drift across this bundle change?" may cite a
     cross-version comparison *as drift*, never *as an improvement result*, and
     only with the documented `cross_version_reason` present.
   - If any artifact is legacy / unprovenanced and no documented reason is
     present, the comparison is not acceptable as stated — surface it as
     unverified and call it out as an action item.
   - Date timestamps are NOT acceptable as a freshness/equivalence signal
     (that was the failure mode this gate exists to prevent).
6. **Cross-VP convergence on remaining issues** — name them.
7. **Decision** — one of:
   - `APPROVED` — sprint shipped, ready to merge
   - `APPROVED-WITH-CONDITIONS` — minor follow-ups recorded but ship is OK
   - `REJECTED-FOR-REVISION` — material blockers remain, sprint continues
   - `ESCALATE-TO-CEO` — judgment call only CEO can make
8. **Write decision file** to `$SPRINT_DIR/cto-decision-$(date +%Y%m%d-%H%M%S).md` with:
   - Decision verdict
   - Reasoning citing specific VP review excerpts
   - Conformance disposition — the NOT-MET/UNVERIFIED items being accepted as known-issues (with follow-up owners) vs. those that blocked
   - Action items if APPROVED-WITH-CONDITIONS or REJECTED
   - PRD status update guidance for VP Prod
9. **Present 5-line summary to CEO.**

Sign as: — CTO
