---
name: game-analyzer
description: Analyze TraitorSim game logs, trust matrix evolution, voting patterns, mission outcomes, and emergent social behaviors. Use when examining game results, debugging gameplay issues, analyzing agent strategies, or when asked about game analysis, trust matrices, voting patterns, or emergent behaviors.
---

# Game Analyzer

Analyze TraitorSim game logs to understand trust matrix evolution, voting patterns, mission performance, and emergent social dynamics. This skill helps debug gameplay issues, validate agent behaviors, and identify interesting strategic patterns.

## Quick Start

```python
# Analyze a completed game
from src.traitorsim.analysis.game_analyzer import GameAnalyzer

analyzer = GameAnalyzer(game_log_path="data/logs/game_2025_12_21.json")

# Get summary statistics
summary = analyzer.get_summary()
print(f"Winner: {summary['winner']}")
print(f"Days survived: {summary['days']}")
print(f"Faithfuls banished: {summary['faithfuls_banished']}")
print(f"Traitors banished: {summary['traitors_banished']}")

# Analyze trust matrix evolution
trust_evolution = analyzer.analyze_trust_evolution()
analyzer.plot_trust_evolution(player_id="player_03")

# Analyze voting patterns
voting_analysis = analyzer.analyze_voting_patterns()
print(f"Most accurate voter: {voting_analysis['most_accurate']}")
print(f"Most swayed voter: {voting_analysis['most_swayed']}")
```

## What to Analyze

### 1. Trust Matrix Evolution

**What to look for:**
- Do agents update suspicions based on evidence?
- Are Bayesian updates working correctly?
- Do high Openness agents update beliefs more readily?
- Do Traitors maintain low suspicion scores?

**Analysis:**

```python
def analyze_trust_evolution(game_log):
    """Track how each agent's trust matrix changes over time"""

    trust_history = defaultdict(list)  # player_id -> [(day, target_id, suspicion)]

    for event in game_log["events"]:
        if event["type"] == "trust_matrix_update":
            trust_history[event["player_id"]].append({
                "day": event["day"],
                "target_id": event["target_id"],
                "suspicion_before": event["suspicion_before"],
                "suspicion_after": event["suspicion_after"],
                "evidence": event["evidence"]
            })

    # Analyze patterns
    for player_id, updates in trust_history.items():
        player = get_player(player_id)

        # Check if high Openness correlates with more updates
        num_updates = len(updates)
        openness = player["personality"]["openness"]

        # Expected: High O = more updates
        print(f"{player['name']} (O={openness:.2f}): {num_updates} trust updates")

        # Check if updates are evidence-based
        for update in updates:
            delta = abs(update["suspicion_after"] - update["suspicion_before"])
            if delta > 0.2:  # Significant update
                print(f"  Day {update['day']}: {update['target_id']} "
                      f"{update['suspicion_before']:.2f} → {update['suspicion_after']:.2f}")
                print(f"  Evidence: {update['evidence']}")
```

**Visualization:**

```python
import matplotlib.pyplot as plt

def plot_trust_evolution(game_log, player_id):
    """Plot how one agent's suspicions evolve over time"""

    fig, ax = plt.subplots(figsize=(12, 6))

    # Get trust updates for this player
    updates = [e for e in game_log["events"]
               if e["type"] == "trust_matrix_update" and e["player_id"] == player_id]

    # Group by target
    by_target = defaultdict(list)
    for update in updates:
        by_target[update["target_id"]].append({
            "day": update["day"],
            "suspicion": update["suspicion_after"]
        })

    # Plot each target's suspicion over time
    for target_id, data in by_target.items():
        days = [d["day"] for d in data]
        suspicions = [d["suspicion"] for d in data]

        target = get_player(target_id)
        color = "red" if target["role"] == "TRAITOR" else "blue"
        ax.plot(days, suspicions, marker='o', label=target["name"], color=color, alpha=0.7)

    ax.set_xlabel("Day")
    ax.set_ylabel("Suspicion Score (0=trust, 1=certain traitor)")
    ax.set_title(f"Trust Evolution: {get_player(player_id)['name']}")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"analysis/trust_evolution_{player_id}.png")
    print(f"Saved to analysis/trust_evolution_{player_id}.png")
```

### 2. Voting Pattern Analysis

**What to look for:**
- Are voting blocs forming?
- Do agents vote consistently based on suspicions?
- Are Traitors coordinating votes?
- Do high Conscientiousness agents vote more consistently?

**Analysis:**

```python
def analyze_voting_patterns(game_log):
    """Analyze voting behaviors and patterns"""

    voting_history = []  # List of {day, voter, nominee, banished, was_traitor}

    for event in game_log["events"]:
        if event["type"] == "round_table_vote":
            voting_history.append({
                "day": event["day"],
                "voter": event["voter_id"],
                "nominee": event["nominee_id"],
                "banished": event.get("was_banished", False),
                "nominee_was_traitor": event.get("nominee_was_traitor", False)
            })

    # 1. Calculate voting accuracy (voted for actual Traitors)
    accuracy = defaultdict(lambda: {"correct": 0, "incorrect": 0})

    for vote in voting_history:
        if vote["banished"]:  # Only count votes for banished players
            voter = vote["voter"]
            if vote["nominee_was_traitor"]:
                accuracy[voter]["correct"] += 1
            else:
                accuracy[voter]["incorrect"] += 1

    # Most accurate voter
    most_accurate = max(accuracy.items(),
                        key=lambda x: x[1]["correct"] / (x[1]["correct"] + x[1]["incorrect"]))

    print(f"Most accurate voter: {get_player(most_accurate[0])['name']}")
    print(f"  Correct: {most_accurate[1]['correct']}, Incorrect: {most_accurate[1]['incorrect']}")

    # 2. Detect voting blocs (agents who vote together frequently)
    vote_alignment = defaultdict(int)  # (player_a, player_b) -> times voted same nominee

    for day in set(v["day"] for v in voting_history):
        day_votes = [v for v in voting_history if v["day"] == day]

        # For each pair of voters
        voters = list(set(v["voter"] for v in day_votes))
        for i, voter_a in enumerate(voters):
            for voter_b in voters[i+1:]:
                # Did they vote for the same nominee?
                nominee_a = [v["nominee"] for v in day_votes if v["voter"] == voter_a]
                nominee_b = [v["nominee"] for v in day_votes if v["voter"] == voter_b]

                if nominee_a and nominee_b and nominee_a[0] == nominee_b[0]:
                    vote_alignment[(voter_a, voter_b)] += 1

    # Top voting blocs
    top_blocs = sorted(vote_alignment.items(), key=lambda x: x[1], reverse=True)[:5]

    print("\nTop voting blocs (voted together most often):")
    for (player_a, player_b), count in top_blocs:
        print(f"  {get_player(player_a)['name']} & {get_player(player_b)['name']}: {count} times")

    # 3. Check if Traitors coordinate
    traitors = [p["id"] for p in game_log["players"] if p["role"] == "TRAITOR"]

    if len(traitors) >= 2:
        traitor_coordination = sum(
            count for (a, b), count in vote_alignment.items()
            if a in traitors and b in traitors
        )
        print(f"\nTraitor coordination: {traitor_coordination} aligned votes")

    return {
        "most_accurate": most_accurate,
        "voting_blocs": top_blocs,
        "traitor_coordination": traitor_coordination if len(traitors) >= 2 else 0
    }
```

### 3. Mission Performance Analysis

**What to look for:**
- Do mission outcomes correlate with agent stats?
- Are Traitors sabotaging effectively?
- Can we detect sabotage vs. genuine failure?

**Analysis:**

```python
def analyze_mission_performance(game_log):
    """Analyze mission outcomes and detect sabotage patterns"""

    missions = [e for e in game_log["events"] if e["type"] == "mission_result"]

    for mission in missions:
        print(f"\nDay {mission['day']}: {mission['mission_name']}")
        print(f"Outcome: {'✅ SUCCESS' if mission['success'] else '❌ FAILURE'}")
        print(f"Prize pot: £{mission['prize_pot_change']:+,}")

        # Analyze participants
        participants = mission["participants"]

        # Calculate expected success rate
        expected_success_rate = 0
        for participant in participants:
            player = get_player(participant["player_id"])
            stat_name = mission["primary_stat"]  # e.g., "intellect"
            stat_value = player["stats"][stat_name]

            # Success probability = stat - stress - personality_modifier
            stress = participant.get("stress", 0)
            prob = max(0, min(1, stat_value - stress))
            expected_success_rate += prob / len(participants)

        print(f"Expected success rate: {expected_success_rate:.1%}")

        # Detect sabotage
        if not mission["success"] and expected_success_rate > 0.7:
            print("⚠️  Likely sabotage (high expected success but failed)")

            # Who sabotaged?
            saboteurs = []
            for participant in participants:
                player = get_player(participant["player_id"])
                if player["role"] == "TRAITOR":
                    saboteurs.append(player["name"])

            if saboteurs:
                print(f"Traitors present: {', '.join(saboteurs)}")

        # Check if failure was due to low stats
        elif not mission["success"]:
            low_performers = [
                get_player(p["player_id"])["name"]
                for p in participants
                if get_player(p["player_id"])["stats"][mission["primary_stat"]] < 0.5
            ]

            if low_performers:
                print(f"Low performers: {', '.join(low_performers)}")
```

### 4. Personality-Behavior Correlation

**What to look for:**
- Do high Extraversion agents dominate Round Tables?
- Do low Agreeableness agents make more accusations?
- Do personality traits correlate with survival?

**Analysis:**

```python
def analyze_personality_behavior(game_log):
    """Correlate personality traits with behaviors"""

    import numpy as np
    from scipy.stats import pearsonr

    players = game_log["players"]

    # 1. Extraversion vs. Round Table participation
    extraversion_scores = []
    speaking_counts = []

    for player in players:
        extraversion = player["personality"]["extraversion"]
        extraversion_scores.append(extraversion)

        # Count how many times they spoke at Round Table
        speaking_count = len([
            e for e in game_log["events"]
            if e["type"] == "round_table_statement" and e["player_id"] == player["id"]
        ])
        speaking_counts.append(speaking_count)

    correlation, p_value = pearsonr(extraversion_scores, speaking_counts)
    print(f"Extraversion vs. Speaking: r={correlation:.3f}, p={p_value:.3f}")

    # 2. Agreeableness vs. Accusations
    agreeableness_scores = []
    accusation_counts = []

    for player in players:
        agreeableness = player["personality"]["agreeableness"]
        agreeableness_scores.append(agreeableness)

        # Count accusations made
        accusation_count = len([
            e for e in game_log["events"]
            if e["type"] == "accusation" and e["accuser_id"] == player["id"]
        ])
        accusation_counts.append(accusation_count)

    correlation, p_value = pearsonr(agreeableness_scores, accusation_counts)
    print(f"Agreeableness vs. Accusations: r={correlation:.3f}, p={p_value:.3f}")
    print(f"Expected: Negative correlation (low A = more accusations)")

    # 3. Neuroticism vs. Survival
    neuroticism_scores = []
    survival_days = []

    for player in players:
        neuroticism = player["personality"]["neuroticism"]
        neuroticism_scores.append(neuroticism)

        # Find when eliminated
        elimination = next((
            e for e in game_log["events"]
            if e["type"] in ["banishment", "murder"] and e["victim_id"] == player["id"]
        ), None)

        survival_days.append(elimination["day"] if elimination else game_log["final_day"])

    correlation, p_value = pearsonr(neuroticism_scores, survival_days)
    print(f"Neuroticism vs. Survival: r={correlation:.3f}, p={p_value:.3f}")
```

### 5. Emergent Behavior Detection

**What to look for:**
- Unexpected alliances forming
- "Bus throwing" (Traitors betraying each other)
- "Shield bluffing" (false Shield claims)
- Alliance betrayals

**Analysis:**

```python
def detect_emergent_behaviors(game_log):
    """Identify interesting emergent patterns"""

    # 1. Detect "Bus Throwing" (Traitor voting for Traitor)
    traitors = [p["id"] for p in game_log["players"] if p["role"] == "TRAITOR"]

    bus_throws = []
    for event in game_log["events"]:
        if event["type"] == "round_table_vote":
            if event["voter_id"] in traitors and event["nominee_id"] in traitors:
                bus_throws.append({
                    "day": event["day"],
                    "thrower": get_player(event["voter_id"])["name"],
                    "thrown": get_player(event["nominee_id"])["name"],
                    "was_banished": event.get("was_banished", False)
                })

    if bus_throws:
        print("🚌 Bus Throwing Detected:")
        for bt in bus_throws:
            status = "BANISHED" if bt["was_banished"] else "survived"
            print(f"  Day {bt['day']}: {bt['thrower']} voted for {bt['thrown']} ({status})")

    # 2. Detect Shield Bluffs
    shield_claims = [e for e in game_log["events"] if e["type"] == "shield_claim"]
    actual_shields = [e for e in game_log["events"] if e["type"] == "shield_used"]

    bluffs = []
    for claim in shield_claims:
        # Check if shield was actually used by this player
        actual = any(s["player_id"] == claim["player_id"] for s in actual_shields)
        if not actual:
            bluffs.append({
                "day": claim["day"],
                "bluffer": get_player(claim["player_id"])["name"]
            })

    if bluffs:
        print("\n🛡️  Shield Bluffs Detected:")
        for bluff in bluffs:
            print(f"  Day {bluff['day']}: {bluff['bluffer']} falsely claimed Shield")

    # 3. Detect Unlikely Alliances (high suspicion but still voting together)
    for day in range(1, game_log["final_day"] + 1):
        day_votes = [e for e in game_log["events"]
                     if e["type"] == "round_table_vote" and e["day"] == day]

        # Find players who voted for same nominee despite high mutual suspicion
        # (Would need trust matrix data)
```

## Instructions

### When Analyzing a Game

1. **Load game log**:
   ```python
   import json
   with open("data/logs/game_2025_12_21.json") as f:
       game_log = json.load(f)
   ```

2. **Run all analyses**:
   ```python
   from src.traitorsim.analysis.game_analyzer import GameAnalyzer

   analyzer = GameAnalyzer(game_log)
   analyzer.run_all_analyses()
   ```

3. **Generate report**:
   ```python
   analyzer.generate_report(output_path="analysis/game_report.md")
   ```

### When Debugging Agent Behavior

1. **Focus on specific agent**:
   ```python
   agent_analysis = analyzer.analyze_agent(player_id="player_03")
   ```

2. **Check expected behavior**:
   - High O agents should update trust frequently
   - High E agents should speak more at Round Table
   - Low A agents should make more accusations
   - High C agents should perform better in missions

3. **Identify anomalies**:
   - Traitors maintaining perfect cover
   - Faithfuls with no trust updates
   - Agents not using their archetype advantages

## Common Analysis Patterns

### Pattern 1: Why Did X Win?

```python
winner = game_log["winner"]
winner_analysis = analyzer.analyze_agent(winner["id"])

# Check strategic decisions
print(f"Voting accuracy: {winner_analysis['voting_accuracy']}")
print(f"Mission performance: {winner_analysis['mission_success_rate']}")
print(f"Alliances formed: {winner_analysis['alliances']}")
print(f"Times targeted: {winner_analysis['times_nominated']}")
```

### Pattern 2: Why Did Traitors Lose?

```python
traitors = [p for p in game_log["players"] if p["role"] == "TRAITOR"]

for traitor in traitors:
    analysis = analyzer.analyze_agent(traitor["id"])

    # Check if they were detected
    if traitor["id"] in game_log["banishments"]:
        print(f"{traitor['name']} was banished on day {analysis['banished_day']}")
        print(f"  Voting patterns: {analysis['voting_consistency']}")
        print(f"  Mission sabotages: {analysis['sabotage_count']}")
        print(f"  Suspicion level at banishment: {analysis['average_suspicion']}")
```

### Pattern 3: Most Interesting Moment

```python
# Find days with most dramatic events
drama_scores = []

for day in range(1, game_log["final_day"] + 1):
    day_events = [e for e in game_log["events"] if e["day"] == day]

    drama_score = (
        len([e for e in day_events if e["type"] == "banishment"]) * 10 +
        len([e for e in day_events if e["type"] == "recruitment"]) * 15 +
        len([e for e in day_events if e["type"] == "shield_used"]) * 8 +
        len([e for e in day_events if e["type"] == "mission_result" and not e["success"]]) * 5
    )

    drama_scores.append((day, drama_score))

most_dramatic = max(drama_scores, key=lambda x: x[1])
print(f"Most dramatic day: Day {most_dramatic[0]} (score: {most_dramatic[1]})")
```

## When to Use This Skill

Use this skill when:
- Analyzing completed games to understand outcomes
- Debugging agent behavior issues
- Validating personality-behavior correlations
- Identifying interesting emergent patterns
- Generating game reports and highlights
- Comparing different game configurations

## When NOT to Use This Skill

Don't use this skill for:
- Real-time game state monitoring (use game engine directly)
- Generating personas (use persona-pipeline skill)
- Validating content (use world-bible-validator skill)
- Managing memory systems (use memory-debugger skill)
