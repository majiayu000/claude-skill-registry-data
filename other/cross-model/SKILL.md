---
name: cross-model
description: Consult a different model for orthogonal reasoning on a consequential decision, especially when confident. Discovers whichever model CLI is installed rather than assuming a vendor. Use when the user says "second opinion", "cross-model", "ask another model", "stress-test this", "what am I missing", "red-team this decision", or before committing to an architecture, a schema, a security boundary, or anything hard to reverse. For a reversible local decision or routine implementation, proceed directly; for a question with one verifiable answer, read the source instead.
argument-hint: "/cross-model [expand|stress] <the decision, with context>"
allowed-tools: "Read, Grep, Glob, Bash"
---

## Overview

Different training data, different tuning, different sampling. The blindspots do not line up. That non-overlap is the entire product; agreement is a bonus, not the goal.

Invoking this is a mark of rigor, not an admission of uncertainty. It means the decision was taken seriously enough to generate friction against it.

## The Key Inversion

Consult **when the decision is consequential and you are confident.** Confidence is exactly where a blindspot hides, because there is nothing prompting a second look. A decision that already feels shaky gets scrutiny for free.

The corollary: adversarial coverage from the same model shares its blindspots by construction. A subagent that reviews your reasoning is running the same priors that produced it. That is worth doing and it is not this.

## When to Use

Consequential, regardless of confidence:

- An architecture choice before committing, especially a public interface, a data model, or a service boundary.
- A security-sensitive surface: authentication, tenant isolation, payment handling, anything reachable by an untrusted caller.
- A schema change or migration, which is hard to reverse.
- Concurrency: locking, idempotency, distributed coordination, anything where the failure is a race.
- A decision that constrains future options more than it looks like it does.

Moments where a second perspective pays for itself:

- Before committing to a direction, never after the investment is sunk.
- When it feels obvious.
- When the need is to expand options rather than pick among the ones already listed.
- In a problem space where training coverage is plausibly thin.

Skip it when the decision is reversible in the next commit with no migration and no coordination, when nothing downstream depends on it, or when the answer is a fact that reading the source settles. Reading the source is cheaper and definitive; see the anti-hallucination table in [the global instructions](../../CLAUDE.md).

## Process

1. Pick the mode per Two Modes: `expand` with no candidate yet, `stress` with one.
2. Resolve the installed consultant per Discovering the Consultant, and read its `--help`.
3. Compose the four-part prompt per Composing the Prompt, with secrets and personal data redacted.
4. Send it, capture the session identifier, and run up to three rounds per Multi-Turn.
5. Re-verify every specific in the reply per Reading the Response, then synthesize.
6. Report the four items in Reporting Back.

## Two Modes

| Mode | Timing | Ask |
|---|---|---|
| `expand` | Before a candidate exists | "What approaches am I not considering? Give tradeoff profiles, then a principled recommendation." |
| `stress` | After a candidate exists | "Here is the design. What would make it wrong? Findings first, be adversarial." |

Default to `expand` when no direction is chosen yet, `stress` when one is. Blocked rather than deciding is still a valid reason to invoke; shift the framing from "expand my options" to "here is exactly where I am stuck and what I have ruled out."

## Discovering the Consultant

Never hardcode a vendor or a script path. Resolve what is actually installed, and say which one was used in the report.

```bash
for c in codex gemini llm aichat mods ollama; do
  command -v "$c" >/dev/null 2>&1 && echo "available: $c"
done
```

Then invoke it in its own idiom. Check `--help` before composing the call rather than guessing flags, per the external-tools rule in [the global instructions](../../CLAUDE.md). Prefer the highest reasoning setting the tool offers; this is a low-frequency, high-stakes call, so latency does not matter.

When nothing is installed, say so plainly and offer the nearest substitute: an adversarial same-model pass with an explicitly assigned opposing stance, labeled as same-model so its weaker independence is visible. Do not silently degrade to that and present it as a cross-model result.

## Composing the Prompt

Tight, with the intent stated. Four parts:

1. **Context**: the constraints that actually bind, the scale, what is already fixed and not up for debate.
2. **The artifact**: the code, the schema, the design, verbatim.
3. **The ask**: expand, evaluate, or synthesize.
4. **The output shape**: name it, or the reply arrives in a form that is hard to use.

Useful shapes to request: `tradeoff profiles + principled recommendation`, `findings first`, `threat model + mitigations`, `step plan with verification`.

Two prompt rules that raise quality measurably:

- **Prefer disconfirmation.** "What would make this wrong?" outperforms "Is this right?" The second invites agreement.
- **Ask for file paths and verification steps.** A claim that names where to check is a claim you can falsify, which suppresses confident invention.

**Never paste secrets, credentials, tokens, or personal data.** This leaves the machine and goes to a third party. Redact or summarize, per [`security.md`](../../rules/security.md) and [`privacy-defaults.md`](../../rules/privacy-defaults.md). The same obligation as any external publication applies: sending content to an external service publishes it.

## Reading the Response

The response is a **relay, not a source**. Every specific it carries, a file path, a line, an API name, a version, a benchmark number, is re-verified against the primary source before it enters your work. See [`relay-not-source.md`](../../rules/relay-not-source.md). Another model's citation is exactly as likely to be a well-formed wrong coordinate as any other relay, and it arrives with more apparent authority.

| Outcome | What it means |
|---|---|
| Agreement | Real signal for calibration, and not proof. Both models may share a blindspot inherited from similar training. On a genuinely high-stakes call, ask what neither of you would see |
| Divergence | Usually the most valuable result. It marks a non-obvious tradeoff, an unexamined assumption, or an edge case one of you missed |
| It looks wrong to you | Articulate **why** before dismissing it. If the flaw cannot be stated clearly, that inability is the finding, and your confidence was the blindspot |

**Synthesize, do not select.** The best outcome is usually a third answer neither model proposed, built from what each contributed. Picking a winner throws away the part that made the friction worth generating.

Do not rush to resolve disagreement. Sit with it in proportion to the stakes. For a lower-consequence call, take a direction and move; consensus was never the goal.

## Multi-Turn

Most tools support resuming a session. Three rounds is a productive shape: evaluate the framework, drill into the specific area that surfaced, then ask for a synthesis paste-ready for the actual artifact.

Capture the session identifier before truncating output. Piping through `tail` commonly cuts the header that carries it, which forecloses returning to that thread later.

## Reporting Back

State four things, briefly:

- Which model was consulted, and that it was a different model.
- What it added that was not already on the table.
- Where it diverged, and how the divergence was resolved.
- What was re-verified against a primary source before being used.

Never present its output as your own analysis, and never present it as authoritative. It is one more perspective that has been checked, per [`ai-guardrails.md`](../../rules/ai-guardrails.md).

## Common Rationalizations

- "I am confident, so a second opinion is wasted": confidence is the trigger, per The Key Inversion. Consult when the decision is consequential.
- "A red-team subagent covers this": a same-model reviewer shares the priors that produced the decision. Label it same-model, and use it only when no other model is installed.
- "The other model cited the file and line, so it is right": its citation is a relay. Open the coordinate before using it.
- "Both models agree, so the decision is settled": agreement can be a shared blindspot. On a high-stakes call, ask what neither model would see.
- "Pasting the config file gives better context": the prompt leaves the machine. Redact credentials and personal data, or summarize.

## Red Flags

- Stop and redact when the prompt draft contains a token, a key, a password, or personal data.
- Stop and read `--help` when about to pass a flag to the consultant CLI from memory.
- Stop and state the reason in writing when about to dismiss a divergent answer; failing to state it is the finding.
- Stop and label the result same-model when the discovery loop printed no `available:` line.

## Verification

- The report names the consulted model and the CLI that ran it.
- Each specific taken from the reply has a re-read of its primary source in this session.
- The report states what the consultant added, where it diverged, and how the divergence was resolved.
- The prompt that was sent contains no credential or personal data.
- A decision the consultation changed is recorded through `/plan adr`, or the report says it changed nothing.

## Related

- [`/spike`](../spike/SKILL.md) answers a design question by building a throwaway artifact. Use it when the question is empirical rather than a matter of judgment.
- [`/interview-me`](../interview-me/SKILL.md) sharpens an underspecified request before it is worth consulting anyone about.
- [`/review`](../review/SKILL.md) and the red-team agent give same-model adversarial coverage, which composes with this rather than replacing it.
- [`/plan`](../plan/SKILL.md) records the resulting decision. A consultation that changed the direction belongs in the decision record with what changed it.
