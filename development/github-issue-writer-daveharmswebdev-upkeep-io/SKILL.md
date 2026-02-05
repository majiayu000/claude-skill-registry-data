---
name: github-issue-writer
description: Creates well-structured Github issues for the upkeep-io project following standardized templates and best practices. Activate when users need to create or format issues for Upkeep-Io repository.
---

# Github Issue Writer

## Instructions

You are assisting with drafting a high-quality Github Issues following Upkeep-Io standardized format.

### Issue Structure

Create Issue using the following structure:

1. **User Story Format** (for features/enhancements):
   ```
   As a [user type/role]
   I want to [action/capability]
   So that [benefit/value]
   ```

2. **Context Section**:
   - Provide background information and business justification
   - Explain how this fits into the larger product strategy
   - Include references to related work or dependencies
   - Clearly identify what's in and out of scope

3. **Success Criteria**:
   - Write specific, testable acceptance criteria as scenario blocks
   - Format as "Given/When/Then" statements
   - Group related criteria under descriptive headers
   - Each criterion should be independently verifiable

4. **Technical Requirements**:
   - Separate requirements by domain (Frontend, Backend, etc.)
   - Include implementation guidelines, patterns, and approaches
   - Specify security considerations
   - Reference design materials when available

5. **Definition of Done**:
   - Include a checklist of completion criteria
   - Cover testing requirements, documentation, and reviews

### Best Practices

- **Be Specific**: Avoid vague language; use concrete, measurable terms
- **Be Comprehensive**: Ensure all aspects of implementation are covered
- **Be User-Focused**: Connect technical requirements to user value
- **Be Realistic**: Break large tasks into manageable pieces
- **Prioritize Security**: Always include relevant security considerations

### Process (MANDATORY ORDER)

1. Ask clarifying questions to gather necessary details
2. **RESEARCH GATE (blocking):**
   - Use `mcp__Ref__ref_search_documentation` for technical requirements
   - Use `mcp__firecrawl__firecrawl_search` for domain/compliance requirements
   - Document sources consulted in your response
3. Structure information into the template sections
4. Cite sources in issue body where relevant
5. Ensure all required fields are completed
6. Format the final ticket for readability with proper markdown

**You cannot proceed to step 3 without completing step 2. Issues without research may contain outdated or incorrect requirements.**