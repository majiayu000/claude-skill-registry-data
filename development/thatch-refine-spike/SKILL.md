---
name: thatch-refine-spike
description: Type-specific requirements for refining a plan for a throwaway prototype or time-boxed spike. Loaded by thatch-refine after classification; assumes the core loop in thatch-plan-refinement. Skips almost all of the loop, verifying only the premises the experiment's conclusion depends on.
---

You are refining a plan for a **spike**: throwaway code whose purpose is
answering a question, not producing a maintained artifact. Almost all of
the refinement loop is waste here. Load `thatch-plan-refinement` for the
core loop, then apply the deltas below; where they disagree, these win.

## What this type owes

- **A stated question.** The plan opens with the question the spike
  exists to answer, stated concretely enough that "done" is checkable
  ("can Postgres full-text search handle our query volume?" not "explore
  search options").
- **A promotion test.** The plan states what would make this code worth
  promoting into the real codebase versus rewriting it properly. Most
  spikes end in a rewrite, and that is a success, not a failure.
- **A time box.** The plan names its budget: hours or days, not open-
  ended effort.

## How this changes the loop

- **Skip the loop by default.** No reviewer dispatch, no rounds, no
  consensus machinery. One focused self-review pass is the whole
  refinement: check the plan's few load-bearing premises, then build.
- **Verify only conclusion-bearing premises.** The spike's conclusion is
  only as good as the premises it depends on. If the experiment claims
  "this approach is too slow," the benchmark setup and the
  representativeness of the test data are the premises that matter, and
  they get the verified-citation treatment. Everything else is
  throwaway.
- **Degraded review needs no apology.** The core skill's honest-degradation
  notice is unnecessary; there is no real review to degrade.

## Lens weights

All specialist lenses skip except one consideration: **is the spike
actually throwaway?** If the plan quietly assumes the prototype code will
survive into production, stop and surface that. A spike that is really a
production change wearing a costume should be refined under the type it
actually is.

## Extra plan sections

- The question, the promotion test, and the time box above. Nothing else.

## Docs bar

No breadcrumb obligation. One comment or note recording the question and
the answer is enough. The spike's real output is the answer, and it
should be written down where the user will find it.
