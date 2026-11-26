---
name: layout
description: 'Where a new file goes in log-cli (rule 2). Every file sits in a domain folder named for what it does: src/{library}/{domain}/, python/<domain>/, scripts/<domain>/; nothing loose. Use when adding a Python module, a script or a check, or when `bun run check:layout` refuses a commit.'
---

# layout

| Where | What goes there |
|---|---|
| `src/{library}/{domain}/` | TypeScript, with the role files (`index.ts`, `types.ts`, `client.ts`, `machine.ts`, `helpers/`; rule 2) |
| `src/browser/` | each browser (`adsPower`, `camoufox`) and what every browser shares: `driver`, `run`, `proxy`, `inspect`, `flow` (rule 2) |
| `python/browser/` | opening the account's browser through its gates: `browserDriver`, `adsPowerBrowser`, `visibleBrowser`, `proxyGate`, `harRecorder` |
| `python/human/` | how the cursor and wheel move: `humanMouse`, `scrollMotion`, `recordMouse` |
| `python/session/` | the processes TypeScript runs: `inspectSession`, `connectSession`, `publishSession`, `profileSession`, `logWorker` |
| `python/login/`, `python/device/`, `python/errors/`, `python/fixtures/` | sign-in, Camoufox's device, the error codes and catalog, test pages |
| `scripts/checks/` | the lefthook gates (`check:*`) |
| `scripts/commitLog/`, `scripts/docs/`, `scripts/hooks/`, `scripts/privacy/`, `scripts/twenty/`, `scripts/datasets/` | the private day-log gate, the generated docs, the agent hooks, the privacy check, Twenty setup and client, dataset builds |

## A new Python module

- Put it in its domain package; a new domain gets its own folder with an `__init__.py` (a docstring saying what it holds).
- Import by package: `from browser import proxyGate`, `from human.humanMouse import HumanMouse`.
- A script run directly (it has `if __name__ == "__main__"`) puts `python/` on its path before its first local import:

```python
import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from browser import proxyGate
```

- TypeScript reaches it by its path (`python/session/inspectSession.py`); tests import it the same way (`sys.path.insert(0, 'python'); from login import autoLogin`).

## A new script

- Put it in its domain folder under `scripts/`; its repo root is two folders up (`join(import.meta.dir, "..", "..")`) and `src` is `../../src/`.
- Add its `package.json` entry and, for a gate, its lefthook command.

`bun run check:layout` (lefthook pre-commit and pre-push) refuses a loose file, tracked or new, and a Python domain without its `__init__.py`.
