---
name: cli-wizard-pattern
description: "Add an opt-in interactive wizard mode to an existing script, CLI, or Taskfile task, or build a new script whose required arguments are supplied by the user at run time. Use when the user asks to add interactive mode, an interactive wizard, a guided prompt flow, a `-i` / `--interactive` flag, numbered selection menus, or confirmation gates to a command — or to create a new script that interviews the user for its inputs. Covers the opt-in principle, numbered-menu selection, computable-option discovery, array-safe argument gathering, confirmation summaries, and clean cancellation. Language-agnostic principles with a tested PowerShell reference implementation."
metadata:
  version: 0.1.0
---

# CLI Wizard Pattern

Add a guided, opt-in wizard to a command so a human can select values instead of
memorizing flags, without changing how automation calls that command.

## When to Use

- Add `-i` / `--interactive` to an existing script or Taskfile task.
- Build a new script whose required arguments come from the user.
- Convert free-text prompts into numbered selection menus.

Not for steps only a human can perform against a third party (use the `wizard`
skill for those); this skill is about a command's own argument surface.

## Core Principles

### 1. Opt-in, never auto-detected

Interactive mode MUST require an explicit flag. Never fall back to interactive
mode when required arguments are missing.

**Why:** agents and CI run commands with no arguments to probe behavior. If a
missing argument silently launches a wizard, the process hangs on a prompt that
nothing will ever answer. Fail fast instead.

| Invocation | Behavior |
|---|---|
| `cmd` (no args, missing required) | Exit non-zero with a usage error |
| `cmd -i` | Launch the wizard |
| `cmd --branch foo` | Non-interactive, unchanged |

### 2. Prefer numbered menus over free text

Every value the tool can compute MUST be offered as a numbered selection. Free
text is the last resort, reserved for values that cannot be enumerated.

**Why:** menus are discoverable, typo-proof, and testable. Free text makes users
guess valid values and forces the parser to validate arbitrary input.

Discover options from the environment before prompting: list registered
worktrees, local branches, remotes, available databases, installed SDKs, known
environments, files matching a pattern. If the set is empty, fail with guidance
rather than prompting for a value the user cannot know.

### 3. Offer escape hatches and safe defaults

- Binary choices render as `1. Yes` / `2. No` with the default marked.
- Any enumerable list that may legitimately be absent (a remote to fetch, an
  optional scope) gets an explicit `(skip)` / `(none)` entry.
- Blank input accepts the documented default.

### 4. Confirm before mutating

After gathering inputs, print a summary of every resolved value and ask for a
final yes/no. This is the user's last chance to catch a wrong selection before
an irreversible operation runs.

### 5. Cancel cleanly at any step

An interruption at any prompt MUST exit without side effects and without a
non-zero error. Provide a quit token (`q`) on selection prompts and treat a
declined confirmation as a clean cancel.

### 6. Gather args, then reuse the existing path

The wizard resolves values into the command's normal parameters and then calls
the unchanged non-interactive logic. Do not fork the core operation.

**Why:** one execution path means one place for bugs, and the non-interactive
path stays provably intact.

## Transformation Workflow

1. **Inventory the argument surface.** List every required and optional
   parameter. Classify each as enumerable (can be discovered) or free-form (must
   be typed). Decide which need prompts.

2. **Add the opt-in flag.** Introduce a boolean interactive switch, aliased to
   `-i`. Keep it mutually exclusive with the identification arguments where the
   parameter system supports sets. Do not make existing required parameters
   mandatory in a way that blocks the flag from being reached.

3. **Build the wizard.** For each parameter, in dependency order:
   - Discover candidate values from the environment.
   - Render a numbered menu (or typed prompt when unavoidable).
   - Validate the selection inside a loop; never trust a single read.
   - Assign the resolved value to the parameter the core path already reads.

4. **Print a confirmation summary** and gate the run behind a yes/no.

5. **Wire the task runner** (if a Taskfile or wrapper invokes the script). Add a
   pass-through variable and forward the flag conditionally. Ensure the runner
   does not force a non-interactive shell mode that would break prompting.

6. **Test both paths.** Verify the non-interactive path is byte-for-byte
   unchanged, and exercise the wizard's cancellation and confirmation gates.

## Testing Checklist

- Non-interactive invocation with full args behaves exactly as before.
- Invocation with missing required args and no flag fails fast (no prompt).
- Wizard: every menu renders the discovered options; invalid input re-prompts.
- Wizard: quitting at each prompt exits 0 with no side effects.
- Wizard: declining the confirmation exits 0 with no side effects.
- Wizard: empty option sets produce a clear error, not an empty menu.

## Anti-Patterns

| Anti-pattern | Why it fails |
|---|---|
| Auto-entering interactive mode when args are missing | Hangs agents and CI on an unanswerable prompt |
| Free-text prompts for values that can be enumerated | Typos reach the operation; users guess valid inputs |
| Changing the non-interactive path's behavior | Breaks automation and scripted callers |
| Prompting without a final confirmation | A wrong menu pick executes an irreversible operation |
| Assuming a single discovered value is an array/collection | Single-result collections break count/size checks |
| Exiting non-zero on a user-initiated cancel | Cancel is a valid outcome, not an error |

## Language References

- **PowerShell / Taskfile:**
  [references/powershell-pattern.md](references/powershell-pattern.md) — ready-to-adapt
  helper functions for numbered menus, yes/no selection, confirmation summaries,
  array-safe discovery, the `-Interactive` parameter block, and Taskfile wiring.

Add a sibling reference file (for example `references/python-pattern.md`) when
another language's implementation is needed; keep this guide as the single home
for the principles above.
