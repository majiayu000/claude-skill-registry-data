---
name: gentle-ai-engram
description: "Trigger: Gentle AI, Engram setup, orchestrator memory, session continuity. Combine NutrIA agent governance with persistent memory."
license: MIT
metadata:
  author: "NutrIA"
  version: "0.1.0"
---

# Activation Contract
Use when running NutrIA agents with Gentle AI and Engram.

# Hard Rules
- Gentle AI manages orchestration behavior; this harness provides NutrIA-specific roles and skills.
- Do not overwrite an existing Gentle AI or Engram configuration.
- Call `mem_context` at session start and `mem_session_summary` before ending a session.
- Use `mem_save_prompt` when the real prompt is available; save only curated, non-sensitive observations.

# Execution Steps
1. Detect existing Gentle AI / Engram setup.
2. Load `team-orchestrator` and the role profile matching the task.
3. Apply Linear, Neon and Stitch safety gates.
4. Persist approved decisions, bugs, discoveries and conventions in Engram.

# Output Contract
Return the selected role, approval owner, current evidence and memory handoff.
