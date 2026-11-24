---
name: audit-anything
description: >-
  Load this skill when asked to audit work already marked done or shipped that no other audit
  skill owns (merged docs, a plugin), an independent reader checks it, and the findings are
  saved. Trigger on "audit this", "audit X against Y". Not for unfinished work (use
  ceh-every-session:review-anything).
argument-hint: "[subject] [criteria]"
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Uses uv, which runs scripts/artifact.py with Python 3.10+, pydantic 2 and PyYAML, to check and
  render the general audit. Without uv it is read and written unchecked and unrendered.
license: Apache-2.0
---

# Audit anything

Have work that is already marked done or shipped checked by a reader independent of whoever built
it, and save the findings as written. Done when a new audit file is saved, its HIGH findings
checked against their cited places, and the reply gives the findings worst first and the file
path.

## Procedure

1. **Name the subject, then route it.** The subject is the files or folders to audit. A subject
   given only as text in the conversation is not audited: say to save it to a file first, and
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

   - Done: go on to step 2.
   - Not yet done: say in one line that the work is not yet done, so it needs a review, not an
     audit, then Invoke the Skill tool with skill="ceh-every-session:review-anything" and stop
     here. When this skill was itself reached by a hand-over from a review, take the audit kind
     and go on: never hand back, so the two cannot loop.
   - About how the work went, not the work itself: that is a retro. Name
     `ceh-session-learning:diagnose-session` for a session, or the period retro skill of
     `ceh-git-workflow` for a period, and stop.

2. **Settle the criteria and the boundary.** The criteria are the files the user named, otherwise
   the repo's vision, the rule files and `CLAUDE.md` that apply to the subject, otherwise the
   subject's own stated purpose. The boundary is which folders and files are the subject. List
   both in the reply before dispatching.
3. **Dispatch one `ceh-every-session:independent-reader`** in the background, on every run. The
   brief holds the kind `audit`, the subject paths and the criteria, and never an earlier audit
   file. The agent is the independent reader an audit needs: it has not seen the session that
   built the work.
4. **Check what came back.** Read the cited place of every `HIGH` finding, and drop one whose
   place does not say what it claims. Record each dropped finding in `not_covered` with the
   reason, so the saved audit keeps what the reader said, and name it in the reply.
5. **Save a new file on every run**, per Output, never updating an earlier audit. Then run
   `uv run --script ${CLAUDE_SKILL_DIR}/scripts/artifact.py render <file>.yaml`, which writes the
   `.md` beside it, and fix the YAML for each error it lists. Without uv, say that the audit went
   unchecked and unrendered. Reply with the findings worst first, what was not covered, and the
   file path.
6. **Act on findings** only as the next section says.

## Acting on findings

The saved report stays as it is: it records what the audit found, never what came of it. Act only
on the findings the user chooses in this session, and only on those this run did not already fix.
Choosing a finding is the request to fix it, and a fix made directly follows this skill's own rule
on commits. With no user to choose, as in a headless run or a report-only subagent, route nothing:
the report stands, and a calling agent does any routing.

| Finding is                               | Route                                                     |
| ---------------------------------------- | --------------------------------------------------------- |
| A bug in this repo's code or config      | `ceh-coding-conduct:find-root-cause`, writes a fix record |
| A feature or design change in this repo  | `ceh-build-plan:write-build-plan`                         |
| A rule for how work is done in this repo | `ceh-every-session:record-project-decisions`              |
| Anything else in this repo               | Fixed directly, with the check that proves it             |
| Outside this repo                        | Left for the user                                         |

Each chosen finding ends handed off, fixed, or dropped with a reason, and stays open only while it
waits on a user decision: one outside the repo, or a route whose plugin is not installed. A row in
a backlog file the repo names (in its README, `CLAUDE.md` or `AGENTS.md`) counts as handed off, and
an open finding gets one there too. Every plan, fix record, rule or backlog row names the audit
file and the finding as its source, the finding by its `id` where the format has one, else by its
`location`. The reply lists each chosen finding with where it went.

## Rules

- The reader judges cold: it gets the subject and the criteria, never this session's reasoning or
  an earlier audit, so its findings are its own.
- Every saved finding cites a place: `path:line`, or for something missing, the file or folder
  it belongs in.
- With no human present the skill still runs whole, since it asks nothing.

## Output

A `general-audit/v1` file, a copy of `${CLAUDE_SKILL_DIR}/assets/general-audit.template.yaml`,
saved to
`.agents_workspace/product/audit/general/<YYYYMMDD-HHMMSS>-${CLAUDE_SESSION_ID}-<target>.yaml`,
the time from one `date +%Y%m%d-%H%M%S` call, with its `.md` rendered beside it in the layout of
`${CLAUDE_SKILL_DIR}/assets/general-audit.template.md`. Every key, the target name rule and the
ordering rule are in `${CLAUDE_SKILL_DIR}/references/general-audit-schema.md`. The reader's
`<location> | <label> | <comment>` line maps to `location`, `severity` and `finding`, and its
`## Not covered` to `not_covered`.
