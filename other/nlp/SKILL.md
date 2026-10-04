---
name: nlp
description: "Process text with NLP. Use when tokenizing, analyzing sentiment, extracting entities, summarizing documents, or measuring similarity."
version: "3.4.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags:
  - nlp
  - text-processing
  - sentiment
  - entities
  - summarization
  - classification
---

# NLP — Natural Language Processing Toolbox

A pure-bash NLP toolkit for text analysis. Tokenize text, analyze sentiment, extract named entities, summarize documents, compute text similarity, and classify text into categories — all from the command line with no external dependencies.

## Commands

### tokenize

Split text into words and sentences. Returns word count, sentence count, individual tokens, and the top 10 most frequent words.

```bash
bash scripts/script.sh tokenize --input "The quick brown fox jumps over the lazy dog."
bash scripts/script.sh tokenize --file document.txt
bash scripts/script.sh tokenize --file document.txt --json
cat essay.txt | bash scripts/script.sh tokenize
```

### sentiment

Analyze text sentiment using built-in positive/negative word lists. Returns polarity (positive/negative/neutral), a score from -1.0 to 1.0, confidence level, and matched word counts. Handles negators (e.g., "not good" flips sentiment) and intensifiers.

```bash
bash scripts/script.sh sentiment --input "I absolutely love this product! It's amazing."
bash scripts/script.sh sentiment --file reviews.txt
bash scripts/script.sh sentiment --input "This was not good at all" --json
```

### extract

Extract named entities from text: names/people (consecutive capitalized words), organizations (with suffixes like Inc, Corp, Ltd, LLC), dates (multiple formats), numbers with units, email addresses, and URLs.

```bash
bash scripts/script.sh extract --input "John Smith works at Google Inc in Mountain View since 2020-01-15. Contact john@google.com"
bash scripts/script.sh extract --file article.txt --json
```

### summarize

Generate a summary by extracting the most important sentences. Scores sentences by word frequency with position bonuses (first/last sentences weighted higher). Control output length with `--sentences N` or `--ratio 0.3`.

```bash
bash scripts/script.sh summarize --file long_article.txt --sentences 3
bash scripts/script.sh summarize --input "Long text here..." --ratio 0.3
cat report.txt | bash scripts/script.sh summarize --sentences 5
bash scripts/script.sh summarize --file paper.txt --json
```

### similarity

Compute similarity between two texts using Jaccard index (word set overlap) and cosine similarity (word frequency vectors). Returns an overall score (average of both), shared word count, and unique word count. Scale: 0.0 = completely different, 1.0 = identical.

```bash
bash scripts/script.sh similarity --text1 "The cat sat on the mat" --text2 "A cat was sitting on a mat"
bash scripts/script.sh similarity --file1 doc1.txt --file2 doc2.txt
bash scripts/script.sh similarity --text1 "hello world" --text2 "hello world" --json
```

### classify

Classify text into user-provided categories using keyword matching. Has built-in keyword dictionaries for common categories: finance, sports, tech, politics, science, health, positive, negative, neutral. Returns the predicted category with confidence scores and hit counts for each category.

```bash
bash scripts/script.sh classify --input "The stock market rallied today on strong earnings" --categories "finance,sports,tech,politics"
bash scripts/script.sh classify --file article.txt --categories "positive,negative,neutral"
bash scripts/script.sh classify --input "New treatment shows promise in clinical trials" --categories "health,science,tech" --json
```

## Global Flags

| Flag | Description |
|------|-------------|
| `--json` | Output results in JSON format instead of plain text |

## Input Methods

All commands accept input via three methods:

1. **`--input "text"`** — inline text string
2. **`--file path.txt`** — read from a file
3. **Pipe via stdin** — `cat file.txt | bash scripts/script.sh <command>`

## Data Storage

This tool is stateless — it does not write to disk. All processing happens in memory and output goes to stdout/stderr.

## Requirements

- Bash 4+ (uses associative arrays)
- `grep` with `-P` (Perl regex) for entity extraction
- `awk` for floating-point calculations
- No Python, no external NLP libraries — pure shell

## When to Use

1. **Quick text analysis** — tokenize a document to get word counts and frequency distributions without leaving the terminal
2. **Sentiment checking** — analyze customer reviews, social media posts, or feedback files for positive/negative polarity
3. **Entity extraction** — pull out names, organizations, dates, emails, and URLs from unstructured text
4. **Document summarization** — distill long articles or reports into key sentences at a chosen ratio
5. **Text comparison** — measure how similar two documents are using Jaccard and cosine metrics for deduplication or plagiarism detection

## Examples

```bash
# Tokenize and get word frequency from a file
bash scripts/script.sh tokenize --file essay.txt

# Sentiment analysis with JSON output
bash scripts/script.sh sentiment --input "The movie was terrible and boring" --json

# Extract entities from an article
bash scripts/script.sh extract --file news_article.txt

# Summarize a long document to 5 key sentences
bash scripts/script.sh summarize --file report.txt --sentences 5

# Compare two documents for similarity
bash scripts/script.sh similarity --file1 original.txt --file2 revised.txt --json

# Classify text into categories
bash scripts/script.sh classify --input "Scientists discovered a new particle at CERN" --categories "science,tech,politics,sports"
```

## Output

Plain text by default with clear section headers. Use `--json` flag for machine-readable JSON output suitable for piping into `jq` or other tools. Sentiment returns polarity and score. Extract returns categorized entity lists. Similarity returns a 0.0–1.0 score.

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
