---
name: finalize-commit
description: Once we are confident our recent changes have captured the essence of the change we want to commit, finalize the commit.
---

# Finalize commit

## Instructions
Ideally, git commits represent atomic changesets that are high-quality enough
to share with other developers. Commits in local development can be messy and
temporary, but commits that are shared by pushing to remotes, submitting pull
requests, etc, should each be high-quality, i.e.:

- Linters (eslint etc) are all passing
- Automated tests are passing and have been augmented to represent recent
  changes

To finalize a commit:

1. Make sure code passes linters

Run all linters and clean up issues you see. Refactor code if necessary.

You should almost never modify linting configs to make linting less strict. If
you believe you have found an exception where it makes sense to modify the
linting config, ask the user what they think.

You should almost never fix problems by ignoring lines in source code (i.e.
`eslint-disable-next-line`) or by ignoring files by name.  If you believe you
have found an exception where it makes sense to ignore lines or files, ask the
user what they think.

Although you may refactor and change the interfaces of classes, functions,
methods, etc, do not change the behavior of the overall system.

2. Make sure automated testing is high-quality

All pre-exising automated tests should pass, unless the intention of the commit
directly changes the behavior described in the specific test.

If you have added any new source files, make sure that those new files each
have their own automated test file as well.

You do not need to be exhaustive in your testing. 100% code coverage is not the
goal. Instead we are aiming for a light scaffolding that helps us prevent
regressions in simple cases.

### About "WIP" commits

"WIP" stands for "Work In Progress": Developers may make local WIP commits that
they intend to squash and cleanup later. If the current branch ends with a
number of commits that all contain "WIP" or "wip" in the commit message, assume
all of those commits are included in the relevant changes to be cleaned up.

Don't squash commits on your own; assume the user will take care of that for you.

### Proof of concept or spike branches

Some branches are "proof of concept" or "spike" branches -- fast, sloppy
development meant to prove out a concept. If you see terms like this in branch
names or commit messages, it's possible that we don't want to invoke this skill
at all. Ask the user if you're uncertain.
