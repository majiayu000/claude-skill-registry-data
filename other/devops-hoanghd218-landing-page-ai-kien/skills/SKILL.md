# Close Phase Skill

**Activation**: `/close-phase` or `/checkpoint`

**Purpose**: Seal the current phase with complete context externalization. Creates closeout file with summary, decisions, excerpts, and rollback checkpoint. Makes it safe to close the terminal.

---

## When to Use

- At human gate approval (end of major phase)
- When you need to switch to a new terminal
- Before a long break from the project
- When context window is filling up
- Anytime you want a clean checkpoint

---

## What It Does

1. **Verifies gate approval** - Ensures human has approved phase completion
2. **Generates summary** - AI-written narrative of what happened
3. **Captures decisions** - All decisions with rationale and rejected alternatives
4. **Preserves excerpts** - Key conversations for future reference
5. **Runs codebase-curator** - Organizes files into canonical locations
6. **Creates rollback checkpoint** - Enables precise restoration
7. **Generates entry brief** - Ready-to-use context for next phase
8. **Confirms safe to close** - All context externalized to disk

---

## Usage

```
/close-phase
```

Or with explicit phase number:

```
/close-phase 7
```

Or as checkpoint alias:

```
/checkpoint
```

---

## Output

```
╔═══════════════════════════════════════════════════════════════════════╗
║  PHASE 7 CLOSEOUT COMPLETE                                            ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  ✓ Summary recorded           (330 words)                             ║
║  ✓ Decisions captured         (4 decisions with rationale)            ║
║  ✓ Excerpts preserved         (3 key conversations)                   ║
║  ✓ Codebase curated           (18 files organized)                    ║
║  ✓ Rollback checkpoint        (CP-007-20250115T1430)                  ║
║  ✓ Entry brief generated      (Ready for Phase 8)                     ║
║                                                                        ║
║  Closeout file: .claude/closeouts/phase-07.yaml                       ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  🧠 CONTEXT FULLY EXTERNALIZED                                         ║
║                                                                        ║
║  Everything from this phase has been recorded to disk.                ║
║  You can safely close this terminal. Nothing will be lost.            ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  TO CONTINUE IN NEW TERMINAL:                                         ║
║                                                                        ║
║  cd /path/to/project && claude                                        ║
║                                                                        ║
║  Then say:                                                             ║
║  ┌─────────────────────────────────────────────────────────────────┐  ║
║  │ Continue from Phase 8. Read .claude/closeouts/phase-07.yaml     │  ║
║  └─────────────────────────────────────────────────────────────────┘  ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## Closeout File Location

`.claude/closeouts/phase-{NN}.yaml`

Example: `.claude/closeouts/phase-07.yaml`

---

## Resuming After Closeout

In a new terminal:

```
Continue from Phase 8. Read .claude/closeouts/phase-07.yaml
```

Or simply:

```
Continue dev-system project.
```

The session-master will detect the closeout and offer to continue.

---

## Related Skills

- `/rollback` - Restore to a previous phase checkpoint
- `/status` - Show current pipeline state
- `/dashboard` - Open visual pipeline dashboard

---

## Implementation

Invokes: `phase-closeout-agent`

The skill:
1. Reads current phase from pipeline-state.json
2. Verifies human gate has been approved (or prompts for approval)
3. Invokes phase-closeout-agent with current phase context
4. Agent generates closeout file
5. Presents confirmation with resume instructions
