---
name: publish-package-cicd
description: CI/CD publishing workflow for npm packages using Changesets + npm Trusted Publishers (OIDC). Use when setting up automated npm publishing for monorepos, configuring GitHub Actions for releases, troubleshooting workspace:* protocol resolution issues, fixing "Cannot find module" errors in published packages, or debugging npm OIDC authentication. Covers Bun + Turborepo + Changesets + npm Trusted Publishers with workspace protocol resolution.
---

# Publish Package CI/CD

Automated npm publishing for Bun monorepos using Changesets + npm Trusted Publishers (OIDC). No npm tokens needed - GitHub Actions authenticates via OIDC.

## Core Workflow

### 1. Create Changeset (Manual File Creation)

**CRITICAL: Never run `bunx changeset` interactively.** Create changeset files manually to avoid the interactive CLI:

```bash
cat > .changeset/your-change-name.md << 'EOF'
---
"package-name": patch
---

Description of the change
EOF
```

**Version bump types:**
- `patch` - Bug fixes, minor updates (0.0.x)
- `minor` - New features, backwards compatible (0.x.0)
- `major` - Breaking changes (x.0.0)

### 2. Commit and Push

```bash
git add .changeset/your-change-name.md
git commit -m "feat: your feature description"
git push origin main
```

### 3. Automated Release Flow

1. **Changesets Action** (`.github/workflows/ci.yml`) detects changeset file
2. Creates/updates "chore: release packages" PR with version bumps + CHANGELOG
3. **On PR merge** → triggers publish workflow (`.github/workflows/publish.yml`)
4. Publishes to npm via OIDC (no npm token)

## Trusted Publishers (OIDC) Setup

### Initial Package Setup (One-Time)

For each package to publish:

1. **Publish v0.1.0 manually:**
   ```bash
   cd packages/your-package
   npm publish --access public
   ```

2. **Configure Trusted Publisher:**
   - Go to https://www.npmjs.com/package/your-package/access
   - Click "Trusted Publishers" → "Add"
   - Fill in:
     - Organization: `your-github-org`
     - Repository: `your-repo-name`
     - Workflow: `publish.yml`
   - Save

3. **Future releases:** Fully automated via GitHub Actions

### How OIDC Works

- No `NPM_TOKEN` secret required
- GitHub Actions has `id-token: write` permission
- npm packages configured with Trusted Publisher pointing to repo + workflow
- npm CLI 11.5.1+ auto-detects OIDC environment
- Provenance attestations generated automatically

## workspace:* Protocol Resolution

**Problem:** `workspace:*` in package.json dependencies doesn't resolve during `npm publish`, causing "Cannot find module" errors for consumers.

**Solution:** Use custom publish script with two-step process:

```bash
# 1. Sync lockfile (resolves workspace:* from lockfile)
bun install

# 2. Pack tarball (resolves workspace:* to actual versions)
bun pm pack

# 3. Publish tarball (supports npm OIDC)
npm publish <tarball>
```

**Why not `bun publish`?** Bun resolves workspace protocols but doesn't support npm OIDC - requires `npm login`.

See `references/publish-script.ts` for full implementation.

## Ignored Packages (Non-Published)

Exclude packages from publishing in `.changeset/config.json`:

```json
{
  "ignore": ["@swarmtools/web", "docs-app"]
}
```

**Important:** Changeset ignore only affects versioning, NOT builds. Must also exclude from turbo:

```bash
# In CI, exclude ignored packages from build
bun turbo build --filter='!@swarmtools/web'
```

## Common Issues

### CLI Bin Script "Cannot find module"

**Symptom:** Published package works, but CLI bin script fails with `Cannot find module '@clack/prompts'`.

**Root cause:** Bin script imports are runtime dependencies, not devDependencies.

**Fix:** Move ALL bin script imports to `dependencies` in package.json:

```json
{
  "dependencies": {
    "@clack/prompts": "^0.7.0",  // Used by bin/cli.ts
    "commander": "^11.0.0"        // Used by bin/cli.ts
  }
}
```

### Lockfile Stale After Changeset Bump

**Symptom:** Publish picks up old versions of `workspace:*` dependencies.

**Root cause:** `bun pm pack` resolves from lockfile, which is stale after version bumps.

**Fix:** Run `bun install` BEFORE `bun pm pack`:

```bash
bun install              # Sync lockfile with new versions
bun pm pack              # Now packs with correct versions
npm publish <tarball>
```

See `references/publish-script.ts` - automatically handles this.

### Local `bunx changeset version` Fails

**Symptom:** `Error: GITHUB_TOKEN not found`

**Root cause:** Changesets needs GitHub API access for PR/changelog generation. Works in CI (has GITHUB_TOKEN), fails locally.

**Fix:** Don't run `bunx changeset version` or `bunx changeset publish` locally. Let CI handle it:
1. Create changeset file manually
2. Push to main
3. CI creates release PR
4. Merge PR → auto-publishes

### Bun Publish vs npm Publish

**Avoid `bun publish`** - doesn't support npm OIDC (requires `npm login`).

**Use `npm publish <tarball>`** - supports OIDC + resolves workspace protocols when publishing tarball created by `bun pm pack`.

## Reference Files

- **references/publish-workflow.yml** - Full GitHub Actions workflow with OIDC + workspace resolution
- **references/changeset-config.json** - Changeset configuration with ignored packages
- **references/publish-script.ts** - Custom publish script handling workspace:* resolution

## Commands Reference

```bash
# Create changeset (manual file creation)
cat > .changeset/fix-thing.md << 'EOF'
---
"pkg-name": patch
---
Fixed the thing
EOF

# Preview version bumps (optional, informational only)
bunx changeset status

# Build packages (exclude ignored)
bun turbo build --filter='!@swarmtools/web'

# Publish (in CI only, via publish.yml)
bun install                    # Sync lockfile
bun pm pack                    # Create tarball with resolved workspace:*
npm publish <tarball>          # Publish with OIDC
```

## Tracking Issues

- **Bun native npm token support:** https://github.com/oven-sh/bun/issues/15601
  - When resolved, can switch to `bun publish` directly
  - Currently must use `npm publish` for OIDC support
