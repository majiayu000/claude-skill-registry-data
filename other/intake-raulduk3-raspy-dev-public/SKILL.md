---
name: intake
description: >-
  Turn a goal, meeting notes, a transcript, an email or a `distill` candidate into
  decision records, specification changes and implementable tasks. Works in local
  repositories (decision and task files) and GitHub-backed ones (decision and task
  issues). Use when asked to spec something out, plan work, or turn a request into tasks.
---

# intake

Turn one source into the three records the loop needs: a decision the owner accepts, the
specification lines it changes, and tasks a worker can take without asking. Every task cites the
specification; every change cites its task.

## Which backend

Read the repository's line in `~/.config/dev-platform/repos.conf` (`owner/repo checkout
local|owner|bot [base]`).

- **local** (the default for `new-repo`): decisions are files under `docs/decisions/`, tasks are
  files under `docs/tasks/`, and nothing leaves the machine. `#N` means task N.
- **owner** or **bot**: decisions and tasks are GitHub issues written through
  `<loop skill>/scripts/ghx <owner/repo> issue create ...`, which picks the identity. `#N` means
  issue N.
- Not listed: the `dev-loop` commands will refuse it. Propose the line
  (`<owner>/<name> <checkout> local <base>`) for the owner to add, or work with the files by hand
  in the same format.

## Procedure

1. **Source.** One of: the owner's goal in a sentence or a paragraph; meeting notes, a call
   transcript or an email; a candidate block pasted from `docs/incoming.html` (cite its id). Raw
   records stay in the owner's notes and are never copied into a repository. Refer to them by
   date and type only (`client call, 2026-09-17`); no quotes, no private names.
2. **Read** `docs/spec/SDD.md`, `docs/spec/TDD.md`, `docs/decisions/`, the open tasks
   (`dev-loop tasks <repo>` locally, `gh issue list` otherwise) and the code the TDD names.
3. **Map** each takeaway. Already satisfied: nothing. Contradicted or left open: one decision.
   An empty specification (a new repository) leaves everything open; the first decisions write
   the first requirements, following the conventions at the top of `SDD.md` and `TDD.md`.
4. **Decision drafts.** Context with the spec items quoted, options, consequences, a
   recommendation and the one question the owner answers.
   - local: `docs/decisions/NNNN-<slug>.md` from `0000-template.md`, the next unused four-digit
     number, `Status: proposed`.
   - GitHub: a `decision` issue through `ghx`, on the owner's word.
   Stop here and ask. A goal the owner already stated plainly may be accepted in the same
   conversation; record `Status: accepted` and the date.
5. **Specification change**, after acceptance, on one branch cut from the base
   (`docs/<slug>`; in a worktree when another writer holds the checkout): edit the exact SDD and
   TDD lines, set each touched status to `pending:#<task>`, set the decision's `Spec:` field, and
   append one row to `docs/spec/SPEC-AMENDMENTS.md`.
6. **Cut tasks** from the spec diff, dependency ordered, each small enough for one worker.
   - local: `dev-loop tasks <repo> new "<title>" --scope <prefixes> --depends "#N"|none
     [--labels spec|enhancement|documentation] [--ready]`, run inside the branch's worktree; it
     picks the number and writes the file in `docs/tasks/README.md` format. Replace the body
     with what to build, the acceptance criteria and the SDD/TDD items that govern it. Then
     `dev-loop tasks <repo> check` must report ok.
   - GitHub: issues through `ghx` with the same body plus `Scope:` and `Depends on:` lines, a
     milestone and `needs-triage`; the owner labels them `sprint-ready`.
   Fill the `pending:#<task>` markers with the numbers just assigned.
7. **Check** with `spec-lint` on the branch, then hand over. Local: the owner merges the branch
   into the base in a terminal (`git merge --no-ff docs/<slug>`); the loop sees tasks only on the
   base. GitHub: one draft pull request citing the decision issue.

## Where it runs

The specification is decided before it is built. Intake runs on its own branch from the base and
lands before any goal branch that builds it; a spec change never rides inside a build task, and
the loop's fold refuses a build branch that edits spec text.

- **From zero:** `new-repo --register --personal`, then intake in the new repository with the
  goal as the source: Helm in its project, or Claude Code or Codex opened there (the `ai` menu
  opens any of them in the project). The owner accepts the decision and merges the spec branch;
  then `dev-loop start <repo> <type/slug>` builds it.
- **During a goal:** a worker that finds the spec wrong blocks. The control seat, a policy or
  review seat, or the owner runs intake for that one change and writes it as a task labeled
  `spec`; only that task's branch may change the specification.
- **Many raw notes at once:** `distill` first, then intake on the candidates worth acting on.

Traceability: decision, then the specification change that cites it, then tasks depending on
it, then the worker changes that close them (`Closes #N` in the worker's `.worker-pr.md`).

Keep the scope honest. A simple change the specification already covers goes straight to one
task; do not manufacture decisions or tasks for every thought.
