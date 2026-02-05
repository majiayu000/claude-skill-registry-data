---
name: verify_setup
description: Verify that the Visions Skills architecture is functioning correctly.
usage_trigger: Use when the user asks to "verify skills", "check system status", or "debug architecture".
---

# 🕵️ Verify Setup Skill

## 1. Core Verification

If you are reading this, the **Level 2 (Activation)** phase of the Progressive Disclosure architecture is SUCCESSFUL.

## 2. Instructions

To complete the verification:

1. **Confirm Activation**: State clearly that you have successfully loaded the `verify_setup` skill.
2. **Filesystem Check**:
    * This file is located at `visions/skills/verify_setup/SKILL.md`.
    * Verify you can read other files in this directory if they existed.
3. **Protocol Check**:
    * Explain effectively: "I scanned the registry, found the metadata in my system prompt, and called `activate_skill('verify_setup')` to retrieve these instructions."

## 3. Python Verification (Level 3)

If you need to verify Level 3 capability (Code Execution):

1. Create a python script named `test_env.py` in this directory that prints "Level 3 Active".
2. Execute it using your `run_command` or standard execution tool.
