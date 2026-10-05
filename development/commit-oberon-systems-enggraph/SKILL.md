---
name: commit
description: Make a git commit in this repository by driving the real commitizen binary under a pty. Use whenever a commit is asked for, before staging or writing any commit message.
---

# /commit

Every commit is made by the real binary - `.venv/bin/cz commit` where the
project carries a virtualenv, otherwise whatever `cz` it provides. There is no
`git cz` alias on this machine. Never `git commit -m`, never a message rendered
by hand to look like commitizen output, and never a reflow of what it emitted,
whitespace included. No `Co-Authored-By` trailer. Work happens directly on
`main`; a temporary branch is merged and deleted at once.

## Pick the adapter first

Read `.cz.yaml` before anything else: its `name:` key names the adapter, and
that adapter has to be installed for `cz` to start at all - a configured but
missing one fails with "The commiter has not been found in the system". One
`pip install` of it is worth trying, and
`cz --name cz_conventional_commits commit` is the way through if that fails.

## With `wyld_cz` (`name: wyld_cz`)

Five questions, in this order:

1. `Select the type of change:` - a list in the order `fix`, `feat`, `build`,
   `docs`, `refactor`; move down it with `\x1b[B`.
2. `What is the scope of this change (e.g. package, tools):` - the one module,
   script or document the commit is about.
3. `Write a short description:` - the subject line.
4. `Provide a longer description (optional):` - a single-line input, so the body
   is one paragraph; the adapter wraps and indents it.
5. `Link to issue (optional):` - normally empty.

The result is `[<type>][<scope>]: <subject>`, which `cz check` and the
commit-msg hook both enforce.

## Without it

No `.cz.yaml`, or one naming an adapter this machine does not have, and
commitizen uses its own `cz_conventional_commits`: a longer type list, then
scope, subject, body and footer, giving `<type>(<scope>): <subject>`. Drive that
form as it comes and do not fake the bracketed shape on top of it; the
repository's commit-msg hook is the authority on what is valid there.

## Driving it

It is interactive and needs a TTY, so run it under `pty.fork`: strip ANSI from
the accumulated output, wait for the prompt substring, sleep ~0.5 s, write the
answer plus `\r`, and clear the match buffer after each step.

`git reset --soft HEAD~1` leaves the files staged when the last commit has to be
made again with a corrected message.
