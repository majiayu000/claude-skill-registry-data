---
name: tool-experimenter
description: Systematically experiment with and improve Bible study tools. Use this skill when the user requests to "experiment|refine|improve {tool-name}".  Don't use it if they are just wanting to run the tool.
---

# Tool Experimenter

## Overview

This skill enables systematic experimentation and improvement of Bible study tools through extensive iterative testing. The process runs **~50+ experiments** across multiple rounds before a tool is deemed production-ready, progressing from broad strategic experiments through deep refinement to final optimization. The skill orchestrates the bible-researcher agent to run experiments, evaluates outcomes, and iteratively refines approaches until diminishing returns are reached.

## When to Use This Skill

Use this skill when:
- User says "experiment with {tool-name}" or "run experiments on {tool-name}" or "improve {tool-name}"
- A Bible study tool needs empirical validation and improvement
- Different approaches to a research task need to be compared
- A tool's effectiveness needs to be tested across diverse verse types

## Experimentation Scale

**Expected Experiment Count:** ~51 runs minimum before production deployment

**Breakdown:**
- Round 1 (Initial Broad Experiments): 3 approaches × 3 verses = **9 runs**
- Rounds 2-5 (Per-Experiment Refinement): 3 approaches × 4-6 verses × 3-4 revisions = **36-54 runs**
- Rounds 6-8 (Winner Deep Refinement): 5-10 additional verses × 2-3 revisions = **10-30 runs**
- Round 9 (Optimization): Remove elements while maintaining quality = **5-10 runs**
- **Total: 60-103 runs** before declaring tool production-ready

## Key Files

Filenames are relative to project root

 - **@bible-study-tools/TEMPLATE.md** - The template and instructions for a tool's README.md file
 - **@STANDARDIZATION.md** - Naming conventions for bible books, versions, citations, languages, etc.
 - **@REVIEW-GUIDELINES.md** - Detailed instructions on how to review a biblical YAML file for accuracy

## Core Workflow

### Phase 1: Initialization and Planning

1. **Load Tool Context**
   - Create and switch to a git branch following git-flow naming conventions
     - Example: feat/tool-sermon-illustrations
   - Read `./bible-study-tools/{tool-name}/README.md` (if exists) to understand:
     - The tool's purpose and research methodology
     - The current schema and data structure
     - Expected outputs and quality criteria
   - Read `./bible-study-tools/{tool-name}/LEARNINGS.md` (if exists) to understand:
     - Past experiment results
     - Known challenges and solutions
     - Techniques that worked well or poorly

  **If the tool does not exist yet:**

  If the tool does not exist, make sure you know what they are trying to achieve and create a new tool for it following the template in `./bible-study-tools/TEMPLATE.md`

2. **Create Experiment Infrastructure**
   - Create directory: `./bible-study-tools/{tool-name}/experiments/` (if not exists)
   - Create subdirectory: `./bible-study-tools/{tool-name}/experiments/output/` for all YAML outputs
   - This will contain all experimental outputs and variations

3. **Design Initial Experiments**
   - Generate **3 fundamentally diverse experimental approaches** that test different strategic directions
   - Use deep thinking to identify truly different approaches, not just variations

   **Example:** If the tool is about Greek words:
   - Experiment A: Focus exclusively on Strong's concordance data
   - Experiment B: Focus on morphological analysis (word forms, tenses, cases)
   - Experiment C: Focus on semantic domains and conceptual relationships

   **Example:** If the tool is asking for sermon illustrations:
   - Experiment A: Find and extract from actual YouTube sermon transcripts for this verse
   - Experiment B: Research cultural touchstones (movies, books, art, history) that illustrate the theme
   - Experiment C: Search sermon illustration databases and compile existing pastor-tested content

   **Critical Guidelines:**
   - Each experiment should pursue a different philosophical approach
   - Experiments should test different hypotheses about what makes the tool valuable
   - Think broadly: different data sources, different organizational structures, different levels of detail
   - Document each experiment's thesis/hypothesis clearly

### Phase 2: Round 1 - Initial Broad Experiments

**Goal:** Establish 3 baseline approaches with initial data
**Target Runs:** 9 (3 experiments × 3 verses)

For each of the 3 initial experiments:

1. **Create Experiment Schema**
   - Copy the base README.md schema as a starting point
   - Modify it according to the experiment's thesis
   - **Target:** Maximum 150 lines (focus on what's unique to this experiment)
   - Save as: `./bible-study-tools/{tool-name}/experiments/{experiment-name}/README-rev1.md`

2. **Test on Representative Verses**
   - Select 3 diverse test verses:
     - **Verse 1:** Well-known, rich context (e.g., John 3:16, John 1:1)
     - **Verse 2:** Moderate complexity (e.g., Matthew 5:3, Colossians 3:1)
     - **Verse 3:** Obscure or challenging (e.g., Habakkuk 3:9, Job 38:36)

3. **Generate Data with bible-researcher Agent**
   - Invoke the bible-researcher agent in parallel for all 9 combinations (3 experiments × 3 verses) with:
     - The experiment's modified README.md
     - The verse reference
   - Save outputs as: `./bible-study-tools/{tool-name}/experiments/output/{BOOK}-{CH:03d}-{VS:03d}-{experiment-name}-rev1.yaml`

4. **Initial Assessment**
   - Review all 9 generated YAML files
   - Review agent feedback (Top 3 Insights, Challenges, Quality Metrics)
   - Identify major blockers or fundamental issues for each experiment
   - Create initial comparison: which experiments show promise, which have critical blockers?

   **Source/Method Optimization Analysis (Critical for Early Phases):**
   - For each experiment, identify the primary data access method:
     - **Web Tools (WebFetch):** Does the source have predictable URL schemas or params?
       - ✅ GOOD: `https://example.com/verse/{book}/{chapter}/{verse}` (can be templated)
       - ✅ GOOD: `https://example.com/search?ref={book}+{chapter}:{verse}` (clear params)
       - ❌ POOR: Requires complex navigation or search-then-click workflows
       - ❌ POOR: Inconsistent URL structures that can't be predicted
     - **WebSearch:** Document which search query patterns work best
     - **MCP/Skills/Scripts:** Evaluate if custom tooling would be more efficient
   - **Decision Criteria:** Prioritize experiments that use predictable, scalable access methods
   - **Documentation:** In LEARNINGS-round1.md, create table:
     | Experiment | Access Method | URL Pattern | Predictability | Scalability |
     |------------|---------------|-------------|----------------|-------------|
     | Exp A | WebFetch | example.com/verse/{ref} | High | Excellent |
     | Exp B | WebSearch | Various queries | Medium | Good |
     | Exp C | Manual navigation | N/A | Low | Poor |

   - Document in: `./bible-study-tools/{tool-name}/experiments/LEARNINGS-round1.md`
   - Commit with: `chore: round 1 initial experiments`

**Parallelization Strategy:**
- Run all 9 agents concurrently (3 experiments × 3 verses)
- This significantly reduces total execution time

**Completion Criteria:** All 3 experiments have been tested on all 3 verses (9 runs complete)

### Phase 3: Rounds 2-5 - Per-Experiment Iterative Refinement

**Goal:** Refine each experiment until confident it represents its approach well
**Target Runs:** 36-54 additional runs (12-18 runs per experiment)

For each of the 3 experiments independently, iterate until the approach is solid:

1. **Analyze Agent Feedback**
   - Read agent reports thoroughly: what worked, what struggled, quality scores
   - Identify patterns across the test verses
   - Prioritize fixes: blockers first, then quality improvements
   - Ask: "Is this experiment's thesis viable, or are there fundamental barriers?"

2. **Create Revision**
   - Update README to address issues (rev2, rev3, rev4, etc.)
   - Document specific changes made and hypothesis for improvement
   - Keep refinements aligned with experiment's core thesis
   - Don't abandon the experiment's unique approach to converge toward another experiment

3. **Test Refinement Across Rounds**

   **Round 2 (first refinement):**
   - Re-run same 3 verses with updated README-rev2
   - Compare quality vs. rev1: did issues get fixed?
   - Agent quality scores should improve by 10-20%

   **Round 3 (second refinement):**
   - If Round 2 showed improvement: refine further based on new feedback
   - If Round 2 failed to improve: try fundamentally different fixes
   - Re-run same 3 verses or add 1-2 new similar verses

   **Round 4 (expansion):**
   - Add 2-3 NEW test verses to verify consistency beyond initial set
   - Choose verses with similar characteristics to test robustness
   - Example: If Habakkuk 3:9 was challenging, try other obscure verses (Nahum 2:1, Zephaniah 2:14)

   **Round 5 (stability check):**
   - Run latest revision on 3-5 additional verses
   - Ensure approach works reliably across broader verse set
   - Quality should be consistent (variation < 15%)

4. **Refinement Stopping Criteria**

   **Stop iterating on this experiment when:**
   - ✅ Quality scores consistently high (8+/10) across all test verses
   - ✅ Agent feedback shows no major blockers or struggles
   - ✅ Approach works reliably for its intended use case
   - ✅ Diminishing returns (improvements between revisions < 5%)

   **OR when fundamental issues can't be fixed:**
   - ❌ Technical blockers (access denied, infrastructure limitations)
   - ❌ Approach doesn't align with project goals after multiple attempts
   - ❌ Quality ceiling is too low despite multiple refinement rounds

5. **Document Refinement Learnings**
   - Update `./bible-study-tools/{tool-name}/experiments/LEARNINGS-round{N}.md` for each major round
   - Note what changed, why, and impact on quality
   - Track revision history and rationale

   **Review Committee Tracking (Rounds 2-5):**
   - In early rounds (2-3), use **broad review committee** with many reviewers asking many questions:
     - Example reviewers: Scholarly Accuracy Reviewer, Translation Sensitivity Reviewer, Contextual Completeness Reviewer, Source Reliability Reviewer, Theological Balance Reviewer, AI Usability Reviewer, Practical Application Reviewer, Cultural Context Reviewer, etc.
     - Each asks 5-10 questions covering their domain
     - Goal: Cast wide net to catch all types of issues
   - **Document which reviewers found which issues:**
     ```markdown
     ## Review Committee Results - Round 2

     | Reviewer | Question | Issue Found | Fixed? | Impact |
     |----------|----------|-------------|--------|--------|
     | Scholarly Accuracy | "Are all dates verified?" | Found unverified claim about 586 BC | Yes | Medium |
     | Source Reliability | "Can all sources be accessed?" | Found 3 broken URLs | Yes | High |
     | AI Usability | "Is citation format consistent?" | Found 12 inconsistent citations | Yes | Low |
     | Practical Application | "Would pastors use this?" | N/A - no issues | N/A | N/A |
     | Cultural Context | "Are non-Western perspectives included?" | Limited to Western sources | No | Low |
     ```
   - Track effectiveness: Which reviewers consistently find real issues? Which questions catch problems?
   - Commit after each round: `chore: round {N} refinements for {experiment-name}`

**Expected Completion:** Each experiment should have 4-6 revisions tested on 6-12 verses total

**Note:** Experiments may complete at different rates. Some may reach quality in 3 rounds (9-15 runs), others may need 5-6 rounds (15-24 runs). Some may be abandoned due to fundamental blockers.

### Phase 4: Round 6 - Cross-Experiment Evaluation and Selection

**Goal:** Determine which approach(es) to advance to production

1. **Comprehensive Cross-Experiment Analysis**
   - Compare final outputs from all experiments that completed refinement
   - Create detailed comparison table in `./bible-study-tools/{tool-name}/experiments/LEARNINGS.md`:

   | Evaluation Criterion | Exp A | Exp B | Exp C | Notes |
   |---------------------|-------|-------|-------|-------|
   | Data Extraction Success Rate | X/Y attempts | X/Y attempts | X/Y attempts | What blocked failures? |
   | Average Quality Score | X.X/10 | X.X/10 | X.X/10 | Across all test verses |
   | Consistency Across Verses | High/Med/Low | High/Med/Low | High/Med/Low | Variance in quality |
   | Source Accessibility | % accessible | % accessible | % accessible | Infrastructure barriers |
   | Target Audience Fit | Rating | Rating | Rating | Would pastors/translators use this? |
   | Methodology Adherence | % | % | % | Deviations required? |
   | AI-Grounding Value | High/Med/Low | High/Med/Low | High/Med/Low | Context depth |
   | Scalability | High/Med/Low | High/Med/Low | High/Med/Low | Can this work for all 31,000 verses? |

   - Weight criteria based on project priorities
   - Calculate overall scores

2. **Decision Point**

   Determine the next course of action:

   **Option A - Clear Winner:**
   - One experiment significantly outperforms others (2+ points higher on 10-point scale)
   - Proceed to Phase 5 (Deep Refinement) with the winning approach only
   - Archive other experiments for reference

   **Option B - Complementary Approaches:**
   - Multiple experiments provide different valuable insights that don't conflict
   - Example: One excels at well-known verses, another at obscure ones
   - Generate 2-3 "blend" experiments combining best elements
   - Run blends through rounds similar to Phase 3 (another 12-24 runs)

   **Option C - Fundamentally Different Tools:**
   - Experiments reveal distinct, incompatible value propositions
   - Split into multiple separate tools
   - Each pursues its own approach independently

   **Option D - All Experiments Insufficient:**
   - None of the approaches meet quality threshold (all < 6/10)
   - Generate 3 entirely new experimental approaches based on learnings
   - Return to Phase 2 with new experiments (another 9+ runs)

3. **Document Decision**
   - Update `./bible-study-tools/{tool-name}/experiments/LEARNINGS.md` with:
     - Executive summary of winner/decision
     - Rationale for selection
     - What made winner superior
     - What was learned from non-winning experiments
   - Commit: `docs: round 6 evaluation and selection`

### Phase 5: Rounds 7-8 - Deep Refinement of Winner

**Goal:** Refine the winning approach to production quality
**Target Runs:** 10-30 additional runs

Now that the strategic direction is clear, focus exclusively on making it excellent:

1. **Expand Test Verse Coverage**
   - Test winning approach on 10-15 additional diverse verses
   - Ensure coverage across:
     - Old Testament and New Testament
     - Narrative, poetry, prophecy, epistles, wisdom literature
     - Well-known and obscure passages
     - Theologically complex and straightforward verses

2. **Structural Refinements** (if needed)
   - Experiment with different schema organizations
   - Test different levels of detail or groupings
   - Example: Flat vs. nested structures, different field names, optional vs. required fields
   - Run 3-5 verses with each structural variant
   - Select structure that best balances completeness and usability

3. **Methodological Refinements**
   - Refine research techniques based on agent feedback
   - Optimize source priorities (which to check first)
   - Test different search strategies
   - Example: Different website access patterns, query formulations
   - Run 3-5 verses with each methodology variant

4. **Prompt and Instruction Refinements** (most granular)
   - Experiment with different instruction phrasings in README
   - Test different examples or constraints
   - Example: Different ways to request citations, emphasis on thoroughness vs. conciseness
   - Run 3-5 verses with each prompt variant
   - Look for subtle quality improvements (5-10% gains)

5. **Quality Consistency Check**
   - Final check: run 5-10 random verses to ensure:
     - Quality scores consistently 8.5+/10
     - Agent feedback is consistently positive
     - Outputs are immediately usable
     - No surprising failures or edge cases

6. **Review Committee Optimization (Rounds 7-8)**

   Based on learnings from Rounds 2-5, optimize the review committee:

   **Analysis:**
   - Review all "Review Committee Results" tables from previous rounds
   - Calculate effectiveness metrics:
     ```
     Reviewer Effectiveness = (Issues Found / Questions Asked) × Average Impact
     Question Effectiveness = (Times It Found Issues / Times It Was Asked)
     ```

   **Optimization:**
   - **Remove low-value reviewers:** Those who found 0 issues across multiple rounds
   - **Remove redundant questions:** Questions that never caught issues
   - **Keep high-value reviewers:** Those who consistently find medium/high impact issues
   - **Refine questions:** Make questions more targeted based on what actually caught problems

   **Example Optimization:**
   ```markdown
   ## Optimized Review Committee - Rounds 7-8

   **Removed (0 issues found across 4 rounds):**
   - Practical Application Reviewer (all outputs were practical)
   - Readability Reviewer (never found issues)

   **Kept and Refined:**
   - Source Reliability Reviewer → Focus on 2 key questions that caught 80% of issues:
     1. "Can all URLs be accessed programmatically?"
     2. "Are all factual claims traceable to sources?"
   - Scholarly Accuracy Reviewer → Focus on 3 questions that found real problems:
     1. "Are all historical dates verified?"
     2. "Are theological claims balanced?"
     3. "Are language-specific claims checked against lexicons?"

   **Result:** 8 reviewers → 3 reviewers, 64 questions → 12 focused questions
   ```

   - Document optimization rationale in LEARNINGS-round{N}.md
   - Goal: **Least reviewers with most focused questions that catch most problems**

**Stopping Criteria:**
- Quality is consistently excellent (8.5+/10)
- Agent feedback shows confidence and satisfaction
- Outputs meet all project standards
- Optimized review committee catches issues efficiently
- Diminishing returns reached (improvements < 3% between iterations)

**Expected Completion:** Winner has been tested on 20-30 total verses with final schema/methodology

### Phase 6: Round 9 - Optimization (Reduction While Maintaining Quality)

**Goal:** Remove unnecessary elements while maintaining output quality
**Target Runs:** 5-10 runs

This phase determines what can be removed or simplified without losing quality:

1. **Schema Optimization**
   - Identify optional fields that are rarely populated or low-value
   - Test removing them: does quality drop?
   - Example: If "historical_context.political_situation" is always empty or generic, remove it
   - Run 3-5 verses without the field
   - If quality maintained, keep it removed; if quality drops, restore it

2. **Instruction Simplification**
   - Identify complex instructions in README that may be unnecessary
   - Test simpler phrasing: does agent still produce quality output?
   - Remove redundant guidance
   - Run 3-5 verses with simplified README
   - Aim for: shortest README that maintains 8.5+/10 quality

3. **Source Optimization**
   - Identify which sources consistently provide value vs. those rarely helpful
   - Test removing low-value sources from required list
   - Does research become faster without quality loss?

4. **Final Validation**
   - Run 5-10 random verses with optimized schema/README
   - Ensure quality remains at 8.5+/10
   - Confirm outputs are leaner but equally valuable
   - Agent feedback should indicate process is streamlined, not stripped

**Completion Criteria:**
- Tool is as simple as possible while maintaining quality
- No unnecessary fields, instructions, or requirements
- Efficient for agents to execute
- Outputs are concise but complete

### Phase 7: Synthesis and Production Deployment

1. **Update Tool README.md**
   - Incorporate the final optimized approach
   - Update schema with validated improvements
   - Add stellar examples discovered during experiments to the examples section
   - Ensure research methodology reflects proven effective techniques
   - Include troubleshooting guidance based on challenges documented
   - Target: 150-250 lines (concise but complete)

2. **Update Tool Registry**
   - Register or update the tool in `/bible-study-tools/tool-registry.yaml`
   - Based on experimentation results, determine appropriate metadata:
     - **Scope:** Based on final optimized file sizes
       - `core`: If files are consistently small (<50 KB) and essential for all queries
       - `standard`: If files are moderate (50-500 KB) and valuable for typical study
       - `comprehensive`: If files are large (>500 KB) or only needed for exhaustive analysis
     - **Category:** lexical|theological|practical|historical|linguistic|topical
     - **Summary:** Concise description (max 20 words) of what the tool provides
   - Example registry entry:
     ```yaml
     {tool-suffix}:
       name: {Tool Name}
       summary: {Brief description from experimentation}
       scope: {core|standard|comprehensive}
       category: {appropriate category}
     ```

3. **Consolidate LEARNINGS.md**
   - Synthesize learnings from all experiment rounds into concise summary
   - Create `./bible-study-tools/{tool-name}/LEARNINGS.md` with format:
     - **Round Summary:** Brief overview of each round
     - **What Worked Well:** Successful techniques, helpful websites, effective schema fields
     - **What Worked Poorly:** Failed approaches, unhelpful sources, problematic structures
     - **Key Insights:** Breakthrough discoveries during experimentation
     - **Stellar Examples:** Best outputs to reference for quality standards
     - **Next Steps:** Future refinement ideas
   - Preserve detailed round documentation in `LEARNINGS-round{N}.md` files for reference
   - Target: LEARNINGS.md = 100-150 lines; detailed round files can be longer

4. **Preserve Experiment History**
   - Keep all experiment folders for future reference
   - Maintain audit trail of tool's evolution
   - Structure:
     ```
     ./experiments/
       ├── {experiment-name-A}/
       │   ├── README-rev1.md
       │   ├── README-rev2.md
       │   └── ...
       ├── {experiment-name-B}/
       ├── {experiment-name-C}/
       ├── output/
       │   ├── {BOOK}-{CH}-{VS}-{experiment-name}-rev{N}.yaml
       │   └── ...
       ├── LEARNINGS.md (concise summary)
       ├── LEARNINGS-round1.md (detailed)
       ├── LEARNINGS-round2.md (detailed)
       └── ...
     ```

5. **Production Readiness Checklist**

   Before declaring tool production-ready, verify:
   - ✅ Tested on 25+ diverse verses
   - ✅ Quality consistently 8.5+/10 across verse types
   - ✅ README is clear, concise (150-250 lines)
   - ✅ Schema is validated and optimized
   - ✅ LEARNINGS.md documents what works and what doesn't
   - ✅ Stellar examples are included in README
   - ✅ No unresolved critical issues
   - ✅ Tool is scalable (can be applied to all 31,000 verses without modification)

6. **Final Comprehensive Validation**

   **Goal:** Go back over ALL key files and validate EVERY requirement was met

   This is the final review before production deployment. Be thorough and systematic.

   **Step 1: Validate Tool Registry Entry**
   - [ ] Tool is registered in `/bible-study-tools/tool-registry.yaml`
   - [ ] Scope is appropriate based on file sizes:
     - [ ] `core` if files <50 KB and essential for all queries
     - [ ] `standard` if files 50-500 KB and useful for typical study
     - [ ] `comprehensive` if files >500 KB or only for exhaustive analysis
   - [ ] Category accurately reflects tool's purpose
   - [ ] Summary is concise (max 20 words) and describes value
   - [ ] Tool suffix matches filename pattern used in outputs

   **Step 2: Validate Tool README.md**
   - [ ] Purpose statement is clear and compelling
   - [ ] Target audience is explicitly defined (pastors, translators, students, etc.)
   - [ ] Research methodology is documented with specific steps
   - [ ] All required sources are listed with access methods
   - [ ] Schema is complete with all required fields documented
   - [ ] **Source access method is optimized:**
     - [ ] If WebFetch: URL pattern is predictable and templatable
     - [ ] If WebSearch: Query patterns are documented
     - [ ] If MCP/Script: Integration is documented
   - [ ] 3-5 stellar examples are included from experiments
   - [ ] Examples cover diverse verse types (well-known, moderate, obscure)
   - [ ] Citation format follows @STANDARDIZATION.md
   - [ ] Quality standards are defined (what makes output excellent?)
   - [ ] Troubleshooting section based on experiment challenges
   - [ ] File is 150-250 lines (concise but complete)

   **Step 3: Validate LEARNINGS.md**
   - [ ] Concise summary format (100-150 lines)
   - [ ] All rounds are summarized briefly
   - [ ] "What Worked Well" section lists specific techniques/sources
   - [ ] "What Worked Poorly" section documents failures
   - [ ] Key insights are clearly articulated
   - [ ] **Source/method optimization is documented:**
     - [ ] Table showing access methods and predictability
     - [ ] Rationale for chosen approach
   - [ ] **Review committee evolution is documented:**
     - [ ] Starting committee composition and question count
     - [ ] Ending committee composition and question count
     - [ ] Rationale for optimization (which reviewers/questions were effective)
   - [ ] Stellar examples are highlighted
   - [ ] Next steps for future improvements are listed
   - [ ] References to detailed LEARNINGS-round{N}.md files

   **Step 4: Validate Detailed Round Files (LEARNINGS-round{N}.md)**
   - [ ] Each round file documents what changed and why
   - [ ] Quality improvements are quantified (scores, metrics)
   - [ ] **Review Committee Results tables are present:**
     - [ ] Documents which reviewers found which issues
     - [ ] Documents which questions caught problems
     - [ ] Tracks effectiveness over rounds
   - [ ] Agent feedback is preserved (Top 3 Insights, Challenges, Quality Metrics)
   - [ ] Blockers and solutions are documented
   - [ ] Files are preserved for audit trail

   **Step 5: Validate Experiment README Files**
   - [ ] Each experiment's thesis is clearly stated
   - [ ] README-rev1 through README-revN show evolution
   - [ ] Final revision represents optimized approach
   - [ ] Schema changes are documented with rationale
   - [ ] Instruction changes are documented with impact
   - [ ] Files demonstrate iterative improvement

   **Step 6: Validate Output Files**
   - [ ] Sample outputs from multiple rounds are preserved
   - [ ] Naming convention is consistent: `{BOOK}-{CH:03d}-{VS:03d}-{experiment-name}-rev{N}.yaml`
   - [ ] Final outputs demonstrate quality improvement over rev1
   - [ ] At least 3 stellar examples are identified for README
   - [ ] Outputs follow @STANDARDIZATION.md citation format
   - [ ] YAML is valid and parseable

   **Step 7: Validate Against Original Requirements**

   Go back to the original tool request and verify:
   - [ ] Tool addresses the original problem statement
   - [ ] Scope is appropriate (not too narrow, not too broad)
   - [ ] Output format meets user needs
   - [ ] Data quality enables AI grounding
   - [ ] Tool is practical for target audience
   - [ ] Scalability to 31,000 verses is feasible

   **Step 8: Validate Optimization Completeness**
   - [ ] **Source/Method:** Chosen approach is most efficient (predictable URLs > search > manual)
   - [ ] **Review Committee:** Optimized to minimum effective reviewers and questions
   - [ ] **Schema:** No unnecessary fields (tested removal in Round 9)
   - [ ] **Instructions:** As concise as possible while maintaining quality
   - [ ] **Performance:** No wasted tool calls or redundant steps

   **Step 9: Final Quality Spot Check**

   Run the optimized tool on 3 random verses (not previously tested):
   - [ ] Quality scores are 8.5+/10
   - [ ] Optimized review committee catches any issues
   - [ ] Outputs are immediately usable
   - [ ] Process is efficient (no wasted steps)
   - [ ] Agent reports confidence and satisfaction

   **If any items fail validation:**
   - Document the gap
   - Create targeted fix
   - Re-test affected areas
   - Update relevant files
   - Re-run validation

   **When all validation passes:**
   - Tool is production-ready
   - Proceed to Step 6 (Commit and Create PR)

7. **Commit and Create PR**
   - Commit with comprehensive message documenting experimentation journey
   - Example:
     ```
     feat: complete sermon-illustrations tool experimentation

     - Completed 9 rounds of experimentation (68 total runs)
     - Tested 28 diverse verses across OT and NT
     - Cultural-artifacts approach emerged as winner (9.3/10 quality)
     - Schema optimized from 45 fields to 32 essential fields
     - README refined from 320 lines to 180 lines
     - Ready for production deployment
     ```
   - Create PR with summary of experimentation process and results
   - Link to key LEARNINGS files for reviewers

## File Naming Conventions

Follow these strict naming patterns:

**Experiment Schema Revisions:**
```
./bible-study-tools/{tool-name}/experiments/{experiment-name}/README-rev{N}.md
```

**Experiment Data Outputs:**
```
./bible-study-tools/{tool-name}/experiments/output/{BOOK}-{CH:03d}-{VS:03d}-{experiment-name}-rev{N}.yaml
```

**Experiment Learnings (Concise Summary):**
```
./bible-study-tools/{tool-name}/experiments/LEARNINGS.md
```

**Experiment Learnings (Detailed Round Documentation):**
```
./bible-study-tools/{tool-name}/experiments/LEARNINGS-round{N}.md
```

Where:
- `{tool-name}`: The Bible study tool being experimented on
- `{experiment-name}`: A descriptive name for the experimental approach (e.g., "cultural-artifacts", "preacher-transcripts")
- `{N}`: Revision or round number (1, 2, 3, etc.)
- `{BOOK}`: USFM 3.0 three-letter book code (MAT, JHN, GEN, etc.)
- `{CH:03d}`: Zero-padded chapter number (001, 005, 038, etc.)
- `{VS:03d}`: Zero-padded verse number (001, 016, etc.)

## Test Verse Selection Strategy

Choose test verses that represent different complexity levels:

**High-Context Verses** (well-studied, rich theological content):
- John 1:1, John 3:16, Matthew 5:3-10, Romans 3:23, Genesis 1:1, Psalm 23:1

**Medium-Context Verses** (moderately studied, specific contexts):
- Colossians 3:1, 1 Samuel 15:3, Daniel 9:25, Psalm 119:105, Acts 17:28

**Low-Context Verses** (obscure, challenging, less-studied):
- Job 38:36, Habakkuk 3:9, Nahum 2:1, Zephaniah 2:14, 3 John 1:4

**Genre Diversity:**
- Narrative: Genesis 1:1, Acts 2:1
- Poetry: Psalm 23:1, Psalm 119:105
- Prophecy: Isaiah 53:5, Habakkuk 3:9
- Epistles: Romans 3:23, Colossians 3:1
- Wisdom: Proverbs 3:5, Job 38:36
- Apocalyptic: Revelation 21:1

Mix categories to ensure experiments work across the full spectrum of Biblical literature.

## Quality Standards

Each experiment should:
- Stay true to its core thesis/hypothesis
- Generate valid YAML that conforms to schema
- Include proper citations following project standards (@STANDARDIZATION.md)
- Provide substantial, AI-grounding content (not superficial summaries)
- Work consistently across different verse types
- Scale to entire Bible without modification

## Success Metrics

The experimentation process is complete when:
- **Sufficient testing:** 50+ experiment runs completed across 25+ verses
- **Clear winner:** A winning approach or blend is validated
- **Consistent quality:** Approach works reliably (8.5+/10) across diverse verse types
- **Optimization complete:** Tool is as simple as possible while maintaining quality
- **Diminishing returns:** Further improvements are < 3% per iteration
- **Production ready:** README, LEARNINGS, and stellar examples are finalized
- **Documented thoroughly:** Future tool usage and development is informed by empirical evidence

## Expected Timeline

**Rough estimates:**
- Phase 1 (Planning): 1-2 hours
- Phase 2 (Round 1): 2-4 hours (9 parallel runs)
- Phase 3 (Rounds 2-5): 6-10 hours (36-54 runs across 3 experiments)
- Phase 4 (Round 6 Evaluation): 1-2 hours
- Phase 5 (Rounds 7-8 Deep Refinement): 4-8 hours (10-30 runs)
- Phase 6 (Round 9 Optimization): 2-3 hours (5-10 runs)
- Phase 7 (Synthesis): 2-3 hours

**Total: 18-32 hours of agent work for a fully validated, production-ready tool**

This investment ensures tools are empirically validated rather than based on assumptions, leading to higher quality AI-grounding data for the entire Bible.
