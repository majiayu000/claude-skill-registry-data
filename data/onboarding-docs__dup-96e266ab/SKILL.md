---
name: Developer Onboarding Documentation
description: Comprehensive onboarding documentation to get new developers productive quickly with clear guides, checklists, and resources.
---

# Developer Onboarding Documentation

## Overview

Developer Onboarding Documentation provides new team members with everything they need to become productive quickly. Good onboarding reduces time-to-first-commit from weeks to days.

**Core Principle**: "New developers should commit code on day 1, deploy to staging by day 3, and feel confident by week 2."

---

## 1. Onboarding Checklist

```markdown
# Developer Onboarding Checklist

## Day 1: Setup & Access
- [ ] Laptop received and configured
- [ ] GitHub account added to organization
- [ ] Slack workspace access
- [ ] Email and calendar setup
- [ ] VPN access configured
- [ ] Password manager setup (1Password/LastPass)
- [ ] Development environment installed
- [ ] First commit pushed (README typo fix)

## Day 2-3: Codebase Familiarization
- [ ] Clone all repositories
- [ ] Run application locally
- [ ] Read architecture documentation
- [ ] Watch architecture walkthrough video
- [ ] Complete "Hello World" task
- [ ] Deploy to staging environment
- [ ] Attend team standup

## Week 1: First Real Task
- [ ] Assigned onboarding buddy
- [ ] Pick first real issue (labeled "good-first-issue")
- [ ] Create pull request
- [ ] Code review process completed
- [ ] Deploy to production
- [ ] Celebrate first deployment! 🎉

## Week 2: Team Integration
- [ ] Attend sprint planning
- [ ] Present work in demo
- [ ] Participate in retrospective
- [ ] Shadow on-call engineer
- [ ] Complete security training

## Month 1: Full Integration
- [ ] Lead a feature from start to finish
- [ ] Give feedback on onboarding process
- [ ] Update onboarding docs with learnings
```

---

## 2. README Structure

```markdown
# Project Name

## Quick Start
\`\`\`bash
git clone https://github.com/company/project.git
cd project
npm run setup
npm run dev
\`\`\`
Visit http://localhost:3000

## What is this project?
[One paragraph description]

## Architecture Overview
[High-level diagram]

## Tech Stack
- **Frontend**: React + TypeScript
- **Backend**: Node.js + Express
- **Database**: PostgreSQL
- **Cache**: Redis
- **Deployment**: AWS ECS

## Development
- [Local Development Guide](docs/development.md)
- [Testing Guide](docs/testing.md)
- [Deployment Guide](docs/deployment.md)

## Common Tasks
- Run tests: `npm test`
- Lint code: `npm run lint`
- Build: `npm run build`
- Deploy to staging: `npm run deploy:staging`

## Getting Help
- **Slack**: #team-backend
- **On-call**: See PagerDuty schedule
- **Documentation**: [Wiki](https://wiki.company.com)
```

---

## 3. Architecture Documentation

```markdown
# Architecture Overview

## System Diagram
\`\`\`
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   React     │────▶│   API       │────▶│  PostgreSQL │
│   Frontend  │     │   Gateway   │     │  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Redis     │
                    │   Cache     │
                    └─────────────┘
\`\`\`

## Key Components

### Frontend (React)
- **Location**: `apps/web/`
- **Purpose**: User interface
- **Owner**: @frontend-team
- **Key Files**: 
  - `src/pages/` - Page components
  - `src/components/` - Reusable components
  - `src/api/` - API client

### API Gateway
- **Location**: `apps/api/`
- **Purpose**: REST API, authentication, rate limiting
- **Owner**: @backend-team
- **Key Files**:
  - `src/routes/` - API endpoints
  - `src/middleware/` - Auth, logging
  - `src/services/` - Business logic

### Database
- **Type**: PostgreSQL 15
- **Schema**: See `prisma/schema.prisma`
- **Migrations**: `prisma/migrations/`

## Data Flow
1. User interacts with React frontend
2. Frontend calls API Gateway
3. API Gateway validates auth token
4. API Gateway queries database
5. Response cached in Redis
6. Data returned to frontend

## Key Decisions
- [ADR-001: Use PostgreSQL](docs/adr/0001-postgresql.md)
- [ADR-002: Use React](docs/adr/0002-react.md)
```

---

## 4. Development Workflow Guide

```markdown
# Development Workflow

## Branching Strategy
\`\`\`
main (production)
  ↑
develop (staging)
  ↑
feature/TICKET-123-description
\`\`\`

## Creating a Feature

### 1. Create Branch
\`\`\`bash
git checkout develop
git pull
git checkout -b feature/TICKET-123-add-user-profile
\`\`\`

### 2. Make Changes
\`\`\`bash
# Make your changes
npm run dev  # Test locally
npm test     # Run tests
npm run lint # Check code quality
\`\`\`

### 3. Commit
\`\`\`bash
git add .
git commit -m "feat(profile): add user profile page"
\`\`\`
Follow [commit conventions](docs/commit-conventions.md)

### 4. Push and Create PR
\`\`\`bash
git push origin feature/TICKET-123-add-user-profile
\`\`\`
Create pull request on GitHub

### 5. Code Review
- Request review from 2 team members
- Address feedback
- Get approval

### 6. Merge
- Squash and merge to develop
- Delete feature branch

### 7. Deploy
- Automatic deployment to staging
- Test on staging
- Create release PR to main
- Deploy to production
\`\`\`

---

## 5. Troubleshooting Guide

```markdown
# Common Issues & Solutions

## "Port 3000 already in use"
\`\`\`bash
# Find and kill process
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 npm run dev
\`\`\`

## "Database connection failed"
\`\`\`bash
# Check Docker is running
docker ps

# Restart database
docker-compose restart postgres

# Check connection string
echo $DATABASE_URL
\`\`\`

## "npm install fails"
\`\`\`bash
# Clear cache
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
\`\`\`

## "Tests failing locally but pass in CI"
\`\`\`bash
# Use same Node version as CI
nvm use 18

# Clear test cache
npm test -- --clearCache
\`\`\`

## Still stuck?
- Check #help channel in Slack
- Ask your onboarding buddy
- Review [FAQ](docs/faq.md)
\`\`\`

---

## 6. Team Practices

```markdown
# Team Practices

## Communication
- **Daily Standup**: 9:30 AM (15 min)
- **Sprint Planning**: Monday 10 AM (1 hour)
- **Retrospective**: Friday 4 PM (30 min)
- **Demo**: Friday 3 PM (30 min)

## Code Review
- All code must be reviewed by 2 people
- Reviews should happen within 24 hours
- Use "Request Changes" for blocking issues
- Use "Comment" for suggestions
- Approve when ready to merge

## On-call Rotation
- Week-long shifts
- Handoff on Monday morning
- Runbooks: [docs/runbooks/](docs/runbooks/)
- Escalation: See PagerDuty

## Working Hours
- Core hours: 10 AM - 4 PM (be available)
- Flexible outside core hours
- Update calendar for time off
- Notify team in #team channel

## Remote Work
- Camera on for standups and planning
- Use Slack status (🏠 WFH, 🍽️ Lunch, 🎧 Focus)
- Async communication preferred
- Document decisions in writing
```

---

## 7. Learning Resources

```markdown
# Learning Resources

## Internal
- [Architecture Decision Records](docs/adr/)
- [API Documentation](https://api.company.com/docs)
- [Design System](https://design.company.com)
- [Engineering Blog](https://blog.company.com)

## External
### TypeScript
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)

### React
- [React Docs](https://react.dev)
- [React Patterns](https://reactpatterns.com)

### Node.js
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)

### PostgreSQL
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com)

## Recommended Reading
- "The Pragmatic Programmer" - Hunt & Thomas
- "Clean Code" - Robert Martin
- "Designing Data-Intensive Applications" - Martin Kleppmann
```

---

## 8. Onboarding Buddy Guide

```markdown
# Onboarding Buddy Guide

## Your Role
Help new developer succeed in first 2 weeks.

## Week 1 Checklist
- [ ] **Day 1**: Lunch together, workspace tour
- [ ] **Day 1**: Help with environment setup
- [ ] **Day 2**: Codebase walkthrough (30 min)
- [ ] **Day 3**: Pair programming session
- [ ] **Day 5**: Check-in: How's it going?

## Week 2 Checklist
- [ ] **Day 8**: Review first PR together
- [ ] **Day 10**: Introduce to other teams
- [ ] **Day 12**: Check-in: Any blockers?
- [ ] **Day 14**: Feedback session

## Tips
- ✅ Be patient, everyone learns differently
- ✅ Encourage questions (no stupid questions!)
- ✅ Share your own onboarding experience
- ✅ Introduce to team members
- ❌ Don't overwhelm with information
- ❌ Don't assume prior knowledge
```

---

## 9. First Week Tasks

```markdown
# First Week Tasks

## Task 1: Fix a Typo (30 min)
**Goal**: Make first commit

1. Find a typo in README.md
2. Create branch: `fix/readme-typo`
3. Fix typo
4. Commit: `docs: fix typo in README`
5. Create PR
6. Get it merged!

## Task 2: Add Your Name (1 hour)
**Goal**: Learn the codebase structure

1. Add yourself to `CONTRIBUTORS.md`
2. Add your photo to `public/team/`
3. Update team page component
4. Test locally
5. Create PR

## Task 3: Implement "Hello World" Feature (4 hours)
**Goal**: End-to-end feature development

1. Create API endpoint: `GET /api/hello/:name`
2. Add frontend component to call it
3. Write tests
4. Deploy to staging
5. Demo to team

## Task 4: Fix a Real Bug (1-2 days)
**Goal**: Real contribution

1. Pick issue labeled `good-first-issue`
2. Reproduce bug locally
3. Fix and add test
4. Create PR
5. Deploy to production
```

---

## 10. Onboarding Documentation Checklist

- [ ] **README**: Quick start guide exists?
- [ ] **Architecture Docs**: System diagram and component overview?
- [ ] **Development Guide**: Setup and workflow documented?
- [ ] **Troubleshooting**: Common issues and solutions?
- [ ] **Team Practices**: Communication and processes documented?
- [ ] **Learning Resources**: Internal and external resources listed?
- [ ] **First Tasks**: Graduated tasks for first week?
- [ ] **Buddy System**: Onboarding buddy assigned?
- [ ] **Feedback Loop**: New developers update docs?
- [ ] **Video Walkthrough**: Architecture overview recorded?

---

## Related Skills
- `45-developer-experience/local-dev-standard`
- `45-developer-experience/dev-environment-setup`
- `45-developer-experience/code-review-standards`
