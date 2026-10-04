---
name: see-it-live
description: "Launch the app and confirm the specific change is actually visible and working: screenshot the UI, curl the endpoint, or run the command. Doubles as the fast smoke pass: boots, core path works, key endpoint responds. Use for run the app, start the server, preview it, see it live, smoke test, sanity check, or post-deploy check."
license: MIT
allowed-tools: Bash
metadata:
  display-name: "See It Live"
  version: "1.1"
  platforms: "claude-code codex"
  tags: "verification runtime evidence"
---

# See it live

Type-check passing and green tests are **not** proof the change works. Behaviour lives in the running app. Before you say "done," start the thing and observe the specific change with your own eyes (or a screenshot / a response body).

## Pick the launch path by project type

Do not assume the launch command - the project always knows better than this table. Enumerate the runnable targets the project itself declares before choosing: build-file targets (`Makefile` / `justfile`), `package.json` scripts, declared CI job names, and the README run/validate section. A named journey/playtest/E2E/smoke target in that inventory outranks a generic launch, and its graphical variant outranks the headless one when one exists and the display environment allows it. Headless-only proof demonstrates absence of errors, not that the change is visible - say so in the evidence when you fall back to it.

| Project type | How to launch | What to observe |
|---|---|---|
| **Game engine (Godot, Unity, defold)** | The project's declared playtest/journey target first (e.g. a `make playtest-*` target, graphical or headless); `godot --headless --quit` to catch parse/script errors fast; the plain run command for interactive | The journey's scripted outcome passes and the changed behaviour happens, not just "scene loads with no errors" |
| **Web frontend** | Start the dev server (`npm run dev` / framework equivalent), open the changed route | Golden path renders AND the error state; screenshot it |
| **Backend / API** | Start the server, `curl` the changed endpoint with a real payload | `/health` returns 200; HTTP status + response shape match expectations |
| **CLI / library** | Run the command/binary with real args (`--help` doubles as a trivial liveness check) | `stdout`/`stderr` AND exit code are correct |

Match the project's actual run command - check its README / `CLAUDE.md` / `package.json` scripts / `justfile` first, don't invent one.

## Confirm the *specific* change, not just "it boots"

- Before launching, write down the one thing you expect to see that proves the change works ("the Save button now shows a spinner", "`/api/jobs` returns `status: queued`").
- Launch, reproduce the exact path that exercises the change, and check for that specific signal.
- "The app still starts" is necessary, not sufficient. A change can boot fine and still be wrong.

## Smoke mode

The same launch paths double as the fast critical-path gate between "built" and "shipped". The critical path is four checks, answered in seconds, not minutes:

- The app **boots** with no fatal error.
- The **core path works** (the single most important thing the product does).
- A **key endpoint responds** (health/liveness or the primary surface).
- **No error spew** in logs or console.

Run it twice: once after integrating a change, and again after deploy or merge. A failed smoke pass is a hard stop: do not proceed to ship until it passes. The post-deploy run hits the **deployed** URL, not localhost - localhost passing tells you nothing about prod - and confirms the new build is actually live (version endpoint, build hash, or a marker from the change). A post-deploy failure is a rollback trigger: surface it loudly, don't bury it.

Keep smoke mode fast and deterministic: no flaky waits, no giant fixtures, no dependence on third-party services you can't stub, a clear pass/fail signal. If you're writing the tenth assertion, you've drifted into `e2e-qa` territory - pull back.

## Capture evidence

- UI: a screenshot of the changed state (and the error state if relevant).
- API/CLI: the actual response body / stdout, pasted, not paraphrased.
- Note the command you ran so it's reproducible.

## Teardown

- Stop the dev server / kill the spawned process when done. Don't leave orphaned ports held or headless instances running.
- If you seeded data or toggled a flag to see it, revert it.

## What this skill is *not*

- Not automated testing - for repeatable checks use `qa-automation` (units) or `e2e-qa` (browser/CLI flows).
- This is the human-in-the-loop "I watched it happen" step; smoke mode is its fast, always-run variant.
