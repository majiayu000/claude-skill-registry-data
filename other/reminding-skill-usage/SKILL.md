---
name: reminding-skill-usage
description: Analyzes your task and suggests which skills from your library would be most helpful. Use when starting a new task or unsure which existing skills apply to your current work.
version: "1.0.0"
---

<objective>
Help you discover and leverage relevant skills from your Claude skills library by analyzing your task description and matching it against available skills.
</objective>

<quick_start>
**Usage:**
```
"I need to [describe your task]"
"What skills should I use for [task]?"
"Help me find the right skill for [problem]"
```

Claude will analyze your request and suggest 2-5 relevant skills to use.
</quick_start>

<process>
## Step 1: Understand the Task

Ask the user what they're trying to accomplish:
- What's the goal?
- What type of work? (coding, writing, data, design, etc.)
- What deliverables are needed?

If they already provided context, skip to Step 2.

## Step 2: Analyze Task Type

Categorize the task into domains:

**Development:**
- Frontend (React, Vue, Svelte, HTML/CSS)
- Backend (API, database, auth, deployment)
- Full-stack (Next.js, integration)
- Mobile (iOS, Android)
- DevOps (Docker, CI/CD, deployment)

**Security:**
- AppSec (OWASP, input validation, secrets)
- Threat modeling (STRIDE, attack surface)
- Compliance (SOC2, GDPR, HIPAA)

**Content & Design:**
- Documents (docx, pdf, xlsx, pptx)
- Design (frontend, UI/UX, responsive)
- Graphics (production assets, brand systems)

**Planning & Process:**
- Project planning (roadmaps, milestones)
- Feature planning (breakdown, implementation)
- Documentation (technical docs, ADRs)

**Automation & Integration:**
- Workflow automation (n8n, Zapier, Make)
- AI agents (LangChain, CrewAI, MCP)
- API integration

**Analysis & Research:**
- Code analysis (audit, refactor)
- Data analysis (CSV, JSON, visualization)
- User research

## Step 3: Match to Skills

Based on task type, suggest relevant skills:

### Document Creation
→ **docx**, **pdf**, **pptx**, **xlsx** skills

### Web Development
→ **frontend-design**, **responsive-design-patterns**, **animation-motion-design**, **ui-component-library**

### Professional Design
→ **professional-web-design**, **production-graphics**, **design-system-builder**, **advanced-visual-design**

### Security & Compliance
→ **staff-engineer-v3** (includes AppSec), **error-tracking** (Sentry)

### Development Workflows
→ **backend-dev-guidelines**, **frontend-dev-guidelines**, **test-fixing**, **git-pushing**

### Planning & Architecture
→ **create-plans**, **feature-planning**, **architecture-diagram-creator**, **flowchart-creator**, **timeline-creator**

### Technical Documentation
→ **technical-doc-creator**, **codebase-documenter**, **internal-comms**

### Automation
→ **workflow-automation**, **ai-agents-workflow**, **mcp-builder**

### Code Quality
→ **code-auditor**, **code-refactor**, **code-transfer**, **debug-like-expert**

### Project Setup
→ **project-bootstrapper**, **create-slash-commands**, **create-subagents**, **create-agent-skills**

### Meta/Tools
→ **skill-packager**, **skill-creator**, **conversation-analyzer**, **build-macos-apps**, **build-iphone-apps**

## Step 4: Provide Recommendations

Format response as:

```
Based on your task to [restate task], I recommend these skills:

1. **skill-name** - Why it's relevant
2. **skill-name** - Why it's relevant
3. **skill-name** - Why it's relevant

Would you like me to use any of these skills now?
```

## Step 5: Invoke if Requested

If user says "yes" or names a skill:
- Read the appropriate SKILL.md from references/
- Follow that skill's workflow
- Complete the task using the skill's guidance

</process>

<skill_categories>
## Available Skill Categories

### 📝 Document Creation
- docx, pdf, pptx, xlsx
- production-graphics, canvas-design

### 💻 Development
- frontend-dev-guidelines, backend-dev-guidelines
- frontend-design, responsive-design-patterns
- ui-component-library, animation-motion-design

### 🔒 Security & Quality
- staff-engineer-v3 (AppSec + Platform)
- error-tracking, code-auditor
- test-fixing, debug-like-expert

### 📊 Planning & Architecture
- create-plans, feature-planning
- architecture-diagram-creator
- flowchart-creator, timeline-creator

### 📚 Documentation
- technical-doc-creator
- codebase-documenter
- internal-comms

### 🤖 Automation & AI
- workflow-automation
- ai-agents-workflow
- mcp-builder

### 🛠️ Tools & Meta
- skill-packager, skill-creator
- create-agent-skills
- conversation-analyzer

### 📱 Platform-Specific
- build-macos-apps
- build-iphone-apps
- webapp-testing

### 🎨 Design Systems
- design-system-builder
- advanced-visual-design
- advanced-ux-patterns
- professional-web-design

### 🔄 Code Operations
- code-refactor, code-transfer
- git-pushing, review-implementing
- file-operations

</skill_categories>

<matching_rules>
## Keyword

See `references/keyword-matching.md` for detailed content.

## Example Interactions

**Example 1: Document Creation**
```
User: "I need to create a quarterly business review presentation"
Assistant: Based on your task to create a quarterly business review presentation, I recommend:

1. **pptx** - Create professional PowerPoint presentations with charts and data
2. **canvas-design** - Design visual elements like cover slides and infographics
3. **xlsx** - Build supporting spreadsheets with financial data

Would you like me to use the pptx skill to start your presentation?
```

**Example 2: Web Development**
```
User: "Build a responsive landing page with smooth animations"
Assistant: Based on your task to build a responsive landing page with animations, I recommend:

1. **frontend-design** - Create professional frontend with modern design patterns
2. **responsive-design-patterns** - Implement mobile-first responsive layouts
3. **animation-motion-design** - Add smooth, performant animations and transitions

Would you like me to use these skills to start building?
```

**Example 3: Security Review**
```
User: "Review this API for security issues"
Assistant: Based on your task to review an API for security issues, I recommend:

1. **staff-engineer-v3** - Comprehensive AppSec review with OWASP compliance
2. **code-auditor** - Systematic code quality and security analysis
3. **backend-dev-guidelines** - Check against backend best practices

Would you like me to use the staff-engineer-v3 skill to perform the security audit?
```

</examples>

<notes>
- This skill acts as a "meta-skill" to help discover other skills
- Best used at start of new tasks or when stuck
- Can be combined with other skills in workflows
- Regularly updated as new skills are added to library
</notes>
