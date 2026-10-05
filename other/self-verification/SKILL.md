---
name: self-verification
description: Use to prevent premature completion claims and require evidence-backed status reporting for PonyBunny work.
---

# Self Verification

## Use this skill when
- reporting implementation progress
- deciding whether something is complete
- reviewing whether evidence is sufficient
- preventing overclaiming

## Goals
- stop false completion claims
- separate coding from proof
- improve reporting precision
- encourage explicit evidence

## Rules
- implemented does not equal verified
- changed code does not prove correctness
- absence of visible error does not prove success
- every behavioural claim needs an evidence path

## Process
1. List the claimed outcomes.
2. For each claim, identify actual evidence.
3. Mark unsupported claims as unverified.
4. State what still needs checking.
5. Report status using approved status words.

## Output contract
Return:
- claims made
- evidence found
- unsupported claims
- correct status labels
- recommended next verification step
