---
name: delegate-bulk-reads
description: >-
  Load before dispatching the bulk-reader subagent: how to write the prompt and verify its answer.
disable-model-invocation: false
user-invocable: false
license: Apache-2.0
---

# Delegate bulk reads

The `bulk-reader` subagent reads on a small model and returns anchored bullets. The file contents
never enter this context, so its answer is all there is to work with. Its own description says when
it is the wrong tool; this covers how to drive it and how to treat what comes back.

**Do not override the worker's model.** The agent file pins it; the `Agent` tool's `model`
parameter would replace that per call. Measured over six runs on a real plugin repository, a larger worker
never wins: on enumerative questions the pinned worker already recalls every fact, so the swap buys
nothing and costs about ten points of saving; on reasoning questions it recovers part of the
missing detail but drops the saving from roughly 60% to 25%, and still omits silently. When an
answer thins out, narrow the question — see below — rather than paying for a bigger reader.

## Procedure

### Delegate above ~400 lines, not above three files

Count lines, not files. The round trip is the prompt plus the reply plus the re-reads below, and
under roughly 400 lines that costs more than reading the files yourself — ten small manifests clear
"three or more files" easily and still lose you tokens. The floor sits near the read guards' own
350-line threshold, which is the same judgement expressed as a hook.

An answer you will verify at many anchors raises the floor further, because each anchor pulls its
own region back in. Checking nineteen anchors in one file re-reads most of that file, which is a
long way to travel to arrive where you started.

### Shape the call

```
Agent(
  subagent_type: "bulk-reader",
  description: "Read auth flow files",
  prompt: """
  QUESTION: Which methods write to the database, and what transaction boundaries do they use?

  FILES:
  - src/service/UserService.java
  - src/db/TransactionManager.java

  Answer only the question. Anchor every claim with path:line.
  """
)
```

**Prefer two narrow calls to one broad one.** Re-sending the same paths with a different question
costs nothing here, since the files go to the worker and never come back — the second call is
priced like the first, not like a re-read. This is the rule that does not carry over from ordinary
delegation, where re-sending context is the expensive part. So when a follow-up question occurs to
you, ask it; do not bundle it into the first call to save a trip you are not paying for.

**Split a "why" into several "wheres".** The worker holds up when the question enumerates — which
of these declare X, does any of this import Y, list every heading — and thins out when the answer
has to be assembled from what it read. It keeps the enumeration and drops a share of the reasoning,
without saying which share. So when your question asks what the code means rather than where
something is, ask for the locations instead and work out the meaning yourself, on lines you have
read.

## Rules

### Trust the anchors, not the prose

The reply has three sections: `## Answer` with every claim anchored `path:line`,
`## Not found / uncertain`, and `## Coverage`.

- **Read the anchored lines before acting on them.** Before an edit, a refactor, or a claim
  reported to the user, `Read(path, offset=..., limit=...)` the region. These files were never
  seen here, so judging whether the summary "looks right" is not a check. An anchor can point at a
  real line and still describe it backwards — the line number being right is not the claim being
  right.
- **A bullet with no anchor is unverified.** Re-delegate with a narrower question instead of
  building on it.
- **Distrust a clean `Not found / uncertain`.** Silent omission is the dominant failure mode of a
  summarizing worker: an answer missing a case looks identical to a complete one. This section is
  the worker's own account of its gaps, so it fails exactly when you most need it — `- Nothing
outstanding.` has come back from runs that missed a quarter of the real hits. An empty section on
  a multi-file question is a reason to check, not a reassurance.
- **Treat `Coverage` as a claim, never as a count.** The rows do add up — the worker sums them
  correctly — and each file usually comes back about one line too long, because a trailing newline
  reads as an extra line. Do not let that small familiar error teach you to skim the section. The
  case that costs you is the other one: a worker that read only the first 50 lines of a 300-line
  file reports `50 lines read`, accurately, under an answer that looks finished. Compare the row
  against the real length whenever the answer matters — it is the only claim in the reply you can
  check without opening the file.
- **Check every path got a verdict, then confirm with a cheap Grep.** The free check first: the
  worker owes every path you sent a verdict in `Answer` — a hit with anchors, or `no match` — so a
  path appearing in none of the three sections was dropped. That costs no tool call and works on a
  question with no greppable pattern. Where the question does have one, `grep -c` it against the
  paths you sent and compare with what came back. Do both when the answer is empty, when
  `Not found / uncertain` is empty, and whenever `Coverage` quotes a number you have not checked.
