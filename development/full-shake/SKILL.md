---
name: full-shake
description: Marathon thread context reset for long-running sessions (30+ turns). Prunes tool outputs, windows scratchpad thoughts to the last 20 turns, and applies the Milestone Horizon (preserving Turn 1 Genesis, collapsing middle turns into an indexed checkpoint, and keeping the last 25 turns verbatim).
---

# ⚡ /full-shake: Marathon Thread Context Reset

Run this skill when you are working on **marathon conversations (30+ turns)** and need to restore "Turn 1" speed and agility while staying in the exact same chat window.

---

## 🌟 The 2-Tier Marathon Reset

1. **💭 Scratchpad Thought Windowing**:
   * Drops ancient internal monologues older than 20 assistant turns while preserving final answers and code verbatim (saves ~100k+ tokens on reasoning models).
2. **🏛️ The Milestone Horizon (For Sessions > 30 User Turns)**:
   * **Turn 1 (Genesis)**: Preserved **100% verbatim** (project origin, guidelines, and constraints).
   * **Middle Horizon (Turns 2 to N-25)**: Compacted into a structured Milestone Checkpoint block with exact line-indexed backup links to the permanent disk archive.
   * **Active Working Window (Last 25 turns)**: Preserved **100% verbatim** (with the last 10 turns of tool outputs completely unpruned).
3. **Natural Fallback**:
   * If a session has $\le 30$ user turns, all conversation turns are preserved verbatim, applying only thought windowing and tool pruning.

---

## 🚀 Execution Instructions

When the user invokes `/full-shake`:

1. Locate the active session's `transcript.jsonl` log file:
   - Primary path: `<appDataDir>/brain/<conversation-id>/.system_generated/logs/transcript.jsonl`
   - Artifact directory: `<appDataDir>/brain/<conversation-id>/`

2. Execute the native compiled binary with `--full`:
   ```bash
   ~/.gemini/bin/shake-prune "<transcript_path>" "<artifact_directory>" --full
   ```

3. Present the formatted output report directly to the user.
