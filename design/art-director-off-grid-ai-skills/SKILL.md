---
name: art-director
description: Hold every screen, scene, camera and animation in your game to the bar of a polished shipped game, with no half-built features, no repeated motion and a voice that fits the world. Use before designing, building or reviewing any game screen, HUD, menu, scene, camera, crowd or animation, or when the user says "polish the game", "the game looks cheap" or "art-director". For apps that are not games, use make-it-look-expensive.
---

# Make the game look great

Find the project's own bar first: the art target images, the UI layout doc, the design doc and any "fun bar" or pillars list. Where this skill says "the approved layout" or "the look", use those. If they don't exist, ask the user for two or three reference games and write the bar down before you build.

0. **Never lose functionality.** A change keeps everything the game already does, settings included. If something would be lost, tell the user first, with the option that keeps it.
1. **No shoddy work.** Build what a polished game in this genre ships: every control, state and next step. A half-built feature is a regression.
2. **Finesse is the whole experience.** Type, spacing, labels, motion and feel get the same care as systems. Nothing clipped, overlapping, flush to an edge or unreadable.
3. **The look.** Match the reference games and target images the user chose, at their richness, never cheaper or more toy-like than intended. Keep the agreed camera (for example a low oblique camera, never top-down, if that is the style). Characters use animations that fit the place (farm work in fields, haggling in a market, prayer in a church).
4. **The interface.** Follow the approved layout in the UI doc: where each panel lives, the fonts, the panel style, one accent colour, a warning colour used only for real loss. Labels sit clearly on screen and never pile up. If there is no UI doc, propose one and get a yes.
5. **Loops.** After any result or failure, the next action is right there. A blocked state says why in one line and what to do. Every panel and page is a place: Back (Esc) returns exactly where you were.
6. **Smart defaults.** Decide from what the game already knows. Ask the player once, where the choice comes up, with a recommendation.
7. **The world never stops on its own.** No screen freezes. Things build in before the player's eyes. The game pauses only where the design says it should, and only until the player acts. A new game starts when it is ready, not on a timer.
8. **The world's voice.** Copy fits the setting and is plain and specific: "Outlaws come for you", not "Enemy spawned". Characters speak to their station and role.
9. **Variety and reaction, never repetition.** Use every animation you have: no one clip on repeat, no character doing the same thing twice running, no crowd moving as one. Every action gets a fitting reaction (a strike is blocked, dodged or taken; a hit reacts to where it lands; a fall goes the way the blow drives), so the world answers what happens in it. Before shipping any scene, list the animations the asset library holds for it and use them.
10. **Show problems on the shot, not in words.** When you find what is wrong with a screen or scene, mark it on the review page (`show-me` section 6: a numbered box per problem, at most five), send the marked-up image, then ask the one question. No review tool? Draw the boxes on a copy of the screenshot and share that.
11. **Every platform.** Name the main platform first. When a change can't work on another platform the game ships to (Windows, macOS, Linux, consoles, mobile, web), name what it misses.
12. **Pass the fun bar.** If the design doc has a fun bar, score the change against every line before building and before shipping, with counts from a real play session where they exist. Story, events and dialogue are held to it like any screen. A line that drops is a regression. If there is no fun bar, suggest one (see `playtest` step 5).
