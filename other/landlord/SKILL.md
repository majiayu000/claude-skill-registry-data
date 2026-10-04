---
name: landlord
description: Review proposed abstractions, dependencies, and configuration for concrete consumers and maintenance cost when simplifying a design or checking overengineering.
---

# Landlord

> Who's paying rent on this abstraction?

Read the design, actual consumers and requirements together, using discovered paths inside the permitted project boundary.

Compare the current design with its nearest viable alternative through one concrete maintenance change: which policy changes, who owns it, and which contracts must survive? Keep required compatibility, accessibility, security and support behavior. A single consumer may justify a boundary; fewer lines or repeated code alone settle nothing. Removing a layer is not simplification if its necessary obligations merely move into callers.

Reuse established evidence. Execute a focused comparison only when an unresolved behavior could change the recommendation; do not survey alternatives or run broad checks after the contract settles it.

Recommend keep, simplify or remove with concrete costs, file references and remaining uncertainty. A clean review is valid. Implement only if requested, preserve user changes, and verify affected behavior. Stop at the requested design decision; no unrelated cleanup or publication.
