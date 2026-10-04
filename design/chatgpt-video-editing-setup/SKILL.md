---
name: chatgpt-video-editing-setup
description: "Set up, repair, or verify the local AI short-video environment: video-use, FFmpeg, the Source Han Sans TW subtitle font, ElevenLabs credentials, and optional HyperFrames skills. Use whenever a user asks to install, configure, fix, reconnect, or check this editing environment. Do not use for Premiere or CapCut help, or to edit/transcribe media; hand those requests to the editing workflow after setup is verified."
---

# ChatGPT Video Editing Setup

Prepare or repair the environment without starting creative work. The outcome is
an evidence-backed readiness report, not a transcript, upload, edit, preview, or
render.

## Read first

Read [the setup runbook](references/setup-runbook.md) for commands and install
choices. Read [security and verification](references/security-and-verification.md)
before handling credentials or declaring anything ready.

## Operating sequence

1. Inspect before changing anything: check the stable paths
   `~/Developer/video-use` and, only when requested, `~/Developer/hyperframes`.
   Recognize normal checkouts and linked worktrees with `git rev-parse`, then
   capture each repository's exact origin, branch or detached state, commit,
   and status. Also check available runtime tools, the Source Han Sans TW
   subtitle font in the user's font directory, and the active agent's Skills
   location. Do not print secrets.
2. Treat any existing path that is not a Git worktree as a hard stop. The only
   accepted origins are the exact official HTTPS URLs in the runbook. A missing
   or different origin and a dirty status are also hard stops: report the
   evidence, never rewrite the remote automatically, and do not pull, reset,
   overwrite, install dependencies, or register a Skill.
3. State the exact mutations needed, including clones, package installs, font
   downloads, large downloads, or Skills-directory changes. Obtain explicit
   approval before any of them. Inspection and a no-cost local version check do
   not imply approval to mutate.
4. After approval, follow the runbook exactly and repeat the repository
   preflight immediately before dependency installation or Skill registration.
   Install/register the complete video-use repository so its helpers remain
   available. Install the Source Han Sans TW subtitle font only from the
   official Adobe Fonts repository, never overwriting an existing font file.
   Treat HyperFrames as optional unless the user specifically needs HTML, CSS,
   or GSAP animation; when requested, require Node.js 22 or newer.
5. Configure ElevenLabs only through an existing environment variable or the
   protected `~/Developer/video-use/.env` path. Never echo, log, or commit a
   credential.
6. Verify with local, no-paid-work checks only, including the subtitle font
   files. Run HyperFrames repository, Node, lockfile, and Core Skills checks
   only if HyperFrames was explicitly approved and installed; otherwise report
   it as not requested. Do not upload media, call transcription, create an edit
   directory, or edit/render video.
7. Report checked paths, approved mutations performed, evidence, versions or
   command outcomes, remaining gaps, and the explicit next action. Never claim
   readiness without successful evidence.

## Handoff boundary

Before any later first media upload to ElevenLabs, identify the source file,
state that it will be uploaded for transcription with ElevenLabs Scribe v2, note
that account quota or charges may apply, and obtain consent. Setup itself ends
before that point.
