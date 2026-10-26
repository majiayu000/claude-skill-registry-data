---
name: write-prd
description: Turn project context (intake answers, meeting transcripts, the cadrage doc) into a clear Product Requirements Document in docs/product/prds/. Use when starting a project, when /progix needs the PRD, or when the user says "write the PRD", "draft requirements", or requirements changed enough to need a rewrite. The PRD is the product's source of intent — what and why, before how.
argument-hint: [project/feature name or "from <context path>"]
allowed-tools: Read Write Edit Glob Grep AskUserQuestion
---

## Context

- Existing PRDs: !`ls -1 docs/product/prds | grep -E '^[0-9]' || echo "none yet"`

## Task

Produce the PRD for **$ARGUMENTS** at `docs/product/prds/NNNN-<slug>.md` (number = next integer after the existing PRDs above). The repo copy is the mirror; the human original lives in Notion → project → PRD.

1. **Gather intent, not solutions.** Read everything the user has: intake answers, pasted transcripts, the PM cadrage doc, `docs/product/vision.md`. The PRD captures the problem and the what/why — keep tech choices out (those are ADRs + specs).
2. **Follow the template** `docs/product/prds/_template.md` exactly: Problem · Goal & success metric · Solution sketch (user-visible behavior; mark painted doors) · Acceptance criteria (become tests) · Non-goals · Clarifications · Proof · Rollout. Set `Status: draft`, `Size: M | L`.
3. **Interview only for gaps** (AskUserQuestion): the non-goals, the success metric, and the single signature feature are the parts requesters most often skip and matter most — pull them out. Anything still open becomes a Clarifications line (dated), not an assumption. Zero open questions is a success state.
4. **Keep it tight.** The PRD is read by the client and the PM — plain language, honest scope. Non-goals are as important as goals: they're how budget and timeline survive. Acceptance criteria must be phrased so each maps to a Jest/RNTL test or a Maestro step.
5. **Map forward.** Each MVP scope item should be phrasable as one or more specs — end by listing the first 2–3 `/create-spec` candidates, ranked.
6. **Register + mirror.** Add the PRD to the index in `docs/product/prds/README.md`. Mirror the human original into Notion if the MCP is connected (or stage it for `/progix` to place). Run `npm run docs:lint`.

A good PRD lets `/create-spec` run without re-litigating product questions — that's the test.
