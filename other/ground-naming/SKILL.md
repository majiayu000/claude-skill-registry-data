---
name: ground-naming
description: Naming patterns. "Specific is better than generic."
---

# Skill: Naming

> "Names are the first documentation."

## The Standard

- **Specific > Generic**: `Builder`, `Calculator` over `Manager`, `Handler`, `Service`.
- **Verb + Noun**: Actions `CreateOrder`, Jobs `SendWelcomeEmail`, Listeners `NotifyAdmins`.
- **Boolean Prefix**: `isValid`, `hasAccess`, `canEdit`.
- **No Type Suffixes**: `Order` not `OrderEntity`, `User` not `UserContract`.

## The Check

Ask yourself:
- Does the name explain *what* it does?
- Does the name explain *why* it exists?
- If you read the filename, do you know the contents?

## Real-World Examples

See [examples.md](examples.md).
