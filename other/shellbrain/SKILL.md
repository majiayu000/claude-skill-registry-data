---
name: shellbrain
description: Recall project knowledge, past decisions, failures, and preferences when they can help a coding task. Capture changed files before responding.
---

# Shellbrain Recall Workflow

Use Shellbrain for remembered project knowledge. It can explain a system's purpose,
past decisions, useful fixes, and constraints learned during earlier work.

## Choose the source

Use code search for current implementation: where a function lives, its parameters,
callers, or present behavior. Use docs or the web for general technical information.
Recall helps with project context that may be missing from those sources.

| Need | Action |
| --- | --- |
| Find the quote endpoint | Search the repo. |
| Understand a previous quote failure | Ask: "What past failures explain a quote returning 503 while the Swap API health check succeeds?" |
| Prepare to change discovery | Ask: "What earlier problems or design decisions matter when changing the discovery-to-optimization handoff in compute_route?" |
| Get project orientation | Ask about the named system's remembered purpose and responsibilities, then check current code. |

A normal question is enough. Include the subject, your task or symptom, and what you need to learn.
Do not invent a prior failure or guess the answer to make a query specific.

## Recall

```bash
shellbrain recall "<self-contained question>"
```

Recall receives only this query. It does not receive your conversation or previous recall questions.
Name the subject again in follow-up questions. Include exact errors or symbols when known.
Avoid vague questions such as "anything relevant?" or requests to solve the whole task.

Run from the target repo. From elsewhere, use:

```bash
shellbrain --repo-root /absolute/path/to/repo recall "<self-contained question>"
```

Read **Memories** for useful knowledge and **Code** for locations to inspect.
Concept claims can appear in Memories along with remembered cases.
Verify current behavior, commands, and paths before relying on them.
Preserve distinctions between proposals, completed changes, and verified results.
An answer can be partial or outdated. Missing information does not prove a feature is absent.
If recall finds nothing useful, continue with code and docs. A provider error is a failed lookup.
Retry a query only when new context gives you a more specific question.

## When to consider recall

Track `goal | surface | obstacle | hypothesis`.
Emit one `SB:` line when this tuple changes, the same approach fails twice,
an error repeats, you switch files or subsystems, you make an evidence-bearing decision,
or you close out.

When prior knowledge may help:

`SB: recall | <goal> | <surface> | <obstacle> | <hypothesis-or-trigger>`

Then ask one focused question. Otherwise:

`SB: skip | same signature | <one-line reason>`

Continue without a recall call when you already have the needed evidence.

## Capture changed files

If you changed any files since your last user-facing response, run `shellbrain snapshot`
exactly once after validation and immediately before your next user-facing response.
Do this on every response cycle where files changed; skip only when no files changed.
Use `--repo-root /absolute/path/to/repo` when outside the repo.

Snapshot captures code state. The background knowledge builder uses session evidence
and snapshots to record lessons and completed problem-solving runs.
Do not manually write memories. `read`, `events`, `memory`, `concept`, and `scenario`
are internal-agent commands; do not call them during working-agent tasks.

## Repair

Use `shellbrain upgrade` to repair installation. If the executable is missing,
check the login profile once for your shell:

```bash
zsh -lc 'source ~/.zprofile >/dev/null 2>&1; command -v shellbrain'
bash -lc 'source ~/.bash_profile >/dev/null 2>&1; command -v shellbrain'
```

Use the resolved executable or plain `shellbrain` afterward.
Do not keep sourcing the login profile on every Shellbrain command.
If still missing, inspect Python's user script directory:

```bash
python3 -c "import sysconfig; print(sysconfig.get_path('scripts', 'posix_user'))"
```

If it contains `shellbrain`, use that path or add it to PATH. Otherwise reinstall.
