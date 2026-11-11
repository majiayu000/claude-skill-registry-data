---
description: Find the research idea or blog file related to given links and add a TODO
model: haiku
---

# Goal
- Given one or more links `<LINKS>`, find the file(s) among the following that are
  related to each link, and add a TODO to the most related file:
  - `research/ideas/*.md`
  - `website/docs/blog/posts/*.md`
  ```text
  // TODO(gp): incorporate the link <LINK> to <TOPIC>
  ```

# Workflow

## Collect Material
- Read the title and content of each link in `<LINKS>` (use `WebFetch` if the URL
  alone is not descriptive enough to judge the topic)
- List all candidate files in the two dirs above

## Match Links to Files
- For each link, compare its topic with each candidate's title, headers, and first
  paragraph. Rank candidates by relevance
- Pick the single best match for each link
  - If several files are close, list them and ask the user which to use
  - If no file plausibly matches, do not force a match. Report it instead

## Add the TODO
- In the matched file, add one line:
  ```text
  // TODO(gp): incorporate the link <LINK> to <TOPIC>
  ```
  where `<TOPIC>` is a short description (under 15 words) of the relevant part of
  the link, e.g., a technique, a result, or a quote
- Placement:
  - If the file has a top-of-file `// TODO(gp): ...` block, add the new line as an
    adjacent line in that block
  - Otherwise, put it near the most related section, e.g., right above the relevant
    bullet point or paragraph
- Change no other content in the file
- If several links map to one file, add one TODO line per link

## Report
- For each link, print the file it was added to and the exact TODO line inserted
- Report any unmatched link explicitly. Do not skip it silently

# Verification
- [ ] Each link matches at most one file, with no forced or guessed match
- [ ] Each inserted line follows the exact `// TODO(gp): incorporate the link <LINK>
  to <TOPIC>` format
- [ ] No content other than the new TODO line(s) changed in the matched file
- [ ] The report lists every link with its target file or "not matched" status
