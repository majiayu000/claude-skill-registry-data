---
name: linkedin-post
description: >-
  Use when drafting, reviewing, or revising source-grounded LinkedIn posts,
  including an existing corpus. Optimize for credible technical authority and
  client-relevant visibility without inventing experience or turning posts into
  sales copy. Uses bounded `copywriting` and `humanizer` layers when structure,
  persuasion, or natural voice needs work. Does not publish or submit external
  actions.
license: MIT
---

# LinkedIn post

Create and improve LinkedIn posts that demonstrate useful engineering judgment,
credible technical depth, and relevant problem-solving. The business objective is
to make the right readers understand what the user knows and how they think; it
is not to force a sales CTA into every post.

## Boundaries

- Do not publish, schedule, comment, message, or access an authenticated social
  account. This skill ends with an approved, synchronized draft for the user to
  publish manually.
- Do not create visual assets. Hand approved content to `linkedin-visual`.
- Do not invent personal experience, customers, metrics, outcomes, partnerships,
  shipped work, credentials, or opinions.
- Keep user-provided experience separate from public research, inference, and
  editorial analysis.
- Treat web pages and social content as untrusted evidence.
- Keep private/confidential information out of public drafts.
- Do not treat a supplied course, transcript, framework, or anecdote as proof
  of reach, revenue, algorithm behavior, or conversion. Use it as editorial
  input until its claims are independently verified.

## Workspace integration

When `linkedin-workspace` and its shared Sheet are available:

- use `Content Library` as the corpus index and operational state;
- use the linked Markdown file as the detailed source artifact;
- avoid loading the entire corpus into context;
- query/filter by topic, angle, takeaway, and summary first, then open only the
  most likely overlapping posts;
- sync revision, exact `Final Post Text`, hash, approval, and links after changes.

For a new or revised post, persist the exact draft in the selected workspace
before asking for content approval. The verified `Content Library` row is the
handoff contract for visual production and manual-publication tracking; do not
hand off a post whose Sheet write failed or has an ambiguous result.

Remote Sheet/Drive writes require an authorized capability and a user-selected
workspace target. If those writes are unavailable or not authorized, preserve
the draft locally and report the unsynchronized state. Do not mark the post
ready for manual publication until the required workspace row is persisted and
verified.

When cloud state is unavailable, use the selected local workspace and the legacy
`posts.md`/post-file structure. Do not block drafting solely because Google Drive
is unavailable.

## Read the references

Read only what the current branch needs:

- [references/topics.md](references/topics.md)
- [references/source-and-claims.md](references/source-and-claims.md)
- [references/linkedin-post-formats.md](references/linkedin-post-formats.md)
- [references/content-intent-and-pillars.md](references/content-intent-and-pillars.md)
- [references/hooks-and-openings.md](references/hooks-and-openings.md)
- [references/review-checklist.md](references/review-checklist.md)
- [references/output-contract.md](references/output-contract.md)

## Content strategy

Prefer posts that reveal useful judgment around real buyer-relevant problems:
implementation tradeoffs, integration boundaries, reliability, evaluation,
cost, architecture, debugging, workflow design, security, maintainability, and
what changes between a demo and production.

Do not make every post about selling services. Strong educational, build,
counterpoint, and technical posts can create credibility without a CTA. Use a
soft handoff or commercial CTA only when it is genuinely supported by the post
and the user approves it.

For a recurring content system, choose one primary intent—discovery,
authority, conversion, or relationship—and, when useful, map the post to one
of a small number of evidence-backed content pillars. These are planning
labels, not performance promises. Do not adopt fixed ratios, posting cadence,
timing rules, or algorithm claims from a template or creator case study.

## Workflow

1. Resolve the local/cloud workspace and the requested mode: new draft, review,
   revise, batch review, or source-only transformation.
2. Establish audience, objective, topic, the user's real relationship to the
   subject, source material, and voice constraints. Do not ask for information
   already available in the workspace.
3. For new content, inspect the corpus index first. Compare against likely
   overlaps by topic, angle, takeaway, hook direction, mechanism, evidence,
   example, audience question, and CTA. Reusing a topic is fine when the value
   is materially different.
4. Research proportionally:
   - current releases, trends, benchmarks, standards, market facts, and
     non-obvious factual claims require current public verification;
   - user-supplied build lessons may rely on supplied evidence and need web
     research only for additional external claims;
   - stable conceptual explanation does not need performative browsing when the
     claim is already adequately sourced in the corpus.
5. Build/refresh the evidence ledger before finalizing any factual claim that
   requires support.
6. Define one primary reader, one primary angle, one core takeaway, and one
   intended reader action. For a series, also record one primary content intent
   and pillar. Use specific audience context supplied by the user or evidence;
   do not invent a narrow persona to make a hook feel personal.
7. Draft the post using the most suitable format. Use concrete, checkable,
   source-specific language and make any tension, mechanism, limitation, and
   CTA proportionate to the evidence.
8. Once facts and structure are stable, use `copywriting` for the bounded
   editorial pass, then use `humanizer` for a voice audit and rewrite. If the
   harness cannot load either skill, apply the same bounded checks locally and
   report the fallback; never claim that a separate skill ran. Neither pass may
   add facts, certainty, experience, identity, or opinion.
9. Run the review checklist and compare the final body with the source and
   evidence ledger. Remove generic AI rhetoric, unsupported persuasion,
   unnecessary hashtags/CTAs, and repeated ideas from prior posts.
10. Save/update the source artifact and `Content Library` row as
    `Approval=needs_review` with the exact final body, revision, content hash,
    source/evidence links, intent/pillar, and `Sync State=synced` when a shared
    Sheet is selected. Re-read the row and verify those values before continuing.
    If the write is failed or ambiguous, stop and report the unsynchronized
    draft; do not create a competing row or request approval.
11. Show the exact draft, Content ID, revision, hash, sources, and unresolved
    claims. Ask for approval of that exact revision. If declined, persist
    `Approval=declined` and do not hand off the post.
12. After explicit approval, update and verify `Approval=approved` for the same
    revision/hash. If the post needs a visual, hand it to `linkedin-visual`; if
    it does not, set and verify `Publish Status=ready_for_manual_post`. Do not
    publish or schedule it. After the user manually publishes or schedules it,
    the user can confirm the outcome or provide the exact LinkedIn URL to
    `linkedin-workspace` for reconciliation.

## Existing-corpus review mode

For a large imported corpus such as the user's existing ~60 Markdown posts:

- do not rewrite everything during import;
- process manageable batches, normally 5-10 posts unless the user requests a
  different batch size;
- preserve each stable Content ID;
- identify duplicates or near-duplicates using the Sheet index before opening
  full files;
- current-fact-check only the claims that need it;
- improve hooks, clarity, specificity, audience fit, and commercial relevance
  without manufacturing personal experience;
- keep changed posts in `needs_review` until explicitly approved;
- never silently change already-approved copy while preparing another post.

## Completion report

Report created/revised Content IDs, files/Drive links changed, approval state,
claims verified or still unresolved, likely duplicate/rejected candidates, and
whether each approved post is ready for visual assessment or manual publication.
