---
name: pr-triage
description: "Fetch CodeRabbit and manual reviewer comments from Azure DevOps PRs and generate an interactive HTML report with severity/status breakdowns. Does NOT interactively loop through comments — triaging is done externally via /pr-judge, which can optionally update the report with verdict/status by comment ID."
compatibility: "Requires: Python 3.7+, Azure DevOps PAT token, .claude folder in repo root"
disable-model-invocation: false
license: "MIT"
metadata:
  author: "Balagurunathan Marimuthu"
  version: "2.2.0"
  improvements: "Fixed Step 6 to use file-based JSON passing instead of CLI arguments. Resolves Windows command-line limit issues (32KB) for large PRs with 20+ comments. Fixed a bug where Refresh mode could reset already-Resolved/Skipped comments back to Pending on a later refresh (comments[] processed list is now derived from status, not passed through as-is). Refresh mode now always writes a new timestamped report file instead of overwriting the original, preserving report history. Added click-to-sort table columns (default: ID ascending)."
---

# EXECUTABLE WORKFLOW: pr-triage

**Start here:** Execute this workflow immediately when skill is invoked.

---

## Status Logic (Simplified)

**Status = External Assignment** (set outside pr-triage):
- `Pending` — Initial state when comment is fetched; not yet reviewed
- `Resolved` — Comment has been reviewed and addressed (typically set by pr-judge after Apply/Fix)
- `Unresolved` — Comment reviewed but marked as unresolved/deferred (typically after Discard on a valid finding)
- `Skipped` — Comment intentionally skipped (not triaged)

**Separate Data** (stored in Technical Info JSON):
- `pr_judge_assessment` — What pr-judge concluded: valid / false_positive / partially_valid / uncertain
- `user_decision` — What the user decided: accept_fix / write_rebuttal / ignore / none

**Key Point:** pr-triage generates reports with all comments at `Pending` initially. After triaging a comment with `/pr-judge`, that skill optionally updates the report by ID with the Status and Verdict you chose. pr-triage itself never modifies status after creation.

---

## Step 0: Check Prerequisites

Before starting, verify all required tools are available:

**Python 3.7+**
```bash
python --version
```
Should output: `Python 3.7.x` or higher

If Python not found:
```
❌ Python 3.7+ is required but not found.

Install Python from: https://www.python.org/downloads/
Then run: python --version to verify

After installation, run /pr-triage again.
```

Exit if Python not available.

---

## Step 1: New or Refresh Existing Report

Ask user with AskUserQuestion (single choice, required):

```
What would you like to do?
```

**Options:**
- A) New Report - Fetch fresh comments and generate a new report
- B) Refresh Existing - Merge fresh comments into an existing report, preserving statuses from prior triage

Store choice in: `mode`

**If mode = New:** Continue to Step 2

**If mode = Refresh:** Go to Step 1a

---

## Step 1a: Load Existing Report (Refresh Mode Only)

Ask user to provide the HTML report path:

```
Enter the HTML report path to refresh:
Example: C:\Repos\docs\reports\pr-triage\1898-pr-triage-20260708-120000.html
```

**Process:**
1. Run extraction script (do NOT print output to Claude):
```bash
python ${CLAUDE_SKILL_DIR}/scripts/extract_report_data.py "<html_path>" > /tmp/pr_triage_extract.json 2>&1
```

2. Check exit code:
   - **Exit 0**: Success → Read `/tmp/pr_triage_extract.json`
   - **Exit 1**: Error → Read error message, show user-friendly message

3. Parse extracted data to get `pr_url` and `pr_number`:
```json
{
  "success": true,
  "pr_number": "1898",
  "pr_url": "https://...",
  "all_comments_count": 122
}
```

4. Store in workflow state:
   - `pr_url` = from extracted data
   - `pr_number` = from extracted data
   - `report_path` = the user-provided path (read-only — used in Step 4 to merge prior triage data; refresh never writes back to this exact file)
   - `report_dir` = `os.path.dirname(report_path)` (the Step 6 output target — refresh writes a **new** timestamped file here, same directory as the original, so prior reports are never overwritten)

5. Show user confirmation:
```
✓ Report loaded successfully
  PR: {pr_number}
  URL: {pr_url}
  Total comments: {all_comments_count}
```

6. **Skip Step 2** — Go directly to Step 3

**If file not found or extraction fails:**
```
❌ {error_message}

Options:
A) Try another file path
B) Start a New Report instead
```

Re-prompt or allow user to switch to New mode.

---

## Step 2: Get PR URL from User (New Mode Only)

Ask the user to provide the full Azure DevOps PR URL using AskUserQuestion.

**Prompt:**
```
Enter your Azure DevOps PR URL:
Example: https://dev.azure.com/org/project/_git/repo/pullrequest/1898

(Copy from your browser address bar)
```

Wait for user input. Parse to extract:
- `pr_number` (from `/pullrequest/{number}`)
- `org` (from `/dev.azure.com/{org}/`)
- `project` (from `/{org}/{project}/`)
- `repo` (from `_git/{repo}/`)

**If parsing fails:** Show error:
```
❌ Invalid Azure DevOps URL format.

Expected format: 
https://dev.azure.com/{org}/{project}/_git/{repo}/pullrequest/{pr_number}

Copy your PR URL from the browser address bar and try again.
```

Re-prompt user.

---

## Step 3: Check for Azure DevOps PAT Token

Check in this order (priority):
1. Environment variable: `ADO_PAT`
2. User-scoped config: `~/.claude/config.json` → `ado_pat` field
3. Repo-scoped config: `./.claude/config.json` → `ado_pat` field (repo root)
4. If none found → Go to Step 3a

**If found:** Store as `pat_token` and continue to Step 4

### Step 3a: Prompt User for PAT Token Setup

**If PAT not found, ask via AskUserQuestion:**

```
Azure DevOps Personal Access Token (PAT) not found.

Choose how to proceed:
A) Set environment variable ADO_PAT
B) Create .claude/config.json in home directory
C) Exit (set up PAT and run again)
```

⚠️ **SECURITY:** Never paste your PAT token here. Set it locally on your machine.

Based on selection:
- **A)**: Tell user: `export ADO_PAT="your-azure-devops-pat"` (in terminal, on their machine)
  - Provide link: Azure DevOps → Settings → Personal Access Tokens
  - Ask them to set it in terminal, then type "done"
  - Re-check for token
  
- **B)**: Show template: `~/.claude/config.json` with `{ "ado_pat": "your-token-here" }`
  - Provide link: Azure DevOps → Settings → Personal Access Tokens
  - Ask them to create file locally, then type "done"
  - Re-check for token

- **C)**: Exit with message: "Set up PAT locally and run `/pr-triage` again"

Do NOT proceed until user confirms they've set PAT locally.

---

## Step 4: Fetch Comments from Azure DevOps

Run Python script silently (do NOT print output to Claude):

**New Mode:**
```bash
python ${CLAUDE_SKILL_DIR}/scripts/fetch_coderabbit_comments.py "<pr_url>" > /tmp/pr_triage_comments.json 2>&1
```

**Refresh Mode:**
```bash
python ${CLAUDE_SKILL_DIR}/scripts/fetch_coderabbit_comments.py "<pr_url>" "<report_path>" > /tmp/pr_triage_comments.json 2>&1
```

The optional 2nd argument tells the script to preserve and merge with existing comments from the report.

### Refresh Mode Merge Behavior

In Refresh mode, the script preserves all prior triage work:

1. **Fresh comments** (in current fetch):
   - Updated with latest severity/description from Azure DevOps
   - Status/verdict from prior triage is preserved by comment ID
   - New comments get Pending status

2. **Old comments** (in prior report but not in fresh fetch):
   - Appended to the result with all prior status/verdict intact
   - Usually resolved/archived comments that no longer appear in current fetch
   - Prevents loss of prior triage work

Result: The final report will contain all comments from both fresh fetch and existing report.

**Output file:** Refresh mode always writes a **new** report file (fresh timestamp, same directory as the original — see Step 6) rather than overwriting `report_path`. The original file is left untouched, so a history of reports accumulates over successive refreshes and no prior triage state can ever be lost to a bad fetch.

**Process:**
1. Run script with output redirected to temporary file
2. Check exit code:
   - **Exit 0**: Success → Read `/tmp/pr_triage_comments.json`
   - **Exit 1**: Error → Read error message from file, show user-friendly error, and **STOP** — do not proceed to Step 6

⚠️ **CRITICAL:** `/tmp/pr_triage_comments.json` is a fixed path that may still hold output from a *previous* run (e.g. from an earlier successful fetch, or a different PR). A non-zero exit code means this run's fetch never wrote fresh data — the file's contents are stale even though the path exists and parses as valid JSON. Never fall through to Step 6 on a non-zero exit just because a file happens to be sitting at that path; always check the exit code first, every time.

**Expected structure (read from file, NOT shown to Claude):**
```json
{
  "success": true,
  "pr_number": "1898",
  "pr_url": "https://...",
  "all_comments": [
    {
      "id": 25197,
      "file": "src/utils.ts",
      "line": 45,
      "severity": "Critical",
      "description": "...",
      "status": "Resolved",
      "pr_judge_assessment": "valid",
      "user_decision": "accept_fix"
    }
  ]
}
```
(`merge_warning` and `generated_at` are included only when applicable — see below — they may be entirely absent from the JSON rather than present as `null`.)

**If merge_warning is present (Refresh mode only):**
Show: `⚠️ Refresh: Could not merge prior comments — {merge_warning}. Using fresh comments only as fallback.`

**If no comments found:** Message: "No CodeRabbit comments found for this PR." Exit gracefully.

**If fetch fails:** Show the error message and offer to retry or exit. Do not proceed to Step 6.

⚠️ **SECURITY:** Script output is read directly from file. Do NOT echo or print it to Claude.

---

## Step 5: Get Report Output Path (New Mode Only)

Ask user where to save the report using AskUserQuestion.

**Prompt:**
```
Where should the report be saved?

Examples:
  C:\Repos\docs\reports\pr-triage
  /home/user/reports
  ./reports

(Press Enter to use default: C:\Repos\docs\reports\pr-triage)
```

Store the path as `report_dir` in workflow state.

Validate path:
- If directory doesn't exist, create it: `mkdir -p {report_dir}`
- If creation fails, show error and re-prompt

**Default:** `C:\Repos\docs\reports\pr-triage`

---

## Step 6: Generate/Regenerate HTML Report (File-Based)

⚠️ **CRITICAL:** Use **file path** instead of inline JSON to avoid Windows command-line limits (32KB max per argument). Large PRs with 20+ comments produce JSON payloads >100KB, causing silent failures.

### 6a: Call Report Generator with File Path

Use Python to write JSON to a temp file, then pass the file path to the script:

**Both New and Refresh Modes:**
```python
import json
import subprocess
import sys
import os

# Read comments from Step 4 output
with open('/tmp/pr_triage_comments.json', 'r') as f:
    comments_data = json.load(f)

pr_number = str(comments_data.get('pr_number', 'unknown'))
# Always pass a directory (not a .html path) so a new timestamped file is generated —
# in both New mode (report_dir chosen in Step 5) and Refresh mode (report_dir derived
# from the original report_path in Step 1a). This is what makes refresh non-destructive.
output_path = '<report_dir>'

# Call the script with file path instead of inline JSON
cmd = [
    sys.executable,
    '${CLAUDE_SKILL_DIR}/scripts/generate_report_react.py',
    pr_number,
    '/tmp/pr_triage_comments.json',  # Pass file path, not JSON string
    output_path
]

result = subprocess.run(cmd, capture_output=True, text=True)

# Check result
if result.returncode == 0:
    output = json.loads(result.stdout)
    report_path = output.get('report_path')
    size_kb = output.get('size_kb', 0)
    comment_count = output.get('comments_count', 0)
else:
    error_msg = result.stderr
    # Handle error - see Step 6b below
```

### 6b: Script Support for File Paths

The `generate_report_react.py` script has been updated to detect file paths:
- If argv[2] is a file path (ends with `.json`), it reads from the file
- If argv[2] is inline JSON, it parses as JSON (backward compatible)
- **No changes needed to existing callers**

### 6c: Error Handling with Fallback

If generation fails, attempt **Direct Python Import** (bypass subprocess):

```python
import sys
import os
import json
from datetime import datetime

# Load directly without subprocess
sys.path.insert(0, '${CLAUDE_SKILL_DIR}/scripts')
from generate_report_react import generate_react_report

with open('/tmp/pr_triage_comments.json', 'r') as f:
    comments_data = json.load(f)

results = {
    "pr_number": comments_data['pr_number'],
    "pr_url": comments_data.get('pr_url', ''),
    "all_comments": comments_data.get('all_comments', []),
    "comments": []
}

# output_path here is always a directory (see 6a) — this bypasses main()'s CLI
# entrypoint, which is what normally turns a directory into a fresh timestamped
# filename, so that resolution must be replicated here to keep refresh non-destructive.
report_dir = output_path
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
report_path = os.path.join(report_dir, f"{results['pr_number']}-pr-triage-{timestamp}.html")

try:
    html = generate_react_report(
        str(results['pr_number']), 
        results, 
        report_path
    )
    
    # Write HTML to file
    os.makedirs(report_dir, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
except Exception as e:
    show_error(f"Report generation failed: {str(e)}")
    return False
```

**Show user on success:**
```
✓ React-based report generated successfully!

Report: {report_path}
Size: {size_kb} KB
Comments: {comment_count}

How to triage:
1. Open the report in your browser
2. For each comment, run: /pr-judge <comment text>
3. When pr-judge asks, provide report path + comment ID to sync status back
4. Report updates in real-time as you triage
```

Store `report_path` in workflow state.

---

## Step 7: Complete

Show final message:

```
✓ pr-triage report ready!

Report: {report_path}

How to triage:
  1. Open the report in your browser
  2. For each comment you want to evaluate, run: /pr-judge <comment text>
  3. When pr-judge finishes, it will ask if you want to update this report
  4. Say Yes, provide the report path + comment ID, and select Status/Verdict
  5. The report updates in real-time — refresh your browser to see changes

If this was a Refresh, this report is a new file — the original report you refreshed from was left untouched. Use this new path for subsequent /pr-judge updates and future refreshes.

The report's client-side filters (Status, Severity) are always available for narrowing the table, and every column header is clickable to sort (default: ID ascending).
```

---

## Error Handling

**At any step, if error occurs:**

Show error message with:
1. What went wrong
2. Suggested fix
3. Ask if user wants to retry or exit

**Examples:**
- "Failed to fetch PR comments" → Check PAT token permissions and PR URL validity
- "Report output directory cannot be created" → Check path permissions
- "Invalid JSON in report" → Report may be corrupted; try a different path or start fresh

---

## References

For more details, see:
- `references/config.example.json` — Configuration template
