---
name: learn-projects
description: "Learn how Nexus projects work. Load when user mentions: learn projects, how do projects work, projects vs skills, project tutorial, what is a project, project structure, project lifecycle, understand projects, explain projects. 8-10 min."
onboarding: true
priority: high
---

## 🎯 AI Proactive Triggering (ONBOARDING SKILL)

**This is an ONBOARDING skill with HIGH PRIORITY for proactive suggestion.**

### When to Proactively Suggest (AI MUST check user-config.yaml)

Check `learning_tracker.completed.learn_projects` in user-config.yaml. If `false`:

**PROACTIVELY SUGGEST when user:**
1. Says "create project" for the FIRST TIME (suggest learning before creating)
2. Describes work that sounds like a project (deliverable, deadline, finite work)
3. Asks about organizing work, tracking progress, or managing tasks
4. Expresses confusion about projects vs skills
5. Starts creating multiple similar "projects" (anti-pattern detection)
6. At the END of setup-goals or setup-workspace (natural next step)
7. When displaying the Nexus menu and `total_projects = 0`

**Suggestion Pattern:**
```
💡 Before creating your first project, would you like a quick 8-minute tutorial
on how Nexus projects work? It covers:
- When to use projects vs skills
- Project structure and lifecycle
- How to track progress effectively

Say 'learn projects' to start, or 'skip' to create your project directly.
```

**DO NOT suggest if:**
- `learning_tracker.completed.learn_projects: true`
- User explicitly says "just create the project" or "skip tutorial"
- User has already created projects successfully

---

# Learn Projects

Teach how Nexus projects work through examples and decision framework.

## Purpose

Help user understand when to create projects vs skills, how projects are structured, and the project lifecycle. Uses concrete examples before abstract concepts.

**Time Estimate**: 8-10 minutes

---

## Workflow

### Step 1: Concrete Examples

Show what IS and ISN'T a project:
```
✅ PROJECTS:
- Build client proposal for Acme Corp
- Research competitors and write analysis
- Create onboarding docs for new hires

❌ NOT PROJECTS (these are skills):
- Generate weekly status reports (repeating)
- Qualify incoming leads (repeating)
- Format documents (repeating)

Pattern: Projects END. Skills REPEAT.
```

**Ask**: "What work are YOU planning? Let's classify it."

---

### Step 2: Decision Framework

```
Question 1: Direction or Work?
  • Direction = Goal (goals.md)
  • Work = Project or Skill

Question 2: Does it repeat?
  • NO → PROJECT (has endpoint)
  • YES → SKILL (reusable)

ANTI-PATTERN:
❌ "weekly-report-week-1", "weekly-report-week-2"...
✅ ONE "weekly-report" SKILL used every week
```

---

### Step 3: Project Structure

```
📁 02-projects/05-client-proposal/
├── 01-planning/
│   ├── overview.md    # What & why
│   ├── plan.md        # How
│   └── steps.md       # Tasks (checkboxes)
├── 02-resources/      # Reference materials
├── 03-working/        # Work in progress
└── 04-outputs/        # Final deliverables
```

---

### Step 4: Lifecycle

```
PLANNING → IN_PROGRESS → COMPLETE → ARCHIVED
```

Explain each state briefly.

---

### Step 5: Practice

**Ask**: "Tell me 3 things you're planning to work on."

For each: apply decision framework together, explain reasoning.

---

### Step 6: How to Create

```
To create a project, say:
• "create project for [description]"
• "new project: [name]"

Ready? Say "create project" to start one!
```

---

### Step 7: Finalize

**Actions** (MUST complete all):

1. **Mark skill complete** in user-config.yaml:
   ```yaml
   learning_tracker:
     completed:
       learn_projects: true  # ADD THIS LINE
   ```

2. **Display completion**:
   ```
   ✅ Learn Projects Complete!

   You now understand:
   • Projects vs Skills (projects END, skills REPEAT)
   • Decision framework (Direction → Work → Repeat?)
   • Project structure (planning → resources → working → outputs)
   • Lifecycle states (PLANNING → IN_PROGRESS → COMPLETE)

   Next steps:
   • 'create project' - Start your first project
   • 'learn skills' - Learn about reusable workflows
   • 'learn nexus' - System mastery
   ```

3. **Prompt close-session**:
   ```
   💡 When you're done working, say "done" to save progress.
   ```

---

## Success Criteria

- [ ] User understands project vs skill distinction
- [ ] User can apply decision framework
- [ ] User knows project folder structure
- [ ] User understands lifecycle states
- [ ] `learning_tracker.completed.learn_projects: true` in user-config.yaml
