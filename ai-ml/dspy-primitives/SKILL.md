---
name: dspy-primitives
description: DSPy typed wrappers (dspy.Image, dspy.Audio, dspy.Code, dspy.History, dspy.File, dspy.Reasoning, dspy.Tool, dspy.ToolCalls, dspy.Example, dspy.Prediction) for multimodal data, files, and structured outputs in signatures. Use when working with non-text inputs like images, audio, or code, passing PDFs or documents to the LM, capturing native reasoning traces from reasoning models, building multimodal AI pipelines, processing images alongside text, handling audio transcription inputs, working with code files as typed inputs, or managing conversation history in multi-turn chatbots. Also used for multimodal DSPy, image input in DSPy signature, process images with DSPy, audio input in DSPy, dspy.File, pass PDF to language model, document input in DSPy, dspy.Reasoning, capture thinking traces, native reasoning output, dspy.Tool, dspy.ToolCalls, typed fields in signatures, non-text data in DSPy, vision model with DSPy, Claude vision with DSPy, multimodal pipeline, image classification with DSPy, pass images to language model, conversation history type, structured types beyond strings, dspy.Example, dspy.Prediction, training data container, labeled examples DSPy, module output DSPy.
---

# DSPy Primitives

Guide the user through DSPy's built-in primitive types for multimodal inputs, code handling, and conversation history.

## Step 1: Understand the task

Before using primitives, clarify:

1. **What kind of non-text data?** Images, audio, code, or conversation history — each has its own primitive type.
2. **Does the LM support it natively?** `dspy.Image` needs a vision model (GPT-4o, Claude 3+, Gemini). `dspy.Audio` needs an audio model (GPT-4o-audio-preview, Gemini). `dspy.Code` and `dspy.History` work with any LM.
3. **Is the data an input, output, or both?** All primitives work as both input and output fields, but some patterns are more natural (e.g., `dspy.Code` for code generation output, `dspy.Image` for image analysis input).

## What are primitives

Primitives are DSPy's custom types that go beyond plain strings. They let you pass images, audio, code, files, and conversation history directly into signatures, and capture structured outputs like native reasoning traces. DSPy handles the formatting, encoding, and adapter logic so the LM receives the data in the right format for its provider.

The core primitives:

| Primitive | Purpose | Typical use case |
|-----------|---------|------------------|
| `dspy.Image` | Images from URLs, files, or bytes | Vision tasks, image analysis, multimodal Q&A |
| `dspy.Audio` | Audio from files, URLs, or arrays | Transcription, audio classification |
| `dspy.Code` | Code with language annotation | Code generation, code review, analysis |
| `dspy.History` | Conversation turns | Chatbots, multi-turn dialogue, follow-up questions |
| `dspy.File` | Files (PDFs, documents) from a path, bytes, or upload ID | Document Q&A, PDF summarization |
| `dspy.Reasoning` | Native reasoning/thinking traces from reasoning models | Capturing o1/o3/R1/extended-thinking output |
| `dspy.Tool` | Wraps a Python callable as a tool the LM can call | Agents, ReAct (see `/dspy-tools`) |
| `dspy.ToolCalls` | The LM's tool-call requests as a structured output | Agents, ReAct (see `/dspy-tools`) |
| `dspy.Example` | A single labeled input/output pair | Training data, few-shot demos, evaluations |
| `dspy.Prediction` | What a DSPy module returns | Reading outputs, comparing results, usage tracking |

## dspy.Image

Wraps an image from any source into a format the LM can process. DSPy normalizes the input into a base64 data URI or plain URL automatically.

### Constructor

```python
dspy.Image(url=<source>, download=False, verify=True)
```

**Parameters:**

- **`url`** — the image source. Accepts:
  - `str` — HTTP/HTTPS URL, GS URL, or local file path
  - `bytes` — raw image bytes
  - `PIL.Image.Image` — a PIL image instance
  - `dict` — `{"url": value}` (legacy form)
  - An already-encoded data URI
- **`download`** (`bool`, default `False`) — whether to download remote URLs to infer MIME type
- **`verify`** (`bool`, default `True`) — whether to verify SSL certificates. Set `False` for self-signed certs.

### Usage in signatures

```python
import dspy

lm = dspy.LM("openai/gpt-4o")  # or "anthropic/claude-sonnet-4-5-20250929", etc. (must be vision-capable)
dspy.configure(lm=lm)

class DescribeImage(dspy.Signature):
    """Describe what you see in the image."""
    image: dspy.Image = dspy.InputField(desc="Image to analyze")
    description: str = dspy.OutputField(desc="Detailed description of the image")

describer = dspy.Predict(DescribeImage)

# From a URL
result = describer(image=dspy.Image(url="https://example.com/photo.jpg"))
print(result.description)

# From a local file
result = describer(image=dspy.Image(url="/path/to/photo.png"))

# From PIL
from PIL import Image as PILImage
pil_img = PILImage.open("photo.png")
result = describer(image=dspy.Image(url=pil_img))
```

### Multiple images

```python
class CompareImages(dspy.Signature):
    """Compare two images and describe the differences."""
    image_a: dspy.Image = dspy.InputField(desc="First image")
    image_b: dspy.Image = dspy.InputField(desc="Second image")
    differences: str = dspy.OutputField(desc="Key differences between the images")
```

## dspy.Audio

Wraps audio data for LMs that support native audio input. Audio is encoded as base64 internally.

### Creating Audio objects

```python
# From a local file
audio = dspy.Audio.from_file("recording.wav")

# From a URL
audio = dspy.Audio.from_url("https://example.com/clip.mp3")

# From a numpy array (e.g., from a microphone or audio processing)
import numpy as np
audio = dspy.Audio.from_array(samples, sampling_rate=16000, format="wav")

# Direct instantiation with base64 data
audio = dspy.Audio(data="<base64-string>", audio_format="wav")
```

### Usage in signatures

```python
import dspy

lm = dspy.LM("openai/gpt-4o-audio-preview")  # or "google/gemini-2.0-flash", etc. (must be audio-capable)
dspy.configure(lm=lm)

class TranscribeAudio(dspy.Signature):
    """Transcribe the spoken content in the audio."""
    audio: dspy.Audio = dspy.InputField(desc="Audio recording to transcribe")
    transcript: str = dspy.OutputField(desc="Transcribed text")

transcriber = dspy.Predict(TranscribeAudio)
result = transcriber(audio=dspy.Audio.from_file("meeting.wav"))
print(result.transcript)
```

### Audio classification

```python
from typing import Literal

class ClassifyAudio(dspy.Signature):
    """Classify the type of audio content."""
    audio: dspy.Audio = dspy.InputField(desc="Audio clip to classify")
    category: Literal["speech", "music", "ambient", "silence"] = dspy.OutputField()
    language: str = dspy.OutputField(desc="Detected language if speech, else 'N/A'")
```

## dspy.Code

Wraps code with a language annotation. DSPy formats it as a markdown code block so the LM sees properly delimited, syntax-aware code.

### Language specification

Use bracket notation to specify the language:

```python
dspy.Code["python"]   # Python code
dspy.Code["java"]     # Java code
dspy.Code["sql"]      # SQL code
dspy.Code["rust"]     # Rust code
# ... any language string works
```

The language tag tells DSPy to format the code as a fenced markdown block (` ```python ... ``` `) and guides the LM on syntax expectations.

### Usage in signatures

**Code generation (output):**

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

class GenerateCode(dspy.Signature):
    """Generate Python code that solves the given problem."""
    problem: str = dspy.InputField(desc="Problem description")
    code: dspy.Code["python"] = dspy.OutputField(desc="Working Python solution")

generator = dspy.Predict(GenerateCode)
result = generator(problem="Write a function that checks if a string is a palindrome")
print(result.code)
```

**Code analysis (input):**

```python
class ReviewCode(dspy.Signature):
    """Review the code for bugs, performance issues, and style problems."""
    code: dspy.Code["python"] = dspy.InputField(desc="Code to review")
    issues: list[str] = dspy.OutputField(desc="List of issues found")
    severity: Literal["clean", "minor", "major", "critical"] = dspy.OutputField()

reviewer = dspy.ChainOfThought(ReviewCode)
result = reviewer(code="def fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)")
print(result.issues)    # ["No memoization — exponential time complexity", ...]
print(result.severity)  # "major"
```

**Code transformation (input and output):**

```python
class ConvertCode(dspy.Signature):
    """Convert the Python code to equivalent Java code."""
    python_code: dspy.Code["python"] = dspy.InputField(desc="Python source code")
    java_code: dspy.Code["java"] = dspy.OutputField(desc="Equivalent Java code")
```

## dspy.History

Represents conversation history as a list of message turns. Use it to build multi-turn chatbots and follow-up interactions in DSPy.

### Creating History objects

```python
# From prior conversation turns
history = dspy.History(messages=[
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "Paris"},
])

# Using field names that match your signature
history = dspy.History(messages=[
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is the capital of Germany?", "answer": "Berlin"},
])
```

History objects are **immutable** (frozen). Create a new History to add turns.

### Usage in signatures

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

class Chat(dspy.Signature):
    """Answer the user's question given the conversation history."""
    history: dspy.History = dspy.InputField(desc="Prior conversation turns")
    question: str = dspy.InputField(desc="Current user question")
    answer: str = dspy.OutputField(desc="Response to the user")

chatbot = dspy.Predict(Chat)
```

### Building conversation incrementally

Capture each response and append it to history for the next turn:

```python
chatbot = dspy.Predict(Chat)

# Turn 1
result = chatbot(
    history=dspy.History(messages=[]),
    question="What is the capital of France?"
)
print(result.answer)  # Paris

# Turn 2 — include previous turn in history
history = dspy.History(messages=[
    {"question": "What is the capital of France?", "answer": result.answer}
])
result = chatbot(
    history=history,
    question="What is its population?"
)
print(result.answer)  # About 2.1 million in the city proper...

# Turn 3 — append again
history = dspy.History(messages=[
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is its population?", "answer": result.answer},
])
result = chatbot(
    history=history,
    question="How does that compare to London?"
)
```

### Helper pattern for managing history

```python
class Chatbot(dspy.Module):
    def __init__(self):
        self.respond = dspy.ChainOfThought(Chat)
        self.turns = []

    def forward(self, question):
        history = dspy.History(messages=self.turns)
        result = self.respond(history=history, question=question)
        self.turns.append({"question": question, "answer": result.answer})
        return result
```

## dspy.File

Wraps a file (PDF, document, etc.) so you can pass it to an LM that supports file inputs. DSPy encodes the file as a base64 data URI (`data:<mime_type>;base64,<...>`) following the OpenAI file content-part spec. Added in DSPy 3.1.

### Creating File objects

```python
# From a local file path (auto-detects MIME type)
file = dspy.File.from_path("./research.pdf")

# From raw bytes
file = dspy.File.from_bytes(pdf_bytes, filename="research.pdf", mime_type="application/pdf")

# From a previously uploaded file (referenced by provider file ID)
file = dspy.File.from_file_id("file-abc123", filename="research.pdf")

# Direct instantiation with a data URI
file = dspy.File(file_data="data:application/pdf;base64,<base64-string>")
```

### Usage in signatures

```python
import dspy

lm = dspy.LM("openai/gpt-4o")  # or "anthropic/claude-sonnet-4-5-20250929", etc. (must support file inputs)
dspy.configure(lm=lm)

class SummarizeDoc(dspy.Signature):
    """Summarize the key findings in the document."""
    file: dspy.File = dspy.InputField(desc="Document to summarize")
    summary: str = dspy.OutputField(desc="Concise summary of the document")

summarizer = dspy.Predict(SummarizeDoc)
result = summarizer(file=dspy.File.from_path("./research.pdf"))
print(result.summary)
```

Use `dspy.File` when you need to feed a whole document to the LM (PDF Q&A, contract review, report summarization) rather than extracting and pasting its text. The model must support file inputs.

## dspy.Reasoning

Captures the native reasoning/thinking trace emitted by reasoning models (o1/o3, DeepSeek-R1, Claude extended thinking) as a structured output field. When the configured model supports native reasoning, DSPy pulls the reasoning trace directly from the response; otherwise it falls back to a generated reasoning field, so the same signature works across reasoning and non-reasoning models. Added in DSPy 3.1.

`dspy.Reasoning` behaves like a string (you can index, slice, concatenate, and call string methods on it) while also being a typed primitive.

### Usage in signatures

```python
import dspy

lm = dspy.LM("openai/o3-mini")  # or "anthropic/claude-sonnet-4-5-20250929" with thinking, "deepseek/deepseek-reasoner", etc.
dspy.configure(lm=lm)

class SolveProblem(dspy.Signature):
    """Solve the math problem."""
    problem: str = dspy.InputField()
    reasoning: dspy.Reasoning = dspy.OutputField(desc="The model's native reasoning")
    answer: str = dspy.OutputField()

solver = dspy.Predict(SolveProblem)
result = solver(problem="If a train travels 60 km in 45 minutes, what is its speed in km/h?")
print(result.reasoning)  # the model's native thinking trace
print(result.answer)     # 80
```

Use `dspy.Reasoning` when you want access to a reasoning model's native thinking as a first-class output. For a plain generated rationale that works on any LM, use `dspy.ChainOfThought` instead — see `/dspy-chain-of-thought`.

## dspy.Tool and dspy.ToolCalls

`dspy.Tool` wraps a Python callable so the LM can invoke it as a tool, and `dspy.ToolCalls` represents the LM's tool-call requests as a structured output type. These are the building blocks for agents and tool use (ReAct). They are covered in depth — including registration, argument schemas, and execution loops — in `/dspy-tools`; reach for that skill rather than constructing these primitives directly.

## dspy.Example and dspy.Prediction

`dspy.Example` is the standard data container in DSPy — every training sample, few-shot demo, and evaluation row is a `dspy.Example`. `dspy.Prediction` extends `Example` and is what every DSPy module returns.

### dspy.Example

```python
# Create an example with arbitrary fields
ex = dspy.Example(question="What is the capital of France?", answer="Paris")
ex = ex.with_inputs("question")  # mark which fields are inputs vs labels

# Access fields by attribute or key
print(ex.question)   # "What is the capital of France?"
print(ex.answer)     # "Paris"
print(ex.keys())     # dict_keys(['question', 'answer'])
print(ex.inputs())   # Example with only input fields (question)
print(ex.labels())   # Example with only label fields (answer)

# Copy with overrides (returns a new Example)
ex2 = ex.copy(answer="Paris, France")

# Convert to plain dict for JSON serialization
print(ex.toDict())
```

`with_inputs()` is required before using an example with optimizers or `dspy.Evaluate` — optimizers use `.inputs()` to construct the forward call and `.labels()` to compare predicted outputs.

### dspy.Prediction

Every call to a DSPy module returns a `dspy.Prediction`:

```python
module = dspy.Predict("question -> answer")
result = module(question="What is 2+2?")

print(result.answer)       # access output field by name
print(result.keys())       # all field names
print(result.get_lm_usage()) # token usage dict from the LM call
```

`dspy.Prediction` also stores intermediate completions when multiple samples are generated (e.g., with `dspy.BestOfN`), accessible via `result._completions`.

For training data construction and optimization workflows, see `/dspy-data`.

## When not to use primitives

- **Prefer text extraction over `dspy.Image` for structured documents.** If you need data from a scanned PDF or form, use a dedicated OCR/parsing library (pdfplumber, PyMuPDF, Tesseract) and pass the extracted text as a string. Vision models reading documents are slower, more expensive, and less reliable for structured data like tables.
- **Pre-transcribe audio rather than using `dspy.Audio` when accuracy matters.** Use a dedicated ASR model (Whisper, Deepgram) first, then pass the transcript text to DSPy. End-to-end audio adds latency and the audio-capable model must also handle your DSPy task.
- **Paste text instead of `dspy.File` for short documents.** For documents under ~2K words, extract the text and pass it directly as a string field. Use `dspy.File` when the document is too long to fit in the prompt or when native file-reading by the model preserves structure (e.g., multi-column layouts).
- **Use `dspy.ChainOfThought` instead of `dspy.Reasoning` on non-reasoning models.** `dspy.Reasoning` is designed for o1/o3/DeepSeek-R1/Claude extended-thinking. On standard models it falls back to a generated reasoning field — `dspy.ChainOfThought` is a more explicit and optimizable approach for those cases.

## Combining primitives in signatures

You can mix primitives with regular typed fields in the same signature:

```python
class AnalyzeScreenshot(dspy.Signature):
    """Analyze a UI screenshot and generate test code for the visible elements."""
    screenshot: dspy.Image = dspy.InputField(desc="Screenshot of the UI")
    framework: str = dspy.InputField(desc="Test framework to use, e.g. 'playwright'")
    test_code: dspy.Code["python"] = dspy.OutputField(desc="Generated test code")
    element_count: int = dspy.OutputField(desc="Number of interactive elements found")
```

```python
class AudioChat(dspy.Signature):
    """Respond to a user's audio message in a conversation."""
    history: dspy.History = dspy.InputField(desc="Prior conversation turns")
    audio_message: dspy.Audio = dspy.InputField(desc="User's spoken message")
    response: str = dspy.OutputField(desc="Text response to the user")
```

## Provider requirements

Not all LM providers support all primitives natively:

| Primitive | Requires |
|-----------|----------|
| `dspy.Image` | A vision-capable model (GPT-4o, Claude 3+, Gemini, etc.) |
| `dspy.Audio` | An audio-capable model (GPT-4o-audio-preview, Gemini, etc.) |
| `dspy.Code` | Any LM (formatted as markdown code blocks) |
| `dspy.History` | Any LM (formatted as conversation turns) |
| `dspy.File` | A model that supports file inputs (GPT-4o, Claude, Gemini, etc.) |
| `dspy.Reasoning` | Best with a reasoning model (o1/o3, DeepSeek-R1, Claude extended thinking); falls back to a generated field on others |

DSPy's adapter system handles the provider-specific formatting. You write the signature once; DSPy translates it for the target LM.

## Gotchas

1. **Claude uses the deprecated `dspy.Image.from_file()` / `from_url()` class methods.** Use `dspy.Image(url="path-or-url")` directly instead — the constructor accepts file paths, URLs, bytes, and PIL images via the `url` parameter.
2. **Claude passes raw strings where a primitive is expected.** If a signature field is typed as `dspy.Code["python"]`, pass a string directly — DSPy's `validate_input` coerces it. But for `dspy.Image` and `dspy.Audio`, you must construct the primitive object explicitly. Raw strings will not be auto-converted.
3. **Claude uses `role`/`content` keys in History messages instead of signature field names.** History messages should use keys matching the signature fields (e.g., `{"question": ..., "answer": ...}`), not the generic `role`/`content` format. Using `role`/`content` works but produces worse prompt formatting because DSPy cannot map the history entries to the right signature fields.
4. **Claude forgets that History is frozen (immutable).** You cannot append to an existing History object. Create a new `dspy.History(messages=[...old_turns, new_turn])` each time. Attempting to mutate raises a `ValidationError`.
5. **Claude uses `dspy.Image` with a non-vision model.** If the configured LM does not support vision (e.g., GPT-4o-mini, older Claude models), image inputs are silently ignored or cause errors. Always verify the model supports the primitive type.
6. **Claude cannot verify multimodal input encoding without inspecting LM history.** To confirm an image or file was properly encoded and sent, inspect `dspy.settings.lm.history[-1]` after a call — the `kwargs` key shows the formatted request. A malformed primitive (empty bytes, wrong MIME type, unsupported URL scheme) shows up as a missing or broken content part in the request, not as a Python exception.

## Additional resources

- [dspy.Image API docs](https://dspy.ai/api/primitives/Image/)
- [dspy.Audio API docs](https://dspy.ai/api/primitives/Audio/)
- [dspy.Code API docs](https://dspy.ai/api/primitives/Code/)
- [dspy.History API docs](https://dspy.ai/api/primitives/History/)
- [dspy.Example API docs](https://dspy.ai/api/primitives/Example/)
- [dspy.Prediction API docs](https://dspy.ai/api/primitives/Prediction/)
- [dspy.Tool API docs](https://dspy.ai/api/primitives/Tool/)
- [dspy.ToolCalls API docs](https://dspy.ai/api/primitives/ToolCalls/)
- [DSPy primitives API index](https://dspy.ai/api/primitives/)
- [dspy.File and dspy.Reasoning](https://dspy.ai/diving-deeper/adapters/) — covered in the Adapters guide under "Custom type wrappers" (no dedicated API page yet)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Defining signatures** — see `/dspy-signatures`
- **Using signatures with modules** — see `/dspy-modules`, `/dspy-predict`, `/dspy-chain-of-thought`
- **Tools and agents (`dspy.Tool`, `dspy.ToolCalls`)** — see `/dspy-tools`
- **`dspy.Example` and training data** — see `/dspy-data`
- **Building chatbots with History** — see `/ai-building-chatbots`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
