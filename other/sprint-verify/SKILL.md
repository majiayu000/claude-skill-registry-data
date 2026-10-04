---
name: sprint-verify
description: Objectively verify that each PRD/sprint-plan acceptance criterion was actually delivered as stated — the independent step BETWEEN the QA drive and /sprint-accept. Aggregates test-results + qa-report + demo-output and runs targeted gap-fill checks, marking every criterion MET / NOT-MET / UNVERIFIED with an evidence pointer. Writes conformance.md. Makes NO ship/no-ship decision (that is /sprint-accept). Run AFTER the dev-report + test re-run + QA drive land, BEFORE accepting. Auto-fire when the CEO asks to verify a sprint's deliverables, "did we build what the plan said", or before a sprint accept.
allowed-tools: Bash(*) Read Write
argument-hint: <sprint-dir>
---

# Sprint Verify: $ARGUMENTS

Maps each acceptance criterion to evidence and marks it MET / NOT-MET / UNVERIFIED. **Objective —
produces `conformance.md` (facts), never a ship decision.** Verify is the synthesizer; tests + the
QA drive + the demo are the evidence producers, so it runs AFTER them.

## Inventory evidence + seed the report

```!
set -uo pipefail
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
SPRINT_DIR="$ARGUMENTS"
SPRINT_DIR="${SPRINT_DIR%% *}"   # first token (ignore trailing flags)
[ -d "$SPRINT_DIR" ] || { echo "ERROR: sprint dir not found: $SPRINT_DIR"; echo "Usage: /sprint-verify <sprint-dir>"; exit 1; }

# Criteria source: prefer scope.md (VP-Product's acceptance criteria), else sprint-plan.md.
CRIT_SRC=""
for f in scope.md sprint-plan.md; do [ -f "$SPRINT_DIR/$f" ] && { CRIT_SRC="$SPRINT_DIR/$f"; break; }; done
[ -n "$CRIT_SRC" ] || { echo "ERROR: no scope.md or sprint-plan.md in $SPRINT_DIR — nothing to verify against."; exit 1; }
echo "criteria source : $CRIT_SRC"

# Evidence inventory — verify AGGREGATES these; it must run after they exist.
echo "evidence present:"
EV=0
for f in test-results.md qa-report.md demo-output.md flow-graph.json dev-report.md; do
  if [ -f "$SPRINT_DIR/$f" ]; then printf '  [present] %s\n' "$f"; EV=$((EV+1)); else printf '  [absent ] %s\n' "$f"; fi
done

# Ordering guard: verify runs AFTER tests + QA. Warn (don't block) if they're missing or stale,
# so the verifier knows un-covered criteria will land UNVERIFIED rather than MET.
[ -f "$SPRINT_DIR/test-results.md" ] || echo "  WARN: no test-results.md — re-run the suite BEFORE verify (it's the ground-truth of the dev-report's 'tests pass' claim); test-backed criteria will be UNVERIFIED."
if [ -f "$SPRINT_DIR/dev-report.md" ] && [ -f "$SPRINT_DIR/test-results.md" ] && [ "$SPRINT_DIR/dev-report.md" -nt "$SPRINT_DIR/test-results.md" ]; then
  echo "  WARN: test-results.md is OLDER than dev-report.md — may be stale; re-run tests before trusting test-backed rows."
fi
# QA drive only matters if a user-facing surface is in scope.
if grep -qiE 'browser|cli|mcp|ui|surface|qa-plan' "$CRIT_SRC" 2>/dev/null && [ ! -f "$SPRINT_DIR/qa-report.md" ]; then
  echo "  WARN: plan references a user-facing surface but no qa-report.md — run /qa-ux <dir> --mode drive BEFORE verify; UX criteria will be UNVERIFIED."
fi

# Seed conformance.md from the template (don't overwrite an existing one — verify may be re-run).
CONF="$SPRINT_DIR/conformance.md"
if [ ! -f "$CONF" ] && [ -f "$ROOT/docs/sprints/_templates/conformance.md" ]; then
  sed "s/<slug>/$(basename "$SPRINT_DIR")/; s/<short-sha>/$(git -C "$ROOT" rev-parse --short HEAD 2>/dev/null || echo unknown)/" \
    "$ROOT/docs/sprints/_templates/conformance.md" > "$CONF"
  echo "seeded $CONF from template — fill it in per Your task."
else
  echo "conformance.md $( [ -f "$CONF" ] && echo 'exists — UPDATE it (re-verify), do not blank prior rows' || echo 'template missing — author from the structure in Your task' )"
fi

# Standing rows — governed derived artifacts (ADR-002). The sprint's repo declares them in
# .claude/derived-artifacts.yaml; the gate is the empirical signal. Checked against the
# WORKTREE: the dev lane does not commit, so its regeneration (or its absence) is on disk.
SREPO="$(git -C "$SPRINT_DIR" rev-parse --show-toplevel 2>/dev/null || true)"
DAG="$ROOT/scripts/agentic/derived-artifact-gate.sh"; [ -n "$SREPO" ] && [ -f "$SREPO/scripts/agentic/derived-artifact-gate.sh" ] && DAG="$SREPO/scripts/agentic/derived-artifact-gate.sh"
if [ -n "$SREPO" ] && [ -f "$SREPO/.claude/derived-artifacts.yaml" ] && [ -f "$DAG" ]; then
  echo ""
  echo "=== STANDING ROWS — governed derived artifacts (ADR-002; signal = derived-artifact-gate.sh --worktree exit 0) ==="
  DOUT="$(bash "$DAG" --worktree --audit --repo "$SREPO" 2>&1)"; DRC=$?
  printf '%s\n' "$DOUT" | grep -E '^  \S+ +(block|warn) +\S+' | grep -v '^  ARTIFACT\|^  ----'
  DAG_ROWS="$(printf '%s\n' "$DOUT" | grep -E '^  \S+ +(block|warn) +\S+' | grep -v '^  ARTIFACT\|^  ----' | python3 -c '
import sys,re
for i,l in enumerate(sys.stdin,1):
    m=re.match(r"\s+(\S+)\s+(block|warn)\s+(\S+)\s*(.*)",l.rstrip())
    if not m: continue
    name,mode,state,detail=m.groups(); status="MET" if state=="OK" else "NOT-MET"
    suffix=(" — "+detail[:110]) if detail else ""
    print(f"| D{i} | derived artifact `{name}` current with the code (ADR-002; mode {mode}) | `derived-artifact-gate.sh --worktree` exit 0 | {status} | `ran: derived-artifact-gate.sh --worktree --audit` → {state}{suffix} |")
')"
  if [ -n "$DAG_ROWS" ] && [ -f "$CONF" ] && ! grep -q 'Standing rows — derived artifacts' "$CONF"; then
    { echo ""; echo "## Standing rows — derived artifacts (ADR-002)"; echo ""
      echo "| # | Acceptance criterion (standing, from the repo manifest) | Declared empirical signal | Status | Evidence pointer |"
      echo "|---|---|---|---|---|"; printf '%s\n' "$DAG_ROWS"; } >> "$CONF"
    echo "  appended $(printf '%s\n' "$DAG_ROWS" | grep -c .) standing row(s) to $CONF — carry them into the Summary counts."
  fi
  [ "$DRC" -eq 3 ] && echo "  NOTE: a NOT-MET standing row is a fact for /sprint-accept to name (accept as known-issue or block) — never silently dropped."
fi

echo ""
echo "=== ACCEPTANCE CRITERIA (verify each of these) — from $CRIT_SRC ==="
grep -nE 'Acceptance:|Empirical signal:|Success Criteria|Requirement|Acceptance Criteria|HARD' "$CRIT_SRC" 2>/dev/null | head -60
echo ""
echo "NOTE: this is a grep hint only — read $CRIT_SRC IN FULL plus the PRD it cites; criteria may be prose."
```

## Your task as CTO (verifier — objective, no ship decision)

You are doing **objective conformance verification**, not accepting the sprint. Produce facts.

1. **Extract every acceptance criterion** from the criteria source (read it in full + the cited PRD). Include `scope.md` "Acceptance" / "Success Criteria", `sprint-plan.md` acceptance criteria, and `qa-plan.md` HARD signals if present. Each criterion ideally declares an **empirical signal** (a command+expected output, an exact string/`data-testid`/log line, or a named demo observation).

2. **For each criterion, gather evidence — aggregate first, then gap-fill:**
   - Look for the result in the existing artifacts: `test-results.md`, `qa-report.md`, `demo-output.md`, the flow-graph. Cite the specific line/section.
   - If nothing covers it, **run the criterion's empirical signal yourself** (the command / the check) and record the actual result. Use the real CLI/Bash; for browser-only signals that need DOMShell, note that they belong to the QA drive — if the QA drive didn't cover it, mark UNVERIFIED (do not re-drive the browser here).
   - **Do NOT trust the dev-report's prose as evidence.** "The dev-report says it works" is not a MET — find the empirical artifact or run the check. (This is the recurring claims-vs-reality failure this step exists to catch.)

3. **Mark each criterion:**
   - **MET** — concrete evidence shows it delivered as stated (cite it).
   - **NOT-MET** — evidence shows it was not delivered / behaves wrong (cite it).
   - **UNVERIFIED** — no evidence and no runnable signal (e.g. criterion had no empirical signal, or needs a surface no one drove). UNVERIFIED is never assumed MET.

3b. **Standing rows.** If the run printed STANDING ROWS (the repo governs derived artifacts per ADR-002), they were appended to `conformance.md` with MET/NOT-MET already set from the gate. Keep them; count them in the Summary. A NOT-MET standing row is a fact the accept decision must name.

4. **Write `conformance.md`** (template seeded above): the criteria table (criterion → declared signal → status → evidence pointer), the MET/NOT-MET/UNVERIFIED summary, and the plan-quality notes (criteria that arrived with no empirical signal, or whose signal was merely "tests pass" — feedback for VP Product). Sign `— CTO`.

5. **Present a 5-line summary to the CEO:** MET N/total, the NOT-MET list, the UNVERIFIED list, and the one-line recommendation for `/sprint-accept` (e.g. "3 NOT-MET — accept only if you're shipping those as known issues"). **State explicitly that this is verification, not acceptance** — the ship decision is `/sprint-accept`, which may accept with these as documented known-issues.

Sign as: — CTO
