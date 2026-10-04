---
name: vault-ai-chat
description: "AI-powered local vault memory and context-aware chat with any OpenAI-compatible API."
source: vault-ai-chat
---

# AI Vault Memory

## Plugin metadata

- **id:** `vault-ai-chat`
- **source:** vault-native
- **plugin-type:** community
- **status:** enabled
- **class:** FULL
- **has-settings:** true

### Commands

- `vault-ai-chat:open-memory` -- AI Vault Memory: Open memory search
- `vault-ai-chat:rebuild-memory` -- AI Vault Memory: Rebuild vault memory index
- `vault-ai-chat:index-current-file` -- AI Vault Memory: Index current file
- `vault-ai-chat:analyze-current-file` -- AI Vault Memory: تحلیل این یادداشت (Analyze)
- `vault-ai-chat:send-selection-to-chat` -- AI Vault Memory: ارسال بخش انتخاب‌شده به چت هوش مصنوعی
- `vault-ai-chat:ai-inline-prompt` -- AI Vault Memory: اعمال هوش مصنوعی روی متن انتخاب‌شده
- `vault-ai-chat:compare-two-files` -- AI Vault Memory: مقایسه دو فایل
- `vault-ai-chat:forget-current-file` -- AI Vault Memory: Forget current file from memory

# AI Vault Memory

**Description:** AI-powered local vault memory and context-aware chat with any OpenAI-compatible API.
**Status:** Enabled
**Plugin ID:** vault-ai-chat

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `vault-ai-chat:open-memory` -- AI Vault Memory: Open memory search
- `vault-ai-chat:rebuild-memory` -- AI Vault Memory: Rebuild vault memory index
- `vault-ai-chat:index-current-file` -- AI Vault Memory: Index current file
- `vault-ai-chat:analyze-current-file` -- AI Vault Memory: تحلیل این یادداشت (Analyze)
- `vault-ai-chat:send-selection-to-chat` -- AI Vault Memory: ارسال بخش انتخاب‌شده به چت هوش مصنوعی
- `vault-ai-chat:ai-inline-prompt` -- AI Vault Memory: اعمال هوش مصنوعی روی متن انتخاب‌شده
- `vault-ai-chat:compare-two-files` -- AI Vault Memory: مقایسه دو فایل
- `vault-ai-chat:forget-current-file` -- AI Vault Memory: Forget current file from memory

## Configuration File

Settings path: `.obsidian/plugins/vault-ai-chat/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/vault-ai-chat/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/vault-ai-chat/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Current Configuration

These are the plugin's current settings (sensitive values redacted):

```
settings:
  language: fa
  apiBaseUrl: https://api.openai.com/v1
  chatModel: gpt-4o-mini
  chunkSize: 1000
  chunkOverlap: 180
  resultCount: 8
  autoIndex: true
  excludedFolders: Templates,Archive
  systemPrompt: You are AI Vault Memory, a precise Obsidian knowledge assistant. Reply in the user's language. Use only provided context when making claims about the vault. Cite vault material as [[path]]. State clearly when context is insufficient.
  enableStreaming: true
database:
  chunks:
    ARCHITECTURE.md#0:13sez4w:
      id: ARCHITECTURE.md#0:13sez4w
      filePath: ARCHITECTURE.md
      heading: FORGE-OS architecture
      text: FORGE-OS separates the visible FORGE workspace from the Linux substrate. FORGE owns Explorer, Applications, System, Workspace Intelligence, chat, terminal, tasks, agent actions, recovery UI, and update entry points. Arch owns the kernel, systemd, PAM, package database, devices, filesystems, networking, audio, and hardware services. KWin/Plasma provide compositor and desktop services beneath FORGE.
      hash: 13sez4w
      updatedAt: 1787564007897
      terms: [55 items: architecture, forge-os, architecture...]
    ARCHITECTURE.md#1:1fvx8om:
      id: ARCHITECTURE.md#1:1fvx8om
      filePath: ARCHITECTURE.md
      heading: Boot and ownership
      text: [string, 647 chars]
      hash: 1fvx8om
      updatedAt: 1787564007897
      terms: [74 items: architecture, boot, and...]
    ARCHITECTURE.md#2:1yg8jig:
      id: ARCHITECTURE.md#2:1yg8jig
      filePath: ARCHITECTURE.md
      heading: Recovery
      text: `autovt@tty2.service` aliases the on-demand FORGE recovery unit. Ctrl+Alt+F2 creates a separate greetd socket, D-Bus, KWin, and `FORGE_RECOVERY_MODE=1` application. It is not started at boot and does not create a second active compositor until requested. Diagnostics run as the configured desktop user; rollback uses a narrow privileged helper after two integrity checks.
      hash: 1yg8jig
      updatedAt: 1787564007897
      terms: [architecture, recovery, autovt, tty2, service, aliases, the, on-demand, forge, recovery, unit, ctrl, alt, f2, creates, separate, greetd, socket, d-bus, kwin, and, forge_recovery_mode, application, it, is, not, started, at, boot, and, does, not, create, second, active, compositor, until, requested, diagnostics, run, as, the, configured, desktop, user, rollback, uses, narrow, privileged, helper, after, two, integrity, checks]
    ARCHITECTURE.md#3:1k2kogn:
      id: ARCHITECTURE.md#3:1k2kogn
      filePath: ARCHITECTURE.md
      heading: Runtime identity and lifecycle
      text: [string, 780 chars]
      hash: 1k2kogn
      updatedAt: 1787564007897
      terms: [103 items: architecture, runtime, identity...]
    ARCHITECTURE.md#4:7gjzfu:
      id: ARCHITECTURE.md#4:7gjzfu
      filePath: ARCHITECTURE.md
      heading: Package architecture
      text: [string, 737 chars]
      hash: 7gjzfu
      updatedAt: 1787564007897
      terms: [94 items: architecture, package, architecture...]
    ARCHITECTURE.md#5:cz1eyj:
      id: ARCHITECTURE.md#5:cz1eyj
      filePath: ARCHITECTURE.md
      heading: Shared application architecture
      text: [string, 630 chars]
      hash: cz1eyj
      updatedAt: 1787564007897
      terms: [87 items: architecture, shared, application...]
    ARCHITECTURE.md#6:1dcwccj:
      id: ARCHITECTURE.md#6:1dcwccj
      filePath: ARCHITECTURE.md
      heading: Release boundary
      text: Source gates prove syntax, dependency resolution, tests, lint, types, bundles, and manifest consistency. Stable publication additionally requires clean/native packages, ISO boot and physical/VM acceptance, cross-platform metadata parity, signing/channel rules, and local-versus-remote artifact hashes. See [the release checklist](docs/RELEASE_CHECKLIST.md).
      hash: 1dcwccj
      updatedAt: 1787564007897
      terms: [architecture, release, boundary, source, gates, prove, syntax, dependency, resolution, tests, lint, types, bundles, and, manifest, consistency, stable, publication, additionally, requires, clean, native, packages, iso, boot, and, physical, vm, acceptance, cross-platform, metadata, parity, signing, channel, rules, and, local-versus-remote, artifact, hashes, see, the, release, checklist, docs, release_checklist, md]
    BUILD_STATE.md#0:1utox92:
      id: BUILD_STATE.md#0:1utox92
      filePath: BUILD_STATE.md
      heading: Current build state
      text: Updated: 2026-08-21
Source version: `0.2.3-test.1` (test ISO candidate; not stable)
Pinned FORGE source: `1e69e647082ab9e35b2dcf3b5331dc1994911471`
      hash: 1utox92
      updatedAt: 1787564007898
      terms: [build_state, current, build, state, updated, 2026-08-21, source, version, 3-test, test, iso, candidate, not, stable, pinned, forge, source, 1e69e647082ab9e35b2dcf3b5331dc1994911471]
    BUILD_STATE.md#1:1oc17e5:
      id: BUILD_STATE.md#1:1oc17e5
      filePath: BUILD_STATE.md
      heading: Implemented
      text: [string, 1000 chars]
      hash: 1oc17e5
      updatedAt: 1787564007898
      terms: [132 items: build_state, implemented, canonical...]
    BUILD_STATE.md#2:16802vi:
      id: BUILD_STATE.md#2:16802vi
      filePath: BUILD_STATE.md
      heading: Implemented
      text: [string, 1000 chars]
      hash: 16802vi
      updatedAt: 1787564007898
      terms: [129 items: build_state, implemented, restart...]
    BUILD_STATE.md#3:1pf71z8:
      id: BUILD_STATE.md#3:1pf71z8
      filePath: BUILD_STATE.md
      heading: Implemented
      text: [string, 999 chars]
      hash: 1pf71z8
      updatedAt: 1787564007898
      terms: [123 items: build_state, implemented, the...]
    BUILD_STATE.md#4:ms9un5:
      id: BUILD_STATE.md#4:ms9un5
      filePath: BUILD_STATE.md
      heading: Implemented
      text: [string, 1000 chars]
      hash: ms9un5
      updatedAt: 1787564007898
      terms: [140 items: build_state, implemented, raphical...]
    BUILD_STATE.md#5:1g90ks3:
      id: BUILD_STATE.md#5:1g90ks3
      filePath: BUILD_STATE.md
      heading: Implemented
      text: RGE_REF`, preventing a moving FORGE `main` from changing the image after source verification.
- The pinned shared renderer uses routed dialogs for file/folder, goal/task, persistent-task, and rename actions; every renderer button has a route contract.
- Home is available on macOS, Windows, Linux, and as the FORGE-OS default. Explorer loads folders on demand, while bounded discovery skips unreadable/container-backed subtrees instead of aborting on `EACCES`.
      hash: 1g90ks3
      updatedAt: 1787564007898
      terms: [65 items: build_state, implemented, rge_ref...]
    BUILD_STATE.md#6:j5g9d3:
      id: BUILD_STATE.md#6:j5g9d3
      filePath: BUILD_STATE.md
      heading: Verification gates
      text: [string, 784 chars]
      hash: j5g9d3
      updatedAt: 1787564007898
      terms: [108 items: build_state, verification, gates...]
    BUILD_STATE.md#7:iuexei:
      id: BUILD_STATE.md#7:iuexei
      filePath: BUILD_STATE.md
      heading: Hardware acceptance still required
      text: [string, 900 chars]
      hash: iuexei
      updatedAt: 1787564007898
      terms: [120 items: build_state, hardware, acceptance...]
    CHANGELOG.md#0:zf66ru:
      id: CHANGELOG.md#0:zf66ru
      filePath: CHANGELOG.md
      heading: Workspace/UI and documentation correction
      text: [string, 999 chars]
      hash: zf66ru
      updatedAt: 1787564007899
      terms: [126 items: changelog, workspace, ui...]
    CHANGELOG.md#1:u58ol2:
      id: CHANGELOG.md#1:u58ol2
      filePath: CHANGELOG.md
      heading: Workspace/UI and documentation correction
      text: ish implemented source from old planning claims. Automatic watch reindexing, package/executable Explorer inspection, a separate top-bar Intelligence popover, packaged Ollama skill assets, and cross-platform parity workflow/script remain explicit gaps.
- Removed the stale tracked `build/node22-bindir` temporary path and the obsolete duplicated 0.2.2 release/session runbooks.
      hash: u58ol2
      updatedAt:
[...truncated -- full settings in data.json]
```
(1 sensitive field(s) redacted)

For full settings, read: `.obsidian/plugins/vault-ai-chat/data.json`

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/data/skills/vault-ai-chat.readme.md")

## Usage

When the user asks for functionality related to AI Vault Memory:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/vault-ai-chat/data.json). If it does not exist, that is normal -- create it with the required settings
3. Configure the plugin by writing data.json with the values needed for the task
4. Execute the task using the appropriate tool:
   - For Obsidian-native commands (including file export): use execute_command
   - For CLI-based conversion needing Pandoc/LaTeX: use execute_recipe
   - For data queries: use call_plugin_api
5. If a command opens a UI dialog, tell the user what to click.

CRITICAL RULES:
- Prefer native Obsidian commands over external tools when both can accomplish the task.
- NEVER create fake output files. If the user asks for a PDF/DOCX/image export, use execute_recipe -- do NOT write content to a .pdf file yourself.
- If a dependency is missing (e.g. Pandoc), tell the user what to install.
IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
