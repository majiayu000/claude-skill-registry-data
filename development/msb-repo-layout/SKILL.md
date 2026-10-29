---
name: msb-repo-layout
description: "Where things live in the msb-manager checkout and what each file is for: msbctl's internal shape (the Sandbox class, cmd_* handlers, main() argparse, the fzf menu with its numbered-prompt fallback), msb-picker, bootstrap.sh and how it is piped into the guest, defaults.toml, each template in templates/, and this repo's own .msb/. Use when you cannot find the code behind a behaviour, or when adding a file, a template or a command."
---

# Repo Layout

Detail carved out of `AGENTS.md`, which keeps only what has to hold in
every session. Repo-specific throughout; the facts here are verified against
msb 0.7.6 and re-checked on 0.7.7.

- `msbctl` — single-file Python CLI (~1900 lines). `Sandbox` class (config resolution, `msb` flag emission), `cmd_*` handlers, `main()` argparse at the bottom, fzf menu with numbered-prompt fallback.
- `msb-picker` — fzf picker used by the desktop entry (`msb-manager.desktop`).
- `bootstrap.sh` — runs once **inside the guest** at create time. `msbctl` pipes it in over stdin (not mounted, so manager code stays out of the VM). Intentionally not `set -e`: every step records its outcome and failures are summarized together so an allowlist can be built in one pass. Parameterized by `MSB_*` env vars.
- `defaults.toml` — what msb-manager ships: egress rule groups, version pins, baseline defaults. Read from the checkout, never copied.
- `templates/` — `config.toml.in` (the short skeleton of *local* overrides install.sh writes once), `sandbox.toml.in`, `dev.yaml.in`, `registry.toml.in`, `registry-repo.toml.in` (a sandbox with no folder), `registry-kandev.toml.in` (one Kandev owns).
- `.msb/` — this repo's own sandbox policy (`sandbox.toml`, `dev.yaml`).
