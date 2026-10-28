---
name: llm-evals
description: Pick and wire the right LLM evaluation tool for a repository - Promptfoo (prompt regression and CI gating on local llama.cpp/Ollama endpoints, red-teaming), DeepEval (pytest-style semantic metrics on LLM outputs), Inspect AI (end-to-end agent evals with tasks, solvers, scorers and sandboxes). Use whenever the user asks to evaluate, regression-test, benchmark or gate prompts, model outputs or agents, to set up eval CI on a local OpenAI-compatible endpoint, or to choose between promptfoo, deepeval and inspect-ai.
---

# LLM evals

Tool-selection guidance and pinned wiring recipes for the three evaluation
frameworks the fleet actually needs. The tools are **dependencies of the
consuming repository** (`uv add` / npm there), never vendored into the kit:
they ship no SKILL.md and the kit stays zero-dependency. Facts were verified
against the official documentation fetched 2026-10-28; each reference file
pins the version, license and source URLs it was checked against.

## Decision matrix

| Situation | Tool | Why |
|---|---|---|
| Regression-test prompts, compare models, gate outputs in CI against a local OpenAI-compatible endpoint (llama.cpp `llama-server`, Ollama) | **Promptfoo** | YAML config, native local providers, deterministic + LLM-graded asserts, exit-code CI gating, OSS red-teaming that runs locally |
| Python repository already using pytest that needs semantic metrics on LLM outputs (relevancy, faithfulness, hallucination, G-Eval) | **DeepEval** | Metrics as pytest asserts, judge can be a local model, judge-free `system_one` mode |
| Evaluate an agent end to end (task, solver, tools, scorer), multi-step runs, needs sandboxing | **Inspect AI** | Task/solver/scorer anatomy, `local` sandbox without Docker; requires Python >= 3.11 |
| Self-refine / reflexion iteration loops | **None** | Not a tool need: carried by the canon execution loop (section 3) and agent PR review (section 4); see the reality-checker and auditor skills |

One tool per repository. Do not adopt any of them for a repository with no
LLM output to gate, and do not stack two where one covers the job.

## Local endpoints at a glance

| Endpoint | Promptfoo | DeepEval | Inspect AI |
|---|---|---|---|
| llama.cpp `llama-server` (`http://localhost:8080/v1`) | `openai:chat:<model>` + `apiBaseUrl` + `apiKeyRequired: false` | subclass `DeepEvalBaseLLM`, pass per metric | `openai-api/llamacpp/<model>` + `LLAMACPP_BASE_URL` |
| Ollama (`http://localhost:11434`) | `ollama:chat:<model>` | `deepeval set-ollama --model ... --base-url ...` | `ollama/<model>` |

Exact syntax and caveats: read the matching reference file before writing any
config.

## Safety rules

1. **No secrets in eval configs** (section 5 discipline): provider configs
   take env var names, never pasted keys. Local endpoints need no key at all -
   wire them keyless instead of embedding credentials.
2. **Read the pinned upstream doc before adopting or upgrading** (section 6
   discipline): each reference file pins the version and doc URLs it was
   verified against (fetch 2026-10-28). Re-verify upstream before a major
   version jump; DeepEval's docs churn fast.
3. **Local judge by default**: the fleet runs llama.cpp and Ollama. Routing an
   eval to a cloud judge (cost, data egress) is an explicit user decision,
   never a default.
4. **Verify the UNVERIFIED flags**: points flagged UNVERIFIED in the reference
   files were not confirmed upstream - test once in the consuming repository
   before relying on them.

## References

- Read [references/promptfoo.md](references/promptfoo.md) when wiring prompt
  regression, provider configs for local endpoints, CI eval commands or
  red-teaming.
- Read [references/deepeval.md](references/deepeval.md) when adding semantic
  metrics to a pytest suite or configuring a local LLM judge.
- Read [references/inspect-ai.md](references/inspect-ai.md) when building an
  agent evaluation task (dataset, solver chain, scorer, sandbox).

Onboarding audit, decision table (including the Self-Refine / Reflexion skip)
and fleet candidate repositories: `docs/llm-eval-skills-2026-10-28.md` in the
agents-kit repository.
