---
name: field-agent-deployment
description: Best practices for developing, testing, and deploying production-ready Field Agents including R&D workflows, version control, testing strategies, and release management
---

# Field Agent Deployment Best Practices

This skill provides comprehensive guidelines for the complete lifecycle of Field Agent development and deployment, from initial R&D through production release.

## When to Use This Skill

Use this skill when you need help with:
- Setting up a Field Agent development workflow
- Structuring a Field Agent project for production
- Creating deployment pipelines for Field Agents
- Implementing testing strategies for Field Agents
- Publishing and releasing Field Agent updates
- Managing Field Agent environments (dev, staging, prod)

## Development Workflow

### R&D Phase Best Practices

#### 1. Project Initiation
Before starting new agent development:

```markdown
## Pre-Development Checklist
- [ ] Validate use case and business requirements
- [ ] Review existing agent catalog to avoid duplication
- [ ] Get stakeholder approval for new agent development
- [ ] Document initial requirements and expected outcomes
- [ ] Set up team communication channel
- [ ] Publish initial draft documentation to alert team
```

#### 2. Environment Strategy

**Development Environments:**
- R&D can occur in any development environment
- Production deployment requires dedicated production instance
- Use environment variables for instance-specific configurations

## Production Publishing Workflow

### Step-by-Step Publishing Process

#### Phase 1: Preparation
```markdown
1. Code Freeze
   - Ensure all features are complete and tested
   - No new features during release cycle
   - Bug fixes only with approval

2. Quality Gates
   - All unit tests passing
   - Integration tests successful
   - Performance benchmarks met
   - Security scan completed
   - Documentation updated
```

#### Phase 2: Pre-Release Testing

**End-to-End Testing Checklist:**
```markdown
- [ ] Test all primary use cases in staging environment
- [ ] Verify tool integrations and data access
- [ ] Validate error handling and edge cases
- [ ] Test with various input formats and user prompts
- [ ] Verify output format consistency
- [ ] Check resource usage (iterations, tokens, runtime)
- [ ] Test timeout and failure scenarios
- [ ] Validate permissions and access control
```

#### Phase 3: Production Deployment

**Deployment Checklist:**
```markdown
## Pre-Deployment
- [ ] Clone/update production repository
- [ ] Export agent configuration from staging
- [ ] Review and validate all configuration files
- [ ] Verify README.md is complete and accurate
- [ ] Check environment-specific variables

## Database & Dependencies
- [ ] Migrate required databases to production instance
- [ ] Verify table schemas match expectations
- [ ] Validate data access permissions
- [ ] Test external API connections
- [ ] Confirm tool dependencies are available

## Deployment
- [ ] Push agent to production instance
- [ ] Verify agent appears in production catalog
- [ ] Test agent activation and loading
- [ ] Run smoke tests in production
- [ ] Monitor initial executions for errors

## Post-Deployment
- [ ] Record demo video of production usage
- [ ] Update documentation with production links
- [ ] Announce release to stakeholders
- [ ] Set up monitoring and alerting
- [ ] Schedule post-deployment review
```

**Deployment Script Template:**
```bash
#!/bin/bash
# deploy-agent.sh

set -e  # Exit on error

AGENT_NAME="customer-segmentation-agent"
PROD_INSTANCE="prod-instance-id"
GITHUB_REPO="https://github.com/your-org/field-agents"

echo "Starting deployment for ${AGENT_NAME}..."

# Step 1: Clone/update repository
if [ -d "field-agents" ]; then
    cd field-agents && git pull origin main && cd ..
else
    git clone ${GITHUB_REPO}
fi

# Step 2: Push to production (use your deployment tool)
echo "Deploying to production instance ${PROD_INSTANCE}..."
# TODO: Replace with your actual deployment command
# Example placeholder: td-agent-cli push --instance ${PROD_INSTANCE} --agent ${AGENT_NAME}
# For TD deployments, consult your infrastructure team for the correct deployment tool

echo "Deployment completed successfully!"
```

## Documentation Standards

### Required Documentation Components

#### 1. README.md Template
```markdown
# [Agent Name]

Brief one-line description of what this agent does.

## Overview
Detailed description of agent purpose, capabilities, and business value.

## Quick Start
\```
# Example usage
[Show simplest possible usage example]
\```

## Features
- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## Prerequisites
- Treasure Data instance access
- Required databases: [list databases]
- Required tools/integrations: [list tools]

## Installation
Step-by-step installation instructions

## Usage
Common usage patterns and examples

## Configuration
Configuration options and parameters

## Troubleshooting
Common issues and solutions

## Contributing
Guidelines for contributions (if applicable)

## License & Support
License information and support contacts
```

#### 2. Technical Documentation
```markdown
# [Agent Name] - Technical Documentation

## Architecture Overview
High-level architecture diagram and component description

## System Prompt
Link to or excerpt of system prompt

## Tools & Functions
Detailed description of each tool:
- Function name
- Purpose
- Input parameters
- Output format
- Example usage

## Data Flow
Describe how data flows through the agent

## Performance Characteristics
- Average execution time
- Token usage patterns
- Resource requirements

## Security & Permissions
Required permissions and security considerations

## Version History
Major versions and changes
```

#### 3. Demo & Examples

**Create Demo Content:**
```markdown
## Demo Video Requirements
- Length: 2-5 minutes
- Show: Primary use case walkthrough
- Include: Input prompt, execution, output
- Highlight: Key features and benefits
- Format: Screen recording with audio narration

## Sample Conversations
Provide 3-5 example conversations:
1. Basic/common use case
2. Advanced use case with options
3. Error handling example
4. Edge case handling
5. Integration with other tools
```

## Release Management

### Version Numbering

Use semantic versioning (MAJOR.MINOR.PATCH):
```
1.0.0 - Initial production release
1.1.0 - New feature added
1.1.1 - Bug fix
2.0.0 - Breaking change
```

### Release Notes Template

```markdown
# Release Notes - v1.2.0

## Release Date
2024-11-15

## Summary
Brief overview of this release

## New Features
- Feature 1: Description and benefit
- Feature 2: Description and benefit

## Improvements
- Improvement 1: What was enhanced
- Improvement 2: Performance optimization details

## Bug Fixes
- Fix 1: Issue resolved
- Fix 2: Error corrected

## Breaking Changes
- Change 1: What changed and migration path
- Change 2: Required updates

## Migration Guide
Step-by-step instructions for upgrading from previous version

## Known Issues
- Issue 1: Workaround if available
- Issue 2: Expected fix timeline
```

### Communication Protocol

**Release Announcement Template:**
```markdown
Subject: [RELEASED] [Agent Name] v1.2.0 - [Key Feature]

Team,

We've released version 1.2.0 of [Agent Name] to production.

**Key Updates:**
• New feature: [Feature name and benefit]
• Improvement: [Performance/usability improvement]
• Bug fix: [Critical fix]

**Links:**
• Production Agent: [link]
• Documentation: [link]
• Demo Video: [link]
• Release Notes: [link]

**Action Required:**
[Any required actions for users/teams]

**Support:**
For questions or issues, contact [support channel/person]

Thanks,
[Your Name]
```

## Monitoring & Maintenance

### Maintenance Schedule

```markdown
## Regular Maintenance Tasks

### Daily
- Review error logs
- Monitor execution metrics
- Check system health

### Weekly
- Review performance trends
- Update documentation if needed
- Check for dependency updates

### Monthly
- Security audit
- Performance optimization review
- User feedback collection and analysis
- Roadmap planning

### Quarterly
- Major version planning
- Architecture review
- Disaster recovery testing
```

## Troubleshooting Guide

### Common Deployment Issues

```markdown
## Issue: Agent Not Appearing in Production

**Symptoms:** Agent deployed but not visible in catalog

**Possible Causes:**
1. Configuration file not properly formatted
2. Agent ID conflict with existing agent
3. Permissions not set correctly

**Solutions:**
1. Validate JSON configuration files
2. Check for ID conflicts in production catalog
3. Verify production instance permissions

## Issue: Tools Failing in Production

**Symptoms:** Tools work in dev but fail in production

**Possible Causes:**
1. Database not migrated to production
2. API credentials not configured
3. Network/firewall restrictions

**Solutions:**
1. Verify database exists: `td db:list | grep [db_name]`
2. Check environment variables and secrets
3. Test network connectivity to external services

## Issue: Poor Performance in Production

**Symptoms:** Agent slower than expected

**Possible Causes:**
1. Large dataset queries without optimization
2. Too many tool iterations
3. Inefficient system prompt

**Solutions:**
1. Add query filters and limits
2. Reduce max_tool_iterations setting
3. Optimize system prompt for efficiency
```

## Best Practices Summary

### Do's ✅
- Always test thoroughly before production deployment
- Use version control for all agent components
- Document every configuration change
- Create comprehensive test suites
- Monitor production usage and errors
- Keep dependencies updated
- Follow semantic versioning
- Communicate releases to stakeholders

### Don'ts ❌
- Don't deploy untested changes to production
- Don't skip documentation updates
- Don't hardcode environment-specific values
- Don't deploy without backup/rollback plan
- Don't ignore error logs and metrics
- Don't make breaking changes without migration guide
- Don't deploy during peak usage hours without notice

## Resources & Tools

### Recommended Development Tools
- **Version Control:** Git with GitHub/GitLab
- **CI/CD:** GitHub Actions, GitLab CI, or Jenkins
- **Monitoring:** Application logging and metrics collection
- **Documentation:** Markdown with auto-generated API docs
