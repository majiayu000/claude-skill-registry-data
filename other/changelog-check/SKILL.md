---
name: changelog-check
description: >
  Checks whether a branch owes the changelog an entry, and drafts the entry when it
  does. Reads the diff against the merge base, decides whether the change alters
  behavior that a user can observe, and compares that against the changelog lines the
  branch adds. Use when the user asks whether a branch or a merge request needs a
  changelog entry, asks why the changelog check failed, or asks to write the entry for
  a branch. Do not use it to assemble the release notes for a whole version, because
  that reads the range between two tags rather than one branch.
argument-hint: "[branch or merge request, defaults to the current branch]"
allowed-tools: [Read, Glob, Grep, Bash]
---

# Changelog Check

Decide whether a branch owes the changelog an entry, and draft that entry when it does.

## Read the change

Take the branch from `$ARGUMENTS`, and default to the current branch.

Read the diff against the merge base, and read the changelog file that the repository keeps.

## Decide whether the change is user-visible

A change is user-visible when a user can observe it without reading the source. That covers a new endpoint, a changed default, a renamed field in a response, a fix for a bug that a user reported, and any break in a public contract.

A change is not user-visible when it only moves code, renames a private symbol, edits a test, or bumps a development dependency.

When one branch carries both kinds, treat the branch as user-visible.

## Report

State the verdict in one line: the branch needs an entry, or it does not.

When it needs one, quote the entry you propose, in the format that the existing entries use, and name the section it belongs under.

When the branch already carries an entry, say whether that entry matches what the diff does. An entry that names a different behavior than the diff misleads a reader more than a missing entry does.

You are done when the report states the verdict, and either quotes a proposed entry or names the existing entry that covers the change.
