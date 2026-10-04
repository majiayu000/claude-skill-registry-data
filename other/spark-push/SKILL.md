---
name: spark-push
description: Launch some action to push the code in git
---

# Add Repository Skill

## Overview & Prerequisites

This skill verify and launch some actions before push in git.

## Prerequisite

1. *If the current branch is "main" or "master", ask to create a new branch !*
2. Do not mention *Claude*.

## Steps
- [ ] Use the [conventionalcommits](https://www.conventionalcommits.org/en/v1.0.0/) to create the *commit summary*.
- [ ] Add a description from the current updated files.
- [ ] Ask if the texts are OK.
- [ ] If yes, push the code.