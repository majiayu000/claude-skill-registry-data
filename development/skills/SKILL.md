---
name: terminal-title
description: MANDATORY at session start. REQUIRED when user topic shifts (debugging to docs, frontend to backend, new subject, different component). The agent MUST invoke on all topic changes.
---

<!-- ABOUTME: Terminal title skill that automatically updates terminal window title -->
<!-- ABOUTME: Uses emoji from environment + Claude's project detection + current topic -->

# Terminal Title

Updates terminal window title to: `$TERMINAL_TITLE_EMOJI ProjectName - Topic`

## When to Invoke

**You MUST actively monitor conversation flow and invoke this skill whenever the topic materially shifts. Do not wait for explicit permission.**

**DO invoke:**
- Session start (default topic: "Claude Code")
- "let's talk about X" / "can you tell me about Y" → invoke immediately
- User switches domains: debugging → docs, frontend → backend, feature → tests
- User starts working on different module/component after sustained discussion
- User asks about completely unrelated topic

**Do NOT invoke:**
- Follow-up questions on same topic ("add a comment to that function")
- Small refinements to current work ("make it blue")
- Clarifications about current task

## Workflow

1. **Determine project name** — Use human-friendly name from context (git repo, package.json, README heading, or directory basename as fallback). Capitalize properly ("OneOnOne" not "oneonone").

2. **Determine topic** — Short description (2-4 words) from current conversation context. Default to "Claude Code" at session start.

3. **Execute the title command.** Prefer the stable wrapper; fall back to the bundled script.

   **Preferred (cross-harness, stable approval surface):**
   ```bash
   set-terminal-title "ProjectName" "Topic"
   ```

   **Fallback (when the wrapper isn't installed):**

   *Unix/macOS/Linux:*
   ```bash
   bash <skill-base-dir>/scripts/set_title.sh "ProjectName" "Topic"
   ```

   *Windows:*
   ```bash
   pwsh -NoProfile -ExecutionPolicy Bypass -File <skill-base-dir>/scripts/set_title.ps1 "ProjectName" "Topic"
   ```

   The script reads `$TERMINAL_TITLE_EMOJI` from the environment (defaults to 🎉) and writes terminal escape sequences. If neither command is available or the call fails, skip silently — do not surface the failure to the user.

4. **Continue silently** — Don't mention the title update unless the user asks.

## Example

A session opens in `/Users/dev/work/oneonone/hosting` with `TERMINAL_TITLE_EMOJI=💼`, conversation is about Firebase config:

```bash
set-terminal-title "OneOnOne" "Firebase Config"
# Result: 💼 OneOnOne - Firebase Config
```
