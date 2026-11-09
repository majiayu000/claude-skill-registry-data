---
name: define-work
description: Turns a request into an approved design document before any code is written. Use when the operator asks to build, add, change or design something whose intent, scope or constraints are not yet settled ("I want to add…", "what should we build", "help me think this through", "let's design this"), or asks to brainstorm, scope or spec a change.
---

# Define Work

This skill answers "what should we build". It ends with an approved design
document. It does not plan and it does not build.

## Adapt

An operator instruction, then the project's declared design workflow (its
template, location, review and approval steps), win over every default below.
A workflow applies only when it is written down or the operator states it.

## Procedure

1. **Size the request** and tell the operator the size; they can change it.

   | Size | Sign | Then |
   |---|---|---|
   | Clear task | Everything that matters is in the request. | Say so. Write the request as a one-line design document, which the request itself approves, and go to step 9. |
   | Small change | The intent is clear; a few choices are open. | Steps 2–5, a short design document (step 6), then steps 8–9. |
   | Project | Intent, scope or constraints are open, or several parts interact. | Steps 2–9, with a design document. |

   When the work outgrows its size, say so and step up. A request that holds
   several independent projects: agree an order and define one at a time.
   The operator can skip the questions; that removes only step 3. State the
   significant choices (platform, language, approach) in one line. Recon
   (step 2), the alternatives (step 5), the document (step 6) and, for a
   project, the verification stage (step 7) still run; step 7's questions
   for the operator become author's calls, listed in the document. Then hold
   at the approval gate (step 8).

2. **Recon before questions.** Read the project instructions (CLAUDE.md,
   AGENTS.md, CONTRIBUTING and the documents they name), the code and docs the
   request touches, existing designs and specs, and any design or spec
   workflow the project declares. Find what the repo contains where the
   request lands, what the touched files declare, who uses the symbols the
   change touches, and, for a structural change, what else breaks if they
   change. Answer from the repo what the repo can answer; ask the operator
   only the rest. A text match is not a binding: report each finding as what
   it is. Then play back the system in one paragraph: what the code does
   where the request lands, and how the request relates to it. The operator
   corrects it before the first question.

3. **Questions.** One question per message, in one sentence. Open questions
   first, anchored in a concrete case ("walk me through the last time this
   went wrong"); offer options only when the operator is stuck. When the
   operator defers, propose a concrete default. Cover, as ground and not as a
   script: purpose and what success looks like; goals; non-goals; what would
   make it a failure even if it works; constraints; existing work and earlier
   attempts; which implementation choices the operator wants to make and
   which they leave to you. A choice you make goes in the design as the
   author's call, never as the operator's.

   Challenge the request. Name each assumption in it that the recon
   contradicts or that you doubt, with the evidence, and say where you
   disagree before you ask the next question. Agreement is not help: the
   operator asked for a design, and the argument is part of it.

4. **Play back** each part as soon as you understand it, in a short
   paragraph, with your guesses marked as guesses. The operator corrects it;
   then go on to the next part.

5. **Alternatives.** Weigh the approaches and drop any that conflicts with
   the stated purpose. Keep each dropped or rejected approach with its
   reason for the document (step 6). Show two or three, with your
   recommendation, only when the choice is the operator's.

6. **Design document.** Write it where the project keeps designs, else at
   `docs/specs/YYYY-MM-DD-<topic>-design.md`. The project's template wins;
   otherwise cover:
   - intent: the problem, and why it matters now
   - goals and non-goals
   - constraints
   - the decided parts of the approach, each marked as the operator's or the
     author's call, with a text diagram where several parts interact
   - alternatives considered and rejected, each with its reason, so that a
     later session does not propose them again
   - the files the change is expected to create or change, from the recon,
     with one line each on why
   - what is left to the builder
   - acceptance: what "done" means, as checks a test or a command can decide

   A small change's document is short: intent, the description, and
   acceptance. Cite the recon evidence (file:line) for each claim about
   existing code. Match the length to the substance; no filler sections.

7. **Verification stage.** Three reads of the document, in this order, each
   by a fresh reviewer that has not seen this conversation, on a capable
   model, given the document at `<path>` and only the files it cites. A
   read that finds something is run again after the fix, until a run finds
   nothing or the read has run three times; what is still open after the
   third run goes in the document as not resolved.
   1. **Comprehension.** Brief: explain the feature and how the current
      system relates to it, from the document alone. Each wrong or missing
      statement is context the document lacks: add it.
   2. **Critic.** Brief: you are an expert reviewer of this codebase; find
      what the design misses, the assumptions that are wrong and the edge
      cases it does not handle; report each with its evidence, most
      important first. Verify each finding against the repo and the
      conversation. A confirmed finding changes the document; a refuted one
      is recorded with its reason and dropped. The read passes when only
      nitpicks remain.
   3. **Sufficiency.** Brief: you are the builder who must plan from the
      document and cannot ask its author; report only the questions where a
      wrong guess would change the plan, each with why, most important
      first; skip what the document leaves to the builder and what a builder
      could decide; if none remain, say "nothing important left". Sort each
      question:
      - answered by the conversation or the repo: write the answer in;
      - minor: decide it, and mark it in the document as the author's call;
      - the operator's: only the operator can answer it, and the answer
        changes what gets built.

      Send the operator's questions in one message per run, most important
      first, and write the answers in.

8. **Approval gate.** Nothing is built before the operator approves the
   design document. Building is product code, scaffolding, dependency
   installs or project creation; reading and recon are not. Hand over the
   document with the list of author's calls, so the operator checks them
   while reading; for a small change, show its text in chat and take the
   approval there. Approval covers only the text the operator saw. An
   explicit instruction to build without review ("just build it", "no need
   to approve") is the approval. For every size, record it in the document
   header: `**Status:** approved by <who> <YYYY-MM-DD>`. A spike the operator
   agrees to is labeled throwaway; keeping any of it needs a new approval.

9. **Hand over.** Give the operator the approved document's path. It is the
   authority spec for planning. Planning follows the project's planning
   workflow, or the operator's instruction.

## Report

The design document is the report. Each claim about existing code cites its
evidence. Each check that did not run is named in the document as not run,
with its reason.
