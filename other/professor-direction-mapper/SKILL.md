---
name: professor-direction-mapper
description: Map a professor or lab's current research mainline, branches, recent pivots, historical lines, highlighted papers, topic counts, delegated student-led publication spine, and reading route from public evidence. Use when Codex needs to decide what a professor currently works on, avoid mistaking past mainlines for current core directions, distinguish current core directions from side or historical lines, prepare HKUST(GZ) RA/advisor scouting, choose papers or surveys to read, or convert a candidate professor page plus publication sources into a direction map before reproduction or outreach. When student-led spine evidence is needed, this skill should delegate that bounded subtask to `student-lead-spine-finder` in a subagent and integrate its returned candidate names/directions rather than doing that large side task inline.
---

# Professor Direction Mapper

Map a professor's public research identity into a decision-useful direction map. The skill is for the step before deep paper reproduction: decide what the professor's mainline is, what is a branch, what is stale or historical, and which papers/surveys should be read next.

The core failure mode this skill must avoid is time-blind ranking: treating a past high-volume or high-citation line as the current mainline when the group has moved on.

## Source Priority

Prefer evidence in this order:

1. Personal homepage, lab homepage, research statement, recruiting statement, project pages.
2. Recent 3-4 year publications from official publication lists, DBLP, OpenAlex, Semantic Scholar, Google Scholar profile exports, ORCID, or field databases.
3. Delegated student-led publication spine from `student-lead-spine-finder`: candidate names, evidence papers, externally checked directions, confidence, and caveats.
4. Highlighted, selected, or featured publications/projects on the professor or lab site.
5. Recent news, talks, grants, code, datasets, benchmarks, and project pages.
6. Bibliometric/topic-modeling outputs as supporting evidence, not as the sole basis.

If sources disagree, treat the professor's own current homepage as the strongest signal for interest, but use recent publication volume to test whether the stated line is active.

Do not let older highlighted papers outrank current activity by default. A highlighted older paper can define a historical foundation, but it needs recent papers, current project language, recruiting text, or student-led continuation to count as current mainline.

## Workflow

1. Establish scope.
   - Identify the professor/lab, institution, target role, and user's purpose.
   - If no public source is provided, search for the official personal or lab homepage before using aggregator pages.
   - For HKUST(GZ), use `hkust-gz-faculty-intel` first when the user needs candidate collection or official profile URLs.

2. Build a source ledger.
   - Record every source URL, source type, access date, and what it can prove.
   - Separate facts from inferences.
   - Flag name ambiguity, stale homepages, missing publication lists, and inaccessible PDFs.

3. Extract public self-positioning.
   - Capture research interests, slogans, lab mission, recruiting text, project categories, and selected publications.
   - Treat repeated labels on the homepage as candidate directions.
   - Note which papers/projects the professor chooses to advertise.

4. Build a recent publication table.
   - Collect titles, years, venues, coauthors, links, abstracts when available, and source.
   - Default window: latest 3-4 years, plus older highlighted papers only as foundation or transition evidence.
   - If the corpus is large, sample transparently: recent papers, highlighted papers, highly cited papers, and papers around apparent pivots.

5. Delegate the recent student-led spine check.
   - Treat "find the lab's recent main student / senior PhD / recurring first-author lead" as a separate workload, not an inline branch of this skill.
   - If subagent tools are available, spawn a subagent and instruct it to use `student-lead-spine-finder` at `C:\Users\Administrator\.codex\skills\student-lead-spine-finder`.
   - Pass the professor/lab name, institution, source URLs or recent paper table, latest 3-4 year window, and any tentative current-mainline hypothesis.
   - Require the subagent to return candidate names, role confidence, evidence papers, externally checked directions from Google Scholar/OpenAlex/Semantic Scholar/personal pages, and caveats.
   - While the subagent works, continue non-overlapping mainline work: homepage analysis, recent publication clustering, and temporal sanity checks.
   - When the subagent returns, integrate its packet as cross-check evidence. Do not let it decide the final mainline by itself.
   - If subagent tools are unavailable, explicitly report that the delegated student-led lane could not run. Ask whether to run it inline or proceed without that cross-check; do not silently absorb the large side task.

6. Cluster directions.
   - Group papers by problem, task, method family, application domain, dataset/benchmark, and recurring keywords.
   - Use counts by year and recency as evidence, not as mechanical proof.
   - Identify shared methodological spine across several surface topics.

7. Classify each direction.
   - Current mainline: current self-positioning plus repeated recent output, delegated student-led continuation evidence, or fresh project/recruiting evidence.
   - Branch: real but narrower line, often with fewer papers, weaker homepage emphasis, or tied to a collaborator/student.
   - Historical mainline: previously important, highly cited, or strongly highlighted, but with little recent continuation.
   - Emerging pivot: recent but still low-volume signal from new papers, projects, grants, or talks.
   - Promotion rule: a direction can move from branch/emerging to current mainline if it has repeated latest-window papers and delegated student-led momentum even if total lifetime count is smaller.
   - Demotion rule: a direction must be downgraded from current mainline if most evidence is older than the latest window and it lacks current self-positioning or delegated student-led continuation.

8. Run a temporal sanity check before finalizing.
   - Ask: "If I ignored all papers older than 4 years, would this still be the mainline?"
   - Ask: "Which direction has the most recent student-led execution?"
   - Ask: "Which old direction is only surviving because of citations, selected-paper status, or the professor's legacy identity?"
   - If the answer changes, report both the historical mainline and current mainline separately.

9. Produce the reading route.
   - For each mainline, select 1-3 group papers to understand the professor's internal framing.
   - Generate survey search queries for the field/problem.
   - Identify likely node papers only after reading or searching the survey.
   - For branch lines, usually recommend group papers plus one survey, without deep reproduction unless user fit depends on it.

10. Recommend next action.
   - Decide whether to proceed to survey search, paper digestion, minimal reproduction planning, outreach prep, or deprioritization.
   - If evidence is too weak, list the missing source needed instead of overclaiming.

## Output Contract

Use the structure in `references/direction-map-template.md` when producing a durable direction map or updating a planning repository.

At minimum, include:

- Verdict: likely mainline, branches, historical lines, emerging pivots.
- Evidence ledger: source-by-source facts.
- Direction table: label, classification, homepage signal, highlight signal, latest-window count, student-led signal, recency, representative papers, confidence.
- Student-led spine: recurring first authors or student-like non-corresponding authors and their directions.
- Recent movement: what appears to be increasing, stable, or declining.
- Reading route: group papers, survey queries, node-paper search targets, reproduction candidates.
- Caveats: ambiguity, stale pages, data gaps, and assumptions.

## Routing With Other Skills

- Use `anysearch` for live web search, official homepage discovery, survey search, and recent public context.
- Use `professor-fit-analyzer` when the user also wants advisor fit, mentoring, lab risk, outreach, or interview strategy.
- Use `google-scholar-profile-intel` for structured author/publication enrichment from OpenAlex or other public bibliographic sources.
- Use `student-lead-spine-finder` as a delegated subagent task whenever student-led spine evidence is needed. The parent call should pass source URLs or a recent paper table, then integrate returned candidate names and directions.
- Use `paper-pdf-to-structured-html` and `paper-term-glossary-builder` after a paper is selected for reading.
- Use `research-experiment-design-reviewer` or a reproduction-planning skill after a node paper is chosen for minimal reproduction.
- Use `advisor-profile-maintainer` only for private long-lived advisor/person profiles; do not send private notes to external search.

## Guardrails

- Do not equate publication count with intellectual importance.
- Do not equate old citations, old selected papers, or past high volume with current mainline.
- Do not infer a professor's private preference from a single paper.
- Do not infer student status from author order alone when identity is unclear.
- Do not treat Google Scholar scraping as canonical; prefer official pages and open bibliographic APIs.
- Do not hide partial coverage. State how many papers were found, clustered, and read or skimmed.
- Do not call a direction stale merely because it has low volume in a low-output field; calibrate to field norms.
- Do not use first-author logic in fields where authorship is alphabetical, solo-author, or otherwise non-contributory without saying so.
- Do not use private notes, emails, or unpublished user material in web search.
