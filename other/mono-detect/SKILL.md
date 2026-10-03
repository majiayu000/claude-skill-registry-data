---
name: mono-detect
description: Detect pnpm workspace structure, optional Turborepo overlay, package metadata, and internal dependency graph for monorepo-aware skills
type: analysis
version: v0.1
argument-hint: "[optional: repository root]"
invocation: sub-skill
parent: mono-plan
---

# Mono Detect

Invoke as `$mono-detect`.

Use this skill to detect a pnpm workspace monorepo and generate the `.agents/monorepo.json` artifact consumed by the monorepo pack.

`mono-detect` is the foundation skill for `mono-exec`, `mono-ship`, and `mono-guard`. Those skills use its output to inject monorepo-aware pre/post steps into the standard `$exec` and `$ship` contracts without duplicating the base workflow.

## Augmentation Injection Pattern

`mono-detect` is the pack's detection foundation for the augmentation injection pattern. It does not replace `$exec`, `$ship`, or base monorepo planning skills; it supplies `.agents/monorepo.json` so `mono-exec`, `mono-ship`, and `mono-guard` can inject monorepo-aware pre-flight and post-integration checks around those existing workflows.

## Process

1. Resolve the target repository root.
   - Use `$ARGUMENTS` as the root when provided.
   - Otherwise use the current working directory.
2. Locate the pack script relative to this skill: `../../scripts/mono-detect.sh` from the monorepo pack root.
3. Check whether `.agents/monorepo.json` is fresh:
   - Run `packs/monorepo/scripts/mono-detect.sh <root> --check-stale`.
   - If it prints `fresh: .agents/monorepo.json`, keep the existing artifact.
   - If the file is missing, stale, or the check does not report fresh, run `packs/monorepo/scripts/mono-detect.sh <root>` to regenerate it.
4. If detection fails because `pnpm-workspace.yaml` is missing:
   - Report that the project is not a detected pnpm monorepo.
   - Suggest `$mono-migrate` as a future V2 migration route when the user wants to convert a single-app project.
   - Do not create `.agents/monorepo.json` by hand.
5. Read `.agents/monorepo.json` and summarize:
   - Workspace manager.
   - Build orchestrator (`turborepo` when `turbo.json` is present, otherwise none).
   - Package count and package paths.
   - Internal dependency graph edges.
   - Turborepo pipeline names.
6. Report staleness behavior:
   - Mention that the artifact is regenerated when `pnpm-workspace.yaml`, `turbo.json`, or workspace `package.json` files are newer than `.agents/monorepo.json`.
7. Route the next step:
   - If detection passed and the user is preparing execution, recommend `$mono-exec`.
   - If detection passed and the user is checking lane safety, recommend `$mono-guard`.
   - If detection failed because this is not a pnpm monorepo, recommend `$mono-migrate` as the V2 advisory route.

## Output

- **Detection:** detected, fresh, regenerated, or not detected.
- **Workspace:** manager, build orchestrator, root path.
- **Packages:** count plus package name/path list.
- **Dependency graph:** internal dependency edges; say `none` when no internal edges exist.
- **Turbo pipelines:** pipeline names when present; say `none` when Turborepo is absent.
- **Artifact:** `.agents/monorepo.json` path and whether it was reused or regenerated.
- **Next work:** concrete follow-up.
- **Recommended next command:** one command.

## Constraints

- Do not edit task files.
- Do not run package manager install/add commands.
- Do not infer non-pnpm workspace managers in V1.
- Do not modify `.agents/monorepo.json` manually; use `mono-detect.sh`.
- Treat `mono-detect` as an augmentation foundation for `mono-exec`, `mono-ship`, and `mono-guard`, not as a replacement for `$exec`, `$ship`, or base monorepo planning skills.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
