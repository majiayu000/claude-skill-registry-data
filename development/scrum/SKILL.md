---
name: Scrum
description: Agile project management framework for iterative software development with sprints, roles, and ceremonies
license: MIT
compatibility:
  - Python
  - JavaScript
  - Java
  - Go
  - All Agile Teams
audience: Software Developers, Product Owners, Scrum Masters
category: software-development
---

# Scrum

## What I Do

I provide comprehensive guidance on implementing Scrum, the most popular Agile framework for managing complex software projects. Scrum structures work into time-boxed iterations called sprints (typically 2-4 weeks), enabling teams to deliver working software incrementally while continuously inspectinG and adapting their process. I cover all Scrum artifacts, events, and roles, helping teams transition from traditional waterfall methodologies to iterative, incremental development that embraces change and maximizes value delivery.

## When to Use Me

Use Scrum when your software project has uncertain or evolving requirements, requires frequent feedback loops, needs to deliver value incrementally, or involves complex problem-solving where upfront planning is difficult. Scrum is ideal for startups building new products, enterprise teams modernizing legacy systems, and any development effort where customer needs might change during development. Avoid Scrum for very small, well-defined projects with fixed requirements where the overhead of Scrum ceremonies would outweigh the benefits.

## Core Concepts

- **Sprints**: Time-boxed iterations (usually 2-4 weeks) where a potentially releasable increment is created
- **Product Backlog**: Prioritized list of features, bugs, and improvements maintained by the Product Owner
- **Sprint Backlog**: Subset of the Product Backlog that the team commits to completing during a sprint
- **Scrum Roles**: Product Owner (value maximization), Scrum Master (process facilitation), Development Team (cross-functional builders)
- **Sprint Planning**: Meeting at sprint start to determine what can be delivered and how it will be achieved
- **Daily Standup**: 15-minute daily sync where team members share progress, plans, and blockers
- **Sprint Review**: Demo of completed work to stakeholders for feedback collection
- **Sprint Retrospective**: Team reflection meeting to identify and implement process improvements
- **Definition of Done**: Shared understanding of criteria that must be met for work to be considered complete
- **Velocity**: Historical measure of work completed per sprint used for capacity planning

## Code Examples

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum

class StoryPointEstimate(Enum):
    """Fibonacci-like story point scale for effort estimation"""
    ONE = 1
    TWO = 2
    THREE = 3
    FIVE = 5
    EIGHT = 8
    THIRTEEN = 13
    TWENTY_ONE = 21

@dataclass
class UserStory:
    """Represents a user story in the Product Backlog"""
    id: str
    title: str
    description: str
    priority: int  # 1 = highest priority
    story_points: Optional[StoryPointEstimate]
    acceptance_criteria: List[str]
    status: str = "TODO"
    assignee: Optional[str] = None

    def meets_definition_of_done(self) -> bool:
        """Check if all acceptance criteria are met"""
        return all(criterion.startswith("[x]") for criterion in self.acceptance_criteria)

@dataclass
class Sprint:
    """Represents a Scrum sprint with time-boxed duration"""
    name: str
    start_date: datetime
    end_date: datetime
    goals: List[str]
    backlog: List[UserStory]

    def days_remaining(self) -> int:
        """Calculate remaining days in the sprint"""
        delta = self.end_date - datetime.now()
        return max(0, delta.days)

    def completion_percentage(self) -> float:
        """Calculate sprint completion based on story points"""
        total_points = sum(s.story_points.value for s in self.backlog if s.story_points)
        completed_points = sum(
            s.story_points.value for s in self.backlog
            if s.story_points and s.status == "DONE"
        )
        return (completed_points / total_points * 100) if total_points > 0 else 0.0

class ScrumTeam:
    """Manages Scrum team composition and capacity"""
    def __init__(
        self,
        name: str,
        product_owner: str,
        scrum_master: str,
        developers: List[str]
    ):
        self.name = name
        self.product_owner = product_owner
        self.scrum_master = scrum_master
        self.developers = developers
        self.velocity_history: List[float] = []

    def calculate_capacity(self, sprint_days: int, holidays: int = 0) -> int:
        """Calculate available story points for next sprint"""
        developers_count = len(self.developers)
        hours_per_day = 6  # Account for meetings, slack
        hours_per_point = 4  # Average hours per story point
        available_days = sprint_days - holidays
        return developers_count * available_days * hours_per_day // hours_per_point

    def record_velocity(self, completed_points: float) -> None:
        """Record sprint velocity for future capacity planning"""
        self.velocity_history.append(completed_points)

    def average_velocity(self, last_n_sprints: int = 3) -> float:
        """Calculate average velocity from recent sprints"""
        recent = self.velocity_history[-last_n_sprints:]
        return sum(recent) / len(recent) if recent else 0.0

# Example usage demonstrating sprint planning workflow
def plan_sprint(
    product_backlog: List[UserStory],
    team: ScrumTeam,
    sprint_duration_days: int
) -> Sprint:
    """Plan a new sprint based on backlog priority and team velocity"""
    avg_velocity = team.average_velocity()
    capacity = team.calculate_capacity(sprint_duration_days)
    
    selected_stories = []
    remaining_capacity = capacity
    
    for story in sorted(product_backlog, key=lambda s: s.priority):
        if story.story_points and remaining_capacity >= story.story_points.value:
            selected_stories.append(story)
            remaining_capacity -= story.story_points.value
    
    sprint = Sprint(
        name=f"Sprint {len(team.velocity_history) + 1}",
        start_date=datetime.now(),
        end_date=datetime.now(),
        goals=["Complete selected user stories", "Address technical debt"],
        backlog=selected_stories
    )
    
    print(f"Planned sprint with {len(selected_stories)} stories")
    print(f"Estimated velocity: {sum(s.story_points.value for s in selected_stories if s.story_points)} points")
    print(f"Team capacity: {capacity} points")
    
    return sprint
```

```python
class DailyStandup:
    """Manages daily scrum meeting tracking and blocker resolution"""
    def __init__(self, team_members: List[str]):
        self.team_members = team_members
        self.standup_log: List[dict] = []

    def conduct_standup(
        self,
        date: datetime,
        updates: dict
    ) -> List[str]:
        """Conduct daily standup and identify blockers"""
        blockers = []
        
        for member in self.team_members:
            if member in updates:
                update = updates[member]
                self.standup_log.append({
                    "member": member,
                    "date": date,
                    "yesterday": update.get("completed", []),
                    "today": update.get("planned", []),
                    "blocker": update.get("blocker", None)
                })
                
                if update.get("blocker"):
                    blockers.append((member, update["blocker"]))
        
        return blockers

    def escalate_blockers(self, blockers: List[tuple]) -> None:
        """Raise blockers to Scrum Master attention"""
        for member, blocker in blockers:
            print(f"ESCALATION: {member} blocked by '{blocker}'")
```

```python
class SprintRetrospective:
    """Facilitates sprint retrospective for continuous improvement"""
    def __init__(self, team: ScrumTeam):
        self.team = team
        self.feedback_items: List[dict] = []

    def add_feedback(
        self,
        category: str,
        what_went_well: str,
        what_to_improve: str,
        action_item: str
    ) -> None:
        """Add retrospective feedback item"""
        self.feedback_items.append({
            "category": category,
            "well": what_went_well,
            "improve": what_to_improve,
            "action": action_item,
            "owner": None,
            "completed": False
        })

    def generate_improvement_plan(self) -> List[dict]:
        """Generate prioritized improvement actions"""
        actions = [
            item for item in self.feedback_items
            if item["action"] and not item["completed"]
        ]
        return sorted(actions, key=lambda x: x["category"])
```

## Best Practices

- Keep sprints at consistent 2-week intervals to establish reliable rhythm and predictability
- Product Owner should maintain a refined, prioritized backlog with clear acceptance criteria
- Daily standups must be time-boxed to 15 minutes with standing to maintain urgency
- Sprint Review should include real working software demonstrations, not status reports
- Retrospectives must result in actionable improvement items with assigned owners
- Story points should estimate complexity, not hours, and remain consistent across the team
- Definition of Done should be enforced strictly to ensure quality and technical debt control
- Avoid scope creep during sprint by strictly managing sprint backlog changes
- Velocity should be used for capacity planning, not as a performance metric
- Technical debt should be explicitly included in each sprint, typically 10-20% of capacity

## Common Patterns

- ** backlog Refinement**: Regular grooming sessions (weekly) to prepare high-priority stories for upcoming sprints
- **Burndown Charts**: Visual tracking of remaining work versus time to identify early warning signs
- **Estimation Poker**: Team-based story point estimation using planning poker for better accuracy
- **Scrum of Scrums**: Scaling pattern for multiple teams coordinating on shared objectives
- **Feature Teams**: Cross-functional teams organized around features rather than components
