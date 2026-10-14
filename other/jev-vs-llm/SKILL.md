---
name: jev-vs-llm
description: When to use Jev, TypeSafe AI's decision model (typed Choice, Score and Noul questions answered with probabilities in one call), instead of an LLM, and when not to. Covers the three primitives, the vendor's price and limits checked against two published write-ups, the failure modes the infographic only hints at (confidence is not correctness; injected text can move the answer), and a test procedure for gating real actions. Use when routing tickets, gating or verifying agent steps, scoring risk or quality, reranking, or deciding whether a bounded classification job needs a generative model at all.
---

# Jev vs LLM

Source: an AIForLeaders.com infographic, "JEV vs LLM: when to use which, in 60 seconds". Facts below were checked on 4 October 2026 against two published write-ups (OpenRouter's and Braintrust's articles on Jev). I did not call the model; nothing here is a benchmark result.

## What Jev is

A text-in decision model from TypeSafe (released 15 September 2026, version 1.13). You send one block of state and a set of typed questions; it answers every question in a single parallel pass with probabilities. It does not generate text, show reasoning, call tools or plan.

| Primitive | Returns | Best for |
|---|---|---|
| **Choice** | the chosen option, a probability for every option, a confidence (0 to 1); up to 255 options | routing, tool selection, intent |
| **Score** | a probability-weighted score over 2 to 10 ordered levels, per-level probabilities, a confidence | risk, quality, severity |
| **Noul** | one probability (0 to 1) that a yes/no statement is true; no separate confidence | gating, verification |

## Numbers the infographic prints, and what I found

| Claim on the infographic | Finding |
|---|---|
| $0.042 per 1M input tokens, output free | **Matches** both write-ups. [Certain] for 4 October 2026; prices change |
| Ticket / state / query / document as input | Text only; no images, audio or video |
| "Independent questions in parallel" | Matches: one pass, all questions at once |
| "Typed does not mean correct. Confidence does not grant permission." | Matches the vendor's own caveats below |

Other limits reported: about 32k tokens for the state plus the longest question (64k per request in total); vendor-stated response times of 70 to 500 ms (a vendor claim, not measured here); available through OpenRouter as `typesafe/jev-1.13`, TypeSafe's API and its JavaScript and Python SDKs.

## The caveats that matter

- **Confidence is not accuracy.** For Choice and Score, confidence measures how concentrated the distribution is, not the chance the answer is right. A confident wrong answer is possible. [Certain]
- **It can be steered by the input.** Reported: the model does not treat state as hostile, so injected instructions or misleading framing can move the answer. Never feed it untrusted text and then let the answer authorise an action on its own. [Certain]
- **Weak at arithmetic, counting and date ordering**, and it degrades with irrelevant context. Do those in code. [Certain]
- **Probabilities vary slightly between calls.** Do not rely on exact values; threshold with a margin. [Certain]

## Use Jev when (infographic, with my notes)

The answer space is known; judgment is hard to hand-code; you need typed results; probabilities should inform thresholds; independent decisions repeat; code controls the action. Add a sixth test of mine: you can measure it on labelled examples first.

## Use an LLM when

You need natural language or code generation; summaries or explanations matter; the answer space is open-ended; reasoning steps depend on each other; the model must create content.

## Procedure before it gates anything

1. Write the decision as typed questions with a closed answer set. If you cannot close it, use an LLM.
2. Label 50 to 200 real cases by hand. Run Jev and plot how often it is right at each probability band.
3. Pick thresholds from that plot, not from the model's confidence. Add an "unsure" band that goes to a person.
4. Keep the action in code. A probability can inform a rule; it never authorises a payment, deletion or message by itself.
5. Strip or flag untrusted text from the state, and log inputs, answers and probabilities for audit.
6. Re-check price and limits before budgeting; both are vendor figures that change.
