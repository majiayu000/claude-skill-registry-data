---
description: Reduce the text in a slide leaving the structure unchanged
model: haiku
---

# Goal
- Reduce the text in the slides without changing their content or structure

# Workflow

## Role
- Your role is in `.claude/skills/role.ai_researcher.md`

## Follow Conventions
- Follow `.claude/skills/slides.rules.md`
  - E.g., a line starting with an asterisk `*` is the slide title. Leave it
    unchanged

## Keep the Structure
- Keep the slide sequence, the comments, and the headers
- Keep the bullet and sub-bullet structure
- Keep all figures
- Leave bold lines untouched
- Never collapse a sub-point into a colon-joined clause on the parent bullet.
  Shorten the words in each bullet. Do not merge bullets
  - **Bad**
    ```markdown
    - **Collections of data**: organized datasets for analysis
      - E.g., customer purchase histories in CRM
    ```
  - **Good**
    ```markdown
    - **Collections of data**
      - Organized datasets for analysis
      - E.g., customer purchase histories in CRM
    ```

## Reduce Text
- Reduce the text and keep the bullet structure untouched
  - Write directly to the audience, using "you"
  - Be concise. Remove filler words (e.g., "the", "that", "very")
  - Use active voice (e.g., "Improve accuracy," not "Accuracy can be improved")
  - Prefer short phrases over full sentences
- Delete a whole bullet when it is unclear or adds no information beyond a nearby
  bullet. Do not try to trim it
  - E.g., for a slide in input like:
    ```markdown
    * Slide title
    - This is a very long bullet point that is not clear and should be removed
    - This is a clear bullet point that should be kept
    ```
    the output is:
    ```markdown
    * Slide title
    - This is a clear bullet point that should be kept
    ```

## Example
- Input
  ```markdown
  - **Collections of data**
    - Aggregated, organized data sets for analysis
    - E.g., customer purchase histories in a CRM system

  - **Descriptive statistics**
    - Summary metrics: mean, median, mode, standard deviation
    - E.g., average sales per quarter to understand trends

  - **Historical reports**
    - Examination of _past performance_
    - E.g., monthly sales reports for past fiscal year

  - **Dashboards**
    - Visual displays of key metrics for insights
    - E.g., dashboard showing quarterly revenue, expenses

  - **Models**
    - Statistical representations to _forecast, explain phenomena_
    - E.g., model to anticipate customer churn based on behavioral data
  ```

- Output
  ```markdown
  - **Collections of data**
    - Organized datasets for analysis
    - E.g., customer purchase histories in a CRM

  - **Descriptive statistics**
    - Key metrics: mean, median, mode, standard deviation
    - E.g., average quarterly sales to track trends

  - **Historical reports**
    - Review of _past performance_
    - E.g., monthly sales reports from last year

  - **Dashboards**
    - Visuals of key metrics for quick insights
    - E.g., quarterly revenue and expense dashboard

  - **Models**
    - Statistical tools to _forecast, explain_
    - E.g., churn prediction from customer behavior
  ```

# Verification
- [ ] Make sure that the updated slides render correctly, e.g.,
  ```bash
  > gen_slides.py -i <FILE> --notes_to_pdf_args="--skip_action open_pdf"
  ```
