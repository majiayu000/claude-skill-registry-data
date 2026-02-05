---
name: skill-isolation-tester
version: 0.2.1
description: Use PROACTIVELY when validating Claude Code skills before sharing or public release. Automated testing framework using multiple isolation environments (git worktree, Docker containers, VMs) to catch environment-specific bugs, hidden dependencies, and cleanup issues. Includes production-ready test templates and risk-based mode auto-detection. Not for functional testing of skill logic or non-skill code.
---

# Skill Isolation Tester

Tests Claude Code skills in isolated environments to ensure they work correctly without dependencies on your local setup.

## When to Use

**Trigger Phrases**:
- "test skill [name] in isolation"
- "validate skill [name] in clean environment"
- "test my new skill in worktree/docker/vm"
- "check if skill [name] has hidden dependencies"

**Use Cases**:
- Test before committing or sharing publicly
- Validate no hidden dependencies on local environment
- Verify cleanup behavior (no leftover files/processes)
- Catch environment-specific bugs

## Quick Decision Matrix

| Request | Mode | Isolation Level |
|---------|------|-----------------|
| "test in worktree" | Git Worktree | Fast, lightweight |
| "test in docker" | Docker | Full OS isolation |
| "test in vm" | VM | Complete isolation |
| "test skill X" (unspecified) | Auto-detect | Based on skill risk |

## Risk-Based Auto-Detection

| Risk Level | Criteria | Recommended Mode |
|------------|----------|------------------|
| Low | Read-only, no system commands | Git Worktree |
| Medium | File creation, bash commands | Docker |
| High | System config changes, VM ops | VM |

## Mode 1: Git Worktree (Fast)

**Best for**: Low-risk skills, quick iteration

**Process**:
1. Create isolated git worktree
2. Install Claude Code
3. Copy skill and run tests
4. Cleanup

**Workflow**: `modes/mode1-git-worktree.md`

## Mode 2: Docker Container (Balanced)

**Best for**: Medium-risk skills, full OS isolation

**Process**:
1. Build/pull Docker image
2. Create container with Claude Code
3. Run skill tests with monitoring
4. Cleanup container and images

**Workflow**: `modes/mode2-docker.md`

## Mode 3: VM (Safest)

**Best for**: High-risk skills, untrusted code

**Process**:
1. Provision VM, take snapshot
2. Install Claude Code
3. Run tests with full monitoring
4. Rollback or cleanup

**Workflow**: `modes/mode3-vm.md`

## Test Templates

Production-ready templates in `test-templates/`:

| Template | Use For |
|----------|---------|
| `docker-skill-test.sh` | Docker container/image skills |
| `docker-skill-test-json.sh` | CI/CD with JSON/JUnit output |
| `api-skill-test.sh` | HTTP/API calling skills |
| `file-manipulation-skill-test.sh` | File modification skills |
| `git-skill-test.sh` | Git operation skills |

**Usage**:
```bash
chmod +x test-templates/docker-skill-test.sh
./test-templates/docker-skill-test.sh my-skill-name

# CI/CD with JSON output
export JSON_ENABLED=true
./test-templates/docker-skill-test-json.sh my-skill-name
```

## Helper Library

`lib/docker-helpers.sh` provides robust Docker testing utilities:

```bash
source ~/.claude/skills/skill-isolation-tester/lib/docker-helpers.sh

trap cleanup_on_exit EXIT
preflight_check_docker || exit 1
safe_docker_build "Dockerfile" "skill-test:my-skill"
safe_docker_run "skill-test:my-skill" bash -c "echo 'Testing...'"
```

**Functions**: `validate_shell_command`, `retry_docker_command`, `cleanup_on_exit`, `preflight_check_docker`, `safe_docker_build`, `safe_docker_run`

## Validation Checks

**Execution**:
- [ ] Skill completes without errors
- [ ] Output matches expected format
- [ ] Execution time acceptable

**Side Effects**:
- [ ] No orphaned processes
- [ ] Temporary files cleaned up
- [ ] No unexpected system modifications

**Portability**:
- [ ] No hardcoded paths
- [ ] All dependencies documented
- [ ] Works in clean environment

## Test Report Format

```markdown
# Skill Isolation Test Report: [skill-name]
## Environment: [Git Worktree / Docker / VM]
## Status: [PASS / FAIL / WARNING]

### Execution Results
✅ Skill completed successfully

### Side Effects Detected
⚠️ 3 temporary files not cleaned up

### Dependency Analysis
📦 Required: jq, git

### Overall Grade: B (READY with minor fixes)
```

## Reference Materials

- `modes/mode1-git-worktree.md` - Fast isolation workflow
- `modes/mode2-docker.md` - Container isolation workflow
- `modes/mode3-vm.md` - Full VM isolation workflow
- `data/risk-assessment.md` - Skill risk evaluation
- `data/side-effect-checklist.md` - Side effect validation
- `templates/test-report.md` - Report template
- `test-templates/README.md` - Template documentation

## Quick Commands

```bash
# Test with auto-detection
test skill my-new-skill in isolation

# Test in specific environment
test skill my-new-skill in worktree  # Fast
test skill my-new-skill in docker    # Balanced
test skill my-new-skill in vm        # Safest
```

---

**Version**: 0.1.0 | **Author**: Connor
