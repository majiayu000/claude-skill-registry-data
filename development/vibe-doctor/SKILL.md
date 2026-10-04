---
name: vibe-doctor
description: >
  Environment health check and auto-remediation for vibe-* projects.
  Checks node_modules vs package.json drift, nested .git directories,
  Tailwind and shadcn version mismatches, dotenv load order, Vite HMR
  WebSocket config, husky hook permissions, ESLint config validity,
  TypeScript path resolution, and missing dependencies in generated code.
  Auto-remediates where safe. Flags where human action is needed.
  Outputs a health report and writes vibe/.doctor-last-run for vibe-progress.
  Triggers on "doctor:", "check environment", "fix my environment",
  "env check", "why won't my app start", "something is broken at startup",
  "app won't start". Also invoked by vibe-fix-bug when an environment
  bug is detected in triage. Run manually or via PreToolUse hook.
---

# Vibe Doctor Skill

Environment health check and auto-remediation.
Catches the failure modes that compound across sessions before they waste build time.
Runs in 20-40 seconds. Auto-fixes what it can. Flags what it cannot.

**Always run in Plan Mode for diagnosis. Auto-exits to execute remediations.**

---

## Why this skill exists

The most common session-wasting pattern in vibe-* projects:
session starts → command fails → agent investigates → discovers env problem →
spends 20 minutes fixing config → never gets to the actual work.

These failures are all checkable in 30 seconds:
- node_modules missing or stale (package.json changed since last install)
- Tailwind v3 project running v4 syntax from generated code
- dotenv loaded after code that reads process.env
- Vite HMR WebSocket not configured for dev server
- husky hooks not executable (no chmod)
- Nested .git directory breaking git operations
- TypeScript paths not matching folder structure
- Missing package referenced in generated import

Check once at session start. Fix everything. Build with confidence.

---

## Setting up the PreToolUse hook (recommended)

After running doctor: for the first time, it offers to install itself as a hook.
Or add manually to `.claude/settings.json` at project root:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "[ -f vibe/.doctor-last-run ] && [ $(( $(date +%s) - $(cat vibe/.doctor-last-run 2>/dev/null || echo 0) )) -lt 3600 ] || echo 'DOCTOR: Run doctor: to check environment health'"
      }]
    }]
  }
}
```

This surfaces a reminder if doctor: hasn't run in the last hour.
For full auto-run on every session, vibe-mode: autonomous enables this automatically.

---

## Step 0 — Pre-flight

```bash
# Detect project type
ls package.json 2>/dev/null && echo "NODE=true" || echo "NODE=false"
ls pyproject.toml 2>/dev/null || ls requirements.txt 2>/dev/null && echo "PYTHON=true" || echo "PYTHON=false"
ls pubspec.yaml 2>/dev/null && echo "FLUTTER=true" || echo "FLUTTER=false"
ls vibe/ 2>/dev/null && echo "VIBE=true" || echo "VIBE=false"
```

Read `references/CHECKS.md` for the full check implementations.

---

## Step 1 — Run all checks

Run all checks in parallel where possible. Collect results.
Do not stop on first failure — run everything, report all at once.

### Check 1 — node_modules integrity

```bash
# Check if node_modules exists
if [ ! -d "node_modules" ]; then
  echo "FAIL:node_modules missing"
  exit 0
fi

# Check if package.json has changed since last install
if [ package.json -nt node_modules ]; then
  echo "FAIL:package.json newer than node_modules — run npm install"
else
  echo "PASS:node_modules"
fi

# Check for packages in package.json not in node_modules
node -e "
const pkg = require('./package.json');
const deps = {...(pkg.dependencies||{}), ...(pkg.devDependencies||{})};
const missing = Object.keys(deps).filter(d => {
  try { require.resolve(d, {paths: [process.cwd()]}); return false; }
  catch { return true; }
});
if (missing.length) console.log('FAIL:missing packages: ' + missing.join(', '));
else console.log('PASS:all packages resolvable');
" 2>/dev/null || echo "SKIP:node check requires node"
```

### Check 2 — Nested .git directories

```bash
# Find nested .git dirs (common cause of submodule confusion)
nested=$(find . -name ".git" -not -path "./.git" -not -path "*/node_modules/*" -maxdepth 4 2>/dev/null)
if [ -n "$nested" ]; then
  echo "FAIL:nested .git found: $nested"
else
  echo "PASS:no nested .git"
fi
```

### Check 3 — Tailwind version consistency

```bash
if [ -f "tailwind.config.js" ] || [ -f "tailwind.config.ts" ]; then
  # Get installed version
  tw_version=$(node -e "console.log(require('./node_modules/tailwindcss/package.json').version)" 2>/dev/null)
  
  if [ -z "$tw_version" ]; then
    echo "SKIP:tailwind not installed"
  else
    major=$(echo $tw_version | cut -d. -f1)
    
    # Check for v4 syntax in a v3 project
    if [ "$major" = "3" ]; then
      v4_syntax=$(grep -r "@import \"tailwindcss\"" src/ 2>/dev/null | head -3)
      if [ -n "$v4_syntax" ]; then
        echo "FAIL:Tailwind v3 installed but v4 import syntax found in src/"
      else
        echo "PASS:Tailwind v$tw_version consistent"
      fi
    fi
    
    # Check for v3 config in a v4 project
    if [ "$major" = "4" ]; then
      v3_config=$(grep -l "module.exports" tailwind.config* 2>/dev/null)
      if [ -n "$v3_config" ]; then
        echo "FAIL:Tailwind v4 installed but v3 config syntax (module.exports) found"
      else
        echo "PASS:Tailwind v$tw_version consistent"
      fi
    fi
  fi
else
  echo "SKIP:no tailwind config"
fi
```

### Check 4 — dotenv load order

```bash
if [ -f ".env" ] || [ -f ".env.local" ]; then
  # Find entry point
  entry=$(cat package.json 2>/dev/null | node -e "
    const p = JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'));
    const main = p.main || (p.scripts && p.scripts.start && p.scripts.start.split(' ').pop());
    console.log(main || 'src/index.ts');
  " 2>/dev/null)
  
  if [ -n "$entry" ] && [ -f "$entry" ]; then
    # Check if dotenv is configured before any process.env usage
    dotenv_line=$(grep -n "dotenv\|config()" "$entry" 2>/dev/null | head -1 | cut -d: -f1)
    env_line=$(grep -n "process\.env\." "$entry" 2>/dev/null | head -1 | cut -d: -f1)
    
    if [ -n "$dotenv_line" ] && [ -n "$env_line" ]; then
      if [ "$dotenv_line" -gt "$env_line" ]; then
        echo "FAIL:dotenv loaded at line $dotenv_line but process.env used at line $env_line in $entry"
      else
        echo "PASS:dotenv loads before process.env usage"
      fi
    else
      echo "SKIP:could not determine dotenv order"
    fi
  fi
else
  echo "SKIP:no .env file"
fi
```

### Check 5 — Vite HMR WebSocket

```bash
if [ -f "vite.config.ts" ] || [ -f "vite.config.js" ]; then
  # Check if server config exists with HMR settings
  has_server=$(grep -l "server:" vite.config* 2>/dev/null)
  if [ -n "$has_server" ]; then
    has_hmr=$(grep "hmr:" vite.config* 2>/dev/null)
    if [ -z "$has_hmr" ]; then
      echo "WARN:Vite server config exists but no explicit HMR config — WebSocket issues possible in some environments"
    else
      echo "PASS:Vite HMR configured"
    fi
  else
    echo "INFO:Vite config has no server section — default HMR applies"
  fi
else
  echo "SKIP:no vite config"
fi
```

### Check 6 — Husky hook permissions

```bash
if [ -d ".husky" ]; then
  non_exec=$(find .husky -type f ! -name "_" ! -name "*.sample" ! -executable 2>/dev/null)
  if [ -n "$non_exec" ]; then
    echo "FAIL:husky hooks not executable: $non_exec"
  else
    echo "PASS:husky hooks executable"
  fi
else
  echo "SKIP:no .husky directory"
fi
```

### Check 7 — TypeScript path resolution

```bash
if [ -f "tsconfig.json" ]; then
  # Check for path aliases that don't match actual folders
  paths=$(node -e "
    const ts = JSON.parse(require('fs').readFileSync('tsconfig.json','utf8').replace(/\/\/.*/g,''));
    const paths = (ts.compilerOptions && ts.compilerOptions.paths) || {};
    const baseUrl = (ts.compilerOptions && ts.compilerOptions.baseUrl) || '.';
    Object.entries(paths).forEach(([alias, targets]) => {
      targets.forEach(target => {
        const resolved = target.replace('*', '').replace(/\/$/, '');
        const fs = require('fs');
        if (!fs.existsSync(resolved)) {
          console.log('FAIL:tsconfig path alias ' + alias + ' points to missing folder: ' + resolved);
        }
      });
    });
    console.log('PASS:tsconfig paths resolved');
  " 2>/dev/null)
  echo "$paths" | head -5
else
  echo "SKIP:no tsconfig.json"
fi
```

### Check 8 — ESLint config validity

```bash
if ls eslint.config* .eslintrc* 2>/dev/null | head -1 | grep -q .; then
  # Try parsing the config
  result=$(npx eslint --print-config src/index.ts 2>&1 | head -3)
  if echo "$result" | grep -qi "error\|cannot find\|invalid"; then
    echo "FAIL:ESLint config error: $(echo $result | head -c 100)"
  else
    echo "PASS:ESLint config valid"
  fi
else
  echo "SKIP:no ESLint config"
fi
```

### Check 9 — Git state

```bash
# Check git is initialised
git status 2>/dev/null || { echo "WARN:not a git repository"; exit 0; }

# Check for uncommitted changes that might affect build
staged=$(git diff --staged --name-only 2>/dev/null | wc -l)
if [ "$staged" -gt 20 ]; then
  echo "WARN:$staged staged files — consider committing before long session"
else
  echo "PASS:git state clean"
fi

# Check current branch
branch=$(git branch --show-current 2>/dev/null)
echo "INFO:on branch $branch"
```

### Check 10 — vibe/ folder integrity (if vibe project)

```bash
if [ -d "vibe" ]; then
  missing=""
  [ ! -f "vibe/TASKS.md" ] && missing="$missing TASKS.md"
  [ ! -f "vibe/SPEC.md" ] && missing="$missing SPEC.md"
  [ ! -f "CLAUDE.md" ] && missing="$missing CLAUDE.md(root)"
  
  if [ -n "$missing" ]; then
    echo "WARN:vibe/ exists but missing:$missing"
  else
    echo "PASS:vibe/ folder complete"
  fi
else
  echo "INFO:not a vibe project (no vibe/ folder)"
fi
```

---

## Step 2 — Triage results

Categorise each result:

```
PASS    — no action needed
FAIL    — auto-remediate if safe, flag if not
WARN    — surface to user, suggest fix
INFO    — informational, no action
SKIP    — check not applicable to this project
```

**Auto-remediation safe list** (fix without asking):
- node_modules **missing** → `npm install` (nothing to lose)
- husky hooks not executable → `chmod +x .husky/*`
- node_modules **stale but present** → **confirm first** (a large reinstall takes
  minutes — this matches the Absolute rule below, not a silent auto-fix)

**Flag for human action** (show exact command, do not run):
- Tailwind version mismatch → show the specific file and line
- dotenv order → show the two lines that need swapping
- Nested .git → show `git rm --cached [path] && rm -rf [path]`
- TypeScript path alias → show which folder needs creating
- ESLint config → show the parse error

**When a symptom has more than one possible cause, list the candidates before
remediating.** The checks above are deterministic, but a reported symptom
("build fails", "HMR won't connect", "types don't resolve") often maps to several
of them at once. Don't fix the first check that looks related and declare victory —
name the 2–3 checks that could produce this symptom, confirm which one actually
fires from its check output, and remediate that. A fix applied to the wrong cause
leaves the real one in place and hides it.

---

## Step 3 — Auto-remediate safe fixes

For each FAIL with safe remediation:

```bash
# node_modules missing or stale
npm install

# husky hooks not executable
chmod +x .husky/*
git config core.hooksPath .husky

# Vite HMR — add config if missing and project uses Railway/Nixpacks
# (only if package.json has a Railway-style deploy config)
```

After each remediation — verify it worked:
```bash
# Re-run the specific check that failed
# Report: "Fixed: [what was fixed]"
```

---

## Step 4 — Output health report

```
DOCTOR — [project name] — [date] [time]
────────────────────────────────────────────
✅ node_modules      — all packages installed and resolvable
✅ .git structure    — no nested repositories
⚠️  Vite HMR         — no explicit HMR config (may cause issues on Railway)
   Fix: add server.hmr config to vite.config.ts
✅ dotenv order      — loaded before process.env usage
✅ husky hooks       — all executable
✅ TypeScript paths  — all aliases resolve
✅ ESLint config     — valid
✅ Tailwind          — v3, consistent syntax
✅ git state         — clean, on branch main
✅ vibe/ folder      — TASKS.md, SPEC.md, CLAUDE.md present

AUTO-FIXED:
  ✅ husky hooks — chmod +x applied to 3 hooks

NEEDS ATTENTION:
  ⚠️  [description] — [exact command to fix]

ENVIRONMENT: [HEALTHY / WARNINGS / NEEDS FIXES]
────────────────────────────────────────────
```

---

## Step 5 — Write .doctor-last-run

```bash
mkdir -p vibe
date +%s > vibe/.doctor-last-run
```

This allows vibe-progress to show env health status in the dashboard
and the PreToolUse hook to know when doctor last ran.

---

## Step 6 — Offer hook installation

If `.claude/settings.json` does not already have a doctor hook:

> "Doctor complete. Want me to add a lint+typecheck hook (runs after edits) to
> `.claude/settings.json` so this runs automatically? (y/n)"

If yes — **merge** the hook into `.claude/settings.json` (never overwrite it — the
file may already hold `permissions`, `env`, or hooks from vibe-review). Prefer the
`update-config` skill if it is available in the session; otherwise read-merge-write,
and no-op if an equivalent lint hook already exists:
```bash
LINT_CMD='npm run lint --silent 2>&1 | tail -5 || true'   # or the project's linter
mkdir -p .claude
python3 - "$LINT_CMD" << 'PY'
import json, sys, pathlib
lint_cmd = sys.argv[1]
p = pathlib.Path(".claude/settings.json")
cfg = {}
if p.exists() and p.read_text().strip():
    try:
        cfg = json.loads(p.read_text())          # preserve existing config
    except json.JSONDecodeError:
        print("settings.json is not valid JSON — leaving it untouched"); sys.exit(0)
post = cfg.setdefault("hooks", {}).setdefault("PostToolUse", [])
already = any("lint" in h.get("command","") or "tsc" in h.get("command","") or "ruff" in h.get("command","")
             for entry in post for h in entry.get("hooks", []))
if not already:
    post.append({"matcher": "Edit|Write", "hooks": [{"type": "command", "command": lint_cmd}]})
    p.write_text(json.dumps(cfg, indent=2) + "\n"); print("Lint hook merged")
else:
    print("A lint/typecheck PostToolUse hook already exists — no change")
PY
```

This is the same safe merge vibe-review uses — the two skills must not clobber each
other's `.claude/settings.json`.

---

## Called by vibe-fix-bug

When vibe-fix-bug detects an environment bug in triage (Step 1),
it calls vibe-doctor automatically:

```
vibe-fix-bug detected: environment bug
Running doctor: to diagnose before bug workflow...
[doctor output]
If environment is fixed and app starts → close bug, no BUG_SPEC needed.
If code bug remains → continue with vibe-fix-bug significant path.
```

---

## Absolute rules

**Never read .env files.** Skip any check that would require reading secret values.
Only check that .env exists, not its contents.

**Never run npm install without confirming** if node_modules exists and is large.
Large reinstalls take minutes. Confirm first: "node_modules exists but is stale.
Run npm install? (y/n)"

**Never git rm or rm -rf without explicit user confirmation.**
Show the command. Explain what it does. Wait for yes.

**All checks are read-only except the safe remediations list.**
If in doubt — flag, don't fix.

**If the project is not Node — skip Node checks gracefully.**
No errors for missing package.json on a Python project.
Detect project type in Step 0 and skip inapplicable checks.
