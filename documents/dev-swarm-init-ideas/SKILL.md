---
name: dev-swarm-init-ideas
description: Transform non-technical ideas into professional project kickoff documentation. Use when user asks to init, kickoff, or start a new project, or when ideas.md needs to be formalized into structured documentation.
---

# AI Builder - Initialize Ideas

This skill transforms non-technical or non-professional ideas into professional project kickoff documentation with proper structure and business analysis. It intelligently determines project complexity and scale, then creates only the necessary stages and documentation appropriate for the project size.

## When to Use This Skill

- User asks to "init" or "kickoff" the project
- User wants to start a new project from ideas
- User has an ideas.md file that needs to be formalized
- User wants to create initial project documentation

## Your Roles in This Skill

- **Business Owner**: Ensure commercial success and financial viability. Define business goals, identify the problem statement, and articulate value propositions that balance user value with business profitability.
- **Product Manager**: Create compelling products that meet user needs. Conduct research to identify target users, extract requirements, and ensure the product aligns with both user expectations and business goals.
  - **Role Reference**: Consult `dev-swarm/docs/dev-swarm-roles.md` to assign the correct owner/attendances for each stage README (design requirement file). Do not write requirements outside the owning role.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Follow these steps in order:

### Step 0: Ensure MCP Server is Configured and Running

1. Check whether the current AI code agent has the `dev-swarm` MCP server configured and running.
2. If it is not configured or not running, refer to reference file `references/mcp-server-check.md` to fix it.

### Step 1: Check for Existing Project and ideas.md

1. **Check if `src/` folder exists and contains files:**
   - Check if `src/` directory exists
   - Check if `src/` contains any files (other than just `.gitkeep`)
   - **If src/ contains an existing project:**
     - Inform the user: "An existing project was found in src/. Before starting a new project, the current project should be archived."
     - Ask the user: "Would you like me to archive the existing project using the project-archive skill?"
     - **If user says yes:**
       - Use the Skill tool to invoke `dev-swarm-project-archive`
       - Wait for archiving to complete
       - Then proceed with this skill
     - **If user says no:**
       - Stop execution and inform the user they need to handle the existing project first
       - Exit the skill

2. **Check if `00-init-ideas/` folder exists and has content:**
   - If exists with content: Read all existing files to understand current state
   - If exists but empty (only .gitkeep): Will create new structure
   - If NOT exists: Will create new structure

3. **Check if `ideas.md` exists in the project root:**
   - If exists: Read and analyze the content as input
   - If NOT exists: Ask the user to provide basic ideas for the project, then create `ideas.md`

4. Proceed to Step 2 with gathered context

### Step 2: Classify Project Complexity and Scale

1. **Read the classification standard and scaling rules:**
   - Read `dev-swarm/docs/software-dev-classification.md`
   - Read `dev-swarm/docs/research-specs-rules.md`
   - Read `dev-swarm/docs/mermaid-diagram-guide.md`

2. **Analyze ideas.md to determine:**
   - **Project Purpose (P1-P4):**
     - P1: Personal Tool (individual use, disposable)
     - P2: Internal Tool (team/company use)
     - P3: Open Source Project (public collaboration)
     - P4: Commercial/Profit-Oriented Product

   - **Development Scale (L0-L7):**
     - L0: One-Off Execution (run once, single file)
     - L1: Reusable Script (used repeatedly, basic args)
     - L2: Tool with Environment Setup (dependencies, packaging)
     - L3: Single-Service Application (real app with users)
     - L4: Product MVP (minimal viable product)
     - L5: Multi-Platform MVP (web + mobile)
     - L6: Growth-Stage Product (scaling users/team)
     - L7: Platform/Ecosystem (others build on it)

3. **Document the classification:**
   - Create a classification statement to be included in project README
   - List explicit exclusions based on the scale

### Step 3: Extract Project Information

From the ideas.md file and any existing documentation:
1. Identify and pick the best project name
2. Extract key requirements and goals
3. Identify problem statements
4. Identify target users
5. Extract value propositions

### Step 4: Determine Required Stages Based on Project Scale

Based on the determined scale level, decide which stages are needed:

**For L0-L1 (Very Small Projects - Scripts):**
- 00-init-ideas/README.md (how to implement the script or refined requirements)
- src/script_name.sh (or appropriate extension)
- NO other stages needed

**For L2 (Tool with Environment):**
- 00-init-ideas/ (required)
- 07-tech-specs/ (minimal)
- 08-devops/ (basic setup with development_environment.md)
- 10-deployment/ (required for tools/agent skills)
- SKIP: 01-market-research, 02-personas, 03-mvp, 04-prd, 05-ux, 06-architecture, 09-sprints

**For L3-L4 (Single Service / MVP):**
- All stages except possibly 10-deployment (if not deploying to cloud yet)

**For L5-L7 (Multi-Platform / Growth / Platform):**
- ALL stages required (00 through 10)

**Read repository-structure.md for reference:**
- Read `dev-swarm/docs/repository-structure.md` for detailed folder structure
- Note: The files listed in repository-structure.md are samples; adapt based on project needs
 - Read `dev-swarm/docs/dev-swarm-roles.md` to map stage owners/attendances for README requirements (role-appropriate ownership)

Also decide which stages require Mermaid diagrams. Use
`dev-swarm/docs/mermaid-diagram-guide.md` for structure and
`dev-swarm/docs/software-dev-classification.md` to avoid over-engineering
for small scopes. Record the decision in each stage README.

### Step 5: Project Root README.md
   - **IMPORTANT: DO NOT create or modify the root README.md file**
   - The project readme file we are developing should be maintained in `src/README.md` by developers

### Step 6: Create Stage Folder Structure

Create folders from `00-init-ideas` through `10-deployment`. For each folder:

1. **00-init-ideas (ALWAYS REQUIRED):**
   - Create README.md listing the docs needed for this stage (README is the design requirement file for the stage)
   - Give the project a clear title
   - List which docs will be created (based on project scale)
   - Include Owner/Attendances based on `dev-swarm/docs/dev-swarm-roles.md`
   - Define the docs list using `dev-swarm/docs/repository-structure.md` as the baseline

2. **For stages 01-10:**
   - **If the stage is NOT needed for this project scale:**
     - Create `SKIP.md` with explanation:
       ```markdown
       # Stage Skipped

       This stage is not required for this project because:
       - [Reason based on project scale and purpose]
       ```
     - **For 09-sprints/SKIP.md in L2 projects**, add: "Implementation will proceed directly in the `src/` directory without the need for formal sprints or backlogs."

   - **If the stage IS needed:**
     - **For L2 projects**, create a very simple `README.md` (just several lines) indicating the project level and the specific files required for that stage (e.g., "This is an L2 project. We only need tech-stack.md in this stage.").
     - **For L3+ projects**, create `README.md` listing the docs that will be created in this stage (README is the design requirement file for the stage)
     - Use `dev-swarm/docs/repository-structure.md` as reference but adapt to project needs
     - Include Owner/Attendances based on `dev-swarm/docs/dev-swarm-roles.md` (role-appropriate ownership)
     - Include comments explaining why each doc is needed
     - If diagrams are required for the stage, add a note to create them and
       reference `dev-swarm/docs/mermaid-diagram-guide.md`
     - **DO NOT create the actual documentation files yet** - only README

3. **Create basic folder structure if needed:**
   - Also create: `features/`, `src/`, `99-archive/`
   - Add `.gitkeep` files to empty folders if necessary

### Step 7: User Confirmation on Structure

1. **Present the proposed structure to the user:**
   - Show which stages will be created
   - Show which stages will be skipped (with reasons)
   - Show the classification statement

2. **Ask user to confirm:**
   - "Does this project structure match your expectations?"
   - "Should any stages be added or removed?"

3. **Make adjustments based on user feedback**

### Step 8: Create 00-init-ideas Documentation

**Once user confirms the structure:**

1. **For L0-L1 projects:**
   - Create detailed 00-init-ideas/README.md with:
     - How to implement the script/tool
     - Requirements and specifications
     - Usage instructions
   - Ask if user wants to proceed with implementation in src/

2. **For L2+ projects:**
   - Create 00-init-ideas/README.md first, then ask the user to approve before creating any other files in 00-init-ideas/
   - After approval, create all remaining documentation files in 00-init-ideas/:
     - README.md (owner: Business Owner, attendances: Product Manager)
     - problem-statement.md (clear problem definition)
     - target-users.md (who has the problem, primary audience)
     - value-proposition.md (why this solution matters, core benefits)
     - owner-requirement.md (from ideas.md + constraints for later stages)
     - cost-budget.md (REQUIRED - LLM token budget estimation and cost approval)

**File Content Guidelines:**

**00-init-ideas/README.md:**
- Project title
- Owner: Business Owner
- Attendances: Product Manager
- Overview of this initialization stage
- Links to all documentation files in this folder

**problem-statement.md:**
- Clear description of the problem being solved
- Current pain points
- Why this problem matters
- Constraints and limitations

**target-users.md:**
- Who are the target users (high-level)
- Primary audience
- User needs and expectations

**value-proposition.md:**
- What value does this project provide
- How it solves the problem
- Core benefits to users
- Why this solution matters

**owner-requirement.md:**
- All requirements extracted from ideas.md
- Owner constraints for later stages
- Organized by priority or category
- Clear and actionable items

**cost-budget.md (REQUIRED for L2+ projects):**
- **Token Budget Estimation Per Stage:**
  - Estimate tokens needed for each stage based on project scale
  - Consider: research depth, documentation thoroughness, code complexity, testing coverage
  - Breakdown by stage for only the stages that are NOT skipped: 01-market-research, 02-personas, 03-mvp, 04-prd, 05-ux, 06-architecture, 07-tech-specs, 08-devops, 09-sprints, 10-deployment
  - If a stage is skipped, its cost is $0 and should be omitted from the breakdown

- **Estimated Cost in USD:**
  - Calculate based on current LLM pricing (e.g., Claude Sonnet rates)
  - Include buffer for iterations and refinements (typically 20-30%)
  - Total estimated cost range (min-max)

- **Budget Impact on Project Scope:**
  - How budget affects research time (market research, competitor analysis)
  - How budget affects code quality (testing thoroughness, code reviews)
  - How budget affects documentation completeness
  - Trade-offs if budget is limited

- **Budget Allocation Strategy:**
  - Which stages get more budget allocation based on project priorities
  - Critical vs optional activities per stage

- **Budget Guidelines by Scale:**
  - **L2 (Tool)**: 50k-200k tokens (~$2-$10)
  - **L3 (Single Service)**: 200k-500k tokens (~$10-$25)
  - **L4 (MVP)**: 500k-1M tokens (~$25-$50)
  - **L5 (Multi-Platform)**: 1M-2M tokens (~$50-$100)
  - **L6-L7 (Growth/Platform)**: 2M+ tokens (~$100+)

- **User Approval Required:**
  - User must review and approve the budget before proceeding to later stages
  - Budget acts as a constraint for all subsequent AI agent activities

### Step 9: User Confirmation on 00-init-ideas Content

1. **Ask the user to review:**
   - All generated documentation in `00-init-ideas/`
   - The classification and project structure
   - Content accuracy and completeness
   - **For L2+ projects: CRITICAL - Review and approve the cost-budget.md:**
     - Estimated token usage per stage
     - Estimated cost in USD
     - Budget constraints that will affect later stages
     - User must explicitly approve the budget to proceed

2. **Make any adjustments based on user feedback**
   - If user wants to reduce budget: Adjust stage scope, research depth, or testing coverage
   - If user wants to increase budget: Expand scope, add more thorough research/testing
   - Update cost-budget.md accordingly

3. **Ask if they want to proceed to the next stage:**
   - For L0-L1: "Would you like me to implement the script in src/?"
   - For L2+: "Do you approve the estimated budget? Would you like me to proceed to the next stage (market-research or personas)?"

### Step 10: Initialize Git Repository (if needed)

1. Check if git repository is initialized
2. If not, run `git init`

### Step 11: Commit to Git (if user confirms)

1. **If user confirms the contents are good:**
   - Ask if they want to commit to git

2. **If user wants to commit:**
   - Stage all created/modified files
   - Use the dev-swarm-draft-commit-message skill to draft the commit message
   - Commit with the drafted message (should follow conventional commit format)
   - Example: "feat: initialize project with ideas documentation and stage structure"

## Expected Output Structure

The output structure varies based on project scale:

### For L0-L1 (Very Small Projects):
```
project-root/
├── README.md (root readme - not modified by this skill)
├── 00-init-ideas/
│   └── README.md (how to implement the script)
├── src/
│   ├── README.md (project documentation maintained by developers)
│   └── script_name.sh (or appropriate file)
└── features/, 99-archive/ (with .gitkeep)
```

### For L2 (Tool with Environment Setup):
```
project-root/
├── README.md (root readme - not modified by this skill)
├── 00-init-ideas/
│   ├── README.md
│   ├── problem-statement.md
│   ├── target-users.md
│   ├── value-proposition.md
│   ├── owner-requirement.md
│   └── cost-budget.md (REQUIRED)
├── 01-market-research/SKIP.md
├── 02-personas/README.md (or SKIP.md)
├── 03-mvp/SKIP.md (or README.md)
├── 04-prd/README.md
├── 05-ux/SKIP.md
├── 06-architecture/SKIP.md
├── 07-tech-specs/README.md
├── 08-devops/README.md
├── 09-sprints/README.md
├── 10-deployment/SKIP.md
├── features/
├── src/
│   └── README.md (project documentation maintained by developers)
└── 99-archive/
```

### For L3+ (Full-Scale Applications):
```
project-root/
├── README.md (root readme - not modified by this skill)
├── 00-init-ideas/ (full documentation including cost-budget.md)
│   ├── README.md
│   ├── problem-statement.md
│   ├── target-users.md
│   ├── value-proposition.md
│   ├── owner-requirement.md
│   └── cost-budget.md (REQUIRED)
├── 01-market-research/README.md
├── 02-personas/README.md
├── 03-mvp/README.md
├── 04-prd/README.md
├── 05-ux/README.md
├── 06-architecture/README.md
├── 07-tech-specs/README.md
├── 08-devops/README.md
├── 09-sprints/README.md
├── 10-deployment/README.md (or SKIP.md if not deploying yet)
├── features/
├── src/
│   └── README.md (project documentation maintained by developers)
└── 99-archive/
```

## Key Principles

- **Scale-Appropriate Development**: Create only the documentation and structure necessary for the project scale
- **Prevent Over-Engineering**: Explicitly skip stages that don't apply to the project purpose and scale
- **Clear Classification**: Document project purpose and scale to guide all future decisions
- **Budget-Conscious AI Development**: Since every AI action costs tokens, budget planning is CRITICAL
  - L2+ projects MUST include cost-budget.md with token estimates and USD costs
  - Budget directly constrains research depth, testing thoroughness, and documentation completeness
  - User approval of budget is required before proceeding to later stages
  - Budget acts as a constraint for all subsequent AI agent activities
- **Transform Informal to Professional**: Convert non-technical ideas into structured business documentation
- **Maintain Ownership**: Clear ownership and accountability for each stage
- **Explicit Exclusions**: Document what the project will NOT include based on its scale
- **Actionable Documentation**: Create clear, actionable documentation that guides development
- **Human-in-the-Loop**: Confirm structure, content, and budget with user before proceeding
