---
name: webapp-testing
description: "Adapt the popular webapp-testing skill to Mikka's Node/Playwright and isolated server workflow. Use for actual user-flow verification, regression reproduction, screenshots, API/DB readback, navigation and failure handling."
---

# Web application testing — Mikka adapter

Method adapted from https://github.com/anthropics/skills/tree/main/skills/webapp-testing (Apache-2.0 upstream). **Upstream Python `with_server.py` is not installed**: Mikka vendors no external executable skill scripts. Use project-owned cloud Linux bootstrap and installed Node/Playwright browser tools, or [mikka-browser-qa](../mikka-browser-qa/SKILL.md).

Read `docs/acceptance.md`, `docs/ci/test-ownership.md` and current owner/test scripts before adding a runner. Keep public/hosted source pair fixed; choose authorized isolated accounts, PostgreSQL and fixture cleanup.

Use reconnaissance (DOM/accessibility snapshot/route) before selectors. Reproduce failures on the original behavior: initial render, click/pending, actual server ACK/error, refresh/readback, navigation, permission changes and recovery. Assert an independently observable result, not a mocked callback or an automatically generated expected value.

For an SSE/WS chat, use ready states and bounded waits, not blanket network-idle. Protect existing test ownership and only add a new test for a distinct, falsifiable contract; retain pre-fix red and post-fix green evidence. Use affected tests and PR screenshots, **not** the retired repository-wide browser E2E CI gate. Physical device, signed Mac and real external-provider acceptance remain separately labeled.
