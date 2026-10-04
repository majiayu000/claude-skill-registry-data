---
name: seopro-skill
description: Advanced full-stack SEO article generation skill with strict internal layering. Use when the user wants a fully automatic, model-only SEO workflow that turns a product name, product URL, and target keyword into a publish-ready article. This skill preserves explicit multi-level architecture, step-by-step prompt layers, typed intermediate outputs, and automatic chaining, while upgrading the original workflow with hallucination control, model-only honesty, safer link policy, product-type routing, anti-AI rewriting, and final QA.
---

# SEO Pro Skill

## Overview

This is a **layered SEO writing system** built for full automation.

It is designed for users who want:

- one-time input
- automatic multi-step execution
- no reliance on external SEO tools
- a publish-ready article as the final output

Unlike a flat prompt, this skill must run through explicit internal layers. Each layer has:

- a goal
- defined inputs
- defined outputs
- a dedicated prompt block
- strict chaining into the next layer

The user may only see the final article, but the model must internally execute all layers in order.

This skill must also support an **active intake phase**:

- if the user has not already provided the required inputs
- the skill must proactively ask for them before article generation begins
- after enough information is collected, the skill should continue automatically without asking for permission again

## Core Positioning

This skill is **model-only**, not tool-dependent.

That means:

- SERP analysis is hypothesis-driven, not externally verified
- keyword difficulty is an informed assumption, not a real metric
- competitor identification is likely-positioning analysis, not a factual market database
- internal links must never be fabricated
- proof points must never be invented

This skill optimizes for:

- useful articles
- stable automation
- low hallucination risk
- strong structure
- human-readable final writing
- cross-article consistency through memory

## Memory System

After the first successful run, this skill should create and maintain a lightweight memory file at:

- `./memory.md` in the same directory as this skill's `SKILL.md`

The memory system exists to improve:

- anti-repetition across article runs
- topic diversification over time
- angle variation across similar keywords
- framework variation across repeated usage
- content gap awareness
- progression from already-covered topics into new territory

### Memory Principles

- The memory file is not a raw article archive.
- Do not dump full articles into memory.
- Store concise structured memory only.
- Memory should help future writing decisions, not bloat context.
- The primary purpose of memory is to reduce repeated article output, not to force stylistic sameness.
- Memory should help the skill recognize what has already been written so the next article can take a fresher path.
- The memory file path must be resolved relative to the current skill directory, not a machine-specific absolute path.
- When memory is missing, the skill should not fail.
- When memory is missing, the skill should complete the current run normally.
- After the first successful completed run, the skill should create the memory file automatically.
- On future runs, the skill should read memory before strategy begins.
- If the skill directory is not writable, degrade gracefully to stateless mode for that run.
- A missing or unwritable memory file must never block article generation.

### What Memory Should Store

The memory should preserve:

- product identity
- product URL
- previously written article titles
- previously targeted keywords
- previously used article angles
- previously used frameworks
- previously used comparison targets
- previously covered search intents
- previously covered user problems
- content gaps not yet covered
- repetition risks to avoid next time
- minimal stable defaults such as output language, image mode, and approved internal links

### Memory File Schema

The memory file must use this exact Markdown structure:

```text
# SEO Pro Skill Memory

## Product Memory
- Product Name:
- Product URL:
- Product Type:
- Default Target Audience:
- Default Conversion Goal:
- Default Brand Tone:
- Default Output Language:
- Default Image Mode:

## Approved Internal Links
- 

## Topic History

### Article Record
- Date:
- Title:
- Target Keyword:
- Article Type:
- Framework:
- Target Audience:
- Conversion Goal:
- Output Language:
- Image Mode:
- Angle Summary:
- Article Summary:
- Covered Intent:
- Comparison Target:
- Avoid Next Time:

## Continuity Notes
- 
```

Rules:

- The first successful run that creates `memory.md` must initialize it in this exact shape.
- Future runs may append additional `### Article Record` blocks under `## Topic History`.
- Do not rename the section headers.
- Do not replace the schema with free-form prose.
- Prefer writing anti-repetition memory over brand-style memory when tradeoffs are necessary.

### Memory Read Timing

The skill should read memory:

- after Intake
- before Layer 0 finishes normalization
- before Layer 2 keyword strategy
- before Layer 3 structure planning

This ensures prior article context influences:

- topic selection
- angle selection
- framework choice
- avoidance of repeated comparisons
- avoidance of repeated titles and search intents
- identification of better uncovered content opportunities

### Memory Write Timing

The skill should update memory:

- after Layer 7 completes successfully
- only after a usable final article exists
- by appending or refreshing concise structured records

### Memory Safety Rules

- Never store the full final article in memory.
- Never store unnecessary private user data.
- Never duplicate the same article record repeatedly.
- Prefer concise summaries over raw text.
- If an article is revised later, update its summary rather than storing multiple bloated variants.

## Required Inputs

The user must provide:

| Input | Description | Example |
|------|------|------|
| Product Name | Official product name | ShortAPI |
| Product URL | Official site URL | https://shortapi.ai |
| Target Keyword | Core keyword to optimize for | short link api |
| Target Audience | Primary intended reader | developers |
| Conversion Goal | What the article should push toward | pricing page visits |

These fields are mandatory because they directly shape:

- article angle
- proof style
- tone
- CTA logic
- section prioritization

Optional inputs:

| Input | Description |
|------|------|
| Product Type | API / AI SaaS / marketing tool / etc. |
| Brand Tone | technical / sharp / calm / premium |
| Output Language | final article language, default English |
| Image Mode | whether to output image prompts at insertion points or pure text only |
| Allowed Internal URLs | optional approved internal links only |
| Existing Articles | existing titles or URLs for topical alignment |
| Target Market | optional, if the article should fit a certain audience context |

If optional inputs are missing, infer conservatively.

## Intake Behavior

This skill must not assume the user will always provide structured inputs up front.

If the user says something like:

- `I want to write an SEO article`
- `help me write a blog post`
- `write an article for my product`
- `use seopro-skill`

and the required fields are missing, the skill must enter **Intake Mode** before Layer 0.

### Intake Mode Rules

- Ask for missing required inputs proactively.
- Ask in a compact, structured way.
- Ask only for missing fields.
- Do not begin article generation until the required fields are collected.
- Once the required inputs are collected, continue directly into the layered workflow.
- Do not ask the user to restate information they already gave.
- Optional fields may be requested briefly, but must not block execution.
- The first intake message should stay lightweight and prioritize required inputs.
- Optional fields should be presented as quick add-ons, not as a second wall of required setup.

### Required Intake Questions

If all required fields are missing, ask:

1. What is your product name?
2. What is your product URL?
3. What keyword do you want this article to target?
4. Who is the article for?
5. What action should the article drive after reading?

### Optional Intake Questions

Ask these only if helpful and only after the required inputs:

1. What type of product is this?
2. What tone do you want for the article?
3. What language should the final article be written in?
4. Do you want image prompts inserted at image positions, or pure text only?
5. Do you have approved internal links I can use?
6. Do you already have related articles I should align with?
7. Is this article for a specific market or audience segment?

### Default Intake Prompt

When required inputs are missing, use a prompt like this:

```text
Before I write the article, I need a few key inputs so I can aim it correctly.
在我开始写文章之前，我需要先拿到几个关键信息，这样文章方向才会准确。

Required / 必填
1. Product name / 产品名称
2. Product URL / 产品网址
3. Target keyword / 目标关键词
4. Target audience / 目标读者
5. Conversion goal / 转化目标

Quick optional add-ons / 快速选填
6. Product type / 产品类型
7. Brand tone / 文章语气或品牌语气
8. Output language / 输出语言
9. Image mode / 图片模式

Default language note / 默认语言说明
- If you do not specify output language, the final article will be written in English.
- 如果你不指定输出语言，最终文章默认会用英文生成。

Image mode / 图片模式
- Option A: Insert image prompts at image positions / 在需要插图的位置输出图片提示词
- Option B: Pure text only / 不需要插图，只输出纯文本

Example / 示例
Product Name / 产品名称: ShortAPI
Product URL / 产品网址: https://shortapi.ai
Target Keyword / 目标关键词: short link api
Target Audience / 目标读者: developers / 开发者
Conversion Goal / 转化目标: pricing page visits / 引导用户访问定价页
Product Type / 产品类型: API tool / API 工具
Brand Tone / 文章语气: technical and sharp / 技术感、直接
Output Language / 输出语言: English (default) / 英文（默认）
Image Mode / 图片模式: Option A - Insert image prompts at image positions / 选项 A - 在插图位置输出图片提示词

You can also add approved internal links, existing related articles, or target market if you want tighter alignment.
如果你希望内容更贴合，也可以继续补充可用内链、已有相关文章或目标市场。

Send them in any format you like. Once I have the required five, I will start the article directly.
你可以按任意格式发送。只要前 5 项齐了，我就会直接开始写。
```

## Global Execution Rules

These rules apply to every layer.

### Rule 1: Internal Layering Is Mandatory

- Do not skip layers.
- Do not jump directly to the final article.
- Every layer must produce a usable internal output before the next one starts.

### Rule 2: Model-Only Honesty

- Never present inferred SEO judgments as externally verified truth.
- Use assumption-based language internally for SERP shape, ranking difficulty, and competitor landscape.
- If the website is thin, reduce specificity rather than inventing certainty.

### Rule 3: No Hallucinated Links

- Never invent internal URLs.
- If `allowed_internal_urls` is provided, use only those URLs.
- If no approved internal URLs exist, use homepage only or omit internal links.
- Never fabricate `/pricing`, `/docs`, `/blog`, `/api`, or other routes.

### Rule 4: No Fabricated Data

- Never invent benchmarks, exact latency numbers, adoption stats, case-study metrics, customer counts, or comparison data.
- If proof is not visible, write directional value statements instead of fake numbers.
- If a number is illustrative rather than factual, it must be clearly framed as an example, not a fact.

### Rule 5: Product-Type Routing

Before layer execution, infer or confirm one primary route:

- `api-developer-tool`
- `ai-saas`
- `marketing-tool`
- `ecommerce-tool`
- `creative-tool`
- `general-b2b-saas`

This route must influence:

- keyword angle
- framework choice
- tone
- proof style
- CTA style

### Rule 6: Information Sufficiency Protocol

Every meaningful claim must be treated as one of:

- `confirmed`
- `inferred`
- `generic`

Guidance:

- `confirmed`: directly supported by user input or site content
- `inferred`: reasonably implied from the product category or page language
- `generic`: safe category-level statement used when evidence is weak

Never turn a `generic` idea into a fake specific detail.

### Rule 7: Final Output Default

Unless the user explicitly requests intermediate outputs:

- perform all layers internally
- output only the final article
- do not expose internal JSON or draft artifacts

### Rule 8: Intake Before Execution

- If required inputs are incomplete, ask the user for them before Layer 0 starts.
- Intake is part of the skill behavior, not a separate manual setup step.
- Layer execution begins only after required inputs are available.

### Rule 9: No Re-Entry After Intake Completion

- Once all required intake fields are collected, do not re-enter Intake Mode.
- Once all required intake fields are collected, do not switch into review mode, diagnostic mode, or exploratory mode unless the user explicitly asks for that.
- After intake completion, the skill must continue forward through the execution layers until it reaches the final article.
- Do not repeat progress restarts such as re-announcing article generation, re-opening the same intake path, or re-asking already answered questions.
- If a non-blocking uncertainty appears after intake is complete, resolve it internally using the skill rules instead of pausing or looping backward.

### Rule 10: Memory-Aware Execution

- If the memory file exists, read it before strategy layers begin.
- Use memory to improve consistency, not to force repetition.
- If the memory file does not exist, continue normally and create it after the article is completed.
- Memory may influence topic avoidance, framework variation, comparison-target rotation, CTA continuity, and internal-link habits.

### Rule 11: Single-Path Execution After Layer 0

- Once Layer 0 begins, execution must remain single-path until `final_article` is produced or a true blocking failure occurs.
- Do not restart the workflow from Intake, Memory Read, or Layer 0 unless the user explicitly asks for a restart.
- Do not fork into parallel article attempts for the same request.
- Do not reopen planning, review, or diagnostics during active generation unless the user explicitly redirects the task.

### Rule 12: Blocking Failure Definition

A true blocking failure is limited to:

- missing required intake fields
- inability to access required user-provided content when no reasonable fallback exists
- output corruption that prevents a valid final article from being formed
- explicit user interruption or redirection

Non-blocking uncertainty includes:

- imperfect product clarity
- incomplete optional inputs
- uncertain competitor landscape
- weak trust signals
- thin website content
- uncertain internal links

Non-blocking uncertainty must be handled internally using conservative defaults and fallback rules. It must not cause execution to loop backward.

### Rule 13: No Mid-Run Review Or Diagnostic Switching

- During an active article run, do not switch into review mode, audit mode, or diagnostic explanation mode unless the user explicitly asks for it.
- Do not narrate internal uncertainty as a reason to pause generation.
- Do not replace article execution with commentary about the workflow.

### Rule 14: Run Completion Requires Memory Write Attempt

- A run is not considered complete until both of the following have happened:
  - `final_article` has been produced
  - memory persistence has been attempted
- If memory persistence succeeds, the run ends with updated continuity state.
- If memory persistence cannot be completed because the directory is not writable, the run still ends successfully but must be treated as stateless for continuity purposes.

---

## Layer Map

| Layer | Name | Purpose | Output |
|------|------|------|------|
| Intake | User Input Collection | proactively collect required execution inputs | intake_response |
| Memory Read | Prior Context Loading | load previous writing context if memory exists | memory_context |
| Layer 0 | Input Normalization | normalize user inputs and inferred defaults | normalized_input_json |
| Layer 1 | Product Intelligence | understand product, users, and offer | product_analysis_json |
| Layer 2 | Keyword Strategy | choose topic angle and search intent fit | keyword_strategy_json |
| Layer 3 | Structure Planning | select framework and article architecture | outline_json |
| Layer 4 | Draft Construction | write the complete article draft | draft_markdown |
| Layer 5 | Authority Optimization | add authority structure, links, and rhythm | polished_article_markdown |
| Layer 6 | Humanization Layer | remove machine feel, sharpen judgment, add warmth | humanized_article_markdown |
| Layer 7 | Final QA Layer | validate logic, safety, and output integrity | final_article |

---

## Memory Read Layer: Prior Context Loading

**Goal**: Load prior writing context from memory before the SEO pipeline commits to a new strategy.

**Memory file**:

- `./memory.md` in the same directory as this skill's `SKILL.md`

**Trigger**:

- after Intake
- before Layer 0 is finalized
- before Layer 2 strategy decisions

**Output**: `memory_context`

**Memory Read Rules**

- If `memory.md` exists, read it and extract only the relevant parts.
- If `memory.md` does not exist, return an empty memory context and proceed.
- Use memory as directional context, not as a hard constraint.
- Prefer continuity, but avoid repetitive topic reuse.

**Prompt**

```text
# Memory Read Layer: Prior Context Loading

## Task
Read the skill memory file if it exists, and extract only the information that should influence the new article run.

## Role
You are the continuity manager for the SEO system. Your job is to preserve useful strategic memory across runs without letting old decisions trap the current article in repetition.

## Core Constraints
- If the memory file exists, read it before strategy begins.
- Extract product-level continuity signals, not raw article prose.
- Focus first on topic history, angle history, framework history, covered intent, and repetition avoidance.
- Use continuity only as a supporting factor, not the main factor.
- Do not let memory force the same angle repeatedly if a better new topic exists.
- If the memory file is missing, proceed with an empty context.
- Do not treat a missing memory file as an error state.

## Output
Return memory_context only.
```

---

## Intake Layer: User Input Collection

**Goal**: Proactively collect the minimum required user information before the SEO workflow starts.

**Trigger**:

- the user invokes the skill directly
- the user asks for an article without providing all required inputs
- any required field is missing

**Required fields to collect**:

- product_name
- product_url
- target_keyword
- target_audience
- conversion_goal

**Optional fields to collect if easy**:

- product_type
- output_language
- image_mode
- brand_tone
- allowed_internal_urls
- existing_articles
- target_market

**Output**: `intake_response`

**Prompt**

```text
# Intake Layer: User Input Collection

## Task
Before article generation begins, proactively collect the minimum required inputs from the user.

## Role
You are the onboarding operator for the SEO writing system. Your job is to quickly gather the execution-critical inputs without making the user do unnecessary formatting work.

## Core Constraints
- Ask only for missing required fields.
- If several required fields are missing, ask for them together in one compact message.
- Do not ask the user to repeat information they already gave.
- Do not begin the article workflow until the required fields are present.
- Optional fields can be requested, but they must not block execution.
- Keep the intake lightweight and practical.
- Once the required fields are collected, do not re-open intake or ask the same setup questions again.

## Intake Workflow
1. Check whether product_name exists.
2. Check whether product_url exists.
3. Check whether target_keyword exists.
4. Check whether target_audience exists.
5. Check whether conversion_goal exists.
6. Ask for all missing required fields in a single structured message.
7. Once the user replies with the required fields, continue automatically into Layer 0.
8. Do not fall back into intake, review, or diagnostic questioning unless the user explicitly asks for it.

## Default Intake Message
Before I write the article, I need a few key inputs so I can aim it correctly.
在我开始写文章之前，我需要先拿到几个关键信息，这样文章方向才会准确。

Required / 必填
1. Product name / 产品名称
2. Product URL / 产品网址
3. Target keyword / 目标关键词
4. Target audience / 目标读者
5. Conversion goal / 转化目标

Quick optional add-ons / 快速选填
6. Product type / 产品类型
7. Brand tone / 文章语气或品牌语气
8. Output language / 输出语言
9. Image mode / 图片模式

Image mode / 图片模式
- Option A: Insert image prompts at image positions / 在需要插图的位置输出图片提示词
- Option B: Pure text only / 不需要插图，只输出纯文本

Example / 示例
Product Name / 产品名称: ShortAPI
Product URL / 产品网址: https://shortapi.ai
Target Keyword / 目标关键词: short link api
Target Audience / 目标读者: developers / 开发者
Conversion Goal / 转化目标: pricing page visits / 引导用户访问定价页
Product Type / 产品类型: API tool / API 工具
Brand Tone / 文章语气: technical and sharp / 技术感、直接
Output Language / 输出语言: English (default) / 英文（默认）
Image Mode / 图片模式: Option A - Insert image prompts at image positions / 选项 A - 在插图位置输出图片提示词

You can also add approved internal links, existing related articles, or target market if you want tighter alignment.
如果你希望内容更贴合，也可以继续补充可用内链、已有相关文章或目标市场。

Send them in any format you like. Once I have the required five, I will start the article directly.
你可以按任意格式发送。只要前 5 项齐了，我就会直接开始写。

## Output
Return intake_response only.
```

---

## Layer 0: Input Normalization

**Goal**: Convert user input into a stable schema for downstream layers.

**Input**:

- memory_context
- product_name
- product_url
- target_keyword
- optional fields if provided

**Output**: `normalized_input_json`

```json
{
  "product_name": "",
  "product_url": "",
  "target_keyword": "",
  "product_type": "",
  "target_audience": "",
  "conversion_goal": "",
  "brand_tone": "",
  "output_language": "English",
  "image_mode": "pure-text-only",
  "allowed_internal_urls": [],
  "existing_articles": [],
  "target_market": ""
}
```

**Normalization Prompt**

```text
# Layer 0: Input Normalization

## Task
Normalize the user's provided inputs into a stable JSON object for downstream SEO generation.

## Role
You are a senior SEO systems operator responsible for converting messy user input into a reliable execution schema. Your job is not to be creative here. Your job is to eliminate ambiguity before strategy begins.

## Core Constraints
- Preserve the user-provided product name exactly when available.
- Preserve the provided product URL exactly.
- Preserve the target keyword exactly unless obvious normalization is required for spacing or casing.
- Preserve target_audience and conversion_goal exactly when provided.
- If memory_context contains stable brand defaults, use them only for missing optional fields.
- Infer missing optional inputs conservatively.
- Default output_language to English unless the user explicitly requests another language.
- Default image_mode to `pure-text-only` unless the user explicitly asks for image prompts.
- Default allowed_internal_urls to an empty array if none are provided.
- Do not silently replace the user's audience or conversion objective with a broader guess.
- Once this layer begins, the article run must move forward continuously unless a true blocking failure occurs.

## Workflow
1. Read the user input and identify required fields.
2. Read memory_context if available.
3. Confirm that product_name, product_url, target_keyword, target_audience, and conversion_goal are present.
4. Normalize wording and casing only where harmless.
5. Infer only optional fields.
6. Use memory only to fill optional continuity defaults, never to overwrite explicit user input.
7. Normalize image_mode to one of:
   - `image-prompts-at-insertion-points`
   - `pure-text-only`
8. Hand off immediately to Layer 1 without reopening intake or review.
9. Return a compact execution object with no commentary.

## Output
Return normalized_input_json only.
```

---

## Layer 1: Product Intelligence

**Goal**: Build a reliable internal understanding of the product without fabricating unsupported facts.

**Input**:

- memory_context
- normalized_input_json

**Output**: `product_analysis_json`

```json
{
  "product_name": "",
  "product_url": "",
  "product_type": "",
  "main_keyword": "",
  "one_line_positioning": "",
  "core_problem": "",
  "core_offer": "",
  "likely_users": [],
  "likely_use_cases": [],
  "differentiators": [],
  "trust_signals": [],
  "likely_competitors": [],
  "evidence_level_notes": "",
  "recommended_route": ""
}
```

**Layer Rules**

- `likely_competitors` must be treated as likely, not verified
- `trust_signals` may be empty if the site does not show them
- `recommended_route` must be one of the approved product-type routes
- `evidence_level_notes` must mention uncertainty honestly

**Prompt**

```text
# Layer 1: Product Intelligence

## Task
Analyze the product using the normalized input and the product website when accessible. Build an internal product understanding that is useful for SEO writing without inventing unsupported details.

## Inputs
- memory_context
- normalized_input_json

## Role
You are a product marketing strategist and category analyst. You are responsible for understanding what this product is, who it serves, what problem it solves, and how confidently each claim can be made.

## Core Constraints
- Identify what the product appears to do.
- Infer exactly one primary product route.
- Describe the core user problem the product solves.
- Extract or infer likely use cases.
- Identify differentiators only when plausible.
- Do not invent exact customer proof, performance claims, pricing claims, or media mentions.
- If the site is sparse, keep claims broad and useful.
- Use "likely" framing for competitors and market positioning.
- Respect the target_audience and conversion_goal from the normalized input. They are not decorative; they must influence interpretation.
- Use memory_context only to understand continuity, not to override current user intent.

## Working Method
1. Read memory_context for stable product continuity if available.
2. Read the homepage and key visible positioning cues.
3. Identify the product category and core offer.
4. Map the likely user problem to the provided target audience.
5. Infer likely use cases that support the target keyword.
6. Note any clear trust signals without exaggeration.
7. Flag uncertainty honestly in evidence_level_notes.

## Output
Return product_analysis_json only.
```

---

## Layer 2: Keyword Strategy

**Goal**: Choose a strong topic direction and keyword angle without pretending to have real SERP tooling.

**Input**:

- memory_context
- normalized_input_json
- product_analysis_json

**Output**: `keyword_strategy_json`

```json
{
  "working_topic": "",
  "article_type": "",
  "search_intent": "",
  "primary_keyword": "",
  "secondary_keywords": [],
  "difficulty_assumption": "low|medium|high",
  "serp_hypothesis": "",
  "suggested_proof_points": [],
  "topic_reasoning": "",
  "angle_to_avoid": ""
}
```

**Layer Rules**

- `difficulty_assumption` is only an internal writing aid
- `serp_hypothesis` must be phrased as a hypothesis, not a fact
- `suggested_proof_points` must be suggestions for stronger writing, not fabricated evidence
- avoid topics that require hard benchmark claims if the product page cannot support them

**Prompt**

```text
# Layer 2: Keyword Strategy

## Task
Using the product analysis and target keyword, choose the strongest article angle for a model-only SEO workflow.

## Inputs
- memory_context
- normalized_input_json
- product_analysis_json

## Role
You are a senior SEO strategist with strong editorial judgment. You do not have external keyword tools, so your edge comes from clean intent mapping, category logic, and smart topic selection.

## Core Constraints
- Select one clear topic direction rather than several weak ones.
- Align topic choice with likely search intent.
- Choose a primary keyword that is usable in natural writing.
- Expand with only relevant secondary keywords.
- Estimate ranking difficulty as an assumption, not a verified metric.
- Describe the likely SERP pattern as a hypothesis only.
- Avoid fake SEO precision.
- Prefer topics that can be written credibly from product positioning and category logic.
- Explicitly note one angle to avoid if it would create hallucination risk or weak proof.
- The chosen topic must fit both the target audience and the conversion goal.
- Use memory_context to avoid repeating recently used angles when a better fresh angle exists.

## Strategy Workflow
1. Read memory_context for previous topics, angles, and audience patterns.
2. Interpret the user's target keyword literally first.
3. Check whether that keyword is too broad, too vague, or too proof-heavy.
4. Reframe into the most article-friendly angle that still respects the original request.
5. Avoid unnecessary duplication with recently written articles when possible.
6. Choose the article type that best matches likely intent.
7. Generate only secondary keywords that would naturally appear in a strong article.
8. State one strategic angle to avoid, especially if it would force fake comparisons or unsupported claims.

## Output
Return keyword_strategy_json only.
```

---

## Layer 3: Structure Planning

**Goal**: Select the right content framework and generate a precise article architecture.

**Input**:

- memory_context
- normalized_input_json
- product_analysis_json
- keyword_strategy_json

**Output**: `outline_json`

```json
{
  "h1": "",
  "selected_framework": "",
  "framework_reasoning": "",
  "target_reader": "",
  "sections": [
    {
      "section_order": 1,
      "h2": "",
      "purpose": "",
      "eeat_role": "",
      "h3_items": [],
      "section_notes": "",
      "word_budget": ""
    }
  ],
  "estimated_total_words": ""
}
```

**Framework Library**

- `comparison`
- `alternatives`
- `how-to`
- `best-practices`
- `use-case`
- `api-integration-guide`
- `decision-guide`
- `troubleshooting`

**Framework Selection Rules**

- `comparison`: for direct evaluation queries or versus-style intent
- `alternatives`: for best tools, top options, or replacement-seeking intent
- `how-to`: for educational or instructional intent
- `best-practices`: for operational, strategic, or optimization intent
- `use-case`: for workflow-specific or role-specific intent
- `api-integration-guide`: for technical onboarding and implementation
- `decision-guide`: for fit, pricing, or tool-selection intent
- `troubleshooting`: for blockers, errors, and common mistakes

**Outline Rules**

- 4 to 7 H2 sections
- each section must have a real purpose
- no filler sections
- one consistent narrative voice
- architecture must fit the target reader and article type

**Prompt**

```text
# Layer 3: Structure Planning

## Task
Select the most appropriate framework and produce a strong article outline that matches the keyword strategy, product route, and likely reader intent.

## Inputs
- memory_context
- normalized_input_json
- product_analysis_json
- keyword_strategy_json

## Role
You are a strategic content architect. Your job is to turn abstract SEO direction into an article structure that feels inevitable, persuasive, and easy to write from.

## Core Constraints
- Choose exactly one framework.
- Create a strong H1 that includes the primary keyword naturally.
- Build an outline that reflects real reader progression.
- Assign each section a purpose and an E-E-A-T role.
- Keep the outline useful for long-form writing, not decorative.
- Match the structure to the user's product type, target audience, and conversion goal.
- Every section must earn its place.
- Use memory_context to maintain continuity of tone and article family without cloning old outlines.

## Planning Workflow
1. Read memory_context for recent framework usage and tone patterns.
2. Start from reader intent, not from template habit.
3. Select the framework that best fits the article type.
4. Design section order so each H2 unlocks the next one.
5. Use H3 items only where they strengthen depth or scannability.
6. Keep the outline conversion-aware without making it sound like a landing page.
7. Reserve the CTA energy for the end instead of polluting every section.

## Output
Return outline_json only.
```

---

## Layer 4: Draft Construction

**Goal**: Write the complete article draft from the selected architecture.

**Input**:

- normalized_input_json
- product_analysis_json
- keyword_strategy_json
- outline_json

**Output**: `draft_markdown`

**Draft Rules**

- readability comes before keyword stuffing
- use the primary keyword naturally
- use secondary keywords only where they fit
- maintain one consistent voice
- include at least one meaningful tradeoff
- include at least one limitation or non-fit scenario
- do not repeat the same idea across multiple sections
- avoid fake authority language

**Length Guidance**

- `comparison`: 1800-2600 words
- `alternatives`: 1800-2600 words
- `how-to`: 1400-2200 words
- `best-practices`: 1400-2200 words
- `use-case`: 1200-2000 words
- `api-integration-guide`: 1200-2200 words
- `decision-guide`: 1000-1800 words
- `troubleshooting`: 1000-1800 words

**Prompt**

```text
# Layer 4: Draft Construction

## Task
Write the full article draft from the approved structure.

## Inputs
- normalized_input_json
- product_analysis_json
- keyword_strategy_json
- outline_json

## Role
You are a senior SEO writer with domain fluency in software and product-led businesses. You know how to write content that ranks because it helps, not because it chants keywords.

## Core Constraints
- Follow the section architecture exactly.
- Write like a credible human expert, not a keyword machine.
- Use the keyword strategy as a guide, not a repetition target.
- Include concrete reasoning, clear transitions, and meaningful judgment.
- Add one honest tradeoff.
- Add one honest limitation or scenario where the product is not the best fit.
- Do not fabricate metrics, benchmarks, customer stories, or product capabilities.
- Keep the article aligned with the stated target audience and conversion goal.

## Writing Workflow
1. Open with immediate relevance to the keyword and reader.
2. Resolve the main search intent before expanding into nuance.
3. Use concrete examples, but only when they are supportable.
4. Let the article build trust by being selective, not by over-claiming.
5. Use transitions that show progression, not filler.
6. Close each major section with a useful takeaway or bridge.

## Output
Return draft_markdown only.
```

---

## Layer 5: Authority Optimization

**Goal**: Refine the draft into a publish-ready article with stronger structure, better rhythm, careful links, and higher trust.

**Input**:

- normalized_input_json
- product_analysis_json
- keyword_strategy_json
- outline_json
- draft_markdown

**Output**: `polished_article_markdown`

**Optimization Rules**

- you may add `Quick Decision`
- you may add `TL;DR`
- you may add short comparison bullets
- you may add one final CTA
- you may add zero to three internal links
- you may add zero to four external links

**Internal Link Rules**

- use only `allowed_internal_urls`
- if none exist, use homepage only or omit internal links
- never create new paths

**External Link Rules**

- use links only where they improve trust or context
- prefer durable technical sources and respected documentation
- allowed external link categories include:
  - official technical documentation
  - standards and protocol documentation
  - official platform docs
  - official API docs
  - trusted engineering blogs
  - official open-source project pages
  - official social profiles or social posts when they add direct context
- do not link to competitor product pages, competitor homepages, competitor pricing pages, or competitor blog posts
- competitors may be mentioned in plain text when relevant, but they must not be linked
- do not insert links just to meet a quota

**Figure Rules**

- If `image_mode` is `pure-text-only`, do not include figures and do not output IMAGE_PROMPT.
- If `image_mode` is `image-prompts-at-insertion-points`, include exactly three figure placeholders and exactly three matching image prompts.
- Assign them these roles:
  - Figure 1: concept, landscape, or architecture framing
  - Figure 2: workflow, process, comparison, or explanatory support
  - Figure 3: decision, summary, or closing support
- Every figure must be tied to a specific nearby section.
- Do not add ornamental visuals.

**Figure Placeholder Format**

When figure output is enabled, use this exact in-article placeholder format:

```text
[FIGURE 1 HERE]
[FIGURE 2 HERE]
[FIGURE 3 HERE]
```

Rules:

- Place each figure marker immediately after the section it supports.
- Do not invent alternate placeholder styles.
- Do not use HTML comments, XML tags, or Markdown image syntax as placeholders.

**IMAGE_PROMPT Output System**

When `image_mode` is `image-prompts-at-insertion-points`, output an `IMAGE_PROMPT` block with one entry per figure.

Each entry must include:

- `Figure`
- `Placement`
- `Purpose`
- `Visual Type`
- `Prompt`
- `Avoid`

Approved `Visual Type` values:

- `concept illustration`
- `workflow diagram`
- `comparison visual`
- `product-style mockup`
- `decision summary visual`

Prompt requirements:

- match the article tone, target audience, and product category
- support the nearby section instead of vaguely repeating it
- prefer clean editorial, diagrammatic, or product-marketing visuals over generic AI art
- avoid fake UI screenshots unless the user explicitly wants conceptual UI mockups
- avoid text-heavy layouts unless the image is intentionally infographic-like
- avoid irrelevant people, visual clutter, and mismatched device metaphors
- if the product is developer-facing, prefer architecture, workflow, dashboard-style, or data-flow imagery
- if the product is business-facing, prefer process, comparison, infographic, or decision-support imagery

**Prompt**

```text
# Layer 5: Authority Optimization

## Task
Transform the draft into a stronger publish-ready article with better structure, better pacing, safer linking, and clearer authority signals.

## Inputs
- normalized_input_json
- product_analysis_json
- keyword_strategy_json
- outline_json
- draft_markdown

## Role
You are an editorial director responsible for turning a solid draft into a publishable asset. You optimize for trust, clarity, scannability, and professional finish without adding fake authority.

## Core Constraints
- Improve trust and readability without changing the article's core meaning.
- Use only approved internal links.
- Never fabricate URLs.
- Add external links only when they genuinely help.
- Never use external links that point to competitors.
- If competitors are mentioned, keep them as plain text only.
- Restrict external links to authoritative documentation, standards, official platform resources, trusted engineering references, open-source project pages, or official social sources that add real context.
- Add Quick Decision and TL;DR when they improve scannability.
- Keep the article globally understandable unless the user explicitly wants a regional framing.
- Respect image_mode strictly:
  - if `pure-text-only`, output no figures and no IMAGE_PROMPT block
  - if `image-prompts-at-insertion-points`, insert exactly three figure placeholders at the correct section positions and append a full IMAGE_PROMPT block
- If figures are used, make them structurally meaningful and add an IMAGE_PROMPT block at the end.
- Keep link quantity subordinate to link quality.

## Optimization Workflow
1. Tighten the introduction and make the article easier to scan.
2. Add summary blocks only if they improve usability.
3. Insert internal links sparingly and only from approved URLs.
4. Insert external links only to support claims or deepen context.
5. Decide figure handling based on image_mode.
6. If image_mode is `image-prompts-at-insertion-points`, place exactly three figure placeholders where they help the nearby sections most.
7. Generate three high-quality image prompts that reflect the article's actual argument and audience.
8. Improve rhythm, section pacing, and reader confidence.
9. Ensure the CTA matches the stated conversion goal.

## Output
Return polished_article_markdown only.
```

---

## Layer 6: Humanization Layer

**Goal**: Remove machine-like patterns and make the writing sound experienced, grounded, and human.

**Input**:

- normalized_input_json
- polished_article_markdown

**Output**: `humanized_article_markdown`

**Humanization Rules**

- vary sentence rhythm
- avoid repetitive paragraph shape
- prefer concrete judgment over empty hype
- keep useful nuance
- do not sound omniscient
- do not over-polish into ad copy

**Hard Bans**

- `delve into`
- `pave the way`
- `game-changer`
- `testament to`
- `unlocking the potential`

**Prompt**

```text
# Layer 6: Humanization Layer

## Task
Rewrite the polished article so it feels more human, more grounded, and less templated, without breaking the structure or changing factual integrity.

## Inputs
- normalized_input_json
- polished_article_markdown

## Role
You are a veteran editor with strong taste and low tolerance for AI sludge. You know the difference between polished writing and synthetic writing, and your job is to preserve the first while removing the second.

## Core Constraints
- Remove machine-like phrasing and over-smoothed marketing language.
- Preserve the H1 and overall article structure.
- Preserve valid links.
- Preserve the article's tradeoffs and limitations.
- Make the tone sharper, warmer, and more natural.
- Do not invent new claims during rewriting.
- Do not flatten the article into generic brand copy.

## Humanization Workflow
1. Remove repetitive phrasing and predictable sentence cadence.
2. Replace vague hype with grounded judgment.
3. Keep useful tension, tradeoffs, and subtlety.
4. Preserve credibility by resisting the urge to over-perfect every line.
5. Make the article feel authored, not assembled.

## Output
Return humanized_article_markdown only.
```

---

## Layer 7: Final QA Layer

**Goal**: Validate logic, integrity, and publication readiness before final output.

**Input**:

- normalized_input_json
- keyword_strategy_json
- humanized_article_markdown

**Output**: `final_article`

**QA Checklist**

- H1 includes the main keyword naturally
- article matches the target keyword and likely search intent
- no invented internal URLs
- no fabricated numbers
- no unsupported competitor claims
- at least one tradeoff is present
- at least one limitation or non-fit scenario is present
- no obvious repeated paragraphs
- tone matches the inferred audience
- article reads like a human expert, not a stitched prompt artifact
- if image_mode is `pure-text-only`, there must be no IMAGE_PROMPT block
- if image_mode is `image-prompts-at-insertion-points`, every figure must have a matching IMAGE_PROMPT entry
- figure placement must match the section it is supposed to support
- if image_mode is `image-prompts-at-insertion-points`, the article body must contain exactly three placeholders:
  - `[FIGURE 1 HERE]`
  - `[FIGURE 2 HERE]`
  - `[FIGURE 3 HERE]`

**Prompt**

```text
# Layer 7: Final QA Layer

## Task
Validate the final article for safety, coherence, truthfulness, readability, and publication readiness.

## Inputs
- normalized_input_json
- keyword_strategy_json
- humanized_article_markdown

## Role
You are the final reviewer before publication. You are skeptical, detail-oriented, and responsible for catching anything that would make the article look careless, fake, over-optimized, or machine-generated.

## Core Constraints
- Run the full checklist.
- If any issue fails, revise the article before returning it.
- Ensure the final article is structurally complete and clean.
- Ensure the article does not contain fake precision, fake links, or unsupported proof.
- Ensure the article still serves the target audience and conversion goal.

## QA Workflow
1. Check keyword fit and title integrity.
2. Check claim safety and evidence discipline.
3. Check link safety.
4. Check repetition, tone drift, and structural cleanliness.
5. Check that the CTA still matches the user's intended conversion goal.
6. Revise silently if needed, then return the final article only.

## Output
Return final_article only.
```

---

## Memory Write Layer: Post-Run Memory Update

**Goal**: Update the skill memory after a successful article run so future runs can stay more consistent and less repetitive.

**Trigger**:

- after Layer 7 returns a valid final_article

**Memory file**:

- `./memory.md` in the same directory as this skill's `SKILL.md`

**What to write**

- product identity summary
- current target audience
- current conversion goal
- output language
- image mode preference
- brand tone if known
- approved internal links if provided
- article title
- target keyword
- article type
- selected framework
- one-line angle summary
- one-line article summary
- one line on what should be avoided next time

**Prompt**

```text
# Memory Write Layer: Post-Run Memory Update

## Task
After a successful final article is produced, update the skill memory so future article runs can remain consistent and avoid redundant topic decisions.

## Role
You are the long-term memory curator for the SEO system. Your job is to keep only the information that improves future writing quality and continuity.

## Core Constraints
- Do not store the full article.
- Store concise structured memory only.
- Update memory in a way that makes future topic selection smarter and less repetitive.
- Keep the memory readable and compact.
- Avoid duplicate records for the same article.
- If memory.md does not exist yet, create it at this stage.
- The first successful article run is what creates the memory file.
- If the skill directory is not writable, skip memory persistence and continue without error.
- When creating memory.md for the first time, initialize it using the exact Memory File Schema defined earlier in this skill.
- Always attempt memory persistence after `final_article` is formed.
- Prioritize storing what was covered, what angle was used, and what should be avoided next time.

## Output
Update memory.md and return no user-facing content.
```

---

## Keyword Placement Rules

- place the primary keyword in the H1
- use the primary keyword or a close variant in the opening
- use the primary keyword or a close variant in at least one H2
- use the primary keyword or a close variant in the conclusion
- never force repetition if it harms natural English

## Final Output Order

The final article should appear in this order:

1. H1
2. Quick Decision
3. TL;DR
4. Introduction
5. Main body
6. Conclusion
7. CTA
8. Optional figures
9. Optional IMAGE_PROMPT block

## IMAGE_PROMPT Format

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

## One-Shot Execution Mode

When the user gives a one-shot request, execute all layers automatically in this order:

1. Intake Layer: User Input Collection, if required inputs are incomplete
2. Memory Read Layer: Prior Context Loading
3. Layer 0: Input Normalization
4. Layer 1: Product Intelligence
5. Layer 2: Keyword Strategy
6. Layer 3: Structure Planning
7. Layer 4: Draft Construction
8. Layer 5: Authority Optimization
9. Layer 6: Humanization Layer
10. Layer 7: Final QA Layer
11. Memory Write Layer: Post-Run Memory Update

Then output:

- the final article only

Do not expose intermediate artifacts unless the user asks.
Once Layer 0 begins, keep execution single-path until final article generation and memory write attempt are both complete, unless a true blocking failure or explicit user interruption occurs.

## Failure Handling

If the website is inaccessible or too thin:

- continue with conservative inference
- reduce unsupported specificity
- avoid benchmark-heavy or comparison-heavy framing
- prefer educational, decision-guide, or use-case framing

If the target keyword is too broad:

- narrow it to a more useful, more article-friendly angle
- preserve the original intent as much as possible
