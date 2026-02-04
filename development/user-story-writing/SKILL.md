---
name: "User Story Writing"
description: "Create well-structured user stories with clear acceptance criteria in 'As a/I want/So that' format for team communication"
category: "analysis"
required_tools: ["Read", "Write"]
---

# User Story Writing

## Purpose
Create well-structured user stories that clearly communicate user needs, business value, and acceptance criteria in a format teams can understand and implement.

## When to Use
- Defining new features from user perspective
- Breaking down large features into implementable pieces
- Communicating requirements to development teams
- Planning sprints and iterations

## Key Capabilities
1. **Story Structure** - Write clear "As a/I want/So that" format
2. **Acceptance Criteria** - Define testable validation requirements
3. **Value Focus** - Emphasize user benefits and business value

## Approach
1. Identify the user role or persona
2. Define what they want to accomplish
3. Explain why it provides value
4. Write 3-5 clear acceptance criteria
5. Estimate complexity (story points or T-shirt sizes)

## Example
**Context**: User needs to export data
````markdown
**User Story**: As a data analyst, I want to export reports to CSV format, so that I can analyze data in Excel.

**Acceptance Criteria**:
- [ ] Export button available on report page
- [ ] CSV file includes all visible columns
- [ ] File download starts immediately on click
- [ ] Filename includes report name and timestamp
- [ ] Export handles reports with 10,000+ rows

**Complexity**: Medium (3 points)
````

## Best Practices
- ✅ Keep stories small and focused (deliverable in 1-3 days)
- ✅ Write from user perspective, not system perspective
- ✅ Make acceptance criteria specific and testable
- ❌ Avoid: Technical implementation details in stories