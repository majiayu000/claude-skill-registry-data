---
name: project-adopt
description: Bring an existing repository (brownfield) under the Keelokit harness without touching its code — installs only .keelokit/, maps each house rule to the checks the repo already has, registers what it can't meet yet as dated exceptions, builds docs/context from what exists, and seeds a backlog from a diagnosis of the real code. Use when the user says "adoptá este repo", "sumá keelokit a este proyecto", "proyecto existente", "brownfield", "aplicá el harness acá", "adopt", or when /keelokit runs in a repo without .keelokit/.
---

# Adopt — the harness on an existing repo, green on day one, debt in plain sight

The code is never modified by this skill without the user's yes. The goal is an honest
`python3 .keelokit/bin/doctor.py`: every house rule either enforced by a real
check, or excepted with a reason, an approver and a date.

| Gate | Output | Human |
|---|---|---|
| intake | `docs/context/` built from what exists | approves the context |
| adopt | `.keelokit/` installed, rules mapped, exceptions registered, doctor passing | approves each exception |
| backlog | diagnosis + stories to pay the debt and continue the product | approves the order |

Record each approval in `.keelokit/state.toml` under `[gates]` as `<gate> = "<YYYY-MM-DD>"`.
Set `[dashboard] lang` to the user's language, and refresh the dashboard (`/keelokit:project-dashboard`)
when a gate's output is ready and after each approval. Never ask for an approval without showing
what it covers: the link to its section and, in the chat, the list itself (each exception with
reason and expiry; the waves and their stories). Explain terms of art in one plain sentence the
first time they come up.

Settle the run decisions once, as project-new's step 0 does, and record them in `[run]`. In
automatic mode the intake and backlog gates can be approved automatically (`"<date> auto"`), but
the adopt gate never is: every exception needs the user's own yes.

## 1. Survey (read-only)

Read, don't run: README, manifests (`package.json`, workspace files, lockfile type), CI
workflows (job names), git hooks (`.githooks`, `.husky`, `core.hooksPath`), lint/format/ts
configs, test setup, Dockerfile/deploy configs, ADRs and any existing requirements or context
docs. Summarise in ten lines: stack vs the house stack, commands, CI jobs, hooks, tests, docs.

Then **diagnose what the project is** — from the code, not from habit. A Claude Code plugin, a
library or a CLI has no hosting, no database and no screens; a SaaS has all three. Decide the
`kind` and the `traits` (vocabulary in the file's header: `typescript`, `ui`, `web`, `mobile`,
`site`, `api`, `database`, `hosted`, `i18n`, `personal-data`, `payments`, `developer-facing`),
each with its evidence, and show them to the user to confirm. After step 2 creates `.keelokit/`,
write them in `.keelokit/profile.toml`:
```toml
kind = "plugin"
traits = ["developer-facing"]   # no ui, no database, no hosting: rules that need them don't apply

[detected]
stack = ["Python 3.11", "Markdown skills", "Copier template"]
tests = ["unittest"]
ci = ["GitHub Actions: tests, template generation"]
hosting = []

[evidence]
hosted = "no deploy config; distributed through the Claude plugin directory"
```
The profile decides which house rules apply (their `needs`), which bug-bash lenses run, and what
the dashboard shows. Never create folders or apps the profile doesn't call for.
Environments found (URLs, who deploys, how) go in `docs/context/environments.md`; if the repo
already deploys, `/keelokit:ship-setup` can turn that into a verified checklist.

## 2. Install the harness layer

```bash
uvx copier==9.18.2 copy --defaults --vcs-ref v<version> --data mode=harness \
  --data project_name="<name>" --data description="<one sentence>" "${KEELOKIT_TEMPLATE:-gh:leosimini/keelokit}" .
```
(`<version>` from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`.) This writes only
`.keelokit/`. Confirm with `git status` that nothing outside `.keelokit/` changed. From now on the
plugin's guard hook is active in this repo.

If the profile has the `mobile` trait, detect how the app launches locally: run
`/keelokit:run-local`, which shows what `.keelokit/bin/run-local.sh detect` found (where the Expo
app, the package manager, the API and the database are), asks only about what it isn't sure of,
and with the user's yes writes the `[local]` block in `.keelokit/profile.toml`. It also asks
before creating `.local-dev/` and adding it to `.gitignore`: that is the one thing outside
`.keelokit/` it touches, and only with a yes. No `mobile` trait: skip this.

## 3. Intake from what exists

Run `/keelokit:plan-intake`. Harvest first: existing briefs, requirement docs, context packs, ADRs and
the code itself are the sources; facts derived from code are `inferred` until the user confirms.
Only then ask the delta.

## 4. Map the house rules

Run the doctor. Rules whose `needs` the profile doesn't have are listed as not applicable — they
are not exceptions and need nothing. For each rule it reports:

1. **The repo already enforces it under another name** (a CI job, a test, a lint rule, a hook) →
   add a local entry with the house rule's id and only `enforced_by` in `.keelokit/rules.local.toml`:
   ```toml
   [[rule]]
   id = "SEC-1"
   enforced_by = ["ci:gitleaks", "hook:guard.py"]
   ```
   The mapped check must enforce the rule **as written**. If it only covers part of it (e.g. CI
   runs the gates but nothing runs them before a push), map what exists and also propose an
   exception for the missing part.
2. **Nothing enforces it** → propose, per rule, one of:
   - add the check now (small, safe changes: a lint rule, a CI step running the doctor) — only
     with the user's yes, and in its own commit;
   - an exception in `.keelokit/exceptions.toml` with reason, approver (the user) and an expiry
     date, plus a backlog story that removes it.
   Never register an exception the user hasn't approved; never map a rule to a check that
   doesn't really enforce it just to go green.
3. **Rule doesn't apply** (e.g. no API) → it is already skipped by its `when`; nothing to do.

Critical areas start empty in an adopted repo (`.keelokit/critical.toml`). During the diagnosis,
propose the areas where the code moves money, sends things, enforces limits or holds other
people's data, and the invariants they keep (`domain.md`). MUT-1 maps to the repo's own mutation
tool if it has one (Stryker, mutmut, PIT); otherwise it is an exception with a date, and a story
to add `scripts/mutation.sh` (Keelokit's version runs any package `test` script under Stryker).

Stack differences from the house stack: one `docs/decisions/0001-existing-stack.md`
(Status, Context, Decision, Consequences) — the repo keeps its stack; the decision makes it
explicit. Don't propose migrations unless the user asks.

Also propose (don't impose): calling `python3 .keelokit/bin/guard.py git-pre-commit` from the
repo's pre-commit hook, and a `doctor` step in CI. Each is a code change → ask first. Until the
git hook exists, rules enforced by `git-hook:pre-commit` show as not enforced for humans — that
is accurate, not a bug: map them to what the repo has, or except them with a date.

## 5. Diagnose and seed the backlog

Write `docs/diagnosis.md`: what the code verifiably does today (with `file:line` evidence), the
debt behind each exception, drift between docs and code, and risks. Then run `/keelokit:plan-backlog`
with two kinds of stories: one per exception (to remove it before its expiry) and the product's
next slice. Stories already delivered (their ids in git history) are never renumbered.

## Close

Report: rules enforced / mapped / excepted (with expiry dates), open gaps by owner, the
decision about the stack, and the first ready stories.
