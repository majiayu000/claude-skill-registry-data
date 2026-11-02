---
name: desktop-operator
description: Move pointer, drag, type and click in a permitted local desktop session.
priority: P0
category: desktop
status: builtin-guidance
---

# Desktop Operator

**Scope:** PyAutoGUI / native OS accessibility. **Source:** https://github.com/asweigart/pyautogui

## Workflow

Prefer native accessibility tree/API when available, then screenshot-based coordinates as fallback. On macOS request Accessibility + Screen Recording permission through the OS; on Windows control the actual Windows desktop via an explicit native helper, not a WSL X display. Use existing Remote Arc process permission and scoped device approval for scripts. For mouse movement, calculate a short monotonic path with easing, bounded duration and screen dimensions; screenshot before/after to verify. Never silently move the pointer on a device the user is actively using. Confirm focused app and coordinates before typing, especially passwords, financial transfers or destructive actions. Do not attempt to bypass OS consent dialogs. PyAutoGUI installation and permission are opt-in per device.

## Device and permission gates

Required authorization scopes: computer:read, computer:write. Scripts, OS/desktop actions, external service side effects, media generation and paid API usage require independent user-approved execution permissions. This skill does not elevate Remote Arc Tool privileges or authorize use of hidden credentials.

## Preflight

Check the engines this skill names before relying on them, with tools you already have (for example `<engine> --version` through start_process, or list_directory on its install folder). Missing executors must be installed explicitly on the correct user device. A Skill being built-in is NOT evidence an engine is present.

## Evidence of completion

Report input constraints, executed tools and device, verified output path/result, permissions used, cost (if known) and failures. Do not imply successful execution from merely writing a plan.
