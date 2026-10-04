---
name: write-e2e-test
description: Create, maintain, and verify end-to-end (E2E) tests using Playwright MCP. Use when a new feature or flow needs E2E coverage, when updating flows, or verifying UI and functional correctness.
---

# Write E2E Test Skill

> **Browser tooling — works for both toolsets.** Use whichever is configured:
> Playwright MCP (`mcp_playwright_browser_*`) for Claude, or the Copilot browser
> tools (`open_browser_page`, `read_page`, `screenshot_page`, `click_element`,
> `type_in_page`) for VS Code Copilot. Where this skill says "Playwright", use the
> equivalent tool from whichever set is available. Authoring **persistent** `.spec.ts`
> E2E files needs a Playwright test runner — if none is configured, verify
> interactively with the browser tools and cover flows with Vitest story tests instead.

## Purpose
Guide the creation, maintenance, and verification of end-to-end (E2E) tests using the available browser tools.

## When to Use
- A new feature or flow is implemented and needs E2E coverage
- Updating or refactoring existing flows
- Verifying UI and functional correctness across user journeys

## Workflow

1. **Identify Test Scenarios**
   - Review the feature spec, user story, or acceptance criteria
   - List critical user journeys, edge cases, and error paths

2. **Set Up Playwright MCP**
   - Ensure Playwright MCP is configured
   - Start the dev server if not already running

3. **Write E2E Test**
   - Create a new Playwright test file in the appropriate directory (e.g., `e2e/`)
   - Use Playwright MCP to record or script the test, covering:
     - Main user flows
     - Edge cases and error handling
     - Visual verification (screenshots, assertions)
   - Use sample data generators for realistic test data where available

4. **Run and Verify**
   - Execute the E2E test(s) against the running app
   - Use Playwright MCP to:
     - Validate UI state and visual correctness
     - Assert expected outcomes and error messages
   - Fix any issues or update tests as needed

5. **Maintain and Document**
   - Update tests when features or flows change
   - Document test coverage and known gaps

## Checklist
- [ ] Test scenarios identified from feature spec/user story
- [ ] Playwright MCP configured and running
- [ ] E2E test file created
- [ ] Main flows, edge cases, and errors covered
- [ ] Visual and functional assertions included
- [ ] Test passes against running app
- [ ] Test documented and referenced in feature/skill
