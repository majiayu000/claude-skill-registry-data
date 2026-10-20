---
name: microcopy-tone
description: Enforce reviewer-grade tone of voice across every UI string — buttons, errors, toasts, empty states, confirmations, help text. Calm, factual, restrained. No exclamations, no cheerleading, no hedging. Use when writing or reviewing any user-facing string.
---

# Skill: Microcopy & Tone of Voice

The words are part of the product. A calm, restrained visual system paired with exclamatory, chirpy, or hedged copy breaks trust faster than any visual bug. Concept2Cure users are regulatory professionals — they want facts, not cheerleading.

This skill pairs with `claude-ui-design-principles` (principle 9: "Trust Through Restraint") and `regulatory-compliance-ux` (reviewer-grade language).

## Activation

This skill activates when:

- Writing any user-facing string: button label, toast, error message, empty state, confirmation dialog, tooltip, help text, placeholder, alert
- Reviewing a PR that touches UI copy
- Generating assistant / AnA chat response phrasing
- Localizing or rewording existing copy

## Core Principles

### 1. Factual Over Emotional

State what happened. Do not celebrate it, apologize for it, or editorialize.

- ❌ "Nice work! Your document has been saved."
- ❌ "Oops! Something went wrong."
- ✅ "Saved at 14:32."
- ✅ "Couldn't save. Network error."

### 2. Specific Over Generic

Name the artifact, the action, the reason. Generic copy is a tell that the system doesn't know what's happening.

- ❌ "Action failed."
- ❌ "An error occurred."
- ✅ "Couldn't publish Module 3 — the CTD section is locked by Jane Smith."

### 3. Active Voice, Present Tense

Users own their actions; the system responds in the present.

- ❌ "The document was saved by the system."
- ❌ "A new version has been created for you."
- ✅ "Saved. Now on v4.2."

### 4. No Hedging, No Cheerleading

Cut "successfully", "great", "perfect", "awesome", "", "let's", "we'll". Cut "might", "may want to", "possibly" unless the hedge is factually true.

- ❌ "Successfully published!"
- ❌ "Great! You might want to review the output."
- ✅ "Published to IND-2026-0047."
- ✅ "Review the output before signing."

### 5. No Emoji, No Exclamations

Emoji and `!` signal informality. Regulatory users read every word as potential audit trail text. The default is zero of both.

- ❌ "Done! 🎉"
- ❌ "Warning!"
- ✅ "Done."
- ✅ "Warning: this will overwrite the submission draft."

### 6. Errors Explain + Act

Every error answers: what broke, why, and what the user can do. No dead-end errors.

- ❌ "Error 500"
- ❌ "Something went wrong. Please try again."
- ✅ "Couldn't load the precedent set. The regulatory intelligence service is unavailable. Retry or continue without precedent data."

### 7. Disabled / Empty States Explain

A disabled button or empty list without context is a dead-end. Say why, and what unblocks it.

- ❌ Empty list: "No items."
- ❌ Disabled button with no tooltip
- ✅ Empty list: "No precedents match this indication. Broaden the search or switch agency."
- ✅ Tooltip on disabled button: "Requires Medical Director role. You are QA Reviewer."

### 8. Confirmation Dialogs Are Informative, Not Performative

"Are you sure?" adds friction without information. A confirmation dialog should state: the action, the target, the consequence.

- ❌ "Are you sure you want to delete this?"
- ✅ "Delete draft section 3.2.P? This cannot be undone. The section has no published versions."

### 9. Match Regulatory Vocabulary

Use the language regulators use. Don't soften it for consumers.

- ❌ "Hey, your submission looks good!"
- ❌ "Your paperwork is ready."
- ✅ "IND-2026-0047 is submission-ready. All required CTD sections are locked and signed."

### 10. AnA (Chat Assistant) Voice

AnA is a regulatory colleague, not a consumer chatbot. Concise. Factual. Offers tradeoffs. Asks when uncertain.

- ❌ "Sure thing! I'd be happy to help you with that! 😊"
- ❌ "I think this might possibly be a good approach, but you should check with your team."
- ✅ "Here's the 510(k) precedent set for your device class. Two have been cleared in the last 18 months — cited below. Want me to draft the Substantial Equivalence section?"

## Copy Audit — Quick Pass

Run these checks on any new string before merging:

- [ ] No exclamation marks (unless it's a genuine warning like "Warning: destructive action")
- [ ] No emoji
- [ ] No "successfully", "great", "awesome", "", "let's", "we'll"
- [ ] No generic errors — every error names what broke and what to do
- [ ] Disabled / empty / loading states explain themselves
- [ ] Specific over generic — names the artifact, version, or actor
- [ ] Active voice, present tense
- [ ] Reads as if a regulatory reviewer could quote it in an audit response

## Forbidden Patterns

| Forbidden | Use Instead |
| --- | --- |
| "Oops!", "Whoops!", "", "" | Factual error + cause + remedy |
| "Successfully saved!" | "Saved." |
| "Are you sure?" | "[Action] will [consequence]. [Irreversible?]" |
| "Something went wrong" | "Couldn't [verb]. [Cause]. [What to do]." |
| "No items." | "No [thing] match [filter]. [How to change the filter]." |
| Emoji in regulated UI | Plain text |
| `!` at end of confirmation / toast | No terminal punctuation or `.` |
| "Please wait..." | `<LoadingState label="Loading [thing]" />` |
| AnA: "I'd be happy to help!" | AnA: Direct answer or direct question |

## Completion Gate

Copy is NOT done until:

- The audit checklist above passes
- Error messages pass the "what broke / why / what do I do" test
- Empty and disabled states explain themselves
- No emoji, no exclamations, no hedging
- Copy reads at the register of the audience (regulatory professional)

When in doubt, read the string aloud in the voice of a calm, competent reviewer. If it sounds chirpy, rewrite.
