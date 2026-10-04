---
name: dspy-signatures
description: Defines typed input/output contracts for LM calls using dspy.Signature, dspy.InputField, and dspy.OutputField. Use when you need to define the input/output contract for an LM call — choosing between inline and class-based signatures, adding type constraints, or using Pydantic models for structured outputs. Common scenarios - defining input and output fields for an LM call, adding type constraints to outputs, using Pydantic models for complex structured output, choosing between inline string signatures and class-based signatures, or declaring field descriptions that guide the model. Also used for define LM call interface, typed outputs in DSPy, Pydantic model as signature, inline vs class signature, field descriptions in DSPy, structured output schema, input output contract for LLM, how to define DSPy signature, type hints in signatures, class-based signature DSPy.
---

# DSPy Signatures

Guide the user through defining DSPy Signatures — typed declarations of what goes into and comes out of an LM call.

## Step 1: What kind of signature?

Ask the user before diving in:

1. **How complex is your I/O?** One input, one output (use inline)? Multiple fields, type constraints, or nested objects (use class-based)?
2. **Do you need structured output?** If the output maps to a database model or API response, you likely want a Pydantic model as the output type.
3. **Are outputs constrained?** If you need categories, booleans, or numeric ranges, you need type annotations.

Then jump to the relevant section below.

## What is a Signature

A Signature declares the input/output contract for an LM call -- field names, types, and descriptions. DSPy compiles it into an optimized prompt automatically. You define the I/O spec; DSPy handles the prompting.

## When to use each style

| Style | When to use | Example |
|-------|-------------|---------|
| **Inline** | Quick one-liner, 1-2 inputs, 1 output, string types | `"question -> answer"` |
| **Class-based** | Multiple fields, type constraints, descriptions, Pydantic outputs | `class Classify(dspy.Signature)` |

**Rule of thumb:** Start inline for prototyping. Switch to class-based when you need type constraints, field descriptions, or more than one output.

## Inline signatures

Inline signatures are strings with `->` separating inputs from outputs: `"question -> answer"`, `"text -> label: bool"`. Supported type suffixes: `str` (default), `int`, `float`, `bool`, `list[str]`.

## Class-based signatures

Class-based signatures give you type constraints, field descriptions, and a docstring that acts as the task instruction. Use them when you need more than a one-liner.

## Field options

Both `InputField` and `OutputField` accept these parameters:

```python
class Example(dspy.Signature):
    """Demonstrate field options."""
    # desc: describes the field to the LM (shows up in the prompt)
    text: str = dspy.InputField(desc="The document to analyze")

    # type constraint via inline annotation (preferred)
    category: Literal["news", "blog", "research"] = dspy.OutputField(desc="The document category")
```

- **`desc`** — a natural language description. Helps the LM understand what the field means. Use this when the field name alone is ambiguous.
- **`type_`** — sets the type constraint on the field. Still supported, but prefer an inline Python annotation (category: Literal[...] = dspy.OutputField(...)).

## Pydantic models as output types

For complex or nested structured output, use a Pydantic `BaseModel` as the output type. DSPy handles serialization and validation automatically.

```python
import dspy
from pydantic import BaseModel, Field
from typing import Optional

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

class LineItem(BaseModel):
    description: str
    quantity: int
    unit_price: float

class Invoice(BaseModel):
    vendor: str
    date: str = Field(description="Invoice date in YYYY-MM-DD format")
    total: float
    items: list[LineItem]
    notes: Optional[str] = None

class ParseInvoice(dspy.Signature):
    """Extract structured invoice data from the raw text."""
    text: str = dspy.InputField(desc="Raw invoice text")
    invoice: Invoice = dspy.OutputField(desc="Parsed invoice data")

parser = dspy.ChainOfThought(ParseInvoice)
result = parser(text="Invoice from Acme Corp, Jan 15 2025. 2x Widget ($10 each), 1x Gadget ($25). Total: $45.")
print(result.invoice.vendor)       # Acme Corp
print(result.invoice.items[0])     # LineItem(description='Widget', quantity=2, unit_price=10.0)
print(result.invoice.total)        # 45.0
```

**When to use Pydantic outputs:**
- You need nested objects (addresses, line items, etc.)
- You want automatic validation (Pydantic enforces types)
- The output maps to a database model or API response
- You need `Optional` fields for data that may not be present

## Common patterns

### Docstrings as task instructions

The docstring is the most important part of a class-based signature. DSPy uses it as the primary instruction to the LM.

```python
# Vague — the LM doesn't know what "classify" means in your context
class Bad(dspy.Signature):
    """Classify the text."""
    text: str = dspy.InputField()
    label: str = dspy.OutputField()

# Clear — tells the LM exactly what to do
class Good(dspy.Signature):
    """Classify the customer support message into a department for routing.
    Consider the primary intent, not just keywords."""
    message: str = dspy.InputField(desc="Customer support message")
    department: Literal["billing", "technical", "account", "general"] = dspy.OutputField()
```

## Advanced: dynamic signatures

For runtime customization without defining new classes:

```python
# Override instructions at call time (inline signatures)
predict = dspy.Predict("question -> answer", instructions="Answer in exactly one sentence.")

# Programmatically modify a class-based signature
MySignature = MySignature.with_instructions("New instructions for this run")

# Add/remove fields dynamically
MySignature = MySignature.append("confidence", dspy.OutputField(), type_=float)
MySignature = MySignature.delete("unused_field")
```

DSPy also supports special input types: `dspy.Image` for image inputs, `dspy.History` for conversation history, `dspy.Audio` for audio inputs, and `dspy.Code` for code content. These are primitives from `dspy` — use them as field type annotations just like `str` or `int`.

## When NOT to use class-based signatures

- **Simple extraction or Q&A** — if `"question -> answer"` captures your task, an inline signature is clearer and shorter. Do not over-engineer with a class when a string works.
- **Prototyping** — start inline, switch to class-based only when you need type constraints, descriptions, or Pydantic outputs.
- **Too many output fields** — if you need more than 4-5 outputs, the LM quality degrades. Split into multiple calls with simpler signatures instead.

## Gotchas

1. **Field names ARE the prompt** -- `text -> summary` works better than `input -> output` because DSPy uses field names directly in the generated prompt. Choose descriptive names.
2. **Literal types need `tuple()` wrapping for dynamic values** -- use `Literal[tuple(["a", "b"])]` not `Literal[["a", "b"]]` when constructing from a list at runtime.
3. **Keep signatures small** -- more than 4-5 output fields degrades quality. Split into multiple calls instead.
4. **The docstring on a Signature class becomes the task instruction** -- write it carefully, as a clear directive. A vague docstring like "Classify the text" performs much worse than "Classify the customer support message into a department for routing."
5. **Field `desc` values are NOT optimized** -- DSPy optimizers (GEPA, MIPROv2, COPRO) tune the Signature docstring and/or few-shot demos, but `InputField(desc=...)`, `OutputField(desc=...)`, and Pydantic `Field(description=...)` values are fixed. If your structured output task relies heavily on field descriptions for guidance, see `/dspy-gepa` for a workaround that flattens field descriptions into the instruction for optimization.

**Verify your signature works** by calling the module with one realistic example and printing every output field. If a Pydantic output raises a validation error, the type constraint is too strict for what the LM produces — relax it or add a `desc` that tells the LM the exact format expected.

## Additional resources

- [dspy.Signature API docs](https://dspy.ai/api/signatures/Signature/)
- [dspy.InputField API docs](https://dspy.ai/api/signatures/InputField/)
- [dspy.OutputField API docs](https://dspy.ai/api/signatures/OutputField/)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Using signatures with modules** — see `/dspy-predict` (Predict), `/dspy-chain-of-thought` (ChainOfThought), `/dspy-modules` (custom modules)
- **Parsing structured data from text** — see `/ai-parsing-data`
- **Classification and sorting** — see `/ai-sorting`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
