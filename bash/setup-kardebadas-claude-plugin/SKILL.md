---
name: setup
description: Use when superb's skills need their dependencies installed or checked — "set up superb", "install the dependencies", "why does pipeline say superpowers is missing", after a fresh plugin install, or on a new machine. Also use when a skill fails complaining that a superpowers sub-skill cannot be found.
argument-hint: "[check]"
---

# Setup

## Overview

Gets `superb`'s dependencies in place, and says plainly what it could not do.

`superb:craft` needs nothing unless its optional browser UI is used.
`superb:pipeline` and `superb:bug-fix` both compose
[superpowers](https://github.com/obra/superpowers) and do not run without it.
Pipeline's standard-library state helper also requires Python 3.11+; Craft's
browser UI remains separately compatible with Python 3.9+.

## Step 1 — Run the check. Always, first.

Run `./check-deps.sh` from this skill's directory. It reports one fact per
line, and **its exit code is the instruction**:

| Exit | Meaning | What you do |
| ---- | ------- | ----------- |
| `0` | Everything required is satisfied | Report it. Stop. |
| `1` | Something is `MISSING` or `DISABLED` | Run the `ACTION` lines, then re-check. |
| `2` | **The state could not be determined** | **Do not install anything.** Report what it said. |

```
HARNESS   claude | codex | unknown
REQUIRED  <name>  OK | MISSING | DISABLED | ERROR | UNKNOWN   <detail>
OPTIONAL  <name>  OK | MISSING                                <detail>
MARKET    <name>  OK | MISSING
ACTION    <the command that fixes the line above it>
NOTE      <something you need to know that is not actionable>
```

If `check` was passed as the argument, report and stop regardless of the exit
code. With no argument, continue to Step 2.

**Exit 2 is not a soft failure.** `ERROR` means the query failed, not that the
dependency is absent — a failed `claude plugin list` says nothing about what is
installed. Installing on an `ERROR` is how a present, working dependency gets
reinstalled over the top of itself. `UNKNOWN` means the same for a different
reason: nothing could look. In both cases report the `NOTE` lines and stop.

`REQUIRED pipeline-python MISSING` is deliberately not followed by an
`ACTION`: report that Pipeline needs Python 3.11+ and stop. Never install or
upgrade a language runtime on the user's behalf.

## Step 2 — Act, where you can

**Only on exit 1, and only on Claude Code.** Run the `ACTION` lines in the
order they were printed — a marketplace has to exist before a plugin installs
from it.

**`DISABLED` is not `MISSING`.** An installed-but-disabled plugin looks present
to anything matching on the name, and its skills never load. The action is
`claude plugin enable superpowers`; reinstalling is not the fix.

**Then re-run `check-deps.sh` and report its actual output.** An install that
printed no error has not been verified; the second run is the verification. If
the re-run does not reach exit `0`, say so and stop — **do not run the same
actions again.** A second identical attempt is how a loop starts, and the
script already told you it did not work.

## Step 3 — What you cannot do, said plainly

**On Codex** (`HARNESS codex`), plugins install through an interactive picker.
Nothing here can run it, and nothing here can inspect it either — which is why
the state is `UNKNOWN` rather than `MISSING`. Report it, then hand over:

> Open `/plugins`, search for `superpowers`, and select Install Plugin.

**On `HARNESS unknown`**, neither CLI was found. Do not guess which harness this
is and do not run installer commands on spec. Report the output, name the two
supported routes, and let the user say which applies.

**Never write to `~/.codex/config.toml`**, or anywhere else under a user's
config. An install writing into user config is exactly what superpowers' own
porting guide forbids.

`superb:pipeline` and `superb:bug-fix` both degrade rather than break when a
subagent mechanism is absent, so this is a limitation to state, not an error to
resolve.

## Optional, and genuinely optional

| Dependency | Used by | Without it |
| ---------- | ------- | ---------- |
| Python 3.9+ | `superb:craft`'s browser UI | Falls back to the `CRAFT.md` questionnaire; nothing lost but the browser |

Report it. **Never install a language runtime to satisfy Craft's optional
report** — that is a decision with consequences well past this plugin, and the
browser fallback means the optional dependency blocks nothing.

The script deliberately does not check whether the user's project is a git
repository: it runs from the plugin's install directory, so it would always be
describing the wrong directory. `superb:pipeline` establishes that itself, where
it can actually see the project.

## Red flags — STOP

- About to install on exit `2` → the script could not tell whether it is already
  there. You are about to reinstall something that may be working.
- About to reinstall something reported `DISABLED` → enable it.
- About to re-run the same `ACTION` lines after a failed re-check → that is a
  loop. Report the output instead.
- About to report success without re-running the check → the second run is the
  only evidence you have.
- About to edit `~/.codex/config.toml`, or any file under a user's config → not
  yours to write.
- About to run `git init` or install a runtime → out of scope, and not asked for.
- About to say "dependencies installed" on Codex or `unknown` → you could not
  check, let alone install. Say that instead.
