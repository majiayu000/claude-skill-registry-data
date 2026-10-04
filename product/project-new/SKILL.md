---
name: project-new
description: Start a new product from zero with the Keelokit harness — intake interview, PRD, stack decision, monorepo skeleton with CI and staging from day 1, and the first backlog. Use when the user says "nuevo producto", "arrancar un proyecto", "kickstart", "quiero construir una app", "armá el proyecto", "new product", or when /keelokit finds no project and the user wants one. Resumes from the pending gate when .keelokit/state.toml exists.
---

# Kickstart — five gates from idea to a working skeleton

| Gate | Output | Human |
|---|---|---|
| 1 intake | `docs/context/` | approves the context |
| 2 product | `docs/prd.md` | approves scope and metrics |
| 3 stack | `docs/stack.md` (apps chosen and why); `docs/decisions/` only for deviations | approves the apps and any deviation |
| 4 skeleton | generated monorepo, `pnpm verify` green, first commit | nothing (unless setup needs their accounts) |
| 5 backlog | `backlog/` with epics, stories, development waves | approves the order |

Rules for the whole run:
- Interview in the user's language; write files in English unless the user asks otherwise.
- The user may be a founder who has never run a software project, let alone agents. The first
  time a term of art comes up (PRD, stack, epic, story, development wave, worktree, invariant,
  gap, staging), explain it in one plain sentence. In Spanish, waves are **olas de desarrollo**.
- The dashboard (`/keelokit:project-dashboard`) is the user's view of the whole run: show it at the
  start, refresh it when a gate's output is ready and after each approval.
- **Never ask for an approval without showing what is being approved.** At each gate: refresh
  the dashboard, give its link and the section (`#stage-<gate>`), and summarise in the chat what
  the approval covers (the lists below). Then ask.
- After each approval, record it in `.keelokit/state.toml` under `[gates]` as
  `<gate> = "<YYYY-MM-DD>"` (`"<YYYY-MM-DD> auto"` when automatic mode approved it). That file
  holds the approvals, the run decisions (`[run]`) and the dashboard's settings (`[dashboard]`:
  `lang`, `url`), nothing else.
- Between gates report progress in one line and continue; stop only at the approvals above —
  and in automatic mode, only where a person is required (below).
- Resume: if `.keelokit/state.toml` exists, continue from the first gate without a date, and
  open the dashboard first so the user sees where the run stopped.

## 0. Where

Ask for the product's name and one sentence of what it is, and propose the folder
`~/Development/<slug>`, where the slug is the name as the template derives it: lowercase ASCII
(accents folded: "Peña S.A." → `pena-s-a`), anything else a dash, and `app-` in front when it
would start with a digit or be empty ("3D Store" → `app-3d-store`). Create it (empty) once the
user agrees. If it exists and is not empty, ask before using it.

Create `.keelokit/state.toml` with `[dashboard] lang = "<the user's language code>"`.

Then settle the two run decisions — **once per project**, with the multiple-choice tool and a
recommendation, explained in plain words:

1. **Run mode.** *Stage by stage* (recommended for a first project): Keelokit stops at the end of
   every stage for the user to review and approve it, and between stories. *Automatic*: it goes
   on alone and stops only where a person is required — the questions only the user can answer
   (the interview, blocking gaps), approving the PRD's scope and metrics or a stack deviation,
   accounts and credentials, and everything `.keelokit/harness/execution-protocol.md` reserves
   for the human (production, money, legal, deleting data, paid services). Every automatic
   approval is recorded and stays reviewable on the dashboard.
2. **How stories are built.** *One at a time* or *in parallel, up to N at once* (2–4); see Close
   for how to explain it.

Record them:
```toml
[run]
mode = "step"        # or "auto"
build = "serial"     # or "parallel"
parallel = 3         # only with build = "parallel"
decided = "<YYYY-MM-DD>"
```
These are fixed: no skill asks them again or changes them on its own. Only an explicit request
from the user changes one (update the value and `decided`, and say so in one line).

Open the dashboard: it shows the stages ahead and these decisions, so the user knows the whole
road before the first question.

**Automatic mode** approves, by itself, the gates no rule reserves for a person — context (only
with no blocking gap open), stack (only with no deviation from the house stack), skeleton and
backlog — records them as `"<date> auto"`, refreshes the dashboard, reports in one line and goes
on. The PRD is always the user's approval. After the backlog it continues straight into
`/keelokit:build-story` with the recorded build mode.

## 1. Intake

Run `/keelokit:plan-intake` in the new folder. When it finishes, refresh the dashboard and show in the
chat: the problem and users in two lines, the invariants (rules that must never break), and the
open gaps with who answers each, blocking first. Then ask for approval. Blocking gaps can stay
open only if the user explicitly accepts them.

## 2. Product (PRD)

Before writing it, say what a PRD is: the Product Requirements Document — what the first version
builds, what it deliberately leaves out, and which numbers will say it worked; what isn't in it
doesn't get built.

Write `docs/prd.md` from the context using `references/prd-template.md`. Every metric has a
number and a date; every scope line is either in or out. Anything the context doesn't support
becomes a gap in `docs/context/gaps.md`, not an assumption. Refresh the dashboard and show in the
chat the **scope** (every in and out line) and the **metrics** (metric, target, date). Then ask
for approval.

## 3. Stack

First, what kind of project this is, from the PRD: a product people use (web, mobile, an API
others call), or something developers use (a library, a CLI, a plugin, a template). The template
builds products. For a developer-facing kind it would only add apps, a database and hosting the
project doesn't need: say so, and instead start a minimal repo (`git init`, README, the context
and PRD already written) and bring the harness in with `/keelokit:project-adopt`, which writes
the profile and applies only the rules that fit.

For a product, the house stack is fixed (`${CLAUDE_PLUGIN_ROOT}/template/.keelokit/harness/stack.md`). Decide
only:
- **apps** — any of `api`, `web`, `mobile`, `site`, justified from the PRD's users and channels;
- **postgis** — only if the domain has geospatial queries.
If a requirement truly can't be met by the house stack, write `docs/decisions/0001-<title>.md`
(Status, Context, Decision, Consequences) and get approval. "Would be nicer" is not a reason.

Nothing more than the PRD needs: no API if nothing is stored or shared, no mobile app if the web
works on phones, no public site if there's nothing to say before sign-up. The skeleton writes
`.keelokit/profile.toml` from the apps; add `personal-data` and `payments` to its `traits` when
the context says so.

Write `docs/stack.md`: the apps chosen, one line each on why (citing the PRD's users and
channels), the apps left out and why, PostGIS yes/no, and any decision record. Refresh the
dashboard, show the same in the chat in plain words (what each app is for the user: "a web app
the receptionist opens on the phone", not "Vite + React"), and ask for approval.

## 4. Skeleton

1. Template source: `$KEELOKIT_TEMPLATE` if set (a fork: `gh:<you>/keelokit`), otherwise
   `gh:leosimini/keelokit`, at the plugin's version tag (`v` + `version` from
   `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`). If git can't reach it (offline), use
   `${CLAUDE_PLUGIN_ROOT}` and warn that the project can't `/keelokit:harness-upgrade` until its
   `.keelokit/answers.yml` `_src_path` points at a git source.
2. Generate into the product folder (existing `docs/` is kept):
   ```bash
   uvx copier==9.18.2 copy --defaults --vcs-ref v<version> --data project_name="<name>" \
     --data description="<one sentence>" --data 'apps=["api","web"]' --data postgis=false \
     "${KEELOKIT_TEMPLATE:-gh:leosimini/keelokit}" <folder>
   ```
   Copier derives the package slug from the name (as in step 0). Add
   `--data project_slug=<slug>` only for one the user chose, and only if it starts with a letter
   and has nothing but lowercase letters, digits and dashes: `--defaults` never asks again, so
   copier stops with a traceback on any other.
3. `git init -b main`, `pnpm install`, then `pnpm verify` and `pnpm mutation --all`. Fix until
   green — the fix belongs in the generated project only if it is product-specific; if the
   template itself is wrong, say so: it must be fixed in Keelokit.
4. First commit, of everything (`git add -A`: `pnpm-lock.yaml` included, or `pnpm verify` can't
   compare it with origin/main): `chore: skeleton from Keelokit v<version>`.
   With a `mobile` app, the template writes `[local]` in `.keelokit/profile.toml` and a
   `run:local` script: mention that `/keelokit:run-local` (or `pnpm run:local`) launches the app and
   its API on a phone or a simulator, and offer it once the skeleton is green.
5. Ask whether to create a private GitHub repo (`gh repo create <slug> --private --source . --push`).
6. Staging: the API deploys to Fly.io from CI. Offer `/keelokit:ship-setup` now: it writes the
   deploy guide, does what needs none of the user's credentials and verifies each step. The Fly
   account, logins, payment and third-party keys stay the user's; never type credentials yourself. Record the gate even if staging setup is deferred, and add a
   non-blocking gap "staging not configured" (owner: user).

## 5. Backlog

Run `/keelokit:plan-backlog`. Refresh the dashboard: it shows the stories by development wave and by
epic. In the chat, list the epics and, per wave, its stories (id and title), plus any story
waiting for a gap. Ask for approval of the epics and the wave order.

## Close

Report in five lines: what exists, `pnpm verify` status, open gaps by owner, the first ready
story, and what needs the user (accounts, approvals). Refresh the dashboard. Mention once that the project
carries a small "Built with Keelokit" credit (README badge, a line at the foot of the public site)
and that the dashboard's footer turns it down or off.

Then, in stage-by-stage mode, offer to start building with the recorded build mode; in
automatic mode, start. When explaining the build modes (at step 0), use plain words (the
dashboard's "How to build" section says the same):
- **One at a time** (`/keelokit:build-story`): one story is built, tested and lands before the next.
  Slower; the user follows every step and Claude usage is spread out. Recommend it for the first
  wave, for sensitive stories and for a first project with agents.
- **In parallel** (`/keelokit:build-story <N>`): N ready stories of the same wave at once, each in its
  own copy of the repo (a worktree) with its own agents. Faster, more Claude usage at the same
  time, several results to review together. Safe because stories in a wave never touch the same
  files.
