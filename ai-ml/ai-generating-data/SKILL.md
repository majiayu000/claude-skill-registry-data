---
name: ai-generating-data
description: Generate synthetic training data when you do not have enough real examples. Use when you are starting from scratch with no data, need a proof of concept fast, have too few examples for optimization, cannot use real customer data for privacy or compliance, need to fill gaps in edge cases, have unbalanced categories, added new categories, or changed your schema. Also used for create training data with AI, not enough examples to train, augment small dataset, generate labeled examples from scratch, cold start problem for AI, need data but cannot label manually, privacy-safe synthetic data, test data generation for ML, create diverse training examples, data augmentation for NLP, bootstrap dataset from nothing, DSPy synthetic data generation, quality filtering, bootstrapping from zero.
---

# Generate Synthetic Training Data

Guide the user through generating high-quality synthetic training data with DSPy. This solves the "I do not have data" problem that blocks every other AI workflow.

## When NOT to generate synthetic data

- **You have enough real data** — 200+ labeled examples is usually enough for optimization. Real data is always better than synthetic.
- **Exact-match tasks** — if your task has a known correct answer (math, lookup, structured extraction from templates), write a script to generate test cases programmatically instead of using an LM.
- **The LM does not understand your domain** — synthetic data inherits the generator LM's biases. For highly specialized domains (medical, legal, niche industry), a few real expert-labeled examples outweigh hundreds of synthetic ones.

## Step 1: Understand the data gap

Ask the user:
1. **What does your AI do?** (classification, extraction, Q&A, generation?)
2. **How many real examples do you have?** (zero, a handful, or hundreds with gaps?)
3. **What is the gap?** (no data at all, missing categories, edge cases, privacy constraints?)
4. **What format are the inputs/outputs?** (text in/category out, text in/JSON out, etc.)

## Step 2: Define what an example looks like

Your generator's outputs should match your task's inputs and expected outputs.

```python
import dspy

# Your task — what the AI will do in production
class ClassifyTicket(dspy.Signature):
    """Classify a support ticket into a category."""
    ticket_text: str = dspy.InputField()
    category: str = dspy.OutputField()

# Generator — produces examples for your task
class GenerateTicketExample(dspy.Signature):
    """Generate a realistic support ticket with its correct category."""
    category: str = dspy.InputField(desc="the target category to generate an example for")
    ticket_text: str = dspy.OutputField(desc="a realistic support ticket for this category")
```

The generator's output fields become inputs to your task. Think of it as: "given what I want the answer to be, generate a realistic input."

## Step 3: Write seed examples

Start with 5-10 hand-written examples. These anchor the generator's understanding of what "realistic" means for your domain.

```python
seeds = [
    dspy.Example(
        ticket_text="I was charged twice for my subscription this month. Order #4521.",
        category="billing"
    ).with_inputs("ticket_text"),
    dspy.Example(
        ticket_text="The app crashes when I try to upload a profile photo on Android.",
        category="bug"
    ).with_inputs("ticket_text"),
    dspy.Example(
        ticket_text="How do I export my data to CSV? I cannot find the option anywhere.",
        category="how-to"
    ).with_inputs("ticket_text"),
    dspy.Example(
        ticket_text="I would love to see dark mode added. The white background hurts my eyes.",
        category="feature-request"
    ).with_inputs("ticket_text"),
    dspy.Example(
        ticket_text="My account got locked after too many login attempts. Please help.",
        category="account"
    ).with_inputs("ticket_text"),
]
```

Even 5 seeds dramatically improve generation quality over zero.

## Step 4: Generate in batches

Pick the strategy that fits your gap:

| Strategy | When to use | Example |
|----------|------------|---------|
| Category-driven | Fix class imbalance, new categories | Generate N per category |
| Seed-and-vary | Augment existing examples with different tones | Vary each seed by tone, length, complexity |
| Scenario-driven | Target specific edge cases | Generate from failure scenario descriptions |
| Difficulty-driven | Build a balanced difficulty curve | Generate easy/medium/hard separately |
| Diversity trick (`sindex`) | Prevent repetitive outputs | Add random seed index to break LM patterns |
| Programmatic (Faker) | Structured fields with known formats | Names, addresses, dates, IDs cheaply at scale |

### Category-driven generation

```python
lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

categories = ["billing", "bug", "how-to", "feature-request", "account"]
examples = []

generator = dspy.Predict(GenerateTicketExample)
for category in categories:
    for i in range(50):
        result = generator(category=category)
        examples.append(
            dspy.Example(ticket_text=result.ticket_text, category=category)
            .with_inputs("ticket_text")
        )

print(f"Generated {len(examples)} examples")
```

### Scenario-driven generation (for edge cases)

```python
class GenerateScenarioTicket(dspy.Signature):
    """Generate a support ticket matching a specific scenario."""
    category: str = dspy.InputField()
    scenario: str = dspy.InputField(desc="the specific scenario to generate")
    ticket_text: str = dspy.OutputField()

gen = dspy.Predict(GenerateScenarioTicket)
scenarios = [
    ("billing", "customer charged in wrong currency"),
    ("billing", "refund for a cancelled subscription"),
    ("bug", "issue only happens on slow network connections"),
    ("how-to", "customer is non-technical and confused by jargon"),
]
for category, scenario in scenarios:
    result = gen(category=category, scenario=scenario)
    examples.append(dspy.Example(ticket_text=result.ticket_text, category=category).with_inputs("ticket_text"))
```

### Programmatic generation with Faker

For structured fields (names, addresses, dates, phone numbers), Faker generates hundreds of thousands of examples instantly with zero LM cost. In one production case, 500K synthetic name records were generated with Faker + custom cultural providers, then used to fine-tune models to 96% accuracy.

```python
from faker import Faker
from faker.providers import BaseProvider

fake = Faker()

# Custom provider for domain-specific data
class TicketProvider(BaseProvider):
    def order_id(self):
        return f"ORD-{self.random_int(1000, 99999)}"

    def product_name(self):
        return self.random_element(["Pro Plan", "Starter", "Enterprise", "Team"])

fake.add_provider(TicketProvider)

# Generate structured training records at scale
examples = []
for _ in range(10_000):
    examples.append(dspy.Example(
        ticket_text=f"Hi, I'm {fake.name()}. Order {fake.order_id()} for {fake.product_name()} "
                    f"was charged to {fake.email()} but I need it on a different card.",
        category="billing"
    ).with_inputs("ticket_text"))
```

**When to use Faker vs LM generation:**
- **Faker** — fields with known formats (names, emails, dates, IDs, addresses). Fast, free, structurally correct.
- **LM generation** — open-ended text, realistic tone, complex scenarios, domain-specific language.
- **Both together** — Faker for structured scaffolding, LM to add realistic surrounding context.

### Diversity trick

Add a random `sindex` field to push the LM toward varied outputs:

```python
import random

class GenerateDiverse(dspy.Signature):
    """Generate a unique and realistic support ticket."""
    category: str = dspy.InputField()
    sindex: str = dspy.InputField(desc="a unique seed index for diversity")
    ticket_text: str = dspy.OutputField()

gen = dspy.Predict(GenerateDiverse)
for category in categories:
    for i in range(50):
        result = gen(category=category, sindex=str(random.randint(0, 1_000_000)))
        examples.append(dspy.Example(ticket_text=result.ticket_text, category=category).with_inputs("ticket_text"))
```

## Step 5: Filter for quality

Generated data always contains bad examples. Generate 2-3x what you need, keep ~50%.

### Metric-based filtering

```python
program = dspy.ChainOfThought(ClassifyTicket)
filtered = []

for ex in examples:
    pred = program(**ex.inputs())
    if metric(ex, pred):
        filtered.append(ex)

print(f"Kept {len(filtered)}/{len(examples)} ({100*len(filtered)//len(examples)}%)")
```

### LM-based assessment (more robust)

```python
class AssessExample(dspy.Signature):
    """Is this a realistic and correctly labeled example?"""
    ticket_text: str = dspy.InputField()
    category: str = dspy.InputField()
    is_realistic: bool = dspy.OutputField(desc="true if this looks like a real support ticket")
    is_correctly_labeled: bool = dspy.OutputField(desc="true if the category matches the ticket")

assessor = dspy.Predict(AssessExample)
filtered = [ex for ex in examples
    if (r := assessor(ticket_text=ex.ticket_text, category=ex.category)).is_realistic and r.is_correctly_labeled]
```

### Deduplicate

```python
seen = set()
unique = [ex for ex in filtered if (k := ex.ticket_text.strip().lower()) not in seen and not seen.add(k)]
filtered = unique
```

## Step 6: Optimize the generator itself (advanced)

Optimizing the prompt used to generate data dramatically improves downstream quality. This is meta-optimization: better generator prompts produce better data.

```python
class DataGenerator(dspy.Module):
    def __init__(self):
        self.generate = dspy.ChainOfThought(GenerateTicketExample)

    def forward(self, category):
        return self.generate(category=category)

def generator_metric(example, prediction, trace=None):
    classifier = dspy.Predict(ClassifyTicket)
    task_example = dspy.Example(ticket_text=prediction.ticket_text, category=example.category).with_inputs("ticket_text")
    task_pred = classifier(**task_example.inputs())
    return task_pred.category.lower() == example.category.lower()

optimizer = dspy.BootstrapFewShot(metric=generator_metric)
optimized_generator = optimizer.compile(DataGenerator(), trainset=seeds)
```

## Step 7: Use generated data for optimization

```python
from dspy.evaluate import Evaluate

random.shuffle(filtered)
split = int(len(filtered) * 0.8)
trainset, devset = filtered[:split], filtered[split:]

program = dspy.ChainOfThought(ClassifyTicket)
optimizer = dspy.MIPROv2(metric=metric, auto="medium")
optimized = optimizer.compile(program, trainset=trainset)

evaluator = Evaluate(devset=devset, metric=metric, num_threads=4, display_progress=True)
score = evaluator(optimized)
print(f"Score on synthetic dev set: {score:.1f}%")
# Typical: 70-85% on synthetic, validate on real data when available

optimized.save("optimized_program.json")
```

If you have even a small number of real examples, use them as the dev set instead — real data gives more trustworthy evaluation.

## Gotchas

- **Claude generates all examples with the same LM config used for the task.** Use a stronger model for generation (e.g., a larger model) and a cheaper model for the task. Higher-quality generation data is worth the extra cost — it directly improves the downstream program.
- **Claude forgets `.with_inputs()` on generated Examples.** Every synthetic `dspy.Example` must call `.with_inputs("field1", ...)` to mark input fields. Without this, the optimizer passes all fields (including expected outputs) to the program, inflating scores.
- **The `n=N` batch parameter is not supported by all providers.** Claude defaults to `dspy.Predict(sig, n=20)` for batch generation, but Anthropic and some other providers do not support the `n` parameter. Use the loop pattern as a reliable fallback for any provider.
- **Claude generates 50 examples and calls it done.** For optimization, you typically need 200+ examples after filtering. Since filtering removes ~50%, generate at least 400-500 raw examples. More is better — generation is cheap compared to the quality improvement.
- **Synthetic eval scores are inflated.** If both training and evaluation data are synthetic, the eval score overestimates real-world quality. Always validate the final optimized program on real data when available, even if it is only 20-30 hand-labeled examples.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Improving accuracy** to measure and optimize your program after generating data -- see `/ai-improving-accuracy`
- **Fine-tuning** once you have enough generated data for weight optimization -- see `/ai-fine-tuning`
- **Kickoff** to scaffold a project, then fill data with this skill -- see `/ai-kickoff`
- **Sorting** for classification patterns your generated data will train -- see `/ai-sorting`
- **Signatures** for defining the generator and task input/output contracts -- see `/dspy-signatures`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For end-to-end worked examples (cold start, edge cases, privacy), see [examples.md](examples.md)
- For API signatures, parameter tables, and quick-reference, see [reference.md](reference.md)
