---
name: onboarding-docs
description: Developer onboarding documentation and learning paths
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Onboarding Documentation Skill

## When to Use This Skill

Use this skill when:

- **Onboarding Docs tasks** - Working on developer onboarding documentation and learning paths
- **Planning or design** - Need guidance on Onboarding Docs approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Create comprehensive developer onboarding documentation for accelerated productivity.

## MANDATORY: Documentation-First Approach

Before creating onboarding docs:

1. **Invoke `docs-management` skill** for onboarding patterns
2. **Verify developer experience best practices** via MCP servers (perplexity)
3. **Base guidance on industry onboarding standards**

## Onboarding Documentation Framework

```text
Onboarding Documentation Layers:

┌─────────────────────────────────────────────────────────────────────────────┐
│  Day 1: Environment Setup                                                    │
│  • Development environment installation                                      │
│  • Access provisioning and credentials                                       │
│  • Tool configuration                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  Week 1: Core Concepts                                                       │
│  • Architecture overview                                                     │
│  • Codebase orientation                                                      │
│  • Development workflow                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  Month 1: Deep Dive                                                          │
│  • Domain knowledge                                                          │
│  • System internals                                                          │
│  • Advanced workflows                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  Ongoing: Reference Materials                                                │
│  • API documentation                                                         │
│  • Runbooks and procedures                                                   │
│  • Best practices and standards                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Onboarding Guide Template

````markdown
# Developer Onboarding Guide

Welcome to [Project/Team Name]! This guide will help you get productive quickly.

---

## Quick Links

| Resource | Link | Purpose |
|----------|------|---------|
| Codebase | [GitHub Repo] | Source code |
| Documentation | [Docs Site] | Technical docs |
| Issue Tracker | [Jira/GitHub] | Tasks and bugs |
| CI/CD | [Azure DevOps/GitHub Actions] | Build pipelines |
| Monitoring | [Grafana/DataDog] | Metrics and alerts |
| Chat | [Slack/Teams] | Team communication |

---

## Day 1 Checklist

### Access Setup

- [ ] GitHub organization invite accepted
- [ ] Azure subscription access granted
- [ ] Slack/Teams workspace joined
- [ ] VPN configured (if applicable)
- [ ] Password manager setup
- [ ] MFA enabled on all accounts

### Development Environment

- [ ] IDE installed and configured
- [ ] Required SDKs installed
- [ ] Repository cloned
- [ ] Project builds locally
- [ ] Tests run successfully

### First Steps

- [ ] Read this onboarding guide
- [ ] Review team conventions
- [ ] Meet your onboarding buddy
- [ ] Schedule 1:1 with team lead

---

## Environment Setup

### Prerequisites

| Tool | Version | Installation |
|------|---------|--------------|
| .NET SDK | 10.0+ | [Download](https://dot.net) |
| Node.js | 22 LTS | [Download](https://nodejs.org) |
| Docker Desktop | Latest | [Download](https://docker.com) |
| Git | 2.40+ | [Download](https://git-scm.com) |
| VS Code / Rider | Latest | IDE of choice |

### Step-by-Step Setup

#### 1. Install Prerequisites

**Windows (winget):**
```powershell
winget install Microsoft.DotNet.SDK.10
winget install OpenJS.NodeJS.LTS
winget install Docker.DockerDesktop
winget install Git.Git
winget install Microsoft.VisualStudioCode
```

**macOS (Homebrew):**

```bash
brew install --cask dotnet-sdk
brew install node@22
brew install --cask docker
brew install git
brew install --cask visual-studio-code
```

#### 2. Clone Repository

```bash
# Clone the main repository
git clone https://github.com/org/project.git
cd project

# Install dependencies
dotnet restore
npm install
```

#### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env.local

# Edit with your values
code .env.local
```

**Required Environment Variables:**

| Variable | Description | How to Get |
|----------|-------------|------------|
| `DATABASE_URL` | PostgreSQL connection | Use local Docker or dev DB |
| `AZURE_CLIENT_ID` | Azure service principal | Request from team lead |
| `API_KEY` | External API key | 1Password vault |

#### 4. Start Development Environment

```bash
# Start infrastructure (database, cache, etc.)
docker compose up -d

# Run database migrations
dotnet ef database update

# Start the application
dotnet run
```

#### 5. Verify Setup

```bash
# Run tests
dotnet test

# Check API health
curl http://localhost:5000/health
```

**Expected Output:**

```json
{
  "status": "Healthy",
  "checks": {
    "database": "Healthy",
    "cache": "Healthy"
  }
}
```

---

## Architecture Overview

### System Context

[Include C4 Context Diagram]

### High-Level Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Load Balancer                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
            ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
            │   Web App    │ │   API        │ │   Worker     │
            │   (Blazor)   │ │   (.NET)     │ │   Service    │
            └──────────────┘ └──────────────┘ └──────────────┘
                    │                │                │
                    └────────────────┼────────────────┘
                                     ▼
                         ┌─────────────────────┐
                         │     PostgreSQL      │
                         └─────────────────────┘
```

### Key Components

| Component | Purpose | Tech Stack |
|-----------|---------|------------|
| Web App | User interface | Blazor, Tailwind CSS |
| API | Backend services | .NET 10, Minimal APIs |
| Worker | Background jobs | .NET Worker Service |
| Database | Data persistence | PostgreSQL 16 |
| Cache | Performance | Redis |
| Queue | Async messaging | Azure Service Bus |

---

## Codebase Orientation

### Repository Structure

```text
project/
├── src/
│   ├── Web/                    # Blazor frontend
│   ├── Api/                    # Backend API
│   ├── Worker/                 # Background services
│   └── SharedKernel/           # Shared code
├── tests/
│   ├── Unit/                   # Unit tests
│   ├── Integration/            # Integration tests
│   └── E2E/                    # End-to-end tests
├── docs/                       # Documentation
├── scripts/                    # Utility scripts
├── .github/                    # GitHub workflows
└── docker-compose.yml          # Local development
```

### Key Files to Review

| File | Purpose | Priority |
|------|---------|----------|
| `README.md` | Project overview | Day 1 |
| `CONTRIBUTING.md` | Contribution guidelines | Day 1 |
| `src/Api/Program.cs` | API entry point | Week 1 |
| `src/SharedKernel/Domain/` | Domain models | Week 1 |
| `docs/architecture/` | Architecture docs | Week 1 |

### Code Conventions

**Naming:**

- Classes: `PascalCase`
- Methods: `PascalCase`
- Variables: `camelCase`
- Constants: `UPPER_SNAKE_CASE`
- Files: Match class name

**Project Structure:**

- Vertical slice architecture
- Feature folders over layer folders
- One class per file (with exceptions for records)

---

## Development Workflow

### Git Workflow

```text
main ────────────────────────────────────────────────────────►
       │                                          │
       └── feature/ABC-123-add-user-auth ─────────┘
             │     │     │
             ▼     ▼     ▼
          commit commit commit
```

**Branch Naming:**

- `feature/TICKET-description` - New features
- `fix/TICKET-description` - Bug fixes
- `chore/description` - Maintenance tasks

**Commit Messages:**

```text
type(scope): description

feat(auth): add OAuth2 support for Azure AD
fix(api): resolve null reference in user service
docs(readme): update installation instructions
```

### Code Review Process

1. Create feature branch from `main`
2. Make changes with meaningful commits
3. Push and create pull request
4. Request review from team member
5. Address feedback
6. Merge when approved (squash merge)

### Testing Requirements

- All new code must have tests
- Minimum 80% code coverage for new features
- Integration tests for API endpoints
- E2E tests for critical user flows

```bash
# Run all tests
dotnet test

# Run with coverage
dotnet test --collect:"XPlat Code Coverage"

# Run specific test project
dotnet test tests/Unit/
```

---

## Common Tasks

### Adding a New API Endpoint

1. Create feature folder in `src/Api/Features/`
2. Add request/response models
3. Implement endpoint handler
4. Add validation
5. Write tests
6. Update OpenAPI documentation

**Example:**

```csharp
// src/Api/Features/Users/GetUser.cs
public static class GetUser
{
    public sealed record Response(Guid Id, string Name, string Email);

    public static void Map(IEndpointRouteBuilder app) =>
        app.MapGet("/api/users/{id:guid}", HandleAsync)
           .WithName("GetUser")
           .WithTags("Users")
           .Produces<Response>()
           .ProducesProblem(StatusCodes.Status404NotFound);

    private static async Task<IResult> HandleAsync(
        Guid id,
        IUserRepository repository,
        CancellationToken ct)
    {
        var user = await repository.GetByIdAsync(id, ct);
        return user is null
            ? Results.NotFound()
            : Results.Ok(new Response(user.Id, user.Name, user.Email));
    }
}
```

### Running Database Migrations

```bash
# Add a new migration
dotnet ef migrations add AddUserTable -p src/Api -s src/Api

# Apply migrations
dotnet ef database update -p src/Api -s src/Api

# Generate SQL script
dotnet ef migrations script -p src/Api -s src/Api -o migration.sql
```

### Debugging

**VS Code:**

1. Set breakpoint (F9)
2. Start debugging (F5)
3. Use debug console for evaluation

**Rider:**

1. Set breakpoint
2. Debug (Shift+F9)
3. Use Evaluate Expression

**Logging:**

```csharp
_logger.LogInformation("Processing request {RequestId}", requestId);
_logger.LogError(exception, "Failed to process {RequestId}", requestId);
```

---

## Learning Path

### Week 1: Foundations

| Day | Topic | Resources |
|-----|-------|-----------|
| 1 | Environment setup | This guide |
| 2 | Architecture overview | `/docs/architecture/` |
| 3 | Codebase walkthrough | Pair with buddy |
| 4 | First bug fix | Assigned starter issue |
| 5 | Code review | Review teammate's PR |

### Week 2-4: Building Competence

- [ ] Complete a small feature end-to-end
- [ ] Write integration tests
- [ ] Participate in sprint planning
- [ ] Present at team standup
- [ ] Shadow on-call rotation

### Month 2-3: Independence

- [ ] Own a medium-sized feature
- [ ] Mentor newer team members
- [ ] Contribute to documentation
- [ ] Join on-call rotation
- [ ] Present technical topic to team

---

## Getting Help

### Onboarding Buddy

Your onboarding buddy is: **[Name]**

- Slack: @[handle]
- Email: [email]

They're your first point of contact for questions!

### Team Channels

| Channel | Purpose |
|---------|---------|
| #team-[name] | General team discussion |
| #team-[name]-dev | Technical questions |
| #incidents | Production issues |
| #random | Non-work chat |

### Escalation

If you're blocked:

1. **Try self-service first**: Search docs, Slack history, Stack Overflow
2. **Ask in team channel**: Others may have same question
3. **Direct message buddy**: For quick questions
4. **Schedule 1:1**: For longer discussions

---

## FAQ

**Q: How do I get access to [system]?**
A: Request in #access-requests channel with your manager's approval.

**Q: Where do I find [documentation]?**
A: Start at [docs-site-url]. Use search or ask in #team-dev.

**Q: What should I do if tests fail on CI?**
A: Check the CI logs first. If unclear, ask in #team-dev with a link to the failed build.

**Q: How do I deploy to staging?**
A: Merging to `main` auto-deploys to staging. Check #deployments channel.

---

## Feedback

We continuously improve our onboarding process. Please share your experience:

- What worked well?
- What was confusing?
- What was missing?

Send feedback to: [email/form/channel]

---

**Next Review:** [Date]

````

## Learning Path Template

```markdown
# Learning Path: [Role/Technology]

## Overview

This learning path helps you become proficient in [topic].

**Estimated Duration:** [X] weeks
**Prerequisites:** [List]

---

## Level 1: Fundamentals (Week 1)

### Goals

- [ ] Understand core concepts
- [ ] Set up development environment
- [ ] Complete "Hello World" tutorial

### Resources

| Type | Resource | Time |
|------|----------|------|
| Video | [Introduction to X] | 30 min |
| Tutorial | [Getting Started] | 2 hours |
| Documentation | [Core Concepts] | 1 hour |

### Exercises

1. [Exercise 1]
2. [Exercise 2]

### Checkpoint

- Can you explain [concept] in your own words?
- Have you built [artifact]?

---

## Level 2: Intermediate (Weeks 2-3)

### Goals

- [ ] Build a complete feature
- [ ] Understand [advanced topic]
- [ ] Write tests

### Resources

| Type | Resource | Time |
|------|----------|------|
| Course | [Deep Dive into X] | 4 hours |
| Book | [Recommended Reading] Chapter 1-5 | 3 hours |
| Practice | [Hands-on Lab] | 2 hours |

### Project

Build [project description] that demonstrates:
- [Skill 1]
- [Skill 2]
- [Skill 3]

### Checkpoint

- Can you [task] without referring to documentation?
- Have you completed the [project]?

---

## Level 3: Advanced (Weeks 4+)

### Goals

- [ ] Optimize for performance
- [ ] Handle edge cases
- [ ] Mentor others

### Resources

| Type | Resource | Time |
|------|----------|------|
| Advanced | [Performance Optimization] | 2 hours |
| Case Study | [Real-world Examples] | 1 hour |
| Community | [Contribute to OSS] | Ongoing |

### Milestone

You've reached proficiency when you can:
- [ ] Design solutions independently
- [ ] Review others' code confidently
- [ ] Explain trade-offs to stakeholders
```

## Best Practices

### Content Principles

| Principle | Description |
|-----------|-------------|
| **Progressive** | Start simple, increase complexity |
| **Practical** | Focus on doing, not just reading |
| **Current** | Keep up-to-date with system changes |
| **Accessible** | Easy to find and navigate |
| **Feedback-driven** | Iterate based on new hire input |

### Anti-Patterns to Avoid

- Overwhelming Day 1 with too much information
- Assuming prior knowledge without verification
- Outdated setup instructions
- No checkpoint/verification steps
- Missing "getting help" information

## Workflow

When creating onboarding docs:

1. **Audit Current State**: What exists? What's outdated?
2. **Interview Recent Hires**: What was confusing? Missing?
3. **Define Learning Goals**: What should they know at each stage?
4. **Create Progressive Content**: Day 1 → Week 1 → Month 1
5. **Add Verification Steps**: How do they know they succeeded?
6. **Test with Real User**: Have someone follow the guide
7. **Iterate**: Update based on feedback

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
