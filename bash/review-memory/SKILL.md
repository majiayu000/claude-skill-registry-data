---
name: review-memory
description: >-
  Persistent Agentic Memory for code reviews. Remembers user rationale decisions
  (accepted or dismissed findings) with branch sensitivity, and captures coding
  conventions from PR comments and discussions for future /code-review runs.
---

# Persistent Code Review Memory

Stores branch-sensitive review decisions (accepted or dismissed rationales) and extracts conventions from PR comments and team discussions to eliminate repetitive review noise and enforce project standards.

---

## Operational Modes

Determine which mode to execute based on the user's prompt or slash command.

### Mode 1: Record Rationale Decision (Accept / Dismiss)
**Triggers:**
- Natural conversation: `"Dismiss REV-1: <reason>"`, `"Accept REV-2"`, `"I dismiss the logic warning on <file> because..."`, `"Ignore REV-3"`.
- Slash command: `/review-memory dismiss <ID> <rationale>` or `/review-memory accept <ID>`.

**Protocol:**
1. Extract the target Finding ID (`REV-X`) or target file/snippet, decision status (`dismissed` or `accepted`), and rationale explanation.
2. If the user only said `"Dismiss REV-X"` without a reason, prompt briefly: *"Please provide a short rationale so future reviews remember why."*
3. Execute the memory store CLI:
   ```bash
   node skills/review-memory/scripts/memory-store.mjs record-decision --id REV-X --status dismissed --rationale "Your reason here"
   ```
   *(For multiline or complex rationales, pass `--payload-file <path>`, `--payload-json`, or pipe via stdin with `--stdin`).*
4. Confirm to user:
   > ✅ Recorded dismissal for **[REV-X]** on branch `[branch-name]`: *"<rationale>"*. Future code reviews on this branch will skip this issue.

---

### Mode 2: Reversible Decisions (Undo / Revoke)
**Triggers:**
- Natural conversation: `"Un-dismiss REV-1"`, `"Revoke decision for REV-1"`, `"Reactivate REV-1"`.
- Slash command: `/review-memory revoke <ID>`.

**Protocol:**
1. Execute:
   ```bash
   node skills/review-memory/scripts/memory-store.mjs revoke-decision --id REV-X
   ```
2. Confirm to user:
   > 🔄 Revoked previous decision for **[REV-X]** on branch `[branch-name]`. Future reviews will flag this issue normally.

---

### Mode 3: Capture Conventions (PR Comments & Discussions)
**Triggers:**
- Natural conversation: `"Note convention from PR #42: ..."`, `"Remember convention: always use dayjs, never raw Date"`, `"Capture conventions from this discussion: [pasted thread]"`.
- Slash command: `/review-memory add-convention <rule> [--tags <tags>] [--source <source>]`.

**Protocol:**
1. Parse the core rule, architectural rationale, domain tags (e.g. `api`, `security`, `ts`, `validation`), and PR/discussion source reference.
2. Default convention scope to `repository` (or `branch` if explicitly requested).
3. Execute:
   ```bash
   node skills/review-memory/scripts/memory-store.mjs add-convention --rule "Rule text" --rationale "Context" --tags "tag1,tag2" --source "PR #42"
   ```
4. Confirm to user:
   > 📌 Saved repository convention: **"<Rule text>"** (Source: *<source>*, Tags: `<tag1>, <tag2>`). Applied to future `/code-review` runs.

---

### Mode 4: Review Orchestration Integration (Query Memory)
**Trigger:** Invoked automatically during Step 1 of `/code-review`.

**Protocol:**
1. Detect repository root and branch:
   ```bash
   git rev-parse --abbrev-ref HEAD
   ```
2. Query active memory for the repository and branch:
   ```bash
   node skills/review-memory/scripts/memory-store.mjs query --repo <repoRoot> --branch <branch> --files "<comma-separated-diff-files>"
   ```
3. Read the JSON output:
   - `activeConventions`: Inject into subagent reviewer prompts under `### Active Project & Branch Conventions`.
   - `dismissedSignatures`: Filter against findings in Two-Tier Consensus. Suppress matches from active blockers/warnings and add them to a collapsed `<details>` skipped audit trail.
4. After review finishes, save the review findings snapshot:
   ```bash
   node skills/review-memory/scripts/memory-store.mjs save-session --repo <repoRoot> --branch <branch> --findings '<json>'
   # or write findings to a temp json file and pass:
   # node skills/review-memory/scripts/memory-store.mjs save-session --repo <repoRoot> --branch <branch> --findings-file <path>
   ```

---

### Mode 5: Status & Maintenance
**Triggers:**
- Natural conversation: `"Show review memory"`, `"What conventions are saved for this repo?"`.
- Slash command: `/review-memory list` or `/review-memory clear`.

**Protocol:**
1. Run:
   ```bash
   node skills/review-memory/scripts/memory-store.mjs list --repo <repoRoot>
   ```
2. Output a concise table showing active branch decisions and repository conventions.
