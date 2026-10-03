---
name: better-options
description: |
  Pressure-test an option set before the operator picks. Catches an AI agent — this one included — conflating two separate problems into one menu, or quietly narrowing the field to a false dilemma that skips the boring option. Borrows debug-mantra's falsify-the-hypothesis rigor (disprove each option before trusting it) then ponytail's minimalism bias (of what survives, favor the smallest) to surface the option nobody named because it wasn't impressive enough.

  Trigger when an agent — this one included — or a user presents two or more options for a non-trivial engineering decision, especially when every option involves new abstractions, infrastructure, or a rewrite; when the framing sounds like "you have to either X or Y," "there's no way around it," or "we'd need to..."; or when the user asks "is that really the only way," "feels like you're overcomplicating this," "are these actually the same problem," or "what's the simplest version that still works." Also self-trigger internally before presenting any option menu on a complicated technical decision — pressure-test it before the menu ever reaches the operator.

  Do not trigger merely because two or more options are on the table — reach for it when the menu bundles separate concerns, omits a simpler path, or treats an assumption as unavoidable. Skip it when only one viable path exists and the menu is honest about that, when the choice is low-stakes and reversible (take-a-step-back's "lighter than it feels" territory), or when an option list already exists and the ask is just to compress it into a call — that's bottom-line's job.
---

# Better Options

Before the operator picks from a menu, check whether the menu is honest.

Two failure modes make an option set worse than useless: it silently **bundles distinct problems** into one set of choices (so every option is really "fix A and B together," and the cheap fix for A alone never gets named), or it presents a **false dilemma** — a field narrowed to the options an agent finds natural to reach for (new service, new abstraction, a rewrite) while the boring option that would actually resolve it sits off the list. Both failure modes look identical from the outside: a confident menu, plausible tradeoffs, nothing wrong that a skim would catch.

## Core idea

Two borrowed disciplines, applied in sequence to the menu itself rather than to a single plan:

1. **Falsify before trusting** (from [debug-mantra](../debug-mantra/SKILL.md)'s falsify and reproduce-as-ground-truth steps) — treat "these are the options" and "this requires X" as hypotheses, not facts. For the leading option, find the cheapest disproof and run it before building on top of the option. When that disproof is available through a tool call — grep, read the code, run the test, query the data — actually invoke it and cite what came back; a prose guess at what the check would probably show is not the same as having run it, and reads as a disproof without being one. A disproof only counts if it points to something concrete — a test, a command, an existing code path, an observable constraint, or a specific piece of missing evidence; "I considered it and it still seems right" is not a disproof. If no cheap disproof is available — nothing to grep, run, or read — say what evidence would supply one instead of skipping the step. If the option's justification doesn't survive a real attempt to knock it down, it doesn't belong on the menu.
2. **Favor the smallest survivor** (from [ponytail](../ponytail/SKILL.md)) — once options survive falsification, don't default to the most architecturally satisfying one. Actively check whether a config flag, an existing feature, a one-line change, or deleting code resolves the actual observed problem — not the theorized one.

An option **survives** falsification when its justification — the claim that *this option is necessary* to resolve the observed problem, not merely that it's *a valid way* to resolve it — holds up against a real attempt to disprove it; plausibility alone doesn't count. That distinction guards point 2 against becoming reflexive minimalism: the bias is toward the smallest *survivor*, not the smallest option outright. A small option that doesn't actually resolve the observed problem isn't a survivor, it's just small, and the bigger option that does survive should win instead.

The conflation check comes first, because it's the cheapest disproof of all: half of inflated option menus dissolve the moment you notice they're answering two questions at once.

## How this differs from the sibling skills

- **take-a-step-back** — "Am I making the best decision possible?" Challenges the frame of a single plan already in motion.
- **iron-triangle** — "Which of speed, cost, or quality am I trading?" Prices a trade once you're inside one option.
- **blast-radius** — "How big is the path I chose, what breaks, how hard to undo?" Sizes an option already picked.
- **bottom-line** — "There's too much here — what's the call?" Compresses an *honest* option list that's just too verbose.
- **better-options** — "Is this menu itself honest — one problem or several, and is the simplest real option even on it?" Fires *before* any of the above, at the moment the menu is assembled, not after one option is chosen or the analysis balloons.

If the menu is already trustworthy and just needs cutting to a call, hand off to bottom-line. If the menu is trustworthy and one option is chosen, take-a-step-back and iron-triangle pick up from there.

## Output format

Lead with what the menu actually is — whichever menu is under test: one an agent or user already stated, or the draft you were about to present yourself before self-triggering this check. Either way, run the check before any menu reaches the operator as a recommendation. Most decisions need only the core three lines.

**The menu:** [The options under test, in one line, plus the decision they're supposedly resolving.]

**Better-options check** — core:
- **Conflation:** [Is this one problem or several wearing one option set? If several, name the split — each sub-problem may have its own trivial fix.]
- **Falsified survivor:** [Walk the cheapest disproof of the leading option's justification. Does it survive? If it doesn't, say so plainly — that option is dead, not "worth keeping in mind."]
- **Simplest surviving option:** [Among what survives, the smallest fix that resolves the *actual observed* problem — config, flag, existing feature, one-liner, deletion — named explicitly, even if it wasn't on the original menu.]

Include these sections only when they change the recommendation:
- **Dropped option:** [The boring option that never made the list, and why it likely got skipped — usually because it isn't architecturally interesting, not because it doesn't work.]
- **False dilemma:** [Only two or three options were named, but a smaller move avoids the tradeoff between them entirely.]
- **What the bundle was hiding:** [When conflation is the finding, name what got obscured — usually the cheap fix for the smaller of the two bundled problems.]

**Do next:** [The smallest concrete action that tests the simplest surviving option — not "consider it," an actual step.]

**Missing:** [Only if a fact you don't have would change which option survives. Omit by default — don't use this field to dodge making the call.]

## Principles

**Check for conflation first.** It's the highest-leverage, cheapest question: "is this actually one decision?" A menu that quietly answers two questions at once inflates every option on it. The tell: options that differ in *what they're actually fixing*, not just in how — option A resolving problem X and option B resolving problem Y is a menu for two problems, not two approaches to one. The same tell applies inside a single option: one that bundles several changes with different risk and reversibility profiles (a "migration" that's really schema change plus data move plus app retooling) is a mini-menu of its own — split it before falsifying it as one thing.

**Disprove, don't just describe.** Don't list an option's tradeoffs and move on — try to knock the option's stated justification down. An option whose justification doesn't survive a real attempt at disproof shouldn't be presented as equally valid to one that does. When the disproof is checkable with a tool, check it — a plausible-sounding refutation that was never run is a description wearing a disproof's clothes.

**The smallest surviving option wins by default.** Complexity has to earn its place by surviving falsification, not by being the more thorough-sounding answer. When two options both survive, the smaller one is the recommendation unless something specific rules it out — name that thing if so.

**Name what a menu-builder would skip, not what's easy to defend.** New service, new abstraction, and rewrite are natural options for an agent to reach for because they're generically defensible. Config flag, delete, and one-liner require actually looking at the specific case — do that looking.

**Distinguish "harder to build" from "actually necessary."** The finding that matters is whether the small option resolves the problem that's actually happening, not whether it feels satisfying next to the more ambitious ones.

**One clean disproof beats a survey of every option's pros and cons.** Resist restating each option's tradeoffs symmetrically — that's bottom-line's job on an honest menu. Here, the job is deciding whether the menu itself deserves to stand.

## Scaling

- **Menu is honest, no conflation, options already minimal** → say so in one line and stop. Don't manufacture a finding — a clean menu is a valid outcome, not evidence the skill missed something. ("Minimal" means no option on the menu can be reduced further and no omitted option is both smaller and sufficient — not that the list is short.) *e.g. "The menu holds: one problem, genuinely viable options, no simpler path missing. Proceed with the stated choice."*
- **Menu is honest but large or overwhelming** → don't just stop silently. Say so and hand off explicitly: "the menu is honest — run bottom-line to cut it to a call." Size, not honesty, is bottom-line's problem to solve.
- **Conflation found** → lead with it; it's usually the whole finding. The falsified-survivor and simplest-option lines then apply per sub-problem, not to the original bundle.
- **False dilemma found (menu is honest about being one problem, but narrow)** → lead with the dropped option and why it got skipped.
- **Only one option is presented, framed as inevitable** ("we have to," "there's no way around it") → treat the necessity claim itself as the hypothesis to falsify. The check still applies with a menu of one — conflation and survivor collapse onto that single option's justification. See Example 3.
- **High-stakes / expensive-to-reverse decision** → add the "What the bundle was hiding" or "False dilemma" line explicitly, and treat "Do next" as a real spike, not a suggestion.
- **User already ran their own falsification and it holds** → confirm briefly and defer; don't re-litigate a check that already happened.
- **Simplest survivor rejected for non-technical reasons** (strategic direction, team skill-building, architectural consistency) → the recommendation stands as stated; the rejection makes it a documented *choice* rather than an oversight. Don't re-litigate a reasoned override.

## Example 1 — a conflated bug report

Input (abridged): An agent reports, "This flaky test needs either a rewrite of the fixture harness or a retry wrapper around the assertion — the harness doesn't isolate state well enough for a single fix."

Output:

> **The menu:** Rewrite the fixture harness, or add a retry wrapper — to fix one "flaky test."
>
> **Better-options check:**
> - **Conflation:** This is two failures wearing one bug report. Test A fails on a timing race; Test B fails from a global left dirty by a prior test. They only look like one flaky test because they run in the same file.
> - **Falsified survivor:** The harness-rewrite justification claims neither test can be isolated without structural change. Disproof: Test B's failure disappears the moment its shared global is reset in teardown — no harness change needed, and Test A never touched that global.
> - **Simplest surviving option:** Add one `afterEach` teardown call that resets the shared global (fixes Test B). Test A's timing race needs its own look — likely a `waitFor` instead of a fixed sleep, not a harness rewrite either.
>
> **Dropped option:** A one-line teardown call was never on the table because the report treated both failures as one symptom needing one structural fix.
>
> **Do next:** Add the teardown reset, rerun both tests in isolation to confirm Test B is the one that clears, then look at Test A's wait condition separately.

## Example 2 — a false dilemma from scale anxiety

Input (abridged): "We're hitting load limits — we should either migrate to Postgres or shard the current MySQL instance."

Output:

> **The menu:** Migrate to Postgres, or shard MySQL — to fix a load problem.
>
> **Better-options check:**
> - **Conflation:** None — this is genuinely one problem (load), not two bundled together.
> - **Falsified survivor:** Both options assume the current schema/indexing is already load-bearing-efficient and the ceiling is structural. Disproof: the slow endpoint runs an unindexed query scanning the full table on every request — that's a single missing index, not a capacity ceiling.
> - **Simplest surviving option:** Add the missing index. Neither migration nor sharding is justified until load is retested against an indexed query.
>
> **False dilemma:** Migrate-or-shard were the two options an agent under scale pressure reaches for by default; "check whether the query is even indexed" isn't architecturally interesting, so it never made the list.
>
> **Do next:** Add the index, rerun the load test, and only revisit migrate-vs-shard if the ceiling persists against an indexed query.

## Example 3 — a menu of one, framed as inevitable

Input (abridged): "We have to rewrite the scheduler — the current one can't handle backpressure."

Output:

> **The menu:** Rewrite the scheduler — the only option offered, framed as required.
>
> **Better-options check:**
> - **Conflation:** None — one problem (the scheduler can't handle backpressure), one option.
> - **Falsified survivor:** The necessity claim is "the current scheduler *cannot* handle backpressure." Disproof: dropping `max_in_flight` from 100 to 10 keeps the queue inside its buffer under the same load test that motivated the rewrite — the current scheduler handles backpressure once the concurrency ceiling is configured correctly. The rewrite's justification does not survive.
> - **Simplest surviving option:** Lower `max_in_flight` to a value the buffer actually supports and rerun the load test. A rewrite isn't justified unless this fails.
>
> **Do next:** Change the config value, rerun the backpressure test that motivated the rewrite claim, and only revisit the rewrite if it still fails.
