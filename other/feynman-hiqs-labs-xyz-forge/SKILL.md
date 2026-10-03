---
name: feynman
description: Convert a highly technical document or subject into a plain, accurate, layman-friendly explanation using Feynman-style teaching moves — everyday analogy, a first-principles ladder, jargon stripping, and honesty about the limits. Use this whenever the user wants to "explain this simply", "make this understandable to a non-technical audience", "translate this for stakeholders / execs / new hires / customers", "ELI5 this doc", "de-jargon this", give me the "plain-English version", "what does this actually mean", or hands over a dense technical doc, spec, paper, RFC, or codebase writeup and wants it made digestible — even if they don't say the word "Feynman". Produces a layered explanation (one-sentence core, then gist, then full plain walkthrough), a jargon-to-plain glossary bridge, analogies that each name where they break down, and a flagged list of anything the source left genuinely unclear. Do NOT use this to merely shorten a document that is already clear (that is a summary, not a translation), to write marketing or persuasive copy, or to "dumb down" in a way that sacrifices accuracy. Do NOT fire on a code snippet, stack trace, error message, or a debugging question — those want a direct answer, not a layered explainer.
---

# feynman

Turn dense technical material into an explanation a smart non-specialist can actually follow — in the spirit of Feynman's *Six Easy Pieces*, without trading away correctness.

## TL;DR of what this skill does

Reads a technical source read-only, understands it, then rebuilds it from the ground up in plain language: a one-sentence core, a gist paragraph, a full walkthrough, a jargon→plain glossary, analogies with their limits marked, and an honest list of what the source left unclear. It is file-first — it always saves the result to a file the user names.

## The one rule everything else serves

> As simple as possible, but **not simpler**.

(That line is an aphorism commonly attributed to Einstein, not to Feynman — a paraphrase, not a quotation from either. It earns its place here on merit, not on provenance.)

Clarity is the goal; dilution is the failure mode. If a simplification would make the reader *believe something false*, it is wrong — even if it reads beautifully. When forced to choose, keep the truth and admit the complexity.

## Non-negotiables (guardrails)

- **Accuracy is the hard constraint.** Never smooth over a concept into something incorrect. A rougher-but-true sentence beats a slick-but-wrong one.
- **Techniques, not persona.** Use Feynman's *moves*. Do **not** imitate his folksy voice, exclamations, or first-person anecdotes. No performed whimsy.
- **Every analogy names where it breaks.** An unlabelled analogy is a future misconception. Say "this holds up to X, but stops working at Y."
- **Flag, don't fabricate.** If the source is ambiguous or you're inferring, mark it — never invent a clean explanation to paper over a gap.
- **Read-only on the source. Additive output.** Observe the doc; never edit it. Never overwrite an existing output file — if the chosen path already exists, disambiguate rather than clobber.

## Inputs

| Input | Default | Notes |
|---|---|---|
| `source` | *(required)* | The technical doc, section, or subject to translate. |
| `audience` | intelligent non-specialist | e.g. "exec", "new engineer", "customer", "board". Calibrates vocabulary and depth, not accuracy. |
| `mode` | `Full` | `Express` = core + gist + glossary + honesty pass. `Full` = adds ladder, analogies, comprehension checks. |

If `audience` or `mode` is unstated, state the default you're assuming in one line and proceed — don't stall for it. (Filename and location are handled at write time; see File delivery.)

## The method — six moves

**Provenance, stated honestly** (this skill's own rule #4 applies to this skill): only Move 2 is
straight out of *Six Easy Pieces* — the atomic-hypothesis passage in Ch. 1, Feynman's own example of
compressing a field into one sentence. Moves 1 and 6 come from the popularized "Feynman Technique," a
study method named after him by others, **not** a method he wrote down. Moves 3–5 are ordinary
instructional design. The set works; it is not a citation. Do not represent it as one.

1. **Understand it yourself first.** Restate the source's actual purpose in one plain sentence. If you can't, you don't understand it yet — go back to the source before writing anything. (This step is not optional; it's the whole method.)
2. **Find the one sentence.** If the reader could keep only a single sentence, what is it? This becomes the core. (Feynman's "everything is made of atoms" move — the maximally compressed true statement.)
3. **Map the jargon.** Extract every load-bearing technical term. Give each a plain-language equivalent. Terms the reader *must* learn stay (and get defined); terms that are just insider shorthand get replaced.
4. **Build the ladder.** Start from the simplest true statement and add exactly one layer of complexity at a time. Never assume a rung the reader hasn't climbed. Motivate *why it matters* before *how it works*.
5. **Ground with analogy.** Attach an everyday analogy to the 2–3 hardest concepts — and immediately mark where each analogy stops being true. Use concrete scale where it helps ("if the packet were a letter, the header is the envelope").
6. **Honesty pass + comprehension check.** Note what the source left unclear, what you approximated, and where the model breaks down. Then give the reader 1–2 questions they can answer *only if* they actually understood it.

## Process (linear)

1. **Ingest.** Read the source fully, read-only. Identify the core purpose and intended real-world effect.
2. **Self-test (Move 1).** Write the one-sentence restatement. If it feels vague, re-read the source — do not proceed on a shaky understanding.
3. **Extract (Moves 2–3).** Pull the core sentence and build the jargon map.
4. **Rebuild (Moves 4–5).** Construct the ladder; attach labelled analogies to the hardest rungs.
5. **Stress-test (Move 6).** Do the honesty pass. Flag ambiguities as `⚠ unclear in source` rather than resolving them silently. Write comprehension checks (Full mode).
6. **Emit.** Deliver the layered output as a saved file per **File delivery** below — write to the house default path, update the index, and verify the file exists before reporting success.

## File delivery

This skill is **file-first**: it always produces a saved file. It follows the same manifest convention as
[shakedown](../shakedown/SKILL.md) — don't invent a third shape.

1. **Never modify the source.**
2. **Write to the house default without asking** — `FEYNMAN/<YYYY-MM-DD>/<slug>-<HHMM>.md` at the repo
   root (use system time; don't guess it). Only if the user *named* a path do you use theirs. Asking
   where to save is a stall, and it hangs an unattended run.
3. **Never overwrite.** If the path exists, append `-2` (then `-3`, …) rather than clobber.
4. **Prepend a one-line entry to `FEYNMAN/INDEX.md`** (newest first) so the folder stays scannable —
   `- <YYYY-MM-DD HH:MM> — [<title>](<YYYY-MM-DD>/<slug>-<HHMM>.md) — <audience>, <mode>`. Create the
   index if it doesn't exist. If the user directed output outside the `FEYNMAN/` tree, skip the index.
5. **Verify the file exists on disk** before reporting success. Do not claim a write that hasn't landed.
6. **Confirm on screen with the path and the one-sentence core** — don't re-dump the whole explanation
   into chat.

## Output contract

Lead with the shortest, highest-value layer so a skimming reader gets the point immediately, then descend into detail.

```
# <Title> — plain-language version
Source: <path/name>  ·  Audience: <audience>  ·  Mode: <mode>

## In one sentence
<the single most-compressed true statement>

## The gist (≈1 paragraph)
<what it is, why it matters, what it does — no jargon>

## How it actually works        (Full mode only)
<the ladder: simplest true thing first, one layer at a time>

## Pictures for the hard parts   (Full mode only)
- <concept>: <everyday analogy>.  ⓘ Holds up to <X>; breaks at <Y>.

## Jargon → plain
| Term in the doc | What it really means |
|---|---|
| <term> | <plain equivalent> |

## What the source left unclear   (honesty pass)
- ⚠ <ambiguity / approximation / where the model breaks>

## Check yourself                 (Full mode only)
1. <question answerable only with real understanding>
```

Express mode emits: one sentence, gist, jargon table, honesty pass.

## When NOT to fire

- The document is already plain — the user wants it *shorter*. That's a summary, not a translation.
- The user wants persuasive or marketing framing. This skill optimizes for *understanding*, not for selling.
- Making it simpler would require stating something false and there's no honest simplification available — say so explicitly rather than forcing it.
