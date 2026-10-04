---
name: dspy-citations
description: Use when you need structured source attribution in AI responses — verifiable citations that link claims to specific passages in source documents. Common scenarios - RAG with citation extraction, grounded answers with document references, legal or compliance use cases requiring source proof, building AI that cites its sources, or verifying which document an answer came from. Related - ai-stopping-hallucinations, ai-searching-docs, dspy-retrieval. Also used for dspy.experimental.Citations, dspy.experimental.Document, cite sources in DSPy, structured citations, source attribution, verify which document answer came from, RAG with citations, grounded answers with references, citation extraction, Anthropic Citations API DSPy, cited_text, document_index, adapt_to_native_lm_feature, parse_lm_response citations, streaming citations.
---

# Add Structured Citations to DSPy Outputs

Guide the user through adding structured citations to DSPy outputs so AI answers can be traced back to specific source passages.

## What are DSPy Citations

`dspy.experimental.Citations` provides structured source attribution for LM outputs. Instead of inline quotes, you get machine-readable citation objects that identify exactly which passage from which document supports each claim. Works natively with Anthropic's Citations API and falls back to prompt-based extraction for other providers.

## When to use Citations

| Use Citations when... | Use something else when... |
|----------------------|----------------------------|
| You need to verify which document supports a claim | Simple RAG where inline quotes are enough |
| Legal/compliance requires source traceability | Output does not reference source material |
| Users need clickable references back to source docs | You only have one source document |
| You want machine-readable citation metadata | Human-readable quotes in text are sufficient |
| Building fact-checking or grounding verification | The task is creative generation (no sources) |

## Step 1: Set up Documents

Create `Document` objects from your source material:

```python
import dspy
from dspy.experimental import Citations, Document

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

# Create documents from your sources
documents = [
    Document(
        data="DSPy is a framework for programming language models. It replaces prompting with composable modules that can be optimized.",
        title="DSPy Overview",
    ),
    Document(
        data="MIPROv2 is the most powerful DSPy optimizer. It jointly optimizes instructions and few-shot demonstrations.",
        title="Optimizers Guide",
    ),
]
```

## Step 2: Build a signature with Citations output

```python
class CitedQA(dspy.Signature):
    """Answer the question using the provided documents. Cite your sources."""
    documents: list[Document] = dspy.InputField(desc="source documents")
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()
    citations: Citations = dspy.OutputField(desc="structured citations for claims in the answer")
```

## Step 3: Use with a standard module

```python
qa = dspy.ChainOfThought(CitedQA)

result = qa(
    documents=documents,
    question="What is the most powerful DSPy optimizer?",
)

print(result.answer)
# "MIPROv2 is the most powerful DSPy optimizer..."

for citation in result.citations.citations:
    print(f"  Cited: '{citation.cited_text}' from document {citation.document_index}")
```

## Step 4: Anthropic native Citations API

Native citations are **automatic** for Anthropic models. There is no special adapter
configuration -- you just configure an Anthropic LM, declare a `Citations` output field,
and pass `documents: list[Document]` as input. DSPy handles the rest.

```python
lm = dspy.LM("anthropic/claude-sonnet-4-5-20250929")
dspy.configure(lm=lm)

# The same CitedQA signature (Citations output + documents input) now uses
# Anthropic's built-in citation extraction -- no adapter kwarg needed.
result = qa(
    documents=documents,
    question="How does DSPy replace prompting?",
)
```

**Native mode advantages:**
- Citations are extracted by the model during generation (not post-hoc)
- `cited_text` exactly matches source text (character-level accuracy)
- `document_index` reliably maps to the input document list

## Step 5: Parse and validate citations

```python
# Each citation has these fields
for citation in result.citations.citations:
    print(f"Cited text: {citation.cited_text}")
    print(f"Document index: {citation.document_index}")
    print(f"Start char: {citation.start_char_index}")
    print(f"End char: {citation.end_char_index}")

# Validate that cited text exists in the source document
for citation in result.citations.citations:
    source_doc = documents[citation.document_index]
    if citation.cited_text in source_doc.data:
        print(f"VALID: Citation found in {source_doc.title}")
    else:
        print(f"INVALID: Citation not found in source")
```

## Step 6: Citations with streaming

Stream answers while accumulating citations:

```python
from dspy.streaming import streamify, StreamListener

qa = dspy.ChainOfThought(CitedQA)

answer_listener = StreamListener(signature_field_name="answer")
streaming_qa = streamify(qa, stream_listeners=[answer_listener])

async for chunk in streaming_qa(documents=documents, question="..."):
    if hasattr(chunk, "answer"):
        print(chunk.answer, end="", flush=True)
    elif isinstance(chunk, dspy.Prediction):
        # Citations are available in the final prediction
        for citation in chunk.citations.citations:
            print(f"\n[{citation.document_index}] {citation.cited_text}")
```

## Step 7: Non-Anthropic fallback patterns

For providers without native citation support (OpenAI, local models, etc.), the
`Citations` output field falls back to prompt-based parsing. For maximum control you
can skip the `Citations` type entirely and use plain-string context with inline markers
-- this is the **prompt-based fallback path**, not the native Anthropic path:

```python
class CitedAnswer(dspy.Signature):
    """Answer using ONLY information from the provided documents.
    For each claim, include [doc_N] inline where N is the document number."""
    context: list[str] = dspy.InputField(desc="numbered source documents")
    question: str = dspy.InputField()
    answer: str = dspy.OutputField(desc="answer with [doc_N] inline citations")

# Number your documents explicitly (plain strings, not Document objects)
numbered_context = [
    f"[doc_{i}] {doc.title}: {doc.data}"
    for i, doc in enumerate(documents)
]

qa = dspy.ChainOfThought(CitedAnswer)
result = qa(context=numbered_context, question="...")
# Parse [doc_N] references from the answer text
```

## Gotchas

1. **Claude omits the `Citations` type import.** You must import from `dspy.experimental` -- it is not in the main `dspy` namespace. Use `from dspy.experimental import Citations, Document`.
2. **Native citations activate automatically for Anthropic models.** When you configure an Anthropic LM and declare a `Citations` output field, DSPy uses Anthropic's native Citations API -- there is no `adapt_to_native_lm_feature` kwarg or special adapter to set. On non-Anthropic models (OpenAI, local), the same `Citations` field silently falls back to prompt-based parsing, which may be less accurate.
3. **Claude hardcodes document indices.** The `document_index` in citations maps to the position in the context list. If you reorder documents, indices change. Always use the index to look up the source, do not hardcode.
4. **Citations are experimental.** The API is in `dspy.experimental` and may change between versions. Pin your DSPy version in production.
5. **Claude generates citations without source material.** Citations only make sense when you provide context documents. Without context, the model fabricates citation metadata. Always pair Citations with a retrieval step.

## Additional resources

- [dspy.ai/api/experimental/Citations](https://dspy.ai/api/experimental/Citations/)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Stopping hallucinations** with grounding -- see `/ai-stopping-hallucinations`
- **Searching docs** for RAG pipelines -- see `/ai-searching-docs`
- **Retrieval** modules for getting context -- see `/dspy-retrieval`
- **Streaming** citations progressively -- see `/dspy-streaming`
- **Install `/ai-do` if you do not have it** -- it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
