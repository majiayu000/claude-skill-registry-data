---
name: function-signature-and-parameter-guidance
description: |
  Design and review caller-facing names and contracts: functions, tools, commands, CLI flags,
  parameters, config keys, env vars, profiles, event types, and node/edge identifiers.
  Check names, descriptions, help, docstrings, schemas, defaults, bounds, units, errors,
  outputs, mutation, and whether values reach behavior.
  Use when asked to "name a parameter", "parameter naming", "name this tool or command",
  "choose a flag, option, or config key", "design an options object", "one tool or two",
  "bool or enum here", "name a profile, field, event, node, or edge",
  "make names clear and unambiguous", "check ISO, platform, or language naming",
  "audit CLI/MCP/JSON-Schema help", "define accepted values or defaults",
  "what should this return on failure", "rename this without breaking callers",
  "improve an error message", "why did the caller pass the wrong argument",
  "why did this parameter do nothing", or "red-team these descriptions".
  Not for local variables, general prose, README copy, release notes, or commits.
---

# Function Signature and Parameter Guidance

<purpose>

A tool or parameter has four visible parts: its **name**, the **description** that teaches it,
the **error** when a caller gets it wrong, and the **behavior** matching all three. Callers are
increasingly AI agents reading a schema once and guessing, so merely *not wrong* still produces
wrong calls. Aim for text that makes the wrong call hard to write, and behavior that fails
loudly when it happens anyway.

**The failures that matter most return success** — a parameter validated, clamped, echoed, and
never used looks correct at every observable layer. So verify behavior matches the text (Group
B passes) before checking the text is right (Group A).

**An example gets read as the whole universe rather than as one case of a general principle.**
That is true of the caller reading your description and of you reading these checks, so the
words must state the concept explicitly — examples alone are not enough. Make the concept
behind the concept explicit, or it is missed entirely. **Apply this to this document too:**
every case named below is one instance of its rule, never the rule's limit.

</purpose>

<workflow>

## The Process

Correctness before brevity, always — trimming a wrong sentence produces a shorter wrong
sentence.

1. **Survey the codebase's existing vocabulary, then applicable standards.** Grep the
   schema and CLI (a code-graph tool such as `search_graph` or `kit symbols` does the same
   faster when the session has one). Two targets: **conventions** — sign, units, naming, what `0`
   already means, since a value's meaning comes from its siblings rather than first
   principles; and **semantic duplicates**, of a parameter (`limit` beside `max_results`) and
   of a whole tool — state each job in a sentence and look for matches, the tell being a
   parameter selecting behavior another tool provides. Extend what exists, or say how each
   differs from its near-twin where the caller reads. Then check governing ISO/domain,
   platform/protocol, and language naming conventions before inventing a name.
2. **Inventory every entry point.** Grep the name across CLI, schema, bindings, config; fix
   all paths. A message correct in one path is routinely bypassed in another.
3. **Trace parse to use.** Text review on a silently ignored parameter is wasted.
4. **Answer the Disambiguation Checklist.**
5. **Write the failing test first**, at the layer that validates; assert the *effect*, not the
   absence of an error; confirm it fails for the expected reason.
6. **Fix, deriving text from the source of truth** wherever names are listed.
7. **Run the passes** — Part 2, Group B first.
8. **Brevity.** Measure, justify outliers, cut no required fact. Lead with the distinguishing
   fact, since tails truncate. Keep a restatement when the reader lacks the original (A8).
9. **Regression-lock.** Assert the *absence* of banned phrasing, not only the presence of the
   good. Presence-only tests let bad wording return alongside.

</workflow>

<requirements>

## The Four Facts

Every parameter description states, and every error message restates:

1. **What the value selects** — not what the field is typed as.
2. **The accepted range**, spelled out as accepted values.
3. **What each notable value does**, including every value the convention gives special
   meaning (`0`, negatives, empty, absent).
4. **What to pass instead**, when rejecting.

Error template:

```
<name> must be <accepted range>, got <value>; <what to pass and what it selects>
```

Worked example:

```
limit must be 0 or greater, got -5; pass a positive count, or 0 for every match
```

Five parts, because fact 4 splits in the message: name, bound, offending value, corrective
action, what the correction selects. Drop any one and the message becomes guessable rather
than actionable.

## Naming Rules

1. **The name says what the value selects.** `transcript_lines` beats `n`, `max`, `size`.
2. **Put the unit in the name.** `preview_chars`, `timeout_ms`, `lines_per_message`. A unit
   in the name survives truncation and paraphrase; one in the description does not.
3. **One concept, one name, every surface.** CLI flag, schema key, kwarg, and config key all
   agree. Divergent names read as different features.
4. **Establish a sign convention once, then honor it everywhere.** If negative means "from
   the end" on one parameter, it means that on all of them — and every signed parameter
   states all four cases (positive, negative, zero, omitted).
5. **State bounds as accepted values, never as absences.** "0 or greater" beats "not
   negative". Negations invert under paraphrase.
6. **Never use math jargon for a bound.** Whether "natural numbers" includes `0` is disputed,
   and `0` is usually the load-bearing value.
7. **Never imply a cost the code does not have.** `snapshot`, `sync`, `rebuild`, `flush`,
   `clone`, `export` all make callers avoid or schedule around a call.
8. **Only name a parameter the caller can set on *this* entry point.** The most common
   accuracy bug in otherwise-helpful guidance.
9. **Derive lists from the source of truth.** An "accepted values" list written as a literal
   drifts. Build it from the structure the dispatcher reads.

## Disambiguation Checklist

Answer all twenty for each tool and parameter. An unanswerable question is a design flaw, not a
documentation gap. The right column names the pass or rule that verifies each answer against
the implementation; answering is yours.

| # | Question | Verified by |
|---|---|---|
| 1 | Does an existing parameter or tool already do this? | A2 |
| 2 | Can the value read as both a count and an index? | A5 |
| 3 | What does `0` do, and does that match its natural reading? | A5 |
| 4 | What does a negative do, and how many items come back? | A5 |
| 5 | Inclusive or exclusive bound? | A5 |
| 6 | What does omission do, and does empty differ? | A6 |
| 7 | What unit, and is it in the name? | rule 2 |
| 8 | Changes which results, or only how they show? | B1 |
| 9 | What does the count count, and in what order? | B5 |
| 10 | Out of range: rejected, clamped, or ignored — and is the effective value reported? | B1 |
| 11 | Does the value reach the behavior, or is it echoed and dropped? | B1 |
| 12 | Which parameters conflict, and what happens when both are set? | B1, B3 |
| 13 | Do listed features compose? Which pairs fail? | B3 |
| 14 | Is every example executed in CI? | B4 |
| 15 | Can a valid-but-wrong value look like a genuine miss? | B5 |
| 16 | Is there an input matching everything that a caller would reach for? | B5 |
| 17 | Does the name imply a cost the code lacks? | rule 7 |
| 18 | If a container: what do empty, absent, and unknown-key mean? Do members interact or override? | B1, B2 |
| 19 | Read cold: what can a stranger not answer? | A9 |
| 20 | Can the caller predict the response shape and know whether it mutates? | B8 |

If a question does not apply, say why in one line. "Not applicable" without a reason is where
concepts get dropped silently.

## Generalizing Beyond the Examples

**The generative rule:** each check asks whether a caller can predict the behavior from type,
name, and description alone. Wherever those under-determine it, the check applies.

**Name the concept before ruling a check out.** The common miss is dismissal by type — *this
one is an enum, not an integer*; *this one is a high-level object* — which skips the concept
entirely and reports clean. Ask what the check is *for*, then whether this parameter can fail
that way.

**In what you write, that means stating the range rather than a sample.** `"e.g. 5"` teaches
nothing about `0` or `-1`; `"a positive count, or 0 for every match"` teaches the whole space.

| Check names | Concept | Also covers |
|---|---|---|
| signed integers | the type hides the value space | `auto`/`default` enum members, sentinels (`""`, `"*"`, `"all"`), tri-state booleans, `0` as epoch-or-unset |
| does the value reach the behavior | *accepted* versus *honored* | structs nobody reads, options merged then overwritten, env vars read once at startup |
| names a parameter the caller cannot set | points where the reader cannot reach | a config file they cannot write, a flag behind a toggle, a method on an object they do not hold |
| empty results are ambiguous | one output covers success and user error | `0` counts, `null`, empty lists, default-valued structs, exit 0 with empty stdout |
| do listed features compose | documented capability exceeds tested surface | capability matrices, format × mode combinations, flag pairs |
| a check phrased for one scalar | a container is a namespace, holding *more* ambiguity | options objects, config blocks, nested structs — every rule applies to each member and to the container (empty? absent? unknown key?) |

</requirements>

<pitfalls>

## What to Avoid

1. **Testing acceptance, not effect** — "no validation error" passes on every silent-ignore bug.
2. **Clamping quietly** — reject, or report the effective value and say it was clamped.
3. **Fixing one code path** — validation guards and dispatch arms drift independently.
4. **Trusting a grep hit as a finding** — short parameter names are usually common English words
   ("limit", "context", "offset", "summary"). Verify each.
5. **Rolling back when tightened validation breaks tests** — those failures usually expose
   pre-existing drift. Read them first.
6. **Deferring as "disproportionate at release time"** — before first publish there is no
   compatibility surface to protect.
7. **Optimizing validation before measuring** — cost is `Ω(k)` in supplied keys, never
   sublinear; a measured typo-rejection round trip ran ~50–60 µs, below the cost of a cache.

Mistakes made while *doing* the review, all observed: testing at a layer that skips validation;
assuming red means the code is wrong when the assertion miscounted; suppressing stderr and
reading the empty output as a result; auditing a build older than your branch; claiming files
diverged without diffing; blaming the tool before re-reading your invocation. Part 2 tabulates
twelve with corrections.

</pitfalls>

<resources>

## References

1. **`references/designing-and-reviewing-signatures-and-parameters.md`**
   1. **Part 1 (design)** — the 8 shapes ambiguous by construction: signed integers,
      inclusivity, empty-vs-absent-vs-null, filter-vs-presentation, pagination and ordering,
      units, no-op filters, containers. The reasoning behind the checklist.
   2. **Part 2 (audit)** — passes B1–B8 then A1–A9, each with the defect justifying it, plus
      process failures, reporting template, regression-lock shape.
   3. **Part 3 (fix)** — the remediation ladder; serializer defaults that discard unknown input
      before any suggestion runs; what each language and boundary permits; algorithm choice
      with thresholds and tie-breaks; libraries per language.
2. **`references/mcp-specifics.md`** — everything protocol-particular, kept out of the passes
   so they stay surface-agnostic: the four declarations a tool should carry, `ToolAnnotations`
   with its defaults and conditionals, the two error channels, a live-server audit recipe, and
   a three-server comparison.
3. **`references/sources.md`** — specifications verified versus cited-but-unverified, observed
   defects with commit and session identifiers, discrepancies, naming decisions.
4. **`tests/test_check_schema_descriptions.py`** — 20 tests, pinning every bug the checker has
   shipped: a false clean bill on zero input, nested parameters skipped under a type union, a
   case-sensitive enum check, and severity tiering.
5. **`scripts/check-schema-descriptions.py`** — JSON Schema and MCP `tools/list` only, any
   server language, since it reads protocol output rather than source.
   1. Per parameter: negation, unstated sign, undocumented default, undocumented enum value,
      vague words, length.
   2. Per tool: permissive schema, missing outputSchema, missing annotations, overloaded names,
      divergent descriptions.
   3. Tiered by severity and named rather than numbered, so renumbering cannot break it. Reads
      no clap/argparse/click/cobra definitions, `--help` output, config files, or docstrings —
      use the passes' grep recipes there. A clean run is not a clean review: the passes it
      skips catch the failures that return success.

</resources>
