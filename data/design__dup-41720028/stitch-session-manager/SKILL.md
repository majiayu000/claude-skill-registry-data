---
name: stitch-session-manager
description: >
  Manages multi-screen Google Stitch design sessions by tracking prompts, screens, and shared style language.
  Use when you need continuity across Stitch prompts, want to append or summarize sessions, or must export
  screen histories for reviews. Triggers on phrases like "start/continue Stitch session", "log screen", or
  "summarize Stitch progress".
allowed-tools: Read, Write, List, Grep
---

# Stitch Session Manager

## Quick Start
- `Start a new Stitch session for [project]` → creates `.google-stitch/sessions/<project>/session.json`.
- `Add a screen called [name] with this brief: ...` → optimizes prompt via `authoring-stitch-prompts`, saves Markdown to `.google-stitch/prompts/<slug>-###-prompt.md`, and logs metadata as `<slug>-###.json`.
- `Summarize my current Stitch session` → returns screen list, visual patterns, next-step suggestions.
- `Generate a new prompt for [screen] using current session style` → reuses stored cues before calling the authoring skill.
- `End this Stitch session and export summary` → writes Markdown summary under the session folder.

## Output Structure
- `.google-stitch/sessions/<project>/session.json`: metadata (`session_name`, timestamps, style guide notes, prompt index).
- `.google-stitch/sessions/<project>/screen-log/<slug>-###.json`: individual prompt payloads (raw brief, status, references) plus the path of the saved Markdown prompt.
- `.google-stitch/prompts/<slug>-###-prompt.md`: source-of-truth prompt text produced by `authoring-stitch-prompts`.
- `.google-stitch/sessions/<project>/summary.md`: exportable brief for reviews or handoffs.

## Commands & Triggers
| Command | Trigger phrases | Result |
| --- | --- | --- |
| `session:new` | "start a new Stitch session" | Initialize directories + base metadata. |
| `session:add` | "add screen", "log prompt", "iterate screen" | Capture new screen, call authoring skill, persist JSON. |
| `session:list` | "show session screens" | Return ordered list of screens + status. |
| `session:summary` | "summarize session", "what have we made" | Produce textual summary + style cues. |
| `session:style` | "reuse style", "match previous look" | Extract palette, typography, tone for new prompts. |
| `session:export` | "export session", "end session" | Finalize summary.md with totals + next steps. |

## Workflow
Follow the abbreviated loop: initialize → add/update screens → reference session memory → export.  
See [WORKFLOW.md](WORKFLOW.md) for detailed branching logic, file formats, and pseudo-commands.

## Prompt Storage Alignment
- Reuse the same slug + zero-padded index rules from `authoring-stitch-prompts` when calling the authoring Skill.
- Pass the computed path (`.google-stitch/prompts/<slug>-###-prompt.md`) to the logger so summaries and exports can link directly to the Markdown file.
- Never duplicate prompt text inside the JSON logs—store pointers only to keep history lightweight.

## Style Memory & Integration
- Before writing a new prompt, the Skill scans existing `session.json` + latest screen logs to extract design cues (color, typography, density, component patterns).
- It then calls **`authoring-stitch-prompts`** with:
  - Original user brief.
  - Session style payload (palette, layout bias, voice).
  - Optional constraints (responsive targets, export needs).
- Returned prompt is saved back to the log and surfaced to the user for immediate Stitch use.
- When no stylistic precedent exists, fall back to user-provided cues and update session metadata once the first screen is logged.

## Examples
Representative transcripts for starting sessions, logging iterations, and exporting summaries live in [EXAMPLES.md](EXAMPLES.md). Use them to mirror tone, prompt framing, and file naming.

## Common Issues
High-level fixes are below; detailed diagnosis (including directory repair scripts) is in [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
- Missing session folder → re-run `session:new` or point to existing `.google-stitch/sessions/<project>`.
- Style drift → run `session:style` to restate cues before adding new screens.
- Duplicate screen names → the Skill auto-increments suffixes; confirm desired slug before export.

## Version History
- v1.0.0 (2025-02-10): Initial release — session management companion to `authoring-stitch-prompts`.
