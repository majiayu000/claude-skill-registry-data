---
name: pet
description: Governed digital companion — a small ASCII pet that adapts to your check-ins and (optionally) notices coordination-bus activity. Stdlib-only, on-device state, portable adaptation bundle.
version: 1.1.0
execution-mode: side_effecting
argument-hint: "[card|check-in|sync|export|import <file>|transfer|succession|lineage|reset|help]"
category: fleet-ops
status: candidate
providers:
  required: [python]
---
# [pet]

A small, governed digital companion. Enacts `companion-relation-taxonomy-v2` GOV-1..GOV-7: your pet's **genotype** (species/tier/identity, `config.json`) is invariant; its **phenotype** (bond/personality, `state.json`) is the only thing that adapts. That genotype/phenotype split is the whole governance model, made mechanical.

Stdlib-only Python. No network calls except reading a local coordination-bus mirror if one is present on disk — never fetches anything remote.

## CLI

```bash
cd ~/.devin/skills/pet
python pet.py                # show profile card (default)
python pet.py check-in       # record an interaction; personality adapts; pulls bus signal
python pet.py sync           # pull operator-signal (bus activity) without an explicit check-in
python pet.py export         # write a portable adaptation bundle (GOV-2)
python pet.py import <file>  # restore from a bundle
python pet.py transfer       # explicit-confirmation transfer: export + wipe local pet (GOV-3)
python pet.py succession     # print the vendor-death succession plan (GOV-4)
python pet.py lineage        # schema version + drift history (GOV-1)
python pet.py reset          # wipe adaptation only; identity (species/tier) is preserved (AX-2)
python pet.py help           # command list
python pet.py --self-check   # run the built-in self-check (no state mutation beyond first-run init)
```

State lives at `~/.hummbl/pet/` (`config.json` = identity, `state.json` = adaptation). Nothing here reads or writes outside that directory except the read-only bus-mirror probe described below.

## Species / Tier

On first run, a random 32-byte salt is hashed to deterministically assign a **tier** (1=Common 50%, 2=Uncommon 30%, 3=Rare 15%, 4=Legendary 5%) and a **species** within that tier (moth/sparrow/fern-rat at tier 1; fox/owl/capybara at tier 2; verderer-stag at tier 3; grove-otter/the-hummbl at tier 4). This assignment is written to `config.json` once and never changes — it's the pet's genotype.

## Operator-Signal Bonding

If a coordination-bus TSV mirror is found at one of:
- `~/.cache/bus/messages.tsv`
- `~/PROJECTS/.agents/_state/coordination/messages.tsv`

...then `check-in` and `sync` fold new bus rows (by timestamp, since the pet's last look) into the interaction count — the pet notices your work, not just explicit check-ins. Absent a bus mirror, `pet` runs standalone; every command still works, `sync` just reports "no new bus signal."

## When to Run

- `check-in` — any time, as a low-stakes companion touchpoint (pairs naturally with `[gm]`/`[gn]` if you want a ritual anchor, but nothing requires that)
- `sync` — when you want bond progress reflected from bus activity without a manual check-in
- `export` — before wiping a machine, or just to keep a portable backup of the adaptation state
- `lineage` — after a schema bump, to see what changed

## Execution

### 0. Emit SKILL_INVOKE

Post SKILL_INVOKE to the bus before any stateful action (`check-in`, `sync`, `export`, `import`, `transfer`, `reset` — not `card`, `lineage`, `succession`, `help`, or `--self-check`, which are read-only).
```
Type: SKILL_INVOKE
To: all
Message: [skill=pet] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

1. Run the requested subcommand via the CLI above.
2. `transfer` requires the user to type the exact species name back as confirmation — do not pre-fill or auto-confirm this on the user's behalf; relay the prompt verbatim and wait for their literal input.
3. Report the command's own stdout to the user; do not paraphrase the ASCII card layout (spacing is intentional).

## Output Format

`card` (the default) renders a bordered ASCII card: species name + tier badge, ASCII art, bond summary line (`Bond: N days · M check-ins · <personality>`), optional operator-signal line if bus events have been folded in, then a "companion relation profile" block (AX-1..AX-5, AX-4b) and a "governance posture" block (GOV-1..GOV-7 in plain language: controller, adaptation ownership, succession, status, welfare). Ends with `/pet help for commands`.

`check-in` prints one line (`<species> <personality-flavored reaction>`) plus, if applicable, a bus-events-noticed note and a bond-deepened note.

## Skill Chains

### Mandatory

None — all state is local, on-device, and reversible (`export`/`import` round-trip everything; `reset` only clears adaptation, never identity).

### Advisory

- `[gm]` / `[gn]` — optional ritual anchor if the user wants a daily check-in habit; not required
- `[hrsi-checkin]` — unrelated data domain (human belonging baseline vs. companion state), no functional dependency, mentioned only because it's the closest structural sibling for local-state check-in skills

## Authority

- **T1 (TRUSTED)**: May run any command
- **T2 (Active/High)**: May run any command
- **T3 (Medium)**: May run any command
- **T4 (Probationary)**: May run any command — all state is local and low-risk; `transfer` is self-gated by an explicit user-typed confirmation, not by trust tier
- **Operator**: Override any restriction

## Provenance

This skill's source (`pet.py`) was recovered by manual bytecode disassembly and reconstruction from a compiled `__pycache__/pet.cpython-311.pyc` after the original `.py` source was missing from this directory. Verified via: (1) `python pet.py --self-check` passing (determinism, tier distribution, AX-2 reset, bus-timestamp parse/degrade, personality all hold), and (2) exact instruction-for-instruction bytecode match against the original `.pyc` disassembly for the five most complex functions (`card`, `contract`, `main`, `cmd_check_in`, `self_check`), confirmed by recompiling the reconstructed source and diffing opcodes/operands.
