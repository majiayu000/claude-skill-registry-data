#!/usr/bin/env bash
# Install the Chord agent skill.
#
# Copies this skill folder to:
#   ~/.claude/skills/chord   (Claude Code, personal skills)
#   ~/.agents/skills/chord   (agents that read the shared ~/.agents/skills folder, e.g. Codex)
# and prints the OpenClaw and Hermes paths with the command to copy it there.
#
# Usage:
#   bash scripts/install.sh                      # both personal folders
#   bash scripts/install.sh --only claude        # just ~/.claude/skills/chord  (or: --only agents)
#   bash scripts/install.sh --project DIR        # DIR/.claude/skills/chord only (project-scoped)
#   bash scripts/install.sh --from-git URL [--subdir PATH]
#                                                # clone URL first and install the skill found in it
#   bash scripts/install.sh --dry-run            # print what would happen, change nothing
#   bash scripts/install.sh --uninstall          # remove the copies this script manages
#
# Safe to run again: each target is replaced as a whole, and only when it is empty or already holds
# this skill (SKILL.md with "name: chord"). No network access unless --from-git is given.
set -euo pipefail

SKILL_NAME="chord"
ONLY=""
PROJECT=""
FROM_GIT=""
SUBDIR="packages/skills/chord"
DRY_RUN=0
UNINSTALL=0

die() { printf 'install.sh: %s\n' "$*" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --only) ONLY="${2:-}"; shift 2 ;;
    --project) PROJECT="${2:-}"; shift 2 ;;
    --from-git) FROM_GIT="${2:-}"; shift 2 ;;
    --subdir) SUBDIR="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --uninstall) UNINSTALL=1; shift ;;
    -h|--help) sed -n '2,21p' "$0"; exit 0 ;;
    *) die "unknown option: $1 (try --help)" ;;
  esac
done

case "$ONLY" in ""|claude|agents) ;; *) die "--only takes 'claude' or 'agents'" ;; esac

# ---- where the skill comes from --------------------------------------------------------------
TMP_DIR=""
cleanup() { [[ -n "$TMP_DIR" && -d "$TMP_DIR" ]] && rm -rf "$TMP_DIR"; return 0; }
trap cleanup EXIT

if [[ -n "$FROM_GIT" ]]; then
  command -v git >/dev/null 2>&1 || die "git is not installed"
  TMP_DIR="$(mktemp -d)"
  printf 'Cloning %s ...\n' "$FROM_GIT"
  git clone --depth 1 --quiet "$FROM_GIT" "$TMP_DIR/repo" || die "git clone failed"
  if [[ -f "$TMP_DIR/repo/SKILL.md" ]]; then SRC="$TMP_DIR/repo"; else SRC="$TMP_DIR/repo/$SUBDIR"; fi
else
  SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi

[[ -f "$SRC/SKILL.md" ]] || die "no SKILL.md in $SRC"
grep -q "^name: ${SKILL_NAME}\$" "$SRC/SKILL.md" || die "$SRC/SKILL.md is not the ${SKILL_NAME} skill"

# ---- targets ---------------------------------------------------------------------------------
TARGETS=()
if [[ -n "$PROJECT" ]]; then
  [[ -d "$PROJECT" ]] || die "project folder $PROJECT does not exist"
  TARGETS+=("$(cd "$PROJECT" && pwd)/.claude/skills/${SKILL_NAME}")
else
  [[ -z "$ONLY" || "$ONLY" == "claude" ]] && TARGETS+=("$HOME/.claude/skills/${SKILL_NAME}")
  [[ -z "$ONLY" || "$ONLY" == "agents" ]] && TARGETS+=("$HOME/.agents/skills/${SKILL_NAME}")
fi

owned_or_empty() {
  # true when the folder does not exist, is empty, or already holds this skill
  local dir="$1"
  [[ ! -e "$dir" ]] && return 0
  [[ -d "$dir" ]] || return 1
  [[ -z "$(ls -A "$dir")" ]] && return 0
  [[ -f "$dir/SKILL.md" ]] && grep -q "^name: ${SKILL_NAME}\$" "$dir/SKILL.md"
}

for dest in "${TARGETS[@]}"; do
  if [[ "$(cd "$SRC" && pwd -P)" == "$( [[ -d "$dest" ]] && cd "$dest" && pwd -P )" ]]; then
    printf 'skip    %s (this is the source folder)\n' "$dest"
    continue
  fi
  owned_or_empty "$dest" || die "$dest exists and is not the ${SKILL_NAME} skill; move it away first"
  if [[ "$UNINSTALL" -eq 1 ]]; then
    if [[ -e "$dest" ]]; then
      if [[ "$DRY_RUN" -eq 1 ]]; then
        printf 'would remove %s\n' "$dest"
      else
        rm -rf "$dest"
        printf 'removed %s\n' "$dest"
      fi
    else
      printf 'absent  %s\n' "$dest"
    fi
    continue
  fi
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf 'would install %s -> %s\n' "$SRC" "$dest"
    continue
  fi
  mkdir -p "$(dirname "$dest")"
  staging="${dest}.installing.$$"
  rm -rf "$staging"
  cp -R "$SRC" "$staging"
  # never ship editor or OS litter
  find "$staging" \( -name '.DS_Store' -o -name '__pycache__' -o -name '*.pyc' \) -prune -exec rm -rf {} + 2>/dev/null || true
  chmod +x "$staging/scripts/"*.sh "$staging/scripts/"*.py 2>/dev/null || true
  rm -rf "$dest"
  mv "$staging" "$dest"
  printf 'installed %s\n' "$dest"
done

if [[ "$UNINSTALL" -eq 0 ]]; then
  cat <<EOF

Other agents (not changed by this script):
  OpenClaw : cp -R "$SRC" ~/.openclaw/skills/${SKILL_NAME}
             (or <your OpenClaw workspace>/skills/${SKILL_NAME} for one workspace)
  Hermes   : cp -R "$SRC" ~/.hermes/skills/${SKILL_NAME}

Optional: export CHORD_API_KEY=... to raise the rate limit and use Chord Ask.
Get a key at https://getchord.xyz/ask (Settings > API Key). Data calls work without one.
Check: python3 <skill folder>/scripts/chord.py chains
EOF
fi
