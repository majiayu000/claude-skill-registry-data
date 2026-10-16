# Step 6 expanded — breaking a change on purpose

## How attempts are weighted

- An **unsuccessful attempt to break** the change carries **5×** the weight of a successful attempt to show it works.
- A **disproof that succeeds ends the hypothesis in its stated form**, right away. Don't work around it while still claiming the original.

## Listing the exits

Before you accept anything, write out every exit and check each one off against a test **you actually ran**. An exit left unchecked holds up acceptance just as a red test would.

- **Control flow** inside the modified function — each branch and early exit, **pre-existing ones too**, since anything inserted beneath an earlier `return` is dead code
- **Who calls it** — production code and tests alike, including any call site that skips an optional parameter
- **What comes back** from each thing the change calls — success, failure, exception, timeout, empty result, lost race
- **Repeats and overlap** — a retry, a message delivered twice, a second worker running at once, the following scheduled run
- **Downstream readers** — every consumer of whatever state the change stores

When the list grows too big to cover, that's a finding in itself: the change is too wide or lives in the wrong spot. Shrink it or move it — never accept it based on whichever exits were easy to test.

## Choosing fixtures

**Go for the fixture the fix is most likely to FAIL on.** When a test passes with the first fixture you thought of, treat that as a red flag, not evidence.

Planting a final state is different from running the code that creates it. A test that writes a record's status field directly tells you about the reader; you learn about the writer only by invoking the writer.

There is one standing exception: squeezed tests, used purely for diagnosis. The Saff Squeeze (SKILL.md step 2a) is supposed to finish with planted state, because cutting out the production path is the very mechanism that narrows the search. Retain such a test for the detail it pins, and retain the high-level test next to it for coverage. Acceptance evidence still has to meet the rule above — at least one test somewhere must call the writer.

Nobody decides to lose that coverage; it erodes. During a tidy-up, the compact, fast, easy-to-read squeezed test looks like the keeper, the sprawling high-level one gets removed, and the writer quietly stops being exercised.

## Checking that a test bites

Rebuild the earlier or naive version of the change and run your tests on it.

- Still green? Then **the test guards nothing**, and needs rewriting.
- Don't trust the bite-check blindly — verify it too. Target the reverted code by line number or by text that occurs only once. A find-and-replace on some common fragment may silently edit a different spot, leaving a perfectly good test looking useless.
- Best case, your tests **fence the behavior in from both sides**: one group catches a version that does too little, another group catches a version that does too much.

## Injecting failures

Failures should come from the *genuine* resource. Throwing from a stub skips the resource entirely, and so never produces the broken condition the fix is there to clean up. Say a stubbed write throws: no real connection, file handle or transaction is left half-done, and a rollback or cleanup test that depends on that stub stays green after you delete the cleanup code.

Aim mocks carefully. The replacement must sit on the exact binding the code under test resolves at call time; put it anywhere else and the genuine implementation executes, leaving the test meaningless.

## Unreachable states

When an attack depends on a state production code can't reach, don't "repair" the code to accommodate it, and don't keep that test. Pin down the **invariant that keeps the state unreachable** instead, so a test breaks the day someone makes it reachable.

## Revising after a disproof

One disproof doesn't doom the entire idea. Adjustable parameters, the placement and the general approach may all survive — the cycle runs *hypothesis → disproof → revised hypothesis*, not *hypothesis → trash*.

The catch: the revised version **carries over none of the earlier evidence**. It begins with zero confidence and goes through everything again, **re-running every attack the original withstood**. Passing tests from before the revision say nothing about the code after it.

What separates a genuine revision from propping up a dead one: **run the disproof that broke it again.** If that attack still succeeds, drop the revision and form a genuinely different hypothesis (SKILL.md step 8).

## Guarding against disproof theater

You can meet this step on paper by running attacks that were never going to succeed and then scoring them as survived. Assume it will happen: the attacks you think of first lean toward cases the fix already covers, since those were on your mind while you wrote it.

Four guards, sorted by how difficult each is to fake.

### 1. The mutation gate — an attack counts only if it kills the PRE-CHANGE code

Each disproof attempt produces **two** results: one on the pre-change code, one on the changed code. "Fails" means the test fails, i.e. it caught a problem.

| Pre-change | Changed | Verdict |
|---|---|---|
| fails | passes | A real attack; include it. |
| passes | passes | It missed the mechanism entirely. **Score it as zero**, and say so out loud. |
| fails | fails | The change doesn't fix it. The claim is disproven; go to SKILL.md step 8. |
| passes | fails | The change broke something that used to work. The claim is disproven; go to SKILL.md step 8. |

In effect, the ["Checking that a test bites"](#checking-that-a-test-bites) routine gets pointed at your disproof attempts. No other guard is as strong, because none of it relies on self-honesty: the check is mechanical, and retrieving the old version takes one `git show`.

**One kind of test slips through the gate: a test cut down from the failure you started with.** Squeezed tests (SKILL.md step 2a), and anything else produced by shrinking a known-bad case, fail on the old code as a matter of course, so they pass the gate although nobody aimed anything. Their home is step 5, whose job is pinning the mechanism. Put them in step 6 and you inflate the number while diluting the substance — precisely what [guard 4](#4-report-content-never-counts) forbids.

**Worked example.** Someone ran a change against the existing suite three separate times, got 95% every time, and offered that as evidence the change was sound. Running the untouched code gave **exactly 95%** too. The suite simply never exercised the modified behavior, so no result it could produce would have refuted anything. What those runs did establish — that nothing previously covered broke — was real and useful. Whether the change actually worked, they couldn't say. Calling them disproof attempts would have been theater, and the gate catches that without any help.

### 2. Pre-register the attack list before implementing

Write down "this is how I'd know it's wrong" during step 3, as the Disproof half of the test plan, **before** any change exists. Once it does, it colors what you can imagine.

Attacks you come up with later are fine and frequently the strongest — but **flag them post-hoc**, since that's where bias gathers. A list drawn up entirely after the code isn't a plan to disprove anything; it's a summary of the code's behavior.

### 3. Predict each outcome, then account for surprise

Write the result you expect *before* you run each attack.

**If all your predictions were right, you ran no experiments.** An attack you're sure will pass is really a confirmation dressed up as a disproof; the useful ones are those where you honestly don't know the answer, or where you expect a failure.

Report the **nearest miss**. A change that got through seven attacks without any close calls deserves more suspicion than one that got through four with a scare — the former usually means the attacks were pointed at the fix's strongest spots.

### 4. Report content, never counts

"Withstood 5 disproof attempts" can be gamed, and the number rewards exactly the wrong behavior: five feeble attacks cost less to produce than a single real one.

So describe attacks individually: **the attack, the thing it could have exposed, and its outcome on the old code.** Close with a spelled-out list of **exits you never ran**. Readers assume silence means coverage, and the exits you left off are often exactly where the bug turns up.

### The limit of all four

None of the four help when the **framing** is off. Rigor applied inside the wrong question never gets out of it.

Take a real debugging session. Three hypotheses came up in turn, and each was attacked and refuted, every refutation genuinely improving the next guess. All three, though, assumed the question *"why does processing this message fail?"* — and the truth was that the message never showed up. Attacking answers could not have uncovered that. What uncovered it was somebody asking something else.

Expect, then, to misframe problems from time to time. An outsider questioning the **question** is worth more than yet another attack on your answer. And each time a disproof lands, the opening move of step 8 is checking whether the framing fell along with the hypothesis.

## Reporting honestly

- Label each claim as either **executed** or merely **read**.
- Before citing how many tests fail, look at the failure messages. Tests that break on argument or type errors because a signature changed aren't pinning any behavior, so leave them out of the count.
- If one of your own disproofs turns out to be wrong, take it back. Wrongly killing a good change is as expensive as shipping a bad one.
- Treat what reviewers and agents say about the code as unverified until you've checked it. Confirmation bias catches them as readily as it catches you.
