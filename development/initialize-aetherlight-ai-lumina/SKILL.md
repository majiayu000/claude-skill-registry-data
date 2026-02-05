---
name: initialize
description: Initialize ÆtherLight in a new repository. Sets up folder structure, Git workflow, configuration files, and development standards.
---

# Initialize ÆtherLight Skill

## What This Skill Does

Sets up ÆtherLight in a new repository:
- Creates standardized folder structure
- Configures Git workflow and branches
- Sets up configuration files
- Establishes development patterns
- Integrates with VS Code/Cursor

## When Claude Should Use This

Use this skill when the user:
- Says "set up ÆtherLight" or "initialize the project"
- Starts a new repository
- Wants to add ÆtherLight to existing project
- Mentions project setup or initialization
- References Issue #6 (initialization process)

## Initialization Process

### 1. Assess Current State
```bash
# Check if repo exists
git status 2>/dev/null || git init

# Check for existing structure
ls -la

# Check for existing CLAUDE.md or cursor files
if [ -f "CLAUDE.md" ]; then
  echo "⚠️ Existing CLAUDE.md found - will enhance, not replace"
  cp CLAUDE.md CLAUDE.md.backup.$(date +%Y%m%d_%H%M%S)
fi

if [ -f ".claude/CLAUDE.md" ]; then
  echo "⚠️ Existing .claude/CLAUDE.md found - will merge"
  cp .claude/CLAUDE.md .claude/CLAUDE.md.backup.$(date +%Y%m%d_%H%M%S)
fi

# Comprehensive project analysis
echo "🔍 Analyzing project type..."

# Framework detection
[ -f "package.json" ] && {
  echo "Node.js project detected"
  grep -q '"react"' package.json && echo "  → React framework"
  grep -q '"vue"' package.json && echo "  → Vue framework"
  grep -q '"@angular/core"' package.json && echo "  → Angular framework"
  grep -q '"express"' package.json && echo "  → Express backend"
  grep -q '"next"' package.json && echo "  → Next.js framework"
}

[ -f "Cargo.toml" ] && echo "Rust project detected"
[ -f "requirements.txt" ] || [ -f "pyproject.toml" ] && echo "Python project detected"
[ -f "go.mod" ] && echo "Go project detected"
[ -f "pom.xml" ] && echo "Java/Maven project detected"
[ -f "build.gradle" ] && echo "Java/Gradle project detected"

# Build system detection
[ -f "Makefile" ] && echo "Make build system detected"
[ -f "webpack.config.js" ] && echo "Webpack bundler detected"
[ -f "vite.config.js" ] && echo "Vite bundler detected"
[ -f "rollup.config.js" ] && echo "Rollup bundler detected"
```

### 2. Create ÆtherLight Structure
```bash
# Core directories
mkdir -p .claude/skills
mkdir -p .claude/commands
mkdir -p .aetherlight/patterns
mkdir -p sprints
mkdir -p docs/patterns
mkdir -p docs/architecture
mkdir -p analysis
mkdir -p tasks

# Development directories (based on project type)
mkdir -p src
mkdir -p tests
mkdir -p scripts

# Initialize pattern library
echo "Creating pattern library templates..."
mkdir -p .aetherlight/patterns/auth
mkdir -p .aetherlight/patterns/database
mkdir -p .aetherlight/patterns/api
mkdir -p .aetherlight/patterns/ui
```

### 3. Initialize Configuration Files

#### Handling Existing CLAUDE.md
```bash
# Function to merge or create CLAUDE.md
create_or_enhance_claude_md() {
  if [ -f "CLAUDE.md" ] || [ -f ".claude/CLAUDE.md" ]; then
    echo "📝 Enhancing existing CLAUDE.md with ÆtherLight integration..."

    # Extract existing content sections
    existing_content=$(cat CLAUDE.md 2>/dev/null || cat .claude/CLAUDE.md 2>/dev/null)

    # Create enhanced version preserving user content
    cat > .claude/CLAUDE.md.enhanced << 'EOF'
# Project Instructions for Claude - ÆtherLight Enhanced

## ÆtherLight Integration
- Voice commands available via backtick (`)
- Sprint management in `/sprints/` directory
- Pattern library in `.aetherlight/patterns/`
- Code analysis via `/code-analyze` command
- Automated workflows via skills

## Original Project Instructions
[EXISTING_CONTENT]

## ÆtherLight Development Standards

### Git Workflow (Enforced)
1. All work in feature branches
2. PRs required for master
3. Semantic commit messages
4. Code review before merge
5. Protected code policy applies after release

### Available Commands
- `/initialize` - Set up project structure
- `/sprint-plan` - Create sprint with branches
- `/code-analyze` - Analyze codebase
- `/publish` - Automated release

### Code Protection Rules
- Released code is PROTECTED
- Refactor-only modifications allowed
- New features as extensions only
EOF

    # Replace placeholder with existing content
    sed -i "s|\[EXISTING_CONTENT\]|$existing_content|" .claude/CLAUDE.md.enhanced

    # Move enhanced version into place
    mv .claude/CLAUDE.md.enhanced .claude/CLAUDE.md
  else
    echo "📝 Creating new CLAUDE.md with ÆtherLight standards..."
    create_new_claude_md
  fi
}

# Function for new CLAUDE.md
create_new_claude_md() {
  cat > .claude/CLAUDE.md << 'EOF'
# Project Instructions for Claude

## Project Overview
[Project description - filled from user input]

## ÆtherLight Features
- Voice-to-code transcription (backtick key)
- Sprint management with Git workflow
- Pattern matching to prevent hallucinations
- Automated code analysis
- Enforced development standards

## Development Standards

### Git Workflow
1. All work in feature branches
2. PRs required for master
3. Semantic commit messages
4. Code review before merge

### Code Standards
- TypeScript/JavaScript: ESLint + Prettier
- Tests required for new features
- Documentation for public APIs
- No console.log in production

## Available Commands
- `/initialize` - Set up project
- `/sprint-plan` - Plan and create sprint
- `/code-analyze` - Analyze codebase
- `/publish` - Release new version

## Project-Specific Rules
[Customized based on user requirements]
EOF
}
```

#### `.claude/settings.json`
```json
{
  "version": "1.0.0",
  "workflow": {
    "requirePR": true,
    "protectedBranch": "master",
    "requireReview": true,
    "semanticCommits": true
  },
  "analysis": {
    "schedule": "weekly",
    "autoFix": false,
    "blockOnCritical": true
  },
  "sprint": {
    "duration": "2 weeks",
    "ceremonies": ["planning", "standup", "review", "retro"]
  }
}
```

#### `.claude/settings.local.json`
```json
{
  "permissions": {
    "allowFileCreation": true,
    "allowFileModification": true,
    "allowGitOperations": true,
    "allowTerminalCommands": true
  },
  "features": {
    "voiceIntegration": true,
    "sprintManagement": true,
    "codeAnalysis": true,
    "patternLibrary": true
  }
}
```

#### `.aetherlight/config.json`
```json
{
  "project_initialized": true,
  "initialization_date": "[TIMESTAMP]",
  "ai_assistant_integration": {
    "claude_md": true,
    "commands": true,
    "skills": true,
    "patterns": true
  },
  "project_metadata": {
    "type": "[DETECTED_TYPE]",
    "frameworks": "[DETECTED_FRAMEWORKS]",
    "language": "[PRIMARY_LANGUAGE]"
  }
}
```

#### Command Files

Create `.claude/commands/sprint-status.md`:
```markdown
---
name: sprint-status
description: Display current sprint progress and task status
---

# Sprint Status Command

Show the current sprint's tasks and their completion status.

## Usage
Read the latest sprint file from `sprints/` directory and display:
- Sprint name and duration
- Task list with status indicators
- Completion percentage
- Blocked tasks
- Next actions

## Implementation
1. Find the most recent SPRINT_*.toml file
2. Parse the TOML structure
3. Display tasks grouped by phase
4. Show progress bars for each phase
5. Highlight blocked or at-risk items
```

Create `.claude/commands/update-task.md`:
```markdown
---
name: update-task
description: Update task status in the current sprint
---

# Update Task Command

Modify a task's status in the active sprint TOML file.

## Usage
`/update-task [task-id] [status]`

Status options:
- pending
- in_progress
- completed
- blocked

## Implementation
1. Read current sprint TOML
2. Find task by ID
3. Update status field
4. Write back to TOML
5. Commit change with semantic message
```

Create `.claude/commands/view-patterns.md`:
```markdown
---
name: view-patterns
description: Browse and search the pattern library
---

# View Patterns Command

Browse available code patterns and templates.

## Usage
`/view-patterns [category]`

Categories:
- auth (authentication patterns)
- database (data access patterns)
- api (API endpoint patterns)
- ui (UI component patterns)

## Implementation
1. List patterns in `.aetherlight/patterns/`
2. Show pattern description and usage
3. Provide copy-paste ready code
4. Include best practices notes
```

### 4. Set Up Git Workflow

#### Initialize Branches
```bash
# Ensure on master
git checkout -b master 2>/dev/null || git checkout master

# Create development branches
git checkout -b develop
git push -u origin develop

# Create initial feature branch
git checkout -b feature/initial-setup
```

#### Configure Git Hooks
Create `.githooks/pre-commit`:
```bash
#!/bin/bash
# Run tests before commit
npm test || exit 1

# Run linter
npm run lint || exit 1

# Check for sensitive data
grep -r "password\|secret\|api_key" --exclude-dir=.git . && {
  echo "Potential secrets found!"
  exit 1
}
```

### 5. Initialize Pattern Library

Create pattern templates in `.aetherlight/patterns/`:

#### Authentication Pattern
`.aetherlight/patterns/auth/jwt-auth.md`:
```markdown
---
name: JWT Authentication
category: auth
tags: [jwt, authentication, security]
---

# JWT Authentication Pattern

## When to Use
- Stateless authentication
- API authentication
- Multi-service architectures

## Implementation
\`\`\`typescript
// Token generation
function generateToken(user: User): string {
  return jwt.sign(
    { id: user.id, email: user.email },
    process.env.JWT_SECRET,
    { expiresIn: '24h' }
  );
}

// Token verification middleware
function verifyToken(req, res, next) {
  const token = req.headers['authorization']?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'No token provided' });

  jwt.verify(token, process.env.JWT_SECRET, (err, decoded) => {
    if (err) return res.status(403).json({ error: 'Invalid token' });
    req.user = decoded;
    next();
  });
}
\`\`\`

## Best Practices
- Store secrets in environment variables
- Use refresh tokens for long sessions
- Implement token rotation
- Add rate limiting
```

#### Database Pattern
`.aetherlight/patterns/database/repository.md`:
```markdown
---
name: Repository Pattern
category: database
tags: [repository, data-access, clean-architecture]
---

# Repository Pattern

## When to Use
- Abstracting data access logic
- Testing with mock data
- Switching between databases

## Implementation
\`\`\`typescript
interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  create(data: CreateUserDto): Promise<User>;
  update(id: string, data: UpdateUserDto): Promise<User>;
  delete(id: string): Promise<void>;
}

class UserRepository implements IUserRepository {
  async findById(id: string): Promise<User | null> {
    return await db.user.findUnique({ where: { id } });
  }

  async create(data: CreateUserDto): Promise<User> {
    return await db.user.create({ data });
  }
  // ... other methods
}
\`\`\`

## Best Practices
- Keep repositories focused on single entities
- Use DTOs for data transfer
- Implement proper error handling
- Add transaction support
```

#### API Pattern
`.aetherlight/patterns/api/rest-controller.md`:
```markdown
---
name: RESTful Controller
category: api
tags: [rest, api, controller]
---

# RESTful Controller Pattern

## When to Use
- Building REST APIs
- CRUD operations
- Resource-based endpoints

## Implementation
\`\`\`typescript
class UserController {
  constructor(private userService: UserService) {}

  async getAll(req: Request, res: Response) {
    try {
      const users = await this.userService.findAll();
      return res.json(users);
    } catch (error) {
      return res.status(500).json({ error: error.message });
    }
  }

  async getOne(req: Request, res: Response) {
    try {
      const user = await this.userService.findById(req.params.id);
      if (!user) return res.status(404).json({ error: 'User not found' });
      return res.json(user);
    } catch (error) {
      return res.status(500).json({ error: error.message });
    }
  }

  // POST, PUT, DELETE methods...
}
\`\`\`

## Best Practices
- Use proper HTTP status codes
- Implement pagination for lists
- Add request validation
- Include error details in development only
```

### 6. Create Initial Sprint

Generate `sprints/SPRINT_INITIAL.toml`:
```toml
[sprint]
name = "Initial Setup Sprint"
type = "setup"
goals = [
  "Repository structure",
  "Development environment",
  "CI/CD pipeline",
  "Documentation"
]

[[phases]]
id = 1
name = "Foundation"
tasks = [
  "Create folder structure",
  "Set up Git workflow",
  "Configure linting",
  "Write README"
]

[[phases]]
id = 2
name = "Integration"
tasks = [
  "VS Code configuration",
  "Install ÆtherLight extension",
  "Configure voice commands",
  "Test workflow"
]
```

### 6. VS Code/Cursor Integration

#### `.vscode/settings.json`
```json
{
  "aetherlight.enabled": true,
  "aetherlight.features": {
    "voice": true,
    "sprint": true,
    "codeAnalysis": true,
    "autoUpdate": true
  },
  "editor.formatOnSave": true,
  "files.exclude": {
    "**/.git": true,
    "**/node_modules": true,
    "**/dist": true
  }
}
```

#### `.vscode/extensions.json`
```json
{
  "recommendations": [
    "aetherlight.aetherlight",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode"
  ]
}
```

### 7. Documentation Templates

#### `README.md`
```markdown
# [Project Name]

> Powered by ÆtherLight 🚀

## Overview
[Project description]

## Setup
\`\`\`bash
# Clone repository
git clone [repo-url]

# Install dependencies
npm install

# Install ÆtherLight globally
npm install -g aetherlight@latest

# Open in VS Code/Cursor
code .
\`\`\`

## Development Workflow

### Starting Work
1. Pull latest: `git pull origin develop`
2. Create branch: `git checkout -b feature/[name]`
3. Open ÆtherLight: Press backtick (`)
4. Voice command: "Start working on [feature]"

### Committing
- Use semantic commits: `feat:`, `fix:`, `docs:`, etc.
- ÆtherLight handles commit messages

### Code Analysis
- Voice: "Analyze my code"
- Command: `/code-analyze`

### Sprint Planning
- Voice: "Plan next sprint"
- Command: `/sprint-plan`

## Project Structure
\`\`\`
.
├── .claude/          # ÆtherLight configuration
├── sprints/          # Sprint definitions
├── src/              # Source code
├── tests/            # Test files
├── docs/             # Documentation
└── analysis/         # Code analysis reports
\`\`\`
```

### 8. Protection Rules

#### `PROTECTED.md`
```markdown
# Protected Code Policy

## What Cannot Be Changed (After Release)

### Core Functions
- Function signatures in published APIs
- Database schemas without migration
- Authentication logic
- Payment processing

### How to Modify Protected Code

1. **Refactoring Only**
   - Create `refactor/[name]` branch
   - Maintain exact same interface
   - All tests must pass
   - Requires 2 reviews

2. **Bug Fixes**
   - Create `fix/[issue]` branch
   - Minimal change principle
   - Add regression test
   - Document in CHANGELOG

3. **New Features**
   - New code only (don't modify existing)
   - Create `feature/[name]` branch
   - Extend, don't replace

## Enforcement

Protected files are marked with:
\`\`\`typescript
/**
 * @protected
 * @since v1.0.0
 * Modification requires refactor branch and review
 */
\`\`\`
```

### 9. User Onboarding

#### Interactive Setup
```typescript
// The skill prompts for:
const projectConfig = {
  name: await ask("Project name?"),
  type: await ask("Project type? (web/api/desktop/library)"),
  language: await ask("Primary language? (ts/js/python/rust)"),
  team: await ask("Team size? (solo/small/large)"),
  workflow: await ask("Workflow preference? (agile/kanban/custom)")
};

// Customizes setup based on answers
```

### 10. Validation

#### Ensure Setup Complete
```bash
# Check all required files exist
required_files=(
  ".claude/CLAUDE.md"
  ".claude/settings.json"
  "README.md"
  ".gitignore"
  "sprints/SPRINT_INITIAL.toml"
)

for file in "${required_files[@]}"; do
  [ -f "$file" ] || echo "Missing: $file"
done

# Verify Git setup
git remote -v || echo "No remote configured"
git branch --list || echo "No branches created"

# Test ÆtherLight
aetherlight --version || echo "ÆtherLight not installed"
```

## Success Criteria

Initialization succeeds when:
- [ ] All directories created
- [ ] Configuration files in place
- [ ] Git workflow configured
- [ ] VS Code integrated
- [ ] Initial sprint created
- [ ] Documentation complete
- [ ] User can start development

## Next Steps

After initialization:
1. Run `/sprint-plan` to plan first real sprint
2. Run `/code-analyze` to baseline code quality
3. Create first feature branch
4. Start development with voice commands