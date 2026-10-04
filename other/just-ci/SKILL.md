---
name: just-ci
description: "`just ci` final check must pass before execution is complete. Use this skill when finishing work in a repository that has a `just ci` recipe."
user-invocable: true
---
# `just ci` Must Pass

`just ci` final check must pass before execution is complete.
Where the project uses `make` rather than `just`, the equivalent full-check target applies instead; discover it with `just --list` or `make help` rather than guessing.

Suppressing linters or modifying configs or the justfiles is NOT ALLOWED.
Reverting uncommitted changes is NOT ALLOWED.
Fix identified issues regardless of change source.
