---
name: share-claude-code-chat
description: Export Claude Code JSONL conversations into high-fidelity HTML pages with safe tool timelines, then deploy them to PreviewShip as public share links. Use when users ask to share a Claude Code chat, export Claude Code history, publish a Claude Code conversation, or create a public URL for implementation and review context.
license: MIT
metadata:
  author: PreviewShip
  version: "1.0.0"
  repository: https://github.com/blockdancez/PreviewShip
  docs: https://previewship.com/docs/share-claude-code-chat
  install: npx skills add blockdancez/PreviewShip --skill share-claude-code-chat -a codex -g --yes
  installLocal: npx skills add blockdancez/PreviewShip --skill share-claude-code-chat -a codex --yes
---

# Share Claude Code Chat

## Requirements

Requires Python 3, Node.js >=18 for Markdown rendering, and the PreviewShip CLI. The workflow is local and offline before deploy: it reads Claude Code session JSONL files from `~/.claude/projects` and does not launch, attach to, or control Claude Code.

## How It Works

Claude Code stores project conversations under `~/.claude/projects/<project-key>/<session-id>.jsonl`. This skill:

1. Locates a Claude Code JSONL session (`scripts/render_chat_html.py --current` chooses the newest local session).
2. Converts Claude Code records into a visible transcript.
3. Renders a self-contained `index.html` with user bubbles, assistant Markdown, context cards, and collapsed processing summaries shown before the related assistant answer.
4. Deploys the HTML with PreviewShip CLI and returns the public URL.

## Privacy Rules

Render only visible, shareable chat content. Never publish hidden thinking text, raw tool results, tool stdout/stderr, system records, file-history snapshots, permission records, settings files, API keys, environment variables, or full selected-file contents. The renderer may show a non-verbatim "Claude Code 思考过程已隐藏" processing row, but it must not include the hidden thinking payload.

Claude Code attachment records can contain entire file contents. The renderer may show a file/directory/IDE-selection card, but it must not include the attachment body.

## Workflow

### 1. Resolve the skill directory

```bash
SKILL_DIR="<directory containing this SKILL.md>"
```

Resolve this dynamically; do not hard-code a user-specific path.

### 2. Render the current Claude Code conversation

```bash
mkdir -p /tmp/claude-code-chat-share
python3 "$SKILL_DIR/scripts/render_chat_html.py" --current --output /tmp/claude-code-chat-share/index.html
```

`--current` picks the newest main `~/.claude/projects/**/*.jsonl` session, skips `subagents/agent-*.jsonl`, and prints the resolved path to stderr.

If the wrong session is selected, list recent sessions and pass one explicitly:

```bash
python3 "$SKILL_DIR/scripts/render_chat_html.py" --list-recent

python3 "$SKILL_DIR/scripts/render_chat_html.py" \
  --input "/Users/<you>/.claude/projects/<project-key>/<session-id>.jsonl" \
  --output /tmp/claude-code-chat-share/index.html
```

The renderer also accepts a hand-written transcript JSON object with a `messages` array as a fallback.

### 3. Verify locally

```bash
python3 -m http.server 4174 --directory /tmp/claude-code-chat-share
```

Check that the page is not blank, message order is correct, Markdown/code blocks render cleanly, and no secrets or raw tool output are present.

### 4. Ensure PreviewShip CLI is available and authenticated

```bash
command -v previewship || command -v npx
previewship whoami || npx -y previewship whoami
```

If not authenticated, stop and ask the user to log in:

```text
请前往 https://previewship.com 登录，创建 API Key，然后运行：
npx previewship login --key ps_live_YOUR_KEY
（或 export PREVIEWSHIP_API_KEY=ps_live_YOUR_KEY）
```

### 5. Choose a deployment name

Use the renderer-generated stable name by default:

```bash
PROJECT_NAME="$(python3 "$SKILL_DIR/scripts/render_chat_html.py" --current --print-project-name)"
```

Override it only when the user explicitly provides a project name. Existing PreviewShip project names are deployment identities; using one updates that project.

### 6. Deploy and return the URL

```bash
previewship deploy /tmp/claude-code-chat-share/index.html -n "$PROJECT_NAME" --json
# or
npx -y previewship deploy /tmp/claude-code-chat-share/index.html -n "$PROJECT_NAME" --json
```

Return the public `previewUrl`, the local HTML path, and any fidelity limitations.

## What the Renderer Parses

- `type=user` with string `message.content` -> visible user bubble.
- `type=user` with `tool_result` content -> tool result status only, no raw output. Safe status snippets such as `Received 19.8KB (200 OK)` may be extracted.
- `type=assistant` with `message.content[].type=text` -> visible assistant Markdown.
- `type=assistant` with `tool_use` -> collapsed processing summary, attached to the preceding assistant progress message when present; otherwise shown before the next visible assistant answer.
- `type=assistant` with `thinking` -> hidden thinking summary row only, never the thinking text.
- `type=attachment` -> context card with filename/path only; attachment body is ignored.
- Ignored: `system`, `permission-mode`, `file-history-snapshot`, `last-prompt`, sidechain records, raw `toolUseResult`, and hidden settings/context records.

## Transcript JSON Shape

```json
{
  "title": "Claude Code Chat",
  "projectName": "claude-code-chat",
  "messages": [
    {
      "role": "user",
      "content": "用户消息",
      "context": [{ "title": "src/App.tsx", "subtitle": "文件", "path": "/abs/path/src/App.tsx" }]
    },
    {
      "role": "assistant",
      "content": "助手 Markdown",
      "tools": [{ "name": "Read", "summary": "src/App.tsx", "status": "completed", "result": "Received 2.1KB (200 OK)" }]
    }
  ]
}
```

Only include fields that were visible or safe to summarize. Add `"visible": false` to omit a message from rendering.

## Error Handling

- No Claude Code sessions found: ask the user to provide `--input` with a JSONL path.
- Wrong current session: use `--list-recent` and rerun with `--input`.
- Unknown event types: ignore them unless they contain visible `message.content[].text`.
- Quota/plan/project-count deploy error: stop and report the error. Do not retry by switching to an unrelated existing project name.
