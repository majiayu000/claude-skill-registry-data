---
name: share-codex-chat
description: Export the current visible Codex conversation into a high-fidelity HTML page and deploy it to PreviewShip as a public share link. Use when users ask to share a Codex chat, export a Codex transcript, publish a Codex conversation, or create a public URL for implementation context.
license: MIT
metadata:
  author: PreviewShip
  version: "2.0.0"
  repository: https://github.com/blockdancez/PreviewShip
  docs: https://previewship.com/docs/share-codex-chat
  install: npx skills add blockdancez/PreviewShip --skill share-codex-chat -a codex -g --yes
  installLocal: npx skills add blockdancez/PreviewShip --skill share-codex-chat -a codex --yes
---

# Share Codex Chat

## Requirements

Requires Python 3 for the renderer and Node.js >=18 for Codex's `marked.esm.js` Markdown parity plus the PreviewShip CLI. The workflow is fully offline and local before deploy: it reads the session transcript from `~/.codex` and never launches, attaches to, or controls Codex.

## When to use this skill

Use this when the user asks to:
- Share the current Codex conversation with other people.
- Turn the current chat into an HTML page / public link.
- Deploy the current conversation to PreviewShip.
- Mentions `share-codex-chat`, "分享当前聊天", "导出 Codex 对话", "生成聊天 HTML", "部署聊天记录".

## How it works (read this first)

Codex stores every desktop conversation locally as a **rollout JSONL** under `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`, and indexes them in `~/.codex/state_5.sqlite` (`threads` table). This skill:

1. **Locates the current conversation's JSONL** by reading those local files — `scripts/render_chat_html.py --current` does this automatically.
2. **Renders it to a self-contained `index.html`** that reproduces the visible Codex chat UI (user bubbles, assistant Markdown, `已处理 <时长> ›` rows, code blocks, file/changed cards, action icons). Markdown is parsed with Codex's own `marked` (via `scripts/md.mjs`) so GFM output matches.
3. **Deploys** the HTML with the PreviewShip CLI and returns the public URL.

It is **fully offline and local**. It does **NOT** launch Codex, attach a debugger, open a second window, or require any debug/remote-debugging flag. The user keeps using Codex normally.

### Privacy (hard rules)
Render only what is visible in the chat. **Never** include hidden system/developer messages, chain-of-thought/reasoning, raw tool calls or tool output, `AGENTS.md` instructions, `<environment_context>`, full `<skill>...</skill>` payloads, API keys, env vars, or secrets — unless the user explicitly pasted that content as a visible chat message and asked to include it. The renderer already filters these; do not defeat it. Redact secret-looking values (e.g. `ps_live_...`).

### Deployment identity safety (hard rules)
PreviewShip project names are deployment identities. Treat deploying with an existing project name as an overwrite/update, not as a harmless retry.

- Use the renderer-generated project name by default. It includes a stable suffix for the current Codex conversation, so repeated deployments from the same conversation update the same project while different conversations do not collide.
- Do not change `-n` to another existing project name after a failed deploy. Never list/search account projects to find a reusable name as a workaround.
- If PreviewShip reports a project count limit, quota limit, plan/subscription limit, permission limit, billing requirement, or upgrade requirement, stop immediately. Tell the user the deploy could not create a new project because of their PreviewShip plan, and ask them to upgrade/delete projects or explicitly provide a project name to update.
- Only deploy to a user-provided existing project name when the user explicitly supplied that exact project name in the current request, or when this same Codex conversation is being redeployed with the same renderer-generated project name.
- If the user explicitly asks to use an existing project name, mention that this will replace/update that PreviewShip project's content before returning the result.

## Workflow

### 1. Resolve the skill directory

```bash
SKILL_DIR="<directory containing this SKILL.md>"
```
Resolve it dynamically; never hard-code a user-specific path.

### 2. Render the current conversation

Single command — it auto-locates the current desktop session's JSONL and renders it:

```bash
mkdir -p /tmp/codex-chat-share
python3 "$SKILL_DIR/scripts/render_chat_html.py" --current --output /tmp/codex-chat-share/index.html
```

- `--current` reads `~/.codex/state_5.sqlite` (newest non-archived desktop thread) and falls back to the newest desktop `rollout-*.jsonl` in `~/.codex/sessions`. It prints the resolved path to stderr so you can confirm it matches the conversation being shared.
- If the user wants a **specific** conversation, or `--current` resolves to the wrong one, pass the JSONL explicitly instead:

```bash
python3 "$SKILL_DIR/scripts/render_chat_html.py" \
  --input "/Users/<you>/.codex/sessions/2026/06/05/rollout-...jsonl" \
  --output /tmp/codex-chat-share/index.html
```

  List recent sessions to pick one:
  ```bash
  sqlite3 ~/.codex/state_5.sqlite \
    "SELECT datetime(updated_at,'unixepoch','localtime'), substr(title,1,40), rollout_path \
     FROM threads WHERE archived=0 AND source='vscode' ORDER BY updated_at DESC LIMIT 10;"
  ```

The renderer also accepts a hand-written transcript JSON (`--input transcript.json`) as a fallback when no local JSONL is available; see "Transcript JSON shape" below.

### 3. Verify locally

```bash
python3 -m http.server 4173 --directory /tmp/codex-chat-share
```
Check (via a browser tool if available, otherwise inspect the file): page is not blank; message order is correct; the first turn is a real user/assistant exchange (not hidden context); no secrets are present; code blocks wrap/scroll cleanly.

### 4. Ensure the PreviewShip CLI is available and authenticated

```bash
command -v previewship || command -v npx
previewship whoami || npx -y previewship whoami
```
If not installed, use `npx -y previewship ...`. If `whoami` shows not authenticated, stop and tell the user:

```text
请前往 https://previewship.com 登录，创建 API Key，然后运行：
npx previewship login --key ps_live_YOUR_KEY
（或 export PREVIEWSHIP_API_KEY=ps_live_YOUR_KEY）
```
Re-run `whoami` after they confirm. Do not guess credentials. Node.js 20+ is required for the CLI.

### 5. Choose a deployment name

Default `-n` to the renderer-generated name. It is based on the conversation title plus a stable current-conversation suffix. Use it exactly; do not remove the suffix or replace it with another account project name.

```bash
PROJECT_NAME="$(python3 "$SKILL_DIR/scripts/render_chat_html.py" --current --print-project-name)"
```
Examples: `创建聊天记录分享技能` → `create-chat-record-sharing-skill-a1b2c3d4`; `分享当前 Codex 对话` → `share-current-codex-chat-a1b2c3d4`. Avoid the fixed name `codex-chat-share` unless the title and session identity are unavailable.

Override `PROJECT_NAME` only when the user explicitly provided a project name in the current request.

### 6. Deploy and return the URL

```bash
previewship deploy /tmp/codex-chat-share/index.html -n "$PROJECT_NAME" --json
# or: npx -y previewship deploy /tmp/codex-chat-share/index.html -n "$PROJECT_NAME" --json
```
Parse the JSON and return the public `previewUrl`. If JSON parsing fails, extract the URL from the CLI output only when unambiguous.

If the deploy fails with quota/plan/subscription/project-count/billing/permission language, stop and report the exact error summary. Do not retry by changing `PROJECT_NAME` to an existing project.

## Required output

At the end, return:
- The PreviewShip URL.
- The local HTML path (`/tmp/codex-chat-share/index.html`).
- Any fidelity limitation, e.g. earlier messages missing because the context was compacted, or images whose binaries were unavailable. Never claim a guaranteed 100% export when source content is missing.

## What the renderer parses (reference)

`render_chat_html.py` reads Codex rollout JSONL and turns visible turns into UI components. You normally don't need to touch this, but it helps when explaining limitations:
- `event_msg.user_message` → user bubble. `payload.message` is the text; `payload.images` / `payload.local_images` / image `text_elements` → right-aligned thumbnails.
- `event_msg.agent_message` with `phase=final_answer` → the visible assistant answer; other phases → collapsed processing detail under `已处理`.
- `event_msg.task_complete.duration_ms` → `已处理 <时长> ›`.
- `event_msg.patch_apply_end.changes` → edited-files card (per-file `+added -deleted`) and file artifact cards, attached to the final answer.
- Ignored as non-visible: `response_item.reasoning`, `function_call*`, `custom_tool_call`, `tool_search_*`, `turn_context`, `session_meta`, `compacted`, and any `AGENTS.md` / `<environment_context>` / `<skill>` / raw tool stdout.
- `response_item.message.content[]` is used only as a fallback when `event_msg` lines are absent.

Markdown is rendered through Codex's bundled `marked` (`scripts/md.mjs`) so tables, task lists, strikethrough, autolinks, and edge cases match Codex; skill/mention links become chips, file paths and external links are styled like Codex. Do not hand-roll Markdown parsing.

## Transcript JSON shape (fallback only)

When no local JSONL exists, `--input` also accepts a transcript object:

```json
{
  "title": "Codex Chat Share",
  "projectName": "codex-chat-share",
  "messages": [
    { "role": "user", "content": "用户消息 Markdown", "attachments": [{ "src": "/abs/or/url.png", "alt": "截图" }] },
    { "role": "assistant", "content": "助手消息 Markdown", "duration": "2m 51s", "timestamp": "星期四19:27",
      "details": ["默认折叠的处理过程"],
      "artifacts": [{ "title": "SKILL.md", "subtitle": "文档 · MD" }],
      "changes": [{ "path": "/abs/file.md", "added": 184, "deleted": 0 }] }
  ]
}
```
Only include `duration`/`timestamp`/`attachments`/`details`/`artifacts`/`changes` when visible in the chat. Local image paths are inlined as compressed thumbnail data URLs so the page stays self-contained and deployable. Add `"visible": false` to keep a message in the JSON but out of the page.

## Error handling

- Transcript incomplete (compaction): render what's visible and label the limitation in the final response.
- PreviewShip quota/permission/plan/project-count error: show the exact error summary and stop. Do not rename the deploy to an existing project unless the user explicitly provided that project name or this same Codex conversation is being redeployed with its stable renderer-generated name.
- Deploy succeeds but URL extraction fails: return the relevant CLI output plus the local file path.
- Sensitive-looking values (keys/tokens/passwords): redact unless the user explicitly asked to publish them.

## Example

User: `用 share-codex-chat 把这段对话部署出去`

Agent:
1. `python3 "$SKILL_DIR/scripts/render_chat_html.py" --current --output /tmp/codex-chat-share/index.html` (confirms resolved session path).
2. Verifies the HTML locally.
3. `previewship whoami`.
4. Reads the stable renderer-generated `PROJECT_NAME`.
5. `previewship deploy ... -n "$PROJECT_NAME" --json`.
6. Returns the PreviewShip URL + local path + any limitation.
