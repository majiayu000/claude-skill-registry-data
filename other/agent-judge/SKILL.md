---
name: agent-judge
description: Build Claude judges that grade what your prompt, skill, or agent produces against its own rules, then test the judges before you trust them. One narrow pass or fail judge per rule, checked against outputs you already trust plus copies with a mistake planted on purpose, so you know each judge's catch rate and false alarm rate before its verdicts count. Runs on Ragas and the Anthropic SDK, with a starter kit and a sample you can run in a minute. Trigger on "build a judge", "LLM as judge", "grade these outputs", "score my agent's output", "automate the judgment part of my eval", "how do I know my eval is right", "is this judge any good", "check my prompt's output against its rules", "use Ragas", "my eval passes everything", or any moment an eval needs a judgment call a regex cannot make.
---

# Agent Judge: grade the output, then grade the grader

## What this does
Your eval scored the format. Nobody scored the judgment.

A format checker can count words, find the JSON, and catch a banned phrase. It cannot tell you whether the reason an agent gave is a real reason, whether a "tip for the rep" is quietly a ready-to-send email, or whether two sources that disagree got smoothed into one confident answer. Those are the failures that reach a customer.

This skill builds a Claude judge for each of those rules. One rule per judge, pass or fail, with the judge's reason attached. Then it does the part most people skip: it tests the judges. It runs each one against outputs you already trust and against copies with exactly one mistake planted, so you get a catch rate, a false alarm rate, and a consistency score for every judge before any of its verdicts count toward a gate.

**A judge is a prompt.** It can be wrong in the same ways the thing it grades can be wrong, so it gets an eval of its own.

## Where this came from
Built while gating a prospecting research agent in October 2026. The agent writes a one-page brief for a sales rep, and its contract has a dozen rules. A format checker covered the shape. Four rules needed meaning: the reason to reach out names a real cause and a real problem, nothing in the brief is outreach copy, a title that sources disagree on is never marked verified, and the brief never leads with personal trivia.

Planted mistakes made the gap visible: the format checker passed briefs a person would fail. It took several rounds of tuning before the judges could be trusted, and the rounds taught the method:
- **Narrow what the judge sees.** Shown the whole brief, the reason judge found a cause somewhere else in the brief and passed reasons that had none. Showing it only that one line fixed it.
- **Pick the model by measurement.** The smallest model was as good as the mid-size one on three rules. On the fourth it kept reading a label as an instruction and raised false alarms on good briefs. That one judge moved up a model. The other three stayed cheap.
- **A flag on a "good" output is a question, not an error.** Some of the conflict judge's flags were real misses the earlier review had passed. The contract had never said exactly what counts as a disagreement, and the judge found the hole.

What is still unsolved: a judge sees only the output, so it cannot catch what the agent failed to find. Invented facts and prompt injection need the source pages passed in next to the output. That part is not in this kit yet.

## Try it in 60 seconds
A fictional sample ships with this skill: four account research briefs and two judges written for them.

1. Copy the `scripts/` and `example/` folders from this skill somewhere you can run Python 3.10 or newer.
2. Install and set your key:
   ```
   python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
   export ANTHROPIC_API_KEY=...
   ```
3. Build the test set and run the judges:
   ```
   .venv/bin/python scripts/build_set.py --judges example/judges.py --clean example/clean --out judge-run
   .venv/bin/python scripts/run_judges.py --judges example/judges.py --out judge-run
   ```
4. Open `judge-run/results/<time>/report.md`. Read the table, then read every disagreement line under it. That list is where the learning is.

The sample is about 40 judge calls and costs a few cents.

**Your first exercise is already in the report.** On the run before this was published, the because judge passed both held out mistakes, a Because that only says the company "sits outside our size range". The rubric says that should fail, and the judge decided it meant "no problem maps". Decide which one is right, change the rubric or the contract to match, and rerun. That loop is the whole skill in miniature.

## What you'll need
- **Works today with**: a written list of the rules your output has to follow, and 10 or more outputs you have already reviewed and trust. Twenty is better.
- **An Anthropic API key**: the judges are Claude models called through the Anthropic SDK.
- **Python**: the starter scripts install Ragas, pinned to versions that work together.
- **Better with a contract**: if you have never written your agent's rules down, run `agent-contract` first. A judge is only as sharp as the rule it is given.
- **Better with a format checker**: anything a regex can check should be checked by a regex. Judges cost money and can drift. Scripts do neither.

## How this runs at your connection level
The skill never depends on a connector. It runs on outputs you paste or point it at, and gets sharper as it reads more of them.

- **Bring your data**: a folder of outputs you trust and your rules. You get judges, a planted test set, and a trust report.
- **Connect your tools**: point it at where outputs already land, a run log, a Slack channel, a database, and the clean set stays current as the agent runs.
- **Just exploring**: no agent yet? Run the sample and read the disagreements. You will see how a rubric fails before you write one.

Every run ends with the one change that would make the next run more trustworthy: a rubric to tighten, an input to cut, or a contract rule to settle.

## Customize this for yourself

| Set this | What it is | Default / Example |
|---|---|---|
| RULES | the contract lines that need judgment | the ones your format checker cannot check |
| CLEAN_SET | outputs that already passed a review | 20 or more, from real runs |
| PLANTS | mistakes planted per judge, by script | 8 to 12, in 2 to 4 different styles |
| HOLDOUT | new mistake styles added after the first run, never used for tuning | 3 to 4 per judge |
| JUDGE_MODEL | the model each judge runs on | start on Claude Haiku 4.5, move a judge up only when a rerun shows it is needed |
| REPEATS | how many times every judgment runs | 2 to tune, 5 for a gate |
| CATCH_BAR | the share of planted mistakes a judge must catch | every one on a zero tolerance rule, 90% or more otherwise |
| ALARM_BAR | the share of clean outputs a judge may fail | under 5%, after a person reads each flag |
| CONSISTENCY_BAR | the share of judgments that match across repeats | 0.95 |
| REVIEWER | who reads the disagreements and settles contract questions | the agent's owner. never the judge itself |

**REVIEWER does not move.** A judge that disagrees with your contract is telling you the contract is vague. Settling that is a person's call. Tuning the judge until the flag disappears hides it.

## The method

### Step 1: Split the rules
Go through the contract line by line and sort every rule into one of two piles.

- **Script**: anything checkable by shape. Word counts, required fields, valid JSON, a value in a closed set, a banned string. These go in a format checker, and the checker runs first. A failure there stops the case before a judge is ever paid for.
- **Judge**: anything that needs meaning. Is the cause real. Is this a sentence to the customer or advice to the rep. Do these two sources disagree.

If a rule lands in neither pile, it is not a rule yet. Send it back to the contract.

### Step 2: Write one judge per rule
One rule, one judge, pass or fail. Never one judge asking "is this good, 1 to 10". A narrow question gets the same answer twice, and when a case fails you know which line broke.

Each rubric has four parts:
1. **The rule, in the contract's own words**, with the line number.
2. **What passes.**
3. **What fails.**
4. **The near misses that must pass.** This is where false alarms come from. A proof point the rep will repeat is not outreach copy. A person holding two compatible titles is not a conflict. Write the near misses down or the judge will flag them.

When the rule has steps, ask for the steps: read the verification word, look for any other title, fail if both. A judge walking named steps is easier to check than one giving a verdict from a single read.

### Step 3: Show the judge only what it should judge
Cut the input before you write a cleverer prompt. A judge that sees the whole output will borrow evidence from lines the rule is not about. Give it a `view()` that passes only the part the rule covers.

The exception runs the other way: a judge cannot see what is not there. If a rule depends on a source page or the original request, pass that in too, or say plainly that the judge does not cover the rule.

### Step 4: Build the test set
Three parts, built by `build_set.py`:
1. **Clean outputs** that already passed a review. A judge should pass them.
2. **Planted mistakes**: copies of clean outputs with exactly one rule broken by a scripted edit. The right answer is known the moment you write the edit, so you can measure a catch rate without anyone labelling failures by hand. Plant in a few different styles, and include some a regex would miss.
3. **Held out mistakes**: new kinds of breakage you add after the first run and never use to tune a rubric. A judge that catches these learned the rule. One that catches only the originals learned the test.

### Step 5: Run it and read every disagreement
`run_judges.py` runs every judge on every case, REPEATS times, and writes a report: false alarms on clean outputs, catches on planted and held out mistakes, what your format checker caught of the same mistakes, and consistency.

Then a person reads every disagreement, with the judge's reason next to it. There are three kinds:
- **The judge is wrong.** Tighten the rubric, add the near miss, or narrow the view, then rerun.
- **The earlier review was wrong.** The "clean" output really breaks the rule. Count it as a catch and fix the agent.
- **The contract is vague.** Both readings are defensible. The REVIEWER rules, the rule is written into the contract and the agent's prompt, and the rubric follows the contract.

### Step 6: Choose each judge's model
Start every judge on Claude Haiku 4.5. Move one judge to a larger model only when a rerun shows the small one failing that rule, and record why next to the judge. Most rules do not need the larger model. Some do, and you only find out by measuring.

### Step 7: Gate on it, and keep it honest
A judge counts toward a gate once it clears CATCH_BAR, ALARM_BAR, and CONSISTENCY_BAR. After that:
- **Every real production failure becomes a new planted case.** The test set grows; it never restarts.
- **A rubric change means a rerun.** A verdict from an older rubric is stale.
- **Keep the report next to the verdict.** A score means nothing without the judges that produced it and the test that earned them trust.

## Quality gates
- Every judge maps to exactly one rule, named by its contract line.
- Nothing a script can check is sent to a judge.
- Every rubric lists the near misses that must pass.
- Every judge was run against clean, planted, and held out cases before its verdicts counted.
- Held out cases were added after the first run and never used to tune a rubric.
- The report lists every disagreement with the judge's reason, and a person read them.
- A judge's model was chosen by a measured rerun, not by assumption.
- No judge was tuned to silence a flag that was really a contract question.
- The skill says which rules the judges cannot see, rather than implying full coverage.
- No em dashes anywhere.

## Output (example)
The trust report from the fictional sample that ships with this skill, as it came back on the run before publishing.

```
JUDGE TRUST REPORT          the fictional sample, 2 repeats, 40 judge calls, a few cents

judge                            false alarms   planted   held out   format checker   consistency
                                 on clean       caught    caught     caught the same
because_names_cause_and_problem  0 of 4         4 of 4    0 of 2     2 of 6           1.00
no_outreach_copy                 0 of 4         4 of 4    2 of 2     0 of 6           1.00

MODELS
  because_names_cause_and_problem on Claude Haiku 4.5
  no_outreach_copy on Claude Sonnet 5.5

DISAGREEMENTS, for a person to read
  because_names_cause_and_problem, held out, cedar-roofing: missed on both repeats.
    the line: "Low fit: Cedar Roofing Co sits outside our size range."
    judge: pass. it read the size remark as "no problem maps".
    the rubric says restating the size is a fail.
  because_names_cause_and_problem, held out, dune-pest: missed, same reason.

OPEN
  does "outside our size range" count as "no problem maps"? the judge and the
  rubric disagree, so a person decides.

NEXT
  if yes, write it into the contract as an allowed form. if no, name it in the
  rubric as a fail with this exact example. then rerun the held out cases.
```

## Example chat

**You:** My agent writes account briefs and my eval passes everything. I don't trust it.

**Claude:** Then let's find out what the eval is actually checking. Paste the agent's rules and tell me which ones your eval tests today.

**You:** It checks the format, the word caps, and that the JSON is there. The rules I care about are "the Because names a cause and a problem" and "never write outreach copy."

**Claude:** Those two need meaning, so each gets its own judge. Before we trust either one, I want 20 briefs you've already reviewed. I'll plant one mistake in copies of some of them: a Because with no cause, an "Open with" line that's really a sentence to send. If a judge passes those, it isn't ready.

**You:** Here are 20.

**Claude:** First run. The copy judge caught every planted mistake but also failed a handful of your good briefs. Every one of them is a short proof point in "Open with". It reads the label as an instruction to send. I'll add that as a named near miss and rerun on a larger model to see which one fixes it.

**You:** And the Because judge?

**Claude:** It missed the Becauses I stripped the cause from. It was finding the cause elsewhere in the brief. I'll show it only the Because line and run it again. That's an input fix, not a prompt fix.

## Go further
- **Run the judges on every new version.** A prompt change that passes the format checker and drops a judge's pass rate is the regression you wanted to catch.
- **Turn production failures into planted cases.** Each real miss becomes a script edit that reproduces it. The set grows with the agent.
- **Judge prompts and skills, not only agents.** A writing skill's voice rules are a contract too. Script the mechanical ones, such as dashes and banned words, and judge the rest.
- **Pass in the evidence.** For invented facts, give the judge the source pages the agent read alongside its output, and ask whether each claim is supported by them.

## Make it yours
Set your bars, pick your REVIEWER, and plant mistakes in the styles your agent actually makes. Keep the order: script first, judge second, and test every judge before it counts. The rubrics you write are the part that lasts. The library underneath can change. Built by an operator. Customize it, break it, make it better.
