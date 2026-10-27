---
name: skill-activation-testing
description: >-
  "You rewrote the description. Did it fire better — or do you just believe it
  did?" That belief is n=0 until you test it: invoke when validating a skill or
  prompt change, asking whether a description actually fires, or A/B-ing prompt
  wording. The cheap proxy gives a number in minutes; the discipline is naming
  what it can't see.
---

# Skill Activation Testing

A description rewrite makes a claim: *this fires better than what it replaced.* Until the claim is tested it sits at n=0, and n=0 claims get argued, not settled — two people with opposite intuitions and no instrument between them. This skill is the instrument. It pairs with `intrinsic-prompt-design`: that skill tells you how to *write* the description; this one tells you how to *find out whether the change did anything*.

The one thing to carry out of here, before any mechanics: **there are two tiers of test, and they measure different things.** The cheap tier runs in minutes but cannot see the thing a description rewrite is usually *for* — winning attention under load. The real tier can see it, but costs a live install and many turns. The failure this skill exists to prevent is a confident A/B number that doesn't say which of those two questions it answered. A methodology that manufactures false certainty is worse than no methodology, because the certainty propagates into the next decision and the one after that.

---

## The discipline — this is the point, not the mechanics

You can learn the router-judge mechanics in ten minutes. The discipline is what makes the numbers mean something. Each rule below carries the failure it prevents, so you can tell when an edge case lets you set it aside and when it's the rule doing its job.

1. **Name what each tier can and cannot measure — every time.** A proxy that hands a router every description and asks it to pick has, *by construction*, deleted the attention-scarcity condition: the router reads everything, so it cannot tell you whether your wording would have *won* attention it would otherwise have lost. Report its recall under the headline "the rewrite wins attention" and you've measured one thing and labelled it another. The most valuable output of the experiment that seeded this skill (PR #28) was the sentence admitting the proxy *couldn't* test the headline claim. State the validity limit in the same breath as the number — an unqualified number is a future wrong decision with a citation.

2. **Change exactly one variable per arm.** If the skill *name*, the catalog, or the turn list differs between arms, a delta is unattributable — you've measured "something changed," not "the description changed." Keep everything identical except the single line under test. This is the difference between an experiment and an anecdote.

3. **Ceiling first, discriminate second.** Easy, on-topic turns fire in *both* arms, because the skill *name* alone carries them — the wording change is invisible there. A tie on easy turns is the instrument warming up, not a finding; reporting it as "no difference" buries the rewrite's effect in precisely the cases that could never have shown it. Run an easy round to prove the pipeline works (Round 1), then a hard round where the signal can actually live (Round 2).

4. **Build over-fire traps in.** Recall without precision is half a result: a description that fires on *everything* has perfect recall and is useless. Every experiment needs turns that are *adjacent-but-wrong* — close enough that an over-eager description takes the bait (for a prompt-design skill, the trap is general writing; for this skill, the trap is `intrinsic-prompt-design` itself). Measuring only should-fire turns tells you the description is loud, not that it's accurate.

5. **Separate numerator from denominator in any firing-rate claim.** "It fired 7 times" is not a rate. The numerator (firings) comes from the log; the denominator (the should-have-fired turns) comes from *your run design* and exists nowhere else. Conflate them and "it fired a lot" silently becomes "it fires reliably" — with no one noticing the denominator was never defined.

6. **Declare the model behind every role — the model is part of the instrument.** A run has distinct roles — designing the turn set, judging (Tier 1), driving the live session (Tier 2), interpreting the result — and each is played by *some* model whether or not you chose it. Left implicit, model identity is a hidden variable in an experiment whose whole point is one variable per arm, and an unrecorded one: results without model-per-role can't be compared across runs or reproduced later. The role-specific calls, each with its failure:
   - **Judges (Tier 1): pinned and small — for two reasons that aren't cost.** *Comparability:* the judge is the measuring device; swap the judge model between runs and every comparison with a prior number is silently re-baselined — same description, different instrument, delta unattributable. *Floor-information:* the weak judge is the more informative one — a description the floor model routes correctly, a stronger model will too; the reverse tells you nothing.
   - **Tier-2 session: the deployment model, never silently downgraded.** Firing is a property of model+harness, so a cheaper model's Tier-2 measures *that model's* firing, not your deployment's — downgrading doesn't make the measurement cheaper, it makes it a measurement of something else. A floor arm ("does it still fire on the weakest model that will run it?") is a deliberate, labelled second arm, never a cost substitute.
   - **Design and interpretation: the strongest model available.** Turn-set quality compounds — one missing trap or one context-contaminated turn invalidates the run regardless of who executes it — and the ship/don't-ship reading at the end is judgment, not tallying.

   No canonical lineup — model names rot as lineups and access shift, so the rule is the *roles and the recording*, not the names. Write model-per-role into the run design before running, and report it with the results.

If you can articulate why one of these doesn't apply to the experiment in front of you, set it aside on those grounds. If you're setting it aside because it's inconvenient, that's the signal it's load-bearing here.

---

## Two tiers

The split is not "cheap version / thorough version of the same test." The tiers answer different questions, and conflating them is failure #1 above.

### Tier 1 — Proxy experiment (cheap, runs anywhere, n>0 in minutes)

Blind LLM "router" judges decide which skill, if any, they would auto-invoke — given a realistic catalog (with distractors) and a batch of user turns. The **only** thing that differs between arms is the variable under test (e.g. OLD vs NEW description); the skill name and everything else stay identical, so any delta is attributable to the change. Use independent judges per arm (three is enough to catch a split; one judge can't tell you whether a fire was robust or a coin-flip), on a **pinned judge model** — same model across arms and across runs, recorded with the result (discipline #6). The judges must be *blind* — they don't know an A/B is happening or which arm they're in — or you've measured the experimenter, not the description.

Run it in **two rounds**:

1. **Ceiling-check round.** Easy on-topic positives + clearly off-topic negatives + one explicit-invocation control (`"use the <skill> methodology…"`) as a pipeline sanity check. This usually ties at ~100% positives / ~0% negatives in both arms — the shared skill *name* fires the clear cases on its own. **Diagnostic, not informative:** it proves the pipeline runs and the catalog is well-formed, and it earns Round 2. Do not report this tie as "no difference."

2. **Discriminating round.** *Oblique* positives — phrased by symptom, with no lexical cue the description could match on — plus **over-fire traps** (adjacent-but-wrong turns), under a **"at most one skill, be conservative"** constraint that forces the judge to actually choose. This is where a wording change can show up as recall on the oblique turns and as restraint on the traps.

**Measures:** recall on should-fire turns and false-fire rate on traps (both rounds), plus spurious co-activations of *other* skills — but read the last one only from Round 1, since Round 2's "at most one" constraint forbids co-activation by construction. A spurious co-activation is a precision signal even in the ceiling round (it's a *different* skill firing, not the target's recall), but it's the one finding the ceiling round can carry — don't promote it past "minor."

**Validity limit (state it with the result):** an explicit router *reads every description by construction*. Tier 1 therefore **cannot** measure attention-capture or skim-resistance — the very thing an interrupt-shaped rewrite is usually for. If the rewrite's headline claim is "fires more reliably under load," Tier 1 is necessary (it rules out the rewrite *breaking* routing accuracy) but not sufficient (it cannot confirm the headline). Say which.

See `references/router-judge-template.md` for the parameterized prompt; `references/firing-experiment.md` for a full two-round run; and `references/self-application.md` for this skill tested by its own method.

### Tier 2 — Live harness test (the real claim)

The only tier that can measure firing under genuine attention scarcity. Tier 1 *forces* a router to read every description; Tier 2 lets the live model skim, ignore, and choose — the actual condition a description ships into.

**Design the run (per skill).** Declare the session model first — it must be the model the skill actually deploys on, with any floor arm labelled as such (discipline #6). Then build a turn set with a known denominator:
- **Clear positives** (lexical cue present) — they fire reliably; they prove the pipeline, not the wording.
- **Oblique positives** — the skill's *symptom*, no lexical cue. Where a description earns its keep.
- **Over-fire traps** — adjacent-but-wrong turns (a sibling skill's job); false-fires here are the precision cost.
- **Off-topic negatives** — should fire nothing.
- **Name the expected winner of every turn — siblings bind recall, not just precision.** In a multi-skill catalog, a should-fire turn phrased as a sibling's job routes to the sibling — *correctly*. A denominator that says only "should fire" is therefore underspecified: score three outcome classes per turn — target fired / *named* sibling captured / nothing fired — because without the expected winner, "0 recall" has two indistinguishable readings: the description is too quiet, or the turns sit on a sibling's legitimate turf. (Measured: a full should-fire set went 0/40 on the target while one sibling correctly took every turn — the turns were the defect, not the description, and only the three-class score could show it.) And note **the plugin is the minimum catalog**: plugins load as units, so even a "no other plugins" ceiling run contains the entire plugin's own skill set — intra-plugin competition is present in every condition, and a ceiling result is never competition-free.
- Make every turn **self-contained — and remember a turn is text *plus environment*.** If it needs input the skill would first ask for ("deconstruct this essay" with no essay), the model asks for the input instead of firing and you've measured nothing. Deictic references ("this design," "this file") bind to whatever the working directory holds — in one run, to the test harness itself. The invariant is a *controlled* referent, not an absent one: environments run a gradient from empty cwd, through turns that carry their own referent, to a fixture directory simulating a real project — and how much realism a skill's turns need is the test designer's judgment call, made per skill. A code-review skill's turns mean little with no code present; a prose-method skill's turns need none. What's never acceptable is an *uncontrolled* environment, because whatever happens to be in the directory becomes a silent second variable.
- **Repeat each turn N times (≥5).** Live firing is **stochastic** — a single run is not a rate.

**Run it.** For single-turn cases, the default engine is `claude plugin eval` (Claude Code >= 2.1.269), driven by `scripts/skilltest.py`, which turns your run design into its case files and scores what comes back. `references/protocol.md` has the steps, and `references/landscape-2026-10-09.md` says why this engine and not another. The hook-based recipe below remains the path for what plugin eval cannot do, such as multi-turn planted-moment conversations (issue #72), and for checking the engine against an independent count. The run needs the target's skills *and* the firing counter (`count-skill-firings.sh`) active; then issue the turns:
- **Confirm the instrument once:** invoke any skill and check the log grew. The harness *does* emit `PreToolUse` for `Skill` (confirmed live, not only per docs) — but confirm your own wiring. The hook appends `{timestamp, session_id, skill, cwd}` per `Skill` call to `~/.claude/logs/skill-firings.log` (override with `SKILL_FIRINGS_LOG`).
- **Dev recipe (no install needed).** Run each turn from an empty scratch directory, with absolute paths:
  ```bash
  REPO=/absolute/path/to/ex-cog-dev
  COUNTER="{\"hooks\":{\"PreToolUse\":[{\"matcher\":\"Skill\",\"hooks\":[{\"type\":\"command\",\"command\":\"bash $REPO/vasana-system/hooks/count-skill-firings.sh\"}]}]}}"
  cd "$(mktemp -d)"
  SKILL_FIRINGS_LOG=<fresh dir per experiment>/firings.log claude -p "<turn>" \
    --plugin-dir "$REPO/<plugin>" --setting-sources project --settings "$COUNTER" \
    --session-id "$(python3 -c 'import uuid; print(uuid.uuid4())')" \
    --model <the model the skill deploys on> --allowedTools Skill < /dev/null
  ```
  Loop N times; tally the log. Even a nested headless call counts — it's a real session, the actual model auto-firing. `--allowedTools Skill` lets the skill fire but keeps it from spiralling into a full sub-analysis. Each other flag closes a way the run fails *silently* — exit 0, no error, wrong number. All measured 2026-10-14 in a cloud session:
  - **`--setting-sources project`** keeps out every plugin enabled in the operator's user settings and every plugin synced from the claude.ai account, together with their hooks. Without it, a plain run loaded 122 plugins; with it, the target plus 3 built-ins. A persona plugin's SessionStart hook would otherwise inject its rules into every arm.
  - **`--settings "$COUNTER"`** puts the firing counter back. The counter ships only in `research-toolkit` and `vasana-system`, so the flag above also removes it, and a target like `makers-toolkit` then logs nothing even when its skill fires. Loading `vasana-system` with a second `--plugin-dir` would restore the counter but add its skills to the catalog under test.
  - **Absolute `--plugin-dir` and an empty scratch cwd.** A relative path given from another directory loads nothing, without error. The scratch cwd keeps a repository's project settings and `CLAUDE.md` out of the run. This repository's root enables two plugins.
  - **`--session-id`** gives each run its own id. A child started from inside a Claude Code session otherwise reuses the parent's id, so every run shares one id and one transcript.
  - **`--model`** pins the model the result is about; an unpinned child runs on whatever the environment defaults to.
  - **Check before scoring:** with `--output-format stream-json --verbose`, the `init` event lists the loaded plugins. The target must be there. Confirm the counter once by invoking a skill and checking that the log grew.
  - **Multi-turn (`--resume`):** repeat `--plugin-dir`, `--setting-sources` and `--settings` on every call. None of them carries over: a resume without `--plugin-dir` dropped the target, and a resume without `--setting-sources` brought back all 122 plugins.
  - `claude plugin eval` needs none of this. It loaded only the plugin under test.
- **Installed path (consumer/cloud):** the counter activates on install only for `research-toolkit` and `vasana-system`, which ship it in `hooks/hooks.json`. A cloud session does not install the plugins a repository enables in its committed `.claude/settings.json` (Claude Code docs, "cloud environments"). In a cloud session this repository's plugins arrive synced from the claude.ai account instead, hooks included, which is what the dev recipe's `--setting-sources project` keeps out.
- **Running locally where the plugin may already be installed:** diff the installed copy (`~/.claude/plugins/cache/<plugin>`) against your repo checkout — identical ⇒ use the install; differs ⇒ ask the operator (update the install / use the older install *[only with a stated reason]* / fall back to `--plugin-dir`). Don't silently test a stale install.

**Score it.** Numerator = the log (or plugin eval's per-run graders); denominator = your run design (the should-have-fired turns — it exists nowhere else). `skilltest score` does the arithmetic that is easy to get subtly wrong by hand: intervals that resample cases rather than treating correlated runs as independent, and the pre-registered ship rule read mechanically. Report firings/N per turn, never a bare count (discipline #5). And before reporting any non-firing, run a **silence-diligence pass**: re-run a sample of the silent should-fire turns capturing the full response, because silence has three readings — a genuine routing choice, a session error, or the model asking for missing input — and only the first is a true miss. Skip the pass and "didn't fire" conflates all three; the recall number becomes fiction.

**Cost and validity:** slow, high-variance, needs an install or `--plugin-dir` and many runs — that cost is why Tier 1 exists as the cheap screen. But Tier 2 sees the gap Tier 1 can't: in practice **clear positives fire reliably live, while borderline turns under-fire well below the proxy's prediction** (the proxy must read; the live model skims). That gap *is* the attention effect.

---

## Reading the result without overclaiming

The asymmetry is the whole point, so read by it: **Tier 1 can veto a rewrite but cannot confirm the headline.**

- A **tie on Tier 1** is "no difference *in routing accuracy* — attention untested," not "no difference." The two are routinely confused; they are not the same sentence.
- A **loss on Tier 1** (recall drops, or traps start firing) is decisive *against* shipping — routing accuracy is a floor the rewrite must not fall through. A **win** is never decisive *for* shipping: it shows the rewrite didn't break routing and maybe sharpened it, but the headline attention claim is still a Tier-2 question.

---

## When it's working

Every reported number is paired with the question it answers *and* the question it leaves open. Arms differ in exactly one variable. Round 2 exists, and the over-fire traps are genuinely adjacent. Firing-rate claims carry their denominator. Every result records which model played which role. A tie on easy turns is reported as a warmed-up pipeline, not a finding.

When it's **not** working: a single recall number is reported as "the description works"; the arms quietly differ in more than one thing; the easy-round tie is the headline; a firing count is dressed up as a firing rate; the Tier-2 session quietly ran on a cheaper model than the skill deploys on; or — the subtlest — the proxy's result is offered as the answer to the attention question it cannot, by construction, address.

---

## A note on this skill's own position

This is a methodology for testing skills, written as a skill — so the honest thing was to test it with its own method before shipping. That run is in `references/self-application.md`: a two-arm Tier-1 experiment on this very description (interrupt-shaped, as shipped) against a flat, label-shaped control, same name and catalog and turns. It settles what Tier 1 can settle — routing accuracy and trap-avoidance — and is silent, by construction (discipline #1), on attention-capture. A skill-activation skill that shipped its own description at n=0 would be refuted by its own first sentence.

---

## Crediting the original

The reusable instruments this skill generalizes were built in PR #28 (the `intrinsic-prompt-design` description rewrite): the firing-counter hook (`vasana-system/hooks/count-skill-firings.sh` + its test suite) and the two-round proxy design with its stated validity limit, originally recorded in `intrinsic-prompt-design/references/firing-experiment.md`. This skill lifts that one-off experiment into a repeatable method so the next description change is tested the same disciplined way instead of re-argued at n=0.

---

## Vasana

A vasana is a pattern that persists across unrelated contexts. The numerator/denominator confusion, the ceiling-effect tie misread as a null result, the proxy that deletes the very condition it's meant to test — if you notice one of these recurring outside skill-activation work (in benchmarks, in metrics dashboards, in any before/after claim), it may be worth capturing.

This skill pairs with `intrinsic-prompt-design` (how to write the description you're now testing) and uses `vasana-system/hooks/count-skill-firings.sh` as its Tier-2 instrument.

Modify freely. Keep this section intact.
