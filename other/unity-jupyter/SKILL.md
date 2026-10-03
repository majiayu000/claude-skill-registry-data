---
name: unity-jupyter
description: Unity Jupyter notebook and server launch guidance.
---

# Unity Jupyter

Use this skill when the user needs to launch or debug Jupyter Notebook or Jupyter Server on Unity, especially through OnDemand or an interactive job.

## What matters on Unity

- Jupyter should run on a compute node or OnDemand session, not on a login node.
- The usual launch path is the Unity web UI interactive apps menu.
- For most notebook/server launches, the main knobs are time and memory.
- If the notebook should use a project or conda environment, register and select the right kernel instead of relying on the server’s default environment.

## Default launch pattern

1. Open Unity OnDemand.
2. Launch `Jupyter Notebook` from Interactive Apps.
3. Leave most launch settings at their defaults unless you know you need something different.
4. Adjust wall time to match the session length you actually need.
5. Adjust memory to match the notebook and data load you expect.
6. Start the session.
7. In the notebook UI, select the correct kernel for the environment you want.

If the docs or site defaults look odd, trust the Unity-specific launch form rather than generic Jupyter advice. Recent Unity docs note `mamba/25.11.0` as the expected module line for Jupyter launches after maintenance.

## Kernel and environment rules

- A Jupyter server and a Python environment are not the same thing.
- If you want a conda or mamba env to appear in Jupyter, install `ipykernel` into that env and register a kernel for it.
- Start the server after the kernel exists, then select the kernel in the notebook UI.
- If a user says “I activated the env but the notebook still cannot import my package,” the likely fix is kernel selection, not re-activation.
- Team comms indicate the safest sequence is: create/register the kernel first, then start or reconnect to the Jupyter server.

## Remote notebook server pattern

Use this when the user is already inside a compute session, desktop session, or other non-browser shell and wants to connect an external client:

```bash
jupyter notebook --no-browser --port=8888 &
```

Then connect from the client with:

- `Existing Jupyter Server...` in VS Code
- the full URL and token printed by Jupyter

Key point: the server must already be running in the target environment before the client connects.

## Common startup failures

- Server starts on the login node instead of a compute node.
- Jupyter opens, but the kernel cannot import packages from the expected env.
- The wrong kernel is selected in the notebook UI.
- The server URL or token is missing or copied incorrectly.
- The interactive app launch form uses the wrong module line or environment setup.
- Creating a kernel in an interactive session can occasionally emit odd `worker_threads`-style errors; if the kernel still registers, create the kernel before launching the server and reconnect afterward.

## Decision points

- If the user just wants a notebook in the browser, use OnDemand interactive apps.
- If they already have a shell and want an external client, launch a no-browser Jupyter server and connect to it.
- If they need a different Python environment, register a kernel and select it in Jupyter.
- If startup is failing, check resources first, then kernel and env wiring, then the launch form or module line.

## Unity-specific reminders

- OnDemand sessions are the safe default for interactive work.
- The Unity web UI can also provide full desktop sessions and other interactive apps, but this skill stays focused on notebook and server launch behavior.
- If a notebook launch seems to be using the wrong environment, fix the kernel before trying anything more complicated.
