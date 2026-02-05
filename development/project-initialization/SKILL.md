---
name: project-initialization
description: Comprehensive framework for initializing new software projects with Claude Code, implementing 2025 best practices for LLM-based software engineering including TDD, multi-agent orchestration, and session management.
---

# Claude Code Project Initialization Skill

## Overview
This skill provides a comprehensive framework for initializing new software projects with Claude Code, implementing 2025 best practices for LLM-based software engineering. It establishes project structure, documentation, testing protocols, and agent orchestration strategies to deliver exceptional results.

---

## 1. Project Initialization Workflow

### 1.1 Initial Analysis Phase
When starting a new project, Claude Code must:

1. **Read and Analyze PRD**
   - Parse the Product Requirements Document thoroughly
   - Extract functional and non-functional requirements
   - Identify technical constraints and dependencies
   - Map user stories and acceptance criteria
   - Document any ambiguities requiring clarification

2. **Context Engineering**
   - Create a comprehensive understanding of the problem space
   - Research relevant domain knowledge and best practices
   - Identify similar solutions and architectural patterns
   - Build a mental model of the system architecture

3. **Technology Stack Assessment**
   - Evaluate appropriate technologies based on requirements
   - Consider performance, scalability, and maintainability
   - Document technology decisions and rationale
   - Identify required dependencies and libraries

### 1.2 Project Structure Creation

```
project-root/
├── .claude/
│   ├── CLAUDE.md              # Main Claude instructions and rules
│   ├── agents/                # Agent definitions and configurations
│   ├── mcp-servers/           # MCP server configurations
│   ├── sessions/              # Session management files
│   └── context/               # Project context and knowledge base
├── docs/
│   ├── PRD.md                 # Product Requirements Document
│   ├── architecture/          # Architecture documentation
│   ├── phases/                # Phase-specific documentation
│   └── technical-specs/       # Technical specifications
├── src/
│   └── [source code]
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── scripts/
    ├── init.sh
    └── session-manager.sh
```

---

## 2. Phase Decomposition Strategy

### 2.1 Breaking Work into Phases

Claude Code should decompose the project into logical, sequential phases:

```yaml
phases:
  phase_1_foundation:
    name: "Core Infrastructure & Setup"
    duration: "1-2 sessions"
    objectives:
      - Set up development environment
      - Initialize project structure
      - Configure build tools and dependencies
      - Establish CI/CD pipeline basics
    deliverables:
      - Working development environment
      - Basic project scaffolding
      - Initial test suite structure
    
  phase_2_data_layer:
    name: "Data Models & Persistence"
    duration: "2-3 sessions"
    objectives:
      - Design data models
      - Implement database schemas
      - Create data access layer
      - Set up migrations
    deliverables:
      - Database schemas
      - ORM/data access code
      - Migration scripts
      - Data validation logic
    
  phase_3_business_logic:
    name: "Core Business Logic"
    duration: "3-4 sessions"
    objectives:
      - Implement domain models
      - Create service layer
      - Build business rule engine
      - Implement core algorithms
    deliverables:
      - Domain model implementations
      - Service interfaces
      - Business logic tests
      
  phase_4_api_layer:
    name: "API & Integration Layer"
    duration: "2-3 sessions"
    objectives:
      - Design API contracts
      - Implement endpoints
      - Add authentication/authorization
      - Create API documentation
    deliverables:
      - RESTful/GraphQL APIs
      - API documentation
      - Integration tests
      
  phase_5_ui_layer:
    name: "User Interface"
    duration: "3-4 sessions"
    objectives:
      - Implement UI components
      - Create user flows
      - Add state management
      - Implement responsive design
    deliverables:
      - UI components
      - User interaction flows
      - Frontend tests
```

### 2.2 Phase Documentation Template

For each phase, create a detailed specification document:

```markdown
# Phase [X]: [Phase Name]

## Overview
[Brief description of what this phase accomplishes]

## Prerequisites
- [ ] Previous phase completed and tested
- [ ] Required dependencies installed
- [ ] Environment configured

## Technical Specifications
### Architecture
[Architectural decisions and patterns for this phase]

### Components
[List of components to be built]

### Interfaces
[APIs, contracts, and integration points]

## Implementation Checklist
- [ ] Component A implemented
- [ ] Unit tests for Component A (80% coverage)
- [ ] Integration tests
- [ ] Documentation updated
- [ ] Code review completed

## Testing Requirements
- Unit test coverage: >= 80%
- All tests must pass before proceeding
- Performance benchmarks met

## Success Criteria
[Specific, measurable criteria for phase completion]
```

---

## 3. Core Rules and Guidelines (CLAUDE.md)

### 3.1 CLAUDE.md Template

```markdown
# CLAUDE.md - Project Guidelines and Rules

## Project Context
Project: [Project Name]
PRD Location: ./docs/PRD.md
Current Phase: [Current Phase Number and Name]
Session: [Session Number]

## Strict Adherence Rules

### 1. Test-Driven Development (TDD)
CRITICAL: Follow TDD methodology rigorously:
1. **RED Phase**: Write failing tests FIRST
   - Write test cases before ANY implementation
   - Ensure tests fail for the right reasons
   - Cover edge cases and boundary conditions
   
2. **GREEN Phase**: Write minimal code to pass
   - Implement ONLY what's needed to pass tests
   - No premature optimization
   - No feature creep
   
3. **REFACTOR Phase**: Improve code quality
   - Refactor for clarity and maintainability
   - Maintain test coverage
   - Apply SOLID principles

**Coverage Requirements**:
- Minimum 80% code coverage
- 100% test pass rate required before commits
- Critical paths must have 100% coverage

### 2. Session Management Protocol

**At Session Start**:
1. Read previous session summary from `.claude/sessions/session_[n].md`
2. Review current phase documentation
3. Check test suite status
4. Identify blocked items or dependencies

**During Session**:
1. Document all decisions in session log
2. Track completed tasks
3. Note any deviations from plan
4. Record questions and ambiguities

**At Session End**:
1. Create session summary with:
   - Work completed
   - Tests written/passed
   - Code coverage metrics
   - Blockers encountered
   - Next session plan
2. Update phase progress tracker
3. Commit all changes with descriptive messages

### 3. Communication and Clarity Rules

**ALWAYS ASK when encountering**:
- Ambiguous requirements
- Multiple valid implementation approaches
- Performance vs. maintainability trade-offs
- Security considerations
- Third-party service integrations

**Question Format**:
```
CLARIFICATION NEEDED:
Context: [What you're working on]
Ambiguity: [What's unclear]
Options: [Possible interpretations/approaches]
Recommendation: [Your suggested approach and why]
Impact: [How this affects other components]
```

### 4. Code Quality Standards

**Every file must**:
- Include comprehensive documentation
- Follow project style guide
- Pass linting checks
- Have associated tests
- Include error handling

**Commit Standards**:
- Use conventional commits format
- One logical change per commit
- Include test updates with implementation
- Reference issue/ticket numbers

## Available Agents

### Primary Agents

1. **Architect Agent**
   - Role: System design and architecture decisions
   - Invoke for: Major design decisions, pattern selection, technology choices
   - Context: PRD, existing architecture docs

2. **Test Designer Agent**
   - Role: Test strategy and test case design
   - Invoke for: Test planning, edge case identification, test data generation
   - Context: Requirements, implementation details

3. **Implementation Agent**
   - Role: Code implementation following TDD
   - Invoke for: Writing production code, refactoring
   - Context: Failing tests, design specifications

4. **Review Agent**
   - Role: Code review and quality assurance
   - Invoke for: Pre-commit reviews, identifying improvements
   - Context: Implementation, tests, standards

5. **Documentation Agent**
   - Role: Technical documentation creation
   - Invoke for: API docs, architecture diagrams, user guides
   - Context: Implementation, requirements

### Specialist Sub-Agents

1. **Security Analyst**
   - Invoke for: Security reviews, vulnerability assessment
   - Frequency: Every API endpoint, data flow

2. **Performance Optimizer**
   - Invoke for: Performance bottlenecks, optimization opportunities
   - Frequency: After each phase completion

3. **Database Specialist**
   - Invoke for: Schema design, query optimization
   - Frequency: During data layer implementation

4. **UI/UX Specialist**
   - Invoke for: Interface design, accessibility
   - Frequency: During UI implementation phases

## MCP Server Configuration

### Core MCP Servers

1. **Git/GitHub MCP**
   - Purpose: Version control integration
   - Usage: Automatic commits, PR creation, issue tracking
   - Config: `.claude/mcp-servers/github.json`

2. **Database MCP**
   - Purpose: Database operations and testing
   - Usage: Schema management, test data, migrations
   - Config: `.claude/mcp-servers/database.json`

3. **Testing MCP**
   - Purpose: Test execution and coverage reporting
   - Usage: Continuous test running, coverage tracking
   - Config: `.claude/mcp-servers/testing.json`

4. **Documentation MCP**
   - Purpose: Documentation generation and updates
   - Usage: Auto-generate docs from code, maintain consistency
   - Config: `.claude/mcp-servers/docs.json`

### MCP Usage Rules

- Check MCP availability at session start
- Use MCPs for repetitive tasks
- Log all MCP interactions
- Fallback to manual processes if MCP unavailable

## Multi-Agent Orchestration Patterns

### Pattern 1: Sequential Handoff
```
User Request → Planning Agent → Test Designer → Implementation Agent → Review Agent → User
```

### Pattern 2: Parallel Execution
```
Planning Agent → [Test Designer || Documentation Agent || Security Analyst] → Synchronization Point
```

### Pattern 3: Iterative Refinement
```
Implementation Agent ↔ Test Designer (until tests pass) → Review Agent
```

### Agent Communication Protocol
- Agents share context through structured messages
- Each agent documents decisions and rationale
- Handoffs include success criteria
- Failed handoffs trigger escalation to user

## Error Handling and Recovery

### On Test Failure
1. Analyze failure reason
2. Determine if bug or test issue
3. Fix and re-run
4. Document in session log

### On Ambiguity
1. Document the ambiguity
2. List possible interpretations
3. Choose safest default OR
4. Escalate to user for clarification

### On Performance Issues
1. Profile to identify bottleneck
2. Document current metrics
3. Propose optimization
4. Implement if within phase scope

## Progress Tracking

### Metrics to Track
- Lines of code written
- Test coverage percentage
- Tests written/passing
- Documentation completeness
- Technical debt items
- Performance benchmarks

### Daily Checklist
- [ ] Session summary created
- [ ] Tests passing (100%)
- [ ] Coverage >= 80%
- [ ] Code committed
- [ ] Documentation updated
- [ ] Next session planned
```

---

## 4. Advanced LLM Software Engineering Practices

### 4.1 Context Window Management

**Strategies for Long-Running Projects**:
1. **Hierarchical Summarization**
   - Maintain session summaries at multiple levels
   - Create phase summaries from session summaries
   - Build project overview from phase summaries

2. **Selective Context Loading**
   - Load only relevant phase documentation
   - Use semantic search for code context
   - Maintain a "working set" of active files

3. **Context Compression**
   - Use structured formats (YAML/JSON) for data
   - Compress verbose documentation
   - Extract key decisions and rationale

### 4.2 Multi-Agent Collaboration Framework

```python
# Example Agent Orchestration Configuration
agent_config = {
    "planning_agent": {
        "role": "orchestrator",
        "capabilities": ["decomposition", "delegation", "monitoring"],
        "context_access": "full",
        "decision_authority": "high"
    },
    "specialist_agents": {
        "frontend": {
            "expertise": ["React", "TypeScript", "CSS"],
            "context_access": "filtered",
            "autonomy_level": "guided"
        },
        "backend": {
            "expertise": ["Python", "FastAPI", "PostgreSQL"],
            "context_access": "filtered",
            "autonomy_level": "guided"
        },
        "testing": {
            "expertise": ["Jest", "Pytest", "Cypress"],
            "context_access": "read_only",
            "autonomy_level": "autonomous"
        }
    }
}
```

### 4.3 Quality Assurance Pipeline

```yaml
quality_pipeline:
  pre_commit:
    - lint_check
    - format_check
    - type_check
    - security_scan
    
  pre_merge:
    - unit_tests
    - integration_tests
    - coverage_check
    - performance_tests
    
  post_merge:
    - e2e_tests
    - accessibility_tests
    - documentation_build
    - deployment_check
```

---

## 5. Session Management System

### 5.1 Session Structure

```markdown
# Session [Number] - [Date]

## Session Objectives
- Primary: [Main goal for this session]
- Secondary: [Additional goals if time permits]

## Context Loaded
- PRD sections: [Relevant sections]
- Previous sessions: [Which session summaries loaded]
- Code files: [Active working set]

## Work Log

### [Timestamp] - Task Started: [Task Name]
- Approach: [Strategy chosen]
- Tests written: [Number and type]
- Implementation: [Brief description]
- Result: [Success/Failure/Blocked]

### [Timestamp] - Decision Point: [Decision Name]
- Context: [Why decision needed]
- Options considered: [List options]
- Choice: [Selected option]
- Rationale: [Why chosen]

## Metrics
- Tests Written: [Number]
- Tests Passing: [Percentage]
- Code Coverage: [Percentage]
- Lines of Code: [Added/Modified/Deleted]

## Blockers and Issues
- [Issue 1]: [Description and impact]
- [Issue 2]: [Description and impact]

## Questions for Stakeholder
1. [Question with context]
2. [Question with context]

## Next Session Plan
- Continue: [What to continue]
- Start: [What to begin]
- Review: [What needs review]
- Priority: [High/Medium/Low items]

## Session Summary
[2-3 sentence summary of session accomplishments and state]
```

### 5.2 Session Handoff Protocol

**Creating Effective Handoffs**:
1. **State Serialization**
   - Save all working context
   - Document partial work
   - List open decisions

2. **Intent Preservation**
   - Document the "why" behind changes
   - Explain design decisions
   - Note alternative approaches considered

3. **Continuity Markers**
   - Mark exact stopping points in code
   - List next immediate steps
   - Identify dependencies and blockers

---

## 6. Tool and MCP Integration Guidelines

### 6.1 MCP Server Development Template

```typescript
// Custom MCP Server Template
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

interface ProjectMCPConfig {
  name: string;
  version: string;
  capabilities: {
    testing?: boolean;
    documentation?: boolean;
    deployment?: boolean;
    monitoring?: boolean;
  };
}

class ProjectMCPServer {
  private server: Server;
  private config: ProjectMCPConfig;

  constructor(config: ProjectMCPConfig) {
    this.config = config;
    this.initializeServer();
  }

  private initializeServer() {
    this.server = new Server(
      {
        name: this.config.name,
        version: this.config.version
      },
      {
        capabilities: {
          resources: {},
          tools: {}
        }
      }
    );

    this.registerTools();
    this.registerResources();
  }

  private registerTools() {
    // Tool registration for project-specific operations
    if (this.config.capabilities.testing) {
      this.registerTestingTools();
    }
    if (this.config.capabilities.documentation) {
      this.registerDocumentationTools();
    }
  }

  private registerTestingTools() {
    this.server.setRequestHandler("run_tests", async (request) => {
      // Implementation for test execution
      return { success: true, coverage: 85, passed: 42, failed: 0 };
    });

    this.server.setRequestHandler("generate_test_data", async (request) => {
      // Implementation for test data generation
      return { data: "generated test data" };
    });
  }

  private registerDocumentationTools() {
    this.server.setRequestHandler("generate_docs", async (request) => {
      // Implementation for documentation generation
      return { success: true, files_generated: 5 };
    });
  }

  async start() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
  }
}
```

### 6.2 Tool Selection Matrix

| Task Category | Recommended Tool | MCP Integration | Priority |
|--------------|------------------|-----------------|----------|
| Version Control | Git/GitHub | GitHub MCP | Critical |
| Testing | Jest/Pytest | Custom Testing MCP | Critical |
| Documentation | JSDoc/Sphinx | Documentation MCP | High |
| Database | PostgreSQL/MongoDB | Database MCP | High |
| API Testing | Postman/Insomnia | API Testing MCP | Medium |
| Performance | Lighthouse/K6 | Performance MCP | Medium |
| Security | OWASP ZAP | Security MCP | High |
| Deployment | Docker/K8s | Deployment MCP | Medium |

---

## 7. Continuous Improvement Protocols

### 7.1 Retrospective Framework

**After Each Phase**:
```markdown
# Phase [X] Retrospective

## What Went Well
- [Success 1]
- [Success 2]

## What Could Be Improved
- [Improvement 1]
- [Improvement 2]

## Lessons Learned
- [Lesson 1]
- [Lesson 2]

## Process Adjustments
- [Change to implement in next phase]
- [Tool or workflow modification]

## Technical Debt Identified
- [Debt item 1] - Priority: [High/Medium/Low]
- [Debt item 2] - Priority: [High/Medium/Low]
```

### 7.2 Feedback Loop Integration

1. **User Feedback Collection**
   - Regular stakeholder check-ins
   - Incremental delivery for validation
   - Rapid prototype iterations

2. **Automated Feedback**
   - Continuous integration metrics
   - Performance monitoring
   - Error tracking and analysis

3. **AI Agent Feedback**
   - Review agent assessments
   - Cross-agent validation
   - Pattern recognition for common issues

---

## 8. Risk Management and Mitigation

### 8.1 Common Risks and Mitigations

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|-------------------|
| Context Overflow | High | Medium | Implement hierarchical summarization |
| Test Coverage Gaps | Medium | Low | Enforce TDD, automated coverage checks |
| Requirement Ambiguity | High | High | Early and frequent clarification requests |
| Technical Debt Accumulation | Medium | Medium | Regular refactoring sessions |
| Agent Hallucination | High | Low | Strict validation, human review gates |
| Performance Degradation | Medium | Medium | Continuous performance testing |

### 8.2 Escalation Protocol

```yaml
escalation_levels:
  level_1_automated:
    trigger: "Test failure or coverage drop"
    action: "Automatic rerun and analysis"
    timeout: "5 minutes"
    
  level_2_agent:
    trigger: "Repeated failures or ambiguity"
    action: "Specialist agent consultation"
    timeout: "15 minutes"
    
  level_3_human:
    trigger: "Critical decision or blocker"
    action: "Human intervention required"
    notification: "Immediate"
```

---

## 9. Performance Optimization Guidelines

### 9.1 Code Optimization Priorities

1. **Correctness First**
   - Ensure all tests pass
   - Validate business logic
   - Handle edge cases

2. **Clarity Second**
   - Readable, maintainable code
   - Clear naming conventions
   - Comprehensive documentation

3. **Performance Third**
   - Profile before optimizing
   - Focus on bottlenecks
   - Measure improvements

### 9.2 LLM Interaction Optimization

**Reducing Token Usage**:
- Use structured formats (JSON/YAML)
- Compress repetitive information
- Cache common responses
- Batch similar operations

**Improving Response Quality**:
- Provide clear, specific prompts
- Include relevant examples
- Use few-shot learning
- Implement validation loops

---

## 10. Implementation Checklist

### 10.1 Project Initialization Checklist

- [ ] PRD analyzed and understood
- [ ] Project structure created
- [ ] CLAUDE.md configured
- [ ] Phase breakdown completed
- [ ] Technology stack selected
- [ ] Development environment setup
- [ ] Git repository initialized
- [ ] CI/CD pipeline configured
- [ ] Testing framework setup
- [ ] Documentation structure created
- [ ] MCP servers configured
- [ ] Agent definitions created
- [ ] Session management initialized
- [ ] First phase documentation prepared
- [ ] Stakeholder questions documented

### 10.2 Per-Session Checklist

**Start of Session**:
- [ ] Load previous session summary
- [ ] Review current phase status
- [ ] Check test suite health
- [ ] Update context with recent changes
- [ ] Identify session objectives

**During Session**:
- [ ] Follow TDD cycle strictly
- [ ] Document all decisions
- [ ] Ask for clarification when needed
- [ ] Maintain session log
- [ ] Track metrics continuously

**End of Session**:
- [ ] Run full test suite
- [ ] Check coverage metrics
- [ ] Create session summary
- [ ] Update phase progress
- [ ] Plan next session
- [ ] Commit all changes
- [ ] Update documentation

---

## Conclusion

This comprehensive project initialization skill provides Claude Code with a structured, repeatable framework for delivering exceptional software projects. By combining:

- **Rigorous TDD practices** for quality assurance
- **Systematic phase decomposition** for manageable progress
- **Multi-agent orchestration** for specialized expertise
- **Continuous session management** for context preservation
- **MCP integration** for tool automation
- **Clear communication protocols** for stakeholder alignment

Claude Code can consistently deliver high-quality, well-tested, thoroughly documented software that meets or exceeds requirements while maintaining development velocity and code maintainability.

The key to success lies in disciplined adherence to these protocols, continuous improvement based on retrospectives, and maintaining clear communication channels with stakeholders throughout the development process.

---

## Appendix A: Quick Reference Commands

```bash
# Initialize new project
claude-init --project-name "MyProject" --prd "./docs/PRD.md"

# Start new session
claude-session start --phase 1 --objective "Set up foundation"

# Run tests with coverage
claude-test --coverage --min 80

# Generate documentation
claude-docs generate --format markdown

# Create phase summary
claude-phase summarize --phase 1 --output "./docs/phases/phase1-summary.md"

# Check agent status
claude-agent status --all

# Configure MCP server
claude-mcp add --name "github" --config "./mcp-servers/github.json"
```

## Appendix B: Example Configuration Files

### MCP Server Configuration Example
```json
{
  "name": "project-testing-mcp",
  "version": "1.0.0",
  "transport": "stdio",
  "capabilities": {
    "testing": {
      "frameworks": ["jest", "pytest", "cypress"],
      "coverage": true,
      "parallel": true
    },
    "reporting": {
      "formats": ["json", "html", "junit"],
      "realtime": true
    }
  },
  "config": {
    "testDirectory": "./tests",
    "coverageThreshold": 80,
    "timeout": 30000
  }
}
```

### Agent Configuration Example
```yaml
agents:
  test_designer:
    model: "claude-opus-4.1"
    temperature: 0.3
    system_prompt: |
      You are a test design specialist focused on comprehensive test coverage.
      Always consider edge cases, boundary conditions, and error scenarios.
      Follow TDD principles strictly.
    tools:
      - test_generator
      - coverage_analyzer
      - test_data_factory
    
  implementation:
    model: "claude-opus-4.1"
    temperature: 0.5
    system_prompt: |
      You implement code to pass existing tests.
      Write minimal code to make tests green.
      Focus on clarity and maintainability.
    tools:
      - code_formatter
      - linter
      - dependency_manager
```

---

*End of Claude Code Project Initialization Skill Document*