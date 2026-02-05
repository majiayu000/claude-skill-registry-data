---
name: Investigation & Analysis
description: Analyze feature requests, refactor plans, or technical decisions to determine investment value and provide recommendations. Use when user mentions investigating, analyzing, or asks "should we build this".
allowed-tools: Read, Grep, Glob
---

# Investigation & Analysis Skill

## Purpose
Analyze feature requests or refactor plans to determine investment value and provide actionable recommendations.

## Auto-Activation Triggers
This skill activates when the user:
- Mentions investigating a feature or idea
- Asks "should we build this?"
- Requests feasibility analysis
- Wants to evaluate ROI or cost/benefit
- Asks "is this worth doing?"
- Mentions analyzing a refactor plan

## Analysis Process

### 1. Context Gathering
**Automatically check:**
- Review relevant existing code/architecture
- Search memory patterns for similar work
- Identify affected components and dependencies
- Review procedural memory for proven patterns

**Tools to use:**
- `Grep` to search codebase for related functionality
- `Glob` to find relevant files
- `Read` to examine current implementation

### 2. Investment Assessment

Evaluate across three dimensions:

#### Technical Factors
- **Implementation Complexity** (1-10 scale)
- **Risk Assessment** (breaking changes, dependencies)
- **Technical Debt Impact** (reduces/increases/neutral)
- **Performance Implications**

#### Business Factors
- **User Value Delivered**
- **Alignment with Project Goals**
- **Time to Implement**
- **Return on Investment**

#### Strategic Factors
- **Architecture Impact**
- **Reusability Potential**
- **Future Flexibility**

### 3. Recommendation Framework

**Question 1: Is it worth the investment?**
- **YES** - High value, reasonable cost, low risk
- **NO** - Low value, high cost, or high risk
- **CONDITIONAL** - Worth it if specific conditions met

**Question 2: What should we do with the request?**
- **KEEP AS-IS** - Plan is solid
- **MODIFY** - Suggest specific improvements
- **PIVOT** - Recommend alternative approach
- **DEFER** - Not now, revisit when [conditions]
- **REJECT** - Clear reasons why not

### 4. Response Format

```markdown
## Investigation: [Feature/Refactor Name]

### Investment Analysis

**Worth the Investment:** [YES/NO/CONDITIONAL]

[Executive summary in 2-3 sentences]

**Key Metrics:**
- Complexity: [X/10]
- Implementation Time: [estimate]
- Risk Level: [Low/Medium/High]
- Value Delivered: [Low/Medium/High]
- ROI: [High/Medium/Low]

### Recommendation: [KEEP/MODIFY/PIVOT/DEFER/REJECT]

[Detailed explanation with supporting evidence]

#### Technical Analysis
[Key technical findings from codebase investigation]

#### Business Justification
[Value proposition and alignment with goals]

#### Proposed Modifications (if MODIFY)
1. [Specific change with rationale]
2. [Specific change with rationale]

#### Alternative Approach (if PIVOT)
[Description of better approach]

### Implementation Considerations

**Prerequisites:**
- [Required before starting]

**Success Criteria:**
- [Measurable outcome]

**Potential Blockers:**
- [Risk] → Mitigation: [strategy]

### Evidence & References
- Code files examined: [file paths]
- Similar patterns in memory: [references]
```

## Best Practices

### 1. Be Evidence-Based
- Reference actual code files examined
- Cite similar attempts from memory
- Include metrics where available

### 2. Be Pragmatic
- Focus on practical impact
- Consider current capacity and priorities
- Balance ideal vs. practical constraints

### 3. Provide Actionable Guidance
- Specific next steps if proceeding
- Clear reasons if not proceeding
- Measurable success criteria

### 4. Check Memory First
Always consult:
- `.claude/memory/active/quick-reference.md`
- `.claude/memory/active/procedural-memory.md`

### 5. Leverage Existing Work
- Search for similar features already implemented
- Identify reusable patterns and components
- Check if request duplicates existing functionality

## Integration

**After Investigation:**
- If approved → Suggest `/orchestrate-tasks` for implementation
- If complex → Suggest `/plan-as-group` for collaborative planning

**Update Context:**
- Document investigation results
- Add insights to procedural memory if reusable

## Examples

### Feature Request
**User:** "Should we add real-time collaboration to the editor?"

**Skill:**
1. Searches codebase for existing editor architecture
2. Checks memory for similar implementations
3. Evaluates WebSocket/polling options
4. Assesses complexity vs. user value
5. Provides recommendation with implementation path

### Refactor Plan
**User:** "I'm thinking about refactoring to async/await"

**Skill:**
1. Examines current implementation
2. Identifies bottlenecks
3. Assesses migration complexity and risk
4. Evaluates performance benefits
5. Recommends phased approach or alternative

## Skill Metadata

**Version:** 1.0.0
**Category:** Planning & Decision Support
