---
name: visual-recap
description: "Side-route skill that renders a change as a single self-contained interactive HTML artifact — a finished diff, PR, or branch, or a plan's decisions and architecture before any of it is built. Three block sets: a scrolling recap for auditing a change (file-tree + change flags, annotated split diffs with line-anchored callouts, schema/API contract cards, UI wireframes, before/after columns, a per-unit series when one root cause repeats across four or more near-identical sites), a paged walkthrough deck for arguing a reader through one (premise → changes → mechanism → aftermath), and forward-looking blocks for a plan (decision cards, options comparisons, architecture diagrams — every field cited or visibly asserted). Diagrams take a CSS spine when trivial and Mermaid-via-CDN when multi-stage or behavioral. Use when a reader who didn't author the change or the plan needs to grasp its shape before reading prose. Optional and never auto-invoked; skip small or obvious diffs, and plans whose decisions foreclose nothing. Not a defect finder (that's /pre-merge), not free-form diagramming (that's /excalidraw-diagram), not a committed artifact (the HTML is transient)."
sources:
  primary:
    - "Best Kept Secrets of Peer Code Review — Jason Cohen"
    - "The Design of Everyday Things — Don Norman"
  secondary:
    - "Thinking in Systems — Donella Meadows"
    - "The Visual Display of Quantitative Information — Edward Tufte"
    - "Envisioning Information — Edward Tufte"
---

# Visual Recap

Render a finished change as a single self-contained interactive HTML file that shows a reviewer the *shape* of the diff before they read the lines: which surfaces moved, which hunks are load-bearing, what's risky — with callouts anchored to the exact lines, then a drop into the literal code. The output is **reviewer comprehension as a portable artifact**, not a defect list.

It renders in one of **two modes**, chosen in Step 1 and never defaulted into: a **scrolling recap** when the reviewer is auditing a change, and a **walkthrough deck** — one idea per screen, premise → changes → mechanism → aftermath — when the reviewer has to be argued through one.

This skill exists because Cohen's strongest empirical finding is *author preparation*: an annotated walkthrough prepared by someone who understands the change correlates with near-zero defect variance. The pipeline produces that annotation as terminal prose (`/pre-merge`, `/walk-commits`) but never as a highlightable, shape-first surface — so the reviewer rebuilds the change's topology in their own head before judging any line. `/visual-recap` produces the missing surface (Meadows: a missing high-bandwidth feedback flow in the review loop) **without any lock-in** — the agent authors the HTML directly; there is no renderer package, no build system, no server, no MCP connector, and no hosted database. GitHub PR review comments stay the durable channel.

It also renders the *forward* direction — a plan's decisions and architecture, before any of it is built. There is no separate `/visual-plan` skill and none is coming (#317): a second command name buys nothing the mode selection in Step 1 does not already buy, and costs an inventory surface in every discovery doc. The two directions share one data model — a recap renders *from* a finished diff, a plan renders *toward* a change that does not exist — which is why they share a token core, a serializer, and a grounding rule rather than a codebase.

## Invocation Position

This is a **side-route skill**. It does not block merge and is **never auto-invoked**.

It reconnects to the main pipeline at the `/pre-merge` → merge boundary, exactly like `/walk-commits`: run it when you want shape-first comprehension before approving, then proceed to merge (and `/compound` if a durable lesson emerged). `/pre-merge` Phase 4 may *recommend* it — without invoking it — when the person merging didn't author the diff, the same way it recommends `/walk-commits`.

Use `/visual-recap` when:

- A reviewer who did **not** author the change needs to grasp its shape across multiple files before reading lines.
- The change's topology (what moved where, which hunks are load-bearing) is hard to hold in your head from flat terminal output.
- You want a portable, line-anchored artifact you can open in a browser and feed answers back from.
- A **plan** commits to decisions that a reader skims past in prose. `/write-a-prd`'s `## Implementation Decisions` is a flat bullet list; nothing in it marks which bullets foreclose something. Reconnects at the `/write-a-prd` → `/prd-to-issues` boundary rather than the merge boundary, and produces the same transient artifact.

Choosing between the two comprehension side-routes: `/walk-commits` steps the branch commit-by-commit with per-commit sign-off — reach for it when the history is the story and each commit deserves its own verdict. `/visual-recap` renders the whole change as one connected surface — reach for it when the final shape matters more than the path that produced it.

**Do not** use `/visual-recap`:

- **For small or obvious diffs.** This is the load-bearing gate. A one-file, few-line change reads faster as plain text; generating ceremony HTML for it is filler bait (Norman, *featuritis*; Meadows, *policy resistance*). If `/pre-merge` or `/walk-commits` terminal output already makes the change legible, do not render a recap. When unsure, skip.
- **To find defects** across the diff — that is `/pre-merge`'s adversarial, dimension-based review. The recap renders *comprehension*, not findings.
- **To draw free-form architecture arguments** — that is `/excalidraw-diagram`. The recap stays clean and structured.
- **To produce a committed artifact** — the HTML is transient (see the transient-artifact rule). Never commit it.

The line that keeps this distinct from `/pre-merge`: **comprehension surface, not defect-finding.** If you catch yourself enumerating bugs, you are running the wrong skill.

## The floor: lean is not thin

The skip gate cuts filler — but a change that *passes* the gate owes the reviewer a substantial surface. The failure mode on the other side of filler is the **thin recap**: a sparse three-block render of a 40-file change — one diagram, one sentence, one file list — that forces the reviewer back into the raw diff anyway, under-serving them exactly as much as boilerplate over-serves them. Restraint applies to *decoration and repetition*, never to *coverage*: every meaningful changed surface either gets a block or is intentionally omitted (see the coverage inventory in Step 3).

- **GOOD** — a 25-file auth change: a two-paragraph overview (objective, the session-storage decision, the token-expiry risk), a data-model card for the `sessions` table, an api-endpoint card for the new refresh route, the file-tree with flags, a CSS flow diagram of the new token path, and five key files each with an intent summary and 2–3 line-anchored callouts.
- **BAD** — the same change as one diagram, one sentence, and a file list; or the opposite wall: every hunk reproduced with a callout on each.

## The shared rendering core

All of the HTML vocabulary, the copy-text serializer, the Grounding Rule, secret-redaction, and the Tufte quality bar live in **`references/visual-rendering-core.md`** — the single bar this skill and `/walk-commits` both author against. The concrete shapes it points at — the fixed CSS token core and copy-paste-ready markup for each block — live in **`references/visual-recap-design.md`**, the canonical skeleton you copy from so artifacts come out consistent run-to-run. That doc has two parts, and they are two **modes**, not two layouts: **Part I (§1–§12)** is the scrolling recap; **Part II (§D1–§D9)** is the walkthrough deck. Both share the §1 token core, the Grounding Rule, secret-redaction, the reading budget, and the transient-artifact rule. Read the core and the part your mode selects, before rendering. The points below are the skill-level discipline; the core is the rendering contract and the design doc is the skeleton.

When a *choice* is what needs rendering rather than a change — three or more mutually exclusive options, each carrying three or more attributes, not orderable on one axis — the block is the **options-comparison** (`references/visual-recap-design.md` §11), and its threshold and its relationship to the `AskUserQuestion` menu live in `references/next-step-menu.md`. That block is forward-looking, so its grounding rule differs: each cell is cited with its source or visibly marked asserted (`references/visual-rendering-core.md` §1, *Forward-looking blocks*).

Two rules from the core are load-bearing and worth restating here:

- **The Grounding Rule.** Every structured value — paths, line numbers, hunk text, ±counts, commit hashes — is mechanically derived from the real diff (`git show`, `git diff`, `git diff --stat`), copied not retyped. The model writes **prose only** (callout notes, hunk intent summaries, change flags). A confidently-wrong recap is more dangerous than plain text because a reviewer who trusts the summary skips the line it got wrong. Visual emphasis must not exceed the real change (Tufte, Lie Factor ≤ 1).
- **Secret-redaction runs before any HTML is written.** Mask values for `*_KEY` / `*_SECRET` / `*_TOKEN` / credentialed URIs / PEM blocks — keep the key, mask the value — and note once in the overview if anything was masked. The artifact is portable; a leaked secret in a copied file is unrecoverable.

## Process

### 1. Resolve the change and apply the skip gate

Resolve what to recap — a branch range, a PR, or a working diff:

```bash
BASE_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD --short 2>/dev/null | sed 's@^origin/@@')
if [ -z "$BASE_BRANCH" ]; then
  for candidate in main master prod develop trunk; do
    if git rev-parse --verify "$candidate" >/dev/null 2>&1; then BASE_BRANCH=$candidate; break; fi
  done
fi
# A name is not a ref. $BASE_BRANCH names the branch (for `--base`, `git switch`);
# $BASE_REF points at it, and is the only thing safe as a range endpoint.
if git rev-parse --verify "origin/$BASE_BRANCH" >/dev/null 2>&1; then
  BASE_REF="origin/$BASE_BRANCH"
else
  BASE_REF="$BASE_BRANCH"
  echo "note: origin/$BASE_BRANCH does not resolve — measuring against the local branch, which may be stale" >&2
fi
git diff --stat "$BASE_REF...HEAD"
git log --oneline --no-merges "$BASE_REF..HEAD"
```

Do not hardcode `main` — detect the base (this repo itself uses `prod`). For a PR, resolve its head/base with `gh pr view <n>`. The `git diff` is three-dot (diff from the merge base) while the `git log` stays two-dot — swapping the diff to two-dot reports deletions for base-side work this branch never touched, and the Grounding Rule above stakes this skill on those ±counts being real.

**Residual:** `$BASE_REF` is only as fresh as the last `git fetch`, and on a triangular fork (or a remote not named `origin`) `origin/$BASE_BRANCH` may be absent or track your fork rather than upstream — the `else` branch then falls back to the local branch, which is the stale-ref behavior this guard exists to avoid. It says so on stderr rather than falling back silently, because a plausible wrong answer with no signal is what let this defect live for five months. If the counts look wrong, `git fetch` and re-run, or set `BASE_REF` by hand.

**Scope the whole work unit.** When invoked mid-session after work has already happened, the default scope is everything the session produced — the original implementation plus follow-up fixes, tests, and doc updates — not just the most recent edit. Exclude unrelated dirty work that predates the session. When regenerating a recap after feedback, keep the broad scope; never narrow it to just the latest fix unless asked.

**Apply the skip gate now.** Look at the `--stat`. If the change is small or obvious — a single file, a handful of lines, a mechanical rename — say so and **recommend skipping the recap**; the terminal output from `/pre-merge` or `/walk-commits` is faster. Only proceed when the topology genuinely warrants a shape-first surface. This gate is the skill's main defense against becoming filler.

**Then choose the mode, and say which you chose and why.** There are two canonical modes and they answer different questions. Do not default into one — a mode that is never selected is a mode that happens when nothing selects anything.

> **Is there one story the screens advance? → the deck. Is the reviewer auditing parallel hunks? → the scroll.**

- **Scroll recap** (`references/visual-recap-design.md` Part I, §1–§12) — a single scrolling column. Take it when the reviewer's job is to check a topology: which files moved, which contracts changed, which hunks are load-bearing. They already hold the *why* and need the *where*.
- **Walkthrough deck** (`references/visual-recap-design.md` Part II, §D1–§D9) — one idea per screen, paged, with a grouped rail and the arc **premise → the changes → the mechanism → aftermath**. Take it when the change has a causal arc and the *why* has to land before any hunk means anything: a sweep with one thesis, a chain of moves that depend on each other, a review's own story.

When both fit, take the scroll — it is the cheaper artifact. Two rules bound the deck and are not negotiable (§D2): **no comparison may span screens**, and **never page a population** — N near-identical instances of one cause are the finding, so they go co-visible in one screen, never one per screen.

**When the subject is a plan rather than a diff, the mode question is answered before you get here.** A shaped PRD, a research artifact, or a proposal has no diff, so the resolve step above does not apply: skip it and render the **forward-looking blocks** instead — **decision cards** (`references/visual-recap-design.md` §13) for the commitments the plan makes, an **options-comparison** (§11) for a fork it has not settled, an **open question** (§14) for what it cannot settle yet, and a **§5 diagram** for the architecture it implies. The scroll shell holds them; the deck holds them when the plan has a causal arc.

Those first three are one decision at three stages, and a live plan surface usually shows more than one stage at once: a question that has no options yet, a fork rendered as a matrix, a choice already made and rendered as a card. **When a card records the outcome of a matrix on the same surface, carry the winning option's slug into the card's id** — the derivation and its worked example are in `references/visual-rendering-core.md` §4's id registry. Numbering the decisions instead is the failure: insert one, regenerate, and every answer already pasted back attaches to a different decision with nothing reporting it.

Two things change, and both are load-bearing. **The Grounding Rule inverts** — there is nothing to derive from, so every field is *cited* (quoted from the PRD or issue body, the research artifact, or current code at `file:line`, and showing that source) or visibly *asserted*, per `references/visual-rendering-core.md` §1. **The skip gate gets stricter, not looser**: render a decision card only for a decision that forecloses something. A plan whose decisions are all preferences reads faster as the prose it already is, and drawing it gives commitments weight they have not earned — the same Lie Factor the recap side guards against, measured in evidence instead of lines.

**When the change feels abstract to the audience, recommend `/re-pitch` — never invoke it.** The deck's premise screen is a re-pitch-shaped retelling (one anchor sentence, every domain term glossed on first use, no forward references), and in the field a `/re-pitch` run mid-session became a deck's opening screen directly. If the reader signals the change is not landing, name `/re-pitch` as the option and let them take it; same rule as every other cross-skill seam here.

### 2. Derive the grounded skeleton (tooling, not prose)

Build the structural inputs mechanically, before writing a single sentence:

- **Topology:** the file list and per-file ±LOC from `git diff --stat`.
- **Hunks:** the actual before/after text and line numbers from `git diff`/`git show` — copied verbatim into the annotated-diff blocks.
- **Commits:** hashes and touched files from `git log`/`git show`.

Run secret-redaction over every hunk at this step (per the core), before any of it reaches the HTML.

### 3. Inventory coverage, then author the prose layer

**Inventory first.** Before writing a sentence, list from the diff every meaningful changed surface: routes/components, schema entities, API endpoints/actions, dialogs/popovers, role/permission states, empty/error states, and shared abstractions. The finished recap must represent each item with a block **or intentionally omit it** (tiny, redundant, not reviewer-visible). This list is the mechanical counter-pressure against the thin recap — and it stays grounded, because it comes from the diff, not from memory.

**Then choose the axis.** The inventory says *what* changed; it does not say how to decompose the recap — and the default (one section per *kind* of block, files as rows inside them) is a choice that gets made by not making it. Ask outright: **is this one root cause repeated across four or more near-identical sites?** One defect copy-pasted into six skills, one rename swept through nine call sites, one policy applied to every route.

- **No** → the default block-type-major layout (`references/visual-recap-design.md` §3–§9). Files are rows in the file tree; you pick the 3–8 that carry the change.
- **Yes** → the **per-unit series** (`references/visual-recap-design.md` §12): one real `<section>` per site, each with its own before/after pair, lede, and typed notes, plus the required all-units matrix. Render it *instead of* sampling the sites into a file tree.

**The 3–8 budget governs depth, never population.** It caps how much you annotate *within* a unit; it does not cap how many units you render. For a sweep the population *is* the finding — five sites fixed, one deliberately exempt, two nearly missed — and sampling destroys the only distinction that matters, because a documented exception then reads exactly like an oversight. Cohen's rule for an oversized review has the same shape: split it into **complete** sessions, never sample one.

**The prose bar.** Under the Grounding Rule the model authors *only* prose — which makes prose the entire authored layer of a recap, and until now the only authored layer in the pack with no stated bar. Hold it to **`references/writing-for-humans.md`**: its revision bar (strip clutter, cut the warm-up, Bar/Beach Test, active verbs, concrete nouns, short-not-shallow) and its *what counts vs. what doesn't* test — the words must carry the **mental model** the grounded blocks cannot show, not a narrativized restatement of the hunk beside them. That doc's *shape* is written for issue and PR bodies; what carries over here is the bar and the mental-model test, not a `## Summary` section.

Write for someone who has worked in this project for a couple of weeks: they know the language and the repo's shape, and they do not know this change. Gloss a domain term the diff introduces on first use.

This bar governs **per-unit prose** — every lede, intent summary, and callout note — where a length cap does not reach. A cap on one global slot says nothing about the twenty short ledes in a per-unit series (`references/visual-recap-design.md` §12), and length was never the failure anyway: an agent narrating a diff it just wrote is the maximally cursed narrator. Hinds found experts underestimate a novice's task time by roughly 2.5×, and that prompting them to recall their own novice struggles did *not* improve the estimate — which is why the instrument here has to be a checkable bar rather than an exhortation to empathize.

Then write the parts the model owns — and only these:

- The **overview**: 1–3 sentences of "what this change is," the scale, and the reading mode (evolution vs. maintenance) for a small change; up to 3 short paragraphs for a large one — the objective, the key decisions visible in the diff, and the risks a reviewer should weigh. Intent first, either way.
- A **change flag** per file (`new` / `moved` / `load-bearing` / `mechanical` / `risky`).
- A one-line **intent summary** above each annotated hunk.
- Callouts on **3–8 key files/hunks** — each key file gets its intent summary and a few high-signal callouts anchored to real line ranges, with excerpts focused (~150 lines max each) and the whole recap inside the reading budget (Cohen/Rigby: ~100–300 LOC of excerpts, 30–60 min). **This is a depth budget, never a population cap:** it bounds how much you annotate *within* a unit, and it does not bound how many units a per-unit series (`references/visual-recap-design.md` §12) renders. A recap that callouts every hunk has rebuilt the diff the reviewer was going to scroll anyway; a recap with one callout for a 40-file change is the thin recap the floor forbids.
- A one-sentence **compatibility note** beside each contract card that needs one (breaking / risky / non-breaking, and for whom).

When the diff changes a **schema or API surface**, the resulting contract is the headline, not the source: render a **data-model card** per changed entity and an **api-endpoint card** per changed route (`references/visual-recap-design.md` §8) — per-field change flags, struck-through `was:` prior types, grounded in the real migration/route diff. Keep the literal SQL/handler hunk for when the exact statement still matters.

When the diff changes **rendered UI** — layout, controls, navigation, dialogs, visible states, design tokens — include **wireframe block(s)** (`references/visual-recap-design.md` §9); code diffs are not a substitute for showing what the user will see. Cover the **entry surface**, the **interaction surface** that opens or changes, and the **resulting state**, plus role variants when permissions changed. After-only is fine for purely additive UI; skip wireframes when the UI delta is trivial. Wireframes are a model-authored block (`references/visual-rendering-core.md` §1 enumerates the carve-outs): labels and controls come from diff-visible strings and component names, and inferred layout says "layout inferred" in the caption.

When the change needs an architecture, data-flow, or sequence picture, **pick the form by what the picture has to say** (`references/visual-recap-design.md` §5). A **trivial spine** — one straight flow, a short sequence, no labeled edges, no branches — takes the **CSS diagram primitive** (`§1/§5 .fc-*`), which renders identically offline with no CDN and no parse grammar. Anything **multi-stage or behavioral** — labeled edges, fan-outs, guards, failure states, a before/after pair of graphs, a dense DAG or ER diagram — takes **Mermaid via CDN**, authored through `/mermaid`, with the visible per-figure degrade note beside it. When the review context is known to be offline, take the CSS primitive regardless and say so in the caption. Whatever the figure carries, the *finding* must also survive offline as prose or a core block (`references/visual-rendering-core.md` §6). (Issue #83 chose Mermaid for GitHub-bound markdown, rendered natively with no CDN — a different context, and untouched.)

### 4. Render the self-contained HTML

Author one `.html` file by copying the canonical skeleton in `references/visual-recap-design.md` — the fixed token core (§1) and the per-block markup (§3–§9) — then filling only the grounded data and the prose. Deviate from the skeleton only where the change genuinely needs it; do not re-derive a fresh design system per run.

- Inline, themeable CSS is load-bearing — copy the skeleton's `:root`/`[data-theme="dark"]` token block verbatim (light default, dark flipped on `[data-theme]`) and keep the variable names. **Every core block must read identically with the network off**; the one licensed exception is a Mermaid **diagram figure**, which may degrade to source text and must carry its degrade note on its own face (`references/visual-rendering-core.md` §6). Any other CDN library is enhancement-only and always has a no-CDN fallback.
- Line-anchored callouts are **direct labels** rendered at the line, not a separate legend (Tufte; Norman, *natural mapping*). Clicking a marker highlights the exact line — scope the highlight to the code cell, not the whole row.
- Maximize data-ink: no chartjunk, no decorative shadows; small multiples + constancy of design for before/after comparisons — labeled side-by-side columns by default, identical scale and frame on both sides, the state named in the column header (never inside the frame); when the content is too wide to halve, stack the two frames rather than hiding one behind a toggle.
- Include the **Copy feedback** button and its layered-clipboard serializer with stable `data-feedback-id`s, exactly per the core's `recap-feedback v1` format — **required whenever the artifact is handed off** (mailed, attached, opened in another session, read asynchronously). When the author is in the room and the reviewer answers out loud, it is an optional final-screen block instead (`references/visual-rendering-core.md` §4). When unsure which case you are in, include it.
- **In deck mode**, page by toggling `hidden` over real `<section>`s that are all in the DOM (§D3) — never by swapping `innerHTML` from a template store. Show-all, browser find, print, and the feedback serializer each depend on it, and a store plus routing is the app this surface exists to avoid.

Write the file to a **transient** path — gitignored `.context/` or `mktemp` — never the tracked tree.

### 5. Open, review, and round-trip the feedback

**Confirm the token core is canonical, not the reviewed app's aesthetic (forcing function).** Before presenting, verify the artifact's `:root`/`[data-theme]` block is the canonical `references/visual-recap-design.md` §1 set — canonical variable names and values — and **not** a palette, font stack, or chrome re-derived from the app under review. This is the deviation most likely to occur on a well-designed downstream app and the most harmful when it does: the neutral instrument adopts its subject's brand and loses run-to-run constancy. It is a checked step, not stated hope (core §6).

The CSS diagram primitive needs no render check — it has no parse grammar and no CDN.
**For every Mermaid figure**, **confirm it renders without a
parse error before presenting it** (a quick load, or a re-check against the
`references/visual-recap-design.md` §5 label-safety rules). The `<pre class="mermaid">` source
fallback shows source text — the exact thing that fails to parse — so it does not stand in for
a rendering check. Authoring such diagrams via `/mermaid` (which verifies its own render)
discharges this up front. Keep it lightweight — no headless-browser harness is required (core §7).

Emit both open paths so the reviewer can choose:

```
open <artifact>.html                # file:// is a secure context
python3 -m http.server 8000         # fallback for sandboxes that block file://
```

The reviewer reads the recap, writes notes/verdicts in-page, clicks **Copy feedback**, and pastes the `recap-feedback v1` block back. Parse it by stable id and either (a) patch the HTML, (b) drive changes into code, or (c) **promote durable items to GitHub PR review comments** — the line-anchored channel that outlives the session. The clipboard is the working transport; GitHub is the system of record.

### 6. Tear down

Delete the HTML (and any screenshots) when the review round is done. What persists is the *decision* — sign-offs and any items promoted to PR comments — not the file. If you want to keep the HTML "for reference," that is the signal to promote its content to a PR comment or `docs/solutions/` entry instead.

## What This Skill is NOT

- **Not a defect review.** It does not sweep the diff for bugs — `/pre-merge` does that and emits advisory findings. Recap renders comprehension.
- **Not free-form diagramming.** It stays clean and structured; exploratory "diagrams that argue" are `/excalidraw-diagram`.
- **Not a graph-layout engine.** Trivial spines use the CSS diagram primitive; multi-stage and behavioral graphs come from `/mermaid`. The core owns callouts and diffs, not hand-positioned graph layout.
- **Not a renderer we ship.** The core is a vocabulary the agent hand-authors against — no package, no build, no server, no committed app. The canonical skeleton (`references/visual-recap-design.md`) is a *copyable reference the agent inlines*, the same status as the §4 serializer — **not** the runtime component library this bullet forbids: no package, no build step, no CDN runtime, nothing the artifact imports. If "self-contained HTML with CDN imports" starts growing state, routing, or an imported component library, pull it back.
- **Not a mandatory stage, and not auto-invoked.** It is optional, gated by the skip-for-small-diffs rule. If a later PR sample shows it is rarely invoked or only fires on diffs `/pre-merge` already covers, fold it into `/pre-merge` as an optional phase (mirrors `/walk-commits`'s own self-deprecation clause).
- **Not a committed artifact.** The HTML is transient — gitignored or `mktemp`, deleted after the round. Per SYSTEM-OVERVIEW §Philosophy.

## Handoff

- **Expected input:** either a finished change to comprehend — a branch range, a PR number, or a working diff, plus the base branch to diff against — or a plan to render forward: a shaped PRD issue, a research artifact, or a proposal whose decisions and architecture a reader has to grasp before slices get cut. No upstream artifact is required for the diff case, though a linked PRD or slice issue helps frame intent.
- **Produces:** a transient, self-contained interactive HTML artifact in the selected mode — a **scrolling recap** (file-tree + change flags, annotated split diffs with line-anchored callouts, schema/API contract cards, UI wireframes for rendered-UI changes, labeled before/after columns, a per-unit series when one root cause repeats across four or more near-identical sites) or a **walkthrough deck** (premise → changes → mechanism → aftermath, one idea per screen, before/after panes inside the screen) — or, for a plan, the **forward-looking blocks**: decision cards for the commitments it makes, an options-comparison for a fork it has not settled, and the architecture it implies, every field cited or visibly asserted. Diagrams render as a CSS spine when trivial and Mermaid-via-CDN when multi-stage or behavioral. Plus the reader's feedback, copied back where the artifact is handed off, with durable items promoted to GitHub PR review comments (diff case) or to the PRD issue body (plan case). A comprehension surface and a decision, not a committed file.
- **Reconnects at:** the `/pre-merge` → merge boundary for a diff — run it before approving, then merge once the change is understood, and `/compound` if a durable lesson emerged. For a plan, the `/write-a-prd` → `/prd-to-issues` boundary: run it when the PRD is shaped and someone who was not in the shaping session has to react before slices get cut.
- **What comes next:** the user merges, or decomposes the plan (or pauses on unresolved items). `/visual-recap` does not invoke anything.
