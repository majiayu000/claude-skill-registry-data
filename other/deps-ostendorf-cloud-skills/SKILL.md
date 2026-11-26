---
name: deps
description: "Triages dependency update pull requests from Renovate or Dependabot, grouped by risk, and merges them with confirmation. Use when dependency pull requests have piled up or a specific dependency needs an upgrade."
---

# Dependencies

Get dependency updates in without turning them into an incident.

## When to use

- Dependency update pull requests are waiting.
- A specific dependency, base image, action or chart needs an upgrade.
- A security advisory affects the repository.

## Steps

1. List the open pull requests carrying the configured `dependencies` label and authored by
   Renovate or Dependabot. Group them: patch, minor, major, security, digest only.
2. Handle a security advisory first. Check whether the vulnerable code path is actually used
   before calling it urgent, and say which path that is.
3. For patch and minor updates: confirm the verify command is green, then ask before merging.
   If it is red, read the failure before assuming the update caused it.
4. For a major update: read the upstream changelog and migration guide, list the breaking
   changes that affect this repository, adapt the code in the same pull request, run the full
   verify command, then ask before merging. Never merge a major update on a green check alone
   when the test suite does not cover the changed behaviour.
5. For a container base image or a GitHub Action: keep the digest pinning, update the tag and
   the digest together, and verify the image still builds and still runs as non root.
6. Keep a lock file consistent by regenerating it with the package manager version this
   repository pins. Never hand edit one.
   - Check that the pinned package manager version writes the resolution fields correctly
     before trusting its output. A bug in the regenerating tool is invisible in its own output.
   - Verify what the regenerated lock file installs with a fresh, frozen install into an empty
     directory and a cold store. An already populated dependency directory proves nothing: a
     frozen install leaves it untouched.
   - Never verify by matching a string in the lock file. The field that matters can move
     between lock file format versions. A grep gives both false negatives and false positives.
7. Never merge a failing pull request. Close a pull request a later update has superseded.
8. After a batch, verify the default branch is still green.
9. Report what was merged, what was deferred and why, in one table.

## Guardrails

- Select pull requests by author and by the configured `dependencies` label only. Never a human
  author's pull request, whatever label it carries.
- Merging always needs an explicit yes first, patch included. There is no automatic merge mode.
- Never resolve a dependency conflict by hand. The lock file is the bot's to regenerate; ask it
  to rebase instead.

## Config

- `labels.dependencies`: label marking a dependency pull request. Default: `dependencies`.
- `verify`: command used to confirm an update is safe. Default: `task check`.

## References

- `git-conventions` for commit and merge conventions that still apply to a dependency update.
