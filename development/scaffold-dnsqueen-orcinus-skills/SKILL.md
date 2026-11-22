---
name: scaffold
description: Set up a new project so build, lint, typecheck, and test all run from day one. Use when a calibrated idea is confirmed and there is no project yet, or when an existing project has no working checks. Only invoke via the orcinus router.
license: MIT
user-invocable: false
---

# SCAFFOLD — a project that is green from day one

Create the smallest project that builds, lints, typechecks, and tests. Do not write the real feature here. Do not commit a red project. The first commit happens only after all four commands pass.

## Rules

- No scaffold before a calibrated brief. If idea-calibrate has not confirmed the problem, user, success criteria, non-goals, and first slice, stop and run it first.
- Do not choose a stack silently. Confirm it with the user in one round, with a recommended answer, and record the choice and why.
- Every file must earn its place. No file without a stated need.
- No real secrets, ever. Placeholders only, in `.env.example`. Never commit a secret, and never ask for one in chat.
- The four commands are the gate. If any fails, fix only the cause and re-run all four.

## Steps, in order

### 1. Confirm the brief and the stack

Read the calibrated brief. Confirm the first slice. Then ask the user to confirm the stack (language, test runner, linter). Record the answer. If the user has no preference, recommend TypeScript with `tsc` and Node's built-in test runner, and say why: no extra test framework to install, and the four commands stay simple.

### 2. Create the tree

Create only these, unless the stack needs one more file — and if so, name the need:

- `README.md` — what the project is, in one paragraph, plus how to run the four commands.
- `package.json` (or the stack's manifest) — with scripts named exactly `build`, `lint`, `typecheck`, `test`.
- `src/` — with one minimal module for the first slice (a stub that does nothing yet, but compiles).
- `tests/` — with one passing test for that stub.
- `docs/constitution.md` — three to five invariants the project will enforce (see step 3).
- `.gitignore` — `node_modules/`, `dist/`, `.env`, and the stack's build output.
- `.env.example` — placeholder names only, no real values.
- `LICENSE` — MIT unless the user says otherwise.

### 3. Write the constitution

In `docs/constitution.md`, write the invariants in plain language, for example:

- No test weakening. Never delete, weaken, or skip a test to make the suite pass.
- One slice at a time. One behaviour, one test, one commit.
- No secrets in the repo.
- Implementer is never the final judge; orcinus-verify checks the work.

These are rules, not wishes. Later work must be able to point at them.

### 4. Secrets and environment

Put placeholder names in `.env.example` only. Put `.env` in `.gitignore` and never commit it. If a service needs a real key, the user provides it on their own machine. Human-only steps (accounts, keys, provisioning) belong to the user, never to the agent.

### 5. Initialise git

`git init -b main`. Do not commit yet.

### 6. Verify — all four, in order

Run, and record the real output and exit code for each:

1. `build`
2. `lint`
3. `typecheck`
4. `test`

All four must pass on the empty project with its one passing test. If any fails, fix only the cause and re-run all four from the top. Do not skip a failing check and do not weaken the test to get a pass.

### 7. First commit

Only now, commit with a clear message. Record in the handoff: what was built, the four commands and their outputs, the stack choice and why, and what the first real slice will be.

## What scaffold is not

Not the feature. Not a stack choice made for the user. Not a place to hide a failing check. If the four commands cannot all pass, the scaffold is not done.

## Sources

Method, in our own words, inspired by: spec-kit (github/spec-kit, MIT) for the spec and constitution pattern; create-mercato-app (MIT) for the scaffolding pattern; repomix (MIT) for the codebase map, which comes after scaffolding, not during it. No text was copied from those projects.
