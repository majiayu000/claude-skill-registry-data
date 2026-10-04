---
name: eval
description: "Generate a complete Langfuse evaluation pipeline: auto-detect app type, create datasets, LLM-as-judge evaluators, scoring configs, and CI integration."
argument-hint: "[project-description]"
allowed-tools: Read Write Edit Bash Grep Glob
model: gpt-5.4
---

# /eval — Langfuse Evaluation Pipeline Generator

Generate evaluation setup for: **$ARGUMENTS**

1. **Discover** — `agents/eval-architect.md` Step 1: Explore codebase, detect LLM app type (RAG, chatbot, agent, code-gen, summarization, classification, extraction), identify prompts, traces, and data flows
2. **Design** — `agents/eval-architect.md` Steps 2-3: Select 4-8 eval dimensions from the dimension matrix, generate seed dataset with 10-20 items covering happy path, edge cases, and adversarial inputs
3. **Generate** — `agents/eval-architect.md` Steps 4-5: Write complete `evals/` directory: config.yaml, evaluators (LLM judge + heuristic), runner.py, ci_eval.py, .env.example
4. **Setup** — `agents/eval-architect.md` Step 6: If `LANGFUSE_SECRET_KEY` is set, run setup_langfuse.py. If not, skip gracefully with instructions.
5. **Document** — `agents/eval-architect.md` Step 7: Generate PM/SME-friendly README
6. **Verify** — Run verification checklist

Rules: Always include at least one heuristic evaluator. Never hardcode API keys. README must be understandable by non-developers.
