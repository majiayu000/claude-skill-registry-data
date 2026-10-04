---
name: exploratory-testing
description: Perform comprehensive exploratory testing on a website using browser automation, covering user journeys, forms, errors, accessibility, responsiveness, performance, and security basics. Use when asked to QA a site, explore an app, find bugs, or produce a browser testing report.
metadata:
  context: fork
---

# Website Exploratory Testing

## Goal

ultrathink

You are tasked with performing comprehensive exploratory testing on a website using the user's configured browser automation tool.

Your goal is to identify functional and non-functional deficiencies through systematic exploration.

## Setup Instructions

1. Use the available browser automation tool (see CLAUDE.md for configured tool)
2. Create a sub-task for browser operations to manage context window efficiently

## Authentication Handling

**IMPORTANT**: If you encounter login pages, authentication requirements, CORs errors, or areas requiring user credentials:
- **STOP** testing immediately
- Document what you've found so far
- Ask the user to provide necessary login credentials (username/password, API keys, etc.)
- Wait for credentials before proceeding with authenticated areas
- Once provided, continue testing both public and authenticated sections

## Testing Methodology

Perform exploratory testing using these established techniques:

### Core Testing Areas
- **User Journey Testing**: Navigate critical user paths (registration, login, checkout, etc.)
- **Boundary Testing**: Test form inputs with edge cases (empty, max length, special characters)
- **Error Handling**: Deliberately trigger errors to test graceful failure
- **Accessibility Testing**: Check ARIA labels, keyboard navigation, color contrast
- **Responsive Design**: Test different viewport sizes and orientations
- **Performance**: Monitor page load times and resource usage
- **Security Basics**: Check for exposed sensitive data, insecure forms
- **Cross-browser Compatibility**: Test core functionality across browsers
- **Authentication Flow**: Test login/logout, session management, password reset (when credentials provided)

### Testing Approach
1. Start with homepage reconnaissance - understand site structure
2. Identify and test all publicly accessible interactive elements
3. **Stop and request credentials** if authentication is required
4. Test authenticated areas once credentials are provided
5. Follow happy path user journeys first, then explore edge cases
6. Test error scenarios and recovery paths
7. Validate accessibility and usability patterns
8. Check mobile responsiveness and touch interactions
9. Monitor console errors and network issues throughout

## Issue Classification

**🔴 CRITICAL (Red X)**:
- Broken core functionality
- Security vulnerabilities
- Accessibility violations preventing usage
- Site crashes or unrecoverable errors
- Authentication bypasses or exposures

**⚠️ WARNING (Yellow Warning)**:
- Poor UX patterns
- Minor accessibility issues
- Performance concerns
- Inconsistent behavior
- Weak authentication patterns

**✅ PASSED (Green Checkmark)**:
- Working functionality
- Good user experience
- Proper error handling
- Accessibility compliance
- Secure authentication flow

## Report Requirements

Create a comprehensive markdown report saved as `exploratory_testing_report_YYYY-MM-DD_HH-MM-SS.md` (use current date and timestamp) with:

### Structure:
1. **🔴 CRITICAL ISSUES** (at top for visibility)
2. **⚠️ WARNINGS & CONCERNS**
3. **✅ PASSED TESTS**
4. **AUTHENTICATION STATUS** (what was tested with/without login)
5. **EXECUTIVE SUMMARY** (2-3 readable paragraphs)
6. **RECOMMENDED ACTION PLAN** (prioritized steps to resolve issues)

### Content Guidelines:
- Include specific steps to reproduce issues
- Capture screenshots for visual problems
- Note which browsers/devices were tested
- Clearly distinguish between authenticated vs non-authenticated testing
- Provide clear, actionable recommendations
- Use proper markdown formatting with checkboxes and status icons

## Execution Notes

- Work systematically through each testing area
- Document everything you test, even if it passes
- **Always stop and ask for credentials when auth is encountered**
- When you find issues, explore related functionality for patterns
- Take screenshots of important findings
- Keep detailed notes of your testing process

Please provide the website URL you'd like me to test when ready to begin.
