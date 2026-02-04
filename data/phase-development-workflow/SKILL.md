---
name: phase-development-workflow
description: Complete 12-step workflow for phase development from branch creation to merge. Use this when starting a new phase or when asked to follow the phase development process.
---

# Phase Development Workflow

Complete workflow for developing and releasing a new phase in the PythonOpenGL blog series project.

## When to use this skill

Use this skill when:
- Starting a new phase development (e.g., "Start Phase 7a development")
- Asked to "follow the phase development workflow"
- Need guidance on the complete development-to-release process

## Complete Workflow (12 Steps)

Follow these steps in order for each phase development:

### Step 1: Branch Creation
**Owner**: User
**Task**: Create and checkout a new branch
**Format**: `phase{number}/{keyword}`
**Examples**: `phase4/shader-triangle`, `phase6b/complex-shapes`

```bash
git checkout -b phase{number}/{keyword}
```

### Step 2: Refactoring (Optional)
**Owner**: Copilot/User
**Task**: Clean up code before adding new features

**Sub-steps**:
1. **2-1**: User specifies refactoring targets and goals
2. **2-2**: Copilot proposes refactoring specification
3. **2-3**: Copilot implements refactoring
4. **2-4**: Copilot creates and runs unit tests
5. **2-5**: User reviews and approves changes

### Step 3: Code & Article Creation
**Owner**: Copilot/User
**Task**: Implement features, write blog article, create tests

**Sub-steps**:
1. **3-1**: User confirms requirements (check existing specs)
2. **3-2**: Copilot implements code and writes article draft
3. **3-3**: Copilot runs automated tests and self-review
4. **3-4**: User reviews test results and approves implementation

### Step 4: Change Review
**Owner**: Copilot/User
**Task**: Review all changes using git diff

**Sub-steps**:
1. **4-1**: Copilot explains changes and intentions
2. **4-2**: User reviews diff and approves

### Step 5: Verification
**Owner**: Copilot/User
**Task**: Run application and verify functionality

**Sub-steps**:
1. **5-1**: Copilot provides execution procedure and test cases
2. **5-2**: User executes application and verifies behavior
3. **5-3**: Copilot creates unit tests for newly added classes
4. **5-4**: User reviews and approves test results

### Step 6: Final Review
**Owner**: User
**Task**: Final review of all changes before commit

### Step 7: Commit & Push
**Owner**: User
**Task**: Commit changes and push to remote

```bash
git add -A
git commit -m "feat: Phase {number} - {feature description}"
git push -u origin phase{number}/{keyword}
```

**Commit message format**:
- Feature: `feat: Phase {number} - {description}`
- Documentation: `docs: Phase {number} - {description}`
- Bug fix: `fix: {description}`
- Refactoring: `refactor: {description}`

**Examples**:
- `feat: Phase 5a - Implement coordinate transformation system`
- `docs: Phase 5a - Update links (published articles)`

**HTTP 400 Error Fix** (for large files like images):
```bash
git config http.postBuffer 524288000  # 500MB
git push origin main
```

### Step 8: Article Publication
**Owner**: User
**Task**: Publish article on Hatena Blog and provide URL

**Platform**: https://an-embedded-engineer.hateblo.jp/

### Step 9: Link Updates
**Owner**: Copilot/User
**Task**: Update links in 4 files after publication

**Sub-steps**:
1. **9-1**: Copilot creates link update plan
2. **9-2**: Copilot modifies files
3. **9-3**: User verifies URLs and commits changes

**Note**: For detailed instructions, see the `update-blog-links-after-publish` skill.

### Step 10: Link Update Review
**Owner**: User
**Task**: Review link updates

### Step 11: Tag & Merge
**Owner**: User
**Task**: Create tag and merge to main

```bash
git checkout main
git merge phase{number}/{keyword} --no-ff -m "Merge branch 'phase{number}/{keyword}' - {summary}

{detailed description}"

git tag -a v{number}.0 -m "Phase {number}: {title}

{release notes}"

git push origin main
git push origin v{number}.0
```

**Merge Policy**: Always use `--no-ff` (no fast-forward) to preserve branch history and make phase boundaries visible in the revision graph.

**Merge Message Template**:
```
Merge branch 'phase{number}/{keyword}' - {one-line summary}

Phase {number}: {Full Title}

## Features
- Feature 1
- Feature 2

## Performance Results (if applicable)
- Metric 1: before → after (change%)

## Testing
- {number} unit tests passing

## Documentation
- Blog URL: {blog article URL}

Closes #{phase number}
```

**Tag Message Template**:
```
Phase {number}: {Title}

Release Date: YYYY/MM/DD
Blog Article: {blog article URL}

## Summary
{1-2 sentence summary}

## Key Features
- Feature 1
- Feature 2

## Performance Results (if applicable)
- Metric 1: value
- Metric 2: value

## Testing
- {number} tests passing

## Files Added/Modified
- {list of main files}

## Dependencies
{New dependencies or "No new dependencies added"}

## Verified Environment
- OS
- Python version
- OpenGL version
```

### Step 12: Phase Completion
**Owner**: Copilot/User
**Task**: Prepare for next phase

**Sub-steps**:
1. **12-1**: Copilot creates next phase preparation plan (issues/tasks)
2. **12-2**: User reviews plan and approves next phase start

## Branch Strategy

- Each phase uses dedicated branch: `phase{number}/{keyword}`
- Tag on article publication: `v{number}.0`
- Merge to main after tagging

## Progress Tracking

When following this workflow, use checkboxes or task tracking to monitor progress:

```markdown
- [x] Step 1: Branch created
- [x] Step 2: Refactoring completed
- [ ] Step 3: Implementation in progress
...
```

## Example Usage

User: "Start Phase 7a development following phase-development-workflow"

Copilot should:
1. Confirm current step (usually Step 1)
2. Guide through each step sequentially
3. Provide clear completion criteria for each step
4. Wait for user approval at key checkpoints (2-5, 3-4, 4-2, 5-4, 6, 10, 12-2)
