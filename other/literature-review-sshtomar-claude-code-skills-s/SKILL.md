---
name: lit-review
description: "Systematic literature review methodology for social science research. Use when conducting systematic reviews, research synthesis, meta-analyses, scoping reviews, or comprehensive literature searches across economics, political science, sociology, education, public health, and development. Produces structured notebook cells with search strategy, evidence table, thematic synthesis, and gap analysis."
argument-hint: "[topic]"
---

<skill_content>

<overview>
A systematic literature review follows a structured, reproducible protocol to identify, evaluate, and synthesize existing research on a topic. This skill enforces methodological rigor by requiring explicit search strategies, transparent inclusion criteria, quality assessment, and structured evidence tables -- all implemented as notebook cells for full reproducibility.

Literature reviews in social science differ from biomedical reviews: gray literature (working papers, policy reports) carries significant weight, quasi-experimental designs are common, and the boundary between "published" and "working" research is fluid. This skill accounts for these disciplinary norms.
</overview>

<mandatory_requirements>

<requirement priority="critical">
  <name>Explicit Search Strategy</name>
  <description>MUST document search terms, databases, date ranges, and inclusion/exclusion criteria BEFORE presenting any findings</description>
  <rationale>Petticrew & Roberts (2006) emphasize that undocumented search strategies make reviews unreproducible and prone to selection bias. In social science, where researcher priors are strong, this discipline is essential</rationale>
  <consequence>Cherry-picked citations that confirm priors rather than representing the field</consequence>
</requirement>

<requirement priority="critical">
  <name>Structured Evidence Table</name>
  <description>ALL sources MUST be recorded in a structured DataFrame with: authors, year, title, journal/source, methodology, sample_size, geographic_scope, key_finding, effect_size, quality_rating, and relevance</description>
  <rationale>Systematic organization prevents narrative bias and makes gaps in the evidence visible (Tranfield et al., 2003). The structured format enables programmatic analysis of the evidence base</rationale>
  <consequence>Narrative reviews without structure tend to over-weight memorable or recent studies</consequence>
</requirement>

<requirement priority="critical">
  <name>Source Evaluation</name>
  <description>Each source MUST be assessed for methodological quality: identification strategy, internal validity, external validity, sample size adequacy, and potential threats. Rate as high/medium/low</description>
  <rationale>Not all evidence is equal. Meta-analyses show that effect sizes vary systematically with study quality (Stanley & Doucouliagos, 2012). In social science, identification strategy is the primary quality marker</rationale>
  <consequence>Treating all studies as equally valid produces misleading syntheses</consequence>
</requirement>

<requirement priority="critical">
  <name>Gap Identification</name>
  <description>The synthesis MUST explicitly identify gaps, contradictions, and unresolved questions in the literature</description>
  <rationale>The primary value of a literature review is mapping what is NOT known, not just summarizing what is. Gap identification motivates new research</rationale>
  <consequence>Review becomes a summary rather than a foundation for new research</consequence>
</requirement>

<requirement priority="high">
  <name>Gray Literature Inclusion</name>
  <description>MUST search working paper repositories (NBER, SSRN, IZA, CEPR, J-PAL, 3ie) alongside peer-reviewed journals</description>
  <rationale>In economics and policy research, the most current and influential work often circulates as working papers for years before publication. Publication bias means published studies systematically overstate effect sizes (Andrews & Kasy, 2019). Excluding gray literature biases reviews toward significant findings</rationale>
  <consequence>Missing the most current research and introducing publication bias into the review</consequence>
</requirement>

<requirement priority="high">
  <name>Thematic Synthesis</name>
  <description>Results MUST be organized thematically, NOT as study-by-study summaries. Synthesize across studies within each theme</description>
  <rationale>Study-by-study presentation fails to identify patterns, contradictions, and the weight of evidence. Thematic synthesis is the distinguishing feature of a good review (Braun & Clarke, 2006)</rationale>
  <consequence>Review reads as an annotated bibliography rather than a synthesis</consequence>
</requirement>

</mandatory_requirements>

<research_question_framework>

For social science reviews, use the SPIDER framework (more flexible than PICO for non-clinical research):

- S (Sample): What population, group, or context?
- PI (Phenomenon of Interest): What intervention, policy, program, or phenomenon?
- D (Design): What study designs to include? (RCT, DID, IV, RDD, qualitative, mixed)
- E (Evaluation): What outcomes or impacts to evaluate?
- R (Research type): Quantitative, qualitative, or mixed methods?

Example: "What is the effect (E: learning outcomes, enrollment) of conditional cash transfer programs (PI) on educational attainment in low- and middle-income countries (S), as measured by experimental and quasi-experimental studies (D, R)?"

For policy evaluation reviews, also consider:
- Implementation context (what makes programs work or fail?)
- Heterogeneity (for whom, where, under what conditions?)
- Cost-effectiveness (what is the cost per unit of impact?)
- Scalability (do effects hold when programs scale?)
</research_question_framework>

<database_guide>

Select at minimum 3 complementary databases appropriate for the domain:

Core Social Science Databases:
- Google Scholar: Comprehensive cross-disciplinary coverage, citation tracking
- SSRN: Working papers in economics, finance, law, political science
- NBER Working Papers: Leading economics research (often years before publication)
- JSTOR: Historical and current peer-reviewed articles across social sciences
- Web of Science / Scopus: Citation-indexed peer-reviewed literature
- EconLit: Economics-specific (AEA journals, books, working papers)

Policy and Development:
- J-PAL Evidence: RCTs in development economics
- 3ie Development Evidence Portal: Impact evaluations in international development
- World Bank Open Knowledge Repository: Policy research and working papers
- IMF Working Papers: Macroeconomics and public finance
- OECD iLibrary: Cross-country policy analysis

Specialized by Discipline:
- ERIC: Education research
- PubMed/PMC: Public health, health economics, epidemiology
- PolicyFile: US public policy research
- Campbell Collaboration: Systematic reviews in social sciences
- Cochrane Library: Health intervention reviews (when relevant)
- IZA Discussion Papers: Labor economics
- CEPR Discussion Papers: European economics research
- arXiv (econ, q-fin, stat): Quantitative methods, econometrics

Preprint and Open Access:
- RePEc/IDEAS: Economics working papers and articles
- OSF Preprints: Open science preprints across social sciences
- EdWorkingPapers (Annenberg): Education policy research

Database Selection Strategy:
1. Primary database for breadth: Google Scholar or Web of Science
2. Working paper repository: NBER, SSRN, or IZA (field-dependent)
3. Specialized database: EconLit, ERIC, J-PAL, etc. (topic-dependent)
4. Gray literature: World Bank, OECD, or government reports
5. Citation chaining: Forward and backward from key papers
</database_guide>

<quality_assessment>

Assess each study's methodological quality based on identification strategy and validity:

Study Design Hierarchy (for causal questions):
1. RCTs (randomized controlled trials / field experiments)
2. Regression discontinuity designs (RDD)
3. Instrumental variables (IV)
4. Difference-in-differences (DID) with pre-trends evidence
5. Propensity score matching / synthetic control
6. Observational with controls (OLS with covariates)
7. Descriptive / correlational studies
8. Qualitative / case studies

Quality Dimensions to Assess:
- Internal validity: How credible is the causal identification?
- Statistical power: Is the sample large enough to detect meaningful effects?
- External validity: How generalizable are the findings?
- Measurement quality: Are key variables well-measured?
- Pre-registration: Was the analysis pre-specified? (reduces p-hacking risk)
- Transparency: Are data and code available for replication?
- Robustness: Do results hold across specifications?

Quality Rating Scale:
- High: Strong identification strategy, adequate power, transparent methods, robust results
- Medium: Reasonable identification with some threats, adequate sample, partial robustness
- Low: Weak identification, small sample, or results sensitive to specification

Red Flags:
- P-values clustered just below 0.05 (possible p-hacking)
- No robustness checks or only one specification reported
- Effect sizes that are implausibly large
- Endogeneity concerns not addressed
- Missing data handled without sensitivity analysis
- Post-hoc subgroup analysis presented as primary finding
</quality_assessment>

<prioritizing_papers>

Prioritize papers based on methodological rigor, venue quality, and influence:

Citation Count Thresholds (social science norms):
| Paper Age | Citations | Classification |
|-----------|-----------|----------------|
| 0-3 years | 10+ | Noteworthy |
| 0-3 years | 50+ | Highly Influential |
| 3-7 years | 50+ | Significant |
| 3-7 years | 200+ | Landmark Paper |
| 7+ years | 200+ | Seminal Work |
| 7+ years | 500+ | Foundational |

Note: Citation norms vary by subfield. Labor economics papers accumulate citations faster than political theory. Use these as rough guides.

Journal Tiers (Economics):
- Tier 1: American Economic Review, Quarterly Journal of Economics, Econometrica, Journal of Political Economy, Review of Economic Studies
- Tier 2: Review of Economics and Statistics, Journal of the European Economic Association, American Economic Journal (all), Journal of Finance, Journal of Labor Economics, Journal of Public Economics, Journal of Development Economics, Economic Journal
- Tier 3: Respected field journals (Journal of Human Resources, Journal of Health Economics, Journal of Urban Economics, etc.)

Journal Tiers (Political Science):
- Tier 1: American Political Science Review, American Journal of Political Science, Journal of Politics
- Tier 2: Comparative Political Studies, World Politics, International Organization, British Journal of Political Science
- Tier 3: Field journals (Political Analysis, Political Behavior, etc.)

Journal Tiers (Sociology):
- Tier 1: American Sociological Review, American Journal of Sociology
- Tier 2: Social Forces, Demography, Sociology of Education
- Tier 3: Field journals

Working Papers:
- NBER Working Papers carry significant weight (peer network vetting)
- SSRN/IZA papers should be assessed on methodology, not venue
- Check if working papers have been subsequently published

Identifying Seminal Papers:
1. Cited by many of the other papers you find (appears across reference lists)
2. Introduced a methodology now widely used (e.g., Angrist & Krueger 1991 for IV)
3. Published in Tier-1 venue with high citation count
4. Referenced in textbooks and survey articles
5. Written by researchers recognized as field leaders
</prioritizing_papers>

<search_techniques>

Boolean Search Construction:
- AND: narrows (both terms required)
- OR: broadens (either term)
- Quotes: exact phrase ("conditional cash transfer")
- Wildcards: education* matches educational, education, educating

Example for a CCT review:
("conditional cash transfer" OR "CCT" OR "cash transfer program")
AND ("education" OR "school enrollment" OR "attendance" OR "learning outcomes")
AND ("developing countries" OR "low-income" OR "Global South")

Citation Chaining:
1. Forward citation search: Find papers citing a key paper (Google Scholar "Cited by")
2. Backward citation search: Review references of key papers
3. Snowball sampling: Start with 3-5 seminal papers, follow citation networks
4. Prioritize papers appearing in multiple reference lists (likely foundational)

Search Refinement:
1. Pilot search: Run broad terms, review first 50 results
2. Note recurring keywords, author names, and journal names
3. Refine search terms based on pilot results
4. Run refined search across all selected databases
5. Document each iteration for reproducibility

Gray Literature Search:
- NBER: Browse by program (Labor Studies, Public Economics, etc.)
- SSRN: Search by keyword and sort by downloads or citations
- Government reports: Search agency websites directly
- Conference proceedings: ASSA/AEA meetings, APPAM, BREAD
- Dissertations: ProQuest Dissertations for emerging research
</search_techniques>

<workflow>

Phase 1: Planning and Scoping (Cell 1)
- Define research question using SPIDER framework
- Develop search terms with synonyms and Boolean operators
- Select minimum 3 complementary databases
- Set date range, language, and geographic constraints
- Define inclusion/exclusion criteria (study design, population, outcomes)
- Specify review type: systematic, scoping, narrative, or meta-analysis

Phase 2: Systematic Search and Source Collection (Cell 2)
- Execute search across all selected databases
- Document search strings, dates, and result counts for each database
- Aggregate results and remove duplicates
- Build structured DataFrame of all identified sources
- Record how each source was found (which search, which database)
- Conduct citation chaining from key papers

Phase 3: Screening and Quality Assessment (Cell 3)
- Apply inclusion/exclusion criteria systematically
- Document exclusion reasons with counts
- Assess methodological quality of each included study
- Assign quality rating (high/medium/low)
- Create screening flow diagram (records found -> deduplicated -> screened -> included)

Phase 4: Thematic Synthesis and Gap Analysis (Cell 4)
- Identify 3-6 major themes across included studies
- Synthesize findings within each theme (NOT study-by-study)
- Compare effect sizes and directions across studies
- Weight synthesis by study quality
- Identify consensus findings, contested claims, and gaps
- Note methodological patterns and limitations across studies

Phase 5: Summary, Implications, and References (Cell 5)
- Synthesize key takeaways (what does the weight of evidence suggest?)
- Discuss implications for policy, practice, or future research
- List specific gaps that future research should address
- Acknowledge limitations of the review itself
- Provide properly formatted reference list
</workflow>

<output_format>

Each phase becomes a separate notebook cell. Pure Python code, no decorators or wrappers.

Cell 1 -- Search Strategy:
```python
import pandas as pd
from datetime import date

# LITERATURE REVIEW: [Topic]
# ============================================================

search_strategy = {
    "research_question": "What is the effect of [intervention] on [outcome] in [population/context]?",
    "framework": "SPIDER",
    "sample": "[population or context]",
    "phenomenon": "[intervention, policy, or phenomenon]",
    "design": "[RCT, DID, IV, RDD, mixed methods, etc.]",
    "evaluation": "[outcomes to measure]",
    "research_type": "[quantitative, qualitative, mixed]",
    "search_terms": [
        '("term1" OR "synonym1") AND ("term2" OR "synonym2")',
        '"exact phrase" AND (outcome1 OR outcome2)',
    ],
    "databases": [
        "Google Scholar",
        "NBER Working Papers",
        "SSRN",
        # Add domain-specific: EconLit, ERIC, J-PAL, 3ie, etc.
    ],
    "date_range": "2010-2025",
    "language": "English",
    "inclusion_criteria": [
        "Peer-reviewed articles or working papers from recognized institutions",
        "Empirical studies with quantitative outcome measures",
        "Study designs: RCT, DID, IV, RDD, or high-quality observational",
        "Population: [specify]",
    ],
    "exclusion_criteria": [
        "Purely theoretical or opinion pieces without empirical evidence",
        "Studies with sample size < [threshold]",
        "Non-peer-reviewed sources without institutional affiliation",
        "Studies outside geographic/temporal scope",
    ],
    "review_type": "systematic",  # systematic, scoping, narrative, meta-analysis
    "date_executed": str(date.today()),
}

# Display search protocol
print("=" * 60)
print("SEARCH PROTOCOL")
print("=" * 60)
for key, value in search_strategy.items():
    if isinstance(value, list):
        print(f"\n{key}:")
        for _item in value:
            print(f"  - {_item}")
    else:
        print(f"\n{key}: {value}")
```

Cell 2 -- Source Collection:
```python
import pandas as pd

# Search Results by Database
# ============================================================
# Document search execution for reproducibility

search_log = [
    {"database": "Google Scholar", "date_searched": "2025-01-15",
     "search_string": '("conditional cash transfer" OR CCT) AND education',
     "results_found": 1240, "after_screening": 45},
    {"database": "NBER", "date_searched": "2025-01-15",
     "search_string": "conditional cash transfer education",
     "results_found": 28, "after_screening": 12},
    # ... more databases
]

search_df = pd.DataFrame(search_log)
print("SEARCH EXECUTION LOG")
print("=" * 60)
print(search_df.to_string(index=False))
print(f"\nTotal results: {search_df['results_found'].sum()}")
print(f"After screening: {search_df['after_screening'].sum()}")

# Evidence Table
# ============================================================
sources = [
    {
        "authors": "Author et al.",
        "year": 2020,
        "title": "Title of the study",
        "journal": "Journal Name or Working Paper Series",
        "methodology": "RCT",  # RCT/DID/IV/RDD/PSM/observational/qualitative
        "sample_size": "N=5,000",
        "geographic_scope": "Mexico",
        "key_finding": "CCT increased enrollment by 8 percentage points",
        "effect_size": "8pp (95% CI: 5-11pp)",
        "quality": "high",  # high/medium/low
        "relevance": "high",  # high/medium/low
        "source_db": "Google Scholar",
        "doi_or_url": "https://doi.org/...",
    },
    # ... more sources
]

lit_table = pd.DataFrame(sources)
lit_table = lit_table.sort_values(["quality", "relevance", "year"],
                                  ascending=[False, False, False])

# Summary statistics
print(f"\nTotal included studies: {len(lit_table)}")
print(f"\nBy methodology:")
print(lit_table["methodology"].value_counts().to_string())
print(f"\nBy quality rating:")
print(lit_table["quality"].value_counts().to_string())

lit_table
```

Cell 3 -- Screening Flow and Quality Assessment:
```python
# SCREENING FLOW
# ============================================================
print("SCREENING FLOW DIAGRAM")
print("=" * 60)

flow = {
    "Records identified through database searching": 1500,
    "Additional records from citation chaining": 45,
    "Records after deduplication": 1200,
    "Records screened (title/abstract)": 1200,
    "Records excluded at screening": 1050,
    "Full-text articles assessed": 150,
    "Full-text excluded (with reasons)": 108,
    "Studies included in synthesis": 42,
}

for _stage, _count in flow.items():
    print(f"  {_stage}: n = {_count}")

# Exclusion reasons
print("\nExclusion reasons (full-text stage):")
_exclusion_reasons = {
    "Wrong population/context": 35,
    "Wrong outcome measures": 28,
    "Insufficient methodology": 22,
    "Duplicate/superseded version": 15,
    "Not available in English": 8,
}
for _reason, _n in _exclusion_reasons.items():
    print(f"  - {_reason}: n = {_n}")

# QUALITY ASSESSMENT
# ============================================================
print("\n" + "=" * 60)
print("QUALITY ASSESSMENT SUMMARY")
print("=" * 60)

_quality_summary = lit_table.groupby(["methodology", "quality"]).size().unstack(fill_value=0)
print(_quality_summary)

# Flag any quality concerns
_low_quality = lit_table[lit_table["quality"] == "low"]
if len(_low_quality) > 0:
    print(f"\nWARNING: {len(_low_quality)} low-quality studies included.")
    print("These will be noted but down-weighted in synthesis.")
```

Cell 4 -- Thematic Synthesis:
```python
# THEMATIC SYNTHESIS
# ============================================================
print("=" * 60)
print("EVIDENCE SYNTHESIS")
print("=" * 60)

# Theme 1
print("\n--- Theme 1: [Theme Name] ---")
print("Studies: [Author1 (Year), Author2 (Year), ...]")
print("Finding: [Synthesized finding across studies, not study-by-study]")
print("Strength of evidence: [Strong/Moderate/Weak]")
print("Consistency: [Consistent/Mixed/Contradictory]")

# Theme 2
print("\n--- Theme 2: [Theme Name] ---")
# ... same structure

# Consensus vs. contested
print("\n" + "=" * 60)
print("EVIDENCE MAP")
print("=" * 60)

print("\nConsensus findings (supported by multiple high-quality studies):")
print("  1. ...")
print("  2. ...")

print("\nContested or mixed findings:")
print("  1. ... [Author1 finds X, but Author2 finds Y; difference may be due to ...]")

print("\nKnowledge gaps:")
print("  1. ... [No studies examine ...]")
print("  2. ... [Limited evidence on ... subpopulation]")
print("  3. ... [Methodological gap: no RCTs on ...]")

print("\nMethodological patterns:")
print(f"  - Most common design: {lit_table['methodology'].mode().iloc[0]}")
print(f"  - Geographic concentration: {lit_table['geographic_scope'].value_counts().head(3).to_string()}")
print("  - Missing designs: [What study types are absent?]")
```

Cell 5 -- Summary and References:
```python
# SUMMARY AND IMPLICATIONS
# ============================================================
print("=" * 60)
print("SUMMARY")
print("=" * 60)

print("\nKey Takeaways:")
print("  1. [What does the weight of evidence suggest?]")
print("  2. [What is the range of effect sizes?]")
print("  3. [What conditions moderate the effect?]")

print("\nImplications for Policy:")
print("  - ...")

print("\nImplications for Future Research:")
print("  - [Specific gaps to fill]")
print("  - [Methodological improvements needed]")
print("  - [Understudied populations or contexts]")

print("\nLimitations of This Review:")
print("  - [Search limitations: databases not searched, language restriction]")
print("  - [Potential publication bias]")
print("  - [Scope limitations]")

# REFERENCES (APA 7th Edition)
# ============================================================
print("\n" + "=" * 60)
print("REFERENCES")
print("=" * 60)

# Generate formatted references from the evidence table
for _idx, _row in lit_table.sort_values("authors").iterrows():
    _ref = f"{_row['authors']} ({_row['year']}). {_row['title']}. {_row['journal']}."
    if _row.get('doi_or_url'):
        _ref += f" {_row['doi_or_url']}"
    print(f"\n{_ref}")
```

</output_format>

<citation_format>

Default: APA 7th Edition (standard for social sciences)

In-text citations:
- Single author: Smith (2023) or (Smith, 2023)
- Two authors: Smith & Jones (2023) or (Smith & Jones, 2023)
- Three or more: Smith et al. (2023) or (Smith et al., 2023)
- Multiple citations: (Angrist, 2001; Duflo et al., 2011; Heckman, 2010)
- With page: (Smith, 2023, p. 42) or (Smith, 2023, pp. 42-45)

Reference list:
- Alphabetical by first author surname
- Hanging indent format
- Include DOI as URL when available

Journal article:
  Smith, J. D., Johnson, M. L., & Williams, K. R. (2023). Title of article in sentence case. Title of Periodical in Title Case, 22(4), 301-318. https://doi.org/10.xxx/yyy

Working paper:
  Smith, J. D. (2023). Title of paper (NBER Working Paper No. 31234). National Bureau of Economic Research. https://doi.org/10.xxx/yyy

Book:
  Author, A. A. (Year). Title of work: Subtitle. Publisher.

Chapter:
  Author, A. A. (Year). Title of chapter. In E. E. Editor (Ed.), Title of book (pp. xx-xx). Publisher.

Alternative: Chicago Author-Date (common in political science and sociology) follows similar in-text conventions but differs in reference formatting. Use whichever the user's field prefers.

Store all citation data in the DataFrame for programmatic formatting.
</citation_format>

<common_mistakes>

<mistake severity="critical">
  <what>Presenting findings without documenting search strategy</what>
  <consequence>Review is unreproducible and vulnerable to selection bias</consequence>
  <prevention>ALWAYS create the search strategy cell first, before collecting any sources</prevention>
</mistake>

<mistake severity="critical">
  <what>Study-by-study summaries instead of thematic synthesis</what>
  <consequence>Review reads as an annotated bibliography, fails to identify patterns or conflicts</consequence>
  <prevention>Organize by theme, synthesize across studies, compare and contrast within themes</prevention>
</mistake>

<mistake severity="critical">
  <what>Ignoring gray literature (working papers, policy reports)</what>
  <consequence>Publication bias toward significant results. Missing current research that has not yet gone through publication lag</consequence>
  <prevention>Search NBER, SSRN, IZA, J-PAL, and relevant institutional repositories alongside journals</prevention>
</mistake>

<mistake severity="high">
  <what>Only citing sources that support one position</what>
  <consequence>Confirmation bias undermines the review's credibility and usefulness</consequence>
  <prevention>Document ALL relevant sources found, including contradictory evidence. Present competing findings fairly</prevention>
</mistake>

<mistake severity="high">
  <what>Treating all studies as equally rigorous</what>
  <consequence>Misleading synthesis that gives observational correlations the same weight as RCT evidence</consequence>
  <prevention>Rate each source for methodological quality and weight synthesis accordingly. An RCT with N=500 is stronger evidence than an OLS study with N=50,000</prevention>
</mistake>

<mistake severity="high">
  <what>No screening flow documentation</what>
  <consequence>Reader cannot assess how studies were selected, making the review appear arbitrary</consequence>
  <prevention>Document records found, deduplicated, screened, and included with exclusion reasons at each stage</prevention>
</mistake>

<mistake severity="medium">
  <what>Searching only one database</what>
  <consequence>Incomplete coverage. Different databases index different journals and working paper series</consequence>
  <prevention>Search minimum 3 complementary databases: one broad (Google Scholar), one disciplinary (EconLit/ERIC), one gray literature (NBER/SSRN)</prevention>
</mistake>

<mistake severity="medium">
  <what>Not documenting search date</what>
  <consequence>Review cannot be updated or reproduced because the evidence base changes over time</consequence>
  <prevention>Record the exact date of each search execution</prevention>
</mistake>

<mistake severity="medium">
  <what>Conflating statistical significance with importance</what>
  <consequence>Large-sample studies with tiny effects dominate over smaller studies with meaningful effects</consequence>
  <prevention>Report and compare effect sizes, not just p-values. Discuss practical significance alongside statistical significance</prevention>
</mistake>

</common_mistakes>

<interpretation_guide>

<interpreting_results>
- Weight evidence by study quality, not just quantity of studies
- Report effect size ranges across studies, not just average effects
- Note when effects are heterogeneous by context, population, or implementation
- Distinguish between absence of evidence and evidence of absence
- Consider publication bias: significant results are overrepresented in published literature
</interpreting_results>

<red_flags>
- All included studies find effects in the same direction (possible publication bias)
- Effect sizes shrink as study quality increases (common pattern indicating bias)
- Geographic concentration (findings from one country may not generalize)
- Temporal clustering (field may have evolved since most studies were conducted)
- Funnel plot asymmetry when enough studies for meta-analysis
</red_flags>

<next_steps>
- Strong consensus with high-quality evidence -> Report with confidence, note remaining gaps
- Mixed evidence -> Investigate sources of heterogeneity (context, methods, populations)
- Limited evidence -> Characterize what is known, emphasize need for more research
- Contradictory high-quality evidence -> Present both sides, analyze why results diverge
</next_steps>

</interpretation_guide>

<references>
<paper>Petticrew, M. & Roberts, H. (2006). "Systematic Reviews in the Social Sciences: A Practical Guide." Blackwell Publishing.</paper>
<paper>Tranfield, D., Denyer, D. & Smart, P. (2003). "Towards a Methodology for Developing Evidence-Informed Management Knowledge." British Journal of Management.</paper>
<paper>Stanley, T.D. & Doucouliagos, H. (2012). "Meta-Regression Analysis in Economics and Business." Routledge.</paper>
<paper>Andrews, I. & Kasy, M. (2019). "Identification of and Correction for Publication Bias." American Economic Review.</paper>
<paper>Braun, V. & Clarke, V. (2006). "Using Thematic Analysis in Psychology." Qualitative Research in Psychology.</paper>
<paper>Snyder, H. (2019). "Literature Review as a Research Methodology: An Overview and Guidelines." Journal of Business Research.</paper>
<paper>Waddington, H. et al. (2012). "How to Do a Good Systematic Review of Effects in International Development." Journal of Development Effectiveness.</paper>
</references>

</skill_content>
