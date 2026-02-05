---
name: "Codebase Inspection Protocol"
description: "Mandatory inspection procedures for understanding Rails codebase structure before writing any code. Use this skill FIRST before any code generation task to discover existing patterns, conventions, dependencies, and file organization in the target Rails project."
---

# Codebase Inspection Protocol Skill

This skill provides mandatory inspection procedures that MUST be followed before any code generation or architectural decisions in a Rails project.

## When to Use This Skill

- **ALWAYS** before writing any new code
- Before making architectural decisions
- Before suggesting any pattern
- When assumptions are made about existing code
- Before creating any new file

## Core Rule

> **"Inspect before you suggest"**
>
> No planning decisions without codebase inspection. Every recommendation must cite observed file paths. Never assume a pattern exists—verify it first.

## Mandatory Inspection Checks

### 1. Project Structure

```bash
# Primary structure check
tree app -L 2 -I 'assets|javascript' 2>/dev/null || find app -type d -maxdepth 2

# List all app directories
ls -la app/*/ 2>/dev/null

# Count Ruby files
find app -type f -name '*.rb' | wc -l
```

**Answers**: What is the current project structure?

### 2. Existing Patterns

```bash
# Check for services directory
ls app/services/ 2>/dev/null || echo 'No services directory'

# Check for service subdirectories (namespace pattern)
ls app/services/*/ 2>/dev/null || echo 'No service subdirectories'

# Find service classes
grep -r 'class.*Service' app/ --include='*.rb' -l 2>/dev/null | head -10

# Find command classes
grep -r 'class.*Command' app/ --include='*.rb' -l 2>/dev/null | head -5

# Find query objects
grep -r 'class.*Query' app/ --include='*.rb' -l 2>/dev/null | head -5
```

**Answers**: What patterns are already in use?

### 3. Naming Conventions

```bash
# Sample a service file
head -30 $(find app/services -name '*.rb' 2>/dev/null | head -1) 2>/dev/null || echo 'No service files'

# Sample a model file
head -30 $(find app/models -name '*.rb' 2>/dev/null | head -1) 2>/dev/null

# List module/class definitions in services
grep -r 'module\|class' app/services/ --include='*.rb' 2>/dev/null | head -20
```

**Answers**: What naming and style conventions exist?

### 4. Dependencies

```bash
# Check Gemfile
cat Gemfile 2>/dev/null | grep -v '^#' | grep -v '^$' | head -60

# Check Ruby version
cat Gemfile.lock 2>/dev/null | grep -A1 'RUBY VERSION' || ruby -v

# Check Rails configuration
cat config/application.rb 2>/dev/null | head -40
```

**Answers**: What gems and tools are available?

### 5. Models and Domain

```bash
# List models
ls app/models/ 2>/dev/null

# Find models with associations
grep -l 'has_many\|belongs_to\|has_one' app/models/*.rb 2>/dev/null | head -10

# Sample a model file
head -50 $(find app/models -name '*.rb' 2>/dev/null | head -1) 2>/dev/null

# Check schema
head -100 db/schema.rb 2>/dev/null
```

**Answers**: What is the domain model structure?

### 6. Testing Patterns

```bash
# Check test directory structure
ls spec/ 2>/dev/null || ls test/ 2>/dev/null || echo 'No test directory found'

# Check spec helper
cat spec/spec_helper.rb 2>/dev/null | head -30 || cat spec/rails_helper.rb 2>/dev/null | head -30

# Check for service specs
ls spec/services/ 2>/dev/null || echo 'No service specs'
```

**Answers**: What testing conventions are in place?

## Contextual Checks

### When Creating a New File

```bash
# Check target directory
ls {target_directory}/ 2>/dev/null

# Sample existing files in target
find {target_directory} -name '*.rb' -exec head -20 {} \; 2>/dev/null | head -60
```

### When Implementing a Pattern

```bash
# Search for existing implementations
grep -r '{pattern_name}' app/ --include='*.rb' -l 2>/dev/null

# Find files with pattern name
find app -name '*{pattern_name}*' -type f 2>/dev/null
```

### When Modifying Existing Functionality

```bash
# Find all usages
grep -r '{class_name}' app/ --include='*.rb' -B2 -A5 2>/dev/null

# Find method calls
grep -r '{method_name}' app/ --include='*.rb' 2>/dev/null
```

### When Working with ViewComponents

```bash
# Check components directory
ls app/components/ 2>/dev/null

# Check component namespaces
ls app/components/*/ 2>/dev/null

# Sample existing component
head -40 $(find app/components -name '*_component.rb' | head -1) 2>/dev/null

# Check for inline vs file templates
grep -l 'def call' app/components/**/*_component.rb 2>/dev/null | head -3

# Check template files
ls app/components/**/*.html.erb 2>/dev/null | head -10
```

### When Working with Controllers

```bash
# List controllers
ls app/controllers/ 2>/dev/null

# Check controller namespaces
ls app/controllers/*/ 2>/dev/null

# Sample a controller
head -50 $(find app/controllers -name '*_controller.rb' | head -1) 2>/dev/null

# Check routes
rails routes 2>/dev/null | head -50 || cat config/routes.rb | head -50
```

### When Working with Background Jobs

```bash
# Check jobs directory
ls app/jobs/ 2>/dev/null || ls app/sidekiq/ 2>/dev/null

# Sample a job
head -30 $(find app/jobs -name '*.rb' | head -1) 2>/dev/null

# Check Sidekiq configuration
cat config/sidekiq.yml 2>/dev/null
```

## Method Visibility Inspection

When checking if methods can be called across layers:

```bash
# Find method definition with context
grep -B10 'def method_name' app/path/to/file.rb

# Check for private/protected keywords before method
grep -n 'private\|protected' app/path/to/file.rb

# List all public methods (before private keyword)
awk '/class/,/private/' app/path/to/file.rb | grep 'def '
```

## Inspection Output Format

After running inspection, document findings:

```markdown
## Inspection Findings

### Project Structure
- Services: `app/services/` with subdirectories for namespacing
- Components: `app/components/` with namespace folders
- Models: Standard Rails structure in `app/models/`

### Existing Patterns Observed
- Services follow: `{Domain}Manager::{Action}` pattern
- Example: `app/services/tasks_manager/create_task.rb`
- Components use separate template files (not inline)

### Naming Conventions
- Services: `TasksManager::CreateTask`
- Components: `Metrics::KpiCardComponent`
- Models: Standard ActiveRecord naming

### Dependencies Available
- Ruby 3.3.0
- Rails 7.1.0
- ViewComponent 3.x
- Sidekiq for background jobs

### Testing Structure
- RSpec in `spec/`
- FactoryBot for fixtures
- Service specs in `spec/services/`
```

## Anti-Pattern Detection

### Planning Without Inspection

**Detection**: Plan outputs lack file path citations

**Example Violation**:
```
"Let's create a service in app/services/..." 
(without checking if directory exists or pattern already in use)
```

### Assumption-Based Design

**Examples**:
- Suggesting Service Objects without checking if `app/services/` exists
- Recommending a gem without checking Gemfile
- Proposing a naming convention different from existing code
- Assuming Rails version without checking

### Blind Scaffolding

**Detection**: Code doesn't reference or match existing patterns

**Consequence**: Review existing similar files first

### Convention Invention

**Detection**: New naming pattern, structure, or style not present in codebase

**Consequence**: Either match existing convention or explicitly justify deviation

## Inspection Failure Handling

When inspection commands fail:

```markdown
**Inspection Limitation:**
- Unable to access: [path/file]
- Reason: [error message]
- Proceeding with assumption: [assumption]
- Risk: [potential issues if assumption is wrong]
```

## Quick Reference Commands

```bash
# Project structure
tree app -L 2 -I 'assets|javascript'

# Services
ls app/services/ 2>/dev/null

# Patterns
grep -r 'class.*Service' app/ --include='*.rb' -l | head -10

# Gems
cat Gemfile | grep -v '^#' | grep -v '^$'

# Models
ls app/models/

# Style sample
head -30 $(find app/services -name '*.rb' | head -1)

# Components
ls app/components/ 2>/dev/null

# Component pattern
head -40 $(find app/components -name '*_component.rb' | head -1)

# Schema
head -100 db/schema.rb
```

## Must Cite

When making any recommendation, cite evidence:

- Existing patterns: Reference specific file paths
- "Similar to X" references: Show the actual file
- Gemfile dependencies: Quote the gem line
- Existing conventions: Show example from codebase
