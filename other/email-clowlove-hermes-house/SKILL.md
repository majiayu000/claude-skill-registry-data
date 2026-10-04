---
name: email
description: Skills for sending, receiving, searching, and managing email from the terminal.
version: 1.0.0
metadata:
  hermes:
    tags: [email]
    related_skills: ['mails', 'himalaya']
---

# Email

## Overview

Skills for sending, receiving, searching, and managing email from the terminal.

## Mails.dev Email CLI

For Mails.dev email infrastructure for AI agents — send/receive emails via `imclaw@mails.dev`, inbox checking, HTML email, and confirmation code verification — see `references/mails-cli.md`. Requires `bun` runtime.

## Sub-skills

- **himalaya**: Himalaya CLI: IMAP/SMTP email from terminal

## Usage

Load individual skills from this category using:
```
skill_view(name="email/{sub_skill}")
```
