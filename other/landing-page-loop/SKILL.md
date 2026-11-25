---
name: landing-page-loop
description: "Build a fast, distinctive landing page with coding agents, the way the getedge.cc homepage was built: one design-token file that generates the CSS, black-and-white wireframes before any styling, a small static site generator instead of a framework, variants side by side, a blind second-model review loop with screenshots at desktop and phone width, a post-release roast, an idle CPU and GPU memory cost check, and an atomic release folder plus symlink deploy with one-command rollback. Use when someone wants a landing page or homepage that looks designed rather than generated, styled from their own example sites or Pinterest images, wants to redesign an existing site with an agent, or wants a repeatable build, review and ship loop for marketing pages."
---

# landing-page-loop

An agent can produce a landing page in minutes. Producing one that looks designed, loads
instantly and costs nothing at rest takes a loop: rules first, structure second, style third,
then a reviewer that has not seen your reasoning, then a cost check, then a release you can
undo in one second. You (the owner) make the calls; the agent builds, screenshots and measures.

**Done means:** the page is generated from tokens by one script, every version is its own
commit, the last blind review round scored 9.5/10 or ended in "agreed", every roast finding
was reproduced before it was fixed, idle CPU is ~0 at 10 s and 45 s, and the live URL returned
200 with the right `<title>` after the release flip.

## 0. Before anything: read what exists

Collect the current page, brand assets, copy the owner already approved, and the owner's
visual input: 3 to 5 example websites they like and/or a Pinterest moodboard (roughly 10 to 20
images). Put it all in one folder the agent reads before every design task. Those examples are
the taste reference for wireframes and styling; without them, stop and ask, do not invent a
style. Never invent positioning copy either; use the owner's words.

## 1. Design system first, then the page

- **One source of truth:** `tokens.json` holds colours, type scale, spacing, radii. A script
  turns it into `tokens.css` (custom properties). Pages never hard-code a colour or size.

  ```python
  # tokens.py: tokens.json -> tokens.css
  import json, pathlib
  t = json.loads(pathlib.Path("tokens.json").read_text())
  lines = [":root {"] + [f"  --{group}-{name}: {value};"
           for group, values in t.items() for name, value in values.items()] + ["}"]
  pathlib.Path("assets/tokens.css").write_text("\n".join(lines) + "\n")
  ```

- **Write the rules down, short:** one paper colour, one ink colour, one accent used only for
  buttons; one display face, large and tight, not bold; one h1; body 18 px at 35 to 55
  characters per line.
- **Write down what is forbidden.** Agents drift toward the same defaults. Name them:
  no purple gradients, no glow, no uppercase micro-labels, no section-card-section rhythm,
  no stock icons. This list does more for distinctiveness than any positive rule.
- **One reference HTML** that shows every rule in use. The agent opens it before every design
  task.

## 2. Black-and-white wireframes before any styling

New page or new section = 3 to 5 wireframes on one HTML page, black and white, each with a
one-line idea. The owner picks one, then styling starts. A styled first build anchors everyone
on colours and hides a wrong structure.

Prompt: `Make 3-5 black-and-white HTML wireframes for <section> on one page, one line each
saying what the idea is. No styling, no colour, real copy.`

## 3. Art and assets

- Commit to one art direction that runs through the page (for example one continuous
  illustrated landscape) instead of a stack of cards.
- Photos of people: square crop on the face, background faded to the paper colour, one
  consistent treatment (for example a halftone in the accent colour).
- Export everything as WebP (or AVIF) at the displayed size. Reference every asset with a
  content hash, `hero.webp?v=<8-char sha>`, so a CDN never serves a stale file.
- Small animated characters or marks as inline SVG, not video.

## 4. Build: a static generator, not a framework

- One script (`build.py` or `home.py`) assembles `index.html` from tokens, HTML partials,
  CSS and JS. Output is plain static files. No framework, no page builder, no client router.
- **Every version is its own commit** with a message that says what changed and why
  (`v13a6: one measured hero composition at every size`). The history is the design log.
- **Variants side by side:** build a, b, c (and d) of the risky part, show them together, the
  owner picks, the next round starts from the winner.
- **Preview before live:** a `noindex` preview with analytics off. Show before and after
  screenshots next to each other for every change.
- For design work, load a frontend design skill if one is available, and still compare its
  result against a plain run: taste skills help looks, plain pages often convert as well.

## 5. Review loop: blind, scored, and owned by you

Every round:

1. Screenshots at 1440 px and 390 px wide, full page, plus a scroll recording turned into a
   contact sheet. Put the owner's example sites or moodboard next to them.
2. A second model reviews **blind**: it gets the images and the goal, not your reasoning or
   the previous scores. It returns a score out of 10 and the top fixes.
3. Fix, rebuild, repeat until 9.5/10 or the reviewer says "agreed".

The reviewer will contradict itself (round 4 asking for the opposite of round 3). You decide,
not the reviewer. Write the decision in the commit message so the next round does not undo it.

After each release, ask a browsing model, word for word:
`fully test and roast <url>, especially ui/ux`, then `ok, go again deep`.
It finds real bugs. Reproduce every finding yourself before fixing it; drop what you cannot
reproduce.

Then read the page yourself as a visitor, full size, phone and desktop: who lands here, what
do they understand in 5 seconds, what do they click.

## 6. Cost check: measure cost, not fps

Frame rate on a fast laptop hides a page that burns CPU forever. Measure in headless Chrome
(or DevTools) after the page settles:

- **Idle CPU** of the renderer at 10 s and at 45 s after load, no input: must be ~0 %.
- **Running animations at rest:** `document.getAnimations().filter(a => a.playState === 'running').length` must be 0.
- **Long tasks** while scrolling with 4x CPU throttling.
- **GPU layer memory** at 2x device pixel ratio (DevTools Layers panel), and **MB transferred**.

Fixes that usually get you there:

- No parallax on the main thread; move art with `transform: translate3d` only while scrolling,
  and write it back flat a few hundred ms after scrolling stops so resting art holds no GPU layer.
- No infinite animations. Ambient motion pauses after ~25 s idle and resumes where it stopped.
- No `will-change` on static art; scroll reveals end on a held frame instead of a live animation.
- Lazy-load films and heavy images near the viewport only.

Record the numbers in the commit message (before and after).

## 7. Release: atomic folder, symlink flip, instant rollback

- Static files behind any web server or CDN. Each release is its own folder,
  `releases/<YYYYMMDD-name>/`; the server root is a symlink `current` pointing at one of them.
- Build the new folder completely (hardlink-copy the previous release, then sync the new
  files over it so unchanged files cost nothing), verify it byte for byte against the commit,
  then flip the symlink atomically: `ln -sfn releases/<id> current.tmp && mv -T current.tmp current`.
- Rollback = point `current` at the previous folder. Print that command before and after the flip.
- Push the commit to your main branch **before** the flip, so a parallel deploy from main cannot
  drop your change. After the flip, `curl` the live URL: expect 200 and the right `<title>`.

## Checklist

- [ ] owner's example sites and/or Pinterest moodboard in the reference folder before any design
- [ ] tokens.json -> tokens.css by script; rules and forbidden list written down
- [ ] owner picked a black-and-white wireframe before styling
- [ ] assets WebP at display size, hashed URLs
- [ ] one generator script, one commit per version, variants side by side
- [ ] blind review at 1440 and 390 until 9.5/10 or agreed; decisions in commit messages
- [ ] post-release roast; every finding reproduced before fixing
- [ ] idle CPU ~0 at 10 s and 45 s, 0 running animations at rest, long tasks checked at 4x
- [ ] release folder + symlink flip, commit pushed first, live URL 200 with the right title
