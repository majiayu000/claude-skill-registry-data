---
name: hebrew-dates-dev
description: "Project-specific skill for developing the Hebrew Dates WordPress Admin dashboard widget. Guides implementation, tracks development process, documents challenges/learnings, and ensures project requirements are met."
compatibility: "WordPress 6.x+, PHP 7.4+"
---

# Hebrew Dates Plugin Development Skill

## Purpose

This skill guides the development of a WordPress Admin dashboard widget that displays the current Hebrew date. It ensures:
- Plugin meets all technical requirements
- Development process is documented for the required README
- Security best practices are followed
- Challenges and learnings are tracked

## Project Requirements Summary

### Plugin Must:
1. Activate without errors
2. Display Hebrew date in a dashboard widget
3. Include basic security hygiene

### Repository Must Include:
1. Plugin files (functional code)
2. README.md with:
   - Why Hebrew dates were chosen
   - AI tools/models used
   - Development process description
   - Struggles encountered and solutions

## When to Use This Skill

Invoke this skill (`/hebrew-dates-dev`) when:
- Starting or resuming plugin development
- Needing guidance on next development steps
- Documenting a challenge or learning
- Preparing to write/update the README
- Reviewing code for security or best practices
- Verifying the plugin meets requirements

## Procedure

### Phase 1: Project Setup

1. **Create plugin file structure:**
   ```
   hebrew-dates-wp-admin/
   ├── hebrew-dates-admin.php     # Main plugin file
   ├── includes/
   │   └── class-hebrew-date.php  # Hebrew date calculation
   ├── README.md                  # Required documentation
   └── .claude/
       └── process-journal.md     # Development log (private)
   ```

2. **Initialize process journal:**
   - Create `.claude/process-journal.md` to track development
   - Log each significant step, challenge, and decision

### Phase 2: Core Implementation

1. **Main plugin file** (`hebrew-dates-admin.php`):
   - Plugin header with proper metadata
   - Security: Direct access prevention
   - Hook into `wp_dashboard_setup` action
   - Register the dashboard widget

2. **Hebrew date calculation** (`includes/class-hebrew-date.php`):
   - Convert current Gregorian date to Hebrew date
   - Format Hebrew date with Hebrew month names
   - Handle edge cases (sunset transitions if desired)

3. **Dashboard widget display:**
   - Clean, readable output
   - Proper escaping of all output
   - Minimal styling (optional inline CSS)

### Phase 3: Security Hygiene

Before considering complete, verify:
- [ ] Direct file access is blocked (`defined('ABSPATH')` check)
- [ ] All output is properly escaped (`esc_html()`, `esc_attr()`)
- [ ] No user input is processed (reduces attack surface)
- [ ] Plugin follows WordPress coding standards

See: `references/security-checklist.md`

### Phase 4: Testing

1. **Activation test:**
   ```bash
   # In wp-env or local WordPress
   wp plugin activate hebrew-dates-admin
   wp plugin list | grep hebrew
   ```

2. **Visual verification:**
   - Log into WordPress Admin
   - Navigate to Dashboard
   - Confirm widget displays with correct Hebrew date

3. **Error check:**
   ```bash
   wp eval "error_reporting(E_ALL); require_once('wp-content/plugins/hebrew-dates-admin/hebrew-dates-admin.php');"
   ```

### Phase 5: Documentation

1. **Update README.md** using the template in `references/readme-template.md`
2. **Review process journal** for key struggles and learnings
3. **Document AI usage** (Claude Code with Opus 4.5)

## Verification Checklist

Before submission:

- [ ] Plugin activates without PHP errors/warnings
- [ ] Dashboard widget appears on Admin Dashboard
- [ ] Hebrew date displays correctly
- [ ] All PHP files have ABSPATH check
- [ ] All output uses WordPress escaping functions
- [ ] README.md contains all required sections
- [ ] Process/challenges are documented

## Process Journal Management

Track development in `.claude/process-journal.md`:

```markdown
## YYYY-MM-DD: [Topic]

### What I did
[Description of work]

### What worked
[Successful approaches]

### What didn't work
[Failed approaches and why]

### What I learned
[Key insights]

### AI assistance
[How Claude Code helped]
```

## Common Issues

### Widget not appearing
- Check hook is `wp_dashboard_setup`, not `admin_init`
- Verify callback function exists and is callable
- Confirm plugin is activated

### Incorrect Hebrew date
- Verify timezone handling
- Check date calculation logic
- Consider sunset transitions (Orthodox calendars switch at sunset)

### Activation errors
- Check for syntax errors: `php -l hebrew-dates-admin.php`
- Verify all included files exist
- Check for PHP version incompatibilities

## References

- `references/development-workflow.md` - Step-by-step implementation guide
- `references/process-journal.md` - Journal template and examples
- `references/security-checklist.md` - Security verification checklist
- `references/readme-template.md` - README.md template for submission

## Escalation

For Hebrew calendar calculations, reference:
- PHP `cal_from_jd()` with `CAL_JEWISH` constant
- The jewish calendar functions in PHP's calendar extension

For WordPress dashboard widgets, reference:
- `wp_add_dashboard_widget()` function
- WordPress Dashboard Widgets API documentation
