---
name: review-build-plan
description: >-
  Load this skill when a build plan or spec exists and nobody has built from it yet, even for a
  quick look before building: review it on scope, engineering, content, design, and developer experience,
  and end with a verdict. Trigger on "review this plan", "just check the phases", "review the
  spec".
argument-hint: "[plan-file]"
compatibility: >-
  Needs uv, which runs scripts/artifact.py with Python 3.10+, pydantic 2 and PyYAML to check a
  plan/v2 plan and render its Markdown, and to check a VISION or STRATEGY YAML before reading it. Without uv the plan is saved unchecked and unrendered, and those files are
  read unchecked.
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Review a Build Plan

Read a plan the way its builder will, before anything is built, and report everything that would
stop the build or send it the wrong way. A plan error caught here costs one edit. Caught in phase
four, it costs every phase built on it. Done means each applicable lens has run, every finding
quotes the plan, and the verdict is delivered.

## Procedure

1. **Find the plans.** Take the paths from the arguments, one or several, or the newest plan in
   the plan folder whose status is `draft` or `ready`, and say which. A slug given in place of a
   path is matched as the format's Location section says. The format is in
   `${CLAUDE_SKILL_DIR}/references/plan-schema.md`. Several plans get one review: steps 2 to 7
   run once over all of them, and each plan gets its own findings, Record entry and saved review. With no plan but a spec (an issue, a PRD, a
   spec file), review the spec with the Scope lens and the gap checks of step 5, and skip what
   concerns phases. With neither, stop: there is nothing to review.

   **A `plan/v2` plan is checked first.** When `<slug>.yaml` sits beside the plan's `.md`, the
   YAML is the plan: read and edit it, never the `.md`. Before acting on it, run
   `uv run --script ${CLAUDE_SKILL_DIR}/scripts/artifact.py check <slug>.yaml`. When it exits 1
   with errors, stop and report them, because a stage that acts on a broken plan builds the wrong
   thing. When its only error is a stale `.md`, run the same command with `render` and go on.
   When it exits 3 or uv is missing, say in the reply that the plan went unchecked, and go on.
   After the last write to the YAML, run `render`.

2. **Review from a fresh context when this session wrote the plans, or a plan already has a
   review file.** Dispatch one background subagent on the session's own model with every plan path
   and `${CLAUDE_SKILL_DIR}/SKILL.md`, told to run steps 3 to 6 on each and return one Output per
   plan, and never give it a review file, so earlier rounds cannot anchor it. One subagent reads
   the shared repo once, where one per plan would read it again for each. The author reads what
   they meant, a fresh reader reads what is written, and only the second is what the builder gets.
3. **Read what the plan rests on**: every file, route, model, and dependency it names in the
   repo. Read no business plan, even when an older plan links to one: the review judges
   the plan against the repo, the vision and the strategy only. A plan claim the repo contradicts
   is a finding. A plan claim that contradicts the repo's `VISION.yaml` or `STRATEGY.yaml` in
   `.agents_workspace/product/`, or its `VISION.md` or `STRATEGY.md` in `docs/`, the root, or
   where the repo's `CLAUDE.md` says, is a finding too. When a
   `VISION.yaml` or `STRATEGY.yaml` sits beside its `.md`, run
   `uv run --script ${CLAUDE_SKILL_DIR}/scripts/artifact.py check <file>.yaml` before reading it
   (formats in `references/vision-schema.md` and `strategy-schema.md`). On exit 1, stop and report its errors, because a review against a
   broken source judges the plan by the wrong standard. On a stale `.md` alone, read the YAML
   instead. On exit 2 or 3, or without uv, say in the reply that the file went unchecked, and go
   on.
4. **Run each lens that applies**, and name the ones you skip with the reason.

   | Lens                     | Applies                                   | Asks                                                                                                                                                                                                                                                                                                                                                     |
   | ------------------------ | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | **Scope**                | Always                                    | Does In deliver the Goal, and is each item needed now? Does the core flow need anything under Out? Is there a cheaper path to the same Goal: an installed library, an existing component, a smaller MVP?                                                                                                                                                 |
   | **Engineering**          | The build includes code                   | Is each phase buildable from the ones before it? Does each Check prove its phase's Builds, or only that something runs? Are timeouts, retries, duplicate requests, and partial writes designed or left open? Do the Design's types rule out illegal states, is each shared value's writer named, and does each module expose only what its callers need? |
   | **Content**              | The deliverable includes documents        | Is each document's reader named, and does In deliver what that reader needs? Is each claim's source decided? Does the structure fit the repo's existing index and numbering? Is each phase buildable from the ones before it? Does each Check prove the content, such as every claim sourced and every link resolving, or only that the file exists?     |
   | **Design**               | The build has a user interface            | Does every screen in scope have its loading, error, and empty state? Does the plan say what the user sees after each action? Is the core flow as short as it can be?                                                                                                                                                                                     |
   | **Developer experience** | The callers are developers: lib, CLI, API | Can a caller reach a first working call from what the plan builds? Are names, error shapes, and defaults decided, or left to the builder? Does a breaking change get a migration path?                                                                                                                                                                   |

5. **Check the gaps every plan is checked for**, whatever the lenses: an In item no phase builds,
   a phase that builds something missing from In, a placeholder (`TODO`, `...`, "adjust as
   needed"), a name spelled two ways, a reference to a file, route, type, or field the plan never
   defines, and any Design item from `write-build-plan` step 5 that applies and is neither
   settled nor deferred.
6. **Grade each finding.** **Blocking**: the build would stop, go wrong, or build the wrong thing.
   **Advisory**: the build succeeds, but worse than it could. Then give the verdict (see Output).
7. **Fix only on request.** By default the review edits no plan content, because the plan belongs
   to its author. It appends one Reviewed entry to the plan's Record (format in the plan format
   file), as a `record` entry in a `plan/v2` YAML or a line under `## Record` in a `plan/v1`
   Markdown plan, so the review stays part of the plan's trail. A spec that is not a plan gets no
   Record line. When asked to fix, edit the plan for each blocking finding whose fix the
   plan or the repo already settles, put a finding that would change In or Out under Open as a
   question with a recommended answer, and set `status: draft` while any blocking finding is open.
   In the review file, set each finding it fixed to `fixed` with the edit as its resolution.

## Rules

- **Quote or suppress.** Every finding quotes the plan line it is about. A missing item names the
  section it belongs in. A finding you cannot anchor goes under Unverified, not in the table.
- **Judge from the plan, not the brief.** A request like "just check the phases" narrows which
  lenses run, never how severe a finding is. Say where the brief asked for less.
- Review only what is unbuilt. In a `building` plan, review the phases still `todo` or
  `unplanned`. A `built` plan is checked against its build by
  `ceh-check-build-against-plan:check-build-against-plan`, not reviewed.
- During the review, turn a question only the plan's owner can answer into a finding with a
  recommended answer.

## Output

The review fills `assets/plan-review.template.yaml`, per the `plan-review/v3` section of
`references/plan-review-schema.md`, one file per plan that every review of the plan adds a round
to. After the last edit, run
`uv run --script ${CLAUDE_SKILL_DIR}/scripts/artifact.py render <file>.yaml`, which writes the
`.md` beside it in the layout of `assets/plan-review.template.md`, and fix the YAML for each error
it lists. Never edit the generated `.md`. On exit 2 or 3, or without uv, say in the reply that the
review went unchecked and unrendered.

| Verdict            | When                                                                               |
| ------------------ | ---------------------------------------------------------------------------------- |
| **Ready to build** | No blocking finding.                                                               |
| **Revise first**   | Blocking findings, each fixable by editing the plan.                               |
| **Rethink**        | A Scope finding changes what to build, or shows the Goal is out of reach as drawn. |

Save the whole review to the plan's review file in `.agents_workspace/product/review/plan/`,
because the Record line keeps only the verdict and counts, and the author fixing the plan in a
later session needs the findings and which are still open. Follow the schema's Review lifecycle:

1. Find the plan's file by its slug. With none, the file is
   `<YYYYMMDD-HHMMSS>-<plan-slug>.yaml`, the time from one `date +%Y%m%d-%H%M%S` call. A found
   `plan-review/v2` file is converted to `v3` in place first.
2. Before merging the new round, re-check each `open` finding against the current plan and set it
   `fixed`, with the resolution `found fixed in round <n>`, where the plan no longer has the
   defect.
3. Append the round, and add its findings with `round: <n>` and `status: open`, skipping one that
   repeats an `open` finding and reopening one that repeats a `fixed` finding.

The main session does this, never the subagent, which returns only its Output. Reply with the
verdict, the blocking findings, the findings still open from earlier rounds, and the path.

## Hands off to

- On **Ready to build**, `ceh-build-plan:implement-from-plan` builds the plan phase by phase.
