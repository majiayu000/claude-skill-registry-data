---
name: write-build-plan
description: >-
  Load this skill before the first edit of a change that has no plan yet: a new app, tool or doc set, a
  feature added to existing code even when it sounds quick, or a multi-file change such as a
  retro's fixes. Writes one plan file. Trigger on "build me X", "add X to the app", "plan this".
argument-hint: "[what to build | <draft plan path>]"
compatibility: >-
  Needs uv, which runs scripts/artifact.py with Python 3.10+, pydantic 2 and PyYAML to check a
  plan/v2 plan and render its Markdown, and to check a VISION, STRATEGY, PRD or ARCHITECTURE YAML
  before reading it. Without uv the plan is saved unchecked and unrendered, and those files are read
  unchecked.
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Write a Build Plan

Turn a request into one plan file that an agent can build from without asking again, in the format
in `${CLAUDE_SKILL_DIR}/references/plan-schema.md`. Done means the plan is saved, audited, and
summarized under Output.

Given the path of a `plan/v2` YAML plan with `status: draft`, or of a `.md` whose frontmatter has
`generated_from: <slug>.yaml`, which resolves to that YAML, complete that plan in place. Another
step, such as a scheduler's intake, may have drafted it with only the goal and the done criteria.
Its goal and every Scope In item stay word for word, and more In items may follow them. Its Design
entries, Open items and record are kept, and step 5 adds entries after them. Its `unplanned`
phases are replaced by the phases step 6 writes. Every step still runs, and step 7 saves to the
same YAML and appends a second Planned entry after the drafter's `Planned: status draft`. A
`plan/v1` Markdown plan with no YAML beside it, or a plan that is not `draft`, is not a completable
draft: say so and write a new plan as usual.

## Procedure

1. **Triage, and announce the label and the deliverable in one line.**

   | Label             | The work                                                                                    | Path                                                  |
   | ----------------- | ------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
   | **Spike**         | Throwaway work to answer one question ("can this library do X?", "does this outline hold?") | No plan. Name the question and stop                   |
   | **Bounded**       | One change inside the existing design: no new component or model                            | A plan of one to three phases                         |
   | **Architectural** | A new app, component, data model, major version, or a new document set or series            | A full plan. A new app gets an MVP boundary in step 3 |

   The label may move up mid-session, never down: a spike that turns into a keeper gets a plan, and
   architectural work keeps its plan when it shrinks.

   The deliverable includes code, documents, or both, read from the request and the repo, never
   asked. Documents count only when they are a deliverable the request names, such as a new
   appendix, guide, deck or analysis. A README, changelog or docstring updated alongside code
   does not. Steps 5 and 6 branch on it, and a build that has both runs both branches.

2. **Read what exists before asking.** When a `VISION.yaml` and `STRATEGY.yaml` exist (in
   `.agents_workspace/product/`, or the `VISION.md` and `STRATEGY.md` in `docs/`, the root, or
   where the repo's `CLAUDE.md` says), read them, and put anything the plan would contradict
   under Open. A plan, vision or strategy found only at the old root `product/`, in a repo whose
   `CLAUDE.md` names no location, is reported with its move (each file under root `product/` to
   the same sub-path under `.agents_workspace/product/`), never read, and never written beside,
   because two folders split the artifacts again. Read the format file, the repo, every plan in the plans
   folder that is not `built`, and only the frontmatter of each `built` one (read its full text
   only when the new work touches what it built), the README, and any issue or spec the user
   named. Read no business plan: take the goal and target user from the request, the vision and
   the strategy, because a business plan's dated tests would become the plan's goal. When a
   `VISION.yaml` or `STRATEGY.yaml` sits beside its `.md`, run
   `uv run --script ${CLAUDE_SKILL_DIR}/scripts/artifact.py check <file>.yaml` before reading it
   (formats in `references/vision-schema.md` and `strategy-schema.md`). On exit 1, stop and report its errors, because a plan built on a
   broken source carries the error into every phase. On a stale `.md` alone, read the YAML
   instead. On exit 2 or 3, or without uv, say in the reply that the file went unchecked, and go
   on.

   **When `.agents_workspace/product/PRD.yaml` exists, plan from its feature.** Check it the same
   way first (format in `${CLAUDE_SKILL_DIR}/references/prd-schema.md`), with the same result on
   each exit code. Match the request to a feature by its `id` or `name`. With a match: the
   feature's `requirements` become Scope In items, each `acceptance` item is covered by a phase
   Check, a `depends_on` feature that is not `built` goes under Open, with its plan in the
   plan's `depends_on` when it has one, and anything the plan would add beyond the feature goes
   under Out. A request that would build a `non_goals` item goes under Open. A request that
   names a `replaced` feature by its `id` or `name` is planned from the feature in its
   `replaced_by`, the first when there are several, with the others named under Open, and the
   reply says which feature replaced it, because a `replaced` entry is history. With no match,
   plan the request as usual and say in the reply that the PRD does not list it, which
   `ceh-product-direction:write-product-requirements` can add.

   **When `.agents_workspace/product/ARCHITECTURE.yaml` exists, read its decisions.** Check it
   the same way first (format in `${CLAUDE_SKILL_DIR}/references/architecture-schema.md`), with
   the same result on each exit code. Read its `technical_design` entries, its `key_decisions`
   whose `status` is `Accepted`, and each diagram marked `planned: true`, which shows where the
   system is going.

   Put whatever is still unclear into **one round** of
   questions, each with a recommended answer. With no human to answer, take each recommended
   answer and list it under Open.

3. **Draw the scope.** Write In and Out. For each candidate item ask: _is this needed to build
   what was asked, now?_ If not, it goes under Out with its reason. For a new app, In is the MVP:
   the smallest set that makes the app usable for its core purpose. If an item can be removed and
   the app still delivers that, it is Out. One plan covers one functionality: a change that lands
   in its own PR and can be checked on its own. When In holds several, split the request into one
   plan each, never into phases of one plan, and run steps 3 to 7 per plan. A plan that needs
   another built first lists it in `depends_on`.

4. **Decide how far to plan in detail.** Plan every phase in full when the build is foreseeable.
   Uncertainty, not size, cuts the detail short: a novel or unproven core mechanic, a decision
   that needs building and seeing first, or an MVP that keeps growing as you discuss it. Then plan
   in full up to the phase that settles the uncertainty, and list the rest as `unplanned`
   one-liners. Detailed phases past an open question are fiction, and building against them
   wastes more than replanning later.

5. **Write the Design.** Only the decisions the phases need, each with its reason. Settle or
   explicitly defer each of these that applies, because each one stops a builder mid-phase when
   it is left open.

   A `technical_design` entry or an `Accepted` decision in `ARCHITECTURE.yaml` binds the plan:
   name the entry by its topic, a part by its topic and title, or the decision by its date and
   title, where a phase relies on it, and do not restate or decide it again. Where a
   `technical_design` entry covers a topic, the entry binds and every `key_decisions` entry on
   that topic is its history. A plan that must depart from one lists it under Open with the
   entry to change or supersede. When the Design would hold a
   decision two or more features share (a stack, a data model, a component boundary) and no
   entry settles it, decide it here as usual and say in the reply that
   `ceh-build-plan:write-technical-design` settles such decisions for the whole product.

   When the build includes code:

   - Auth, and who owns each resource. A resource that exists but belongs to someone else returns
     the same status as a missing one, so the response does not leak that it exists.
   - Pagination on list endpoints, environment variable names, and the migration strategy.
   - Cross-origin requests: allowed origins, and the cookie policy when auth uses cookies.
   - Resources created by an explicit action, never implicitly by the first dependent action,
     which races with a second request arriving before the resource exists.
   - Loading, error, and empty states for every screen that fetches.
   - For an LLM feature: model and provider, how the message list is built from stored messages,
     and what happens when a conversation outgrows the context window.
   - For each new type, function, or module other code calls: its signature with the errors it
     returns, and the file it lives in, named for its concern and never a catch-all (`utils`).
     Then check the shape. Illegal states: name a value each type can hold that the domain
     forbids, and tighten the type or say where it is validated, once. Runs twice: say what each
     write (a row, a file, a message) does on a retry, and make it idempotent or say why it runs
     once. Shared state: name who writes each value two requests or processes touch. Smallest
     interface: a module that exposes most of what it holds hides nothing, so merge or cut it.

   When the deliverable includes documents:

   - The reader, and what they can do after reading that they could not before.
   - Where each claim's source comes from and how it is cited, matching the repo's existing
     citations.
   - Where each new file goes, its name in the repo's numbering, and every index or README that
     must link it.
   - The conventions read from the existing files: heading levels, section order, terms, and date
     style.
   - What a finished document holds: no placeholder, every claim sourced, every link resolving.

6. **Sequence the phases.** Foundations first (data model, auth, or, for documents, the outline
   and the index entries) before the features that use them. No phase relies on anything a later
   phase introduces. Prefer thin vertical slices that leave the deliverable usable, but when a foundation and a slice pull against each other, the
   foundation wins. Give each phase a Check a builder can run. More than six phases is a sign to
   re-run step 4.

7. **Audit, then save.**
   - Every In item is built by some phase, and nothing a phase builds is missing from In.
   - Every phase has a runnable Check, or names its manual check and why.
   - No placeholder (`TODO`, `...`, "adjust as needed"), no reference to a file, route, type, or
     field the plan does not define, and no field named differently in two places.

   Save the plan as `plan/v2`: `<YYYYMMDD-HHMMSS>-<slug>.yaml` in the plan folder, the time from
   one `date +%Y%m%d-%H%M%S` call, a filled copy of
   `${CLAUDE_SKILL_DIR}/assets/plan.template.yaml`, with `status: ready`, or `status: draft` when
   an Open question blocks building, and a Planned entry in its `record`. Leave `depends_on` out
   when the plan needs no other built first. Then run
   `uv run --script ${CLAUDE_SKILL_DIR}/scripts/artifact.py render <file>.yaml` and fix the YAML
   for each error it lists until it exits 0, which writes the `.md` beside it. Never write the
   `.md` by hand: it is generated. When the command exits 3 or uv is missing, say in the reply
   that the plan was saved unchecked and unrendered.

   **Link the plan in the PRD,** only when step 2 matched a feature. Add the plan's repo-relative
   YAML path to that feature's `plans`, unless it is already there, so a second run adds
   nothing. Set the feature's `status` to `planned` when it was `todo` or `built`, since a built
   feature with a new plan is in flight again. Set the PRD's `updated`, then run `artifact.py
render` on `PRD.yaml` as for the plan.

8. **Have them reviewed, once.** After the last plan of the session's batch is saved (the split
   from step 3, or the plans a caller such as a retro asked for), invoke the Skill tool with
   skill="ceh-build-plan:review-build-plan" with every saved plan's YAML path, whatever their
   labels. One review over the batch reads the repo once, which saves the tokens of a fresh reviewer
   per plan. That skill reviews from a fresh context on its own, so do not dispatch a reviewer
   yourself.

## Rules

- One plan per functionality. Leave a `built` plan as written: new work gets a new plan file. A
  draft passed by path is completed, not written again.
- Write only the plan's YAML and, with a matched feature, that feature's `status` and `plans` and
  the PRD's `updated`. Each Markdown is rendered from its YAML.
- Leave every decision that is not needed now under Out or Open, not in Design.

## Output

Close the reply with:

- The label from step 1 and each plan's YAML path, with its `depends_on`, and the PRD feature it
  delivers, or that the PRD lists none.
- The In list, and the phases one line each with their Check.
- Open: every assumption taken without an answer.
- The review's verdict from step 8.

## Hands off to

- `ceh-build-plan:implement-from-plan` builds the plan phase by phase.
