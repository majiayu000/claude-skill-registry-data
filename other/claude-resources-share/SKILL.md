---
name: claude-resources-share
description: "Share Claude Code resources (memories, settings, skills, hooks, etc.) across projects via the centralized claude-settings repo. Use when: (1) User says 'share claude resource', 'sync settings', or 'export to claude-settings', (2) User wants to copy .claude/* files to the central repo, (3) Reusing memory or skills across projects, (4) Backing up local Claude config to the global repo."
argument-hint: "[-a|--auto]"
---

# Claude Resources Share

One-direction publish from `$HOME/.claude/` (private) to `$HOME/repos/p/claude-resources` (public).

## Auto mode

If the user passes `-a` or `--auto` (e.g. `/claude-resources-share -a`, `/claude-resources-share --auto`, or wording like "auto", "if no problems do copy and push", "do it all if clean"), enable **auto mode**:

- **Step 1**: still run the scan, but if findings are clean (no HIGH/MEDIUM priority issues per `/purge-private-info`), skip the user-confirmation gate and proceed automatically. If findings are NOT clean, stop and report — do not auto-proceed.
- **Step 6**: skip the choice prompt and run `/co` with push (option 1) automatically.

In normal mode (no flag), follow the original gates: ask for confirmation after the scan and ask which commit option to use.

## Paths

- **Source**: `$HOME/.claude/`
- **Target**: `$HOME/repos/p/claude-resources`

## Directories to copy

| Source | Target |
|--------|--------|
| `$HOME/.claude/commands/` | `commands/` |
| `$HOME/.claude/skills/` | `skills/` |
| `$HOME/.claude/agents/` | `agents/` |
| `$HOME/.claude/hooks/` | `hooks/` |
| `$HOME/.claude/scripts/` | `scripts/` |
| `$HOME/.claude/web/` | `web/` |
| `$HOME/.claude/CLAUDE.md` | `CLAUDE.md` |

## Excludes (apply to all rsync operations)

- `node_modules/`
- `.claude/` (stray nested config dirs inside subtrees, e.g. `skills/.claude/`)
- `.docusaurus/`
- `build/`
- `dist/`
- `__pycache__/`
- `.DS_Store`
- `*.pyc`
- `.cache/`
- `pnpm-lock.yaml`
- `package-lock.json`
- `target/`

## Symlinks

Skip symlinks during copy. Symlinks in `$HOME/.claude/skills/` typically point to project-local repos that do not exist on a fresh machine, so dereferencing or preserving them in the public bundle would break the install. The rsync flag `--no-links` skips them entirely.

## Plugin manifests (preserved)

The public repo contains `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json` so users can install the bundle via `/plugin marketplace add takazudo/claude-resources`. These files live ONLY in the public repo (not in `$HOME/.claude/`), and Step 3's cleanup loop must NOT delete `.claude-plugin/`.

## Workflow

### Step 1: Scan for private info

Invoke the `/purge-private-info` command, targeting the source directories listed above. Scan file contents for:

- API keys, tokens, passwords, webhook keys
- Client/corporate names that appear to be real clients
- Personal SNS accounts (other than the repo owner's)
- Hardcoded absolute paths containing usernames (e.g., `$HOME/`)

Present all findings to the user. **Do NOT proceed until the user explicitly confirms** there are no problems or that findings are acceptable.

In **auto mode** (`-a` / `--auto`): if the scan reports no HIGH/MEDIUM priority findings (clean result), skip the confirmation gate and proceed to Step 2. If anything is flagged, stop and report — auto mode never auto-confirms a non-clean scan.

### Step 2: Prepare target directory and pull latest

```bash
# Create target if it doesn't exist
mkdir -p $HOME/repos/p/claude-resources
```

If the target has a `.git/` directory, pull latest to avoid conflicts:

```bash
cd $HOME/repos/p/claude-resources
git pull --rebase
```

If not a git repo, the user should initialize it separately.

### Step 3: Remove old content and fresh copy

First, remove all old content in the target (preserving `.git/`, `.gitignore`, `README.md`, `LICENSE`):

```bash
# Remove previous copies (but preserve git and repo meta files)
cd $HOME/repos/p/claude-resources
for dir in commands skills agents hooks scripts web; do
  rm -rf "./$dir"
done
rm -f ./CLAUDE.md
```

Then copy fresh from source using rsync. **IMPORTANT**: Pass each `--exclude` flag separately — do NOT store them in a shell variable, as variable expansion breaks glob patterns like `*.pyc`. The `--no-links` flag is critical: it skips symlinked skills/commands/agents that point to project-local repos.

```bash
SRC="$HOME/.claude"
DST="$HOME/repos/p/claude-resources"

for dir in commands skills agents hooks scripts web; do
  rsync -av --no-links \
    --exclude=node_modules \
    --exclude=.claude \
    --exclude=.docusaurus \
    --exclude=build \
    --exclude=dist \
    --exclude=__pycache__ \
    --exclude=.DS_Store \
    --exclude='*.pyc' \
    --exclude=.cache \
    --exclude=pnpm-lock.yaml \
    --exclude=package-lock.json \
    --exclude=target \
    "$SRC/$dir/" "$DST/$dir/"
done
cp "$SRC/CLAUDE.md" "$DST/CLAUDE.md"
```

### Step 4: Verify and clean

After copying, verify no excluded artifacts leaked through and confirm the plugin manifests are still in place:

```bash
DST="$HOME/repos/p/claude-resources"

# Check for leaked node_modules
leaked=$(find "$DST" -name node_modules -type d 2>/dev/null)
if [ -n "$leaked" ]; then
  echo "WARNING: Leaked node_modules found, removing:"
  echo "$leaked"
  find "$DST" -name node_modules -type d -exec rm -rf {} + 2>/dev/null
fi

# Clean .DS_Store files
find "$DST" -name .DS_Store -delete 2>/dev/null

# Sanity check: plugin manifests must exist for marketplace install to work
for f in .claude-plugin/marketplace.json .claude-plugin/plugin.json; do
  if [ ! -f "$DST/$f" ]; then
    echo "ERROR: Missing $f -- marketplace install will fail. Restore before pushing."
  fi
done

# Sanity check: no symlinks should have leaked through
leaked_links=$(find "$DST" -type l 2>/dev/null)
if [ -n "$leaked_links" ]; then
  echo "WARNING: Symlinks leaked through (should be skipped via --no-links):"
  echo "$leaked_links"
  find "$DST" -type l -delete 2>/dev/null
fi
```

### Step 5: Summary

Report file counts per directory:

```bash
DST="$HOME/repos/p/claude-resources"
for dir in commands skills agents hooks scripts web; do
  echo "$dir: $(find "$DST/$dir" -type f | wc -l) files"
done
echo "CLAUDE.md: 1 file"
```

### Step 6: Commit and push

**Normal mode**: Ask the user whether they want to commit and push the changes to the target repo. **Do NOT auto-commit or auto-push.** Present the options:

1. Commit and push
2. Commit only (no push)
3. Skip (leave changes uncommitted)

If the user chooses to commit, use the `/co` skill to commit inside the target repo directory. If they also want to push, push after committing.

**Auto mode** (`-a` / `--auto`): skip the prompt. Run `/co` inside the target repo directory and push (equivalent to option 1) without asking. Report the commit and push result back to the user.

## Scan whitelist

The following items are known and acceptable — do NOT flag them during the Step 1 scan:

- IFTTT webhook event names in `hooks/notify-ifttt.sh` (the key itself is in an env var)
- References to "CodeGrid", "esa", repo names like `takazudo-codegrid-writing`, `takazudo-esa-writing` in skills/agents (publicly known authorship)
- `$HOME/repos/w/` and `$HOME/repos/p/` directory structure references (personal convention, no secrets)
- Work-org/employer names (`pxgrid`, `SAISONCARD`) appearing only as "never touch" exclusions or account-scope notes, e.g. in `skills/gm-clean/SKILL.md` and `skills/db/references/env-secrets.md` (accepted; do not flag or block auto mode)
- The repo owner's own email/username (`takazudo@gmail.com`, `takazudo`)

## Important rules

- **Never copy from public to private.** This is strictly one-direction.
- **Never skip Step 1.** The safety scan is mandatory every time.
- **Never auto-confirm a non-clean scan.** In auto mode, only proceed when the scan is fully clean; any HIGH/MEDIUM finding stops the flow and requires user input. In normal mode, always wait for explicit user approval after the scan.
- **Never store rsync excludes in a shell variable.** Pass each `--exclude` flag inline to avoid glob expansion issues.
- **Never delete `.claude-plugin/`** during cleanup. Step 3 only removes `commands/`, `skills/`, `agents/`, `hooks/`, `scripts/`, `web/`, and `CLAUDE.md` — the plugin manifests are public-repo-only files and must persist across shares.
- **Never include symlinks.** Use `--no-links` in rsync. Symlinked skills/commands/agents point to project-local repos that do not exist on a fresh machine and would break installs from the marketplace.
