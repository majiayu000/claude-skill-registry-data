---
name: change-integrator
description: Use this skill after a code PR is merged to integrate approved specs, update the retrospective with learnings, and clean up branches. It now automatically summarizes the retrospective file to keep it concise. Triggers include "integrate change", "post-merge cleanup", or completing a feature implementation.
---

# Change Integrator Skill

## Purpose

Perform post-merge integration tasks after a code PR is successfully merged. This skill completes the development cycle by moving approved specs from `docs/changes/` to `docs/specs/`, updating the retrospective with learnings, cleaning up feature branches, and updating project board status. It ensures the repository remains clean and the documentation reflects the current state.

A key feature of this skill is the **automated maintenance of `RETROSPECTIVE.md`**. When the file grows too large, the script automatically uses the Gemini CLI to summarize older entries, keeping the document concise and readable while preserving key historical learnings.

## When to Use

Use this skill in the following situations:

- After a code PR is merged to main
- Completing a feature that had a spec proposal
- Finalizing a task and cleaning up branches
- Updating retrospective with completed work
- Moving approved specs to source-of-truth location

## Prerequisites

- Code PR has been merged to main branch
- Feature branch name is known
- PR number is known
- Project board item ID is known (if using project boards)
- `gh` CLI tool installed and authenticated
- `gemini` CLI tool installed and authenticated
- Currently on main branch with latest changes

## Workflow

### Step 1: Verify PR is Merged

Before running integration, confirm the PR was successfully merged:

```bash
gh pr view PR_NUMBER --json state,mergedAt
```

Ensure the state is "MERGED" and mergedAt timestamp is populated.

### Step 2: Identify Integration Needs

Determine what needs to be integrated:
- **Spec files**: Was this a feature with a spec proposal in `docs/changes/`?
- **Branch cleanup**: What is the feature branch name?
- **Project board**: What is the item ID to mark as done?
- **Retrospective**: What were the key learnings from this task?

### Step 3: Run the Helper Script (Optional)

If using the automated script for integration:

```bash
bash scripts/integrate-change.sh -p PR_NUMBER -b BRANCH_NAME -i ITEM_ID -w "WENT_WELL" -l "LESSON" [-c CHANGE_DIR]
```

**Parameters**:
- `-p`: PR number that was merged
- `-b`: Feature branch name (e.g., `feat/45-restructure-doc-indexer`)
- `-i`: Project board item ID
- `-w`: A quote about what went well.
- `-l`: A quote about the key lesson learned.
- `-c`: Optional path to change proposal directory (e.g., `docs/changes/my-feature`)

### Step 4: Understand What the Script Does

The helper script automates these steps:

1.  **Verifies PR is merged**: Queries GitHub API and aborts if PR is not in MERGED state.
2.  **Switches to main and pulls**: Ensures work is on the latest main branch.
3.  **Deletes feature branch**: Removes both remote and local branches.
4.  **Integrates spec files (if applicable)**: Moves `spec-delta.md` to `docs/specs/` and commits the change.
5.  **Updates project board**: Sets the task status to "Done".
6.  **Updates retrospective**: Appends a new entry. If `RETROSPECTIVE.md` exceeds a line limit (e.g., 150 lines), it **automatically summarizes older sprint entries** using the Gemini CLI to keep the file manageable.
7.  **Pushes all changes**: Pushes integration commits to main.

### Step 5: Manual Integration (Alternative)

If not using the script, perform these steps manually:

#### 5a. Switch to Main and Update

```bash
git switch main
git pull
```

#### 5b. Delete Feature Branch

```bash
# Delete remote branch
git push origin --delete feat/45-restructure-doc-indexer

# Delete local branch
git branch -D feat/45-restructure-doc-indexor
```

#### 5c. Integrate Spec Files (If Applicable)

If the feature had a spec proposal:

```bash
# Identify the change directory
ls docs/changes/

# Move spec-delta to specs
SPEC_NAME="my-feature"
cp docs/changes/$SPEC_NAME/spec-delta.md docs/specs/$SPEC_NAME.md

# Remove change directory
rm -r docs/changes/$SPEC_NAME

# Commit integration
git add docs/
git commit -m "docs: Integrate approved spec from feat/45-my-feature"
```

#### 5d. Update Project Board

```bash
gh project item-edit \
  --project-id PROJECT_ID \
  --id ITEM_ID \
  --field-id FIELD_ID \
  --single-select-option-id DONE_OPTION_ID
```

#### 5e. Update Retrospective

Add learnings to RETROSPECTIVE.md following the established format. See the retrospective for examples.

```bash
# Edit RETROSPECTIVE.md to add entry
git add RETROSPECTIVE.md
git commit -m "docs: Add retrospective for PR #45"
```

#### 5f. Push Changes

```bash
git push
```

### Step 6: Verify Integration

After integration completes:

```bash
# Verify branch deleted
git branch -a | grep feat/45

# Verify spec integrated (if applicable)
ls docs/specs/

# Verify retrospective updated
tail -20 RETROSPECTIVE.md

# Verify project board updated
gh project item-list PROJECT_NUMBER --owner @me
```

## Automated Retrospective Summarization

To prevent `RETROSPECTIVE.md` from becoming unmanageably long, the `integrate-change.sh` script includes an automated summarization feature powered by the Gemini CLI.

**How it works:**
1.  **Threshold Check**: Before adding a new entry, the script checks the line count of `RETROSPECTIVE.md`.
2.  **Trigger**: If the line count exceeds a defined threshold (e.g., 150 lines), the summarization process is triggered.
3.  **Preservation**: The script preserves the initial sections of the file, including the introduction and the "Historical Learnings" section.
4.  **Summarization**: It takes the older sprint entries, sends them to the `gemini` CLI, and requests a concise summary that preserves key learnings and markdown structure.
5.  **Reconstruction**: The script then overwrites `RETROSPECTIVE.md` with the preserved header, a new "Summarized Sprints (via Gemini)" section, and the newly generated summary.
6.  **New Entry**: Finally, it appends the new retrospective entry to the freshly summarized file.

This ensures that the file remains a valuable and readable source of information without requiring manual pruning.

## Error Handling

### PR Not Merged

**Symptom**: Script reports PR is not in MERGED state

**Solution**:
- Verify PR number is correct
- Wait for PR to be merged
- Check auto-merge status if enabled
- Manually merge PR if needed

### Branch Already Deleted

**Symptom**: Git reports branch doesn't exist

**Solution**:
- This is normal if auto-merge deleted the branch
- Continue with remaining integration steps
- Script handles this gracefully with `|| echo "..."`

### Spec Directory Not Found

**Symptom**: Script cannot find change directory

**Solution**:
- Verify the change directory path is correct
- Check if this feature even had a spec proposal
- Skip spec integration step if not applicable
- Use `-c` flag only when spec exists

### Permission Denied on Project Board

**Symptom**: GitHub API returns 403 error

**Solution**:
- Verify project board IDs are correct
- Ensure you have write access to the project
- Check `gh` authentication: `gh auth status`
- Update script configuration variables if needed

### Gemini CLI Issues

**Symptom**: The script fails during the "Updating retrospective..." step with an error related to the `gemini` command.

**Solution**:
- Ensure the `gemini` CLI is installed and in your system's PATH.
- Verify you are authenticated. Run `gemini auth` if needed.
- Check for any Gemini API-related issues or outages.
- If the issue persists, you can temporarily increase the `RETROSPECTIVE_MAX_LINES` variable in the script to bypass the summarization and add your entry.

### Retrospective Format Issues

**Symptom**: The automated summary has formatting problems or seems to have lost critical information.

**Solution**:
- The summarization is automated and may not be perfect. The original, unsummarized content is not retained by the script.
- You can review the commit history for `RETROSPECTIVE.md` in git to find the previous version if you need to recover information.
- Manually edit the summarized content to fix any formatting issues.
- Consider adjusting the prompt sent to the Gemini CLI within the `summarize_retrospective` function in the script for better results in the future.

## Configuration Notes

The script uses these hardcoded configuration variables (lines 31-33):

```bash
PROJECT_ID="PVT_kwHOARC_Ns4BG9YU"
FIELD_ID="PVTSSF_lAHOARC_Ns4BG9YUzg32qas"  # Workflow Stage
DONE_OPTION_ID="6bc77efe"
```

**To adapt for your project:**
1. Find your project ID: `gh project list --owner @me`
2. Find field ID: `gh api graphql -f query='...'` (see GitHub docs)
3. Find done option ID: Query project field values
4. Update these variables in the script

**Note**: A future version should detect these dynamically.

## Notes

- **Run after PR is merged**: This is post-merge cleanup, not pre-merge preparation
- **Spec integration is optional**: Only for features that started with spec proposals
- **Retrospective is required**: Always update with learnings from completed work
- **Branch cleanup prevents clutter**: Keeps repository clean and organized
- **Project board sync**: Ensures status accurately reflects completed work
- **Manual steps work too**: Script is a convenience, not required
- **Integration commits go to main**: These are documentation updates, not code changes
- **Keep retrospective focused**: Capture what worked, what didn't, and key lessons
- **One PR per integration**: Run the workflow once per merged PR
- **Script is not fully automated**: Still requires parameters and decision-making