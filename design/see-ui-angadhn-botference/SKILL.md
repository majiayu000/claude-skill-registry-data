---
name: see-ui
description: Look at any web UI you build or change — render it headless with `botference see` and read the screenshots — because layout and design failures produce NO errors or warnings. Use after every UI change, before declaring done, and whenever a human says something "looks wrong".
---

# see-ui — look at the page before you say it's done

Layout and design failures are invisible to your normal loop: the DOM is
valid, the CSS applied, the console silent — and the page is still
broken to a human eye (a chart squashed into 5% of its width renders
"successfully"). Code and logs cannot catch "technically correct but
looks wrong". Pixels can, and you can read pixels.

## The command

```bash
botference see <target> [label] [--viewport WxH]... [--basic-auth U:P] [--out DIR]
```

- `<target>`: a URL, a bare `:port` (localhost), a **local file path**
  (HTML, SVG — rendered via file://, no server needed: the way to
  verify charts, reports, and mockups you just wrote), or the NAME of a
  running `botference service` — its listening port is discovered from
  the live process, you never need to know it.
- Never hand-roll rendering via ImageMagick/qlmanage/rsvg to check a
  chart — their SVG engines have artifacts Chrome does not; `see` is
  the trustworthy lane and works from your sandbox.
- Default viewports: `390x844` (phone — real mobile layout, since
  responsive CSS answers to viewport width) and `1440x900` (desktop).
- It prints `wrote: <path>.png` lines. **Read those images.** That is
  the entire point — do not run the command and skip looking.
- Output defaults to `.botference/shots/` (gitignored by convention).

## Protocol

1. After ANY change that affects rendered UI, screenshot both default
   viewports and look at them before reporting the change as done.
2. When a human reports something "looks wrong/bad/off", screenshot
   FIRST, at the viewport they used (phone screenshots → `390x844`),
   and compare with what they see. Do not reason about CSS from source
   alone.
3. If the app has a login form, your screenshot will show only the
   gate. Fix that properly: let bare-localhost requests through
   unauthenticated (the review engine's rule — anyone on the loopback
   port already owns the machine). `--basic-auth` helps only for HTTP
   basic auth, not form gates.
4. Charts and figures: vision discovers a failure class once — then
   lock it out forever with a deterministic test on the generated
   SVG/scales, no browser needed. Assert data coverage (observed data
   spans ≥ ~half the x-range; projections must not compress history),
   containment (points inside the plot area, y-domain spans the data,
   no NaN coordinates), and legibility (labels don't collide, sane
   tick counts, markers above minimum visible size). **Every visual
   chart fix ships with the invariant test that would have failed on
   the bad render.**

## Notes

- Engine: headless system Chrome — no Playwright, nothing to install.
  A `--virtual-time-budget` is applied so client-drawn charts finish
  rendering before the shot.
- **Sandboxes are handled — run the command yourself.** Your sandbox
  cannot launch Chrome (seatbelt kills it); `botference see` detects
  that and hands the job to the see-broker service automatically,
  printing the same `wrote:` paths. Do not retry Chrome by hand and do
  not ask a human for pixels. If it reports "no see-broker service is
  alive", relay exactly this to the machine owner:
  `botference service start see-broker -- botference see --serve`
- Emulation caveat: it is Chrome at phone size, not iOS Safari. If a
  bug reproduces on a real iPhone but not in your render, say so —
  that is the one case that justifies installing Playwright (for its
  WebKit engine), a decision for the human, not you.
- `botference service list` shows what is running if you are unsure of
  a service name.
