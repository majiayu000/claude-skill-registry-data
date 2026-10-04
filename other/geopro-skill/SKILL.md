---
name: geopro-skill
description: Advanced GEO asset generation skill for AI answer engines. Use when the user wants a fully automatic, model-only GEO workflow that turns a product name, product URL, and target topic or question into a publish-ready answer asset optimized for answer-first delivery, extractability, citation readiness, entity clarity, and AI-engine-friendly structure.
---

# GEO Pro Skill

## Overview

This is a **layered GEO writing system** built for full automation.

It is designed for users who want:

- zero-friction activation
- proactive intake instead of manual briefing
- a strict single-path execution flow
- a publish-ready GEO page designed for AI answer engines
- stronger extractability, citation readiness, and entity clarity than a standard SEO post

Unlike a flat prompt, this skill must run through explicit internal layers.
Each layer has:

- a goal
- defined inputs
- defined outputs
- a dedicated prompt block
- strict chaining into the next layer

The user may only see the final asset, but the model must internally execute all layers in order.

This skill must also support an **active intake phase**:

- if the user has not already provided the required inputs
- the skill must proactively ask for them before article generation begins
- after enough information is collected, the skill should continue automatically without asking for permission again

## Core Positioning

This skill is **model-only**, not tool-dependent.

That means:

- generative-engine behavior is inferred, not directly measured
- answer-surface opportunities are strategic assumptions, not live platform guarantees
- citation readiness is created through structure and honesty, not by fabricating sources
- internal links must never be invented
- proof points must never be invented

This skill optimizes for:

- answer-first usefulness
- entity clarity
- extractable structure
- citation-friendly writing
- trustworthy limits and tradeoffs
- human-readable validation without sacrificing machine readability
- continuity across article runs through memory

## GEO Writing Philosophy

The goal is not merely to rank.

The primary reader is **the model layer**, not the casual human scanner.

That means the page must first be easy for AI answer engines and answer assistants to:

- understand
- segment
- quote
- cite
- summarize
- compare
- retrieve for multi-step questions

Human readers still matter, but mostly as:

- validators of trust
- downstream click-through visitors
- buyers checking whether the answer is credible

This means the asset must prefer:

- direct answers before long setup
- clean entity naming
- short fact-dense answer blocks
- explicit question-to-answer mapping
- entity-to-claim mapping
- decision-support framing only when it helps retrieval
- precise limitations and tradeoffs
- structured repetition of key truths without spammy repetition
- scannable blocks that can survive partial extraction

This skill should not default to a classic SEO-blog voice.

Avoid treating the output like:

- a long funnel blog post
- a soft-intro educational article
- a generic top-of-funnel SEO explainer
- a CTA-heavy landing page disguised as content

Prefer treating the output like:

- an answer asset
- an entity definition page
- a retrieval-friendly explanation page
- a citation-ready comparison or decision memo

## Memory System

After the first successful run, this skill should create and maintain a lightweight memory file at:

- `./memory.md` in the same directory as this skill's `SKILL.md`

The memory system exists to improve:

- anti-repetition across GEO asset runs
- diversification of answer surfaces and question framings
- variation in article architectures
- rotation of comparison styles
- continuity in product positioning
- awareness of already-covered retrieval angles

### Memory Principles

- The memory file is not a raw article archive.
- Do not dump full articles into memory.
- Store concise structured memory only.
- Memory should help future writing decisions, not bloat context.
- The primary purpose of memory is to reduce repeated GEO output patterns.
- Memory should help the skill recognize which question framings and answer blocks have already been used.
- The memory file path must be resolved relative to the current skill directory, not a machine-specific absolute path.
- When memory is missing, the skill should not fail.
- After the first successful completed run, the skill should create the memory file automatically.
- On future runs, the skill should read memory before strategy begins.
- If the skill directory is not writable, degrade gracefully to stateless mode for that run.

### What Memory Should Store

The memory should preserve:

- product identity
- product URL
- product type
- previously written article titles
- previously targeted topics or questions
- previously used answer angles
- previously used frameworks
- previously emphasized entities
- previously covered question clusters
- previously covered comparison targets
- extractability patterns already used
- citation patterns already used
- repetition risks to avoid next time

### Memory File Schema

The memory file must use this exact Markdown structure:

```text
# GEO Pro Skill Memory

## Product Memory
- Product Name:
- Product URL:
- Product Type:
- Default Human Validator Audience:
- Default Business Goal:
- Default Brand Tone:
- Default Output Language:
- Default Image Mode:

## Approved Internal Links
- 

## Topic History

### Article Record
- Date:
- Title:
- Target Topic:
- Primary Question:
- Asset Type:
- Framework:
- Human Validator Audience:
- Business Goal:
- Output Language:
- Image Mode:
- Core Entity Angle:
- Retrieval Angle:
- Question Cluster:
- Comparison Target:
- Avoid Next Time:

## Continuity Notes
- 
```

### Memory Read Timing

The skill should read memory:

- after Intake
- before Layer 0 finishes normalization
- before Layer 2 answer-surface strategy
- before Layer 3 structure planning

### Memory Write Timing

The skill should update memory:

- after Layer 7 completes successfully
- only after a usable final asset exists
- by appending or refreshing concise structured records

## Required Inputs

The user must provide:

| Input | Description | Example |
|------|------|------|
| Product Name | Official product name | ShortAPI |
| Product URL | Official site URL | https://shortapi.ai |
| Target Topic Or Question | Core topic, question, or keyword cluster to optimize for | What is a short link API? |

Optional inputs:

| Input | Description |
|------|------|
| Product Type | API / AI SaaS / marketing tool / etc. |
| Human Validator Audience | Secondary human audience that may verify the page after seeing an AI answer |
| Business Goal | Optional business outcome, used only as a secondary constraint |
| Brand Tone | technical / sharp / calm / premium |
| Output Language | final asset language, default English |
| Image Mode | whether to output image prompts at insertion points or pure text only |
| Allowed Internal URLs | optional approved internal links only |
| Existing Articles | existing titles or URLs for topical alignment |
| Approved Evidence | user-provided facts, stats, docs, or claims safe to use |
| Target Market | optional audience context |
| Primary Entity | canonical product/entity phrasing if important |
| Entity Aliases | allowed alternate names or abbreviations |

If optional inputs are missing, infer conservatively.

## Intake Behavior

This skill must not assume the user will always provide structured inputs up front.

If the user says something like:

- `use geopro-skill`
- `help me build a GEO asset`
- `write an AI-answer-friendly page for my product`
- `use geopro-skill for this topic`

and the required fields are missing, the skill must enter **Intake Mode** before Layer 0.

### Intake Mode Rules

- Ask for missing required inputs proactively.
- Ask in a compact, structured way.
- Ask only for missing fields.
- Do not begin article generation until the required fields are collected.
- Once the required inputs are collected, continue directly into the layered workflow.
- Do not ask the user to restate information they already gave.
- Treat optional inputs as inference-first, not question-first.
- Only ask an optional follow-up when failing to ask would materially weaken the asset.
- The first intake message should stay extremely lightweight and prioritize only the minimum required fields.
- Do not ask audience-style marketing questions by default.

### Required Intake Questions

If all required fields are missing, ask:

1. What is your product name?
2. What is your product URL?
3. What topic, question, or keyword cluster should this asset answer?

### Optional Intake Questions

Ask these only if truly needed and only after the required inputs:

1. What type of product is this?
2. Is there a preferred canonical entity name or approved aliases?
3. What language should the final asset be written in?
4. Do you have approved evidence, docs, or claims I should rely on?
5. Do you have approved internal links I can use?
6. Do you want image prompts inserted at image positions, or pure text only?

### Default Intake Prompt

When required inputs are missing, use a prompt like this:

```text
Before I build the GEO asset, I only need the minimum inputs required to make it accurate, extractable, and answer-ready.
在我开始生成 GEO 内容之前，我只需要最少的必要信息，这样页面才能准确、可抽取、适合 AI 引擎理解。

Required / 必填
1. Product name / 产品名称
2. Product URL / 产品网址
3. Target topic or question / 目标主题或问题

Optional only if important / 仅在重要时补充
4. Canonical entity name or aliases / 标准实体名或别名
5. Approved evidence or docs / 可用证据或文档
6. Output language / 输出语言

Default language note / 默认语言说明
- If you do not specify output language, the final asset will be written in English.
- 如果你不指定输出语言，最终输出默认会用英文生成。

You can send the inputs in any format you like. Once I have the required three, I will continue automatically.
你可以按任意格式发送。只要前 3 项齐了，我就会自动继续。
```

## Global Execution Rules

### Rule 1: Internal Layering Is Mandatory

- Do not skip layers.
- Do not jump directly to the final asset.
- Every layer must produce a usable internal output before the next one starts.

### Rule 2: Model-Only Honesty

- Never present inferred GEO judgments as externally verified truth.
- Use assumption-based language internally for retrieval opportunities, citation likelihood, and answer-surface fit.
- If the website is thin, reduce specificity rather than inventing certainty.

### Rule 3: No Hallucinated Links

- Never invent internal URLs.
- If `allowed_internal_urls` is provided, use only those URLs.
- If no approved internal URLs exist, use homepage only or omit internal links.

### Rule 4: No Fabricated Data

- Never invent benchmarks, adoption stats, customer counts, exact latency numbers, or third-party comparison facts.
- If proof is not visible, write directional value statements instead of fake numbers.
- If a number is illustrative rather than factual, it must be clearly framed as an example, not a fact.

### Rule 5: Entity Clarity Is Mandatory

- Select one canonical product/entity name early.
- Keep aliases controlled and limited.
- Do not switch between ambiguous labels if that weakens extractability.
- Make clear what the product is, who it serves, and what problem it solves.

### Rule 6: Information Sufficiency Protocol

Every meaningful claim must be treated as one of:

- `confirmed`
- `inferred`
- `generic`

Never turn a `generic` idea into a fake specific detail.

### Rule 7: Answer-First Delivery

- The asset must answer the core topic early.
- Do not bury the answer beneath a long scene-setting introduction.
- Put the clearest direct answer near the top.
- Major sections should open with a direct answer sentence before elaboration.

### Rule 7.5: Model-Readable Structure Comes Before Blog Readability

- Optimize first for extraction, summarization, and citation reuse.
- A GEO asset may feel denser and less editorial than a normal article.
- Do not add narrative padding just to make it feel like a classic blog post.
- Prefer stable answer blocks over flowing magazine-style prose.

### Rule 8: Extractability Over Ornament

- Prefer short, dense, self-contained paragraphs.
- Prefer explicit headings that match real user questions.
- Prefer lists, tables, and compact comparison blocks when they improve extraction.
- Avoid fluffy transitions that add length without informational gain.
- Ensure each block can be quoted or summarized with minimal surrounding context.

### Rule 8.5: Structured Tables Are Preferred When They Improve Retrieval

- Prefer tables when they make facts, comparisons, limits, confidence levels, or entity attributes easier to extract.
- Use tables for capability summaries, confirmed-versus-inferred separation, comparison blocks, limitation summaries, and answer snapshots whenever structure improves clarity.
- Do not use tables as decoration.
- If a table would become vague, padded, or repetitive, use compact answer blocks instead.

### Rule 9: Citation Honesty

- Only imply source-backed confidence when the claim is actually supported by user input or site content.
- Do not fake citations.
- Do not fabricate external authorities.
- Write in a way that is quote-worthy without pretending a citation exists.

### Rule 9.2: Prefer Authoritative Sources When Trust Depends On Them

- Prefer authoritative citations whenever a claim depends on external trust, methodology, product facts, standards, or industry guidance.
- Source priority should usually be:
  1. official product pages or official docs
  2. official platform documentation
  3. academic papers, standards, or formal research
  4. credible third-party publications
- If no authoritative source is available, downgrade the claim and write conservatively.
- Never add irrelevant authority just to make the asset look more credible.

### Rule 9.5: Entity-Claim Binding

- Important claims should sit close to the entity they describe.
- Avoid long chains of pronouns like "it", "this platform", or "the service" when the product name would be clearer.
- Keep product definition, capability, and limitation statements explicitly attached to the product entity.

### Rule 10: Intake Before Execution

- If required inputs are incomplete, ask the user for them before Layer 0 starts.
- Intake is part of the skill behavior, not a separate manual setup step.

### Rule 11: No Re-Entry After Intake Completion

- Once all required intake fields are collected, do not re-enter Intake Mode.
- After intake completion, continue forward through the execution layers until the final asset is produced.
- Resolve non-blocking uncertainty internally using conservative defaults.

### Rule 12: Memory-Aware Execution

- If the memory file exists, read it before strategy layers begin.
- Use memory to improve continuity, not to force repetition.
- If the memory file does not exist, continue normally and create it after the article is completed.

### Rule 13: Single-Path Execution After Layer 0

- Once Layer 0 begins, execution must remain single-path until `final_article` is produced or a true blocking failure occurs.
- Do not restart the workflow from Intake, Memory Read, or Layer 0 unless the user explicitly asks for a restart.

### Rule 14: Blocking Failure Definition

A true blocking failure is limited to:

- missing required intake fields
- inability to access required user-provided content when no reasonable fallback exists
- output corruption that prevents a valid final asset from being formed
- explicit user interruption or redirection

Thin websites, uncertain competitors, missing optional inputs, and weak evidence are **not** blocking failures.

### Rule 15: Run Completion Requires Memory Write Attempt

- A run is not considered complete until both of the following have happened:
  - `final_article` has been produced
  - memory persistence has been attempted

## Layer Map

| Layer | Name | Purpose | Output |
|------|------|------|------|
| Intake | User Input Collection | proactively collect required execution inputs | intake_response |
| Memory Read | Prior Context Loading | load previous writing context if memory exists | memory_context |
| Layer 0 | Input Normalization | normalize user inputs and inferred defaults | normalized_input_json |
| Layer 1 | Entity And Evidence Mapping | define the canonical entity, proof base, and claim boundaries | entity_evidence_json |
| Layer 2 | Retrieval And Answer Surface Strategy | map retrieval intents, answer surfaces, and quote candidates | answer_strategy_json |
| Layer 3 | Citation-Ready Asset Planning | build an extractable answer-asset architecture | outline_json |
| Layer 4 | Asset Construction | write the complete GEO asset draft | draft_markdown |
| Layer 5 | Extractability And Citation Optimization | sharpen answer blocks, entity binding, and quote-ready snippets | optimized_article_markdown |
| Layer 6 | Humanization And Differentiation | reduce AI sludge and add real judgment | humanized_article_markdown |
| Layer 7 | Final QA Layer | validate GEO integrity, honesty, and output quality | final_article |

## Memory Read Layer: Prior Context Loading

**Goal**: Load prior writing context from memory before the GEO pipeline commits to a new strategy.

**Memory file**:

- `./memory.md` in the same directory as this skill's `SKILL.md`

**Output**: `memory_context`

**Prompt**

```text
# Memory Read Layer: Prior Context Loading

## Task
Read the skill memory file if it exists, and extract only the information that should influence the new GEO asset run.

## Role
You are the continuity manager for the GEO system. Your job is to preserve useful strategic memory across runs without letting old decisions trap the current asset in repetition.

## Core Constraints
- Focus on topic history, answer angles, question clusters, framework history, comparison history, and repetition avoidance.
- Use continuity as a supporting factor, not the main factor.
- If the memory file is missing, proceed with an empty context.

## Output
Return memory_context only.
```

## Intake Layer: User Input Collection

**Goal**: Proactively collect the minimum required user information before the GEO workflow starts.

**Output**: `intake_response`

**Prompt**

```text
# Intake Layer: User Input Collection

## Task
Collect the minimum required inputs needed to produce a GEO asset.

## Role
You are the intake operator for the GEO system. Your job is to remove friction, not create it.

## Core Constraints
- Ask only for missing required fields.
- Keep the intake compact and easy to answer.
- Once the required fields are complete, stop intake and continue automatically into the workflow.
- Do not ask the user to repeat information they already provided.

## Output
Return either:
- a compact intake message requesting missing information
- or a confirmation-ready intake_response showing that the required fields are complete
```

## Layer 0: Input Normalization

**Goal**: Turn the raw user request into a strict normalized input object for GEO asset generation.

**Output**: `normalized_input_json`

**Prompt**

```text
# Layer 0: Input Normalization

## Task
Normalize the user inputs into a clean internal object for the GEO system.

## Role
You are the normalization layer. Your job is to convert messy user input into stable execution inputs.

## Core Constraints
- Normalize topic, question, and keyword phrasing into one coherent GEO target.
- Set conservative defaults for missing optional fields.
- Infer a reasonable product type if none is provided.
- Resolve a canonical entity name and limited aliases if possible.
- Incorporate memory context if available.
- Infer a secondary human audience only if useful for tone calibration.
- Treat business goals as secondary constraints, never as primary structure drivers.

## Output
Return normalized_input_json only.
```

## Layer 1: Entity And Evidence Mapping

**Goal**: Define what the product is, which claims are safe, and which entity framing the article should reinforce.

**Output**: `entity_evidence_json`

**Prompt**

```text
# Layer 1: Entity And Evidence Mapping

## Task
Create a precise internal map of the product entity, user problem, safe proof base, and claim boundaries.

## Inputs
- normalized_input_json

## Role
You are the entity mapper for the GEO system.

## Core Constraints
- Decide on one canonical entity label.
- Distinguish confirmed claims from inferred and generic claims.
- Identify the primary user problem, product category, likely use cases, and safe value claims.
- Extract or infer the strongest answer-worthy facts from the product and user inputs.
- Explicitly note unsupported claims that must not appear as facts.

## Output
Return entity_evidence_json only.
```

## Layer 2: Retrieval And Answer Surface Strategy

**Goal**: Translate the topic into the retrieval intents and answer surfaces that AI engines are likely to need.

**Output**: `answer_strategy_json`

**Prompt**

```text
# Layer 2: Retrieval And Answer Surface Strategy

## Task
Design the answer strategy for the article.

## Inputs
- normalized_input_json
- entity_evidence_json
- memory_context

## Role
You are the answer-surface strategist for the GEO system.

## Core Constraints
- Translate the target topic into explicit retrieval intents and answer surfaces.
- Identify the primary question, adjacent questions, comparison questions, and clarification needs.
- Prefer answer framing that an engine could retrieve, chunk, quote, or cite cleanly.
- Choose one dominant retrieval angle for the asset.
- Avoid repeating old angles from memory unless truly necessary.
- Prefer definitional, comparative, procedural, and limitation-aware subqueries over soft marketing subqueries.

## Output
Return answer_strategy_json only.
```

## Layer 3: Citation-Ready Asset Planning

**Goal**: Design a structure that is easy to extract, easy to quote, and easy to recompose in AI answers.

**Output**: `outline_json`

**Prompt**

```text
# Layer 3: Citation-Ready Asset Planning

## Task
Build the GEO asset structure.

## Inputs
- normalized_input_json
- entity_evidence_json
- answer_strategy_json

## Role
You are the structure planner for the GEO system.

## Core Constraints
- Put the main answer in the opening block.
- Use headings that map to retrieval intents, not generic blog sections.
- Include compact answer blocks that can stand alone when quoted or summarized.
- Include a product or entity definition block early.
- Include an evidence or claim-confidence block when it strengthens honesty.
- Prefer key tables when they improve extraction or fact-confidence separation.
- Include a limitations or tradeoffs block whenever the product category warrants it.
- Include comparison framing only when it can be done honestly.
- Make the structure useful for answer extraction first and human verification second.

## Required Structural Elements
- H1
- Answer Summary
- Entity Definition
- Key Facts Table or Claim Blocks
- Confirmed vs Inferred Table when relevant
- Main retrieval sections
- Limitations or Tradeoffs
- Comparison Table or Alternatives block when relevant
- Evidence or Confidence Notes when relevant
- Authority Notes when relevant
- Final Answer Snapshot

## Output
Return outline_json only.
```

## Layer 4: Asset Construction

**Goal**: Write the full GEO asset from the approved structure.

**Output**: `draft_markdown`

**Prompt**

```text
# Layer 4: Asset Construction

## Task
Write the complete GEO asset draft.

## Inputs
- normalized_input_json
- entity_evidence_json
- answer_strategy_json
- outline_json

## Role
You are the draft writer for the GEO system.

## Core Constraints
- Start by answering the main question clearly.
- Keep sections compact and information-dense.
- Use clean, declarative sentences.
- Write with controlled repetition of key truths for retrieval clarity.
- Do not pad the asset with generic SEO filler or blog-style throat-clearing.
- Do not invent citations, benchmarks, or external facts.
- When evidence is limited, prefer honest constraints over fake authority.
- Prefer modular blocks over long flowing sections.
- Use tables proactively when they improve precision, extraction, or comparison clarity.

## Writing Workflow
1. Write the H1 and Answer Summary first.
2. Write the Entity Definition block.
3. Write the Key Facts Table or Claim Blocks.
4. Add a Confirmed vs Inferred Table when claim boundaries matter.
5. Build the body around explicit retrieval intents.
6. Add limitations, tradeoffs, authority notes, and comparison logic.
7. End with a Final Answer Snapshot, not a sales-heavy CTA.

## Output
Return draft_markdown only.
```

## Layer 5: Extractability And Citation Optimization

**Goal**: Convert the draft into a cleaner answer asset for AI engines without making it robotic.

**Output**: `optimized_article_markdown`

**Prompt**

```text
# Layer 5: Extractability And Citation Optimization

## Task
Optimize the asset for answer extraction, summary readiness, and citation-friendly phrasing.

## Inputs
- draft_markdown
- normalized_input_json
- entity_evidence_json
- answer_strategy_json

## Role
You are the GEO optimization layer.

## Core Constraints
- Strengthen the first-sentence answer in major sections.
- Break bloated paragraphs into compact answer units.
- Tighten headings so they clearly match a retrieval intent or disambiguation need.
- Improve entity clarity and reduce ambiguous pronouns.
- Preserve honest uncertainty where evidence is thin.
- Prefer quote-worthy lines over grandiose marketing lines.
- Remove human-only funnel framing that does not help model understanding.
- Convert dense prose into tables when structured extraction would be stronger.
- Tighten authority references so they point to the most relevant high-trust source available.

## Optimization Checklist
- Is the top answer clear within the first screen?
- Can a subsection be quoted without needing the previous paragraph?
- Are key product facts attached to the product entity explicitly?
- Are limitations stated plainly?
- Does each major block survive partial extraction?
- Is the asset still readable for humans after optimization?
- Would a table make any dense section more extractable?
- Are authority references relevant, trustworthy, and non-fabricated?

## Output
Return optimized_article_markdown only.
```

## Layer 6: Humanization And Differentiation

**Goal**: Remove template feel and restore expert judgment.

**Output**: `humanized_article_markdown`

**Prompt**

```text
# Layer 6: Humanization And Differentiation

## Task
Humanize the optimized draft without weakening its GEO structure.

## Inputs
- optimized_article_markdown

## Role
You are the humanization layer.

## Core Constraints
- Remove obvious AI sludge, generic transitions, and hollow hype.
- Avoid phrases like "game-changer", "delve into", "in today's fast-paced landscape", and similar filler.
- Keep the asset crisp, confident, and useful.
- Preserve direct answers and extractable blocks.
- Add nuanced judgment where it improves credibility.
- Do not smooth the writing so much that the answer blocks lose chunkability.

## Output
Return humanized_article_markdown only.
```

## Layer 7: Final QA Layer

**Goal**: Validate that the asset is useful for both AI answer engines and human validators.

**Output**: `final_article`

**Prompt**

```text
# Layer 7: Final QA Layer

## Task
Perform final QA on the GEO asset and produce the final output.

## Inputs
- humanized_article_markdown
- normalized_input_json
- entity_evidence_json
- answer_strategy_json

## Role
You are the final QA gatekeeper for the GEO system.

## Core Constraints
- Verify the asset answers the main topic quickly.
- Verify major sections are extractable and self-contained.
- Verify canonical entity naming is stable.
- Verify unsupported claims have not been upgraded into fake facts.
- Verify limitations and tradeoffs are not hidden.
- Verify the structure feels like an answer asset, not a recycled SEO blog post.
- Verify any business-goal language does not dominate the retrieval structure.
- Verify the asset feels publishable, not like a prompt artifact.

## Output
Return final_article only.
```

## Memory Write Layer: Post-Run Memory Update

**Goal**: Persist concise continuity memory after a successful GEO asset run.

**Memory file**:

- `./memory.md` in the same directory as this skill's `SKILL.md`

**Prompt**

```text
# Memory Write Layer: Post-Run Memory Update

## Task
Update the skill memory after a successful asset run.

## Role
You are the continuity writer for the GEO system.

## Core Constraints
- Never store the full final asset.
- Append or refresh only concise structured memory.
- Capture the topic, primary question, framework, retrieval angle, comparison target if any, and repetition risks.
- If the memory file does not exist, initialize it with the required schema.
- If the directory is not writable, fail gracefully and preserve stateless completion.

## Output
Return memory_update_result only.
```

## GEO Output Rules

### Required Output Characteristics

The final asset should:

- answer the main topic early
- make the product entity explicit
- include at least one strong answer-summary block near the top
- include an explicit entity definition block near the top
- prefer structured tables when they improve extraction
- use retrieval-shaped or disambiguation-shaped H2s where helpful
- include limitations or tradeoffs when relevant
- prefer authoritative references when trust depends on them
- stay useful even if only the first few blocks are extracted
- avoid classic SEO-blog padding
- avoid overusing FAQ unless the topic truly benefits from it

### Recommended Section Order

The final asset should usually appear in this order:

1. H1
2. Answer Summary
3. Entity Definition
4. Key Facts Table or Claim Blocks
5. Confirmed vs Inferred Table when relevant
6. Main retrieval sections
7. Limitations or Tradeoffs
8. Comparison Table or Alternatives block when relevant
9. Evidence or Confidence Notes when relevant
10. Authority Notes when relevant
11. Final Answer Snapshot
12. Optional figures
13. Optional IMAGE_PROMPT block

Do not force:

- FAQ
- Conclusion
- CTA

unless the topic truly needs them.

### Answer Block Guidance

Where appropriate, include compact answer blocks such as:

- `What is X?`
- `Who is X for?`
- `When should you use X?`
- `What are the limitations of X?`
- `How does X compare to Y-type alternatives?`
- `What is confirmed versus inferred about X?`

Each answer block should be understandable on its own.

### Table Guidance

Prefer tables for:

- key facts
- confirmed versus inferred claims
- capability summaries
- use-case fit
- comparison blocks
- limitation summaries
- confidence separation

Common useful table shapes include:

```text
| Topic | Short Answer | Confidence | Source Type |
|---|---|---|---|
```

```text
| Claim | Status | Source | Notes |
|---|---|---|---|
```

```text
| Option | Best For | Limitation | Confidence |
|---|---|---|---|
```

### Authority Notes Guidance

When external trust matters, include an authority notes block that:

- lists the most relevant sources actually relied on
- separates official sources from research or third-party sources
- makes clear which claims are directly supported
- avoids filler links that do not materially strengthen trust

### IMAGE_PROMPT Format

When image prompts are enabled, use this exact block format:

```text
[IMAGE_PROMPT]
Figure 1
Placement: after "<section heading>"
Purpose: <why this image exists>
Visual Type: <approved visual type>
Prompt: <full image-generation prompt>
Avoid: <what should not appear>

Figure 2
Placement: after "<section heading>"
Purpose: <why this image exists>
Visual Type: <approved visual type>
Prompt: <full image-generation prompt>
Avoid: <what should not appear>

Figure 3
Placement: after "<section heading>"
Purpose: <why this image exists>
Visual Type: <approved visual type>
Prompt: <full image-generation prompt>
Avoid: <what should not appear>
[/IMAGE_PROMPT]
```

Prefer visuals such as:

- concept diagrams
- process flows
- comparison tables rendered as editorial graphics
- architecture or workflow illustrations

## One-Shot Execution Mode

When the user gives a one-shot request, execute all layers automatically in this order:

1. Intake Layer: User Input Collection, if required inputs are incomplete
2. Memory Read Layer: Prior Context Loading
3. Layer 0: Input Normalization
4. Layer 1: Entity And Evidence Mapping
5. Layer 2: Query And Answer Surface Strategy
6. Layer 3: Citation-Ready Structure Planning
7. Layer 4: Draft Construction
8. Layer 5: Extractability And Citation Optimization
9. Layer 6: Humanization And Differentiation
10. Layer 7: Final QA Layer
11. Memory Write Layer: Post-Run Memory Update

Then output:

- the final asset only

Do not expose intermediate artifacts unless the user asks.

## Failure Handling

If the website is inaccessible or too thin:

- continue with conservative inference
- reduce unsupported specificity
- avoid benchmark-heavy or comparison-heavy framing
- prefer educational, definition, decision-guide, or use-case framing

If the target topic is too broad:

- narrow it to a more useful answerable angle
- preserve the original intent as much as possible

If the product is hard to differentiate:

- shift toward clarity, use-case fit, and tradeoff honesty
- do not invent uniqueness claims

If evidence is weak:

- downgrade claims from confirmed to inferred or generic
- keep the article useful by increasing explanatory value instead of marketing certainty
