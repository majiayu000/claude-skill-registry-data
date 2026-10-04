---
name: sprint-fanout
description: Draft per-repo sprint plans in parallel through the resolved review engine for a given PRD or goal. Each plan lands at the target repo's docs/sprints/sprint-XX/sprint-plan.md path. Use when the CEO wants to start a multi-repo sprint based on a PRD or shared goal, wants to see how the dev teams would scope a piece of work, or says things like "draft plans for X across these repos" or "let's scope work for this PRD". Auto-fire when the CEO references a PRD/goal path and asks for sprint planning. CEO can still type the slash for explicit gating.
allowed-tools: Bash(*) Read Write
argument-hint: <prd-or-goal-path> [--repos repo1,repo2] [--sprint NN] [--dry-run]
---

# Sprint Fanout: $ARGUMENTS

Drafts a sprint-plan.md per active repo by feeding the PRD/goal + per-repo CLAUDE.md to the **configured engine** in parallel. Engine resolved by `scripts/agentic/resolve-review-engine.sh` (`REVIEW_ENGINE` env → `.review-engine` file → default `subagent`). For CLI engines (`gemini`/`kimi`/`claude-p`) the body drafts inline; for `subagent`/`handoff` the body stages per-repo prompts and the CTO drafts them via the Agent tool.

## Setup + dispatch

```!
set -uo pipefail
# CTO-HOME ANCHORING. These skills read the fleet registry, which lives in the CTO home
# — but `git rev-parse` returns whatever repo the SHELL happens to sit in. A lingering cd
# into a project repo made /handoff report "no target repos found" and made vp-review
# resolve personas against the wrong tree. $CLAUDE_PROJECT_DIR is the session's project
# root regardless of cwd drift, so it is the correct anchor; git root is the fallback.
CTO_HOME_REQUIRED=1
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
if [ ! -f "$CTO_REGISTRY" ]; then
  echo "ERROR: fleet registry not found at $CTO_REGISTRY"
  echo "  This skill must run from the CTO home (the repo holding .cto/projects.yaml)."
  echo "  If you are in a project repo, the session project dir is wrong — reopen in the CTO home."
  exit 1
fi

# zsh doesn't word-split unquoted parameter expansion by default. Skills run
# in whatever shell the harness uses (zsh on macOS). This makes `for tok in $ARGS`
# behave consistently in both bash and zsh.
[ -n "${ZSH_VERSION:-}" ] && setopt sh_word_split

# Parse arguments
ARGS="$ARGUMENTS"
PRD_PATH=""
REPOS_FILTER=""
SPRINT=""
DRY_RUN=0

for tok in $ARGS; do
  case "$tok" in
    --repos=*)   REPOS_FILTER="${tok#--repos=}" ;;
    --sprint=*)  SPRINT="${tok#--sprint=}" ;;
    --dry-run)   DRY_RUN=1 ;;
    --*)         echo "Unknown flag: $tok" >&2 ;;
    *)           [ -z "$PRD_PATH" ] && PRD_PATH="$tok" ;;
  esac
done

if [ -z "$PRD_PATH" ] || [ ! -f "$PRD_PATH" ]; then
  echo "ERROR: provide a path to a PRD or goal file as the first argument"
  echo "Usage: /sprint-fanout <path> [--repos r1,r2] [--sprint NN] [--dry-run]"
  exit 1
fi

# Resolve sprint number — default to next available across repos, but for v1
# require explicit --sprint if not provided
if [ -z "$SPRINT" ]; then
  SPRINT="XX-TBD"
fi

# Output dir for staging + summary
OUT=/tmp/cto/sprint-fanout-$(date +%Y%m%d-%H%M%S)
mkdir -p "$OUT"
echo "Staging dir: $OUT"
echo "PRD/goal: $PRD_PATH"
echo "Sprint: $SPRINT"
echo "Dry-run: $DRY_RUN"
echo ""

# Read active repos
python3 - <<PYEOF > "$OUT/repos.tsv"
import re
with open('$CTO_REGISTRY') as f:
    text = f.read()
blocks = re.split(r'(?=- name:)', text)
filter_set = set("$REPOS_FILTER".split(',')) if "$REPOS_FILTER" else None
for b in blocks:
    m = re.search(r'- name:\s*(\S+)', b)
    p = re.search(r'path:\s*(\S+)', b)
    a = re.search(r'active:\s*(\S+)', b)
    if not m or not p:
        continue
    name = m.group(1)
    path = p.group(1)
    is_active = (a is None) or a.group(1).lower() not in ('false','no','0')
    if not is_active:
        continue
    if filter_set and name not in filter_set:
        continue
    print(f"{name}\t{path}")
PYEOF

NUM_REPOS=$(wc -l < "$OUT/repos.tsv" | tr -d ' ')
echo "Active target repos: $NUM_REPOS"
cat "$OUT/repos.tsv" | sed 's/^/  /'
echo ""

if [ "$NUM_REPOS" -eq 0 ]; then
  echo "ERROR: no active repos matched"
  exit 1
fi

# Resolve the engine (shared resolver) — configurable per CEO 2026-06-19, not hardcoded gemini.
RESOLVER="$ROOT/scripts/agentic/resolve-review-engine.sh"
ENGINE=$( [ -x "$RESOLVER" ] && "$RESOLVER" || echo subagent ) || true
case "$ENGINE" in claude) ENGINE=claude-p;; dual) ENGINE=gemini;; none|"") ENGINE=subagent;; esac
[ "$ENGINE" = "claude-p-blocked" ] && { echo "ENGINE=claude-p refused (metered; set REVIEW_ALLOW_METERED=1)"; exit 3; }
[ "$ENGINE" = "claude-p" ] && [ "${REVIEW_ALLOW_METERED:-0}" != "1" ] && { echo "ERROR: claude-p is metered; set REVIEW_ALLOW_METERED=1."; exit 1; }
echo "ENGINE=$ENGINE"
echo ""
echo "Staging per-repo prompts$( [ "$ENGINE" = gemini ] || [ "$ENGINE" = claude-p ] && echo ' + firing in parallel' )..."
date
PRD_CONTENT=$(cat "$PRD_PATH")

while IFS=$'\t' read -r REPO_NAME REPO_PATH; do
  REPO_CLAUDE_MD=""
  [ -f "$REPO_PATH/CLAUDE.md" ] && REPO_CLAUDE_MD=$(head -200 "$REPO_PATH/CLAUDE.md")

  PROMPT_FILE="$OUT/${REPO_NAME}-prompt.md"
  cat > "$PROMPT_FILE" <<EOF
You are the Dev Team for the repo: $REPO_NAME at $REPO_PATH.

TASK: Draft a sprint plan for sprint $SPRINT scoped to your repo's portion of the following PRD/goal.

PRD / GOAL:
---
$PRD_CONTENT
---

YOUR REPO'S CLAUDE.md (first 200 lines for context):
---
$REPO_CLAUDE_MD
---

OUTPUT REQUIREMENTS:
- Produce a sprint plan in markdown
- Title: "# Sprint $SPRINT — <one-line summary>"
- Sections: Scope, Tasks (numbered list with file paths + effort estimates), Test Plan, Acceptance Criteria, Dependencies, Risks
- Keep tasks specific to THIS repo only. Do not propose work in other repos.
- If the PRD doesn't apply to this repo, output: "NO_SCOPE_FOR_THIS_REPO" and explain in one line why.
- Do NOT write code in the plan. Plan only.
EOF

  OUT_PLAN="$OUT/${REPO_NAME}-plan.md"
  if [ "$ENGINE" = "gemini" ] || [ "$ENGINE" = "kimi" ] || [ "$ENGINE" = "codex" ] || [ "$ENGINE" = "claude-p" ]; then
    # Stdin-only invocation — every CLI engine reads the prompt on stdin.
    if [ "$ENGINE" = "gemini" ]; then RUNCMD="cat '$PROMPT_FILE' | gemini"
    elif [ "$ENGINE" = "kimi" ]; then RUNCMD="cat '$PROMPT_FILE' | '$ROOT/scripts/agentic/openrouter-chat.sh'"
    elif [ "$ENGINE" = "codex" ]; then RUNCMD="cat '$PROMPT_FILE' | '$ROOT/scripts/agentic/codex-exec.sh'"  # UNTESTED (2026-07-02)
    else RUNCMD="cat '$PROMPT_FILE' | claude -p --max-turns 1"; fi
    # TIMEOUT MUST STAY UNDER THE HARNESS SHELL CAP. A skill body's shell is reaped at
    # roughly two minutes; an engine call with a longer internal timeout dies WITH its
    # parent, leaving a 0-byte plan in the staging dir and no status file. Keep this
    # below the cap so every call resolves to a real SUCCESS or ERROR while the body
    # still lives. (Queued redesign: detach via nohup + status file and poll from "Your
    # task", the way the subagent path already avoids the cap entirely.)
    FANOUT_TIMEOUT="${FANOUT_TIMEOUT:-90}"
    TIMEOUT_BIN=""
    command -v gtimeout >/dev/null 2>&1 && TIMEOUT_BIN="gtimeout"
    [ -z "$TIMEOUT_BIN" ] && command -v timeout >/dev/null 2>&1 && TIMEOUT_BIN="timeout"
    echo "  -> firing $ENGINE for $REPO_NAME (timeout ${FANOUT_TIMEOUT}s)..."
    ( if [ -n "$TIMEOUT_BIN" ]; then "$TIMEOUT_BIN" "$FANOUT_TIMEOUT" sh -c "$RUNCMD" > "$OUT_PLAN" 2> "$OUT/${REPO_NAME}.log"
      else sh -c "$RUNCMD" > "$OUT_PLAN" 2> "$OUT/${REPO_NAME}.log"; fi
      RC=$?
      # A zero exit with no output is NOT success. An engine that dies, refuses, or is
      # reaped can exit 0 having written nothing; marking that SUCCESS is what lets an
      # empty file land in a sprint dir and be read as a drafted plan.
      SZ=$(wc -c < "$OUT_PLAN" 2>/dev/null || echo 0)
      if [ "$RC" -ne 0 ]; then echo "ERROR($RC)" > "$OUT/${REPO_NAME}.status"
      elif [ "${SZ:-0}" -lt 200 ]; then echo "FAILED-EMPTY(${SZ}b)" > "$OUT/${REPO_NAME}.status"
      else echo "SUCCESS" > "$OUT/${REPO_NAME}.status"; fi ) &
  else
    # subagent / handoff: a skill body can't draft via an Agent/window — the CTO does (Your task).
    echo "  -> staged prompt for $REPO_NAME (engine=$ENGINE: CTO drafts via the Agent tool)"
    echo "PENDING" > "$OUT/${REPO_NAME}.status"
  fi
done < "$OUT/repos.tsv"

wait
if [ "$ENGINE" = "gemini" ] || [ "$ENGINE" = "kimi" ] || [ "$ENGINE" = "codex" ] || [ "$ENGINE" = "claude-p" ]; then
  echo "All $ENGINE calls done at $(date)"
else
# Subagent model (model policy 2026-09-25): every Agent call passes `model:` explicitly. An
  # Agent call that omits it inherits the PARENT's model — a CTO on the stretch model then runs
  # every review/draft on it too. The alias comes from the lane pin (.cto/devteam-model;
  # `default` maps to the policy's lane family, .cto/model-budget.yaml).
  AGENT_MODEL="$(bash "$ROOT/scripts/cto/resolve-devteam-model.sh" --alias 2>/dev/null)"; AGENT_MODEL="${AGENT_MODEL:-opus}"
  echo "AGENT_MODEL=$AGENT_MODEL   # pass model: \"$AGENT_MODEL\" on EVERY Agent call below"
  echo "DISPATCH=$ENGINE — prompts staged; the CTO drafts each plan via the Agent tool (see Your task)."
fi
echo ""

# Report per-repo result
echo "=== RESULTS ==="
printf "%-32s %-12s %s\n" "REPO" "STATUS" "PLAN PATH"
echo "------------------------------------------------------------------------"
while IFS=$'\t' read -r REPO_NAME REPO_PATH; do
  STATUS=$(cat "$OUT/${REPO_NAME}.status" 2>/dev/null || echo "UNKNOWN")
  PLAN="$OUT/${REPO_NAME}-plan.md"
  SIZE=$(wc -c < "$PLAN" 2>/dev/null || echo "0")
  # The NO_SCOPE_FOR_THIS_REPO sentinel only marks whole-plan-skip if it appears
  # in the FIRST 5 lines (i.e. the gemini response opens with it). Plans that
  # mention it inline as a per-PRD callout ("PRD-011 NO_SCOPE_FOR_THIS_REPO —
  # belongs to other repo") are valid plans, not skips.
  if head -5 "$PLAN" 2>/dev/null | grep -q "NO_SCOPE_FOR_THIS_REPO"; then NO_SCOPE=1; else NO_SCOPE=0; fi
  if [ "$NO_SCOPE" -gt 0 ]; then
    STATUS="SKIPPED"
    NOTE="(no scope for this repo)"
  else
    NOTE="$SIZE bytes"
  fi
  printf "%-32s %-12s %s %s\n" "$REPO_NAME" "$STATUS" "$PLAN" "$NOTE"
done < "$OUT/repos.tsv"

if [ "$DRY_RUN" -eq 1 ]; then
  echo ""
  echo "DRY-RUN: plans staged at $OUT but NOT written to per-repo sprint dirs."
  echo "Review the plans, then re-run without --dry-run to land them."
else
  echo ""
  echo "Writing plans to per-repo sprint dirs..."
  while IFS=$'\t' read -r REPO_NAME REPO_PATH; do
    STATUS=$(cat "$OUT/${REPO_NAME}.status" 2>/dev/null || echo "UNKNOWN")
    [ "$STATUS" != "SUCCESS" ] && continue
    PLAN="$OUT/${REPO_NAME}-plan.md"
    # The NO_SCOPE_FOR_THIS_REPO sentinel only marks whole-plan-skip if it appears
  # in the FIRST 5 lines (i.e. the gemini response opens with it). Plans that
  # mention it inline as a per-PRD callout ("PRD-011 NO_SCOPE_FOR_THIS_REPO —
  # belongs to other repo") are valid plans, not skips.
  if head -5 "$PLAN" 2>/dev/null | grep -q "NO_SCOPE_FOR_THIS_REPO"; then NO_SCOPE=1; else NO_SCOPE=0; fi
    [ "$NO_SCOPE" -gt 0 ] && continue
    DEST_DIR="$REPO_PATH/docs/sprints/sprint-$SPRINT"
    mkdir -p "$DEST_DIR"
    cp "$PLAN" "$DEST_DIR/sprint-plan.md"
    echo "  wrote $DEST_DIR/sprint-plan.md"
  done < "$OUT/repos.tsv"
fi
```

## Your task as CTO

**First check the `ENGINE=` / `DISPATCH=` lines in the script output.**

**If `DISPATCH=subagent` (default) or `handoff`:** the plans were NOT drafted yet — you draft them now. For each `repo=… prompt=… plan=… dest=…` repo, launch one `Task`/Agent call in parallel (single message), **passing `model: "<AGENT_MODEL>"` from the output above on every call** (omitting it inherits your model), instructing it to read the staged prompt file (`$OUT/<repo>-prompt.md`), draft the sprint plan exactly per the prompt's OUTPUT REQUIREMENTS (markdown only, this-repo-only, `NO_SCOPE_FOR_THIS_REPO` if it doesn't apply), and **write it to both `$OUT/<repo>-plan.md` and the dest `…/docs/sprints/sprint-<NN>/sprint-plan.md`** (unless `--dry-run`, then staging only). When all return, proceed to synthesize. (Engine is bright-line clean: in-session Agent = subscription pool.)

**If the CLI engine ran (gemini/kimi/codex/claude-p):** (note: `codex` is ⚠️ untested — sanity-check its output before trusting it the way you would gemini/kimi) plans are already drafted + landed above.

Then, regardless of engine, synthesize:

1. **Headline:** "Drafted N plans, M skipped (no scope), K failed"
2. **For each non-skipped plan:** read it briefly via Read tool, note the top 2-3 tasks and the effort estimate
3. **Cross-repo synthesis:** flag any tasks across repos that seem to duplicate work or that imply an interface contract that wasn't in the PRD
4. **Recommend next step to CEO:**
   - If plans look good: `/vp-review docs/sprints/sprint-NN/sprint-plan.md` per repo, then `/sprint-accept`
   - If plans need revision: identify which repos and what to fix, suggest re-running with refined prompt

Present a tight summary to the CEO. Brief. Sign as: — CTO
