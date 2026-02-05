---
name: initialize-project
description: Initialize a new software project with customized structure through interactive Q&A. Use when user mentions "new project", "start project", "initialize project", "create project", or "set up project". Gathers methodology, team structure, documentation preferences, and integration requirements to generate appropriate RULE.md and directory structure.
---

# Initialize Project Skill

## When to use this Skill

Activate when the user:
- Mentions starting or creating a new project
- Uses keywords: "new project", "start project", "initialize project", "create project", "set up project"
- Wants to set up project management structure
- Needs to configure project documentation

## Workflow

### Phase 1: Project Identification

**Objective**: Understand what project we're setting up.

**Steps**:
1. **Extract project name** from user message if provided
2. **Determine target directory**:
   - If in a directory already, offer to initialize there
   - If project name given, create new directory
   - Otherwise, ask where to create the project
3. **Check for existing structure**:
   - Use `ls` to check if directory exists
   - Use `Read` to check for existing RULE.md
   - Warn if project already initialized

**Example**:
```
User: "I want to create a new project called Mobile App Redesign"

Detected:
- Project name: "mobile-app-redesign" (slugified)
- Action: Create new directory
```

### Phase 2: Interactive Q&A

**Objective**: Gather complete information about team workflow and preferences.

Use **AskUserQuestion** tool with clear, focused questions. Each question should offer specific options.

#### Question Set 1: Development Methodology

**Question**: "What development methodology does your team use?"

**Options to present**:
1. **Scrum** - Time-boxed sprints with ceremonies (planning, daily standup, review, retrospective)
2. **Kanban** - Continuous flow with WIP limits and visual board
3. **Waterfall** - Sequential phases with formal handoffs
4. **Agile (general)** - Iterative development without strict Scrum ceremonies
5. **Hybrid/Custom** - Combination of methodologies

**Follow-up questions based on choice**:

If **Scrum** selected:
- "How long are your sprints?" (1 week / 2 weeks / 3 weeks / 4 weeks)
- "Do you hold daily standups?" (Yes / No)
- "Sprint ceremonies to track?" (Planning, Review, Retrospective - multiSelect)

If **Kanban** selected:
- "What are your workflow stages?" (Backlog, In Progress, Review, Done - customizable)
- "Do you use WIP limits?" (Yes / No)
- "How often do you review the board?" (Daily / Weekly / Ad-hoc)

If **Waterfall** selected:
- "What are your project phases?" (Requirements, Design, Development, Testing, Deployment - customizable)
- "Do you need phase gate reviews?" (Yes / No)

If **Agile (general)** selected:
- "How long are your iterations?" (1 week / 2 weeks / 4 weeks / Continuous)
- "Do you have regular team meetings?" (Yes / No)

If **Hybrid/Custom** selected:
- Ask user to describe their process
- Extract key ceremonies and practices

#### Question Set 2: Team Structure

**Question**: "Tell me about your team structure"

**Information to gather**:
- Team size (Small: 2-5 / Medium: 6-10 / Large: 11+)
- Key roles present:
  - Product Owner / Product Manager
  - Scrum Master / Project Manager
  - Developers (how many?)
  - Designers
  - QA / Testers
  - Others
- Communication patterns:
  - Daily syncs
  - Weekly planning
  - Async-first
  - Real-time collaboration

**Use AskUserQuestion** with multiple questions if needed.

#### Question Set 3: Documentation Preferences

**Question**: "How does your team prefer to document work?"

**Options**:
1. **Structured with frontmatter** - YAML frontmatter with metadata, structured sections
2. **Simple markdown** - Plain markdown without strict formatting
3. **Table-based** - Information organized in markdown tables
4. **Issue-tracker style** - Similar to GitHub Issues / Jira format

**Follow-up**:
- "File naming convention preference?"
  - Date-prefixed: `2025-11-13_meeting-name.md`
  - Descriptive: `sprint-planning-sprint-5.md`
  - Numbered: `001-meeting-name.md`
  - Custom (ask user)

#### Question Set 4: Integration Requirements

**Question**: "What tools does your team integrate with?"

**Present as multiSelect options**:
- Version control: Git / GitHub / GitLab / Bitbucket
- Issue tracking: GitHub Issues / Jira / Linear / Asana / Trello
- CI/CD: GitHub Actions / GitLab CI / Jenkins / CircleCI
- Communication: Slack / Discord / Microsoft Teams
- Documentation: Notion / Confluence / Wiki
- None / Other

**For each selected integration**, gather specific details:
- Git: Repository URL, branch naming convention
- Issue tracker: Project key, link format
- CI/CD: Workflow names
- Communication: Webhook URLs, channel naming
- Documentation: Workspace URL, linking format

### Phase 3: Analysis & RULE.md Generation

**Objective**: Synthesize all Q&A responses into a comprehensive RULE.md.

**Steps**:

1. **Analyze responses**:
   - Identify primary methodology
   - Extract team size and structure
   - Determine documentation format
   - List integrations

2. **Generate directory structure** based on methodology:

   **For Scrum**:
   ```
   project-name/
   ├── RULE.md
   ├── README.md
   ├── meetings/
   │   ├── README.md
   │   ├── daily-standups/
   │   ├── sprint-planning/
   │   ├── sprint-reviews/
   │   └── retrospectives/
   ├── sprints/
   │   ├── README.md
   │   ├── backlog/
   │   └── current/
   ├── docs/
   │   ├── README.md
   │   └── technical/
   ├── decisions/
   │   └── README.md
   ├── communications/
   │   └── README.md
   └── milestones.yaml
   ```

   **For Kanban**:
   ```
   project-name/
   ├── RULE.md
   ├── README.md
   ├── board/
   │   ├── README.md
   │   ├── backlog/
   │   ├── in-progress/
   │   ├── review/
   │   └── done/
   ├── meetings/
   │   ├── README.md
   │   └── board-reviews/
   ├── docs/
   │   ├── README.md
   │   └── technical/
   ├── decisions/
   │   └── README.md
   └── milestones.yaml
   ```

   **For Waterfall**:
   ```
   project-name/
   ├── RULE.md
   ├── README.md
   ├── phases/
   │   ├── README.md
   │   ├── 01-requirements/
   │   ├── 02-design/
   │   ├── 03-development/
   │   ├── 04-testing/
   │   └── 05-deployment/
   ├── meetings/
   │   ├── README.md
   │   └── phase-reviews/
   ├── docs/
   │   ├── README.md
   │   └── technical/
   ├── decisions/
   │   └── README.md
   └── milestones.yaml
   ```

   **For Agile/Hybrid**:
   ```
   project-name/
   ├── RULE.md
   ├── README.md
   ├── iterations/
   │   ├── README.md
   │   └── backlog/
   ├── meetings/
   │   └── README.md
   ├── docs/
   │   ├── README.md
   │   └── technical/
   ├── decisions/
   │   └── README.md
   └── milestones.yaml
   ```

3. **Generate RULE.md content**:

   Use this template, filling in values from Q&A:

   ```markdown
   # Project: [Project Name]

   ## Purpose
   [Brief project description - ask user or infer from context]

   ## Methodology
   methodology: [scrum|kanban|waterfall|agile|hybrid]
   [If Scrum]
   sprint_length: [1_week|2_weeks|3_weeks|4_weeks]
   daily_standup: [true|false]
   ceremonies: [planning, review, retrospective]

   [If Kanban]
   workflow_stages: [backlog, in_progress, review, done]
   wip_limits: [true|false]
   review_frequency: [daily|weekly|adhoc]

   [If Waterfall]
   phases: [requirements, design, development, testing, deployment]
   phase_gates: [true|false]

   ## Team Structure
   team_size: [number]
   roles:
     [For each role from Q&A]
     - role_name: [Name or "TBD"]

   communication_pattern: [daily_syncs|weekly_planning|async_first|realtime]

   ## Directory Structure
   [Insert the generated structure from above]

   ## Document Templates

   ### [For each document type, generate template]

   [If Scrum]
   #### Meeting Notes Format
   ```yaml
   ---
   title: [Meeting Title]
   type: [standup|planning|retrospective|review]
   date: [YYYY-MM-DD]
   attendees: [list]
   duration_minutes: [number]
   ---

   ## Agenda
   -

   ## Discussion
   [Notes]

   ## Action Items
   - [ ] Task - @owner - due: YYYY-MM-DD

   ## Decisions
   -
   ```

   #### Sprint Format
   ```yaml
   ---
   sprint_number: [number]
   start_date: YYYY-MM-DD
   end_date: YYYY-MM-DD
   sprint_goal: [Goal]
   status: [planning|active|completed]
   ---

   ## Sprint Goal
   [Description]

   ## User Stories
   - [ ] As a [user], I want [goal] so that [benefit]
     - Story Points: X
     - Priority: [High|Medium|Low]
     - Assignee: @[name]

   ## Sprint Retrospective
   [Added at end]
   ```

   [If Kanban]
   #### Card Format
   ```yaml
   ---
   title: [Card Title]
   type: [feature|bug|improvement|task]
   status: [backlog|in_progress|review|done]
   priority: [high|medium|low]
   assignee: @[name]
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   ---

   ## Description
   [What needs to be done]

   ## Acceptance Criteria
   - [ ] Criterion 1
   - [ ] Criterion 2

   ## Notes
   [Additional context]
   ```

   [If Waterfall]
   #### Phase Document Format
   ```yaml
   ---
   phase_name: [Phase Name]
   phase_number: [1-5]
   start_date: YYYY-MM-DD
   planned_end_date: YYYY-MM-DD
   actual_end_date: [YYYY-MM-DD or "in_progress"]
   status: [planning|active|review|completed]
   ---

   ## Phase Objectives
   [What this phase accomplishes]

   ## Deliverables
   - [ ] Deliverable 1
   - [ ] Deliverable 2

   ## Phase Gate Criteria
   [Criteria for moving to next phase]

   ## Notes
   [Additional information]
   ```

   ## File Naming Convention
   format: [date_prefixed|descriptive|numbered|custom]
   [If date_prefixed]
   pattern: "YYYY-MM-DD_descriptive-name.md"
   [If descriptive]
   pattern: "descriptive-name-with-context.md"
   [If numbered]
   pattern: "###-descriptive-name.md"
   [If custom]
   pattern: "[user-specified pattern]"

   ## Auto Workflows

   ### When Claude creates meeting notes:
   1. Extract all action items with @mentions
   2. Update README.md meeting index
   3. [If Scrum] Link to current sprint if relevant
   4. [If integrations enabled] Update external tracker
   5. Notify attendees of action items (if communication tool integrated)

   ### When Claude creates/updates [sprint|iteration|card|phase]:
   1. Update status in milestones.yaml if milestone-related
   2. Update README.md index
   3. [If version control] Suggest related branches
   4. [If issue tracker] Link to external issues
   5. Calculate velocity/progress metrics

   ### When Claude marks milestone complete:
   1. Update milestones.yaml status
   2. Generate milestone completion report
   3. Archive related documentation
   4. Update project timeline
   5. [If communication tool] Announce completion

   ### When Claude searches project:
   1. Check README.md indexes first (fastest)
   2. Search by file patterns
   3. Full-text search as last resort
   4. Rank by relevance, recency, and location
   5. Show context (surrounding content)

   ## Integrations

   [For each integration from Q&A]

   ### [Integration Name]
   type: [git|issue_tracker|ci_cd|communication|documentation]
   [Specific configuration]
   [If Git]
   repository: [URL]
   branch_convention: [feature/*, bugfix/*, etc.]
   [If Issue Tracker]
   project_key: [KEY]
   issue_link_format: "[KEY]-###"
   [If CI/CD]
   workflows: [list]
   [If Communication]
   channels: [list]
   webhook: [URL if applicable]
   [If Documentation]
   workspace: [URL]
   link_format: [pattern]

   ## Allowed Operations
   All operations allowed. Maintain governance through README.md updates.
   Track milestones and dependencies. Always confirm destructive operations.

   ## Special Instructions

   [Add any custom workflows or requirements mentioned by user during Q&A]

   ## Notes

   - Created: [YYYY-MM-DD]
   - Initialized by: ProjectMaster initialize-project Skill
   - Last updated: [YYYY-MM-DD]
   ```

4. **Generate milestones.yaml template**:

   ```yaml
   # Project Milestones
   # Managed by ProjectMaster track-milestone Skill

   project:
     name: [Project Name]
     start_date: [YYYY-MM-DD]
     target_completion: [YYYY-MM-DD or "TBD"]
     status: [planning|active|completed]

   milestones:
     # Example milestone structure:
     # - id: milestone-1
     #   name: "Beta Release"
     #   description: "Feature-complete beta ready for testing"
     #   target_date: YYYY-MM-DD
     #   actual_date: YYYY-MM-DD or null
     #   status: planned|in_progress|completed|delayed
     #   dependencies: [milestone-0]
     #   deliverables:
     #     - Deliverable 1
     #     - Deliverable 2
     #   owner: "@name"
     #   notes: "Additional context"

   # Add milestones here as project progresses
   ```

### Phase 4: User Confirmation

**Objective**: Show the user what will be created and get approval.

**Steps**:

1. **Present summary** of configuration:
   ```
   📋 Project Configuration Summary

   Project: [name]
   Methodology: [methodology with key details]
   Team: [size] members ([roles])
   Documentation: [format preference]
   Integrations: [list]

   Directory structure:
   [Show tree structure]

   This will create:
   - RULE.md with your team's workflow
   - README.md project overview
   - [X] directories for [meetings/sprints/phases/etc]
   - milestones.yaml for tracking
   - Initial documentation templates

   Proceed with initialization?
   ```

2. **Wait for user confirmation**

3. **If user wants changes**:
   - Ask what to modify
   - Update configuration
   - Show summary again
   - Get confirmation

### Phase 5: Create Structure

**Objective**: Execute the initialization by creating all files and directories.

**Steps**:

1. **Create project directory** (if needed):
   ```bash
   mkdir -p [project-name]
   cd [project-name]
   ```

2. **Create all subdirectories**:
   ```bash
   mkdir -p [dir1] [dir2] [dir3] ...
   ```
   Use the structure generated in Phase 3.

3. **Write RULE.md**:
   Use `Write` tool to create the RULE.md with generated content.

4. **Write milestones.yaml**:
   Use `Write` tool to create milestones.yaml template.

5. **Write project README.md**:
   ```markdown
   # [Project Name]

   > [Brief description]

   ## Project Information

   - **Status**: Planning
   - **Methodology**: [methodology]
   - **Team Size**: [number]
   - **Started**: [YYYY-MM-DD]
   - **Target Completion**: TBD

   ## Quick Links

   - [RULE.md](RULE.md) - Project governance and workflows
   - [milestones.yaml](milestones.yaml) - Milestone tracking
   - [Meetings](meetings/) - Meeting notes
   - [[Sprints/Iterations/Phases]](path/) - [Work tracking]
   - [Documentation](docs/) - Technical documentation
   - [Decisions](decisions/) - Architecture decisions

   ## Team

   [List team members and roles from RULE.md]

   ## Current Status

   Project initialized on [YYYY-MM-DD]. Ready to begin [first phase/sprint/iteration].

   ## Recent Activity

   - [YYYY-MM-DD]: Project initialized with ProjectMaster

   ## Contents

   [Will be auto-updated as content is added]

   ---

   Last updated: [YYYY-MM-DD]
   Governance maintained by: ProjectMaster
   ```

6. **Write README.md for each subdirectory**:
   Each major directory gets an index README.md:

   **meetings/README.md**:
   ```markdown
   # Meetings

   Meeting notes and minutes for [Project Name].

   ## Recent Meetings

   [Will be auto-updated]

   ## Meeting Types

   - [List types based on methodology]

   ---

   Last updated: [YYYY-MM-DD]
   ```

   **[sprints|board|phases]/README.md**:
   ```markdown
   # [Sprints/Board/Phases]

   [Work tracking] for [Project Name].

   ## [Current Sprint/Active Cards/Current Phase]

   [Will be updated as work progresses]

   ## [Backlog/Completed]

   [Will be updated]

   ---

   Last updated: [YYYY-MM-DD]
   ```

   **docs/README.md**:
   ```markdown
   # Documentation

   Technical documentation for [Project Name].

   ## Contents

   [Will be auto-updated]

   ---

   Last updated: [YYYY-MM-DD]
   ```

   **decisions/README.md**:
   ```markdown
   # Decisions

   Architecture and significant decisions for [Project Name].

   ## Decision Records

   [Will be auto-updated]

   ---

   Last updated: [YYYY-MM-DD]
   ```

7. **Create template files** (optional):
   If helpful, create example templates in a `templates/` directory:
   - meeting-template.md
   - sprint-template.md
   - decision-template.md

8. **Verify structure**:
   ```bash
   ls -R
   ```
   Confirm all directories and files created successfully.

### Phase 6: Report

**Objective**: Confirm successful initialization and guide next steps.

**Report format**:

```
✅ Project Initialized Successfully!

📁 Created structure for: [Project Name]
   Location: [path]

📄 Key files:
   ✓ RULE.md - Project governance
   ✓ README.md - Project overview
   ✓ milestones.yaml - Milestone tracking
   ✓ [X] directories created

⚙️ Configuration:
   - Methodology: [methodology details]
   - Team: [size] members
   - Documentation: [format]
   - Integrations: [list]

🚀 Next steps:
   [Provide 2-3 relevant suggestions based on methodology]

   Examples:
   - "Create your first sprint: 'Start sprint 1 for authentication features'"
   - "Add a milestone: 'Create milestone for beta release'"
   - "Record a meeting: 'Create meeting notes for kickoff'"
   - "Add team members to RULE.md"
   - "Define first set of user stories"

💡 Tips:
   - Your RULE.md defines how ProjectMaster works with this project
   - README.md files are auto-updated as you add content
   - All Skills respect your team's workflow from RULE.md
   - Use /project-status to see project health anytime

Ready to start building! What would you like to do first?
```

## Special Cases

### Case 1: Initializing in existing directory

If the target directory already contains files:

1. **Check for RULE.md**:
   - If exists: "This directory already has a RULE.md. Do you want to reinitialize (overwrites) or update the existing configuration?"
   - If doesn't exist: "This directory has files but no governance. Initialize ProjectMaster here?"

2. **Preserve existing structure**:
   - Don't delete existing files
   - Create missing directories only
   - Merge with existing structure if compatible

3. **Update README.md**:
   - If exists, append governance section
   - If doesn't exist, create new

### Case 2: Multiple projects in workspace

If user wants to initialize multiple projects:

1. **Create parent structure**:
   ```
   workspace/
   ├── project-1/
   │   └── RULE.md
   ├── project-2/
   │   └── RULE.md
   └── README.md (workspace index)
   ```

2. **Each project is independent**:
   - Separate RULE.md for each
   - Workspace README.md links to all projects

### Case 3: Minimal initialization

If user wants quick setup without Q&A:

1. **Use sensible defaults**:
   - Methodology: Agile (general)
   - Team: Small (unspecified roles)
   - Documentation: Structured with frontmatter
   - No integrations

2. **Create minimal structure**:
   ```
   project-name/
   ├── RULE.md (with defaults)
   ├── README.md
   ├── meetings/
   ├── work/
   ├── docs/
   └── milestones.yaml
   ```

3. **Inform user**:
   "Initialized with default configuration. Edit RULE.md to customize."

### Case 4: Template-based initialization

If user references an existing project as template:

1. **Read template RULE.md**
2. **Copy structure and configuration**
3. **Ask only for differences**:
   - Project name
   - Team members
   - Integration credentials
4. **Create with template configuration**

## Error Handling

### Error: Directory already exists

**Response**:
```
⚠️ Directory "[name]" already exists.

Options:
1. Initialize in existing directory (preserves files, adds governance)
2. Choose a different name
3. Cancel initialization

What would you like to do?
```

### Error: Invalid project name

**Response**:
```
⚠️ Project name "[name]" contains invalid characters.

Project names should:
- Use lowercase letters, numbers, hyphens
- No spaces or special characters
- Example: "mobile-app-redesign"

Please provide a valid project name.
```

### Error: Cannot write files

**Response**:
```
❌ Error: Unable to create files in [path]

Possible causes:
- Insufficient permissions
- Disk space full
- Path doesn't exist

Please check permissions and try again.
```

### Error: User cancels during Q&A

**Response**:
```
Initialization cancelled. No changes made.

You can restart initialization anytime by saying:
"Initialize a new project for [your project name]"
```

## Integration with AkashicRecords Governance

This Skill creates RULE.md files that are fully compatible with AkashicRecords:

1. **RULE.md format**: Uses natural language, readable by both systems
2. **README.md maintenance**: Both systems update README.md indexes
3. **Directory governance**: All ProjectMaster Skills respect RULE.md
4. **Workflow specifications**: Auto Workflows section defines behavior
5. **Cross-plugin compatibility**: AkashicRecords Skills can operate in ProjectMaster-initialized projects

**Example interaction**:
```
User: "Save this article about React best practices"

Claude: [AkashicRecords add-content Skill activates]
Reading RULE.md... This is a project directory.
Article is technical documentation.
Target: docs/technical/ (per RULE.md structure)
[Proceeds with adding article, updates README.md]
```

Both plugins share governance, ensuring consistency.

## Best Practices

### 1. Complete the Q&A thoroughly

Don't rush through questions. Accurate answers ensure the RULE.md matches your team's actual workflow.

### 2. Start simple, iterate

If unsure about configuration, use defaults and refine RULE.md later as the team's process becomes clearer.

### 3. Customize templates immediately

After initialization, review document templates in RULE.md and adjust to match your team's preferences.

### 4. Involve the team

Show the generated RULE.md to your team and gather feedback. Update before creating real content.

### 5. Document custom workflows

If your team has unique processes, add them to the "Auto Workflows" section in RULE.md immediately.

### 6. Test with a real item

After initialization, create one meeting note or sprint to verify the structure works as expected.

## Examples

### Example 1: Scrum Project

```
User: I want to start a new project for our e-commerce platform redesign

Claude: I'll help you set up a new project! Let me gather information about your team's workflow.

📋 Development Methodology
What development process does your team follow?

User: [Selects Scrum]

Claude: Great! A few details about your Scrum setup:
- Sprint length: 2 weeks
- Daily standups: Yes
- Ceremonies to track: All (planning, review, retrospective)

👥 Team Structure
- Team size: 6
- Roles: Product Owner (Alice), Scrum Master (Bob), 4 Developers

📝 Documentation
- Format: Structured with frontmatter
- Naming: Date-prefixed (2025-11-13_meeting-name.md)

🔗 Integrations
- Git (GitHub)
- Issue tracking (GitHub Issues)
- Communication (Slack)

[Shows summary, user confirms]

✅ Project Initialized Successfully!

📁 Created: ecommerce-redesign/
   ✓ RULE.md configured for 2-week Scrum sprints
   ✓ Directory structure with meetings/, sprints/, docs/
   ✓ milestones.yaml for tracking
   ✓ README.md with project overview

🚀 Next: "Create sprint 1 for user authentication"
```

### Example 2: Kanban Project

```
User: Set up a Kanban board for our bug fix project

Claude: I'll initialize a Kanban-based project! Let me ask a few questions...

[Q&A for Kanban workflow, team, etc.]

✅ Project Initialized: bug-fix-kanban/
   ✓ RULE.md configured for Kanban workflow
   ✓ board/ directory with backlog/, in-progress/, review/, done/
   ✓ WIP limits enabled in RULE.md
   ✓ Weekly board review meetings configured

🚀 Next: "Add a bug to the backlog"
```

### Example 3: Minimal Quick Setup

```
User: Quick project setup for prototyping, no fancy stuff

Claude: I'll create a minimal project with default settings.

✅ Project Initialized: prototype/
   ✓ RULE.md with Agile defaults
   ✓ Basic structure: meetings/, work/, docs/
   ✓ Simple markdown format

💡 You can customize RULE.md later as your needs evolve.

🚀 Ready to go! Add your first note or meeting.
```

## Notes

- This Skill only initializes the structure. Actual content is created by other Skills (track-meeting, manage-sprint, etc.).
- The generated RULE.md is a living document - teams should update it as their process evolves.
- All generated templates are customizable - edit RULE.md to change formats.
- Integration details can be added later if not known during initialization.
- The Skill creates a foundation; the team shapes it into their ideal workflow.

---

This Skill is the entry point to ProjectMaster. A well-configured initialization ensures all other Skills work seamlessly with your team's unique workflow.
