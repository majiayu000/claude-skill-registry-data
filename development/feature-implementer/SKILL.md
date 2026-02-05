---
name: feature-implementer
description: Implement feature steps using git worktrees, build and test adaptively, update implementation plan, and generate test plans. This skill should be used when ready to implement one or more steps from an implementation plan, automatically adapting to any framework, language, or project structure.
---

# Feature Implementer Skill

## Purpose

Execute implementation steps from a plan, manage git worktrees for parallel development, adaptively build and test code, maintain plan progress, and generate comprehensive test plans. Works with any language, framework, or architecture through intelligent adaptation.

## When to Use This Skill

Use this skill when:

- Implementation plan is ready (created by `implementation-planner`)
- Ready to implement one or more steps from the plan
- Need to create git worktrees for parallel development
- Want automatic build/test execution after implementation
- Need to update plan progress systematically
- Want to generate test plans based on implementation changes

## Implementation Workflow

### Phase 1: Setup and Preparation

1. **Read the Implementation Plan**
   - Locate plan file (Plan.md, implementation-plan.md, etc.)
   - Identify next step(s) to implement
   - Check dependencies are satisfied
   - Identify if worktree is needed

2. **Create Git Worktree (if needed)**
   - Use `git-workflow-manager` skill for worktree creation
   - Follow GitFlow conventions: `feature/{name}`, `fix/{name}`, etc.
   - Switch to worktree directory

3. **Understand Project Structure**
   - Identify project type by reading config files
   - Find build commands (package.json, Makefile, .csproj, etc.)
   - Find test commands
   - Locate where to implement changes

**Adaptive Discovery:**
```
- React/Node: Read package.json → scripts.build, scripts.test
- .NET: Find *.csproj → dotnet build, dotnet test
- Python: Look for setup.py, pyproject.toml, Makefile
- Go: Check go.mod → go build, go test
- Rust: Find Cargo.toml → cargo build, cargo test
- Generic: Look for Makefile, build scripts
```

### Phase 2: Implementation

1. **Implement the Step**
   - Follow the step description from plan
   - Create/modify files as specified
   - Apply design patterns identified in research
   - Follow existing code conventions in the project

2. **Document Changes**
   - Add comments where complex logic exists
   - Update related documentation if needed
   - Note any deviations from original plan

**Key Principle:** Trust developer judgment for implementation details. The plan provides "what" and "where", developer provides "how".

### Phase 3: Build and Test

1. **Build the Project**
   - Execute build command discovered in Phase 1
   - Capture build output
   - If build fails: Fix errors, rebuild
   - If build succeeds: Proceed to testing

2. **Run Relevant Tests**
   - Execute test command discovered in Phase 1
   - Run tests related to changes (unit, integration)
   - Capture test results
   - If tests fail: Fix and re-run
   - If tests pass: Proceed to plan update

**Adaptive Testing:**
```bash
# Examples of adaptive test execution
# JavaScript/TypeScript
npm test

# .NET
dotnet test

# Python
pytest
python -m pytest

# Go
go test ./...

# Rust
cargo test

# Generic
make test
./run-tests.sh
```

**If Build/Test Commands Unknown:**
- Search for scripts in project root
- Check CI/CD config files (.github/workflows, .gitlab-ci.yml)
- Ask user: "How do you build/test this project?"

### Phase 4: Update Plan Progress

1. **Mark Step Complete**
   - Update checkbox in plan: `- [ ]` → `- [x]`
   - Update phase progress percentage
   - Note any blockers discovered
   - Document any deviations from plan

2. **Check Next Steps**
   - Identify if more steps can be done now
   - Check if dependencies are satisfied
   - Determine if iteration continues or pauses

**Plan Update Example:**
```markdown
## Phase 2: Backend Implementation

- [x] Step 2.1: Create EmailService class ✅
- [x] Step 2.2: Implement SendEmail method ✅
- [ ] Step 2.3: Add email queueing (next)

**Progress:** 2/3 steps complete (67%)
```

### Phase 5: Generate Test Plan

1. **Use `test-plan-generator` Skill**
   - Analyze changes made (git diff)
   - Determine types of tests needed
   - Generate test-plan.md with checkboxes
   - Avoid duplicate test coverage

2. **Test Plan Contents**
   - API tests (if backend changes)
   - E2E tests (if user-facing changes)
   - Unit tests (if complex logic added)
   - Performance tests (if performance-critical)

See `test-plan-generator` skill for detailed test plan generation.

## Handling Different Project Types

### React/TypeScript Project

**Discovery:**
```bash
# Files: package.json, tsconfig.json, vite.config.ts
# Build: npm run build
# Test: npm test
# Dev: npm run dev
```

**Implementation Pattern:**
- Components in `src/components/`
- Services in `src/services/`
- Types in `src/types/`
- Follow existing naming conventions

### .NET Web API Project

**Discovery:**
```bash
# Files: *.csproj, Program.cs, appsettings.json
# Build: dotnet build
# Test: dotnet test
# Run: dotnet run
```

**Implementation Pattern:**
- Controllers in `Controllers/`
- Services in `Services/`
- Entities in `Domain/Entities/`
- Follow existing namespace structure

### Python Project

**Discovery:**
```bash
# Files: setup.py, pyproject.toml, requirements.txt
# Build: python -m build (if applicable)
# Test: pytest, python -m pytest
# Run: python main.py or module-specific
```

**Implementation Pattern:**
- Follow existing module structure
- Use virtual environment
- Respect PEP 8 conventions

### Go Project

**Discovery:**
```bash
# Files: go.mod, go.sum
# Build: go build
# Test: go test ./...
# Run: go run main.go
```

**Implementation Pattern:**
- Follow Go package conventions
- Respect existing structure

### Generic/Unknown Project

**Discovery Strategy:**
1. Look for Makefile → `make`, `make test`
2. Look for build scripts → `./build.sh`, `./test.sh`
3. Check README for build/test instructions
4. Ask user: "How do I build and test this project?"

## Using Git Worktrees

### When to Use Worktrees

✅ **Use worktrees when:**
- Implementing multiple features in parallel
- Want to preserve working state in main worktree
- Working with team members on different features
- Need to switch between features frequently

❌ **Don't use worktrees when:**
- Simple linear development (single feature)
- Quick fixes that take <1 hour
- User doesn't need parallel development

### Creating Worktree

Use `git-workflow-manager` skill:

```bash
# Create feature worktree
# git-workflow-manager will handle:
# - Creating ../repo-worktrees/feature/feature-name/
# - Creating branch feature/feature-name
# - Setting up worktree
```

Refer to `git-workflow-manager` skill for detailed worktree management.

## Iteration Strategy

### Single-Step Implementation

Implement one step, build, test, update plan, generate test plan, done.

**Use when:**
- Steps are independent
- Step is complex and needs full focus
- User wants incremental progress

### Batch Implementation

Implement multiple related steps, build once, test once, update plan, generate test plan.

**Use when:**
- Steps are tightly coupled
- Build time is long
- Steps must work together to be testable

### Continuous Iteration (Workflow Mode)

Implement → Build → Test → Update → Next step → Repeat until phase complete.

**Use when:**
- User wants autonomous completion of a phase
- Steps are clear and dependencies satisfied
- Build/test feedback loop is fast

## Adaptive Build and Test Execution

### Build Execution Strategy

1. **Try Common Commands:**
   ```bash
   # Try in order based on project type detected
   npm run build
   dotnet build
   make
   go build
   cargo build
   python -m build
   mvn package
   gradle build
   ```

2. **Parse Build Output:**
   - Detect errors vs warnings
   - Identify files with errors
   - Extract error messages
   - Determine if build succeeded

3. **Handle Build Failures:**
   - Report errors clearly
   - Identify cause if possible
   - Suggest fixes if errors are common patterns
   - Iterate: Fix → Rebuild

### Test Execution Strategy

1. **Try Common Test Commands:**
   ```bash
   npm test
   dotnet test
   pytest
   go test ./...
   cargo test
   make test
   mvn test
   ```

2. **Selective Testing (if possible):**
   - Run only tests related to changes
   - Skip slow integration tests during iteration
   - Run full test suite before marking complete

3. **Handle Test Failures:**
   - Report which tests failed
   - Extract failure messages
   - Determine if failures are related to changes
   - Iterate: Fix → Retest

## Plan Update Best Practices

### Checkbox Updates

```markdown
# Before
- [ ] Step 1: Create EmailService

# After
- [x] Step 1: Create EmailService
```

### Progress Tracking

```markdown
## Phase 2: Backend (67%)

- [x] Step 2.1: Done
- [x] Step 2.2: Done
- [ ] Step 2.3: Next
```

### Notes on Deviations

If implementation differs from plan:

```markdown
- [x] Step 2.2: Implement SendEmail method
  **Note:** Used Microsoft Graph instead of SMTP as decided during research
```

### Documenting Blockers

If step cannot be completed:

```markdown
- [ ] Step 3.1: Deploy to staging
  **Blocker:** Staging environment credentials not available
  **Status:** Waiting for DevOps team
```

## Integration with Other Skills

### Dependencies

- **`git-workflow-manager`**: For worktree creation and management
- **`test-plan-generator`**: For generating test plans after implementation

### Workflow Position

```
feature-research → implementation-planner → feature-implementer → test-executor → test-fixer
                                                    ↓
                                            test-plan-generator
```

## Common Implementation Patterns

### Pattern 1: Backend API Endpoint

**Plan Step:** "Create POST /api/forms endpoint"

**Implementation:**
1. Create controller method
2. Add route attribute
3. Define DTO
4. Add validation
5. Implement business logic
6. Return response
7. Build and test

### Pattern 2: Frontend Component

**Plan Step:** "Create FormBuilder component"

**Implementation:**
1. Create component file
2. Define props interface
3. Implement component logic
4. Add styling
5. Export component
6. Build and test

### Pattern 3: Database Migration

**Plan Step:** "Add Submission entity to database"

**Implementation:**
1. Create entity class
2. Add DbSet to context
3. Create migration
4. Review migration SQL
5. Apply migration
6. Verify schema

## Tips for Effective Implementation

1. **Read Plan Carefully**: Understand the step fully before coding
2. **Check Dependencies**: Ensure prerequisite steps are complete
3. **Follow Conventions**: Match existing code style and patterns
4. **Build Often**: Don't wait until end to build
5. **Test Incrementally**: Test as you go, not just at the end
6. **Update Plan Promptly**: Mark steps complete immediately
7. **Document Deviations**: Note any changes from original plan
8. **Ask When Uncertain**: If build/test commands unknown, ask user
9. **Generate Test Plans**: Don't forget to create test-plan.md
10. **Communicate Progress**: Keep plan updated for visibility

## Bundled Resources

- `references/implementation-checklist.md` - Quality checklist for implementations
- `references/update-plan-guide.md` - Guide for updating plans
- `references/common-build-patterns.md` - Build/test commands by framework
