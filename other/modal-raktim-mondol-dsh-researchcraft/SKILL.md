---
name: modal
description: "Use Modal for GPU/CPU remote compute beyond what the modal_run tool covers — Volumes, Secrets, Queues, deployed apps/endpoints."
---

# modal

Load this before any Modal task that is more than "run one command remotely and get the result back" — that narrower case is already covered by the built-in `modal_run` tool (upload inputs, run `command` on a remote CPU/GPU instance, download outputs, always terminates the instance).

Reach beyond `modal_run` — via the `bash` tool and the `modal` CLI — for anything it doesn't do: deploying a persistent app or web endpoint, managing a `modal.Volume`/`modal.Secret`/`modal.Queue`/`modal.Dict` directly, hot-reloading a Modal app during development, or inspecting logs/billing for an existing deployment.

## Prerequisites

- `MODAL_TOKEN_ID` / `MODAL_TOKEN_SECRET` (Settings -> ResearchCraft API keys, or env) — same credentials `modal_run` uses.
- The `modal` CLI (ships with the `modal` Python package). **Install it yourself if it's missing** — don't ask the user to do it:

  ```bash
  if ! command -v modal >/dev/null 2>&1; then
    uvx modal --version   # run ad hoc per call, no persistent install needed
    # or, for a persistent CLI across a long session:
    uv tool install modal
  fi
  modal --version
  ```

  `uvx modal ...` needs no install step at all (fetches and runs on demand) — reach for `uv tool install modal` only if a task will call `modal` many times and the per-call `uvx` overhead actually matters.
- Modal is cloud-only — there is no local dev mode; every `modal` CLI call needs network access and a configured token.

## Working with the CLI

The CLI surface moves faster than any static doc — run `modal --help` / `modal <command> --help` and trust that over anything below, and check `modal changelog --since <date>` if something looks newer than expected:

```
modal --version                 # confirm the SDK/CLI version in use
modal run <file>::<fn>          # run a Modal function or local entrypoint once
modal deploy <file>              # deploy a persistent app
modal serve <file>               # hot-reload dev server for web endpoints
modal shell <file>                # interactive shell inside a Modal container
modal volume list / get / put   # manage a modal.Volume (persistent storage across runs)
modal secret list / create      # manage modal.Secret objects
modal app list / logs <app>     # inspect deployed/running apps
modal billing                   # workspace billing info
```

Async Python against the SDK should use Modal's `.aio()` interface (e.g. `await modal.Function.remote.aio(...)`) rather than wrapping sync calls.

## Choosing a lane

- One-shot command on remote compute, with the plugin handling upload/download/cleanup: `modal_run`.
- Persistent storage across multiple calls, a deployed endpoint, or anything CLI/SDK-native (Volumes, Secrets, Queues, Dicts, `deploy`/`serve`): the `modal` CLI directly.

Always terminate/clean up what you created for a one-off task; leave deployed apps running only when the user actually wants a persistent endpoint.
