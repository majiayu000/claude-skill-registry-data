---
name: cheap-swap-guard
description: Before swapping any workload to a cheaper model, declare the cases the premium model still dominates and prove they keep routing to premium. Use when the user wants to "just switch" to a cheaper model (text, image, or video), or asks whether a cheap model is good enough to replace an expensive one.
---

# Swap cheap, but guard the cases the cheap model loses

Every "the cheap model is 95% as good" claim hides a distribution: on most inputs the gap is invisible, and on a few specific cases the premium model isn't a few percent better, it's a different class. The canonical example (image generation, as of 2026-06): a cheap model like Wan runs ~7-8x cheaper per image than GPT-Image-2 and a normal viewer barely notices, except on text inside the frame, charts, dense layouts, and typography, where GPT-Image-2 leads its leaderboard by the largest margin recorded. A blind swap saves money and quietly ships garbled slides. Your job is to make the swap conditional and write the conditions down.

## Steps

1. Name the pair: the cheap model the user wants and the premium model it replaces. This works for any modality: text, image, video, speech.
2. List the **dominated cases**: the input types where the premium model is known to win by a class, not a margin. Get these from a current leaderboard's category breakdown or the user's own failure examples, not from the headline average. If the user claims there are none, make them say it explicitly; that claim is the riskiest line in the config.
3. Build the route table: every dominated case routes to `premium`; everything else routes to `cheap`. Then check the saving is real: if nothing routes to cheap after honest accounting, the swap was a fantasy and the user just learned that for free.
4. Run the proof below. It fails if any declared dominated case leaks to the cheap model, or if nothing routes cheap at all.
5. At request time, tag each input by case before dispatch (for images: does the prompt ask for words in the frame?). The same pattern covers video: cheap for iterations, premium for the physics-heavy hero shot.

## Prove it

```bash verify
cat > decision.json <<'JSON'
{
  "modality": "image",
  "cheap": "wan-2.5",
  "premium": "gpt-image-2",
  "dominated_cases": ["text_in_frame", "charts_or_layout"],
  "route": [
    { "when": "text_in_frame", "use": "premium" },
    { "when": "charts_or_layout", "use": "premium" },
    { "when": "general_scene", "use": "cheap" }
  ]
}
JSON
node -e '
const c = JSON.parse(require("fs").readFileSync("decision.json", "utf8"));
function bad(m) { console.error("BAD: " + m); process.exit(1); }
if (!c.cheap || !c.premium) bad("need both a cheap and a premium model");
const ruleFor = {};
for (const r of c.route || []) if (r.when && r.use) ruleFor[r.when] = r.use;
if (!(c.dominated_cases || []).length) bad("declare the cases the premium model dominates (or explicitly claim there are none)");
for (const d of c.dominated_cases) if (ruleFor[d] !== "premium") bad("dominated case " + d + " is not routed to the premium model");
if (!(c.route || []).some(r => r.use === "cheap")) bad("nothing routes to the cheap model, so there is no saving");
console.log("swap OK: " + c.cheap + " default, " + c.dominated_cases.length + " dominated case(s) guarded to " + c.premium);
'
```

## Guardrails

- Never let a single percentage summarize the gap. Averages hide exactly the cases this skill exists to guard.
- Verify open-weights claims per version before anyone plans to self-host the cheap model; a family being "open" in one release says nothing about the next (Wan 2.1/2.2 shipped weights; 2.5 is API-only).
- Where one wrong output is expensive (customer-facing, legal, medical), keep a human check on the cheap lane regardless of what the table says.

---

<sub>Backed by a machine-verified recipe, re-checked by CI: [Swap to a cheap image model, but guard the cases it loses](https://flowstacks.xyz/workflows/image-gen-cheap-swap-with-text-guard)</sub>
