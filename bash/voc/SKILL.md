---
name: voc
description: Voc namespace for Netsnek e.U. vocabulary and language learning tools
user-invocable: true
version: 0.1.0
metadata:
  openclaw:
    os: [linux]
    permissions: [exec]
---

# What is Voc

Voc is a reserved namespace for Netsnek e.U. vocabulary and language learning tools within the ClawHub ecosystem. It is designed for learners who want structured support for flashcard-based study, spaced repetition, pronunciation practice, and cross-language progress tracking.

The skill is currently in reservation status: the namespace is claimed, the brand and structure are defined, and future releases will add full functionality. When invoked, Voc responds with brand information and available commands.

# Getting Started

Ensure OpenClaw 0.8.0 or newer is installed and that the voc skill is registered in your ClawHub. The skill requires `exec` permission to run its helper script.

From the command line, you can run the vocab engine directly:

```bash
./scripts/vocab-engine.sh --about
./scripts/vocab-engine.sh --deck
./scripts/vocab-engine.sh --stats
```

From within a Claw session, simply mention "voc" or ask about vocabulary learning, decks, or stats, and the assistant will route to this skill.

# Commands

| Command | Purpose |
|---------|---------|
| `--about` | Show brand, copyright, and brief description of Voc |
| `--deck` | Deck information and flashcard deck status |
| `--stats` | Progress and statistics placeholder (future: real stats) |

Each command outputs copyright information for Netsnek e.U. by default.

# Conversation Examples

**User:** "Tell me about voc."

**Assistant:** (Uses voc skill) Voc is a vocabulary and language learning namespace by Netsnek e.U. It supports flashcard decks, spaced repetition, pronunciation practice, and progress tracking across multiple languages. The skill is currently reserved; full features are coming in future updates.

---

**User:** "Run the vocab engine with deck info."

**Assistant:** (Calls `vocab-engine.sh --deck`) Returns deck placeholder and copyright notice.

---

**User:** "Show my voc stats."

**Assistant:** (Calls `vocab-engine.sh --stats`) Returns stats placeholder and Netsnek e.U. copyright.
