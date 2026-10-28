---
name: pb-tauri-e2e
description: >-
  Multi-phase E2E, live-app and binary security audit for Tauri v2
  desktop apps with sidecars: IPC, sidecars, CDP, canvas, permissions,
  ASD-STE100 report.
category: engineering-method
kind: playbook
trigger: ["test tauri app", "e2e tauri", "audit ao 2.0", "desktop app test", "tauri audit", "live test tauri"]
inputs: [app_dir, "test_suite?"]
requires:
  skills: [rust-pro, tauri-pilot, godmode-engineering, godmode-shipping, webapp-testing, playwright-skill, live-preview-canvas, plan-canvas, systematic-debugging, clean-code, quick-recap]
  agents: [reviewer, silent-failure-hunter, security-reviewer]
  mcps: [chrome-devtools, bdb-computer-use-mcp, open_design_mcp]
  tools: [cargo, tauri-driver, npx, curl, lsof]
  store: []
go_points: [ship-binary, publish-playbook]
outputs: ["production_artifacts/pb-tauri-e2e-<date>.md", "production_artifacts/ipc_benchmark.json", "production_artifacts/binary_security_audit.md", "production_artifacts/live_test_screenshots/"]
verify: "All IPC commands respond <10ms; Sidecar gracefully terminates on exit 0; 0 zombie processes; 0 open blocking findings; Live CDP & Computer-Use tests pass."
difficulty: advanced
est_time: 15-45 min
---

# Deep desktop, live app and E2E testing for Tauri v2
What you get: a complete multi-phase test, live interaction, and security audit for Tauri v2 (Rust Core + React 19 Frontend) desktop applications with sidecar architecture (such as BDB Agent Orchestrator), producing a deterministic ASD-STE100 audit report.

## Inputs
- app_dir — the Tauri application root directory (default: current directory or workspace root), containing `src-tauri/` and `src/`
- test_suite (optional) — specific test suite or scenario filter; defaults to full audit (all 8 phases)

## Live testing and debug tools

| Tool / MCP / Skill | Type | Function in playbook |
| :--- | :--- | :--- |
| `chrome-devtools` MCP | MCP Server | Connects the agent live via CDP (`--remote-debugging-port=9222`) to the running Tauri webview (`puppeteer_evaluate`, `puppeteer_screenshot`, `puppeteer_click`, console log streaming). |
| `bdb-computer-use-mcp` | MCP Server | Native OS-level desktop access: focus window (`activate_window`), native clicks, keyboard input, and screenshot inspection of macOS/Windows windows. |
| `tauri-driver` & Playwright | CLI / Tool | Official Tauri WebDriver for automated UI and event control via WebView2 (Windows) or WebKit (macOS). |
| `tester-army/e2e` | Framework | Replay-capable agent testing: natural action steps (`agent.act`) hashed and cached — regression runs incur zero model cost. |
| `live-preview-canvas` & `plan-canvas` | Skill / Tool | Interactive visual feedback layer: drop visual markers (red dots) and live annotations on UI bugs during test runs. |
| REA & Cutter methodology | Security | Static binary inspection of compiled Rust executable (ASLR/PIE, symbol stripping, secret leak scan). |

## Steps

1. Ponytail & Electron de-bloat scan (frontend hygiene & legacy stripping) — scan `src/` and `code_snippets/` for legacy Electron artifacts:
   - Regex audit: `grep -rn "ipcRenderer\|remote\|electron-store\|nodeIntegration\|process.type"`
   - Verify no synchronous Node.js `fs` calls run in browser context.
   - Verify Window 1 and Window 2 are configured as isolated webviews with no Node globals (`withGlobalTauri: false`).
2. Tauri v2 permission matrix & CSP audit (security and permissions architecture) — inspect `src-tauri/tauri.conf.json` and `src-tauri/capabilities/`:
   - Content Security Policy (CSP): no `unsafe-eval` and no unauthorized remote scripts in `default-src` and `script-src`.
   - Granular IPC permissions: only explicitly registered commands allowed from webview capabilities.
3. Rust core build & binary inspection (REA/Cutter methodology, stripping & strings scan):
   - Compile and audit Rust core: `cargo clippy --all-targets -- -D warnings` (strict type safety, zero unhandled unwraps).
   - Security audit of external crates: `cargo audit` (if installed).
   - Binary verification: `otool -hv target/release/*` (or `target/debug/*`) to verify PIE/ASLR.
   - Secret scan: `strings target/release/* | grep -E "AKIA|secret|bearer"` to verify no credentials are baked into the binary.
4. Sidecar process lifecycle & zombie reaper (graceful shutdown, port 3101 lock) — start the app and test daemon sidecar lifecycle (`ao :3101`):
   - Port binding: port 3101 must respond within 1,500ms after app start (`curl http://localhost:3101/health`).
   - Shutdown trapping: on app termination (SIGINT/SIGTERM), no zombie daemon process may remain (`lsof -i :3101` must be empty).
5. Rust IPC benchmark & multi-window bridge (latency and event stress testing):
   - Test IPC communication: 1,000 parallel or sequential `tauri.invoke("ping")` calls (or daemon HTTP/WS ping requests) — average latency must be < 2ms (p95 < 10ms).
   - Event emission from Window 1 to Window 2 must arrive losslessly without dropping frames on the main thread.
6. Live-app testing via CDP & Computer-Use MCP (live webview debugging & OS-level interaction):
   - Start Tauri with remote debugging: `--remote-debugging-port=9222` (or WebKit remote inspector).
   - Live CDP inspection (`chrome-devtools` MCP): attach to port 9222, capture live rendered state via `puppeteer_screenshot`, and check console logs (`puppeteer_evaluate`) for uncaught errors (`Uncaught TypeError`, CSP blocks).
   - OS-level interaction (`bdb-computer-use-mcp`): focus native window via `activate_window("BDB Agent Orchestrator")`, simulate OS mouse movements and clicks on window elements/menus, and test window resizing and multi-display behavior.
7. Replay-capable E2E UI testing (tester-army/e2e & Morphy Canvas stress test) — execute user scenarios:
   - Scenario 1: App starts with Window 1 (Vibe Coding).
   - Scenario 2: Morphy Canvas loads with zoom & pan (60 FPS benchmark).
   - Scenario 3: Create HTML MicroCard in sandboxed iframe mode (cross-origin isolation verified).
   - Scenario 4: Open Window 2 (Cloud Workspace) without freezing Window 1.
   - Replay caching: cache successful `agent.act` steps to enable deterministic replays without model cost.
   - Visual feedback: on UI regressions, trigger `live-preview-canvas` or `plan-canvas annotate` to place red-dot markers on screenshot evidence.
8. [GO] Binary and playbook sign-off — if releasing the binary or publishing artifacts (`ship-binary`, `publish-playbook`): review the test results, binary hardening evidence, and open findings before proceeding. The run stops here until the human types GO.
9. ASD-STE100 audit report & status traffic light — write the final report to `production_artifacts/pb-tauri-e2e-<date>.md`:
   - 🟢 GREEN (PASS): All IPC tests < 5ms, 0 zombie processes, 0 Electron artifacts, binary hardened with PIE/ASLR, live CDP and OS interactions clean.
   - 🟡 YELLOW (WARN): Functionally intact, but latency spikes, console warnings, missing cargo-audit, or unstripped dev symbols present.
   - 🔴 RED (BLOCKING): IPC hangs, zombie sidecar remaining after exit, open security vulnerabilities, or webview crash.

Run log: `production_artifacts/pb-tauri-e2e-<date>.md` in the start directory, never committed

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- GO is by contract in every harness. The go-gate hook is only a backstop on Claude Code, OpenCode and agy (Codex: unverified; Cursor, Kimi: none). A missing hook is never permission to proceed.
- A failed check stops the run: write the failure into the run log and report. No silent retries beyond what a step names.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
