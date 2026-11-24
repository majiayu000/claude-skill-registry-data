---
name: laws-of-ux
description: "Fitts, Hick, Miller and Jakob applied to real screens."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, ux]
    category: web
    related_skills: [web-design, usability-heuristics]
    web_designer_stages: [ia, wireframe]
---

# Laws of UX Skill

Apply psychology-derived rules to real screens: Fitts, Hick, Miller, Jakob and Von Restorff. This skill covers sizing targets, limiting choices, chunking content, and deciding whether to follow a platform convention. It does not cover Nielsen's 10 heuristics, which have their own skill, and it does not cover visual styling. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- When sizing targets, limiting choices, chunking content, or deciding whether to follow a platform convention.
- In IA, when deciding how many items a menu or a screen should offer.
- In wireframing, when placing the primary action and chunking long content.
- When a destructive action must be kept away from the primary action.
- When one item on a page must be the one the visitor remembers.
- Not as a reason to break a convention without cause: Jakob's Law favours the familiar unless there is a reason to depart.
- Not as exact numbers: the laws describe tendencies to design with, not formulas to compute a layout from.

## Prerequisites

- The run is active and the coordinator loaded this skill for its stage or stages.
- The sitemap and the top tasks are known, so choices and chunks follow real tasks.
- The wireframe is in progress or in review, so target sizes and placements can still change cheaply.
- The primary action per screen is named, so Fitts's Law has a target to size and place.

## How to Run

1. Place primary actions large and close to where the visitor already is; place destructive actions smaller and further away.
   - The primary call to action is the easiest thing on the screen to hit.
   - A destructive action is never as large or as close as the primary one.
2. Limit options per screen, applying Hick's Law: fewer, clearer choices decide faster.
   - Cut options that serve no top task; group the rest so the choice is between few clear groups.
3. Chunk long content into groups of about 7 items, applying Miller's Law.
   - A list, a form and a set of cards each chunk into groups the visitor can hold together.
4. Follow familiar conventions for basic tasks, applying Jakob's Law; break a convention only with a named reason.
   - Sign-in, search, checkout and navigation follow the patterns visitors already know.
   - A departure names its reason in the stage record; a departure with no reason is reverted.
5. Make the one item that must be remembered distinct, applying Von Restorff.
   - The distinct item differs in size, colour or position — one difference, not all three at once.
6. Record the target sizes, choice counts, chunks and convention decisions in the stage record.
   - Record the reason for every convention departure beside the departure itself.
7. Re-check after any fix, and record what changed.
   - A changed target, chunk or convention is re-checked against its law before the stage closes.
   - The sizes and counts recorded are the ones in the final wireframe, not earlier drafts.

## Quick Reference

- Fitts's Law: larger and closer targets are faster to hit.
- Hick's Law: more choices mean slower decisions.
- Miller's Law: chunking, about 7 items per chunk.
- Jakob's Law: users expect your site to work like others they know.
- Von Restorff: distinct items are remembered.
- Source collection: Laws of UX (Yablonski).
- Primary actions: large and close; destructive actions: smaller and further.
- Choices: few and clear per screen; more choices mean slower decisions.
- Chunking: groups of about 7 items, following the content.
- Conventions: familiar for basic tasks; a departure names its reason.
- Memory: the distinct item is the one remembered.
- Result: the primary CTA is the easiest thing to hit, and no basic task needs a new convention.
- Source collection: Laws of UX (Yablonski).

## Procedure

### 1. What it is

Psychology-derived rules collected in Laws of UX (Yablonski): Fitts's Law (larger/closer targets are faster to hit), Hick's Law (more choices = slower decisions), Miller's Law (chunking, ~7 items), Jakob's Law (users expect your site to work like others they know), Von Restorff (distinct items are remembered).

### 2. How Hermes applies it

Hermes makes primary actions large and close, destructive actions smaller/further, limits options per screen, chunks long content, and follows familiar conventions unless there is a reason to break them.

### 3. What it returns to the stage

- `ia` stage record: `sitemap` and `navigation` carry the choice limits — how many items each menu and screen offers — and `flows` carry the chunked task steps.
- `wireframe` stage record: `pages` carries the target sizes and placements per page — the primary action large and close, destructive actions smaller and further, content chunked into groups of about 7.

### 4. Good looks like

Primary CTA is the easiest thing to hit; menus offer few, clear choices; nothing requires learning a new convention to complete a basic task.

## Pitfalls

- A primary action that is small or far away: the most important target is the hardest to hit, against Fitts's Law.
- A destructive action as large and close as the primary one: the easiest thing to hit is the one that cannot be undone.
- Too many choices on one screen: Hick's Law says decisions slow down, and visitors stall or leave.
- Long unchunked content: Miller's Law says groups of about 7 are held together; a wall of 20 items is not.
- A novel convention for a basic task: Jakob's Law says visitors bring habits from other sites; a new pattern for sign-in or checkout is a cost with no benefit.
- No distinct item where one must be remembered: Von Restorff says the distinct item is the one recalled, so a page where everything looks alike leaves nothing recalled.
- Chunking by sevens for its own sake: groups of about 7 follow the content, they do not chop a natural group of 5 or 9 into arbitrary sevens.
- A convention followed where it harms the task: Jakob's Law favours the familiar, but a familiar pattern that hides the primary action is still wrong.
- The distinct item overdone: everything made distinct means nothing is distinct, and Von Restorff stops working.

## Verification

- The primary CTA is the largest and closest target on its screen; destructive actions are smaller and further.
- Each menu and screen offers few, clear choices; no screen overloads the visitor with options.
- Long content is chunked into groups of about 7 items.
- Basic tasks follow familiar conventions; every departure from a convention names its reason.
- The one item that must be remembered is distinct from its neighbours.
- Chunks follow the content; no natural group is chopped into arbitrary sevens.
- The distinct item differs by one difference — size, colour or position — not by all three at once.
- A familiar pattern that hides the primary action is not kept for familiarity's sake.
- Choice limits and chunked steps are recorded in the IA stage record, and target sizes in the wireframe record.
- The wireframe record carries the final target sizes and placements, not earlier drafts.
- The visual judger checks target prominence and placement; the responsive judger checks the same at mobile widths. The skill does the work and the judgers check it; the skill never grades its own output.

## Coordinator wiring

Loaded by stages: ia, wireframe. Returns: `ia.navigation` (choice limits per menu and screen); `ia.flows` (chunked task steps); `wireframe.pages` (target sizes and placements per page). Judger boundary: visual judger checks target prominence and placement; responsive judger checks them at mobile widths.
