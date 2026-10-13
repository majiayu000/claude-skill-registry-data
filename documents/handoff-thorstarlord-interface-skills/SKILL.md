---
name: handoff
description: Use when the user ends a session, asks for a session summary, or needs to create a handoff document for another agent to continue the work.
---

# Handoff

Produce a professional Feature Completion Summary from the current session's git history and conversation context. The output is a markdown file saved to `docs/handoffs/YYYY-MM-DD-feature-name.md` that the next session (or another agent) can read to resume work without replaying the entire conversation.

Data sources in priority order:
1. **Git log** — `git log --oneline -20` (commit history)
2. **Git diff** — `git diff --stat HEAD~N` (changed files)
3. **Conversation context** — what the agent remembers from this session
4. **Test results** — `python -m pytest tests -q --tb=no` (final pass/fail count)

## Output Format

Write the output file to `docs/handoffs/YYYY-MM-DD-feature-name.md`. Create `docs/handoffs/` if it doesn't exist. Use this template:

```markdown
---
type: handoff
session: [feature-name]
date: [YYYY-MM-DD]
status: GREEN | RED
next_task: [single next technical task, 5-8 words]
---

# Session Summary — [Feature Name]

## Commits

[Numbered list of commits on the working branch, newest first.
 Include short hash + message for each.]

## Files Modified/Created

[Bold each file path; one-line description of what changed.]

## Verification

[Exact command the next agent should run to confirm the repository is green before starting work.]

```bash
python -m pytest tests -q --tb=no
```

[Expected output: X passed, Y failed.]

## Global Status

Ran full test suite: X passed, Y failed, Z warnings.
Global status: GREEN | RED

## Architectural Decisions

[Bullet list of key decisions with the choice, rationale, AND the alternative considered.
 Format:
 - **Decision**: [what was decided]
   **Why**: [rationale, trade-offs, constraints]
   **Alternative**: [the rejected option and why it was rejected]
]

## Locked ADRs

[Explicit list of ADRs that govern this architecture. No deviations permitted without a new ADR.]

- ADR-0001: [title] — [one-sentence scope]
- ADR-0002: [title] — [one-sentence scope]

## Frontier

[The single next technical task for the next session.
 Be specific enough that the next agent can start without context.
 Include file paths, function names, and the expected approach.]

## Blockers (if any)

[Things that are stuck, why, and what would unblock them.]

## Agent Re-hydration Block

[3-sentence paragraph. Copy-paste this into a brand-new chat session to instantly restore context.]

I am starting a new session. Load the `handoff` skill and read `docs/handoffs/YYYY-MM-DD-feature-name.md` to understand the current state and the Frontier, then begin the next task on the list. Before making any changes, run `python -m pytest tests -q --tb=no` to confirm the repository is GREEN.
```

## Workflow

### 1. Gather Evidence

Run in parallel where possible:

- `git log --oneline -20` — recent commits on current branch
- `git diff --stat HEAD~1` — changed files in the latest commit (or HEAD~N for N commits)
- `git status --short` — any uncommitted changes
- `python -m pytest tests -q --tb=no` — final test count

If the session spans multiple branches, run `git branch --show-current` first.

### 2. Extract Architectural Decisions

Scan the conversation context for moments where a trade-off was made and a specific choice was locked. Look for:

- "We decided X instead of Y because..."
- "The trade-off is..."  
- "The alternative considered was..."
- Explicit "Decision" markers from ADRs or grilling sessions

For each decision, explicitly name the **Alternative Considered** and why it was rejected. This prevents the next agent from re-suggesting the rejected option.

Aim for 3-5 decisions per session.

### 3. Identify Locked ADRs

Scan the conversation and `docs/adr/` directory for ADR files. List every ADR that governs the area being handed off. The "Locked ADRs" section makes it explicit to the next agent: "These decisions are frozen. Do not deviate without a new ADR."

### 4. Identify the Frontier

The frontier is the single next concrete task. It must name:

- The file to modify (or create)
- The function or class to implement
- The expected approach (one sentence)
- The test to write (one sentence)

Example: "Implement `apply_proposal_to_blueprint()` in `src/auteur/structure/proposal_application.py` — the function takes a `StructureProposal` with a selected option and mutates the `StoryBlueprint` accordingly. Write a test that verifies the blueprint's `story_engine` field is populated after applying a `preserve_intent` option."

### 5. Write the Re-hydration Block

Write a 3-sentence paragraph that the user can copy-paste into a brand-new chat session. It must:

1. Instruct the agent to load the `handoff` skill and read this handoff file
2. Point to the Frontier as the next task
3. Include the verification command to run before starting

### 6. Create Directories and Save

Create the directory with `exec_shell("mkdir -p docs/handoffs")`.

Save the assembled document with `write_file` to `docs/handoffs/YYYY-MM-DD-feature-name.md`.
All file paths in the handoff MUST be relative (e.g. `docs/handoffs/file.md`). NEVER use absolute `file:` paths — they break when the repository is cloned to a different machine or directory.

### 7. PERSISTENCE CHECK — Mandatory Verification

After saving, you MUST verify the file was physically written to disk. Announcing the file without triggering the tool is a FAILURE.

1. Run `exec_shell` to list the directory: `ls -la docs/handoffs/` or `dir docs\handoffs\`
2. Confirm the file exists and its size is greater than 0 bytes
3. If the file is missing or empty: stop, diagnose why the tool call failed, call `write_file` again, and re-verify

The handoff is not complete until the file is confirmed on disk. A handoff that only exists in the session transcript has zero value across sessions.

DO NOT announce completion until the file path is confirmed via `list_dir` or `exec_shell` output.

## Common Mistakes

- **Writing from memory alone** — always run `git log` and test counts. Don't rely on what you remember.
- **Vague frontier** — "Finish the feature" is not a frontier. Name the file, the function, and the test.
- **Omitting blockers** — if something is incomplete, say so explicitly with the reason.
- **No test count** — always run `pytest` and report the exact number.
- **Missing Alternative Considered** — every decision needs a rejected alternative. The next agent WILL suggest it.
- **No re-hydration block** — the handoff is for humans + agents. Without the block, the agent starts cold.

## When Not to Use

- For project-wide documentation (use `docs/architecture.md` instead)
- For bug reports or issues (use GitHub Issues instead)
- For personal notes not intended for another agent