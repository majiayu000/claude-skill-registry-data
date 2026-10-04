---
name: x4-balance
description: Ground a balance or stat-tuning discussion in measured values before proposing any change. Opens by naming which instrument answers which question and what a zero from each one means, so the numeric tools get reached for instead of recalled. Use when the user asks to rebalance, tune, compare or sanity-check stats (damage, range, speed, hull, shields, price, production), asks "is this overpowered / underpowered / consistent with the rest", or wants a proposed value checked before it is written. Enforces the three-values rule and the in-sector vs out-of-sector check.
allowed-tools: Bash, Read, Grep
---

Balance work fails in a specific way: a number gets quoted from a file, from a mod page, or
from memory, and everything downstream inherits it. The tools that prevent that exist and
are the ones least often reached for — so this skill starts by putting them in front of you.

Run tools via uv from the tool dir:
`cd $CLAUDE_PROJECT_DIR/tools/x4validate && uv run --python 3.13 <tool> <args>`

## Step 0 — state the route BEFORE the sweep

Before the first query, write one line: **the question · the instrument · what a zero would
mean.** A balance investigation is a long chain of calls, and a wrong instrument at step 2
is invisible by step 9 because every later number is consistent with it. Stating the route
makes a misroute visible in the conversation instead of buried in a tool result.

## The instrument card

| the question you are actually asking | reach for | what a ZERO / empty result means |
|---|---|---|
| what does the game **currently** use for this value? | `x4effective show <kind> <id>` · `x4effective attr <kind> <prop>` (that prop across every entity of the kind) | the entity is not in the effective tree — check the kind, then whether anything supplies it |
| **who set it**, and did a mod win? | `x4effective who-sets <kind> <id> <prop>` | nothing overrides it; the value is vanilla |
| what does **vanilla** ship, independent of the modlist? | `x4effective` built with no overlays, or read the base file | a claim about vanilla is NOT refuted by the effective tree disagreeing — different tiers |
| how does this value sit against **comparable content**? | `x4stats wares <mod>` · `x4stats macro <path/to/*_macro.xml>` | ⚠ advisory, never a verdict — it grounds the discussion, it does not settle it |
| is this entity a **near-duplicate** of one already installed? | `x4similar --candidate <mod>` | no near-duplicate found *within its class+purpose filter* — not "nothing similar exists" |
| does the change **collide** with the installed set? | `x4compat check <mod>` | no collision over the effective tree; load order is the engine's MEASURED rule (signature and apply order, in-game probe 2026-09-26; the profile root applies after the game root, and a dependency does not cross between them) -- the Steam Workshop root is unmeasured |
| do the selectors actually **resolve**? | `x4validate <mod>` (add `--tier b` if it touches another mod) | run it — a `sel=` that matches nothing is the cheapest and most expensive bug here |
| what **values exist across the corpus** for this attribute? | BaseX `ask.py --db x4eff` | a bare zero is a lead; only `ask.py` with a coverage denominator makes it a finding |

⚠ **`x4stats` and `x4similar` are the two instruments most often named and least often run.**
They are the balance-specific ones. If a balance discussion finishes without either being
invoked, say so out loud rather than letting it pass.

## The three values — mandatory, no bare numbers

For every value you propose changing, state all four:

| | |
|---|---|
| **vanilla** | what base+DLC ship |
| **effective** | what it is right now, with the winning source NAMED (or "no override, still vanilla") |
| **proposed** | the new value |
| **in-game effect** | what the player sees or feels — direction, rough magnitude, what it touches. Not "sets X to N". |

A selector written against the *vanilla* value silently matches nothing when something else
already changed it. That is the single most expensive bug class here, and the three-values
rule exists to catch it before the edit, not after the test cycle.

## The in-sector / out-of-sector check — mandatory

Name the mechanic that balances the change **in sector**, then state whether **out of sector**
models it. OOS is arithmetic: a factor absent from the formula does not exist. If a change's
cost is paid by a mechanic — interception, dodging, positioning, turret traverse — ask what
pays that cost OOS. Often nothing does, and the change is IS-only.

Verify against the actual OOS scripts rather than reasoning from what IS does. An assumed
formula is an ASSUMED-tier claim.

## Label the regime — every combat claim says IS, OOS, or BOTH

A combat number without a regime label is a half-finding wearing the grammar of a whole one.
State the label in the sentence that carries the number.

| label | means |
|---|---|
| **IS** | in-sector only: physics, projectile travel, turret traverse, interception, RNG. |
| **OOS** | out-of-sector only: arithmetic in `aiscripts/fight.attack.object.*`. |
| **BOTH** | verified separately in each — two measurements, never one generalised. |
| **UNKNOWN** | say so. It is valid, and common. |

**How to tell which you are reading, mechanically:** in the attack aiscripts `<attention min="visible">`
is the IN-SECTOR branch and `<attention min="unknown">` is OUT OF SECTOR. A property read inside
one is scoped to that regime and nothing else — check the enclosing block before quoting any
formula from those files.

**A stat's VALUE is usually engine-wide; its USE usually is not.** Different claims, separate
labels: measuring the number tells you nothing about which regime consumes it. A day of work
once derived a spoof curve to float precision before the question *"is this IS and OOS?"* found
**17 reads, ZERO inside `attention min="visible"`** — the transform is engine-wide, every
formula on it out-of-sector only.

⚠ **Scope a corpus claim PACKED-INCLUSIVE before recording it.** That measurement first read
*"2 places across 399 vanilla documents"* — loose-vanilla only, blind to a packed mod reading the
stat in sector. Re-run over 963 documents it found a third reader (`combat_tactics_script`).

**Two more requirements before the change:** check **who does not have the thing** (a gap tactics
cover IS can be decisive OOS, where arithmetic does not), and **pin OOS first** — it is crunchable,
IS is not, so treat IS as the variable.

## Before proposing

- Check the design charter first — *"the game does X"* is **evidence, never justification**.
- Label every claim's tier: MEASURED (with the denominator) · READ (file and line) · INFERRED
  (hedged out loud) · ASSUMED (say what would confirm it).
- State a confidence level and the assumptions under it. Below 90%, the next step is a
  measurement, not a change.
- A destructive change — removing content, stripping attributes — needs explicit approval and
  a higher evidence bar, whatever the confidence.

## Output shape

Lead with the table of three values. Then the IS/OOS reading. Then the instruments actually
run and what each returned, including the ones that returned nothing. Close with the
confidence level and what would raise it.
