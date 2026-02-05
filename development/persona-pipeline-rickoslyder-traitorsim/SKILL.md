---
name: persona-pipeline
description: Generate AI agent personas with authentic backstories, demographics, and personality traits for TraitorSim. Use when creating new characters, generating personas, building character libraries, or when asked about persona generation, backstory creation, or character development. Orchestrates Deep Research + Claude synthesis pipeline.
---

# Persona Generation Pipeline

Generate complete AI agent personas with realistic backstories, demographics, and OCEAN personality traits for the TraitorSim game. This skill orchestrates the 5-stage pipeline that uses Gemini Deep Research for demographic grounding and Claude Opus for narrative synthesis.

## Quick Start

```bash
# Generate 15 personas (estimated cost: $6-7)
./scripts/generate_persona_library.sh --count 15

# Or run stages individually:
python scripts/generate_skeleton_personas.py --count 15
python scripts/batch_deep_research.py --input data/personas/skeletons/test_batch_001.json
python scripts/poll_research_jobs.py --jobs data/personas/jobs/test_batch_001_jobs.json
python scripts/synthesize_backstories.py --reports data/personas/reports/test_batch_001_reports.json
python scripts/validate_personas.py --library data/personas/library/test_batch_001_personas.json
```

## Pipeline Overview

The persona generation pipeline consists of 5 stages:

**Stage 1: Skeleton Generation**
- Creates demographic skeletons with archetype assignments
- Samples OCEAN traits from archetype ranges
- Ensures archetype diversity (max 2 per archetype for small batches)
- Output: `data/personas/skeletons/*.json`

**Stage 2: Deep Research Submission**
- Submits background research jobs to Gemini Deep Research agent
- Researches real-world UK demographics for occupation/location
- ~10-20 minutes per job (runs in background)
- Quota-limited: Submit in waves (6→4→2 pattern typical)
- Output: `data/personas/jobs/*_jobs.json` (job IDs)

**Stage 3: Research Job Polling**
- Polls Deep Research jobs until completion
- Status: processing → in_progress → completed
- Retrieves completed reports (20-30KB each)
- Output: `data/personas/reports/*_reports.json`

**Stage 4: Backstory Synthesis**
- Uses Claude Opus 4.5 to generate narrative backstories
- Applies World Bible constraints (in-universe brands)
- Batch synthesis: single query generates multiple personas
- Incremental pattern: only synthesize NEW personas
- Output: `data/personas/library/*_personas.json`

**Stage 5: Validation**
- Validates persona quality and completeness
- Detects forbidden brand leakage (Starbucks, Facebook, etc.)
- Checks OCEAN/stats ranges
- Verifies required fields present
- FAILS FAST if validation errors (no fallback)

## Instructions

### Full Pipeline Execution

When asked to generate a complete persona library:

1. **Determine batch size** (recommend 15-20 for testing, 100+ for production)

2. **Run the master orchestration script**:
   ```bash
   ./scripts/generate_persona_library.sh --count 15
   ```

3. **Monitor quota limits**:
   - Deep Research quota follows pattern: 6→4→2→2 jobs per wave
   - If quota errors occur, wait 5-10 minutes and retry
   - See "Quota Management" section below

4. **Verify results**:
   - Check validation output for 100% pass rate
   - Verify 0 brand leaks detected
   - Confirm archetype distribution is diverse

### Incremental Generation (Adding to Existing Library)

When asked to add more personas to an existing library:

1. **Load existing personas**:
   ```python
   with open('data/personas/library/test_batch_001_personas.json') as f:
       existing_personas = json.load(f)
   existing_ids = {p['skeleton_id'] for p in existing_personas}
   ```

2. **Generate new skeletons** (avoiding duplicate IDs)

3. **Submit Deep Research jobs** for new skeletons only

4. **Synthesize only new personas**:
   ```bash
   # Extract only new reports
   python -c "import json; ..."  # Filter to new reports

   # Synthesize
   python scripts/synthesize_backstories.py --reports /tmp/new_reports_only.json --output /tmp/new_personas

   # Merge
   python -c "import json; ..."  # Combine existing + new
   ```

5. **Validate merged library**

### Quota Management

Deep Research API has rate limits (specific limits not publicly documented). Use these strategies:

**Strategy 1: Wave Submission**
```python
# Submit in waves with delays
wave_sizes = [6, 4, 2, 2, 1]  # Observed pattern
for wave_size in wave_sizes:
    jobs = submit_batch(wave_size)
    time.sleep(300)  # 5 min between waves
```

**Strategy 2: Client-Side Tracking**
```python
from scripts.quota_tracker import QuotaTracker

tracker = QuotaTracker(rpm_limit=10, rpd_limit=100)
if tracker.can_make_request():
    submit_job()
    tracker.record_request()
else:
    wait_time = tracker.time_until_available()
    time.sleep(wait_time)
```

**Strategy 3: Exponential Backoff**
```python
for attempt in range(max_retries):
    try:
        submit_job()
        break
    except QuotaError:
        wait_time = min(2 ** attempt * 60, 3600)  # Max 1 hour
        time.sleep(wait_time)
```

### World Bible Constraints

Ensure personas use in-universe brands (not real-world brands):

**Approved In-Universe Brands:**
- Highland Spring Co. (water)
- Cairngorm Coffee Roasters (coffee)
- Heather & Thistle Crisps (snacks)
- Loch Provisions (meals)
- Royal Oak Spirits (alcohol)
- Baronial Casual Wear (clothing)
- ScotNet (social media/internet)
- CastleVision (production company)

**Forbidden Real-World Brands:**
- Starbucks, Costa, Pret (use Cairngorm Coffee)
- Facebook, Instagram, Twitter (use ScotNet)
- Netflix, BBC iPlayer (use CastleVision)
- Evian, Fiji (use Highland Spring)

Validation automatically detects forbidden brands using word boundary regex.

## Cost Estimates

**Per Persona:**
- Deep Research: ~$0.35
- Claude Opus synthesis (batch): ~$0.05
- **Total: ~$0.40-$0.45 per persona**

**Batch Estimates:**
- 15 personas: ~$6-$7
- 50 personas: ~$20-$22
- 100 personas: ~$40-$45

**Cost Optimization:**
- Use batch synthesis (single query for multiple personas)
- Use incremental synthesis (only generate new personas)
- Reuse persona library across multiple game runs (no runtime cost)

## Archetype System

13 predefined archetypes with distinct gameplay tendencies:

1. **The Prodigy** - High intellect, high openness
2. **The Charming Sociopath** - Low agreeableness, high extraversion
3. **The Misguided Survivor** - Low openness, high neuroticism
4. **The Comedic Psychic** - High extraversion, low conscientiousness
5. **The Bitter Traitor** - Low agreeableness, high neuroticism
6. **The Infatuated Faithful** - High agreeableness, low intellect
7. **The Quirky Outsider** - High openness, neurodivergent traits
8. **The Incompetent Authority** - Facade conscientiousness, low intellect
9. **The Zealot** - High conscientiousness, low openness
10. **The Romantic** - High agreeableness, trusting
11. **The Smug Player** - Low agreeableness, moral superiority
12. **The Mischievous Operator** - Low conscientiousness, Machiavellian
13. **The Charismatic Leader** - High social influence, high extraversion

Each archetype has:
- OCEAN trait ranges (e.g., openness: 0.8-0.95)
- Stat biases (intellect, dexterity, social_influence)
- Typical occupations and demographics
- Strategic gameplay profile

## Validation Criteria

Personas must pass ALL validation checks:

- ✅ Required fields present (name, backstory, demographics, personality, stats)
- ✅ OCEAN traits in valid ranges (0.0-1.0)
- ✅ Stats in valid ranges (defined by archetype)
- ✅ Backstory length: 200-1600 characters
- ✅ Zero forbidden brand leakage
- ✅ UK-appropriate names and locations
- ✅ Archetype distribution is diverse

**Fail Fast**: If validation fails, the pipeline stops immediately. No random fallback.

## Persona Card Structure

Each persona card contains:

```json
{
  "skeleton_id": "skeleton_010",
  "archetype": "charismatic_leader",
  "archetype_name": "The Charismatic Leader",
  "name": "Gemma Ashworth-Clarke",
  "demographics": {
    "age": 31,
    "occupation": "motivational speaker",
    "location": "London",
    "socioeconomic": "upper-middle",
    "gender": "female"
  },
  "personality": {
    "openness": 0.72,
    "conscientiousness": 0.78,
    "extraversion": 0.91,
    "agreeableness": 0.65,
    "neuroticism": 0.54
  },
  "stats": {
    "intellect": 0.75,
    "dexterity": 0.60,
    "social_influence": 0.88
  },
  "backstory": "First-person narrative (200-300 words)...",
  "key_relationships": ["..."],
  "formative_challenge": "...",
  "political_beliefs": "...",
  "hobbies": ["...", "...", "..."],
  "strategic_approach": "..."
}
```

## Common Issues and Solutions

**Issue: Quota errors during Deep Research submission**
- Solution: Submit in waves, wait 5-10 min between waves
- See quota management strategies above

**Issue: Jobs stuck in "processing" status**
- Solution: Keep polling, Deep Research takes 10-20 min per job
- Check for "in_progress" status (not just "completed")

**Issue: Brand leakage detected**
- Solution: Review synthesis prompts, ensure World Bible constraints clear
- Update `src/traitorsim/utils/world_flavor.py` with new forbidden brands

**Issue: Backstory too short/long**
- Solution: Adjust synthesis prompt to specify 200-300 words
- Update validation limits if needed

**Issue: Re-synthesizing existing personas (wasting cost)**
- Solution: Use incremental synthesis pattern
- Filter reports to only NEW skeleton IDs before synthesis

## Advanced Usage

See [docs/PERSONA_GENERATION_LESSONS.md](../../docs/PERSONA_GENERATION_LESSONS.md) for:
- Complete 12-lesson post-mortem from 15-persona test batch
- Detailed cost analysis
- Timeline projections for 100+ persona batches
- Production readiness checklist
- All quota management strategies with code examples

## Testing

Test the pipeline with a small batch first:

```bash
# Generate 2 test personas
python scripts/generate_skeleton_personas.py --count 2 --output data/personas/skeletons/test_mini.json
python scripts/batch_deep_research.py --input data/personas/skeletons/test_mini.json --output data/personas/jobs/test_mini_jobs.json

# Monitor completion
python scripts/poll_research_jobs.py --jobs data/personas/jobs/test_mini_jobs.json --output data/personas/reports/test_mini_reports.json

# Synthesize
python scripts/synthesize_backstories.py --reports data/personas/reports/test_mini_reports.json --output data/personas/library/test_mini_personas.json --model claude-opus-4-5-20251101

# Validate
python scripts/validate_personas.py --library data/personas/library/test_mini_personas.json
```

Expected output: 100% validation pass, 0 brand leaks, ~$0.90 cost for 2 personas.

## Requirements

**Environment Variables:**
```bash
export GEMINI_API_KEY="..."            # For Deep Research
export CLAUDE_CODE_OAUTH_TOKEN="..."  # For Claude synthesis
```

**Python Dependencies:**
```bash
pip install google-genai claude-agent-sdk
```

**File Structure:**
```
data/personas/
├── skeletons/       # Stage 1 output
├── jobs/            # Stage 2 output (job IDs)
├── reports/         # Stage 3 output (research reports)
└── library/         # Stage 4 output (final personas)

scripts/
├── generate_skeleton_personas.py
├── batch_deep_research.py
├── poll_research_jobs.py
├── synthesize_backstories.py
└── validate_personas.py
```

## Success Metrics

A successful persona generation run should achieve:
- ✅ 100% validation pass rate
- ✅ 0 forbidden brand leaks
- ✅ Diverse archetype distribution
- ✅ Realistic UK demographics and backstories
- ✅ Cost within estimates (~$0.45/persona)
- ✅ All OCEAN traits within archetype ranges
- ✅ Backstories reference specific locations, occupations, relationships

## When to Use This Skill

Use this skill when:
- Creating a new persona library for a game
- Adding personas to an existing library
- Testing archetype designs with real generated personas
- Troubleshooting persona quality issues
- Understanding persona generation costs and timelines
- Converting random personality initialization to grounded personas

## When NOT to Use This Skill

Don't use this skill for:
- Real-time persona generation during gameplay (personas are pre-generated offline)
- Modifying existing personas (use archetype-designer skill instead)
- Validating World Bible lore compliance (use world-bible-validator skill)
- Managing API quotas (use quota-manager skill instead)
