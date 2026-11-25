---
description: Simplify markdown text with ASD-STE100 and plain language, keep format
model: sonnet
---

# Goal

- Rewrite the text of a markdown file in ASD-STE100 Simplified Technical English and
  ISO 24495-1 plain language
- Change only the words inside each line
  - Keep the format of the file: headers, bullets, nesting, bold and italic tags,
    code blocks, tables, links, and blank lines
- Write the result back to the same file

# Conventions

- Follow the markdown conventions in `.claude/skills/markdown.rules.md`
- Follow the bullet-list conventions in `.claude/skills/text.rules.md`

# Workflow

## Save the Original

- Copy the input file `<FILE>` to a temporary file `<ORIG_FILE>`
  ```bash
  > cp <FILE> <ORIG_FILE>
  ```
- Use `<ORIG_FILE>` in `# Verification`, then delete it

## Find What to Keep

- Mark every element that the rewrite must not change
  - Headers: text and level
  - Fenced code blocks: the whole block, including the language tag
  - Inline code, URLs, link targets, file paths, and math
  - Tables: structure and separator rows
  - YAML front matter and HTML comments
  - Proper names, product names, and technical terms
    - Technical names are allowed in ASD-STE100 even if they are not in the
      dictionary
  - Bold labels at the start of a bullet (e.g., `**Goal**`)
    - Simplify the text after the label
  - Quoted text and bibliographic references

## Rewrite the Text

- Process the file line by line, bullet by bullet
- Rewrite the text of each bullet or paragraph in place with the writing rules below
- Keep one bullet as one bullet
  - Never merge two bullets
  - Never split a bullet into two bullets
  - Never turn a bullet into a paragraph or a paragraph into a bullet
- Keep the nesting level and the list marker of every bullet
  - Keep `-` as `-`, `1.` as `1.`, and `- [ ]` as `- [ ]`
- Keep the order of bullets, paragraphs, and sections
- Keep the information
  - Do not add facts, do not remove facts, and do not change numbers
  - Delete a word only if the word has no meaning (filler, vague modifier)

## Wrap the Lines

- Wrap the rewritten prose at 85 characters
- Indent the continuation lines to align with the text after the list marker
- Do not change the wrapping of lines that the rewrite did not touch

## Clean Up

- Delete `<ORIG_FILE>`

# Writing Rules

## One Word, One Meaning

- Use only the primary, literal meaning of a word
- Use the same word for the same concept in the whole file
  - Never use a synonym for variety
  - **Bad**: "Start the server. Launch the service. Boot the daemon."
  - **Good**: "Start the server. Start the service. Start the daemon."
- Replace an idiom or a metaphor with a literal statement
  - **Bad**: "This step is the backbone of the pipeline."
  - **Good**: "The pipeline needs this step."

## Active Voice

- Write every sentence in active voice
  - **Bad**: "The cache is cleared by the script."
  - **Good**: "The script clears the cache."
- Start a step with a direct imperative verb
  - **Bad**: "The valve should be turned."
  - **Good**: "Turn the valve."
- Keep the passive voice only if the actor is unknown and no active form exists

## Sentence Length

- Keep a procedural step under 20 words
- Keep a descriptive sentence under 25 words
- Write one instruction per sentence
  - **Bad**: "Open the file, delete the header, and save the result."
  - **Good**: "Open the file. Delete the header. Save the result."
- Do not use semicolons
  - Write two sentences instead
- Write contractions in full
  - E.g., write "do not", not "don't"
- Split a long sentence inside the same bullet
  - Keep the sentences in one bullet
  - Never create a new bullet to hold the split part

## Paragraph Length

- Keep a paragraph at 6 sentences or fewer
- If a prose paragraph has more than 6 sentences, split it with one blank line
  - Do this only for a prose paragraph
  - Do not split a bullet into paragraphs
- Keep an existing list as a list
  - Do not convert an inline series (e.g., "A, B, and C") into a new bullet list
  - Do not convert a bullet list into prose

## Noun Clusters

- Never stack more than three nouns without a preposition
  - **Bad**: "main pump control panel assembly"
  - **Good**: "control panel for the main pump"
- Rewrite a longer cluster with prepositions or a relative clause
  - **Bad**: "user session timeout error handler"
  - **Good**: "handler for the error when the user session times out"

## No Filler

- Delete a conversational opening
  - E.g., "Let's take a look at", "In this section, we will"
- Delete a vague modifier
  - E.g., "very", "quite", "somewhat", "various", "a number of"
- Delete a hedge
  - E.g., "it seems that", "might possibly", "in some cases"
- Replace a long phrase with a short one
  - **Bad**: "in order to"
  - **Good**: "to"

# Constraints

- Do not change the format of the file
  - The count and the order of headers, bullets, code blocks, and tables must stay
    the same
- Do not change the meaning of a sentence to make it shorter
  - If a rewrite loses information, keep the original sentence
- Do not rewrite a line that already follows the writing rules
- Write only the file. Do not add a summary, a comment, or a note to the file
- Do not commit the changes

# Examples

- **Bad** (changes the format: merges the sub-bullets into one line)
  ```markdown
  - **Cache**
    - The cache is cleared by the script when it is started
    - Various settings can be configured in order to change the size
  ```
  becomes
  ```markdown
  - **Cache**: The script clears the cache at start and you can set the size.
  ```
- **Good** (changes only the words: same bullets, same nesting, same label)
  ```markdown
  - **Cache**
    - The script clears the cache at start
    - Set the size in the config file
  ```

# Verification

- [ ] The structure is unchanged
  - The markers of headers, bullets, and fences are the same as in `<ORIG_FILE>`
  - The command prints no output when the structure is the same
    ```bash
    > diff \
        <(grep -oE '^ *(#+ |[-*+] |[0-9]+\. |```)' <ORIG_FILE>) \
        <(grep -oE '^ *(#+ |[-*+] |[0-9]+\. |```)' <FILE>)
    ```
- [ ] Fenced code blocks, inline code, URLs, and headers are unchanged
- [ ] No sentence has more than 25 words
- [ ] No step has more than 20 words
- [ ] No paragraph has more than 6 sentences
- [ ] No line is longer than 85 characters, except in code blocks and tables
- [ ] The output is in the same file `<FILE>`
- [ ] `<ORIG_FILE>` is deleted
