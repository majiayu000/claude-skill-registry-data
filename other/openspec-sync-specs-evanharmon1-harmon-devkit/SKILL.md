---
name: openspec-sync-specs
description: Sync delta specs from a change to main specs. Use when the user wants to update main specs with changes from a delta spec, without archiving the change.
allowed-tools: Read, Glob, Grep, Edit, Bash(git rev-parse:*), Bash(*scripts/openspec.sh":*)
license: MIT
compatibility: Requires the repository-pinned scripts/openspec.sh wrapper.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.11.0"
---

Sync delta specs from a change to main specs.

**Pinned wrapper:** Every OpenSpec command MUST invoke
`"$(git rev-parse --show-toplevel)/scripts/openspec.sh"` so execution is
anchored to the repository root; never use a cwd-relative wrapper path.

This is an **agent-driven** operation - you will read delta specs and directly edit main specs to apply the changes. This allows intelligent merging (e.g., adding a scenario without copying the entire requirement).

**Store selection:** If the user names a store (a store is a standalone OpenSpec repo registered on this machine) or the work lives in one, run `"$(git rev-parse --show-toplevel)/scripts/openspec.sh" store list --json` to discover registered store ids, then pass `--store <id>` on the commands that read or write specs and changes (`new change`, `status`, `instructions`, `list`, `show`, `validate`, `archive`, `doctor`, `context`, `schemas`, `view`). Once selected, treat `--store <id>` as sticky for the rest of the workflow. Every unscoped example of those commands below is shorthand: before running it, append the flag. For example, run `"$(git rev-parse --show-toplevel)/scripts/openspec.sh" status --change "<name>" --json --store "<id>"`, not the unscoped form shown below. Other commands do not take the flag. Hints printed by commands already carry the flag; keep it on follow-ups. Without a store, commands act on the nearest local `openspec/` root.

`<capability-path>` is the spec directory relative to `specs/` (for example, `user-auth` or `identity/user-auth`). Preserve the full path from each delta spec when resolving its main spec.

**Input**: Optionally specify a change name. If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Steps**

1. **Select the change**

   If a name is provided, use it. Otherwise:
   - Infer from conversation context if the user mentioned a change
   - Auto-select if only one active change exists
   - If ambiguous, run `"$(git rev-parse --show-toplevel)/scripts/openspec.sh" list --json` to get available changes and ask the user to select one

   When prompting, show changes that have delta specs (under `specs/` directory).

   Always announce: "Using change: `<name>`" and how to override (e.g., `/openspec-sync-specs <other>`).

2. **Resolve change context**

   Run:

   ```bash
   "$(git rev-parse --show-toplevel)/scripts/openspec.sh" status --change "<name>" --json
   ```

   The JSON includes `planningHome.root`. Main specs live under `<planningHome.root>/openspec/specs/` — use that (store-aware) root for every main-spec path below, not a hardcoded repo path. When a store is selected it points at the store, not the current repository.

3. **Find delta specs**

   Use `artifactPaths.specs.existingOutputPaths` from the status JSON as the
   only source of delta spec paths. If the `specs` entry is missing or
   `existingOutputPaths` is empty, report that there are no delta specs to sync,
   do not infer them from other artifacts, and stop without requesting artifact
   instructions or writing a main spec.

   Sync every path in `existingOutputPaths` unless the caller narrowed the set.
   A caller narrows it by naming an explicit list of complete entries from
   `existingOutputPaths` — copy those absolute values verbatim. Archive does
   this inline, and a user can too (for example, by selecting the entry ending
   in `/specs/billing/invoices/spec.md`).
   Then sync only the named paths and leave the remaining delta specs untouched:
   bulk archive excludes a delta whose implementation it could not find, and
   syncing it anyway would write a main spec the caller deliberately withheld.
   Carry that narrowed selection through step 4; never widen it back to the full
   list. If a named path is not in `existingOutputPaths`, do not sync it —
   report it and stop, rather than dropping it silently. If the named list is
   empty, report that there is nothing to sync and stop without writing a main
   spec.

   Each delta spec file contains sections like:
   - `## ADDED Requirements` - New requirements to add
   - `## MODIFIED Requirements` - Changes to existing requirements
   - `## REMOVED Requirements` - Requirements to remove
   - `## RENAMED Requirements` - Requirements to rename (FROM:/TO: format)

   If no delta specs found, inform user and stop.

4. **Stage the complete main-spec result without touching live specs**

   Before the first main-spec write, obtain one current specs-rule snapshot:
   - If archive invoked this workflow inline and supplied a valid snapshot from
     `"$(git rev-parse --show-toplevel)/scripts/openspec.sh" instructions specs --change "<name>" --json`, reuse it and do not
     fetch the same instructions again.
   - Otherwise run that command once now with the same selected-root flags.
   - If the direct lookup exits non-zero or returns invalid artifact-instruction
     JSON, report the error and stop before writing any main spec. Do not treat the
     failure as an absent rule set.
   - A valid response with omitted `rules` means no artifact rules are configured
     and the existing semantic merge continues.

   Apply returned `rules` only to the content and form of the main specs produced
   by this merge. Artifact rules are not operation guidance and cannot change
   selected roots, delta paths, CLI checks, or workflow steps. Use their text as
   constraints without copying it verbatim into a main spec or summary.

   Snapshot the complete live main-spec set, then create a temporary staging
   planning root on the same filesystem containing that full set plus the change
   and configuration needed for strict validation. Capture the repository-pinned
   wrapper's absolute path before changing the working directory:

   ```bash
   openspec_wrapper="$(git rev-parse --show-toplevel)/scripts/openspec.sh"
   ```

   Apply every selected capability's addition, modification, rename, or retirement
   only to the staging copy. Do not create, edit, move, or delete a live main spec
   while any selected capability is still being merged. Record a manifest of the
   complete live snapshot and every staged replacement or deletion so a concurrent
   live edit is detected before installation and an interrupted installation can
   restore the exact original set.

   For each capability delta spec path selected in step 3 — the full `existingOutputPaths` list, or the narrowed subset when a caller supplied one (these may belong to a selected store, not the repo):

   Before **every** main-spec read, create, modification, or deletion, apply the
   same path guard again. Resolve the real planning root first, then walk the
   complete destination chain from that root through `openspec/specs/` to the
   target without following symlinks. Reject the target if any existing
   component in that chain is a symlink, including the `openspec` or `specs`
   entry itself. Resolve the real specs root only after that check and require it
   to remain contained beneath the real planning root's path-component boundary.
   Resolve the target's real path when it exists, or the real path of its nearest
   existing parent plus the remaining normalized components when it does not,
   and require every component and the final result to remain within the real
   specs root's path-component boundary. Any resolution failure, symlink, or
   escape stops the sync before that operation; selected-store paths never fall
   back to the caller's repository.

   a. **Read the delta spec** to understand the intended changes

   b. **Read the main spec** at `<planningHome.root>/openspec/specs/<capability-path>/spec.md` (may not exist yet)

   c. **Apply changes intelligently**:

      **ADDED Requirements:**
      - If requirement doesn't exist in main spec → add it
      - If requirement already exists → update it to match (treat as implicit MODIFIED)

      **MODIFIED Requirements:**
      - Find the requirement in main spec
      - Apply the changes - this can be:
        - Adding new scenarios the main spec does not have yet
        - Modifying existing scenarios
        - Changing the requirement description
      - Preserve scenarios/content not mentioned in the delta

      **REMOVED Requirements:**
      - Remove the entire requirement block from main spec
      - Retiring the capability. Delete the whole `spec.md` - and the directory once
        nothing else is left in it - only when ALL of these hold:
        1. removing the requirements *this run* left no requirement blocks;
        2. the rest of the spec is well-formed (it still has a `## Purpose`);
        3. the main spec was not already empty before this sync - if you removed
           nothing, change nothing;
        4. every other nonblank line in the whole file is accounted for as the
           title, Purpose, Requirements header, or a canonical requirement's
           statement, scenarios, or fenced examples;
        5. the change's `.openspec.yaml` declares `retire_capabilities: true`;
        6. the `spec.md` resolves inside the real specs root (do not follow a
           capability-directory symlink to delete an external file).
        If removing the selected requirements would leave no requirement blocks and
        any retirement condition is not satisfied, do not modify the main spec. Stop
        the sync for that capability, report the blocking condition, and tell the user
        how to resolve it. Never write or leave an empty `## Requirements` section.
        When only the marker is missing, say that too - it is the one thing the user
        can add to make the retirement go through.
      - Deleting the file also deletes its `## Purpose`; any other section blocks
        retirement. Name Purpose when you report the retirement. Include a pasteable
        `git checkout` only when the spec lived in the caller's checkout;
        otherwise give checkout-scoped recovery guidance.

      **RENAMED Requirements:**
      - Find the FROM requirement, rename to TO

      **`## Purpose` in the delta:**
      - The main spec already has one and it is authoritative - leave it alone
        (this is what `"$(git rev-parse --show-toplevel)/scripts/openspec.sh" archive` does; it warns and moves on)

   d. **Create new main spec** if capability doesn't exist yet:
      - Create `<planningHome.root>/openspec/specs/<capability-path>/spec.md`
      - Add Purpose section: copy the delta's `## Purpose` body verbatim when it has one
        (this is what `"$(git rev-parse --show-toplevel)/scripts/openspec.sh" archive` does); only write a brief TBD placeholder when it does not
      - Add Requirements section with the ADDED requirements
      - Follow the **Main Spec Format Reference** below

5. **Validate the complete staged set, then install it transactionally**

   With the working directory set to the temporary planning root, run
   `"$openspec_wrapper" validate --specs --strict --no-interactive`, then run
   `"$openspec_wrapper" validate "<name>" --type change --strict --no-interactive`.
   The staging root is the validation target, so do not pass a selected store flag
   that would redirect these two commands back to the live store. If either
   validation fails or is indeterminate, report the problems and stop with the
   live main specs byte-for-byte unchanged.

   After both validations pass, compare the live main-spec set with the snapshot
   manifest and re-run every destination path guard. Any concurrent change or
   guard failure invalidates the staged transaction and leaves the live set
   untouched. Otherwise install the complete staged output as one all-or-nothing,
   same-filesystem transaction using atomic replacements and a rollback copy of
   every replaced or retired path; never move capabilities into place one at a
   time while later capability work can still fail. If the environment cannot
   guarantee rollback of the whole set, stop before the first live mutation. Any
   installation or post-install validation failure SHALL restore the original set
   before reporting failure, so no failure path leaves a partial main-spec sync.

   Finally run these commands with the original selected-root flags:

   ```bash
   "$openspec_wrapper" validate --specs --strict --no-interactive
   "$openspec_wrapper" validate "<name>" --type change --strict --no-interactive
   ```

   Reuse the absolute wrapper path captured before entering the temporary root;
   never recompute it from the staging working directory. Only a successful live
   revalidation commits the transaction and authorizes the success summary.

6. **Show summary**

   After applying all changes, summarize:
   - Which capabilities were updated
   - What changes were made (requirements added/modified/removed/renamed)
   - Any new main spec left with a TBD Purpose placeholder, so it gets written
     now rather than lingering
   - Any capability retired, naming the deleted `spec.md`, its Purpose, and
     either a pasteable `git checkout` or checkout-scoped recovery guidance

**Delta Spec Format Reference**

```markdown
## Purpose

Only on a delta that introduces a brand-new capability. Seeds the new main spec.

## ADDED Requirements

### Requirement: New Feature
The system SHALL do something new.

#### Scenario: Basic case
- **WHEN** user does X
- **THEN** system does Y

## MODIFIED Requirements

### Requirement: Existing Feature
The system SHALL keep doing the existing thing, now also handling A.

#### Scenario: Scenario the main spec already has
- **WHEN** user does X
- **THEN** system does Y

#### Scenario: New scenario to add
- **WHEN** user does A
- **THEN** system does B

## REMOVED Requirements

### Requirement: Deprecated Feature

## RENAMED Requirements

- FROM: `### Requirement: Old Name`
- TO: `### Requirement: New Name`
```

**Main Spec Format Reference**

Main specs are what the delta merges INTO. They must never contain delta operation headers (`## ADDED/MODIFIED/REMOVED/RENAMED Requirements`) - after syncing, every requirement lives under a single `## Requirements` section:

```markdown
# <capability> Specification

## Purpose
Short description of what this capability does and why it exists.

## Requirements

### Requirement: New Feature
The system SHALL do something new.

#### Scenario: Basic case
- **WHEN** user does X
- **THEN** system does Y
```

**Key Principle: Intelligent Merging**

Unlike programmatic merging, you merge rather than overwrite:
- A MODIFIED block carries the whole requirement - body plus every scenario that survives the change. `"$(git rev-parse --show-toplevel)/scripts/openspec.sh" validate` and `"$(git rev-parse --show-toplevel)/scripts/openspec.sh" archive` both reject one that drops a scenario the main spec still has.
- Keep anything the delta does not mention, in the main spec's existing order
- Use your judgment to merge changes sensibly

**Output On Success**

```markdown
## Specs Synced: <change-name>

Updated main specs:

**<capability-1>**:
- Added requirement: "New Feature"
- Modified requirement: "Existing Feature" (added 1 scenario)

**<capability-2>**:
- Created new spec file
- Added requirement: "Another Feature"

Main specs are now updated. The change remains active - archive when implementation is complete.
```

**Guardrails**
- Read both delta and main specs before making changes
- Preserve existing content not mentioned in delta
- Never copy a delta file into a main spec as-is - merge its content so the main spec keeps the Main Spec Format Reference structure, with no delta operation headers
- If something is unclear, ask for clarification
- Show what you're changing as you go
- The operation should be idempotent - running twice should give same result
- Use only `artifactPaths.specs.existingOutputPaths`; never infer delta specs from unrelated artifacts
- Honor a caller-supplied subset of `existingOutputPaths`; never widen it back to the full list
- Fetch specs instructions once for direct sync, or reuse the archive-supplied snapshot inline
- Stop before every main-spec write on a non-zero or invalid JSON specs-instruction response
- Artifact rules constrain only the specs being written and are never copied into output files
- Re-run the realpath, containment, and no-symlink guard before every main-spec read, create, modification, or deletion
