---
name: writing-workflow-tutorials
description: >
  Writes step-by-step workflow tutorials for FlashFusion: automation walkthroughs,
  AI tool setup guides, and reproducible workflows for newsletter creators.
  Covers tutorial structure, tool-specific patterns, and complexity calibration.
  Activates when writing a workflow tutorial, creating a how-to guide, building
  a step-by-step walkthrough for FlashFusion readers, or producing the Workflow
  of the Week section.
when_to_use: >
  Also triggers on: write a tutorial, how-to guide, workflow walkthrough,
  step-by-step guide, workflow of the week, set up this tool, automation tutorial,
  beginner workflow, n8n walkthrough, Zapier tutorial, Make automation guide,
  newsletter how-to, AI tool setup guide. Output routing (Rule 0) always runs
  first. No mandatory intake gate — ship with defaults and labeled assumptions
  unless context is entirely absent.
version: "2.0.0"
allowed-tools: Read Write
---

# Writing Workflow Tutorials — FlashFusion How-To System

Tutorials that readers can complete in the same session they read them. This skill governs structure, complexity calibration, and quality standards for all FlashFusion workflow tutorials.

---

## Rule 0 — Output Mode Gate (runs before any content)

Decide where the output goes before writing a single word of tutorial content.

1. **Inline** when: "show me", "draft this", "in chat", conversational review, or output ≤ 600 words
2. **File output** when: user says "save", "download", "docx", "export", or tutorial is deep-dive (> 600 words + full template)
3. **Both — inline first, then file** when: user says "show me and save it"
4. **Ambiguous → inline.** Never produce a file for a tutorial the user hasn't previewed.

Declare mode in one line before content:
`Mode: inline` / `Mode: file → outputs/[tutorial-slug].md` / `Mode: inline + file`

---

## Rule 1 — Context Gate (conditional — does NOT always run)

Fires ONLY when BOTH are true:
1. No tutorial type, topic, or target audience identifiable from conversation context
2. The output is a new standalone tutorial — not a revision, quick draft, or iteration

If either condition is false → pick the matching type from the Quick-Start Decision Tree, label assumed parameters inline (`// assumed: Beginner, newsletter section`), and proceed without asking.

**"Just do it" override:** If user says "just write it", "just do it", or "ship it" → skip gate. Pick the closest tutorial type from context, label all assumptions, and proceed.

---

## Rule 2 — Tutorial Type and Structure (preserved)

### Quick-Start Decision Tree

```
Tutorial type?
  ├─ Quick workflow (5–10 steps) ── Newsletter section length; ≤400 words
  ├─ Deep-dive workflow ────────── Full tutorial; 600–900 words + screenshots
  ├─ Automation setup ──────────── n8n/Zapier/Make specific; include JSON/template
  ├─ AI tool configuration ─────── Setup + prompt configuration + test run
  └─ Integration tutorial ──────── Connect two tools; prerequisites → steps → verify
```

### Tutorial Structure Template

```
WORKFLOW OF THE WEEK: [Title]
Time to implement: [X minutes]
Tools needed: [List exactly]
Difficulty: [Beginner / Intermediate / Advanced]

WHAT YOU'LL BUILD
[1–2 sentences: the specific outcome, not the general benefit]

STEPS
1. [Clear imperative instruction]
   → [Expected result or what to look for]
2. [Next step]
   → [Expected result]
...

TEST IT
[How to verify the workflow worked — specific observable outcome]

VARIATIONS
[1–2 ways to extend or adapt for different use cases]
```

### Usage Examples

**Example 1 — Claude research workflow**
```
WORKFLOW: AI-Assisted Newsletter Research Brief
Time: 20 minutes setup + 10 minutes/week
Tools: Claude API (or claude.ai), Notion
Difficulty: Beginner

WHAT YOU'LL BUILD
A repeatable research process that extracts creator angles from 5–10 articles
in under 10 minutes, outputting a structured brief ready for drafting.

STEPS
1. Open a new Claude conversation (claude.ai works; API gives more control)
   → You'll use this as your research workspace for the session

2. Paste this system prompt at the start of the conversation:
   "You are helping me research a creator-tech newsletter. For each article
    I share, extract: (1) the specific change or update, (2) why a solo
    newsletter creator should care, (3) one action they can take immediately,
    (4) relevance score 1-5."

3. Paste each article you want to evaluate (one per message)
   → Claude returns a structured evaluation for each

4. At the end: "Summarize the top 3 items by score as a research brief"
   → Brief is ready for drafting

TEST IT
Share 3 articles. Verify you get scores + creator angles for each.
If output is too generic, add "assume reader is a solo newsletter creator
writing about AI tools" to the system prompt.
```

**Example 2 — Complexity calibration**
Beginner: Step count ≤8; no code; free tools preferred; 15 minutes max
Intermediate: Up to 15 steps; may include paid tools; code blocks with explanation
Advanced: 15+ steps; API access required; assume technical literacy

**Example 3 — n8n workflow tutorial**
For automation tutorials, always include:
- The workflow JSON (importable)
- Credential setup instructions
- A test case with expected output
- Common error and fix ("if you see X error, the fix is Y")

---

## Rule 3 — Inlined Delivery Gates (no external file dependencies)

These gates run on every tutorial before delivery. No file reads required. If `references/` files are present, use them as supplements — never depend on them to run.

**Gate 1 — Tested or labeled:** Tutorial either asserts it has been run with the exact steps as written, or carries a prominent label: `INITIAL WALKTHROUGH — NOT YET TESTED. Update after running.`

**Gate 2 — Accurate time estimate:** "Time to implement" must be a real estimate or carry `(estimated)`. Never blank, never `TBD`, never fabricated precision.

**Gate 3 — Complete tools list:** Every required tool, account, permission, and paid tier appears in "Tools needed". Hidden prerequisites are not allowed.

**Gate 4 — Verify step with observable outcome:** A "TEST IT" block must name a specific thing to look at — not "it should work now."

**Gate 5 — Complexity correctly calibrated:** Beginner = ≤8 steps, no code, free tools, ≤15 min. Intermediate = ≤15 steps, paid tools OK, code with explanation. Advanced = 16+ steps, API required, technical literacy assumed.

---

## Delivery Checklist (HARD — enforce, do not skip)

- [ ] **Output mode declared before any tutorial content.** FAIL: the first produced token is tutorial content, not a mode declaration.

- [ ] **Tutorial tested OR labeled as untested.** FAIL: "Time to implement" or numbered steps appear without either (a) confirmation the tutorial was run exactly as written, or (b) the `INITIAL WALKTHROUGH — NOT YET TESTED` label at the top.

- [ ] **"Time to implement" is a non-placeholder value.** FAIL: field is blank, contains "TBD", or the estimate is more than 2× the actual step count (e.g., "5 minutes" for a 15-step tutorial).

- [ ] **All required tools, accounts, and tiers are in "Tools needed".** FAIL: any step references a tool, account, API key, OAuth credential, or paid tier that does not appear in the Tools needed header.

- [ ] **"TEST IT" section present with a specific observable outcome.** FAIL: section is absent, or the only instruction is "run the workflow" / "it should work" without naming what output to inspect.

- [ ] **Difficulty level matches actual step count and tool requirements.** FAIL: a Beginner tutorial contains code blocks, requires a paid tier, or has >8 steps; OR an Advanced tutorial has ≤8 steps and no API or CLI requirement.

---

## CLAIMS / COUNTEREXAMPLES / CONTRADICTIONS

- [GENERATED] Including a "TEST IT" step with a specific observable outcome reduces "I tried this and it didn't work" reader complaints because the verification step surfaces setup issues before publication.
- [GENERATED] Over-detailed tutorials (30+ steps) lose readers mid-way — split complex workflows into Part 1/Part 2 across two issues rather than a single 1,000-word walkthrough.
- ! CONTRADICTION: "Test before publishing" vs. "cover new tools quickly" — for brand-new tools (day-one releases), label as "INITIAL WALKTHROUGH — NOT YET TESTED" and update in the next issue. Do not fabricate test confirmation.

---

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS

- **`scripts/` is empty.** This skill produces tutorial text, not code artifacts. No automation scripts exist. A future script could validate step counts and word counts against the Quick-Start Decision Tree targets.
- **`assets/` is empty.** Intended for screenshot templates and reference images. Any tutorial referencing actual tool screenshots should archive them here for version tracking (UI changes between tool versions).
- **No FlashFusion voice/tone gate.** The delivery checklist enforces structure but not prose voice. If a FlashFusion brand voice guide exists, a Gate 6 against it would close this gap.
- **Word count not machine-checked.** Decision tree defines target lengths (≤400 / 600–900 words) but no checklist FAIL condition catches over/under word count, because the skill delivers inline text with no post-tool hook. A `hooks: post-tool-use` entry would make this hard-enforceable.
- **No staleness trigger.** Tutorials referencing specific tool UIs (n8n, Zapier, Make) go stale when those tools update. No mechanism flags a tutorial for re-testing after N months.
