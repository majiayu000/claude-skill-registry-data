---
name: Qupdate
user_invocable: true
description: 'Use for "update plugin", "upgrade", "update qe", "update codex", or "codex plugin". Updates marketplace metadata/cache, framework files, installed Codex assets, and the bridge for the current install.'
allowed-tools: "Bash(claude plugin:*), Bash(npm:*), Bash(node:*), Bash(git fetch:*), Bash(git show:*), Bash(git pull:*), Bash(git -C:*)"
invocation_trigger: When the framework, its Codex assets, or the codex-plugin-cc bridge need updating.
recommendedModel: haiku
---

# Qupdate - One-Command Update (Marketplace + Framework + Codex bridge)

## Role
Single entry point that brings every QE update target to latest:

| # | Target | What it covers |
|---|--------|----------------|
| A | QE marketplace metadata/cache | marketplace checkout, `plugin.json`, `marketplace.json`, Claude plugin cache metadata |
| B | QE Framework body → Claude (`~/.claude`) | skills, agents, hooks, scripts |
| C | QE Framework body → Codex (`~/.codex`) | QE Codex asset/hook fences via `install.js` |
| D | codex-plugin-cc bridge plugin | Codex engine routing bridge (separate plugin) |

B+C come from the framework installer. A is the Claude plugin marketplace/download layer
that decides which plugin metadata and cache version Claude sees. D is the Codex bridge
plugin managed through `claude plugin`. This skill runs A first, then B/C, then D.

## Execution Procedure

### Step 0: Pre-flight — is the latest release reachable on `origin`?
The tarball path runs `git pull`, which only helps if the newest release was pushed to
`origin`. Publishing a release may leave a freshly cut release
only in the local checkout (commit + tag present, `origin` behind).

```bash
git fetch origin --tags --quiet
LOCAL=$(node -p "require('./package.json').version" 2>/dev/null)
REMOTE=$(git show origin/main:package.json 2>/dev/null | node -p "JSON.parse(require('fs').readFileSync(0)).version" 2>/dev/null)
echo "local=$LOCAL  origin=$REMOTE"
```

- `local` **ahead of** `origin` (unpushed release) → `git pull` brings nothing. Skip the
  tarball path and use the repository-local install (path 3) to sync already-released local
  assets. Remind the user that `git push origin main --tags` is still needed to publish.
- `origin` ahead or equal → tarball/native paths are safe.

### Step 1: Refresh QE marketplace metadata and plugin cache (target A)
Qupdate must align marketplace metadata before installing body assets. Do not manually edit
`.claude-plugin/plugin.json` or `.claude-plugin/marketplace.json`; version fields are owned by
the release/admin workflow. Refresh from git/Claude plugin commands, then verify.

1. If running inside the QE framework checkout, verify source metadata first:

   ```bash
   node scripts/check-metadata-drift.mjs || node scripts/sync-metadata.mjs
   node scripts/check-metadata-drift.mjs
   ```

   `sync-metadata.mjs` mirrors `package.json` into `plugin.json` and the nested
   `marketplace.json` qe-framework entry. If it changes files, report them as source changes
   that still need the normal QE commit/release path.

2. If the local Claude marketplace checkout exists, fast-forward it:

   ```bash
   MP="$HOME/.claude/plugins/marketplaces/inho-team-qe-framework"
   if [ -d "$MP/.git" ]; then
     git -C "$MP" fetch origin --tags --quiet
     git -C "$MP" pull --ff-only
   fi
   ```

   If this fails because the marketplace checkout has local changes, stop and report the dirty
   files. Do not overwrite them.

3. Refresh the Claude plugin download/cache metadata when QE is installed as a marketplace plugin:

   ```bash
   claude plugin update qe-framework@inho-team-qe-framework
   ```

   This step is now required for plugin-mode installs when the latest release is reachable on
   `origin`. It refreshes the marketplace plugin cache metadata, but still does not replace all
   installed body assets; continue with Step 2.

4. Verify marketplace metadata against the expected release version:

   ```bash
   node -e "const fs=require('fs'); const path=require('path'); const home=process.env.HOME; const expected=JSON.parse(fs.readFileSync('package.json','utf8')).version; const files=[path.join(home,'.claude/plugins/marketplaces/inho-team-qe-framework/.claude-plugin/plugin.json'),path.join(home,'.claude/plugins/marketplaces/inho-team-qe-framework/.claude-plugin/marketplace.json')]; for (const f of files) { if (!fs.existsSync(f)) { console.log('missing '+f); continue; } const j=JSON.parse(fs.readFileSync(f,'utf8')); const got=j.version || (j.plugins||[]).find(p=>p.name==='qe-framework')?.version || 'unknown'; console.log(`${f}: ${got} ${got===expected?'OK':`!= ${expected}`}`); }"
   ```

   Report any mismatch. If Step 0 shows the release exists only in the local checkout and is not
   on `origin/main`, marketplace/cache metadata cannot honestly match the local version yet; use
   Step 2 path 3 for local asset sync and tell the user to publish the release first.

### Step 2: Update the QE Framework body (targets B + C)
Choose exactly one path:

1. **Native plugin update** — only acceptable as a metadata/download pre-step when QE is
   installed as a Claude marketplace plugin and the latest release is reachable on `origin`.
   It is not a complete QE update by itself.

   ```bash
   claude plugin update qe-framework
   ```

   Note: native update refreshes the marketplace plugin cache only. It does **not** mirror the
   absolute-path `~/.claude/scripts` copy or sync Codex assets (C), and it must not be the
   final step when the user expects all installed plugin code/values to be replaced.
   Step 1 already runs this for plugin-mode installs; always follow with path 2 or 3.

2. **Checked-out release tarball install** — covers B + C in one shot when the release is on
   `origin`. The tarball filename is derived from `package.json` — never hardcode a version.
   This is a full replacement sync: stale QE plugin-cache files are pruned and legacy Codex
   QE assets are purged before current assets are installed.

   ```bash
   git pull
   VER=$(node -p "require('./package.json').version")
   npm pack --cache /tmp/qe-npm-cache
   npm install -g "./inho-team-qe-framework-${VER}.tgz"
   qe-framework-install
   ```

3. **Repository-local direct install** — covers B + C without rebuilding the global tarball.
   The correct fallback when Step 0 shows an unpushed local release, or when the user is
   already inside a QE checkout and needs installed assets to exactly match this checkout.
   This is also a full replacement sync.

   ```bash
   node install.js
   ```

**Selection rule:**
- Local checkout **ahead of** `origin` (unpushed release) → path 3 (`node install.js`).
- Already inside a QE checkout, asset sync only → path 3.
- Plugin-mode install, no Codex/abs-script dependency → path 1 may be used first, but must
  be followed by path 2 or 3 for full replacement.
- Otherwise → path 2 (tarball, covers B + C).
- Do not recommend `npm update -g @inho-team/qe-framework` unless the package is published to npm.

### Step 3: Update the codex-plugin-cc bridge (target D)
The Codex bridge is a **separate** plugin (`codex@openai-codex`), not part of the QE body.

1. Read current status with `getCodexPluginInfo()` from `scripts/lib/codex_bridge.mjs` (reads
   `~/.claude/plugins/installed_plugins.json`). Display:

   ```
   Codex bridge (codex-plugin-cc)
     Installed: {yes / no}
     Version:   {version or n/a}
     Path:      {installPath or n/a}
     Commit:    {sha or n/a}
   ```

2. Check latest available via `claude plugin marketplace search codex` or the marketplace
   cache at `~/.claude/plugins/marketplaces/`. Compare installed vs latest.

3. Use `AskUserQuestion` to confirm before changing anything:
   - **Not installed** → Option: Install (`claude plugin install codex@openai-codex`) /
     Skip ("Codex is optional. All SIVS stages will use Claude.").
   - **Update available** → Option: Update (`claude plugin install codex@openai-codex`
     reinstalls to latest) / Skip ("Staying on v{current}.").
   - **Up to date** → "No action needed."

### Step 4: Verify
- Re-check QE marketplace metadata/cache version:

  ```bash
  node -e "const fs=require('fs'); const path=require('path'); const home=process.env.HOME; const expected=JSON.parse(fs.readFileSync('package.json','utf8')).version; const paths=[path.join(home,'.claude/plugins/marketplaces/inho-team-qe-framework/.claude-plugin/plugin.json'),path.join(home,'.claude/plugins/marketplaces/inho-team-qe-framework/.claude-plugin/marketplace.json')]; let ok=true; for (const p of paths) { if (!fs.existsSync(p)) continue; const j=JSON.parse(fs.readFileSync(p,'utf8')); const got=j.version || (j.plugins||[]).find(x=>x.name==='qe-framework')?.version; if (got !== expected) { ok=false; console.log(`MISMATCH ${p}: ${got} != ${expected}`); } else console.log(`OK ${p}: ${got}`); } process.exit(ok?0:1)"
  ```

- If the Codex bridge changed, re-read `installed_plugins.json` to confirm the new version.
- Optionally validate SIVS config from the plugin root (the `qe:validate` npm script lives
  only in the framework repo, not the target project):

  ```bash
  node -e "(async()=>{const {pathToFileURL}=await import('url');const {join}=await import('path');const fs=await import('fs');const home=process.env.HOME||process.env.USERPROFILE||'';const _cr=join(home,'.claude','plugins','cache','inho-team-qe-framework','qe-framework');const _cand=[process.env.CLAUDE_PLUGIN_ROOT,join(home,'.claude','plugins','marketplaces','inho-team-qe-framework')];if(fs.existsSync(_cr))for(const v of fs.readdirSync(_cr).sort().reverse())_cand.push(join(_cr,v));_cand.push(join(home,'.claude'));const base=_cand.find(b=>b&&fs.existsSync(join(b,'hooks','scripts','lib','session-resolver.mjs')))||join(home,'.claude');await import(pathToFileURL(join(base,'scripts','validate_svs_config.mjs')).href)})()"
  ```

### Step 5: Report result
Report per target:
- A — QE marketplace metadata/cache: updated / unchanged / mismatch (with version evidence)
- B — Claude framework assets: updated / unchanged (which path)
- C — Codex framework assets: updated / unchanged
- D — codex-plugin-cc bridge: installed / updated / up-to-date / skipped
- whether Claude/Codex should be restarted

## Will
- Refresh and verify QE marketplace metadata/cache before body asset sync
- Update the QE Framework body for both Claude and Codex via the correct installer path
- Check, install, or update the codex-plugin-cc bridge on user confirmation
- Report per-target results and the next restart step

## Will Not
- Modify any project files
- Modify SIVS engine configuration
- Manually write marketplace/plugin version fields outside the release/admin workflow
- Force-install the Codex bridge without user confirmation
- Install or update unrelated MCP server packages
- Run without user invocation
