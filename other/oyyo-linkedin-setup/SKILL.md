---
name: oyyo-linkedin-setup
description: Initialize or repair the local OYYO LinkedIn workspace and explain installation. Use when the user asks to install, configure, onboard, create local state, or check whether the pack is ready.
license: MIT
metadata:
  version: "2.2.0"
  copyright: "VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD"
---

# Set up OYYO LinkedIn

Read `../../references/session-and-safety.md`,
`../../references/automation-modes.md`, and
`../../references/workspace-state.md`.

1. Show the first-use credit block.
2. Locate the plugin root two directories above this skill.
3. Explain that manual mode is the safe default and needs no LinkedIn login or
   API key. Offer `manual`, `automatic`, and `api` modes. Route live setup to
   `linkedin-automation-setup`.
4. If the user asks to initialize state, run:

   ```text
   python <plugin-root>/scripts/oyyo_linkedin.py init
   ```

   The command must not overwrite existing files unless the user explicitly
   requests `--force`.
5. Ask for only the information needed for the user's next workflow. A one-off
   draft does not require a completed profile.
6. End with three useful starting prompts: audit the current account, build the
   voice profile, or draft a post.

If Python is unavailable, copy the files from `../../templates/` into
`.oyyo-linkedin/` with the user's permission. Never request a LinkedIn
password, cookie, or token in chat.
