---
name: claude-design-system-prompt
description: Install and customize the reverse-engineered Claude Design system prompt to turn any LLM into an opinionated, accessibility-aware design collaborator
triggers:
  - "set up the Claude Design system prompt"
  - "install the design system prompt"
  - "configure the design assistant prompt"
  - "use the Claude Design collaborator"
  - "add design skills to this agent"
  - "integrate the accessibility-aware design prompt"
  - "customize the design system prompt"
  - "run a design audit with Claude prompt"
---

# claude-design-system-prompt

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## What it does

`claude-design-system-prompt` is a reverse-engineered system prompt and skill library that transforms any LLM into an opinionated design collaborator that:

- **Rejects AI slop**: No generic SaaS gradients, emoji decoration, or rounded-corner cards
- **Enforces accessibility**: WCAG compliance, semantic HTML, keyboard navigation, motion preferences
- **Prioritizes content**: Every element must earn its place—no filler
- **Uses real web standards**: CSS Grid, `oklch()`, `text-wrap: pretty`, interactive prototypes
- **Thinks in systems**: Components and tokens over one-off pages

The prompt includes 20 design principle chapters and 14 invokable procedural skills for production, extraction, and review work.

## Installation

### Clone the repository

```bash
git clone https://github.com/Trystan-SA/claude-design-system-prompt.git
cd claude-design-system-prompt
```

### Directory structure

```
claude/                              # For Claude Code / Claude.ai
├── system-prompt.md                 # 20-chapter design philosophy
└── skills/                          # 14 procedural skills
codex/                               # For OpenAI Codex (single-loop variant)
├── AGENTS.md                        # Auto-discovered entry point
├── system-prompt.md
└── skills/
```

## Using the system prompt

### Direct integration (any LLM)

Copy the entire contents of `claude/system-prompt.md` (or `codex/system-prompt.md` for Codex) and paste it as the system prompt:

```markdown
<!-- Example: Claude.ai Custom Instructions -->
Paste full contents of claude/system-prompt.md here
```

The agent will automatically follow the design philosophy and reference skills by name when tasks match.

### Programmatic integration (API)

```python
# Python example with Anthropic API
import anthropic
from pathlib import Path

# Load the system prompt
system_prompt = Path("claude-design-system-prompt/claude/system-prompt.md").read_text()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-opus-4.8-20250514",
    max_tokens=4096,
    system=system_prompt,
    messages=[{
        "role": "user",
        "content": "Design a landing page for a climate data API"
    }]
)

print(message.content)
```

```javascript
// Node.js example with Anthropic SDK
import Anthropic from '@anthropic-ai/sdk';
import { readFileSync } from 'fs';

const systemPrompt = readFileSync(
  'claude-design-system-prompt/claude/system-prompt.md',
  'utf-8'
);

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const message = await client.messages.create({
  model: 'claude-opus-4.8-20250514',
  max_tokens: 4096,
  system: systemPrompt,
  messages: [{
    role: 'user',
    content: 'Create a wireframe for a developer documentation site'
  }]
});

console.log(message.content);
```

## Invoking skills

Skills are self-contained procedures. When a user's request matches a skill, the agent loads and follows it.

### Production skills (build something)

```bash
# Discovery and direction
"Run discovery questions for this project"
"Set the frontend aesthetic direction"

# Exploration and prototyping
"Create wireframes with 3 variations"
"Make an interactive prototype"
"Generate variations across different aesthetic axes"

# Special formats
"Make a deck presentation"
"Make this design tweakable with a floating panel"
```

### System skills (extract structure)

```bash
# Extract from existing sources
"Extract the design system from the Stripe homepage"
"Extract components from this codebase"
```

### Review skills (audit and fix)

```bash
# Comprehensive audits
"Run an accessibility audit"
"Check for AI slop"
"Review hierarchy and rhythm"
"Review all interaction states"
"Run a polish pass"
```

## Skill workflow examples

### Greenfield project flow

```markdown
1. Run discovery-questions
   → Gather context, goals, constraints, audience

2. Set frontend-aesthetic-direction
   → Commit to palette, typography, tone

3. Create wireframe
   → 3+ low-fidelity variations

4. Make-a-prototype
   → Interactive clickable prototype

5. Run polish-pass
   → Final accessibility, slop, hierarchy, interaction review
```

### Brand-aware flow

```markdown
1. Design-system-extract
   → Pull tokens from existing brand site

2. Generate-variations
   → 3+ high-fidelity variations using brand tokens

3. Make-tweakable
   → Add floating tweak panel for live adjustments

4. Polish-pass
   → Final review gate
```

### Audit-only flow

```markdown
1. Accessibility-audit
   → WCAG, semantic HTML, keyboard, motion

2. AI-slop-check
   → Detect gradient/emoji/font/house-style tropes

3. Hierarchy-rhythm-review
   → Size, weight, color, spacing scale

4. Interaction-states-pass
   → Hover, active, disabled, focus, loading, validation
```

## Loading individual skills

If you want to invoke a specific skill programmatically:

```python
from pathlib import Path

# Load main prompt + specific skill
system_prompt = Path("claude/system-prompt.md").read_text()
wireframe_skill = Path("claude/skills/wireframe.md").read_text()

combined_prompt = f"{system_prompt}\n\n## ACTIVE SKILL\n\n{wireframe_skill}"

message = client.messages.create(
    model="claude-opus-4.8-20250514",
    system=combined_prompt,
    messages=[{"role": "user", "content": "Wireframe a SaaS dashboard"}]
)
```

## Customization

### Adapt for your environment

The default prompt assumes HTML output (like Claude.ai's design tool). To adapt:

**For Figma plugins:**
- Edit chapters 2 (Workflow) and 17 (Output principles)
- Replace HTML references with Figma API calls
- Keep chapters 5–16 (design principles) unchanged

**For code-only assistants:**
- Update chapter 14 (Respecting the medium) to reference your framework
- Add framework-specific component examples

**For chat-only design coaches:**
- Remove artifact/output instructions from chapter 17
- Focus on conversational guidance and critique

### Adjust model calibration

The `claude/` variant is optimized for Anthropic Fable 5 / Opus 4.7+ models. For older models or other providers:

**Restore stronger imperatives:**
```markdown
<!-- Current (calm) -->
Ask questions when context is insufficient.

<!-- Older models (directive) -->
CRITICAL: You MUST ask at least 3 questions before proceeding.
```

**Add explicit quotas:**
```markdown
<!-- Current (conditional) -->
Generate variations when exploring aesthetic directions.

<!-- Older models (quota) -->
Always generate at least 3 variations for every design request.
```

### Add custom skills

Create a new skill in `claude/skills/`:

```markdown
# my-custom-skill.md

## When to invoke
Invoke when the user requests [specific trigger condition].

## Procedure

### Phase 1: Discovery
1. Ask [specific questions]
2. Confirm [specific constraints]

### Phase 2: Execution
1. [Step-by-step process]
2. [Expected output format]

### Phase 3: Review
1. [Quality gates]
2. [Handoff to other skills if needed]
```

Then reference it in `system-prompt.md` chapter 20.

## Configuration

### Environment variables

No API keys required for the prompt itself. When using with LLM APIs:

```bash
# Anthropic
export ANTHROPIC_API_KEY=your_key_here

# OpenAI
export OPENAI_API_KEY=your_key_here
```

### Platform-specific settings

**Claude Code:**
- Place `system-prompt.md` in your project's `.claude/` directory
- Skills auto-load when referenced by name

**Cursor:**
- Add to `.cursorrules` file
- Reference skills in comments

**OpenAI Codex:**
- Use `codex/AGENTS.md` as entry point (auto-discovered)
- Skills run sequentially instead of parallel

## Troubleshooting

### Agent skips question rounds

**Symptom:** Agent jumps straight to design without asking questions  
**Fix:** The current Claude models need explicit triggers. Ensure you're using `claude/` variant. If using older models, add stronger imperatives:

```markdown
When context is insufficient, always ask questions before proceeding.
```

### Agent produces generic SaaS aesthetics

**Symptom:** Cream backgrounds, terracotta accents, serif display type  
**Fix:** Explicitly invoke `frontend-aesthetic-direction` skill first:

```bash
"Set the frontend aesthetic direction with 4 distinct options"
```

The skill's four-directions protocol prevents house-style collapse.

### Skills not triggering automatically

**Symptom:** Agent doesn't recognize when to invoke a skill  
**Fix:** Current models under-reach for optional capabilities. Be explicit:

```bash
# Instead of:
"Design a landing page"

# Say:
"Run discovery questions, then create wireframes with 3 variations"
```

### Reviews miss obvious issues

**Symptom:** Accessibility or slop checks don't catch known problems  
**Fix:** Current models follow "only report important" too literally. The prompt uses coverage-first reviews, but you may need to chain skills:

```bash
"Run accessibility-audit, then ai-slop-check, then hierarchy-rhythm-review"
```

### Output doesn't use modern CSS features

**Symptom:** Design uses old CSS instead of Grid, `oklch()`, etc.  
**Fix:** Reference chapter 14 (Respecting the medium) explicitly:

```bash
"Create a prototype using CSS Grid and oklch() colors per the medium principles"
```

## Real-world examples

### Complete greenfield flow

```python
import anthropic
from pathlib import Path

system_prompt = Path("claude/system-prompt.md").read_text()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Phase 1: Discovery
discovery = client.messages.create(
    model="claude-opus-4.8-20250514",
    system=system_prompt,
    messages=[{
        "role": "user",
        "content": "I need a landing page for a climate data API. Run discovery questions."
    }]
)

# User answers questions, then:

# Phase 2: Aesthetic direction
direction = client.messages.create(
    model="claude-opus-4.8-20250514",
    system=system_prompt,
    messages=[
        {"role": "user", "content": "Run discovery questions..."},
        {"role": "assistant", "content": discovery.content[0].text},
        {"role": "user", "content": "[Answers to questions]"},
        {"role": "user", "content": "Set the frontend aesthetic direction with 4 options"}
    ]
)

# Phase 3: Wireframes
wireframe = client.messages.create(
    model="claude-opus-4.8-20250514",
    system=system_prompt,
    messages=[
        # ... previous context ...
        {"role": "user", "content": "Create wireframes using direction option 2"}
    ]
)

# Phase 4: Interactive prototype
prototype = client.messages.create(
    model="claude-opus-4.8-20250514",
    system=system_prompt,
    messages=[
        # ... previous context ...
        {"role": "user", "content": "Make an interactive prototype from wireframe B"}
    ]
)

# Phase 5: Polish
final = client.messages.create(
    model="claude-opus-4.8-20250514",
    system=system_prompt,
    messages=[
        # ... previous context ...
        {"role": "user", "content": "Run a full polish pass"}
    ]
)
```

### Extract design system from existing site

```javascript
import Anthropic from '@anthropic-ai/sdk';
import { readFileSync } from 'fs';

const systemPrompt = readFileSync('claude/system-prompt.md', 'utf-8');
const extractSkill = readFileSync('claude/skills/design-system-extract.md', 'utf-8');

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const message = await client.messages.create({
  model: 'claude-opus-4.8-20250514',
  system: `${systemPrompt}\n\n## ACTIVE SKILL\n\n${extractSkill}`,
  messages: [{
    role: 'user',
    content: 'Extract the design system from https://stripe.com - analyze colors, typography, spacing, components'
  }]
});

// Returns structured tokens: colors, typography, spacing scale, components
console.log(message.content);
```

### Chain multiple review skills

```python
reviews = [
    "accessibility-audit",
    "ai-slop-check", 
    "hierarchy-rhythm-review",
    "interaction-states-pass"
]

results = []
for skill_name in reviews:
    skill_path = f"claude/skills/{skill_name}.md"
    skill_content = Path(skill_path).read_text()
    
    response = client.messages.create(
        model="claude-opus-4.8-20250514",
        system=f"{system_prompt}\n\n{skill_content}",
        messages=[{
            "role": "user",
            "content": f"Run {skill_name} on the current prototype"
        }]
    )
    
    results.append({
        "skill": skill_name,
        "findings": response.content[0].text
    })

# Aggregate all findings
print("=== COMPREHENSIVE REVIEW ===")
for result in results:
    print(f"\n## {result['skill']}")
    print(result['findings'])
```

## Contributing

The project welcomes:
- Additional review skills (copy review, motion review, dark-mode parity)
- Adapted prompts for other environments (Figma, terminal-only)
- Real-world failure cases to defend against
- Translations into other languages

Keep the operational tone and avoid bloat—every chapter must earn its place.

## License

MIT — use, modify, and distribute for any purpose, including commercial use.
