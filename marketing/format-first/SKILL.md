---
name: format-first
description: >
  Decide WHAT SHAPE of content to make, and refuse the platform folklore that
  circulates as fact. Encodes a claim set traced to primary sources — Meta's own
  engineering writeup and Transparency Center system cards, Mosseri's actual posts,
  and the psychology literature behind "hooks" and repetition — separating what is
  documented, what is hypothesis, and what is unsupported. Ships a linter that GRADES
  each claim — refuted, contested, unverified, folklore — and errors only on the ones
  contradicted by a primary source that was actually loaded, because "no source found"
  is a statement about a search, not about the world. The core move is choosing a FORMAT (visual grammar x script
  structure) as the invariant and letting topic vary, rather than the reverse.
  Use when, PRE-PRODUCTION: (1) choosing what shape a piece should take before it
  is written, (2) deciding how often to repeat a format and when to rotate it,
  (3) verifying a platform/algorithm claim from a course, thread, or guru,
  (4) auditing a draft or strategy doc for recommender folklore and untraceable
  statistics. NOT FOR: producing the artifact (use content-creation), generating
  visuals (use content-engine), page markup (use seo-llmeo), running an engagement
  loop (use social-intelligence), or **anything about a finished piece's reach,
  length, or citation by AI answer engines — that is citable, including the
  short-post-vs-long-article decision.** Triggers on "what format should I use",
  "is the algorithm punishing me", "should I post daily", "does this algorithm
  claim hold up", "which format should I repeat", "3-second hook", "verify this platform
  claim".
---

# format-first

Most content advice optimizes the wrong variable. It picks a **topic** and varies the
shape. This inverts that: pick a **format** and let the topic vary.

A format is *visual grammar* (how it is shot, framed, paced) x *script structure*
(where the beats land). It is the thing a viewer recognizes before they process a
single word — and it is the thing almost nobody chooses deliberately.

## Epistemic stance (read this before quoting anything)

This skill separates these grades, and the separation is the point:

| Grade | Meaning | Example |
|---|---|---|
| **Documented** | The operator publishes it | ANN retrieval over item embeddings; `"similarity to other reels"` is a named input signal |
| **Hypothesis** | Plausible, no source located here establishes it | that format consistency lowers embedding variance and thereby improves retrieval | <!-- format-lint: allow=embedding-variance-asserted -->
| **Refuted** | Contradicted by a primary source that was loaded | the misquoted "polished aesthetic" line |
| **Contested** | The literature genuinely disagrees | whether subliminal exposure is stronger | <!-- format-lint: allow=subliminal-stronger -->
| **Unverified** | Origin could not be located — **not** proof of falsity | the 3–5x sends weighting; a widely-quoted effect size |

The single most important line: **no source in the set searched here describes
format-level clustering.** That set is Meta's own published material — the Explore
engineering writeup, the Reels Chaining system card, `about.instagram.com`, Mosseri's
accounts, the Transparency Center — enumerated in `references/evidence-map.md` §1.

By this skill's own grades that is `unverified`, not `refuted`. Absence from an operator's
own description of its system is real evidence and stronger than a failed keyword search,
because those pages exist to enumerate ranking inputs. It is not proof: the systems are
proprietary and nothing obliges the published descriptions to be complete. The positive
mechanism — that consistency improves retrieval — is a working hypothesis with a
plausibility argument. Say so, in both directions.

## The loop

1. **Choose a format, not a topic.** Highest-leverage decision, almost never made
   deliberately.
2. **Probe, do not guess.** Watch several instances of a candidate format through to the
   end, then see whether the feed serves you more of that shape. If it does, the shape has
   a resident audience the recommender already serves. This is a *behavioural* test —
   valid regardless of whether the embedding hypothesis holds. (No source located here specifies
   how many instances; a handful is enough to notice the shift.)
3. **Copy the skeleton, supply your own substance.** Structure is fair game; content
   is not — and reposting others' content is the one thing that triggers a real
   account-level gate (Instagram's originality policy de-recommends primarily
   non-original accounts; it does not touch followers).
4. **Repeat it.** The counterintuitive part — and the part resting on the hypothesis
   above, not on a measured result. The argument is that consistent items are easier for
   a similarity-based retriever to match to an audience that already engaged. Treat it
   as the best available guess, and watch your own numbers.
5. **Hold more than one format; rotate on measured decay.** No source located here supports a specific
   count or interval — rotate on your own numbers. The wearout literature is *laboratory
   stimulus* research and transporting it to platform formats is an analogy, not a
   finding; what it does support is that liking rises then falls with repetition, and that
   the curve differs by modality (**visual inverted-U; auditory came out U-shaped**), so
   do not port repetition advice from video to audio.
6. **Calibrate the hook to existing knowledge.** A curiosity gap only fires if the
   viewer already has enough context to perceive it as a gap. This is why generic hooks
   fail on cold audiences — structurally, not for craft reasons.
7. **Match the signal to the goal.** Likes weigh slightly more for *connected* reach,
   sends slightly more for *unconnected*. "Would someone send this?" is the growth
   question; "was that satisfying?" is the retention question.

## Expectations, calibrated

- **Expect a heavy tail, not a hit rate.** The operator whose method seeded this skill
  reported most of their own posts underperforming even after a breakthrough. That is one
  self-reported account, not a measured base rate — do not quote a ratio.
- **An audience is not a delivery guarantee.** In a study of 347 TikTok users and 9.2M
  recommendations, only 10.3% of *viewed videos originated from followed accounts*
  (https://doi.org/10.1145/3613904.3642433). Note what that does **not** say: it measures
  video origin, not delivery path, and it is TikTok rather than Instagram. It does not
  establish that reach is re-earned per item — it establishes that most of what people
  watch does not come from accounts they follow.

## When the audience can verify

The default law is that reach selects for the *legibility* of expertise rather than its
correctness — **because most audiences cannot check**. If yours can (technical,
professional, scientific), that inverts: correctness stops being a moat choice and
becomes closer to a distribution requirement. You cannot out-polish a full-time creator,
and you do not need to. The differentiated format for a builder is usually the one that
*shows the work*: take a claim everyone repeats, traverse to the primary source, report
what survives.

Guard against the failure that pairs with it: an artifact that performs its own claimed
mechanism on you and offers the sensation as proof. Feeling an effect is not evidence
that the proposed explanation of it is correct.

## The gate (deterministic)

```bash
python3 scripts/format_lint.py DRAFT.md            # ERROR on refuted claims
python3 scripts/format_lint.py DRAFT.md --strict   # warnings fail too
python3 scripts/format_lint.py - --json            # stdin, machine-readable
```

Severity follows the ledger's **grade**: of the claim rules, only `refuted` (contradicted
by a primary source that was loaded) exits non-zero. Malformed lint controls — an unclosed
fence, an unclosed or nested `disable` — also exit non-zero, because a silently disabled
gate is worse than a noisy one. `contested`, `unverified`, `folklore` and
`hypothesis_as_fact` are WARN — because "I could not find a source" is a statement about a
search, not about the world, and a gate that conflates the two manufactures the false
confidence it exists to prevent. Use `--strict` to fail on warnings too.

Sentences that **negate, correct, or attribute** a claim do not fire, so the linter does
not punish the corrections it exists to promote. Fenced blocks and well-formed YAML
frontmatter are exempt; a leading `---` horizontal rule is not. Suppress narrowly with
`<!-- format-lint: allow=<rule-id> -->` (that line only) or a `disable`/`enable` region —
an unclosed or nested region is itself an ERROR, and any region that hides a finding is
reported as one (`suppressed-findings`, naming what it hid and where).

**The bypasses, stated plainly**, because a gate whose escape hatches are undocumented is
a gate you cannot reason about:

| Bypass | Scope | Why it exists |
|---|---|---|
| `<!-- format-lint: allow=<id> -->` | that line, that rule | quoting a claim in order to correct it |
| `<!-- format-lint: disable -->` … `enable` | the region | a block quotation; the region reports what it hides |
| a resolvable URL/DOI in the same paragraph | that finding, **only for rules that opt in** | see below |
| an unclosed fence | everything after it | which is why it is an ERROR |

**A disable region cannot hide anything quietly.** Whatever it suppresses is reported as
`suppressed-findings`, naming the rules and the line range:

```
WARN  L2  (suppressed-findings · lint_control)  «format-lint: disable»
      This region hides 2 finding(s) on lines 3-4: algorithm-punishes, three-second-hook.
```

It is the one guard here with no threshold in it.

That sample sits in a fenced block for a reason, and the reason is worth a sentence: a rule
id such as `algorithm-punishes` contains the very string its own rule matches, so quoting <!-- format-lint: allow=algorithm-punishes -->
the linter's output in prose makes the document flag itself. Fence the output, or mark the
line — the second option is what the line you are reading does.

Its severity is **inherited from the worst thing it hides**. Suppressing warnings is
ordinary editorial practice and stays a WARN; suppressing an ERROR is itself an ERROR, so
wrapping a refuted misquotation in a disable region cannot turn a failing document into a
passing one.

That is deliberate. A coverage-ratio guard used to live here, erroring when a region
covered "most" of a document, and six consecutive review rounds defeated it with six
different ways of padding the denominator: fenced code, frontmatter, lint's own markers,
bare `---` rules, `-` bullets, `|---|---|` separators, `>`, `#`, and finally ordinary HTML
comments. Each round closed one shape and left the class open, because a ratio over
"prose" invites an argument about what counts as prose and every answer was wrong at a new
edge. Reporting the fact instead ends the argument: padding cannot change what a region
hid.

The citation bypass is the one to watch. A WARN-grade rule asserts *"this circulates with no located
source"*, so a sentence that **supplies** a source has already done what the rule asks —
`"According to Instagram, its algorithm demotes primarily non-original accounts:
https://creators.instagram.com/blog/rewarding-original-creators-on-instagram"` is true,
cited, and was flagged as folklore until this existed — the sentence you just read is
itself suppressed by the rule it describes.

The citation must be a **resolvable locator**: an http(s) URL with a real host and a path,
a DOI in either form, or an arXiv / PubMed / PMC identifier — `arXiv:2301.00001` and
`PMID: 12345678` included, not only their URL forms. A bare `example.com/page` does not
suppress, and neither does a naked `https://`, a malformed host like `https://..com/path`,
or an identifier embedded in another word like `NOTPMC1234`. Note that `references/evidence-map.md` cites several sources as
backticked bare domains — that house style is *not* a suppression marker, deliberately: a
bypass should be narrower than a citation convention, not wider. The consequence is that a
resolvable link in the same paragraph silences those two grades' claims in that paragraph.

The cut is **per rule**, declared as `citation_resolves` in the ledger, and the question it
answers is narrow: *does supplying a source answer THIS rule's complaint?* Four of eleven
rules say yes. The rest say no, for three different reasons:

- **The literature disagrees** (`contested`). Citing one side does not settle a
  disagreement.
- **A mechanism is asserted as established** (`hypothesis_as_fact`). A citation does not
  make it so.
- **The complaint is about source QUALITY, not source existence.** `three-second-hook`'s
  finding is that every located source is a content farm — so a URL would satisfy the
  bypass while *confirming* the complaint. A regex cannot tell a content farm from a
  journal, so this rule does not opt in.

Two coarser cuts were tried and both were wrong. Keying on **severity** swept in
`contested` and `hypothesis_as_fact`, which a cross-model review caught. Keying on
**grade** still swept in `three-second-hook` and `post-daily`, which probing the fix
caught. An absent key means no bypass: it must be opted into, never inherited.

The scope is the **paragraph**, deliberately narrower than the ±3-line window the precision
rule uses. A line window let a URL in a *different* paragraph — even one **above** the
claim — silence it, which turns "cite your source" into "put a link somewhere nearby".
Block scope still spans a hard wrap, which is the only thing it ever needed to span.

Extend it by editing `references/claims-ledger.json` — pattern, message, and the
correct replacement. Every rule needs both polarities in `tests/`.

**What counts as a citation is code, not configuration.** It used to be a ledger field, and
guarding it turned out to be impossible in that shape: any finite set of "this must not
count" examples can be evaded by a pattern written against it, and any finite set of "this
must count" examples wrongly rejects a legitimately narrower policy such as DOI-only. The
two pull against each other by construction. A resolvable locator — an http(s) URL with a
path, a DOI, an arXiv, PubMed or PMC id — is now fixed in the code, because making it
configurable was making the gate configurable into silence.

**The ledger is validated strictly, including its key names.** An unknown top-level key or
rule key is an error, not an extension point: `precision_without_sources`, one letter off,
would otherwise load cleanly and switch off an entire rule class while the run kept
reporting documents as clean. Nothing may quietly change *what is checked* without changing
*what is said*. Nor may a `refuted` rule opt into the citation bypass, nor a pattern or
citation marker match the empty string — each of those is a way to configure the gate into
silence, and each is refused at load.

**Before you trust it, sweep your own archive.**

```bash
python3 scripts/corpus_sweep.py ~/writing                       # what fires, per rule
python3 scripts/corpus_sweep.py ~/writing --compare old.json    # what a ledger edit changed
```

A rule that fires on a third of your existing work is a rule you will learn to ignore, and
a widened pattern is where the next false positive comes from. `--compare` runs both
ledgers over the same tree and prints only the delta; every *added* finding has to be a
true positive or the coverage was bought with noise. That check is not decorative — the
first draft of the word-form-multiplier rule added three findings across 3,328 files and
**two of them were the enumeration idiom** ("the problem is threefold"), which is why the
rule now requires a measurement context. Rerun the command to regenerate those numbers.

## Anti-rationalization

| Excuse | Reality |
|---|---|
| "I'll pick a format once I know what to say." | Backwards. The format is the container; topic fills it. Choosing topic-first is why output scatters. |
| "This creator posts daily, so cadence works." | Survivorship. No source located here evidences volume-as-strategy, and it is precisely what the source case study spent two years disproving. |
| "The 3-second hook is settled." | A targeted search found no peer-reviewed basis — only content farms and platform-vendor marketing. | <!-- format-lint: allow=three-second-hook -->
| "A precise number makes it credible." | Precision is rhetorical and freely available. It does not entail that a measurement happened — run the linter. |
| "The algorithm is punishing my account." | No per-format punitive state appears in the sources searched (evidence map §1). There is one real account-level gate and it is about originality. | <!-- format-lint: allow=algorithm-punishes -->
| "It worked on me, so the explanation is right." | That is the counterfeit-verifier move. Sensation is not a discriminating test between hypotheses. |

## Provenance

Derived from `broomva/workspace` BRO-2145 (PR #376, merged `195a9e54`): a full ingest of
a paid-acquisition funnel plus its 36:56 sales video, transcribed locally, with every
load-bearing claim traced to a primary source. **That upstream research arc** was
cross-reviewed over three rounds scoring 2/10 -> 5/10 -> 6/10, catching two genuine errors
in it.

**This skill's own review record is separate, and long.** Twenty-two cross-model
adversarial rounds, scoring **2, 5, 5, 5, 6, 6, 5, 5, 6, 6, 5, 6, 5, 6, 6, 6, 6, 6, 6, 6,
8** (one round timed out before rendering a verdict, though it produced a real finding),
plus a dogfood pass against a real unseen article that found two defects all 47 tests had
missed. It passed on the twenty-second.

**Eighteen rounds sat at 5-6, and the reason is the most useful thing here.** At round 21
the reviewer was asked directly whether that reflected a defective artifact or a surface a
finite review cannot exhaust, and answered: *defective* — "twenty rounds finding repeated
silent bypasses in the same core detector is not merely arbitrary-input
inexhaustibility." It was right. Three consecutive rounds had each found one branch of the
citation-locator alternation missing a boundary condition, and I had been adding the missing
boundary each time. A rule spelled out per branch is a rule you can forget once per branch.

Replacing the per-branch boundaries with a single token-alignment invariant — applied to
every match whichever branch produced it, so that adding a branch cannot reintroduce the
bug — moved the score from 6 to 8 in one round, and the reviewer withdrew the diagnosis:
"the defective per-branch shape is gone."

Coverage went 47 tests to 184, with a mutation proof for every fix. What the rounds found:

- **Universal-absence phrasing** — the defect this skill exists to prevent, in this skill.
  Sites throughout asserted absence as a property of the world rather than of a search:
  format clustering "documented nowhere", absent from "any PUBLIC documentation", "there
  is no per-format punitive state", "unevidenced", "every source is a content farm", "no
  source establishes". Every one is a claim about a *search*, which is precisely the grade
  this skill defines as `unverified`.

  It took four passes, and the reason is worth more than the count: the first three swept
  for the *wording* already found, so each pass caught only rephrasings of the last. The
  pass that converged swept for the **shape** — any sentence asserting absence without
  naming what was searched — and found sites the wording-based greps could not see. A
  count produced that way is a count of what the pattern happened to match, so none is
  quoted here; the sites that remain quoting the old phrasings are these, describing the
  defect.
- **Fence tracking** treated any ` ``` ` or `~~~` as a toggle, so a ` ``` ` inside a
  ` ```` ` block closed it early and the rest was linted as prose. A fence is now a
  character *and* a length, and a closing run must carry no info string.
- **Frontmatter parsing**, twice. A bare ` ``` ` in a YAML value opened a fence no `---`
  could close, so the entire document went exempt and its claims were silently missed;
  frontmatter now resolves before the fence scan. And an *indented* `---` inside a block
  scalar was mistaken for the closing delimiter, ending the frontmatter early and linting
  YAML as prose; the delimiter is now column-zero only.
- **The citation bypass**, which a reviewer's counter-example forced into existence and a
  later round twice narrowed: first from a ±3-line window to the claim's own paragraph (a
  URL in a *neighbouring* paragraph was silencing claims), then from "any WARN grade" to
  `unverified` and `folklore` only — because `contested` means the literature disagrees,
  and citing one side of a disagreement does not settle it.
- **A vacuous guard, deleted.** `citation_markers` was a ledger list no code path read,
  and a test asserted properties of it under the docstring "Regression on a real finding".
  It passed whatever the linter did. The field is gone; the test now exercises the regex
  the linter actually compiles, in both polarities.
- **Paraphrase coverage**, widened where it was cheap and honest: anthropomorphic verbs
  beyond "punish" (demote/suppress/throttle/shadowban/bury/deprioritise), cadence phrased
  as "each day" or "seven days a week" or in the past tense, the variance hypothesis in
  five more verbs, and word-form multipliers. Each widening carries a paired negative
  fixture and was swept against 3,328 real files.

**The exit code is the only signal, so it is classified deliberately.** `0` clean, `1`
findings, `2` bad input. A ledger fails to load in three unrelated ways and they are not
conflated: anything about the **path or content you supplied** (missing, permission-denied,
a directory, not UTF-8, not JSON, schema-invalid, a pattern that will not compile) exits 2
with no traceback, because you fix the ledger; anything about the **machine** (out of
memory, a failing disk) propagates with its real traceback, because calling that "bad
input" would send you to edit a ledger that is fine; and `KeyboardInterrupt` is never
caught at all.

**Still known-open.** A ledger is **trusted configuration**. Its patterns are validated at
load, but a pattern that *compiles* and then
explodes at match time (`(a+)+$`) loads cleanly and will hang the run. Detecting that is a
halting problem in miniature, and a heuristic for it would be a weaker gate than the one it
guards. Treat a ledger the way you treat a linter config: as code you are choosing to run.

The matcher is regex-over-text, so a claim stated in words the ledger does not list still
passes; the widenings above narrow that gap, they do not close it.
Block boundaries are line-structural, not a real Markdown parse. Do not read a clean run as
proof a document is sound; read it as proof it contains none of the specific strings in the
ledger. Full graded claim set: `references/evidence-map.md`.

Recheck the ledger after **2027-02-12** — platform documentation moves.
