---
name: dspy-chatadapter
description: Deep dive into dspy.ChatAdapter -- the default adapter that formats DSPy signatures into multi-turn chat messages with field delimiters, parses LM responses back into typed Python objects, and falls back to JSONAdapter on failure. Use when you need to understand how DSPy builds prompts, debug why a model ignores output format, customize prompt rendering, enable native function calling, use callbacks, generate fine-tuning data, or control the JSON fallback. Also used for how DSPy formats prompts, field delimiters, prompt template rendering, parse error debugging, ChatAdapter vs JSONAdapter vs TwoStepAdapter, format_finetune_data, dspy prompt inspection, why model output is wrong format, adapter callbacks, native function calling in DSPy.
---

# dspy.ChatAdapter -- How DSPy Formats Prompts

## Step 1: Understand what you need

Before diving into adapter internals, clarify:

1. **Are you debugging a formatting issue?** (model ignores format, parse errors, wrong output structure)
2. **Do you need to customize how prompts are built?** (system messages, field order, special providers)
3. **Are you generating fine-tuning data?** (need OpenAI-compatible message format)
4. **Do you need native function calling or structured output?** (provider-specific features)

If you just need to pick the right adapter, start with `/dspy-adapters` instead -- it covers the decision between ChatAdapter, JSONAdapter, TwoStepAdapter, and XMLAdapter.

## What ChatAdapter does

ChatAdapter is the default adapter in DSPy. Every time a module calls an LM, ChatAdapter handles two jobs:

1. **Format**: Converts signature + demos + inputs into a list of chat messages (system, user, assistant)
2. **Parse**: Extracts output fields from the LM response using `[[ ## field_name ## ]]` delimiters

You never call it directly -- DSPy uses it behind the scenes. But understanding its internals helps you debug formatting issues and customize behavior.

## Constructor

```python
dspy.ChatAdapter(
    callbacks=None,                    # list[BaseCallback] | None
    use_native_function_calling=False, # bool
    native_response_types=None,        # list[type] | None
    use_json_adapter_fallback=True,    # bool
    parallel_tool_calls=None,          # bool | None
)
```

| Parameter | Type | Default | What it controls |
|-----------|------|---------|-----------------|
| `callbacks` | `list[BaseCallback] \| None` | `None` | Callback hooks executed during format/parse |
| `use_native_function_calling` | `bool` | `False` | Use provider-native function calling for structured output |
| `native_response_types` | `list[type] \| None` | `None` | Output field types handled by native LM features instead of text parsing |
| `use_json_adapter_fallback` | `bool` | `True` | Automatically retry with JSONAdapter when parsing fails |
| `parallel_tool_calls` | `bool \| None` | `None` | Enable provider-side parallel tool-call generation when native function calling is active |

## How formatting works

ChatAdapter converts a DSPy call into a multi-turn message list:

```
System message:    Task instructions from the signature docstring
                   + field structure showing expected input/output format
                   + output type hints and constraints

Demo messages:     For each few-shot demo:
                     User message:      input fields with [[ ## field ## ]] headers
                     Assistant message:  output fields with headers + [[ ## completed ## ]]

History messages:  If dspy.History is used, prior conversation turns

User message:      Current input fields with headers
                   + output format reminder (for long conversations)
```

### The field delimiter system

ChatAdapter marks each field with header delimiters:

```
[[ ## question ## ]]
What is the capital of France?

[[ ## answer ## ]]
Paris

[[ ## completed ## ]]
```

The `[[ ## completed ## ]]` marker signals that the LM has finished all output fields. This is how `parse()` knows where output ends.

### Inspecting what gets sent to the LM

Use `dspy.inspect_history()` to see the exact messages ChatAdapter builds:

```python
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

program = dspy.ChainOfThought("question -> answer")
result = program(question="What is DSPy?")

# See the full prompt and response
dspy.inspect_history(n=1)
```

## How parsing works

When the LM responds, `parse()`:

1. Splits the response text on `[[ ## field_name ## ]]` headers
2. Maps each section to the corresponding output field
3. Calls `parse_value()` to cast each value to its declared Python type
4. Validates all required output fields are present
5. Returns a dict of field names to typed values

If any step fails, the adapter raises `AdapterParseError` -- which triggers the JSON fallback (if enabled).

## The JSON fallback mechanism

By default, ChatAdapter automatically retries with JSONAdapter when parsing fails:

```
ChatAdapter.parse() succeeds? -> Return result
                     fails?   -> Is it an LMError?
                                   Yes -> Re-raise (cannot fix by reformatting)
                                   No  -> Retry entire call with JSONAdapter
```

This means most parse failures self-heal without intervention. To observe when fallback triggers, enable debug logging or check `dspy.inspect_history()` for duplicate calls.

To disable the fallback:

```python
adapter = dspy.ChatAdapter(use_json_adapter_fallback=False)
dspy.configure(lm=lm, adapter=adapter)
# Now parse failures raise AdapterParseError immediately
```

## Native function calling

Some providers (OpenAI, Anthropic) support native structured output via function calling. ChatAdapter can use this instead of text-based field delimiters:

```python
adapter = dspy.ChatAdapter(use_native_function_calling=True)
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"), adapter=adapter)

# Output fields are now enforced via the provider's function calling API
# rather than text delimiters in the prompt
```

Use `native_response_types` to limit which output types use native features:

```python
from pydantic import BaseModel

class StructuredResult(BaseModel):
    category: str
    confidence: float

# Only use native function calling for Pydantic output types
adapter = dspy.ChatAdapter(
    use_native_function_calling=True,
    native_response_types=[BaseModel],
)
```

## Few-shot demo formatting

ChatAdapter formats demos as user/assistant message pairs. Demos come in two flavors:

**Complete demos** (all fields present):
```
User:      [[ ## question ## ]]
           What color is the sky?
Assistant: [[ ## answer ## ]]
           Blue
           [[ ## completed ## ]]
```

**Incomplete demos** (some fields missing -- common during bootstrapping):
```
User:      This is an example of the task, though some input or output
           fields are not supplied.
           [[ ## question ## ]]
           What color is the sky?
Assistant: [[ ## answer ## ]]
           Blue
           [[ ## completed ## ]]
```

The prefix on incomplete demos tells the LM not to infer missing fields from incomplete examples.

## Conversation history

ChatAdapter handles `dspy.History` fields by converting them into alternating user/assistant message pairs inserted before the current input:

```python
import dspy

class Chatbot(dspy.Module):
    def __init__(self):
        self.respond = dspy.Predict("history: dspy.History, question -> response")

    def forward(self, history, question):
        return self.respond(history=history, question=question)

# History becomes prior message pairs in the formatted prompt
history = dspy.History(
    messages=[
        {"role": "user", "content": "Hi there"},
        {"role": "assistant", "content": "Hello! How can I help?"},
    ]
)
```

## Generating fine-tuning data

ChatAdapter can produce OpenAI-compatible fine-tuning data from your DSPy programs:

```python
adapter = dspy.ChatAdapter()

# Generate fine-tuning format for a single example
finetune_data = adapter.format_finetune_data(
    signature=my_signature,
    demos=my_demos,
    inputs={"question": "What is DSPy?"},
    outputs={"answer": "A framework for programming LMs"},
)
# Returns: {"messages": [{"role": "system", ...}, {"role": "user", ...}, {"role": "assistant", ...}]}
```

This is useful when you want to fine-tune a model on the exact prompt format DSPy uses, ensuring the fine-tuned model responds in a way ChatAdapter can parse reliably.

## ChatAdapter vs the other adapters

| Aspect | ChatAdapter | JSONAdapter | TwoStepAdapter | XMLAdapter |
|--------|-------------|-------------|----------------|------------|
| **Delimiter style** | `[[ ## field ## ]]` headers | JSON object keys | Natural language (step 1) + ChatAdapter (step 2) | `<field>...</field>` XML tags |
| **Parse resilience** | Falls back to JSONAdapter | `json_repair` library | Delegated to extraction LM | Falls back to JSONAdapter |
| **Native structured output** | Optional (`use_native_function_calling`) | On by default | N/A | No |
| **LM calls per prediction** | 1 | 1 | 2 (main + extraction) | 1 |
| **Best for** | General use, most models | Reliable structured output, complex Pydantic types | Reasoning models (o1, o3) | Models that respond well to XML |

> **BamlAdapter** (`dspy.adapters.BamlAdapter`) exists in the source (`dspy/adapters/baml_adapter.py`) but has no official docs page and is undocumented — treat as experimental. Do not recommend it in production code.

### When to switch away from ChatAdapter

- **Parse errors on complex output types** (nested Pydantic, lists of objects) -> `JSONAdapter`
- **Reasoning model produces worse answers with format constraints** -> `TwoStepAdapter`
- **Model responds better to XML structure** (some Anthropic models) -> `XMLAdapter`
- **No issues** -> Keep ChatAdapter (the default is good)

## Gotchas

- **Claude instantiates ChatAdapter when it is not needed.** ChatAdapter is the default -- `dspy.configure(lm=lm)` already uses it. Only instantiate explicitly when you need to change a parameter like `use_json_adapter_fallback=False` or `use_native_function_calling=True`.
- **Claude sets `use_native_function_calling=True` for all providers.** Not all providers support native function calling. OpenAI and Anthropic do; many local models and smaller providers do not. If the provider does not support it, the call fails. Check provider capabilities before enabling, or let ChatAdapter fall back to text-based delimiters.
- **Claude does not realize parse failures auto-heal via JSON fallback.** When a model garbles the `[[ ## field ## ]]` format, ChatAdapter automatically retries with JSONAdapter. Before adding manual error handling or switching adapters, check `dspy.inspect_history()` to see if the fallback already succeeded silently.
- **Claude calls `DSPyInstrumentor().instrument()` after the adapter is configured and expects to see adapter details in traces.** The adapter formats and parses happen inside the LM call. Instrumentation captures the LM call, but adapter internals (which delimiter style was used, whether fallback triggered) are not always visible in traces. Use `dspy.inspect_history()` for adapter-level debugging.
- **Claude forgets `[[ ## completed ## ]]` when manually constructing few-shot demos.** If you build demos by hand (not via optimization), omitting the completion marker causes the LM to keep generating past the expected output. Let DSPy handle demo formatting through `BootstrapFewShot` or `LabeledFewShot` rather than manually constructing demos with delimiters.

## Additional resources

- [dspy.ChatAdapter API docs](https://dspy.ai/api/adapters/ChatAdapter/)
- [dspy.JSONAdapter API docs](https://dspy.ai/api/adapters/JSONAdapter/)
- [dspy.TwoStepAdapter API docs](https://dspy.ai/api/adapters/TwoStepAdapter/)
- [dspy.XMLAdapter API docs](https://dspy.ai/api/adapters/XMLAdapter/)
- [reference.md](reference.md) — constructor, all methods, format/parse protocol
- [examples.md](examples.md) — debugging parse failures, mixed adapter pipelines, fine-tuning data generation

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **All adapters overview** (ChatAdapter vs JSONAdapter vs TwoStepAdapter vs XMLAdapter) -- see `/dspy-adapters`
- **Signatures** that adapters format and parse -- see `/dspy-signatures`
- **LM configuration** that adapters communicate with -- see `/dspy-lm`
- **Debugging and inspection** tools including `inspect_history` -- see `/dspy-utils`
- **Fine-tuning** with data generated by `format_finetune_data` -- see `/ai-fine-tuning`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
