---
name: ai-understanding-images
description: Analyze images and extract structured data from visual content using AI. Use when analyzing product photos, extracting text from screenshots, generating alt text for accessibility, visual question answering, categorizing images by content, reading receipts and invoices from photos, OCR with AI, describing images for search indexing, product photo categorization, document image processing, chart and graph extraction, UI screenshot analysis, image-to-structured-data pipelines.
---

# AI Understanding Images

Use DSPy's `dspy.Image` type to pass images into signatures alongside text. Vision LLMs return structured data from photos, screenshots, documents, and charts.

---

## Step 1 - Understand the image task

Before writing code, ask:

- What images will you process? (URLs, local files, base64, cloud storage?)
- What do you need to extract? (text, categories, attributes, descriptions?)
- Does the output need to be structured? (typed fields vs. free text?)
- Are you processing images in batch or one at a time?
- Does the task require reasoning about the image, or just direct extraction?

---

## Step 2 - Build a basic image analyzer

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

class AnalyzeImage(dspy.Signature):
    """Analyze the image and answer the question."""
    image: dspy.Image = dspy.InputField(desc="The image to analyze")
    question: str = dspy.InputField(desc="What to extract or analyze")
    answer: str = dspy.OutputField(desc="Analysis result")

analyzer = dspy.Predict(AnalyzeImage)

# From a URL
result = analyzer(
    image=dspy.Image(url="https://example.com/photo.jpg"),
    question="What product is shown?"
)

# From a local file
result = analyzer(
    image=dspy.Image(url="photo.jpg"),
    question="What product is shown?"
)

print(result.answer)
```

---

## Step 3 - Vision model selection

| Model | Strengths | Notes |
|---|---|---|
| `openai/gpt-4o` | Best overall vision quality | Higher cost |
| `openai/gpt-4o-mini` | Fast, cheap, good for simple tasks | Weaker on complex layouts |
| `anthropic/claude-sonnet-4-5-20250929` | Balanced quality/cost, strong image reasoning (Sonnet/Opus 4.x) | Good for production |
| `google/gemini-2.5-flash` | Long context, PDF support | Check API availability |

All models listed here support image inputs. Always verify vision support before deploying.

---

## Step 4 - Combine image with text context

For richer analysis, pass supplemental text alongside the image:

```python
from typing import Literal
from pydantic import BaseModel

class ProductAttributes(BaseModel):
    category: str
    color: str
    condition: Literal["new", "used", "damaged"]
    description: str

class CategorizeProduct(dspy.Signature):
    """Categorize a product from its photo and any provided context."""
    image: dspy.Image = dspy.InputField(desc="Product photo")
    context: str = dspy.InputField(desc="Additional context such as listing title or seller notes")
    attributes: ProductAttributes = dspy.OutputField(desc="Extracted product attributes")

categorizer = dspy.Predict(CategorizeProduct)
result = categorizer(
    image=dspy.Image(url="https://example.com/item.jpg"),
    context="Listed as: Vintage leather jacket, size M"
)
print(result.attributes.category, result.attributes.condition)
```

---

## Step 5 - Common patterns

### Alt text generation

```python
class GenerateAltText(dspy.Signature):
    """Generate concise, accurate alt text for accessibility."""
    image: dspy.Image = dspy.InputField(desc="Image to describe")
    context: str = dspy.InputField(desc="Page or article context where the image appears")
    alt_text: str = dspy.OutputField(desc="Alt text under 125 characters, describing the image content")

alt_gen = dspy.Predict(GenerateAltText)
result = alt_gen(
    image=dspy.Image(url="https://example.com/team-photo.jpg"),
    context="About page of a SaaS startup"
)
```

### Receipt and invoice OCR

```python
from typing import List

class LineItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total: float

class ExtractReceipt(dspy.Signature):
    """Extract all line items and totals from a receipt or invoice photo."""
    image: dspy.Image = dspy.InputField(desc="Photo of receipt or invoice")
    line_items: List[LineItem] = dspy.OutputField(desc="All line items found")
    subtotal: float = dspy.OutputField(desc="Subtotal before tax")
    tax: float = dspy.OutputField(desc="Tax amount")
    total: float = dspy.OutputField(desc="Total amount due")

extractor = dspy.Predict(ExtractReceipt)
result = extractor(image=dspy.Image(url="receipt.jpg"))
```

### Chart and graph data extraction

```python
class ExtractChart(dspy.Signature):
    """Extract the data series and labels from a chart or graph image."""
    image: dspy.Image = dspy.InputField(desc="Chart or graph image")
    chart_type: str = dspy.OutputField(desc="Type of chart - bar, line, pie, etc.")
    title: str = dspy.OutputField(desc="Chart title if present")
    data_summary: str = dspy.OutputField(desc="Summary of the data shown, including key values")

chart_reader = dspy.Predict(ExtractChart)
```

### UI screenshot analysis

```python
class AnalyzeUI(dspy.Signature):
    """Analyze a UI screenshot and identify components and issues."""
    image: dspy.Image = dspy.InputField(desc="UI screenshot")
    focus: str = dspy.InputField(desc="What aspect to analyze - layout, accessibility, bugs, etc.")
    findings: str = dspy.OutputField(desc="Detailed findings about the UI")
    suggestions: List[str] = dspy.OutputField(desc="Actionable improvement suggestions")

ui_analyzer = dspy.ChainOfThought(AnalyzeUI)
result = ui_analyzer(
    image=dspy.Image(url="screenshot.png"),
    focus="accessibility issues"
)
```

---

## Step 6 - OCR vs vision model tradeoff

| Scenario | Recommended approach |
|---|---|
| Clean printed text on white background | Tesseract or cloud OCR (faster, cheaper) |
| Handwritten text | Vision LLM (GPT-4o, Claude Sonnet) |
| Mixed layout with images and text | Vision LLM |
| Receipts with varied formatting | Vision LLM |
| High-volume document digitization | Dedicated OCR service + vision LLM for exceptions |
| Extracting structured fields from forms | Vision LLM with typed output |
| Sub-100ms latency requirement | Dedicated OCR only |

---

## Step 7 - Image preprocessing

Vision models have token budgets per image. Large images consume more tokens and slow responses.

```python
from PIL import Image as PILImage
import io, base64

def resize_for_vision(image_path: str, max_side: int = 1024) -> dspy.Image:
    """Resize image so the longest side is at most max_side pixels."""
    img = PILImage.open(image_path)
    ratio = min(max_side / img.width, max_side / img.height, 1.0)
    if ratio < 1.0:
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, PILImage.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return dspy.Image(url=f"data:image/jpeg;base64,{b64}")

image = resize_for_vision("large_photo.jpg")
result = analyzer(image=image, question="What is shown?")
```

Recommended limits:
- Max 1024px on the longest side for most tasks
- JPEG quality 80-85 for photos; PNG for screenshots with text
- Avoid sending multiple large images in a single call

---

## Step 8 - Evaluate visual tasks

For description quality, use an AI judge:

```python
class ImageDescriptionJudge(dspy.Signature):
    """Judge whether an image description is accurate and complete."""
    image: dspy.Image = dspy.InputField(desc="The original image")
    description: str = dspy.InputField(desc="Description to evaluate")
    score: int = dspy.OutputField(desc="Score from 1 to 5, where 5 is fully accurate and complete")
    reasoning: str = dspy.OutputField(desc="Explanation of the score")

judge = dspy.Predict(ImageDescriptionJudge)
```

For structured extraction (OCR, receipts), use exact match or field-level comparison:

```python
def eval_receipt_extraction(prediction, ground_truth):
    correct_items = sum(
        1 for item in prediction.line_items
        if item.description in [g.description for g in ground_truth.line_items]
    )
    recall = correct_items / max(len(ground_truth.line_items), 1)
    total_match = abs(prediction.total - ground_truth.total) < 0.01
    return {"item_recall": recall, "total_correct": total_match}
```

---

## When NOT to use vision LLMs

- **Object detection at scale** - use YOLO, Detectron2, or a dedicated CV API
- **Simple OCR on clean printed text** - Tesseract or cloud OCR is faster and cheaper
- **Pixel-level segmentation** - use Segment Anything or dedicated segmentation models
- **Real-time video processing** - vision LLMs have too much latency
- **Sub-100ms latency** - vision LLMs typically take 1-5 seconds per image
- **High-volume identical-format documents** - train a specialized model or use template OCR

---

## Key patterns

```python
# Pattern 1 - Direct extraction with typed output
class ExtractFields(dspy.Signature):
    """Extract structured fields from the image."""
    image: dspy.Image = dspy.InputField()
    fields: MyDataModel = dspy.OutputField()

extractor = dspy.Predict(ExtractFields)

# Pattern 2 - Reasoning about image content
class ReasonAboutImage(dspy.Signature):
    """Reason step by step about what the image shows."""
    image: dspy.Image = dspy.InputField()
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()

reasoner = dspy.ChainOfThought(ReasonAboutImage)

# Pattern 3 - Batch processing
images = [dspy.Image(url=p) for p in image_paths]
results = [extractor(image=img) for img in images]

# Pattern 4 - Iterative refinement when quality is low
refiner = dspy.Refine(dspy.Predict(AnalyzeImage), N=3, reward_fn=my_reward)
```

---

## Gotchas

- **Wrap image inputs in `dspy.Image`** - Claude writes raw URL strings as image inputs instead of wrapping them. Always wrap the URL or local path directly: `dspy.Image(url="https://...")` or `dspy.Image(url="local/path.jpg")`. Raw strings are treated as text, not images. (The old classmethods `from_url()`, `from_file()`, and `from_PIL()` are deprecated — use `dspy.Image(url=...)` for all forms.)

- **Verify the model supports vision** - Claude picks a model that does not support image inputs. Not all LLMs handle images. Confirm vision support for your chosen model before deploying (GPT-4o, Claude 3.5+, Gemini 2.x all work).

- **Use `dspy.Refine` not `dspy.Assert`** - Claude uses `dspy.Assert`/`dspy.Suggest` to validate image outputs. Use `dspy.Refine` with a reward function for iterative improvement instead.

- **Resize before sending** - Claude sends full-resolution images without resizing. Large images (4K, RAW photos) consume excessive tokens and can hit context limits. Resize to max 1024px on the longest side before processing.

- **Match module to task** - Claude applies `dspy.ChainOfThought` to all image tasks. Use `dspy.Predict` for direct extraction (OCR, field parsing). Reserve `dspy.ChainOfThought` for tasks that genuinely benefit from image reasoning, like diagnosing a bug from a screenshot.

---

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- `/ai-parsing-data` - parse structured data from text; complement with image extraction for mixed inputs
- `/ai-stopping-hallucinations` - reduce made-up field values in vision extraction pipelines
- `/ai-checking-outputs` - validate extracted fields after vision model output
- `/dspy-refine` - iterative refinement when initial image analysis quality is low
- `/dspy-modules` - understand `dspy.Predict` vs `dspy.ChainOfThought` for image tasks
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For API details (dspy.Image constructor, field parameters, module selection table), see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md):
  - Product photo categorizer
  - Alt text generator
  - Receipt/invoice OCR pipeline
