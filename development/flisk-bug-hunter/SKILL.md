---
name: flisk-bug-hunter
description: Finds bugs in the flisk CLI, its generated files and its MCP server by chaos testing - picking the right tier (graph, gates, Docker, CLI fuzz, state, MCP), writing an oracle that does not cry wolf, running thousands of cases, bucketing the findings, proving each one by hand, fixing it with a test and a deliberate-break check. Use when asked to find bugs, harden a command, hunt regressions after a change to service.json handling, `flisk up`, `flisk config` or the MCP tools, or when users report that an edit "did not take effect".
license: MIT
compatibility: Needs the checkout, Bun and Node 22+. The Docker tier also needs Docker (Compose and Buildx) and Tilt on PATH. The tiers never start a real stack.
metadata:
  author: flisk-sh
  version: "1.0"
---

# Hunting flisk bugs with chaos tests

The tiers live in `tests/chaos/` (see its README for the commands). This skill is the method: how to pick a tier, how to judge the output, and how to turn a finding into a fix that stays fixed. Most of what it records was learned the hard way, by writing a rule that was too strict and then finding out which real project it broke.

## 1. The one idea

A command is wrong when **a check accepted something that a later step then refused or broke**. `flisk up` says yes, then Tilt, Compose or Docker says no, minutes later. Hunt that gap. Every tier below is a different way of finding an input the early check lets through, or a place where two commands that describe the same project disagree.

Three kinds of bug turned up again and again:
- **gate gap:** `flisk up --dry-run` accepts a value that breaks the generated Tiltfile, Compose file or Dockerfile (an unsafe name, a malformed `secrets`, a user `dockerfile`);
- **disagreement:** two commands answer differently about one project (`resources` against the files on disk, `config regenerate` against `config verify`, the CLI graph against the Tilt graph);
- **raw crash:** an unhandled error ends as a runtime stack trace, or kills a long-running server such as `flisk mcp`.

## 2. Pick the tier by what you suspect

| Suspect | Tier | Cost |
|---|---|---|
| a `dependsOn` edit does not change the graph | graph (`tests/chaos/graph`): random edits checked against the Tilt graph, `flisk up --dry-run` and `flisk config verify` | seconds per case |
| a service.json value passes the check | gates (`gates/bulk.ts`): millions of seeded good and corrupted sets, in memory | about 50,000 sets a second |
| a value passes the check but breaks Compose, Tilt or the Dockerfile | Docker (`docker/run.ts`, variants in `docker/variants.ts`): one field changed at a time, then Tilt eval, `docker compose config`, `docker buildx build --check` | about 3 cases a second |
| a command crashes or lies for odd arguments or a damaged project | CLI fuzz (`cli/fuzz.ts`) | about 15 runs a second |
| commands disagree after a sequence of edits | state (`cli/state.ts`) | a project per sequence |
| an image is bigger than its contents | size (`docker/size.ts`) plus `docker history` of a real image (section 4) | seconds, no build |
| an agent tool crashes the server or returns garbage | MCP (`cli/mcp.ts`) | one server per project state |

Start with the cheapest tier that could see the bug. Scale only after a small run is clean or the findings are understood.

## 3. Write the oracle before the generator

An oracle states what must hold for **any** input, without knowing what the command is for. Good ones used here:
- the process ends with exit code 0, 1 or 2, never a signal or timeout;
- no runtime stack trace (`at x (file:1:2)`, `node:internal`, `TypeError:`) in stdout or stderr;
- with `--json`, stdout is exactly one JSON envelope `{ schemaVersion, data, errors }`, and it agrees with the exit code;
- no `[object Object]`, `NaN` or a bare `undefined` where a value belongs;
- the MCP server stays up, and every call gets one reply;
- the listing commands agree with the disk, and a second `flisk config regenerate` changes nothing.

An oracle that cries wolf wastes the whole run. After every first run, **read each bucket and ask whether the tool or the oracle is wrong**. These were oracle mistakes, not bugs, and the oracle was fixed:
- `-v`, `-h` and `help` print text on purpose, and a usage screen with exit 2 is how a command says "invalid arguments";
- a word the caller typed (`undefined`) is echoed in an "unknown argument" error;
- `--stack --json` makes `--json` the value of `--stack`, so no JSON was requested;
- exit 127 means a helper such as `npx` is not installed on this machine;
- two services on one port are harmless in Docker (only Traefik publishes a host port), but the native runtime refuses them.

## 4. Hunting image size

Size bugs hide because nothing fails. Two cheap moves find them:
1. **Look at a real image first.** `docker images` lists what is on the machine; compare an image with its siblings (an agent was 181 MB, its migrator 1.54 GB). Then `docker history` shows which layer holds the bytes. Two layers of the same size, one a `COPY` and one a `RUN`, mean a file tree was stored twice.
2. **Turn the cause into a static rule** in `docker/size.ts` and run it over the Dockerfiles generated for every resource type. No image is built, so it takes seconds and can run in CI.

Causes seen so far: a recursive `chown`/`chmod` after a `COPY` (every file stored again; use `COPY --chown`); `apk add` without `--no-cache`; `apt-get install` without removing the index; `COPY . .` before the dependency install. Prove the mechanism on a tiny offline Dockerfile with a 60 MB file (`COPY` then `chown -R` was 651 MB, `COPY --chown` 531 MB) before claiming a saving, and say plainly which numbers were measured and which were read from a layer listing. Building the real generated image needs the golden base images that Tilt builds first, so it is usually not possible in a quick session.

## 5. Run, then bucket

Give every random case a seed (`--seed`) so a finding replays. Group failures by tool, oracle and a **normalised** first line (strip digits, paths, quoted strings) so 4,000 hits of one bug show up as one bucket with a count and one reproduction. A run that prints 12 buckets is readable; one that prints 12,000 lines is not.

Typical yield, as a guide to effort: about 28,000 CLI fuzz cases found 3 real bugs, 100 state sequences found 1, and the Docker tier found one in a few dozen cases. Argument fuzzing is cheap and finds crashes; the Docker and state tiers find the expensive, user-visible ones.

## 6. Prove it by hand before believing it

For each bucket:
1. Reproduce it with a plain command in a fresh temp project (`flisk project --yes --no-agent-skills`, then `flisk resource <name> --yes --type backend --stack main`).
2. Find the line of source that causes it. Do not guess from the symptom.
3. Decide whether it is a bug or a design choice by reading the schema, the docs and the code comments. `flisk config regenerate` leaving the per-service compose alone is by design (`flisk up` writes it); the message around it was the bug.
4. If the claim cannot be reproduced, say so and withdraw it. A test that "shows" a missing value can pass because the file was never generated at all (`tilt alpha tiltfile-result` writes no app compose). Check that your check can fail.

## 7. Fix it the way the codebase expects

- Put the rule where the existing checks live: `cli/src/utils/service-manifest.ts` for field shapes, `cli/src/utils/service-config-checks.ts` for project-wide checks that `flisk up` runs before Tilt.
- **Prefer a warning when real projects might already have the value.** A rule inferred from the Docker tier was too strict twice (enum values, and `..` in a build path that `flisk import` writes itself) and broke the compose-import journey. Check what `flisk import` and the examples write before you refuse something.
- Add a unit test next to the check, a CLI test when the behaviour is visible in output (`cli/src/commands/__tests__/`, with `runFlisk` and `createTempDir` from `test-support`), and the case in the chaos catalogue so it cannot return.
- **Deliberate-break check:** put the bug back and see the new test fail. `bin/flisk.js` runs `cli/dist-bundle` when it exists, so swapping one file in `cli/dist` proves nothing; rebuild instead.
- Add a CHANGELOG line under "Unreleased", a `docs/troubleshooting.md` entry for any new check name (the `doctor-check-docs` ratchet drops otherwise), and update `docs/reference/machine-readable-cli.md` when a `--json` shape changes.

## 8. Verify like CI does

Run these from the repository root and read the result, not just the exit code:
- `npm --prefix cli run typecheck` (the CI typecheck uses `tsconfig.typecheck.json`, which includes the tests, so a plain `tsc --noEmit` can pass where CI fails);
- `npm --prefix cli run lint`, then `npm --prefix cli test`;
- `npm --prefix cli run build`, then `git add -f cli/dist`, commit, and `npm --prefix cli run check:dist` (it only passes on a committed tree);
- `make test-shell` and the scoreboard (`make scores`);
- the Docker tiers again after any gate change: 0 broken and 0 "refused though valid" is the bar.

On a machine without Node or with network limits, some CLI test files fail for reasons that have nothing to do with the change. Run the same files on a clean `origin/main` worktree and compare the failure count before blaming yourself.

## 9. Mistakes to avoid

- Committing run output (a `*-report.json`). Reports go to the temp directory.
- Bundling unrelated fixes. One PR per finding family, with the chaos case that found it.
- Reporting a count of "bugs" instead of reproduced ones. Say what was run, how many buckets, how many were real, and what was withdrawn.
- Running anything that starts or stops a real stack from a fuzzer. Force `--dry-run`, and keep every project path inside a temp directory.
- Editing generated files (`.flisk/`, `.flisk-out/`, `**/*.autogenerated.*`). Fix the source or the template.
- Evaluating the Tiltfile without enabling the stack. `flisk up` adds a newly found stack to the `pre_alpha` phase of `.flisk/project.json`; `--dry-run` does not, and `tilt alpha tiltfile-result` then writes no Dockerfile or compose at all. Add the stack to `enabledStacks` first, or a missing file looks like a missing feature.
- Trusting `tilt alpha tiltfile-result` to write the app compose. To test a compose generator, call it directly from a small Tiltfile (see `tests/tilt-engine/test_dependson_graph.py` for the pattern).

## 10. Findings log (add a line for every bug, in the order found)

Each line: what broke, which tier or move found it, and the fix. Keep it short; the PR has the detail.

- `dependsOn` edits not reaching the graph: stack names, the deprecated `dependencies` key, wrong-typed values, frontends' `backendName`. Graph tier. One shared reading in `cli/src/utils/dependency-graph.ts`.
- 35 service.json values that passed `flisk up` and then broke Tilt, Compose or Docker (unsafe names, wrong types, absolute build paths). Docker tier. Gate in `service-manifest.ts`.
- Live-only: discovery daemon left disabled, Tilt dropping file watches on a cycle, `status` hiding a Tiltfile error. A real `flisk up`, not a dry run.
- Native `command` services ignored `dependencies` and refused stack names in `dependsOn`. Hand probe of a native project. `native-runtime.ts` now uses the shared reading.
- A service with its own `dockerfile` failed the whole Tiltfile on the generated `.dockerignore`. Docker tier, variant `dockerfile=Dockerfile`.
- `flisk networks` on a corrupt `project.json` ended as an unhandled rejection with a stack trace. CLI fuzz. `parseAsync` plus one handler.
- Names starting with a hyphen (`--stack --json` made `services/--json/x`). CLI fuzz. Name pattern.
- `flisk resource` accepted a name another service.json already used. State tier. Refused with the existing path.
- The MCP `up` tool killed the whole server when `projectPath` did not exist (unhandled spawn `error`). MCP tier.
- A required secret with no value failed the whole Tiltfile through Compose interpolation; malformed `secrets` crashed the generator; a `params` value silently beat a secret. Docker tier `secrets` variants and a user report. Gate, shape errors and a warning.
- `flisk config regenerate` said it was done while per-service files were stale. User report. It now lists them; `flisk up` writes them.
- The migrator image stored `node_modules` twice (a 332 MB `COPY` plus a `chown -R` layer; 1.54 GB against 181 MB for the agent). `docker history` of a real image. `COPY --chown`, and the size lint.
- Not fixed, recorded in issue 2692: the migrator base carries a 294 MB global Bun install, and each migrator installs its own full `node_modules` on top.
