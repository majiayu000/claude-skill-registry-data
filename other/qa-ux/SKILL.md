---
name: qa-ux
description: Drive the live product as a skeptical end-user across browser (DOMShell MCP), CLI, and MCP surfaces, then produce a defect report + a derived UX flow-graph + provenance-stamped hero assets. Two modes — `--mode plan` authors qa-plan.md at sprint-planning time (HARD vs SOFT assertions, hero shots, in-scope surfaces); `--mode drive` (default) is the accept-time gate that exercises the running app against qa-plan.md before /sprint-accept. Use when a user-facing sprint needs UX/output-quality verification, or to author a QA test plan up front. Implements docs/personas/qa-ux.md.
allowed-tools: Bash(*) Read Write
argument-hint: <sprint-dir> [--mode plan|drive] [--surfaces browser,cli,mcp] [--url <app-url>] [--engine gemini|claude] [--handover <path>]
---

# QA-UX: $ARGUMENTS

Runs the QA-UX persona (`docs/personas/qa-ux.md`) against a sprint. **plan** mode authors the
test plan before code; **drive** mode is the accept-time gate that drives the live app.

## Setup + standup

```!
set -uo pipefail
[ -n "${ZSH_VERSION:-}" ] && setopt sh_word_split
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"; cd "$ROOT" || { echo "ERROR: not in a repo"; exit 1; }

ARGS="$ARGUMENTS"
SPRINT_DIR=""; MODE="drive"; SURFACES=""; URL=""; ENGINE="claude"; HANDOVER=""
# Accept BOTH `--flag=value` and `--flag value` (the argument-hint shows the space
# form). Bare `--flag` sets EXPECT so the next token fills it — otherwise a value
# like `plan` falls through to the positional branch and the flag silently keeps
# its default (the `--mode plan` -> stays `drive` bug caught in review).
EXPECT=""
for tok in $ARGS; do
  if [ -n "$EXPECT" ]; then
    case "$EXPECT" in
      mode)     MODE="$tok" ;;
      surfaces) SURFACES="$tok" ;;
      url)      URL="$tok" ;;
      engine)   ENGINE="$tok" ;;
      handover) HANDOVER="$tok" ;;
    esac
    EXPECT=""; continue
  fi
  case "$tok" in
    --mode=*)     MODE="${tok#--mode=}" ;;
    --surfaces=*) SURFACES="${tok#--surfaces=}" ;;
    --url=*)      URL="${tok#--url=}" ;;
    --engine=*)   ENGINE="${tok#--engine=}" ;;
    --handover=*) HANDOVER="${tok#--handover=}" ;;
    --mode)       EXPECT=mode ;;
    --surfaces)   EXPECT=surfaces ;;
    --url)        EXPECT=url ;;
    --engine)     EXPECT=engine ;;
    --handover)   EXPECT=handover ;;
    --*)          echo "Unknown flag: $tok" >&2 ;;
    *)            [ -z "$SPRINT_DIR" ] && SPRINT_DIR="$tok" ;;
  esac
done

if [ -z "$SPRINT_DIR" ]; then
  echo "Usage: /qa-ux <sprint-dir> [--mode plan|drive] [--surfaces browser,cli,mcp] [--url <app-url>] [--engine gemini|claude]"
  exit 1
fi
[ -d "$SPRINT_DIR" ] || { echo "ERROR: sprint dir not found: $SPRINT_DIR"; exit 1; }

PERSONA="$ROOT/docs/personas/qa-ux.md"
QA_PLAN="$SPRINT_DIR/qa-plan.md"
QA_REPORT="$SPRINT_DIR/qa-report.md"
ASSETS="$SPRINT_DIR/assets"
[ -f "$PERSONA" ] || echo "WARN: persona not found at $PERSONA (sync it from the template)"

echo "persona   : $PERSONA"
echo "sprint    : $SPRINT_DIR"
echo "mode      : $MODE"
echo "surfaces  : ${SURFACES:-<read from qa-plan / auto>}"
echo "engine    : $ENGINE   (default+only: interactive Claude — NEVER claude -p; gemini engine DEPRECATED 2026-06-19)"
echo ""

if [ "$MODE" = "plan" ]; then
  if [ ! -f "$QA_PLAN" ] && [ -f "$ROOT/docs/sprints/_templates/qa-plan.md" ]; then
    cp "$ROOT/docs/sprints/_templates/qa-plan.md" "$QA_PLAN"
    echo "seeded $QA_PLAN from template — author it (HARD/SOFT assertions, surfaces, hero shots)."
  else
    echo "qa-plan : ${QA_PLAN} ($( [ -f "$QA_PLAN" ] && echo exists || echo MISSING template ))"
  fi
  echo "PLAN MODE — author/refine the qa-plan; no live driving."
  exit 0
fi

# ---- drive mode ----
[ -f "$QA_PLAN" ] || { echo "ERROR: $QA_PLAN missing — run '/qa-ux $SPRINT_DIR --mode plan' first (shift-left: the plan precedes the drive)."; exit 1; }
mkdir -p "$ASSETS"

# engine=gemini: DEPRECATED 2026-06-19. Google removed the gemini-CLI free tier
# (IneligibleTierError / reasonCode UNSUPPORTED_CLIENT — "migrate to the Antigravity suite").
# Every gemini call now hard-fails at auth, so the gemini drive can no longer run. Fail loud
# and point at the claude engine (the default) rather than dispatching into a broken path.
if [ "$ENGINE" = "gemini" ]; then
  echo "ERROR: the gemini drive engine is DEPRECATED/DEAD as of 2026-06-19 (Google UNSUPPORTED_CLIENT;"
  echo "  migrate-to-Antigravity). It cannot authenticate. The Claude engine is now the default + only path."
  echo "  Re-run WITHOUT --engine gemini (or with --engine claude). NOTE: this same gemini death also"
  echo "  breaks /vp-review and /sprint-fanout — flagged separately to the CTO/CEO."
  exit 1
fi

# engine=claude (default + only): LAUNCH an interactive Claude session via qa-drive-claude.sh
# (reuses /handoff machinery — brief in docs/, skill writes pending-prompt.md, pre-authorizes
# trust+MCP+permissions, records the window id, AUTO-SENDS the "go" kickoff). Zero-touch; the
# CTO never hand-edits .claude/. Optional --handover <path> drives from an existing brief.
if [ "$ENGINE" = "claude" ] && [ -x "$ROOT/scripts/agentic/qa-drive-claude.sh" ]; then
  echo "DRIVE MODE (engine=claude) — launching an interactive Claude session via qa-drive-claude.sh ..."
  "$ROOT/scripts/agentic/qa-drive-claude.sh" "$SPRINT_DIR" --url "$URL" ${HANDOVER:+--handover "$HANDOVER"}
  echo ""
  echo "CLAUDE DRIVE LAUNCHED — zero-touch (window id recorded, 'go' kickoff auto-sent). If it doesn't"
  echo "start, grant Terminal Accessibility perm or type 'go' + Enter in the tab. Artifacts land in the sprint dir."
  exit 0
fi

# fallback (no engine script available): standup guard, then drive IN-SESSION per Your task.
if [ -x "$ROOT/scripts/agentic/qa-standup.sh" ]; then
  "$ROOT/scripts/agentic/qa-standup.sh" --url "$URL" --sprint-dir "$SPRINT_DIR" || { echo "STANDUP FAILED — aborting drive (target unreachable / prod-guard tripped / DOMShell not wired)."; exit 1; }
else
  echo "WARN: scripts/agentic/qa-standup.sh missing — proceed only on a known non-prod target."
fi
echo ""
echo "DRIVE MODE (in-session fallback) — standup OK. Adopt QA-UX and drive per Your task below."
echo "Artifacts to produce: $QA_REPORT , $SPRINT_DIR/flow-graph.json(+.md) , $ASSETS/"
```

## Your task as QA-UX

**Adopt the persona:** read `docs/personas/qa-ux.md` in full and operate as **QA-UX** (review/adversarial; you drive and report, you never fix). Then execute the selected mode.

### If `--mode plan`
Author/refine `qa-plan.md` (template seeded above):
1. Declare the **in-scope surfaces** (browser / CLI / MCP) this sprint exposes.
2. For each journey, write the acceptance signals split into **HARD** (exact string/pattern/`data-testid`/selector — deterministic, will graduate to `tests/e2e/`) and **SOFT** (semantic judgment).
3. Name the **hero shots** (critical delivered features to capture) and the **fault-domain routing** expectations.
4. Link each journey back to the PRD requirement / RICE it verifies.
Stop after writing the plan — no live driving. Sign `— QA`.

### If `--mode drive` (accept-time gate)

**Engine=claude (default + only):** the setup block above launched an interactive Claude session in the UX repo (`qa-drive-claude.sh`) that pre-authorizes the workspace, records the window id, and auto-sends the "go" kickoff. THAT session is the drive — it calls `domshell_execute` directly and writes the artifacts. From the CTO session your job is to **monitor (`/peek <repo>`) and then read the produced `qa-report.md` + flow-graph + assets and summarize — do NOT re-drive.** (The former gemini engine is deprecated/dead as of 2026-06-19.)

**If you ARE the launched drive session** (you received the brief), adopt QA-UX and drive it yourself by calling `domshell_execute` directly — never re-invoke the `/qa-ux` skill:
1. **Drive each in-scope surface** against `qa-plan.md`:
   - **browser** → DOMShell MCP. **PRECONDITION: `domshell_execute` MUST be in your tool list.** The standup (`qa-standup.sh`) already self-registers DOMShell into `.mcp.json`; if the tool is still absent, the session simply wasn't restarted afterward (MCP loads at session start). In that case **do NOT substitute API/DB inspection and call it a browser drive**: mark the browser surface `BLOCKED — DOMShell registered but session not restarted`, finish the other surfaces, and tell the CTO to restart the session + re-run. **If present:** **open your OWN tab group first** (`group_id:"new"`, name it `qa-ux-<sprint>`, carry the returned `[lane: <id>]` on every call, and **`group close <group_id>` when done** — the harness also sweeps orphan `qa-ux-*` lanes on exit — NEVER the shared/default lane, so you don't hijack a human's tabs or collide with another agent). Then `ls`/`cd`/`cat`/`text`/`grep`/`extract_table` to assert HARD signals; judge SOFT signals; `screenshot` each hero feature.
   - **CLI** → Bash: invoke the real CLI, capture stdout/stderr + exit codes, assert HARD, judge SOFT.
   - **MCP** → call the repo's own MCP server as an agent would; check tool-description fidelity, round-trips/token cost, error recovery.
2. **Build the UX flow-graph** as a byproduct (`$SPRINT_DIR/flow-graph.json` + Mermaid `flow-graph.md`): nodes = UI states (route + HARD landmarks, transient DOM stripped), edges = actions (+ the API calls they fire + any defect). `diff` against the prior sprint's if present.
3. **Tag every finding** by severity (`BLOCKER/MAJOR/MINOR/NOTE`) AND fault-domain (`client/integration/server/data-quality/ux/unverified`), each with concrete evidence. Route `data/quality` to VP-DS — do NOT make statistical claims.
4. **Redact before persisting:** run every transcript / report / captured log through `scripts/agentic/qa-redact.sh --in-place <file>` BEFORE it lands in `assets/`. Screenshots rely on UI-level masking at capture. No credential/token/PII leaves the QA lane.
5. **Write `qa-report.md`** (template: `docs/sprints/_templates/qa-report.md`): surface-by-surface pass/fail, findings, flow-graph diff summary, hero-asset index, and a recommended **ship / no-ship** posture.

### Then, as CTO
Summarize for the CEO: surfaces driven, BLOCKER/MAJOR counts by fault-domain, hero assets captured, flow-graph delta, and the ship/no-ship recommendation. **Gate semantics:** the report must exist and be reviewed before `/sprint-accept`; shipping with known defects is a CTO/CEO call, documented in the `cto-decision`. Sign `— CTO`.
