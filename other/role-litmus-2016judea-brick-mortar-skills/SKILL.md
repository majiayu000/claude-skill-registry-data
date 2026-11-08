---
name: role-litmus
description: Run a grounded customer persona against your live product — a site, a tool, a downloadable file — as a real-life litmus test of whether that role would actually use it instead of what they use today. Five passes (cold arrival from one phone screenshot, cognitive walkthrough of their top task, the file test, a four-forces switch verdict against a named incumbent, a ranked Kano want-list) with rules that counter the documented failures of synthetic personas (median answers, sycophancy, unranked needs). Use when you say "run the personas", "litmus test the site", "would a <role> actually use this", "what data are we missing", or "is this page confusing".
---

# Role litmus

**Be the customer this role actually is, arrive the way they arrive, attempt the task they actually
have, open the file you actually serve, and default to walking away.** Not a code review and not a
design review. The question is whether this role would use it instead of the incumbent they
already pay for.

**Done when:** a dated run record exists with a verdict that was not assumed and at least one
finding that names **a step, a column or a quote**. A run that produces only impressions has
failed, not passed.

## Why the rules exist

Synthetic personas have a documented failure record: they converge on the median answer, they are
trained to agree with the framing they're given, they rank nothing, and their failure state is a
clean bill of health. Read `references/paradigms.md` before your first run; it carries the
citations. The finding that shapes everything: **synthetic personas are good at audits and bad at
context.** Point them at what can be checked.

## Rule 0: the persona is blind to the repo

A critic who has read *why* a card is empty will rationalise it.

- **Preferred: a blind subagent.** Give it exactly four things: the persona file, the pass protocol
  below, the screenshots, and the downloaded file. Not your docs, not your build scripts, not
  your memory or CLAUDE.md. Its report is the pass output.
- **Fallback: order of operations.** Write passes 1-5 **before** opening any file that explains the
  product. Then reconcile.
- **Already contaminated?** Say so in the run record and name the passes it touches (mostly pass 4:
  knowing the reason for a gap is how you excuse it).

## The personas

One file per role in `personas/`, from `personas/TEMPLATE.md`. Ground each in the role's own
public voice (forums, subreddits, trade press) with permalinks; see `reddit-mining`. Two traps:

- **A forum that looks right can be the wrong population.** An "appraisal" forum can be mostly
  residential when your role is commercial; a "business broker" forum is the sell side when your
  persona is the buyer. Check, and say which population the persona is drawn from.
- **Derive the role list from the product, not from a table that can go stale.** If your page
  lists roles, read them off the page or the build every run.

## The five passes

Run in order; write each before starting the next.

### Pass 1 · Cold arrival: is anything here for me?
Load the page as they arrive: on a phone (390x664, mobile + touch), from the link they'd tap
(with its UTM if your page varies by source). Screenshot. From **that screenshot alone, before
scrolling**: What is this (in their vocabulary, §4)? Is anything here for me? What do I do next?
Anything that needs a scroll is a finding. Then shoot 1440x900 too: phone-only passes hide wide bugs.

### Pass 2 · Cognitive walkthrough: where do I get lost?
Take the persona's **#1 task** (§2), not a feature from your menu. Walk it end to end (home ->
entry point -> the tool or file -> the result). At every step ask the four questions:
1. Will I try to achieve the right effect?
2. Will I notice the correct action is available?
3. Will I associate the action with the effect I want?
4. After acting, will I see that progress was made?
Every **no** is a finding naming the step. A "no" on Q1 at the first screen is the most expensive
finding there is. Screenshot every step; drive it, don't narrate it.

### Pass 3 · The file test: does the output answer the promise?
The pass that is not an opinion. Download or capture exactly what the product serves (CSV, report,
API response). Against the page's own promise:
1. Does it answer the question the page asked, column by column?
2. Is there a column whose meaning can't be guessed from its name (open it in the tool the persona
   uses, §3, not a JSON viewer)?
3. Is there a blank that reads as a zero? The most dangerous shape in a file someone prices from.
4. Does the row count match the claim?
5. Can the persona do the job with their real skill ceiling (no code, no joins if they can't)?
6. Can it be pointed at one thing they care about (one address, one company)? A filter that can't
   is a menu.
Missing data found here is a fact; missing data imagined from the page is a guess.

### Pass 4 · The switch test: would they actually change?
Four forces against the **named incumbent** (§3):

| Force | What to write |
|---|---|
| Push | what's wrong with what they do today (sourced, not invented) |
| Pull | what yours gives that theirs doesn't (quoted from the page or the file) |
| Anxiety | what stops them trusting yours: no update date, unnamed provenance, an unexplained coverage % |
| Habit | what's in their workflow and what switching costs |

**The verdict starts at `no change` and must be moved** by a quotable line from the page or a
specific column in the file. Verdicts: **switch** (stop using the incumbent for this task),
**supplement** (use it alongside, for a named task), **no change** (wouldn't open it twice).
`supplement` is the honest ceiling for most roles. `switch` against an expensive incumbent, claimed
without a quote, is sycophancy showing.

### Pass 5 · The want list
**Capped at three, ranked, Kano-classed** (must-be / performance / delight / indifferent). A flat
list is discarded. Then the **won't-use list** from §6, each with its reason. Never ask the persona
what it wants in the abstract; derive wants from a task it already does and a tool it already pays
for.

## The five rules

1. **Blind to the repo.** A critic who has read the reasoning rationalises the decision.
2. **No hypotheticals.** Every behavioural claim cites past behaviour (a permalink, a tool they pay
   for). "Would you use this" produces a polite lie from synthetic and real respondents alike.
3. **Refusal is the default verdict.** The model is trained to agree with the framing.
4. **Ranked and capped at three.** Unranked needs are the documented failure.
5. **A finding names a step, a column or a quote.** "The page is confusing" can be neither fixed nor
   dismissed.

## Reconcile (after the passes, not before)

Now read the builder and your docs. Check: does a missing-data finding land on something you've
labelled "coming soon" for a reason that isn't the real reason? Does a finding contradict a limit you
publish? Reconciliation may **kill** a finding (the column exists; the persona misread it) or
**promote** one. It never softens a finding because the reason is understandable.

## Output

`litmus/YYYY-MM-DD-<role_id>.md`:

```markdown
# <Label> — litmus, YYYY-MM-DD
**Verdict:** switch | supplement | no change — one sentence, with the reason.
**Blind:** subagent | order-of-operations | CONTAMINATED (passes)
## Findings
| # | Sev | Pass | Where | Finding | What would fix it |
(severity: blocks the task / degrades it / cosmetic)
## Want list — ranked, capped at 3, Kano-classed
## Won't use — with reasons
## Frame findings — FENCED. Ignorable.
## Sources
```

Frame-level findings (the overall navigation or positioning) go in the fenced section as notes, never
proposals or edits. The front door has a high bar; quarantining respects it without censoring the
persona.

## Cross-role synthesis

After several roles: **what more than one role asked for is the build-queue signal; what one role
asked for is a curiosity.** Write a dated synthesis file.

## Traps

- **Nothing here edits the shipped product.** Findings are findings.
- **Forum posts are voice, never a number.** Unknown n, self-selected. Never "X% of brokers say".
- **A persona is not a demographic sketch.** No invented name, age or hobby. The job, the tasks, the
  toolstack, the vocabulary, the refusals.
- **Don't run it against a live campaign** without excluding your QA traffic from analytics.
- **Re-run rather than revise.** Dated run records are the proof a fix worked.
