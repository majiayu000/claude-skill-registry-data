---
name: heygen
description: HeyGen integration for AI agents via ClawLink — browser login, no API key setup. Connect HeyGen by pasting your API key. Watch the short video on the connect page if you need help finding it in HeyGen's dashboard. Use this skill when the user wants to work with HeyGen (AI & ML) — connect HeyGen, read or update HeyGen data, or take actions in HeyGen from chat instead of saying you cannot access it.
---

# HeyGen

Use **HeyGen** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect HeyGen once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect heygen   # opens browser → authorize HeyGen
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using HeyGen

```bash
npx @useclawlink/cli actions heygen "<what you want to do>"   # find an action
npx @useclawlink/cli describe heygen <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run heygen <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `heygen_add_looks_to_photo_avatar_group` | Tool to add additional looks (images) to an existing photo avatar group. Use when you need to expand an avatar group with new image variations. Maximum 4 image keys can be added per request. |
| `heygen_add_motion` | Tool to add natural motion or animation to an existing photo avatar, turning a still image into a moving, lifelike one. Use when you need to animate an avatar or add motion effects to a static photo avatar. The endpoint returns a new ID for the motion-enabled avatar. |
| `heygen_check_photo_look_generation_status` | Tool to retrieve the current status and details of a photo avatar or look generation by its ID. Use when you need to check if a photo avatar generation is complete or monitor generation progress. |
| `heygen_create_folder` | Tool to create a new folder under your HeyGen account. Use when you need to organize content by creating a new folder. Once created, you can place videos in the folder by providing the folder_id parameter when generating videos. |
| `heygen_create_knowledge_base` | Tool to create a new knowledge base with a specified name, opening line, and custom prompt for Interactive Avatar streaming sessions. Use when you need to set up a new knowledge base with custom AI behavior. |
| `heygen_create_photo_avatar_group` | Tool to create an avatar group which can include both AI-generated and user-uploaded photos of the avatar. Use when you need to create a new avatar group for training or managing avatar photos. |
| `heygen_create_webm_video` | Tool to create a WebM format video with transparent background featuring an avatar speaking text or audio. Use when you need to generate WebM videos with transparent backgrounds for overlaying on other content. Note that this API endpoint does not support custom avatars - only HeyGen's studio avatars are supported. The output format will be WebM instead of MP4 to preserve transparency. |
| `heygen_delete_an_avatar_video` | Tool to delete a video by its ID from HeyGen account. Supports deletion of both generated (avatar) videos and translated videos. Use when you need to remove a video that is no longer required or to manage storage. |
| `heygen_delete_asset` | Tool to delete a specific asset by its unique asset ID from HeyGen account. Use when you need to remove an asset (image, video, or audio) that is no longer required. |
| `heygen_delete_knowledge_base` | Tool to delete a specific knowledge base by its ID. Use when you need to permanently remove a knowledge base from the HeyGen streaming platform. |
| `heygen_delete_photo_avatar` | Tool to delete a photo avatar by its ID from HeyGen account. Use when you need to remove a photo avatar that is no longer required. |
| `heygen_delete_photo_avatar_group` | Tool to delete a photo avatar group by its ID from HeyGen account. Use when you need to remove a photo avatar group that is no longer required. |

## Notes

- **No API key for HeyGen itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect heygen`.
- The action list above is a snapshot; `npx @useclawlink/cli actions heygen` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
