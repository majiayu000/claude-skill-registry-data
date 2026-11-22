---
name: idea
description: >-
  File a GitHub issue directly from the repo you are standing in with medium-deep operator alignment,
  targeted recon, an architectural sketch, and an automated multi-model consult pass (Codex/Agy)
  applying the Elephant-Goldfish Model (EGM) paraphrase-first comprehension lens. Creates zero files
  on disk and calls no ledger or HQ tools. Trigger on /idea, "file an issue for this", "write this up
  as a GH issue", "capture this idea", "park this", or the legacy /file-issue.
---

# /idea — direct-to-GitHub issue capture with EGM alignment

Captures new ideas, features, refactors, and architectural spikes directly into a well-structured GitHub issue with zero on-disk footprint. It anchors the proposal in operator intent, traces relevant code seams with medium recon, validates the sketch across models using the Elephant-Goldfish Model (EGM) paraphrase-first comprehension lens, and publishes cleanly via `gh issue create`.

Writers this skill calls, and nothing else: `gh issue create` (the issue) and `gh issue comment` (the consult dispositions record). While filing, it writes no files to disk, creates no ledger rows, touches no HQ tools, writes no test code, and never commits. The issue's own verification plan follows the target repo's test policy.

## Usage

```
/idea <one-line what and why>      # harvest → recon → draft sketch → consult → preview & confirm → file
/idea                              # ask for the one-liner first
```

## Steps

0. **Verify environment and remote repository.**
   Ensure the GitHub CLI is authenticated and determine the current repository:
   ```bash
   gh auth status || { echo "idea: gh CLI not authenticated"; exit 1; }
   REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null)
   [ -n "$REPO" ] || { echo "idea: not in a valid git repository with GitHub remote"; exit 1; }
   BASE=$(git rev-parse --short HEAD)
   ```

1. **Harvest operator context & align.**
   Reconstruct the problem statement and motivation from the ongoing session:
   - What problem is being solved, and why now?
   - What are the operational goals and user constraints?
   - What is the expected behavior vs. observed behavior?
   If crucial information is missing, ask up to three concise clarifying questions before proceeding.

2. **Medium recon & prior art check.**
   Perform targeted recon on the codebase:
   - Identify relevant subsystems, entry points, and call paths.
   - Run `gh issue list --search "<keywords>" --state open` to ensure no duplicate issue already tracks this ask. If a matching open issue exists, confirm with the operator before continuing.
   - Pin the recon findings to `Recon: <sha>` (`git rev-parse --short HEAD`).

3. **Draft the issue body (Streamlined 4-Part Structure).**
   Render the issue body into the four canonical sections:

   ### 1. Context & Operator Alignment
   - Problem statement, motivation, and operational/business context.
   - User alignment summary: what is desired and why.

   ### 2. Recon & Code Seams
   - Existing subsystems, key files, entry points, and state writes.
   - Blast radius and integration base (`development@<sha>`).

   ### 3. Proposed Sketch & Approach
   - Architectural sketch and high-level design.
   - Implementation plan: ordered steps extending existing code without duplicate subsystems.
   - Trade-offs, alternatives considered, and risk/rollback considerations.

   ### 4. Acceptance & Non-Goals
   - Checklist of falsifiable acceptance criteria (`- [ ] ...`).
   - Explicit **"What it's not"** boundary section (EGM lens): distinguish stated non-goals/exclusions from deferred work and unauthorized changes.

   *Footer:*
   `Recon: <sha> · base: development@<sha> · review: consult pending`

4. **Consult pass (Codex/Agy with EGM comprehension lens).**
   Load the `consult` skill to fan the draft out to Codex and Agy:
   - **Comprehension Lens First (GH-1414 / EGM):** Without author conversation history, each reviewer evaluates the draft and returns:
     1. **What this proposes** (2–3 sentences)
     2. **How the existing system works, per this document**
     3. **What it's not** (explicit boundaries, stated exclusions vs. inferred/deferred work)
   - **Technical Validation:** Reviewers inspect cited code paths for feasibility, missing requirements, and subsystem conflicts.
   - **Dispositions:** Adjudicate reviewer findings, refine the draft, and format the consult dispositions (reviewer notes, severities, and author resolutions).

5. **Preview & operator confirmation.**
   Present the proposed title, drafted body, and consult comprehension summary ("What this is", "How it works", "What it's not") in chat for the operator.
   Obtain **one** explicit operator confirmation before filing.

6. **File to GitHub.**
   Publish the issue directly using `gh issue create`, piping the body through stdin/heredoc so zero files remain on disk:
   ```bash
   ISSUE_URL=$(gh issue create --title "$TITLE" --body "$BODY")
   ```
   Immediately post the consult dispositions as the initial issue comment:
   ```bash
   gh issue comment "$ISSUE_URL" --body "$DISPOSITIONS"
   ```

7. **Report.**
   Report the newly created issue URL and a concise summary to the operator.

## Guardrails

- **Zero on-disk footprint:** No files created in `PROJECT/1-INBOX/` or anywhere in the repo; no ledger entries in `releases.db` or `releases.sql`.
- **No HQ or preflight contract:** Do not call `hq.sh`, `find-hq.sh`, `hq park`, or `swarm-preflight.sh`.
- **Retain EGM alignment:** The paraphrase-first comprehension lens ("What this proposes", "How the existing system works", "What it's not") must run during consult and be reflected in the draft.
- **Operator confirmation required:** Never file an issue without previewing the title, body, and EGM comprehension summary for operator approval.
