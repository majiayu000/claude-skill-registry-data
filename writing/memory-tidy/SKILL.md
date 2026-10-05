---
name: memory-tidy
description: Keep Claude Code's always-loaded MEMORY.md index healthy — trim over-length entries, move done work to the archive, fold domains into hub files, and give orphaned notes a pointer so they stay findable. Triggers on "/memory-tidy", "tidy memory", "my memory index is huge", "MEMORY.md is over budget", "orphaned memory notes", "clean up memory". Also run it yourself when the memory guard reports RED or the index approaches its budget. Do NOT touch an index another machine owns — ownership is declared in memory_scope.json, never guessed.
license: MIT
---

# Memory Tidy

`MEMORY.md` is loaded into **every** session. It is not a file, it is rent you pay on every turn.
Past a fixed size the harness truncates it and says nothing: the tail silently disappears and your
agent stops knowing things it "remembers". So this is about **retention**, not tidiness.

Three tiers, and only the first one costs tokens continuously:

* `MEMORY.md` — **hot dispatcher**, loaded every turn. Target 60–100 lines, one pointer per line,
  `- [Title](file.md) — hook`, ≤150 chars.
* `hub-*.md` — **warm sub-index**, not auto-loaded. A domain of ≥3 related lines lives here.
* `MEMORY-archive.md` — **cold**, not auto-loaded, grep-only. Done work + coverage for orphans.

## Step 0 — ownership (skipping this is how you corrupt someone's memory)

```bash
python3 ~/.claude/scripts/memory_scope.py --explain
```

`~/.claude/projects/` holds three things that look identical: your own indexes, byte-identical
copies **synced from another machine**, and throwaway worktrees. Writing into a synced copy means
two writers on one file. Declare ownership in `memory_scope.json`; never infer it. An undeclared
machine exits 3 loudly, because a machine that silently tidies nothing looks exactly like a healthy one.

## Step 1 — look before you touch

```bash
sh ~/.claude/scripts/memory_tidy.sh --dry-run --force
```

Prints the detectors' verdict and renders the prompt without changing anything. Read the rendered
prompt — that is what the model will act on.

## Step 2 — the mechanical part (no model, 0 tokens)

```bash
python3 ~/.claude/scripts/memory_orphan_cover.py --dry-run
python3 ~/.claude/scripts/memory_orphan_cover.py
```

An orphan is not lost data, it is **unreachable** data — which at recall time is the same thing.
Pointers go into the archive, which is not auto-loaded, so coverage costs zero live budget. The hook
comes from each note's own `description:` field: the script transcribes, it does not invent.

## Step 3 — fold a domain into a hub

A domain with ≥3 related live lines and no hub gets one. Do it in the same pass; do not ask.

```bash
python3 ~/.claude/scripts/memory_fold.py --index <MEMORY.md> --map <mapping.json> --dry-run
```

Judgement (which slug belongs to which domain) lives in the mapping and is yours. Byte-moving is the
script's job. This is deliberate: the documented failure mode of folding is **summary-grounding** —
a model rewrites the hook "while it's in there" and the detail that made the pointer findable
evaporates. The script never paraphrases, and it refuses to write at all if any folded slug would
lose reachability.

## Step 4 — judgement (yours, not the script's)

* **Keep LIVE** only a standing rule that could fire in a session that never opens the hub.
* **Archive** closed one-offs, finished projects, superseded tools.
* Before archiving, grep the note for open tails (`pending|BLOCKED|TODO|⚠`). A genuine unfinished
  action goes on your task board, not into a grave.
* Unsure whether something is still live? **Keep it live.** Over-pruning costs more than under-pruning.
* A hook cut mid-sentence ("…before «X") is a defect, not compactness. Repair it from the note's
  `description:`.

## Step 5 — verify, and only then say done

```bash
MEMORY_GUARD_EXCLUDE="$(python3 ~/.claude/scripts/memory_scope.py --exclude)" \
  python3 ~/.claude/scripts/memory_guard.py
```

Must print GREEN. **The model's own summary of its work is not evidence** — the guard is the judge.

## Gotchas worth knowing before you hit them

* **A pin list shared across machines.** If the pinned note only exists on one machine, every other
  machine's "a pinned rule fell out!" alarm can never be cleared — and "restoring" the pointer
  creates a *dead* pointer. A pin applies only where the note actually lives.
* **Generated files counted as memories.** Tooling writes a hints file next to the index; counting
  it as an orphan creates an eternal chore. An alarm nobody can clear teaches people to ignore alarms.
* **A logged-out CLI that exits 0.** Headless `claude -p` without a session printed an error and
  returned success; routines stamped green and produced nothing. Check `claude auth status`.
* **launchd has no catch-up.** A calendar job missed while the machine slept is skipped silently —
  schedule two slots. The second is free when the detectors say "nothing to do".
* **Project dirs starting with `-`** are read as flags by CLI tools: `md5 -q ./path`, not `md5 -q path`.

## Test

```bash
python3 tests/test_memory_tidy.py    # 37 checks, ~1s, no LLM, no network, temp fixture
```
