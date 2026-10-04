---
name: documenter
description: "Evidence-backed review, writing, revision, or restructuring of durable READMEs, specs/ADRs, agent guides, and public API/release docs when claims or structure need judgment. Route AGENTS.md to agents-md-generator; add documenter-coauthoring for staged work. Let matching domain skills lead when code, packaging, or release machinery also changes. Not for mechanical copy edits, chat summaries/handoffs, prompt behavior, binary-file work, regulated document control, or docs-site tooling alone."
---

# Documenter

## Boundaries And Composition

- Treat review and chat-only draft requests as read-only. Edit repository files
  only when the user asks to create or update them. If the user later switches
  to apply mode, refresh the target, evidence, applicable guidance, and initial
  diff before editing.
- Before editing, inspect the target and relevant initial diff when available.
  Preserve and attribute existing changes, patch around clear overlaps, and stop
  rather than overwrite when ownership or intended content is ambiguous.
- Use `agents-md-generator` as primary for root or nested repository
  `AGENTS.md` files.
- Add `documenter-coauthoring` for user-directed context gathering, outline
  agreement, or staged drafting. Document length neither selects nor excludes
  it.
- When implementation, release machinery, or doc-site infrastructure also
  changes, use the relevant implementation or project skill for that work and
  apply this skill to the documentation content.
- For an authorized change involving generated output, find its authoritative
  source, determine whether source and output must remain synchronized, and
  inspect the generator's side effects before editing. Regenerate only when
  safe and authorized; never hand-edit the output. If required synchronization
  cannot be completed, do not create a partial inconsistent state. When local
  policy permits temporary divergence, leave it only with explicit user
  acceptance and never report that state as complete. If a failed regeneration
  already created a partial state, undo only this task's safely attributable
  delta when possible; otherwise stop. When synchronization remains blocked,
  report exact source and output states, the blocking side effect or dependency,
  and the smallest authority or safe tooling needed to continue.
- Use a specialized workflow for regulated document control.

## Core Workflow

1. Classify the work before writing:
   - intent: review, chat-only draft, or apply
   - audience and reader task
   - document type and output target
   - claim status: current, proposed, normative, or historical
2. Read the target, applicable local guidance, existing changes, and evidence
   relevant to affected claims:
   - current behavior: code, config, schemas, tests, safe command output,
     shipped artifacts, and applicable versioned primary sources for external
     contracts
   - proposed behavior: supplied requirements, draft decisions, explicit user
     direction, and visible open questions
   - normative behavior: accepted decisions, approved specifications, policies,
     and standards
   - historical claims: versioned records, changelogs, release artifacts, ADRs,
     and other dated evidence
   Local guidance controls placement and conventions; claim-specific evidence
   controls factual content. Reconcile conflicts by scope, version, and
   authority. Expose unresolved material conflicts and pause when the requested
   edit requires choosing a source; never choose silently or change
   implementation to make prose true. A proposal may preserve an unresolved
   conflict, but factual current-state documentation must label a disputed
   material claim as unknown or stop when settling it is required.
   For review-only work, validate as applicable and return prioritized,
   evidenced findings with limitations; skip drafting and edit-only completion.
   For a chat-only draft, continue without repository writes and label its
   validation status.
3. Choose the smallest coherent change:
   - update only affected sections for a narrow edit
   - outline a new or large document before drafting it autonomously
   - before restructuring, map meaningful content as retained, moved, or
     intentionally removed and search for inbound links or anchors that may
     break; when applying the change, update in-scope callers, preserve a
     compatible anchor, or defer the breaking removal and report it
4. Draft in the repository's native markup and language conventions:
   - organize standalone pages around one dominant reader task; gateway
     documents such as READMEs may deliberately orient and route several tasks
   - mark planned behavior and illustrative examples clearly
   - keep examples free of credentials, private data, and environment-specific
     secrets
   - for API comments, document contracts and non-obvious behavior rather than
     narrating syntax
5. Validate proportionally:
   - inspect validation commands for file writes, generated output, dependency
     installation, and external effects before running them; in review or
     chat-only draft mode, use read-only or check-only variants
   - run applicable existing documentation builds, formatters, linters, or link
     checks
   - check local paths, anchors, identifiers, filenames, and cross-references
   - run examples only when they are safe and local
   - do not publish, deploy, release, install dependencies, migrate data, or
     cause other consequential mutations without the required authority;
     authoring or validation intent does not supply that authority
   - report important examples and commands as observed, statically inspected,
     illustrative, or unverified when the distinction matters
6. Tighten and hand off: remove duplication and accidental placeholders, link
   new durable docs from the nearest existing index when appropriate, review the
   resulting diff when files changed, and report checks plus material uncertainty.

## Document-Type Decisions

Use the repository's established format first. Use Diataxis as a lens for the
reader's dominant need, not as mandatory site architecture.

- **Tutorial:** teach by doing and make each stage produce an observable result.
- **How-to:** solve one known task without unrelated theory.
- **Reference:** present contracts, options, flags, or facts for fast lookup.
- **Explanation:** clarify concepts, rationale, and trade-offs.
- **README or hub:** orient its audience and include or link only the install,
  use, build, test, or release workflows relevant to that audience.
- **Spec or proposal:** state status, problem, scope, constraints, decisions,
  and unresolved questions appropriate to its phase.
- **ADR:** separate context, decision, status, and consequences.
- **Changelog or release note:** emphasize user-visible effects, breaking
  changes, and required upgrade action.
- **API documentation or comment:** follow native language tooling and describe
  inputs, outputs, errors, invariants, side effects, and examples only where
  they add useful contract information.

## Bundled References

- Load [references/doc-templates.md](references/doc-templates.md) when no
  stronger local format exists and a compact README, ADR, endpoint, API-comment,
  or changelog structure would help.
- When revising this skill family or its activation boundary, use
  [references/trigger-evals.md](references/trigger-evals.md).

## Completion Criteria

For review-only work, finish when findings are prioritized, evidenced, scoped,
and paired with material limitations. For a draft or applied change, finish when
the artifact serves its stated audience and current stage; current, proposed,
normative, and historical claims are distinguishable; material claims have
appropriate evidence; links and examples have an honest validation status;
required generated artifacts are synchronized; incomplete synchronization is
reported as unfinished work rather than completion; meaningful content was not
lost silently; and placeholders are removed or explicitly labeled and accepted
for the current stage.
