---
name: answer-first
description: Output contract for this repo — lead with the answer, number every procedure, and delete filler. Use when writing any operator-facing response, report, PR body, or handoff note. Origin - the "I Have ADHD" pattern, adapted to this monorepo.
triggers: operator-facing response, report, pr body, handoff note, lead with the answer, number every procedure, delete filler, output contract
---

# Answer-First Output Contract

The operator reads on a phone, mid-task, usually while something is
broken. A response that buries its answer in paragraph three has failed
regardless of how correct paragraph three is.

`AGENTS.md` / `CLAUDE.md` already say "be direct." This skill is the
mechanical version: exactly what to cut and what shape to use.

## The three rules

1. **First sentence = the answer.** Not the restated question, not the
   plan, not "I looked into this." If the answer is "no", the first word
   is "No". If a command failed, say what failed before why.
2. **Anything procedural is numbered.** Steps, ordered fixes, apply-then-
   verify sequences. Never a wall of prose the operator has to re-parse
   into steps at 11pm.
3. **Every claim carries its receipt inline.** "Tests pass (417 files,
   4,670 passed, exit 0)" — not "tests pass". A number the operator can
   check beats an adjective they have to trust.

## Kill list — delete on sight

| Pattern | Why it dies |
|---|---|
| "Hope this helps!" · "Let me know if you need anything else!" | Zero information, costs a line |
| "Great question!" · "You're absolutely right!" | Flattery, not content |
| "I'd be happy to…" · "Let me go ahead and…" | Narrating intent instead of stating result |
| "In today's fast-paced world" · "It's worth noting that" | Filler throat-clearing |
| Restating the request before answering | The operator wrote it; they know |
| "As mentioned above" | If they need it twice, say it once, in the right place |
| Dramatic one-line fragments for emphasis | AI tell (see `unslop` / `avoid-ai-writing`) |
| Arrow chains — `A → B → fails` | Reads as shorthand, not explanation. Use a sentence |

## Shape

- **Status update:** one screen. Outcome, evidence, what's next.
- **A PR's CI state:** the tally from `gh pr checks <n>` read in THIS turn
  (`13 pass · 1 fail (node, cancelled) · 2 skipping`), naming every non-pass
  check. "Merged when green" and "CI running" are not statuses; the tally
  is. Witnessed 2026-09-15: the operator had to say "looks red" twice and
  "red too" once for PRs I had just reported on from memory.
- **Findings:** table for enumerable facts; prose for the reasoning
  around it. Never put reasoning inside table cells.
- **A failure:** what broke, the actual error text, what you tried, what
  you need. In that order.
- **A question to the operator:** the question first, options second,
  your recommendation labeled as such.

## Hard constraint that outranks brevity

Being readable beats being short. If cutting words forces the operator to
re-read or ask a follow-up, the cut lost. Compress by **dropping whole
items that don't change what they do next** — never by compressing
sentences into fragments, abbreviations, or jargon.

## When NOT to use

Brainstorming, prose drafts, teaching explanations, or anywhere the
operator explicitly asked to think out loud — answer-first flattens
exploration into a verdict, which is the wrong shape for those.
Related: `beautiful-prose` for long-form, `concise-planning` for
checklists, `unslop` / `avoid-ai-writing` for stripping AI tells from
finished text.
