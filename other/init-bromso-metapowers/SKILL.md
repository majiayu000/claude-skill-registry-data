---
description: Initialize a .metapowers/ directory and configure active domains for a project
---

# Init

Initialize the `.metapowers/` directory for the current project. Set up the project configuration and choose which domains to activate.

## Prerequisites

None — this is typically the first Metapowers command you run in a new project.

## Process

1. **Check if `.metapowers/` already exists:**
   - If it exists, read `.metapowers/config.md` and show current configuration
   - Ask if the user wants to update the configuration
   - If it doesn't exist, proceed with initialization

2. **Ask the user:**
   - What is the project name?
   - Which domains will you use? Present the full list:
     - Design (component design with Figma integration)
     - Research (Double Diamond discovery and validation)
     - Development (plan, build, test, debug, review, ship)
     - Marketing (RACE Framework campaigns)
     - Branding (brand creation and compliance)
     - Accessibility (WCAG-EM audits)
     - Project Management (Scrum workflow)
     - Coaching (domain-specific mentorship)
     - Leadership (team development and management)
     - Legal (contracts, compliance, governance)

3. **Create the directory structure:**
   - Create `.metapowers/` root directory
   - Create subdirectories for each selected domain
   - Create `.metapowers/reports/` for cross-domain reports

4. **Write the project configuration:**
   - Write `.metapowers/config.md` with:
     - Project name
     - Active domains
     - Date initialized
     - Notes or goals (if the user provided any)

5. **Suggest next steps:**
   - Based on selected domains, recommend which to start with
   - Provide the first command to run

## Output

The project configuration written to `.metapowers/config.md`. Present the initialized structure and suggested next steps to the user.
