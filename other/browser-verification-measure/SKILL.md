---
name: browser-verification-measure
kind: pattern
rule: browser-verification
description: Pattern of rule browser-verification. Load when a conclusion about layout needs a number behind it — ready-made measurements, a computed value broken down over all nodes, a narrow screen through an iframe, pitfalls of the computer tool. Not for raising a stand — pattern browser-verification-stand.
---
<!-- rt-kit v0.34.0 · patterns/browser-verification-measure.md · a17eb7cd05da · правится надстройкой, не здесь -->

# Measurement instead of a look

Pattern of the rule `browser-verification`. What must be true — the law
`docs/constitution/verifiability.md`.

## When to use

- Layout was edited, and the result needs confirming.
- The screen looks wrong, and there is nothing to search for: a search over the code answers
  "clean".
- A narrow screen is under check.

## A conclusion is backed by a number

`getComputedStyle`, `getBoundingClientRect`, contrast, matching centres, landing in the viewport.
"Looks fine" is never a check result.

A measurement answers only the question asked. A match on the listed properties says nothing about a
rule that is not in the measured list. The rows of the profile popup matched the reference by
padding, font size and rounding, while the reference paints no hover background there at all — a
full-width highlight held on for two rounds with correct numbers. If the reference sources are
available, the divergence is found by reading, and the measurement stays a check of the result.

The look of an element that today is visible on no screen is not confirmed by a measurement, and a
rule about it stays a hypothesis.

## The waiting state is measured on a delayed request

A button in waiting, a list skeleton and a loading bar live exactly as long as the request runs: on
a stand that is a fraction of a second, and no measurement call can catch them. The request itself
is delayed, not the measurement.

The technique has three parts, and the third is mandatory: the network call is substituted, the
answer is held for a few seconds, and it ends with a refusal. A real answer would leave a real
record on the stand — that is how an extra row got into the stand's database.

```javascript
globalThis.__realFetch ??= globalThis.fetch;
globalThis.fetch = (input, init) => {
    const url = typeof input === 'string' ? input : input.url;
    if (!url.includes('<the piece of the address being held>')) {
        return globalThis.__realFetch(input, init);
    }
    return new Promise((resolve) => {
        setTimeout(() => resolve(new Response('{}', { status: 500 })), 5000);
    });
};

'substituted';
```

The substitution is removed by assigning the saved one back: the page lives until reload, and a
forgotten substitution leads the next measurement astray.

The sign that this is exactly the case: the button on the screenshot in its ordinary look, while
the request has already gone out in the list of network calls. Assembling the technique anew each
time costs more than reading it here: over one epic it was assembled three times.

## A value that is not in the code

The typeface, `line-height`, colour and `appearance` of form elements are set by the browser, and
the tree has none of these values. A search over the code answers "clean" for such a defect, the
linter and the build are silent. It is found by breaking the computed value down over all nodes of
the page, not by measuring a couple of elements:

```javascript
[...document.querySelectorAll('*')].reduce((acc, el) => {
    const key = getComputedStyle(el).fontFamily;
    acc[key] = (acc[key] ?? 0) + 1;
    return acc;
}, {});
```

That is how 91 controls out of 106 set in the wrong typeface were found on the admin dashboard,
and 13 out of 87 on the site's main page. The count fits any inherited property: what is looked at
is not one value but the number of nodes with an unexpected one.

## Measurement across all thresholds at once

A measurement at one width per call gives numbers from different minutes: between calls the page
is redrawn, and they cannot be compared. So the widths are run as a batch in one pass — each lives
in its own frame, and the measurement is taken from all of them at once:

```javascript
await (async (address, widths, row) => {
    const frames = widths.map((width) => {
        const frame = document.createElement('iframe');
        frame.style.cssText = `width:${width}px;height:900px;border:0;position:fixed;left:-9999px`;
        frame.src = address;
        document.body.appendChild(frame);
        return { width, frame };
    });

    await Promise.all(frames.map(({ frame }) => new Promise((done) => (frame.onload = done))));

    return frames.map(({ width, frame }) => {
        const view = frame.contentWindow;
        const doc = frame.contentDocument;
        const cells = [...doc.querySelectorAll(row)];

        return {
            asked: width,
            got: view.innerWidth,
            heights: [...new Set(cells.map((el) => Math.round(el.getBoundingClientRect().height)))],
            scrolls: doc.documentElement.scrollWidth > doc.documentElement.clientWidth,
            escaped: cells.filter((el) => el.getBoundingClientRect().left > view.innerWidth).length,
        };
    });
})('/screen', [360, 599, 600, 904, 905, 1239, 1240, 1440], '.field');
```

The answer is read by three signs, and the first is not about looks:

- **the heights of neighbours in one row are equal** — a set of values in `heights` longer than
  one means the fields came out different sizes;
- **there is no horizontal scrolling** — `scrolls` is true where the content is wider than the
  frame;
- **no left edge goes past the frame width** — `escaped` above zero. On a screenshot this is not
  visible at all: an element beyond the right edge looks absent.

The frame width is smaller than the ordered one by a scrollbar, so the comparison is against `got`,
not against the number from the list. A threshold named by the ordered width turns out on the other
side of itself in the frame.

## Narrow screen

`resize_window` does not work when Chrome is in full-screen mode: the tool reports success,
`innerWidth` does not change, media queries stay desktop. Narrow widths are checked in a nested
iframe of the needed width — inside it `matchMedia` counts from the frame; at `width: 375px` and
`border: 2px` the inner `innerWidth` equals 371.

Changing the number of elements in a container is a layout edit: it is checked at 375, not only by
response codes.

## An input event is not replaced by a faked value

**Scrolling set by assignment gives no event.** The scroll value changes, but the subscriber does
not fire on the document, on the window or on the root node. The sign the application computes by
the event stays as it was, and the edit made reads as not made — two sessions in a row took apart a
working listener.

Hence two checks, and neither replaces the other: the mechanics are checked with a real wheel, and
the layout under the sign — with a sign set by hand. The class is put on the host, and what depends
on it is measured; the threshold takes no part in that.

The sign that this is exactly the case: the listener is set, the scroll value changed, the event
counter is zero. There is no need to take the listener itself apart after that — it works.

## Pitfalls of the `computer` tool

- Click coordinates are the coordinates of the **screenshot**, not CSS pixels: at a viewport of 2560
  the screenshot arrives 1568 wide, and a click at the "seen" coordinate goes astray, giving a false
  signal. Recompute by the actual scale or aim through `find`.
- The `zoom` area must lie entirely inside the viewport.
- An `await` between clicks is mandatory: a synchronous loop of "clicked — read the DOM" reads the
  state before the redraw and returns stale values.
- `select_browser` goes stale after 300 seconds. On a long check this fires in the middle of the
  work — it is not a stand failure; repeat the call and go on. The pinned profile is named by the
  tree itself — by an environment variable or by its own file next to the layout settings. It is
  asked from the helper, not remembered: the identifier is local to the machine and does not travel
  into the package at all.

## A long run is started in the page, not in the call

A tool call is cut off by its own limit at about forty-five seconds, while the walk it started
goes on — nobody will ask it for the result any more. One width from the set of screens takes
about a minute and a half, so not one fits into a call.

The order is this: the call puts the walk into a page variable and ends at once, and the following
calls ask that same variable whether it is done.

```javascript
globalThis.__probe = { done: false, rows: [] };
(async () => {
    for (const w of [375, 480, 481, 768, 769, 1080, 1081, 1380]) {
        globalThis.__probe.rows.push(await measureWidth(w));
    }
    globalThis.__probe.done = true;
})();

'started';
```

The tool's answer is truncated at about fifteen hundred characters with no mark: the end of the
summary looks not cut off but absent — output gathered in one pass and printed at once reads as
shorter than it is. So what was gathered stays in the variable whole, and is printed in slices by
index.

## Router behaviour is reproduced by clicks

Substituting the address, `history.pushState` with `popstate` and entering by a direct link raise
the application anew, and it has no accumulated state — no open outlet, no guard of the previous
panel. A clean pass over the addresses reads as "the defect is not confirmed": the event feed panel
got stuck on the very first click from the menu and passed the check by addresses three times.

## Common misses

- A comment in a config is a hypothesis like any other. A claim about eviction of a cache record
  held on through three rounds of adversarial code review and was refuted by one `curl`.
- The conclusion "no defect, it is the cache" closes the investigation, so it is accepted only
  after a check on a clean build.
- A defect in a client chunk from a compilation before the edit looks like a defect in the code:
  the sign of a dev build is bundle names without a hash.
