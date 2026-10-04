---
name: review-feature-suite
description: >
  Reviews a whole suite of `.feature` files against each other and reconciles them. This is
  cross-file consistency auditing for Gherkin and BDD. Makes sure that the suite holds one shared
  language across files, reuses step phrasing instead of duplicating it, carries no contradictory or
  redundant scenarios, and stays consistent in tags, naming, and data. Use whenever the user has
  several `.feature` files, in a Cucumber, SpecFlow, Behave, or plain Gherkin suite, and wants to
  audit, align, reconcile, or de-duplicate them as a set. Use it also when the user says "our
  features use different words for the same thing", "do these scenarios contradict each other",
  "find duplicate steps across our features", or "make our feature files consistent". To author or
  refine one feature on its own, use a single-feature skill such as define-behavior where one is
  available.
argument-hint: "[path to a features directory or glob]"
allowed-tools: [Read, Glob, Grep, Edit, AskUserQuestion]
---

# Review Feature Suite

A single `.feature` file can be flawless on its own and still be wrong next to its neighbors. A BDD suite earns its value through three properties. The whole team shares one language, all the way down into the code. Step definitions are written once and reused. The features stand as living documentation that does not contradict itself. Those properties exist only *across* files, so you can only check them across files. That is the whole job of this skill: read every `.feature` file as one corpus, and reconcile it.

Work in two phases: **critique first, edit second.** Build the picture, present the findings, settle the judgment calls with the user, and only then change files.

## Build the inventory first

The findings live in the relationships between files. Do not read one file at a time and judge as you go. Assemble a compact cross-file picture first, then reason over it. Use `Glob` to enumerate the `.feature` files from the path or glob that the user gave, and search the project when the user gave neither. Then use `Grep` to pull the raw material out of all files at once, instead of holding every full file in context:

- **Steps**: every `Given`, `When`, `Then`, `And`, and `But` line, so you see which phrasings recur and which are near-duplicates.
- **Tags**: every `@tag`, so you see the taxonomy and its typos.
- **Titles**: every `Feature:`, `Scenario:`, and `Scenario Outline:` line.
- **Actors and data**: the roles, the currency, number, and date values, and the named entities that recur, so drift in how they are written stands out.

Grep is the deterministic extraction layer. Your judgment turns that inventory into findings.

## What to check

There are four clusters. The first two are usually mechanical to fix, once you choose the canonical form. The third is judgment that you report rather than resolve. The fourth is lint.

**Shared language.** The same role, object, or state must carry the same name everywhere, and it must reuse the words that the business already uses. Hunt synonym drift, such as `order` against `purchase` against `cart`, `user` against `customer` against `shopper`, and `sign in` against `log in` against `authenticate`. Hunt role-name drift too, such as `Editor` against `editor` against `Content Editor`. Also flag a role or state that scenarios lean on and the suite never introduces. The fix is to pick one canonical term per concept and use it everywhere. First confirm that the words really name one thing, as the next section describes.

**Step-library consistency.** Steps that mean the same thing must be phrased identically, because each distinct phrasing tends to spawn its own step definition in the automation layer. Drift here quietly doubles the code behind the suite. Cluster steps by *behavior*, not by string similarity. `Given I am logged in` and `Given the user is signed in` are the same step, despite low lexical overlap. `Given the cart holds 3 items` and `Given the cart holds 4 items` are deliberately different, despite high overlap. Lexical similarity proves nothing on its own, so judge by what the step does. Also flag parameterization drift, where one file hardcodes a value that another file parameterizes.

**Logical consistency.** Here the suite can actively mislead its readers. Look for contradictions, which are two scenarios that assert different outcomes for the same precondition and action. One example is `SPRING10` that gives 10% off in one feature and 15% off in another. Another is a rule stated one way here and the opposite way there. Look for duplicated behavior specified in two places, because the two copies drift apart under maintenance. Look for orphaned preconditions, such as `Given the user has a premium subscription` when no scenario specifies how a user becomes premium. Report all of these, and resolve none of them in silence, because picking a side is a business decision rather than a cleanup.

**Conventions and metadata lint.** Check the connective tissue for consistency. File naming must use kebab-case aligned with the feature title, with one `Feature` per file. The tag taxonomy must carry no typos such as `@regresion`, and no single idea tagged two ways. Units, currency, dates, and the phrasing of observable outcomes must match, so `€72` and `72 euros` cannot both appear. Scenario titles must be declarative and say what is true, rather than "test X", and no title can repeat across files.

## Resolve ambiguity before you fix anything

A suite-wide rename is only as good as the canonical form behind it, and several of those choices belong to the user. Collect every ambiguous point, and ask through `AskUserQuestion`, before you propose edits. A guess here is expensive: a wrong canonical term, or a side chosen in silence in a contradiction, propagates one confident mistake across every file at once.

Ask about at least these four things:

- **Which synonym is canonical** when several name one concept. Do not assume that the most frequent one is the one that the business prefers.
- **Whether a near-name distinction is intentional.** `order` against `cart`, `customer` against `account`, and `submit` against `confirm` can be real product distinctions. The suite is then right to keep them, rather than collapse them as drift.
- **Which outcome is correct** in each contradiction. You report the conflict, and the user decides the truth.
- **Whether duplicated behavior is redundant or deliberate**, before you merge it away.

Batch these into as few rounds as you can, so the user does not get drip-fed questions. Carry the answers into the fixes.

## Critique first, fix second

Present the findings before you touch anything. Rank them by severity rather than group them by cluster, so the user sees what matters most first:

- **Blocking**: a contradiction, or anything that makes the suite specify the wrong behavior.
- **Important**: vocabulary drift, a duplicate or near-duplicate step, an orphaned precondition, or a real convention break.
- **Nit**: cosmetic lint.

Tag each finding with its cluster, and point at the specific files and lines. Then offer to apply the findings. Offer three choices: every blocking and important finding, everything, or a subset the user picks. Make the edits directly. Get two things right while you apply them:

- A vocabulary or step normalization must hit **every** occurrence in **all** files, not only the ones you quoted. A half-applied rename leaves the suite less consistent than before.
- **Never** resolve a contradiction automatically. Apply a side only after the user chooses it, as *Resolve ambiguity before you fix anything* describes.

## Before you finish

Re-read your changes as a skeptical teammate, and hunt the failures that survive a first pass:

- A rename that missed a file, a `Background`, or a `Scenario Outline` placeholder, which leaves the drift that you set out to remove.
- A normalization that flattened an intentional distinction that the user wanted to keep.
- A "contradiction" that was two legitimately different contexts, now wrongly reconciled.
- A canonical term that you picked yourself instead of confirming with the user.
