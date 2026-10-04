---
description: Show all active projects across all Metapowers domains
---

# Status

Scan the `.metapowers/` directory and show the status of all active projects across all domains.

## Prerequisites

None — utility skill, run anytime.

## Process

1. **Read the domain registry:**
   - Read `plugins/metapowers/shared/domain-registry.md` for the list of all domains and their artifact patterns

2. **Scan `.metapowers/` directory:**
   - List all subdirectories under `.metapowers/`
   - For each domain directory found, list all project subdirectories
   - For each project, list all artifact files present

3. **Determine project status:**
   - Count total phases in the domain's methodology
   - Count completed phases (numbered artifact files present)
   - Determine status: Not Started, In Progress (X/Y phases), Complete
   - Note the last modified date of the most recent artifact

4. **Check for cross-domain connections:**
   - Does a branding project exist? (other domains may reference it)
   - Are there coaching reviews for any projects?
   - Any accessibility audits completed?

5. **Present the status directly to the user** in a table format:

   ```
   Domain              Project              Status         Last Updated
   ──────              ───────              ──────         ────────────
   design              button               3/5 phases     2026-04-23
   research            onboarding           Complete       2026-04-22
   branding            acme                 5/5 phases     2026-04-23
   development         auth-system          1/4 phases     2026-04-24
   coaching            login-form           2 reviews      2026-04-23
   accessibility       checkout-flow        Not Started    —
   ```

6. **Highlight attention items:**
   - Projects that are in progress but stale (last update > 7 days ago)
   - Domains with no projects started
   - Cross-domain gaps (e.g., branding exists but no brand audit run yet)

## Output

Present the status directly to the user. No artifact file created — this is a real-time status check.
