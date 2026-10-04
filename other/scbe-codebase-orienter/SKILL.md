---
name: scbe-codebase-orienter
description: Explain the SCBE-AETHERMOORE repo, separate live code from generated or archival material, and route work to the correct entrypoints. Use when Codex needs a fast codebase walkthrough, startup map, module ownership summary, or guidance on whether a feature lives in `src/`, `api/`, `scripts/`, `artifacts/`, or docs.
---

# SCBE Codebase Orienter

Use this skill when the repo feels too large or too mixed to reason about quickly.

## Orientation Workflow

1. Read `AGENTS.md` and `package.json` first.
2. Read `references/repo-map.md` for the high-level lane breakdown.
3. Read `references/runtime-entrypoints.md` when the task involves running code, APIs, HYDRA commands, or the webtoon/manhwa lane.
4. Separate active code from support material before making claims.

## Repo Truths

- Treat `src/` as the main codebase, but note that it is hybrid: it contains both TypeScript package modules and Python runtime modules.
- Treat `package.json` as the clearest statement of the npm-distributed TypeScript surface.
- Treat `src/api/main.py` and `api/main.py` as different service lanes, not duplicates with identical purpose.
- Treat `scripts/` as the operational control plane. Many real workflows live there before they become package APIs.
- Treat `artifacts/`, `dist/`, and most of `training-data/` as outputs, corpora, or generated assets unless the user explicitly wants those lanes.
- Treat docs as guidance, not proof. When behavior matters, verify against code in `src/`, `api/`, and `scripts/`.

## Output Pattern

When explaining the codebase, answer in this order:

1. What the repo is trying to do.
2. Which top-level lanes are active.
3. Which file or directory is the right entrypoint for the user's goal.
4. Which areas are generated, historical, or likely to be noisy.
5. Which command to run next if the user wants to inspect or execute something.

## Avoid These Mistakes

- Do not flatten the repo into "just one API". Explain whether the question is about the governance API in `api/` or the newer control-plane work in `src/api/`.
- Do not treat all docs as current. Prefer code and tests when there is tension.
- Do not send users into `artifacts/` or `training-data/` unless the task is specifically about datasets, webtoon outputs, exports, or generated evidence.
- Do not assume every top-level folder is product-critical. Many are experiments, snapshots, or support lanes.

## References

- Use `references/repo-map.md` for the core lane map and "where to start" view.
- Use `references/runtime-entrypoints.md` for run commands and file-level entrypoints.
