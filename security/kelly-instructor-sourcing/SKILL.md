---
name: kelly-instructor-sourcing
description: Run a Busabase-backed sandbox desk for scoring and triaging course-instructor ("讲师") candidates found on a recruiting-style platform. Use whenever the user invokes $kelly-instructor-sourcing or /kelly-instructor-sourcing, wants a lightweight instructor candidate tracker, needs to score sourcing-platform leads against a three-axis rubric (background endorsement, expertise depth/breadth, teaching-service ability) before reaching out, or wants to log a WeChat add without building a live-connected outreach tool. Three subcommands - setup, criteria, review - plus the desk itself. v1 is sandbox-only — every dataset is deterministic mock data, it never connects to a real sourcing-platform or messaging account, and it never sends a message or automates a WeChat add - that stays entirely human-performed outside the app.
metadata:
  category: sales-crm
  tags:
    - risk:sandbox
    - surface:busabase
    - industry:education
  busabase:
    template: true
    folderSlug: kelly-instructor-sourcing
    resources:
      - criteria
      - candidates
    risk: sandbox

---

# Kelly Instructor Sourcing

Turn a rough "who are we looking for" hypothesis into a scored, triaged pool of
講師/instructor candidates: capture the search criteria and a three-axis
scoring rubric, score each candidate a human found on a recruiting-style
platform, and record the connection state as it happens in the real world.
Everything in v1 is sandbox-only — see Product Boundary.

## Subcommands

| Invocation | What to do |
| --- | --- |
| `/kelly-instructor-sourcing setup` | Create or adopt the Busabase Folder and two Bases, then verify them. |
| `/kelly-instructor-sourcing criteria` | Capture or edit the search-criteria hypothesis and the three-axis scoring rubric. |
| `/kelly-instructor-sourcing review` | Enter or update candidate leads, score them against the rubric, and move them through the queue. |
| `/kelly-instructor-sourcing` | Open the desk and report the current bounded next step. |

Run `setup`, then `criteria`, then `review` the first time. Afterwards,
`review` repeats as new candidates surface. There is no `send` subcommand:
first-stage scope is 获取信息 → 建立连接 → 录入数据 only, and the actual
WeChat exchange happens manually outside this app — `review` records that it
happened, it never performs it.

## Dependencies

Before changing the app:

1. Read `$kelly-app-skill-creator` for product behavior, responsive UI, and the canonical `content/kelly-instructor-sourcing-app/` artifact.
2. Read `$busabase` for target Space, ChangeRequests, review, merge, and Vault behavior.
3. Read `$busabase-app-creator` for runtime, SDK, security, validation, and AirApp deployment.
4. Read `references/instructor-sourcing-schema.md` before changing fields, statuses, or the scoring rubric shape.

If a dependency is unavailable, finish deterministic local artifact work but
stop before its Busabase or AirApp operation and name the missing dependency.
Never introduce a second backend.

## Product Boundary

- **Sandbox only, deterministic data only.** `?demo=1` seeds a fixed set of
  fictional candidates and a fixed criteria record. No live scraping, no real
  candidate data, and no real platform or messaging credential exists
  anywhere in this skill.
- **Never connects to a real sourcing-platform account.** This skill does not
  authenticate against, browse, or automate any recruiting-style platform.
  That integration is explicitly out of scope until its automation
  boundaries, account-safety limits, and personal-data handling rules have
  been researched and confirmed — none of which has happened yet.
- **Never sends a message and never automates a WeChat add.** Guiding a
  candidate to WeChat and adding them is entirely human-performed outside
  this app. The app's only job once a human tells it that happened is to
  record the date on that candidate's own row.
- **Scope is 获取信息 → 建立连接 → 录入数据 only.** Post-cooperation scoring,
  meeting booking, and call/session recording or archiving are out of scope
  for v1 and must not be implied by any screen or copy.
- **Score what a human already assessed.** The three-axis rubric
  (endorsement, expertise, teaching-service) exists so a human's judgment is
  captured consistently, not so the app infers a score on its own.
- **Every candidate carries its scoring evidence.** `match-notes` is
  human-editable free text explaining the scores; do not auto-generate
  scoring text that was not reviewed by a person.

## Product Overlay

- **Research** — candidate discovery. v1 is manually or demo-seeded only;
  there is no live scraping. This represents 获取信息.
- **Plan** — score each candidate 0-100 on three rubrics (endorsement,
  expertise, teaching-service), derive an overall score, and hold a
  `screening` attention queue of candidates still needing a decision.
- **Action** — a human marks a screened candidate `qualified` or
  `not-qualified`; later, once a real-world WeChat add has actually happened
  outside the app, the human records it and the candidate moves to
  `connected`. Writing that record into Busabase is 录入数据 — there is no
  separate send step.
- **Retrospective** — out of scope for v1. No post-cooperation scoring,
  meeting outcomes, or call archiving.

## `/kelly-instructor-sourcing setup`

Confirm the Space first. Setup is idempotent and resolves resources from the
declared Folder; nobody copies Node IDs into config. Re-read after every
ChangeRequest and report a pending CR rather than claiming the workspace
exists. In demo mode (`?demo=1`) no Busabase connection happens at all.

## `/kelly-instructor-sourcing criteria`

Capture or update, in the `kelly-instructor-sourcing-criteria` record:

- the search-keyword and experience/activity filter hypotheses;
- plain-language "what good looks like" text for each of the three rubric
  axes (endorsement, expertise, teaching-service);
- the overall `qualify-threshold` a candidate's score must clear to be
  marked `qualified` by a human.

Put uncertainty into the rubric text; never present a filter hypothesis as a
confirmed platform capability.

## `/kelly-instructor-sourcing review`

For every candidate record in `kelly-instructor-sourcing-candidates`:

- name, public platform headline, and which search context surfaced them;
- a 0-100 score per rubric axis, with `match-notes` explaining the evidence;
- the derived overall score;
- current `status`.

A human marks `qualified` or `not-qualified` once all three axis scores are
recorded. Once a human has actually added the candidate on WeChat outside
this app, `review` records `wechat-added-at` and then `connected` with
`logged-at`. Never skip straight to `connected` without a recorded
`wechat-added-at` — that field is the evidence the real-world step happened.

## Busabase Resources

| Resource | Purpose |
| --- | --- |
| `kelly-instructor-sourcing-criteria` | One search-criteria hypothesis and the three-axis scoring rubric text, plus the qualify threshold. |
| `kelly-instructor-sourcing-candidates` | One row per candidate with headline, search context, per-axis and overall scores, notes, status, and connection timestamps. |

See `references/instructor-sourcing-schema.md` for exact field slugs and
status transitions.

## Screens

- `#/criteria` — search-criteria hypothesis and the three rubric axes,
  editable.
- `#/all` — every candidate, list/detail, sorted so `screening` candidates
  needing a decision surface first.
- `#/qualified` — candidates a human has marked `qualified`, whether or not
  a WeChat add has been recorded yet.
- `#/connected` — candidates with a recorded real-world WeChat add.
- `#/settings/<tab>` — commands, guide, resources, and connection.

## Stop Conditions

Stop rather than guess when the search criteria or rubric text is missing; a
candidate lacks a required field or an axis score before a qualify/reject
decision; a candidate is marked `connected` without a recorded
`wechat-added-at`; the target Space is ambiguous; or a required dependency is
unavailable. Never attempt a real connection to a sourcing platform or a
messaging channel from this skill — that boundary is unresearched and out of
scope for v1.

## App Contract

- Keep the canonical Hono project in `<skill-root>/content/kelly-instructor-sourcing-app/`; use the same source
  locally and in AirApp.
- Store criteria and candidates only in Busabase through `busabase-sdk`.
- Demo data (`?demo=1`) is explicit, deterministic, non-persistent, and
  cannot write anywhere — mutations only touch an in-memory array.
- There is no send/execution path in v1 at all: no outbound message, no
  platform automation, and no messaging credential anywhere in this skill.
- Keep the desktop sidebar/list/detail shell, true mobile list/detail flow,
  hash routes, and responsive Help & Settings from the creator contract.
