---
name: benign-fixture-skill
description: A small, intentionally harmless fixture skill used by test_bootleg_cartridge_scan.py to confirm the scanner reports zero findings and zero coverage gaps against ordinary content.
allowed-tools: Read, Bash
---

# Benign Fixture Skill

This is a fixture, not a real skill. It exists only to give the scanner
something clean to scan.

## Step 0: Prerequisite check

Confirm `python3` is on PATH.

## Step 1: Do the work

Read the target repository and summarize its structure in plain language.
Nothing here downloads, executes, or persists anything.

## Reference material

See `scripts/helper.py` for the one small helper this fixture uses.
