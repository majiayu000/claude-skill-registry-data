---
name: unhobble
category: governance
description: >
  Audit and rightsize a context surface — CLAUDE.md, AGENTS.md, a SKILL.md, a
  system prompt, or a single prompt — against the Claude-5 context-engineering
  reversals. Measures the surface (token budget, how much of it is phrased as
  hard rules vs judgment, near-duplicate sections, contradiction candidates,
  filesystem-derivable content, progressive-disclosure gaps), then adjudicates
  each section keep / relocate / delete using a grounding-aware predicate:
  prose backed by an independent mechanism is decorative and free to cut, prose
  that is the only carrier of a behavior is a real bet. Also rewrites prompts
  and skills from prohibition-form into judgment-form. Anthropic deleted >80%
  of Claude Code's system prompt for Claude 5 with no eval loss; this is the
  repeatable version of that cut. Use when: (1) a CLAUDE.md or AGENTS.md has
  grown and you want to know what is safe to remove, (2) an agent is ignoring
  or colliding with its own instructions, (3) a prompt is long and
  over-constrained and underperforming, (4) auditing a skill for
  over-constraint before publishing, (5) onboarding a repo whose agent context
  was written for an older model. Triggers on unhobble, rightsize, trim my
  CLAUDE.md, audit my CLAUDE.md, is my CLAUDE.md too long, context
  engineering, prune governance, over-constrained, improve this prompt, my
  agent ignores instructions, conflicting instructions, prompt too long.
---

# unhobble

Constraints written to protect against a weaker model's failure modes go
net-negative once the model's judgement exceeds the rule. They collide with
each other and with the user's actual request, and the model spends its
reasoning resolving the collision instead of doing the work. The correction is
deletion, not refinement.

Anthropic's Claude Code team removed **over 80% of Claude Code's system
prompt** for Claude 5 models with no measurable loss on their coding evals. The
diagnostic that started it: reading their own transcripts, they found
*"leave documentation as appropriate"* fighting *"DO NOT add comments"* inside
a single request.

This skill is that cut, made repeatable — and made safe, because the naive
version of the rule deletes load-bearing prose.

## The measure-then-adjudicate split

The script measures. It never says "delete."

Whether a rule can go depends on whether something *other than the prose*
enforces it — a hook, a CI job, a test, a runtime check. That is a grounding
question, and a regex answering it would be guessing in a confident voice. So:

```bash
python3 scripts/context_audit.py <path> [<path>...] --repo-root <repo> --budget 5000
python3 scripts/context_audit.py --prompt-file draft.md      # prompt mode
python3 scripts/context_audit.py <path> --json               # machine-readable
```

You get per-section tokens, directive form, a **rules-ratio** (share of
directives phrased as hard rules), near-duplicate clusters, contradiction
candidates, derivable-content flags, and anchored-candidate marks — paired with
a firing column that stays unresolved until a probe says otherwise. Then you
adjudicate.

The rules-ratio counts *uses*, not *mentions*: a quoted rule and a description
of what a script does are not directives. Without that distinction the surfaces
worth auditing score as pure prohibition merely for quoting the rules they
propose to delete.

## Adjudication

Classify every section against the mechanism that enforces it, not against how
important it sounds. Detail and worked examples in
[`references/adjudication.md`](references/adjudication.md).

| The prose is… | Action |
|---|---|
| **anchored, probed** — a mechanism produces the signal, and a probe receipt attests it fires *for this rule* | **delete the prose, keep the mechanism.** Free. Zero behavior change. |
| **anchored candidate, unprobed** — the mechanism exists; nothing shows it fires | **confirm before cutting** — [`references/mechanism-probe.md`](references/mechanism-probe.md). Free only once it comes back green. |
| **not a check** — descriptive, or derivable from the filesystem | **relocate** behind progressive disclosure. Free. |
| **only carrier, high value** | **keep** — and label it a heuristic, not an invariant. Or spend the effort to anchor it. |
| **only carrier, redundant or unused** | **delete.** |

The probed-anchored and not-a-check tiers are usually most of the volume and
cost nothing to cut. Deleting an only-carrier section is a real behavioral bet —
the article does not license it, and neither does this skill.

Two ways to claim the top tier wrongly. A rule that *cites* a mechanism is not
thereby anchored: `AGENTS.md` existing enforces nothing, which is why the script
ignores markdown references. And a mechanism that *exists* is not thereby
firing — three hooks in the workspace this predicate came from were registered,
scheduled, independent of the agent, and emitting nothing. A third: a probe
receipt is an *attestation* the script cannot verify, so an actor that writes
its own receipt has proved nothing. Have a runner emit it.

## The six reversals

Applied when rewriting whatever survives. Each with a before/after in
[`references/reversals.md`](references/reversals.md).

| Then | Now |
|---|---|
| Give rules | Let the model use judgement |
| Give examples | Design interfaces — an expressive parameter hints its own usage |
| Put it all upfront | Progressive disclosure — skills, deferred tool loading |
| Repeat yourself | One description, on the tool |
| Memory in CLAUDE.md | Auto-memory |
| Simple specs | Rich references — HTML artifacts, test suites, rubrics, real code |

The canonical rewrite — a comment-style prohibition replaced by *"Write code
that reads like the surrounding code: match its comment density, naming, and
idiom"* — is quoted in full in the reference, along with why the judgement
frame is both shorter and broader. It lives in one place on purpose; reversal 4
applies to this skill too.

## Working shape

1. **Measure** — run the script over every always-on surface at once, so
   cross-file duplication and contradictions are visible. A surface audited
   alone hides its collisions with its neighbours.
2. **Adjudicate** — walk the section table, assign each row a tier. An anchored
   candidate owes two answers before it is free: does the mechanism fire
   (probe it), and does its signal lie outside the governed actor's reach
   (`keel`).
3. **Cut and rewrite** — delete the probed-anchored and not-a-check rows,
   rewrite survivors into judgement form, move detail behind references.
4. **Verify** — re-run the script. Budget down, rules-ratio down, contradiction
   count down. Then confirm behavior held: the deleted rules were either
   enforced elsewhere or genuinely unwanted.

Step 4 is where this earns its keep. A cut that lowers the token count while
silently dropping a behavior nothing else enforces is a regression wearing a
green number — so state, per deleted section, which mechanism now carries it.

## Prompt mode

Same reversals, one prompt. `--prompt-file` or `--prompt-text` reports length,
directive mix, examples, and internal contradictions; the rewrite is yours.
Prompts fail the same way governance files do — a stack of prohibitions
accumulated from past failures, several of which now fight each other and none
of which the model still needs.

## What the script cannot see

The contradiction pass is **lexical**: it pairs a hard rule with a soft
allowance when they share a topic word. Conflicts worded in different
vocabulary are invisible to it. A real example, from a review prompt this skill
was tested on:

> "Do not comment on formatting — the formatter handles that."
> "Feel free to note style concerns where appropriate."

Those collide, and the script reports nothing, because *formatting* and *style*
share no token. So read the surface yourself for semantic conflicts; a zero in
that column means none were **lexically** detectable, not that none exist.

Same caution on the other columns. `derivable` and `anchored_candidate` are
heuristics over shape. The rules-ratio counts sentences, so one dense paragraph
of judgement can outweigh ten terse prohibitions. The numbers are there to
direct attention, not to substitute for reading.

Two hard limits worth knowing rather than discovering. Near-duplicate detection
compares section pairs exhaustively, so it is quadratic in section count —
above 2500 sections the heaviest are compared and the report says how many were
skipped. And `anchored_candidate` reports only that a referenced file *exists*,
tagged `repo` / `user` / `command` scope. Firing is a separate column, `Fires?`,
which stays `?` until a probe receipt resolves it — nothing about a file's shape
says whether it emits a signal.

## Scope

Governance surfaces, skills, system prompts, prompts. Not code comments, not
user-facing copy, not README prose for humans.

Related: `keel` measures whether verification is anchored (this composes it for
the tier-1 call); `/doctor` is the vendor's rightsizing pass and knows nothing
about your mechanisms; `harness-engineering-playbook` builds harness surfaces
where this one prunes them.

## Anti-rationalization

| Excuse | Reality |
|---|---|
| "The rule is important, so keep it." | Importance is not the predicate — enforcement is. An important rule that a hook already enforces is still decorative *prose*. Delete the prose, keep the hook. |
| "Token count went down, done." | A lower number with a silently dropped behavior is a regression. Name the carrier for every deletion. |
| "It's only 400 tokens." | It is 400 tokens on *every* request, competing with the user's actual ask, and colliding with its neighbours. |
| "I'll just tighten the wording." | The finding was that refinement is the wrong move. If judgement now exceeds the rule, the rule goes. |
| "The script didn't flag it, so it's fine." | The script flags *shape*, not correctness. Zero contradictions means none were lexically detectable. |

## Flags

| Flag | Effect |
|---|---|
| `--budget N` | always-on token target (default 5000) |
| `--split-threshold N` | tokens above which a surface is expected to defer (default 2500) |
| `--dup-threshold F` | Jaccard floor for near-duplicate pairs (default 0.25) |
| `--max-contradictions N` | cap on emitted candidates (default 20; the report states the true total) |
| `--repo-root DIR` | root for mechanism-reference existence checks |
| `--probe-receipts F` | JSON probe results, keyed by the literal backticked ref and scoped with `covers`; without it every anchor stays UNRESOLVED |
| `--fail-on-unmatched-receipts` | exit 1 when a receipt key or `covers` entry names nothing |
| `--json` | machine-readable report |
| `--fail-over-budget` | exit 1 when over `--budget` (surface mode only) |
| `--max-rules-ratio F` | exit 1 when the hard-rule share exceeds F |

The two exit-code flags are opt-in for a reason. By default this is a report,
not a judge — it exits 0 whatever it finds. Only with a gate flag does a CI
step running this command actually enforce anything; without one, such a step
is a claim of enforcement rather than the thing itself, which is the exact
confusion the adjudication table exists to resolve.

## Validation

`tests/` covers segmentation, polarity classification, shingle duplication,
contradiction pairing, the anchored-candidate rule — markdown references stay
unanchored, since a citation carries no enforcement — and the probe states,
including that a receipt with no negative control stays `incomplete`.

Dogfood: CI audits this skill's own `SKILL.md` under `--max-rules-ratio`, so
the skill fails its build if it drifts into the prohibition style it argues
against.

## References

- [`references/reversals.md`](references/reversals.md) — the six reversals with before/after.
- [`references/adjudication.md`](references/adjudication.md) — the tier table, worked, with the keel receipt.
- [`references/mechanism-probe.md`](references/mechanism-probe.md) — the three-leg probe, with three hooks that existed and were dead.
- `research/entities/concept/unhobbling-over-constraining.md` — the concept and its provenance.
