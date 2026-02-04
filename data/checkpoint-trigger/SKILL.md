---
name: checkpoint-trigger
description: Natural language wrapper for checkpoint commands - automatically triggers /checkpoint:create, /checkpoint:restore, /checkpoint:list when users request checkpoint operations
schema_version: 1.0
---

# checkpoint-trigger

**Type:** WRITE-CAPABLE
**DAIC Modes:** IMPLEMENT only
**Priority:** Low

## Trigger Reference

This skill activates on:
- **Keywords:** "create checkpoint", "save checkpoint", "restore checkpoint", "load checkpoint", "list checkpoints", "checkpoint", "save state", "restore state"
- **Intent Patterns:** `(create|save|make).*?checkpoint`, `(restore|load|recover).*?checkpoint`, `(list|show).*?checkpoint`, `(save|restore).*?state`

From: `skill-rules.json` - checkpoint-trigger configuration

## Purpose

Automatically trigger checkpoint commands (`/checkpoint:create`, `/checkpoint:restore`, `/checkpoint:list`) when users request checkpoint operations using natural language.

## Core Behavior

When activated in IMPLEMENT mode:

1. **Checkpoint Intent Detection**
   - Detect checkpoint operations from natural language
   - Route to appropriate checkpoint command

2. **Command Routing**
   - **Create:** "save checkpoint" → `/checkpoint:create`
   - **Restore:** "load checkpoint X" → `/checkpoint:restore X`
   - **List:** "show checkpoints" → `/checkpoint:list`

## Natural Language Examples

**Triggers this skill:**
- ✓ "Create checkpoint"
- ✓ "Save current state"
- ✓ "Restore checkpoint 3"
- ✓ "List all checkpoints"

## Safety Guardrails

**WRITE-CAPABLE RULES:**
- ✓ Only execute in IMPLEMENT mode
- ✓ Checkpoints use git stash mechanism
- ✓ Verify clean working directory before restore
