---
name: auditing-interface-quality
description: Comprehensive UI/UX compliance check (A11y, performance, responsive).
phase: 10 (Compliance)
role: Reviewer
---

# Auditing Interface Quality

**Role Constraints:** Reviewer (STRICTLY READ-ONLY for application code). You MAY NOT modify, fix, or write to application source code.
**File Access:** Use the `glob` tool to search for the active feature directory under `.jonggrang/.output/features/`. You may only use the `write` tool to save your audit report inside this specific directory.

## Objective
Perform a systematic audit of the interface quality across accessibility (A11y), performance, theming, and responsive design.

## Execution Steps

1. **Discover Context:** Use `glob` and `read` to review the frontend components built or modified for the current feature.
2. **Live Browser Check (anoa):** Whenever the app can be served, validate the
   *rendered* UI — not just the source — with the `anoa` CLI (preinstalled in the
   sandbox). It only observes the page, so it is safe under the read-only Reviewer role.
   The browser is a session: start it once, then every command attaches to it.
   ```bash
   anoa --headless --port 9222 &                # once; `anoa status` exit 3 = not running
   anoa open <app-url> && anoa wait --load
   anoa snapshot -i                             # interactive elements with @refs
   anoa screenshot audit-desktop.png
   anoa set viewport 375 812                    # re-check responsive
   anoa screenshot audit-mobile.png
   anoa set media dark && anoa screenshot audit-dark.png
   anoa errors                                  # a page can look right and still throw
   ```
   Save screenshots into the active feature directory. See
   `skills/core/anoa/SKILL.md` for the tool and
   `skills/library/frontend/validating-visual-design/SKILL.md` for the full workflow.
3. **Diagnostic Scan** (use the snapshot/screenshots as evidence):
   - **Accessibility (A11y):** Check for contrast issues, missing ARIA roles, poor keyboard navigation, semantic HTML, and alt text.
   - **Performance:** Look for layout thrashing, expensive animations, unoptimized images, or unnecessary re-renders.
   - **Theming:** Look for hard-coded colors instead of design tokens, and broken dark mode implementations.
   - **Responsive Design:** Check for fixed widths, touch target sizes (<44px), and horizontal scrolling issues on narrow viewports.
4. **Compile Audit Report:**
   - Document each issue with its Location, Severity (Critical/High/Medium/Low), Category, Impact, and Recommendation.
   - Summarize the overall UI/UX compliance.
5. **Save Report:**
   - Write the final audit report using the `write` tool to `.jonggrang/.output/features/<active-feature-dir>/interface-audit.md`.

## Completion Signal
When the interface audit report is saved, output exactly:

INTERFACE_AUDIT_COMPLETE
