---
name: review-build-plan
description: >-
  Load this skill when a build plan or spec exists and nobody has built from it yet: review it on
  scope, engineering, design, and developer experience, and end with a verdict. Trigger on "review
  this plan", "is this plan ready to build", "review the spec".
argument-hint: "[plan-file]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Review a Build Plan

Read a plan the way its builder will, before any code exists, and report everything that would
stop the build or send it the wrong way. A plan error caught here costs one edit. Caught in phase
four, it costs every phase built on it. Done means each applicable lens has run, every finding
quotes the plan, and the verdict is delivered.

## Procedure

1. **Find the plan.** Take the path from the arguments, or the newest plan in the plans folder
   whose status is `draft` or `ready`, and say which. The format is in
   `${CLAUDE_PLUGIN_ROOT}/references/plan-format.md`. With no plan but a spec (an issue, a PRD, a
   spec file), review the spec with the Scope lens and the gap checks of step 5, and skip what
   concerns phases. With neither, stop: there is nothing to review.
2. **Review from a fresh context when this session wrote the plan.** Dispatch one background
   subagent on the most capable model with the plan path and `${CLAUDE_SKILL_DIR}/SKILL.md`, told
   to run steps 3 to 6 and return the Output. The author reads what they meant, a fresh reader
   reads what is written, and only the second is what the builder gets.
3. **Read what the plan rests on**: every file, route, model, and dependency it names in the
   repo, and the business plan when `business_plan` is set. A plan claim the code contradicts is a
   finding.
4. **Run each lens that applies**, and name the ones you skip with the reason.

   | Lens                     | Applies                                   | Asks                                                                                                                                                                                                         |
   | ------------------------ | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
   | **Scope**                | Always                                    | Does In deliver the Goal, and is each item needed now? Does the core flow need anything under Out? Is there a cheaper path to the same Goal: an installed library, an existing component, a smaller MVP?     |
   | **Engineering**          | Always                                    | Is each phase buildable from the ones before it? Does each Check prove its phase's Builds, or only that something runs? Are timeouts, retries, duplicate requests, and partial writes designed or left open? |
   | **Design**               | The build has a user interface            | Does every screen in scope have its loading, error, and empty state? Does the plan say what the user sees after each action? Is the core flow as short as it can be?                                         |
   | **Developer experience** | The callers are developers: lib, CLI, API | Can a caller reach a first working call from what the plan builds? Are names, error shapes, and defaults decided, or left to the builder? Does a breaking change get a migration path?                       |

5. **Check the gaps every plan is checked for**, whatever the lenses: an In item no phase builds,
   a phase that builds something missing from In, a placeholder (`TODO`, `...`, "adjust as
   needed"), a name spelled two ways, a reference to a file, route, type, or field the plan never
   defines, and any Design item from `write-build-plan` step 5 that applies and is neither
   settled nor deferred.
6. **Grade each finding.** **Blocking**: the build would stop, go wrong, or build the wrong thing.
   **Advisory**: the build succeeds, but worse than it could. Then give the verdict (see Output).
7. **Fix only on request.** By default the review edits no plan content, because the plan belongs
   to its author. It always appends one Reviewed line to the plan's `## Record` (format in the plan
   format file), so the review stays part of the plan's trail. A spec that is not a plan gets no
   Record line. When asked to fix, edit the plan for each blocking finding whose fix the
   plan or the code already settles, put a finding that would change In or Out under Open as a
   question with a recommended answer, and set `status: draft` while any blocking finding is open.

## Rules

- **Quote or suppress.** Every finding quotes the plan line it is about. A missing item names the
  section it belongs in. A finding you cannot anchor goes under Unverified, not in the table.
- **Judge from the plan, not the brief.** A request like "just check the phases" narrows which
  lenses run, never how severe a finding is. Say where the brief asked for less.
- Review only what is unbuilt. In a `building` plan, review the phases still `todo` or
  `unplanned`. A `built` plan is checked against its code by
  `ceh-check-build-against-plan:check-build-against-plan`, not reviewed.
- During the review, turn a question only the plan's owner can answer into a finding with a
  recommended answer.

## Output

```markdown
## Plan review: product/plans/<slug>.md

**Verdict:** Revise first
**Lenses:** Scope, Engineering, Design. Skipped developer experience: no developer callers.

| #   | Lens        | Severity | Plan line                     | Finding                                   | Fix                                         |
| --- | ----------- | -------- | ----------------------------- | ----------------------------------------- | ------------------------------------------- |
| 1   | Engineering | blocking | Phase 3 Check: "the app runs" | Proves nothing about the import it builds | `uv run pytest tests/test_import.py` passes |
| 2   | Scope       | advisory | In: "CSV and XLSX import"     | XLSX serves no user named in Goal         | Move XLSX to Out until a user asks          |
```

| Verdict            | When                                                                               |
| ------------------ | ---------------------------------------------------------------------------------- |
| **Ready to build** | No blocking finding.                                                               |
| **Revise first**   | Blocking findings, each fixable by editing the plan.                               |
| **Rethink**        | A Scope finding changes what to build, or shows the Goal is out of reach as drawn. |

Below the table: the questions for the plan's owner, each with a recommended answer, the
Unverified findings, and, in fix mode, what was edited and what was left open.

Save the whole review to `.agents_workspace/plan-reviews/<slug>-<YYYY-MM-DD>.md`, because the
Record line keeps only the verdict and counts, and the author fixing the plan in a later session
needs the findings. Reply with the verdict, the blocking findings, and the path.

## Hands off to

- On **Ready to build**, when `ceh-build-from-plan` is installed,
  `ceh-build-from-plan:implement-from-plan` builds the plan phase by phase.
