---
title: "AgentFEM workflow skill for coding assistants"
description: "Use the versioned AgentFEM skill to guide an AI assistant through model setup, execution and result inspection using public interfaces."
---

# AgentFEM skill

The repository ships a standards-compatible AgentFEM skill that teaches coding
agents the public workflow, project lifecycle, result contract, scientific
validation boundary, and safe extension rules.

The canonical source is
[`skills/agentfem/SKILL.md`](https://github.com/haoming-luo/agentfem/blob/main/skills/agentfem/SKILL.md).
It is versioned with the code so that agent behavior can evolve alongside API
and project-format changes.

The directory is self-contained: keep `SKILL.md`, `agents/`, and `references/`
together. A skill-aware agent can load it directly from the repository. For a
personal Codex installation, copy or link the complete `skills/agentfem/`
directory to `$CODEX_HOME/skills/agentfem/` (or
`~/.codex/skills/agentfem/` when `CODEX_HOME` is unset); copying only
`SKILL.md` omits the scientific and implementation references.

The main skill stays concise and routes detailed material progressively:
workflow guidance is read for modeling tasks, while concepts, module ownership,
validation, and extension rules are loaded only when the task requires them.

## What the skill is for

- discover and validate an AgentFEM installation;
- create and operate projects through the public workflow;
- interpret structured failures and simulation results;
- preserve the distinction between execution and scientific verification;
- route reusable finite-element functionality to the correct module;
- upgrade older projects without silently rewriting scientific intent.
- freeze runtime and scientific-input evidence, run safe local ensembles, and
  build traceable convergence/loading/response experiments;
- inspect declared private extensions without automatically executing or
  installing untrusted packages.

The skill does not guess API keywords. It begins with
`agentfem.public_api("core")`, `models.model_api("core")`, and the provider
contracts reported by `agentfem capabilities --json`. Compatibility names may
remain executable during 0.2.x, but new cases use the canonical vocabulary.

The skill complements the machine-readable `/agentfem.json` manifest and
scientific `src/agentfem/knowledge/catalog.json`; it does not replace the public API or the
solver's deterministic checks.

## Performance and reproducible delivery

The optional companion skill
[`skills/agentfem-performance/SKILL.md`](https://github.com/haoming-luo/agentfem/blob/main/skills/agentfem-performance/SKILL.md)
guides performance investigation, fast-path migration and reproducible project
delivery. Keep its `references/` directory with it. Install the complete
`skills/agentfem-performance/` directory in a supported skill location using
the same copy-or-link approach above. The repository is the versioned source;
refresh local copies deliberately when updating, preserving local changes.

It distinguishes unchanged-algorithm comparisons from new-method accuracy
studies and hardware tuning. Past worker counts, step counts and timings are
not universal requirements. It contains no private meshes or material laws.

Both skills are development guidance distributed under the repository's
Apache-2.0 license, not numerical libraries or runtime dependencies. An ordinary
prepared project runs through the installed AgentFEM program without a skill,
an AI account or an agent editing its files during the solve. Record the actual
runtime and test the documented launch command before claiming that a particular
delivery supports it; a custom launcher is not evidence that `agentfem run`
has been accepted for that delivery.
