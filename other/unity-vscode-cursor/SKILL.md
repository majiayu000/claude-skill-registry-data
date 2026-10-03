---
name: unity-vscode-cursor
description: Unity remote editor workflows for VS Code and Cursor, including acceptable usage, login-node caveats, and safer patterns.
---

# Unity VS Code / Cursor

Use this skill when the user is asking about remote editing on Unity with VS Code or Cursor, especially over SSH, with a remote editor server, or from a browser/desktop session.

## What Is Acceptable

- Use remote editing for code navigation, small edits, and normal development work.
- Use VS Code Remote SSH or Cursor remote workflows to connect to a compute node, desktop session, or other approved non-login host.
- Use the Unity jump host only as the documented gateway into the cluster, not as a workstation or compute host.
- Edit files on a login node only if the work is lightweight and does not start background servers, indexing, or builds.

## What Not To Do On Login Nodes

- Do not run heavy builds, tests, package installs, or model loads on login nodes.
- Do not leave VS Code Server, Cursor servers, language servers, watchers, or large indexing jobs running on login nodes.
- Do not treat a login node as a long-lived remote workstation.
- Do not use the jump host for interactive development beyond the documented SSH entry point.

## Safer Patterns

- Prefer local editing plus sync when the task is mostly file editing.
- Prefer a compute-node allocation for remote editor sessions that need indexing, language servers, or background tooling.
- Prefer Unity OnDemand desktop sessions when you need a browser-backed GUI environment.
- If you need notebook or app-style work, use the Unity web UI rather than forcing it through an editor server.

## Remote SSH Caveats

- Remote editor servers are real processes with CPU, RAM, and disk impact.
- A remote server that feels local on a laptop can still be too much for a login node.
- If the editor wants to keep a daemon alive, move that session to a compute node or desktop allocation.
- Watch for hidden background work: file watchers, TypeScript/Python servers, search indexing, extension scans, and repo-wide symbol indexing.

## Unity-Specific Guidance

- Unity docs and team norms favor OnDemand as the easiest access path for browser-based desktop, Jupyter, MATLAB, and similar GUI workflows.
- Unity login nodes are for light coordination, copying, and editing, not for computation.
- Remote SSH access goes through the documented jump host and VPN/2FA path, not direct workstation-style use.
- If the user needs a GUI, browser app, or persistent interactive environment, steer them toward Unity Desktop / Simple Desktop / Jupyter instead of trying to make VS Code or Cursor do everything.

## Decision Rule

- If the task is simple editing, remote SSH may be fine.
- If the task needs background compute, indexing, or long-lived processes, use a compute node or OnDemand session.
- If the task needs a browser GUI or notebook, use the Unity web UI flow.

## When To Hand Off

- Use `unity` for general cluster rules and routing.
- Use `unity-python-envs` for package, conda, wheel, and environment setup.
- Use `unity-ondemand` for web UI, desktops, and app-launch workflows.
- Use `unity-jupyter` for notebook-specific launch settings and troubleshooting.
- Use `unity-slurm` for batch scheduling and GPU request details.
