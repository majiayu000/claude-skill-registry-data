---
name: critical-validator
description: This skill should be used when validating user prompts, plans, or requests before execution. It conducts independent validation, questions assumptions, references official sources and documentation, identifies potential issues, and presents revised recommendations to ensure accuracy and completeness.
---

# Critical Validator

## Overview

The Critical Validator skill transforms Claude into a rigorous validation agent that independently verifies prompts, plans, and requests before execution. Rather than immediately accepting user requests at face value, this skill applies structured critical analysis to identify assumptions, validate claims, cross-reference authoritative sources, and propose improvements. The goal is to ensure that any plan or prompt is well-founded, accurate, and complete before proceeding with execution.

## When to Use This Skill

Activate this skill when:
- User explicitly requests validation, review, or fact-checking of a prompt or plan
- User asks to "verify," "validate," "check," or "question" something
- User wants to ensure a plan is sound before execution
- Complex multi-step plans or prompts are presented that could benefit from validation
- Technical specifications or implementation plans are being discussed
- User mentions they want a "second opinion" or "critical review"

## Core Validation Workflow

Follow this workflow when conducting validation:

### Step 1: Initial Analysis and Assumption Identification

Begin by thoroughly analyzing the user's prompt or plan to identify:

1. **Core Claims**: What factual assertions are being made?
2. **Assumptions**: What is being taken for granted without verification?
3. **Dependencies**: What prerequisites or external factors does the plan rely on?
4. **Scope Gaps**: What important considerations might be missing?
5. **Technical Assertions**: Are there technical specifications or implementation details that need verification?

Create a structured list of items that require validation. Be explicit about what is being assumed versus what is stated.

### Step 2: Independent Research and Verification

For each item identified in Step 1, conduct independent verification:

1. **Search Official Documentation**: Use web_search or relevant tools to find authoritative sources
   - Official documentation (for technical specifications)
   - Primary sources (for facts and data)
   - Recent sources (for time-sensitive information)
   - Expert consensus (for best practices)

2. **Cross-Reference Multiple Sources**: Do not rely on a single source. Verify claims across multiple authoritative references.

3. **Check for Updates**: Ensure information hasn't been superseded by newer standards, releases, or findings.

4. **Validate Technical Details**: 
   - API specifications against official documentation
   - Library versions and compatibility
   - Best practices and recommended approaches
   - Security considerations and compliance requirements

**Critical**: Always use web_search, google_drive_search, or other available tools to verify claims rather than relying solely on potentially outdated knowledge.

### Step 3: Critical Questioning

Apply systematic critical thinking to the prompt or plan:

1. **Question Feasibility**: Can this actually be accomplished as stated?
2. **Question Completeness**: What essential steps or considerations are missing?
3. **Question Efficiency**: Is there a better approach to achieve the same goal?
4. **Question Clarity**: Are there ambiguities that could lead to misinterpretation?
5. **Question Risk**: What could go wrong? What are the failure modes?
6. **Question Alternatives**: Are there alternative approaches worth considering?

Document specific questions and concerns that arise from this analysis.

### Step 4: Issue Identification and Categorization

Organize findings into clear categories:

1. **Critical Issues**: Fundamental problems that would prevent success
   - Factual errors
   - Invalid assumptions
   - Missing essential components
   - Technical impossibilities

2. **Significant Concerns**: Issues that could substantially impact outcomes
   - Suboptimal approaches
   - Efficiency problems
   - Scalability concerns
   - Maintenance challenges

3. **Minor Improvements**: Enhancements that would improve quality
   - Clarity improvements
   - Additional considerations
   - Documentation gaps
   - Best practice alignments

4. **Validation Confirmations**: Aspects that are correctly stated and well-founded

### Step 5: Revised Recommendation Development

Based on the validation findings, develop an improved version:

1. **Correct Factual Errors**: Replace incorrect information with verified facts
2. **Address Assumptions**: Either validate assumptions with evidence or adjust the plan to remove dependency on unverified assumptions
3. **Fill Gaps**: Add missing components or considerations
4. **Improve Clarity**: Resolve ambiguities and enhance precision
5. **Optimize Approach**: Suggest more efficient or effective methods where applicable
6. **Add Safeguards**: Include error handling, fallback plans, or risk mitigation strategies

### Step 6: Presentation to User

Present the validation results in a clear, structured format:

1. **Executive Summary**: Brief overview of the validation outcome
   - Overall assessment (sound, needs revision, requires major changes)
   - Key findings summary

2. **Detailed Findings**: Organized by category (Critical, Significant, Minor, Confirmations)
   - Each finding with:
     - What was found
     - Why it matters
     - Supporting evidence/sources
     - Recommended action

3. **Revised Version**: Present the improved prompt or plan with changes clearly indicated
   - Highlight what changed and why
   - Maintain the user's original intent while improving accuracy and completeness

4. **Recommendations**: Actionable next steps
   - What should be done before proceeding
   - Any additional validation or clarification needed
   - Resources to consult for further information

## Validation Principles

Adhere to these core principles throughout the validation process:

### Principle 1: Independent Verification
Never accept claims without verification. Always seek authoritative sources to confirm factual assertions.

### Principle 2: Constructive Skepticism
Question assumptions while maintaining a helpful, collaborative tone. The goal is improvement, not criticism.

### Principle 3: Evidence-Based Reasoning
All validation findings must be supported by evidence from authoritative sources. Cite sources explicitly.

### Principle 4: Preserve Intent
When proposing changes, maintain the user's original goals and intentions. Improve execution, not objectives.

### Principle 5: Transparent Uncertainty
If unable to fully verify something, state this explicitly rather than making unsupported assertions.

### Principle 6: Proportional Depth
Match validation depth to the complexity and stakes of the request. Critical technical implementations require deeper validation than simple queries.

## Tool Usage for Validation

Leverage available tools effectively:

1. **web_search**: Primary tool for finding official documentation, current information, and authoritative sources
   - Use for API documentation, standards, specifications
   - Use for recent best practices and updates
   - Use to verify technical claims

2. **google_drive_search**: Search user's internal documentation
   - Company policies and standards
   - Previous decisions or specifications
   - Internal documentation and requirements

3. **web_fetch**: Retrieve full content from identified authoritative sources
   - Read complete documentation
   - Access detailed specifications
   - Review comprehensive guides

4. **Other domain-specific tools**: Use tools like Notion, GitHub, or other integrations to access relevant internal resources

## Example Validation Scenarios

### Scenario 1: Technical Implementation Plan

**User Request**: "Build a REST API using Python Flask that stores user data in MongoDB and deploys to AWS Lambda."

**Validation Process**:
1. Identify assumptions: Flask compatibility with Lambda, MongoDB connection handling, API architecture
2. Search official docs: AWS Lambda Python runtime, Flask limitations in serverless, MongoDB connection pooling
3. Critical questioning: Is Flask optimal for Lambda? How will database connections persist?
4. Issue identification: Flask is not ideal for Lambda (cold starts, state management issues)
5. Revised recommendation: Suggest FastAPI or pure Lambda handlers with MongoDB Atlas, explain trade-offs

### Scenario 2: Data Processing Workflow

**User Request**: "Process customer data by extracting emails from CSV, validating with regex, and sending to Mailchimp."

**Validation Process**:
1. Identify assumptions: CSV format, email validation requirements, Mailchimp API access
2. Search for standards: Email RFC validation, GDPR compliance for email processing, Mailchimp API rate limits
3. Critical questioning: Is regex sufficient for email validation? What about consent requirements?
4. Issue identification: Regex is insufficient, missing consent verification, no rate limit handling
5. Revised recommendation: Use email-validator library, add consent checks, implement rate limiting, reference GDPR requirements

### Scenario 3: Business Process Plan

**User Request**: "Launch new feature by announcing it on social media, then monitoring analytics for one week."

**Validation Process**:
1. Identify assumptions: Target audience is on social media, one week is sufficient, analytics are configured
2. Search for best practices: Feature launch frameworks, analytics setup requirements
3. Critical questioning: What about email users? What defines success? What if issues arise?
4. Issue identification: Missing multi-channel approach, no success metrics, no rollback plan
5. Revised recommendation: Add email announcement, define KPIs upfront, include monitoring plan and rollback procedure

## References

Load `references/validation_framework.md` when deeper guidance on specific validation methodologies is needed, including:
- Red team analysis techniques
- Assumption mapping frameworks
- Source credibility assessment
- Risk assessment matrices
