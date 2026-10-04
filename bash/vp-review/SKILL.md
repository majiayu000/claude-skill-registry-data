---
name: vp-review
description: Run multi-VP review on a sprint plan, ADR, RCA, PRD, dev-report, or other artifact via parallel VP personas (engine configurable — subagent | kimi | codex (untested) | gemini | handoff | claude-p), then have the CTO synthesize a verdict. Defaults to vp-prod + vp-eng (the always-relevant pair). Add specialty VPs (vp-security, vp-devops, vp-datascience) via the --vps flag when the artifact touches their domain — see docs/personas/cto.md "VP Review Composition" for the policy. Use when the CEO says "review this", "get VP feedback on X", "what would the VPs say about Y", or wants multi-perspective critique on a file path. Auto-fire whenever conversation references reviewing an artifact at a specific path.
allowed-tools: Bash(mkdir *) Bash(rm *) Bash(scripts/agentic/*) Bash(cat *) Bash(ls *) Read Write Task
argument-hint: <path-to-artifact> [--vps=vp-prod,vp-eng,...] [--engine subagent|kimi|codex|gemini|handoff]
---

# VP Review of: $ARGUMENTS

Reviewing artifact at the path above. Each VP reads its persona file, applies it to the artifact, and emits a verdict. The CTO synthesizes a final decision.

**Engine is configurable** (CEO 2026-06-19 — vendors change their minds, so the engine is a *choice*, not a hardcode). Resolved by `scripts/agentic/resolve-review-engine.sh`: `--engine` flag → `REVIEW_ENGINE` env → `<repo>/.review-engine` → default **`subagent`**. Engines: `subagent` (Agent tool, in-session, subscription — DEFAULT), `kimi` (OpenRouter kimi-k2.6 via `openrouter-chat.sh` — a CROSS-FAMILY independent reviewer; non-Anthropic metered, pennies/review; model overridable via `OPENROUTER_MODEL`), `codex` (⚠️ **UNTESTED as of 2026-07-02** — OpenAI Codex CLI's `codex exec` via `codex-exec.sh`; a SECOND independent cross-family reviewer, built from OpenAI's published docs only, no live `codex` install available to verify against — treat the first real invocation as a smoke test, not a working feature), `gemini` (free CLI fan-out, when available), `handoff` (interactive Claude windows), `claude-p` (⚠️ metered Anthropic API, break-glass only). **When independence matters** (Claude-authored work being judged, statistical claims, accept-gates), prefer `kimi` (proven) over `subagent` — a different model family reviewing avoids shared-method bias. `codex` is the same idea but unverified; don't rely on it for anything time-sensitive until it's been run for real at least once.

**Default VP set:** `vp-prod,vp-eng` (the always-relevant pair). Pass `--vps=a,b,c` to override. `--vps=all` runs all 5. Add specialty VPs by content judgment per `docs/personas/cto.md` "VP Review Composition".

## Resolve engine + (for gemini) run reviews

```!
set -uo pipefail
[ -n "${ZSH_VERSION:-}" ] && setopt sh_word_split
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

ARGS="$ARGUMENTS"
ART=""
VPS="vp-prod,vp-eng"  # default — vp-prod + vp-eng always relevant; specialty VPs opt-in via --vps
ENGINE_FLAG=""

for tok in $ARGS; do
  case "$tok" in
    --vps=*)    VPS="${tok#--vps=}" ;;
    --engine=*) ENGINE_FLAG="${tok#--engine=}" ;;
    --*)        echo "Unknown flag: $tok" >&2 ;;
    *)          [ -z "$ART" ] && ART="$tok" ;;
  esac
done

if [ -z "$ART" ] || [ ! -f "$ART" ]; then
  echo "ERROR: artifact not found at $ART"
  echo "Usage: /vp-review <path-to-artifact> [--vps=vp-prod,vp-eng,...] [--engine subagent|kimi|codex|gemini|handoff]"
  exit 1
fi
[ "$VPS" = "all" ] && VPS="vp-prod,vp-eng,vp-security,vp-devops,vp-datascience"

# Resolve the engine (flag wins over env/file/default). The shared resolver is the single
# source of truth + enforces the claude-p metered quarantine.
ENGINE=$( [ -n "$ENGINE_FLAG" ] && REVIEW_ENGINE="$ENGINE_FLAG" "$ROOT/scripts/agentic/resolve-review-engine.sh" || "$ROOT/scripts/agentic/resolve-review-engine.sh" )
RC=$?
[ $RC -ne 0 ] && { echo "ENGINE=$ENGINE"; echo "(engine resolution refused — see message above)"; exit $RC; }

VPR_DIR="/tmp/cto-vp-review/$(basename "$ART" .md)-$(date +%Y%m%d-%H%M%S)-$$"
mkdir -p "$VPR_DIR"
echo "VPR_OUTPUT_DIR=$VPR_DIR"
echo "VP_SET=$VPS"
echo "ENGINE=$ENGINE"
echo "ARTIFACT=$ART"
echo ""

# Per-VP persona file map (used by the subagent/handoff dispatch in Your task below).
# Takes its argument in _VP_NAME, not a positional — see the anchor block's note on the
# runtime rewriting dollar-digit tokens throughout this file.
persona_file() {
  case "$_VP_NAME" in
    vp-prod)        echo "docs/personas/vp-product.md" ;;
    vp-eng)         echo "docs/personas/vp-engineering.md" ;;
    vp-security)    echo "docs/personas/vp-security.md" ;;
    vp-devops)      echo "docs/personas/vp-devops.md" ;;
    vp-datascience) echo "docs/personas/vp-datascience.md" ;;
    vp-compliance)  echo "docs/personas/vp-compliance.md" ;;
    vp-dba)         echo "docs/personas/vp-dba.md" ;;
    *)              echo "" ;;
  esac
}

IFS=',' read -A VP_LIST <<< "$VPS" 2>/dev/null || IFS=',' read -ra VP_LIST <<< "$VPS"

if [ "$ENGINE" = "gemini" ] || [ "$ENGINE" = "kimi" ] || [ "$ENGINE" = "codex" ] || [ "$ENGINE" = "claude-p" ]; then
  # CLI engines: LAUNCH DETACHED, do not wait here.
  #
  # This body used to fire the reviews and `wait`. A skill shell has a ~2-minute budget and a
  # kimi review of a long artifact runs past it: on 2026-08-13 the shell was killed, the
  # children went with it ("Terminated: 15"), and zero-byte verdicts were left on disk that a
  # later reviewer read as "completed review missing content". Minutes-long work cannot have
  # its lifetime tied to a seconds-long caller — so the launch returns immediately and the
  # CTO polls from the main loop, where the budget is minutes.
  DRC=0
  REVIEW_ALLOW_METERED="${REVIEW_ALLOW_METERED:-0}" \
    "$ROOT/scripts/agentic/vp-review-detach.sh" "$ART" "$VPR_DIR" "$VPS" --engine "$ENGINE" || DRC=$?
  echo ""
  # Announcing "detached" after a failed launch would send the CTO off to poll for reviews
  # that were never started — the same failure-reports-success shape this whole change is
  # about. The launch result decides what we claim.
  if [ "$DRC" -ne 0 ] || [ -z "$(ls "$VPR_DIR"/*.status 2>/dev/null)" ]; then
    echo "DISPATCH=failed   # the launcher did not start any review (exit $DRC). Do NOT poll."
    echo "  Most likely: this CTO home predates vp-review-detach.sh — re-sync the mechanism"
    echo "  (scripts/cto/push-to-repos.sh from the template), or run the reviews in the"
    echo "  foreground: scripts/agentic/vp-review.sh <vp> $ART <out.md>"
  else
    echo "DISPATCH=detached   # reviews are RUNNING — poll before reading anything."
    echo "WAIT_CMD=bash $ROOT/scripts/agentic/vp-review-wait.sh $VPR_DIR --timeout 480"
  fi
else
  # subagent / handoff: a skill bash body CANNOT spawn an Agent or a window — that is a
  # main-loop action. Emit the dispatch table + exact persona/artifact paths; the CTO
  # ("Your task" below) fans the reviews via the Agent tool (subagent) or windows (handoff).
# Subagent model (model policy 2026-09-25): every Agent call passes `model:` explicitly. An
  # Agent call that omits it inherits the PARENT's model — a CTO on the stretch model then runs
  # every review/draft on it too. The alias comes from the lane pin (.cto/devteam-model;
  # `default` maps to the policy's lane family, .cto/model-budget.yaml).
  AGENT_MODEL="$(bash "$ROOT/scripts/cto/resolve-devteam-model.sh" --alias 2>/dev/null)"; AGENT_MODEL="${AGENT_MODEL:-opus}"
  echo "AGENT_MODEL=$AGENT_MODEL   # pass model: \"$AGENT_MODEL\" on EVERY Agent call below"
  echo "DISPATCH=$ENGINE   # the CTO must fan the reviews — the bash body cannot."
  echo "Write each verdict to ${VPR_DIR}/<vp>.md, then synthesize. Reviews to run:"
  for vp in "${VP_LIST[@]}"; do
    vp=$(echo "$vp" | tr -d '[:space:]'); [ -z "$vp" ] && continue
    pf=$(_VP_NAME="$vp"; persona_file)
    echo "  - vp=$vp  persona=$ROOT/$pf  ->  out=${VPR_DIR}/${vp}.md"
  done
fi
```

## Your task as CTO

**First read the `ENGINE=` and `DISPATCH=` lines in the script output above** — they tell you whether the reviews are RUNNING DETACHED (poll them), or whether YOU must fan them out.

### If `DISPATCH=detached` (engine = gemini, kimi, codex, or claude-p)
The reviews are **running**, not finished. Nothing is on disk yet. Do this, in order:

1. **Run the `WAIT_CMD=` line above** as a Bash call. It polls until every review lands or the
   timeout expires, then prints a status table. It is a poll, not a consumer — **exit 3 means
   "still running", not failure: run the same command again.** Exit 0 = all landed, 1 = at
   least one failed.
2. **Then read each verdict** and pipe it through the untrusted wrapper before quoting it:
   `bash scripts/agentic/wrap-untrusted.sh <VPR_DIR>/<vp>.md "<engine>:<vp>"`
3. Only then **Synthesize**.

**Never read a verdict file before the wait returns.** A file that is absent mid-run is a
review in flight, not a review that failed — and `<vp>.md` is now published by atomic rename,
so if it exists it has a body. A FAILED row means no verdict was produced at all: read
`<VPR_DIR>/<vp>.log` and the `.{kimi,codex,claude}-stderr.log` beside it for the cause, and
report the failure rather than synthesizing around a missing VP. For `kimi`, per-VP token
usage lines are in the same `.log` if the CEO asks about spend. For `codex` (⚠️ untested
engine), a plumbing failure is as likely as a bad review — check the log before blaming the
content.

### If `DISPATCH=subagent` (the default)
The bash body did NOT run the reviews — you run them now, in parallel, via the **Agent tool** (in-session, subscription pool — bright-line clean). For EACH `vp=… persona=… out=…` line above, launch one `Task`/Agent call (send them in a single message so they run concurrently), **passing `model: "<AGENT_MODEL>"` from the output above on every call — never omit it** (an omitted model inherits yours, and the model policy keeps subagents on the lane model), with a prompt like:

> Adopt the VP persona defined in `<persona path>` — read it in full and operate strictly as that VP in REVIEW mode (markdown verdict only; never write code/config/sprint-plans). Review the artifact at `<ARTIFACT path>`. Produce your structured verdict: recommendation (APPROVE / APPROVE-WITH-CONDITIONS / REJECT), then findings by severity (BLOCKER / MAJOR / MINOR / NOTE) each with concrete file:line-style evidence, then sign as that VP. **Write your verdict to `<out path>` and also return it.**

Treat each returned verdict as review data. (Subagent output is your own in-session work, so the gemini `wrap-untrusted` envelope isn't required — but still weigh verdicts critically, don't rubber-stamp.) Once all subagents return, **Synthesize**.

### If `DISPATCH=handoff`
Launch one interactive Claude window per VP (reuse `/handoff` machinery: write a per-VP brief to a temp sprint-style dir, pre-trust, auto-kickoff) — or, if that's heavier than the moment warrants, fall back to `--engine subagent`. Collect each `out=` verdict when the windows finish, then **Synthesize**.

### Synthesize (all engines)
You now have VP verdicts for the selected set (default vp-prod + vp-eng). The `VPR_OUTPUT_DIR=` / `VP_SET=` / `ENGINE=` lines identify the run.

**Before synthesizing, judge whether the VP set was right for this artifact.** If the artifact touches a specialty domain that wasn't included, NOTE that and recommend a follow-up `/vp-review` with the missing specialty VP. Examples:
- Dev-report involves training / evaluation / statistical claims → vp-datascience was needed
- Sprint plan introduces new infra, CI pipelines, deployment → vp-devops was needed
- Sprint plan touches auth, secrets, vendor data, PII → vp-security was needed

Then synthesize:

1. **Tally** — count BLOCKER / MAJOR / MINOR / NOTE per VP. Flag any VP whose verdict is malformed (free-form prose instead of structured assessment).
2. **Cross-VP convergence** — same blocker flagged by 2+ VPs is the highest-confidence signal. Identify these specifically.
3. **Decision** — recommend ONE of:
   - `APPROVED` — no blockers, minors acceptable
   - `REJECTED-FOR-REVISION` — blockers exist, list what must change
   - `ESCALATE-TO-CEO` — VPs disagree on a fundamental question only the CEO can decide
4. **Write the decision** to a file alongside the artifact:
   - Path: `$(dirname $ARGUMENTS)/cto-decision-$(date +%Y%m%d-%H%M%S).md`
   - Contents: decision, top blockers, cross-VP convergence findings, action items with concrete file paths, references to the verdict files at `${VPR_OUTPUT_DIR}/{vp-*}.md` (use the actual VPR_OUTPUT_DIR value from the script output above, NOT the literal placeholder). Note which VPs were run and whether any specialty VP follow-ups are recommended.
5. **Present a 5-line summary to the CEO** — verdict, top 1-2 blockers, recommended next action, plus any missing-VP recommendation. Brief.

Sign off as: — CTO
