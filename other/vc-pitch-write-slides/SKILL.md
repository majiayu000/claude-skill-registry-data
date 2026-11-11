---
description: Write a VC pitch deck of at most 10 slides as smd slides
model: opus
---

# Goal
- Given a company description, write a venture capital (VC) pitch deck of at most
  10 slides in smd format
- The deck covers at least: the problem, the solution, the addressable market, and
  the go-to-market plan
- Write an investment pitch, not a lecture. Follow `## Pitch Style`
- Follow `.claude/skills/slides.rules.md`, except where `# Conventions` overrides it
  (tags, sections, `Roadmap`, `Summary`, `References`)
- Follow the slide syntax in `.claude/templates/slides.template.md`
- Follow `.claude/templates/vc_pitch_slides.template.md` for the slide order and
  the content of each slide

# Workflow

## Role
- Act as a startup founder who pitched seed and Series A investors, and as a VC
  partner who has read thousands of decks
- The audience is a VC investment committee: technical, financial, short on time,
  and skeptical
  - Each slide answers one investor question in under 30 seconds of reading

## Input
- The user provides:
  - A company description, notes, or a file `<TOPIC>`. Read the file if given
    - If there is no company description, ask the user once, then stop
  - (Optional) `<COMPANY>`: company name
    - Default: `NewCo`, with a TODO to replace the working name
  - (Optional) `<FOUNDERS>`: founder names
  - (Optional) `<ROUND>`: funding round, e.g., `Seed`, `Series A`
  - (Optional) `<ASK>`: amount raised
  - (Optional) `<NUM_SLIDES>`: number of slides, 9 or 10
    - Default: `<NUM_SLIDES> = 10`. Outside 9-10, use the closest bound
  - (Optional) `<LOGO_PATH>`: logo path relative to the repo root
    - Default: a placeholder logo (see `## Add Logo`)
- Use only facts present in the input
  - Do not invent market sizes, revenue, customers, growth rates, or biographies
  - For each missing fact, write a placeholder and a TODO (see `## Flag Doubts` and
    `## Placeholders and Special Characters`)

## Plan Deck
- Write a one-line pitch `<TAGLINE>` of at most 15 words: the customer, the pain,
  and the outcome
  - E.g., `Cut month-end close from 10 days to 2 for mid-size finance teams`
- Fit the deck in `<NUM_SLIDES>` slides, never more than 10
  - The count includes `* Cover / Company Purpose`
  - The count excludes `* Sources`
- Always keep these 9 slides, the minimum deck
  - `* Cover / Company Purpose`
  - Problem slide
  - Solution slide: includes the product and how it works, with a diagram
  - Market slide: TAM, SAM, SOM, and why now
  - Business model slide: includes unit economics and a 3-year revenue path
  - Go-to-market slide
  - Competition slide
  - Team slide
  - Ask slide: includes the reasons to invest
- Add the Traction slide when `<NUM_SLIDES>` is 10
  - When `<NUM_SLIDES>` is 9, put the traction in one **Traction** lead-in on
    `* Cover / Company Purpose`
- Do not add a slide for the product, why now, existing alternatives, or
  financials, since the slides above already carry them
- Keep the order from `## Deck Structure`

## Add Logo
- If the user gave no `<LOGO_PATH>`, download a placeholder logo showing the company
  name
  ```bash
  > curl -sSL -o <SCRATCH_DIR>/logo.png "https://placehold.co/480x160/0B2545/FFFFFF/png?text=<COMPANY>&font=montserrat"
  > file <SCRATCH_DIR>/logo.png
  ```
  - Replace each space in `<COMPANY>` with `+` in the URL
  - Download into a new, empty `<SCRATCH_DIR>` and confirm `file` reports
    `PNG image data`
  - Copy it to `assets/images/<COMPANY>_logo_placeholder.png` and set `<LOGO_PATH>`
    to that path
  - Add a TODO to replace the placeholder with the real logo
- Never keep the default logo of `type=UMD_slides`. A university logo makes the deck
  read as a lecture

## Write Slides
- Write the metadata block first, then every slide
- Follow `# Conventions` for slide content
- Use the heading of the template slide as the title of each slide (see
  `## Slide Titles`)

## Add Visuals
- Follow `.claude/skills/figure.rules.md`
- Add at least 3 figures
  - A product or solution diagram
  - The nested TAM, SAM, SOM diagram on the market slide
  - The phase diagram on the go-to-market slide
- Put each figure beside its text in 60/40 columns, per
  `.claude/skills/slides.rules.md` `# Visuals`
  - Use 65/35 when the text spills onto an extra page
- Draw TAM, SAM, SOM as nested Graphviz clusters
- Draw go-to-market phases left to right, with `fontsize=16` and subtitle
  `point-size="13"`, so labels stay readable in a 40% column
- Follow `.claude/skills/graphviz.rules.md` and the "Architecture Style" section of
  `.claude/templates/graphviz.template.md`
- Use a `styled-table` for numbers investors compare: competition, unit economics,
  use of funds
  - Follow `.claude/skills/slides.rules.md` `## Typst Tables`

## Flag Doubts
- Put a comment right above each bullet whose content is missing or uncertain
  - **Uncertain**: a number or claim from memory, a self-made estimate, or an
    unverified source
  - **Missing**: a fact the input does not contain
- Use one of these formats, starting at column 0
  ```
  // TODO(gp): Check <WHAT> : <WHY IN DOUBT>
  // TODO(gp): Provide <WHAT> : not in the input
  ```
- Never indent the comment. The preprocessor strips only lines that start with `//`,
  so an indented comment renders inside the slide

## Save Result
- Save the deck to `<OUTPUT_FILE>`
  - If the user gave an output path, use it
  - Otherwise, create `<STEM>.vc_pitch.slides.md` in the current dir
    - `<STEM>` is the input file name without extension, or `<COMPANY>` in lowercase
      with underscores
  - A deck in a course `lectures_source` dir uses the extension `.smd`
  - A standalone deck outside `lectures_source` uses `.slides.md`, which
    `class_scripts/gen_slides.py` treats as standalone
- Say in the slides file how it was generated, with this comment right after the
  metadata block:
  ```
  // Generated by `.claude/skills/vc_pitch.write_slides/SKILL.md`
  ```
- If `<OUTPUT_FILE>` already exists, ask the user before overwriting it

## Render and Check Layout
- Render the deck to `<PDF_FILE>`, which `gen_slides.py` writes next to
  `<OUTPUT_FILE>`
  ```bash
  > gen_slides.py -i <OUTPUT_FILE> --slides_engine typst --notes_to_pdf_args="--skip_action open_pdf"
  ```
- Confirm each slide fits on one page
  - `<PDF_FILE>` must have `<NUM_SLIDES> + 2` pages: the slides, the title page, and
    `* Sources`
  ```bash
  > pdfinfo <PDF_FILE> | grep Pages
  ```
- Build a contact sheet and check every page
  ```bash
  > pdftoppm -png -r 50 <PDF_FILE> <SCRATCH_DIR>/p
  > magick montage <SCRATCH_DIR>/p-*.png -tile 4x -geometry +4+4 <SCRATCH_DIR>/sheet.png
  ```
- Fix each defect, then render again
  - A slide that spills onto an extra page: cut words, inline a formula, or widen
    the text column
  - Overlapping table cells: shorten the text or raise the weight in `col-widths`
  - A placeholder missing from the PDF: escape it (see
    `## Placeholders and Special Characters`)

## Report
- Do not print the slides on screen
- Print only the paths of `<OUTPUT_FILE>` and `<PDF_FILE>`, and the list of all TODO
  comments

# Conventions

## Metadata Block
- Start the file with this block, in this order
  ```
  // type=UMD_slides
  // course_title=<COMPANY>: Investor Presentation
  // lesson_title=<ROUND>: <TAGLINE>
  // Authors=<FOUNDERS>
  // logo=<LOGO_PATH>
  // slides_engine=typst
  ```
  - Escape a placeholder in `course_title` and `lesson_title`, e.g.,
    `// lesson_title=\<ROUND\>: <TAGLINE>`
    - Typst reads a bare `<ROUND>` as a label and drops it
  - Always set `Authors`. The `UMD_slides` default prints
    `Instructor: Dr. GP Saggese` on the title slide
    - List founders alphabetically, as the user gives the names, e.g.,
      `// Authors=GP, Samarth, Vedanshu`
    - If founders are unknown, write `// Authors=<FOUNDERS>`, unescaped, and a TODO
      comment after the block
  - Always set `logo` (see `## Add Logo`)
- Follow `.claude/skills/slides.rules.md` `## First Slide`

## Deck Structure
- Use no `#` and no `##` header. Each header adds a "Table of Content" page, which
  makes the deck read as a lecture
- Place the slides in this order, skipping those not selected
  - `* Cover / Company Purpose`: the one-slide summary of the company
  - Problem slide
  - Solution slide: includes the product and how it works
  - Traction slide
  - Market slide: includes why now
  - Business model slide: includes the financials
  - Go-to-market slide
  - Competition slide
  - Team slide
  - Ask slide: ends with the reasons to invest
  - `* Sources`: last slide, only if the deck cites a source
- Do not add `* Roadmap`, `* Summary`, or `* References`. Use the fixed slides
  `* Cover / Company Purpose` and `* Sources` instead
- Follow the slide order and the content of each slide in the template
  `.claude/templates/vc_pitch_slides.template.md`
  - `* Cover / Company Purpose` carries the content of the template cover
- If the input has no commercial traction, move the Traction slide to just after
  the Market slide
- Group the slides in 5 acts, so that each act answers one investor doubt
  - Hook: `* Cover / Company Purpose`, Problem, Solution
  - Proof: Traction
  - Opportunity: Market
  - Engine: Business model, Go-to-market, Competition
  - People and plan: Team, Ask

## Slide Titles
- Use the heading of each template slide as the slide title
  - Copy the heading text from `.claude/templates/vc_pitch_slides.template.md`,
    without the `#` and without the number
  - Do not reword the title and do not write a headline that states a claim
- Use these titles, in this order, skipping the slides not selected
  ```markdown
  * Cover / Company Purpose
  * Problem
  * Solution and Product
  * Traction (Past Milestones)
  * Market Size and Why Now
  * Business Model and Financials
  * Go-to-Market (GTM) Strategy
  * Competition and Moat
  * Team
  * The Ask
  * Sources
  ```
  - `Sources` is the only title that is not in the template
- Put the key number of the slide in its first lead-in, since the title carries
  none
- **Bad** (a headline, a different title than the template)
  ```markdown
  * Outbound Burns Time, Money, and Domains
  * A \<TAM\> Market, Sized Bottom-Up
  ```
- **Good** (the template title)
  ```markdown
  * Problem
  * Market Size and Why Now
  ```

## Pitch Style
- Do not use `@Tag@` labels (e.g., `@Definition@`, `@Fact@`, `@Naive Solution@`).
  They render as colored lecture labels
- Start every top-level bullet with a bold lead-in of 1-5 words and a colon
  - Put the number in the lead-in when the bullet has one
  - Separate top-level bullets with a blank line
- Use plain English: no formal definitions, no `\triangleq`, no symbols bound to
  quoted meanings
  - Use `$\times$` for a product in a sizing or cost line
- Write about customers in the third person, and name the company
- **Bad** (lecture style: tag and definition vocabulary)
  ```markdown
  - @Fact@: the hit rate of cold outreach is often below 1%
  ```
- **Good** (pitch style: bold lead-in that carries the number)
  ```markdown
  - **Under 1% hit rate**: hundreds of cold emails yield a handful of replies
  ```
- Use these lead-ins per slide
  - `* Cover / Company Purpose`: **What**, **Who pays**, **Model**, **Edge**,
    **Raising**, plus **Traction** when the deck has no Traction slide
  - Problem slide: one lead-in per quantified pain (rate, hours, dollars, risk),
    then **Typical case** for one customer scenario
  - Solution slide: **Today** (how customers cope), **With <COMPANY>** (the
    outcome), then 2-3 benefits (e.g., **Pay on outcome**), then **How it
    works** with one user flow as an `E.g.,` sub-bullet
  - Market slide: **TAM**, **SAM**, **SOM**, **Cross-check**, then **Why now**
    with one dated trend per sub-bullet
  - Go-to-market slide: **Beachhead**, one lead-in per phase (e.g.,
    **Months 0-12**), **Target CAC**
  - Competition slide: the table, then **<COMPANY>'s edge**
  - Business model slide: **Pricing**, **Repeat buying**, **Cost driver**,
    **Unit economics** (table), **Revenue path** with one sub-bullet per year
    for 3 years, then **Assumptions**
  - Traction slide: **Commercial** first, then one lead-in per validation signal
  - Team slide: the founder name in bold, then the role and one credential
  - Ask slide: **The round**, **Milestones**, **Use of funds** (table), then
    **Why invest** with 3 sub-bullets, one reason each, each backed by a slide

## Placeholders and Special Characters
- Escape a placeholder in slide text as `\<PLACEHOLDER\>`. Pandoc drops a bare
  `<PLACEHOLDER>` as raw HTML, and Typst reads it as a label, so it vanishes from
  the PDF
- Keep a bare `<PLACEHOLDER>` in these places
  - `//` comments, including `// Authors=`
  - Typst string cells, e.g., `("NewCo", "<MODEL>")`
  - Graphviz plain labels, e.g., `label="SOM: $<SOM>"`
  - Graphviz HTML-like labels need `&lt;PLACEHOLDER&gt;`
- Write a dollar sign in slide text as `\$`, so pandoc never reads it as math
- **Bad** (the placeholder vanishes and `$` can open math)
  ```markdown
  - **Pricing**: $<PRICE> per meeting
  ```
- **Good**
  ```markdown
  - **Pricing**: \$\<PRICE\> per meeting
  ```

## Problem and Solution
- Show one problem
  - Quantify the pain in dollars, hours, or error rate
  - Name the customer persona that feels the pain
  - Do not mention the product on the problem slide
- Show the solution as a customer outcome, not a feature list
  - Contrast **Today** with **With <COMPANY>** to show why current tools fail
  - Add at most 3 benefits after **With <COMPANY>**
- **Bad** (product on the problem slide, no number, no persona)
  ```markdown
  * Problem

  - **Problem**: finance is hard and our AI platform makes it easy
  ```
- **Good** (one pain, one persona, numbers in the lead-ins)
  ```markdown
  * Problem

  - **\<DAYS\> days to close**: mid-size finance teams close the books in
    \<DAYS\> days each month

  - **\<HOURS\> analyst hours**: go to manual reconciliation in each close
  ```

## Addressable Market
- Size TAM, SAM, and SOM, each in one bullet with the figure in the lead-in
  - **TAM**: yearly revenue if every potential customer buys
  - **SAM**: the part of TAM reachable with the current product, region, and channel
  - **SOM**: the revenue captured within a stated number of years
- Use a bottom-up calculation as the main estimate. Top-down figures (analyst
  reports) are allowed only as a cross-check
  - Investors reject "we only need 1% of a huge market"
- Write the calculation as plain arithmetic: customers $\times$ units $\times$ price
- State the currency, the time unit (per year), and the year of each figure
- Attach a source to every number in the slide text, and list it on `* Sources`
- **Bad** (top-down, no source, no SAM or SOM)
  ```markdown
  - **Huge market**: the global logistics software market is worth \$50B

  - **1% share**: is enough to reach \$500M
  ```
- **Good** (bottom-up, plain arithmetic, doubts flagged)
  ```markdown
  * Market Size and Why Now

  // TODO(gp): Check <N> and <ACV> : not in the input, find a cited source
  - **TAM \$\<TAM\> a year**: \<N\> \<CUSTOMER_TYPE\> in \<REGION\> $\times$
    \$\<ACV\> a year each

  - **SAM \$\<SAM\> a year**: \<N_REACH\> customers reachable with today's
    product and channel

  - **SOM \$\<SOM\> in \<YEARS\> years**: \<SHARE\>% of SAM, starting from the
    beachhead
  ```

## Go to Market
- Name the beachhead: the one customer segment to win first
- For the beachhead, state the buyer, the channel, and the sales motion (self-serve,
  inside sales, or enterprise sales)
- Write 3 phases, one bullet each, with the time window in the lead-in
  - Each phase has a target segment, a channel, and one numeric milestone (e.g.,
    `\<N\> paying customers`, `\$\<ARR\> ARR`)
- State the target customer acquisition cost (CAC) and the payback period
- Show the phases in a left-to-right Graphviz diagram, beachhead first
- **Bad** (no segment, no channel, no milestone)
  ```markdown
  - **Growth**: leverage partnerships and digital marketing to scale
  ```
- **Good**
  ```markdown
  - **Beachhead**: \<SEGMENT\>, bought by the \<BUYER_TITLE\>, sold through
    \<CHANNEL\> with \<MOTION\>

  - **Months 0-12**: win \<SEGMENT\>, reach \<N\> paying customers

  - **Months 12-30**: expand to \<ADJACENT_SEGMENT\> via \<CHANNEL_2\>, reach
    \$\<ARR_1\> ARR

  - **Months 30-60**: scale through \<NEW_CHANNEL\>, reach \$\<ARR_2\> ARR

  - **Target CAC**: \$\<CAC\> per customer, paid back in \<MONTHS\> months
  ```

## Competition
- Show 3-5 real alternatives, including the status quo (spreadsheets, in-house
  tools, manual work)
- Never claim "no competitors"
- Use a `styled-table` with the company in the last row and `bold-first-col: true`
  - Put the table at the top level of the slide, with no bullet above it
  - Choose 3-4 columns that matter to the customer
- Follow the table with one **<COMPANY>'s edge** bullet: the durable difference
- **Bad** (no competitors)
  ```markdown
  - **Competition**: \<COMPANY\> has no direct competitors
  ```
- **Good**
  ````markdown
  ```{=typst}
  #styled-table(
    headers: ("Option", "<CAPABILITY_1>", "<CAPABILITY_2>", "<CAPABILITY_3>"),
    rows: (
      ("Spreadsheets", "No", "Manual", "Free"),
      ("<COMPETITOR>", "Yes", "No", "High"),
      ("<COMPANY>", "Yes", "Yes", "Low"),
    ),
    bold-first-col: true,
  )
  ```

  - **\<COMPANY\>'s edge**: \<DURABLE_DIFFERENCE\>
  ````

## Business Model, Traction, Team, Ask
- **Business model**: state who pays, for what, how much, and how often
  - Show the unit economics in a one-row `styled-table`: price per unit, cost per
    unit, gross margin, and lifetime value (LTV) to CAC ratio
  - State the cost driver in plain English, e.g., `cost per meeting = cost per
    prospect $\times$ prospects per meeting`
  - Show the revenue path for 3 years, one number per year, with the
    assumptions behind it, e.g., customers $\times$ price per year
  - Flag each missing value
- **Traction**: lead with commercial metrics (revenue, paying customers, letters of
  intent), each with a value and date, e.g., `\<N\> customers as of \<MONTH_YEAR\>`
  - If there is no traction, write the strongest validation signal (pilots, letters
    of intent, waitlist size) and flag it
- **Team**: one bullet per founder, with the name in bold, a role, and one
  verifiable credential related to the problem
- Ask: state the amount `<ASK>`, the round, and the runway in months
  - List 2-3 milestones the round reaches, ending with the one that justifies the
    next round
  - Show use of funds as a `styled-table` beside the milestones (60/40 columns),
    with shares summing to 100%
- **Why invest**: close the Ask slide with 3 reasons, each backed by a slide of the
  deck

## Claims and Style
- Use measurable statements
  - **Bad**: `a revolutionary, best-in-class platform`
  - **Good**: `cuts reconciliation time from <X> hours to <Y> hours`
- Do not use hype words (revolutionary, disruptive, game-changing, world-class,
  best-in-class, cutting-edge)
- Name the company, not "it" or "we", in the problem and solution bullets
- Cite a source in the slide text for every external number, and list it in
  `* Sources`
  - Format each entry as in `.claude/skills/slides.rules.md` `## References Slide`
    and `.claude/skills/references.rules.md`
  - Verify each source exists before listing it
  - If a source cannot be verified, add ` ???` after its link and a TODO comment

## Slide Pitfalls
- Avoid these defects, on top of the ones in the sections above
  - `* Cover / Company Purpose`: a vague mission statement instead of customer,
    pain, and outcome
  - Solution slide: a feature list, roadmap items shown as shipped, or a dense
    architecture diagram
  - Traction slide: vanity metrics (downloads, page views) with no link to
    revenue, and future milestones, which belong on the Ask slide
  - Market slide: undated trends and generic statements (e.g., "AI is growing
    fast")
  - Business model slide: several unproven revenue streams, or a hockey-stick
    revenue path with no assumptions
  - Competition slide: a 2x2 chart where only the company sits in the top-right
    corner
  - Team slide: full CVs and credentials unrelated to the problem
  - Ask slide: an ask with no milestones, or no call to action

# Constraints
- Total slides: at most 10, counting `* Cover / Company Purpose`, excluding
  `* Sources`
- Each slide fits on one PDF page
- At most 7 top-level bullets per slide and 3 lines per bullet
- Wrap text at 80 columns
- No `@Tag@` labels and no `#` or `##` headers
- No emoji and no non-ASCII characters (use LaTeX, e.g., `$\to$`)
- No `---` page separators and no period at the end of a bullet
- Do not join two clauses with a dash inside a bullet. Use a sub-bullet or a colon
- Do not use `\text{...}` in math mode
- Do not write `// From:` lines, since a pitch has no source slides
- Do not invent facts. Every figure comes from the input, or is a placeholder with a
  TODO comment

# Verification
- [ ] Count the slides. The output must have at most 10
  ```bash
  > grep '^\* ' <OUTPUT_FILE> | grep -v '^\* Sources$' | wc -l
  ```
- [ ] Confirm the fixed slides and the four required topics are present
  ```bash
  > grep -c '^\* Cover / Company Purpose$' <OUTPUT_FILE>
  > grep -c '\*\*With ' <OUTPUT_FILE>
  > grep -cE '\*\*(TAM|SAM|SOM)' <OUTPUT_FILE>
  > grep -c '\*\*Beachhead\*\*' <OUTPUT_FILE>
  ```
- [ ] Confirm every TODO comment starts at column 0
  ```bash
  > grep -n '^ \+// TODO' <OUTPUT_FILE>
  ```
- [ ] Confirm each number that has no source has a `// TODO(gp)` line above it
- [ ] Confirm the deck has at least 3 figures and at least one `styled-table`
- [ ] Confirm `// logo=` points to an existing file and `// Authors=` lists the
      founders in alphabetical order
- [ ] Confirm the slide order follows the template
      `.claude/templates/vc_pitch_slides.template.md`
- [ ] Confirm each slide title equals a template heading (see `## Slide Titles`)
  ```bash
  > grep '^\* ' <OUTPUT_FILE>
  > grep '^# ' .claude/templates/vc_pitch_slides.template.md
  ```
- [ ] Confirm that the slides render and each slide fits on one page (see
      `## Render and Check Layout`)
- [ ] The slides file says it was generated by
      `.claude/skills/vc_pitch.write_slides/SKILL.md`
