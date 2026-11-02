---
name: principle-attack-the-premise
description: Apply when two or more fixes resting on one belief have failed the same gate (a test, a review, an eval).
disable-model-invocation: true
---

# Attack the premise

Fixes that keep failing at one gate usually share a wrong belief; another
careful fix built on it fails the same way.

- Once two or more fixes that rest on one premise have failed the same gate,
  make no further fix that assumes it until the premise is written and tested.
- Write the premise as one sentence: the belief every failed fix took for
  granted.
- Test it with an observation whose result would differ if the premise were
  false. Rereading the code that embodies the belief is not such a test.
