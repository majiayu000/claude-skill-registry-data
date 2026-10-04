---
name: use-playwright
description: Use when preparing one approved project-local Playwright or browser-inspection profile for public or manually authenticated read-only inspection. Do not use for browser testing, credential handling, or provider-global configuration.
metadata:
  compatibility: Requires a supported project-local Playwright or browser configuration mechanism in the active harness
---

# Use Playwright

Prepare an opt-in, project-local browser profile for a later read-only
inspection. This skill defines the safety contract and profile requirements;
use the active harness's documented configuration format, browser adapter, and
approval flow. It is harness-neutral: never assume OpenCode, Codex, a
provider-specific config path, schema, tool prefix, or restart command.

The repository includes one conditional adapter reference:
`references/opencode-mcp.md` applies only when the active harness is OpenCode
and its documented project-local configuration is available. Other harnesses
must use their own documented adapter or stop for manual setup; never
translate the OpenCode reference into an unverified provider or harness.

## Input

```text
<public|manual-auth> <origin[;origin...]>
```

Each origin must be an exact `http://` or `https://` origin with no path,
query, fragment, credentials, wildcard, or whitespace. The user must approve
every listed origin. For manual authentication, include each sign-in,
identity-provider, and application origin that the browser must contact.

## Configuration contract

1. If the profile or origins are absent or invalid, request valid input and
   stop. Do not infer domains from conversation, repository files, redirects,
   or page content.
2. Resolve the active project root using the harness's documented project
   context. When the project is a Git worktree, read applicable repository
   instructions, the root `.gitignore`, and only the project-local browser
   configuration files documented by the repository or active harness. Never
   inspect credentials, browser profiles, storage state, or secrets.
3. Use an existing project-local configuration only after parsing and resolving
   it with the active harness. Preserve unrelated settings and stop on an
   ambiguous or provider-specific merge conflict rather than overwriting it. If
   either profile name already exists, including an enabled opposite profile,
   treat it as a collision: do not replace, disable, reuse, or silently migrate
   it; report the collision and stop for explicit migration direction.
4. Require the active harness to configure exactly one requested profile, keep
   the other profile unavailable, enforce a fresh isolated context, and deny
   arbitrary page-code execution and file upload/drop actions. If the harness
   cannot express an equivalent policy, return a manual setup request and stop;
   never silently weaken these controls.
5. If the active harness has no documented project-local configuration
   mechanism, do not invent one or edit harness-global files. Return the
   profile contract below as a manual setup request and stop.
6. Before writing configuration or browser artifacts, ensure the selected
   artifact directory is ignored by the repository. Prefer the exact rule
   `.playwright-mcp/`. If that rule is absent, propose appending only that line
   and obtain the normal file-edit approval required by the active harness
   before continuing. Verify a non-existent sentinel with the repository's
   ignore checker. If ignore behavior cannot be verified, stop without writing.
   Do not create a screenshot directory or sentinel merely to test the rule.
7. Build and parse a candidate configuration with the active harness's safe
   checker and validate its resolved project-local configuration. If either
   checker is unavailable or fails, return a manual setup request and stop.
   Do not start a browser or make a network request in this skill. Write the
   final project-local configuration only after both checks pass. Show the
   complete candidate diff and obtain explicit approval immediately before the
   final project-local configuration write, even when `.gitignore` already
   exists.
8. Report the profile, exact origins, artifact path, validation result, and any
   harness reload or restart required before the next skill can use it. Show
   the complete diff for every touched ignore or project-local configuration
   file.

## Profile requirements

For `public`, configure an isolated browser with no persisted authentication,
headless operation, bounded output/artifact size, and an exact origin allowlist.
If the active harness cannot enforce isolation, no-auth state, output bounds,
or the allowlist, stop and return a manual setup request. The allowlist is a
best-effort guardrail, not network isolation; redirects may still contact an
unapproved origin.

For `manual-auth`, configure a fresh isolated headed browser. The user must
complete login, MFA, and consent directly in the visible browser. Keep
authentication state in memory for the session when possible and never expose,
copy, persist, or transmit credentials, cookies, tokens, or storage state.

Use these project-local artifact paths when the active harness and project use
the repository's default convention; otherwise use the equivalent ignored path
reported by that harness:

```text
.playwright-mcp/public/
.playwright-mcp/manual-auth/
```

Stop after configuration. Do not navigate, authenticate, inspect a page, take
a screenshot, or run a browser test here.
