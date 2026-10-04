---
name: research-lifecycle-pipeline
description: Use when a researcher asks where to start, which project skill fits the current stage of a study, or in what order literature scoping, source access, vault upkeep, drafting, citation verification, disclosure, and review response should run.
---

# Research Lifecycle Pipeline

## When to use

Use this skill when the user needs orientation across the project skills rather than one specific check: a study is starting, a stalled project is resuming, or the user asks which skill applies right now. Once the stage is clear, hand the work to that stage's skill and return here only at the next boundary. It is not for performing any stage's work itself; for scoping reviews that is prisma-scoping-review-pipeline, for pre-analysis registration that is preregistration-analysis-plan-ledger, for release packaging that is open-science-release-packager, and for sensitive data handling that is sensitive-data-anonymization-gate.

## Inputs

- The current stage, or a short project description from which the stage can be inferred.
- Which artifacts already exist: research question, source list, vault, draft, reference list, reviewer letter.
- Language scope, Turkish, English, or both.
- Deadlines or venue constraints that reorder priorities.

## Workflow

1. Place the project on the lifecycle: scoping, sourcing, organizing, drafting, verifying, disclosing, responding, releasing.
2. Match the active stage to its skills and say why:
   - social-science-literature-triage owns scoping.
   - Sourcing runs through regional-access-workflow, and mcp-research-stack-triage joins when tool configuration is the blocker.
   - memory-vault-architect designs the organizing layer, with source-passport-ledger tracking individual sources.
   - Drafting belongs to bilingual-manuscript-scaffold. Analysis sections bring in statistical-consultation-protocol or qualitative-coding-discipline.
   - apa-doi-verifier carries the verifying stage alone.
   - Disclosure work pairs ai-disclosure-auditor with ethics-irb-ai-protocol when a board application is involved.
   - For responding, rebuttal-traceability-matrix structures the answers and anti-ai-trace-revision repairs the prose.
   - Releasing closes with repo-release-integrity-check, joined by bilingual-booklet-pairing for paired-document parity, journal-fit-screening for venue choice, and conference-materials-bilingual for presentation work.
   - agentic-session-debugger applies at any stage when the tooling itself misbehaves.
3. State the ordering rule that matters at the current boundary: verification before disclosure, disclosure before submission, traceability before resubmission.
4. Stop at the boundary, present the recommendation with its reason, and wait for the user's decision before going further.
5. When a stage needs an ethics board, a statistician, or legal advice, say so plainly instead of routing to a skill.

## Output

Return:

- The diagnosed stage and the evidence for the diagnosis.
- The skill or skills to invoke now, each with its reason.
- The next boundary and the condition that must hold to cross it.
- Items that need a human professional rather than a skill.
- What to record at session end: the diagnosed stage, the skills recommended and why, the boundary condition stated, and any open human-decision points.

## Verification

- Every recommended skill exists in the installed set and is named exactly.
- No stage is skipped silently, and any skipped stage is listed with the user's consent.
- The verification-before-disclosure ordering is never reversed.
- Each boundary crossing was confirmed by the user, in the conversation.
- Before closing: the stage record is written where the next session can find it, and any skill handoff is named with the reason it was triggered.

## Safety

This skill routes work, it does not perform it. A routing recommendation never substitutes for ethics review, statistical consultation, or legal advice. Do not chain stages automatically, and do not start another skill's workflow without the user's confirmation at the boundary.

## Example prompt

"Tezin tartışma bölümünü yazıyorum ama kaynak listem dağınık, hangi adımdayım ve nereden devam etmeliyim?"

Expected smoke output:

- Stage diagnosis at the organizing and verifying boundary, with the evidence.
- A recommendation to run source-passport-ledger and then apa-doi-verifier before drafting continues.
- The condition for moving on to disclosure work.

## Türkçe kullanım notu

Bu beceri tek bir işi yapmaz, sıradaki doğru beceriyi gösterir. Araştırmanızın neresinde olduğunuzu anlatın, aşama teşhis edilir, o aşamanın becerisi gerekçesiyle önerilir ve bir sonraki sınırın koşulu söylenir. Aşama geçişleri sizin onayınızla olur, doğrulama tamamlanmadan beyana geçilmez, beyan tamamlanmadan sunum yapılmaz. Etik kurul, istatistikçi ya da hukukçu gereken yerde beceri önermek yerine bunu açıkça belirtir — bu kararlar becerinin değil, ilgili uzmanın yetkisindedir.
