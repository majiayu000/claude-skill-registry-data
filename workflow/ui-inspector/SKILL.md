---
name: ui-inspector
description: Understand screenshot controls with DOM first and optional OmniParser vision.
priority: P1
category: desktop
status: builtin-guidance
---

# UI Inspector

**Scope:** OmniParser / screenshot tooling. **Source:** https://github.com/microsoft/OmniParser

## Workflow

Follow DOM/accessibility tree first for browser pages. For arbitrary desktop screenshots with permission, optionally use OmniParser to identify UI elements and candidate click targets. Treat visual coordinates as guesses: check display scaling, multiple screens, app focus, occlusion and the target before using existing mouse/process tools. Do not auto-install large vision model weights, silently send private screenshots to hosted APIs, or act based on a low-confidence bounding box. Use cropped screenshots only with explicit consent. Verify each mutation by a fresh screenshot or accessibility snapshot; stop after repeated misses.

## Device and permission gates

Required authorization scopes: computer:read. Scripts, OS/desktop actions, external service side effects, media generation and paid API usage require independent user-approved execution permissions. This skill does not elevate Remote Arc Tool privileges or authorize use of hidden credentials.

## Preflight

Check the engines this skill names before relying on them, with tools you already have (for example `<engine> --version` through start_process, or list_directory on its install folder). Missing executors must be installed explicitly on the correct user device. A Skill being built-in is NOT evidence an engine is present.

## Evidence of completion

Report input constraints, executed tools and device, verified output path/result, permissions used, cost (if known) and failures. Do not imply successful execution from merely writing a plan.
