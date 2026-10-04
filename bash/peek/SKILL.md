---
name: peek
description: Peek into a per-repo Phase 2 dev team session by tailing its JSONL transcript. Shows recent thinking blocks, current tool call, and last outputs without leaving the CTO session. Use when CEO asks "what's the dev team doing?", "show me what acme-ui is thinking", or wants real-time visibility into a backgrounded session.
allowed-tools: Bash(*) Read
argument-hint: <repo-name>
---

# Peek: $ARGUMENTS

Tails the named repo's Phase 2 session JSONL to show what the dev team is doing right now.

```!
set -uo pipefail
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
  echo "ERROR: fleet registry not found at $CTO_REGISTRY — run this from the CTO home."
  exit 1
fi
REPO_NAME="$ARGUMENTS"

if [ -z "$REPO_NAME" ]; then
  echo "Usage: /peek <repo-name>"
  echo ""
  echo "Active repos with tracked sessions:"
  python3 - "$CTO_REGISTRY" <<'PYEOF'
import re, os, sys
from pathlib import Path
with open(sys.argv[1]) as f:
    text = f.read()
for b in re.split(r'(?=- name:)', text):
    m = re.search(r'- name:\s*(\S+)', b)
    p = re.search(r'path:\s*(\S+)', b)
    a = re.search(r'active:\s*(\S+)', b)
    if not m or not p:
        continue
    is_active = (a is None) or a.group(1).lower() not in ('false','no','0')
    if not is_active:
        continue
    sess_id_file = Path(p.group(1)) / '.claude' / 'current-session.id'
    has_session = "session" if sess_id_file.exists() else "no-session"
    print(f"  {m.group(1):<32}  {has_session}")
PYEOF
  exit 1
fi

# Resolve repo path from registry. Accepts exact name OR a suffix alias
# ("tuner" -> "acme-service-a", "morphology" -> "acme-service-b").
REPO_PATH=$(python3 - "$CTO_REGISTRY" "$REPO_NAME" <<'PYEOF'
import re, sys
with open(sys.argv[1]) as f:
    text = f.read()
arg = sys.argv[2]
# First pass: exact match
for b in re.split(r'(?=- name:)', text):
    m = re.search(r'- name:\s*(\S+)', b)
    p = re.search(r'path:\s*(\S+)', b)
    if m and m.group(1) == arg and p:
        print(p.group(1))
        break
else:
    # Second pass: suffix alias (after "acme-" prefix or last "-" segment)
    candidates = []
    for b in re.split(r'(?=- name:)', text):
        m = re.search(r'- name:\s*(\S+)', b)
        p = re.search(r'path:\s*(\S+)', b)
        if not m or not p:
            continue
        name = m.group(1)
        # match if arg is the suffix after "acme-" OR the last hyphen-segment
        if name == f"acme-{arg}" or name.endswith(f"-{arg}"):
            candidates.append((name, p.group(1)))
    if len(candidates) == 1:
        print(candidates[0][1])
    elif len(candidates) > 1:
        import sys
        print(f"ERROR: ambiguous alias '{arg}' matches: {[c[0] for c in candidates]}", file=sys.stderr)
PYEOF
)

if [ -z "$REPO_PATH" ]; then
  echo "ERROR: repo '$REPO_NAME' not found in .cto/projects.yaml (tried exact + suffix-alias match)"
  exit 1
fi

SESS_ID_FILE="$REPO_PATH/.claude/current-session.id"
if [ ! -f "$SESS_ID_FILE" ]; then
  echo "No tracked Phase 2 session for $REPO_NAME (file not found: $SESS_ID_FILE)"
  echo "Either no session was started, or its SessionStart hook didn't record the ID."
  exit 0
fi

RECORDED_SESSION_ID=$(cat "$SESS_ID_FILE" | tr -d '[:space:]')
echo "Recorded session ID: $RECORDED_SESSION_ID"
echo "Repo path: $REPO_PATH"

# Find the project's JSONL dir (derived from the repo path with / → -)
PROJECT_DIR_NAME="$(echo "$REPO_PATH" | sed 's|/|-|g')"
PROJECT_DIR="$HOME/.claude/projects/$PROJECT_DIR_NAME"

# Locate the JSONL.
#
# IMPORTANT: current-session.id may be STALE because every sub-claude
# (vp-review.sh's claude engine, any other Task subagent) fires the
# SessionStart hook which overwrites current-session.id. The live dev-team
# session may differ from what current-session.id says.
#
# Strategy: prefer the largest JSONL in the project dir modified in the last
# 2 hours (heuristic: the dev-team session is the long-lived one and has the
# biggest transcript; sub-claude review sessions are short and small). Fall
# back to current-session.id if no recent JSONLs exist.
JSONL=$(find "$PROJECT_DIR" -maxdepth 1 -name '*.jsonl' -mmin -120 -type f 2>/dev/null | xargs ls -lS 2>/dev/null | head -1 | awk '{print $NF}')
JSONL_SESSION_ID=""
if [ -n "$JSONL" ]; then
  JSONL_SESSION_ID=$(basename "$JSONL" .jsonl)
fi

if [ -n "$JSONL" ] && [ "$JSONL_SESSION_ID" != "$RECORDED_SESSION_ID" ]; then
  echo "NOTE: largest-recent JSONL is $JSONL_SESSION_ID, NOT the recorded session_id."
  echo "      This usually means a sub-claude (vp-review.sh, etc.) overwrote current-session.id."
  echo "      Showing live dev-team session ($JSONL_SESSION_ID), not the recorded one."
fi

# Fallback: if no recent JSONL found, use the recorded session_id
if [ -z "$JSONL" ]; then
  JSONL=$(find "$HOME/.claude/projects" -name "${RECORDED_SESSION_ID}.jsonl" -type f 2>/dev/null | head -1)
fi

if [ -z "$JSONL" ]; then
  echo "ERROR: no JSONL found for $REPO_NAME under $PROJECT_DIR/ (and recorded session $RECORDED_SESSION_ID not found either)"
  echo "Session may have been deleted or there's nothing to peek at."
  exit 1
fi

echo "JSONL: $JSONL"
SIZE=$(wc -c < "$JSONL")
LINES=$(wc -l < "$JSONL")
MTIME=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$JSONL")
AGE_SEC=$(( $(date +%s) - $(stat -f "%m" "$JSONL") ))
echo "Size: $SIZE bytes, $LINES lines, last activity $AGE_SEC seconds ago ($MTIME)"
echo ""

# Parse last N entries for thinking blocks + tool calls + recent outputs.
#
# NOTE: do NOT use `tail | python3 - <<PYEOF` — the pipe and the heredoc both
# claim stdin, behavior is undefined, and the tail output can end up being
# interpreted as the python script (which then crashes on bare `false` from
# the JSONL). Pass JSONL via env var and read it inside the script.
echo "=== Recent activity (last ~50 entries, parsed) ==="
JSONL_FILE="$JSONL" python3 - <<'PYEOF'
import os, json
path = os.environ['JSONL_FILE']
events = []
with open(path) as f:
    for line in f.readlines()[-50:]:
        try:
            events.append(json.loads(line))
        except Exception:
            pass

for e in events[-20:]:
    msg = e.get('message', {})
    role = msg.get('role', '') if isinstance(msg, dict) else ''
    ts = e.get('timestamp', '')[:19]

    if isinstance(msg, dict):
        content = msg.get('content', [])
        if isinstance(content, list):
            for c in content:
                if not isinstance(c, dict):
                    continue
                ct = c.get('type', '?')
                if ct == 'thinking':
                    text = c.get('thinking', '')[:300]
                    print(f"[{ts}] THINKING: {text}{'...' if len(c.get('thinking','')) > 300 else ''}")
                elif ct == 'text' and role == 'assistant':
                    text = c.get('text', '')[:300]
                    print(f"[{ts}] ASSISTANT: {text}{'...' if len(c.get('text','')) > 300 else ''}")
                elif ct == 'tool_use':
                    name = c.get('name', '?')
                    inp = json.dumps(c.get('input', {}))[:200]
                    print(f"[{ts}] TOOL_USE: {name}({inp})")
                elif ct == 'tool_result':
                    text = str(c.get('content', ''))[:200]
                    print(f"[{ts}] TOOL_RESULT: {text}{'...' if len(str(c.get('content','')) ) > 200 else ''}")
        elif isinstance(content, str):
            print(f"[{ts}] {role.upper()}: {content[:300]}")
PYEOF
```

## Your task as CTO

Above is the recent activity from the named dev-team session. Summarize for the CEO in 5 lines or fewer:

1. **What it's working on now** (current task or tool call)
2. **What it most recently completed** (the last assistant text or tool_result)
3. **Any signs of being stuck** (repeated same tool calls, error patterns)
4. **Estimated time on current task** (if visible from activity timestamps)
5. **Recommendation:** keep watching / intervene / wait for completion

If the session looks healthy and progressing, say so simply. Don't manufacture concerns.

Sign as: — CTO
