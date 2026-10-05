---
name: chronicle
description: |
  Maintain and update the persistent project chronicle (docs/chronicle.md).
  Trigger when:
  - The human requests a history summary or chronicle update.
  - Starting work on a new codebase and needing context on its evolution.
  - Prompt contains keywords: /chronicle, chronicle, project history, git log summary, history summary.
---

# Chronicle Workflow

A structured approach to maintaining a high-level, conceptual project chronicle (`docs/chronicle.md`). This chronicle serves as a persistent decision record, mapping the evolution of the codebase's architecture, workflows, and conventions to optimize agent context and human understanding.

---

## Purpose

Standard git logs are either too detailed or too fragmented to provide deep architectural context. The **Chronicle Workflow** maintains an incremental, high-level chronicle file in the repository. Because it uses a commit cutoff marker in its frontmatter, it can be updated cheaply and incrementally over time, serving as a durable project history journal.

---

## Execution Protocol

To update or initialize the chronicle, follow these steps:

### 1. Prepare Pending Logs
Run the helper script in prepare mode:
```bash
python3 skills/chronicle/scripts/update_chronicle.py --prepare
```

If the chronicle is already up to date, the script will output:
`Chronicle is already up to date with HEAD.` and you may exit.

Otherwise, it will output a batch of up to 50 commits (from oldest to newest) along with changed files. Note the `TARGET_END_SHA` printed at the end of the output — you pass it back to the write step so the recorded range is bound to exactly the commits you summarized (immune to HEAD moving in between).

### 2. Group and Summarize
Using your LLM reasoning, analyze the batch output. Group the commits into conceptual themes rather than listing them raw. Focus on **why** changes were made, what design decisions were reached, and major milestones.

Organize the summary into the following categories where relevant:
- **Architectural Shift / Design Decisions**: Major structural changes, folder reorganizations, and key trade-offs.
- **Workflow & Rulesets**: Updates to workflows, rulesets, and agent configurations.
- **Features & Implementation**: Core user-facing features and implementations.
- **Infrastructure & Quality**: CI, tooling, linting, and test configurations.
- **Documentation**: Significant documentation changes (beyond minor typos).

### 3. Commit the Update
Run the helper script in write mode, passing the `TARGET_END_SHA` from Step 1 and your structured Markdown summary:
```bash
python3 skills/chronicle/scripts/update_chronicle.py --write --end-sha <TARGET_END_SHA> --summary "<Markdown formatted summary>"
```

### 4. Repeat
If the write command output indicates remaining pending commits (e.g., `Remaining pending commits: N`), repeat from Step 1 until the prepare command reports that it is fully up to date.

---

## Output Format Guidelines

The chronicle summaries should be written in clean, concise Markdown. Avoid listing individual commit SHAs in the summary text (the headers already track the ranges). Example format:

```markdown
- **Architectural Shift**: Distilled global ruleset to align with axiom/persona conventions.
- **Workflow & Rulesets**: Formalized planning workflows by adding `SKETCH` and `PLAN` protocols.
- **Quality & Infrastructure**: Ignore cache files and standardize tooling in the root configuration.
```
