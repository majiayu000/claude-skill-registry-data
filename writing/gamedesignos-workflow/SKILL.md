---
name: gamedesignos-workflow
description: AI-native game design, concept validation, and prototyping system with evidence-first agent skills for analysis, concept architecture, and workflow evolution
triggers:
  - analyze this game's experience and create an evidence report
  - turn this game idea into a validated concept architecture
  - help me write a game design proposal
  - diagnose this game's experience density and retention issues
  - evolve this game design workflow with WOOP and OODA
  - translate this game design text to professional Chinese
  - curate these game design sources into a knowledge base
  - create a player promise contract for this concept
---

# GameDesignOS Workflow Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

GameDesignOS is an evidence-first agent skill system for game design analysis, concept architecture, validation planning, and AI workflow evolution. It transforms game experience diagnosis, concept development, proposal writing, experience-density optimization, and design knowledge curation into reusable, contract-driven agent instructions.

## What GameDesignOS Does

GameDesignOS provides 7 specialized skills that work together through contracts (evidence indexes, player promises, validation plans, ED handoffs):

1. **Game Experience Analyzer** - Turn screenshots/recordings/PVs into timestamped evidence reports
2. **Game Concept Architect** - Convert ideas into player promises, core loops, and validation plans
3. **Game Design Proposal Writer** - Assemble research into decision-ready proposals
4. **Game Experience Density Optimizer** - Diagnose retention/pacing issues with A/B plans
5. **Paranoia AI System Evolver** - Upgrade workflows with WOOP/VOI/OODA/evals
6. **Game Design Book Translator** - Translate English design texts to professional Chinese
7. **Game Design Source Curator** - Build maintainable design knowledge bases

## Installation

### Clone the Repository

```bash
git clone https://github.com/ParanoiaGames/GameDesignOS.git
cd GameDesignOS
```

### Install Skills in Your Agent Environment

Copy the skill folders you need into your agent's skill directory:

```bash
# For Cursor/Claude Code/Codex (example paths)
cp -r game-experience-analyzer/ ~/.cursor/skills/
cp -r game-concept-architect/ ~/.cursor/skills/
cp -r game-design-proposal-writer/ ~/.cursor/skills/
cp -r game-experience-density-optimizer/ ~/.cursor/skills/
cp -r paranoia-ai-system-evolver/ ~/.cursor/skills/
cp -r game-design-book-translator/ ~/.cursor/skills/
cp -r game-design-source-curator/ ~/.cursor/skills/
```

### Verify Installation

Each skill has a `SKILL.md` manifest. Check that:
- The `name` field matches the folder name
- Relative links to `references/`, `templates/`, `examples/` resolve correctly

```bash
# Verify a skill's structure
ls -la game-experience-analyzer/
# Should show: SKILL.md, references/, templates/, examples/
```

## Core Skills and Usage Patterns

### 1. Game Experience Analyzer

**Purpose:** Convert game media (screenshots, gameplay recordings, trailers, PVs) into evidence-linked diagnosis reports.

**Trigger:**
```
Use $game-experience-analyzer to analyze this gameplay recording into timestamped evidence, Hook/Loop/Link/Surprise diagnosis, issue cards, and validation recommendations.
```

**Input Types:**
- Screenshots of gameplay moments
- Gameplay recording URLs or files
- Trailer/PV links (YouTube, Bilibili)
- Steam page media

**Output Contract:**
```yaml
evidence_index:
  sample_boundary: "0:00-15:23 first session"
  timestamped_evidence:
    - timestamp: "0:34"
      frame: "./evidence/frame-0034.png"
      observation: "Tutorial skips player verb introduction"
      issue_severity: "high"
  
  hook_loop_link_surprise:
    hook: "Strong visual hook at 0:12 with city reveal"
    core_loop: "Build → Battle → Upgrade cycle clear at 2:45"
    link: "Weak motivation link between missions"
    surprise: "Boss reveal at 8:30 creates high interest"

issue_cards:
  - id: "ISS-001"
    type: "feature_exposure"
    priority: "P0"
    evidence: ["frame-0034.png", "frame-1205.png"]
    fix_hypothesis: "Add verb tutorial before first combat"
```

**Example Usage:**

```python
# In your agent conversation:
"""
I have a 10-minute gameplay recording of our new roguelike.
Use $game-experience-analyzer to create an evidence report with:
- Timestamped feature exposure ledger
- Hook/Loop/Link/Surprise diagnosis
- Issue cards prioritized by retention risk
- Validation recommendations for A/B tests

Recording: ./recordings/session-001.mp4
"""
```

**Real Example Output:**
See `game-experience-analyzer/examples/survival-33-days-gameplay-experience-report.md` for a 41-minute recording analyzed with timestamps, visual evidence, and actionable fixes.

### 2. Game Concept Architect

**Purpose:** Transform one-line game ideas into structured concept seeds, player promises, core loops, and validation plans.

**Trigger:**
```
Use $game-concept-architect to turn this game idea into a concept seed, player promise contract, core loop, scope gate, and prototype validation plan.
```

**Input:**
```
One-line idea: "A farming game where you grow magical creatures instead of crops"
```

**Output Contract:**
```yaml
player_promise_contract:
  player_verbs: ["nurture", "harvest", "combine", "discover"]
  action_goal_alignment:
    core_action: "Daily creature care with visible trait evolution"
    short_term_goal: "Unlock new creature types (session)"
    medium_term_goal: "Master breeding combinations (week)"
    long_term_goal: "Complete creature compendium (month)"
  
  uncertainty_sources:
    - "Which trait combinations produce rare creatures?"
    - "What feeding patterns unlock evolution paths?"
  
  scope_gate:
    must_have: ["5 base creatures", "breeding system", "trait visualization"]
    nice_to_have: ["creature marketplace", "seasonal events"]
    out_of_scope: ["PvP battles", "multiplayer trading"]

validation_plan:
  prototype_scope: "Single creature lifecycle with 3 evolution paths"
  key_metrics: ["breeding attempts per session", "discovery moments per hour"]
  success_criteria: "60% of players attempt 3+ breedings in first session"
```

**Example Usage:**

```python
# In your agent conversation:
"""
Use $game-concept-architect to develop this idea:

"A reverse tower defense where you play as the monsters trying to reach the castle, 
and you unlock new monster types by failing in creative ways"

I need:
- Concept seed with player verbs
- Player promise contract
- Core loop with 3 layers
- Scope gate for 3-month prototype
- Validation plan with testable hypotheses
"""
```

### 3. Game Design Proposal Writer

**Purpose:** Assemble concept briefs, evidence, and constraints into decision-ready proposals (publisher pitches, internal greenlight docs, vertical slice plans).

**Trigger:**
```
Use $game-design-proposal-writer to turn this concept brief, validation plan, evidence notes, and production constraints into a decision-ready commercial proposal.
```

**Input Structure:**
```yaml
inputs:
  concept_brief: "./concepts/creature-farm-v2.md"
  evidence_index: "./evidence/prototype-playtest-2024-12.md"
  validation_plan: "./validation/breeding-engagement-test.md"
  production_constraints:
    team_size: 4
    timeline: "12 months"
    target_platform: "PC/Steam"
```

**Output Contract:**
```yaml
proposal_structure:
  executive_summary:
    one_line_pitch: "Creature breeding farm with discovery-driven progression"
    target_audience: "Stardew Valley + Pokemon players (ages 16-35)"
    market_positioning: "Premium indie ($19.99), PC-first with console ports"
  
  proof_of_play:
    evidence: ["prototype-v2 playtest results", "wishlist conversion 8.2%"]
    validated_hooks: ["breeding discovery loop", "trait visualization joy"]
  
  scope_and_timeline:
    mvp_scope: "15 creatures, 3 biomes, breeding system"
    milestone_gates:
      - month_3: "Core loop validated (retention > 40%)"
      - month_6: "Content pipeline proven (1 creature/week)"
      - month_9: "Beta with 30 creatures, polish pass"
  
  risks_and_mitigation:
    - risk: "Breeding complexity overwhelming new players"
      evidence: "Playtest feedback 12/15 confused in first 10min"
      mitigation: "Simplified tutorial + progressive complexity"
```

**Example Usage:**

```python
# In your agent conversation:
"""
Use $game-design-proposal-writer to create a publisher pitch using:

Concept: [paste creature farm concept]
Evidence: We have prototype playtest data showing 45% day-1 retention
Team: 4 people (2 engineers, 1 artist, 1 designer)
Timeline: 18 months to 1.0
Budget ask: $300k

Format: Publisher pitch deck outline with proof of play section
"""
```

### 4. Game Experience Density Optimizer

**Purpose:** Diagnose retention/pacing issues and create weekly A/B experiment plans with instrumentation.

**Trigger:**
```
Use $game-experience-density-optimizer to turn this first-session retention problem into ED diagnosis, weekly A/B variants, instrumentation, and rollback gates.
```

**ED Framework:**
```yaml
experience_density_dimensions:
  CLP: "Core Loop Participation (actions/minute)"
  SF: "Soft Friction (waiting, confusion, busywork)"
  EB: "Embodiment (control responsiveness, feedback)"
  AR: "Atmospheric Richness (audiovisual coherence)"
  MD_min: "Minimum Discovery (new info/minute)"
```

**Input Example:**
```yaml
problem_statement:
  metric: "Day 1 retention dropped from 42% to 31% after tutorial update"
  hypothesis: "New tutorial adds 8 minutes of soft friction before core loop"
  evidence: "./analytics/retention-drop-2024-12.csv"
```

**Output Contract:**
```yaml
ed_diagnosis:
  current_state:
    CLP_first_10min: 2.1  # actions per minute
    SF_tutorial: 8.3      # minutes before first core action
    MD_min: 0.4           # discoveries per minute
  
  lever_recommendations:
    - lever: "SF_reduction"
      change: "Cut tutorial from 8min to 3min, defer advanced features"
      expected_delta: "SF: 8.3→3.1, CLP: 2.1→3.8"
      cost: "2 days implementation"

weekly_experiment:
  variant_matrix:
    control: "Current 8min tutorial"
    variant_a: "3min core tutorial, advanced defer to first use"
    variant_b: "Tutorial skippable after 1min with comeback hints"
  
  instrumentation:
    events:
      - "tutorial_started"
      - "tutorial_completed"
      - "first_core_action"
      - "session_10min_reached"
    dashboard_fields:
      - "tutorial_completion_rate"
      - "time_to_first_core_action"
      - "d1_retention_by_variant"
  
  decision_rules:
    success_criteria: "Variant retention > control + 5pp (p<0.05)"
    rollback_trigger: "Variant retention < control - 3pp after 500 users"
```

**Example Usage:**

```python
# In your agent conversation:
"""
Use $game-experience-density-optimizer to diagnose this problem:

Our puzzle game's first session used to average 12 minutes, now it's 8 minutes.
Completion rate stayed the same (78%) but day-7 retention dropped 40%→28%.

Create an ED diagnosis with:
- CLP/SF/EB/AR/MD-min measurements
- 3 variant hypotheses for weekly A/B test
- Telemetry event plan
- Pre-registered decision rules
- Rollback gates

Data: ./analytics/session-length-drop.csv
"""
```

**Showcase Case:**
See `docs/showcases/elliot-experience-density-report/` for a real demo ED analysis with screenshot evidence, metric horizon, and variant matrix.

### 5. Paranoia AI System Evolver

**Purpose:** Upgrade prompts, workflows, schemas, and agent rules with WOOP/VOI/OODA/evals/gates.

**Trigger:**
```
Use $paranoia-ai-system-evolver to upgrade this workflow with a WOOP Task Card, VOI, OODA, eval checks, Human Gate, and rollback.
```

**WOOP Framework:**
```yaml
woop_task_card:
  wish: "Improve concept-to-prototype validation workflow"
  outcome: "80% of concepts have testable hypotheses before prototyping"
  obstacle: "Designers skip validation planning when excited about idea"
  plan: "Add validation gate to concept architect output contract"
```

**VOI Calculation:**
```yaml
value_of_information:
  decision: "Should we add multiplayer to creature farm?"
  uncertainty_cost: "$120k dev cost × 60% failure risk = $72k"
  information_value: "1-week prototype test reduces risk to 20%"
  voi: "$72k - $24k - $8k (test cost) = $40k net value"
  recommendation: "Run test before committing to multiplayer"
```

**Example Usage:**

```python
# In your agent conversation:
"""
Use $paranoia-ai-system-evolver to improve this prompt:

Current: "Analyze this game and tell me if it's good"

Issues:
- No evidence requirement
- Vague success criteria
- No output contract

Upgrade with:
- WOOP task card
- VOI calculation for analysis depth
- OODA loop for iterative refinement
- Eval checks for evidence quality
- Human gate for final judgment
- Rollback path if analysis is off-track
"""
```

### 6. Game Design Book Translator

**Purpose:** Translate English game design texts (books, essays, chapters) to professional Chinese with reviewable terminology.

**Trigger:**
```
Use $game-design-book-translator to translate and polish this game design chapter into professional Chinese, including terminology and figure captions.
```

**Input Example:**
```markdown
# Chapter 3: The Core Loop

A game's core loop is the repeating cycle of actions that players perform most frequently.
In a shooter, this might be: aim → shoot → hit → reload.
In a strategy game: gather → build → attack → expand.

The strength of a core loop determines how engaging moment-to-moment play feels.
```

**Output Contract:**
```yaml
translation_output:
  body: |
    # 第三章：核心循环
    
    游戏的核心循环（Core Loop）是玩家最频繁执行的重复性动作周期。
    在射击游戏中，这可能是：瞄准 → 射击 → 命中 → 装填。
    在策略游戏中：收集 → 建造 → 攻击 → 扩张。
    
    核心循环的强度决定了时刻体验的参与感。
  
  terminology_glossary:
    - source: "core loop"
      target: "核心循环"
      note: "保留英文以维持专业语境"
    - source: "moment-to-moment play"
      target: "时刻体验"
      alternatives: ["逐刻玩法", "即时体验"]
```

**Example Usage:**

```python
# In your agent conversation:
"""
Use $game-design-book-translator to translate this essay:

[Paste English game design text]

Requirements:
- Professional Chinese game design terminology
- Keep key English terms in parentheses where standard
- Maintain formatting (headings, lists, emphasis)
- Create terminology glossary for review
"""
```

### 7. Game Design Source Curator

**Purpose:** Transform scattered articles, videos, creator profiles, and websites into a maintainable game design knowledge base.

**Trigger:**
```
Use $game-design-source-curator to review these game design sources and turn accepted items into a maintainable local knowledge base.
```

**Input Example:**
```yaml
sources_to_review:
  - url: "https://www.youtube.com/watch?v=example"
    type: "video"
    topic: "roguelike progression design"
  - url: "https://www.gamedeveloper.com/example-article"
    type: "article"
    topic: "player onboarding patterns"
  - creator: "Mark Brown (Game Maker's Toolkit)"
    platform: "YouTube"
```

**Output Contract:**
```yaml
knowledge_base_entry:
  id: "SOURCE-2024-001"
  title: "Roguelike Progression Design - Balancing Runs"
  type: "video"
  creator: "Game Maker's Toolkit"
  url: "https://youtube.com/watch?v=example"
  date_published: "2024-03-15"
  
  key_concepts:
    - "Meta-progression vs run-progression tension"
    - "Unlock pacing in roguelikes"
    - "Examples: Hades, Dead Cells, Slay the Spire"
  
  tags: ["roguelike", "progression", "meta-progression", "unlocks"]
  
  relevance_score: 9
  notes: "Strong examples from shipped games. Directly applicable to creature farm unlock design."
  
  citations:
    - project: "creature-farm"
      context: "Breeding unlock pacing reference"
```

**Example Usage:**

```python
# In your agent conversation:
"""
Use $game-design-source-curator to process these sources:

1. Mark Brown's video on roguelike progression (YouTube link)
2. This GDC talk on onboarding (link)
3. Derek Yu's blog posts on Spelunky design

Create knowledge base entries with:
- Key concepts extracted
- Relevance scores for my creature breeding game
- Tagging for future search
- Citation recommendations
"""
```

## Contract-Driven Workflow Chains

GameDesignOS skills pass structured contracts to enable multi-step workflows:

### Chain 1: Idea → Validated Concept → Proposal

```yaml
step_1:
  skill: game-concept-architect
  input: "One-line game idea"
  output_contract: "player_promise_contract + validation_plan"

step_2:
  skill: game-experience-analyzer
  input: "Early prototype recording + validation_plan from step 1"
  output_contract: "evidence_index + issue_cards"

step_3:
  skill: game-design-proposal-writer
  input: "player_promise_contract + evidence_index + team_constraints"
  output_contract: "decision_ready_proposal"
```

**Example:**
```python
# Step 1: Architect the concept
"""
Use $game-concept-architect:
Idea: "Reverse tower defense where you play as monsters and unlock types by failing creatively"
"""

# Step 2: Analyze prototype evidence
"""
Use $game-experience-analyzer:
Recording: ./prototypes/reverse-td-playtest-01.mp4
Validation plan: [paste from step 1]
"""

# Step 3: Write the proposal
"""
Use $game-design-proposal-writer:
Concept: [paste from step 1]
Evidence: [paste from step 2]
Team: 3 people, 12 months
Format: Internal greenlight proposal
"""
```

### Chain 2: Retention Problem → ED Diagnosis → Validated Fix

```yaml
step_1:
  skill: game-experience-analyzer
  input: "Current build recording"
  output_contract: "evidence_index with retention issues flagged"

step_2:
  skill: game-experience-density-optimizer
  input: "evidence_index + retention metrics"
  output_contract: "ed_diagnosis + weekly_experiment_plan"

step_3:
  skill: paranoia-ai-system-evolver
  input: "weekly_experiment_plan"
  output_contract: "instrumentation + decision_rules + rollback_gates"
```

## Configuration and Environment

GameDesignOS skills are self-contained Markdown packages with no external dependencies. Configuration is embedded in skill frontmatter:

```yaml
# Example: game-experience-analyzer/SKILL.md frontmatter
name: game-experience-analyzer
version: "0.6.1"
domain: game-design
method: evidence-first
contracts:
  output: evidence_index
  required_fields: [sample_boundary, timestamped_evidence, issue_cards]
```

### Environment Variables

If you extend skills with external tools (e.g., video analysis APIs), reference environment variables:

```python
# Example: hypothetical video analysis extension
import os

VIDEO_API_KEY = os.getenv("GAMEDESIGN_VIDEO_API_KEY")
if not VIDEO_API_KEY:
    print("Warning: GAMEDESIGN_VIDEO_API_KEY not set. Using manual timestamp extraction.")
```

**Do not hardcode API keys.** Always use environment variables.

## Common Patterns and Best Practices

### Pattern 1: Evidence-First Analysis

Always ground judgments in timestamped, visual, or metric evidence:

```yaml
# Good: Evidence-linked issue
issue:
  id: "ISS-042"
  observation: "Player confused about crafting UI"
  evidence:
    - type: "screenshot"
      path: "./evidence/frame-0523.png"
      timestamp: "5:23"
      note: "Player hovers over 3 buttons without clicking"
    - type: "playtest_quote"
      participant: "P07"
      quote: "I don't know which button starts crafting"

# Bad: Vague opinion
issue: "The crafting UI is confusing and needs improvement"
```

### Pattern 2: Player Promise Contract

Always define player verbs, action-goal alignment, and uncertainty sources:

```yaml
player_promise:
  core_verbs: ["explore", "collect", "combine", "discover"]
  
  action_goal_alignment:
    immediate_action: "Explore 1 room, collect 1 ingredient"
    session_goal: "Discover 2 new recipes"
    weekly_goal: "Unlock advanced crafting station"
  
  uncertainty_sources:
    - "Which ingredient combinations work?"
    - "Where are rare ingredients hidden?"
  
  validation_hypothesis: 
    "If players discover ≥2 recipes in first session, 
     60% will return next day"
```

### Pattern 3: Rollback Gates in Experiments

Every A/B test needs pre-registered rollback rules:

```yaml
experiment:
  variant: "Tutorial reduced from 8min to 3min"
  
  rollback_triggers:
    - condition: "Completion rate < 70% (vs 78% baseline)"
      sample_size: "500 users"
      action: "Revert to 8min tutorial, analyze drop-off points"
    
    - condition: "Day-7 retention < 25% (vs 28% baseline)"
      sample_size: "1000 users"
      action: "Rollback + add deferred tutorial hints"
  
  success_criteria:
    - "Day-1 retention > 35% (vs 31% baseline)"
    - "Time-to-first-action < 4min (vs 9min baseline)"
    - "Day-7 retention ≥ 28% (no regression)"
```

### Pattern 4: Human Gates for Critical Decisions

Use Human Gates before committing to large changes:

```yaml
decision_gate:
  decision: "Add multiplayer feature (12 weeks dev time)"
  
  pre_gate_requirements:
    - "VOI calculation showing >$50k net value"
    - "Prototype test with 50 users showing >70% interest"
    - "Technical feasibility audit complete"
  
  human_review_questions:
    - "Does this align with our 6-month roadmap?"
    - "Do we have server infrastructure budget?"
    - "What scope cuts needed to fit timeline?"
  
  post_gate_action:
    approved: "Proceed with multiplayer, defer creature types 6-8"
    rejected: "Focus on single-player depth, revisit in 6 months"
```

## Troubleshooting

### Skill Not Found by Agent

**Problem:** Agent says "I don't recognize the $game-experience-analyzer skill"

**Solution:**
1. Verify the skill folder is in your agent's skill directory
2. Check that `SKILL.md` exists in the root of the skill folder
3. Ensure the `name` field in YAML frontmatter matches the folder name

```bash
# Verify structure
ls -la ~/.cursor/skills/game-experience-analyzer/
# Should show: SKILL.md, references/, templates/, examples/

# Check frontmatter
head -n 5 ~/.cursor/skills/game-experience-analyzer/SKILL.md
# Should show: --- name: game-experience-analyzer ...
```

### Relative Links Broken

**Problem:** Skill references show as broken links

**Solution:** GameDesignOS skills use relative paths. Ensure you copied the entire folder structure:

```
game-experience-analyzer/
├── SKILL.md
├── references/
│   ├── hook-loop-link-surprise.md
│   └── evidence-standards.md
├── templates/
│   └── evidence-index-template.yaml
└── examples/
    └── survival-33-days-gameplay-experience-report.md
```

If you moved files, update relative links in `SKILL.md`:

```markdown
# Before (if you flattened structure)
See [Hook/Loop/Link/Surprise](./references/hook-loop-link-surprise.md)

# After (if references/ folder is missing)
See [Hook/Loop/Link/Surprise](./hook-loop-link-surprise.md)
```

### Output Missing Contract Fields

**Problem:** Skill output is prose instead of structured contract

**Solution:** Explicitly request contract format in your prompt:

```python
# Vague prompt (may produce prose)
"Analyze this game"

# Contract-requesting prompt (produces structured output)
"""
Use $game-experience-analyzer to analyze this recording.

Output format: evidence_index contract with:
- sample_boundary
- timestamped_evidence (array of timestamp/frame/observation)
- hook_loop_link_surprise (object)
- issue_cards (array with id/type/priority/evidence/fix_hypothesis)
"""
```

### Validation Plan Too Abstract

**Problem:** Validation plans say "test with users" without metrics

**Solution:** Request hypothesis + metric + success criteria:

```python
# Abstract (not actionable)
"Test if players like the breeding system"

# Concrete (actionable)
"""
Validation hypothesis:
"If players discover ≥2 breeding combinations in first 15 minutes,
 60% will return for a second session"

Metric: breeding_discoveries_per_session
Success criteria: ≥60% session-2 return rate (p<0.05, n≥100)
Instrumentation: Log 'breeding_attempt', 'breeding_success', 'discovery_moment'
"""
```

## Advanced Usage: Custom Skill Extensions

You can extend GameDesignOS skills by adding custom references or templates:

### Add a Custom Analysis Lens

Create a new reference document:

```markdown
// game-experience-analyzer/references/custom-lens-puzzle-difficulty.md

# Puzzle Difficulty Lens

## Observation Dimensions

1. **First-Attempt Success Rate**
   - Baseline: 30-40% for well-tuned puzzles
   - Evidence: Count players who solve without hints

2. **Time-to-Hint Request**
   - Baseline: 2-3 minutes optimal struggle time
   - Evidence: Log time between puzzle_start and hint_request

3. **Abandon Rate**
   - Baseline: <10% puzzle abandonment
   - Evidence: puzzle_start without puzzle_complete in 10min

## Issue Cards

If first-attempt success >70%: "Puzzle too easy, reduce clarity or add red herrings"
If time-to-hint <60s: "Puzzle unclear, improve visual communication"
If abandon rate >20%: "Puzzle too hard, add progressive hints"
```

Reference it in your prompt:

```python
"""
Use $game-experience-analyzer with custom-lens-puzzle-difficulty reference
to analyze this puzzle game recording.
"""
```

### Create a Custom Template

Add a team-specific proposal template:

```yaml
# game-design-proposal-writer/templates/custom-internal-greenlight.yaml

internal_greenlight_template:
  sections:
    - title: "One-Line Pitch"
      required: true
      max_length: "100 chars"
    
    - title: "Strategic Alignment"
      questions:
        - "Does this fit our 2-year portfolio vision?"
        - "Does this leverage our core tech/IP?"
    
    - title: "Proof of Play"
      required_evidence:
        - "Prototype playtest results (n≥20)"
        - "Key metric: session length, retention, or engagement"
    
    - title: "Resource Request"
      fields:
        - team_size
        - timeline_months
        - external_costs
    
    - title: "Risk Register"
      required_risks: ["technical", "market", "team"]
      mitigation_required: true
    
    - title: "Decision Request"
      options: ["Greenlight", "Prototype deeper", "Shelve"]
```

Use it in proposals:

```python
"""
Use $game-design-proposal-writer with custom-internal-greenlight template
to format this concept for our Q2 greenlight review.
"""
```

## Real-World Workflow Example

Here's a complete workflow from idea to validated proposal:

```python
# Day 1: Concept Generation
"""
Use $game-concept-architect:

Idea: "A city builder where buildings have personalities and relationships, 
       and you balance industrial efficiency with neighborhood harmony"

Requirements:
- Player verbs and action-goal alignment
- Player promise contract
- Core loop (3 layers)
- Scope gate for 6-month prototype
- Validation plan with testable hypothesis
"""
# Output: concept_seed.yaml, player_promise.yaml, validation_plan.yaml

# Day 2-7: Build Prototype
# [Prototype a 5-minute slice: place 3 buildings, see personality reactions]

# Day 8: Evidence Collection
"""
Use $game-experience-analyzer:

Recording: ./prototypes/city-personalities-playtest-01.mp4
Validation plan: [paste validation_plan.yaml from Day 1]

Focus on:
- First building placement (Hook)
- Personality reveal moments (Surprise)
- Does harmony mechanic create meaningful choices? (Loop)
"""
# Output: evidence_index.yaml with timestamps and issue cards

# Day 9: Retention Diagnosis
"""
Use $game-experience-density-optimizer:

Problem: First playtest showed players quit after 3 buildings (6 min average session).
Expected: 10 min session with 6-8 buildings placed.

Evidence: [paste evidence_index.yaml]

Create:
- ED diagnosis (CLP/SF/EB/AR/MD-min)
- Weekly A/B variants (3 options)
- Instrumentation plan
- Decision rules and rollback gates
"""
# Output: ed_diagnosis.yaml, weekly_experiment.yaml

# Day 10: Proposal Assembly
"""
Use $game-design-proposal-writer:

Format: Internal greenlight proposal

Inputs:
- Concept: [paste player_promise.yaml]
- Evidence: [paste evidence_index.yaml]
- ED diagnosis: [paste ed_diagnosis.yaml]
- Team: 4 people (2 eng, 1 artist, 1 designer)
- Timeline: 6 months to playable vertical slice
- Budget: Internal (no external costs)

Include:
- Proof of play section with personality mechanic validation
- Risk: Harmony mechanic may be too abstract
- Decision request: Greenlight 6-month
