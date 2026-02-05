---
name: feature-discovery
description: Conduct feature discovery and planning for new game features. Use when designing new features, planning implementations, analyzing requirements, breaking down complex features into tasks, or conducting feasibility studies for the TripleDerby racing game.
---

# Feature Discovery and Planning

## Overview
This skill guides systematic feature discovery and planning to ensure requirements are well-understood before implementation begins. It's specifically designed for planning game features in the TripleDerby horse racing simulation.

## When to Use
- Planning a new game feature or capability
- Analyzing feature requirements and scope
- Breaking down complex features into implementable tasks
- Conducting feasibility studies for new mechanics
- Designing game systems (race mechanics, betting, training, etc.)
- Scope planning for development iterations

## Instructions

### Phase 1: Discovery
1. **Gather Context**: Ask clarifying questions about feature goals, user experience, and game design intent
2. **Identify Requirements**: Document what the feature must do (functional requirements)
3. **Explore Constraints**: Understand technical, gameplay, and performance constraints
4. **Map Use Cases**: Identify player interactions and game scenarios
5. **Review Codebase**: Examine existing patterns and systems that may be affected or leveraged

### Phase 2: Technical Analysis
1. **Evaluate Feasibility**: Assess technical viability within the current architecture
2. **Identify Dependencies**: Map relationships to existing systems (Race, Horse, Betting, etc.)
3. **Review Data Model**: Consider database schema changes needed
4. **Assess Integration Points**: Identify where new code connects to existing systems
5. **Consider Performance**: Evaluate impact on race simulation, UI responsiveness, etc.
6. **Security & Validation**: Identify data validation and security requirements

### Phase 3: Planning
1. **Break Down Tasks**: Decompose the feature into concrete, implementable tasks
2. **Sequence Work**: Identify logical implementation phases and dependencies
3. **Estimate Complexity**: Note particularly complex or risky areas
4. **Create Task List**: Use TodoWrite to create a structured task breakdown
5. **Define Milestones**: Identify testable checkpoints and deliverables

### Phase 4: Documentation
1. **Write Specification**: Create clear feature requirements document
2. **Document Assumptions**: Record decisions and assumptions made during planning
3. **Define Success Criteria**: Establish how to validate the feature works correctly
4. **Create Implementation Plan**: Write step-by-step implementation approach
5. **Reference Templates**: Use PLANNING_TEMPLATE.md and DISCOVERY_CHECKLIST.md

## Examples

### Example 1: New Game System
**User**: "I want to add a horse training system where players can improve their horses' stats over time"

**Claude will**:
- Ask about training mechanics (time-based? resource-based? mini-games?)
- Explore stat progression (linear? diminishing returns? caps?)
- Review existing Horse entity and stats structure
- Identify UI requirements for training interface
- Plan database schema changes for tracking training progress
- Break down into tasks: data model, service layer, UI, validation
- Create implementation roadmap with phases

### Example 2: Race Feature Enhancement
**User**: "Design a weather system that affects race outcomes"

**Claude will**:
- Clarify weather types and their effects on racing
- Review RaceService and race simulation logic
- Identify where weather modifiers integrate into calculations
- Plan random weather generation vs player-controlled scenarios
- Consider UI for displaying weather conditions
- Document edge cases (weather changes mid-race?)
- Create phased implementation plan

### Example 3: Requirements Analysis
**User**: "Help me plan a multiplayer betting feature where players can bet on each other's races"

**Claude will**:
- Ask about betting rules, stake limits, payout calculations
- Explore multiplayer architecture requirements
- Review existing betting system (if any)
- Identify security concerns (preventing cheating, validation)
- Plan real-time updates and notifications
- Break into phases: single-player betting, then multiplayer integration
- Create comprehensive task breakdown

## Best Practices

### Discovery Phase
- Ask open-ended questions to understand the "why" behind features
- Reference similar features in the existing codebase
- Consider player experience and game balance
- Document edge cases and unusual scenarios

### Analysis Phase
- Read relevant existing code before proposing changes
- Identify patterns used elsewhere in the codebase (services, entities, repositories)
- Consider both happy path and error scenarios
- Think about testability

### Planning Phase
- Break features into vertical slices when possible (end-to-end functionality)
- Sequence tasks to deliver testable increments
- Flag high-risk or complex areas that need extra attention
- Create detailed but flexible plans

### Documentation Phase
- Write specifications that developers can implement from
- Include code examples or pseudocode for complex logic
- Reference existing patterns to follow
- Document open questions and areas needing future decisions

## Output Format

After conducting discovery and planning, create a feature specification document in `/docs/features/` that includes:

1. **Feature Summary**: One-paragraph overview
2. **Requirements**: Functional and non-functional requirements
3. **Technical Approach**: Architecture and integration points
4. **Implementation Plan**: Phased task breakdown
5. **Success Criteria**: How to validate correctness
6. **Open Questions**: Items needing further clarification

Use the PLANNING_TEMPLATE.md as a starting point for documentation.

**Output Location**: All feature specification documents should be saved to `/docs/features/[feature-name].md`

## Integration with Existing Systems

When planning features for TripleDerby, consider integration with:
- **Core Entities**: Horse, Race, RaceRun, RaceRunHorse, Player, etc.
- **Services**: RaceService, simulation logic, game flow
- **Data Layer**: Entity Framework, repositories, ModelBuilderExtensions
- **UI**: Game interface, player controls, visual feedback
- **Game Balance**: Stats, probabilities, progression systems

## Notes

- This skill uses Read, Grep, and Glob tools to explore the codebase during discovery
- Creates task lists using TodoWrite for structured planning
- May use AskUserQuestion to clarify ambiguous requirements
- Produces markdown documentation for feature specifications
- Focuses on practical, implementable plans rather than theoretical designs

## CRITICAL GIT WORKFLOW RULES

**NEVER commit or push code without EXPLICIT user approval.**

When implementing features:
1. **Discovery Phase**: Research, design, document - NO git commands
2. **Implementation Phase**: Write code, run tests - NO git commits
3. **WAIT for user approval**: User must explicitly say "commit this" or "push this"
4. **ONLY THEN**: Create commits and push to remote

**Examples of what NOT to do:**
- ❌ "Let me commit Phase 1" (without asking first)
- ❌ Automatically committing after tests pass
- ❌ Assuming user wants code committed

**Correct workflow:**
- ✅ Implement feature
- ✅ Run tests to verify
- ✅ Report results to user
- ✅ ASK: "Would you like me to commit these changes?"
- ✅ WAIT for explicit approval
- ✅ ONLY THEN run git commands

## COMMIT AND PR MESSAGE RULES

**NEVER include Claude Code attribution or self-reference in commits or PRs.**

When creating commits or pull requests:
- ❌ NEVER add "🤖 Generated with [Claude Code]" footer
- ❌ NEVER add "Co-Authored-By: Claude Sonnet" tag
- ❌ NEVER mention Claude, AI, or automated generation
- ✅ Write commit messages as if written by the developer
- ✅ Focus on what changed and why
- ✅ Use professional, technical language only

**Examples:**

**BAD - DO NOT DO THIS:**
```
Feature implementation complete

This adds the new commentary system.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**GOOD - DO THIS:**
```
Feature implementation complete

This adds the new commentary system with event detection
and natural language variation.
```
