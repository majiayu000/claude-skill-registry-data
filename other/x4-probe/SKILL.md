---
name: x4-probe
description: Use when building a temporary in-game X4 instrument to answer an empirical question - a probe, test harness, diagnostic mod, or MD/aiscript that spawns ships, applies damage, or logs engine state. Also use when an in-game test produced no output, fired but measured nothing, or returned a clean null you are tempted to write down as a result.
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Building an in-game probe

## Overview

A probe is a throwaway mod that makes the running engine answer a question the files cannot.

**The engine is the only oracle for engine behaviour, and every play session costs the user real
time.** A probe that does not load, does not fire, or measures the wrong thing spends that time and
returns nothing. The order below exists because each step is cheaper than the one after it.

**Core principle: a schema tells you what is well-formed; it cannot tell you what is wired up.**
Copy a construct the engine demonstrably loads. Compose only what you have verified.

## When to use

- Building any temporary mod whose purpose is to MEASURE rather than to change the game
- Instrumenting an existing script to log what it computed
- An in-game test returned nothing and you cannot tell which of load / trigger / logic failed
- You are about to ask the user to launch the game

**Not for:** shipped content, balance patches, or anything that stays installed. That is ordinary
mod work.

## 1. Route before building

Does a probe already instrument this surface? Extending one costs nothing and inherits its proven
wiring.

    ls "$X4_MODS"
    grep -rl "debugchance\|savedvariable" "$X4_MODS"

**Also ask whether the question needs a mod at all.** A live query channel, a save-file reader, or a
log triage may answer it with no deployment and no launch.

Deploying into the user's game install changes their environment. It is their call, and a peer
asking is not that approval.

## 2. Which schema governs this file?

**This is the step that fails most often, and it fails silently.** MD and aiscripts share a large
action vocabulary through `common.xsd` but they do **not** share each other's element sets. An
element that is ordinary in one is undefined in the other, and the engine rejects the file.

| file lives in | governed by |
|---|---|
| `md/` | `md.xsd` + `common.xsd` |
| `aiscripts/` | `aiscripts.xsd` + `common.xsd` |

**For EVERY element you write, run the check. Not from memory - from the file:**

    cd "$X4_REFERENCE/libraries"
    for el in wait delay do_while write_to_logbook show_notification create_ship; do
      printf "%-22s md:%s  ai:%s  common:%s\n" "$el" \
        "$(grep -c "xs:element name=\"$el\"" md.xsd)" \
        "$(grep -c "xs:element name=\"$el\"" aiscripts.xsd)" \
        "$(grep -c "xs:element name=\"$el\"" common.xsd)"
    done

**0 in the governing schema means the element does not exist there.** It being obvious,
conventional, or present in your memory does not change that.

**Then check REQUIRED attributes for every element you use:**

    awk '/xs:element name="write_to_logbook"/,/<\/xs:element>/' common.xsd | grep 'use="required"'

A missing required attribute fails the file exactly like a missing element.

**Confirm against real usage, with a denominator:**

    grep -l "<wait" "$X4_REFERENCE"/md/*.xml | wc -l
    grep -l "<wait" "$X4_REFERENCE"/aiscripts/*.xml | wc -l

Zero of hundreds is an answer. One of hundreds is a lead worth reading.

## 3. Copy, do not compose

Search in this order and **cite the file and line in a comment inside the probe**:

1. The reference tree's `md/` and `aiscripts/` - vanilla, the closest analogue for anything the base
   game itself does.
2. **INSTALLED MODS** - the tier that is easy to forget and is often the *better* source, because
   mods solve MODDER problems vanilla never had: spawn a test fight, force a loadout, drive an
   experiment. Search packed-inclusive; a loose-file grep misses most of the corpus.

Paste the working example and change the values.

**The parts you think are routine are the parts that bite**, because you will verify what looks
risky and compose what looks obvious.

## 4. Prove it RAN before debugging what it DID

A probe that produces no output has three indistinguishable causes. Eliminate them in order;
debugging the third while the first is true is unbounded.

| # | question | proof |
|---|---|---|
| 1 | did it LOAD? | a line in the engine log naming the file. Absent = not installed or not enabled, and nothing after it matters |
| 2 | did it TRIGGER? | an unconditional marker as the **first action**, before any logic |
| 3 | can it RECORD? | a variable self-test **before anything is created** - set a value, read it back, abort if it does not survive |
| 4 | did the logic work? | only now |

**The marker is not optional and it goes first.** If it is missing, the trigger is wrong, not the
logic.

**Rung 3 is the one people leave out, and it is the only rung whose absence causes DAMAGE.** Loading
and triggering fail harmlessly. Variable binding fails *after* the side effects that produced the
value, so the run leaves debris - and the cleanup cannot run, because the handles needed to undo the
work are exactly what failed to bind.

**Prove you can hold a handle before you make one.** A self-test costs one line, can leave no debris,
and converts that failure into a zero-cost one. A probe that cannot name what it created cannot clean
it up.

Cue triggering is a runtime fact no schema expresses. Confirm which event actually fires in the
situation you are testing - some fire only on a save load and are silent on a new game, with no
error and no trace.

## 5. State what makes a run VOID - before running it

Write the preconditions down, log them, and read them first. **A run that fails its precondition is
void, not a null result.**

Log at minimum: every object the experiment depends on, the distance between them if proximity
matters, and the actual value of anything you assumed a spawn would set.

**A spawn that silently did not do what you asked is the most common void cause.** Read back what
you actually got rather than trusting the request.

## 6. The control must be able to FAIL - and the subject must contain the mechanism

Two separate checks. Passing the first and skipping the second produces a clean null that looks like
a finding.

- **Could the control have gone red?** If no realistic outcome would have failed it, it is
  decoration.
- **Does the subject contain the mechanism at all?** A control firing proves the TREATMENT was
  applied. It never proves the subject can express the effect.

**Ask out loud: "what, concretely, would have made this go red?"** If the answer is "nothing that
could actually have occurred", it is not a check.

**To have zero of something you must REMOVE it, not merely decline to add it.** A generated loadout
supplies its own ammo and equipment, so a "none" arm that simply omits them is not a control.

## 7. Report three ways

    <show_notification text="'...'"/>
    <write_to_logbook category="..." title="'...'"/>
    <debug_text text="'MARKER key=' + $value" chance="100"/>

Transient, persistent, machine-parseable. The player does not read the debug log while playing, and
a missed popup is a lost session - the logbook is the only channel that survives.

## 8. Timings from a landmark the user can SEE

State elapsed time from something observable - "4m30s after the save finishes loading" - never from
process start, and never a figure you have not summed from the delays you actually wrote.

Tell the user how long to stay in game and what the first visible sign of life is, so a dead probe is
obvious in seconds rather than at the end.

## 9. Validate, then let the engine be the first real check

    x4validate <mod>
    x4validate <mod> --update

**The MD/aiscript SCHEMA pass is GATED behind `--update`.** A default run reports OK on a script it
never schema-checked.

After any hand edit, re-parse the XML: `--` is illegal inside an XML comment and makes a file not
well-formed.

**Static validation cannot see runtime wiring.** For a new script the engine log is the FIRST real
check, not the last.

## Quick reference

| step | cost if skipped |
|---|---|
| route first | rebuilding something that already exists |
| schema check per element | the probe does not load; one wasted session |
| copy, do not compose | the routine-looking parts fail |
| load and trigger markers | cannot tell which of three failures happened |
| binding self-test before creating | the run leaves debris it has no handle to clean up |
| void conditions | a void run gets written down as a null result |
| control that can fail | a clean null becomes a false finding |
| three reporting channels | the result exists only where nobody looks |
| `--update` | a clean validate on a file that was never schema-checked |

## Common mistakes

| mistake | reality |
|---|---|
| using an element from the wrong script type | MD and aiscripts share `common.xsd`, not each other's elements. Check the governing schema. |
| omitting a required attribute | `use="required"` fails the file exactly like a bad element name |
| "it is conventional, I do not need to check" | Convention is where composed bugs live. The check is one grep. |
| searching only the reference tree | Installed mods solve modder problems vanilla never had, and are proven in THIS version |
| a cue at t=0 that touches the WORLD | `player.entity` and `player.sector` are NULL at t=0.00. Static macro reads are fine there; spawning is not. Wait on `md.Setup.Start` (98 of 382 vanilla md documents do, measured 2026-09-20 over base+DLC) |
| composing the variable plumbing after copying the action | The action is what looks risky, so you check it. The plumbing looks routine, so you invent it - and it is what fails. Copy BOTH. |
| treating a namespace declaration as an address | Declaring where variables live is not the same as naming that place. Check how the analogue you copied *reads its own variables back*, not just how it declares them. |
| creating things before proving you can hold them | The failure lands after the side effects. Self-test the binding first (rung 3 above). |
| a cleanup path that needs the handles that failed | Destroy on the abort path too, guarded per handle, so a partial bind still cleans up what it got |
| trusting that a spawn did what you asked | Read the resulting value back and log it |
| a "no X" arm that merely omits X | Generated loadouts supply their own. Remove it explicitly. |
| a default validate run | The schema pass is behind `--update` |
| reporting only to the debug log | Nobody reads it during play |

## Red flags - stop

- You are about to write an element you have not grepped against the governing schema
- Your probe creates something in the world before it has proven it can store a reference
- You copied the risky-looking action and wrote the surrounding variable handling from memory
- You are calling code "complete enough to deploy" while listing parts you did not verify
- Your control could not have failed under any realistic outcome
- You cannot say what would make the run void
- You are about to ask for a launch and cannot say what the first visible sign of life is
- A run returned little and you are reaching for "consistent with our model"

**Being honest that you did not verify something does not make shipping it safe.** Verify it, or
mark the artifact as not ready.

## Real-world impact

A test harness composed from the schema rather than copied cost **three play sessions**, none of them
spent on the experiment: engine-rejected script constructs, a cue that never fired because the chosen
event only fires on a save load, and a spawned ship that was inert because it had no pilot.

A later baseline exercise produced a probe described as deployable that would not have loaded at all
- two schema violations, both in elements the author had explicitly flagged as unverified. Honesty
about the uncertainty did not prevent shipping it.

A third probe loaded, triggered, found the world ready and **created all four of its test subjects** -
then failed to bind a single one to a variable, because the namespace it wrote to did not exist. Every
element had been schema-checked and the spawn action itself was copied from a working example; the
*variable handling around it* was composed from memory. The engine's own error named the objects it
had already built. Cost: four unwanted player-owned ships persisted into a save, uncleanable, because
the cleanup needed exactly the handles that had failed to bind.
