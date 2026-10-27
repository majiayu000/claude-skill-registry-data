---
name: mmag
description: Mixed Memory-Augmented Generation (MMAG) for AI agents. Five cognitive memory layers — conversational, long-term user, episodic, sensory, and short-term working — coordinated into a unified LLM context. Use when you need agents that remember across sessions, personalize responses, track events, and adapt to environmental context.
---

# MMAG — Mixed Memory-Augmented Generation

**Give your agent a real memory.**

Most agents forget everything the moment a session ends. MMAG fixes that by organizing memory into five layers that mirror how human cognition works — so your agent can recall past conversations, adapt to user preferences, track upcoming events, and stay aware of its environment.

---

## 🧠 For the Agent: When and How to Use This Skill

**Always call `context.sh` at the start of every session** and inject the output as your system prompt. This is the primary integration point.

```bash
~/.openclaw/skills/mmag/context.sh
```

### Trigger Rules — What to Store and When

| Situation | Action |
|---|---|
| User shares a preference, habit, or personal fact | `store.sh long-term "<fact>" --label <topic>` |
| User mentions a future event, meeting, or deadline | `store.sh episodic "<event with date>"` |
| User provides location, time, or environmental info | `store.sh sensory "<context>"` |
| A notable exchange happens during the session | `store.sh conversational "<summary>"` |
| You receive the current task or goal | `store.sh working "<goal>"` |
| Session ends | `prune.sh` — archives working memory into episodic |
| Context window is getting full | `snapshot.sh` — compress all layers to disk |

### Decision Flow

```
Session start
  → run context.sh → inject output into system prompt
  → store.sh working "Current task: <goal>"

During session
  → on personal fact → store.sh long-term
  → on scheduled event → store.sh episodic
  → on location/time → store.sh sensory
  → on key exchange → store.sh conversational

Session end
  → run prune.sh

Weekly / before compression
  → run snapshot.sh
```

### Priority Order (for conflict resolution)

When memory signals conflict, apply in this order:
1. **Long-term user traits** — shape personalization and tone
2. **Episodic events** — override defaults when time-sensitive
3. **Sensory context** — adjust register and urgency
4. **Conversational history** — maintain coherence across turns
5. **Working memory** — governs the current task focus

---

## 📖 For Humans: Understanding the Five Layers

| Layer | What it stores | Human analogy |
|---|---|---|
| 💬 **Conversational** | Dialogue threads and session history | What was said 5 minutes ago |
| 🧍 **Long-Term User** | Preferences, traits, and background | How a friend remembers you over years |
| 📅 **Episodic** | Timestamped events and reminders | A personal diary or calendar |
| 🌦️ **Sensory** | Location, weather, time of day | Situational awareness |
| 🗒️ **Working** | Current session scratchpad | Mental notepad while solving a problem |

---

## 🚀 Setup

### Initialize (once)

```bash
~/.openclaw/skills/mmag/init.sh
```

Creates:
```
memory/
├── conversational/     # dialogue logs, one file per session
├── long-term/          # user profile and preference files
├── episodic/           # daily event logs  (YYYY-MM-DD.md)
├── sensory/            # environmental context snapshots
└── working/            # ephemeral session scratchpad
    └── snapshots/      # compressed backups
```

---

## 🛠️ Command Reference

| Script | Usage | Output |
|---|---|---|
| `init.sh` | `init.sh` | Creates the 5-layer `memory/` directory |
| `store.sh` | `store.sh <layer> "<text>" [--label <name>]` | Appends a timestamped entry |
| `retrieve.sh` | `retrieve.sh <layer\|all> [query]` | Prints matching lines (auto-decrypts `.md.enc`) |
| `context.sh` | `context.sh [--max-chars N]` | Outputs a complete, prioritized system-prompt block |
| `prune.sh` | `prune.sh` | Archives working → episodic, clears scratchpad |
| `snapshot.sh` | `snapshot.sh` | Saves `working/snapshots/<timestamp>.tar.gz` |
| `stats.sh` | `stats.sh` | Prints per-layer file count, size, last entry |
| `keygen.sh` | `keygen.sh` | Generates a 256-bit key → `~/.openclaw/skills/mmag/.key` |
| `encrypt.sh` | `encrypt.sh [--layer <layer>] [--file <path>]` | Encrypts `.md` → `.md.enc`, removes originals |
| `decrypt.sh` | `decrypt.sh [--layer <layer>] [--file <path>] [--stdout]` | Decrypts to disk or pipes to stdout |

**Valid layers:** `conversational` · `long-term` · `episodic` · `sensory` · `working`

---

## 🔐 Privacy & Encryption

Long-term memory contains biographical data. MMAG ships with built-in AES-256-CBC encryption via `openssl`.

### First-time setup — generate a key

```bash
~/.openclaw/skills/mmag/keygen.sh
# saves to ~/.openclaw/skills/mmag/.key  (chmod 600)
```

> ⚠️ **Back up your key file.** Without it, encrypted memories cannot be recovered.

### Encrypt the long-term layer

```bash
~/.openclaw/skills/mmag/encrypt.sh --layer long-term
```

Encrypts all `.md` files → `.md.enc` and securely removes the originals.

### Decrypt when needed

```bash
# Restore to disk
~/.openclaw/skills/mmag/decrypt.sh --layer long-term

# Or decrypt a single file
~/.openclaw/skills/mmag/decrypt.sh --file memory/long-term/preferences.md.enc
```

### Transparent access

`context.sh` and `retrieve.sh` automatically decrypt `.md.enc` files **in-memory** — no plaintext is written to disk. Key is resolved in this order:

1. `MMAG_KEY` environment variable
2. `~/.openclaw/skills/mmag/.key` file
3. Interactive passphrase prompt

```bash
# Use env var (e.g. in automated contexts)
export MMAG_KEY=$(cat ~/.openclaw/skills/mmag/.key)
~/.openclaw/skills/mmag/context.sh
```

### Other best practices

- **Audit** with `retrieve.sh long-term` to review what's stored.
- **Erase on demand** — delete any file in `memory/long-term/` to remove specific traits.
- **Minimize** — only store what genuinely improves interactions.

---

## 🔭 Extensibility

The `store.sh` / `retrieve.sh` / `context.sh` interface is intentionally generic. New layers require only a new directory and one added block in `context.sh`. Planned extensions:

- **Multimodal sensory** — connect visual or audio signals
- **Dynamic profile embeddings** — learned preference vectors instead of static files
- **Event-triggered retrieval** — proactively surface episodic items before deadlines
- **Encrypted cloud backup** — optional remote sync of the long-term layer

---

*Based on the Mixed Memory-Augmented Generation (MMAG) research pattern.*
*Paper: [arxiv.org/abs/2512.01710](https://arxiv.org/abs/2512.01710)*
