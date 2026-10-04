---
name: onboard
version: 1.1.0
description: Set up the workspace by guiding the PM through populating context files.
---

# /onboard

Sets up the workspace by guiding the PM through populating context files.

## Trigger

- User runs `/onboard`
- Auto-trigger: 3 or more context files contain only a heading

## Context file structure

Route input to the right file using these structures:

- **company.md** — What We Do (who you are, who it's for, core problem), Market (market definition, primary JTBD, ICP segments, scope), Stage & Size, Current Priorities (top 2-3), Constraints (budget, headcount, tech debt, timeline)
- **product.md** — What It Is (value proposition), Key Differentiators (2-3 reasons to choose you), Current State (shipped, in progress, broken)
- **competitors.md** — One section per competitor: what they do, strengths, weaknesses, our angle against them
- **personas.md** — One section per persona: who they are, their goal, their pains with signal strength and a real quote

## Workflow

### 1. Read context state

Read all 4 context files (`context/company.md`, `context/competitors.md`, `context/personas.md`, `context/product.md`). Classify each as empty (only heading), thin (missing key sections), or solid (most sections filled). Don't tell the PM this classification yet. Use it to guide your questions.

### 2. Open with a braindump

Start open. Don't ask structured questions yet.

- **All empty:** "Tell me about your product. Dump everything: pitch deck, company description, competitor names, user research, strategy docs, a URL, whatever you've got. The messier the better, just get it out of your head. I'll sort it."
- **Partially filled:** "I see some context already. [1-2 sentences on what's solid]. What's changed recently, or what should I know that's not captured yet?"
- **All solid:** "Your context looks solid. Anything need updating, or are you here to work on something?"

If the PM seems unsure what to share: "Do you have any of these lying around? A pitch deck, company website, existing PRD, investor update, competitor list, interview notes, strategy doc. Paste, link, or drop files in `data/`. Any of these will speed things up."

### 3. Parse, tag, and write

After the PM shares, process everything in one pass:

- Route each piece to the right context file following the structure above
- **Tag facts vs assumptions.** As you write to context files, distinguish:
  - Stated directly with evidence or specifics → write as-is
  - Vague, aspirational, or inferred → tag with `[Assumption, verify]`
- **Proactive web lookup:** When the PM mentions their company name, offer to look it up: "Want me to search for [company] and pre-fill what I can find? You can correct anything that's wrong." If they agree, search and populate company, product, and competitors with what's publicly available. Tag all web-sourced content with `[Source: web, verify]` so the PM knows what to check.
- When given a URL or company name, use web search to gather real information. Don't make things up.
- If a URL returns little useful info, say so and ask the PM to fill the gaps manually
- If input touches multiple files, update all of them in one pass
- Never overwrite existing context. Append or refine. If new info contradicts existing info, keep both and note: `[Updated: YYYY-MM-DD] Previously X, now Y.`

### 4. Summarize back

Before asking more questions, play back what you captured. This builds trust and catches misunderstandings early.

"Here's what I got from that: [2-4 sentence summary of what you wrote]. I flagged a couple of things as assumptions. Does this sound right, or should I fix anything?"

Show the progress checklist:
```
Context status:
- [x] Company — solid
- [ ] Competitors — thin (missing strengths/weaknesses)
- [ ] Personas — empty
- [x] Product — solid
```

### 5. Ask pointed follow-ups

Now ask questions, but targeted, not a form. Pick 2-3 questions max based on the biggest gaps. Follow the outside-in order (company → market → competitors → personas → product) but don't force it.

**Question style:**
- Fill market gaps: "What space or market are you in?" "What problem are your customers hiring you to solve?"
- Probe assumptions: "You mentioned users struggle with onboarding. Is that from data, interviews, or a hunch?"
- Fill critical gaps: "Who are your main competitors? Even just names is fine, I can research the rest."
- Challenge where useful: "You said you're targeting enterprise. What makes you confident that's the right segment?"

**Don't interrogate.** After 2-3 questions, process the answers (step 3-4 again) before asking more. The rhythm is: braindump → summarize → 2-3 questions → summarize → 2-3 questions.

### 6. Check if context is sufficient

Minimum viable context to do useful work:
- **Company:** know what you do, who it's for, and current priorities
- **Market:** know what market you're in and the primary JTBD
- **Product:** know what exists and what's broken
- **Competitors:** at least 2-3 named
- **Personas:** at least 1 real user type with a real pain

When met, say so and offer the next step. Follow this order:
- Company solid, Market thin → "I know who you are. What market or space are you in? What problem are your customers hiring you to solve?"
- Company + Market solid → "Want me to map out who else is in this space and how they approach it?"
- Personas solid → "You've got strong personas. Want me to synthesize any interview data you have, or keep going?"
- Product solid → "Want me to draft a one-pager for something you're considering? Or fill in more context first?"

Don't force it. If the user wants to keep going, keep going. The goal is to show value early.

When all files are solid: "Context is looking good. You could run `/analyze-competitors` to go deeper on competition, or `/prd` to start speccing something out."

**Progressive deepening:** Don't try to fill everything during onboarding. Get to "good enough" and let other skills deepen context as a side effect of real work. When `/prd` finds thin personas, it asks 1-2 questions. When `/analyze-competitors` finds no competitors listed, it asks. Context grows through use, not just onboarding.

## Edge cases

- **Resuming a partial onboard:** The skill reads current file state each time, so it naturally picks up where things are thin. No session state needed.
- **Contradictory info:** Flag it, keep both versions with dates. Let the PM decide which is current.
- **PM dumps everything at once:** Parse it, update multiple files in one pass, report all changes.
