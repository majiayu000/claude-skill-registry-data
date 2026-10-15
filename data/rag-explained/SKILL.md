---
name: rag-explained
description: Learn what RAG (retrieval-augmented generation) is by building a small one over your own documents, so an AI answers from your pricing, playbooks, and policies with a citation on every sentence, and says "not in the sources" instead of guessing. Explains when RAG is the right tool and when pasting the documents in is simpler, then hands the answers to rag-judge to grade. Ships a readable pipeline (chunk, search, answer) with no vector database and no embeddings, plus a fictional sales library to try it on. Trigger on "what is RAG", "explain RAG", "retrieval augmented generation", "make the AI answer from our docs", "chat with our playbook", "build a knowledge base bot", "the AI keeps making up our pricing", "ground answers in our content", "do I need a vector database", or any time someone wants an AI to answer from their own material.
---

# RAG Explained: an open-book exam for your AI

## What this does
Ask a chatbot what your discount policy is and it will tell you. Confidently. With a number nobody at your company ever approved.

The model is answering from memory, and it has never seen your discount policy. RAG fixes that by changing the exam. **Retrieval-augmented generation** means: before the model answers, look up the passages in your documents that hold the answer, hand it those passages, and tell it to answer from them only, citing each one. Closed-book becomes open-book. And an open-book student who cannot find the answer in the book should say so, which is the part most RAG builds forget.

This skill teaches it by building one. A small pipeline you can read in one sitting splits your documents into passages, finds the ones that match a question, and has Claude answer from them with a citation on every sentence, or reply "Not in the sources." Then it saves each answer next to the passages it was shown, so `rag-judge` can grade whether the retrieval found the right passage and whether the answer stuck to it.

**RAG is a retrieval problem first.** The model can only answer from what the search hands it.

## Where this came from
Built to answer one real question: "which of my skills does X, and what does it do?", asked against an operator's own catalog of published skills and posts. A few hundred documents, too many to paste into every question, and they change every week.

What the build taught:
- **Finding the right document is not finding the right passage.** One answer came back "Not in the sources" even though the right document was retrieved. The fact sat in a table row, and the chunk holding that row never made the top results. The decline was honest. The search was the miss.
- **Keyword search went further than expected.** Plain keyword ranking, the kind search engines used for decades, held up well on documents written in a consistent voice. Embeddings help with synonyms. They were not the first thing missing.
- **Declining is a feature.** Every question with no answer in the documents got "Not in the sources", including one trap where a document mentioned a number in passing that had nothing to do with the question.
- **Your reference answers can be wrong too.** One question had two correct answers in the same document, and the model quoted the other one. Write test questions carefully, or the grader will punish a right answer.

What it does not do yet: catch synonyms ("cost" will not find "price"), keep a table row attached to its heading when a chunk splits, or rank by anything but word overlap. The Go further section names the fixes.

## Try it in 60 seconds
A fictional sales library ships with this skill: five short documents for a made-up scheduling software company (pricing, discounts, ideal customer, objections, competitors) and eleven questions, three of which have no answer in the documents.

1. Copy the `scripts/` and `example/` folders from this skill somewhere you can run Python 3.10 or newer.
2. Install and set your key:
   ```
   python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
   export ANTHROPIC_API_KEY=...
   ```
3. Index the library and ask it something:
   ```
   .venv/bin/python scripts/rag.py index --docs example/docs --out rag-run
   .venv/bin/python scripts/rag.py ask --out rag-run "How much discount can a rep give without asking anyone?"
   ```
4. Run all eleven questions and look at what comes back:
   ```
   .venv/bin/python scripts/rag.py batch --out rag-run --questions example/questions.jsonl
   ```
   Open any file in `rag-run/answers/`. Each one shows the question, the passages the model was shown, and its answer. Ask yourself whether every sentence in the answer is in those passages. That question is what `rag-judge` automates.

The whole sample costs about a cent.

## What you'll need
- **Works today with**: a folder of your documents as `.md` or `.txt` files. Export from Notion, Google Docs, or a wiki to Markdown first.
- **An Anthropic API key**: only the answer step calls Claude. Indexing and search are plain Python.
- **Ten real questions** your team actually asks, with the phrase from the document that answers each one. Those become your test set.
- **Better with `rag-judge`**: it grades whether retrieval found the right passage and whether each answer stuck to it.

## How this runs at your connection level
The skill never depends on a connector. It runs on files you export today and gets sharper as the documents stay current.

- **Bring your data**: export a folder of documents, index it, ask questions. You get cited answers and a test set today.
- **Connect your tools**: point the index at a synced folder (a Drive export, a docs repo, a Notion sync), re-index on a schedule, and the answers stay current without anyone pasting.
- **Just exploring**: run the fictional library, then ask it questions it cannot answer, and watch it decline.

Every run ends with the one change that would make the next run sharper: a passage that should have been found, a document that needs a clearer heading, or a question to add to the test set.

## Customize this for yourself

| Set this | What it is | Default / Example |
|---|---|---|
| DOCS | the folder of documents to answer from | your playbook, pricing, policies, battlecards, as Markdown |
| CHUNK_WORDS | how big each passage is | 220 words, split on headings first |
| TOP_K | how many passages the model is shown per question | 4 |
| MODEL | the model that writes the answer | claude-opus-5-5 |
| NOT_FOUND | the exact words for "the answer is not here" | Not in the sources. |
| QUESTIONS | real questions with the phrase that answers each | 10 or more, plus a few with no answer in the docs |
| REVIEWER | who reads the answers before anyone relies on them | the owner of the documents |

**NOT_FOUND does not move.** A RAG that never declines is a RAG that guesses, and its guesses carry your company's name.

## The method

### Step 1: Decide whether you need RAG at all
Three options, simplest first:
- **Paste the documents in.** If everything fits in one prompt and rarely changes, put it all in the prompt and skip retrieval entirely. Current Claude models read very long prompts. This is the simplest RAG there is, and often the right one.
- **RAG.** When there are too many documents to paste every time, when they change often, or when every answer needs a citation someone can check.
- **Fine-tuning.** Almost never for facts. Training a model on your pricing teaches it to sound like your pricing, not to know this quarter's price.

### Step 2: Split the documents into passages
Each passage should answer one kind of question on its own. Split on headings first, then paragraphs, and keep each passage's heading with it, because the heading is often the words a question uses. Around 200 words is a reasonable start. Too small and a passage loses its context. Too big and the model is shown a page to find one line.

Write your documents for retrieval as much as for reading: one topic per section, a heading that says what the section answers, and no key fact stranded in a table with no words around it.

### Step 3: Find the passages that match the question
The kit uses BM25, a keyword ranking: a passage scores high when it contains the question's rarer words. No embeddings, no vector database, nothing to host. It misses synonyms and paraphrases. Add embeddings when your test set shows keyword search missing passages it should find, not before.

### Step 4: Answer from the passages only
The instructions do three jobs: answer only from the passages shown, cite the passage behind every sentence, and say the exact NOT_FOUND line when the passages do not hold the answer. The citation is what lets a reader, and a judge, check the answer.

### Step 5: Save what the model saw
Save each answer next to the question and the passages it was shown. Without that record nobody can tell a retrieval miss from an answer that drifted, and those need different fixes.

### Step 6: Grade it before anyone relies on it
Run `rag-judge` on the saved answers. A script checks whether the passage holding the answer was found. Two trust-tested judges check whether every claim is supported by the passages, and whether the answer declined exactly when it should have.

## Quality gates
- Every answer cites a passage for every sentence, or says the NOT_FOUND line exactly.
- Every answer is saved with the question and the passages it was shown.
- The test set includes questions with no answer in the documents, and every one of them was declined.
- Retrieval misses are counted at the passage level, not the document level.
- Nobody relies on the answers until a person has read them and `rag-judge` has graded them.
- No em dashes anywhere.

## Output (example)
One answer from the fictional library, as `rag.py ask` returns it.

```
## Question
How much discount can a rep give without asking anyone?

## Sources
[discount-policy#1] Who can approve what
A rep can offer up to 10% off the annual price on their own. Between 10% and 20%
needs the sales manager. Anything above 20% needs the head of sales, and comes with
a written reason in the deal record.

[discount-policy#2] What we never discount
Implementation for the Scale plan is never discounted, because a rushed rollout is
the top reason Scale customers churn in their first year.
...

## Answer
A rep can offer **up to 10% off the annual price** on their own [discount-policy#1].
Discounts between 10% and 20% need the sales manager's approval, and anything above
20% needs the head of sales plus a written reason in the deal record
[discount-policy#1].

Implementation for the Scale plan can never be discounted [discount-policy#2].
```

And the batch run's progress lines on the sample:

```
q01: passage found | answered
...
q08: passage found | answered
u01: no answer expected | declined
u02: no answer expected | declined
u03: no answer expected | declined
11 answers -> rag-run/answers.
```

## Example chat

**You:** Our reps keep asking the AI about discount rules and it makes numbers up. Can we make it answer from our actual policy?

**Claude:** Yes. That's what RAG is for: look up the right part of your policy first, then answer from it with a citation. First question, though: how big is the policy?

**You:** About ten pages, plus pricing and a few battlecards.

**Claude:** That might fit in one prompt. If it changes rarely, pasting it in is simpler than building retrieval. Does it change often?

**You:** Pricing changes every quarter and the battlecards change monthly.

**Claude:** Then RAG earns its keep. Export those docs to Markdown, give me ten questions reps actually ask and the line in the doc that answers each, and include two or three questions the docs can't answer. I'll index them, run the questions, and show you every answer next to the passages it used. The unanswerable ones matter most: if it guesses on those, it isn't ready.

## Go further
- **Add embeddings when keyword search misses.** If your test set shows passages missed because the question used different words, add embedding search alongside the keyword ranking, and keep both.
- **Keep tables with their headings.** Turn table rows into sentences ("STALE_DAYS: days since last engagement, default 90") so a row survives being split from its heading.
- **Filter before you search.** Tag documents by product, region, or date, and filter on the tag first. Last year's pricing should not compete with this year's.
- **Grade every change.** A new chunk size or a new document set can quietly break answers that used to work. Rerun the test set and `rag-judge` after each change.

## Make it yours
Point it at your documents, write ten questions your team really asks, and keep NOT_FOUND exactly where it is. The pipeline is small on purpose so you can see every step before you swap one out. Built by an operator. Customize it, break it, make it better.
