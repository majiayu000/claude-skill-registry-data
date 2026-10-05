---
name: optimise-seo
description: Use when explicitly authorized to implement a bounded, approved SEO action in a codebase or content system, verify the exact change, and report its limitations; do not use for broad audits, self-approved production changes, or outcome guarantees.
---

# SEO Implementation Coordinator

## Purpose

Apply or prepare a specific, user-authorized SEO change after its evidence, product decision, owner, scope, acceptance criteria, verification, and rollback are known. This skill coordinates the chain from an approved action to local acceptance and, only when separately authorized, exact-candidate release and live closeout. It is not an audit, an auto-publisher, or implied deployment authority.

Read `references/implementation-gate.md` before modifying a workspace.
Read [verification-modes.md](references/verification-modes.md) before choosing per-action, batch-final, or production-comparison verification.
Read [external-closeout.md](references/external-closeout.md) before identifying or releasing a production candidate, especially from a dirty or generated worktree.

## Authorization gate

Require all of the following before changing files or systems:

- explicit user/authorized-owner request to implement the named action;
- validated upstream finding/action plan or equivalent evidence record;
- exact target repository/content system and permitted scope;
- owner, acceptance criteria, verification plan, risk, and rollback;
- facts/copy/schema/data approved for the target locale.
- independent authorization states for implementation, release, and provider mutation.

If any is missing, prepare an implementation plan or patch proposal only. Do not infer approval from an audit result, a pending action-plan artifact, a backlog item, or the desire to “improve SEO.”

## Implementation workflow

1. **Reconfirm scope.** Quote the action ID/objective, target files/URLs, intended behavior, non-goals, and success/guardrail conditions. Inspect the current state; preserve unrelated work.
2. **Choose the owning lane.** Content edits follow `seo-content`; technical changes follow `seo-technical`; markup follows `seo-schema`; locale annotations follow `seo-hreflang`; sitemap changes follow `seo-sitemap`; product/feed, local, video, news/Discover, agentic task-flow, architecture, and authority work follows its matching specialist. Measurement-only actions follow `seo-performance` or `ai-visibility-monitor` and never become implementation by implication. Do not silently substitute a different change.
3. **Make the smallest reversible change that satisfies the decision.** Modify only the approved files/data. “Smallest” cannot shrink or replace an explicit product-owner end state. Preserve facts, locale, consent/accessibility, analytics, and security behavior. Do not add `llms.txt`, crawler directives, schema, pages, links, or copy merely because they sound SEO-related.
   For an approved broad rank-higher/site optimization, “complete” also means the owned baseline surfaces were handled: query-to-page ownership, unique title, semantically complete meta description, canonical/indexability, and hostname favicon/site identity. Implement them from approved facts and owned brand assets or record the exact blocking dependency; do not silently omit them as minor details. When the approved title, description, or H1 is exact, bind that copy into the live release plan instead of accepting presence-only validation.
4. **Preserve source and candidate identity.** In a dirty worktree, identify authored sources, generators, and generated outputs before editing. Never reset, clean, overwrite, or revert unrelated work. Record a candidate manifest containing expected source paths, generated outputs, build identity/hash, corpus summary, and `gitDirty=1` when applicable; compare post-build generated diffs with the initial worktree.
5. **Verify the implementation.** Choose a verification mode and run the complete declared gate. Batch-final verification accumulates every action's criteria and reruns the entire final gate after a failure. Match the verification universe to the change universe; record every attempt and what remained unverified.
6. **Close externally only when separately authorized.** Discover the actual deployment mechanism, verify the candidate identity, deploy exactly that candidate, record the deployment ID and alias, and run `seo-technical` live verification over the affected universe. Provider operations are a further authorization phase owned by `seo-performance` and require their own receipt.
7. **Prepare handoff.** Report changed files, candidate identity, exact behavior, test attempts, release/live evidence when authorized, provider-operation evidence when authorized, pending outcomes, rollback, and comparison prerequisites. If a later phase lacks authorization, name that exact closeout blocker; when authorization arrives, resume this same chain.

## Guardrails

- Never promise crawl, index, rank, citation, traffic, revenue, or conversion results.
- Do not expand the task from one approved action into a broad “fix everything” change.
- Do not overwrite unrelated user work, secrets, configurations, or analytics data.
- Do not replace a dirty worktree with a clean copy or edit a generated artifact without identifying its source/generator ownership.
- Treat crawler policies, canonicals, robots/noindex, redirects, privacy/security, pricing, health/legal/financial claims, and localization as high-risk changes needing explicit review and rollback.

## Output

Return an implementation receipt: decision/action/evidence reference, files/systems changed, candidate manifest, acceptance verification and attempts, external/production checks, release/live receipt when present, provider receipt when present, pending outcomes, known limitations, and rollback. If no implementation was authorized, return a reviewable plan rather than making changes.
