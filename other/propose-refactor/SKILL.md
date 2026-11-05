---
name: propose-refactor
description: propose a refactor plan for an area
argument-hint: "<area>"
disable-model-invocation: true
---

propose how to make an area simpler, more straightforward and robust, and refactor away traces of growing pains. this skill ends at the plan; implementation is a separate request

if no area was given, ask "What area is in scope?" and wait for the answer

the area is the centre of the sweep, not a fence: follow a finding into callers, shared code or contracts when the fix needs it, and say where it crosses the line

when you are sure it is the right thing, contracts, API responses and behaviour are open to change; every point that changes behaviour states the before and after

sub-agents leave the codebase untouched: the mapper writes only `map.md`, and the others return findings as their final response

## steps

1. map: spawn 1 sub-agent to write `playground/propose-refactor/<area-slug>/map.md`: entry points (routes, jobs, pages), contracts the area exposes (API shapes, types, events), callers outside the area, compatibility branches and feature flags, and hot spots from recent `git log`. done when every entry point and contract is listed with its file

2. lenses: spawn 4 sub-agents, 1 per lens, in parallel as far as free agent slots allow. each reads the map, then the code, and returns twice its quota in the [point format](#point-format):
   - small cuts (3): small changes that drop code or compatibility branches, or reduce cognitive complexity
   - type safety (3)
   - ponytail (3): apply `/ponytail`
   - architecture (2): read and follow [/improve-codebase-architecture](../improve-codebase-architecture/SKILL.md) through its explore step, exploring directly in place of its nested sub-agent, and return its candidates in the point format in place of the HTML report and grilling loop

   done when all 4 have returned

3. merge: check each finding's claims against the code, consolidate overlapping findings into 1 point that counts toward every category it serves, and add 1 bold change of your own drawn from the whole picture. done when every kept point is verified and each category has its quota (3, 3, 3, 2, 1)

4. second opinion: give a `/cross-harness-sub-agent` the map and the merged list, and ask what it would cut, add or rank differently. done when each piece of pushback is adopted or rejected with a reason checked against the code

5. report, with every point ranked by ROI (payoff for effort), highest first:
   - 80/20 plan: the points with the best ROI
   - extended list: the remaining points, for going 1 step further

## point format

- title and the categories it serves
- the change, and what it removes
- behaviour: before -> after, or "none"
- effort: S, M or L
