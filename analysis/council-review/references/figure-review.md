# Gate F - Figure & Visualization Integrity (conditional)

This gate runs **only if the work actually contains figures** (plots, diagrams,
schematics, tables presented as exhibits, rendered results panels). If the target
has no visual exhibit, mark Gate F **N/A - no figures present** and move on. Do not
invent a figure critique for a text-only draft, and do not down-rank a proposal for
lacking figures it isn't expected to have yet.

**Only critique what you can actually observe.** Figures often arrive as images the
reviewer cannot truly see (a PDF raster, a `.png` you can't open, a figure referenced
but not attached). Do not hallucinate a visual critique. If you cannot inspect the
figure itself, say so explicitly and restrict Gate F to what *is* observable: the
caption text, the panel references, and whether the claim the figure is cited for is
supported by the caption. Never invent axis ranges, colors, or error bars you did not
see. A confident critique of a figure you couldn't view is itself a Gate-0-style
integrity failure of the review.

When figures *are* present and inspectable, they carry a large share of a paper's
persuasive load:
a reviewer often forms a verdict from the abstract plus the figures before reading
the body. A figure that is unclear, over-loaded, or quietly dishonest costs the
paper more than a clumsy paragraph. This gate judges each figure on four axes, then
checks the figure set as a whole.

The four axes, per figure:

## F1 - Message / takeaway

- Does the figure make **one** clear point, and can you state it in a sentence?
- Does the **caption state that takeaway**, or is it a bare label ("Figure 3:
  results")? A caption that only names the axes forces the reader to reverse-engineer
  the point. The strongest captions lead with the finding ("X exceeds baseline at
  every layer; error bars are 95% bootstrap CI"), then define the elements.
- Is the figure **self-explanatory** - understandable from figure + caption alone,
  without hunting through the body text for what a track, color, or arrow means?
- Is there a figure at all for each **headline claim**? A central claim with no
  supporting figure or table is a finding (it reads as unsupported). Conversely, a
  figure carrying no claim is clutter.

**FAIL looks like:** a caption that states no result; a panel whose meaning is
undecipherable without three paragraphs of body text; a figure the reader cannot
summarize in one sentence.

## F2 - Honesty of the visual encoding

This is where figures overclaim without a single overstated word. Owned jointly
with Boromir (overclaim) and Aragorn (provenance).

- **Axes:** truncated / non-zero baselines that inflate a tiny effect; dual y-axes
  that manufacture a correlation; log scale used silently to flatten a blow-up;
  inconsistent axis ranges across panels being compared.
- **Uncertainty:** are there **error bars / CIs / spread**, and does the caption say
  what they are (SD, SEM, 95% CI, n)? Bars without a stated meaning are
  uninterpretable. A bare mean with no spread is a Gate 1 problem made visual.
- **Baseline / ceiling drawn:** is the **chance line / noise ceiling** actually on
  the plot, or does the eye get to read "high" with nothing to read it against?
- **Aggregate vs anecdote:** is this the *distribution* or a **hand-picked example**?
  A single flattering trace narrated as typical is the visual form of cherry-picking.
- **n and units:** is the sample size behind each point recoverable? Are units and
  normalization labeled?

**FAIL looks like:** a bar chart starting at 0.9 that turns a 1% gain into a
skyscraper; a "representative" example with no aggregate; accuracy bars with no
error bars and no chance line.

## F3 - Readability & accessibility

Grounded in journal figure guidance (Nature, Science): a figure should be as simple
as is compatible with clarity, and comprehensible to a reader from a related field.

- **Colorblind-safe:** no red/green as the sole distinction; prefer blue-orange or
  viridis-family palettes; never rely on color *alone* to encode meaning (add shape,
  pattern, direct labels).
- **Legibility:** are labels, ticks, and legend text readable at print size? Tiny
  fonts and 12-item legends are a readability FAIL.
- **Overload:** too many series, panels, or annotations competing for one point.
  Small-multiple restraint beats a single dense panel.
- **Redundancy:** a figure that should be one sentence or a two-number table. Journal
  guidance says data that can be stated briefly in text should not become a figure.

**FAIL looks like:** a 9-line red/green spaghetti plot; a legend no one can map to
the lines; a figure conveying a single number.

## F4 - Claim-figure correspondence

The cross-check between what the text asserts and what the picture actually shows.

- Does the figure **support the sentence that cites it**, or is it decorative /
  loosely related?
- Does a figure quietly show a **null or a mixed result** that the abstract narrates
  as a clean win? (Panel shows overlapping distributions; text says "clearly
  separates.") That mismatch is a **Blocker** - the strongest kind of figure finding.
- Are panels referenced in order and all referenced panels present (no "Fig 4c" that
  doesn't exist, no orphan panel)?

**FAIL looks like:** abstract claims separation; the figure shows overlap. Text says
"monotonic improvement"; the plot has a dip. A cited panel that isn't in the figure.

---

## Figure-set level

After the per-figure pass, judge the set:

- **The 30-second read.** Skim only the abstract + figures + captions. Do you arrive
  at the paper's thesis? If the figures don't carry the argument on their own, the
  paper is under-built visually, even if every individual figure is fine.
- **One figure = one job.** Is there a redundant pair making the same point? A
  missing figure for a claim that badly needs one (usually the main result or the
  key ablation)?
- **The money figure.** Name the single figure the paper's contribution rests on.
  Apply F1-F4 to it hardest. If the money figure is weak, that is the review's
  highest-leverage fix.

## How Gate F feeds the verdict

- A **Blocker** (F4 mismatch: figure contradicts a central claim) is treated like any
  Gate-level Blocker and can force REJECT / MAJOR REVISION on its own.
- F2 dishonesty (misleading axes, missing uncertainty on the headline figure) is at
  least **Major** - it inflates the reader's read of the evidence.
- F1 / F3 issues are usually **Minor** in gatekeeper mode but are **first-class,
  generative feedback** in development mode: this is where the skill helps the paper
  land, not just survive.

## Development-mode figure feedback (generative, not just fault-finding)

When the user is still writing (development mode), don't stop at PASS/FAIL. For each
weak figure give the **one edit that raises it most**:

- Rewrite the caption to lead with the takeaway (offer the sentence).
- Name the specific encoding fix (add the chance line; add 95% CI whiskers; switch
  the red/green to viridis; start the axis at 0; split the dense panel into two).
- If a headline claim has no figure, propose the figure that would carry it (what's
  on each axis, what the reader should see).
- Point at the money figure and say what would make it undeniable.

The test of good figure feedback: the author knows exactly what to redraw and why it
will read as stronger evidence.
