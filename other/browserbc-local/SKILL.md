---
name: browserbc-local
description: "Use when Codex needs to operate the local BrowserBC / Journey Forge browser-workflow recorder installed on this Windows machine: start or verify the local server, rebuild or locate the Chrome extension, record browser workflows, inspect BrowserBC-generated skills, or adapt BrowserBC output into Codex skills. Also use when the user mentions BrowserBC, Browser-BC, Journey Forge, browser recording, trace-to-skill, or recording browser actions into reusable skills."
---

# BrowserBC Local

## Local Installation

The BrowserBC / Journey Forge checkout is installed at:

```text
D:\agent-workflow-lab\harnesses\browser-bc
```

The local control panel runs at:

```text
http://127.0.0.1:8099/
```

The built Chrome extension directory is:

```text
D:\agent-workflow-lab\harnesses\browser-bc\extension\dist\chrome-mv3
```

Read `references/local-setup.md` when you need the exact installation notes, verification results, or manual commands.

## Quick Workflow

1. Check the local installation before changing anything:

   ```powershell
   powershell -ExecutionPolicy Bypass -File C:\Users\Administrator\.codex\skills\browserbc-local\scripts\browserbc_local.ps1 status
   ```

2. If the server is not running, start it:

   ```powershell
   powershell -ExecutionPolicy Bypass -File C:\Users\Administrator\.codex\skills\browserbc-local\scripts\browserbc_local.ps1 start
   ```

3. If the Chrome extension is missing or stale, rebuild it:

   ```powershell
   powershell -ExecutionPolicy Bypass -File C:\Users\Administrator\.codex\skills\browserbc-local\scripts\browserbc_local.ps1 build-extension
   ```

4. Ask the user to load the unpacked Chrome extension from the reported `extension\dist\chrome-mv3` directory if it is not already loaded.

5. Keep secrets out of chat and Git. BrowserBC needs an LLM key only when distilling recordings into skills. Do not create, print, or sync `.env.local`; if configuration is needed, direct the user to set it locally through BrowserBC's panel or a private ignored file.

## Codex Skill Adaptation

BrowserBC's default output target is Claude-style skills under `C:\Users\Administrator\.claude\skills`. Treat those outputs as drafts, not automatically trusted Codex skills.

When adapting BrowserBC output into Codex:

- Prefer a temporary review folder first by setting `JFL_SKILLS_ROOT` outside both global Codex and Claude skill roots.
- Inspect generated `SKILL.md`, `TRACE_GUIDE.md`, `meta.json`, and `evidence.jsonl`.
- Remove site-specific credentials, private URLs, personal data, cookies, request bodies, and fragile selectors.
- Convert the final result into a normal Codex skill under `C:\Users\Administrator\.codex\skills\<skill-name>`.
- Sync the complete runnable bundle into `D:\工作流优化\codex-research-workflow-html\skills\<skill-name>` and run the normal repo/global validation and SHA-256 parity checks.

## Validation Commands

Use these smoke checks after setup or repair:

```powershell
cd D:\agent-workflow-lab\harnesses\browser-bc
.\.venv\Scripts\python.exe -c "import server.server; print('server import ok')"
.\.venv\Scripts\python.exe -m harness.main --help
cd extension
npx --yes pnpm@11.9.0 run typecheck
npx --yes pnpm@11.9.0 run build
```

For this wrapper skill itself, validate with:

```powershell
python C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\Administrator\.codex\skills\browserbc-local
```
