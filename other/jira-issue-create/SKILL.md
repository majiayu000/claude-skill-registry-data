---
name: jira-issue-create
description: Create one or more Jira issues through acli from user-approved drafts using heading-based Context, Acceptance criteria, and Engineering notes sections. Use only when explicitly invoked to create Jira issues; use jira-issue-refine when requirements still need refinement.
---

# Jira Issue Creation

Create one Jira issue or a batch of issues with three plain ADF sections: Context, Acceptance criteria, and Engineering notes. Render each section title as a heading and do not wrap sections in panels.

## Inputs

Extract these values from the request:

- `project` (required): Jira project key, such as `DXAI`. Ask if missing.
- `parent` (optional): Epic or parent key for the created issues.
- `type` (optional): Work item type. Default to `Task`.
- `content source` (optional): Local document, pasted text, or prose describing the issue or issues. For a batch, identify what defines one issue.

## Workflow

### 1. Check authentication

Run `acli auth status`. If authentication is missing, stop and ask the user to run `acli auth login`. Suggest `! acli auth login` when an interactive command is needed.

Continue only when the output shows `✓ Authenticated` for the expected site.

### 2. Gather content

- Read any referenced source document.
- When a parent is given, fetch it for context and tone with `acli jira workitem view <EPIC> --json`.
- Draft these sections for each issue:
  - **Context:** Explain why the issue exists, what it covers, and its role in the larger effort.
  - **Acceptance criteria:** Use an ordered list. Start each item with a bold lead phrase followed by one sentence, such as "**Pilot flows run:** ...".
  - **Engineering notes:** Use bullets with bold labels for risks, constraints, useful details, and relevant links.

Gloss bare identifiers such as KR2, G4, or U3 with a short inline explanation. Use only requirements from the request or source material. Do not invent requirements.

### 3. Confirm drafts

This is a human checkpoint. Do not call any tool in this step because a dialog can hide the draft that the user must review.

Send one Markdown message with:

1. Each issue summary as a heading.
2. The complete Context, Acceptance criteria, and Engineering notes content that will be created.
3. This final line: "Reply **approve** to create the issue(s), or tell me what to change."

End the turn. Continue only after the user approves. If the user requests edits, show each complete revised draft and wait again.

The complete draft shown at this checkpoint must be the exact content later sent to Jira.

### 4. Generate ADF description files

Write a small ES-module script in a scratch directory. Import the builders from `scripts/adf_helpers.mjs` by absolute path and emit one ADF JSON file per issue. Build each description with `doc()`, which fixes the three headings and their order. Node.js 18 or later is required.

```js
import {
  doc,
  para,
  text,
  acItem,
  bulletList,
  listItem,
} from "<skill-base-dir>/scripts/adf_helpers.mjs";
import { writeFileSync } from "node:fs";

// Build one doc(...) per issue.
writeFileSync("<scratch-dir>/<issue>.json", JSON.stringify(adfDoc, null, 2));
```

Run the script with `node <scratch-dir>/gen_issues.mjs`. Do not copy the helper or write generated files into the skill directory.

Do not add ADF `panel` nodes.

Confirm that each output file exists and that a JSON parser accepts it.

### 5. Create issues

Create the first issue alone to confirm that Jira accepts the ADF:

```bash
acli jira workitem create --project <KEY> --type <Type> \
  [--parent <EPIC>] --summary "<summary>" --description-file <file>.json
```

After it succeeds, create the remaining issues in one command chain with `&&`, without separate approval prompts.

- Pass the raw ADF document to `--description-file`; do not wrap it in another object.
- Pass the epic key directly to `--parent`.
- Treat the issue as created only when the command prints `✓ Work item <KEY> created`.
- After a failure, a timeout, or a lost response, the issue may exist anyway. Before you run a create command again, search for it, for example `acli jira workitem search --jql 'project = <KEY> AND summary ~ "\"<summary>\"" AND created >= -1d' --fields "key,summary"`, and create only the issues that are missing.

### 6. Verify and report

- When a parent was set, run `acli jira workitem search --jql "parent = <EPIC>" --fields "key,summary,status,issuetype"`. The issue-type field is `issuetype`, not `type`.
- Inspect one created issue as JSON. Confirm that its description has the three top-level headings in order and no `panel` nodes.
- Report every created issue key and URL, plus any judgment calls.

Finish only after every created issue is verified and its URL is reported. If creation or verification fails, report the failed issue and the observed error without claiming full success.
