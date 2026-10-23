---
name: ui-control
description: Verify graphical browser, desktop, or Electron behavior through the actual interface. Use when screenshot, accessibility, console, network, trace, or browser-driven evidence is required; not for terminal-hosted interfaces, which belong to cli-control.
---

# UI Control

Gather reproducible evidence from the actual graphical surface without changing production behavior.

## Workflow

1. Identify the target surface, build or session, and observable contract.
2. Reuse the authorized running or authenticated surface when it is the target. Start a local app only when necessary and authorized. In a real authenticated session, an action can be an external write. Perform the interactions the user asked you to verify through the interface, such as submitting a form with invalid input to see it rejected. Never send requests directly to the server, and do not submit valid data, send, purchase, delete, or change settings beyond those interactions without explicit authority.
3. Prefer existing repository harnesses. Otherwise use the host's browser tools, or Playwright when it is already installed; do not install automation for a one-off probe. Locate controls by stable roles, labels, identifiers, or application markers.
4. Perform only actions needed for the requested behavior or a concrete risk. After each action, wait for its observable result instead of a fixed delay, and confirm it before the next action.
5. Capture the smallest relevant screenshot, accessibility output, console entry, network evidence, or trace from the running interface. Markup or source code alone does not show behavior: observe it.
6. Check loading, empty, error, keyboard, focus, responsive, and cleanup states only when material to the contract.
7. Clean up only servers, profiles, sessions, and artifacts created by this workflow.

Keep verification read-only unless the parent task separately authorizes implementation. Use `behavior-implement` for fixes, `phase-validate` for contract acceptance, and `test-gap-review` for evidence sufficiency.

Do not retain sensitive evidence, use stale selectors, or terminate user-owned resources.

Finish with the surface tested, actions, observed result, retained evidence, and blockers or limitations. Label a general rule you infer from the observations, such as how a filter matches, as an inference, and name the inputs you tried.
