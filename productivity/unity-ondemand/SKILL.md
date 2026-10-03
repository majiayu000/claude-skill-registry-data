---
name: unity-ondemand
description: Unity OnDemand web UI workflows for browser-first access, desktops, and app/server launches.
---

# Unity OnDemand

Use this skill for Unity's web UI. It is the right entry point when the user wants a browser shell, file transfer, a desktop session, or a hosted app/server launch.

## When to use OnDemand

- Use OnDemand when the workflow is easier in a browser than over SSH.
- Use it for file browsing/transfers, getting a shell in a browser, opening a full Linux desktop, or launching Unity-hosted interactive apps.
- Use it when you want to stay out of the login-node workflow as much as possible and let the web UI handle the session entry point.
- If the task is specifically a notebook server, use the `unity-jupyter` subskill for launch tuning and kernel details.

## How to think about it

- Browser shell: good for quick setup, inspection, and light coordination before handing off heavy work to Slurm.
- Desktop session: best when the workflow truly needs a full GUI, drag-and-drop file handling, or an application that behaves like a desktop app.
- App/server launch: best when the web UI can start the tool directly and the tool exposes its own browser interface.
- Prefer the lightest viable UI. Use a desktop only when the application really needs a desktop; otherwise use a browser app/server launch.

## Unity-specific advice

- Unity's OnDemand is part of the ASC Unity experience and is meant to reduce friction for common HPC tasks without replacing Slurm.
- The important Unity OnDemand entry points to remember are `Shell Access`, `Files`, `Unity Desktop`, `Unity Simple Desktop`, `Jupyter Notebook`, and `Matlab`.
- If a browser-launched app needs more CPU, memory, GPU, or time than the default, choose the right resource request up front instead of relying on a retry.
- If a launch fails after a maintenance window or module change, suspect the module selection first, not the browser.
- For interactive compute work launched from OnDemand, keep the session bounded and remember that the resources still belong to the cluster scheduler.
- OnDemand can coexist with SSH-based workflows, but it is often the easier first step for people who do not want to manage shells and tunnels by hand.
- If you need a browser workflow on a remote machine, OnDemand is preferred over ad hoc desktop forwarding.

## Good Defaults

- Choose a browser app launch if the work can stay in a browser.
- Choose `Unity Desktop` or `Unity Simple Desktop` if you need a full Linux desktop.
- Choose `Jupyter Notebook` through the `unity-jupyter` skill if the workflow is notebook-centric.
- Choose `Matlab` from Interactive Apps if the work is specifically MATLAB-centric.
- Escalate to batch or a dedicated interactive job if the web app is really just a front end for longer compute.
