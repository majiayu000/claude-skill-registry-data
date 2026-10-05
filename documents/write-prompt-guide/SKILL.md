---
name: write-prompt-guide
description: Produce a pack-specific PROMPT_GUIDE.md that teaches end users what to type to get a good run out of one Agent Skill pack, from that pack's own SKILL.md, README, and open issues. Use when a skill pack has agent-facing docs but nothing telling a human how to invoke it well.
---

# Write a Prompt Guide

A skill pack's `SKILL.md` tells an **agent** what to do. Its `README.md` tells a reader what the pack **is**. Neither tells a **user** what to type, what context to hand over before the run starts, or which of the pack's known limitations they have to compensate for by hand. That gap is what this skill fills, for one named target pack at a time.

This is not a prompt-engineering tutorial. A generic "be specific, give examples" page helps nobody who already installed the pack. The deliverable is specific to one pack: its real inputs, its real invocation triggers, its real output shape, and its real open bugs.

## Evidence basis

The structure below is not invented. It is the intersection of the official prompting documentation of four model/agent providers — Anthropic, OpenAI, Google, and BytePlus — recorded with URLs and per-claim attribution in this repo's [`SOURCES.md`](../../../SOURCES.md) (`ANTHROPIC-PROMPTING-01`, `OPENAI-PROMPTING-01`, `GOOGLE-PROMPTING-01`, `BYTEPLUS-PROMPTING-01`).

Two techniques appear in all four independently and a third in two of them independently, which is why these three are the non-negotiable spine of every guide this skill produces:

1. **Structural separation of instructions, context, examples, and input** — Anthropic via XML tags (`<instructions>`, `<context>`, `<input>`), OpenAI and BytePlus via the same four Markdown sections (`# Identity`, `# Instructions`, `# Examples`, `# Context`), Google via "XML tags or Markdown". Four sources, one technique.
2. **Few-shot examples** — Anthropic asks for 3–5, relevant and diverse, wrapped in `<example>`/`<examples>`; OpenAI calls it "a handful of input/output examples"; BytePlus's general-task template requires at least two worked Question/Output pairs; Google contrasts zero-shot with few-shot.
3. **Match instruction precision to the model's reasoning mode** — OpenAI: reasoning models want high-level goals, GPT models want "precise instructions that explicitly provide the logic and data required"; BytePlus draws the same line between deep-thinking and non-deep-thinking models. Two independent sources, identical principle.

Anthropic supplies the remaining spine pieces from Claude's specific angle: explain *why* a constraint matters rather than only stating it, set a role in one sentence, put long/stable material near the top and the query at the end, and — for agentic runs — track state explicitly and chain complex work into steps. Google adds the iteration moves (rephrase, reorder, decompose or chain) and explicit constraints covering both what to do and what not to do. BytePlus adds the discipline that comes before any of it: define success criteria first, then iterate Update → Test → Debug → Evaluate, versioning as you go.

Two items in the source material are **API-level and do not apply** to a user typing at a Claude Agent Skill in chat, and a guide should say so rather than silently importing them: generation-parameter tuning (temperature/topK/topP, Google) and prompt-caching placement (OpenAI) — the user does not control either from a chat turn. RAG/file-search wiring (OpenAI) is likewise out of scope unless the target pack itself takes file inputs.

## Workflow

### 1. Read the target pack, do not assume it

Work from the live repo, not memory. For the target pack, extract:

- **What it actually does** — from each `SKILL.md`'s `description` frontmatter and workflow steps, not from the README's marketing sentence.
- **Its inputs** — what the user must supply (a URL, a repo, a file, a tier of access, pasted transcripts) and what is optional.
- **Its invocation triggers** — the `description` field is what makes an agent auto-load the skill; a good prompt echoes that vocabulary. Note the trigger words.
- **Its output shape** — sections, scoring model, report template. Users prompt better when they know what they are going to get.
- **Orchestrator vs. specialist structure** — if one skill delegates to others, the guide must say which single skill to name and let it fan out, instead of listing fourteen skills a user has to pick between.
- **Known gotchas** — read the target repo's **open issues and open PRs**: `gh issue list --repo <owner>/<repo> --state open` and `gh pr list --repo <owner>/<repo> --state open`. A false-negative bug, a scope limitation, an unmerged fix — each is something a user must know to double-check by hand. This step is mandatory; a guide that documents only the happy path is the failure mode this skill exists to prevent.

### 2. Fill the general-task template, adapted to invoking a skill

BytePlus's general-scenario template is `{role}`, `{context}`, `{task}`, numbered rules, at least two worked examples, explicit output-format requirements. Adapt each slot to a chat invocation rather than an API call:

| Template slot | What it becomes in a skill invocation |
|---|---|
| role | Usually unnecessary — the pack's `SKILL.md` already sets the role. Recommend one only where the pack serves multiple audiences (e.g. "report for a non-technical client"). |
| context | The facts the pack cannot discover on its own: the target, the business model, what access the user already has, what was already tried. |
| task | Name the skill or echo its trigger vocabulary, plus the scope boundary (one page vs. whole site, which tier). |
| rules | Numbered constraints, each with its reason attached — the *why* is what generalizes (Anthropic). |
| examples | The good vs. less-effective pairs of §3, not examples of the pack's output. |
| output format | The deliverable the user wants: report template, file path, ticket list, PDF. |

### 3. Write `PROMPT_GUIDE.md` with exactly these sections

1. **Quick start** — the shortest prompt that reliably gets a good run. One line, copy-pasteable, in a fenced block. If the pack has an orchestrator, the quick start names the orchestrator.
2. **Giving useful context** — a table or list of what to supply and *why each one changes the run*: the target, the scope, access already granted, the audience for the output, constraints. Anthropic's rule applies to the guide itself: state the reason, not only the requirement.
3. **Structuring a complex or multi-phase request** — show one worked multi-phase prompt using either Markdown sections (`# Identity` / `# Instructions` / `# Examples` / `# Context`) or XML tags (`<context>`, `<task>`, `<constraints>`, `<output_format>`). Say plainly that the two are interchangeable here and that consistency within one prompt matters more than the choice. Include the long-context placement rule: stable/bulk material first, the actual ask last.
4. **Good vs. less-effective prompt examples** — **at least two pairs**, in Anthropic's "Less effective / More effective" shape, each pair followed by one sentence naming *what specifically changed and what it buys*. Pairs must be drawn from real ways this pack gets under-prompted, not generic ones.
5. **Known limitations to mention explicitly** — every item traced to a real, linked issue or PR on the target repo, with its current state stated accurately (open issue, merged fix, fix pending in an unmerged PR — these are different things and must not be blurred). Each item says what the user should verify manually as a result.
6. **Where to go deeper** — links to the pack's own `SKILL.md`, `README.md`, and any existing docs (running/installation guides, example-prompt catalogues). Do not restate what those files already cover; point at them.

### 4. Add a structural check where the target repo supports one

If the target repo has a deterministic eval or docs-validation layer, add a check that the guide has all six sections and that every capability it names exists in the target pack. Where it does not, the guide still ships — but say so rather than implying it is validated.

## Guardrails

- **Never describe a capability the target pack does not have.** Every feature, flag, input, and output section named in the guide must trace to a line in the pack's own `SKILL.md`/`README.md`. This is the single highest-value failure to prevent: a prompt guide is read as authoritative and a fabricated capability sends users to type prompts that quietly do nothing.
- **Never present an unmerged fix as shipped.** "Fixed in PR #104" and "fixed" are different claims. State the branch/PR status as it actually is on the day of writing, and date the statement.
- **Do not soften the limitations section to make the pack look better.** Its whole purpose is telling a user what to double-check by hand.
- **Do not turn the guide into a prompt-engineering tutorial.** If a paragraph would be equally true of any pack, cut it or replace it with the pack-specific version.
- **Do not duplicate an existing doc.** If the repo already has an example-prompts catalogue or an installation guide, cross-link; a second drifting copy is worse than none.
- **Cite the methodology, do not paraphrase it as folklore.** Claims about what makes a prompt effective belong to the four provider sources in `SOURCES.md`; do not invent additional "best practices" without a source.

## Distinguish from neighbouring skills

`write-a-skill` authors the pack's agent-facing instructions. `skills-marketplace-readiness` prepares a pack for discovery and installation. This skill covers the layer after both: the pack exists and is installed, and a human now has to prompt it well.
