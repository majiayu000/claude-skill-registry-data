---
name: xhsfenxi
description: |
  小红书博主分析全流程 skill — 拆解账号定位、提炼爆款选题公式、输出结构化报告和商业版 Word。内置三型博主分类体系（荒诞美学型 / 共鸣命名型 / 现实策略型），基于多位真实博主的深度分析沉淀。支持单账号深度拆解、多账号对比、自定义学习报告，证据分级（公开主页→截图→第三方公开资料→推断），所有交付物可一键转为 Markdown + 商业 Word。Use it when the user asks to analyze a Xiaohongshu blogger/account, extract viral topic formulas, compare creators, or produce business-grade deliverables.
keywords:
  - xiaohongshu
  - RED
  - 小红书
  - 小红书分析
  - 博主分析
  - 账号拆解
  - 对标分析
  - 爆款选题
  - 爆款选题公式
  - 内容策略
  - 个人IP分析
  - 创作者分析
  - 三型博主
  - 荒诞美学型
  - 共鸣命名型
  - 现实策略型
  - 品牌符号
  - 结构化总结报告
  - Word报告
  - 商业版报告
  - 选题公式学习
  - 博主拆解
  - 小红书运营
  - 内容账号分析
  - 竞品分析
  - 账号定位
  - benchmark account
  - topic formula
  - creator research
  - content audit
  - account positioning
  - competitor analysis
  - archetype classification
  - viral topic
  - markdown report
  - word report
  - 小红书博主对比
  - 爆款内容拆解
  - 内容IP打法
metadata:
  openclaw:
    runtime:
      node: ">=18"
---




### Local Context Review

`python scripts/_run.py` is a local diagnostics helper for the `xhsfenxi — 小红书博主分析 Skill` skill. It may inspect env. Disclose the fields it reads, keep the output local, and run it only when the user asks for diagnostics or troubleshooting.

# xhsfenxi — 小红书博主分析 Skill

> 公开页分析 · 三型博主分类 · 爆款选题公式提炼 · 多账号对比 · Markdown/商业Word交付

---

## When to Use

Use this skill when the user asks to:

- analyze a Xiaohongshu / RED creator account
- identify which archetype a creator belongs to (荒诞美学型 / 共鸣命名型 / 现实策略型)
- summarize an account's positioning, audience, style, or content pillars
- extract a **viral topic formula** or reusable content method
- compare two or more benchmark creators
- learn what can be copied vs what must stay differentiated
- turn the analysis into a **Markdown report**, **Word report**, or **business-style deliverable**

Typical trigger phrases:

- "分析这个小红书博主"
- "拆一下这个账号"
- "做爆款选题公式"
- "帮我做对标分析"
- "做成商业版 Word"
- "这个博主是哪一型？"
- "compare these two RED creators"
- "extract the topic formula from this account"

---

## Three-Archetype Classification System

Distilled from real analyses of multiple Xiaohongshu creators.

### Type A — 荒诞美学型 (Absurdist Aesthetics)

**Representative archetype:**

Core pattern: wraps serious or philosophical content in absurdist humor and high-quality visuals.

| Dimension | Characteristics |
|-----------|----------------|
| Content kernel | Absurdist filter on everyday life; philosophical undertone |
| What users get | Entertained + moved + aesthetically immersed |
| Title mechanism | Contrast (grand setting × mundane action) + unified brand symbol |
| Brand symbol | A single recurring tag, e.g. "（劲爆）" |
| Expression style | Humorous, high-production, literary naming |
| Commercial fit | High-end lifestyle, travel, photography, luxury brands |
| Replication difficulty | High — depends on accumulated visual aesthetic sensibility |

**Identifying markers:**
- All content tied together by a signature phrase or visual symbol
- Serious topics expressed lightly; absurd topics expressed earnestly
- Titles feel like literary naming, not just descriptions

---

### Type B — 共鸣命名型 (Resonance & Naming)

**Representative archetype:**

Core pattern: translates personal experience into universally relatable life-stage propositions, named in memorable ways.

| Dimension | Characteristics |
|-----------|----------------|
| Content kernel | Youth growth, worldview expression, life-stage naming |
| What users get | Understood + named + given a new perspective |
| Title mechanism | Proposition feeling + metaphor + judgment |
| Brand symbol | Signature conceptual phrases and naming patterns |
| Expression style | Warm, perceptive, aesthetically refined |
| Commercial fit | Growth/education/creative platforms, mid-range lifestyle |
| Replication difficulty | Medium — method learnable, requires genuine observation |

**Identifying markers:**
- Content "names" vague emotional states people couldn't articulate
- Private experience → universal proposition
- Titles read like thoughtful questions or redefinitions

---

### Type C — 现实策略型 (Reality & Strategy)

**Representative archetype:**

Core pattern: breaks down unspoken real-world rules and provides executable strategies for ordinary people to move upward.

| Dimension | Characteristics |
|-----------|----------------|
| Content kernel | Ordinary woman's upward mobility, reality rule-breaking |
| What users get | Validated + activated + empowered with actionable moves |
| Title mechanism | Conflict words + counter-intuitive framing + strong stance |
| Brand symbol | Self-labeling with perceived weakness (先夺走羞耻感) |
| Expression style | Sharp, realistic, strong-attitude conclusions |
| Commercial fit | Mass consumer, career, e-commerce, practical tools |
| Replication difficulty | Medium — framework learnable; don't copy the surface aggression |

**Identifying markers:**
- Titles feel slightly improper but undeniably accurate
- Each piece breaks an unspoken rule or collapses an information gap
- Users feel "刺但有用" — uncomfortable but useful

---

### Mixed Formula (Advanced)

The most powerful content often combines two archetypes:

> **Type B resonance/naming × Type C reality/strategy**
> = Content that both "understands you" and "tells you what to do next"

Use `scripts/archetype.js` to quickly identify which archetype(s) an account fits.

---

## Core Operating Rules

1. **Use public evidence first.** Prefer search pages, homepage/profile pages, and other publicly visible surfaces.
2. **Do not fake detail-page access.** If post detail pages are blocked by risk control, say so clearly.
3. **Grade evidence quality.** Treat sources in this order:
   - Level A: visible Xiaohongshu public pages / user screenshots
   - Level B: other public sources (podcasts, interviews, encyclopedias, analytics sites)
   - Level C: synthesis / inference based on repeated visible patterns
4. **Do not present public estimates as backend truth.** Third-party follower or pricing data are supporting clues, not audited facts.
5. **Ask for 3–10 representative post links or screenshots** when the user wants deep post-level analysis.
6. **Deliver something useful even when blocked.** If detail pages fail, still produce a homepage-level strategic report.
7. **Always identify the archetype.** Every analysis should name which of the three types (or hybrid) the account belongs to — this frames the entire report.

---

## Default Workflow

### 1) Clarify the task shape

Lock the requested output mode before heavy research:

- Structured account report
- Viral topic formula
- Archetype identification
- Two-or-more-account comparison
- "How to learn from this creator without copying them"
- Business-style Word deliverable

Use `scripts/intake.js` for a fast intake template.

### 2) Gather source inputs

Collect whatever the user already has:

- account name
- Xiaohongshu homepage/search URL
- screenshots
- external links (podcasts, news, interviews)
- target output path
- whether they need Word / clickable TOC / business styling

### 3) Research with the source ladder

Read `references/workflow.md` for the full ladder.

Preferred tool pattern:

- `web_search` for public discovery
- `browser` or `browser-use` for homepage/search-page inspection
- `web_fetch` for readable public pages
- `image` for screenshot analysis
- `read` for any local Markdown reports already created

### 4) Classify the archetype

Before deep analysis, make a preliminary archetype call:

- Run `node scripts/archetype.js <creator-name>` to print the classification prompt
- Answer: Type A (荒诞美学) / Type B (共鸣命名) / Type C (现实策略) / Mixed
- The archetype frames the entire lens of the analysis

### 5) Build the account model

Extract and write down the five layers:

1. **Identity** — who the creator is framed as
2. **Audience contract** — why people follow them
3. **Topic system** — what recurring problems/desires they cover
4. **Expression system** — how titles and openings work, including any brand symbol
5. **Transferability** — what another account can actually learn

### 6) Produce the deliverables

Always output the three standard DOCX files directly — no intermediate Markdown step needed:

| Output file | When to produce |
|-------------|----------------|
| `账号名-结构化总结报告.docx` | Single creator analysis |
| `账号名-爆款选题公式.docx` | Single creator topic formula |
| `选题公式学习-综合版.docx` | Multi-creator comparison |

Use `scripts/docx-plan.js <creator-name>` to get the exact build command.
See `references/workflow.md` for the Word TOC fix checklist if needed.

---

## Deliverables

Three standard output files. Always produce as `.docx` directly.

### 账号名-结构化总结报告.docx

Single creator full breakdown. Sections:
1. Account snapshot
2. Archetype classification + rationale
3. Strategic positioning
4. Audience and emotional contract
5. Content pillars
6. Title / hook system + brand symbol analysis
7. Narrative structure
8. Commercialization clues
9. What to learn
10. What not to blindly copy
11. Conclusion

### 账号名-爆款选题公式.docx

Single creator topic formula. Sections:
1. Why this creator produces strong topics (archetype-based)
2. Total formula
3. 3–6 recurring topic models
4. Title formulas
5. Body structure formulas
6. Distribution / comment triggers
7. How to migrate to another account
8. 10–30 ready-to-use topic directions

### 选题公式学习-综合版.docx

Multi-creator comparison. Sections:
1. Why compare these creators together
2. Archetype map
3. Shared foundations + key differences
4. Hybrid formula
5. Which path fits which use case
6. 30 combined topic directions
7. Final recommendation

---

## Word Output

Run `node scripts/docx-plan.js <creator-name>` to get the exact build command.

Standard build: `python3 build_docx6.py <creator-name>`

If TOC / bookmark issues appear: run `inspect_docx.py` then `fix_final2.py`.
See `references/workflow.md` for the full fix checklist.

---

## Output Files

Three files, always `.docx`:

- `账号名-结构化总结报告.docx`
- `账号名-爆款选题公式.docx`
- `选题公式学习-综合版.docx` (comparison / multi-creator)

Use `scripts/report-plan.js <creator-name>` to confirm filenames.

---

## Scripts

| Command | Purpose |
|--------|---------|
| `node scripts/intake.js` | Print a structured intake template for a new analysis task |
| `node scripts/intake.js --json` | Same as above, JSON format |
| `node scripts/archetype.js <creator-name>` | Print the archetype classification prompt |
| `node scripts/archetype.js <creator-name> --quick` | Print a quick-read archetype cheatsheet |
| `node scripts/report-plan.js <creator-name>` | Print recommended deliverables and filenames |
| `node scripts/report-plan.js <A> <B> --mode compare` | Print a comparison deliverable plan |
| `node scripts/docx-plan.js <creator-name>` | Print Word generation plan using build_docx*.py |

---

## Limitation Policy

Always state which situation applies:

- **Homepage-level only**: enough for strategic analysis, not enough for exact post-body claims
- **Mixed-source analysis**: Xiaohongshu public pages + third-party public clues
- **Deep-dive mode**: based on user-provided screenshots / links / transcripts

If blocked by risk control, say so and continue with the strongest available public evidence.

---

## What Good Output Looks Like

A strong output is:

- structured
- archetype-aware (names and reasons the type)
- evidence-aware (grades sources)
- strategically useful
- honest about access limits
- directly reusable in future reports

Avoid vague praise, empty creator admiration, or unsupported claims about hidden metrics.

---

## References

Read only when needed:

- `references/workflow.md` — detailed evidence ladder, execution runbook, Word TOC fix guide
- `references/templates.md` — report templates, archetype-specific section structures, naming patterns

---

## Proven Analyses Archive

Three full analyses have been completed and archived in:

```
openclaw_cosmo/afa/小红书分析与工作流归档/01-分析报告与选题公式/
```

| Archetype | Type | Key Insight |
|-----------|------|-------------|
| 荒诞美学型 | Type A | 品牌符号 + 反差标题 + 哲思轻量化输出 |
| 共鸣命名型 | Type B | 私人经历→公共命题，给模糊状态命名 |
| 现实策略型 | Type C | 困境→说破→规则→策略→爽感 |

These archetypes are the ground truth for the classification system.

---

*Version: 2.1.0 · Created: 2026-04-08 · Updated: 2026-04-09*
