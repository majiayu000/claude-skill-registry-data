---
name: himap-travel
title: "HiMAP-Travel: Hierarchical Multi-Agent Planning for Long-Horizon Constrained Travel"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2603.04750"
keywords: [Agent Planning, Long-horizon Tasks, Constraint Management, Multi-agent Coordination, Tool Use]
description: "Solves long-horizon planning problems with global constraints by decoupling planning into strategic (resource allocation) and tactical (execution) levels. Prevents constraint drift through synchronized state tracking and cooperative bargaining."
---

# HiMAP-Travel: Preventing Constraint Drift in Multi-Day Planning Through Hierarchical Decomposition

Long-horizon planning with LLM agents fails when maintaining global constraints across many steps. As planning progresses and intermediate outputs accumulate in context, the model's attention to initial constraints diminishes—budget allocations drift, resource conflicts emerge, and logical inconsistencies cascade. This constraint drift is invisible until terminal failure, making multi-day itinerary generation particularly brittle.

HiMAP-Travel solves this through hierarchical decomposition: a strategic coordinator allocates resources across planning horizons while tactical executors operate independently on sub-problems. This limits effective context length per executor and forces explicit constraint tracking through synchronized state, preventing attention drift.

## Core Concept

Decompose long-horizon planning (e.g., 7-day trip) into two levels:

1. **Strategic Coordinator**: Allocates global resources (total budget, required destinations, daily allocations) and monitors constraint compliance atomically
2. **Tactical Executors**: Day-level planners work in isolation with bounded context, receiving daily budgets and constraints as clear inputs

The coordinator acts as a transaction monitor: executors propose plans, the coordinator validates against global state, and if infeasible, triggers resource reallocation rather than regeneration.

## Architecture Overview

- **Coordinator Module**: Maintains global state (Σ), validates constraint compliance, handles resource reallocation
- **Executor Modules**: Specialized day-planners receiving daily context windows with isolated state
- **Synchronized Global State (Σ)**: Tracks budget, visited venues (fuzzy-matched), transportation modes, time constraints
- **Checkpoint/Rollback Protocol**: Executors can retry with adjusted allocations without regenerating entire sub-plans
- **Unified Policy Network**: Single GRPO-trained model π_θ with role-conditioned prompts for both coordinator and executor roles

## Implementation Steps

Create a hierarchical planning system with explicit state synchronization. The coordinator routes between executors and maintains consistency.

**Coordinator State Management**

Track global constraints and validate executor proposals:

```python
# Global state maintained by coordinator
class GlobalPlanningState:
    def __init__(self, total_budget, num_days, required_venues, constraints):
        self.total_budget = total_budget
        self.num_days = num_days
        self.remaining_budget = total_budget
        self.required_venues = set(required_venues)
        self.visited_venues = set()
        self.day_allocations = {}  # day -> allocated budget
        self.transportation_modes = []  # track consistency
        self.violated_constraints = []

    def allocate_budget_to_day(self, day, amount):
        """Allocate daily budget from global pool"""
        if self.remaining_budget < amount:
            raise InfeasibleAllocation(f"Insufficient budget: {amount} > {self.remaining_budget}")
        self.remaining_budget -= amount
        self.day_allocations[day] = amount

    def validate_venue_addition(self, venue_name):
        """Check if venue can be added without duplication"""
        # Fuzzy match against visited venues
        matched = fuzzy_match_venue(venue_name, self.visited_venues, threshold=0.85)
        if matched:
            return False, f"Venue '{venue_name}' already visited (matched: {matched})"
        return True, None

    def validate_executor_output(self, day, plan_dict):
        """Validate day-level plan against global constraints"""
        issues = []
        venues_in_plan = plan_dict.get('venues', [])
        daily_cost = plan_dict.get('total_cost', 0)

        # Check budget
        if daily_cost > self.day_allocations.get(day, 0):
            issues.append(f"Daily cost {daily_cost} exceeds allocation {self.day_allocations[day]}")

        # Check venue duplication
        for venue in venues_in_plan:
            valid, reason = self.validate_venue_addition(venue)
            if not valid:
                issues.append(reason)
            else:
                self.visited_venues.add(venue)

        # Check transportation consistency
        transport = plan_dict.get('transport_mode')
        if transport and self.transportation_modes and transport != self.transportation_modes[-1]:
            issues.append(f"Transport mode change {self.transportation_modes[-1]} -> {transport}")

        return len(issues) == 0, issues
```

**Coordinator-Executor Communication**

The coordinator orchestrates planning rounds and handles infeasibility:

```python
def hierarchical_planning_loop(coordinator_model, executor_models, global_state, num_days):
    """
    coordinator_model: LLM trained to allocate resources
    executor_models: day-level planners (can be same model with different prompts)
    global_state: GlobalPlanningState instance
    num_days: total planning horizon
    """
    all_daily_plans = []

    for day in range(1, num_days + 1):
        # Step 1: Coordinator decides daily budget allocation
        coordinator_prompt = f"""
        You are a travel budget coordinator. Total budget: ${global_state.total_budget}
        Remaining: ${global_state.remaining_budget}
        Days remaining: {num_days - day + 1}
        Required venues not yet visited: {global_state.required_venues - global_state.visited_venues}

        Allocate budget for day {day}. Return JSON: {{"daily_budget": <number>, "day_notes": "<strategy>"}}
        """

        coord_response = coordinator_model.generate(coordinator_prompt)
        daily_budget = json.loads(coord_response)['daily_budget']

        # Allocate globally
        global_state.allocate_budget_to_day(day, daily_budget)

        # Step 2: Executor plans for this day
        executor_prompt = f"""
        You are a travel executor planning day {day}/{num_days}.
        Daily budget: ${daily_budget}
        Required venues to eventually visit: {global_state.required_venues - global_state.visited_venues}
        Previously visited: {list(global_state.visited_venues)}

        Generate a detailed itinerary for today. Return JSON: {{"venues": [...], "total_cost": <number>, "transport_mode": "<mode>"}}
        """

        max_retries = 3
        for attempt in range(max_retries):
            executor_response = executor_models[day].generate(executor_prompt)
            day_plan = json.loads(executor_response)

            # Validate against global state
            valid, issues = global_state.validate_executor_output(day, day_plan)

            if valid:
                all_daily_plans.append(day_plan)
                break
            else:
                if attempt < max_retries - 1:
                    # Replan with constraint feedback
                    executor_prompt += f"\n\nConstraint violations: {', '.join(issues)}\nRevise plan to fix these issues."
                else:
                    # Coordinator re-allocates resources
                    coordinator_prompt += f"\nDay {day} executor failed: {issues}. Re-allocate resources."
                    coord_response = coordinator_model.generate(coordinator_prompt)
                    new_budget = json.loads(coord_response)['daily_budget']
                    global_state.day_allocations[day] = new_budget
                    executor_prompt = executor_prompt.replace(f"${daily_budget}", f"${new_budget}")

    return all_daily_plans
```

**Executor Role-Conditioned Inference**

Use the same model for both coordinator and executor via system prompt conditioning:

```python
def get_system_prompt(role, context):
    """Role-conditioned system prompts for unified policy"""
    if role == "coordinator":
        return """You are a strategic travel budget coordinator. Your job is to allocate
        global resources across the planning horizon while respecting constraints. Think
        systemically about resource distribution and constraint satisfaction."""

    elif role == "executor":
        return """You are a tactical travel planner executing a single day of an itinerary.
        You have a daily budget and must select venues and routes that fit within constraints.
        Propose detailed, feasible daily plans."""

    return ""
```

## Practical Guidance

**Hyperparameters**:
- Daily planning window: 2-4 venues per day works well; more causes executor context overflow
- Budget allocation strategy: Give coordinator 10-20% discretionary budget for reallocation
- Fuzzy match threshold for venues: 0.85 (0.8-0.9 range is robust)
- Max executor retries: 2-3 before coordinator re-allocates

**When to Apply**:
- Multi-day/multi-step planning with hard constraints (budget, resource limits, required checkpoints)
- Tasks where constraint drift accumulates (travel, project management, procurement)
- Problems where context length is a bottleneck (100+ intermediate steps)

**When NOT to Apply**:
- Single-horizon problems (one-shot planning without constraint accumulation)
- Tasks with very loose constraints that drift doesn't matter
- Scenarios where constraint conflicts need dynamic negotiation rather than reallocation

**Key Pitfalls**:
- Executor context windows too large—defeats purpose of hierarchical decomposition
- Coordinator prompts too vague—allocations become inconsistent; use explicit JSON schemas
- Not tracking constraint violations during executor failures—cascading failures result
- Fuzzy matching threshold too low—allows duplicate venues; too high—rejects valid alternatives

**Integration Notes**: Works as a planning wrapper around any LLM; requires structured JSON output from both coordinator and executors; rollback mechanism needs version control of global state.

**Evidence**: Achieves 52.65% final pass rate on TravelPlanner benchmark (+8.67pp over sequential baselines); provides 2.63x speedup through executor parallelization; maintains constraint satisfaction across 7-day itineraries with >95% global consistency.

Reference: https://arxiv.org/abs/2603.04750
