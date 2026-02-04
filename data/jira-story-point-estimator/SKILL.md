---
name: JIRA Story Point Estimator
description: Estimates story points for JIRA tickets by analyzing complexity, scope, and comparing to historical team data. Activates when users ask to estimate, point, or size a ticket, or ask "how many points should this be?"
---

# JIRA Story Point Estimator Skill

## When to Use This Skill

Activate this skill when the user:
- Asks "estimate this ticket" or "how many story points?"
- Asks to "size" or "point" a ticket
- Asks "what should this be pointed at?"
- Wants help with sprint planning estimation
- Asks "is X points right for this ticket?"
- Reviews a ticket that needs story points

## Story Point Scale Reference

HyperFleet uses a modified Fibonacci sequence for story points:

| Points | Meaning | Typical Scope | Notes |
|--------|---------|---------------|-------|
| **0** | Tracking Only | Quick/easy task with stakeholder value | Rarely used. For tasks worth tracking but with negligible effort compared to a 1-pointer |
| **1** | Trivial | One-line change, extremely simple task | The smallest issue possible - everything scales from here. No risk, very low effort, very low complexity |
| **3** | Straightforward | Time consuming but fairly straightforward work | Doesn't have to be complex, but usually time consuming. Minor risks possible |
| **5** | Medium | Requires investigation, design, collaboration | Probably needs discussion with others. Can be quite time consuming or complex. Risks involved |
| **8** | Large | Big task requiring investigation and design | Requires collaboration with others. Solution can be quite challenging. Risks are expected. **Design doc required** |
| **13** | Too Large | Should be split into smaller stories | Ideally, this shouldn't be used. If you see an issue this big, it must be broken down |

## Estimation Methodology

### Step 1: Fetch Ticket Details

```bash
jira issue view TICKET-KEY --plain 2>/dev/null
```

### Step 2: Analyze Complexity Factors

**Scope Indicators (examine description and acceptance criteria):**
- Number of acceptance criteria
- Number of components/files likely affected
- Integration points mentioned
- Testing requirements

**Complexity Indicators:**
- New feature vs. modification vs. bug fix
- Requires new patterns or unfamiliar technology
- External dependencies (APIs, services)
- Database/schema changes
- Security implications
- Documentation requirements

**Risk Indicators:**
- Ambiguity in requirements
- Dependencies on other tickets
- Time-sensitive (blocks other work)
- Requires coordination with other teams

### Step 3: Find Similar Historical Tickets

Search for comparable completed tickets:

```bash
jira issue list -q"project = HYPERFLEET AND status = Done AND type = Story" --plain 2>/dev/null | head -20
```

```bash
jira issue list -q"project = HYPERFLEET AND status = Done AND 'Story Points' is not EMPTY AND type = Story" --plain 2>/dev/null | head -20
```

### Step 4: Provide Estimation

## Output Format

### Estimation for: TICKET-KEY

**Summary:** [Ticket title]
**Type:** [Story/Task/Bug]

---

#### Complexity Analysis

| Factor | Assessment | Impact |
|--------|------------|--------|
| Scope | [Small/Medium/Large] | [Description] |
| Technical Complexity | [Low/Medium/High] | [Why] |
| Dependencies | [None/Few/Many] | [List if any] |
| Testing Effort | [Minimal/Moderate/Extensive] | [Why] |
| Risk/Uncertainty | [Low/Medium/High] | [Why] |

---

#### Recommendation

**Suggested Story Points: X**

**Confidence Level:** [High/Medium/Low]

**Reasoning:**
- [Primary factor 1]
- [Primary factor 2]
- [Comparison to similar work]

---

#### Similar Completed Tickets (for reference)

| Ticket | Summary | Points | Similarity |
|--------|---------|--------|------------|
| TICKET-A | [Summary] | 5 | High - similar scope |
| TICKET-B | [Summary] | 3 | Medium - simpler version |

---

#### Considerations

- **If higher:** [What would make this larger]
- **If lower:** [What would make this smaller]
- **Break-down suggestion:** [If 13+ points, suggest how to split]

## Setting Story Points

Once agreed, set story points using:

```bash
jira issue edit TICKET-KEY --custom story-points=X --no-input
```

Or for Story Point Estimate field (Next-gen projects):

```bash
jira issue edit TICKET-KEY --custom story-point-estimate=X --no-input
```

## Team Calibration Notes

When estimating, consider:
- Team's typical velocity (points completed per sprint)
- Recent similar work and how long it actually took
- Team familiarity with the codebase area
- Current sprint load and focus

## Anti-Patterns to Flag

- **Anchoring**: Don't let existing (wrong) estimates bias you
- **Scope Creep**: Point what's written, not what might be added
- **Hero Estimates**: Assume average team member, not expert
- **Planning Fallacy**: Add buffer for unknowns
- **Story Point Inflation**: Keep consistent with team baseline
