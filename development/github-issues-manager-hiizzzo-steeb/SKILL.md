---
name: github-issues-manager
description: Connect Claude Code with GitHub Issues for rapid problem resolution. This skill should be used when users need to manage, analyze, prioritize, and resolve GitHub issues automatically without manual intervention.
---

# GitHub Issues Manager

This skill provides seamless integration between Claude Code and GitHub Issues, enabling rapid issue detection, analysis, prioritization, and automated resolution workflows for STEEB application development.

## When to Use This Skill

Use this skill when:
- Automatically detecting new GitHub issues in STEEB repository
- Analyzing and categorizing incoming issues
- Prioritizing issues based on impact and user feedback
- Creating automated issue responses and solutions
- Tracking issue resolution progress
- Generating issue reports and statistics
- Managing issue workflows and assignments
- Creating pull requests for issue fixes

## Core Capabilities

### 1. Issue Detection and Analysis
- Monitor new issues in real-time
- Analyze issue content for categorization
- Extract key information and requirements
- Identify duplicate or related issues
- Assess issue severity and impact level

### 2. Automated Issue Triage
- Categorize issues by type (bug, feature, enhancement, etc.)
- Prioritize based on user reactions and business impact
- Assign appropriate labels and milestones
- Estimate complexity and effort required
- Detect blocking issues that need immediate attention

### 3. Issue Resolution Automation
- Generate code fixes for common issues
- Create pull requests automatically
- Update issue status and comments
- Link related issues and pull requests
- Generate test cases for resolved issues

### 4. Workflow Management
- Track issue lifecycle from creation to resolution
- Generate comprehensive reports and analytics
- Monitor development team performance
- Identify recurring patterns and systemic issues

## Issue Categories and Detection

### Bug Issues
**Detection Patterns:**
- Keywords: "bug", "error", "crash", "broken", "not working"
- Error messages, stack traces, console logs
- Screenshots showing incorrect behavior
- Performance degradation reports

**Automated Actions:**
- Reproduce bug in development environment
- Create minimal reproduction case
- Generate test case for bug verification
- Suggest code fixes based on common patterns

### Feature Requests
**Detection Patterns:**
- Keywords: "feature", "add", "implement", "new functionality"
- User stories or requirement specifications
- Mockups or design screenshots
- Competitive feature analysis

**Automated Actions:**
- Analyze feature complexity
- Create development timeline
- Generate implementation plan
- Identify dependencies and blockers

### Enhancement Requests
**Detection Patterns:**
- Keywords: "improve", "optimize", "enhance", "better"
- Performance improvement suggestions
- UX/UI improvement proposals
- Code optimization opportunities

**Automated Actions:**
- Measure current performance baseline
- Identify optimization opportunities
- Generate performance benchmarks
- Create improvement implementation plan

### Documentation Issues
**Detection Patterns:**
- Keywords: "docs", "documentation", "readme", "guide"
- Missing or outdated information
- API documentation requests
- User manual improvements

**Automated Actions:**
- Update relevant documentation files
- Generate code examples
- Create user guides
- Update README and API docs

## Automated Workflows

### Issue Triage Workflow
```yaml
Trigger: New Issue Created
Steps:
  1. Analyze issue content and attachments
  2. Categorize issue type (bug/feature/enhancement/docs)
  3. Assess severity and impact level
  4. Assign appropriate labels
  5. Estimate complexity and timeline
  6. Assign to appropriate developer/team
  7. Set milestone and priority
  8. Generate initial response
```

### Bug Resolution Workflow
```yaml
Trigger: Bug Issue Detected
Steps:
  1. Extract error details and reproduction steps
  2. Analyze codebase for related code
  3. Create minimal reproduction case
  4. Generate potential fix
  5. Create automated test case
  6. Implement fix in development branch
  7. Create pull request
  8. Link to original issue
  9. Request code review
  10. Update issue with fix status
```

### Feature Implementation Workflow
```yaml
Trigger: Feature Request Approved
Steps:
  1. Analyze requirements and specifications
  2. Design implementation approach
  3. Break down into development tasks
  4. Create development timeline
  5. Implement feature in feature branch
  6. Add tests and documentation
  7. Create pull request
  8. Request review and testing
  9. Merge to main branch
  10. Update issue with implementation status
```

## Scripts and Automation Tools

### Issue Monitor Script
```bash
# Monitor new issues and trigger automated workflows
python .claude/skills/github-issues-manager/scripts/monitor_issues.py --repo santi-billy1/stebe --webhook
```

### Issue Analyzer Script
```bash
# Analyze existing issues and generate insights
python .claude/skills/github-issues-manager/scripts/analyze_issues.py --repo santi-billy1/stebe --output report.json
```

### Automated Fix Generator
```bash
# Generate code fixes for common issue patterns
python .claude/skills/github-issues-manager/scripts/generate_fix.py --issue-number 123 --create-pr
```

### Issue Reporter Script
```bash
# Generate comprehensive issue reports
python .claude/skills/github-issues-manager/scripts/issue_report.py --repo santi-billy1/stebe --period monthly
```

## Issue Response Templates

### Bug Response Template
```markdown
## 🔍 Bug Analysis

**Issue:** {{issue_title}}
**Severity:** {{severity_level}}
**Affected Users:** {{user_count}}

### 🐛 Problem Description
{{extracted_description}}

### 🔧 Investigation Results
{{analysis_results}}

### 💡 Proposed Solution
{{solution_proposal}}

### ⏱️ Implementation Timeline
{{implementation_timeline}}

### 📋 Action Items
- [ ] {{action_item_1}}
- [ ] {{action_item_2}}
- [ ] {{action_item_3}}

### 🚀 Status
- **Current Status:** {{current_status}}
- **Next Update:** {{next_update}}
```

### Feature Request Response Template
```markdown
## ✨ Feature Request Analysis

**Request:** {{issue_title}}
**Requester:** {{user_name}}
**Priority:** {{priority_level}}

### 📋 Requirements Analysis
{{requirements_analysis}}

### 🎯 Implementation Plan
{{implementation_plan}}

### ⏰ Development Timeline
{{development_timeline}}

### 📊 Impact Assessment
{{impact_assessment}}

### 🔄 Status Updates
- **Requirements:** {{requirements_status}}
- **Design:** {{design_status}}
- **Development:** {{development_status}}
- **Testing:** {{testing_status}}
- **Deployment:** {{deployment_status}}
```

## Integration with STEEB Development

### Repository Configuration
- **Repository:** `santi-billy1/stebe`
- **Main Branch:** `main`
- **Development Branches:** `feature/*`, `bugfix/*`, `hotfix/*`
- **Protected Branches:** `main`, `develop`

### Issue Labels
- **Type:** `bug`, `feature`, `enhancement`, `documentation`, `question`
- **Priority:** `critical`, `high`, `medium`, `low`
- **Status:** `new`, `in-progress`, `review`, `testing`, `done`
- **Component:** `ui`, `backend`, `database`, `api`, `mobile`, `web`

### Team Members and Assignees
- **Maintainer:** Santiago Benítez (Santi)
- **Developers:** BillyBoy Team members
- **Designers:** UI/UX team
- **Testers:** QA team

## Performance Metrics and KPIs

### Issue Resolution Metrics
- **Time to First Response:** < 24 hours for new issues
- **Time to Resolution:** < 7 days for bugs, < 14 days for features
- **Resolution Rate:** > 90% of issues resolved within SLA
- **Customer Satisfaction:** > 4.5/5 rating from issue reporters

### Development Metrics
- **Code Quality:** 90%+ test coverage for bug fixes
- **Deployment Frequency:** Multiple deployments per week
- **Lead Time:** < 3 days from PR to merge
- **Change Failure Rate:** < 5% of deployments cause issues

## API Integration Points

### GitHub API Endpoints
```javascript
// Issue Management
GET /repos/{owner}/{repo}/issues
POST /repos/{owner}/{repo}/issues
PATCH /repos/{owner}/{repo}/issues/{issue_number}

// Pull Request Management
GET /repos/{owner}/{repo}/pulls
POST /repos/{owner}/{repo}/pulls
PATCH /repos/{owner}/{repo}/pulls/{pull_number}

// Repository Management
GET /repos/{owner}/{repo}
GET /repos/{owner}/{repo}/branches
GET /repos/{owner}/{repo}/labels
```

### Webhook Events
- `issues.opened` - New issue created
- `issues.closed` - Issue resolved
- `pull_request.opened` - New PR created
- `pull_request.closed` - PR merged
- `push` - Code pushed to repository

## Error Handling and Recovery

### Common Error Scenarios
- **GitHub API Rate Limiting:** Implement exponential backoff
- **Authentication Issues:** Refresh tokens and re-authenticate
- **Network Failures:** Retry with circuit breaker pattern
- **Invalid Issue Data:** Validate and sanitize input data

### Recovery Procedures
```bash
# Restart monitoring services
python scripts/restart_monitoring.py

# Resync issue data
python scripts/resync_issues.py --force

# Validate issue integrity
python scripts/validate_issues.py --fix-errors
```

## Security and Privacy

### Access Control
- **GitHub Token:** Secure storage with rotation policies
- **Repository Permissions:** Minimum required permissions
- **Data Encryption:** Encrypt sensitive issue data
- **Audit Logging:** Log all issue management actions

### Privacy Considerations
- **User Data:** Anonymize personal information
- **Code Analysis:** Handle proprietary code securely
- **Communication:** Secure communication channels
- **Data Retention:** Retain data only as long as necessary

## References and Resources

### GitHub Documentation
- GitHub REST API reference
- GitHub GraphQL API documentation
- GitHub Actions workflows
- GitHub Webhooks configuration

### STEEB Development Resources
- STEEB repository structure and conventions
- STEEB coding standards and guidelines
- STEEB testing framework and practices
- STEEB deployment and CI/CD processes

### Integration Tools
- GitHub CLI (`gh`) command-line interface
- GitHub API client libraries
- Webhook management platforms
- Issue tracking and project management tools