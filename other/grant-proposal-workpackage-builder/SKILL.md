---
name: grant-proposal-workpackage-builder
description: Use when a research proposal needs work packages, milestones, deliverables, a timeline, a risk register, and budget-justification scaffolding, while keeping scientific claims and feasibility honest and human-owned.
---

# Grant Proposal Work Package Builder

## When to use

Use this skill when a research idea must be shaped into a fundable proposal: structuring work packages with clear dependencies, assigning responsibilities, building a milestone timeline, registering risks, writing an impact statement that does not overstate, and justifying each budget line against a specific activity. It applies across funding types — national, European, institutional, or foundation — and at any proposal stage from first draft to revision after panel feedback. It is not for polishing prose that is disconnected from a real research plan, and it is not a substitute for ethics board submission, which belongs to ethics-irb-ai-protocol, or for preregistration, which belongs to preregistration-analysis-plan-ledger.

## Inputs

- The research idea, framed at minimum as a problem and a proposed approach.
- The funding call text, including priorities, eligibility criteria, and required sections.
- The project duration and start date.
- The team composition and roles, even provisionally.
- The budget ceiling and any funder-mandated cost categories.
- The target beneficiary group or end user.
- Data management and ethics requirements specified by the call or institution.

## Workflow

1. Decompose the research idea into four layers: the problem the proposal addresses, the overall aim, the specific and measurable objectives, and the outputs the funder can point to.
2. Map each objective against the call's stated priorities and record where the alignment is direct and where it is argued.
3. Build the work package table with packages arranged in dependency order, each carrying a lead, a duration, a list of tasks, and at least one quality indicator.
4. Assign deliverables to work packages and place them on the timeline, distinguishing internal milestones from funder-facing deliverables.
5. Classify risks at five levels — technical, ethical, time, budget, and team — and pair each risk with a mitigation measure.
6. Write the impact statement from the evidence base, not from aspiration: name the pathway from output to outcome, state who benefits and how this will be measured, and avoid claims that the project cannot support.
7. Justify every budget line by linking it to a specific work package activity; flag any line that cannot be so linked for the researcher to resolve.
8. Draft the data management and ethics section at the same time as the main proposal body, not afterward. Hand off to research-lifecycle-pipeline when the funded project moves into execution, to ethics-irb-ai-protocol for board submission, to preregistration-analysis-plan-ledger when the analysis plan must be registered, and to open-science-release-packager when outputs require a release plan.

## Output

Return:

- An aim-and-objectives breakdown separating the overall aim from specific, measurable objectives.
- A work package table with leads, durations, tasks, and quality indicators.
- A milestone and deliverables timeline distinguishing internal from funder-facing items.
- A risk register covering the five risk levels, each with a mitigation measure.
- An impact statement grounded in the evidence base and linked to measurable outcomes.
- A budget justification table linking each line to a work package activity, with unlinked lines flagged.
- A data management and ethics section skeleton.
- What to record at session end: the proposal file path, budget lines still awaiting researcher confirmation, the ethics submission route, and the handoff conditions for ethics-irb-ai-protocol and preregistration-analysis-plan-ledger.

## Verification

- Every work package has a named lead, a stated duration, and at least one quality indicator.
- Every deliverable is assigned to a work package and appears on the timeline.
- Every budget line is linked to at least one work package activity; unlinked lines are flagged, not silently resolved.
- The impact statement contains no claim that outpaces what the project's design can support.
- The risk register covers all five risk levels.
- Before closing: the researcher has reviewed the impact claims for honesty, the budget for completeness, and the ethics pathway for feasibility within the proposal timeline.

## Safety

A funded proposal is a public commitment, so a gap in it carries consequences beyond style. An impact claim the design cannot support, a budget line with no traceable rationale, or a work package with no assigned owner can lead to a rejected proposal, an audit finding, or a project that cannot be delivered as promised. This skill therefore flags rather than resolves any gap between what the proposal claims and what the plan can deliver. AI may draft and structure, but the researcher owns every scientific claim, every budget decision, and the feasibility assessment. If the project involves human participants, ethics review must be planned into the timeline from the outset, not treated as a later administrative step.

## Example prompt

"Bu araştırma fikrini fon başvurusu mantığına dönüştür. Problem, amaç, hedef, iş paketleri, teslim edilebilir çıktılar, risk planı, etki beyanı ve bütçe gerekçesini hazırla; iş paketlerini bağımlılık sırasıyla kur ve bütçe satırlarını faaliyetlere bağla."

Expected smoke output:

- An aim-and-objectives breakdown with the overall aim and at least three specific objectives.
- A work package table with leads, durations, and quality indicators, arranged in dependency order.
- A risk register covering technical, ethical, time, budget, and team risks with mitigations.
- A budget justification table linking each line to a work package, with any unlinked lines flagged for the researcher.

## Türkçe kullanım notu

Bu beceri, araştırma fikrini denetlenebilir bir proje başvurusuna dönüştürür: problem ve amaç ayrımı, bağımlılık sırasıyla kurulmuş iş paketleri, beş düzeyde tutulan risk kaydı, her faaliyete bağlı bütçe gerekçesi ve abartmadan yazılmış etki beyanı. Yapay zekâ taslak kurar ve yapıyı oluşturur, ancak bilimsel iddia, bütçe kararı ve fizibilite değerlendirmesi araştırmacıya aittir. Bütçe ahlaki bir metindir: her satırın hangi faaliyete dayandığı açık olmalıdır, bağlanamayan satır araştırmacıya işaretlenerek iletilir. Etki beyanı projenin tasarımının destekleyebileceğinden ileri giderse bu açıkça belirtilir. İnsan katılımcı içeren çalışmalarda etik kurul süreci başvuru takviminin başında planlanır, sonradan eklenmez. Proje onaylandığında research-lifecycle-pipeline yürütme aşamasına, ethics-irb-ai-protocol kurul başvurusuna, preregistration-analysis-plan-ledger analiz planı tesciline ve open-science-release-packager açık bilim yayın planına devir için hazırdır.
