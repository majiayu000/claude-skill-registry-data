---
name: tdd
description: Builds a feature or bugfix test first, so each test states what the code should do. Use when implementing any feature or bugfix, before writing implementation code.
---

# Test-Driven Development

A test written before the code states what the code should do; a test written after tends to restate what the code happens to do. Write each test first.

Ask your partner one question at a time, in plain text; do not use the AskUserQuestion tool, because some clients show only the tool's question and drop the text around it. Put what your partner needs to answer in the same message: the problem and why it matters, then the options, recommended first, each with a short bold label in words (never numbers or letters) and a one-line reason. End with a line naming those labels in the same order, such as `Reply with **new PR**, **straight to main**, or **drop it**.`, and make the question the last thing in the message, after any tool use. Your partner may answer with an option, their own alternative, a question or an aside. Keep messages short: lead with the decision, then only the detail needed to answer it. Before a stretch of work that takes more than a moment, such as dispatching a reviewer, writing a spec or plan, or fixing findings, say in one line what you are about to do; after your partner answers, say what comes next before starting it.

When you find something worth doing later that this work does not include, add it as an item to `.dietpowers/trackers/open-items.md`, following `## Open items` in `${CLAUDE_PLUGIN_ROOT}/shared/trackers.md`, and say so in one line.

Commit your work on the feature branch as you go: the spec and plan may be held back, code never is. If you are on `main`, `master` or the plan's `Base:` branch, first ask once: "I'll create branch `<name>` for this work. Reply with **yes** or **no**." If your partner declines, do no code work until a branch is agreed. Nothing is pushed or merged without asking.

1. Write one small test for one behaviour. Name it after the behaviour, not the function. Inside a plan, the task's Tests are the starting set; add a test when you find a behaviour they miss.
2. Run it. Confirm it fails, and that it fails because the feature is missing rather than from a typo or a broken setup. A test that passes at this point is testing something that already works; fix the test.
3. Write the simplest code that makes it pass and works for every valid input, not only the test's. No extra options, no unrelated cleanup, nothing the test does not ask for.
4. Run it again. Confirm it passes, the rest of the suite still passes, and the output is clean with no stray errors or warnings. If it fails, fix the code. If the test itself is wrong, say so and correct it openly; never weaken a test to get to green. If it is wrong because the spec is wrong, invoke the `dietpowers:update-spec` skill.
5. Refactor while green: remove duplication, improve names, extract helpers. Add no behaviour.
6. Repeat for the next behaviour.

Production code written before a failing test: delete it and start at step 1. Adapting it while writing tests produces tests that describe the code instead of the requirement.

Assert on real behaviour, not on mock behaviour. Match test style to the surrounding suite. If a test is hard to write, the interface is probably hard to use — treat that as a design signal.

For a bug: write a test that reproduces it, watch it fail, then fix it. The test is what stops the bug coming back.

Terminal state: if you are working within another dietpowers skill's steps (`dietpowers:execute-plan`, `dietpowers:adversarial-review`, `dietpowers:handle-feedback`, `dietpowers:prove-done`), or the plan for this branch still has unticked tasks, return to that skill and continue where it stopped. Otherwise, commit the change and its tests, then invoke the `dietpowers:adversarial-review` skill on the code.

Depth: writing-good-tests.md, ${CLAUDE_PLUGIN_ROOT}/shared/condition-based-waiting.md
