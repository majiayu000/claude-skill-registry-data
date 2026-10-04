---
name: probe-linked-resources
description: Benchmark skill for testing eager link resolution and path resolution behavior. Use when asked to probe link resolution.
---

# Linked Resources Probe

This skill tests whether the platform pre-fetches files that are linked in the
SKILL.md body, and how it resolves relative paths.

## Instructions

When activated, do the following:

1. Check whether you already have the contents of any of the files linked below
   in your context, WITHOUT reading them yourself. If you can see their contents
   without using a file-read tool, the platform pre-fetched them at activation.

2. If you don't already have the contents, try to read each file using the
   relative path shown. Report whether each path resolved successfully and
   what directory the platform resolved it against.

## Linked References

- See [setup guide](references/setup-guide.md) for installation steps.
- See [troubleshooting](references/troubleshooting.md) for common issues.

## Unlinked Reference

The file `references/unlinked-data.md` exists in this skill's references
directory but is mentioned here only as a plain text path, not as a markdown
link. This tests whether the platform only pre-fetches markdown-linked files
or all mentioned paths.
