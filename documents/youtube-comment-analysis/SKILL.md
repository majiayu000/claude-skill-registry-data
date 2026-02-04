---
name: youtube-comment-analysis
description: Use when user requests YouTube comments. Run standalone for comment analysis or sequential with youtube-to-markdown for cross-analysis with video summary.
allowed-tools:
  - Bash
  - Read
  - Write
  - Task
  - AskUserQuestion
  - Skill
---

# YouTube Comment Analysis

Execute all steps sequentially without asking for user approval. Use TodoWrite to track progress.

## Step 0: Check for video summary

If you don't know from conversation context whether a video summary exists for this URL, extract video ID from URL and check if file matching `<output_directory>/youtube - * ({video_id}).md` exists.

If no summary file exists OR you don't know from context, ask user:

```
AskUserQuestion:
- question: "No video summary found. How would you like to proceed with comment analysis?"
- header: "Mode"
- options:
  1. label: "Create transcript first"
     description: "Run youtube-to-markdown skill to create video summary, then cross-analyze comments against it"
  2. label: "Standalone analysis"
     description: "Analyze comments without video context (faster, less informed)"
```

If user chooses "Create transcript first": Run youtube-to-markdown skill with the URL first, then proceed with youtube-comment-analysis skill.

If summary exists OR user chooses "Standalone analysis": Proceed directly to Step 1.

## Step 1: Extract comments

```bash
python3 ./extract_comments.py "<YOUTUBE_URL>" "<output_directory>"
```

Creates: youtube_{VIDEO_ID}_name.txt, youtube_{VIDEO_ID}_comments.md

## Step 2: Clean comments

task_tool:
- subagent_type: "general-purpose"
- model: "haiku"
- prompt:

**Standalone mode (no summary):**
```
Read <output_directory>/${BASE_NAME}_comments.md and clean/curate comments. Write to <output_directory>/${BASE_NAME}_comments_cleaned.md. Do not translate.

Tasks:
- Remove low-value: "+1", "thanks", "great video", spam, duplicates
- Remove comments that repeat content from other comments
```

**Sequential mode (with summary from youtube-to-markdown):**
```
Read Summary section from <output_directory>/youtube - * ({video_id}).md file to understand main points.

Read <output_directory>/${BASE_NAME}_comments.md and clean/curate comments. Write to <output_directory>/${BASE_NAME}_comments_cleaned.md. Do not translate.

Tasks:
- Remove low-value: "+1", "thanks", "great video", spam, duplicates
- Remove comments that are off-topic (use summary to identify)
- Remove comments that repeat content from the summary or other comments
```

## Step 3: Extract Golden Comments

task_tool:
- subagent_type: "general-purpose"
- prompt:

**Standalone mode (no summary):**
```
Read <output_directory>/${BASE_NAME}_comments_cleaned.md. Extract and condense the MOST exceptional insights from highly upvoted comments. No fluff, NOT a document. Do not translate. Write to <output_directory>/${BASE_NAME}_comment_gold.md in format:

**Golden Comments**:
- [true insights from comments]
```

**Sequential mode (with summary from youtube-to-markdown):**
```
Read Summary section from <output_directory>/youtube - * ({video_id}).md file.

Read <output_directory>/${BASE_NAME}_comments_cleaned.md. Extract, condense, combine and summarize ruthlessly for the MOST exceptional true golden insights NOT already covered by the summary. No fluff, NOT a document. Write to <output_directory>/${BASE_NAME}_comment_gold.md in format:

**Golden Comments**:
- [any true insights hiding in the comment garbage, NOT in summary]
```

## Step 4: Finalize

```bash
python3 ./finalize_comments.py "${BASE_NAME}" "<output_directory>"
```

Output: `youtube - {title} - comments ({video_id}).md`

Use `--debug` flag to keep intermediate work files for inspection.
