---
name: vhs
description: Techniques for creating deterministic terminal demo screencasts with VHS
---

# VHS Demo Recording

[VHS](https://github.com/charmbracelet/vhs) records terminal sessions by scripting keystrokes in `.tape` files and rendering them as GIFs. Use `Wait+Screen /regex/` to synchronize with interactive TUI elements instead of fragile fixed `Sleep` durations. VHS can only detect text *appearing* on screen, not disappearing — keep this constraint in mind when designing wait conditions.

## Non-Deterministic TUI Responses

When recording an LLM-powered TUI, detecting when a response is **complete** requires special care. Naive approaches all fail:

| Approach | Why it fails |
|---|---|
| Fixed `Sleep` | Not deterministic |
| Unique marker in prompt (`XYZENDXYZ`) | Appears in the typed prompt on screen — `Wait+Screen` matches immediately |
| Math formula (`347+829` → wait for `1176`) | LLM computes the answer in its visible *thinking trace* before the response finishes |
| `Wait+Line /^MARKER$/` | TUI padding/borders prevent exact line matching |
| `Hide` + type marker | `Hide` only hides VHS command log, not terminal content |

### The concatenation trick

Ask the LLM to **concatenate two words** and print the result. The prompt contains both words *separately* but never the combined string:

```tape
Type "briefly explain this repo. Then print ALFA concatenated with BRAVO."
Enter
Wait+Screen /ALFABRAVO/
```

**Why it works:**
1. **Typed prompt** shows `...ALFA concatenated with BRAVO` — no `ALFABRAVO`
2. **Thinking trace** says "I need to concatenate ALFA and BRAVO" — no `ALFABRAVO`
3. **Response** outputs `ALFABRAVO` — the only match

Use uncommon words (ALFA, BRAVO, ZULU) so the combined form can't appear accidentally.

## Tips

- **Run VHS from the correct CWD** — it inherits the working directory. If the prompt references "this repo", the CWD must be the repo root, not a subdirectory.
- **Inspect GIF frames** when debugging timing issues:
  ```bash
  ffmpeg -i demo.gif -vf "select='eq(n\,100)'" -vsync vfr /tmp/frame.png
  ```

## Nix Integration

- If the project uses Nix, create a dedicated `flake.nix` for the demo (e.g., `doc/demo/flake.nix`) so anyone can reproduce the recording with `nix run`.
- **Reference tape by Nix store path** in flake apps (`vhs "${./.}/demo.tape"`) — don't `cd` into the store, as it may contain a `flake.nix` that confuses `nix run` inside the recording.
