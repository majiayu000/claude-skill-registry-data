---
name: pr-review
description: Review a pull request for correctness, clarity, and test coverage, and leave findings ranked by severity.
license: Apache-2.0
---

# PR review

Read the diff, then the tests that cover it. For each change ask three questions: does it do what the description says, could it fail on an input the author did not consider, and is there a test that would catch that failure.

Report findings most severe first. Each finding names the file and line, states the defect in one sentence, and gives the input that triggers it.
