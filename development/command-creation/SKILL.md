---
name: command-creation
description: >
  Use this skill when creating or refining custom Claude Code slash commands. Slash commands are
  user-invoked reusable prompts that can accept arguments, reference files, and execute bash operations.
  Helps design command syntax, argument handling, file references, bash execution, and frontmatter
  configuration. Automatically invoked when user requests "create a command", "make a slash command",
  "add a /command", or mentions custom command development.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(ls:*), Bash(tree:*)
---

# Command Creation Skill

This skill helps create production-ready custom slash commands following Anthropic's official specifications.

## What is a Slash Command?

A **slash command** is a user-invoked reusable prompt stored as a Markdown file. Unlike skills (model-invoked) or agents (complex AI assistants), slash commands are:

- **User-triggered**: Explicitly invoked with `/command-name`
- **Template-based**: Expand to prompts with placeholders
- **Lightweight**: Simple Markdown files with optional frontmatter
- **Quick access**: Fast way to reuse common instructions

## Commands vs Skills vs Agents

| Feature | Command | Skill | Agent |
|---------|---------|-------|-------|
| **Invocation** | User (`/name`) | Model (automatic) | User or Task tool |
| **Complexity** | Simple prompt template | Capability with logic | Full AI assistant |
| **Arguments** | Yes ($1, $2, $ARGUMENTS) | N/A | N/A |
| **File access** | Yes (@file) | Via tools | Via tools |
| **Bash exec** | Yes (!command) | Via tools | Via tools |
| **Use case** | Quick prompts, workflows | Autonomous features | Domain expertise |

**When to use Commands**: Reusable prompts, quick text expansion, parametrized instructions, file processing workflows

## Command Structure

### Basic Command (Prompt only)

```markdown
Please review this code for security vulnerabilities and provide
specific recommendations for improvement.
```

File: `.claude/commands/security-review.md`
Usage: `/security-review`

### Command with Frontmatter

```markdown
---
description: Review code for security vulnerabilities with OWASP focus
argument-hint: [file-path] [--strict]
allowed-tools: Read, Grep, Glob
model: opus
disable-model-invocation: false
---

Please perform a comprehensive security audit of the codebase, focusing on:
- OWASP Top 10 vulnerabilities
- Authentication and authorization issues
- Input validation and sanitization
- Secrets exposure
```

## Frontmatter Fields

All frontmatter fields are **optional**.

### description
Brief explanation shown in `/help` and for SlashCommand tool.

```yaml
description: Generate comprehensive API documentation from OpenAPI spec
```

**Best practices**:
- 1 sentence, concise
- Describe what it does, not how
- Include key features

### argument-hint
Expected arguments for autocomplete and help.

```yaml
argument-hint: <endpoint-url> [--format json|yaml]
argument-hint: [file-pattern]
argument-hint: <branch-name>
```

**Syntax conventions**:
- `<required>` - Required argument
- `[optional]` - Optional argument
- `|` - Choice between options

### allowed-tools
Restrict which tools the command can use.

```yaml
allowed-tools: Read, Write, Grep, Glob
allowed-tools: Bash(git:*), Bash(npm:*)
allowed-tools: Read, WebFetch
```

**Why restrict**:
- Security: Prevent dangerous operations
- Focus: Command only needs specific tools
- Safety: Avoid accidental file modifications

### model
Override the model for this command.

```yaml
model: opus      # Complex reasoning
model: sonnet    # Balanced (default)
model: haiku     # Fast, simple tasks
```

### disable-model-invocation
Prevent SlashCommand tool from invoking this command.

```yaml
disable-model-invocation: true   # Only user can invoke
disable-model-invocation: false  # Claude can invoke (default)
```

**Use cases**:
- Private commands for personal use only
- Commands with dangerous operations
- Commands requiring user confirmation

## Argument Handling

### $ARGUMENTS
Captures all passed arguments as a single value.

```markdown
Please analyze the following: $ARGUMENTS
```

Usage:
```
/analyze-text This is some text to analyze
```

Expands to:
```
Please analyze the following: This is some text to analyze
```

### $1, $2, $3, ... (Positional Arguments)
Access individual arguments by position.

```markdown
Compare $1 with $2 and explain the differences in $3 format.
```

Usage:
```
/compare file1.py file2.py detailed
```

Expands to:
```
Compare file1.py with file2.py and explain the differences in detailed format.
```

### Default Values
Provide defaults for missing arguments.

```markdown
Run tests in ${1:-development} environment with ${2:-verbose} output.
```

Usage:
```
/run-tests
```

Expands to:
```
Run tests in development environment with verbose output.
```

Usage with arguments:
```
/run-tests production quiet
```

Expands to:
```
Run tests in production environment with quiet output.
```

### Combining Arguments

```markdown
---
argument-hint: <action> <target> [options]
---

Execute $1 on $2 with options: $3
Fallback environment: ${3:-default}
All arguments: $ARGUMENTS
```

## File References

### @file Syntax
Include file contents in the prompt.

```markdown
Please review this code:

@src/api/users.py

Focus on error handling and security.
```

When invoked, Claude reads `src/api/users.py` and includes its contents.

### Multiple Files

```markdown
Compare these two implementations:

**Old version:**
@src/legacy/auth.py

**New version:**
@src/current/auth.py

Highlight improvements and potential issues.
```

### File Arguments

```markdown
Review the file: @$1

And compare with: @$2
```

Usage:
```
/compare-files old-code.py new-code.py
```

### File Patterns (with Glob)

```markdown
Analyze all TypeScript files in the components directory.

Use the Glob tool to find files matching: src/components/**/*.tsx
```

## Bash Execution

### ! Prefix for Bash Commands
Execute bash commands and include output.

```markdown
---
allowed-tools: Bash(git:*), Bash(npm:*)
---

Check the current git status:

!git status

And list recent commits:

!git log --oneline -5
```

**Security requirement**: Must declare allowed bash commands in frontmatter.

```yaml
allowed-tools: Bash(git:*), Bash(npm:*), Bash(docker:*)
```

### Bash with Arguments

```markdown
---
allowed-tools: Bash(git:*)
---

Show git log for branch: $1

!git log origin/$1..HEAD --oneline
```

Usage:
```
/branch-diff main
```

### Command Chaining

```markdown
---
allowed-tools: Bash(npm:*), Bash(git:*)
---

Run the following commands:

!npm run test
!npm run build
!git status
```

## Extended Thinking

Commands can trigger extended thinking by including extended thinking keywords.

```markdown
---
description: Analyze architectural implications of a design decision
---

Please analyze this architectural decision with extended thinking:

$ARGUMENTS

Consider:
- Long-term implications
- Alternative approaches
- Trade-offs and risks
```

Presence of "extended thinking" in the command triggers extended thinking mode.

## File Organization

### Project Commands (Shared with Team)

```
.claude/commands/
├── development/
│   ├── start-dev.md
│   ├── run-tests.md
│   └── build-prod.md
├── git/
│   ├── sync-main.md
│   └── cleanup-branches.md
└── review.md
```

Appears as:
- `/start-dev` (project:development)
- `/run-tests` (project:development)
- `/sync-main` (project:git)
- `/review` (project)

### Personal Commands (Cross-Project)

```
~/.claude/commands/
├── personal/
│   ├── daily-standup.md
│   └── task-summary.md
└── notes.md
```

Appears as:
- `/daily-standup` (user:personal)
- `/task-summary` (user:personal)
- `/notes` (user)

### Namespacing
Subdirectories organize commands but don't affect command names.

```
.claude/commands/api/create-endpoint.md
```

Command: `/create-endpoint` (not `/api/create-endpoint`)
Shown as: `/create-endpoint` (project:api)

**Conflict resolution**: Project-level commands take precedence over user-level when names match.

## Command Patterns

### Code Review Command

```markdown
---
description: Comprehensive code review focusing on quality and maintainability
argument-hint: [file-pattern]
allowed-tools: Read, Grep, Glob
model: opus
---

Perform a detailed code review covering:

1. **Code Quality**
   - Readability and clarity
   - Naming conventions
   - Code organization

2. **Best Practices**
   - Design patterns
   - Error handling
   - Performance considerations

3. **Security**
   - Input validation
   - Authentication/authorization
   - Data protection

$ARGUMENTS

Provide specific, actionable feedback with code examples.
```

### Git Workflow Command

```markdown
---
description: Complete feature branch workflow from creation to PR
argument-hint: <feature-name>
allowed-tools: Bash(git:*)
---

Execute feature branch workflow for: $1

!git checkout -b feature/$1
!git push -u origin feature/$1

Branch created: feature/$1

Next steps:
1. Make your changes
2. Commit with: /commit-feature $1
3. Create PR with: /create-pr $1
```

### Test Runner Command

```markdown
---
description: Run tests with coverage and generate report
allowed-tools: Bash(npm:*), Bash(pytest:*), Write
---

Running test suite with coverage...

!npm run test:coverage

Generate summary report:
- Test results
- Coverage percentage
- Failed tests details
- Recommendations for improving coverage
```

### Documentation Generator Command

```markdown
---
description: Generate API documentation from code
argument-hint: <directory-path>
allowed-tools: Read, Grep, Glob, Write
model: opus
---

Generate comprehensive API documentation for code in: $1

1. Scan for all public APIs, functions, and classes
2. Extract docstrings and type hints
3. Identify request/response formats
4. Document error cases
5. Generate examples

Output format: Markdown with clear hierarchy
```

### File Comparison Command

```markdown
---
description: Compare two files and highlight differences
argument-hint: <file1> <file2>
allowed-tools: Read
---

Compare these files and explain key differences:

**File 1: $1**
@$1

**File 2: $2**
@$2

Analysis:
1. Structural differences
2. Logic changes
3. Potential issues
4. Recommendations
```

### Environment Setup Command

```markdown
---
description: Set up development environment for this project
allowed-tools: Bash(npm:*), Bash(pip:*), Bash(cp:*), Read, Write
---

Setting up development environment...

!npm install

Copy environment template:
!cp .env.example .env

Please configure the following in .env:
- Database credentials
- API keys
- Service URLs

Verify setup:
!npm run verify-setup
```

## Advanced Features

### Conditional Logic in Prompts

```markdown
---
argument-hint: <command> [--verbose]
---

Execute $1

${2:+Include detailed logging and timing information}
${2:-Use standard output}
```

### Multi-Step Workflows

```markdown
---
description: Complete deployment workflow
argument-hint: <environment>
allowed-tools: Bash(npm:*), Bash(git:*), Bash(ssh:*)
---

Deploying to: $1

Step 1: Run tests
!npm run test

Step 2: Build application
!npm run build

Step 3: Push to repository
!git push origin main

Step 4: Deploy to $1
!ssh deploy@$1-server "cd /app && git pull && pm2 restart app"

Deployment complete! Verify at: https://$1.example.com
```

### Template Expansion

```markdown
---
description: Create new React component
argument-hint: <ComponentName>
allowed-tools: Write
---

Create a new React component: $1

\`\`\`tsx
// src/components/$1.tsx
import React from 'react';

interface ${1}Props {
  // Define props
}

export const $1: React.FC<${1}Props> = (props) => {
  return (
    <div>
      {/* Component content */}
    </div>
  );
};
\`\`\`

\`\`\`tsx
// src/components/$1.test.tsx
import { render } from '@testing-library/react';
import { $1 } from './$1';

describe('$1', () => {
  it('renders correctly', () => {
    const { container } = render(<$1 />);
    expect(container).toBeInTheDocument();
  });
});
\`\`\`
```

## Testing Your Command

1. **Create command file**:
   ```bash
   echo "Review this code: @\$1" > .claude/commands/quick-review.md
   ```

2. **Test basic invocation**:
   ```
   /quick-review src/app.py
   ```

3. **Test with multiple arguments**:
   ```
   /compare file1.py file2.py
   ```

4. **Test bash execution**:
   ```
   /git-status
   ```

5. **Verify frontmatter**:
   ```
   /help
   ```
   Confirm description appears correctly.

## Common Mistakes to Avoid

❌ **Undefined arguments**
```markdown
Review $1 and $2
```
Usage: `/review file.py` (only one argument)
Result: `$2` remains as literal text

✅ **Default values**
```markdown
Review $1 ${2:+and compare with $2}
```

❌ **Bash without tool permission**
```markdown
!git status
```
Missing: `allowed-tools: Bash(git:*)`

✅ **Proper permissions**
```markdown
---
allowed-tools: Bash(git:*)
---

!git status
```

❌ **Complex logic in commands**
```markdown
If $1 is production, then deploy carefully, otherwise...
```
Commands should be simple templates

✅ **Use agents for complex logic**
```markdown
Use the deployment-agent to deploy to $1 environment
```

❌ **Missing argument hints**
```markdown
---
description: Deploy application
---

Deploy to $1 with $2 configuration
```

✅ **Clear argument hints**
```markdown
---
description: Deploy application
argument-hint: <environment> <config-file>
---

Deploy to $1 with $2 configuration
```

## Command vs Skill vs Agent Decision

| Need | Use |
|------|-----|
| Quick text expansion | **Command** |
| Reusable prompt with args | **Command** |
| File reference workflow | **Command** |
| Bash execution workflow | **Command** |
| Autonomous capability | **Skill** |
| Complex domain expertise | **Agent** |

## Resources

Reference the examples directory for:
- Complete command definitions across different use cases
- Argument handling patterns
- Bash execution examples
- Multi-file workflow commands

---

**Next Steps**: After creating a command, test with various argument combinations, verify bash execution works as expected, and document usage in project README or command help text.
