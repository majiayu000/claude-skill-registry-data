---
name: run-cg-agent-harness
description: Build, run, drive, screenshot, and smoke-test the cgagentharness console (Rust axum server + browser UI) on a headless Linux box with a fake local model. Use when asked to run, start, launch, screenshot, or verify the harness/console/server end-to-end.
disable-model-invocation: true
---

# Run and verify the harness

Fresh homes use HTTPS and restricted account bootstrap. Prefer the maintained
public-backend and browser scripts over this directory's historical `driver.mjs`,
which assumes HTTP/auth-off startup and is not current acceptance evidence.
Do not apply those assumptions to a real home or use a key as a login substitute.

From the repository root, with the pinned toolchain and an isolated home:

```bash
cargo build --release --locked
python3 scripts/test-desktop-backend.py
node scripts/chat-browser-acceptance.mjs
```

The Python suite uses disposable homes, a real built backend, HTTPS/account
login and a mock local model. `CGAH_TEST_BINARY` selects another binary. The
browser suite uses installed Chrome and a Node runtime with WebSocket; it serves
mock APIs and checks the real console/CSP. `CHROME_BIN` selects Chrome. Neither
suite establishes actual-model or native WebKit acceptance.

For a real disposable Chrome/model coding workflow, follow
`docs/CONSOLE_JOBS.md` and `scripts/browser-fixture.py`. That fixture explicitly
opts into HTTP, retains account login, uses a local bare remote and mocks GitHub
publication. No actual GitHub write is part of acceptance.

For ordinary operation:

```bash
./target/release/cgagentharness serve
```

Use an unused port and one server per home. A fresh installation signs in with
`admin` / `admin` and requires password replacement. Native app trust and external
browser trust differ; follow `docs/SECURE_RESEARCH.md` rather than bypassing
certificate checks. Use its authenticated `account` and `web` CLI examples for
terminal operations. Preserve existing home/config/model state and never set a
global Git identity for disposable tests.

Run full repository checks per `AGENTS.md`. Actual native desktop verification is
macOS-specific and recorded separately in `docs/DESKTOP_ACCEPTANCE.md`; Linux
builds do not establish equivalent sandbox or WebKit behavior.
