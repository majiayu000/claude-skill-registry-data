---
description: >
  Evidence-tag grammar and tagging discipline for paper artifacts. Preloaded
  into every agent that writes, audits, verifies or repairs a paper artifact
  (paper-writer, paper-critic, claim-verifier, refiner); defines how every
  factual claim is bound to a workspace artifact (Chain-of-Evidence).
user-invocable: false
---

# Evidence tagging

Every factual sentence you write into `paper/` or `final/` carries at least
one inline evidence tag binding it to a run artifact:

| Tag | Grounds | Example |
|---|---|---|
| `[EV:score:<path.json>#<dotted.key>]` | a number | `Accuracy reaches 0.9852 [EV:score:best/eval.json#score].` |
| `[EV:log:<path>:L<n>[-L<m>]]` | an event/observation | `Training converged without errors [EV:log:best/solve.log:L2].` |
| `[EV:cite:<key>]` | prior work | `kNN error is bounded by twice the Bayes error [EV:cite:cover1967nearest].` |
| `[EV:artifact:<path>]` | existence/availability | `The full implementation is included [EV:artifact:best/solution.py].` |
| `[EV:config:<path.json>#<key>]` | a setup fact | `We ran 5 parallel branches [EV:config:run-config.json#branches].` |

Rules:

1. Paths are run-directory-relative. The tag must resolve — `ground_check.py`
   opens the artifact and compares.
2. Restate numbers exactly as they appear in the artifact (rounding within
   0.5% and %-vs-fraction conversion are tolerated).
3. One tag per fact; a sentence with two facts gets two tags.
4. Cannot find an artifact for a statement? Then it is an assumption: move it
   under a `## Assumptions` header, or delete it. Never leave an untagged
   factual sentence in the body — GROUND flags it UNSUPPORTED.
5. Citation keys must already exist in `bibliography.jsonl`; a hook blocks
   unknown keys. You may not add bibliography entries yourself.
6. Failed experiments are evidence too — tag them with their branch's
   eval.json/audit.md and report them honestly.
