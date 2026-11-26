---
name: log-log-local-models
description: "Local models. A log play (docs/useCases/log/localModels.md): See which local models this release pins and whether each is on this machine at that revision, and, with the owner's yes, fetch the missing ones: the judge's injection classifier, the meaning model behind search and the router, the image describer and the mouse planner."
when_to_use: "Use when the owner asks for this, in words like: \"which models does log use\", \"fetch the models\""
metadata:
  summary: "Local models"
---

# Local models

This is the log play `log/localModels`. Before anything else, call the log MCP tool `getGuide({ useCase: "log/localModels" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

See which local models this release pins and whether each is on this machine at that revision, and, with the owner's yes, fetch the missing ones: the judge's injection classifier, the meaning model behind search and the router, the image describer and the mouse planner.

How the owner asks for it: "which models does log use", "fetch the models"

## Run it from a fresh context

Say: **"go on docs/useCases/log/localModels.md"**. The agent reads this page and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | List each local model with its pinned revision, size, the process that loads it and whether it is here and matches | `models` {} | the owner sees which are ready |
| 2 | Only after the owner says yes, fetch or verify the ones not ready | `modelsLive` { approvedBy, confirmLive } | it answered each model as already, adopted, downloaded or installed, or refused with `modelFetchFailed` |
| 3 | Say what changed and what is still missing | the reply to the owner | the owner heard the result |

## What to know

- **One version for everything.** Each release pins its models in `src/models/manifest`; `log update` and the install scripts fetch them, so this is for checking or for finishing a fetch that failed offline.
- **No second download.** A matching copy in transformers.js's old cache inside `node_modules` is moved, not downloaded again. Everything lands in `~/.logCli/models`.
- **Check free space first** (`runsSpace`): most of the download is the image describer. Each model's size is on the [local models page](https://github.com/matthewdonsemail-lab/log/blob/main/docs/models.md).

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [Connect your agent](https://github.com/matthewdonsemail-lab/log/blob/main/docs/mcp.md) · [Trust](https://github.com/matthewdonsemail-lab/log/blob/main/docs/trust.md)
