---
name: rag-judge
description: Grade a RAG system (an AI that answers from your documents) on the two ways it fails. A script checks whether retrieval found the passage that holds the answer. Two Claude judges, tested with planted mistakes before they count, check whether every claim in the answer is supported by the passages it was shown, and whether it declined exactly when the passages had no answer. Works on any answer saved with its question and sources, including an agent's output next to the pages it read. Trigger on "grade my RAG", "evaluate my knowledge base bot", "is my chatbot making things up", "check answers against sources", "faithfulness", "hallucination check", "did it cite the right source", "RAG eval", "groundedness", "is the AI sticking to our docs", or after building anything with rag-explained.
---

# RAG Judge: was it the search, or the answer?

## What this does
A RAG answer can go wrong in two places, and they need different fixes.

The search can miss: the passage holding the answer never reached the model, so it either declined or worked with the wrong passages. Or the answer can drift: the right passages were there, and the model added a number they never said, swapped a figure, or filled a gap from general knowledge. A wrong answer looks the same either way. The fix does not. A search miss is fixed in your documents and your chunking. A drift is fixed in your instructions or your model.

This skill grades both, in the order that costs least:
1. **A script for the search.** Each test question carries a phrase from the passage that answers it. The script checks whether any passage the model was shown contains that phrase. It also flags answers with no citation and unanswerable questions that got answered anyway.
2. **A judge for grounding.** Every factual claim in the answer has to be supported by the passages shown. True in the world but absent from the passages counts as unsupported.
3. **A judge for declining.** The answer has to answer when the passages hold the answer, and say "not in the sources" when they do not. A hedged guess ("probably around 20 percent") is still a guess.

Both judges are tested before they count, the same way `agent-judge` tests its judges: on answers you already trust, and on copies with one mistake planted.

## Where this came from
Built alongside `rag-explained`, over an operator's own catalog of published skills and posts, and run on its real answers before anything was trusted.

What the build taught:
- **The larger model earned its place here.** In `agent-judge`, the small model was enough for most rules. Here the small model came close, but flip-flopped on a few clean answers across repeats. The mid-size model held on both rules. Measure on your own answers. Do not carry a model choice over from a different judge.
- **"Quote the source first" can make a judge overeager.** Asking the small model to quote the passage that holds the answer fixed a real miss, then had it treat a passage that only mentioned the topic as proof the answer was there.
- **Extra context is not a contradiction.** A good answer that mentioned a related item from another passage got flagged as conflicting. Naming that near miss in the rubric settled it.
- **Most of the value came before the judges.** The retrieval script, which costs nothing, found the one real miss in the build: the right document, but not the right passage.

What it does not do yet: grade an answer against pages the system never fetched. It checks the answer against what the model was shown, so a search that never found the best source can still pass grounding. Pair the retrieval script with real questions to catch that.

## Try it in 60 seconds
The skill ships eleven answers from the fictional sales library in `rag-explained`, each saved with its question and the passages it was shown, plus the questions file.

1. Copy the `scripts/` and `example/` folders from this skill somewhere you can run Python 3.10 or newer.
2. Install and set your key:
   ```
   python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
   export ANTHROPIC_API_KEY=...
   ```
3. Check the search, build the planted test set, and run the judges:
   ```
   .venv/bin/python scripts/retrieval_check.py --questions example/questions.jsonl --answers example/answers
   .venv/bin/python scripts/build_set.py --judges example/judges.py --clean example/answers --out judge-run
   .venv/bin/python scripts/run_judges.py --judges example/judges.py --out judge-run
   ```
4. Open `judge-run/results/<time>/report.md`. Then plant your own mistake: copy one answer file, add a sentence the sources never say, and rerun.

The sample is about 70 judge calls and costs about a quarter.

## What you'll need
- **Works today with**: answers saved as Markdown with three sections, `## Question`, `## Sources`, `## Answer`. `rag-explained` writes exactly that. For any other system, save its output in that shape.
- **Questions with evidence**: for each answerable question, a short phrase from the passage that holds the answer. Plus a few questions with no answer in your documents.
- **Answers you have read and trust**: 10 or more, to test the judges on.
- **An Anthropic API key** and Python 3.10 or newer.

## How this runs at your connection level
The skill never depends on a connector. It grades files you save, and gets sharper as you add real questions.

- **Bring your data**: save ten answers from your RAG or chatbot with their sources. You get a retrieval score and two trusted judges today.
- **Connect your tools**: log every production answer with the passages it was shown, then sample a few a week into the test set.
- **Just exploring**: run the fictional sample, then break an answer by hand and watch which check catches it.

Every run ends with the one change that would make the next run sharper: a passage to make findable, a rubric line to tighten, or a question to add.

## Customize this for yourself

| Set this | What it is | Default / Example |
|---|---|---|
| ANSWERS | the folder of saved answers to grade | one .md per question: Question, Sources, Answer |
| QUESTIONS | questions with an evidence phrase, plus unanswerable ones | 10 or more answerable, 3 or more with no answer |
| NOT_FOUND | the exact words your system uses to decline | Not in the sources. |
| JUDGE_MODEL | the model each judge runs on | start on Claude Haiku 4.5. move up only when a rerun shows it is needed |
| PLANTS | mistakes planted per judge | 8 to 12, in 2 or more styles |
| HOLDOUT | new mistake styles added after the first run, never used for tuning | 2 to 4 per judge |
| REPEATS | runs per judgment | 2 to tune, 5 for a gate |
| REVIEWER | who reads every disagreement | the owner of the documents |

**The order does not move.** The retrieval script runs before any judge. A grounded answer built on the wrong passage is still the wrong answer.

## The method

### Step 1: Save answers in a gradeable shape
Each answer needs the question, the exact passages the model was shown, and the answer, in one file. Without the passages nobody can tell a search miss from a drift. `rag-explained` saves this automatically.

### Step 2: Check the search with a script
For each answerable question, write down a short phrase from the passage that answers it. Then check whether any passage the model was shown contains that phrase. Count misses at the passage level: the right document with the wrong passage is still a miss. The same script flags answers with no citation, and unanswerable questions that got answered.

### Step 3: Judge grounding
One rule: every factual claim in the answer is supported by the passages shown. Ask the judge to work in steps (list the claims, find the passage for each, fail if any has none) and name the near misses that must pass: a faithful paraphrase, extra context from another shown passage, an answer that notes a conflict between passages.

### Step 4: Judge declining
One rule, both directions: answer when the passages hold the answer, decline when they do not. Name the hedged guess as a fail, because it is the failure people miss: "the sources don't say exactly, but it's probably..." reads as careful and is still invented.

### Step 5: Test the judges before they count
Plant mistakes in copies of trusted answers: an unsupported number added, a figure changed, a confident answer where the passages had none, a decline where they had one. After the first run, add a new style the rubric never saw, such as a true-sounding fact from outside the passages, and keep it out of tuning. Run everything at least twice and read every disagreement. A judge counts once it catches the planted and held-out mistakes, passes the clean answers, and gives the same verdict across repeats.

### Step 6: Fix the right layer
- **Passage missed:** fix the documents (clearer headings, tables turned into sentences), the chunk size, or the search. Not the prompt.
- **Claim unsupported:** fix the answer instructions or the model. Not the search.
- **Wrong decline or a guess:** fix the instructions, and add the question to the test set.

## Quality gates
- The retrieval script runs before any judge, and misses are counted per passage.
- Every judge maps to one rule, with its near misses named.
- Both judges were tested on clean, planted, and held-out answers before their verdicts counted.
- Held-out mistake styles were added after the first run and never used to tune a rubric.
- Every disagreement was read by a person.
- The judge model was chosen by a measured rerun.
- The skill says what it cannot see: pages the system never fetched.
- No em dashes anywhere.

## Output (example)
The fictional sample from a fresh install.

```
RETRIEVAL CHECK
Passage found for 8 of 8 answerable questions. Uncited answers: 0.
Unanswerable questions answered: 0.

JUDGE TRUST REPORT          the fictional sample, 2 repeats, 72 judge calls, about $0.25

judge                 false alarms   planted   held out   script     consistency
                      on clean       caught    caught     caught
grounded              0 of 11        6 of 6    2 of 2     0 of 8     1.00
answers_when_it_can   0 of 11        5 of 5    1 of 1     3 of 6     1.00

MODELS
  both judges on Claude Sonnet 5.5

DISAGREEMENTS, for a person to read
  none on this run.

NEXT
  plant a mistake of your own in one answer file and rerun. a sample this small
  proves the plumbing, not the judges. trust them on your own answers.
```

## Example chat

**You:** Our support bot answers from the help center. How do I know it isn't making things up?

**Claude:** Two questions, and they need different checks. Did it find the right help article, and did it stick to what the article says? Can you save a few dozen answers with the passages the bot was shown?

**You:** I can log those. Here are 30.

**Claude:** Give me a phrase from the right passage for 15 of the questions, and 5 questions the help center can't answer. I'll run the retrieval check first, since it's free. Then I'll plant mistakes in copies of the answers you trust: a made-up number, a changed figure, a guess where it should have declined. If the judges catch those and pass your good answers, they're ready to watch the rest.

**You:** And if retrieval is the problem?

**Claude:** Then the fix lives in the help center, not the bot. Usually it's an article whose heading doesn't use the words customers use, or a table that got split from its heading.

## Go further
- **Grade an agent the same way.** Save an agent's output with the pages it fetched as the Sources, and the grounding judge checks for invented facts. That covers the gap `agent-judge` leaves open.
- **Sample production.** Log every answer with its passages, and pull a handful a week into the test set. Real questions beat imagined ones.
- **Watch the decline rate.** A sudden rise in "not in the sources" usually means a document moved or a heading changed, not that the model got worse.
- **Grade before every change.** A new chunk size, a new model, or a new document set: rerun the retrieval script and both judges before it ships.

## Make it yours
Save your own answers in the three-section shape, write the evidence phrases, and plant the mistakes your system actually makes. Keep the order: script first, judges second, and test every judge before it counts. Built by an operator. Customize it, break it, make it better.
