---
name: openmotion
description: Create and edit videos with OpenMotion, recreate a reference video, or adapt an editable template. Connect to the OpenMotion Cloud Streamable HTTP MCP service and complete OAuth 2.1 login and onboarding when missing, then continue through the matching production workflow. Use for OpenMotion setup and first use; an already-selected specialist continues directly. Repository development does not trigger video production.
---

# OpenMotion

Turn a reference, template or creative brief into an editable video project in OpenMotion Cloud Studio, with real-time preview and MP4 export through the same workspace.

## Connect once

Discover the current host's OpenMotion MCP tools first. If connected to the target deployment origin, call `openmotion_get_project` to identify the workspace and resume existing work. Preserve projects, credentials, project/version identities and unrelated host settings. Do not reinstall or re-authenticate a working connection. An authorized OAuth client can access all of your projects in the selected workspace.

If OpenMotion is missing, disconnected, or pointed at a different deployment origin, read the maintained [cloud connection guide](https://github.com/nexu-io/openmotion/blob/main/docs/install.md) (or `<ORIGIN>/install.md` if the user specifies a target deployment) and follow its current-host instructions:
- Connect directly to the remote **Streamable HTTP `/mcp`** endpoint (`https://motion.open-design.ai/mcp` by default) using **OAuth 2.1** (or a workspace Personal Access Token `om_pat_*` when OAuth 2.1 is unavailable).
- Do **not** install an npm package, clone this repository, or start a local Studio/stdio backend.
- When the current host provides a built-in browser, prefer completing OAuth login and workspace consent inside that built-in browser (falling back to the system browser if unavailable or blocked), and wait for completion before verifying. Keep built-in vs. system browser cookie separation silent unless the user asks or hits a sign-in or workspace gate.
- For pure setup/install requests (no specific `projectId`, `templateId`, `skillId`, reference video, or creative brief), follow the maintained onboarding flow once the tools are available in the current chat. Use `/api/onboarding/prepare` for the localized welcome, cloud template library link/tab, and three frozen preview cards. Derive onboarding language from the user's request (`zh`, `en`, `ja`, `ko`, `fr`, `es`, `pt`, else `en`).
- For task-driven handoffs (the user already supplied a `projectId`, `templateId`, `skillId`, reference video, or creative brief), skip onboarding cards after authorization and continue directly with the user's task (carrying the full task verbatim if auto-handing off to a fresh conversation).

Installing this Skill with Skills CLI installs instructions only. Check that `openmotion_get_project` succeeds before claiming current-chat tool activation. After OAuth succeeds, tell the user they can send their creative request. If the tools are still unavailable and you cannot hand off to a ready conversation, ask the user to open a new Codex chat (or a new conversation in their MCP client) and send their request there. Keep `/install.md` internal to the Agent. Use `<ORIGIN>/mcp-setup` for any user-facing setup help.

Connecting alone does not request a film, project edit, export or paid generation. If the user only asked to install or connect, finish onboarding and wait. If they already supplied a creative brief, continue with it after setup.

## Continue with the matching workflow

Read the selected installed Skill, or its full MCP resource through `resources/read`. Cloud MCP serves all workflow guides dynamically via `resources/read`; do not depend on local sibling files in a standalone Skills CLI copy.

| User intent | Skill | MCP resource |
| --- | --- | --- |
| Original video, narrative, motion or sound design | openmotion-director | `openmotion://workflow/director/start` |
| Browse or adapt an existing editable template | openmotion-template-to-video | `openmotion://workflow/template/start` |
| Recreate a reference video for this film | openmotion-recreate | `openmotion://workflow/recreate/start` |
| Turn a reference into a reusable template | openmotion-video-to-template | `openmotion://workflow/video-to-template/start` |
| Scoped edits under established decisions, preview, troubleshooting or export | openmotion-production | `openmotion://workflow/production/start` |
| Generate an individual image, video, speech or music asset | openmotion-media | `openmotion://workflow/media/start` |

In cloud mode, import media with `openmotion_import_assets` using `action=prepare_upload` + `upload_ticket`, a public HTTPS `url`, or a zero-copy workspace `library_asset` (local disk `sourcePath` values are unsupported in cloud deployments).

Continue directly in that workflow, preserving the user's brief and existing decisions. These are instructions for the same Agent, not recursive tasks or a new creative intake. The selected workflow owns reference reading, revision protection, asset generation, preview and delivery. Read its conditional references as needed; do not load every workflow. Technical export validation, actual playback and human visual acceptance remain separate.
