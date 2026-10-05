---
name: grill-with-docs
description: A relentless interview to sharpen a plan or design, which also creates docs (ADRs and glossary) as we go.
disable-model-invocation: true
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the codebase or project files, look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.

Throughout the session, apply the `domain-modeling` skill: challenge my terms against the glossary in `CONTEXT.md`, sharpen fuzzy language into canonical terms, stress-test relationships with concrete edge-case scenarios, and update `CONTEXT.md` and `docs/adr/` inline as terms and decisions crystallise — creating those files lazily if they don't exist yet.

Do not enact the plan until I confirm we have reached a shared understanding.
