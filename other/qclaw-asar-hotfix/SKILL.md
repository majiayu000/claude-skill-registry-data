---
name: qclaw-asar-hotfix
description: "Patch packaged QClaw.app (no source code) by modifying app.asar frontend bundles. Use when users have older QClaw versions and need to: (1) make invite-code checks only active on localhost with DEV_MODE=true and bypassed in production, (2) remove visibility restrictions for `other` and `system-config` model providers, and (3) ensure these providers appear in the model vendor dropdown."
---

# QClaw Asar Hotfix

## Overview

Use this skill when the user only has a packaged `QClaw.app` and needs the same frontend hotfix across old versions.

This skill ships one deterministic patcher script:
- `scripts/patch_qclaw_asar.py`

## Workflow

1. Run patch in non-destructive mode first.

```bash
python3 /Users/tangchunwu/.codex/skills/qclaw-asar-hotfix/scripts/patch_qclaw_asar.py \
  --app /Applications/QClaw.app \
  --output ~/Desktop/app.asar.patched \
  --no-install
```

2. If patch summary looks correct, apply to the app in place.

```bash
python3 /Users/tangchunwu/.codex/skills/qclaw-asar-hotfix/scripts/patch_qclaw_asar.py \
  --app /Applications/QClaw.app
```

3. Ask the user to fully quit and reopen QClaw.

## What The Script Patches

- Invite-code gate in chat/login frontend:
  - Enable check only when `location.hostname=="localhost" && localStorage.DEV_MODE==="true"`
  - Bypass in production/non-localhost
- Model provider visibility:
  - Remove frontend filters that hide `system-config`
  - Add `other` provider option to model vendor dropdown when missing
  - Ensure provider sets/maps include `other` and `system-config`

## Validation Checklist

After patching, verify by extracting the output asar and checking these expectations:

1. Invite code gate is DEV_MODE-local only.
2. Model-setting provider list includes both `other` and `用户系统配置`.
3. No residual filter like `filter(k=>k.key!==vn)` for provider visibility.

Suggested checks:

```bash
TMP=$(mktemp -d)
cd "$TMP"
npx -y @electron/asar extract /Applications/QClaw.app/Contents/Resources/app.asar ext
rg -n -F 'localStorage.getItem("DEV_MODE")==="true"' ext/out/renderer/assets/*.js
rg -n -F 'key:"other",label:"其他"' ext/out/renderer/assets/*.js
rg -n -F 'key:vn,label:"用户系统配置"' ext/out/renderer/assets/*.js
rg -n -F 'l.filter(k=>k.key!==vn)' ext/out/renderer/assets/*.js || true
```

## Rollback

The script creates a backup next to `app.asar`:
- `app.asar.bak.hotfix.<timestamp>`

Rollback command:

```bash
cp /Applications/QClaw.app/Contents/Resources/app.asar.bak.hotfix.<timestamp> \
   /Applications/QClaw.app/Contents/Resources/app.asar
```

## Notes

- Prefer running with `--no-install` first for unknown versions.
- If script reports `未匹配到可修改的补丁位点`, inspect `out/renderer/assets/*.js` and extend patch literals/regex in `scripts/patch_qclaw_asar.py`.
- Keep edits scoped to renderer bundles; do not modify binary/executable files.
