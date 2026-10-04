---
description: Check pi's dispatch environment (which provider/model a dispatch reaches, the thinking binding, the co-pilot guard)
disable-model-invocation: true
---

Check first:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/pi-doctor" --check
```

The `effective` block in the output is "who a dispatch will actually reach". **Having no
`~/.claude/pi-delegate/config.json` is normal** — it means a dispatch uses the user's own pi default
model (`defaultProvider` / `defaultModel` in `~/.pi/agent/settings.json`).

If problems are reported, explain each one's impact to the user before asking whether to act on it:

- `reasoning-missing` / `compat-missing` — only shows up for a **local OpenAI-compatible server**
  (e.g. omlx, LM Studio, llama.cpp, vLLM): when a model is missing `reasoning: true` or the
  `compat.chatTemplateKwargs.enable_thinking` binding, `--thinking off` **silently has no effect**,
  and the model keeps thinking without ever acting. This class can be fixed automatically.
- `drafter-selected` — the model about to be dispatched to looks like a speculative-decoding
  co-pilot (draft / assistant); calling it directly returns HTTP 500. Ask the user to switch to the
  target model; if it's a false positive, adjust `drafter_patterns` in the config. **This class is
  never auto-fixed**, because which model to use is the user's decision.

Once they agree, fix whatever can be fixed automatically (a backup is made first, as `models.json.pi-delegate.bak`):

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/pi-doctor" --fix
```

`--fix` only adds the thinking binding to a model that is **already registered and confirmed to be a
local chat-template endpoint**. It never creates a provider, never inserts a model, and never touches
other models — those need values only the user knows, and a guessed configuration is harder to debug
than no configuration.
