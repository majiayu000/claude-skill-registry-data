---
name: progress
description: Show progress bars for background agents by checking which expected files have landed on disk. Use when the user types /progress, asks "how far along is the agent", "what's the progress", "show me a progress bar", or wants to see what background agents have written so far. Also useful mid-wait when multiple parallel agents are running.
---

# Agent Progress Dashboard

Show a visual progress dashboard for running or recently completed background agents by checking which of their expected output files exist on disk.

## How it works

Background agents receive prompts listing specific files to create. This skill finds those agents, extracts the expected file list from their prompts, checks which files exist on disk, counts lines, and renders a progress bar.

## Step 1: Find agent task files

Use Bash to find recent agent output files for the current project. The transcript directory follows the pattern `/private/tmp/claude-501/<project-slug>/*/tasks/*.output`. The project slug is derived from the working directory path with `/` replaced by `-`.

```bash
# Find the tasks directory for the current session
PROJ_SLUG=$(echo "$PWD" | sed 's|/|-|g; s|^-||')
TASKS_DIR=$(find /private/tmp/claude-501/ -path "*${PROJ_SLUG}*/tasks" -type d 2>/dev/null | head -1)
ls -lt "$TASKS_DIR"/*.output 2>/dev/null | head -20
```

If no tasks directory is found, try a broader search or tell the user no background agents were found.

## Step 2: Extract agent metadata from each transcript

For each `.output` file, extract the agent description and the file list from its prompt. Agent transcripts are JSONL. The first few lines contain the launch metadata including the agent's `description` and `prompt`.

```bash
# Extract agent name and prompt from transcript
head -5 "$TASKS_DIR/<id>.output" | python3 -c "
import json, sys
for line in sys.stdin:
    try:
        d = json.loads(line.strip())
        # Look for the agent spawn message or initial prompt
        msg = d.get('message', {})
        content = msg.get('content', []) if isinstance(msg, dict) else []
        for block in (content if isinstance(content, list) else []):
            if isinstance(block, dict) and block.get('type') == 'tool_use' and block.get('name') == 'Agent':
                inp = block.get('input', {})
                print(json.dumps({'description': inp.get('description',''), 'prompt': inp.get('prompt','')}))
    except: pass
"
```

## Step 3: Parse expected files from the prompt

Look for file paths in the agent's prompt. Common patterns:
- Lines containing `.cs`, `.ts`, `.py`, `.md` etc. that look like file creation instructions
- Lines like `**\`FileName.cs\`**` or `1. **FileName.cs**` or `- \`path/to/file.cs\``
- Lines mentioning "create", "write", "add" near a filename
- Numbered lists of files to create

Use a Python script or grep to extract these. Also check for modification targets ("restyle in-place", "wire up", "modify").

```bash
# Extract expected files from prompt text
echo "$PROMPT" | python3 -c "
import sys, re
text = sys.stdin.read()
# Match **\`FileName.ext\`** and similar patterns
files = re.findall(r'\*\*\x60([A-Za-z][\w.]+\.\w+)\x60\*\*', text)
# Also match numbered items like '1. **FileName.cs**'
files += re.findall(r'\d+\.\s+\*\*\x60?([A-Za-z][\w.]+\.\w+)\x60?\*\*', text)
# Deduplicate preserving order
seen = set()
for f in files:
    if f not in seen:
        seen.add(f)
        print(f)
"
```

## Step 4: Check file existence and count lines

For each expected file, determine:
- Whether it exists on disk (search common project paths)
- Line count if it exists
- Whether it's a new file or a modification (check git status)

```bash
# For each file, check existence and count lines
for FILE in $EXPECTED_FILES; do
    FOUND=$(find "$PROJECT_ROOT" -name "$FILE" -type f 2>/dev/null | head -1)
    if [ -n "$FOUND" ]; then
        LINES=$(wc -l < "$FOUND")
        echo "[x] $FILE  $LINES loc"
    else
        echo "[ ] $FILE  (pending)"
    fi
done
```

For modified files, use `git diff --stat -- <path>` to show `(+N/-M)` instead of total LOC.

## Step 5: Render the progress dashboard

Format output exactly like this for EACH agent:

```
<Agent Description>: [████████████░░░░░░░░] 7/11 files

  [x] CalloutBubble.cs        249 loc
  [x] StationPrompts.cs       142 loc
  [x] NavigationOverlays.cs   302 loc
  [ ] HudStatusBar.cs         (pending)
  [ ] HudContextHints.cs      (pending)
                              ---------
                              ~1,093 loc new
```

### Progress bar rendering

- Total width: 22 chars inside brackets
- Filled: `█` (U+2588) for each completed unit
- Empty: `░` (U+2591) for each remaining unit
- Scale: `round(done/total * 22)` filled blocks

### File list formatting

- `[x]` for files that exist on disk, `[ ]` for pending
- Right-align the LOC/status column at a consistent position
- For modified files (not new): show `restyled (+N/-M)` or `wired (+N/-M)`
- Separator line: spaces then `─────────` (box drawing horizontal)

### Combined totals (after all agents)

If multiple agents are shown, add a combined total at the bottom:

```
─── Combined ───────────────────────────────
  Impl-A:  [██████████████████████] 3/3   630 loc
  Impl-B:  [██████████████████████] 4/4   934 loc
  Impl-C:  [████████████████░░░░░░] 8/11  ~1,093 loc
                                          ─────────
                                   Total: ~2,657 loc new + 88 changed
```

## Step 6: Agent status detection

Determine whether each agent is still running or completed:
- Check if the `.output` file's last line contains `"status":"completed"` — if so, mark as done
- If not completed, the agent is still running — show current file count as in-progress
- For completed agents with all files landed, show a checkmark: `done`

## Edge cases

- **No agents found**: "No background agents detected for this project."
- **Agent with no parseable file list**: Show the agent name with "unable to extract file list from prompt" and skip the progress bar.
- **Files in unexpected locations**: Search recursively from project root. If a file could be in multiple locations, prefer the one matching the agent's prompt context.
- **Very recent agents**: The transcript may not have the full prompt yet. Show "agent starting..." if the output file is < 1KB.

## Important

- Do NOT read full agent transcript files — they can be 50MB+ and will overflow context. Only read the first 5-10 lines for metadata.
- Use Bash for all file operations. Python one-liners for parsing are fine.
- Keep output concise — the user wants a quick glance, not a report.
- If the user doesn't specify which agents, show ALL recent agents (last 2 hours).
