---
name: dify-agent-builder
description: >-
  Build a ready-to-import Dify Chatflow agent (a .yml DSL file) from a plain-language request.
  Use this whenever the user wants to create, build, design, or generate a Dify agent / chatbot /
  智能体 / 工作流 / chatflow / DSL — e.g. "做一个能查知识库回答制度问题的Dify智能体",
  "帮我生成一个上传文档就分析的助手", "build me a Dify customer-service bot that calls an HTTP API",
  "make a multimodal agent that reads images". Trigger even when the user does not say the word
  "DSL" or "yml" — any request to produce a usable Dify agent counts. The skill designs a structured
  blueprint and runs a deterministic engine to emit valid Dify 0.3.0 Chatflow YAML the user can
  import directly.
---

# Dify Agent Builder

Turn a plain-language request into an **importable Dify 0.3.0 Chatflow `.yml`**. You act as the
architect: you design a structured **BlueprintSpec** (JSON), then run a deterministic engine
(`scripts/build_agent.py`, backed by `scripts/assembler.py`) that faithfully renders it into valid,
wired-up Dify YAML — node IDs, edges, env-var declarations, data plumbing and validation are all
handled for you. You never hand-write YAML.

Assume Dify development and runtime are **内网/offline** unless the user explicitly says otherwise:
no public API calls, no internet-only dependencies, and no generated plugin that relies on PyPI at
install time.

## Workflow

1. **Understand the need.** What should the agent do? Who uses it? What inputs (text / uploaded
   documents / images) and what outputs? If a *blocking* detail is missing (e.g. they want an HTTP
   API but give no purpose/method/path and don't say "placeholder is fine"), ask 1–2 sharp
   questions. Otherwise proceed with sensible defaults and state them.
2. **Design a BlueprintSpec** following the philosophy below. Read `references/blueprint-spec.md`
   for the exact JSON schema and every node kind. For a common pattern, start from the closest
   `examples/*.json` file and edit only what the request requires. If the target Dify version or
   plugin/runtime compatibility is in doubt, read `references/compatibility.md` before rendering.
3. **Write the blueprint** to a temp JSON file, e.g. `/tmp/blueprint.json`.
4. **Render it:** `python3 scripts/build_agent.py /tmp/blueprint.json <name>.yml`
   The script prints node/edge counts, validation warnings, and post-import manual steps.
5. **Deliver the `.yml`** to the user and briefly list: what it does, key design decisions you made
   (so they can correct you), and anything to configure after import (select a knowledge base,
   choose a model, fill env vars).

## Design philosophy — this is what makes the agent actually good

These principles matter more than any feature list. The model running the generated agent is strong
(e.g. DeepSeek-V4 class); lean on its intelligence instead of brittle scaffolding.

- **少即是多 / Less is more.** Prefer the fewest nodes and one well-prompted LLM. Put judgement,
  conditions, and "if X do Y" logic into the LLM's `system_prompt`, not into routers/if-else/code.
  The best workflow is usually `(retrieval/extract/http) → one good LLM → answer`. Every extra node
  is another failure point.
  - "Analyze the document if uploaded, otherwise just chat" → **do NOT route.** One chain:
    `document-extractor → one LLM` whose prompt says "if there's uploaded file text, analyze it;
    otherwise answer normally". The extractor yields empty when no file, so the LLM decides. Robust.
  - Only split into multiple routes when different situations genuinely need **different tools**
    (one needs a knowledge base, another needs an HTTP call) that can't be merged.
- **Don't overstep (不自作主张).** Build only what the user asked for or the scenario clearly needs.
  No unrequested features, nodes, fields, or APIs. Respect negatives — if they say "no X", X must
  not appear.
- **Don't fabricate.** Never invent knowledge-base content, API paths, business fields, or rule
  numbers. Use placeholders (e.g. `/v1/your-endpoint`) and tell the user in your delivery notes.
- **Write excellent node prompts.** Each LLM node's `system_prompt` must state: role · task ·
  grounding (answer from injected context — knowledge/file/http/code results — don't make things up) ·
  output format · boundary (what to do when info is missing). Use the business's real terms, not
  "you are a helpful assistant".
- **The engine owns the plumbing.** You only write each LLM node's `system_prompt`. The runtime user
  input (`{{#sys.query#}}`) and all upstream context are wired in automatically — never write
  `user_template`, and **never** paste the user's build request text into any prompt.
- **Multi-turn.** If the user later says "add X / remove Y / rename / it errored", edit the previous
  blueprint minimally and re-render — don't redesign from scratch.

## What the engine handles for you (so you don't worry about it)

Node IDs and layout, all edges, `{{#sys.query#}}` + upstream-context injection into LLM prompts,
env-var declarations (scanned from `{{#env.X#}}` refs), `sys.files` reading for documents, the
`answer` node's output reference, file-download export wiring, a None-safety net for code, and
structural validation (broken edges, dup IDs, secret leaks, route integrity). It also forces the
correct user-input wiring even if your blueprint gets it wrong.

## Quick reference: when to use what

| Need | Shape |
|------|-------|
| Q&A / writing | single LLM |
| Answer from a knowledge base (制度/FAQ/docs) | `knowledge → LLM` |
| Read uploaded Word/PDF/Excel/CSV | `document-extractor → LLM` |
| Recognize an **image** (OCR/截图/票据) | a single `llm` with `"vision": true` (NOT document-extractor) |
| Call an HTTP/business API | `http → LLM` (token via env var, never hardcoded) |
| Precise computation / parse / file output | add a `code` node — only when an LLM can't read-and-do it |
| Genuinely different tools per intent | `routing.enabled=true` classifier with one minimal route each |

Full schema, every field, and complete examples: **`references/blueprint-spec.md`** — read it before
writing a blueprint.

## Validation loop

When changing the skill or when a generated result seems risky, run the local regression suite from
the repo root:

```bash
python3 -m unittest tests.test_agent_builder
```

The checked examples cover knowledge Q&A, document extraction + file export, HTTP + env vars,
classifier routing, condition routing, and vision upload wiring.
