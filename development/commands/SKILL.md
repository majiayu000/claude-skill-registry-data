---
description: Create a new Claude Code skill with guided interactive workflow
argument-hint: <skill-type>
---

Use the @skill-creator-agent to guide you through creating a comprehensive, validated skill definition.

**Agent's Role (Context-Heavy Analysis):**
- Gather requirements and define skill scope with business objectives
- Guide you through structured choice selection for scope (narrow/versatile/comprehensive)
- Conduct business value analysis including ROI and impact assessment
- Guide you through value analysis depth selection (essential/comprehensive/strategic)
- Develop technical specification with architecture and implementation plan
- Guide you through implementation approach selection (rapid/structured/enterprise)
- Generate comprehensive skill manifest following standardized template structure
- Guide you through documentation completeness selection (essential/comprehensive/enterprise)
- Perform quality validation checking structure, content, technical requirements, and completeness
- Validate all outputs before proceeding to next phase
- Handle all interactive prompting, guidance, and validation

**Agent Output Required:**
The agent MUST return:
1. **Skill Requirements Summary**: Clear purpose, scope boundaries, use cases, and success criteria
2. **Business Value Analysis**: Problem statement, value proposition, ROI assessment, stakeholder alignment, and risk evaluation
3. **Technical Specification**: Functional requirements, non-functional requirements, architecture, implementation plan, testing strategy, and deployment plan
4. **Complete SKILL.md Content**: Full skill manifest with all sections populated following the standardized template structure
5. **Validation Report**: Comprehensive quality validation results with structural, content, technical, and completeness checks
6. **Recommended File Path**: Suggested location for SKILL.md based on skill type and category
7. **Commands to Execute**: Exact Write command to create SKILL.md file at specified path with generated content

**Main Claude's Role (Execution):**
After receiving the agent's analysis:
- Execute the Write command to create SKILL.md file at the specified path
- Verify the file was created successfully
- Display the validation report provided by the agent
- Confirm skill creation completion
- Show next steps for testing or deployment

**Workflow**: Agent analyzes → Main Claude executes → Changes actually happen
