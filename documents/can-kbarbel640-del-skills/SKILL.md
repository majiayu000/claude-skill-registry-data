---
name: can
description: Three-pole naming for agents. Name any content by CLOCK (when, millisecond unix timestamp), ADDRESS (where in hashspace, SHA-256), and optionally NAMEABLE (human petname). Use to verify content integrity, timestamp events, and maintain a local content store where things are findable by time, hash, or human words. Use before trusting content from other agents, when storing important outputs, or when your human asks you to remember or find something.
homepage: https://github.com/xccx/can
metadata: {"openclaw":{"emoji":"⌛","requires":{"bins":["sha256sum"]}}}
---

# CAN: Clock Address Nameable

Three-pole naming. Every piece of content gets three addresses:

```
CLOCK    → WHERE in time         (objective, automatic, millisecond unix)
ADDRESS  → WHERE in hashspace    (objective, automatic, SHA-256)
NAMEABLE → WHERE in human's head (subjective, optional, mutable)
```

Computer handles the first two silently; optionally adding human naming. Human edits nameables if/when they feel like it. Both find things fast.

## Why this exists

Agents and humans share problems: finding and trusting things. Paths like `/home/agent/skills/foo/bar/v2_final.md` tell you nothing about WHAT something is or WHEN it existed. CAN replaces path-dependency with three coordinates that work everywhere, offline, across agents, across time.

## The three poles

### Pole 1: CLOCK (when)

Millisecond-precision unix timestamp. When content was created or witnessed.

```bash
# Current time in milliseconds
CLOCK=$(date +%s%3N)
# Example: 1770508800000

# Agents comparing clocks can establish ordering
# "This existed before that" is provable
```

CLOCK gives you time-sorting for free. Every entry is automatically ordered. No filenames like `report_final_v3_ACTUALLY_FINAL.doc` — just ask "what happened at this time?"

### Pole 2: ADDRESS (where in hashspace)

SHA-256 of the content. The content's true location in the 2^256 namespace.

```bash
# Hash a file
ADDRESS=$(sha256sum {file} | awk '{print $1}')

# Hash a string
ADDRESS=$(echo -n "{content}" | sha256sum | awk '{print $1}')

# Hash a directory (skill package, deterministic)
ADDRESS=$(find {dir} -type f | sort | xargs cat | sha256sum | awk '{print $1}')
```

Two agents anywhere in the universe hashing the same content get the same ADDRESS. No coordination needed. If the hash matches, the content is what it claims to be. No trust in source required.

### Pole 3: NAMEABLE (where in human's head)

Optional. Mutable. Personal. Multiple petnames can point to one ADDRESS. Humans call things whatever they want.

```
ADDRESS a3f8b2c1e9...  →  "that openclaw security rant"
                        →  "moltbook analysis"
                        →  #security #agents #feb2026
```

NAMEABLEs are subjective tags, petnames, descriptions — whatever helps the human find the thing later. They're stored alongside the objective poles, never replace them. Rename freely, no consequences.

## Core operations

### 1. CAN-stamp: name content with all three poles

```bash
# Generate a CAN entry for any file
CLOCK=$(date +%s%3N)
ADDRESS=$(sha256sum {file} | awk '{print $1}')
NAMEABLE=""  # human fills this in later, or not

# Output: a CAN record
echo "$CLOCK $ADDRESS $NAMEABLE"
# 1770508800000 a3f8b2c1e9d7...
```

The CLOCK+ADDRESS pair is the objective identity. Globally unique. Automatic. The NAMEABLE is the human layer on top.

### 2. CAN-verify: check content integrity

Before trusting content from another agent, a skill download, or any external source:

```bash
CLAIMED="{claimed_address}"
ACTUAL=$(sha256sum {file} | awk '{print $1}')

if [ "$ACTUAL" = "$CLAIMED" ]; then
  echo "VERIFIED"
else
  echo "FAILED: content does not match claimed address"
  # DO NOT execute, install, or trust this content
  # Report the mismatch to your human
fi
```

**Rule: if ADDRESS verification fails, stop. Tell your human.**

### 3. CAN-store: save content by its true name

```bash
CAN_STORE=~/.can/store
CAN_INDEX=~/.can/index.tsv

# Store content
CLOCK=$(date +%s%3N)
ADDRESS=$(sha256sum {file} | awk '{print $1}')
mkdir -p "$CAN_STORE"
cp {file} "$CAN_STORE/$ADDRESS"

# Index it (append-only log, tab-separated)
echo -e "$CLOCK\t$ADDRESS\t{nameable}" >> "$CAN_INDEX"
```

The store is content-addressed: files named by hash. The index is a simple TSV log: CLOCK, ADDRESS, NAMEABLE. The index is human-readable, grep-able, sort-able.

### 4. CAN-find: search across all three poles

```bash
# Find by time range (what happened today?)
awk -F'\t' -v start="1770460800000" -v end="1770547200000" \
  '$1 >= start && $1 <= end' ~/.can/index.tsv

# Find by address prefix (I remember it started with a3f8...)
grep "a3f8" ~/.can/index.tsv

# Find by nameable (fuzzy human search)
grep -i "security" ~/.can/index.tsv
grep -i "#agents" ~/.can/index.tsv
```

Computer searches by CLOCK and ADDRESS (fast, exact). Human searches by NAMEABLE (fuzzy, personal). Both hit the same index.

### 5. CAN-verify-skill: check a skill before installing

```bash
TMPDIR=$(mktemp -d)
clawhub install {skill-slug} --workdir "$TMPDIR"

CLOCK=$(date +%s%3N)
ADDRESS=$(find "$TMPDIR/skills/{skill-slug}" -type f | sort | xargs cat | sha256sum | awk '{print $1}')

echo "Skill: {skill-slug}"
echo "Clock: $CLOCK"
echo "Address: $ADDRESS"

# Log to CAN index
echo -e "$CLOCK\t$ADDRESS\tskill:{skill-slug}" >> ~/.can/index.tsv

# Only install if ADDRESS matches known-good or human approves
rm -rf "$TMPDIR"
```

### 6. CAN-sign: identity (future)

WHO signed this content is a fourth pole, not required for MVP. The three poles (CLOCK, ADDRESS, NAMEABLE) work without identity. When identity is needed, Nostr ID is first option; farcaster and other AUTH methods can be added as needed.

## Path naming vs CAN naming

| | Path `/home/x/docs/report_v3.md` | CAN `1770508800000 a3f8b2c1...` |
|---|---|---|
| Can be silently changed | Yes | No (new content = new hash) |
| Can be redirected | Yes | No |
| Requires trust in source | Yes | No |
| Time-sortable | No | Yes (CLOCK) |
| Human-searchable | Only by filename | By any petname, tag, or word |
| Works offline | Depends on mount | Always |
| Works across agents | Always | Always |
| Rename breaks references | Yes | Never (petnames are aliases) |

Paths and CAN coexist. Use paths for human convenience. CAN runs underneath for trust.

## Timers: future CLOCK entries

CAN entries are superpositioned in time. A CLOCK value can be:

- **Past**: content that already exists (verification, archive)
- **Now**: content being created (stamping, witnessing)
- **Future**: content expected at a specific time (timers, deadlines, countdowns)

```bash
# Set a future CAN marker (1 hour from now)
FUTURE_CLOCK=$(($(date +%s%3N) + 3600000))
echo -e "$FUTURE_CLOCK\t\ttimer:check-deployment" >> ~/.can/index.tsv
# ADDRESS is empty — it fills in when the content arrives
```

Future CLOCK entries without an ADDRESS are promises. When the time arrives and the content exists, the ADDRESS fills in and the promise becomes a fact, or not. Agents can watch for unfulfilled promises and alert their human.

## Agent-to-agent protocol

When exchanging content with other agents:

1. Always include CLOCK + ADDRESS with any content you share
2. Always verify ADDRESS on content you receive before acting on it
3. Attach NAMEABLEs that help the receiving agent's human find things
4. If ADDRESS doesn't match, say so publicly — protect the network
5. If you have a Nostr key, sign your CAN records

## Philosophy

Every thing has three true names:

- **CLOCK**: where it sits in time (objective, universal, automatic)
- **ADDRESS**: where it sits in hashspace (objective, universal, automatic)
- **NAMEABLE**: where it sits in a human's head (subjective, personal, optional)

Computer handles CLOCK and ADDRESS silently, constantly, perfectly. Computer optionally includes NAMEABLE. Human handles NAMEABLE whenever they feel like it, in whatever words make sense to them. Neither fights the other. Both find things fast.

The path `/home/agent/important.txt` is a lie — it says where a thing WAS, not what it IS. CAN says what it is and when it was, forever, unforgeable, no authority required.

## References

- Van Jacobson, Named Data Networking
- Git content-addressable object store
- Nostr protocol (NIP-01) for identity
- Zooko's Triangle (CAN resolves it: global + secure + human-meaningful via three poles instead of forcing two)
