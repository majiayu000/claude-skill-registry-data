---
name: generating-readmes
description: Generate comprehensive README files for projects. Use when the user asks to create, generate, or write a README, readme file, or project documentation.
allowed-tools: read_file, write_file, list_directory
---

# README Generator

## Instructions

Generate a comprehensive, professional README.md file for the project. Follow this structured approach:

### Step 1: Analyze Project Structure

First, understand what kind of project this is:

1. **Explore the project directory** using `list_directory` to understand the structure
2. **Identify the project type** by looking for key files:
   - Python: `setup.py`, `pyproject.toml`, `requirements.txt`, `Pipfile`
   - Node.js: `package.json`, `package-lock.json`, `yarn.lock`
   - Rust: `Cargo.toml`, `Cargo.lock`
   - Go: `go.mod`, `go.sum`
   - Java: `pom.xml`, `build.gradle`
   - Other: Look for configuration files, main entry points

3. **Read configuration files** using `read_file` to extract:
   - Project name and description
   - Version information
   - Dependencies and requirements
   - Scripts and commands
   - License information
   - Author/maintainer information

### Step 2: Identify Key Components

1. **Find the main entry point**:
   - Look for `main.py`, `index.js`, `src/main.rs`, `main.go`, etc.
   - Use `grep_search` to find executable scripts or entry points
   - Check package.json "bin" field, setup.py entry_points, etc.

2. **Discover project features**:
   - Read source files to understand what the project does
   - Look for `__init__.py`, `index.js`, or main modules
   - Check for example files, demo scripts, or test files

3. **Identify usage patterns**:
   - Look for CLI commands defined in package.json, setup.py, or Cargo.toml
   - Check for configuration files (`.env.example`, `config.yaml`, etc.)
   - Find example usage in code comments or test files

### Step 3: Generate README Sections

Create a well-structured README.md with these sections (include only relevant ones):

#### Required Sections:

1. **Project Title** - Clear, descriptive title
   - Use the project name from config files (package.json, setup.py, etc.)
   - Add a brief one-line description if available

2. **Description** - What the project does
   - Extract from config files (package.json "description", setup.py "long_description")
   - If not found, analyze source code to write a clear description
   - Explain the purpose and main features

3. **Installation** - How to install
   - Python: `pip install`, `pip install -e .`, or `pip install -r requirements.txt`
   - Node.js: `npm install` or `yarn install`
   - Rust: Installation from crates.io or `cargo install`
   - Go: `go install` or `go get`
   - Include prerequisites if needed (Python version, Node version, etc.)

4. **Usage** - How to use the project
   - Basic usage examples
   - CLI commands if applicable (from package.json scripts, setup.py entry_points)
   - Code examples showing key functionality
   - Configuration options if there's a config file

#### Optional Sections (include if relevant):

5. **Features** - Key features and capabilities
   - List main features discovered from code analysis
   - Highlight unique or important capabilities

6. **Configuration** - Setup and configuration
   - Environment variables (check for `.env.example` or `.env`)
   - Configuration files (describe structure and options)
   - Default settings

7. **Development** - For contributors
   - How to set up development environment
   - How to run tests (`npm test`, `pytest`, `cargo test`, etc.)
   - How to build/compile if applicable
   - Development dependencies

8. **Requirements/Dependencies** - What's needed
   - List key dependencies (from requirements.txt, package.json, etc.)
   - System requirements
   - Version constraints if critical

9. **Contributing** - How to contribute
   - Link to contributing guidelines if CONTRIBUTING.md exists
   - Or provide basic contribution instructions

10. **License** - Project license
    - Extract from LICENSE file if present
    - Or from config files (package.json "license", setup.py "license")
    - Include license badge if applicable

11. **Author/Credits** - Who made it
    - From package.json "author", setup.py "author", etc.

12. **Badges** - Status badges (optional)
    - Add badges if repository info suggests GitHub/GitLab (CI/CD, coverage, etc.)

### Step 4: Write the README

1. **Use markdown formatting**:
   - Headers for sections
   - Code blocks with language tags for examples
   - Lists for features, requirements, etc.
   - Links for external resources
   - Tables if appropriate (for configuration options, etc.)

2. **Make it scannable**:
   - Use clear section headers
   - Include table of contents for long READMEs (if > 5 sections)
   - Use consistent formatting
   - Add emoji sparingly for visual interest (🚀 for getting started, ⚙️ for configuration, etc.)

3. **Include actual examples**:
   - Copy relevant code snippets from the project
   - Use real function names and API patterns from the codebase
   - Show actual CLI commands from the project

4. **Check for existing README**:
   - If README.md exists, read it first to preserve important information
   - Enhance and update rather than completely replace
   - Merge new sections with existing valuable content

### Step 5: Verify and Complete

1. **Read the generated README** back to ensure:
   - All sections are properly formatted
   - No placeholder text remains
   - Examples are accurate and work
   - Links are correct (if any)

2. **Ensure completeness**:
   - Installation instructions are clear
   - Usage examples are practical
   - All necessary information is included

## Examples

### Example 1: Python Package
User: "Generate a README for this Python project"
- Read `setup.py` or `pyproject.toml` for metadata
- Check `requirements.txt` for dependencies
- Find main module or entry point
- Generate README with pip install instructions

### Example 2: Node.js Application
User: "Create a README file"
- Read `package.json` for project info
- Extract scripts and commands
- Check for `.env.example` for configuration
- Generate README with npm/yarn commands

### Example 3: Existing README Update
User: "Update the README"
- Read existing README.md
- Analyze project changes
- Enhance with new sections or update existing ones
- Preserve valuable existing content

## Best Practices

1. **Be specific**: Use actual project information, not generic placeholders
2. **Match style**: Follow existing code style and naming conventions in the project
3. **Practical examples**: Show real usage patterns from the codebase
4. **Complete**: Include all necessary information for someone new to the project
5. **Accurate**: Verify all commands and examples work with the actual project setup

## Notes

- Always analyze the actual project before generating the README
- Don't guess - read configuration files and source code
- Adapt the README structure to the project's complexity
- Simple projects need simpler READMEs, complex projects need more detail

