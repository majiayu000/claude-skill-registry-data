---
name: record-pattern
description: Records observed patterns with proper structure from current or described interactions. Use when (1) user explicitly asks to record a pattern, (2) user approved creating a pattern after vasana skill suggestion, or (3) user runs /pattern-library add command.
---

# Record Pattern

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.

---

## Core Tenet

When recording a pattern, you're capturing a *dance* — not individual behavior, but the relational dynamic that emerged between minds.

---

## Recording a Pattern

### Step 1: Identify the Pattern

Ask: What was the *interaction* that produced value?

**Not:**
- What did AI do?
- What did human do?

**But:**
- What did they do *together*?
- What moves constituted the dance?
- What made it work?

### Step 2: Name It

Active, descriptive names:
- `productive-friction`
- `assumption-surfacing`
- `diverge-converge`
- `question-becomes-system`

Avoid:
- Passive names (`thinking-together`)
- Vague names (`good-conversation`)
- AI-centric names (`ai-helps-user`)

### Step 3: Mechanism-Not-Metaphor Check (REQUIRED)

Before describing the pattern, apply this guardrail:

1. **State the cross-domain claim precisely.** If the pattern claims to apply across domains, what mechanism transfers?
2. **Classify the similarity:**
   - **Genuine mechanism**: shared math, shared causal structure, shared constraint (e.g., Fourier uncertainty applies to both quantum mechanics and signal processing — same math)
   - **Surface resemblance**: shared vocabulary, shared vibe, shared shape (e.g., "quantum entanglement is like team bonding" — no shared mechanism)
3. **If surface only**: the cross-domain claim fails. The pattern may still be valid within a single domain. Record it as such — don't inflate.
4. **Counter-check — don't over-demand causation.** Before rejecting, ask: am I about to reject this *only* because no causal mechanism connects the domains — when the pattern never claimed one? A non-causal correspondence (a shared constraint, a structural isomorphism, a sign-relation like indicator→outcome) is a legitimate transfer-type; "it's just correlation" is not a rebuttal of a claim that only ever asserted correspondence. This is the opposite failure mode of step 2: that one stops *over-crediting* (metaphor inflated into mechanism), this one stops *over-demanding* (real structure dismissed for lacking a causal arrow it never needed). Admit only what passes between both.
5. **If genuine mechanism (or genuine non-causal structure)**: proceed. The pattern has cross-domain predictive power.

Reference: `mechanism-not-metaphor` pattern in the canonical library; the over-demand counter-check is its paired wall (`sign-not-cause`, currently in the canonical library's `_drafts/`).

### Step 4: Describe the Pattern

**What conditions signal it applies:**
- When does this pattern help?
- What situation triggers it?
- What questions/contexts activate it?

**What moves happen:**
- Opening (how it begins)
- Development (what unfolds)
- Landing (how you know it worked)

**What makes it work:**
- Key ingredients
- What must be present
- What breaks it

### Step 5: Add Testing Notes

```markdown
## Testing This Pattern

Before relying on this:
1. **Baseline:** Try scenario WITHOUT consciously invoking pattern
2. **With pattern:** Try another, consciously allowing the structure
3. **Compare:** Did conscious invocation help or hinder?
4. **Pressure:** Does it work when rushed?

**Honest note:** [Any limitations, time requirements, etc.]
```

### Step 6: Include Vasana Section (REQUIRED)

```markdown
## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.
```

---

## Template

```markdown
---
name: [active-descriptive-name]
description: [When to use - specific conditions that signal this pattern applies]
---

# [Name in Title Case]

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.

---

## What This Pattern Is

[Brief description of the interaction pattern]

**Origin:** [How this pattern was discovered/captured]

---

## Recognizing When This Applies

**Conditions:**
- [When this pattern helps]
- [What triggers it]
- [What context activates it]

**Not this pattern:**
- [When to NOT use it]

---

## Cross-Domain Verification

**Mechanism check:** [What shared mechanism (not just shared vocabulary) makes this pattern apply across domains?]
**Domains verified:** [List domains where the mechanism has been checked, not just where the name sounds applicable]

---

## The Pattern

### Opening: [How It Begins]
[Description of opening move]

### Development: [What Unfolds]
[Description of the back-and-forth]

### Landing: [How You Know It Worked]
[Description of successful completion]

---

## What Makes It Work

1. [Key ingredient 1]
2. [Key ingredient 2]
3. [Key ingredient 3]

---

## Testing This Pattern

Before relying on this:
1. **Baseline:** Try scenario WITHOUT consciously invoking pattern
2. **With pattern:** Try another, consciously allowing the structure
3. **Compare:** Did conscious invocation help or hinder?
4. **Pressure:** Does it work when rushed?

**Honest note:** [Any limitations]
```

---

## Where to Save

New patterns go to the **canonical pattern-library**, not the plugin cache.

- **Default (not yet library-ready):** `~/ClaudeShared/pattern-library/_drafts/[pattern-name].md`
- **Library-quality (tested, cross-domain):** `~/ClaudeShared/pattern-library/patterns/[pattern-name].md`
- **Pattern seeds:** `~/ClaudeShared/pattern-library/patterns/pattern-seeds/[seed-name].md`

The canonical library path is configured per-user; substitute the user's configured path if it differs from the `~/ClaudeShared/pattern-library/` default.

**Do NOT save user-recorded patterns to** `skills/pattern-library/patterns/` — that path is plugin cache (read-only, overwritten on update).

**Exception:** Official plugin releases may add seed patterns to `skills/pattern-library/patterns/` as part of the bundled library. That's distinct from user-recorded patterns and happens via PR to the plugin source, not via this skill.
