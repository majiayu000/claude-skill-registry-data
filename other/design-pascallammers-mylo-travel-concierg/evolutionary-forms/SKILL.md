---
name: evolutionary-forms
description: Generate and evolve abstract visual forms through a Darwinian selection process. Use when users want to create organic shapes, evolve visual designs, breed form variations, or explore parametric design through natural language descriptions like "soft protective curves".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Evolutionary Form Generation

Create and evolve organic visual forms through parametric generation and selective breeding.

## When to Use This Skill

Activate when the user:
- Wants to generate abstract/organic visual forms
- Mentions "evolve", "breed", or "iterate" designs
- Describes forms with aesthetic terms ("soft", "protective", "organic", "bold")
- Asks for variations on a visual theme
- Wants to explore parametric design possibilities

## Quick Start

```bash
# Initialize project
uv run python -m evolutionary_drawbot init

# Generate initial population
uv run python -m evolutionary_drawbot gen0 --population 16

# Generate with natural language constraints
uv run python -m evolutionary_drawbot gen0 --population 16 --prompt "soft protective 4 lobes"

# View contact_sheet.pdf, then record winners
uv run python -m evolutionary_drawbot select gen_000 --winners 1,5,9,13

# Breed next generation from winners
uv run python -m evolutionary_drawbot breed gen_000

# Check status anytime
uv run python -m evolutionary_drawbot status
```

## The Darwin Loop

```
┌─────────────────────────────────────────────────────────┐
│                                                          │
│   1. GENERATE         2. REVIEW          3. SELECT       │
│   ───────────        ─────────          ────────        │
│   gen0/breed    →    contact_sheet.pdf  →  winners.json  │
│                                                          │
│                           ↓                              │
│                                                          │
│   4. BREED            ←────────────────────────          │
│   ───────                                                │
│   Creates next generation from selected winners          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Output Structure

```
output/generations/
├── gen_000/
│   ├── population.jsonl      # Genome records (parameters + metadata)
│   ├── candidates/
│   │   ├── 0001.svg          # Individual form SVGs
│   │   ├── 0001_meta.json    # Rendering metadata
│   │   └── ...
│   ├── contact_sheet.pdf     # Grid view for selection
│   └── winners.json          # Selected winner indices
└── gen_001/
    └── ...
```

## Natural Language Translation

The system translates descriptive words into parameter constraints:

| Word | Effect |
|------|--------|
| **soft** | High roundness, moderate tension, slight wobble |
| **protective** | High envelope_factor, moderate lobe_depth |
| **organic** | More wobble, moderate roundness |
| **bold** | Deeper lobes, stronger presence |
| **delicate** | Minimal wobble, shallow lobes, high roundness |
| **flowing** | Low tension, high roundness |

### Example Prompts

```bash
# Soft, protective forms
--prompt "soft protective curves"

# Organic flower-like shapes
--prompt "organic flowing 5 petals"

# Bold, structured forms
--prompt "bold angular 3 lobes"

# Delicate, minimal shapes
--prompt "delicate subtle round"
```

## Parameters

The soft_blob generator uses 8 parameters (stored normalized 0-1):

| Parameter | Range | Description |
|-----------|-------|-------------|
| `lobe_count` | 2-6 | Number of radial lobes |
| `lobe_depth` | 0-1 | Indent depth between lobes |
| `envelope_factor` | 0.3-0.9 | Protective/embracing quality |
| `roundness` | 0-1 | Curve smoothness |
| `wobble` | 0-0.2 | Organic irregularity |
| `tension` | 0.3-0.9 | Bezier curve tightness |
| `aspect` | 0.6-1.4 | Width/height ratio |
| `rotation` | 0-360 | Base orientation |

## Configuration

Edit `config/brand_dna.json` to customize:
- Parameter ranges and defaults
- Fill/stroke colors and widths
- Evolution settings (mutation rate, population size)

## CLI Commands Reference

### `init`
Initialize project directories and verify config.

### `gen0`
Generate initial population (generation 0).

```bash
uv run python -m evolutionary_drawbot gen0 [options]

Options:
  --population, -n INT    Population size (default: 16)
  --prompt, -p TEXT       Natural language constraints
```

### `render`
Re-render candidates and contact sheet.

```bash
uv run python -m evolutionary_drawbot render GENERATION
```

### `select`
Record selected winners by their index numbers.

```bash
uv run python -m evolutionary_drawbot select GENERATION --winners INDICES

Example:
  uv run python -m evolutionary_drawbot select gen_000 --winners 1,5,9,13
```

### `breed`
Create next generation from selected winners.

```bash
uv run python -m evolutionary_drawbot breed GENERATION [options]

Options:
  --population, -n INT    Offspring count (default from config)
```

### `status`
Show current evolution status and next steps.

```bash
uv run python -m evolutionary_drawbot status
```

## Programmatic Usage

```python
from evolutionary_drawbot import FormGenome, ParameterSpec
from evolutionary_drawbot.evolution import generate_population, breed
from evolutionary_drawbot.translator import translate_prompt
from evolutionary_drawbot.render import render_genome
from evolutionary_drawbot.contact_sheet import generate_contact_sheet

# Translate prompt to constraints
constraints = translate_prompt("soft protective 4 lobes")

# Generate population
population = generate_population(
    size=16,
    gen_num=0,
    prompt_constraints=constraints
)

# Render individual genome
render_genome(population[0], output_dir, canvas_size=(200, 200))

# Create contact sheet
generate_contact_sheet(population, "contact_sheet.pdf")

# Breed from winners
parents = [population[0], population[4], population[8]]
offspring = generate_population(
    size=16,
    gen_num=1,
    parents=parents,
    mutation_rate=0.2
)
```

## Workflow Examples

### Example 1: Explore "care and safety" aesthetics

```bash
# Start with protective, nurturing forms
uv run python -m evolutionary_drawbot gen0 -n 16 --prompt "protective nurturing soft"

# Review contact_sheet.pdf, select forms that feel most "safe"
uv run python -m evolutionary_drawbot select gen_000 --winners 2,7,11,15

# Breed and continue refining
uv run python -m evolutionary_drawbot breed gen_000

# After a few generations, you'll have a refined family of forms
```

### Example 2: Create brand mark variations

```bash
# Start with specific structural constraints
uv run python -m evolutionary_drawbot gen0 -n 24 --prompt "bold 4 lobes organic"

# Select the most distinctive candidates
uv run python -m evolutionary_drawbot select gen_000 --winners 3,8,12,19,22

# Breed with larger population for more variation
uv run python -m evolutionary_drawbot breed gen_000 -n 24
```

### Example 3: From random to refined

```bash
# Start completely random
uv run python -m evolutionary_drawbot gen0 -n 32

# Select interesting directions (no prior bias)
uv run python -m evolutionary_drawbot select gen_000 --winners 5,11,23,28

# Let the evolution discover the aesthetic
uv run python -m evolutionary_drawbot breed gen_000
```

## Integration with DrawBot Designer

The evolved forms can be used in DrawBot layouts:

```python
import drawBot as db
from evolutionary_drawbot.genome import load_population
from evolutionary_drawbot.form_generators import generate_soft_blob

# Load a winning form
population = load_population("output/generations/gen_003/population.jsonl")
winner = population[4]  # Form #5

# Use in a poster layout
db.newPage(612, 792)
path = generate_soft_blob(winner, center=(306, 500), size=300)
db.fill(0.2, 0.3, 0.4)
db.drawPath(path)

# Add text using the design system...
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No forms appear | Check DrawBot is installed: `uv sync --extra drawbot` |
| Winners not saved | Use 1-based indices, comma-separated |
| Diversity too low | Increase mutation_rate in brand_dna.json |
| Forms too similar | Select more diverse winners, increase population |
| Prompt not working | Check keyword spelling (see translator.py) |

## Available Keywords

### Softness/Hardness
soft, gentle, hard, angular, sharp

### Protection/Safety
protective, safe, embracing, nurturing, sheltering

### Organic/Natural
organic, natural, flowing, fluid

### Strength/Boldness
bold, strong, powerful

### Delicacy
delicate, subtle, light

### Complexity
complex, simple, intricate

### Shape
round, curved, wavy, scalloped

### Proportion
tall, wide, compact

### Structure
petals, lobes, flower, clover

### Numbers
two, three, four, five, six (+ lobes/petals)

## Files

```
evolutionary_drawbot/
├── __init__.py           # Package exports
├── __main__.py           # CLI entry point
├── cli.py                # Command implementations
├── parameters.py         # ParameterSpec with [0..1] normalization
├── genome.py             # FormGenome dataclass + persistence
├── evolution.py          # breed(), mutate(), generate_population()
├── translator.py         # NLP → parameter constraints
├── render.py             # Genome → SVG + metadata
├── contact_sheet.py      # PDF contact sheet generator
└── form_generators/
    └── soft_blob.py      # Bezier-based organic forms

config/
└── brand_dna.json        # Parameter ranges, style, evolution settings
```

## Future Extensions

- Additional form generators (crystalline, geometric, etc.)
- Automated fitness evaluation
- Layout template evolution
- Color parameter breeding
- Web-based selection UI
