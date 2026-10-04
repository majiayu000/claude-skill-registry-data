---
name: a11y
description: Audit and implement accessibility in Flutter apps. Use when adding semantic labels, testing screen reader compatibility, ensuring WCAG compliance, fixing accessibility issues, or making UI accessible to all users. Covers Semantics widgets, contrast ratios, touch targets, and assistive technology support.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# a11y - Accessibility Implementation

Make Flutter apps accessible to everyone. Semantic labels, screen reader support, WCAG compliance.

## When to Use This Skill

- Adding semantic labels to custom widgets
- Auditing code for accessibility issues
- Testing with screen readers (TalkBack/VoiceOver)
- Fixing accessibility violations
- Implementing focus management

## Quick Reference

### The Four Pillars

1. **Perceivable** - Semantic labels, contrast ≥4.5:1, text scaling
2. **Operable** - Touch targets ≥48dp, focus order, keyboard nav
3. **Understandable** - Clear labels, error guidance
4. **Robust** - Semantics widget, live regions, proper roles

### Key Requirements

| Check | Requirement | Test |
|-------|-------------|------|
| Contrast | ≥4.5:1 | `textContrastGuideline` |
| Touch targets | ≥48×48dp | `androidTapTargetGuideline` |
| Labels | All interactive | `labeledTapTargetGuideline` |

### Commands

```bash
# Audit for accessibility issues
dart run .claude/skills/a11y/scripts/check.dart

# Audit specific feature
dart run .claude/skills/a11y/scripts/check.dart --feature auth

# Generate accessibility test file
dart run .claude/skills/a11y/scripts/check.dart --generate-tests feature_name
```

## Workflow

### 1. Audit

```bash
dart run .claude/skills/a11y/scripts/check.dart --feature {feature}
```

Look for: Images without `semanticLabel`, `IconButton` without `tooltip`, custom widgets without `Semantics`.

### 2. Add Semantics

Use patterns from [semantics-guide.md](semantics-guide.md):
- Images: `semanticLabel` property
- Icon buttons: `tooltip` property
- Custom widgets: `Semantics` wrapper

### 3. Test

Add accessibility tests per [testing-guide.md](testing-guide.md):

```dart
await expectLater(tester, meetsGuideline(textContrastGuideline));
await expectLater(tester, meetsGuideline(androidTapTargetGuideline));
await expectLater(tester, meetsGuideline(labeledTapTargetGuideline));
```

### 4. Manual Verification

Test with VoiceOver (iOS) and TalkBack (Android). All controls should be announced clearly.

## Guides

| Guide | Use For |
|-------|---------|
| [semantics-guide.md](semantics-guide.md) | Semantics widget patterns, roles, labels, focus |
| [testing-guide.md](testing-guide.md) | Automated and manual a11y testing |
| [examples.md](examples.md) | Complete accessible Flutter code |

## Checklist

- [ ] Images have `semanticLabel` or `ExcludeSemantics`
- [ ] `IconButton` has `tooltip`
- [ ] Custom widgets have `Semantics` wrapper
- [ ] Touch targets ≥48×48dp
- [ ] Text contrast ≥4.5:1
- [ ] Focus order matches visual layout
- [ ] Tested with VoiceOver/TalkBack
- [ ] Accessibility labels use i18n (`t.feature.accessibility.key`)

## Related Skills

- `/design` - Touch targets, contrast (visual aspects)
- `/testing` - Add accessibility tests with other tests
- `/i18n` - Localize accessibility labels
