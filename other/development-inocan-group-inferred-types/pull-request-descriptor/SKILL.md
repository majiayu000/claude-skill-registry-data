---
name: pull-request-descriptor
description: Analyze code diffs and commit messages between current branch and target branch to generate comprehensive Pull Request descriptions in markdown format. Automatically selects appropriate PR template and creates structured, informative PR descriptions ready for submission.
---

# Pull Request Descriptor

## Overview

This skill analyzes the changes between your current branch and a target branch (typically main/master) to generate comprehensive, well-structured Pull Request descriptions. It examines code diffs, commit history, and changed files to create informative PR descriptions that help reviewers understand the changes quickly.

## When to Use

Use this skill when:
- Ready to create a Pull Request
- User asks to "create PR description", "write PR summary", "PR 설명 작성해줘"
- Need to document changes for team review
- Want to generate a structured PR description automatically
- Preparing to merge a feature branch

**IMPORTANT:** This skill generates the PR description content. To actually create the PR on GitHub, use `gh pr create` command after generating the description.

## Key Features

- 🔍 Analyzes code diffs between branches
- 📝 Examines commit messages for context
- 📊 Identifies changed files and their purposes
- 🎯 Selects appropriate PR template automatically
- 📋 Generates structured markdown descriptions
- 🔄 Supports multiple PR templates (feature, bugfix, refactor, etc.)
- 🌐 Adapts to project language (English/Korean)
- 💾 Automatically saves to `pull_requests` directory
- ❓ Prompts user for target branch selection

## Core Workflow

### Step 1: Ask User for Target Branch

**IMPORTANT: Always ask the user to specify the target branch.**

```bash
# Check current branch first
git branch --show-current
```

**Ask the user:**

```markdown
현재 브랜치에서 어느 브랜치와 비교할 PR 설명을 생성할까요?

대상 브랜치를 입력해주세요 (예: main, develop, master):
```

**Wait for user to provide the target branch name.**

Common target branches:
- `main` - 기본 메인 브랜치
- `master` - 레거시 메인 브랜치
- `develop` - 개발 브랜치
- Custom branch names

**Validate the branch exists:**

```bash
# Check if target branch exists locally or remotely
git rev-parse --verify <target-branch> 2>/dev/null || git rev-parse --verify origin/<target-branch> 2>/dev/null
```

If branch doesn't exist, inform user and ask again.

### Step 2: Analyze Branch Differences

**Gather comprehensive change information:**

```bash
# Get commit history from target branch divergence point
git log <target-branch>..HEAD --oneline
git log <target-branch>..HEAD --format="%H%n%s%n%b%n---"

# Get complete diff from divergence point
git diff <target-branch>...HEAD --stat
git diff <target-branch>...HEAD --shortstat

# Get list of changed files with status
git diff <target-branch>...HEAD --name-status

# Get detailed diff for analysis
git diff <target-branch>...HEAD
```

**Important:** Use three-dot syntax (`...`) to compare from the merge base, not two-dot syntax.

**Analyze the following:**

1. **Commit Messages:**
   - All commits that will be included in the PR
   - Look for patterns in commit types (feat, fix, refactor, etc.)
   - Identify the main theme of changes
   - Note any breaking changes or important notes in commit bodies

2. **Changed Files:**
   - Total number of files changed
   - Lines added/removed
   - File types (source code, tests, docs, config)
   - Affected modules or components

3. **Code Changes:**
   - New features added
   - Bugs fixed
   - Code refactored
   - Dependencies updated
   - Tests added/modified
   - Documentation changes

4. **Scope and Impact:**
   - Which parts of the codebase are affected
   - Backend vs frontend changes
   - API changes
   - Database schema changes
   - Breaking changes

### Step 3: Determine PR Type and Select Template

**Analyze the changes to determine PR type:**

**Feature PR:**
- Adds new functionality
- Introduces new components/modules
- Extends existing features
- Multiple `feat:` commits

**Bugfix PR:**
- Fixes bugs or issues
- Corrects broken functionality
- Primarily `fix:` commits
- May reference issue numbers

**Refactor PR:**
- Code restructuring without functionality changes
- Performance improvements
- Code cleanup
- Primarily `refactor:` or `perf:` commits

**Documentation PR:**
- Updates documentation
- Adds code comments
- Updates README or guides
- Primarily `docs:` commits

**Chore PR:**
- Dependency updates
- Configuration changes
- Build system updates
- Primarily `chore:` commits

**Mixed PR:**
- Contains multiple types of changes
- Use the most prominent type
- Or use a general template

**Select appropriate template from `references/` directory based on PR type.**

### Step 4: Generate PR Description

**Use the selected template and fill in the sections:**

#### Core Sections (All Templates)

**1. Title:**
- Concise summary of changes (50-72 characters)
- Use conventional commit style if project uses it
- Examples:
  - `feat(auth): Add OAuth2 login support`
  - `fix(api): Resolve rate limiting issue`
  - `refactor(ui): Improve component structure`

**2. Summary:**
- 2-4 bullet points describing the main changes
- Focus on WHAT changed, not HOW
- Be concise but informative
- Use active voice

**3. Changes:**
- Detailed breakdown of changes by category
- Group related changes together
- Use subsections if needed (Backend, Frontend, Tests, Docs)
- Include file references where helpful

**4. Motivation and Context:**
- WHY these changes were made
- What problem does this solve?
- Link to issues if applicable
- Provide background for reviewers

**5. Testing:**
- How were these changes tested?
- New tests added?
- Manual testing performed?
- Edge cases covered?
- Testing checklist

**6. Screenshots/Examples (if applicable):**
- For UI changes, include before/after screenshots
- For API changes, show example requests/responses
- For CLI changes, show example usage

**7. Breaking Changes:**
- List any breaking changes
- Migration guide if needed
- Affected areas

**8. Related Issues/PRs:**
- Link to related issues: `Closes #123`, `Fixes #456`
- Link to related PRs
- Link to documentation

**9. Checklist:**
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated and passing
- [ ] No new warnings or errors
- [ ] Breaking changes documented

#### Template-Specific Sections

**Feature Template:**
- New functionality description
- Use cases
- Configuration options
- Feature flags (if applicable)

**Bugfix Template:**
- Bug description
- Root cause analysis
- Fix explanation
- Regression prevention

**Refactor Template:**
- Before/after comparison
- Performance impact
- Behavior unchanged confirmation

### Step 5: Review and Format

**Ensure the description is:**

1. **Well-Structured:**
   - Clear hierarchy with markdown headers
   - Proper use of lists and code blocks
   - Logical flow of information

2. **Complete:**
   - All relevant sections filled
   - No placeholder text remaining
   - All questions answered

3. **Accurate:**
   - All file references correct
   - Change counts accurate
   - No exaggeration or omission

4. **Professional:**
   - Clear, concise language
   - No typos or grammar errors
   - Consistent formatting
   - Appropriate tone

5. **Actionable:**
   - Reviewers know what to focus on
   - Testing steps are clear
   - Next steps identified

### Step 6: Save PR Description to File

**IMPORTANT: Automatically save the generated description to `pull_requests` directory.**

**Create directory if it doesn't exist:**

```bash
# Create pull_requests directory if not exists
mkdir -p pull_requests
```

**Generate filename based on current branch and date:**

```bash
# Get current branch name
CURRENT_BRANCH=$(git branch --show-current)

# Generate filename: pr-<branch-name>-<YYYYMMDD>.md
FILENAME="pull_requests/pr-${CURRENT_BRANCH}-$(date +%Y%m%d).md"
```

**Save the PR description:**

```bash
# Save to file
cat > "${FILENAME}" <<'EOF'
[Generated PR description content here]
EOF

echo "✅ PR 설명이 저장되었습니다: ${FILENAME}"
```

### Step 7: Present to User

**Show the generated PR description and file location:**

```markdown
## 📋 PR 설명 생성 완료

**파일 저장 위치:** `pull_requests/pr-<branch-name>-<date>.md`
**PR 유형:** Feature
**사용된 템플릿:** `feature-template.md`

---

[Generated PR description content here]

---

## 다음 단계

생성된 PR 설명이 `pull_requests` 디렉토리에 저장되었습니다.

**PR 생성하기:**

```bash
# GitHub CLI로 PR 생성
gh pr create --title "PR 제목" --body-file pull_requests/pr-<branch-name>-<date>.md

# 또는 파일 내용을 복사해서 GitHub UI에 붙여넣기
```

**파일 수정이 필요하면:**
- 저장된 파일을 직접 편집하거나
- 이 스킬을 다시 실행하여 새로운 설명 생성
```

**Output file naming convention:**
- Format: `pr-<branch-name>-<YYYYMMDD>.md`
- Example: `pull_requests/pr-feature-oauth-20251105.md`
- Date ensures multiple versions can coexist
- Branch name makes it easy to identify

## Integration with Workflow

This skill is typically used as **Step 7** in the development workflow:

1. ✅ Analyze requirements (prompt-enhancer)
2. ✅ Document plan (requirements-documenter)
3. ✅ Implement features (implementation-guide)
4. ✅ Review code (code-reviewer)
5. ✅ Write tests (test-generator)
6. ✅ Final review (review-finalizer)
7. ➡️ **Create PR description (this skill)**
8. Submit PR and address review comments

**Inputs:**
- Current branch with completed feature
- Target branch (user-specified via prompt)
- Commit history
- Code changes

**Outputs:**
- Comprehensive PR description in markdown (always saved to `pull_requests/` directory)
- File naming: `pr-<branch-name>-<YYYYMMDD>.md`
- Ready for use with `gh pr create` or GitHub UI

## PR Templates

The skill includes multiple templates in the `references/` directory:

1. **`feature-template.md`** - For new features
2. **`bugfix-template.md`** - For bug fixes
3. **`refactor-template.md`** - For refactoring work
4. **`docs-template.md`** - For documentation updates
5. **`chore-template.md`** - For maintenance tasks
6. **`standard-template.md`** - General purpose template

**Customize templates** for your project's needs by editing files in `references/`.

## Best Practices

### DO ✅

- Analyze ALL commits from the divergence point
- Include context about WHY changes were made
- Reference related issues and PRs
- Provide clear testing instructions
- Highlight breaking changes prominently
- Use appropriate markdown formatting
- Keep summary concise but informative
- Include visual aids (screenshots, diagrams) when helpful
- Make it easy for reviewers to understand changes
- Use consistent language with project conventions

### DON'T ❌

- Don't just list commit messages
- Don't omit important context
- Don't use vague descriptions like "various updates"
- Don't forget to mention breaking changes
- Don't skip the testing section
- Don't leave placeholder text in the template
- Don't make the description too long or too short
- Don't forget to proofread
- Don't ignore project-specific PR guidelines

## Advanced Features

### Handling Complex PRs

**For large PRs with many changes:**

1. Group changes by module or feature
2. Use collapsible sections for detailed info
3. Provide a high-level summary first
4. Link to detailed documentation if needed

**Example:**

```markdown
## Summary

This PR implements the new user dashboard with analytics, notifications, and settings.

## Changes by Module

<details>
<summary>📊 Analytics Module (15 files changed)</summary>

- Added analytics service
- Created chart components
- Implemented data aggregation
...
</details>

<details>
<summary>🔔 Notifications Module (8 files changed)</summary>

...
</details>
```

### Multi-Language Support

**Detect project language preference:**

```bash
# Check recent PRs and commit messages
gh pr list --limit 10 --json title

# Check if project is primarily Korean or English
```

**Use appropriate language in description:**
- Korean projects: Write description in Korean
- English projects: Write description in English
- Mixed: Ask user preference

### Auto-Detecting Breaking Changes

**Scan for breaking changes:**

```bash
# Look for BREAKING CHANGE in commit messages
git log <target-branch>..HEAD --format="%B" | grep -i "BREAKING CHANGE"

# Look for major version bumps
git diff <target-branch>...HEAD -- package.json | grep '"version"'

# Look for deleted/renamed public APIs
```

**Highlight prominently if found:**

```markdown
## ⚠️ BREAKING CHANGES

This PR contains breaking changes that require action:

1. **API Endpoint Renamed**: `/api/users` → `/api/v2/users`
   - Migration: Update all API calls to use new endpoint

2. **Function Signature Changed**: `authenticate(token)` → `authenticate(credentials)`
   - Migration: Pass `{token}` object instead of string
```

### Including Statistics

**Add helpful statistics to description:**

```markdown
## 📊 Statistics

- **Commits:** 12
- **Files Changed:** 47 files (+1,234 / -567 lines)
- **Components:** 8 new, 5 modified
- **Tests:** 23 new test cases
- **Coverage:** +5.2% (now 87.3%)
```

## Common Scenarios

### Scenario 1: Simple Feature PR

**Context:** Single feature, 3-5 commits, well-scoped

**Approach:**
- Use `feature-template.md`
- Concise summary with bullet points
- Focus on what the feature does
- Include basic testing info

### Scenario 2: Bug Fix PR

**Context:** Fixing a reported issue

**Approach:**
- Use `bugfix-template.md`
- Reference the issue number
- Explain root cause
- Describe the fix
- Show how it's verified

### Scenario 3: Large Refactor PR

**Context:** Major code restructuring, many files changed

**Approach:**
- Use `refactor-template.md`
- Emphasize "no behavior change"
- Group changes by area
- Before/after comparisons
- Comprehensive test coverage info

### Scenario 4: Mixed PR

**Context:** Contains features, fixes, and refactoring

**Approach:**
- Use `standard-template.md`
- Organize by change type
- Use sections for each type
- Prioritize the main change type

## Error Handling

### No Changes Detected

```markdown
ℹ️ No changes detected between current branch and <target-branch>.

Possible reasons:
- Branch is up to date with target
- Branch not pushed to remote
- Already merged

Check with:
$ git log <target-branch>..HEAD
```

### Target Branch Doesn't Exist

```markdown
❌ Target branch '<target-branch>' not found.

Available branches:
- main
- develop
- master

Please specify the correct target branch.
```

### Uncommitted Changes

```markdown
⚠️ Warning: You have uncommitted changes.

커밋되지 않은 변경사항은 PR 설명에 포함되지 않습니다.

권장사항:
- 변경사항을 먼저 커밋하거나
- 변경사항을 stash 하고 진행하거나
- 현재 상태 그대로 PR 설명 생성 (WIP 포함 가능)

계속 진행할까요?
```

### Branch Not Pushed

```markdown
⚠️ Current branch is not pushed to remote.

PR cannot be created until branch is pushed.

Run:
$ git push -u origin $(git branch --show-current)

Then create PR.
```

## Configuration

### Custom Templates

**Add project-specific templates:**

1. Create new template in `references/`
2. Follow existing template structure
3. Add sections relevant to your project
4. Update template selection logic

### Project Guidelines

**Adapt to project PR guidelines:**

```bash
# Check if project has PR template
ls .github/PULL_REQUEST_TEMPLATE.md
ls .github/pull_request_template.md
ls docs/PULL_REQUEST_TEMPLATE.md
```

**If project template exists, merge with our generated content.**

### Language Preference

**Set default language:**

```markdown
## Language Configuration

Default language: [auto-detect | english | korean]

Auto-detect checks:
1. Recent PR titles and descriptions
2. Commit message language
3. README language
4. User preference if unclear
```

## Examples

### Example 1: Feature PR

**User:** "PR 설명 작성해줘" (current branch: feature/oauth-login)

**Skill asks:** "현재 브랜치에서 어느 브랜치와 비교할 PR 설명을 생성할까요? 대상 브랜치를 입력해주세요 (예: main, develop, master):"

**User:** "main"

**Analysis:**
```bash
$ git log main..HEAD --oneline
abc1234 feat(auth): implement OAuth2 login
def5678 feat(auth): add OAuth provider configuration
ghi9012 test(auth): add OAuth integration tests
jkl3456 docs(auth): update authentication guide

$ git diff main...HEAD --shortstat
15 files changed, 847 insertions(+), 123 deletions(-)
```

**Generated Description:**

```markdown
# feat(auth): OAuth2 로그인 기능 추가

## Summary

- OAuth2 인증 플로우 구현 (Google, GitHub 지원)
- 기존 이메일/비밀번호 로그인과 통합
- OAuth 제공자 설정 UI 추가
- 통합 테스트 및 문서 작성 완료

## Changes

### Backend
- `src/auth/oauth/` - OAuth2 인증 서비스 구현
  - `OAuthService.ts` - OAuth 플로우 처리
  - `providers/` - Google, GitHub 제공자 구현
- `src/config/oauth.config.ts` - OAuth 설정 관리

### Frontend
- `src/pages/LoginPage.tsx` - OAuth 로그인 버튼 추가
- `src/components/OAuthButton.tsx` - 재사용 가능한 OAuth 버튼
- `src/hooks/useOAuth.ts` - OAuth 상태 관리 훅

### Tests
- `tests/integration/oauth.test.ts` - OAuth 플로우 통합 테스트
- `tests/unit/OAuthService.test.ts` - 서비스 단위 테스트

### Documentation
- `docs/authentication.md` - OAuth 설정 가이드 추가
- `README.md` - OAuth 기능 설명 업데이트

## Motivation and Context

사용자들이 소셜 계정으로 빠르게 로그인할 수 있도록 OAuth2 인증을 추가했습니다.
이메일/비밀번호 방식과 병행하여 사용자 편의성을 높입니다.

Closes #234

## Testing

### Manual Testing
- ✅ Google OAuth 로그인 테스트
- ✅ GitHub OAuth 로그인 테스트
- ✅ 기존 이메일 로그인 정상 동작 확인
- ✅ 에러 처리 (취소, 실패) 테스트

### Automated Tests
- 23 new integration tests (OAuth flows)
- 17 new unit tests (OAuthService, providers)
- All tests passing ✅

## Screenshots

[OAuth login buttons on login page]

## Checklist

- [x] Code follows project style guidelines
- [x] Self-review completed
- [x] Comments added for complex OAuth flow logic
- [x] Documentation updated (authentication guide)
- [x] Tests added and passing
- [x] No new warnings or errors
- [x] Environment variables documented in .env.example

---

📝 Generated with [claude-skills](https://github.com/your-org/claude-skills)
```

**Saved to:** `pull_requests/pr-feature-oauth-login-20251105.md`

**Next:** Use `gh pr create --title "feat(auth): OAuth2 로그인 기능 추가" --body-file pull_requests/pr-feature-oauth-login-20251105.md` to create the PR.

### Example 2: Bugfix PR

**User:** "create PR description" (current branch: fix/rate-limit-bug)

**Skill asks:** "현재 브랜치에서 어느 브랜치와 비교할 PR 설명을 생성할까요? 대상 브랜치를 입력해주세요 (예: main, develop, master):"

**User:** "main"

**Analysis:**
```bash
$ git log main..HEAD --oneline
abc1234 fix(api): correct rate limiting calculation
def5678 test(api): add rate limit edge case tests

$ git diff main...HEAD --shortstat
3 files changed, 45 insertions(+), 12 deletions(-)
```

**Generated Description:**

```markdown
# fix(api): Correct rate limiting calculation for burst requests

## Summary

- Fixed incorrect rate limit calculation that allowed burst requests to bypass limits
- Added edge case tests to prevent regression
- Verified fix in production-like environment

## Changes

- `src/middleware/rateLimit.ts` - Fixed time window calculation
- `tests/rateLimit.test.ts` - Added burst request test cases

## Bug Description

Rate limiting was using `Math.floor()` for time window calculation, which allowed
users to make burst requests at window boundaries and exceed the intended limit.

**Example:**
- Limit: 10 requests per minute
- Bug: User could make 10 requests at 00:59 and 10 more at 01:00 (20 in 2 seconds)
- Expected: Maximum 10 requests in any 60-second window

## Root Cause

```typescript
// Before (incorrect)
const window = Math.floor(Date.now() / windowSize);

// After (correct)
const window = Date.now() - windowSize;
```

## Fix

Changed from fixed time window to sliding window algorithm:
- Track request timestamps instead of window-based counting
- Remove expired timestamps before checking limit
- Provides true rate limiting across window boundaries

## Testing

### Manual Testing
- Verified burst request scenarios
- Tested with various time windows (1s, 1m, 1h)
- Confirmed existing functionality unaffected

### Automated Tests
- Added 5 new test cases for edge cases
- All existing tests still passing
- Coverage: +2.3% (now 89.1%)

## Related Issues

Fixes #456

## Checklist

- [x] Bug fix verified in dev environment
- [x] Regression tests added
- [x] No breaking changes
- [x] Performance impact assessed (negligible)
- [x] All tests passing
```

**Saved to:** `pull_requests/pr-fix-rate-limit-bug-20251105.md`

**Next:** Use `gh pr create --title "fix(api): Correct rate limiting calculation for burst requests" --body-file pull_requests/pr-fix-rate-limit-bug-20251105.md` to create the PR.

## Summary

This skill helps create comprehensive, professional Pull Request descriptions by:

1. **Prompting user for target branch** - Always asks which branch to compare against
2. **Analyzing code changes** - Thoroughly examines commits and diffs
3. **Selecting appropriate template** - Automatically chooses the right PR template
4. **Generating structured descriptions** - Creates well-formatted markdown content
5. **Saving to organized location** - Automatically saves to `pull_requests/` directory
6. **Including complete context** - Provides all information reviewers need
7. **Following project conventions** - Adapts to Korean language and project style

**Result:** Clear, informative PR descriptions saved to `pull_requests/pr-<branch>-<date>.md`, ready to use with `gh pr create` or GitHub UI.
