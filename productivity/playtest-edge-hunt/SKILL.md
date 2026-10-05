---
name: playtest-edge-hunt
description: Run the main-thread loop that walks a fixed six-area conversation with tmct, finds an edge, minimizes it, fixes it, and ships it every iteration. Invoke when the operator says "run a playtest", names an iteration budget, or asks for routine hardening of the six standing user-journey areas.
---

# playtest-edge-hunt — the main-thread playtest loop: find an edge, fix it, ship it

This skill turns `EXAMPLE_PLAYTEST_LOG.md` (written for a human playtester) into a loop Claude
Code runs itself, against the LOCAL working copy — always `node bin/tmct.mjs` from this repo,
never an npm-installed tmct. **Each iteration walks one continuous, realistic conversation
through all six standing areas (§4)** — not one grammar axis picked from a list — looking for
edges (a request tmct can't parse, or one that parses but returns the wrong or no answer) as it
goes, documents whatever it finds in a numbered log under `./playtests/`, fixes it, retests, then
commits, rolls the version, and pushes. Then the next iteration starts.

> **Invoke it by telling a session:** *"Follow the `playtest-edge-hunt` skill"*, optionally naming
> an iteration budget ("run 5 playtests").

## What this skill is for

This skill runs on the main thread, serially: walk one conversation across the fixed six-area arc
(§4), find an edge, minimize it, fix it, regression-test it, and ship it — then start the next
iteration. Depth comes from repeating the same six areas with fresh content each run, not from
breadth across frames or personas. Each iteration ends in a commit, a version bump, and a numbered
`playtests/PLAYTEST_LOG_*.md`. Use it for routine, hands-on hardening of the six user-journey
areas every session actually touches.

## 0. Ground rules

- **Main thread only.** This is a deliberate exception to CLAUDE.md's coordinator/background-agent
  model. The loop is serial by nature (probe → diagnose → fix → retest → ship) and each step
  feeds the next; splitting it across agents adds hand-off cost and nothing else. Long commands
  (the full `npm test`) still tee to a file: `npm test 2>&1 | tee /tmp/pt-test.log | tail -20`.
- **Ship every iteration.** The operator's standing instruction for this activity: at the end of
  each iteration, commit, roll the version (patch bump of `package.json` + `package-lock.json`),
  and push — one push per iteration, the bump commit part of that push. This is an explicit
  versioning instruction; per CLAUDE.md it is not up for debate and you never pause to ask about
  cadence. CI publishes on the version bump on `main`.
- **`npm test` green at every commit**, plus the CLI smoke:
  `printf 'hi\n/exit\n' | node bin/tmct.mjs` must greet and exit 0.
- **Local build, isolated memory.** Never let a playtest session write to this repo's `.tmct/`.
  Every probe session runs against a fresh scratch repo (§3).

## 1. The loop

Repeat until a stop condition (§7) fires:

1. **Check prior coverage first.** Before anything else, survey the existing
   `playtests/PLAYTEST_LOG_*.md` files — every log walks all six areas (§4) now, so "coverage"
   means which SPECIFIC probes were used within each area, not which areas were touched (all six
   are touched every run, by design). `grep -h -i -E 'area [1-6]|persona|topic|task' playtests/PLAYTEST_LOG_*.md`
   shows what's already been tried; pick fresh personal-fact types, codebases, teach content,
   code-tasks, and research topics this run rather than replaying the same six scripted turns.
2. **Start the log.** Copy `EXAMPLE_PLAYTEST_LOG.md` to `playtests/PLAYTEST_LOG_<NNN>.md`
   (`NNN` = highest existing number + 1, zero-padded; `mkdir -p playtests` on first run). Adapt
   the copy (§2).
3. **Walk all six areas (§4) in one continuous session.** Not one area per iteration — one
   realistic conversation this iteration, opening with a personal introduction (area 1) and
   moving through orientation, codebase exploration, teach+infer, a code-shaped planning ask, and
   a research ask (areas 2–6) in order, closing the session genuinely at the end. Record the tmct
   version under test and, per area, which specific probe content was used (which personal fact,
   which codebase, which taught fact, which code-task, which research topic) at the top of the
   log — that's what future runs check in step 1.
4. **Probe naturally within each area** (§3) until you hit an edge, or the area completes clean.
   Max 3 examples per sentence structure inside any one area: the grammar rules are separate from
   the lexicon, so a third lexical variant of a failing shape proves nothing new.
5. **Minimize every edge found.** Strip the failing request word by word until it parses; keep
   the closest passing form and the minimal failing form as a pair. That pair defines the edge
   precisely and becomes the regression test. Walking six areas in one session routinely turns up
   more than one genuine edge — minimize each independently; don't stop at the first.
6. **Capture** in the log: one `test:` section per edge found (§6 — Given/When/Expected/Actual,
   the verdict, the verbatim session log), tagged with which of the six areas it came from.
   Succinct per edge — a couple of discriminating examples, not every probe run — but capture
   every genuine edge this session found, not just the first. A clean area (no edge) still gets
   one line in the log saying so.
7. **Diagnose and fix every captured edge** (§5), rerun the exact failing probes plus `npm test`
   until passing. If a fix can't be made to pass without collateral damage, mark that edge's
   result `Fail (unable to pass)` with one paragraph on why, revert the attempt, and still ship
   the log with whatever else did pass.
8. **Ship.** Commit the fix + its regression test + the playtest log (repo-local identity),
   bump the patch version, push. Then go to 1.

## 2. Adapting the copied log

The copy starts as `EXAMPLE_PLAYTEST_LOG.md` verbatim; make it a record, not a manual:

- Retitle to `tmct playtest <NNN> — six-area session` and delete the Installation section and
  the npx/npmjs/gitlab orientation text. Replace with a short header: the tmct version under
  test (`package.json` at iteration start), the example repo used, and — per §1 step 3 — which
  specific probe content each of the six areas (§4) used this run (the personal fact, the
  codebase, the taught fact, the code-task, the research topic), so the next run's coverage check
  (§1 step 1) can vary rather than repeat.
- Keep the structure from the `test: …` heading down: **Expectations** (Given / When / Expected /
  Actual), **Result**, **Play test session log**, **Retest** / **Retest result** / **Retest
  session log**. One `test: <name>` section per edge found, tagged with its area number
  (§1 steps 5–6) — six areas walked in one session routinely turns up more than one genuine
  edge; capture every one found, not just the first.
- Add a short **Fix** section between Result and Retest: which layer changed (§5's map), what
  the change was, and which test file carries the regression. No commit hashes, no "Gap N"
  labels — plain description.
- Delete the example placeholder content as you replace it. `(example)` markers must not
  survive into a shipped log.

## 3. Probe recipe

Sessions are deterministic and $0, so replay is exact. This skill's session now spans all six
areas (§4) in one run, so it needs a REAL indexed codebase, not just an empty seeded repo — areas
3–5 don't exist without one.

**One session, one repo, for the whole run:**

```bash
SCRATCH=$(mktemp -d)
cp -r examples/mini-webapp "$SCRATCH"   # or another shipped example — never the committed fixture directly
printf 'hi, i'"'"'m alex, i work mostly on the backend\nwhat can you help me with\nwhat modules import http.mjs\n<…continue through areas 2-6…>\n/exit\n' \
  | node bin/tmct.mjs chat --repo "$SCRATCH/mini-webapp"
```

- **Never run `chat --repo` directly against a committed `examples/*/.tmct/graph.json`** — a live
  session writes session/provenance state back into that fixture, dirtying a checked-in file.
  Copy the example to a `mktemp -d` scratch dir first: capture the path in a variable, clean up
  ONLY that exact path when done — never a wildcard glob (other playtest cycles and agents share
  `/tmp` concurrently).
- Areas 1, 2, 4 (its personal/general half), and 6 don't strictly need an indexed codebase and
  can run against a bare `tmct init --repo "$SCRATCH"` seed if a run wants to isolate them — but
  the standard six-area session (§4) runs all six against ONE codebase-backed repo, since a real
  user doesn't re-init between asking "what can you do" and "what does this module import."
- When a probe needs taught state (inference chains, personal facts), the teach lines are part of
  the same piped script — that keeps the whole scenario in one reproducible command, which is
  what goes in the log.
- Record the exact `printf` script in the log next to its session output. Retest = rerun the
  same command.
- **`--narrate` is the diagnostic tool**: add it (or `TMCT_NARRATE=1`) to see, per turn, which
  strategy matched, which pattern fired, and what the goal inference was. Probe without it
  (clean logs for the doc), diagnose with it.
- `node bin/tmct.mjs memory --repo "$SCRATCH" --verbose` shows what a teach turn actually
  stored — the fastest way to tell a parse failure from a storage/retrieval failure.
- `/help` inside chat lists every query shape tmct claims to support; claims it can't honour
  are edges too.

## 4. The six standing areas — walked every run, in order, in one session

These are not grammar axes (§4.1 covers those, orthogonally) — they're the user-journey
territory a real tmct session actually crosses, roughly in the order a genuine first session
would hit them. Every iteration's probe conversation (§3) moves through all six; vary the
SPECIFIC content (which fact, which topic, which task) run to run, per §1 step 1.

1. **Personal introductions and remembering personal facts shared.** Open the session with a
   self-introduction — a name, a role, an incidental preference ("hi, I'm Priya, I mostly touch
   the frontend", "hey — Sam here, I like short answers"). Don't just check it's accepted:
   reference it again LATER in the same session, unprompted by a direct "what's my name" if
   possible, to test it's actually carried, not accepted-and-dropped. This is a genuinely
   different memory surface from a taught graph fact (area 4) — test it on its own terms.
2. **Orientation with the chat's capabilities.** Ask what tmct can do — `/help`, "what can you
   help me with", "how do I use this", "what kinds of questions can I ask". A new user asks this
   early, for real; the answer must actually orient someone with zero context, and per this
   project's own "verify every offered example, in-state" discipline, any suggested example this
   turn offers must actually be tried later in the same session before counting the turn as a
   real answer.
3. **Finding out about an indexed codebase.** Point tmct at the session's real example repo (§3)
   and explore it the way a developer actually would: concept → instance → its relations → their
   relations, natural phrasing ("what functions are in Task", "what defined saveStore", "what
   about imports"), letting `it`/`that` anaphora carry the focus.
4. **Being taught facts and making inferences on them, including references to topics from the
   ingested codebase.** Teach a fact — general/commonsense, personal, or one that names something
   from the indexed codebase (e.g. "the Store module is the one I maintain") — then ask a
   FOLLOW-UP that requires COMBINING it with something else already known, not just recalling it
   verbatim (teach-then-INFER, not teach-then-recall). The highest-value probes here mix a taught
   fact with a codebase-grounded one in a single inference — a genuinely different, harder path
   than either alone, and one a generic teach-then-infer probe or a pure-codebase drill-down alone
   would not reach. Also probe what a SECOND assertion does to
   a first here — re-teach the same fact, teach a conflicting one, add a dated "as of <year>"
   claim — per the sibling-resolution axis (§4.1), which lives in this area.
5. **Asking for changes in state — planning, framed as a simple code task, not the Hanoi puzzle.**
   tmct's built-in planning demo is Towers-of-Hanoi; this area deliberately asks for a plan
   against the SAME indexed codebase instead — "how would I rename the Store class to
   DataStore", "what would it take to remove this unused import", "plan how I'd add a method to
   X" — exercising `PLAN_CODE_PLANNING.md` Track 5's planning-over-code-states machinery
   (`src/domain/codeplan/`) with real, graph-grounded actions. This is a deliberate shift in
   playtest emphasis toward the code-task shape, not a claim that Hanoi-style planning stops
   being a valid capability to probe elsewhere.
6. **Researching a topic and getting back a digest.** Ask tmct to look something up — a live
   Wikipedia lookup (`/wiki on` first, or `--live-wikipedia`), the local reference corpus, or a
   codebase question broad enough to need the completions/digest pipeline ("give me a detailed
   summary of how X works"). A real answer here reads as a DIGEST — an opener plus grouped,
   sourced content, not one flat sentence or a bare wall — and cites where it came from.

Close the session genuinely (a real thanks/goodbye turn, not just the last structural question) —
a session that flows perfectly in the middle but hits a wall on "cheers, that's everything" still
fails the fluid-conversation bar.

### 4.1 Surface variation within an area (orthogonal — apply for depth, not instead of §4)

Once an area's baseline probe (§4) is in, the productive move for going deeper on IT specifically
is to hold MEANING constant and vary FORM until the answer changes — the surface-variation axis.
Axes worth walking inside whichever area turned up something interesting, or as a spot-check
elsewhere, roughly in order of yield:

- **The paraphrase ladder.** Take a canonical passing query ("what is a dog") and climb:
  drop determiners ("what is dog"), contract ("what's a dog"), wrap in politeness ("could you
  tell me what a dog is"), invert to yes/no ("is a dog an animal"), passive ("what is a horse
  used for" ↔ "what is used for riding"), cleft ("it's a dog that barks — true?"). tmct's
  history says the ladder's upper rungs are where edges live.
- **Relation coverage.** Repeat a passing shape across relations: IsA, HasA, CapableOf, UsedFor,
  PartOf. A shape often works for the relation it was built for and no other.
- **Inference depth.** The grandfather scenario in the example log is the template: teach a
  chain, then query at 1 hop, 2 hops, 3 hops. Find the hop count where inference stops.
- **Negation and quantifiers.** "what can't fly", "is a dog not a cat", "do all dogs bark",
  "which animals can fly". These stress normalize.mjs's frames before any grammar runs.
- **Teach-side variation.** The same fact phrased differently: "ahab is john's father",
  "john's father is ahab", "ahab fathered john", plurals ("dogs are animals"), conjunctions
  ("ahab is male and is the father of john"). Then verify each with the SAME query, so the
  variable is the teach parse alone.
- **Multi-word and awkward terms.** "guinea pig", "ice cream", terms colliding with query
  keywords ("what is a what-if analysis").
- **Anaphora.** "what is a dog" then "can it bark", "what about cats". Context carry-over is a
  known thin spot; establish where it starts failing rather than that it fails.
- **The teach/query boundary.** Bare declaratives ("dogs bark") — teach, query, or refusal?
  Whatever it does, is it the same every time?
- **Sibling resolution and the dated teach** (design: `PLAN_FACT.md`; bench pins: infbench's
  `c2SiblingResolution` template). What does a SECOND assertion do to a first? Walk the four
  shapes: (1) teach the identical fact twice — the re-teach must corroborate onto one fact, never
  duplicate it or read as a contradiction; (2) teach a second object under a multi-valued
  predicate ("a dog has legs", then "a dog has a tail") — both must hold, no disagreement
  warning, and the first still answers; (3) teach a conflicting object under a single-valued one
  ("rex's owner is anna", then "rex's owner is bruno") — both must stay stored AND both must
  surface on the read-back, never one silently dropped; (4) teach a claim dated earlier than a
  live one — "the probe's owner is anna as of 2019", then "the probe's owner is bruno" — and
  confirm the resolution: until the dated-teach frame ships, the "as of" surface being DECLINED
  (not silently stored undated, which would invert the sun/newspaper ordering) is the correct
  behavior to verify; once it ships, the dated record must store, the read-back must show both,
  and the undated live teach must win as the current value. A dated teach that stores WITHOUT its
  date is this axis's highest-value edge — file it, don't shrug it.

Don't force all eight axes into one session — spend them where §4's baseline pass already found
something worth pushing on, and log which axes got real use this run (§1 step 1) so a later run
varies rather than repeats.

## 5. Diagnosing and fixing — the layer map

Run the failing probe with `--narrate` first. Which strategy matched (or that none did) tells
you which layer owns the fix. The interpretation pipeline
(`src/domain/interpret/pipeline.mjs`) runs, in precedence order: normalize → grammar → keyword-spot →
noise-strip → ACE → constructions.

| Symptom | Layer to look at |
|---|---|
| A surface wrapper/rhetorical frame around a shape that already works | `src/domain/interpret/normalize.mjs` (PHRASING_FRAMES, negation frames) |
| A genuinely general question shape nothing handles | `src/domain/interpret/strategies/grammar.mjs` (anchored templates T1–T10) |
| A specific surface construction mis-read by keyword-spot (wrong subject/object direction, agent nouns, genitives, compounds) | `data/templates/constructions/*.toml` — the free-form templating layer |
| Teach sentence not parsed / stored wrongly | `src/domain/grammar/` (ACE grammar, lexicon) — verify with `tmct memory` |
| Parsed fine, answer phrased badly | `src/answer-variants.*`, `data/templates/responses.jsonl`, `src/services/finish.mjs` + `data/templates/grammar-rules.toml` (byte-stable contract — read that file's header first) |

**The templating mindset (this is the important one).** When a fix means adding a special case
to a general rule (an extra `|alternative` in a grammar.mjs regex, a carve-out for one phrasing),
stop and ask whether you're overfitting. The project's preferred move for irregular language is
the construction bank: `data/templates/constructions/` holds closed template families as DATA
(pattern → AST skeleton), loaded by `src/domain/interpret/strategies/constructions.mjs` and validated at
load time against the closed relation/entity vocabularies. This is the same layer that fixed
"store.mjs's importers" / "store.mjs importers" without touching the general grammar. The rules:

- A new bank is a NEW `.toml` file in that directory — the loader picks it up in filename order;
  no code change. Construction ids continue the sequence (T11–T13 exist; take the next numbers).
- Closed is deliberate. Hand-curate the vocabulary; a false-positive match on an unrelated
  phrasing is worse than an honest miss. If you catch yourself wanting a wildcard where the
  closed alternation goes, that's the overfitting alarm ringing on the other side — the shape
  may really belong in grammar.mjs as a general template instead. General shape → grammar.mjs;
  irregular surface realization of an existing shape → construction bank; one weird phrasing
  that generalizes to nothing → consider whether it's an edge worth shipping at all, and if so
  say so in the log rather than distorting a rule for it.
- Invalid entries are dropped at load, never coerced — so a bank fix that silently does nothing
  usually means a `kind`/`entityType` outside the closed vocabulary. Check with `--narrate`.

Every fix ships with a regression test named for the behavior it checks ("resolves 'X's
importers' as a reverse imports query"), never for the playtest that found it. The minimal pair
from §1 step 5 is the test's input.

## 6. What "captured succinctly" means

The log is evidence, not a transcript dump. Per edge:

- **Expectations block** — Given (any prior teach/answers, as a fenced log), When (the probe
  lines), Expected (one line), Actual (verbatim). Two or three probe lines maximum — the
  discriminating ones.
- **Result** — `Fail`, then after the fix, **Retest result** — `Pass` (or
  `Fail (unable to pass)` + one paragraph).
- **Session logs** — the real terminal output, fenced as `txt`, trimmed to the relevant turns.
  Keep the startup banner once (it names the version), not per snippet.

## 7. Stop conditions

The loop ends when the FIRST of these fires:

- **Budget.** The iteration count named at invocation is reached (default 10 if none given).
- **Two no-change iterations in a row.** A no-change iteration is one that ships no code/data
  change: all six areas (§4) were walked this run and every one came back clean. The log still
  gets written (it documents passing coverage across all six areas, with the specific probe
  content used, per §2) and shipped — the instruction to push and roll every iteration stands
  even for a log-only iteration.
- **Plateau.** Three consecutive iterations end `Fail (unable to pass)`. Fixes have stopped
  yielding; further probing is measurement, not improvement. Write a closing note in the last
  log listing the unfixable edges as candidates for a PLAN doc, and stop.

On stop, report to the operator: iterations run, edges found/fixed/unfixable per area (§4),
versions shipped, and which §4.1 surface-variation axes have seen real use vs are still
untouched.
