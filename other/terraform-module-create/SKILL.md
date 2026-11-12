---
name: terraform-module-create
description: Work in progress, not usable yet. Will create a new module repository from a module profile. Use terraform-module-maintainer today.
---

# Terraform Module Create

## Status

Work in progress. This skill does nothing yet: refuse the request, read and write nothing, and use terraform-module-maintainer instead.

## Use cases

- "create a module for service Y", for a module family that has a profile, such as terraform-aws-modules.
- A new in-house module that follows a custom profile.

## Responsibilities

- It will set up a new repository directory with the files and templates the profile lists.
- It will hand the module code to the Full create mode of terraform-module-maintainer, with its coverage ledger from the provider schema.
- It will have terraform-module-reviewer review the whole module before it hands the module back, and will fix or report what the review finds.
- It will create a remote repository, or push to one, only after a new message from the user confirms it.

## Non-goals

- No terraform apply and no state.
- No release, tag or registry publication.
- No module rules of its own. They stay in the profile and in terraform-module-maintainer.

## Open questions

- Whether it creates the remote repository, or only a local tree that the user pushes.
- Which credentials the trusted run and the plan of a new module need, and how the user names them.
- How it derives the repository name and the module name from the request.
