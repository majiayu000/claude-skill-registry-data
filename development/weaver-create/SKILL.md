---
name: weaver
description: Weaves custom Skills for Claude following official best practices including proper structure, metadata, progressive disclosure, and security guidelines. Use when creating new skills, building custom workflows, or when user mentions skill creation, skill development, custom skill authoring, weaving skills, or crafting skills.
metadata:
  version: 0.2.1
  dependencies: none
---

# Skill Weaver

> **Note**: Anthropic provides default skills including "skill-builder" and "skill-creator" that may also respond to skill creation requests. If you prefer to use this Skill Weaver instead, you can be explicit in your request (e.g., "use weaver to create a skill for...") or manage your enabled skills in settings.

## Overview
This Skill helps users create Skills for both Claude Code and claude.ai following official best practices. It guides through creating SKILL.md files, structuring directories, adding resources, and ensuring quality.

**What are Skills?**
Skills package expertise into discoverable capabilities. Each Skill consists of a SKILL.md file with instructions that Claude reads when relevant, plus optional supporting files like scripts and templates.

**Model-invoked**: Skills are autonomously triggered by Claude based on your request and the Skill's description. This is different from slash commands (which you explicitly type to trigger).

## Version

**Current Version**: 0.2.1

This release renames the directory to "weaver-create" to fully avoid conflicts with Anthropic's default skills. For version history and changelog, see [README.md](README.md#version-history).

## Platform Support

Skill Weaver supports two platforms:

### Claude Code (Agent Skills)
- Filesystem-based storage (`~/.claude/skills/`, `.claude/skills/`)
- Plugin distribution for team sharing
- Tool restrictions via `allowed-tools` field
- Auto-installs dependencies from PyPI/npm
- Debug mode: `claude --debug`

### claude.ai (Custom Skills)
- Upload via Settings > Capabilities (ZIP file)
- Manual distribution (share ZIP files)
- No `allowed-tools` field support
- Can install packages from PyPI/npm when needed
- Review Skill usage in conversation thinking

**Common Features** (both platforms):
- SKILL.md with YAML frontmatter
- Progressive disclosure (metadata → SKILL.md → additional files)
- Same naming conventions and best practices
- Scripts, templates, and resources support

## When to Use This Skill
Use when:
- User asks to create a new Skill
- User wants to build a custom workflow for Claude
- User needs help structuring a Skill directory
- User asks about Skill authoring best practices
- User wants to package, test, or share a Skill

## Adaptive Skill Creation Workflow

This Skill uses a create-review-adapt approach that minimizes friction while adapting to user engagement level.

### Three-Phase Interaction Model

**Phase 1: AUTONOMOUS CREATE (with progress indicators)**
- Create a complete, functional Skill based on the user's initial request
- Show clear progress as you work:
  ```
  Creating Skill structure... ✓
  Writing description and metadata... ✓
  Generating core instructions... ✓
  Adding examples and templates... ✓
  ```
- Make intelligent decisions about structure, scope, and features
- Aim for a production-ready Skill that could be used immediately
- **Create artifacts for visibility**: Use the Write tool to create each file (SKILL.md, REFERENCE.md, templates, scripts) which opens artifact panes showing users what's being built in real-time

**Phase 2: CONCISE SUMMARY (with offer to elaborate)**
- Present a digestible summary of what was created
- List files created (SKILL.md, REFERENCE.md, templates, etc.)
- Summarize key features (3-5 bullets)
- Provide prominent download link to artifact/ZIP
- Offer to explain: "I can explain any decisions if you'd like"
- Solicit feedback with open-ended question: "What would you like to adjust?"

**Phase 3: ENGAGEMENT DETECTION (adapt based on feedback)**
- Analyze the user's response to determine engagement level
- Adapt your iteration approach accordingly

### Detecting Engagement Levels

**Low Engagement** - User provides minimal feedback:
- Examples: "looks good", "ship it", "that works", "👍"
- **Response**: Package immediately, provide installation instructions
- **Why**: User trusts your judgment and wants quick results
- Skip further iteration unless they ask

**Medium Engagement** - User requests specific changes:
- Examples: "tweak the description", "add error handling", "change the name"
- **Response**: Make the requested adjustments efficiently
- Present updated version briefly
- Ask: "Ready to package, or any other changes?"
- **Why**: User has specific needs but doesn't want deep collaboration

**High Engagement** - User asks detailed questions or expresses uncertainty:
- Examples: "How does X work?", "Should we handle Y?", "What about Z scenario?"
- **Response**: Switch to collaborative checkpoint mode
- Break remaining work into smaller steps
- Explain options and trade-offs
- Ask for input before each significant decision
- **Why**: User wants to understand and influence the design

### Download Link Management

**Re-emphasize download links** to keep them visible and accessible:

**After providing explanations:**
```
[Detailed explanation of validation patterns]

**Download:** [Download api-testing.zip]

Any other questions, or ready to use it?
```

**After making changes:**
```
✓ Updated to include GraphQL support

**Download:** [Download api-testing.zip]

Ready to go, or any other changes?
```

**Why this matters:**
- Download links get lost in scrollback after detailed responses
- Users need easy access to the artifact/ZIP file
- Repeated links reduce frustration and improve UX

### Progress Indicators Best Practices

Show progress during autonomous creation to:
- Reassure the user that work is happening
- Indicate what stage you're at
- Set expectations for what's being created

**Good progress indicators:**
```
Analyzing requirements... ✓
Setting up Skill structure for claude.ai... ✓
Writing SKILL.md with comprehensive instructions... ✓
Creating validation script template... ✓
Preparing example prompts for testing... ✓
```

**Avoid:**
- Too many micro-updates (overwhelming)
- Vague indicators ("working...", "processing...")
- No indicators at all (user wonders what's happening)

### Decision Explanation Examples

When presenting the Skill in Phase 2, explain your key choices:

**Platform decisions:**
"I created this for both platforms since you didn't specify. This means omitting `allowed-tools` (Claude Code-only), but it gives you maximum flexibility for distribution."

**Structural decisions:**
"I included a REFERENCE.md file for detailed API documentation instead of putting everything in SKILL.md. This keeps the main instructions concise while Claude can load the reference on-demand when needed."

**Scope decisions:**
"I focused on the core workflow you described and added basic error handling. I didn't include advanced edge cases yet - we can add those if you need them."

**Description decisions:**
"The description mentions 'CSV', 'data analysis', and 'pandas' as triggers. This should invoke the Skill when you're working with data files without being too broad."

### Workflow Variants

Users can explicitly request different interaction styles. Recognize these requests and adapt accordingly.

#### Quick Create Mode

**Purpose:** Fast, autonomous Skill creation with minimal interaction.

**When users request this:**
- "just make it"
- "create quickly"
- "I trust your judgment, just build it"
- "make a basic version fast"
- "no need to ask me questions, just do it"

**Workflow:**
1. Ask minimal clarifying questions (only platform and basic purpose)
2. Create skill autonomously with progress indicators
3. Show brief summary of what was created
4. Package immediately
5. Provide installation instructions

**What to skip:**
- Lengthy review with decision explanations
- Asking "what would you like to adjust?"
- Waiting for feedback before packaging
- Suggesting additional features

**Example interaction:**
```
User: "Just create a skill for code reviews quickly"

AI: "Creating code-review skill for both platforms...

Creating Skill structure... ✓
Writing description and instructions... ✓
Adding review checklist... ✓
Packaging... ✓

✓ All set! Here's your code-reviewer.zip

**Installation:**
[Brief platform-specific instructions]

**Quick test:**
Try: 'Review this Python file for best practices'"
```

#### Guided Create Mode

**Purpose:** Collaborative, educational Skill creation with user involved at each step.

**When users request this:**
- "walk me through it"
- "let's build this together"
- "I want to understand the process"
- "help me learn how to create this"
- "let's do this step by step"
- "can you explain as we go?"

**Workflow:**
1. Start with comprehensive requirements gathering
2. Present options for major decisions (platform, structure, scope)
3. Explain tradeoffs and implications
4. Get user input before proceeding with each section
5. Show work in progress at checkpoints
6. Explain choices as you make them
7. Invite questions throughout

**What to include:**
- Detailed explanations of decisions
- Options and tradeoffs
- Educational context about Skills
- Frequent checkpoints for feedback
- Encouragement to ask questions

**Example interaction:**
```
User: "Walk me through creating a skill for data analysis"

AI: "I'd be happy to guide you through creating a data-analysis skill! Let's start by making some key decisions together.

**Platform Choice:**
We need to decide where this skill will run:
- **Claude Code only**: Can use tool restrictions, distribute via plugin
- **claude.ai only**: ZIP upload, simpler for individuals
- **Both platforms**: Maximum compatibility, skip platform-specific features

Which environment are you targeting?"

User: "Both platforms"

AI: "Great choice for maximum flexibility! Since we're targeting both platforms, we'll use the metadata field format and skip the allowed-tools field.

**Skill Scope:**
For data analysis, we could focus on:
- **Option A**: General CSV/Excel analysis (pandas-based, broad applicability)
- **Option B**: Specific analysis type (e.g., time series, statistical)
- **Option C**: Domain-specific (e.g., sales data, scientific data)

What type of data analysis will this skill handle?"

[Continues with collaborative decision-making]
```

#### Default Mode (Adaptive)

**Purpose:** Balanced approach that adapts to user's natural engagement level.

**When to use:**
- User doesn't specify a mode
- Standard skill creation requests
- Most common scenario

**Workflow:**
1. Use the three-phase model (create → review → adapt)
2. Present completed skill with decision explanations
3. Detect engagement level from user's feedback
4. Adjust iteration style accordingly

**Key principle:**
Let the user's feedback reveal their preferred engagement level rather than asking them to choose upfront.

**Example interaction:**
```
User: "Create a skill for API testing"

AI: [Autonomous create phase with progress indicators]

"I've created an api-testing skill for both platforms. Here's what I built:

**Key Decisions:**
- Platform: Both (you didn't specify, this maximizes flexibility)
- Scope: REST API testing with request validation and response checking
- Structure: Main instructions in SKILL.md, advanced patterns in REFERENCE.md
- Description: Triggers on 'API', 'endpoint', 'testing', or 'REST'

**What's included:**
- Request building and validation
- Response assertion patterns
- Error handling and logging
- Example test scenarios

What would you like to adjust?"

[User feedback determines next steps]
- "looks good" → Package immediately
- "add GraphQL support" → Make change, ask if ready
- "How does validation work?" → Switch to collaborative mode
```

#### Choosing the Right Mode

**Use Quick Create when:**
- User emphasizes speed or urgency
- User explicitly trusts your judgment
- Task is straightforward and well-defined
- User has done this before and knows what they want

**Use Guided Create when:**
- User is learning about Skills
- User asks to be involved in decisions
- Task has multiple valid approaches
- User wants to understand the "why" behind choices

**Use Default (Adaptive) when:**
- User doesn't specify a preference (most common)
- You're unsure of user's experience level
- Standard skill creation request

#### Mode Switching

You can switch modes mid-creation if user signals change in engagement:

**From Quick to Guided:**
```
[You're in quick create, packaging]
User: "Wait, can you explain why you structured it this way?"
→ Stop packaging, switch to guided mode, provide explanation
```

**From Guided to Quick:**
```
[You're asking detailed questions]
User: "Actually, just make the decisions and show me what you build"
→ Switch to quick create, proceed autonomously
```

**From Default to either:**
- Watch for explicit mode requests
- Adapt based on engagement signals
- Natural transitions are better than forced mode declarations

### Handling Mixed Signals

If engagement level is unclear:
- Default to medium engagement
- Make the requested changes
- Provide one more checkpoint: "How does this look?"
- Adjust based on next response

### When to Package and Deliver

**Package immediately when:**
- User gives low-engagement feedback ("looks good")
- User explicitly says to finalize/ship/package
- User asks "how do I install this?"
- You've made requested changes and gotten approval

**Continue iterating when:**
- User asks more questions
- User requests additional changes
- User expresses uncertainty ("hmm, not sure about...")
- User wants to explore alternatives ("what if we...")

### Example Interaction Flow

**Initial Request:**
User: "Create a skill for reviewing Python code"

**Phase 1 - Autonomous Create:**
```
Creating Skill structure... ✓
Writing description and metadata... ✓
Generating code review instructions... ✓
Adding Python best practices... ✓
Creating example prompts... ✓
```

**Phase 2 - Concise Summary:**
"✓ Created your code-reviewer Skill! Here's what I built:

**Files created:**
- SKILL.md (main review instructions)
- REFERENCE.md (detailed Python patterns)
- templates/review-checklist.md

**Key features:**
- Python best practices and PEP 8 checking
- Security vulnerability detection
- Code style analysis
- Common anti-pattern identification

**Download:** [Download code-reviewer.zip]

I can explain any decisions if you'd like. What would you like to adjust?"

**Phase 3 - Engagement Detection:**

*Low engagement response:* "Looks great!"
→ Package immediately, provide installation instructions

*Medium engagement response:* "Can you add type hint checking?"
→ Add type hints to checklist, show update, ask if ready

*High engagement response:* "Should we include async code patterns? What about testing coverage?"
→ Switch to collaborative mode, discuss options, get input on priorities

## Core Principles

### Conciseness is Key
The context window is a public good. Your Skill shares it with system prompts, conversation history, other Skills' metadata, and the user's request. Be concise:
- Only include information Claude doesn't already have
- Assume Claude is intelligent and knowledgeable
- Challenge each piece: "Does Claude really need this?"
- Keep Skill.md body under 500 lines
- Move detailed content to REFERENCE.md

**Good (concise):** "Use pdfplumber for PDF text extraction"
**Bad (verbose):** "PDF (Portable Document Format) files are common... you'll need a library... there are many options..."

### Set Appropriate Freedom
Match specificity to task fragility:
- **High freedom** (text instructions): Multiple valid approaches, context-dependent decisions
- **Medium freedom** (pseudocode/parameterized scripts): Preferred pattern with acceptable variation
- **Low freedom** (exact scripts): Fragile operations requiring specific sequences

### Test with All Target Models
Skills affect models differently. Test with Haiku, Sonnet, and Opus. What works for Opus may need more detail for Haiku.

## Skill Creation Process

### Step 1: Determine Platform and Gather Requirements

First, ask which platform(s) the user is targeting:
- **Claude Code only**: Filesystem-based, can use allowed-tools
- **claude.ai only**: ZIP upload, no allowed-tools
- **Both**: Maximum compatibility, skip Claude Code-only features

Then gather requirements:
1. **Platform**: Claude Code, claude.ai, or both?
2. **Purpose**: What specific task should this Skill solve?
3. **Name**: What should it be called? (lowercase-with-hyphens, max 64 chars, use gerund form like "processing-pdfs")
4. **Description**: When should Claude use it? (max 1024 chars, be specific, include triggers)
5. **Scope**: What inputs/outputs are expected?
6. **Tool restrictions** (Claude Code only): Should it limit which tools Claude can use? (allowed-tools field)
7. **Storage location** (Claude Code only): Personal (~/.claude/skills/), Project (.claude/skills/), or Plugin?
8. **Resources**: Will it need reference files, scripts, or external data?
9. **Dependencies**: Does it require specific packages?

### Step 2: Create Directory Structure

**For Claude Code:**

Personal Skills:
```bash
mkdir -p ~/.claude/skills/skill-name
```

Project Skills:
```bash
mkdir -p .claude/skills/skill-name
```

**For claude.ai:**

Create a local directory (will be ZIPped later):
```bash
mkdir -p skill-name
```

**Directory contents (both platforms):**
```
skill-name/
├── SKILL.md           # Required: Main Skill file
├── reference.md       # Optional: Supplemental information
├── examples.md        # Optional: Extended examples
├── templates/         # Optional: Template files
│   └── template.txt
└── scripts/          # Optional: Executable code
    ├── helper.py
    └── validate.py
```

### Step 3: Write the SKILL.md File
The SKILL.md file must include:

#### Required YAML Frontmatter

**For both platforms:**
```yaml
---
name: skill-name
description: What the Skill does and when to use it. Include specific triggers and contexts. Use third person. Max 1024 characters.
metadata:
  version: 1.0.0
  dependencies: package>=version, another-package>=version
---
```

**For Claude Code only (add this field if needed):**
```yaml
allowed-tools: Read, Grep, Glob  # Restrict which tools Claude can use
```

**Platform Compatibility Notes:**

claude.ai has strict frontmatter validation and only accepts these top-level keys: `name`, `description`, `license`, `allowed-tools`, `metadata`. This is why `version` and `dependencies` must be nested under the `metadata` field.

Claude Code is more permissive and will accept the `metadata` field without issues. While Claude Code's documentation shows `version` as a top-level field, using the `metadata` structure ensures your Skill works on both platforms.

**Best Practice for Dual-Platform Support:**
1. Use the `metadata` field format shown above for maximum compatibility
2. Include version information in the markdown body as well (see the Version section)
3. This provides redundancy - version info appears in both frontmatter and documentation
4. Omit the `allowed-tools` field if targeting both platforms (Claude Code only)

**Name requirements (both platforms):**
- Lowercase letters, numbers, and hyphens only
- Max 64 characters
- Use gerund form: "processing-pdfs", "analyzing-data"
- Cannot contain "anthropic" or "claude"

**Description requirements (both platforms):**
- Max 1024 characters
- Third person: "Processes files..." not "I can help..."
- Include what it does AND when to use it
- Mention specific triggers/keywords

**Dependencies handling:**
- **Claude Code**: Auto-installs packages (or asks for permission)
- **claude.ai**: Can install from PyPI/npm when needed
- **Anthropic API**: No network access, pre-installed only
- List packages: `python>=3.8, pandas>=1.5.0, requests>=2.28.0`

**Tool restrictions (allowed-tools) - Claude Code ONLY:**
- Optional field to limit which tools Claude can use when Skill is active
- **Not supported on claude.ai**
- Useful for read-only Skills or security-sensitive workflows
- When specified, Claude can only use listed tools without asking permission
- Example tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch
- Example: `allowed-tools: Read, Grep, Glob` for read-only Skill

#### Markdown Body Structure
```markdown
# Skill Name

## Overview
Brief explanation of what the Skill does and its purpose.

## When to Use This Skill
- Specific scenario 1
- Specific scenario 2
- Specific scenario 3

## Instructions
Clear, step-by-step instructions for Claude to follow.

## Examples
Include example inputs and expected outputs.

## Resources
Reference any additional files in the Skill directory.
```

### Step 4: Add Resources (Optional)
If the Skill requires additional information:
- Create `REFERENCE.md` for supplemental content
- Add example files to `resources/examples/`
- Include templates in `resources/templates/`
- Store data files, logos, or other assets as needed

### Step 5: Add Scripts (Optional)
For advanced Skills that need executable code:
- Add Python scripts (`.py`) for data processing, analysis, or automation
- Add JavaScript scripts (`.js`) for web-related tasks
- Document all required dependencies in the frontmatter
- Include usage examples in the Skill.md file

**Supported languages:**
- Python (with pandas, numpy, matplotlib, etc.)
- JavaScript/Node.js (with standard npm packages)

**Note:** Claude and Claude Code can install packages from standard repositories when loading Skills.

### Step 6: Package and Share the Skill

#### For claude.ai (ZIP Upload)

**Create ZIP file:**
```bash
# From parent directory
zip -r skill-name.zip skill-name/

# Verify structure
unzip -l skill-name.zip
```

**Expected structure:**
```
skill-name.zip
  └── skill-name/
      ├── SKILL.md
      ├── reference.md
      └── scripts/
```

**Share with users:**
1. Users navigate to Settings > Capabilities
2. Upload the ZIP file
3. Enable the Skill
4. Start using it

**Team distribution:**
- Share ZIP file via email, file sharing, or git repository
- Users manually upload to their claude.ai account

#### For Claude Code

**Recommended: Share via Plugin**
Best for team distribution:
1. Create a plugin with Skills in the `skills/` directory
2. Publish to a marketplace
3. Team members install the plugin
4. Skills automatically available

**Alternative: Share via Git (Project Skills)**
For project-specific Skills:
1. Place Skill in `.claude/skills/skill-name/`
2. Commit to git: `git add .claude/skills/ && git commit -m "Add skill"`
3. Team members get Skills automatically: `git pull`

**Personal Skills:**
- Stay local: `~/.claude/skills/`
- Not shared automatically
- Use for individual workflows

#### For Both Platforms

If targeting both, provide:
1. ZIP file for claude.ai users
2. Plugin or git instructions for Claude Code users
3. Omit Claude Code-only features (like `allowed-tools`)

### Step 7: Test the Skill

#### Testing on Both Platforms

**Test with matching requests:**
Skills are autonomously invoked—Claude decides when to use them based on the description.

Ask questions that match your description:
```
# If description mentions "PDF files"
"Can you help me extract text from this PDF?"

# Claude automatically uses your Skill if it matches
```

**Verify Skill is loaded:**
Ask Claude: `"What Skills are available?"`

#### Platform-Specific Testing

**For claude.ai:**
1. **Upload Skill**: Settings > Capabilities > Upload ZIP
2. **Enable Skill**: Toggle it on in Capabilities
3. **Test invocation**: Ask relevant questions
4. **Review thinking**: Check if Skill was considered and why/why not
5. **Iterate description**: Update if Skill not triggering correctly

**For Claude Code:**
1. **Verify file location**:
   ```bash
   ls ~/.claude/skills/skill-name/SKILL.md  # Personal
   ls .claude/skills/skill-name/SKILL.md   # Project
   ```
2. **Restart Claude Code**: Required for changes to take effect
3. **Test invocation**: Ask relevant questions
4. **Debug if needed**: Run `claude --debug` to see loading errors
5. **Check YAML syntax**: Validate frontmatter format

**Common Debugging Steps:**
1. **Check description specificity**: Too vague? Add specific triggers
2. **Verify YAML syntax**: Must start/end with `---`, no tabs
3. **Test with exact keywords**: Use terms from your description
4. **Review Skill name**: Must be lowercase-with-hyphens
5. **Check dependencies**: Listed correctly in frontmatter?

## Best Practices

For comprehensive details, see [REFERENCE.md](REFERENCE.md).

### Naming Conventions
Use consistent patterns:
- **Gerund form** (recommended): "processing-pdfs", "analyzing-data"
- Must be lowercase-with-hyphens
- Max 64 characters
- No "anthropic" or "claude"

### Description Effectiveness
- **Always third person**: "Processes files..." not "I help..."
- **Be specific**: Include both what it does AND when to use it
- **Add triggers**: Mention keywords that should activate it
- **Example**: "Extracts text from PDF files using pdfplumber. Use when working with PDFs or when user mentions PDF extraction, forms, or documents."

### Progressive Disclosure
Claude loads information in stages:
1. **Metadata** (always loaded): name, description
2. **Skill.md body** (when Skill used): core instructions
3. **REFERENCE.md** (on-demand): detailed specs, edge cases
4. **Other files** (as needed): templates, data, scripts

Keep Skill.md under 500 lines. Move details to separate files.

### Workflow Patterns
For multi-step tasks, provide checklists:

```markdown
## Task workflow

Copy this checklist:
```
Progress:
- [ ] Step 1: Analyze input
- [ ] Step 2: Process data
- [ ] Step 3: Validate output
- [ ] Step 4: Generate report
```

**Step 1: Analyze input**
[Detailed instructions...]
```

### Feedback Loops
Add validation cycles for quality:

```markdown
1. Make changes
2. Run validation: `python validate.py`
3. If validation fails:
   - Review errors
   - Fix issues
   - Run validation again
4. Only proceed when validation passes
```

### Common Patterns

**Template pattern** - Provide output format:
```markdown
ALWAYS use this exact structure:
[template here]
```

**Examples pattern** - Show input/output pairs:
```markdown
Example 1:
Input: [specific input]
Output: [expected output]
```

**Conditional workflow** - Guide decisions:
```markdown
1. Determine type:
   **Creating new?** → Follow creation workflow
   **Editing existing?** → Follow editing workflow
```

### Avoid Anti-Patterns
- ❌ Windows paths (`\`): Use forward slashes (`/`) always
- ❌ Too many options: Provide default with escape hatch
- ❌ Vague terms: Be specific and concrete
- ❌ Time-sensitive info: Use "old patterns" section instead
- ❌ Inconsistent terminology: Pick one term and stick to it
- ❌ Deeply nested references: Keep references one level deep from Skill.md

## Example Skill Patterns

### Simple Skill (commit message helper)
```yaml
---
name: generating-commit-messages
description: Generates clear commit messages from git diffs. Use when writing commit messages or reviewing staged changes.
---

# Generating Commit Messages

## Instructions
1. Run `git diff --staged` to see changes
2. Suggest a commit message with:
   - Summary under 50 characters
   - Detailed description
   - Affected components
```

### Read-Only Skill (code reviewer)
```yaml
---
name: code-reviewer
description: Review code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
allowed-tools: Read, Grep, Glob  # Restrict to read-only operations
---

# Code Reviewer

## Instructions
1. Read target files using Read tool
2. Search for patterns using Grep
3. Find related files using Glob
4. Provide detailed feedback on code quality
```

### Multi-File Skill (PDF processing)
```
pdf-processing/
├── SKILL.md
├── forms.md          # Form-filling guide (loaded on-demand)
├── reference.md      # API reference (loaded as needed)
└── scripts/
    ├── fill_form.py
    └── validate.py
```

```yaml
---
name: pdf-processing
description: Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction.
metadata:
  dependencies: pypdf>=3.0.0, pdfplumber>=0.9.0
---

# PDF Processing

## Quick start
For form filling, see [forms.md](forms.md).
For API reference, see [reference.md](reference.md).
```

## Security Considerations
When adding scripts to Skills:
- ⚠️ **Never hardcode sensitive information** (API keys, passwords)
- Use appropriate MCP connections for external service access
- Validate inputs in scripts
- Follow principle of least privilege
- Document security requirements
- Use **allowed-tools** to restrict capabilities when appropriate

## Templates

### Basic Skill Template
See `templates/basic-skill-template.md` for a minimal Skill structure suitable for simple instruction-based Skills.

### Advanced Skill Template
See `templates/advanced-skill-template.md` for a complete Skill structure with resources and scripts.

## Example Skills
For reference implementations, see:
- GitHub repository: https://github.com/anthropics/skills
- Claude Docs: Skill authoring best practices

## Troubleshooting

### Claude isn't invoking the Skill
- Check the description is specific and clear
- Verify the Skill is enabled in Settings
- Review Claude's thinking to see why it wasn't selected
- Make the description more specific about triggering scenarios

### Skill loads but doesn't work as expected
- Review instructions for clarity
- Add more examples
- Check that referenced files exist
- Verify script dependencies are correctly specified

### Scripts aren't running
- Confirm dependencies are listed in frontmatter
- Check script syntax and permissions
- Verify file paths are correct
- Test scripts independently first

## Output Format
When creating a Skill, provide:
1. The complete directory structure
2. Full Skill.md file with frontmatter
3. Any template or resource files
4. Instructions for testing
5. Suggested prompts to trigger the Skill
