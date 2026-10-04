---
name: new-project
description: Stand up a new multi-repo project's PRIVATE CTO home (<project>-cto) from this template's mechanism, and either scaffold its dev repos (greenfield) or wire it to a fleet that already exists (adopt — e.g. after a mono-repo refactor). Scaffolds everything LOCALLY and prints the exact gh/git commands to publish — nothing irreversible auto-fires. Use when the CEO says "create a new project", "set up the CTO repo", "we split the mono-repo and need a CTO home", or wants the IP-separation pattern (public template = mechanism only; private <project>-cto = IP) bootstrapped.
allowed-tools: Bash(*) Read Write
argument-hint: <project> [--repos=repo1,repo2] [--adopt] [--org=<gh-org-or-user>]
---

# New Project / CTO Home: $ARGUMENTS

Scaffolds a private `<project>-cto` operating home from this template's mechanism, then
either creates new dev repos (greenfield) or registers an existing fleet (`--adopt`).
**Local-only + print-commands:** this skill writes files on disk and prints the `gh`/`git`
commands to publish — it never deletes, pushes, or creates a GitHub repo itself.

## Scaffold

```!
set -uo pipefail
[ -n "${ZSH_VERSION:-}" ] && setopt sh_word_split

ARGS="$ARGUMENTS"
PROJECT=""; REPOS=""; ADOPT=0; ORG="<your-gh-org-or-user>"
for tok in $ARGS; do
  case "$tok" in
    --repos=*) REPOS="${tok#--repos=}" ;;
    --org=*)   ORG="${tok#--org=}" ;;
    --adopt)   ADOPT=1 ;;
    --*)       echo "Unknown flag: $tok" >&2 ;;
    *)         [ -z "$PROJECT" ] && PROJECT="$tok" ;;
  esac
done

if [ -z "$PROJECT" ]; then
  echo "ERROR: usage  /new-project <project> [--repos=a,b] [--adopt] [--org=<gh-org>]"
  echo "  greenfield: /new-project acme --repos=acme-core,acme-web --org=acme-inc"
  echo "  adopt:      /new-project acme --adopt   (wires <project>-cto to repos in projects.yaml)"
  exit 1
fi

TPL=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
PARENT=$(dirname "$TPL")
HOME_DIR="$PARENT/${PROJECT}-cto"
MODE="greenfield"; [ "$ADOPT" -eq 1 ] && MODE="adopt-existing"

echo "project        : $PROJECT"
echo "mode           : $MODE"
echo "template (src) : $TPL"
echo "CTO home (dst) : $HOME_DIR"
echo "repos          : ${REPOS:-<none given>}"
echo ""

if [ -e "$HOME_DIR" ]; then
  echo "ERROR: $HOME_DIR already exists — refusing to overwrite. Remove it or pick another name."
  exit 1
fi

# --- 1. Scaffold the private CTO home from the template mechanism (local copy) ---
echo "== scaffolding CTO home =="
mkdir -p "$HOME_DIR"
rsync -a \
  --exclude='.git/' --exclude='.DS_Store' --exclude='__pycache__/' --exclude='*.pyc' \
  --exclude='.claude/settings.json' --exclude='.claude/settings.local.json' \
  --exclude='.claude/scheduled_tasks.lock' --exclude='.claude/current-session.id' \
  --exclude='.claude/*.id' --exclude='.claude/.permissions-asked' \
  --exclude='.cto/projects.yaml' --exclude='README.md' \
  "$TPL"/ "$HOME_DIR"/

# Adapt CLAUDE.md title (the genericized template's CTO-home detection already covers any -cto repo)
perl -CSD -i -pe "s/^# CTO Agent .*/# CTO Agent \x{2014} ${PROJECT}-cto (${PROJECT} fleet CTO home)/ if \$. == 1" "$HOME_DIR/CLAUDE.md"

# IP dirs (the place project intellectual property lives — kept out of the public template)
mkdir -p "$HOME_DIR/docs/roadmap/prds" "$HOME_DIR/docs/architecture/decisions" "$HOME_DIR/docs/ideation" "$HOME_DIR/docs/handoff"

cat > "$HOME_DIR/README.md" <<EOF
# ${PROJECT}-cto

Private CTO operating home for the **${PROJECT}** fleet. Holds the project's IP (PRDs,
FLEET-ADRs, strategy/research, IDEO sessions, CTO decisions) under \`docs/\`, plus a copy of
the orchestration mechanism (skills, hooks, personas, scripts, templates) and the live
\`.cto/projects.yaml\`. Run the ${PROJECT} CTO from here. This repo is PRIVATE and never
holds the public template's job — it is the IP side of the public/private split.
EOF

# --- 2. Seed .cto/projects.yaml ---
mkdir -p "$HOME_DIR/.cto"
{
  echo "# CTO Project Registry for ${PROJECT}"
  echo "# Gitignored (local filesystem paths). One entry per repo in the fleet."
  echo "projects:"
} > "$HOME_DIR/.cto/projects.yaml"

REG_REPOS="$REPOS"
# In adopt mode with no --repos, inherit the active repos from the template's own registry if present
if [ "$ADOPT" -eq 1 ] && [ -z "$REG_REPOS" ] && [ -f "$TPL/.cto/projects.yaml" ]; then
  REG_REPOS=$(grep -E '^\s*- name:' "$TPL/.cto/projects.yaml" | sed 's/.*- name:[[:space:]]*//' | paste -sd, -)
  echo "(adopt) inherited repos from template registry: $REG_REPOS"
fi

if [ -n "$REG_REPOS" ]; then
  OLDIFS="$IFS"; IFS=','
  for r in $REG_REPOS; do
    r=$(echo "$r" | tr -d '[:space:]'); [ -z "$r" ] && continue
    RPATH="$PARENT/$r"
    printf '  - name: %s\n    path: %s\n    description: TODO\n    language: TODO\n    active: true\n' "$r" "$RPATH" >> "$HOME_DIR/.cto/projects.yaml"
  done
  IFS="$OLDIFS"
else
  echo "  # - name: ${PROJECT}-core" >> "$HOME_DIR/.cto/projects.yaml"
  echo "  #   path: $PARENT/${PROJECT}-core" >> "$HOME_DIR/.cto/projects.yaml"
  echo "  #   active: true" >> "$HOME_DIR/.cto/projects.yaml"
fi
echo "  wrote $HOME_DIR/.cto/projects.yaml"

# --- 3a. Greenfield: scaffold each new dev repo locally ---
DEV_SCAFFOLD=""
if [ "$ADOPT" -eq 0 ] && [ -n "$REPOS" ]; then
  echo ""
  echo "== scaffolding dev repos (greenfield, local) =="
  OLDIFS="$IFS"; IFS=','
  for r in $REPOS; do
    r=$(echo "$r" | tr -d '[:space:]'); [ -z "$r" ] && continue
    RD="$PARENT/$r"
    if [ -e "$RD" ]; then echo "  SKIP $r (exists)"; continue; fi
    mkdir -p "$RD/.claude/hooks" "$RD/docs/sprints" "$RD/docs/architecture/decisions" "$RD/scripts"
    cp "$TPL/CLAUDE.devteam.md" "$RD/CLAUDE.md"
    cp -r "$TPL/docs/personas" "$RD/docs/personas" 2>/dev/null || true
    cp -r "$TPL/docs/sprints/_templates" "$RD/docs/sprints/_templates" 2>/dev/null || true
    cp -r "$TPL/scripts/agentic" "$RD/scripts/agentic" 2>/dev/null || true
    [ -f "$TPL/.gitignore" ] && cp "$TPL/.gitignore" "$RD/.gitignore"
    cp "$TPL/.claude/settings.permissive.json" "$RD/.claude/settings.permissive.json" 2>/dev/null || true
    [ -d "$TPL/.claude/hooks" ] && cp "$TPL/.claude/hooks/"* "$RD/.claude/hooks/" 2>/dev/null || true
    chmod +x "$RD/.claude/hooks/"*.sh 2>/dev/null || true
    # settings.json with the three dev-team session-tracking hooks already wired
    # (from settings.devteam.json.template, _comment fields stripped) so the repo
    # is tracked from its first session — /handoff also self-heals this at dispatch.
    python3 -c "import json; d=json.load(open('$TPL/.claude/settings.devteam.json.template')); d.pop('_comment',None); h=d.get('hooks',{});
[h.pop(k) for k in list(h) if k.startswith('_comment')]; open('$RD/.claude/settings.json','w').write(json.dumps(d, indent=2) + '\n')" 2>/dev/null \
      || cp "$TPL/.claude/settings.devteam.json.template" "$RD/.claude/settings.json"
    # Review engine: provisional seed only. The CEO is asked for the project's choice in
    # "Your task as CTO" below, and set-review-engine.sh then rewrites this across the CTO
    # home + every dev repo. Written through that script so the value is validated and
    # lands at the repo ROOT (resolve-review-engine.sh never reads a .claude/ copy).
    bash "$TPL/scripts/agentic/set-review-engine.sh" "$RD" "$(bash "$TPL/scripts/agentic/set-review-engine.sh" --fleet-default)" >/dev/null 2>&1
    echo "  scaffolded $RD"
    DEV_SCAFFOLD="$DEV_SCAFFOLD $r"
  done
  IFS="$OLDIFS"
fi

# --- 4. Print the publish commands (nothing irreversible ran above) ---
echo ""
echo "================================================================"
echo " SCAFFOLD COMPLETE (local only). Run these to PUBLISH:"
echo "================================================================"
echo ""
echo "# 1) CTO home — PRIVATE (holds IP):"
echo "(cd $HOME_DIR && git init && git add -A && \\"
echo "   git commit -m 'init ${PROJECT}-cto (CTO home)' && \\"
echo "   gh repo create ${ORG}/${PROJECT}-cto --private --source=. --remote=origin --push)"
echo ""
if [ "$ADOPT" -eq 0 ] && [ -n "$DEV_SCAFFOLD" ]; then
  echo "# 2) New dev repos (PRIVATE; pick visibility per your needs):"
  for r in $DEV_SCAFFOLD; do
    echo "(cd $PARENT/$r && git init && git add -A && \\"
    echo "   git commit -m 'scaffold ${r} (dev team)' && \\"
    echo "   gh repo create ${ORG}/${r} --private --source=. --remote=origin --push)"
  done
elif [ "$ADOPT" -eq 1 ]; then
  echo "# 2) ADOPT — the existing repos are registered in projects.yaml above."
  echo "#    To push the dev-team mechanism into an EXISTING repo (run per repo, review first):"
  echo "#      cp $TPL/CLAUDE.devteam.md <repo>/CLAUDE.md"
  echo "#      cp -r $TPL/docs/personas <repo>/docs/personas"
  echo "#      cp -r $TPL/docs/sprints/_templates <repo>/docs/sprints/_templates"
  echo "#      mkdir -p <repo>/.claude && cp $TPL/.claude/settings.permissive.json <repo>/.claude/"
  echo "#      printf 'subagent\\n' > <repo>/.review-engine        # repo ROOT, not .claude/"
  echo "#    (or run /new-project's dev-scaffold against a copy first to diff before committing.)"
  echo ""
  echo "#    If this project's IP currently lives in a PUBLIC repo, scrub it: move IP to ${PROJECT}-cto,"
  echo "#    then DELETE+RECREATE the public repo (force-push leaves old commits fetchable by SHA)."
fi
echo ""
echo "# 3) Then author the first PRD under $HOME_DIR/docs/roadmap/prds/ and run the CTO from ${PROJECT}-cto."
echo "MODE=$MODE HOME_DIR=$HOME_DIR"
```

## Your task as CTO

**First, settle the review engine** — a project-start choice, like the permissions posture.
Every VP review, sprint fan-out and accept-gate runs through it, so it is worth one question
now rather than a surprise at the first accept gate. Run
`bash scripts/agentic/set-review-engine.sh --menu` for the live menu, then ask via
`AskUserQuestion` (header: "Review engine"), offering:

- **kimi (recommended)** — OpenRouter `moonshotai/kimi-k2.6`. Cross-**family** reviewer, so a
  VP verdict is genuinely independent of the model that wrote the work. Metered but
  non-Anthropic (pennies per review); needs `OPENROUTER_API_KEY`.
- **subagent** — in-session Agent calls. Free, no API key, no external CLI. Same-family: Claude
  reviewing Claude, which is a weaker accept-gate.
- **handoff** — the review runs in its own interactive Claude window. Free, slowest; use when a
  review needs tools.

State the tradeoff plainly — independence versus pennies — and recommend `kimi` for any
project whose accept gates matter. Then apply the answer to the CTO home **and every
scaffolded dev repo**:

```
bash scripts/agentic/set-review-engine.sh <repo-path> <engine>    # once per repo, + the CTO home
```

Setting it on the CTO home is what makes it the project default: `push-to-repos.sh` reads that
file to seed and heal every dev repo from then on. Changing it later is the same one command.

Then summarize for the CEO. The CTO home (and, in greenfield mode, the dev repos) are
scaffolded **on disk** — nothing has been pushed or created on GitHub:

1. **Headline:** "Scaffolded `<project>-cto` (mode: greenfield|adopt-existing) — local only."
1a. **Review engine:** the chosen engine, and that it is now the project default for syncs.
2. **What's on disk:** the CTO-home path, that its CLAUDE.md is title-adapted (the `-cto`
   detection is already generic), the seeded `.cto/projects.yaml`, and (greenfield) the dev-repo dirs.
3. **The publish commands** printed above — present them as the CEO's explicit next step
   (the skill deliberately does NOT create/push repos; that's irreversible + outward-facing).
   Remind them the CTO home must be **private**.
4. **Next:** author the first PRD under `docs/roadmap/prds/`, then run the project's CTO from
   `<project>-cto`. For adopt mode, note the optional "push mechanism into existing repos" steps
   and (if IP leaked into a public repo) the scrub-and-recreate remediation.

Sign as: — CTO
