---
name: planning
description: "Use before touching code on any change that needs thinking through, and always on entering plan mode or writing an implementation plan. Trigger on 'plan this', 'how should we build X', 'what is the approach', 'design this feature', 'propose the steps', 'work out how to fix this bug', 'how should we refactor this', and 'do not write code yet', even when the user never says the word plan. Produces a concise plan with an ASCII diagram, a YAGNI check, validation against the project's docs, an interview on anything the project has no convention for, a subagent review phase, and a verification phase."
---

# Planning

A plan says what will change and why, in enough detail that a junior developer could execute it without asking questions. It is not the change itself. The junior still writes the code, so the plan's job is to leave no decision open, not to leave no line unwritten.

That distinction is what keeps a plan reviewable. Whoever approves it reads it in a couple of minutes and answers yes or no. Nobody can approve two hundred lines of CSS pasted into a step, so a plan carrying its own implementation smuggles that code past the only review it gets before it lands.

## What goes in, and what stays out

Write down the decisions. Leave out anything the executor can look up.

The reader is deciding whether to approve the plan, and the executor is a competent developer or agent with the repo, its docs, and any source material in front of them. So a step names the file and the change, and the plan spends its words on the choices that would otherwise be made badly, made twice, or quietly reopened.

In the plan:

- the decision, and the reasoning wherever it isn't obvious: which of two approaches, and why
- anything already settled with the user, so the executor doesn't reopen it
- constraints the code doesn't announce, above all the ones that break something quietly: names existing callers or tests depend on, an order that matters, a call that has to come after another, a convention this change deliberately breaks. Ask what the executor could change innocently and only hear about from a red test.
- where the source material lives, by path, url, or id

Out of the plan:

- code. No function bodies, no CSS rules, no markup, no values copied out of a design or a spec. For a value, ask whether writing it down records a decision or copies a reference. A breakpoint read off the design is a reference, so point at the design. `session.set_expiry(0)` is the decision itself, that an unticked box ends the session when the browser closes, so write it even though Django's own docs describe the call. If the executor can look the value up once they know the decision, it doesn't belong here. Same for a line or two that is itself the decision, such as a signature the rest of the plan hangs on.
- anything transcribed from a source the plan has just pointed at. If the executor can read the design file, copying it into the plan only creates a second copy to go stale.
- restatements of this skill. It is loaded when the plan runs, so the plan needn't explain what the reviewers look for or why a fresh auditor helps.

If a step seems to need the code to be unambiguous, the ambiguity is usually in the decision above it. Name that decision instead.

## Ground the plan in the project's rules

Before drafting, read the project's own documentation so the plan follows the house rules, not your defaults:

- `CLAUDE.md` or `AGENTS.md`, and the docs they point to
- what the product is for and what is out of scope (for example `docs/PRODUCT.md`), along with the decisions already taken, so the plan does not reopen a settled question
- coding rules and linter configs (for example `docs/CODING-RULES.md`)
- architecture docs when the change spans components (for example `docs/ARCHITECTURE.md`)
- testing docs (for example `docs/TESTING.md`), so verification uses the project's real test commands

Validate the drafted plan against these before presenting it. If the plan must break a documented convention, say so and why, so the reader approves the deviation knowingly.

Reading widely is not licence to write widely. What the reader needs from all of it is a sentence or two, and the rest shows up as steps that happen to be right.

## Ask when the project has no answer

Reading the project's docs settles most questions. This rule is for what they don't cover: a code path with no precedent in the repo, a choice that would set a standard the next change copies, or anything the plan would otherwise have to assume. Interview the user and get a decision before presenting the plan.

An assumption buried in a plan is dangerous precisely because plans get approved. The reader is checking the shape of the change, so a guess written in the same confident tone as the decisions goes by unnoticed, and by the time it turns out wrong it is in the repo with sign-off behind it. An accidental convention is worse still, because whoever writes the next change copies the pattern they find, and a choice made in passing quietly becomes the house style.

How to ask:

- Ask straight away when the gap changes the shape of the plan, since everything downstream gets drafted on top of it. Hold the smaller ones and ask them together, before presenting.
- Offer the options you can actually see, each with what it costs, and say which one you would pick and why. "How should we handle caching?" hands back the work you were asked to do.
- Say what depends on the answer, so the user can judge how much it matters.
- Record the answer in **What and why** as settled, with the reasoning. That is what stops the executor, or a later session, reopening it.

Not everything needs asking. A question the docs already answer needs reading, not an interview. A choice that is local, reversible, and invisible outside the file it lives in needs a sensible default and a line in the plan. Save the interview for what the project will have to live with.

## YAGNI is the default

Plan the smallest change that fully satisfies the request. Apply this when designing the code paths; it doesn't need its own section in the plan:

- no abstractions for hypothetical future callers: no single-implementation interfaces, no config for values that never vary
- no opportunistic refactoring bundled into the change
- prefer extending existing code over adding new layers

## Structure of the plan

Keep the plan readable in a couple of minutes. Use this shape:

```markdown
## What and why
One or two sentences: the change, and the problem it solves. Any
context the reader needs, and anything already agreed, goes here.

## How it fits together
A diagram (see below), plus a sentence or two walking through it.

## Steps
1. Ordered, concrete steps. Each names the exact file(s) it touches
   and what changes, in one to three lines.

## Review
Which reviewers run, and what each is given. A line each.

## Verification
The test command, the functional steps, and the final audit.

## Documentation
Each doc this change invalidates and the update it needs. A line each.
```

Concrete means real paths, functions, and commands: "add `validateVoucher()` to `src/vouchers/service.ts`", not "update the voucher logic". Vague steps push the thinking onto whoever executes the plan. Concrete stops at the boundary of the file and the change; past that it is transcription.

Budget the Steps. They fit on one screen, roughly 60 lines, because Steps is the section that bloats: length there is nearly always copied detail rather than decisions, so cut there first. A Steps section that will not fit is usually a change worth splitting.

The other sections carry their own limits rather than a share of that one. The diagram stays at five to ten nodes, and Review, Verification, and Documentation run a line per reviewer, per command, and per doc.

## The diagram

Every plan includes one diagram showing the components the change touches and how they interact:

- a **flow** of calls or data for new or changed logic
- a **sequence** across lanes when the change spans components or services
- a **model** of the types and their relationships when the change is mostly the domain model

Draw it in ASCII inside a plain fenced block. Plans are read in a terminal, which has no Mermaid renderer: a Mermaid block arrives as its own source, so the reader parses syntax instead of seeing the shape.

Keep it small (five to ten nodes), name nodes after real files, classes, or services, and mark what is new or changed so the delta is visible at a glance. The diagram's job is to show the change, not the whole system.

```
  POST /checkout
        |
        v
  api/routes/checkout.ts
        |
        v
  vouchers/service.ts       [new] validateVoucher()
        |
        v
  vouchers/repository.ts
```

## The review phase

Once the change is implemented, review it with subagents launched in parallel. A subagent starts with none of the context built up while writing the code, so it reads the diff the way a reviewer would: it can only judge what is actually there. Each reviewer covers one concern:

- **Requirement fit** (`model: "sonnet"`): does the change actually do what the requirement asks? Give this reviewer the original requirement and the diff, nothing else.
- **Project conventions** (`model: "haiku"`): does the change follow the project's documented rules? Give this reviewer the coding rules and architecture docs alongside the diff.
- **Simplicity and YAGNI** (`model: "sonnet"`): code smells, unnecessary abstractions, speculative flexibility, and anything that could be done more simply.
- **Comments** (`model: "haiku"`): over-commented code. Comments that restate the code, narrate the change, or justify it to a reviewer are noise; only comments that carry constraints the code can't show should survive.

Pass the model to the Agent tool. The Haiku reviewers match the diff against something already written down, a documented rule or a comment that either carries a constraint or doesn't, and a checklist is what the cheap model runs reliably. The Sonnet reviewers have no checklist: they judge whether the code means what the requirement asked for, and whether an abstraction earns its keep.

Reviewers report findings; they don't fix. Every finding comes back to the main agent to resolve, and changed code goes back through a fresh review. Repeat until the reviews come back clean.

In the plan itself, this section is one line per reviewer, naming what that reviewer is handed and which model it runs on. The briefs above are already in context when the plan runs, so repeating them in the plan is padding.

## The verification phase

Every plan ends with a verification phase covering both kinds of testing:

- **Automated tests**: which tests will be written or updated, and the exact command that runs the suite. Follow the project's testing docs.
- **Functional testing**: the exact steps to run the product, drive the changed behaviour, and what the expected result looks like. "Run the tests" is not functional testing; using the feature is.

If a step can't be verified locally (needs credentials, a deployed environment), say so in the plan.

When verification is done, spawn one final subagent on Haiku (`model: "haiku"`) to audit the whole plan. Give it the full plan and access to the repo, and have it check every part off: each step done as written, every review finding resolved, both kinds of verification actually run, every listed doc updated. The agent that did the work is the worst judge of whether it's finished; a fresh context can only trust what it can see in the repo. The auditor reports gaps, the main agent closes them, and the work isn't complete until the audit comes back clean.

Write this section as the commands and the steps. The reasoning above is why the phase exists, not something the plan repeats.

## Keep the docs from rotting

A stale doc misleads worse than a missing one, so updating docs is part of the change, not a follow-up. List every doc the change invalidates and the update each needs: the README, architecture and testing docs, coding rules, API references, runbooks. Check `CLAUDE.md` and `AGENTS.md` too; a renamed file or command breaks the pointers they hold. If nothing needs updating, say so, so the reader knows it was checked.

One line per doc: the path, and what changes in it.

## Before presenting

Read the plan back twice.

First as the junior who has to execute it. Every step names its files, every command exists in the project, the diagram matches the steps, no step leaves a decision hanging, and no assumption is standing in for an answer the user should have been asked for.

Then as the reviewer who has to approve it, with a delete key. What here could the executor have worked out alone? Copied values, restated instructions, background that belongs in the source rather than the plan. Cut all of it. The first read can only make a plan longer, so the second one is what keeps it a plan.
