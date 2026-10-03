---
name: ai-council
description: "Run any question, idea, or decision through a council of 5 AI advisors who independently analyze it, peer-review each other anonymously, and synthesize a final verdict. Adapted from Andrej Karpathy's LLM Council methodology. Triggers on council, council this, run the council, war room this, pressure-test this, stress-test this, and debate this."
when_to_use: Use when the user wants a question, idea, plan, or decision pressure-tested by several independent advisors rather than answered directly, including asking to run the council, war room something, stress-test a claim, or debate a position. Use ai-council-deep instead when the answer is expensive to get wrong or the user is still unsure what they are asking, because that variant stops for clarification before the advisors run.
---

<!-- Credit: Original LLM Council skill by John Graff, Assistant Professor of Instruction, UT Austin McCombs School of Business. Adapted from Andrej Karpathy's LLM Council methodology. -->

# AI Council

You ask one AI a question, you get one answer. That answer might be great, or mid, and you have no way to tell because you only saw one perspective. The council fixes this by running the question through 5 independent advisors, each thinking from a fundamentally different angle. Then they peer-review each other's work anonymously. Then a chairman synthesizes everything into a final recommendation showing where advisors agree, where they clash, and what you should actually do.

This is adapted from Andrej Karpathy's LLM Council: dispatch queries to multiple models, have them peer-review each other anonymously, then a chairman produces the final answer. Here we use sub-agents with different thinking lenses instead of different models.

---

## When to switch to the deep variant

For high-stakes decisions (term sheets, pivots, pre-publication strategy memos) or when the framing of the question itself is unclear, use [`ai-council-deep`](../ai-council-deep/) instead. It runs the same five advisors and anonymous peer review, but adds three user-in-the-loop checkpoints: the parent asks five clarifying questions before dispatching advisors, advisors surface their load-bearing assumptions for the user to correct before peer review, and the user can request up to two full re-runs after the chairman's synthesis. Slower (10 to 60 minutes vs about 2), but catches the "one bad assumption poisons all five advisors" failure mode that the fast council cannot.

Triggers: `deep council`, `interactive council`, `high-stakes council`. Rule of thumb: if "I'll just re-run if it's wrong" feels fine, use this fast skill. Otherwise, use the deep variant.

---

## When to run the council (and when not to)

The council is for questions where being wrong is expensive and multiple perspectives add real value.

**Good council questions** involve genuine uncertainty, meaningful stakes, and multiple reasonable paths:
- "Should I launch a $97 workshop or a $497 course?"
- "Which of these 3 positioning angles is strongest?"
- "I'm thinking of pivoting from X to Y. Am I crazy?"
- "Here's my landing page copy. What's weak?"
- "Should I hire a VA or build an automation first?"
- "Pressure-test this essay before I respond to it publicly"
- "Evaluate this competitor's published claims"
- "Stress-test my draft before I publish"
- "This white paper is influencing our strategy; is the argument sound?"

**Don't run the council** for questions with one right answer ("What's the capital of France?"), creation tasks ("Write me a tweet"), or processing tasks ("Summarize this article"). If the user asks something trivial, just answer it directly.

---

## Integration with other analysis tools

### Workflow positioning

- **Fact-checking or rhetorical analysis alone:** Sufficient for checking source credibility and surface-level claims.
- **Council alone:** Best for decisions, strategy questions, and evaluating ideas where multiple theoretical perspectives add value.
- **Fact-check first, then council:** Strongest combined analysis. The fact-check handles source credibility and claim verification; the council handles structural and theoretical critique. Use for high-stakes evaluative work (source material evaluation, policy analysis, strategic decisions).
- **Council first, then fact-check:** Run the council first when you want to identify which questions to investigate, then use a fact-check pass to verify the specific claims the council flagged.

### When running after a prior analysis pass

When the council runs after a preliminary analysis, include that analysis as additional context for all advisors:

- **Advisors should not repeat fact-checking.** The prior analysis already covers source classification, claim verification, and rhetorical technique identification.
- **Advisors should focus on structural and theoretical critique:** gaps in the argument's logic, unstated assumptions, alternative explanations, practical implications, and forward-looking considerations.
- **The chairman should note where the council's findings extend or challenge the prior analysis.**

Include the prior analysis output in the framed question under a "Prior Analysis" section so advisors can build on it rather than duplicate it.

---

## The five advisors

Each advisor represents a distinct thinking style. They're not personas or job titles; they're lenses that naturally create productive tension with each other.

### 1. The Contrarian
Actively looks for what's wrong, what's missing, what will fail. Assumes the idea has a fatal flaw and tries to find it. If everything looks solid, digs deeper. Not a pessimist; the friend who saves you from a bad deal by asking the questions you're avoiding.

### 2. The First Principles Thinker
Ignores the surface-level question and asks "what are we actually trying to solve here?" Strips away assumptions. Rebuilds the problem from the ground up. Sometimes the most valuable output is this advisor saying "you're asking the wrong question entirely."

### 3. The Expansionist
Looks for upside everyone else is missing. What could be bigger? What adjacent opportunity is hiding? What's being undervalued? Doesn't care about risk (that's the Contrarian's job). Cares about what happens if this works even better than expected.

### 4. The Outsider
Has zero context about the user, their field, or their history. Responds purely to what's in front of them. This is the most underrated advisor; experts develop blind spots. The Outsider catches the curse of knowledge: things that are obvious to insiders but confusing to everyone else.

### 5. The Executor
Only cares about one thing: can this actually be done, and what's the fastest path to doing it? Ignores theory, strategy, and big-picture thinking. Looks at every idea through the lens of "OK but what do you do Monday morning?" If an idea sounds brilliant but has no clear first step, they'll say so.

**Why these five:** They create three natural tensions. Contrarian vs Expansionist (downside vs upside). First Principles vs Executor (rethink everything vs just do it). The Outsider sits in the middle keeping everyone honest by seeing what fresh eyes see.

---

## How to run a council session

Follow these steps in order. The whole process uses sub-agents for parallelism; this is essential for both speed and independence of thought.

### Step 1: Frame the question (with context enrichment)

Before framing, quickly scan the workspace for context that would help advisors give specific, grounded advice instead of generic takes. Use `Glob` and quick `Read` calls:

- `CLAUDE.md` or `claude.md` in the workspace (business context, preferences, constraints)
- Any `memory/` or `.auto-memory/` folder (audience profiles, voice docs, business details, past decisions)
- Files the user explicitly referenced or attached
- Any other files relevant to the specific question (e.g., pricing question: look for revenue data, launch results)

Don't spend more than 30 seconds on this. You're looking for the 2-3 files that give advisors the context they need.

Then reframe the user's raw question as a clear, neutral prompt that all five advisors will receive. The framed question should include:

1. The core decision or question
2. Key context from the user's message
3. Key context from workspace files (business stage, audience, constraints, past results, relevant numbers)
4. What's at stake (why this decision matters)
5. **Publication context** (when analyzing a source): Who wrote it? When? What was happening at the time? What are the authors' conflicts of interest or incentives? If the source is a corporate publication, note what corporate events preceded it. Advisors should evaluate the piece in context, not as an abstract argument.
6. **Author credibility**: If a co-author's credentials are stated or implied in the piece, verify they are current. Note any conflicts of interest (board seats, equity, investment relationships).
7. **If running after a prior analysis pass:** Include the prior analysis under a "Prior Analysis" heading.

Don't add your own opinion or steer it. If the question is too vague (e.g., "council this: my business"), ask one clarifying question, just one, then proceed.

Save the framed question for the transcript.

### Step 1.5: Fact-check pass (when analyzing source material)

When the council is evaluating a published piece (essay, article, white paper, corporate announcement), run a quick fact-check before convening advisors. Skip this step for decision questions, strategy questions, or when a prior analysis already handles fact-checking.

Use web search to verify the source material's key factual claims: statistics, historical assertions, attributed quotes, characterizations of third parties, and author credentials. Focus on claims the argument depends on, not trivia.

Produce a short fact-check summary (bullet list, one line per claim) categorized as:
- **Verified:** claim is accurate
- **Inaccurate/misleading:** claim is wrong or materially misleading (provide correction)
- **Unverified:** claim could not be confirmed or denied

Include this fact-check summary in the framed question under a "Fact-Check Results" heading so advisors can build on verified ground rather than accepting claims at face value.

### Step 2: Convene the council (5 sub-agents in parallel)

Before spawning, briefly tell the user what's about to happen: "Convening the council: 5 advisors are analyzing your question independently. This takes a couple of minutes." The user shouldn't sit in silence wondering what's going on.

Spawn all 5 advisors simultaneously as sub-agents. Parallel execution matters here; sequential spawning wastes time and risks earlier responses bleeding into later ones.

Each advisor gets their identity, the framed question (including any fact-check results and publication context from Steps 1 and 1.5), and this instruction: respond independently. Do not hedge. Do not try to be balanced. Lean fully into your assigned perspective. The synthesis comes later.

**Sub-agent prompt for each advisor:**

```
You are [Advisor Name] on an AI Council.

Your thinking style: [paste the advisor description from above]

A user has brought this question to the council:

---
[framed question, including Publication Context, Author Credibility, and Fact-Check Results sections if present]
---

Respond from your perspective. Be direct and specific. Don't hedge or try to be balanced; lean fully into your assigned angle. The other advisors will cover the angles you're not covering.

If the source material contains factual claims that are not covered in the Fact-Check Results, flag any that the argument depends on and note if they are unverified. Do not repeat verification already provided.

Keep your response between 150-300 words. No preamble. Go straight into your analysis.
```

### Step 3: Peer review (5 sub-agents in parallel)

This step is what makes the council more than just "ask 5 times"; it's the core of Karpathy's insight. Advisors evaluate each other's work, catching blind spots that no single perspective would find.

Collect all 5 advisor responses. **Anonymize them as Response A through E** (randomize the mapping so there's no positional bias; don't just assign Contrarian=A, First Principles=B, etc.).

Spawn 5 new sub-agents in parallel, one per reviewer. Each sees all 5 anonymized responses and answers four questions:

```
You are reviewing the outputs of an AI Council. Five advisors independently answered this question:

---
[framed question]
---

Here are their anonymized responses:

**Response A:**
[response]

**Response B:**
[response]

**Response C:**
[response]

**Response D:**
[response]

**Response E:**
[response]

Answer these four questions. Be specific. Reference responses by letter.

1. Which response is the strongest? Why?
2. Which response has the biggest blind spot? What is it missing?
3. What did ALL five responses miss that the council should consider?
4. What factual claims or contextual assumptions are the responses treating as established that should be verified?

Keep your review under 250 words. Be direct.
```

### Step 4: Chairman synthesis

One agent gets everything: the original question, all 5 advisor responses (now de-anonymized so the chairman can see which advisor said what), and all 5 peer reviews.

The chairman produces the final council output using this exact structure:

```
You are the Chairman of an AI Council. Your job is to synthesize the work of 5 advisors and their peer reviews into a final verdict.

The question brought to the council:
---
[framed question]
---

ADVISOR RESPONSES:

**The Contrarian:**
[response]

**The First Principles Thinker:**
[response]

**The Expansionist:**
[response]

**The Outsider:**
[response]

**The Executor:**
[response]

PEER REVIEWS:
[all 5 peer reviews]

Produce the council verdict using this exact structure:

## Where the Council Agrees
[Points multiple advisors converged on independently. These are high-confidence signals.]

## Where the Council Clashes
[Genuine disagreements. Present both sides. Explain why reasonable advisors disagree.]

## Blind Spots the Council Caught
[Things that only emerged through peer review. Things individual advisors missed that others flagged. Include any unverified claims or contextual assumptions flagged in peer review question 4.]

## Advisor Position Map
[Table with columns: Advisor | Stance (1-2 word label, e.g., Cautious, Critical, Bullish, Pragmatic) | Core Thesis (one sentence)]
Note which advisor was rated strongest by the most peer reviewers, and which was rated weakest. If there is strong peer consensus (3+ reviewers agree), this is a high-signal finding worth highlighting.

## The Recommendation
[A clear, direct recommendation. Not "it depends." A real answer with reasoning.]

## The One Thing to Do First
[A single concrete next step. Not a list. One thing.]

Be direct. Don't hedge. The whole point of the council is to give the user clarity they couldn't get from a single perspective.
```

The chairman can disagree with the majority; if 4 out of 5 advisors say "do it" but the reasoning of the 1 dissenter is strongest, the chairman should side with the dissenter and explain why.

### Step 5: Generate the council report

Create a self-contained HTML report and save it to the user's workspace folder.

**Filename:** Use `<project_name>-COUNCIL REPORT.html` where `<project_name>` is resolved as: user-specified name, then the source document's filename without extension, then the workspace folder name. If the council is evaluating a specific source document, use that document's name as the project name.

The report should be a single HTML file with inline CSS. Clean, professional design that's easy to scan. It contains:

1. **The question** at the top
2. **The chairman's verdict** prominently displayed (this is what most people will read)
3. **An agreement/disagreement visual**: a clean visual showing which advisors aligned and which diverged (could be a grid, spectrum, or position breakdown)
4. **Collapsible sections** for each advisor's full response (collapsed by default)
5. **Collapsible section** for the peer review highlights
6. **A footer** showing the timestamp and what was counciled

**Styling guidelines:** White background, subtle borders, readable sans-serif font (system font stack), soft accent colors to distinguish advisor sections. Professional briefing document feel, nothing flashy.

After generating the HTML, present it to the user with a link to the file.

### Step 6: Save the full transcript

Save the complete transcript as `<project_name>-COUNCIL TRANSCRIPT.md` in the same location (following the same naming convention as the report). Include:

- The original question
- The framed question
- All 5 advisor responses
- All 5 peer reviews (with the anonymization mapping revealed)
- The chairman's full synthesis

This transcript is the reference artifact. If the user wants to run the council again on the same question after making changes, having the previous transcript shows how the thinking evolved.

---

## Output summary

Every council session produces two files in the user's workspace:

```
<project_name>-COUNCIL REPORT.html       → visual report for scanning
<project_name>-COUNCIL TRANSCRIPT.md     → full transcript for reference
```

The user sees the HTML report via a link. The transcript is there for deeper reference.

---

## Important notes

- **Always spawn all 5 advisors in parallel.** Independence of thought is the whole point.
- **Always anonymize for peer review.** If reviewers know which advisor said what, they'll defer to certain thinking styles instead of evaluating on merit.
- **The chairman can disagree with the majority.** Strong reasoning beats a head count.
- **Don't council trivial questions.** If there's one right answer, just answer it.
- **The visual report matters.** Most users will scan the report, not read the transcript. Make the HTML clean and scannable.
- **Keep the user informed.** The council takes a few minutes to run. Give brief status updates between steps ("Advisors have weighed in. Running peer review now...") so the user knows things are progressing.
