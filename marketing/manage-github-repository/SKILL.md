---
name: manage-github-repository
description: Audit, rename, and polish a GitHub repository across its local checkout and remote settings. Use when Codex needs to synchronize a local and GitHub repository name, set the description, homepage URL, or topics, create repository branding and a GitHub social preview, restructure a README, or prepare and publish a cohesive repository identity. Uses GitHub CLI for supported remote operations and delegates visual identity work to $create-context-aware-logos.
---

# Manage GitHub Repository

Treat the repository name, remote metadata, visual identity, and README as one release. Use GitHub
CLI for supported repository mutations and `$create-context-aware-logos` for visual assets.

## Workflow

1. Inspect the repository before proposing changes:
   - read the primary README, manifest files, license, repository layout, Git status, remotes, and
     recent commits;
   - run `gh --version` and `gh auth status`;
   - determine the repository's audience, actual capabilities, package or product name, and current
     public URL;
   - preserve unrelated working-tree changes.
2. Draft one explicit change set containing:
   - current and proposed `OWNER/REPOSITORY`;
   - local checkout path after rename;
   - description of at most 350 characters;
   - homepage URL, or an explicit decision to leave it unset;
   - a focused topic list using lowercase hyphenated terms;
   - planned logo, lockup, social preview, and README changes.
3. Show the plan and obtain confirmation before any remote mutation, push, or local directory rename.
   Treat confirmation for the requested change set as authorization for those exact operations only.
4. Read [references/github-surfaces.md](references/github-surfaces.md) before producing assets or
   editing repository settings.
5. Invoke `$create-context-aware-logos` with the repository context. Require the GitHub repository
   deliverables from that skill, including `social-preview.png` at 1280 x 640 and under 1 MB.
6. Update the README around real user needs:
   - place the lockup or mark near the title with useful alt text;
   - state what the project does before installation details;
   - include the shortest verified install or usage path;
   - document prerequisites and limitations without invented claims;
   - keep badges restrained and link every badge to a meaningful destination;
   - preserve useful existing content and maintain translated READMEs together.
7. Run the deterministic metadata helper in preview mode, inspect its plan, then rerun with `--apply`:

```powershell
python scripts/manage_repository.py `
  --repo-path <checkout> `
  --name <new-name> `
  --description "<description>" `
  --homepage "<url>" `
  --topic <topic> --topic <topic> `
  --rename-local
```

8. Verify the local and remote result:
   - `git status --short --branch`;
   - `git remote get-url origin`;
   - `gh repo view OWNER/NEW-NAME --json nameWithOwner,description,homepageUrl,repositoryTopics,url`;
   - asset dimensions, file size, SVG rendering, and README links;
   - the repository page and social preview through a browser when browser automation is available.
9. Commit only intended files and push normally. Never force-push merely because the repository was
   renamed. Report any remaining manual step, especially social-preview upload.

## GitHub CLI

Use `gh` as the MVP dependency because it provides authenticated, supported commands for repository
metadata and rename operations. If `gh` is missing, pause before mutation and install it with the
platform's official package path only after approval. If authentication is missing, ask the user to
complete `gh auth login`; do not request or print a token.

The helper is safe by default: without `--apply` it only prints the planned commands. It updates
metadata first, renames the remote repository second, updates the local `origin` URL third, and
attempts the local checkout rename last. If the operating system holds the checkout directory open,
leave the completed remote changes intact and rename the directory from its parent in a fresh shell.

For external GitHub commands, use `$private-github-proxy` when that skill is available in the current
environment. Do not persist proxy configuration.

## Boundaries

- Do not change visibility, transfer ownership, rewrite history, delete topics, or alter branch
  protection unless the user separately requests it.
- Do not claim GitHub has a repository-logo field. The README logo and social preview are separate
  surfaces.
- Do not use undocumented API endpoints to upload the social preview. Upload it through the
  repository's Settings page with browser automation, or give the user that one manual step.
- Do not rename package identifiers, import paths, deployment targets, or external integrations just
  because the repository changes name. Audit and propose those as separate compatibility changes.
- Do not commit generated concepts, temporary renders, secrets, credentials, or local configuration.
