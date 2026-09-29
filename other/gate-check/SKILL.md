---
name: gate-check
description: >-
  Find the decisions in a pipeline that do not need the expensive model and
  propose the gate for each: a rule, a classic classifier, or a small model,
  with fail-closed routing. Use when the user asks to cut model costs or
  latency, says the big model handles everything, or wants a triage /
  routing / filter layer in front of an agent. Analysis plus an optional
  baseline scaffold. Do NOT use for auditing context layout (context-audit)
  or for building eval suites (evals-bootstrap).
---

# Find the gates

Theory: [Cheap decisions](https://undefined-ui.github.io/second-brain-os/#course-3-gate/cheap-decisions)
and [Gate practice](https://undefined-ui.github.io/second-brain-os/#course-3-gate/gate-practice).
An agent does two kinds of work: it writes, which needs a big model, and it
decides — is this spam, which queue, does this need a person — which is a
bounded question the answer to which comes from a set you already know.
A gate is a cheap decision layer that sorts the stream so the expensive
model only sees the items that actually need judgement.

## Workflow

1. **Map the decisions.** Read the pipeline's entry points and prompts and
   list every decision made before or during a model call: classification,
   routing, filtering, yes/no triage, priority, language, "is this even for
   us". Ignore the writing — only bounded decisions with a known label set.
2. **Count what each costs today.** For each decision currently made by the
   big model: calls per day if known, tokens per call, and what a wrong
   answer costs. A decision worth one bit that burns a frontier call is the
   headline finding.
3. **Propose the cheapest gate that can hold it**, in rising order of cost:
   - a **rule** — regex, allowlist, header check: free, instant, blind to
     anything unanticipated; always the first layer, never the last
   - a **classic classifier** — logistic regression or similar over simple
     features, trained on a few hundred labelled examples: milliseconds,
     fractions of a cent, and the baseline every fancier option must beat
   - a **small / System One model** — when the input is too varied for
     features but the output is still a label with a confidence score
4. **Route fail-closed.** Every gate needs a confidence threshold, and doubt
   goes down the safe path: unsure means escalate to the big model (or a
   person), never means guess. Say explicitly what each gate's unsure route is.
5. **Offer the baseline scaffold.** If the user wants to proceed, generate
   the module's thirty-minute exercise for their data: a `label.py` that
   samples ~200 real examples for hand-labelling, and a `baseline.py` that
   trains the classic classifier and prints accuracy against a held-out
   split. Every vendor claim and small-model option must beat this number
   on their data before it earns a place in the pipeline.

## Output format

```
Gate check — <pipeline>
decisions found: <n>, currently on the big model: <n>

1. <decision> — <where in the code>
   today: <who decides, est. cost>   label set: <the labels>
   gate: <rule | classifier | small model> — <why this tier>
   unsure -> <escalation path>
   saves: <est. calls/tokens diverted>
...
```

Rank by savings. If a decision genuinely needs the big model — open-ended,
no stable label set, wrong answers are cheap to fix — say so and leave it
alone; a gate that guesses is worse than no gate.
