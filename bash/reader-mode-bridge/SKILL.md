---
name: reader-mode-bridge
description: Turn saved HTML, copied article text, or PDF excerpts into a deterministic local reading handoff with clean metadata and export-ready output.
---

# Reader Mode Bridge

Use this skill when the user needs a real local cleanup pass before a web article, PDF excerpt, or copied reading fragment moves into notes, chat, or another document.

Reader Mode Bridge fits best when the task is about:

- turning copied reading input into one stable handoff without another cleanup pass
- preserving title, source, and readable body text when the original input is noisy
- attaching front-browser-tab metadata to clipboard text so the handoff keeps its source
- exporting a clean reading payload as markdown, prompt text, plain text, or JSON

## Quick Start

From the skill folder:

```bash
python3 scripts/reader_mode_bridge.py doctor
python3 scripts/reader_mode_bridge.py clean --clipboard --front-tab --format markdown
python3 scripts/reader_mode_bridge.py clean --file ~/Downloads/article.html --format prompt
python3 scripts/reader_mode_bridge.py clean --file ~/Downloads/paper.pdf --title "Paper excerpt" --format markdown
pbpaste | python3 scripts/reader_mode_bridge.py clean --stdin --source-url https://example.com/article --format prompt
python3 scripts/reader_mode_bridge.py copy --text "<h1>Sample</h1><p>Reader handoff body.</p>" --format markdown
```

## What the helper does

- reads saved HTML, markdown, text, clipboard content, stdin, or local PDFs when `pdftotext` is available
- removes common boilerplate such as share prompts, cookie lines, duplicate lines, and other short navigation debris
- keeps one clean title, one source label, and one readable body so the handoff lands in notes or chat without manual repair
- can attach the current Safari or Chrome-family front-tab title and URL when the article text came from the clipboard
- renders plain text, markdown, prompt-friendly text, or JSON output and can copy the result to the macOS clipboard

## Workflow

1. Run `doctor` once if you need to confirm `pbcopy`, `pbpaste`, `pdftotext`, or AppleScript support.
2. Use `clean` with `--clipboard`, `--stdin`, `--text`, or `--file` to create the reading handoff.
3. Add `--front-tab` when the source text came from a browser and you want the current tab metadata attached automatically.
4. Use `copy` when the next move is pasting the cleaned handoff directly into Codex, Notes, a ticket, or a chat thread.

## Guardrails

- Do not invent source metadata that is not present in the input, the supplied flags, or the active front tab.
- Keep the tool local and deterministic; it should not depend on network access or remote reader services.
- Treat PDF extraction as best-effort and fail clearly when `pdftotext` is unavailable instead of pretending the PDF was read.
- Reader Mode Bridge cleans and formats content; it should not summarize, rewrite, or mutate the source beyond cleanup and truncation.

## Prototype

- `prototype/` sketches a menu-bar shell with source metadata, cleanup notes, reading metrics, and export actions.
- Keep the SwiftUI surface menu-bar first and compact enough to support the quick "clean this and move it on" moment.

## Resources

- `scripts/reader_mode_bridge.py`: deterministic local helper for reading cleanup and export
- `references/cleanup-contract.md`: supported inputs, outputs, and cleanup heuristics
- `prototype/`: SwiftUI starter files for a compact macOS reader handoff surface
