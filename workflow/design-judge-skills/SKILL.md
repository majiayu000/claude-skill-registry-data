---
name: design-judge-skills
description: Evidence-driven agent skills for design award research, evaluation, matching, entry preparation, and submission checks across 11+ major design awards
triggers:
  - help me apply for design awards
  - evaluate this design for award submission
  - find similar award-winning designs
  - which design award should I enter
  - prepare my design award entry text
  - check my award submission package
  - design award pipeline workflow
  - match my project to design awards
---

# design-judge-skills

> Skill by [ara.so](https://ara.so) — Design Skills collection.

`design-judge-skills` is a collection of modular agent skills that decompose the design award application process into discrete, verifiable workflows: award-winning case research, design evaluation, award matching, entry writing, and submission readiness checks.

The project covers 11 major design awards including iF DESIGN AWARD, Red Dot, IDEA, DIA, K-Design, GOOD DESIGN AWARD Japan, Core77, James Dyson Award, and EPDA. It includes observational data from **22,125 award-winning or finalist works** and enforces evidence-based evaluation with official source validation.

## Installation

### NPX Skills Installation (Recommended)

Requires [Node.js 18+](https://nodejs.org/).

**List available skills:**

```bash
npx skills add SeanJ1ang/design-judge-skills --list
```

**Install all skills globally for Codex:**

```bash
npx skills add SeanJ1ang/design-judge-skills --global --agent codex --skill '*' --yes --copy
```

**Install for Claude Code:**

```bash
npx skills add SeanJ1ang/design-judge-skills --global --agent claude-code --skill '*' --yes --copy
```

**Install a single skill with dependencies:**

```bash
# design-award-search and design-award-match require design-judge-shared
npx skills add SeanJ1ang/design-judge-skills --global --agent codex \
  --skill design-award-search --skill design-judge-shared --yes --copy
```

**Install to all supported agents:**

```bash
npx skills add SeanJ1ang/design-judge-skills --all
```

**Check and update:**

```bash
npx skills list --global --agent codex
npx skills update --global --yes
```

### Manual Installation

For agents that support `SKILL.md` format:

1. Clone the repository to a stable path
2. Copy complete skill directories to your agent's skill directory
3. Preserve `SKILL.md`, `agents/`, `references/`, `scripts/`, `examples/`, and `tests/`
4. When installing `design-award-search` or `design-award-match`, also install `design-judge-shared`

## Skills Overview

The project provides 6 user-facing skills plus 1 shared support package:

| Skill | Status | Purpose |
|-------|--------|---------|
| `design-award-pipeline` | Beta | Orchestrates multi-stage award workflows and maintains handoff records |
| `design-award-search` | Stable | Retrieves and verifies similar award-winning cases from official sources |
| `design-evaluation` | Beta | Evaluates design quality and presentation with evidence-based scoring |
| `design-award-match` | Beta | Matches projects to awards, tracks, and categories with eligibility checks |
| `design-information-prep` | Beta | Extracts facts and prepares award entry text from user materials |
| `design-submission-check` | Beta | Validates submission packages against current official requirements |
| `design-judge-shared` | Support | Shared taxonomy and source registry (dependency only) |

## Workflow Patterns

### Complete Award Application Pipeline

```text
Use $design-award-pipeline to plan the complete award route from the provided materials and maintain stage handoff records.
```

The pipeline skill determines the minimal sufficient path based on user intent and current materials. It does NOT force execution of all stages.

### Finding Award-Winning Benchmarks

```text
Use $design-award-search to find officially verified award-winning cases similar to this rehabilitation training product.
```

**Key behaviors:**
- Searches official award galleries (iF, Red Dot, IDEA, etc.)
- Verifies each case by navigating to the official detail page
- Reports case metadata: award name, year, category, project title, designer, country
- Search summaries and third-party sites are used for discovery only

### Evaluating Design Quality

```text
Use $design-evaluation to evaluate the design in the attached files. I confirm the maturity level as "student concept". Output separate scores for design substance, presentation quality, evidence confidence, and critical issues.
```

**Maturity levels** (user must specify):
- `student-concept`: Conceptual work without market release
- `early-stage-product`: Pre-production or limited release
- `market-product`: Publicly available commercial product

**Evaluation dimensions:**
- Design substance (innovation, user value, feasibility, sustainability)
- Presentation quality (visual clarity, narrative logic, material completeness)
- Evidence confidence (factual vs. inferred vs. needs-user-confirmation)
- Critical issues (structural disqualifiers, misrepresentation risks, IP concerns)

**Example output structure:**

```markdown
## Design Substance: 7.8/10
- Innovation: 8/10 [evidence: novel mechanism in attached patent draft]
- User Value: 8/10 [evidence: user research summary p.3]
- Feasibility: 7/10 [inferred from CAD model; material sourcing not confirmed]
- Sustainability: 8/10 [evidence: LCA report attached]

## Presentation Quality: 6.5/10
- Visual Clarity: 7/10
- Narrative Logic: 6/10 [gap: user journey not visualized]
- Material Completeness: 6/10 [missing: technical specs diagram]

## Evidence Confidence: MEDIUM
- 60% factual (from attached documents)
- 25% model inference (from images and context)
- 15% needs user confirmation (material sourcing, certifications)

## Critical Issues: 2 items
1. [ELIGIBILITY] Production timeline unclear → may affect student vs. professional track
2. [EVIDENCE] Sustainability claim lacks third-party certification
```

Scores are for decision support only. They do NOT predict award probability.

### Matching Awards and Categories

```text
Use $design-award-match to compare award fit for iF Student, Red Dot Design Concept, DIA, Core77, and James Dyson for this project.
```

**Match outputs:**
- Structural eligibility (geographic, entity type, IP rights, timeline)
- Category recommendations with official taxonomy references
- Track selection (when applicable: student vs. professional, concept vs. product)
- Award fee, deadline (re-verified from official pages at runtime)
- Submission priority ranking with rationale

**Example snippet:**

```markdown
## iF DESIGN STUDENT AWARD
- Eligibility: ✓ PASS (student status confirmed, no geographic restriction)
- Best Category: 08 Health & Care → 08.03 Rehabilitation
- Fee: €0 (student track)
- Deadline: 2026-12-15 (re-verified from https://ifdesign.com/en/student-award)
- Priority: HIGH (strong alignment with evaluation criteria; no concept-stage penalty)

## Red Dot Design Concept
- Eligibility: ✓ PASS (concept stage accepted)
- Best Category: Living → Wellness & Healthcare
- Fee: €299 Early Bird / €399 Regular
- Deadline: 2026-10-31 Early / 2026-12-31 Regular
- Priority: MEDIUM (good fit but higher cost; consider after iF Student results)
```

### Preparing Entry Text

```text
Use $design-information-prep to prepare IDEA entry text from the attached materials. First list missing facts, then output English drafts with character count validation.
```

**Workflow:**
1. Extracts facts from user-provided documents (briefs, research, specs, images)
2. Reports missing mandatory fields for target award
3. Generates entry text drafts (title, description, innovation statement, etc.)
4. Validates character/word limits against official requirements
5. Tags each sentence with source attribution or `[INFERRED]` / `[USER CONFIRM]`

**Example output:**

```markdown
## Missing Information for IDEA Entry
- [ ] Project completion date (required)
- [ ] Retail price or production cost estimate
- [ ] Specific material certifications (referenced in sustainability claim)

## Draft: Project Title (max 100 chars)
**VitalGrip Rehabilitation Glove** [78 chars] ✓

## Draft: Design Innovation (max 500 words)
VitalGrip introduces a modular resistance system... [source: design brief p.2]
The sensor array provides real-time feedback... [source: technical spec diagram]
Preliminary user testing showed 40% improvement... [INFERRED from user research summary; USER CONFIRM exact metric]

[Draft continues...]
Word count: 487/500 ✓
```

### Submission Readiness Check

```text
Use $design-submission-check to validate this submission package against current Red Dot Product Design official requirements and provide a go/no-go recommendation.
```

**Check dimensions:**
- File format, resolution, size limits (re-verified from official submission guide)
- Mandatory vs. optional materials completeness
- Consistency across title, description, category, visual materials
- IP and rights declarations (model releases, trademark conflicts, authorship)
- Payment and entry form status

**Output format: go / conditional go / no-go**

```markdown
## Submission Check: Red Dot Product Design 2027

### File Compliance: ✓ PASS
- Main image: 3000×2250px JPG, 4.2MB ✓
- Supporting images (4): all 3000×2250px JPG ✓
- Video: MP4 1920×1080, 45s, 28MB ✓

### Content Completeness: ⚠ CONDITIONAL
- ✓ Project title, description, category
- ✓ Designer/company information
- ⚠ Innovation statement present but does NOT reference technical validation (recommended for this category)
- ✗ Sustainability documentation missing (required for "Sustainable Product" sub-category)

### Consistency Check: ✓ PASS
- Title matches across entry form and visual materials
- Category "01.03 Medical & Health" aligns with project scope

### Rights & IP: ⚠ CONDITIONAL
- ✓ Designer authorship declared
- ⚠ Model release for user testing photos not provided (required if faces visible)

## Recommendation: CONDITIONAL GO
**Action required before submission:**
1. Upload model release forms for user testing photos
2. Add technical validation reference to innovation statement (recommended)
3. Either remove "Sustainable Product" tag OR provide third-party certification

**Estimated fix time:** 2-4 hours
```

## Configuration & Data Sources

### Official Source Validation

Skills re-verify time-sensitive information (deadlines, fees, eligibility, format specs) at runtime by scraping official award pages. The `design-judge-shared/source-registry.md` maintains canonical URLs.

**Example source registry entry:**

```markdown
### iF DESIGN AWARD
- Main: https://ifdesign.com/en/design-award
- Submission Guide: https://ifdesign.com/en/submit
- Categories: https://ifdesign.com/en/categories
- Winners Gallery: https://ifdesign.com/en/winner-gallery
```

### Category Taxonomy

`design-judge-shared/category-taxonomy.md` maintains normalized category mappings across awards. Example:

```markdown
## Health & Medical Devices
- iF: 08 Health & Care
- Red Dot: Living → Wellness & Healthcare
- IDEA: Medical & Scientific Products
- DIA: Healthcare & Wellness
- K-Design: Medical & Health
```

### Observational Benchmark Data

Evaluation skills reference 22,125 aggregated observations from past winners (2015-2025) to provide descriptive context. This data:
- Does NOT alter core scoring logic
- Does NOT predict award probability
- Provides pattern recognition for presentation quality and category norms
- Is anonymized (no private project details)

See [benchmark coverage documentation](docs/benchmark-coverage.md) for privacy and limitation details.

## Environment Variables

No API keys or authentication required for basic functionality. Optional:

```bash
# For enhanced web scraping (if official sites use anti-bot measures)
export BROWSERLESS_API_KEY=your_key_here

# For bulk processing (optional concurrency limit)
export MAX_CONCURRENT_EVALUATIONS=5
```

## Common Patterns

### Pattern 1: Student Concept → Award Route

```python
# User provides: concept boards, research deck, CAD renderings
# Agent workflow:

# Step 1: Evaluate to confirm strengths and gaps
"Use $design-evaluation with maturity level 'student-concept'"

# Step 2: Match to student-friendly awards
"Use $design-award-match to compare iF Student, Red Dot Concept, Core77, James Dyson, and DIA for this student concept"

# Step 3: Prepare entry for top match
"Use $design-information-prep for iF DESIGN STUDENT AWARD"

# Step 4: Pre-submission check
"Use $design-submission-check for iF Student entry package"
```

### Pattern 2: Multi-Award Strategy

```python
# For a market product targeting multiple awards:

# Step 1: Find positioning benchmarks
"Use $design-award-search to find similar award winners in the smart home category from the past 3 years"

# Step 2: Evaluate against benchmark patterns
"Use $design-evaluation with maturity level 'market-product'"

# Step 3: Prioritize awards by fit and cost
"Use $design-award-match to compare iF, Red Dot Product, IDEA, DIA, K-Design, and GOOD DESIGN Japan"

# Step 4: Batch prepare entries for top 3
"Use $design-information-prep for iF DESIGN AWARD, Red Dot Product Design, and IDEA"
```

### Pattern 3: Pipeline Orchestration

```python
# When user says: "I have a rehabilitation glove concept and want to enter design awards"

"Use $design-award-pipeline to determine the optimal workflow and maintain handoff state"

# Pipeline decides minimal path, e.g.:
# 1. Evaluation (to assess readiness)
# 2. Award match (to select targets)
# 3. Information prep (for selected awards)
# 4. Submission check (before deadline)

# Pipeline maintains state file to resume or skip stages
```

## Troubleshooting

### Issue: Skill not triggering

**Solution:** After installation, start a NEW agent session to refresh skill registry. For Codex:

```bash
npx skills list --global --agent codex  # verify installation
# Then restart Codex session
```

### Issue: "Missing design-judge-shared" error

**Solution:** Install the shared dependency:

```bash
npx skills add SeanJ1ang/design-judge-skills --global --agent codex \
  --skill design-judge-shared --yes --copy
```

### Issue: Evaluation returns "insufficient evidence"

**Cause:** Missing or ambiguous design materials.

**Solution:** Provide at minimum:
- Visual materials (renderings, photos, or presentation boards)
- Project description (brief, design statement, or report)
- Maturity level confirmation from user

### Issue: Award match returns "eligibility unclear"

**Cause:** Missing structural information (student status, geographic location, IP ownership, production timeline).

**Solution:** Explicitly confirm:
- Entity type (student, startup, established company)
- Designer location (for geographic restrictions)
- IP ownership status
- Project completion date (for timeline-based eligibility)

### Issue: Official page scraping fails

**Cause:** Award website structure changed or anti-bot protection.

**Temporary workaround:** Manually verify deadline/fee from official site and provide to agent:

```text
I've verified from the official iF page: deadline is 2026-12-15, fee is €0 for students. Use this information for the match analysis.
```

**Long-term fix:** Report the issue at https://github.com/SeanJ1ang/design-judge-skills/issues with the affected award and URL.

### Issue: Character count validation fails

**Cause:** Award official requirement changed.

**Solution:** Cross-check the current submission guide link in `design-judge-shared/source-registry.md` and report discrepancy as an issue.

## Testing

Each skill includes example inputs and expected outputs in `skills/<name>/examples/` and automated tests in `skills/<name>/tests/`.

**Run tests for a specific skill:**

```bash
cd skills/design-evaluation
python tests/test_evaluation.py
```

**Run all tests:**

```bash
python run_all_tests.py
```

## Design Principles

1. **Official sources first:** Award rules and cases reference official pages; search summaries and third-party sites are for discovery only
2. **Separate fact from inference:** User materials, model inferences, and user-confirmation items are explicitly tagged
3. **Transparent scoring:** Fit scores and evaluation ratings support decisions but DO NOT predict award probability
4. **Single responsibility:** Skills do not cross boundaries (search ≠ evaluation ≠ matching ≠ prep ≠ check)
5. **No official impersonation:** Skills align with public criteria but do not simulate undisclosed judge preferences or internal processes

## Contributing

See [contribution guidelines](docs/CONTRIBUTING.md). Key points:

- Skill directory names match frontmatter `name` (kebab-case only)
- Core workflows stay in `SKILL.md`; long rules/specs go in `references/`
- Repeatable operations become `scripts/` with corresponding tests
- Do NOT commit API keys, cookies, user project materials, or copyrighted full case content
- Current year, deadlines, fees, and format specs must be runtime-verified from official sources

## License

Apache-2.0. See [LICENSE](LICENSE).

## Links

- Repository: https://github.com/SeanJ1ang/design-judge-skills
- Benchmark Coverage: [docs/benchmark-coverage.md](docs/benchmark-coverage.md)
- Skill Index: [README.md#6-技能索引](README.md#6-技能索引)
- English Documentation: [README_EN.md](README_EN.md)
