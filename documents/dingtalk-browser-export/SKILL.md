---
name: dingtalk-browser-export
description: Export the currently open DingTalk/Alidocs document from a logged-in Chrome session without relying on the browser save dialog. Use this whenever the user asks to export, download, save, or back up the current DingTalk document to Word (.docx), PDF, or Markdown, especially when Chrome download popups would block automation.
---

# DingTalk Browser Export

Use this skill when the user wants the current DingTalk document from their real Chrome session exported to a local file without getting blocked by the browser's save dialog.

This skill is for the browser-export path, not the OpenAPI path:
- Prefer this skill when the user is already logged into DingTalk in Chrome.
- Prefer this skill when the user explicitly wants the same export result as DingTalk's web UI.
- Do not use this skill for editing document content.

## Prerequisites

- OpenClaw Chrome extension is installed and connected.
- `openclaw` CLI is available locally.
- Chrome already has the target DingTalk document open and visible.
- The active relay profile may be `chrome-relay` or another extension-backed profile; do not assume it is named `chrome`.

## Workflow

1. Confirm the active Chrome tab is a DingTalk/Alidocs document.
2. Run the bundled script:

```bash
python3 /Users/derek/.agents/skills/dingtalk-browser-export/scripts/export_current_dingtalk.py
```

If you need to force a specific profile:

```bash
python3 /Users/derek/.agents/skills/dingtalk-browser-export/scripts/export_current_dingtalk.py --browser-profile chrome-relay
```

3. By default the script exports `.docx` to `/Users/derek/output/doc`.
4. Report the saved file path back to the user.

## Format options

Use `--format` when needed:

```bash
python3 /Users/derek/.agents/skills/dingtalk-browser-export/scripts/export_current_dingtalk.py --format pdf
python3 /Users/derek/.agents/skills/dingtalk-browser-export/scripts/export_current_dingtalk.py --format md
```

Supported values:
- `docx`
- `pdf`
- `md`

## Operational notes

- The script does not wait for Chrome's save dialog.
- It triggers DingTalk's own export job in the page, captures the export result URL, and downloads the generated file directly to a fixed local path.
- If the toolbar DOM shifts, rerun once after re-focusing the desired Chrome tab. The script already re-reads the current active tab every run and probes multiple header buttons before failing.

## Output

Always return:
- the document title
- the export format
- the saved local path

If export fails, say whether it failed at:
- finding the active DingTalk tab
- opening the export menu
- waiting for the export job result
- downloading the generated file
