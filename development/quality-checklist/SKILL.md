---
name: quality-checklist
description: Code review quality checklist. Use before commits and during code review.
---

# Quality Checklist

## 1. Project Patterns

### Icons
- [ ] Icons via `core::ArtProvider::getInstance().getIcon()`?
- [ ] QActions via `core::ArtProvider::getInstance().createAction()`?
- [ ] NO hardcoded paths `QIcon("path/...")`?

### UI Strings
- [ ] All user-visible strings via `tr()`?
- [ ] NO hardcoded strings in UI?

### Configuration
- [ ] Config via `core::SettingsManager::getInstance()`?
- [ ] NO hardcoded configuration values?

### Colors
- [ ] Colors via `core::ArtProvider::getInstance().getPrimaryColor()`?
- [ ] Or via `core::ThemeManager::getInstance().getCurrentTheme()`?
- [ ] NO hardcoded `QColor(r, g, b)`?

### Logging
- [ ] Using `core::Logger::getInstance().info/debug/error()`?
- [ ] Appropriate log levels?

## 2. Code Quality

### Naming
- [ ] Files: snake_case.cpp?
- [ ] Classes: PascalCase?
- [ ] Methods: camelCase?
- [ ] Members: m_camelCase?
- [ ] Constants: UPPER_SNAKE_CASE?

### Comments
- [ ] Doxygen for public methods (`///`)?
- [ ] No commented-out code?
- [ ] No TODO/FIXME in new code?

### Code style
- [ ] No unused imports/includes?
- [ ] No unused variables?
- [ ] Consistent indentation?

## 3. Documentation

### CHANGELOG.md
- [ ] Entry in [Unreleased] section?
- [ ] Correct category (Added/Changed/Fixed)?

### ROADMAP.md
- [ ] Checkbox marked [x] if feature complete?
- [ ] NO task numbers added?

### OpenSpec
- [ ] tasks.md updated (checkboxes)?
- [ ] status updated (if task complete)?

## 4. Build & Tests

### Build
- [ ] Build passes? (`scripts/build_windows.bat Debug`)
- [ ] No new warnings?

### Tests
- [ ] Existing tests still pass?
- [ ] New tests added (if new feature)?

## 5. Review Decision

### Approve if
- All checkboxes above are checked
- No critical issues found

### Request changes if
- Missing tr() for UI strings
- Hardcoded icons/colors
- Missing CHANGELOG entry
- Build fails
- Tests fail

### Block if
- Security issues
- Breaking changes without discussion
- Major architectural violations

## 6. Output Format

```json
{
  "decision": "approve" | "request_changes" | "block",
  "summary": "Brief summary",
  "issues": [
    "Issue 1 description",
    "Issue 2 description"
  ]
}
```
