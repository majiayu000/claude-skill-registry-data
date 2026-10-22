---
name: make-bot-ui
description: "Explain the inactive Cursor/Grok Bot integration and its missing native integrations. Use when the original make-bot-ui workflow is requested. Diagnostic only; this port cannot create its routines, secrets, webhook runner, or bot connection."
disable-model-invocation: true
---

# Make bot UI

This skill is diagnostic only in the shared pstack port. The original Cursor/Grok Bot workflow is preserved in the untouched upstream snapshot. It is not operational here.

Read the unsupported-integration limits through [CODEX.md](../../CODEX.md). This port has no adapter for Cursor routine creation, secret-request cards, Cursor webhook endpoints, connector credential files, or wake-on-webhook execution. Do not request a sender key in chat, invent a routine ID, install networking software, or present a static page as a connected bot.

If invoked, explain the missing capabilities and identify the intended user flow. A replacement would require a separately scoped service, authentication design, secret handling, deployment target, and real trigger runner. Keep a proposed design or draft within the requested scope. Do not claim the original integration was installed or verified.
