---
name: pr-review
description: Review a pull request for correctness, clarity, and test coverage, and leave findings ranked by severity. Uses a checklist and a scoring rubric.
license: Apache-2.0
metadata:
  category: engineering
---

# PR review

Read the diff, then the tests that cover it. Walk the checklist in `references/checklist.md` before writing anything.

For each change ask three questions: does it do what the description says, could it fail on an input the author did not consider, and is there a test that would catch that failure.

Score each finding with the rubric in `assets/rubric.json`. Report findings most severe first. Each finding names the file and line, states the defect in one sentence, and gives the input that triggers it.
