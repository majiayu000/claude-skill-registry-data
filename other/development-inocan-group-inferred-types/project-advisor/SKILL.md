---
name: project-advisor
description: Analyzes project requirements and recommends optimal Claude Code configuration with agents, MCP servers, and Skills for sustainable builds with minimal errors
version: 1.0.0
---

# Project Advisor Skill

Intelligent project analysis and recommendation system for Claude Code projects.

## Purpose

When starting a new project or adding Claude Code to an existing project, this Skill helps you:
1. Identify which agents match your workflow needs
2. Select appropriate MCP servers for integrations
3. Recommend Skills for specialized tasks
4. Ensure security best practices
5. Provide working configuration examples

## When to Use This Skill

Use this Skill when:
- **Starting a new project** - Get complete Claude Code setup recommendations
- **Adding automation** - Identify which agents would help
- **Integrating services** - Determine which MCP servers are needed
- **Security review** - Understand security implications
- **Team onboarding** - Help new team members configure Claude Code

## How It Works

### Step 1: Project Analysis

I'll ask you questions about your project:

**Project Type Questions:**
- What are you building? (web app, API, data pipeline, etc.)
- What's your tech stack? (React, Python, PostgreSQL, etc.)
- What external services do you use? (GitHub, Slack, AWS, etc.)
- What workflows need automation? (testing, deployment, docs, etc.)
- What are your security requirements?

**Team Questions:**
- How many developers?
- What's your deployment process?
- Any compliance requirements? (GDPR, HIPAA, SOC2, etc.)

### Step 2: Recommendation Generation

Based on your answers, I'll provide:

**Agent Recommendations:**
- Which agents match your needs
- Why each agent is recommended
- Configuration examples
- Priority order for implementation

**MCP Server Recommendations:**
- Required MCP servers
- Security configurations
- Installation steps
- Environment variable setup

**Skills Recommendations:**
- Useful Skills for your use case
- How to install and use them
- Examples from official Skills repository

**Security Guidance:**
- Security considerations specific to your project
- Required security measures
- Security checklist
- Compliance requirements

### Step 3: Implementation Guide

I'll provide:
- Step-by-step setup instructions
- Working configuration examples
- Links to relevant patterns and documentation
- Timeline estimates
- Common pitfalls to avoid

## Example Interactions

### Example 1: New E-Commerce Web App

**User:** "I'm building an e-commerce web app with React, PostgreSQL, and Stripe payments"

**Project Advisor Response:**

```markdown
# E-Commerce Web Application Analysis

## Project Type: Web Application (E-Commerce)
## Tech Stack: React, PostgreSQL, Stripe
## Risk Level: HIGH (payment processing)

## Recommended Agents

### Priority 1 (Essential)
1. **security-auditor-agent** ⚠️ CRITICAL
   - WHY: Payment processing requires PCI compliance
   - WHEN: Before every deployment
   - CONFIG: See agent-patterns/security-auditor-agent/

2. **webapp-testing-agent**
   - WHY: E-commerce requires reliable UI testing
   - FOCUS: Checkout flow, cart functionality
   - CONFIG: See agent-patterns/webapp-testing-agent/

3. **testing-agent**
   - WHY: Test payment logic and data operations
   - FOCUS: Unit and integration tests
   - CONFIG: See agent-patterns/testing-agent/

### Priority 2 (Highly Recommended)
4. **code-review-agent**
   - WHY: Maintain code quality across team
   - CONFIG: See agent-patterns/code-review-agent/

5. **deployment-agent**
   - WHY: Safe, automated deployments
   - CONFIG: See agent-patterns/deployment-agent/

## Recommended MCP Servers

1. **@modelcontextprotocol/server-postgres** (Database)
   Security: Use read-only user when possible
   ```json
   {"postgres": {"args": ["-y", "@model contextprotocol/server-postgres", "${DATABASE_URL}"]}}
   ```

2. **@modelcontextprotocol/server-github** (Version Control)
   Security: Minimal token scopes
   ```json
   {"github": {"env": {"GITHUB_TOKEN": "${GITHUB_TOKEN}"}}}
   ```

3. **@modelcontextprotocol/server-fetch** (Stripe API)
   Security: Review all API calls
   ```json
   {"fetch": {"args": ["-y", "@modelcontextprotocol/server-fetch"]}}
   ```

4. **@modelcontextprotocol/server-puppeteer** (E2E Testing)
   ```json
   {"puppeteer": {"args": ["-y", "@modelcontextprotocol/server-puppeteer"]}}
   ```

## Security Requirements

⚠️ **CRITICAL - Payment Processing Security:**
- PCI DSS compliance required
- Never log credit card numbers
- HTTPS only
- Secrets in environment variables
- Regular security audits
- Stripe webhook signature verification

## Implementation Steps

1. Run security review: /security-check
2. Configure security-auditor-agent (Priority 1!)
3. Set up PostgreSQL MCP with limited user
4. Configure Stripe in test mode first
5. Set up testing agents
6. Implement checkout flow with tests
7. Security audit before production
8. Deploy with deployment-agent

## Estimated Timeline
- Setup: 3-5 days
- Security configuration: 2-3 days
- Agent integration: 1 week
- Testing setup: 1 week

## Critical Warnings
❌ DO NOT deploy to production without security audit
❌ DO NOT hardcode Stripe keys
❌ DO NOT skip E2E tests for checkout flow
✅ DO run /security-check before every deploy
✅ DO use test mode for Stripe during development
✅ DO implement rate limiting
```

### Example 2: Backend API

**User:** "Building a Python FastAPI backend with PostgreSQL"

**Project Advisor Response:**

```markdown
# Backend API Analysis

## Recommended Agents
1. testing-agent (API tests)
2. documentation-agent (OpenAPI docs)
3. security-auditor-agent (API security)
4. deployment-agent (CI/CD)

## Recommended MCPs
1. postgres (database access)
2. github (version control)
3. fetch (external API testing)

## Security Focus
- API authentication/authorization
- Rate limiting
- Input validation
- SQL injection prevention

## Next Steps
1. Configure testing-agent for API tests
2. Set up documentation-agent for OpenAPI spec
3. Implement security scanning
4. Set up CI/CD pipeline
```

## Using This Skill

### In Claude Code

Simply describe your project:

```
I'm building a [type] project with [tech stack] that needs [features]
```

I'll analyze your requirements and provide tailored recommendations.

### Common Questions I Can Answer

**"What agents should I use for my project?"**
→ I'll analyze your project type and recommend specific agents

**"Which MCP servers do I need?"**
→ I'll identify integrations and suggest MCP servers

**"Is my configuration secure?"**
→ I'll review security implications and suggest improvements

**"How do I get started?"**
→ I'll provide step-by-step setup instructions

**"What's the best way to structure my Claude Code setup?"**
→ I'll recommend a phased approach based on priorities

## Knowledge Base

This Skill draws from:
- `advisors/project-advisor.md` - Detailed analysis logic
- `decision-trees/` - Quick decision guides
- `agent-patterns/` - Agent configurations
- `mcp-catalog/` - MCP server details
- `security/` - Security best practices
- `reference-repos/` - Official examples

## Best Practices

**For Best Results:**
1. Be specific about your tech stack
2. Mention external services you need
3. Note any security/compliance requirements
4. Describe your team size
5. Specify your deployment environment

**Good Example:**
"Building a React SaaS app with Stripe payments, PostgreSQL database, deployed on Vercel, team of 5 developers, need GDPR compliance"

**Vague Example:**
"Making a web app" (I'll ask follow-up questions)

## Continuous Improvement

This Skill stays current by referencing:
- Official Anthropic Skills repository
- Latest Agent SDK documentation
- Current MCP server catalog
- Updated security best practices

Update reference repositories weekly:
```bash
./update-references.sh
```

## Related Skills

- **agent-recommender-skill** - Focused on agent selection
- **mcp-recommender-skill** - Focused on MCP integration
- **security-auditor-skill** - Security-focused analysis

## Version History

- v1.0.0 (2025-10-18) - Initial release with comprehensive project analysis
