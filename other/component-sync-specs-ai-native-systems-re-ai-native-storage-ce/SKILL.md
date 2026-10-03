---
name: component-sync-specs
description: Ensure a component implementation is synchronized with its specifications.
argument-hint: "[component-name, component-name, ...]"
---

For each component identified in $ARGUMENTS, run the following:
1. /speckit-sync-analyze
2. /speckit-sync-propose --interactive
3. /speckit-sync-apply

