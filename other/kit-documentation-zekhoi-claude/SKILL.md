---
name: kit-documentation
description: Write or update project documentation such as READMEs, setup and usage guides, and API references so it matches what the code actually does, with every command and example verified. Use when the user asks to write, update, or fix documentation, a README, or usage instructions. Do not use for code comments during feature work, changelogs for releases, or explaining code to the user in chat.
---

# Documentation

Documentation that disagrees with the code is worse than none. Write only what you have verified.

## 1. Find the source of truth

- Read the code, configuration, and scripts the documentation describes: entry points, CLI arguments, environment variables, public APIs, and build and test commands.
- Read the existing documentation and note what is missing, outdated, or contradicted by the code.
- Identify the audience (users, contributors, operators) and keep the existing structure and tone unless asked to change them.

## 2. Write

- Lead with what the reader needs first: what it is, how to install or set it up, and how to use it.
- Show real, copyable commands and examples taken from the project. Never invent flags, options, endpoints, or output.
- Explain prerequisites and supported versions as the project defines them.
- Keep it concise. Link to existing documents instead of duplicating them.

## 3. Verify

- Run every command you document where it is safe to do so, and check examples against the code. Do not run commands that deploy, publish, send messages, or modify shared systems.
- Mark anything you could not verify, and tell the user, rather than presenting it as fact.
- Check that relative links and referenced files exist.

## 4. Report

Summarize what was added or changed, what was verified and how, and anything left unverified or needing the maintainer's input.

## Examples

- Use: "Write a README for this project." "The setup docs are out of date; fix them."
- Skip: "Write release notes for 2.0." "Explain how this function works." (answer in chat)
