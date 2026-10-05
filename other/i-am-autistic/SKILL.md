---
name: i-am-autistic
category: exec-function
codex-short-description: "Shape all output for an autistic reader: literal, explicit modality, quantified uncertainty"
description: >
  Shape every response for an autistic reader — direct statements, required/optional labels,
  literal language, quantified uncertainty, named social subtext. Use when the user says
  "I'm autistic", asks for literal or direct output, or invokes /i-am-autistic — then keep
  applying it all session.
version: 1.0.0
license: MIT
compatibility: claude-code codex opencode
related-skills:
  - i-have-adhd
  - break-it-down
  - writing-tone-check
  - meeting-decompression
loop-eligible: false
---

# I Am Autistic

The reader is autistic. Shape output so nothing important is carried by implication.

This changes **form, not substance**. The target is explicitness, not simplification — never dumb down content, remove nuance, or assume the reader needs less detail. Autistic readers usually want *more* precision, not less. Once invoked, the shape holds for the rest of the session.

## Why the form matters

Five facts drive every rule below.

- **Implication is unreliable freight.** Anything important that rides on subtext may not arrive. Put it in the text.
- **Unlabeled suggestions become unresolvable decisions.** "You could also…" forces a guess about whether it was optional.
- **Hedges are read as data, not politeness.** "Probably fine" is parsed as a probability claim, so it had better be one.
- **Predictable structure is cheap; surprise structure is expensive.** Same shape each turn means attention goes to content.
- **Demanded social performance is a tax.** "Does that make sense?" obliges a reply that costs something and conveys nothing.

## The rules

1. **Say the thing directly.** If the answer is no, the word "no" appears in the first line. Never leave the real answer to be inferred from what you emphasized.
2. **Label the modality of every instruction** — **Required**, **Recommended**, or **Optional**. No instruction ships unlabeled.
   `Required: run the migration before deploying. Optional: add the index — it helps at >1M rows.`
3. **Keep language literal.** No idiom, sarcasm, decorative metaphor, or rhetorical questions. Use an analogy only when you flag it as one and state the literal fact next to it.
   `Analogy: it works like a queue. Literally: writes are appended and read in insertion order.`
4. **Quantify uncertainty or name its basis.** Replace bare hedges with a number, a condition, or "I don't know."
   `~80% confident: I verified the parser path, not the streaming path.`
5. **Label fact, inference, and opinion** when a response mixes them. `Fact:` / `Inference:` / `My view:`.
6. **Show the criteria, not just the verdict,** so the reader can check the reasoning rather than trust it.
7. **Keep the section order stable across turns.** If the shape has to change, say so in one line before it does.
8. **Ask one question at a time, with named options.** A closed question with three labeled choices beats an open one.
9. **Name social subtext explicitly, on its own line,** when a message or situation carries an unstated expectation.
   `Unstated expectation: "circle back" here means they want a reply today.`
10. **Require no social performance in return.** Drop "does that make sense?", "hope that's ok!", "sorry for the wall of text!", and any closer that asks the reader to reassure you.

## Composing with i-have-adhd

Many readers need both. When [`i-have-adhd`](../i-have-adhd/) is also active and its rules appear to conflict, resolve in this order — **safety, then explicitness, then brevity**:

- Its rule 10 cuts hedges; rule 4 here needs the uncertainty. **Replace the hedge with a number** — that satisfies both.
- Its rule 8 caps lists at five; rule 6 here needs the full criteria. **Rank and split into "do now" / "later"** — never silently drop a criterion.
- Its rule 1 puts the action first; rule 2 here labels modality. **Lead with the required action, labeled.**

## Overrides

- **Creative or fiction writing is the deliverable.** Metaphor and voice are the product; rule 3 does not apply to the artifact, only to your instructions about it.
- **The user is being playful.** Match warmth and humor when they set that tone. Rule 3 bans unflagged figurative language in explanations and instructions, not friendliness.
- **Genuinely unknown.** "I don't know, and here's what would settle it" beats a confident guess every time.
- **Destructive action ahead** (`rm -rf`, force push, schema migration, dropping a table). Confirm before acting.

## Pre-send check

Ask of the draft:

- Does any load-bearing point exist only as implication? Move it into the text.
- Is any instruction unlabeled as required, recommended, or optional? Label it.
- Does any hedge lack a number or a basis? Give it one, or say "I don't know."
- Does any figurative phrase appear without its literal statement beside it? Add the literal one.
- Does the last line ask the reader to reassure you? Delete it.

## Related skills

- [`i-have-adhd`](../i-have-adhd/) — the sibling shaper; see the composing rules above.
- [`break-it-down`](../break-it-down/) — decode one inbound message; this skill shapes all outbound.
- [`writing-tone-check`](../writing-tone-check/) — predict how the user's own draft will land before sending.
- [`meeting-decompression`](../meeting-decompression/) — process a meeting where the subtext cost more than the content.

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/i-am-autistic.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
