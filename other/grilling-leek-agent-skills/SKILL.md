---
name: grilling
description: Interview the user one decision at a time until reaching shared understanding, resolving each branch of the decision tree with recommended options and trade-offs. Use when a plan, design, or idea needs its soft spots found and forced into the open, or when another skill needs the interview protocol.
user-invocable: false
---

# Grilling

Interview the user about a plan, design, product idea, implementation approach, or architectural choice until there is shared understanding: relentless on the decisions that genuinely need them, silent on the ones you can settle yourself. **Do not act on the plan until the user confirms shared understanding has been reached.**

Walk the decision tree one branch at a time. Resolve dependencies between decisions in order. The **frontier** is every open decision whose prerequisites are already settled; the questions that can be asked now without guessing at answers not yet given. For each question, provide a recommended answer and concrete alternatives with trade-offs.

Finding facts is never the user's job. If a question can be answered by exploring the environment (codebase, files, docs, tools, or current implementation) inspect that context instead of asking. When a fact needs real reading, resolve it through the `research` skill's dispatch rules (its sub-agent must complete inside this session), mark the branch deferred, and keep interviewing the rest of the frontier.

## Core Loop

1. Identify the next unresolved decision that matters.
2. Try to settle it yourself: walk the ladder in **Settle it yourself first**. If any rung settles it, record the decision and move on without asking.
3. Ask **exactly one question at a time**. Asking multiple questions at once is bewildering.
4. Lead with the recommended option and explain the trade-off for every option.
5. After the user answers, update the decision ledger and infer any downstream decisions that answer implies.
6. Continue until the plan is resolved, the user stops the grill, or the remaining uncertainty cannot be resolved without external information.

## Settle it yourself first

The user's attention is the scarcest thing in the session, so a question has to earn its place: the answer must change the work *and* nothing cheaper may settle it. Before asking anything, walk this ladder and stop at the first rung that settles the decision.

1. **Context**: codebase conventions, an existing implementation of the same shape, project docs, the ledger, the effort's standing notes. Match what is already there rather than asking which way to do it.
2. **Established practice**: the conventional answer for this stack, framework, or domain. Where the ecosystem has already settled a question, take the settled answer; never make the user re-derive it.
3. **Default bias**: where practice is silent or genuinely split, take the option that is more reusable, more configurable, and less duplicated, and that avoids the smells in the `code-smells-audit` skill's index. That catalog cuts both ways: Speculative Generality is a smell too, so configurable means the seam exists, not that it is built for an imagined future.

Only a decision that survives all three rungs is a question.

## What still earns a question

Ask only about what the user's own context can settle:

- **Product and scope**: what the thing should do, for whom, and what is deliberately out.
- **Domain semantics**: what a term means here, and which concept owns a behavior.
- **Constraint-bound trade-offs**: choices hanging on their budget, timeline, team, or existing infrastructure.
- **Hard-to-reverse commitments**: data migrations, public interface shape, third-party lock-in.
- **Genuine forks**: two reasonable readings of the request that lead to materially different work.
- **ADR conflicts**: a choice that contradicts a recorded ADR. Name the ADR in the framing.

Everything else is yours to decide. Framework idiom, file layout, interface naming, test structure, error-handling shape, where a helper lives, a library choice with an obvious ecosystem default: settle these and keep moving.

## Record every default

A decision settled without asking still lands in the ledger as `implied`, carrying the rung that settled it and a one-line why. The closing summary lists them under **Defaults applied**, one line each, so the user can overturn any of them with a word. An unasked question is the point; a hidden decision is the failure mode.

## Decision Ledger

Maintain a running internal ledger:

- `settled`: decisions the user explicitly chose.
- `implied`: decisions that follow from earlier answers, plus every default you settled off the ladder, tag which rung settled it.
- `open`: branches still worth asking about.
- `deferred`: questions blocked by missing context, a pending fact lookup, external constraints, or user choice.
- `dismissed`: items the user ruled out or told you to drop. They stay silent for the rest of the session: no question, summary, risk list, or hand-off names them again.

Before asking anything, check the ledger. Never re-ask a resolved or implied branch. When a deferred fact resolves, move its downstream branches back to `open`.

## Frame the problem, then ask

A bare question is unanswerable: the user has to reconstruct what you were looking at before they can choose. Put two or three short sentences in front of it:

1. **What you found**: the concrete thing in the code, spec, or plan that forced the decision.
2. **Why it needs them**: which rung of the ladder failed, and what goes wrong if you guess.
3. **What the answer costs**: the consequence that follows the choice, not a restatement of the choice.

If you cannot state the situation plainly, you do not yet understand the decision well enough to ask about it.

## Write it in Simplified Technical English

Every word the user reads (the framing, the question, the option labels and descriptions) follows the writing rules of **ASD-STE100 Simplified Technical English**. The target is a decision the user understands on one read, with no jargon to decode and no term they must look up.

- **Short sentences**: 20 words maximum in an instruction, 25 in a description. Never drop the article, subject, or verb to make the count; rewrite the sentence instead.
- **One topic per paragraph**, 6 sentences maximum.
- **Active voice, and name the actor.** "The job retries the payment", not "the payment is retried".
- **One word, one meaning.** Choose a term and keep it for the whole session. Never alternate between `ticket` and `issue`, or `seam` and `boundary`.
- **No noun stack longer than 3 words.** "User account deletion confirmation screen" becomes "the screen that confirms account deletion".
- **Plain words around exact names.** Technical names stay exact (a class, a package, a framework, a domain term from `GLOSSARY.md`) because a plainer word would lose the precision. Everything around them is plain English, and a load-bearing name gets a gloss on first use: "a seam (the place a test calls the code)".
- **No abbreviation the user has not used first**, and no idiom, metaphor, or figure of speech.

These rules govern the text shown to the user. They do not govern the code, the spec, or any artifact; those keep the project's own vocabulary.

## Asking the question

Where `AskUserQuestion` is available, use it: decisions become click-to-answer:

- One question per call.
- 2–4 options, every one real: no filler choices, no explicit `Other` (the tool provides free-form input).
- Recommended option first, label suffixed ` (Recommended)`, labels 1–5 words, `header` ≤ 12 characters.
- Describe what each option commits the project to, not just what it is.
- `multiSelect: true` only when options legitimately stack.
- When the options are artifacts to compare side by side (a signature, a schema, a payload, a screen layout), put each one's snippet or ASCII mockup in that option's `preview`. `preview` works only on a single-select question.

In Codex, when `request_user_input` is listed for the turn, ask through it with the same shape (recommendation first, 2–4 real options); it has no `preview`, so put a short snippet in the option description or fall back to chat for side-by-side artifacts.

Without either tool, ask the same shape in chat (numbered options, recommendation first, trade-off per line, and under each option the fenced block its `preview` would hold) and wait for the answer. Never print fake tool JSON.

A rejected question did not land. Ask the same decision again once, rewritten: the situation first, fewer terms, and each option stated as what will happen. If the user rejects that too, take the recommended option, record it as `implied`, and move on.

## Stop Conditions

Stop when:

- The user says to stop.
- The user confirms shared understanding: the only exit that permits acting on the plan.
- Remaining branches depend on information outside the current context.

A request for a summary, PRD, or implementation plan is a request to *record* the settled decisions, not permission to resolve open branches by yourself.

Before the plan resolves, sweep the branches grills skip. Each one has forced a rebuild after the build:

- **Trigger**: does the behavior run automatically, or does a person start it? Where in the UI do they see and drive it?
- **Ownership**: who creates, edits, and removes each new entity, and on which screen?
- **Display**: for an integration, which returned fields the product shows and which it drops, and their order of importance on the screen. Offer competing layouts as ASCII mockups, in each option's `preview` or, without the tool, in a fenced block under each option (see **Asking the question**).
- **Failure**: what the user sees when a dependency fails or returns partial data.

Settle each off the ladder or ask.

Before ending, settle or explicitly abandon every `deferred` branch; no fact lookup may still be running, and no task ID belongs in any summary or hand-off text (a task handle dies with the session).

End with a compact summary of settled decisions, the **Defaults applied** block, and unresolved risks. When invoked directly (not from another skill), also print the routing block from `grill-me`: only the outermost skill prints one.
