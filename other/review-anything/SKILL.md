---
name: review-anything
description: >-
  Load this skill when asked to review work not yet marked done that no other review skill owns
  (a doc, a design, a rule file, a draft): an independent reader checks it, and the verdict is
  saved. Trigger on "review this", "review X against Y". Not for a diff (use
  ceh-git-workflow:write-code-review).
argument-hint: "[subject] [criteria]"
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Uses uv, which runs scripts/artifact.py with Python 3.10+, pydantic 2 and PyYAML, to check and
  render the general review. Without uv it is read and written unchecked and unrendered.
license: Apache-2.0
---

# Review anything

Have work that is not yet marked done checked by a reader who has not seen the session that wrote
it, and save the result where the next session finds it. Done when the review file is saved, its
findings checked against their cited places, and the reply gives the verdict and the file path.

## Procedure

1. **Name the subject, then route it.** The subject is the files or folders to review. A subject
   given only as text in the conversation is not reviewed: say to save it to a file first, and
   stop. Then look for an owner first, whichever word the user typed:

   | Subject                           | Owner                                                   |
   | --------------------------------- | ------------------------------------------------------- |
   | A build plan not yet built        | `ceh-build-plan:review-build-plan`                      |
   | A built plan against its build    | `ceh-check-build-against-plan:check-build-against-plan` |
   | A diff or PR                      | `ceh-git-workflow:write-code-review`                    |
   | A business plan                   | `ceh-product-direction:develop-business-plan`           |
   | A plan to be questioned in rounds | `ceh-every-session:stress-test-plan`                    |
   | Security of a codebase            | `ceh-security-audit:audit-codebase-security`            |
   | A test suite                      | `ceh-testing:audit-test-suite`                          |
   | An interface                      | `ceh-usability-audit:audit-interface`                   |
   | Error text                        | `ceh-usability-audit:audit-error-messages`              |
   | A first run                       | `ceh-usability-audit:simulate-newcomer-first-run`       |

   For a plan to be questioned in rounds, Invoke the Skill tool with
   skill="ceh-every-session:stress-test-plan" and stop here. For any other owner in the session's
   skill list, load it, follow it, and stop here. When the owner is not installed, say in one line
   which plugin is missing and go on.

   With no owner, decide the kind from the state of the work. It is **done** when it is merged
   into the default branch, published, released, a plan with `status: built`, or the user says it
   is done. It is **not yet done** when it is uncommitted, on a branch that is not merged, a
   draft, or a plan not yet built. When any part of the subject is not yet done, such as a merged
   file with uncommitted edits, the whole subject is not yet done. When the state cannot be told,
   as outside a git repository, the word the user typed decides. Check with `git status` and
   `git log <default-branch> -- <path>`.

   - Not yet done: go on to step 2.
   - Done: say in one line that the work is done, so it needs an audit, not a review, then Invoke
     the Skill tool with skill="ceh-every-session:audit-anything" and stop here. When this skill
     was itself reached by a hand-over from an audit, take the review kind and go on: never hand
     back, so the two cannot loop.
   - About how the work went, not the work itself: that is a retro. Name
     `ceh-session-learning:diagnose-session` for a session, or the period retro skill of
     `ceh-git-workflow` for a period, and stop.

2. **Settle the criteria:** the files the user named, otherwise the repo's vision, the rule files
   and `CLAUDE.md` that apply to the subject, otherwise the subject's own stated purpose. List the
   subject and the criteria in the reply before dispatching.
3. **Dispatch one `ceh-every-session:independent-reader`** in the background, on every run, also
   when this session did not write the subject, so there is one path. The brief holds the kind
   `review`, the subject paths and the criteria, and never an earlier review file.
4. **Check what came back before saving.** Read the cited place of every `blocking` finding, and
   drop a finding whose place does not say what it claims. Record each dropped finding in the
   round's `not_covered` with the reason, and name it in the reply. Then set the verdict from what
   remains: `Done` when no `blocking` finding is left, saying in `verdict_detail` that a finding
   was dropped.
5. **Save the review**, per Output, following the Review lifecycle in
   `${CLAUDE_SKILL_DIR}/references/general-review-schema.md`:
   1. Find the target's file in `.agents_workspace/product/review/general/` by its Lookup rule.
      A found file whose `subject` differs from this subject is not the target's file: save a new
      one whose target ends in `-2`, or the next free number.
   2. In a found file, re-check each `open` finding against the subject as it is now, and set it
      `fixed` with `found fixed in round <n>` where the defect is gone.
   3. Merge the new round: a finding that repeats an `open` one is not added again, and one that
      repeats a `fixed` one reopens it with a note in its resolution.

   Then run `uv run --script ${CLAUDE_SKILL_DIR}/scripts/artifact.py render <file>.yaml`, which
   writes the `.md` beside it, and fix the YAML for each error it lists. Without uv, say that the
   review went unchecked and unrendered. Reply with the verdict, the findings, what was not
   covered, and the file path.

6. **Fix nothing unless asked.** When asked, fix, then set each fixed finding's `status` and
   `resolution` and render again.

## Rules

- The reader judges cold: it gets the subject and the criteria, never this session's reasoning or
  an earlier review, so its findings are its own.
- Every saved finding cites a place: `path:line`, or for something missing, the file or folder
  it belongs in.
- With no human present the skill still runs whole, since it asks nothing.

## Output

A `general-review/v1` file, a copy of
`${CLAUDE_SKILL_DIR}/assets/general-review.template.yaml`, saved to
`.agents_workspace/product/review/general/<YYYYMMDD-HHMMSS>-<target>.yaml`, the time from one
`date +%Y%m%d-%H%M%S` call when the file is first saved, with its `.md` rendered beside it in the
layout of `${CLAUDE_SKILL_DIR}/assets/general-review.template.md`. Every key, the target name rule
and the verdict rules are in `${CLAUDE_SKILL_DIR}/references/general-review-schema.md`. The
reader's `<location> | <label> | <comment>` line maps to `location`, `label` and `comment`, and its
`## Not covered` to the round's `not_covered`.
