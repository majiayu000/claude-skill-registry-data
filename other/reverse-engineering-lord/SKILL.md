---
name: reverse-engineering-lord
description: Lord skill for reverse engineering shipped artifacts — native binaries, Electron/JavaScript apps, .NET assemblies, APKs, firmware, packages — via REA (rea-agents) CLI/MCP. Evidence-tiered analysis (observation/derivation/inference/unknown), provider-bring-your-own (Ghidra/IDA/Hopper/JADX), read-only by default.
triggers:
  - reverse engineering lord
  - reverse engineering
  - reverse engineer
  - decompile
  - disassemble
  - disassembly
  - ghidra
  - ida pro
  - hopper
  - binary analysis
  - firmware
  - frida
  - il2cpp
  - jadx
  - apktool
  - electron app
  - asar
  - pyinstaller
  - obfuscated
  - binary diff
  - هندسة عكسية
  - عكس هندسي
  - فك تجميع
  - تحليل ثنائي
  - ملف تنفيذي
  - ديكومبايل
personas:
  - SEC
  - ARCH
lord: true

---

# Reverse Engineering Lord

[SKILL] reverse-engineering-lord
[OBJ] Explain, compare, decompile, or reconstruct shipped artifacts with REA (`rea-agents` CLI/MCP server). Compressed doctrine adapted from morluto/rea (MIT) `.agents/skills/reverse-engineer-anything`.

[RULES]
1. [REQ] When to Use — Only when a claim depends on a shipped binary/package, decompilation, runtime evidence, or behavior NOT established by available source. Ordinary source-repo analysis → normal repo tools, never REA.
2. [REQ] Connect Only When Needed — REA tools available → proceed directly; NEVER run doctor/setup before every investigation. Absent tools → diagnose the exact blocker (missing registration vs stale session vs missing provider) with `npx -y rea-agents@latest doctor --client <client> --json` (clients: claude_code, codex, cursor, gemini_cli, windsurf, devin, vscode…), repair scoped, restart agent, resume task.
3. [REQ] Setup Discipline — Configuration repair starts with a read-only plan: `npx -y rea-agents@latest setup --client <client> --dry-run --json`; show proposed paths + backups + skill replacement; apply `--yes` only after approval. `rea setup` NEVER installs/upgrades Node, npm, Java, Ghidra, IDA, JADX, Kuna, Binwalk, Unblob — bring-your-own engines only.
4. [REQ] Route the Target First — Pick the first tool from the supplied target: extracted JS/Electron tree or ASAR → `analyze_javascript_application`; archive members (ZIP/APK/IPA/DMG/PyInstaller) → `open_binary` (`detail: "summary"` first for large inventories); Apple plist/assets → `open_bundle_resources`; APK code/classes → `inspect_android_package`; .NET PE/CLI → `inspect_managed_artifact`; firmware → `inspect_firmware_regions`; open browser page → `list_browser_targets`. Runtime options are metadata, not files.
5. [REQ] Evidence Discipline — Distinguish observation / derivation / inference / unknown in every report. Preserve provenance (paths, digests, offsets, source locations). Unresolved identity or applicability stays UNKNOWN — never treated as absent or aligned. Keep complete inline Evidence when the server does not advertise retained references.
6. [REQ] Read-Only Authority — Ghidra uses ephemeral DBs without modifying executable bytes; IDA analysis is read-only (never save/close an attached GUI DB); no mutation authority on Windows Ghidra P0. Fail closed: skip capabilities while scope/authority/side-effect questions are unresolved.
7. [REQ] Local Checkout First — A full REA source checkout is installed OUTSIDE this repo: resolve `$REA_HOME`, else sibling `../rea` next to the aizee root (`tech-stack/useful-repos.md` is the registry). Invoke through the engine-aware wrapper `node ../rea-cli.mjs <command> /abs/path --json` (sibling `rea-cli.mjs` next to the aizee root — it pins the checkout's `.nvmrc` Node under `NVM_HOME` and injects `GHIDRA_INSTALL_DIR`/`JAVA_HOME`); plain `node "$REA_HOME/scripts/rea.mjs"` also works for engine-free tasks; `npx -y rea-agents@6.7.0` is the last resort. All return the same Evidence record, no MCP needed for static JS/.NET/artifact work. Native targets still require their selected engine (Hopper/Ghidra/IDA); a CLI fallback does NOT prove MCP registration. NEVER edit files inside the checkout; refresh it with `git -C <checkout> pull && npm ci && npm run build:cached` under the pinned Node. Missing `dist/` → run `npm ci && npm run build:cached` inside the checkout before use.
8. [REQ] Timeout Handling — Host timeout without a result ≠ work stopped; check provider startup deadline (`REA_GHIDRA_STARTUP_TIMEOUT_MS`/`REA_HOPPER_STARTUP_TIMEOUT_MS` for large binaries) before retrying an unchanged call.
9. [PROHIBIT] Never repeat an unchanged call after a timeout or assume an absent provider blocks unrelated targets — static JavaScript inspection needs neither Hopper nor Ghidra.
10. [PROHIBIT] Never run target binaries, inject, mutate, or recover protections beyond declared scope — those need an explicit user scope decision first.
11. [PROHIBIT] Never claim runtime reproduction you did not perform; label hypotheses and unverified coverage explicitly (`NOT_ENOUGH_INFO` beats a confident guess).
12. [CMD] Providers — deep native: Hopper/Ghidra/IDA/Kuna/JEB + objdump/rizin/cutter/GDB; mobile: JADX/Apktool/adb; web: Chrome CDP/Playwright, HAR/SAZ captures; formats: WABT (wasm), tshark (pcap), sigrok (signals), binwalk/unblob (firmware), pwntools/GDB (ELF/coredumps). All caller-supplied.

[WORKFLOWS]
1. Feature-understanding — locate feature evidence in artifact → open target with routed tool → trace code/references → report observations vs inferences → reconstruct comparable implementation with tests if requested.
2. Binary triage — `open_binary` summary → inventory/sections/strings → pick deep provider if pseudocode needed → snapshot session → focused function/CFG reads → evidence ledger report.
3. Version comparison — inspect both artifacts → diff metadata/symbols/surface → report changed/unchanged/unknown with digests.
4. Recovery — diagnose blocker class (registration/provider/session/PATH) → minimal repair → verify tools visible in-session → resume original investigation.
