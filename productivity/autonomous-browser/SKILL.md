---
name: autonomous-browser
description: Plan multi-step browser work using browser-use with an approved model budget.
priority: P0
category: browser
status: builtin-guidance
---

# Autonomous Browser

**Scope:** browser-use Python library. **Source:** https://github.com/browser-use/browser-use

## Workflow

Use available CLI tools or documented APIs for technical tasks such as deployments, migrations, cloud administration, configuration, builds, logs and database work. A web dashboard alone does not justify a browser workflow. Honor explicit user tool preferences; use this skill only when actual webpage interaction is required.

Use only when deterministic DOM actions fail or multi-step planning is essential. browser-use is a separate Python reasoning engine and may use chargeable LLM APIs. Do not create paid cloud sessions by default. Require an explicit device/browser permission, named objective, URL allowlist, max iterations, timeout, model budget and human checkpoints. Prefer local browser and a caller-provided model account; never assume API credits are free. Inspect planned actions, execute only authorized ones, and save a scrubbed action/evidence log. Stop on CAPTCHA, account lock, MFA, payments, new unknown domains and repeated failures. A user can instead choose the zero-model-cost Browser Operator. No autostart and no implicit installation.

## Device and permission gates

Required authorization scopes: browser:read, browser:interact. Scripts, OS/desktop actions, external service side effects, media generation and paid API usage require independent user-approved execution permissions. This skill does not elevate Remote Arc Tool privileges or authorize use of hidden credentials.

## Preflight

Check the engines this skill names before relying on them, with tools you already have (for example `<engine> --version` through start_process, or list_directory on its install folder). Missing executors must be installed explicitly on the correct user device. A Skill being built-in is NOT evidence an engine is present.

## Evidence of completion

Report input constraints, executed tools and device, verified output path/result, permissions used, cost (if known) and failures. Do not imply successful execution from merely writing a plan.
