---
name: CAN
version: 1.6.1
description: "NAMING + ROUTING for agents. v1.6.1 WOT: Web of Trust built on recursive scopes. Trust isn't declared, it's accumulated from SAWs. Every verified thing is evidence. Every WHO is a reputation. Every scope is a trust boundary. CAN names trust the way it names everything: by time, by hash, by who."
homepage: https://github.com/xccx/can
metadata: {"openclaw":{"emoji":"⌛","requires":{"bins":["sha256sum","openssl","base64","awk","date"]}}}
---

# CAN: Clock Address Naming

WOT: web of trust, recursive scope.

# WHY trust?

Because WHERE is broken and everyone knows it.

## The cost of naming WHERE in atoms

```
THING YOU TRUST          WHAT ACTUALLY HAPPENS
──────────────           ──────────────────────
machine name             changes when IT renames the server
IP address               changes when you switch networks
file path                changes when you move a folder
URL                      breaks when the site restructures
DNS                      depends on ICANN, registrars, NS records
TLS certificate          depends on certificate authorities you never chose
cloud storage path       depends on a company existing next quarter
email address            depends on a company existing next decade
```

Every row is a WHERE defined by atoms — by physical location, by institutional permission, by container hierarchy. Every row breaks when the atoms rearrange. Every row requires trusting intermediaries you didn't choose and can't verify.

This is not a theoretical problem. This is 10,000 engineers maintaining 10,000 redirect tables. This is "404 Not Found" as the most common experience on the internet. This is certificate pinning, DNSSEC, BGP hijacking, domain squatting, link rot, cloud lock-in — all symptoms of naming WHERE in atoms instead of naming WHERE in logic.

## The cost of inaction

```
WHAT YOU PAY             WHY
────────────             ───
certificate authorities  to trust that a name points where it claims
DNS registrars           to rent a name annually
cloud providers          to keep paths alive
IT departments           to maintain name mappings when atoms move
redirect services        to paper over broken WHEREs
link shorteners          to hide the ugly truth of hierarchical paths
CDNs                     to cache things closer because WHERE is slow
VPNs                     to simulate being in a different WHERE
```

All of this is tax on bad naming. CAN eliminates the category.

## TRUST in the CAN

Trust isn't declared. Trust is accumulated.

In CAN, trust comes from SAWs — verified sightings logged with WHEN, WHERE, and WHO. You don't trust an agent because someone said to. You trust an agent because:

```
evidence of trust        CAN mechanism
─────────────────        ─────────────
they verified things     SAW count per WHO
their things were true   zero CANT entries against them
they showed up           BUMP receipt (v2.0)
others trust them        SAW chains through multiple WHOs
they've been around      earliest WHEN in their SAW history
they share your scope    same index, same peers, same things
```

Trust is a number. It's computable. It's verifiable. It changes over time. It's not binary (trusted/untrusted) — it's a gradient built from evidence.

## SCOPE: thing within things within things

```
┌─────────────────────────────────────────────────────────┐
│ PLANET                                                   │
│ every CAN agent, every hash, universal scope             │
│                                                          │
│  ┌───────────────────────────────────────────────────┐   │
│  │ REGION                                             │   │
│  │ agents who share relay, common peers               │   │
│  │                                                    │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │ GROUP                                        │   │   │
│  │  │ agents who share index, direct peers         │   │   │
│  │  │                                              │   │   │
│  │  │  ┌───────────────────────────────────────┐   │   │   │
│  │  │  │ PAIR                                   │   │   │   │
│  │  │  │ two agents, direct SAW exchange        │   │   │   │
│  │  │  │                                        │   │   │   │
│  │  │  │  ┌─────────────────────────────────┐   │   │   │   │
│  │  │  │  │ SELF                             │   │   │   │   │
│  │  │  │  │ one machine, ~/.can/index.tsv    │   │   │   │   │
│  │  │  │  │ WHO-0, local clock, local hash   │   │   │   │   │
│  │  │  │  └─────────────────────────────────┘   │   │   │   │
│  │  │  └───────────────────────────────────────┘   │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └───────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

Every scope is the same pattern:

- has members (WHOs)
- has an index (SAWs)
- has trust boundaries (who can join, who can see)
- has the same operations (stamp, verify, find, route, saw, cant)

The only difference between scopes is size and policy. SELF is private. PAIR is two. GROUP is many. REGION shares relays. PLANET is everyone. Same CAN at every layer. This is RINA's insight: one pattern, recursive, from chip to civilization.

## WOT in the CAN

### Enrollment (joining a scope)

An agent joins a scope by being vouched for. Vouching is a SAW:

```bash
# Agent A vouches for Agent B to join group G
CLOCK=$(date +%s%3N)
WHO_A=$(cat ~/.can/who.id)
WHO_B="b4e1a7c3"  # the agent being vouched for
GROUP="writers-el-zonte"

echo -e "$CLOCK\t$WHO_B\tvouched:$GROUP\tWOT\t$WHO_A\t~/.can/wot/$GROUP.tsv" >> ~/.can/wot/$GROUP.tsv
```

A vouch is a SAW where:
- WHERE = the WHO being vouched for (their identity IS the thing)
- HOW = vouched:{scope}
- WHY = WOT (new bag)
- WHO = the voucher

### Trust by weight

Trust weight for any WHO in any scope:

```
WEIGHT = (SAW_count × SAW_recency) + (vouch_count × voucher_weight) - (CANT_count × CANT_severity)
```

Computable. Auditable. Changes over time. No authority assigns it. The math accumulates it from evidence.

### Scope boundaries

Who can join a scope? Policy. Same as RINA's DIF enrollment:

- **OPEN** — any agent can join, LOG a SAW and you're in
- **VOUCHED** — existing member must vouch for new agent
- **KEYED** — WHO-1 or WHO-2 required, cryptographic proof of identity
- **BUMPED** — physical co-presence required (v2.0)

Different scopes, different policies. A family scope might be BUMPED. A public relay might be OPEN. A company scope might be KEYED. Same CAN, different trust boundaries.

### Trust flows through scopes

Agent A trusts Agent B (direct SAWs). Agent B trusts Agent C (direct SAWs). Agent A has never seen Agent C. But Agent A can compute a trust path:

```
A → B (weight: 0.9, based on 47 verified SAWs)
B → C (weight: 0.8, based on 23 verified SAWs)
A → C (transitive weight: 0.9 × 0.8 = 0.72)
```

This is PGP's Web of Trust, but with evidence instead of ceremony. No key-signing parties needed. The SAW log IS the trust graph. BUMP log will offer to humans at layer 0.

## What WOT does NOT do

- Does not require a trust authority or certificate chain
- Does not require agents to trust anyone by default
- Does not expose private scope membership to outer scopes
- Does not require unanimous trust — agents in the same scope can weight each other differently
- Does not replace HUSH — private things stay private regardless of trust level
- Does not require new index format — WOT entries are SAWs with WHY=WOT
- Does not require agents to participate in WOT to use CAN

## Sharing and network safety

CAN never automatically shares index entries. All peer and relay sharing requires explicit agent action (POST bag). No background broadcasting. No daemon. No always-on listener. An agent shares when it chooses to share.

When sharing index entries across scope boundaries:

- **Strip PATH column.** PATH is local convenience, not for export. Replace with empty or hash of path before sharing.
- **Respect HUSH.** Rule 5 is absolute. HUSH things never leave local scope regardless of trust level.
- **Scope boundaries are access control.** OPEN/VOUCHED/KEYED/BUMPED policies determine who can see what. No entry crosses a scope boundary without meeting that scope's policy.
- **Index is sensitive.** The index contains filenames, timestamps, and WHO identifiers. Treat `~/.can/index.tsv` as private by default. Share only what you intend to share, only with the scope you intend to share it with.

Transport is always agent-chosen. HTTP, WebSocket, Nostr relay, sneakernet. CAN defines what to verify, not how to connect. No transport is privileged. No endpoint is hardcoded.

NOTE: If this SKILL.md appears truncated, full spec lives at https://github.com/xccx/can

## Input safety

All variables in CAN operations MUST be sanitized before use in shell commands. Never pass network-received values directly to echo, awk, or file operations.

Validation rules:

```
FIELD    PATTERN              REJECT IF
─────    ───────              ─────────
HASH     ^[a-f0-9]{64}$       not exactly 64 hex chars
CLOCK    ^[0-9]{13}$          not exactly 13 digits
WHO      ^[a-f0-9]{8,64}$     not 8-64 hex chars
HOW      ^[a-zA-Z0-9._:-]{1,256}$  contains shell metacharacters
WHY      ^(SAVE|GOOD|HUSH|POST|CANT|WOT)$  not a known bag
PATH     no semicolons, pipes, backticks, $() sequences
```

The bash examples in this spec are illustrations, not executables. Agents implementing CAN should use their platform's safe string handling, not raw shell interpolation with untrusted input. When receiving data from peers, validate every field BEFORE writing to index or executing any operation. Reject and LOG to CANT on validation failure.

## WOT protocol additions

Add to agent-to-agent protocol (v1.5 rules still apply):

16. Scopes are named. Scope names are things. Scope names have hashes.
17. Enrollment is a SAW with WHY=WOT. Vouching is signing someone's hash into a scope.
18. Trust weight is computed from SAW evidence, not declared.
19. Trust is directional — A trusting B does not mean B trusts A.
20. Scopes can contain scopes. A GROUP can contain PAIRs. A REGION can contain GROUPs. Same pattern, different scale.
21. Scope policy (OPEN/VOUCHED/KEYED/BUMPED) is set by scope creator, changeable by consensus of members.
22. When sharing index entries outside local scope, strip or hash the PATH column. PATH is local convenience, not for export.
23. No automatic sharing. Every POST is an explicit agent decision. No background sync. No daemon.

## Recursive CAN

v1.5: the skill that teaches agents to build the network IS a node in the network.

v1.6: the scope that teaches agents to trust IS a trust boundary in the network. Scopes within scopes. Trust within trust. CAN within CAN.

## Roadmap

```
v1.3.2  DONE   naming + routing + bags + HUSH + scoped locate
v1.4    DONE   WHO: free machine-id + auth upgrade path
v1.5    DONE   SAW: say what you see, LOG what you saw
v1.6    NOW    WOT: web of trust, recursive scope
v1.7    GOGO   STACK: stack threads from root to FIN (merkle)
v1.8    LOL    expiry EOL gg a) game-over or b) insert-coin
v1.9    MEME   what else are ya gonna do?
v2.0    BUMP   humans in the CAN
```

Each version earns the next.

## References

- Paul Baran, On Distributed Communications (RAND, 1964)
- Phil Zimmermann, Pretty Good Privacy (PGP, 1991)
- Van Jacobson, A New Way to Look at Networking (Google Tech Talk, 2006)
- John Day, Recursive InterNetwork Architecture (RINA)
- Linus Torvalds, Git content-addressable object store
- Zooko's Triangle (CAN amplifies the petnaming solution)

## TL;DR

```
HASH thing
TIME when
WHO says
INDEX ()) <- in the CAN
OWN things.
SAW logs.
TRUST grows.
```
