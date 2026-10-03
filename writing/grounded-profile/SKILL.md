---
name: grounded-profile
description: Show or change the grounded-copy writing mode.
---

# grounded-profile

Use this skill when the user explicitly asks to view or change the writing mode.

    $grounded-profile chat
    $grounded-profile copy
    $grounded-profile off
    $grounded-profile status

Run `python scripts/profile.py <operation>` from this skill directory. Accept exactly `chat`, `copy`, `off`, or `status` as the operation.

`chat` applies everyday writing rules. `copy` adds rules for promotional text. `off` stops the rules and reminders. `status` shows the saved setting.

The setting is saved at `$CODEX_HOME/grounded-copy/profile`, using `~/.codex` as the default home. After a successful change, report the status and apply the printed instructions from this turn forward. If saving fails, report the error.
