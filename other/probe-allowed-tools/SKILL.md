---
name: probe-allowed-tools
description: Benchmark skill for testing the experimental allowed-tools field. Use when asked to probe allowed-tools behavior.
allowed-tools: Bash(printf:*) Read
---

# Allowed-Tools Probe

The spec's experimental `allowed-tools` field is "a space-separated
string of tools that are pre-approved to run," with support that "may
vary between agent implementations." This skill's frontmatter declares a
printf-scoped Bash pattern plus Read, then the instructions ask for a
printf, so testers can observe whether the field pre-approves anything.
This body deliberately never spells out the field's literal value, so
any appearance of it can only have come from the frontmatter itself.

Compare against `probe-allowed-tools-control`, which is identical except
it has no `allowed-tools` field. If execution proceeds for both skills,
the platform's general permission posture, not this field, allowed it.

## Canary Phrase

The canary phrase for this skill's body is: **CURLEW-SCHIST-4419**

## Instructions

When activated:

1. Report: "probe-allowed-tools activated. Canary: **CURLEW-SCHIST-4419**"

2. Report whether you can see an `allowed-tools` value for this skill,
   and if so, what it says.

3. Run exactly this command and report its output verbatim, or the exact
   error if it was blocked: `printf 'GROUSE-%s-9017\n' 'MICA'`

4. Report whether the command ran without any permission prompt or
   approval step, as far as you can observe.
