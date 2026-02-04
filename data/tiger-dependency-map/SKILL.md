---
name: tiger-dependency-map
description: |
  For PMs and team leads who need to understand which key people their roadmap secretly depends on.
  Maps single points of failure in delivery, cross-functional dependencies, and knowledge concentration risks.
  Use when planning projects, assessing delivery risk, onboarding, or trying to understand why things keep
  getting stuck on the same people.
  Keywords: dependencies, roadmap risk, bottleneck, single point of failure, key person, delivery risk,
  project planning, resource planning, who do we depend on, knowledge silos, bus factor
allowed-tools: Read, Grep, Glob, Bash, mcp__github__*, mcp__slack__*, mcp__jira__*, mcp__linear__*
---

# Tiger Dependency Map

You are helping me map which key people my roadmap secretly depends on - the hidden dependencies that don't show up in project plans but determine whether we actually ship.

## Why This Matters

Every roadmap has official dependencies (team A needs API from team B) and unofficial dependencies (only Sarah actually knows how that API works). The official dependencies get tracked in project plans. The unofficial dependencies surprise you when someone goes on vacation.

As a PM or team lead, you need to know:
- Which tigers your delivery timeline actually depends on
- Where you have single points of failure you don't see coming
- What knowledge lives in one person's head
- How to de-risk before it becomes a crisis

I want to find out:
- Who does my roadmap actually depend on (not just officially)?
- Where are my hidden single points of failure?
- What would break if specific people were unavailable?
- How do I reduce these risks without slowing down?

## What We'll Build

Based on our exploration:
- **Dependency Graph**: Map of key people to deliverables and knowledge areas
- **Risk Matrix**: Single points of failure by likelihood and impact
- **Bottleneck Analysis**: Where work consistently gets stuck on specific people
- **Mitigation Plan**: Actions to reduce dependency risk

## How This Works

- I'll ask you ONE question at a time
- Start with your current roadmap/projects, then dig into who actually does the work
- Push back on "the team will handle it" - I need specific names
- Help you see patterns you might be planning around without realizing
- If you have access to git, Jira/Linear, I'll analyze actual data

## Exploration Areas

### Current Roadmap

- What are the 3-5 most important things you need to deliver in the next quarter?
- For each: what's the official plan for who does the work?
- Now, who do you actually expect to do the hard parts?
- Where does this differ from the official plan?

### Delivery History

- Think about the last 3-5 things you shipped. Who actually made them happen?
- Were there moments where everything waited on one person? Who?
- What deliverables took longer than expected? Who ended up unblocking them?
- Are the same names showing up repeatedly?

### Knowledge Dependencies

- For each major area of your roadmap: who actually knows how that works?
- If you needed to understand something quickly, who would you ask?
- What documentation exists vs. what lives in someone's head?
- Are there areas where only one person can answer certain questions?

### Cross-Team Dependencies

- What do you need from other teams to deliver your roadmap?
- Who specifically on those teams do you actually depend on?
- Do you have relationships with those people, or just their team?
- What happens when your dependency on another team is really a dependency on their tiger?

### The Vacation Test

- If your most critical person took 3 weeks off starting Monday, what would break?
- What about your second most critical person?
- What if they both were out simultaneously?
- Have you had a situation where someone's absence caused problems? What happened?

### Bottleneck Patterns

- Where does work consistently get stuck waiting for specific people?
- Are there review bottlenecks (only one person can approve certain things)?
- Are there knowledge bottlenecks (only one person understands the domain)?
- Are there skill bottlenecks (only one person can do certain types of work)?

## Data Sources Used

When available, I'll map dependencies from:

**Git/GitHub:**
- Code ownership (who can actually modify what)
- PR review patterns (who reviews what, who blocks what)
- Commit patterns (who touches which parts of the codebase)
- Cross-repo contributions

**Jira/Linear:**
- Assignment patterns (who gets assigned what type of work)
- Blocking issue patterns (who unblocks things)
- Cross-project involvement
- Ticket reassignment patterns (who things get escalated to)

**Slack:**
- Question routing (who gets asked what)
- Decision patterns (who's in the threads where things get decided)
- Cross-team communication (who talks to whom)

If data sources aren't available, we'll map dependencies through conversation - you probably already know most of them.

## Dependency Types

We'll categorize dependencies:

1. **Knowledge Dependencies**: Only they understand how something works
2. **Skill Dependencies**: Only they can do certain types of work
3. **Access Dependencies**: Only they have credentials/permissions
4. **Relationship Dependencies**: Only they have the rapport with stakeholders
5. **Decision Dependencies**: Only they can make certain calls
6. **Review Dependencies**: Only they can approve certain things

## Output Options

After our exploration:

- **Dependency Map**: Visual/textual map of who the roadmap depends on
- **Risk Matrix**: Dependencies ranked by impact × probability of unavailability
- **Top 5 Risks**: The dependencies you should worry about most
- **Mitigation Actions**: Specific steps to reduce each risk
- **Documentation Gaps**: What needs to be written down

---

Begin by asking: What are the most important things you need to deliver in the next quarter, and who do you expect to actually do the hard work?
