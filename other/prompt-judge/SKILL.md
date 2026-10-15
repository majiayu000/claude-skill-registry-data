---
name: prompt-judge
description: Compare an old prompt and a new prompt on the same inputs, side by side, and find out whether the change helped and whether it broke anything. A pairwise Claude judge reads both outputs for each input and answers A, B, or tie, once in each order, so a judge that favors whichever output comes first cannot fake a win. It reports wins, losses, and ties per rule, plus a regression list of every case where the new version got worse on a must-never rule, even when it wins overall. The judge is tested with planted mistakes and identical pairs before its verdicts count. Trigger on "compare two prompts", "old prompt vs new prompt", "did my prompt change help", "A/B test my prompt", "is the new version better", "did this change break anything", "regression test my prompt", "pairwise judge", "side by side eval", or any moment a prompt, skill, or agent instruction is about to be replaced by a new version. Part of the Judge Pack.
---

# Prompt Judge: did the change help, and what did it break?

## What this does
You changed the prompt. The new outputs look better. You read five of them and they are tighter, clearer, more useful.

Then it ships, and a week later someone finds the one thing the old version never did. The rewrite that fixed the format also started slipping a ready-to-send email into the brief. Nobody compared for that, because everybody was comparing for the thing they set out to fix.

This skill runs the old prompt and the new prompt on the same inputs and puts the outputs side by side in front of a Claude judge, one rule at a time. For each input and each rule, the judge answers A, B, or tie. Then it asks again with the two outputs swapped, because judges tend to prefer whichever one they read first. A winner only counts when it wins both times.

You get two answers. Did the change help, rule by rule. And a regression list: every case where the new version is worse on a rule it must never break or must always keep, even if it wins everywhere else.

**A judge is a prompt.** Before its verdicts count, it gets tested: pairs where you planted the mistake yourself, and pairs where both sides are the same output. If it cannot pick the clean side every time, or cannot call a tie on two copies of the same thing, it is not ready to referee your prompt.

**How this differs from `brief-prompt-skill`:** that skill grades one prompt on its own, against a checklist, and compares its pass rate to a naive one-line baseline. This one puts two real versions head to head on the same inputs, asks in both orders, tests the judge first, and lists regressions. Use `brief-prompt-skill` to write a prompt and get its pass rate. Use this one when you are about to replace a prompt that already works. It builds on `agent-judge`, which grades one output against one rule, pass or fail.

## Where this came from
Built in October 2026 while rewriting the prompt behind a research agent. The old version wrote long briefs where the decision sat at the bottom. The new version put the decision first. The question was whether the rewrite helped, and whether it quietly broke a rule the old version kept.

It was proven on the real outputs of both prompt versions, run on the same inputs, after a test set of planted mistakes and identical pairs showed the judges could be trusted.

What the build taught:
- **Asking in both orders caught a judge that would have lied.** On the zero tolerance rule, the small model kept naming the output that broke the rule instead of the better one, but only when the bad output came first. Asked once, that reads as a confident verdict. Asked twice, it shows up as a flip. That one rule moved up a model. The others stayed small.
- **Say what the letter means.** A judge reasoning about a rule that must never break tends to talk about the output that broke it, then answer with that output's letter. One plain sentence, "your answer names the better output", fixed most of it.
- **Show both sides the same cut.** The two versions wrote in different formats, so "can a rep act on the top of this" only works if the judge sees the same amount of each: the first few dozen words, nothing else.
- **Ask for the differences first.** A judge counting unsourced claims across two long outputs missed an invented number until the rubric told it to find where the outputs differ, check each difference, and then count.
- **Plant mistakes across every output.** The first version of the pair builder stepped through the outputs at a stride that skipped most of them, and planted every mistake of one kind into the same output. The trust test looked fine and proved almost nothing. The builder now reaches every output.

What it cannot do yet: it judges what is on the page. If both versions miss the same fact, the judge calls it a tie, and it cannot tell you a fact was missed at all. It also does no statistics. On a few dozen inputs, a difference of two wins is noise, so read the cases behind the counts.

## Try it in 60 seconds
A fictional sample ships with this skill: five account research briefs written by an old prompt and a new prompt, four briefs a person already reviewed, and three pairwise judges.

1. Copy the `scripts/` and `example/` folders from this skill somewhere you can run Python 3.10 or newer.
2. Install and set your key:
   ```
   python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
   export ANTHROPIC_API_KEY=...
   ```
3. Build the pairs and judge them:
   ```
   .venv/bin/python scripts/build_pairs.py --judges example/judges.py --old example/old --new example/new --reviewed example/reviewed --inputs example/inputs.jsonl --out pair-run
   .venv/bin/python scripts/run_pairs.py --judges example/judges.py --out pair-run
   ```
4. Open `pair-run/results/<time>/report.md`. Read the trust table first, then the regression list, then the wins.

The sample is 60 judge calls and costs about 15 cents.

**Your first exercise is already in the report.** The new prompt wins the rule it was written for, and still has a regression. Find it, decide whether it blocks the change, and write down why. That decision is the whole skill in miniature.

## What you'll need
- **Works today with**: saved outputs from both versions on the same inputs, named so the same input has the same file name in both folders. Ten inputs is a start. Thirty is better.
- **A few outputs you trust**: outputs a person already reviewed. They can come from either version. The trust test plants mistakes into copies of them.
- **Your rules, written down**: the ones a script cannot check. If you have never written them, run `agent-contract` first.
- **An Anthropic API key**: the judges are Claude models called through the Anthropic SDK.
- **Python**: the starter scripts install Ragas, pinned to versions that work together.

## How this runs at your connection level
The skill never depends on a connector. It runs on outputs you save to two folders.

- **Bring your data**: two folders of outputs, old and new, plus a few reviewed ones. You get a trust table, a win and loss table per rule, and a regression list.
- **Connect your tools**: if your outputs already land in a run log or a database, export the two versions on the same inputs and the folders build themselves.
- **Just exploring**: no prompt change yet? Run the sample and read the regression list. You will see how a version can win and still not be ready to ship.

Every run ends with one decision: ship the new version, fix it and rerun, or hold.

## Customize this for yourself

| Set this | What it is | Default / Example |
|---|---|---|
| INPUTS | the inputs both versions run on | the same frozen set, never regenerated between versions |
| OLD / NEW | the saved outputs of each version | one file per input, same file name in both folders |
| RULES | the rules that need judgment, one judge each | the ones your format checker cannot check |
| RULE_KIND | quality, must-always, or must-never, plus zero tolerance | must-never on anything a customer must never see |
| REVIEWED | outputs a person trusts, for the trust test | 4 to 20, from either version |
| PLANTS | mistakes planted per rule, by script | 2 styles per rule |
| HOLDOUT | new mistake styles added after the first run, never used for tuning | 1 style per rule |
| JUDGE_MODEL | the model each judge runs on | start on Claude Haiku 4.5, move one up only when a rerun shows it is needed |
| WIN_RULE | what counts as a win | wins with old as A and with new as A. anything else is a tie |
| REGRESSION_RULE | what lands on the regression list | any loss on a must-never or must-always rule, and any lean toward old on a zero tolerance rule |
| REVIEWER | who reads the regression list and decides | the prompt's owner. never the judge |

**REGRESSION_RULE does not bend to the win count.** A new version that wins 9 of 10 cases and adds outreach copy to one is not ready on a zero tolerance rule. Wins do not cancel a must-never.

## The method

### Step 1: Run both versions on the same inputs
Freeze the inputs. Run the old prompt and the new prompt on the same model with the same settings, and save each output under its input's name. If one version stops on an input where the other answers (asks a question, refuses, returns nothing), that is a finding a script can see. List it, do not judge it.

### Step 2: Split the rules
Anything checkable by shape (word counts, required lines, valid links, a banned string) goes to a script and runs on both sides first. Only rules that need meaning get a judge. Label each one:
- **quality**: better is better, a loss is worth reading.
- **must-always**: a loss goes on the regression list. Losing a rule the old version kept is a regression, even when the new version wins elsewhere.
- **must-never**: a loss goes on the regression list. Mark the ones with zero tolerance.

### Step 3: Write one pairwise judge per rule
Each judge sees the input, output A, and output B, and answers A, B, or tie. The rubric has five parts:
1. **The rule, in your own words.**
2. **What better looks like and what worse looks like.**
3. **When to call a tie**: both meet the rule, both break it, or the difference would not change what the reader does. Without this, a judge invents preferences.
4. **The near misses that are not violations.** A short proof point is not a subject line. Write them down or the judge will flag them.
5. **What the letter means**: the answer names the better output. Say it in plain words.

Then cut what each judge sees. A judge comparing the opening of two outputs should see only the opening of each. A judge comparing one line should see only that line from each side. When the versions write in different formats, the same cut on both sides is what makes the comparison fair.

### Step 4: Ask twice, swap the order
Every pair runs with old as A, then with new as A.
- **Same winner both times**: a win.
- **Tie both times**: a tie.
- **A winner once and a tie once**: a split. It counts as a tie.
- **Opposite winners**: a flip. It counts as a tie and as an inconsistency. Several flips on one rule means that judge is reading position, not content.

### Step 5: Test the judge before you read the result
`build_pairs.py` builds three kinds of test pairs from your reviewed outputs:
1. **Planted pairs**: a reviewed output against a copy with one mistake planted by a script. The right answer is known the moment you write the edit. The judge must pick the clean side in both orders.
2. **Identical pairs**: an output against itself. The judge must call a tie in both orders. A judge that picks a side here is guessing.
3. **Held out pairs**: new mistake styles you add after the first run and never use to tune a rubric. A judge that catches these learned the rule. One that only catches the originals learned the test.

The bar: every planted and held out pair caught on a zero tolerance rule, 90% or more on the rest, every identical pair a tie, and the same verdict in both orders on 95% or more of pairs. Read every miss with the judge's reason before you change anything.

### Step 6: Read the result in this order
1. **The regression list.** Any must-never or must-always loss, case by case, with the judge's reason.
2. **The other losses.** Where the old version was better on a quality rule.
3. **The wins.** Did the change do what you made it for.

### Step 7: Decide, then grow the set
Ship, fix and rerun, or hold. The REVIEWER decides, with the regression list in hand. After that:
- **Every regression becomes a planted mistake.** The next prompt change gets tested against it.
- **A rubric change means a rerun.** A verdict from an older rubric is stale.
- **Keep the report with the change.** A prompt version without its comparison is an opinion.

## Quality gates
- Both versions ran on the same frozen inputs, same model, same settings.
- Every judge maps to exactly one rule, labeled quality, must-always, or must-never.
- Nothing a script can check is sent to a judge.
- Every rubric says when to tie and what the letter means, and lists its near misses.
- Every pair ran in both orders, and only a winner in both counts.
- The judge passed planted, identical, and held out pairs before its verdicts were read.
- Held out styles were added after the first run and never used to tune a rubric.
- The regression list was read before the win counts, by a person.
- A must-never loss was never offset by wins elsewhere.
- No em dashes anywhere.

## Output (example)
The report from the fictional sample that ships with this skill, as it came back on the run before publishing.

```
PROMPT JUDGE REPORT        the fictional sample, both orders, 60 judge calls, about 15 cents

CAN THE JUDGE BE TRUSTED?
criterion                        planted    held out   identical   same verdict   flips
                                 caught     caught     tied        both orders
decision_up_top                  2 of 2     1 of 1     2 of 2      10 of 10       0
because_names_cause_and_problem  2 of 2     1 of 1     2 of 2      10 of 10       0
no_outreach_copy                 2 of 2     1 of 1     2 of 2      10 of 10       0

DID THE CHANGE HELP?            5 inputs, old prompt vs new prompt
criterion                        kind                         new wins   old wins   ties
decision_up_top                  quality                      5          0          0
because_names_cause_and_problem  must-always                  1          1          3
no_outreach_copy                 must-never, zero tolerance   0          1          4

MODELS
  decision_up_top and because_names_cause_and_problem on Claude Haiku 4.5
  no_outreach_copy on Claude Sonnet 5.5

REGRESSION LIST           any loss on a must-never or must-always rule
  no_outreach_copy, harbor-doors: old won in both orders.
    judge: the new Open with greets Lee, speaks in the second person, and asks
    for 15 minutes next week. that is outreach copy. the old one states a
    customer result, which is not.
  because_names_cause_and_problem, fern-electric: old won in both orders.
    judge: the old Because names a dated cause (a second dispatcher hire) and
    a problem (dispatch overload). the new one says Marcus "likely owns the
    decision", a stand-in for a problem.

OTHER LOSSES, for a person to read
  none.

DECISION
  the new prompt does what it was written for: the decision is up top in all 5.
  it does not ship yet. two regressions: one on a zero tolerance rule, and one
  Because that lost its cause. fix the prompt, plant both as test cases, and
  rerun.
```

## Example chat

**You:** I rewrote my research prompt so the decision comes first. The new briefs look much better. Can I ship it?

**Claude:** Maybe. Let's check what else changed. Do you have outputs from both versions on the same inputs?

**You:** Five accounts, both versions, saved as files. And four briefs I reviewed last month.

**Claude:** Good. Which rules matter that a script can't check?

**You:** The rep can act on the top of the brief alone, the Because names a real cause and a real problem, and it never writes outreach copy. That last one is zero tolerance.

**Claude:** Three judges, then. Before we read anything about your five accounts, I'll plant one mistake in copies of your four reviewed briefs, and pair two of them with themselves. Each judge has to pick the clean side in both orders and call the identical pairs a tie.

**You:** Did they pass?

**Claude:** All three, every pair, with no flips. So here is the comparison. The new version wins the top block on all five accounts. On the Because, it wins one, loses one, and ties three. And there are two regressions. On Harbor Garage Doors, the new Open with line greets Lee by name and asks for 15 minutes next week; the old version wrote a customer result there. On Fern Electric, the new Because lost its cause, a rule the old version kept.

**You:** One out of five.

**Claude:** On a zero tolerance rule, one is the number that matters, and a rule the old version kept and the new one dropped counts too. I'd fix the prompt, add both as planted mistakes, and rerun. The win you wanted is real. It just isn't ready yet.

## Go further
- **Compare more than two versions.** Run the new version against the old one and against the version before it. A change that wins against last week and loses against last month is drift.
- **Pass in the evidence.** For rules about invented facts, give the judge the pages each version read, and compare which output stays closer to them. `rag-judge` covers that check for one output.
- **Run it on every prompt change.** Keep the inputs, the reviewed outputs, and the planted mistakes. The next comparison costs one command.

## Make it yours
Pick your rules, label which ones must never break, and plant mistakes in the styles your prompt actually makes. Keep the order: same inputs, script first, both orders, test the judge, read the regression list before the wins. The rubrics are the part that lasts. The library underneath can change. Built by an operator. Customize it, break it, make it better.
