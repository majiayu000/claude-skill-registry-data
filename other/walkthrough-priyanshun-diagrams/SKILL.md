---
name: walkthrough
description: Build a narrated, step-synced diagram walkthrough (local Kokoro voice + animated SVG, one self-contained HTML page with a recall quiz, predict pauses and source links) for a long mechanism the user wants to learn once — onboarding, a pipeline, a request path. Use when the user asks for a walkthrough, a narrated explainer or a "video", or accepts an offer of one. Never build one unasked; for short flows a text diagram in the reply is enough.
---

# Narrated walkthrough

The "video" is an HTML page, not an MP4. It beats a video in four ways:
- **Arrows light up on the spoken word.** A cue lights the node or arrow when the voice says the matching word, not just at the start of the step.
- **Predict pauses.** The page stops before a step and asks what happens next.
- **"Test me" quiz.** It hides the labels and asks the viewer to click where each step happens.
- **Source links.** Each step shows the `file:line` it comes from in the real repo.

The page is one file of about 700 KB per minute of narration. It works offline and on a phone.

This skill is the top layer. The **diagrams:flow** skill draws every picture (Mermaid → arrows by libavoid → sketch or clean theme); this skill adds the voice, cues, quiz and item card. Read `${CLAUDE_SKILL_DIR}/../flow/SKILL.md` for the diagram rules: flow or sequence, the look file, colour meaning, Mermaid gotchas.

```
Mermaid diagram + look ─► scene.json ─► nw --check ─► fix ─► nw ─► page.html
 (diagrams:flow rules)                                                │
                        window.__nw.selftest() in the browser pane ◄┘
```

## 1. Write the scene

Write the scene in a working folder (not inside the plugin) and serve that folder on localhost: a launch.json preview entry or `python3 -m http.server`. The browser pane cannot open `file://` URLs.

```json
{
  "title": "What happens when you place an order",
  "lead": "One line saying what this explains.",
  "voice": "af_heart",
  "repo": "~/code/shop",
  "theme": "clean",
  "diagram": "graph LR\n  customer[Customer<br/>web browser]\n  shop[Shop API<br/>order service]\n  ...\n  shop -->|charge card| pay",
  "look": {"customer": {"kind": "external", "color": "slate", "at": [0, 0]}, "provider": {"color": "sky"}},
  "legend": [{"color": "slate", "label": "Outside your system"}],
  "steps": [
    {"caption": "The shop saves a pending order, then asks the payment provider to charge the card.",
     "focus": ["shop"], "edges": [["customer", "shop"]],
     "cues": [{"at": "charge the card", "focus": ["pay"], "edges": [["shop", "pay"]]}],
     "ask": {"q": "The card is charged. How does the shop find out?", "a": "The provider sends a signed webhook."},
     "src": "src/checkout/create-order.js:42"}
  ]
}
```

**The diagram**
- `diagram` is Mermaid: `graph TD|LR` for a flow, `sequenceDiagram` for a sequence. `look` and `legend` follow the diagrams:flow rules. The same Mermaid also renders as chat text with `${CLAUDE_SKILL_DIR}/../flow/fd`.
- `theme` is `clean` (the default: crisp lines) or `sketch` (hand-drawn on graph paper).
- Use 4–8 nodes. A label has at most 3 words; a sub-label (`<br/>` second line) has at most 4.
- **Flow:** give `at` positions in the look whenever the flow branches, loops back or skips a node. Without them, nodes are placed in layers, which can render long and small. The phone layout ignores `at` and stacks nodes in the order the narration first lights them.
- Give a decision's two outcomes different sides: one straight down, one straight right (for example `decide` at [2,1], `orders` at [3,1], `retry` at [2,2]). If the build warns that two arrows "run side by side", move a box with `at`.
- Draw the direction the *data* moves. If the worker reads a file from S3, the arrow is S3 → worker, not worker → S3. Label most arrows with the verb that travels them.
- **Sequence:** use it when the order matters, or who waits for whom ("the customer sees processing before the payment is confirmed"). Steps light messages by number with `"msgs": [3]` instead of `"edges"`. Participants are the `focus` ids. On a phone the sequence keeps readable text and scrolls sideways, following the lit message.
- The older format (`nodes`, `edges`, `groups` written as JSON) still builds. Do not mix it with `diagram`.

**Steps**
- Use 5–9 steps. Each `caption` is one or two short sentences, under about 40 spoken words.
- `say` is optional. By default the voice reads the caption after the speech rules and the lexicon (section 2). Write `say` only when the spoken wording must differ.
- `focus` and `edges` (flow) or `msgs` (sequence) light the step from its first word.
- `cues` relight the diagram when the voice reaches the `at` phrase: one or more consecutive words of the spoken line, matched in order. Use a cue when one step crosses several nodes, so a node is not lit for 10+ seconds while the narration moves on.
- `item` is the thing travelling through the flow, as it looks *at this moment*: `{"name": "Charge", "fields": {"status": "pending"}}`. It shows in a card beside the caption, coloured like the box it sits in, and carries forward until a later step or cue replaces it. Use real field names and values from the code or data, never invented ones. Mask personal values (card digits, addresses) with `…`. Set `item` on cues too, so the card changes on the spoken word ("parses" → the parsed payload).
- `carry` (18 characters or fewer) labels the pill that rides each lit arrow for about 1.4 s after the step or cue starts ("order", "charge", "webhook", "yes"). Without it the pill shows the item's name.
- `ask` adds a predict pause before the step. Use it on 1–3 steps, at the "aha" points, where the next move is not obvious.
- `src` is `"path:line"` or a list of them, relative to `repo`. The build checks that each file and line exists and stamps the repo's git SHA in the footer.

**Content rules**
- Use real names and numbers from the work, never invented samples.
- Use the same word for the same thing in every step.
- Each node, label and arrow must match what the code really does. Check the code before you draw an edge.

## 2. Check, then build

`${CLAUDE_SKILL_DIR}/nw` wraps build.py with the shared venv. Run from the scenes folder:

```bash
"${CLAUDE_SKILL_DIR}/nw" my-scene.json --check 2>/dev/null
```

`--check` runs in about 2 seconds and generates no audio. It prints JSON with:
- **`warnings`:** schema errors, arrows that pass behind a node, two unrelated arrows that run side by side, an arrow label with no clear spot, labels too wide for their box, a group covering a node that isn't in it, symbols left in the spoken text, steps that are too long, and `src` paths that don't exist.
- **`ok`:** false when there is any warning or error. The full build still writes the page with warnings and reports `ok:true`; read its `warnings` too.
- **`[phone]` warnings** come from the phone column, which ignores `at`. Fix them by changing which step first lights one of the named boxes, or by dropping an arrow, not by moving `at`.
- **`pronunciation`:** each spoken line, plus the phonemes for every acronym, number and symbol. Read them. A wrong reading gets an entry in `lexicon`, either the scene's own or the shared `${CLAUDE_SKILL_DIR}/lexicon.json` for recurring terms. The value is plain words ("IST" → "India time") or misaki inline phonemes (`"ARC": "[ARC](/ˌAˌɑɹsˈi/)"`).
- The speech rules already handle ₹ amounts (→ "842 rupees and 82 paise"), 24-hour times (02:00 → "2 AM"), vN.N.N versions, arrows, "e.g.", "i.e." and "&".

```bash
"${CLAUDE_SKILL_DIR}/nw" my-scene.json 2>/dev/null
```

The build prints one JSON line: `ok`, `out`, `engine`, `seconds`, `steps`, `cues`, `kb` and `warnings`.
- **Exit 2:** a scene error. **Exit 3:** Kokoro failed. A build never falls back to the system voice silently. Pass `--allow-fallback` (or `--say`) only if the user accepts the robotic voice: macOS `say`, or `espeak-ng` on Linux when it is installed.
- **Voices:** `af_heart` downloads with the model. Any other voice (`am_michael`, `bf_emma`, `bm_george`) downloads a small voice file on first use, which needs the network.

## 3. Verify in the browser pane, then hand over

1. Open the page from your localhost server: `http://localhost:<port>/<name>.html?v=<n>`. Change `?v=` after every rebuild, because the pane caches pages.
2. Wait for the audio metadata, then run `JSON.stringify(window.__nw.selftest())`. It walks every step and cue, and reports:
   - what each one lit;
   - arrows that cross a node;
   - text wider than its box;
   - the on-screen label size, which must be at least 10 px;
   - the audio duration against the build;
   - arrow and group labels that overlap each other or a box;
   - two arrows that share no box but run side by side (flows only).
   `ok:true` is the bar to pass.
3. Run it once at desktop width (`resize_window` 1100×900) and once at `mobile`, then reset to `desktop`. Take one screenshot of each layout.
4. Give the user the path. Mention `#3`-style deep links, the number keys, the speed menu, "Test me" and "Copy as notes", which copies the walkthrough as Markdown notes.
5. Publish it as an artifact only if the user wants to share it. The page is self-contained, so publish the HTML directly.

## Don'ts

- No MP4 export. It throws away the cues, the quiz and the predict pauses.
- No CDN libraries. The page must stay one offline file. Diagram libraries run at build time in the diagrams plugin (Claude Code installs them from its package.json).
- Do not switch to an automatic box-placement engine (ELK, dagre) by default. ELK was tried: chain flows came out 7.8 times wider than tall, with 7 px labels.
- No extra voices, music or avatars. They add novelty, not recall.
