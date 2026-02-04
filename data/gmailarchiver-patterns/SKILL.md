---
name: gmailarchiver-patterns
description: >-
  GMailArchiver architecture, layer patterns, and component design. Use when
  working with cli, core, data, connectors, or shared layers, or understanding
  component dependencies. Triggers on: architecture, layer, pattern, component,
  cli layer, core layer, data layer, SOLID, dependency, contract.
---

# GMailArchiver Coding Patterns

This skill provides guidance on coding patterns and conventions for GMailArchiver.

## Source Documentation

**Always read the authoritative sources for current patterns:**

1. **`CLAUDE.md`** - Quick reference for AI assistants, includes:
   - Project overview
   - Development commands
   - Architecture summary
   - Key patterns and safety architecture

2. **`docs/ARCHITECTURE.md`** - Complete system architecture:
   - Layer-based architecture (cli, core, data, connectors, shared)
   - Layer dependency rules and contracts
   - Data integrity architecture
   - Component responsibilities

3. **`docs/CODING.md`** - Coding standards:
   - Style guidelines (line length, imports)
   - Type hint requirements
   - Error handling patterns

4. **`docs/PROCESS.md`** - Development workflow:
   - 6-phase development process
   - Definition of done
   - Quality gates

## Layer Documentation

Each layer has its own architecture documentation:
- `src/gmailarchiver/cli/ARCHITECTURE.md` - CLI layer design
- `src/gmailarchiver/core/ARCHITECTURE.md` - Business logic design
- `src/gmailarchiver/data/ARCHITECTURE.md` - Data layer design
- `src/gmailarchiver/connectors/ARCHITECTURE.md` - Connectors design
- `src/gmailarchiver/shared/ARCHITECTURE.md` - Shared utilities design

## Usage

When working on code:
1. Read the relevant ARCHITECTURE.md files for the layer(s) you're modifying
2. Follow patterns documented in those files
3. If patterns change, update the documentation (not this skill)

The source documentation is the **single source of truth** - this skill just points you there.
