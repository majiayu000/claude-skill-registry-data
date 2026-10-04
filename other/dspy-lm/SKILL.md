---
name: dspy-lm
description: Use when you need to configure which language model DSPy uses — setting up providers, API keys, model parameters, or assigning different models to different pipeline stages. Common scenarios - setting up OpenAI or Anthropic API keys, configuring model parameters like temperature and max_tokens, using different models for different pipeline stages, switching between providers, using local models with Ollama or vLLM, or setting up Azure OpenAI. Related - ai-switching-models, ai-cutting-costs, ai-kickoff. Also used for dspy.LM, dspy.configure, configure language model in DSPy, OpenAI API key setup DSPy, Anthropic Claude with DSPy, use Ollama with DSPy, local model DSPy, Azure OpenAI DSPy setup, model temperature and max_tokens, different models per module, multi-model DSPy pipeline, vLLM with DSPy, change provider without changing code, model configuration DSPy.
---

# Configure Language Models with dspy.LM

`dspy.LM` is DSPy's unified interface for calling language models. It wraps [LiteLLM](https://docs.litellm.ai/docs/providers) so any provider -- OpenAI, Anthropic, Google, Together AI, Ollama, vLLM, and 100+ others -- works through one consistent API. You configure a model once, then every DSPy module uses it automatically.

## Basic setup

```python
import dspy

# Create an LM instance with a provider/model string
lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.

# Set it as the default for all DSPy modules
dspy.configure(lm=lm)

# Now any module uses this LM automatically
classify = dspy.ChainOfThought("text -> label")
result = classify(text="DSPy is great")
print(result.label)
```

The pattern is always: `dspy.LM("provider/model")` then `dspy.configure(lm=lm)`.

## Step 1 — Gather context

Before configuring an LM, confirm if not already clear:

1. **Which provider?** OpenAI, Anthropic, Google, Together AI, Groq, Azure, or local (Ollama/vLLM)?
2. **Single model or mixed pipeline?** One model everywhere, or different models per stage for cost/quality tradeoffs?
3. **Reasoning model involved?** (o1, o3, o4, DeepSeek-R1, Claude extended thinking) — these require `temperature=1.0` or `None` and large `max_tokens`.
4. **Local/offline requirement?** Privacy or no-internet constraints point to Ollama or vLLM, which need extra setup.

## Provider strings

DSPy uses the LiteLLM `"provider/model-name"` format. Here are the most common providers:

| Provider | Example string | Notes |
|----------|---------------|-------|
| OpenAI | `"openai/gpt-4o"` | Default provider, auto-detected |
| OpenAI | `"openai/gpt-4o-mini"` | Cheaper, faster |
| Anthropic | `"anthropic/claude-sonnet-4-5-20250929"` | |
| Anthropic | `"anthropic/claude-haiku-4-5-20251001"` | Fast and cheap |
| Google | `"gemini/gemini-2.0-flash"` | |
| Together AI | `"together_ai/meta-llama/Llama-3-70b-chat-hf"` | Open-source models |
| Groq | `"groq/llama-3.1-70b-versatile"` | Fast inference |
| Ollama (local) | `"ollama_chat/llama3.1"` | Requires `api_base` |
| Azure OpenAI | `"azure/my-gpt4-deployment"` | Requires `api_base` + `api_key` |
| OpenAI-compatible | `"openai/my-model"` | Any server with `api_base` |

See [LiteLLM provider docs](https://docs.litellm.ai/docs/providers) for the full list.

## Constructor parameters

```python
lm = dspy.LM(
    model="openai/gpt-4o",           # Required: "provider/model-name"
    model_type="chat",                # "chat" (default), "text", or "responses"
    temperature=0.7,                  # Sampling temperature (default: provider default)
    max_tokens=1000,                  # Max output tokens (default: provider default)
    cache=True,                       # Enable built-in caching (default: True)
    num_retries=3,                    # Retry on transient failures (default: 3)
    use_developer_role=False,         # Use developer/system role (default: False)
    # Plus any extra kwargs passed to LiteLLM
)
```

### Key parameters

- **`model`** (required) -- The provider/model string. This is the only required argument.
- **`temperature`** -- Controls randomness. Lower = more deterministic. Set to `0.0` for reproducible outputs. Reasoning models (o1, o3) require `temperature=1.0` or `None`.
- **`max_tokens`** -- Maximum tokens in the response. Reasoning models require `max_tokens >= 16000` or `None`.
- **`cache`** -- When `True` (the default), DSPy caches LM responses to reduce costs and speed up repeated calls. Set to `False` to disable.
- **`num_retries`** -- Number of retries with exponential backoff on transient failures.
- **`model_type`** -- Usually leave as `"chat"`. Use `"text"` for completion-only models. Use `"responses"` for OpenAI responses API.

## Per-module LM assignment

You do not have to use the same model for every step. Assign different LMs to different modules with `set_lm()`:

```python
expensive_lm = dspy.LM("openai/gpt-4o")
cheap_lm = dspy.LM("openai/gpt-4o-mini")

# Set a default
dspy.configure(lm=cheap_lm)

class MyPipeline(dspy.Module):
    def __init__(self):
        self.classify = dspy.Predict("text -> category")
        self.generate = dspy.ChainOfThought("text, category -> summary")

    def forward(self, text):
        category = self.classify(text=text)
        return self.generate(text=text, category=category.category)

pipeline = MyPipeline()

# Route: cheap model for classification, expensive for generation
pipeline.classify.set_lm(cheap_lm)
pipeline.generate.set_lm(expensive_lm)
```

### When to use each override method

| Method | Scope | Persistent? | Use when |
|--------|-------|-------------|----------|
| `dspy.configure(lm=lm)` | Global default | Yes | Setting the LM once at program start |
| `module.set_lm(lm)` | Per-module instance | Yes | Routing specific steps to a different model permanently |
| `dspy.context(lm=lm)` | Code block | No (reverts after) | One-off call with a different LM without changing defaults |

### Temporary LM override with `dspy.context`

Use `dspy.context` to temporarily switch LMs for a block of code:

```python
with dspy.context(lm=expensive_lm):
    # Everything inside uses expensive_lm
    result = pipeline(text="important document")

# Back to the default LM outside the block
```

## Direct LM calls

You can call an `LM` instance directly for one-off prompts outside of DSPy modules:

```python
lm = dspy.LM("openai/gpt-4o-mini")

# Pass a string prompt
response = lm("What is the capital of France?")
print(response)  # returns a list of strings

# Pass a messages list (chat format)
response = lm(messages=[
    {"role": "user", "content": "What is the capital of France?"}
])
print(response)  # returns a list of strings
```

Direct calls are useful for quick tests, but for structured tasks use DSPy modules and signatures -- they give you type checking, optimization, and caching.

## Environment variables

Set API keys as environment variables. Never hardcode them.

```bash
# OpenAI
export OPENAI_API_KEY=sk-...

# Anthropic
export ANTHROPIC_API_KEY=sk-ant-...

# Together AI
export TOGETHER_API_KEY=...

# Google
export GEMINI_API_KEY=...

# Groq
export GROQ_API_KEY=...

# Azure OpenAI
export AZURE_API_KEY=...
export AZURE_API_BASE=https://your-resource.openai.azure.com/
```

DSPy (via LiteLLM) reads these automatically. You can also pass `api_key` directly to `dspy.LM()` if needed, but environment variables are preferred.

## Caching

DSPy caches LM responses by default. This means:

- **Repeated identical calls are free** -- same prompt, same parameters, same model returns a cached result instantly with no API call.
- **Development is faster** -- re-running your script doesn't re-call the LM for already-seen inputs.
- **Optimization is cheaper** -- optimizers that re-evaluate examples benefit from cached results.

### Controlling caching

```python
# Caching enabled (default)
lm = dspy.LM("openai/gpt-4o-mini", cache=True)

# Disable caching for this LM
lm = dspy.LM("openai/gpt-4o-mini", cache=False)

# Configure cache settings globally (controls disk and memory tiers separately)
dspy.configure_cache(
    enable_disk_cache=True,        # Toggle on-disk caching
    enable_memory_cache=True,      # Toggle in-memory caching
    disk_size_limit_bytes=None,    # Optional: cap disk cache size
    memory_max_entries=None,       # Optional: cap in-memory entries
)
```

Cache is stored locally. If you need different responses for the same prompt (e.g., generating diverse examples), disable caching or use different `temperature` values.

## Useful methods

| Method | Purpose |
|--------|---------|
| `lm("prompt")` | Direct call -- returns list of strings |
| `lm.copy(**kwargs)` | Deep copy with updated parameters |
| `lm.inspect_history()` | View recent request/response history |
| `lm.dump_state()` | Serialize config (excludes API keys) |

### Inspecting history

```python
lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

classify = dspy.Predict("text -> label")
classify(text="Hello world")

# See what was sent to the LM
dspy.inspect_history(n=1)
```

## Connecting to local models

### Ollama

```python
# Start Ollama: ollama serve
# Pull a model: ollama pull llama3.1
lm = dspy.LM(
    "ollama_chat/llama3.1",
    api_base="http://localhost:11434",
    api_key="",
    temperature=0.7,
    num_ctx=8192,  # set context window explicitly — Ollama defaults to 4096
)
dspy.configure(lm=lm)
```

For full Ollama setup (model selection, GPU tuning, context window gotchas, optimization tips), see `/dspy-ollama`.

### vLLM or any OpenAI-compatible server

```python
# Start vLLM: vllm serve meta-llama/Llama-3.1-8B-Instruct
lm = dspy.LM(
    "openai/meta-llama/Llama-3.1-8B-Instruct",
    api_base="http://localhost:8000/v1",
    api_key="none",
)
dspy.configure(lm=lm)
```

For any server that exposes an OpenAI-compatible `/v1/chat/completions` endpoint, use the `"openai/model-name"` provider string with `api_base` pointing to your server.

For full vLLM setup (tensor parallelism, GPU sizing, quantization, production deployment), see `/dspy-vllm`.

## Gotchas

1. **Claude omits the provider prefix from the model string.** Claude writes `dspy.LM("gpt-4o-mini")` instead of `dspy.LM("openai/gpt-4o-mini")`. While some models auto-detect the provider, the explicit `"provider/model"` format is required for reliable routing through LiteLLM. Always include the provider prefix.
2. **Claude sets `temperature=0` for reasoning models.** OpenAI reasoning models (o1, o3, o4, gpt-5 families) require `temperature=1.0` or `None`. Setting `temperature=0` raises an error. Similarly, `max_tokens` must be `>= 16000` or `None` for these models.
3. **Claude calls `dspy.configure(lm=lm)` inside `forward()`.** Configuration should happen once at the top of your script, not per-call. Calling `dspy.configure` inside `forward()` resets global state on every invocation and breaks caching. Use `set_lm()` or `dspy.context()` for per-module or temporary overrides instead.
4. **Claude forgets `api_base` for local models.** Ollama and vLLM require `api_base` pointing to the local server (`http://localhost:11434` for Ollama, `http://localhost:8000/v1` for vLLM). Without it, DSPy tries to reach the cloud API and fails with an authentication error.
5. **Claude hardcodes API keys in source code.** Set API keys as environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.) — DSPy reads them automatically via LiteLLM. Passing `api_key=...` directly to `dspy.LM()` is supported but should be reserved for local dev overrides, not production code.

## Related DSPy model classes

- **`dspy.Embedder`** — For computing text embeddings (RAG, semantic search). Uses the same LiteLLM provider string format: `dspy.Embedder("openai/text-embedding-3-small")`. Not an LM — cannot be passed to `dspy.configure(lm=...)`. See [dspy.ai/api/models/Embedder/](https://dspy.ai/api/models/Embedder/).
- **`BaseLM`** (upcoming) — DSPy 3.3.0 (beta) introduces a typed `BaseLM` interface with `LMRequest`/`LMResponse` typed boundaries. Stable 3.2.1 uses `dspy.LM` as documented here.

## Additional resources

- [dspy.LM API docs](https://dspy.ai/api/models/LM/)
- [dspy.Embedder API docs](https://dspy.ai/api/models/Embedder/)
- [LiteLLM provider docs](https://docs.litellm.ai/docs/providers)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **`/dspy-signatures`** -- Define what your LM should do (inputs, outputs, types)
- **`/dspy-modules`** -- Wrap signatures with inference strategies (Predict, ChainOfThought, ReAct)
- **`/ai-switching-models`** -- Safely migrate between providers with re-optimization
- **`/ai-cutting-costs`** -- Reduce LM costs with per-module assignment and cheaper models
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
