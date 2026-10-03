---
name: ord-align
description: Validate whether an OSS tool is worth building through staged namespace, existing-solution, and feasibility review
type: analysis
version: v0.2
required_conventions: [alignment-page]
context_intake: scoped
research_workflow: lightweight
---

# ORD Align

Invoke as `/ord-align`.

Rapid alignment check for an ORD candidate. Validates feasibility, checks the npm namespace, surveys existing solutions, and produces a go/no-go decision only after staged HTML review approval.

## Report-First Approval Gate

Default to scope-first approval. Before namespace checks, existing-solution review, synthesized feasibility analysis, verdicts, downstream routing, or markdown writes, inspect only enough repository, user, and source context to identify the candidate, clarify scope, propose the validation plan, list assumptions, and ask 1-3 required user questions when needed.

Stage 1 output is a lightweight `review` HTML alignment page at `alignment/ord-align-<slug>.html` plus a concise conversation request for final compiled YAML approving the validation scope. The page must render the candidate summary, scope/non-goals, proposed package-name checks, existing-solution check categories, feasibility dimensions, assumptions, proposed final artifact path, and approval gates. Stop for final compiled YAML. Do not run `npm view`, synthesize a verdict, recommend GO/NO-GO, write `alignment/ord-<slug>.md`, or emit downstream routing in Stage 1.

After final compiled YAML approves the validation scope, perform the lightweight ORD validation in the same `review` HTML page. Run the npm namespace checks, existing-solution checks, feasibility analysis, effort estimate, adoption-signal review, and evidence review. Then stop again for feedback-only YAML or final compiled YAML artifact approval before writing the markdown alignment doc.

Only after final compiled YAML approves a GO artifact may this skill write `alignment/ord-<slug>.md` and convert the HTML page to `confirmed`. Emit downstream routing after approved artifacts have been written or updated: route to `/ord-ship` after an approved GO markdown doc is written, or route back to `/ord-scan` after an approved NO-GO outcome is preserved in the confirmed HTML page.

## Staged Alignment Workflow

Use this staged workflow for every candidate validation.

1. **Stage 1 - Candidate scope discovery and approval.** Read the most recent approved ord-scan output or `$ARGUMENTS` for the candidate. Inspect only enough context to identify the tool concept, candidate package names, target developer persona, intended v1 boundary, licensing/dependency concerns, and source categories to check. Ask 1-3 required user questions only when the available context is missing, contradictory, or unsafe to interpret. Build `alignment/ord-align-<slug>.html` in `review` status and stop for final compiled YAML approving the validation scope.
2. **Stage 2 - Validation and artifact review.** Only after approved scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, run the validation checks. Check npm namespace availability with `npm view <name>` when possible, inspect existing solutions, evaluate whether v1 can ship in 1-3 days, estimate effort, and review adoption signals. Update the same HTML page with the complete validation substance as structured review UI: namespace results, existing-solution comparison, feasibility matrix, effort estimate, evidence notes, assumptions/confidence, verdict rationale, proposed final artifact path, and artifact approval gates. Stop for feedback-only YAML or final compiled YAML artifact approval. Do not write `alignment/ord-<slug>.md` in Stage 2.
3. **Stage 3 - Finalize approved outcome.** Consume final compiled YAML for artifact approval only when it has `approval_status: ready-for-agent-review` and no unresolved negative feedback. Apply approved edits first. If the approved verdict is GO, write the one-page markdown alignment doc to `alignment/ord-<slug>.md` and convert the HTML page to `confirmed` with the approval record preserved. If the approved verdict is NO-GO, confirm the HTML page with the approval record and do not create the markdown alignment doc. Emit routing only after the approved artifact has been written or updated.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, package-availability, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence.
- For target persona, scope boundary, v1 ambition, risk appetite, naming preference, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, state what is known, what is inferred, and what evidence would change the verdict.

## Process

1. **Identify candidate:** Read the most recent approved ord-scan output or `$ARGUMENTS` for the tool concept to evaluate.
2. **Light interview before Stage 1 approval:** Ask only what's needed:
   - Target developer persona unclear?
   - Scope boundary question (what's in v1 vs. later)?
   - Licensing or dependency concern?
3. **Validate after Stage 1 approval:**
   - **npm namespace:** Is the desired package name available? Check `npm view <name>`. If taken, is a scoped package (`@scope/name`) viable?
   - **Existing solutions:** What already exists? Why is it insufficient? Be honest. If a good solution exists, recommend NO-GO.
   - **Feasibility:** Can v1 ship in 1-3 days? What's the minimal useful API surface?
   - **Effort estimate:** Break down into core logic, CLI/API surface, tests, docs, and publish pipeline.
   - **Adoption signal:** Is there evidence developers want this? Use GitHub issues, forum posts, developer discussions, or prior ord-scan evidence when available.
4. **Verdict review:** Present GO or NO-GO with one-line rationale in the Stage 2 HTML page and wait for artifact approval.
5. **If approved GO:** Produce a 1-page alignment doc:
   - Package name (confirmed available or scoped fallback)
   - One-line description (what goes in package.json)
   - Target developer persona
   - Core API surface (3-5 exported functions or CLI commands)
   - Tech stack (TypeScript, build tool, test framework)
   - Ship deadline (date)
   - Success metric (downloads, stars, or adoption signal to watch)

## Output

Stage 1 output is only the scope-review alignment page at `alignment/ord-align-<slug>.html` and a concise request for final compiled YAML approving validation scope.

Stage 2 output is the updated artifact-review alignment page. It contains the namespace checks, existing-solution comparison, feasibility matrix, effort estimate, evidence notes, assumptions/confidence, verdict rationale, proposed final artifact path, and approval gates.

Stage 3 output for approved GO outcomes is the confirmed HTML page plus the approved markdown alignment doc at `alignment/ord-<slug>.md`. End the markdown doc with:

```md
**Verdict:** GO
**Next work:** build the package
**Recommended next command:** /ord-ship
```

Stage 3 output for approved NO-GO outcomes is only the confirmed HTML page. End the handoff with:

```md
**Verdict:** NO-GO
**Next work:** scan for another candidate
**Recommended next command:** /ord-scan
```

## Constraints

- Do not begin implementation or scaffolding.
- Keep the markdown alignment doc to 1 page.
- Keep the validation lightweight. Do not expand into full ord-scan research depth, do not create a working packet unless explicitly needed to preserve user-provided evidence, and do not perform broad market research.
- If the candidate came from ord-scan, reference it; don't re-research the whole opportunity space.
- Run `npm view` to check namespace availability when possible, but only after Stage 1 scope approval.
- Do not write `alignment/ord-<slug>.md`, emit `/ord-ship` routing, or emit `/ord-scan` routing before final artifact approval.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/ord-align-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention.
