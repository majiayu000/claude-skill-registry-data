---
name: building-command-line-interfaces
description: >-
  Guides applying the command-line interface contract while building or reviewing a tool — choosing an exit status,
  placing output on the right stream, and recognising which runtime default has to be overridden.
when_to_use: >-
  Use when building or changing a command-line entry point, adding a failure path or output mode, or reviewing a change
  that touches exit statuses, streams, or structured output.
compatibility: Requires read access to the repository's governance conventions.
---

# Building Command-Line Interfaces

[Command-Line Interface](../../../repo-governance/conventions/command-line-interface.md) fixes the contract and its
[eight modules](../../../repo-governance/conventions/command-line-interface/README.md) hold the rules. This skill covers
the judgement of applying them, not the rules themselves.

## Ask What the Caller May Conclude

Choosing an exit status is one question asked in one direction: **what may a caller conclude from this number?**

Work forward from the caller, never backward from the code path. A tempting status is usually a description of what went
wrong internally, which is the body's job. The number answers only whether the result can be trusted, and the hardest
case is the one worth slowing down for — deciding whether this path is a result the caller should act on, or a failure
to produce one. When unsure, ask whether a script that treated this as a real answer would then do something wrong. If
it would, the path is not a result.

## Assume the Runtime Is Wrong

Every runtime and every command framework breaks part of this contract by default, in a different place and for a
different reason. A tool is not conforming because nobody changed anything; it conforms because someone overrode a
default and left a test behind proving it stayed overridden.

The defaults worth checking first, because they are the ones that silently look fine:

- What the process reports when it panics, throws, or aborts — commonly a status the contract reserves for a result.
- What happens when a reader closes the pipe, which is the single most common real defect.
- What a death by signal reports, which frameworks tend to collapse into a result status.
- Which stream the usage text reaches on a failed invocation, since a framework often writes it through a stream the
  calling program supplies.

Set each one explicitly at construction rather than relying on it. A default that happens to be right today is not a
decision, and the next dependency upgrade is free to change it.

## Prefer the Dependency's Own Type

Before implementing a rule, check whether the argument parser already has it. A parser that ships a three-state colour
setting, a reserved help flag, or a usage exit status has already made the decision this contract asks for; exposing its
type is both less code and less to keep in step.

## Reviewing

- A new number in an exit path is the finding. Ask what code in the body would carry the same meaning.
- A diagnostic on standard output is the other finding, and a failed run that leaves anything on standard output is the
  same defect wearing a different hat.
- A structured output change needs its version considered, because something is parsing it.
