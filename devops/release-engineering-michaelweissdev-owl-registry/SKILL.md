---
name: release-engineering
description: >
  Coordinate, verify, and execute safe software release engineering workflows.
  Use when validating build artifacts, ensuring cross-manifest version consistency,
  running pre-release verification checklists, drafting release notes, planning
  rollbacks, or preparing distribution packages for automated CI/CD release tags.
compatibility: >
  Agent Skills-compatible coding agents preparing and verifying software releases.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "release-engineering, deployment, packaging, semver, artifacts, devops"
  topics: "version-control, devops, software-development"
---

# Release Engineering and Distribution

Release engineering ensures that software artifacts are built reproducibly, validated against strict quality gates, tagged consistently, and deployed safely with proven rollback plans. An agent must never publish packages or push production release tags without explicit user authorization.

## Core Rules

1. **Explicit authorization required for publishing**: Never trigger public distribution (`cargo publish`, `twine upload`, `npm publish`, production git tags) without clear, documented user approval.
2. **Version consistency across all manifests**: Ensure the release version matches exactly in `pyproject.toml`, `Cargo.toml`, `package.json`, documentation, and git tags.
3. **Reproducible, clean build environment**: Always build release artifacts from a clean working tree without untracked files or uncommitted modifications.
4. **Pre-flight smoke testing**: Verify the compiled artifact in an isolated clean environment (e.g. install the generated wheel or binary in an empty container) before distribution.
5. **Rollback strategy is mandatory**: Every release plan must specify exact rollback steps in case of post-deployment failure.

---

## 1. Pre-Release Quality Gates Checklist

Before creating a release candidate:

```
[ ] 1. Clean Working Tree: `git status --porcelain` returns empty.
[ ] 2. Test Suite Passes: All unit, integration, and end-to-end tests pass (100% green).
[ ] 3. Static Analysis Passes: Linter, type-checker, and security audit pass without warnings.
[ ] 4. Changelog Updated: `CHANGELOG.md` has version heading and release date under ISO format.
[ ] 5. Version Manifests Synchronized: Check all metadata files for exact version match.
[ ] 6. Artifact Verification: Generated binaries, wheels, or tarballs inspect cleanly.
```

---

## 2. Version Synchronization Verification

In multi-file or polyglot repositories, ensure versions do not drift:

```bash
# Example script to verify version consistency across manifests
check_versions() {
  local target_ver="1.4.0"

  echo "Checking Python manifest..."
  grep -q "version = \"$target_ver\"" pyproject.toml || { echo "pyproject.toml mismatch"; return 1; }

  echo "Checking Changelog..."
  grep -q "## \[$target_ver\]" CHANGELOG.md || { echo "CHANGELOG.md missing version header"; return 1; }

  echo "All release manifests match version $target_ver."
}
```

---

## 3. Artifact Smoke Testing in Isolated Sandbox

Never assume a package works just because tests passed against local source files:

```bash
# 1. Build artifacts cleanly
rm -rf dist/
python -m build

# 2. Create isolated sandbox environment
TMP_VENV=$(mktemp -d "/tmp/release_test_XXXXXX")
python3 -m venv "$TMP_VENV"

# 3. Install the BUILT wheel (not source files)
"$TMP_VENV/bin/pip" install dist/*.whl

# 4. Smoke test CLI and import from outside the repository directory
(cd /tmp && "$TMP_VENV/bin/python" -c "import my_package; print(my_package.__version__)")
(cd /tmp && "$TMP_VENV/bin/my-cli" --version)

# 5. Clean up sandbox
rm -rf "$TMP_VENV"
echo "Smoke test passed successfully."
```

---

## 4. Release Tagging and Rollback Planning

### Safe Git Tagging
```bash
# Create an annotated, signed release tag
git tag -a v1.4.0 -m "Release version 1.4.0: Caching layer and security fixes"

# Verify tag points to intended commit
git show v1.4.0 --stat
```

### Rollback Plan Documentation
Document rollback mechanisms before triggering deployments:
- **Container / Kubernetes**: `kubectl rollout undo deployment/api-server`
- **Package Registry**: YANK version rather than delete (`cargo yank --version 1.4.0`). Note that npm/PyPI prevent re-uploading an existing version string.
- **Git**: If a release commit introduces fatal regressions, tag a patch fix (`v1.4.1`) that reverts the bad commit (`git revert <commit>`), rather than deleting remote tags.

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| Building from a dirty working tree | Uncommitted local debug files included in distribution archive | Run `git status` and build from fresh clone or CI |
| Untested release artifacts | Wheel is missing critical non-Python data files (e.g. templates) | Smoke test the built wheel in an isolated venv |
| Forgetting to update version in one manifest | Inconsistent telemetry, failed dependency resolutions | Automate manifest checking script |
| Deleting git tags on remote | Breaks downstream builds that pinned exact tag sha | Issue a patch release (`v1.4.1`) with a clean revert |

---

## 6. Verification Checklist

- [ ] `git status` confirms zero uncommitted files or unstaged modifications.
- [ ] Version string is identical in all project manifests.
- [ ] Artifacts inspected with `unzip -l` or `tar -tf` for unexpected files.
- [ ] Smoke test passes in clean temporary sandbox environment.
- [ ] Release notes and changelog ready.
- [ ] User authorization obtained before publishing.
