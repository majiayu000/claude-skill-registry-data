---
name: setup
description: First-time environment setup for a freshly cloned copy of this template. Checks prerequisites (git identity, gh auth, review-engine env vars — ANTHROPIC_API_KEY should be UNSET, OPENROUTER_API_KEY needed for the kimi engine), asks whether this clone operates as the CTO home directly or should spawn a separate private <project>-cto home, discovers already-cloned sibling repos on disk and offers to register + deploy the template's dev-team mechanism into them, and writes .cto/projects.yaml. Auto-fires on "set up my environment", "get started", "onboard me", first session in a fresh clone (the preflight [FIRST-RUN] directive), or when the CEO asks to add more repos to an existing registry. Idempotent — safe to re-run to register additional repos later.
allowed-tools: Bash(*) Read Write Task
argument-hint: (no arguments — fully interactive)
---

# Setup

Onboards a fresh clone of this template: checks prerequisites, decides how this clone operates,
and registers (and optionally deploys the mechanism into) the repos it will orchestrate.

## Gather prerequisite state + scan for candidate repos

```!
set -uo pipefail
[ -n "${ZSH_VERSION:-}" ] && setopt sh_word_split
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

echo "=== Prerequisite checks ==="
"$ROOT/scripts/agentic/preflight.sh" 2>&1 || true

echo ""
echo "=== Additional setup-specific checks ==="
command -v git >/dev/null 2>&1 && echo "  [ok] git: $(git --version)" || echo "  [MISSING] git — required, install from https://git-scm.com/"
if git config user.name >/dev/null 2>&1 && git config user.email >/dev/null 2>&1; then
  echo "  [ok] git identity: $(git config user.name) <$(git config user.email)>"
else
  echo "  [WARN] git identity not fully configured — run: git config --global user.name \"Your Name\" && git config --global user.email you@example.com"
fi
if command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then
    echo "  [ok] gh CLI authenticated"
  else
    echo "  [WARN] gh CLI installed but not logged in — run: gh auth login"
  fi
else
  echo "  [WARN] gh CLI not found — needed to publish new repos (https://cli.github.com/)"
fi
command -v claude >/dev/null 2>&1 && echo "  [ok] claude CLI: $(claude --version 2>/dev/null | head -1)" || echo "  [note] claude CLI not on PATH (fine if you're only using the IDE/desktop app)"
command -v gemini >/dev/null 2>&1 && echo "  [note] gemini CLI present (dead as a review engine since 2026-06-19 — not needed; subagent/kimi cover reviews)" || echo "  [ok] gemini CLI absent — expected, not required"
command -v python3 >/dev/null 2>&1 && echo "  [ok] python3: $(python3 --version)" || echo "  [MISSING] python3 — required by several scripts (openrouter-chat.sh, settings tooling)"
if [ -n "${OPENROUTER_API_KEY:-}" ]; then
  echo "  [ok] OPENROUTER_API_KEY set — kimi review engine (cross-family independent VP reviews) available"
else
  echo "  [note] OPENROUTER_API_KEY not set — kimi engine unavailable; subagent (in-session Agent) still works for all reviews"
fi
command -v codex >/dev/null 2>&1 && echo "  [note] codex CLI present — 'codex' review engine (⚠️ UNTESTED as of 2026-07-02) could be tried; verify its first real output before trusting a verdict" || echo "  [note] codex CLI absent — fine, it's an untested/optional engine, not required for anything"
if [ -n "${ANTHROPIC_API_KEY:-}${ANTHROPIC_AUTH_TOKEN:-}" ]; then
  echo "  [WARN] ANTHROPIC_API_KEY/ANTHROPIC_AUTH_TOKEN is set — verify intent, this repo's bright-line assumes subscription auth, not metered API"
else
  echo "  [ok] no ANTHROPIC_API_KEY/ANTHROPIC_AUTH_TOKEN set (expected)"
fi

echo ""
echo "=== Repo identity ==="
REPO_NAME="$(basename "$ROOT")"
echo "  this clone: $REPO_NAME  (path: $ROOT)"
case "$REPO_NAME" in
  *-cto) echo "  already named as a CTO home (*-cto) — treat as 'operate in place'." ;;
  agent-workflow-template) echo "  still named as the public template — ask whether to operate in place or spawn a private <project>-cto home." ;;
  *) echo "  custom name — likely already a deliberate CTO-home rename; treat as 'operate in place'." ;;
esac

echo ""
echo "=== Existing registry ==="
if [ -f "$ROOT/.cto/projects.yaml" ]; then
  echo "  .cto/projects.yaml EXISTS — this is a re-run (add more repos). Existing entries:"
  grep -E '^\s*- name:' "$ROOT/.cto/projects.yaml" | sed 's/^/    /' || echo "    (none parsed — file may be empty/template-only)"
else
  echo "  .cto/projects.yaml does NOT exist — first-time setup."
fi

echo ""
echo "=== Candidate sibling repos (git repos next to this clone, not yet registered) ==="
PARENT="$(dirname "$ROOT")"
REGISTERED=""
[ -f "$ROOT/.cto/projects.yaml" ] && REGISTERED=$(grep -E '^\s*- name:' "$ROOT/.cto/projects.yaml" | sed 's/.*- name:[[:space:]]*//')
FOUND=0
for d in "$PARENT"/*/; do
  d="${d%/}"
  name="$(basename "$d")"
  [ "$d" = "$ROOT" ] && continue
  [ -d "$d/.git" ] || continue
  case "$name" in *-cto) continue ;; esac
  already=0
  for r in $REGISTERED; do [ "$r" = "$name" ] && already=1; done
  [ "$already" -eq 1 ] && continue
  branch=$(git -C "$d" branch --show-current 2>/dev/null)
  echo "  - $name  (path: $d, branch: ${branch:-unknown})"
  FOUND=$((FOUND+1))
done
[ "$FOUND" -eq 0 ] && echo "  (none found — no sibling git repos next to this clone)"
```

## Your task as CTO

You now have: prerequisite check results, this clone's identity, whether a registry already
exists, and a list of candidate sibling repos. Walk the CEO through onboarding:

1. **Present prerequisites plainly.** Group into "ready to go" vs "needs attention" — for
   anything `[MISSING]` or `[WARN]`, give the one-line fix already printed above. Don't block on
   `[note]` items (gemini absence, no OPENROUTER_API_KEY) — those are optional capabilities, not
   requirements. `python3`/`git` missing IS blocking — stop and tell the CEO to install it first.

2. **If `.cto/projects.yaml` does NOT exist yet** (first-time setup), ask via `AskUserQuestion`:
   *"How should this clone operate?"*
   - **"As my CTO home directly (recommended)"** — use this clone in place. Simplest; fine for a
     personal/private fork. This clone's `.cto/projects.yaml` becomes the live registry.
   - **"Spawn a separate private `<project>-cto` home"** — keep this clone as a clean template
     (e.g. if it tracks a shared/public upstream you don't want to accumulate project IP in).
     Ask the CEO for a project name, then invoke the **`/new-project`** skill (via the Skill tool)
     with `--adopt` if sibling repos were found (pass them via `--repos=`) or plain greenfield
     otherwise. `/new-project` handles the rest (scaffolds `<project>-cto`, seeds its registry,
     prints publish commands) — once it's invoked, **stop here**; do not also write this clone's
     own registry.

   If `.cto/projects.yaml` DOES already exist, skip this question — you're just adding repos to
   an established setup.

3. **If operating in place** (or adding to an existing in-place registry): if candidate sibling
   repos were found, ask via `AskUserQuestion` (multiSelect): *"Which of these already-cloned
   repos should be registered as dev-team repos?"* — one option per repo found, labelled with
   its name. If none were found, tell the CEO none were discovered and that repos can be added
   any time by re-running `/setup` or editing `.cto/projects.yaml` directly.

4. **For each repo the CEO selects:** append an entry to `.cto/projects.yaml` (create the file
   with the standard header — copy the structure from `.cto/projects.yaml.example` — if it
   doesn't exist yet) with `name`, `path`, `description: TODO — ask the CEO or infer from the
   repo's README`, `language` (infer from the repo if obvious, e.g. `pyproject.toml` → python,
   `package.json` → typescript/javascript), `active: true`.

4a. **Settle the review engine** — a project-start choice, like the permissions posture, and
   worth one question now rather than a surprise at the first accept gate. Every VP review,
   sprint fan-out and accept-gate runs through it. Skip only if this clone's `.review-engine`
   already holds a selectable value. `bash scripts/agentic/set-review-engine.sh --menu` prints
   the live menu; ask via `AskUserQuestion` (header: "Review engine"):

   - **kimi (recommended)** — OpenRouter `moonshotai/kimi-k2.6`. Cross-**family**, so a VP
     verdict is genuinely independent of the model that wrote the work. Pennies per review,
     non-Anthropic; needs `OPENROUTER_API_KEY` (the prerequisite check above reports it).
   - **subagent** — in-session Agent calls. Free, no API key. Same-family: Claude reviewing
     Claude, a weaker accept-gate.
   - **handoff** — review runs in its own interactive Claude window. Free, slowest.

   Apply it to **this clone** (the CTO home) — that file is what makes it the project default:

   ```
   bash scripts/agentic/set-review-engine.sh . <engine>
   ```

   `push-to-repos.sh` then seeds and heals every dev repo from it in step 5. If the CEO picks
   `kimi` without `OPENROUTER_API_KEY` set, say plainly that reviews will fail until it is
   exported, and offer `subagent` as the no-key option.

5. **Ask whether to deploy the template's dev-team mechanism into the selected repos now.** If
   yes, run:
   ```
   ./scripts/cto/push-to-repos.sh <repo1> <repo2> ...
   ```
   (only the repos just selected — don't blanket-push to repos already set up). This writes
   `CLAUDE.md`, `.claude/settings.json`, hooks, `scripts/agentic/`, `docs/personas/`, and
   `docs/sprints/_templates/` into each target — **it does NOT commit**. Tell the CEO the files
   are on disk uncommitted; committing is the dev-team session's call (or theirs), consistent
   with never bulk-committing into a repo you don't own the working state of. If any target repo
   is dirty (uncommitted changes already present), still write the mechanism files (they're
   template-owned, not app code) but flag it so the CEO knows there's other WIP in that repo.

6. **Mark setup complete and record the CTO home:**
   ```
   mkdir -p .claude && touch .claude/.setup-done
   mkdir -p ~/.cto && pwd > ~/.cto/home
   ```
   `~/.cto/home` is the last-resort anchor for every skill. Skills resolve the CTO home from
   `$CTO_HOME` → `$CTO_REPO` → `$CLAUDE_PROJECT_DIR` → a walk up from the cwd → this file.
   `$CLAUDE_PROJECT_DIR` has been observed empty inside skill shells, and a shell that has
   cd'd into a dev repo makes the walk-up miss, so without this file those sessions fail
   (loudly, but they fail). One line here prevents it.

7. **Summarize:** what's registered, what got deployed, and the next real step — author the first
   PRD under `docs/roadmap/prds/` and pick a permissions posture (`default`/`acceptEdits`/
   `bypassPermissions`, toggle any time with Shift+Tab) if that hasn't already been asked this
   session.

Sign as: — CTO
