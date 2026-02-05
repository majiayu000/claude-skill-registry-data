---
name: skilzy-creator
description: Comprehensive toolset for creating, converting, validating, and packaging Skilzy-compliant AI agent skills. This skill should be used when users want to initialize a new skill, convert a Claude skill archive to the Skilzy format, validate an existing skill's structure and compliance, or package a skill for distribution to the Skilzy registry.
---

# Skilzy Skill Creator

This skill provides a complete suite of tools and guidance for managing the entire lifecycle of Skilzy-compliant AI agent skills.

## Part 1: Understanding Skilzy Skills

### What Are Skills

Skills are modular, self-contained packages designed for the Skilzy.ai universal skills registry. They extend AI agents' capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks—they transform a general-purpose agent into a specialized agent equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex and repetitive tasks

### Anatomy of a Skilzy Skill

Every Skilzy skill consists of required metadata files and optional bundled resources:

```
skill-name/
├── skill.json (required)        - Skilzy manifest with metadata
├── SKILL.md (required)           - Agent instructions with YAML frontmatter
├── README.md (required)          - Human-readable registry documentation
├── LICENSE (required)            - License file
├── assets/
│   └── icon.svg                 - Skill icon for registry
├── scripts/                     - Executable code (Python/Bash/etc.)
├── references/                  - Documentation loaded into context as needed
└── assets/                      - Files used in output (templates, icons, etc.)
```

### The Dual Documentation System

Skilzy skills maintain **two separate documentation files** for different audiences:

**`SKILL.md` (For AI Agents):**
- Contains detailed, technical instructions for AI execution
- Includes YAML frontmatter (`name`, `description`) for backwards compatibility with Claude
- Specifies workflows, decision trees, and references to bundled resources
- Written in imperative/infinitive form
- AI agents load this file directly via filesystem access

**`README.md` (For Human Users):**
- Provides high-level overview for the skill registry
- Explains what the skill does and when to use it
- Describes features and benefits
- Includes installation/setup instructions
- Written for non-technical audience
- Displayed on the skill's detail page at skilzy.ai
- Referenced as `entrypoint` in `skill.json`

**Critical Distinction:** The `entrypoint` field in skill.json points to README.md so the registry displays human documentation, but AI agents always load SKILL.md directly for execution instructions.

### Resource Types Explained

**Scripts (`scripts/`)**

Executable code for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Example**: `scripts/rotate_pdf.py` for PDF rotation tasks
- **Benefits**: Token efficient, deterministic, may be executed without loading into context
- **Note**: Scripts may still need to be read by the agent for patching or environment-specific adjustments

**References (`references/`)**

Documentation and reference material intended to be loaded as needed into context to inform the agent's process and thinking.

- **When to include**: For documentation that the agent should reference while working
- **Examples**: `references/schema.md` for database schemas, `references/api_docs.md` for API specifications
- **Use cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when the agent determines it's needed
- **Best practice**: Information should live in either SKILL.md or references files, not both. Prefer references files for detailed information unless it's truly core to the skill.

**Assets (`assets/`)**

Files not intended to be loaded into context, but rather used within the output the agent produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/logo.png` for brand assets, `assets/template.pptx` for PowerPoint templates, `assets/boilerplate/` for code templates
- **Use cases**: Templates, images, icons, boilerplate code, fonts, sample documents that get copied or modified
- **Benefits**: Separates output resources from documentation, enables use without loading into context

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by the agent (Unlimited*)

*Unlimited because scripts can be executed without reading into context window, and references are loaded selectively.

---

## Part 2: The Skill Creation Workflow

Follow this workflow in order. Each step includes **mandatory reference loading** when detailed technical information is required.

### Step 1: Understanding the Skill with Concrete Examples

**Do not skip this step** unless the skill's usage patterns are already clearly understood.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

**Ask the user questions such as:**

- "What functionality should this skill support?"
- "Can you give some examples of how this skill would be used?"
- "What would a user say that should trigger this skill?"
- "Are there specific file types, APIs, or workflows this skill should handle?"

**Example questions for an image-editor skill:**

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed.

**Conclude this step when** there is a clear sense of the functionality the skill should support.

---

### Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly
3. Identifying metadata (keywords, dependencies, permissions) that will help users discover and use the skill

**Example analysis for a `pdf-editor` skill:**

When handling queries like "Help me rotate this PDF":
1. Rotating a PDF requires re-writing the same code each time
2. A `scripts/rotate_pdf.py` script would be helpful
3. Keywords: `["pdf", "document", "rotation", "editing"]`
4. Dependencies: `{"python": ["PyPDF2>=3.0"]}`

**Example analysis for a `frontend-webapp-builder` skill:**

When handling queries like "Build me a todo app":
1. Writing a frontend webapp requires the same boilerplate HTML/React each time
2. An `assets/template/` directory containing boilerplate project files would be helpful
3. Keywords: `["frontend", "react", "webapp", "html", "javascript"]`
4. Dependencies: `{"system": ["node"], "python": []}`

**Example analysis for a `bigquery` skill:**

When handling queries like "How many users have logged in today?":
1. Querying BigQuery requires re-discovering the table schemas and relationships each time
2. A `references/schema.md` file documenting the table schemas would be helpful
3. Keywords: `["bigquery", "sql", "database", "analytics"]`
4. Permissions: `{"network": {"allowedHosts": ["bigquery.googleapis.com"], "description": "Query BigQuery API"}}`

**Create a planning document that lists:**
- Scripts to include in `scripts/`
- Reference files to include in `references/`
- Assets to include in `assets/`
- Keywords for discoverability
- Dependencies (Python packages, system tools, other skills)
- Permissions required (network, filesystem)

---

### Step 3: Initialize the Skill

**Skip this step only if** the skill being developed already exists and iteration or packaging is needed. In that case, proceed to Step 4.

When creating a new skill from scratch, **always run the `init_skill.py` script**. The script generates a complete skill directory with all required files, making the creation process efficient and reliable.

**Basic usage:**

### Command Syntax

```bash
python scripts/init_skill.py <skill-name> [options]
```

**Arguments:**
- `<skill-name>` - Name of the skill (required in non-interactive mode)

**Options:**
- `--non-interactive` - Run without prompts (for AI agents)
- `--description <text>` - Skill description (required in non-interactive)
- `--author <name>` - Author name
- `--license <type>` - License type (default: MIT)
- `--keywords <list>` - Comma-separated keywords
- `--repository <url>` - Git repository URL
- `--python-deps <list>` - Comma-separated Python packages
- `--system-deps <list>` - Comma-separated system tools
```

**What this creates:**
- Complete skill directory with `skill.json`, `SKILL.md`, `README.md`, `LICENSE`
- Empty resource directories: `scripts/`, `references/`, `assets/`
- Example files that can be customized or deleted

**⚠️ REQUIRED: Before executing the initialization command, MUST load `references/tool-init.md` to understand:**
- Complete command syntax and all available options
- Interactive vs non-interactive mode
- What each generated file contains
- Default values and how to customize them
- Example workflows

**To load the reference:**

```bash
cat references/tool-init.md
```

After loading the reference and understanding the tool, execute the initialization command and proceed to Step 4.

---

### Step 4: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another instance of an AI agent to use. Focus on including information that would be beneficial and non-obvious to another agent. Consider what procedural knowledge, domain-specific details, or reusable assets would help another agent execute these tasks more effectively.

**Writing style for all skill content:** Use **imperative/infinitive form** (verb-first instructions), not second person. Use objective, instructional language (e.g., "To accomplish X, do Y" rather than "You should do X"). This maintains consistency and clarity for AI consumption.

#### Step 4a: Add Bundled Resources

Based on the planning from Step 2, implement the reusable resources:

**Scripts:**
1. Create each script identified in the planning phase
2. Place in `scripts/` directory
3. Include docstrings explaining parameters and return values
4. Make scripts executable if needed
5. Test each script independently

**References:**
1. Create each reference file identified in the planning phase
2. Place in `references/` directory
3. Use clear markdown formatting
4. Include examples and usage guidance
5. Keep files focused on a single topic

**Assets:**
1. Add each asset file/directory identified in the planning phase
2. Place in `assets/` directory
3. Organize by type (templates/, images/, etc.)
4. Include any necessary metadata files

**Delete unused example files** created by the initialization script.

#### Step 4b: Write SKILL.md (Agent Instructions)

The SKILL.md file already has YAML frontmatter with a TODO placeholder. Update it by answering these questions:

1. **What is the purpose of the skill?** (2-3 sentences)
2. **When should the skill be used?** (Specific triggers, file types, scenarios)
3. **How should the agent use the skill in practice?**
   - Reference all bundled scripts by path
   - Explain when to load reference files
   - Provide decision trees for complex workflows
   - Include examples for common use cases

**Keep SKILL.md lean:** Move detailed information to `references/` files. SKILL.md should contain:
- Overview and purpose
- When to use the skill
- High-level workflows
- Pointers to bundled resources
- References to load for detailed information

**Update the YAML frontmatter description** to be complete and informative. The description should specify WHEN to use the skill (specific scenarios, file types, or tasks that trigger it).

#### Step 4c: Write README.md (Human Documentation)

The README.md is for human users browsing the Skilzy registry. It should be high-level and accessible.

**Include these sections:**

1. **Overview** - What the skill does in 2-3 sentences
2. **Features** - Key capabilities (bullet list)
3. **When to Use** - Example scenarios
4. **Installation** - `skilzy install <author>/<skill-name>.skill`
5. **Usage Examples** - Sample user requests that trigger the skill
6. **Requirements** - Any prerequisites or setup needed
7. **License** - Brief license statement

**Tone:** Friendly and accessible, written for non-technical users. Avoid implementation details.

#### Step 4d: Update skill.json Metadata

The skill.json manifest was generated with default values. Update it based on planning from Step 2.

**Required updates:**

1. **description** - Complete, informative explanation (20-250 characters)
   - Must specify WHAT the skill does
   - Must specify WHEN to use it (scenarios, file types, triggers)
   - Example: "Processes and analyzes CSV files to generate statistical summaries. Use when the user uploads a CSV and requests data analysis, trends, or visualizations."

2. **keywords** - Array of lowercase, hyphen-separated keywords
   - Include domain terms, file types, use cases
   - Example: `["pdf", "document", "editing", "rotation", "merge"]`

3. **dependencies** - List ALL required dependencies
   - `python`: Python packages (e.g., `["pandas>=2.0", "numpy>=1.20"]`)
   - `system`: System tools (e.g., `["ffmpeg", "imagemagick"]`)
   - `skills`: Other skills (e.g., `["data-validator>=1.0.0"]`)

4. **permissions** - Declare required resource access
   - `network`: If skill makes API calls
   - `filesystem`: If skill reads/writes specific paths

5. **author** - Your name or organization
6. **license** - License identifier (e.g., "MIT", "Apache-2.0")
7. **repository** - Source code URL if applicable

**⚠️ REQUIRED: Before editing skill.json, MUST load `references/schema-reference.md` to understand:**
- Complete schema specification
- Field-by-field explanations
- Validation rules for each field
- Common patterns and examples

**To load the schema reference:**

```bash
cat references/schema-reference.md
```

**Optional: Load `references/examples.md`** for complete skill.json examples from real skills.

After loading references and understanding the schema, update the skill.json file.

---

### Step 5: Validate and Package

Before packaging, the skill must be validated to ensure it meets all Skilzy specifications.

#### Validation

**⚠️ REQUIRED: Before running validation, MUST load `references/tool-validate.md` to understand:**
- What the validator checks
- Schema validation rules
- Filesystem validation rules
- How to interpret validation output
- Common errors and how to fix them

**To load the validation reference:**

```bash
cat references/tool-validate.md
```

After loading the reference, run the validation command:

```bash
python scripts/validate_skill.py <path/to/skill-directory>/
```

**If validation fails:**
1. Review the error messages carefully
2. Load `references/troubleshooting.md` for guidance on specific errors
3. Fix the identified issues
4. Re-run validation until all checks pass

**To load troubleshooting guide when errors occur:**

```bash
cat references/troubleshooting.md
```

**Do not proceed to packaging until validation passes.**

#### Packaging

Once validation passes, package the skill for distribution.

**⚠️ REQUIRED: Before running packaging, MUST load `references/tool-package.md` to understand:**
- Packaging process and options
- Output directory specification
- Custom naming options
- Archive structure
- What gets included in the package

**To load the packaging reference:**

```bash
cat references/tool-package.md
```

After loading the reference, run the packaging command:

```bash
python scripts/package_skill.py <path/to/skill-directory>/ -o dist/
```

This creates a `.skill` archive in the `dist/` directory named `{skill-name}-{version}.skill`.

---

### Step 6: Publish to Registry

Once the skill is packaged, publish it to the Skilzy registry to make it available to all users.

**Publishing options:**

**Option 1: Using the Skilzy SDK (Recommended)**

```bash
# Install the SDK
pip install skilzy

# Authenticate with your API key
skilzy login <your-skilzy-api-key>

# Publish the packaged skill
skilzy publish dist/my-skill-1.0.0.skill
```

**Option 2: Web upload**

1. Visit https://skilzy.ai/publish
2. Log in with your account
3. Upload the `.skill` file
4. Fill in any additional registry metadata
5. Submit for publication

**Getting an API key:**
1. Create an account at https://skilzy.ai
2. Navigate to Settings > API Keys
3. Generate a new API key
4. Use for SDK authentication

**After publishing:**
- Skill becomes discoverable at https://skilzy.ai/skills/{author}/{skill-name}
- Users can install with: `skilzy install {author}/{skill-name}.skill`
- Registry displays the README.md content on the skill's detail page

---

### Step 7: Iterate

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**

1. **Use the skill on real tasks** - Test with actual user requests
2. **Notice struggles or inefficiencies** - Where did the agent get confused? What took too long?
3. **Identify improvements** - How should SKILL.md or bundled resources be updated?
4. **Implement changes:**
   - Update SKILL.md instructions
   - Add or modify scripts
   - Add reference files for missing information
   - Update skill.json dependencies or keywords
5. **Update version number** - Follow Semantic Versioning:
   - Increment PATCH for bug fixes (1.0.0 → 1.0.1)
   - Increment MINOR for new features (1.0.1 → 1.1.0)
   - Increment MAJOR for breaking changes (1.1.0 → 2.0.0)
6. **Re-validate and re-package** - Repeat Step 5
7. **Publish updated version** - Repeat Step 6

**Gather feedback from:**
- Direct testing and observation
- User reports and feature requests
- Error logs and failure cases
- Performance metrics

Continue iterating to refine the skill over time.

---

## Part 3: Tool Quick Reference

The Skilzy Creator includes four Python tools for skill management. Each tool has detailed documentation in the `references/` directory.

### Available Tools

**`init_skill.py`** - Initialize new skill directories

**Purpose:** Create a new, valid Skilzy skill directory with all required files and proper structure.

**Basic usage:** `python scripts/init_skill.py <skill-name> --non-interactive`

**When to use:** Creating a brand new skill from scratch (Step 3)

**⚠️ Load `references/tool-init.md` before using**

---

**`convert_skill.py`** - Convert Claude skills to Skilzy format

**Purpose:** Migrate a skill from the Claude format (YAML frontmatter only) to the modern Skilzy format while maintaining backwards compatibility.

**Basic usage:** `python scripts/convert_skill.py <path/to/claude-skill.zip>`

**When to use:** Converting an existing Claude skill to Skilzy format

**⚠️ Load `references/tool-convert.md` before using**

---

**`validate_skill.py`** - Validate skill compliance

**Purpose:** Verify that a skill directory conforms to the Skilzy specification by checking schema compliance and filesystem integrity.

**Basic usage:** `python scripts/validate_skill.py <path/to/skill-directory>/`

**When to use:** Before packaging (Step 5) or when debugging issues

**⚠️ Load `references/tool-validate.md` before using**

---

**`package_skill.py`** - Package skills for distribution

**Purpose:** Bundle a validated skill into a distributable `.skill` archive suitable for upload to the Skilzy registry.

**Basic usage:** `python scripts/package_skill.py <path/to/skill-directory>/ -o dist/`

**When to use:** After validation passes in Step 5

**⚠️ Load `references/tool-package.md` before using**

---

## Part 4: Best Practices

### 1. Separation of Concerns

**SKILL.md = Technical instructions for AI agents**
- Detailed procedural steps
- References to bundled resources
- Decision trees and conditionals
- Written for machine consumption (though human-readable)

**README.md = High-level overview for humans**
- What the skill does
- Why users should install it
- Key features and benefits
- Installation and usage guidance

This dual-documentation system ensures the registry displays human-friendly content while agents receive precise instructions.

### 2. Write Clear, Actionable Agent Instructions

In SKILL.md, use imperative form:

✅ "To process a CSV file, execute `scripts/process_csv.py <filename>`"

❌ "You should process CSV files using the script"

Provide context and examples:

```markdown
## Processing Tabular Data

When the user provides a CSV or Excel file:

1. Identify the file type by extension
2. If CSV: Execute `python scripts/process_csv.py <filename>`
3. If Excel: Execute `python scripts/process_excel.py <filename>`
4. Parse the output and present results to the user
```

### 3. Organize Bundled Resources Strategically

**`scripts/` directory:**
- Name files descriptively: `validate_email.py`, not `utils.py`
- Include docstrings explaining parameters and return values
- Make scripts executable when appropriate
- Test scripts independently

**`references/` directory:**
- Store schemas, API documentation, or detailed guides
- Use when information is too detailed for SKILL.md
- Reference by path in SKILL.md: "See `reference/api_docs.md` for full endpoint list"

**`assets/` directory:**
- Template files meant to be copied or modified
- Images or icons used in output
- Boilerplate code directories
- Not loaded into context; used in the final output

### 4. Validate Continuously During Development

Integrate validation into your workflow:

1. Make changes to skill files
2. Run `python scripts/validate_skill.py my-skill/`
3. Fix any errors immediately
4. Repeat until validation passes

Don't wait until packaging to validate. Catching errors early saves time.

### 5. Write Descriptive Metadata

In `skill.json`, the `description` field should:

- Be 20-250 characters (enforced by schema)
- Specify **what** the skill does
- Specify **when** it should be used
- Include trigger scenarios or file types

**Example:**

```json
{
  "description": "Processes and analyzes CSV files to generate statistical summaries. Use when the user uploads a CSV and requests data analysis, trends, or visualizations."
}
```

### 6. Use Keywords for Discoverability

Add relevant keywords to help users find your skill:

```json
{
  "keywords": ["data", "csv", "analysis", "statistics", "excel"]
}
```

Keywords should:
- Be lowercase
- Use hyphens for multi-word terms (`data-analysis`)
- Be specific to the skill's domain
- Help with registry search

### 7. Version Your Skills Semantically

Follow **Semantic Versioning (SemVer)**:

- `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)
- Increment MAJOR for breaking changes
- Increment MINOR for new features (backwards compatible)
- Increment PATCH for bug fixes

**Example progression:**
- `0.1.0` - Initial development
- `1.0.0` - First stable release
- `1.1.0` - Added new feature
- `1.1.1` - Fixed a bug
- `2.0.0` - Breaking change (API change, file structure change)

### 8. Keep SKILL.md Lean

Move detailed information to reference files:

- Database schemas → `references/schema.md`
- API documentation → `references/api_docs.md`
- Detailed examples → `references/examples.md`
- Troubleshooting → `references/troubleshooting.md`

SKILL.md should contain only:
- Overview and purpose
- High-level workflows
- When to load reference files
- Pointers to bundled resources

---

## Reference Loading Guide

**CRITICAL:** Load the following references as needed during the workflow. Do not skip reference loading when indicated.

**During Step 3 (Initialize):**
- **MUST load** `references/tool-init.md` before running init_skill.py
- Command: `cat references/tool-init.md`

**When Converting Existing Skills:**
- **MUST load** `references/tool-convert.md` before running convert_skill.py
- Command: `cat references/tool-convert.md`

**During Step 4 (Edit skill.json):**
- **MUST load** `references/schema-reference.md` to understand schema
- Command: `cat references/schema-reference.md`
- **Optional:** Load `references/examples.md` for complete examples
- Command: `cat references/examples.md`

**During Step 5 (Validate):**
- **MUST load** `references/tool-validate.md` before running validation
- Command: `cat references/tool-validate.md`
- **If errors occur:** Load `references/troubleshooting.md`
- Command: `cat references/troubleshooting.md`

**During Step 5 (Package):**
- **MUST load** `references/tool-package.md` before running packaging
- Command: `cat references/tool-package.md`

**When Encountering Any Errors:**
- Load `references/troubleshooting.md` for diagnosis and solutions
- Command: `cat references/troubleshooting.md`
