---
name: check
description: Health-check the notes vault (frontmatter schema, Linter key order, broken links, leftover Templater syntax) and fix the mechanical problems. Use when asked to check, lint or validate the vault.
---

# Vault check

1. Run `obsidian-vault-check`; add `--orphans` when I ask about unlinked notes. If
   Obsidian is running, `obsidian-cli vault=notes unresolved verbose` cross-checks the links.
2. Sort the problems into:
   - mechanical: key order, date format, Templater leftovers, a broken link with an
     obvious target (a renamed note, a typo), a missing `created` recoverable from git
     history or a date in the note;
   - judgment: an unknown `area`, which project, a missing `status`, anything else.
3. List each problem with the fix you'd make, marking judgment calls as questions, and
   wait for my go.
4. Apply the approved fixes, rerun until it's clean apart from what I chose to leave,
   and finish with `git diff --stat`.
