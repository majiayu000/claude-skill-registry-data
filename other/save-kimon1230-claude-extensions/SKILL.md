---
name: save
description: Save all session progress to status tracking files. Use when you want to checkpoint work mid-session or before ending.
risk: safe
---

# Save Progress

This skill must only be invoked from the main session, never from a subagent.

1. **Determine the project name** (used for file paths in all later steps):
   a. If a `~/.claude/status/*/session-progress.md` was written earlier this session, reuse that project name.
   b. Else if inside a git repo with a remote, use the `origin` remote. Parse the last path component, stripping any trailing `.git` (e.g., `my-lib` from `git@github.com:user/my-lib.git` or `https://github.com/user/my-lib.git`).
   c. Else use the basename of the git root (`git rev-parse --show-toplevel`).
   d. Else use the basename of the current working directory.
   e. If still ambiguous, ask the user.

2. **Capture test state** (do NOT run tests yourself — a Stop hook already runs pytest automatically):
   - If tests ran recently in this session, reference those results (pass/fail counts).
   - If no test results are available, record "No test results available this session."
   - Do NOT invent results.

3. **Create the directory** `~/.claude/status/<project-name>/` if it does not exist.

4. **Write/update** `~/.claude/status/<project-name>/session-progress.md` with:
   - **Timestamp**: `YYYY-MM-DD HH:MM UTC`
   - **Current task**: what you were working on
   - **Completed**: detailed progress using typed entries. Each entry is classified and formatted as follows:

     **Entry types:**
     - **Decision**: The change involved choosing between alternatives or a non-obvious approach. MUST include a `Why:` line.
     - **Observation**: A factual record of what happened with no meaningful alternatives considered. Plain body, no `Why:` required.
     - When in doubt, prefer `decision` — better to over-document rationale than lose it.

     **Entry format:**
     ```markdown
     ### [decision] Title describing the choice <!-- id:a1b2c3d4e5f6a7b8 -->
     Why: Rationale for this decision (SACRED — never compress or paraphrase).
     What: Implementation details (optional).

     ### [observation] Title describing what happened <!-- id:e5f6a7b8c9d0e1f2 -->
     Plain body text describing the change.
     ```

     **Entry IDs:** Generate a unique ID for each new entry — 16 hex characters (e.g., `a1b2c3d4e5f6a7b8`). Just produce a random-looking 16-char hex string.

     **Appending to existing files:** When updating an existing `session-progress.md`, preserve all existing entries verbatim — only append new ones.

     **Auto-captured entries:** If a `## Auto-captured` section exists (added by the auto-capture hook), review those entries:
     - Promote useful ones to the main **Completed** section.
     - Upgrade observations to decisions with a `Why:` line where appropriate.
     - Remove the `## Auto-captured` section after processing.

     **Entry body content** — draw from these details as appropriate:
     - **Per-batch/phase breakdown** when following a plan — what each batch accomplished
     - **Files created, modified, or deleted** — explicit paths (e.g., `src/foo/bar.py` — added `MyClass`, refactored `process()`)
     - **Implementation specifics** — functions, classes, modules, config options added or changed
     - **Issues encountered and workarounds** — anything the next session should know about (e.g., "ruff F401 requires atomic edits", "had to retry due to X")
     - **Prior session context** — when resuming multi-session work, summarize what earlier sessions completed so the file is self-contained
   - **Remaining**: bullet list of what's left, with enough detail to pick up without re-reading the plan
   - **Test state**: from step 2
   - **Key decisions**: any architectural or design choices made
   - **Active plan**: path to the current plan file in `~/.claude/plans/<project-name>/`, or "None"
   - **Context needed to continue**: anything a fresh session needs to know (key file paths, uncommitted state, critical checkpoints, next batch to start)

5. **Update or create** `~/.claude/status/<project-name>/project-status.md` — the cumulative project history across all sessions:

   **If the file does not exist**, create it with these sections (adapt to the project):
   - **Overview**: one-line project description
   - **Last Updated**: timestamp
   - **Version History**: table of released versions with features (if applicable)
   - **Phase Progress**: table of completed items with status and key files touched
   - **Plans on Disk**: paths to active/completed plan files with status
   - **Test Results**: latest pass/fail/skip counts, coverage, lint status
   - **Next Steps**: what comes next
   - **Deferred Work**: backlog items with references to where they're documented
   - **Git State**: uncommitted changes summary (user handles git)

   **If the file already exists**, read it first and update the sections that changed this session:
   - Add new rows to phase/version tables for completed work
   - Update test results with latest counts
   - Update plans on disk (add new plans, mark completed ones)
   - Update next steps to reflect current state
   - Update git state if relevant
   - Update last updated timestamp
   - Do NOT delete or rewrite sections that haven't changed
   - If the file uses different section names, match its existing structure — don't force the template above

6. Confirm to the user what was saved and where.
