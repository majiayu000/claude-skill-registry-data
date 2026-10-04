---
name: spark-check-before-push
description: Launch some action before create push in git
---

# Add Repository Skill

## Overview & Prerequisites

This skill verify and launch some actions before push in git only for the *created/updated* files.

## Steps

- [ ] Check if there is not TODO anymore. If no, display the list of the results.
- [ ] Check if all **public** code are documented. If no, display the list of the results.
- [ ] Check if there is no commented code (except for the documentation). If no, display the list of the result.
- [ ] Copyright line must be present and includes current year
- [ ] No empty lines contain whitespace or tabs
- [ ] All class members accessed with `self.`
- [ ] Launch the ```$ swiftlint``` and if necessary ```$ swiftlint --fix``` command line
- [ ] Check Package.swift use remote URL instead of local path