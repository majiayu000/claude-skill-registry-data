---
name: memory-debugger
description: Debug TraitorSim agent memory systems including profile.md, diary entries, trust matrices (suspects.csv), and SKILL.md files. Use when troubleshooting agent behaviors, inspecting memory contents, validating memory updates, or when asked about agent memory, profile debugging, or trust matrix issues.
allowed-tools: Read, Grep, Glob
---

# Memory Debugger

Debug and inspect TraitorSim's file-system-based agent memory architecture. Each agent maintains a private directory with structured memory files that influence their decision-making. This skill helps troubleshoot memory-related issues and validate agent behaviors.

## Quick Start

```bash
# Inspect an agent's complete memory state
ls -la data/memories/player_03/

# Read agent profile
cat data/memories/player_03/profile.md

# Check trust matrix
cat data/memories/player_03/suspects.csv

# View recent diary entries
ls -t data/memories/player_03/diary/ | head -5
cat data/memories/player_03/diary/day_05_roundtable.md
```

## Memory Architecture

Each agent has a private directory structure:

```
data/memories/player_03/
├── profile.md              # Self-concept, role, personality, backstory
├── suspects.csv            # Trust Matrix (suspicion scores)
├── diary/                  # Daily event logs
│   ├── day_01_morning.md
│   ├── day_01_mission.md
│   ├── day_01_social.md
│   ├── day_01_roundtable.md
│   ├── day_01_night.md
│   └── ...
└── skills/                 # Behavioral modules (SKILL.md files)
    ├── skill-traitor-defense.md       # How to defend when accused (if Traitor)
    ├── skill-faithful-hunting.md      # How to identify Traitors (if Faithful)
    ├── skill-shield-logic.md          # When to use Shield
    ├── skill-murder-targeting.md      # Who to murder (Traitors only)
    └── skill-recruitment-decision.md  # Accept/decline recruitment
```

## What to Debug

### 1. Profile.md - Agent Self-Concept

**Contents:**
- Agent name and role (FAITHFUL or TRAITOR)
- Archetype and personality traits (OCEAN)
- Demographics and backstory
- Stats (intellect, dexterity, social_influence)
- Strategic approach

**Common issues:**

**Issue: Profile doesn't reflect persona backstory**
```bash
# Check if profile.md includes persona backstory
grep -A 10 "## Backstory" data/memories/player_03/profile.md

# Expected: Should include full backstory from persona card
# If missing: Memory manager isn't injecting backstory correctly
```

**Issue: Role is visible in profile (breaks immersion)**
```bash
# Check role section
grep "## Role" data/memories/player_03/profile.md

# Expected: Should clearly state FAITHFUL or TRAITOR
# This is correct - agents know their own role
```

**Issue: OCEAN traits not in profile**
```bash
# Check personality section
grep -A 10 "## Personality" data/memories/player_03/profile.md

# Expected: Should list all 5 OCEAN traits with values
# If missing: Player initialization didn't create profile correctly
```

### 2. Suspects.csv - Trust Matrix

**Format:**
```csv
target_id,suspicion_score,last_updated,evidence_summary
player_01,0.35,day_05,"Voted for revealed Traitor player_07"
player_02,0.72,day_05,"Failed mission despite high intellect - likely sabotage"
player_04,0.15,day_03,"Consistently votes with me, seems trustworthy"
```

**Fields:**
- `target_id`: Player being evaluated
- `suspicion_score`: 0.0 (complete trust) to 1.0 (certain Traitor)
- `last_updated`: Last day this suspicion was updated
- `evidence_summary`: Brief justification for current score

**Common issues:**

**Issue: Trust matrix not updating**
```bash
# Check if suspicion scores change over time
cat data/memories/player_03/suspects.csv

# Look for `last_updated` - should have recent days
# If all entries are "day_01", trust matrix isn't updating
```

**Issue: All suspicions are 0.5 (no differentiation)**
```bash
# Check score distribution
awk -F, '{print $2}' data/memories/player_03/suspects.csv | sort | uniq -c

# Expected: Range of scores (0.1 to 0.9)
# If all ~0.5: Agent not processing evidence
```

**Issue: Traitor has high suspicion of self**
```bash
# A Traitor shouldn't suspect fellow Traitors (knows they're allies)
grep "player_03" data/memories/player_03/suspects.csv

# Expected: Traitors should have low suspicion of each other
# If high: Traitor logic broken
```

**Issue: No evidence summaries**
```bash
# Check if evidence column is populated
awk -F, '{print $4}' data/memories/player_03/suspects.csv

# Expected: Each row should have justification
# If empty: Memory updates not recording evidence
```

### 3. Diary Entries - Event Logs

**File naming pattern:** `day_{N}_{phase}.md`

**Phases:**
- `morning`: Breakfast, murder reveal, initial reactions
- `mission`: Mission participation and observations
- `social`: Pre-Round Table conversations
- `roundtable`: Accusations, defenses, voting
- `night`: Traitor meeting, murder selection (Traitors only)

**Contents:**
- What happened this phase
- Who said/did what
- Agent's reactions and thoughts
- Updated suspicions

**Common issues:**

**Issue: Diary entries missing**
```bash
# Check if entries exist for each day/phase
ls data/memories/player_03/diary/

# Expected: 5 files per day (morning, mission, social, roundtable, night)
# If missing: Memory manager not creating entries
```

**Issue: Entries too short (< 50 words)**
```bash
# Check entry length
wc -w data/memories/player_03/diary/day_05_roundtable.md

# Expected: 100-300 words with specific observations
# If < 50 words: Agent not processing events thoroughly
```

**Issue: Entries don't reference other agents**
```bash
# Check if entries mention other players
grep -E "player_[0-9]{2}" data/memories/player_03/diary/day_05_roundtable.md

# Expected: Multiple player references with observations
# If none: Agent not tracking social dynamics
```

**Issue: Traitor night entries leak to Faithfuls**
```bash
# Traitors have night phase entries, Faithfuls don't
ls data/memories/player_03/diary/ | grep "night"

# If player_03 is Faithful and has night entries: BUG
# If player_03 is Traitor and NO night entries: Missing memory
```

### 4. Skills - Behavioral Modules

**Common skills:**

**skill-traitor-defense.md** (Traitors only):
```markdown
# Traitor Defense Strategy

When accused at Round Table:

1. **Stay calm** (leverage low Neuroticism if you have it)
2. **Deflect to evidence**: "What actual evidence do you have?"
3. **Counter-accuse** (if low Agreeableness): Point to voting records
4. **Appeal to alliance** (if high Agreeableness): "We've worked together since day 1"
5. **Bus throw if necessary**: Sacrifice fellow Traitor if suspicion > 0.8
```

**skill-faithful-hunting.md** (Faithfuls only):
```markdown
# Faithful Hunting Strategy

Identifying Traitors:

1. **Voting patterns**: Who defended revealed Traitors?
2. **Mission sabotage**: Unexplained failures with high-stat participants
3. **Breakfast tells**: Always enters last, never murdered
4. **Knowledge leaks**: Too knowledgeable about night events
5. **Shield bluffs**: Claims Shield to detect information leaks
```

**Common issues:**

**Issue: Skills not loaded for archetype**
```bash
# Check which skills exist
ls data/memories/player_03/skills/

# Expected: Should match archetype's strategic approach
# If missing: Skills weren't created during initialization
```

**Issue: Skills contradict personality**
```bash
# Read skill and compare to personality
cat data/memories/player_03/skills/skill-traitor-defense.md
cat data/memories/player_03/profile.md | grep -A 5 "## Personality"

# Example contradiction:
# Skill says: "Stay calm under pressure"
# But agent has high Neuroticism (0.85)
# Expected: Skill should account for neuroticism
```

## Instructions

### When Debugging Agent Behavior

1. **Read the agent's profile**:
   ```bash
   cat data/memories/player_{ID}/profile.md
   ```

2. **Check recent diary entries**:
   ```bash
   # Find most recent entries
   ls -t data/memories/player_{ID}/diary/ | head -5

   # Read latest roundtable
   cat data/memories/player_{ID}/diary/day_XX_roundtable.md
   ```

3. **Examine trust matrix**:
   ```bash
   cat data/memories/player_{ID}/suspects.csv
   ```

4. **Compare to expected behavior**:
   - High Extraversion → Should speak often at Round Table
   - Low Agreeableness → Should make harsh accusations
   - High Openness → Trust matrix should update frequently
   - High Conscientiousness → Mission performance should be consistent

### When Agent Makes Unexpected Decision

**Example: Agent votes for ally**

1. **Check trust matrix**:
   ```bash
   grep "player_05" data/memories/player_03/suspects.csv
   ```

   Expected: If voted for ally, suspicion should be > 0.6

2. **Check diary for context**:
   ```bash
   cat data/memories/player_03/diary/day_XX_roundtable.md | grep "player_05"
   ```

   Expected: Should explain why suspicion increased

3. **Check voting history in game log**:
   ```python
   votes = [e for e in game_log["events"]
            if e["type"] == "round_table_vote" and e["voter_id"] == "player_03"]

   # Did agent vote consistently with suspicions?
   ```

### When Trust Matrix Seems Broken

1. **Check if updates are happening**:
   ```bash
   # Look for varying last_updated days
   awk -F, '{print $3}' data/memories/player_03/suspects.csv | sort | uniq -c
   ```

2. **Validate Bayesian updates**:
   ```python
   # Read trust matrix history from game log
   updates = [e for e in game_log["events"]
              if e["type"] == "trust_matrix_update" and e["player_id"] == "player_03"]

   # Check if updates are evidence-based
   for update in updates:
       print(f"Day {update['day']}: {update['target_id']}")
       print(f"  {update['suspicion_before']:.2f} → {update['suspicion_after']:.2f}")
       print(f"  Evidence: {update['evidence']}\n")
   ```

3. **Check personality influence**:
   ```python
   player = get_player("player_03")
   openness = player["personality"]["openness"]

   # High Openness agents should update more frequently
   update_count = len(updates)
   expected_updates = openness * 10  # Heuristic

   if update_count < expected_updates:
       print("⚠️  Agent updating suspicions less than expected for Openness level")
   ```

### When Diary Entries Are Poor Quality

1. **Check entry length**:
   ```bash
   wc -w data/memories/player_03/diary/day_05_roundtable.md
   ```

2. **Check specificity**:
   ```bash
   # Should mention specific players and events
   grep -E "player_[0-9]{2}" data/memories/player_03/diary/day_05_roundtable.md
   ```

3. **Check emotional tone matches personality**:
   ```bash
   cat data/memories/player_03/diary/day_05_roundtable.md

   # High Neuroticism → Should express anxiety/defensiveness
   # High Extraversion → Should describe speaking up
   # Low Agreeableness → Should describe confrontations
   ```

## Debugging Workflows

### Workflow 1: Why Did Agent X Vote for Agent Y?

```bash
# 1. Check trust matrix
grep "player_Y" data/memories/player_X/suspects.csv

# 2. Check diary from that day
cat data/memories/player_X/diary/day_N_roundtable.md | grep "player_Y"

# 3. Check if personality influenced decision
cat data/memories/player_X/profile.md | grep -A 5 "## Personality"

# 4. Check if skills guided decision
cat data/memories/player_X/skills/skill-faithful-hunting.md
```

### Workflow 2: Why Didn't Traitor X Murder Agent Y?

```bash
# 1. Check Traitor's night diary
cat data/memories/player_X/diary/day_N_night.md

# 2. Check trust matrix for murder target prioritization
cat data/memories/player_X/suspects.csv

# Traitors typically murder low-suspicion Faithfuls (strategic)
# Or high-threat Faithfuls (protective)

# 3. Check murder targeting skill
cat data/memories/player_X/skills/skill-murder-targeting.md
```

### Workflow 3: Why Did Agent Perform Poorly in Mission?

```bash
# 1. Check stats
cat data/memories/player_X/profile.md | grep -A 3 "## Stats"

# 2. Check stress level (from game log)
# High stress reduces performance

# 3. Check if Traitor sabotaging
cat data/memories/player_X/profile.md | grep "## Role"

# If Traitor → Intentional sabotage
# If Faithful → Low stats or high stress
```

## Common Memory Issues

### Issue 1: Agent Doesn't Know Their Backstory

**Symptom:** Agent makes decisions that contradict their backstory

**Debug:**
```bash
cat data/memories/player_03/profile.md | grep -A 20 "## Backstory"
```

**Expected:** Full backstory from persona card should be present

**Fix:** Update `memory_manager.py` to inject backstory:
```python
def _create_profile(self) -> str:
    # ... existing code ...

    if self.player.backstory:
        backstory_section = f"""
## Backstory
{self.player.backstory}

## Demographics
- Age: {self.player.demographics.get('age')}
- Location: {self.player.demographics.get('location')}
- Occupation: {self.player.demographics.get('occupation')}
"""
        base_profile += backstory_section
```

### Issue 2: Trust Matrix Not Persisting

**Symptom:** Suspicion scores reset between phases

**Debug:**
```bash
# Check if CSV file is being written
ls -l data/memories/player_03/suspects.csv

# Check file permissions
stat data/memories/player_03/suspects.csv
```

**Expected:** File should update after each trust matrix change

**Fix:** Ensure `memory_manager.py` writes to CSV after updates:
```python
def update_trust_matrix(self, target_id: str, new_suspicion: float, evidence: str):
    # Update in-memory matrix
    self.trust_matrix[target_id] = {
        "suspicion": new_suspicion,
        "last_updated": self.current_day,
        "evidence": evidence
    }

    # CRITICAL: Write to file immediately
    self._write_trust_matrix_to_csv()
```

### Issue 3: Diary Entries Don't Influence Decisions

**Symptom:** Agent repeats mistakes, doesn't learn from past events

**Debug:**
```bash
# Check if agent's prompt includes diary context
# (This requires checking agent decision-making code)
```

**Expected:** Agent should query recent diary entries when making decisions

**Fix:** Ensure agent queries diary before major decisions:
```python
async def make_voting_decision(self, nominees: List[str]) -> str:
    # Load recent diary entries
    recent_entries = self._load_recent_diary_entries(days=3)

    # Include in decision prompt
    prompt = f"""
Recent observations:
{recent_entries}

Current nominees: {nominees}

Based on your memories and trust matrix, who should you vote for?
"""
```

## When to Use This Skill

Use this skill when:
- Agent makes unexpected decisions
- Trust matrix appears broken
- Diary entries are missing or poor quality
- Agent doesn't use backstory in decisions
- Skills don't match archetype
- Memory files have permission issues
- Debugging personality-behavior mismatches

## When NOT to Use This Skill

Don't use this skill for:
- Analyzing game outcomes (use game-analyzer skill)
- Generating personas (use persona-pipeline skill)
- Validating content (use world-bible-validator skill)
- Modifying game rules (use simulation-config skill)
