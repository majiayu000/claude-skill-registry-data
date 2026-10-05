---
name: openrind-desktop-orchestrator-npm-publish
description: |
  Publish the openrind-desktop-orchestrator npm package with clean git hygiene.

  Triggers when user mentions:
  - "openrind-desktop-orchestrator npm publish"
  - "publish openrind-desktop-orchestrator"
  - "bump openrind-desktop-orchestrator"
---

## Quick usage (already configured)

1. Ensure you are on the default branch and the tree is clean.
2. Bump versions via the shared release bump (this keeps `openrind-desktop-orchestrator` aligned with the app/desktop release).

```bash
pnpm bump:patch
# or: pnpm bump:minor
# or: pnpm bump:major
# or: pnpm bump:set -- X.Y.Z
```

3. Commit the bump.
4. Preferred: publish via the "Release App" GitHub Actions workflow by tagging `vX.Y.Z`.

Manual recovery path (sidecars + npm) below.

```bash
pnpm --filter openrind-desktop-orchestrator build:sidecars
gh release create openrind-desktop-orchestrator-vX.Y.Z packages/orchestrator/dist/sidecars/* \
  --repo openrind/openrind-shell \
  --title "openrind-desktop-orchestrator vX.Y.Z sidecars" \
  --notes "Sidecar binaries and manifest for openrind-desktop-orchestrator vX.Y.Z"
```

5. Build openrind-desktop-orchestrator binaries for all supported platforms.

```bash
pnpm --filter openrind-desktop-orchestrator build:bin:all
```

6. Publish `openrind-desktop-orchestrator` as a meta package + platform packages (optionalDependencies).

```bash
node packages/orchestrator/scripts/publish-npm.mjs
```

7. Verify the published version.

```bash
npm view openrind-desktop-orchestrator version
```

---

## Scripted publish

```bash
./.opencode/skills/openrind-desktop-orchestrator-npm-publish/scripts/publish-openrind-desktop-orchestrator.sh
```

---

## First-time setup (if not configured)

Authenticate with npm before publishing.

```bash
npm login
```

Alternatively, export an npm token in your environment (see `.env.example`).

---

## Notes

- `openrind-desktop-orchestrator` is published as:
  - `openrind-desktop-orchestrator` (wrapper + optionalDependencies)
  - `openrind-desktop-orchestrator-darwin-arm64`, `openrind-desktop-orchestrator-darwin-x64`, `openrind-desktop-orchestrator-linux-arm64`, `openrind-desktop-orchestrator-linux-x64`, `openrind-desktop-orchestrator-windows-x64` (platform binaries)
- `openrind-desktop-orchestrator` is versioned in lockstep with Openrind Desktop app/desktop releases.
- openrind-desktop-orchestrator downloads sidecars from `openrind-desktop-orchestrator-vX.Y.Z` release assets by default.
