---
name: release-this
description: "Orchestrates the full powerball-harness plugin release with build, validation, version bump, CHANGELOG, tag, and GitHub Release. Use when releasing this plugin."
when_to_use: "release this plugin, release harness, cut a release, publish harness, ship harness, release-this"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Agent"]
argument-hint: "[patch|minor|major|--dry-run|--complete]"
model: sonnet
effort: low
---

# Release This Plugin

Project-specific release orchestrator for the claude-code-harness plugin.
Runs all plugin-specific checks (build, consistency, validation, Codex templates, version sync), then handles the full release: version bump, CHANGELOG update, commit/tag/push, and GitHub Release creation.

## Quick Reference

| Argument | Behavior |
|----------|----------|
| `patch` | Patch version bump (bug fixes, x.y.Z+1) |
| `minor` | Minor version bump (new features, x.Y+1.0) |
| `major` | Major version bump (breaking changes, X+1.0.0) |
| `--dry-run` | Run steps 1–5 only; print what would happen; skip publishing |
| `--complete` | Mark release complete only (step 7 — empty commit + push) |

## Execution Flow

### Step 1: Cross-platform binary build if there are changes in `go/` since the last release

Run `make build-all` to compile darwin-arm64, darwin-amd64, and linux-amd64 binaries unless there are no changes in `go/` source files since the last release. This ensures that any build issues are caught before proceeding with release validation or publishing steps.

```bash
make build-all
```

Fail immediately if `make build-all` exits non-zero. Do not proceed to step 2.

### Step 2: Plugin consistency checks

Run the 13 plugin-specific consistency checks. These verify symlink integrity, template consistency, version alignment, and structural invariants.

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/check-consistency.sh"
```

### Step 3: Full plugin validation

```bash
bash ./tests/validate-plugin.sh
```

This runs all CI-gated checks: marketplace.json structure, skill frontmatter, hook schemas, section 9 migration residue scan, and section 10 skill-description audit.

### Step 4: Codex template verification

Verify that the Codex CLI configuration templates and the Codex-specific skill bodies are present and readable. Missing files would ship a broken Codex experience to users.

**4a. Codex CLI config templates** (`harness/templates/codex/`):

```bash
ls -la harness/templates/codex/
```

Confirm `AGENTS.md`, `README.md`, `config.toml`, `.codexignore`, and `rules/` are all present.

**4b. Codex skill bodies** (`harness/templates/codex-skills/`):

```bash
ls -la harness/templates/codex-skills/
ls harness/templates/codex-skills/*/SKILL.md
```

Confirm each subdirectory (`breezing`, `harness-schedule-run`, `harness-work`) contains a `SKILL.md`. A missing `SKILL.md` means that Codex-variant skill is broken.

### Step 5: Version sync check

Verify that `harness/VERSION` and `harness/harness.toml` agree before proceeding.

```bash
HARNESS_RELEASE_EXTRA_VERSION_FILES="harness/harness.toml" bash "${CLAUDE_SKILL_DIR}/scripts/sync-version.sh" check
```

If there is a mismatch, stop and ask the user to run:
```bash
HARNESS_RELEASE_EXTRA_VERSION_FILES="harness/harness.toml" bash "${CLAUDE_SKILL_DIR}/scripts/sync-version.sh" sync
```
or manually reconcile the files before proceeding.

---

**Dry-run stops here.** In `--dry-run` mode, steps 1–5 run normally but no release is published, no files are written, and no git commits or tags are created. Report what the release would contain and what the new version would be, then exit.

---

### Step 6: Release phases (preflight → CHANGELOG → commit/tag/push → GitHub Release)

Create the wrapper lock:

```bash
mkdir -p .claude/state && touch .claude/state/harness-release-wrapper.lock
```

**Phase 0–2 (preflight + version bump)**: Delegate to `releaser` agent via `setup` invocation:

```
Agent(
  subagent_type: "releaser",
  description: "run preflight and bump version",
  prompt: "{\"schema_version\":\"releaser-request.v1\",\"invocation\":\"setup\",\"bump_type\":\"<patch|minor|major>\"}"
)
```

Parse `new_version` from the `releaser-response.v1` response. If `status` is `"error"`, surface the `error` field and abort.

**Phase 3 (CHANGELOG)**: Move `[Unreleased]` content into `## [X.Y.Z] - YYYY-MM-DD`. Keep empty `## [Unreleased]` above it. Format rules: [`references/writing-changelog.md`](${CLAUDE_SKILL_DIR}/references/writing-changelog.md).

**Phase 3.5 (Validate release notes)**: Validate CHANGELOG and release notes:

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/validate-release-notes.sh"
```

**Phase 4–5 (commit/tag/push)**: Delegate to `releaser` agent via `finalize` invocation:

```
Agent(
  subagent_type: "releaser",
  description: "commit, tag, push release v<new_version>",
  prompt: "{\"schema_version\":\"releaser-request.v1\",\"invocation\":\"finalize\",\"version\":\"<new_version>\"}"
)
```

Parse `git_hash` from the response. If `status` is `"error"`, surface the `error` and `changes` fields.

**Phase 6 (GitHub Release)**: Create the GitHub Release:

```bash
gh release create "v${NEW_VERSION}" \
  --title "v${NEW_VERSION} - <one-line summary>" \
  --notes "$(cat <<'EOF'
## What's Changed
...
EOF
)"
```

Wait for GitHub Release creation to succeed before proceeding to step 7.

### Step 7: Completion marking commit

After step 6 finishes, create an empty commit to mark the release as fully complete, then push it. Remove the wrapper lock when done.

```bash
NEW_VERSION=$(cat harness/VERSION)
git commit --allow-empty -m "chore: mark v${NEW_VERSION} release complete"
git push origin "$(git rev-parse --abbrev-ref HEAD)"
rm -f .claude/state/harness-release-wrapper.lock
```

This empty commit is the explicit record that "all release work is done." It is separate from the `chore: release vX.Y.Z` commit created by the releaser agent.

---

## `--complete` Mode

When called with `--complete`, execute only step 7 (the completion marking commit). Use this if step 6 already finished but the completion commit was not created.

```bash
NEW_VERSION=$(cat harness/VERSION)
# Verify a GitHub Release exists for this version before marking complete
gh release view "v${NEW_VERSION}" || { echo "ERROR: GitHub Release v${NEW_VERSION} not found. Create it first."; exit 1; }
git commit --allow-empty -m "chore: mark v${NEW_VERSION} release complete"
git push origin "$(git rev-parse --abbrev-ref HEAD)"
```

## Related Skills

- `harness-review` — Run before release to catch issues early
- `harness-plan` — Plan the next release tasks
- `harness-work` — Work on tasks

## Related Rules and References

- `harness/rules/versioning.md` — SemVer classification criteria and batch release policy
- `harness/rules/github-release.md` — GitHub Release Notes format
- [`references/versioning-rules.md`](${CLAUDE_SKILL_DIR}/references/versioning-rules.md) — Detailed versioning rules
- [`references/writing-changelog.md`](${CLAUDE_SKILL_DIR}/references/writing-changelog.md) — CHANGELOG format guide
