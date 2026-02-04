---
name: check-a11y
description: Perform accessibility audit on web pages. Use when users ask to check accessibility, audit WCAG compliance, verify ARIA usage, check color contrast, audit keyboard navigation, or analyze screen reader compatibility. Detects ARIA issues, focus problems, contrast issues, and semantic HTML violations.
---

# Check A11y (Accessibility)

Perform accessibility audit on web pages for WCAG 2.1 compliance.

## Quick Start

```bash
cd /path/to/html-checker/scripts
bun src/check-a11y.ts <URL>
```

## CLI Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--verbose` | `-v` | false | Show all checks including passed |
| `--json` | `-j` | false | Output results as JSON |
| `--level` | `-l` | AA | WCAG level (A, AA, AAA) |

## Checks Performed

| Check | WCAG | Severity | Description |
|-------|------|----------|-------------|
| Missing lang | 3.1.1 | Error | HTML has no lang attribute |
| Skip link missing | 2.4.1 | Warning | No skip to main content link |
| Missing landmarks | 1.3.1 | Warning | No main, nav, header landmarks |
| Empty links | 2.4.4 | Error | Links with no accessible name |
| Empty buttons | 4.1.2 | Error | Buttons with no accessible name |
| Missing focus styles | 2.4.7 | Warning | Interactive elements lack focus indicator |
| Tabindex > 0 | 2.4.3 | Warning | Positive tabindex disrupts focus order |
| ARIA hidden focusable | 4.1.2 | Error | Focusable element inside aria-hidden |
| Invalid ARIA | 4.1.2 | Error | Invalid ARIA attributes or values |
| Missing alt | 1.1.1 | Error | Images without alt text |
| Low contrast | 1.4.3 | Warning | Text contrast below 4.5:1 |
| Auto-playing media | 1.4.2 | Warning | Audio/video with autoplay |

## Usage Examples

```bash
# Basic audit
bun src/check-a11y.ts https://example.com

# Verbose output
bun src/check-a11y.ts https://example.com --verbose

# AAA level compliance
bun src/check-a11y.ts https://example.com --level AAA
```

## Output Example

```
Accessibility Audit for https://example.com
WCAG Level: AA

Summary:
  Passed: 18
  Warnings: 5
  Errors: 3

Page Structure:
  [OK] Language declared: lang="en"
  [OK] Main landmark present
  [WARNING] No skip link found
  [WARNING] Multiple nav without labels

Interactive Elements:
  [OK] 45 links checked
  [ERROR] 2 empty links found
  [OK] 12 buttons checked
  [WARNING] 3 buttons rely on icon only

ARIA Usage:
  [OK] Valid ARIA roles
  [ERROR] aria-labelledby references missing ID
  [WARNING] Redundant ARIA on semantic elements

Issues:
  [ERROR  ] Empty link at position 12 (WCAG 2.4.4)
    <a href="/search"><i class="icon-search"></i></a>
  [ERROR  ] Invalid aria-labelledby at position 34 (WCAG 4.1.2)
    <div aria-labelledby="nonexistent-id">
  [WARNING] No skip link (WCAG 2.4.1)
    Add <a href="#main">Skip to content</a>

Score: 72/100 (Level AA)

Recommendations:
  - Add aria-label to icon-only links
  - Fix aria-labelledby references
  - Add skip link for keyboard users
```

## WCAG Quick Reference

### Level A (Minimum)

- 1.1.1: Non-text content needs alt text
- 2.1.1: All functionality via keyboard
- 4.1.2: Name, role, value for UI components

### Level AA (Recommended)

- 1.4.3: Contrast ratio 4.5:1 minimum
- 2.4.7: Focus visible
- 3.1.2: Language of parts

### Level AAA (Enhanced)

- 1.4.6: Contrast ratio 7:1
- 2.4.9: Link purpose from link text alone
