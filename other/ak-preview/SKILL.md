---
name: ak-preview
description: "View files or generate visual explanations, slides and diagrams such as code walkthroughs or HTML/Markdown presentations."
when_to_use: "Invoke for file previews or architecture visualization."
category: media
keywords: [preview, visual, slides, diagrams, HTML]
argument-hint: "[path] OR [--html] --explain|--slides|--diagram|--ascii [topic] OR --html --diff|--plan-review|--recap [--ak-render] [--no-antv|--no-diagram-design|--no-editorial-visuals]"
metadata:
  author: agentkit
  version: "1.2.2"
  attribution: "Visual self-review pattern for diagram output adapted from fireworks-tech-graph by yizhiyanhua-ai (MIT)"
---

# Preview

Universal viewer + visual generator. View existing content OR generate new visual explanations.

## Default (No Arguments)

If invoked without arguments, use `ask_user capability` to present available preview operations:

| Operation | Description |
|-----------|-------------|
| `(view)` | View a file or directory |
| `--explain` | Generate visual explanation |
| `--slides` | Generate presentation slides |
| `--diagram` | Generate architecture diagram |
| `--ascii` | Terminal-friendly diagram |
| `--stop` | Stop preview server |
| `--html --explain` | Self-contained HTML explanation (opens in browser) |
| `--html --diagram` | Self-contained HTML diagram with zoom controls |
| `--html --slides` | Magazine-quality HTML slide deck |
| `--html --diff` | Visual diff review (HTML) |
| `--html --plan-review` | Plan vs codebase comparison (HTML) |
| `--html --recap` | Project context snapshot (HTML) |
| `--ak-render` | Opt-in (implies `--html`; also selected by a project `.ak-render/` directory): compile `--explain`, `--diff`, `--plan-review` or `--recap` HTML from a Page Spec with AK Render (`references/ak-render-route.md`) |

Present as options via `ask_user capability` with header "Preview Operation", question "What would you like to do?".

## Usage

### View Mode
- `/ak-preview <file.md>` - View markdown file in novel-reader UI
- `/ak-preview <directory/>` - Browse directory contents
- `/ak-preview --stop` - Stop running server

### Generation Mode (Markdown)
- `/ak-preview --explain <topic>` - Generate visual explanation (ASCII + Mermaid + prose)
- `/ak-preview --slides <topic>` - Generate presentation slides (one concept per slide)
- `/ak-preview --diagram <topic>` - Generate focused diagram (ASCII + Mermaid)
- `/ak-preview --ascii <topic>` - Generate ASCII-only diagram (terminal-friendly)

### Generation Mode (HTML)
- `/ak-preview --html --explain <topic>` - Self-contained HTML explanation
- `/ak-preview --html --slides <topic>` - Magazine-quality HTML slide deck
- `/ak-preview --html --diagram <topic>` - HTML diagram with zoom controls
- `/ak-preview --html --diff [ref]` - Visual diff review
- `/ak-preview --html --plan-review [plan-file]` - Plan vs codebase comparison
- `/ak-preview --html --recap [timeframe]` - Project context snapshot

## Argument Resolution

When processing arguments, follow this priority order:

1. **`--stop`** → Stop server (exit)
2. **`--html` flag present** → Set HTML output mode flag (continues to next step)
3. **Generation flags** (`--explain`, `--slides`, `--diagram`, `--ascii`) → Generation mode. Load `references/generation-modes.md`
4. **HTML-only flags** (`--diff`, `--plan-review`, `--recap`) → Auto-set HTML mode, then generation mode. Load `references/generation-modes.md`
5. **Visual workflow without explicit mode** → Load `references/visual-explanation-routing.md` to choose mode
6. **Resolve path from argument:**
   - If argument is an explicit path → use directly
   - If argument is a contextual reference → resolve from recent conversation context
7. **Resolved path exists on filesystem** → View mode. Load `references/view-mode.md`
8. **Path doesn't exist or can't resolve** → Ask user to clarify

**Topic-to-slug conversion:**
- Lowercase the topic
- Replace spaces/special chars with hyphens
- Remove non-alphanumeric except hyphens
- Collapse multiple hyphens → single hyphen
- Trim leading/trailing hyphens
- **Max 80 chars** - truncate at word boundary if longer

**Multiple flags:** If multiple generation flags provided, use first one; remaining treated as topic.

**Placeholder `{topic}`:** Replaced with original user input in title case (not the slug).

## Error Handling

| Error | Action |
|-------|--------|
| Invalid topic (empty) | Ask user to provide a topic |
| Flag without topic | Ask user: "Please provide a topic: `/ak-preview --explain <topic>`" |
| Topic becomes empty after sanitization | Ask for topic with alphanumeric characters |
| File write failure | Report error, suggest checking disk space and permissions |
| Server startup failure | Check if port in use, try `/ak-preview --stop` first |
| No generation flag + unresolvable reference | Ask user to clarify which file they meant |
| Existing file at output path | Overwrite with new content (no prompt) |
| Server already running | Reuse existing server instance, just open new URL |
| Parent `plans/` dir missing | Create directories recursively before write |
| `--diff` without git context | Explain: "No git repo detected. Run inside a git repository." |
| `--plan-review` without plan file or active plan | Explain: "Provide a plan file path or run from a session with an active plan." |
| `--recap` without git history | Explain: "No git history found. Run inside a git repository with commits." |
| `--html --ascii` combination | Not supported — `--ascii` is terminal-only by design. Suggest `--html --diagram` instead |
| `--diff` with PR number but `gh` unavailable | Explain: "GitHub CLI (gh) is required for PR diffs. Install from https://cli.github.com/" |

## HTML route

For HTML only, load `references/html-mode-workflow.md` and the relevant artifact reference.
View mode does not load design guidance. Preserve accepted theme, typography and interaction
choices across updates; load additional libraries only when the artifact needs them.
