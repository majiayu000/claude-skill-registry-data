---
name: msb-testing
description: "Tests and spikes: tests/harness.py MsbctlTest giving each test a throwaway HOME and a freshly loaded msbctl with preflight() and the agent filter patched out and the network off, tests/fake/msb recording argv and the env vars a test names and exiting 2 on an unknown call, tests/fake/tailscale, assert_not_in_argv() to prove a planted secret never reaches argv, and the re-runnable spikes/NN-*.sh with the host-specific env vars each needs. Use when writing or debugging a test, or when a mechanism needs a real PASS/FAIL check on live msb."
---

# Testing

Detail carved out of `AGENTS.md`, which keeps only what has to hold in
every session. Repo-specific throughout; the facts here are verified against
msb 0.7.6 and re-checked on 0.7.7.

- `tests/` — stdlib `unittest`, run by `check.sh`: `tests/harness.py` (`MsbctlTest`) gives each test a throwaway HOME and a freshly loaded `msbctl`, with `preflight()` and the agent filter patched out and the network off; `tests/fake/msb` records argv and the env vars a test names, keeps state, and exits 2 on any call it does not know; `tests/fake/tailscale` records `serve` calls. Assert what reaches `msb`, and with `assert_not_in_argv()` that a planted secret does not.
- `spikes/NN-*.sh` — re-runnable PASS/FAIL scripts, one per mechanism the design relies on (SSH agent over vsock, mount ownership, per-port rules, persistence, hostname rules, memory reclaim, token placeholders, profile seeding, DNS rebind, a LAN model endpoint's key). Run one with `./spikes/07-claude-token-secret.sh`. Several need host-specific env vars (e.g. `ALLOW_HOST`, `ALLOW_PORT`) with no defaults, on purpose. Each must assert both the allowed and the denied half.
