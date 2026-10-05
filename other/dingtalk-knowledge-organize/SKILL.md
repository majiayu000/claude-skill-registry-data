---
name: dingtalk-knowledge-organize
description: Use when the user wants to inventory, organize, classify, clean up, move, rename, deduplicate, or remediate DingTalk knowledge base files with a CSV approval workflow, especially when only uncertain files should be deep-read before executing approved changes.
---

# DingTalk Knowledge Organize

Use this skill when the user wants a controlled organization workflow for a DingTalk knowledge base.

This skill uses the `dws` skill as its execution backend for DingTalk document operations. Prefer `dws doc` for create/list/read/move/rename/folder-create actions instead of raw HTTP APIs whenever execution in DingTalk is required.

The workflow has five stages:

1. Quick scan all files without reading contents.
2. Generate an initial remediation CSV with suggested categories and actions.
3. Let a human admin review the CSV.
4. Re-run with admin feedback and deep-read only the uncertain files.
5. Execute the approved CSV and write a report.

## What this skill is for

- Full knowledge base inventory, not just `ALIDOC`.
- Initial classification based on folder path, file name, extension, and metadata.
- Minimal deep reading only for uncertain files.
- Approval-first execution. Do not move or rename anything before admin confirmation.

## Current scripts

### 1. Scan a knowledge base

Use:

```bash
python3 /Users/derek/.agents/skills/dingtalk-knowledge-organize/scripts/scan_dingtalk_workspace_inventory.py \
  --workspace-name "Global BD/国际业务部"
```

This script:
- reads credentials from `~/.dingtalk-skills/config`
- finds the workspace by exact name first, then substring match
- recursively walks the entire node tree
- writes a JSON inventory under `/Users/derek/Documents/memory/钉钉知识库/`

Inventory generation still uses metadata/API scanning because that is the fastest way to build a complete remediation table.

### 2. Build the remediation CSV

Use:

```bash
python3 /Users/derek/.agents/skills/dingtalk-knowledge-organize/scripts/build_remediation_csv.py \
  --inventory-json "/path/to/inventory.json"
```

Optional:

```bash
python3 /Users/derek/.agents/skills/dingtalk-knowledge-organize/scripts/build_remediation_csv.py \
  --inventory-json "/path/to/inventory.json" \
  --existing-csv "/path/to/prior.csv"
```

This script:
- covers all files in the inventory
- proposes `proposed_category`
- proposes `proposed_action`
- leaves `move_to` blank when no move is suggested
- marks uncertain rows with `needs_content_review=yes`
- preserves `admin_decision` and `notes` from a prior CSV when provided

## CSV schema

Use this exact header:

```text
workspace_name,file_path,size_mb,file_type,source_url,modified_time,proposed_category,name_based_confidence,needs_content_review,review_reason,content_summary,duplicate_group,proposed_action,rename_to,move_to,admin_decision,notes
```

Field intent:
- `file_type`: original file type inferred from extension, falling back to DingTalk node category
- `proposed_category`: target business category after cleanup
- `needs_content_review`: `yes` only when path and filename are not enough
- `proposed_action`: one of `keep`, `move`, `rename`, `move_and_rename`, `duplicate_candidate`, `move_to_待归档`, `pending_review`
- `move_to`: blank when no move is suggested
- `admin_decision`: left blank for human review, then filled before execution

## Decision rules

### Step 1: Quick scan only

Do not read document bodies in step 1.

Use only:
- workspace name
- full path
- file name
- extension
- DingTalk node category
- modified time

### Step 2: Mark only uncertain files for deep reading

Mark `needs_content_review=yes` when:
- the name is generic, such as `test`, `资料`, `模板`, `版本1`, `副本`
- the path and file name point to conflicting business categories
- duplicate candidates need disambiguation
- the item sits at the root or another obviously temporary location

Keep the deep-read pool small. Bias toward path-based decisions first.

### Step 3: Approval gate

Do not execute moves, renames, or deletions unless the user explicitly says the admin has confirmed the CSV.

### Step 4: Execution

When execution is requested:
- treat `admin_decision` as the source of truth
- execute DingTalk operations through `dws doc`
- create missing folders through `dws doc folder create`
- move archive candidates into a `待归档` folder instead of deleting anything
- leave untouched rows with empty `move_to`

Use:

```bash
python3 /Users/derek/.agents/skills/dingtalk-knowledge-organize/scripts/execute_remediation_csv_dws.py \
  --inventory-json "/path/to/inventory.json" \
  --csv-path "/path/to/remediation.csv" \
  --dry-run
```

Then after explicit admin confirmation:

```bash
python3 /Users/derek/.agents/skills/dingtalk-knowledge-organize/scripts/execute_remediation_csv_dws.py \
  --inventory-json "/path/to/inventory.json" \
  --csv-path "/path/to/remediation.csv" \
  --execute
```

Execution rules:
- read `admin_decision` first
- if `admin_decision` is blank, skip the row
- support `keep`, `move`, `rename`, `move_and_rename`, `move_to_待归档`
- require `move_to` for move-like actions except `move_to_待归档`, which defaults to `待归档`
- require `rename_to` for rename-like actions
- resolve target folders by path under the workspace root, creating missing folders with `dws doc folder create`
- call `dws doc move --node ... --folder ... --format json`
- call `dws doc rename --node ... --name ... --format json`

### Step 5: Report

After execution, produce a report with:
- total files processed
- counts by `proposed_action`
- counts by final destination
- count of deep-read files
- count of rows skipped due to missing approval
- command-level successes and failures from `dws`

## Output expectations

For step 1, always return:
- the workspace scanned
- total file count
- output CSV path
- how many rows were marked `needs_content_review=yes`
- a short note on the main heuristics used

For step 2, always return:
- updated CSV path
- how many admin decisions were preserved
- how many uncertain files still remain

For step 4, always return:
- what was executed
- what was skipped
- the report path

## `dws doc` command notes

Use `dws doc` as the source of truth for execution syntax:

- `dws doc list --workspace <WS_ID> --format json`
- `dws doc list --folder <FOLDER_ID> --format json`
- `dws doc folder create --name "xxx" --folder <PARENT_ID> --format json`
- `dws doc move --node <DOC_ID> --folder <TARGET_FOLDER_ID> --format json`
- `dws doc move --node <DOC_ID> --workspace <WS_ID> --format json`
- `dws doc rename --node <DOC_ID> --name "New Name" --format json`

When implementing or running execution:
- always pass `--format json`
- use `--help` before relying on a command you have not used recently
- for real execution, add `--yes` only after explicit user confirmation
