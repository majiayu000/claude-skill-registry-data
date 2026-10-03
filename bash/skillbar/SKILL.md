---
name: skillbar
description: Build, run, troubleshoot, or extend SkillBar, the codex-goated-skills macOS menu bar manager. Use when Codex needs to work on the `apps/skillbar` workspace, validate repo-driven catalog parsing, exercise install or update wiring through `bin/codex-goated`, or keep the local preset, pack, and installed-state flows honest.
---

# SkillBar

Use this skill when the user wants to work on the real SkillBar product surface in `apps/skillbar`. Do not route general skill-authoring, pack curation, or repo marketing work here unless the request is specifically about the SkillBar app or its local install flows.

If the current repo contains `apps/skillbar`, use that workspace by default. Otherwise, pass `--workspace /path/to/skillbar` to the runner script.

## Quick Start

1. Use `bash scripts/run_skillbar.sh doctor` from the repo root, or pass `--workspace /path/to/skillbar` if the app lives elsewhere.
2. Use `bash scripts/run_skillbar.sh inspect` before editing so the app model, services, tests, and CLI entrypoint stay visible.
3. Use `bash scripts/run_skillbar.sh smoke-install skillbar` to verify one real install path against a temporary destination.
4. Use `bash scripts/run_skillbar.sh smoke-update skillbar` to verify the overwrite path after update wiring changes.
5. Use the repo-health actions in SkillBar itself, or `bash scripts/run_skillbar.sh catalog-check`, when you touch skill or pack metadata and need to verify the generated catalog is current.
6. Use the repo-health actions in SkillBar itself, or `bash scripts/run_skillbar.sh audit`, for the full repo skill and pack integrity sweep.
7. Use `python scripts/skill_market_loop.py develop` or `bin/codex-goated develop` for the bounded self-development loop that rebuilds the catalog, audits the market, and runs SkillBar doctor/typecheck/catalog/audit checks.
8. Use `bash scripts/run_skillbar.sh generate` after changing `project.yml`.
9. Use `bash scripts/run_skillbar.sh typecheck` for a fast source-level sanity pass before a full build.
10. Use `bash scripts/run_skillbar.sh test` once Xcode is ready.
11. Use `bash scripts/run_skillbar.sh run` after UI changes so the menu bar app relaunches from the local build output.

## Workflow

### Before Editing

- Read `skills/skillbar/references/project-map.md` for the actual app layout and validation path.
- If the task changes project settings or app metadata, inspect `apps/skillbar/project.yml` and `apps/skillbar/SkillBarApp/Info.plist` first.
- Treat `skills/*` in the repo as the catalog source of truth.
- Treat `~/.codex/skills` as the installed-state source of truth unless the user picks another destination.
- Treat `bin/codex-goated catalog check` and `bin/codex-goated audit` as the repo-health checks for skill metadata and pack integrity.

### Product Boundary

- SkillBar owns:
  - local catalog discovery from the repo checkout
  - installed-state visibility
  - install and update actions delegated to `bin/codex-goated`
  - curated preset bundles built from existing skills
  - repo pack browsing and pack install/update actions built from `collections/*`
  - setup for repo path and installed-skills path
- SkillBar does not own:
  - skill creation or editing outside the app workflow
  - remote marketplace sync
  - third-party registries
  - secrets for unrelated tools

### Editing Guidance

- Keep the experience menu-bar-first and compact. Do not turn SkillBar into a full dashboard app unless the user asks.
- Reuse `bin/codex-goated` for install and update actions instead of inventing parallel tooling.
- Preserve deterministic metadata parsing with graceful fallback when optional fields are missing.
- Keep preset bundles static and understandable; they should not become a second catalog system.
- Treat repo packs as read-only catalog entries that install or refresh their bundled skills.
- If you touch install flows, run `smoke-install` before calling the work complete.
- If you touch update flows, run `smoke-update` to prove overwrite behavior through `bin/codex-goated`.
- If you touch skill or pack metadata, run `catalog-check`; if you touch repo-wide catalog plumbing, run `audit` too.
- Use `typecheck` when you only need a fast source-level sanity check before a full build.

### Validation

- Prefer the local runner script before manual `xcodegen` or `xcodebuild` commands.
- Run `doctor` first if the machine may be missing Xcode setup.
- Run `smoke-install` for at least one skill when the work touches install wiring, CLI integration, or repo-root resolution.
- Run `smoke-update` when the work touches update wiring, overwrite behavior, or refresh semantics.
- Run `catalog-check` when the work touches skill metadata, pack membership, or generated catalog freshness.
- Run `audit` when the work touches repo-wide catalog plumbing or you want the stronger integrity sweep.
- Run `typecheck` when you want the fastest local check of the app sources or when Xcode is not fully ready.
- Run `test` before calling the work complete when Xcode is ready. If Xcode is blocked, report the exact blocker from the runner.

## Example Prompts

- `Use $skillbar to inspect the SkillBar workspace, tighten the preset flow, and validate one real install path.`
- `Use $skillbar to run doctor, test the app, and fix the local catalog parser.`
- `Use $skillbar to improve the menu bar UI without breaking the repo-driven install and update actions.`
- `Use $skillbar to add repo-pack browsing and keep the pack install path honest.`

## Resources

- `scripts/run_skillbar.sh`: repo-root wrapper for the packaged SkillBar runner. Use this from the repo root for doctor, inspect, generate, open, build, typecheck, test, run, smoke-install, smoke-update, catalog-check, and audit.
- `skills/skillbar/scripts/run_skillbar.sh`: packaged implementation that the repo-root wrapper delegates to.
- `scripts/skill_market_loop.py develop` and `bin/codex-goated develop`: one-shot local development loop for catalog refresh, market audit, and SkillBar validation.
- `skills/skillbar/references/project-map.md`: target map, key files, and validation expectations.
- `../../bin/codex-goated`: the CLI that SkillBar should continue delegating install and update work to.
- `../../collections/`: repo-pack source files that SkillBar now surfaces in its pack browser.
