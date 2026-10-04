---
name: cross-agent-second-opinion
description: Use when a high-stakes analysis, citation set, or decision should be checked by a second independent AI agent that verifies rather than decides, or when disagreement between agents must be surfaced for the human to adjudicate.
---

# Cross-Agent Second Opinion

## When to use

Use this skill when an output produced by one AI agent — an analysis, a citation set, a release package, a revision trace, or a code block — is high-stakes enough that a second independent agent should review it before the human acts on it. This includes outputs where a single-agent error could change a scientific conclusion, cause a citation to be published incorrectly, or introduce a defect into a release package. It also applies when two agents have already produced conflicting outputs and the disagreement needs to be surfaced clearly for the human to adjudicate rather than resolved automatically. It is not for using the second agent as a final decision-maker, and it is not for treating agreement between two agents as proof of correctness — two models can agree on an error. After the second-opinion cycle closes, hand citation discrepancies to apa-doi-verifier, statistical concerns to statistical-consultation-protocol, tool-level misbehavior to agentic-session-debugger, and cross-tool capability questions to agent-portability-matrix.

## Inputs

- The first agent's output: the artifact to be reviewed.
- The files or data the second agent will need to perform its review — scoped to the minimum necessary.
- The review criteria: what the second agent should check for, stated before it sees the output.
- The target second agent or environment.
- Sensitive-data boundaries that constrain what the second agent may see.
- The human decision criteria: what kinds of disagreement require human adjudication rather than automatic resolution.

## Workflow

1. Define clearly what is being reviewed and what the second agent is asked to check — not to improve, not to decide, but to surface risk, inconsistency, and missing evidence.
2. Scope the file set sent to the second agent: include only what is necessary for the review and verify that nothing sensitive crosses the boundary.
3. Instruct the second agent to produce a disagreement report, not a revised version — its role is verification, not authorship.
4. Classify every disagreement the second agent surfaces: human decision required, source verification required (route to apa-doi-verifier), code execution required, or data-boundary question.
5. Break any corrections that both agents agree on into small, traceable diffs before applying them.
6. Present disagreements to the human researcher with enough context to adjudicate without re-reading both full outputs.
7. Record the human's decision in a decision log, noting which disagreements were resolved and how.

## Output

Return:

- A second-opinion report listing every point where the second agent's assessment differs from the first agent's output.
- A classified disagreement list: human decision, source verification, code execution, or data boundary, for each item.
- A list of high-risk recommendations from the first agent that the second agent flagged.
- Items that require human adjudication, presented in priority order.
- Applicable corrections as small diffs, held pending human approval.
- Recommendations from the second agent that should not be applied automatically, with the reason stated.
- What to record at session end: the output file path, the disagreement items still awaiting human decision, and the handoffs dispatched to apa-doi-verifier or statistical-consultation-protocol.

## Verification

- The second agent received only the files scoped for review — no additional context from the first agent's session was passed implicitly.
- Every disagreement is classified; none are left as unresolved noise.
- No correction was applied without the human researcher's explicit sign-off.
- Disagreements between agents are visible in the output, not suppressed because they were inconvenient.
- Before closing: the decision log records the human's adjudication for every classified disagreement, and any item routed to a downstream skill is named explicitly.

## Safety

The second agent is a verification tool, not a second referee — its role is to surface what the first agent may have missed, not to override it. Agreement between two agents is not evidence of correctness; both can share the same blind spot. Sensitive data, raw interview transcripts, and student-identifying material are not duplicated for a second review without first passing through sensitive-data-anonymization-gate. Disagreements are surfaced to the human, never resolved by a majority-vote heuristic. Keep AI contribution visible at every stage: record the review stage, both model identities, the contribution level of each, and the human review step.

## Example prompt

"Bu çıktıyı ikinci ajan denetimine hazırlamak istiyorum. Hassas veri sınırlarını koruyarak ikinci görüş raporu, uyuşmazlık listesi ve insan kararı gereken noktaları oluştur."

Expected smoke output:

- A second-opinion report classifying each disagreement as human decision, source verification, code execution, or data boundary.
- A list of high-risk first-agent recommendations flagged by the second agent.
- Applicable corrections held as small diffs, each awaiting human approval before any change is made.

## Türkçe kullanım notu

Bu beceri ikinci bir yapay zekâ ajanını bağımsız bir doğrulama aracı olarak devreye sokar — ikinci ajan karar mercii değil, denetim aracıdır. Birinci ajanın ürettiği analiz, atıf kümesi, release paketi ya da revizyon izleri yüksek riskli ise, tek ajan hatası bilimsel sonucu değiştirme ihtimali taşıyorsa ya da iki ajan çelişkili çıktı ürettiyse bu beceri kullanılır. İkinci ajana yalnızca inceleme için gereken dosyalar iletilir, hassas veriler güvenli ön işlemden geçmeden ikinci araca taşınmaz. İki ajanın aynı fikirde olması doğruluğun kanıtı değildir — ortak körlük riski her zaman vardır. Uyuşmazlıklar görünür kılınır, çoğunluk oyu mantığıyla gizlenmez — her uyuşmazlık noktasında verilen karar insan araştırmacı tarafından karar günlüğüne işlenir. Atıf anlaşmazlıkları apa-doi-verifier'a, istatistiksel sorular statistical-consultation-protocol'e, araç düzeyindeki sorunlar agentic-session-debugger'a devredilir.
