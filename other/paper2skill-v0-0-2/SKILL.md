---
name: paper2skill
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
description: "Convert arXiv and ML/AI research papers into ready-to-use Claude agent skills in seconds — so anyone can apply cutting-edge techniques without reading the full paper. Use this skill whenever the user wants to turn a paper into a skill, extract practical techniques from research, build a skill library from papers, create a paper-to-skill pipeline, convert arXiv papers into reusable agent instructions, or batch-process multiple papers into skills. Also trigger when someone asks about extracting actionable knowledge from papers, building skill libraries from literature, making research practical for LLM agents, or systematically converting academic contributions into structured agent capabilities."
---

# Paper2Skill: Turn Research Papers into Agent Skills Anyone Can Use

This skill converts academic papers into structured, actionable agent skills. Each output skill lets an AI agent apply a paper's core technique out-of-the-box — without the user needing to read or understand the original paper.

Skills must be generated from the original arXiv paper (preferably the HTML version at `https://arxiv.org/html/XXXX.XXXXX`), not from summaries, blog posts, or third-party descriptions. The goal is to distill what is genuinely useful about each research contribution for future research and practical application.

## Important: What Makes a Useful Agent Skill

Based on Anthropic's Complete Guide to Building Skills for Claude, effective skills share these traits:

1. **Outcome-focused, not feature-focused.** A skill describes what it accomplishes for the user, not its internal structure.
2. **Progressive disclosure.** Frontmatter (always loaded) → SKILL.md body (loaded when relevant) → scripts/ and references/ (loaded on demand). Keep SKILL.md under 5,000 words.
3. **Specific and actionable instructions.** "Run `python scripts/validate.py --input {file}`" beats "Validate the data before proceeding."
4. **Trigger-rich descriptions.** Include both technical terms AND problem-oriented phrasing so users who don't know the paper's name still activate the skill.
5. **Code that explains itself.** Every code block must be preceded by 1-2 sentences saying what it does and why. Long code goes in `scripts/`, not inline.

## Output Skill Specification (v0.0.2)

Every skill produced by this engine MUST conform to this spec.

### Required Folder Structure

```
skill-name/
├── SKILL.md                # Required — main skill file
├── scripts/                # Optional — executable code files
│   ├── core_algorithm.py   # E.g., the main technique implementation
│   └── utils.py            # E.g., helper functions
└── references/             # Optional — supplementary docs
    └── detailed-guide.md   # E.g., full hyperparameter sweep results
```

### Required YAML Frontmatter Fields

Every generated SKILL.md MUST include ALL of these fields:

```yaml
---
name: meaningful-kebab-case-name   # REQUIRED: descriptive kebab-case (see Naming Rules below)
title: "Actual Paper Title Here"   # REQUIRED: the full paper title as published
version: 0.0.2                     # REQUIRED: must match the engine version (currently 0.0.2)
engine: skillxiv-v0.0.2-claude-opus-4.6  # REQUIRED: fixed engine identifier
license: MIT                       # REQUIRED: always MIT
url: "https://arxiv.org/abs/XXXX.XXXXX"  # REQUIRED: verified arXiv link (must resolve, no placeholders)
keywords: [Keyword One, Keyword Two, Keyword Three, ...]  # REQUIRED: inline YAML list with square brackets
description: "Plain text description here"  # REQUIRED: see Description Rules below
---
```

### Naming Rules

The `name` field (which also becomes the folder name) MUST be a meaningful, descriptive kebab-case identifier that communicates the skill's purpose at a glance.

**Strictly prohibited:**
- Raw arXiv IDs like `2505-00212` — these are opaque numbers that tell nobody anything
- Generic names like `paper-skill` or `new-technique`
- Paper acronyms alone without context (e.g., `dash` — what is DASH?)

**Good names** — derived from the paper's core contribution:
- `dash-shampoo-optimizer` — technique name + domain
- `hazard-aware-rl-clipping` — method + application
- `sparse-attention-training` — key concept + context
- `multi-agent-failure-attribution` — problem being solved

A researcher browsing a list of skill names should immediately understand what each skill is about.

### Description Rules

The `description` field is the single most important part — it determines whether the skill gets triggered. Follow this structure:

```
[What the skill does — outcome-focused] + [When to use it — trigger conditions]
```

**Rules:**
- Under 1024 characters
- MUST include BOTH what the skill does AND when to use it
- Focus on outcomes, not features
- **Plain text only** — no XML tags (`<` or `>`), no YAML block scalars (`>` or `|`), no special markup
- Include specific tasks users might say (e.g., "stabilize PPO training", "reduce inference latency")
- Mention file types if relevant (e.g., "works with .safetensors checkpoints", "outputs ONNX models")
- Always use a double-quoted string on one line: `description: "Your text here"`
- NEVER use YAML multi-line syntax like `description: >` or `description: |` — these cause parsing issues

**Good example:**
```
description: "Stabilize reinforcement learning training for LLMs by detecting and correcting hazardous policy updates before they cause training collapse — instead of wasting GPU hours on diverged runs. Use when you want to stabilize PPO training, prevent reward hacking during RLHF, implement adaptive importance ratio clipping, or fix training instability. Also for questions about RL divergence, KL management, or making RL post-training reliable."
```

**Bad examples:**
```
# BAD: YAML block scalar — causes ">" to appear in parsed description
description: >
  Accelerate second-order optimization...

# BAD: Feature-focused, tells user nothing about outcomes
description: "A skill that implements the MHPO algorithm from arXiv:2603.16929 using hazard functions."

# BAD: Contains XML-like angle brackets
description: "Uses <attention> mechanism for <sequence> processing."
```

### URL Verification

The `url` field MUST be a verified, working arXiv link. Follow this process:

1. If the paper came from HuggingFace, check if the arXiv ID is provided. HuggingFace sometimes uses its own paper IDs — do NOT use `huggingface.co/papers/` URLs.
2. Construct the arXiv URL as `https://arxiv.org/abs/XXXX.XXXXX`.
3. **Verify the link resolves** by fetching the arXiv abstract page. If blocked, use web search with the paper title to find the correct arXiv ID.
4. NEVER use placeholder URLs like `https://arxiv.org/abs/0000.00000` or `https://arxiv.org/abs/TBD`.

### Keyword Extraction

Extract 5-10 keywords from the paper that cover:
- The technique name (e.g., "GRPO", "speculative decoding")
- The problem domain (e.g., "reinforcement learning", "image segmentation")
- Key methodological terms (e.g., "importance sampling", "knowledge distillation")
- Application areas (e.g., "LLM alignment", "robotics control")

**Format:** Use Title Case for each keyword. MUST be an inline YAML list with square brackets on one line:

```yaml
keywords: [Model Architecture, Mamba, State Space Models, SSM, Long Context, Efficient Inference]
```

**NEVER use YAML block list syntax.** The following is WRONG and will cause parsing errors:

```yaml
# WRONG — do not use this format
keywords:
  - optimization
  - second-order
  - efficiency
```

## Phase 1: Paper Selection

Not every paper makes a good skill. Score each on these five dimensions (need 3/5):

1. **Actionable technique** — Does it introduce a method someone could implement?
2. **Clear problem-solution structure** — One sentence: what problem, how solved?
3. **Generalizable** — Useful beyond the paper's specific dataset/task?
4. **Implementation-describable** — Core approach fits in under 200 lines of pseudocode?
5. **Agent-relevant** — Would an LLM agent benefit from knowing this?

### Paper Type → Skill Focus

| Paper Type | Skill Focus | Name Pattern |
|-----------|------------|--------------|
| New architecture | Implementation guide with architecture code | `technique-name-architecture` |
| Training technique | Training loop + hyperparameters + tips | `technique-name-training` |
| Evaluation/benchmark | Diagnostic framework + mitigations | `technique-name-evaluation` |
| System/infrastructure | Architecture patterns + deployment | `technique-name-system` |
| Analysis/finding | Diagnostic tools + workarounds | `problem-name-analysis` |
| Framework/pipeline | End-to-end workflow with stages | `framework-name-pipeline` |

## Phase 2: Paper Reading for Skill Extraction

### Accessing the Paper

**CRITICAL: Always read the original arXiv paper.** Do NOT generate skills from HuggingFace daily paper summaries, blog post descriptions, or third-party abstracts. The skill must be grounded in the actual paper content.

Prefer these access methods in order:

1. **arXiv HTML version** (`https://arxiv.org/html/XXXX.XXXXX`) — the best source: full paper content in readable HTML. Try this first by constructing the URL from the arXiv ID.
2. **arXiv abstract page** (`https://arxiv.org/abs/XXXX.XXXXX`) — metadata, abstract, and links
3. **arXiv PDF** (`https://arxiv.org/pdf/XXXX.XXXXX`) — use if the HTML version is not available (not all papers have one)
4. **GitHub repo** — if linked in the paper, skim README and core implementation for additional context

**Note:** The HTML version is available for most recent papers but not all. If `https://arxiv.org/html/XXXX.XXXXX` returns a 404, fall back to the PDF or abstract page. When all URLs are blocked, use web search with the paper title to find the content.

**Never rely on:** HuggingFace paper page summaries, Twitter/X threads, blog posts, or any secondary source as the primary input for skill extraction. These are acceptable for discovery/triage only.

### Four-Pass Reading Strategy

**Pass 1 — Abstract + Figures (2 min):** Get the one-sentence contribution. Look at the architecture diagram. Is there a clear technique?

**Pass 2 — Method Section (5 min):** Extract the core algorithm/pipeline, key equations (translate to code, not LaTeX), architecture components, input/output specs.

**Pass 3 — Experiments (3 min):** Mine for hyperparameter values, ablation insights (which components matter), failure cases, comparison baselines.

**Pass 4 — Related Work (1 min):** Understand what this replaces. Informs the "Why This Approach" section.

### Extraction Template

Fill this in before writing:

```
PAPER: [title]
ARXIV: [verified arXiv ID, e.g., 2603.19199]
URL: [full verified arXiv URL]
ONE-LINE: [what it does in plain English]
PROBLEM: [what existing approaches get wrong]
CORE TECHNIQUE: [the key innovation in 2-3 sentences]
ARCHITECTURE: [components and how they connect]
KEY ALGORITHM: [pseudocode or step-by-step]
HYPERPARAMETERS: [what values work, from experiments]
ABLATION INSIGHTS: [what matters, what doesn't]
FAILURE MODES: [when/why it breaks]
PRACTICAL APPLICATIONS: [real-world use cases]
CODE AVAILABLE: [yes/no, URL if yes]
KEYWORDS: [5-10 extracted keywords for the frontmatter]
```

## Phase 3: Writing the Skill

### SKILL.md Body Template

Follow this canonical structure for every generated skill. The template below uses escaped fences for illustration — in actual output, use real markdown fences with language labels.

**Title section:**

```
# [Technique Name]: [One-line outcome — what it lets you DO]
```

Then 1-2 paragraphs grounding the problem in practical terms, not academic framing.

**Core Concept section:** The key idea in plain language. What makes this different. The "aha" the reader needs.

**Architecture Overview section:** Summarize the system's components and data flow in plain text. Use bullet points or numbered lists — NOT ASCII art diagrams. ASCII diagrams are hard for other agents to parse and add no value over a clear textual description.

Good example:
- **Input:** Raw training data (text corpus or instruction dataset)
- **Stage 1 — Reward Model:** Scores candidate outputs using a learned preference function
- **Stage 2 — Policy Optimizer:** Updates the language model weights using PPO with the reward signal
- **Feedback loop:** KL divergence constraint prevents the policy from drifting too far from the reference model
- **Output:** Fine-tuned model with aligned behavior

Bad example (do NOT do this):
```
Input → Reward Model → Policy Optimizer → Output
              ↓
         KL Constraint (feedback)
```

**Implementation section:** This is the bulk of the skill. Break into numbered steps, each with:

1. A step heading: `### Step 1: [Component Name] — [What it does]`
2. 1-2 sentences explaining WHY this component exists
3. A code block (language-labeled, 10-40 lines, showing the NOVEL part)
4. If code exceeds ~40 lines, reference a `scripts/` file instead

Example of a well-structured implementation step:

```python
# Computes adaptive clipping ratio based on hazard function.
# Standard PPO uses a fixed clip threshold (typically 0.2), which causes
# sudden gradient loss. This smoothly attenuates large importance ratios.
class HazardClip:
    def __init__(self, base_clip: float = 0.2, hazard_scale: float = 1.0):
        """base_clip: starting threshold; hazard_scale: sensitivity to divergence."""
        self.base_clip = base_clip
        self.hazard_scale = hazard_scale

    def compute_clip(self, importance_ratio: torch.Tensor) -> torch.Tensor:
        hazard = self.hazard_scale * torch.log1p(torch.abs(importance_ratio - 1.0))
        adaptive_clip = self.base_clip * torch.exp(-hazard)
        return adaptive_clip
```

**Practical Guidance section:** Include a hyperparameter table, "When to Use This", "When NOT to Use This", and "Common Pitfalls" subsections.

**Reference section:** Always include the arXiv paper link on its own line using the format below. Optionally add code repo URL on a second line.

```
Paper: https://arxiv.org/abs/XXXX.XXXXX
Code: [GitHub URL if available]
```

### Code Handling Rules

These are critical — the most common flaw in extracted skills is poorly handled code.

**Rule 1: Every code block must be explained.**
Before each code block, write 1-2 sentences stating: (a) what the code does, and (b) why it's needed. Never dump a code block without context.

**Rule 2: Label the coding language.**
Always specify the language in the markdown fence: ` ```python `, ` ```bash `, ` ```yaml `, etc. Never use bare ` ``` `.

**Rule 3: Keep inline code concise and core.**
Each inline code block in SKILL.md should be 10-40 lines max. It should show the NOVEL part of the technique — not boilerplate like imports, logging setup, or argument parsing.

**Rule 4: Long code goes in `scripts/`.**
If a complete implementation exceeds ~50 lines, create a `scripts/` file:

```
scripts/
├── core_algorithm.py     # The main technique (with docstrings + inline comments)
├── training_loop.py      # Full training script if applicable
└── evaluate.py           # Evaluation/diagnostic script if applicable
```

Reference it from SKILL.md like this:

> Complete training script with all components integrated: see `scripts/training_loop.py`

**Rule 5: Be specific about what each code block does.**
Follow the pattern from Orchestra-Research skills — each code section has a clear purpose label:

```python
"""Step 1: Initialize the reward model with hazard-aware loss.
This replaces standard cross-entropy with a survival-analysis loss
that penalizes catastrophic policy updates more heavily."""
```

### Writing Style

1. **Lead with "why", not "what".** Instead of "This section describes the modulator," write "Standard PPO clips ratios with a hard threshold, causing sudden gradient loss. The modulator smoothly attenuates instead."

2. **Engineering docs, not paper abstracts.** Replace "We propose a novel framework" with "This technique replaces X with Y because..."

3. **Assume domain basics, explain what's new.** A skill about SAMA doesn't explain diffusion from scratch.

4. **Include hyperparameter tables.** Practitioners need concrete numbers from experiments.

5. **Always include "When NOT to use" guidance.** Every technique has boundaries.

### Content Quality: What Is Actually Useful

Ask yourself: "What is really useful about this research that can benefit future research and practitioners?" The skill should NOT be a mechanical template-filling exercise. It should distill genuine insight.

**Do:**
- Extract the core algorithmic insight that makes this paper's contribution novel
- Include concrete experimental findings (what worked, what didn't, specific numbers from ablations)
- Describe real failure modes and limitations the authors discovered
- Provide practical integration guidance — how would someone actually use this in their own work?
- Highlight connections to related techniques and when to prefer one over another

**Do NOT:**
- Fill in placeholder text like "Use case 1", "key_param_1", "Description and how to avoid" — if you don't have real content from the paper, leave the section out entirely
- Generate stub code with empty `pass` statements — either show real implementation logic or omit the code block
- Copy boilerplate section structures without substantive content
- Create ASCII art or box-and-arrow diagrams — use plain text bullet points instead
- Paraphrase the abstract as the entire skill — the skill must go deeper than the abstract

## Phase 4: Quality Validation

### The 5-Point Quality Check

Run these checks on every generated skill:

1. **Standalone test:** Read only the skill (not the paper). Can you understand what to implement?
2. **Code review:** Would the code blocks run? Any undefined variables or type mismatches? Are all code blocks language-labeled?
3. **Trigger test:** Does the description trigger for 5+ phrasings of the core use case?
4. **Depth check:** Does the skill tell you something beyond a 2-sentence summary?
5. **Practitioner test:** Does it help someone USE the technique? (Implementation steps, hyperparameters, failure modes, decision criteria.)

### Frontmatter Validation Checklist

- [ ] `name`: meaningful descriptive kebab-case (NOT raw arXiv IDs like `2505-00212`), matches folder name
- [ ] `title`: actual paper title as published
- [ ] `version`: set to `0.0.2` (must match the engine version)
- [ ] `engine`: set to `skillxiv-v0.0.2-claude-opus-4.6`
- [ ] `license`: set to `MIT`
- [ ] `url`: verified arXiv link that resolves (not a placeholder)
- [ ] `keywords`: 5-10 keywords, formatted as inline list `[A, B, C]` (NOT YAML block list syntax)
- [ ] `description`: under 1024 chars, plain text only (no `<` `>` tags, no YAML `>` or `|` scalars), outcome-focused, includes specific trigger tasks users might say, mentions file types if relevant

### Code Quality Checklist

- [ ] Every code block has 1-2 sentences of context before it
- [ ] Every code fence specifies a language (` ```python `, not ` ``` `)
- [ ] No inline code block exceeds ~40 lines
- [ ] Long implementations live in `scripts/` with references from SKILL.md
- [ ] Code shows the NOVEL parts, not boilerplate
- [ ] Scripts in `scripts/` have docstrings explaining their purpose

## Batch Processing Pipeline

When converting multiple papers at once (e.g., from a date range of arXiv submissions):

### Step 1: Triage (5 min for 20-30 papers)
- Read titles and abstracts from arXiv
- Discard papers failing the convertibility checklist
- Rank by impact and skill diversity

### Step 2: Paper Reading
- For each selected paper, fetch the arXiv HTML version (`https://arxiv.org/html/XXXX.XXXXX`) first; fall back to PDF if HTML is unavailable
- Fill extraction template for each paper from the **original arXiv content** (not HuggingFace summaries or other secondary sources)
- **Verify arXiv URLs for all selected papers**
- Final selection: typically 5-15 papers

### Step 3: Batch Writing
- Write in order of most to least familiar domain
- Reuse structural patterns across similar paper types
- Maintain consistent section naming and code style

### Step 4: Cross-Skill Review
- Check for redundancy across skills
- Verify trigger descriptions don't overlap excessively
- Ensure diverse domain coverage
- Validate all frontmatter fields against the checklist

## Common Mistakes to Avoid

1. **Raw arXiv IDs as names** — `2505-00212` is meaningless. Use descriptive kebab-case names like `multi-agent-failure-attribution`.

2. **YAML block scalar descriptions** — Using `description: >` causes a literal `>` character to appear in parsed output. Always use a double-quoted string on one line: `description: "Your text here"`.

3. **YAML block list keywords** — Using indented `- keyword` syntax instead of inline `[A, B, C]` format breaks parsing. Always use: `keywords: [Keyword One, Keyword Two]`.

4. **ASCII art architecture diagrams** — Box-and-arrow diagrams are hard for agents to parse. Use bullet-point text descriptions of components and data flow instead.

5. **Generating from secondary sources** — Never write a skill from a HuggingFace summary, blog post, or tweet. Always read the actual arXiv paper (preferably the HTML version).

6. **Stub/placeholder content** — Never output "Use case 1", "key_param_1", or code blocks with empty `pass` statements. If you don't have real content from the paper, omit the section.

7. **Code dumps without narrative** — Every code block needs preceding explanation. A skill with unexplained code is as useless as one with no code at all.

8. **Unlabeled code fences** — Always specify ` ```python `, ` ```bash `, etc. Never bare ` ``` `.

9. **Feature-focused descriptions** — "Implements the XYZ algorithm using hazard functions" tells the user nothing about outcomes. Write "Prevents RL training collapse by detecting dangerous policy updates before they happen."

10. **Descriptions with XML/angle brackets** — Never use `<` or `>` in the description field. Plain text only.

11. **Academic voice** — "We propose" → "This technique replaces". Engineering docs, not paper prose.

12. **Missing "when NOT to use"** — Every technique has boundaries. A skill without limitations will be misapplied.

13. **Inline code too long** — If a code block exceeds ~40 lines, move it to `scripts/` and reference the path.

## Reference

Informed by Anthropic's Complete Guide to Building Skills for Claude and the Orchestra-Research AI-Research-SKILLs repository (github.com/Orchestra-Research/AI-Research-SKILLs) structure patterns. Skills must always be extracted from original arXiv papers, not secondary sources.
