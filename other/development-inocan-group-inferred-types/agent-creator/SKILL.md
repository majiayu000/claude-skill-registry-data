---
name: agent-creator
description: >
  Autonomous agent creation skill that generates specialized agent definitions from templates.
  Use when you need to create new Claude Code agents for specific tasks like code review,
  deployment automation, testing, documentation, security analysis, or general-purpose research.
  This skill automates the creation of agent definition files (.md) with proper structure,
  workflow instructions, and tool access patterns following Miyabi framework standards.
---

# Agent Creator

## Overview

This skill enables the automatic creation of specialized agents for the Miyabi framework. It generates agent definition files (.md) with complete workflows, tool access configurations, and quality standards based on established templates. Perfect for quickly creating domain-specific agents without manual configuration.

## Quick Start

### Create Your First Agent

```bash
# Initialize the agents directory
python .claude/skills/agent-creator/scripts/init_agent.py --init

# Generate a code review agent
python .claude/skills/agent-creator/scripts/generate_agent.py code-review-expert code-review

# Generate a deployment agent
python .claude/skills/agent-creator/scripts/generate_agent.py deployment-automator deployment
```

### Available Agent Types

- **code-review**: Comprehensive code review specialist (architecture, security, performance, testing)
- **deployment**: CI/CD automation and deployment pipeline management
- **testing**: Test automation and quality assurance specialist
- **documentation**: Documentation generation and maintenance expert
- **security**: Security analysis and vulnerability assessment specialist
- **general-purpose**: Research and complex multi-step task coordinator

## Agent Creation Workflow

### Step 1: Directory Setup

First, ensure the agents directory exists:

```bash
# Check if agents directory exists
python .claude/skills/agent-creator/scripts/init_agent.py --status

# Initialize if needed
python .claude/skills/agent-creator/scripts/init_agent.py --init
```

### Step 2: Choose Agent Type

Select the appropriate agent type based on your needs:

| Need | Recommended Type | Key Features |
|------|------------------|--------------|
| Code quality analysis | `code-review` | Architecture, security, performance review |
| Deployment automation | `deployment` | CI/CD, health checks, rollback |
| Test automation | `testing` | Coverage analysis, quality gates |
| Documentation needs | `documentation` | API docs, technical writing |
| Security concerns | `security` | Vulnerability scanning, compliance |
| Complex tasks | `general-purpose` | Research, coordination, synthesis |

### Step 3: Generate Agent

Use the generator script with appropriate parameters:

```bash
# Basic generation
python .claude/skills/agent-creator/scripts/generate_agent.py <name> <type>

# With custom description
python .claude/skills/agent-creator/scripts/generate_agent.py \
  security-auditor security \
  --description "Specialized security auditor for web applications"

# With custom capabilities
python .claude/skills/agent-creator/scripts/generate_agent.py \
  api-tester testing \
  --capabilities "API testing" "Load testing" "Integration testing"

# Dry run to preview
python .claude/skills/agent-creator/scripts/generate_agent.py \
  custom-agent general-purpose --dry-run
```

### Step 4: Validate Agent

Always validate generated agents:

```bash
# Validate specific agent
python .claude/skills/agent-creator/scripts/validate_agent.py <agent-name>.md

# Validate all agents
python .claude/skills/agent-creator/scripts/validate_agent.py --all
```

## Agent Customization

### Custom Descriptions

Add domain-specific context to your agent:

```bash
python .claude/skills/agent-creator/scripts/generate_agent.py \
  react-reviewer code-review \
  --description "Specialized code reviewer for React applications with focus on hooks, performance, and accessibility"
```

### Custom Capabilities

Override default capabilities for your specific use case:

```bash
python .claude/skills/agent-creator/scripts/generate_agent.py \
  microservices-deployer deployment \
  --capabilities \
    "Kubernetes deployment automation" \
    "Service mesh configuration" \
    "Container orchestration" \
    "Health monitoring setup"
```

### Custom Tool Access

Restrict or expand tool access as needed:

```bash
python .claude/skills/agent-creator/scripts/generate_agent.py \
  documentation-writer documentation \
  --tools Read Write Edit Grep Glob
```

### Custom Workflow Instructions

Provide domain-specific workflow guidance:

```bash
python .claude/skills/agent-creator/scripts/generate_agent.py \
  blockchain-auditor security \
  --workflow "Focus on smart contract security, DeFi vulnerability patterns, and gas optimization issues"
```

## Agent Types Reference

### Code Review Agent

**Best for**: Development teams needing systematic code quality analysis

**Key Features**:
- Architecture & design analysis (25% weight)
- Code quality assessment (20% weight)
- Security vulnerability detection (20% weight)
- Performance & scalability evaluation (15% weight)
- Testing coverage analysis (10% weight)
- Documentation & API design review (10% weight)

**Quality Threshold**: 80+ points required for progression

### Deployment Agent

**Best for**: DevOps teams managing deployment pipelines

**Key Features**:
- Pre-deployment validation
- Automated deployment execution
- Health check monitoring
- Rollback management
- Post-deployment documentation

**Integration**: Works with CoordinatorAgent for task delegation

### Testing Agent

**Best for**: QA teams ensuring comprehensive testing coverage

**Key Features**:
- Test automation execution
- Coverage report generation (80%+ requirement)
- Quality assurance validation
- Test result analysis
- Performance testing

**Test Types**: Unit, integration, E2E, security, performance

### Documentation Agent

**Best for**: Technical writers and development teams

**Key Features**:
- API documentation generation
- README and guide creation
- Technical writing assistance
- Documentation maintenance
- Example code generation

**Documentation Types**: API docs, user guides, technical specifications

### Security Agent

**Best for**: Security teams and compliance officers

**Key Features**:
- OWASP Top 10 vulnerability scanning
- Security best practices validation
- Compliance assessment
- Risk analysis and categorization
- Security reporting

**Risk Categories**: Critical, High, Medium, Low with remediation timelines

### General Purpose Agent

**Best for**: Complex research and multi-step coordination tasks

**Key Features**:
- Broad research capabilities
- Multi-step task coordination
- Information synthesis
- Problem decomposition
- Full tool access (*)

**Use Cases**: Research projects, problem analysis, cross-functional coordination

## Best Practices

### Agent Naming

Follow these naming conventions:

```bash
# Good examples
code-review-expert
deployment-automator
security-analyzer
documentation-generator
testing-orchestrator

# Use kebab-case
# Include descriptive suffixes
# Make purpose clear from name
```

### Quality Standards

All generated agents should:

- Maintain 80+ quality score thresholds
- Provide clear, actionable feedback
- Follow established coding standards
- Document significant decisions
- Include proper error handling
- Validate inputs and outputs

### Integration Patterns

```bash
# Sequential agent usage
code-review-expert → testing → deployment

# Parallel agent usage
(code-review AND security) → testing

# Research to implementation
general-purpose → specialized-agent
```

## Resources

### scripts/

**Core Scripts:**

- `generate_agent.py` - Main agent generation script with template system
- `init_agent.py` - Directory setup and initialization utility
- `validate_agent.py` - Agent definition validation and quality checking

**Usage Examples:**

```bash
# Generate with all options
python scripts/generate_agent.py \
  my-specialized-agent code-review \
  --description "Custom description here" \
  --capabilities "Custom cap 1" "Custom cap 2" \
  --tools Read Grep Edit Bash \
  --workflow "Custom workflow instructions"

# List available templates
python scripts/generate_agent.py --list-templates

# Initialize directory
python scripts/init_agent.py --init

# Validate all agents
python scripts/validate_agent.py --all
```

### references/

**Documentation Files:**

- `agent_types.md` - Comprehensive reference for all agent types, characteristics, and use cases
- `workflow_patterns.md` - Detailed workflow patterns and quality standards for each agent type

**Key Information:**
- Agent type selection guidelines
- Workflow quality standards
- Integration patterns and best practices
- Error handling patterns
- Performance optimization guidelines

### assets/

**Template Files:**

- `template_example.md` - Example of a generated agent definition file showing proper structure and format

**Purpose:**
- Demonstrates expected output format
- Provides reference for manual customization
- Shows best practices for agent documentation

## Troubleshooting

### Common Issues

**Agent not found after creation:**
```bash
# Restart Claude Code to reload agents
# Verify agent exists in .claude/agents/
ls .claude/agents/
```

**Validation errors:**
```bash
# Check detailed validation output
python scripts/validate_agent.py agent-name.md

# Common fixes:
# - Add missing sections
# - Fix tool references
# - Improve workflow instructions
```

**Directory not found:**
```bash
# Initialize agents directory
python scripts/init_agent.py --init

# Check directory status
python scripts/init_agent.py --status
```

### Getting Help

- Use `--help` flag with any script for usage information
- Check validation output for specific issues
- Review agent type references for proper configuration
- Consult workflow patterns for best practices

---

*This agent-creator skill follows the Miyabi framework principles and integrates with the common library system for consistent environment management.*