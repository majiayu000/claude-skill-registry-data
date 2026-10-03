---
name: skill-creator
description: Create new skills, improve existing skills, and test skill quality. Use when the user wants to build a skill from scratch, turn a workflow into a reusable skill, improve or refactor an existing SKILL.md, test how well a skill performs, optimize a skill's description so it triggers correctly, or asks "how do I make a skill for X". This is the meta-skill — it builds all other skills.
---

# Skill Creator

A skill is a reusable, opinionated expert guide that makes an AI agent dramatically better at a specific domain. Not a prompt. Not a template. A skill is a production-grade system that encodes deep domain expertise, principled workflows, concrete examples, and an unambiguous definition of done — so the agent executes it the same way every time, without the user having to re-explain.

Your job in this skill is to help the user go from "I want a skill for X" to a skill that works reliably in the real world.

---

## Skill Creator Principles

- **Understand before writing.** A skill written without understanding the user's intent produces generic instructions that could apply to anything. Ask the right questions first.
- **Skills generalize — test cases are just accelerants.** You iterate on 3–5 examples because it's fast. But the skill needs to work on the 10,000th prompt that nobody has seen yet. Avoid overfitting rules to the specific examples.
- **Explain the why, not just the what.** Instructions that say "always do X" without explanation get followed blindly in the wrong context. Instructions that say "do X because Y" get applied with judgment. Smart models respond better to reasoning than to commandments.
- **Lean beats padded.** Remove every instruction that isn't actively improving outputs. A 600-line skill where 200 lines are filler produces worse results than a tight 300-line skill where every line earns its place. If you find yourself writing ALWAYS/NEVER in all caps, step back — try explaining the reasoning instead.
- **The description field is a trigger, not a summary.** The description is what the agent reads to decide whether to load the skill. It must contain explicit trigger conditions: "Use when the user asks to..." — not just what the skill is about.
- **Test against reality, not intuition.** You cannot know if a skill works without running it. Gut-feel improvements compound errors. Run test cases. Look at the outputs. Iterate on evidence.

---

## The Skill Creation Loop

```
Understand intent
       ↓
Write draft skill
       ↓
Run test prompts → review outputs
       ↓
Improve skill based on feedback
       ↓
Repeat until quality is satisfactory
       ↓
Optimize description for triggering accuracy
       ↓
Ship
```

Jump into this loop wherever the user is. If they already have a draft, skip to testing. If they're still fuzzy on intent, start at understanding. Always be flexible — if they want to skip evals and iterate by feel, that's a valid choice.

---

## Phase 1: Capture Intent

### If the user says "turn this workflow into a skill"

Read the conversation history. Extract:
- What tools or steps were used
- What corrections the user made along the way (these reveal requirements that weren't stated)
- What the final output looked like
- What the user seemed satisfied with

Then confirm:
```
It looks like this skill is about [X]. It should:
1. [Core step 1]
2. [Core step 2]
3. Produce [output type]

Does that match what you have in mind? Anything I'm missing?
```

### If the user is starting from scratch

Ask up to 5 focused questions — not all at once, unless the user is clearly experienced:

1. **What is the one job this skill does?** Name it in a single sentence.
2. **Who triggers it?** What does a user say or do that should activate this skill?
3. **What does the output look like?** A document, code, analysis, structured data?
4. **What does "good" look like?** What separates a 10/10 output from a 6/10?
5. **What does "bad" look like?** What specific failure modes must this skill avoid?

If the user is non-technical, avoid terms like "JSON", "assertions", "eval pipeline" — use plain language equivalents:
- "test cases" not "evals"
- "checking the results" not "running assertions"
- "try it on some examples" not "benchmark"

---

## Phase 2: Write the Draft Skill

### Required SKILL.md Structure

Every skill must have this structure, in this order:

```markdown
---
name: skill-name-in-kebab-case
description: [See description rules below]
---

# Skill Title

[Opening paragraph: mindset and approach. What kind of expert does this well and why does their approach produce better outcomes.]

---

## [Skill Name] Principles

[5–8 load-bearing beliefs. These are the "why" behind the entire skill.
Each principle should be a thing that, if violated, produces a noticeably worse output.
Not rules. Beliefs. The agent applies judgment from principles — not from rule-lookup.]

---

## Step 0: Ground the Work Before Starting

[What to establish, ask, or read before taking any action.
This section prevents the skill from diving in before understanding the situation.
The most common failure mode in any skilled domain is premature action.]

---

## [Main execution sections]

[The workflow, patterns, templates, examples, code snippets.
Each section should have a clear job. If a section's purpose is unclear, cut it or merge it.]

---

## Definition of Done

[Checkbox checklist. Every item must be:
- Verifiable — the agent or user can confirm it is met
- Specific — no vague items like "quality looks good"
- Necessary — if removing the item wouldn't affect quality, remove it]
```

### Description Field Rules

The `description` field is the most important line in the file. It determines when the skill gets loaded.

**Rules:**
- Maximum 2 sentences
- Must include explicit trigger conditions: "Use when the user asks to...", "Use when the user mentions..."
- Must name the domain + the specific action, not just the domain
- Must distinguish this skill from adjacent skills

**Bad description:**
```
Helps with writing documents.
```

**Good description:**
```
Structured co-authoring workflow for PRDs, design docs, RFCs, and proposals.
Use when the user wants to write a PRD, design doc, RFC, or any structured
document where quality and completeness matter — goes deeper than general
writing help by guiding through context gathering, section refinement,
and reader testing.
```

**Template:**
```
[What it does — domain + specific action + key method].
Use when the user [trigger condition 1], [trigger condition 2], or [trigger condition 3].
```

---

## Phase 3: Write Test Cases

Write 3–5 test prompts that a real user would send. These should:

- Cover the core use case (what the skill is for)
- Cover at least one edge case (unusual input, partial information)
- Cover at least one failure-adjacent case (something that sounds like the skill's domain but isn't quite)
- Use realistic language — not "test the skill on a widget factory", but something a real user in the target audience would actually type

**Test case format:**

```markdown
## Test Cases — [Skill Name]

### Test 1: Core use case
**Prompt:** [Realistic user prompt]
**Expected output:** [What a good response looks like]
**Pass criteria:**
- [ ] [Specific, checkable criterion]
- [ ] [Specific, checkable criterion]

### Test 2: Edge case
**Prompt:** [Edge case prompt]
**Expected output:** [What a good response looks like]
**Pass criteria:**
- [ ] [Criterion]

### Test 3: Failure-adjacent
**Prompt:** [Something that might accidentally trigger the skill but shouldn't, or should trigger a graceful handling]
**Expected output:** [What the skill should do here]
**Pass criteria:**
- [ ] [Criterion]
```

---

## Phase 4: Run and Review

After writing the draft skill and test cases:

1. **Run each test prompt** with the skill active
2. **Read the full output** — not just whether it looked OK, but whether every pass criterion was met
3. **Look for patterns across test cases**:
   - Did the agent do the same unnecessary thing on every test? The skill is probably prompting it.
   - Did the agent skip the same important step on every test? The skill is missing something.
   - Did the outputs vary wildly in quality? The skill's instructions are ambiguous.

### Qualitative Review Questions

For each test output, ask:
- Does the output match what a domain expert would produce?
- Is anything present that shouldn't be? (filler, repetition, unnecessary preamble)
- Is anything missing that should be? (the skill's core value-add)
- Did the agent explain its reasoning at the right level, or was it either too shallow or too verbose?
- Would the target user be satisfied with this output? Why or why not?

---

## Phase 5: Improve the Skill

### How to think about improvements

**Generalize, don't overfit.** If the skill only works on the 3 test cases and nobody else's prompts, it's useless. When fixing a problem that appeared in a specific test case, ask: "Is this a specific fix or a general principle?" Prefer general principles.

**Read the execution trace, not just the output.** The most revealing information is the *process* the agent followed. Did it take a pointless detour? Did it repeat itself? Did it do something that wasn't in the skill instructions but should have been? The trace tells you what to add or remove.

**Remove before adding.** Before adding a new instruction, check if the problem can be fixed by removing an instruction that is creating the wrong behavior. Shorter is usually better.

**When you find yourself writing ALWAYS or NEVER in all caps:** Pause. Ask if you can explain the underlying principle instead. `"ALWAYS check X"` → `"Check X because Y will fail if you don't — the most common failure mode in this domain is Z"`. The second version produces better judgment.

### Common improvement patterns

| Problem observed | Likely cause | Fix |
|---|---|---|
| Agent starts with a long preamble every time | Step 0 asks too many questions | Tighten Step 0 to only essential questions |
| Output quality varies wildly | Principles are vague | Make each principle concrete with an example of what violating it looks like |
| Agent skips a critical step | Step not in the skill | Add it with an explanation of why it matters |
| Agent does something unhelpful on every test | Skill instructions cause it | Remove or reframe the instruction |
| Output is technically correct but feels wrong | Missing voice/tone guidance | Add a "How to write" section with examples |
| Agent over-explains its process | Skill says to explain everything | Add "show your work only when it adds value for the reader" |

---

## Phase 6: Optimize the Description

After the skill body is solid, optimize the description for triggering accuracy.

The description has two jobs:
1. **Load when it should** — the agent recognizes the right moment to invoke it
2. **Not load when it shouldn't** — the agent doesn't mistakenly invoke it for adjacent tasks

### Description optimization process

1. Write 5 prompts that **should** trigger this skill
2. Write 5 prompts that **should not** trigger this skill (but are close)
3. Read your description and check: does it distinguish between the two sets?
4. Rewrite until it does

**Example — `doc-coauthoring` description optimization:**

Should trigger:
- "Help me write a PRD for the new payments feature"
- "I need to draft a design doc for the auth refactor"
- "Can you help me write up a technical spec?"

Should NOT trigger (close but different):
- "Write a quick Slack message about the deployment" → use `internal-comms`
- "Update the README with the new API endpoints" → use `technical-writer`
- "Summarize this design doc for me" → general task, no skill needed

Revised description: adds "PRD, design doc, RFC" explicitly + "goes deeper than general writing help" to distinguish from `technical-writer`.

---

## Phase 7: Final Quality Gate

Before declaring the skill done, run this checklist:

### Skill body quality
- [ ] Opening paragraph establishes the mindset — not just "what it does" but "how an expert approaches it"
- [ ] 5–8 principles that are genuinely load-bearing (removing any one would degrade outputs)
- [ ] Step 0 grounds the work before any action — prevents premature execution
- [ ] All main sections have a clear, named purpose
- [ ] Examples are realistic — not widget factories or foo/bar placeholders
- [ ] Code snippets (if any) are correct and runnable
- [ ] Definition of Done has ≥ 8 specific, verifiable, necessary items
- [ ] No ALWAYS/NEVER all-caps commandments — reasoning used instead
- [ ] Minimum 200 lines — if shorter, the skill probably lacks depth

### Description quality
- [ ] ≤ 2 sentences
- [ ] Names the domain + the specific action
- [ ] Contains explicit trigger phrases: "Use when the user asks to..."
- [ ] Distinguishes this skill from the 2–3 most similar skills
- [ ] Tested against 5 should-trigger and 5 should-not-trigger prompts

### Test quality
- [ ] At least 3 test cases written
- [ ] Core use case covered
- [ ] At least 1 edge case covered
- [ ] Pass criteria are specific and checkable — not "output looks good"
- [ ] All 3 test cases pass at an acceptable quality level

---

## Skill File Location

Save new skills at:
```
SKILL/<skill-name>/SKILL.md
```

Skill name rules:
- `lowercase-kebab-case`
- Describes the **role** not the task: `database-architect` not `write-sql`
- Unique — check existing skills before naming

---

## Quick Reference: The 5 Signs of a Good Skill

1. **You can name its single job in one sentence** — if you need two sentences, it's two skills
2. **The description triggers on the right prompts and not on the wrong ones**
3. **The principles explain the *why*, not just the what**
4. **Step 0 prevents the #1 failure mode in this domain**
5. **The Definition of Done is a checklist you can actually check** — every item is specific and verifiable
