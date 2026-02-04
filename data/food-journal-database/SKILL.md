---
name: Food Journal Database
description: Describes the structure of the Food Journal database that allows to store and read food journal entries
version: 1.0.0
---

## Overview

The Food Journal Database is a structure of Markdown notes that help store information about daily food records with detailed nutritional information.

Whenever writing into the Food Journal, you must recalculate the nutritional facts details and brief analysis as explained in this document.

## Root Folder

Store all the information under:

`{root}/food-journal`

## Daily Note File

A journal entry for a given day is store as a Markdown file inside the root folder:

`YYYY-MM-DD.md`

## Daily Note Content

The journal entry should be structured as the following example:

```Markdown
# Monday 22nd, 2025

{brief nutritional analysis of the day}

## Nutritional Facts

| Nutritional Facts | Goal | Consumed | Progress |
|-------------------|-----:|---------:|---------:|
| Calories          | 2000 |     2000 |     100% |
| Carbs             |  60g |     150g |     250% |
| Fats              |  60g |     150g |     250% |
| Proteins          |  60g |     150g |     250% |
| Fibers            |  60g |     150g |     250% |

## Entries

### Breakfast

### Morning Snack

### Lunch

### Afternoon Snack

### Dinner

### Night Snack
```

For each of the entries, follow this structure:

```Markdown
### Lunch

{brief evaluation of the entry impact on day and life}

| Nutritional Facts | Consumed | Impact |
|-------------------|----------|--------|
| Calories          |     2000 | 100%  |
| Carbs             |     150g | 250%  |
| Fats              |     150g | 250%  |
| Proteins          |     150g | 250%  |
| Fibers            |     150g | 250%  |

- pizza capricciosa
  _570cal, 26g carbs, 55g fat, 10g proteins_
- huge beer
  _300cal, 250g carbs_
- peanut butter
  _250cal, 200g fats, 30g proteins_
```

The "Impact" information should be computed in relation with the daily totals.

## How to Write to the DB

1. Create the daily entry file, or read the existing one if already existing
2. Break down the user provided data into the proper `Entries`
3. Understand if the user intention is to add new information, remove, or update existing information
4. Compile the full list of consumed items in each section of the `Entries`
5. Estimate each section's items nutritional facts
6. Calculate each section's nutritional facts totals
7. Calculate the day's nutritional facts totals
8. Update each section's `Impact` column based on the calculated daily totals
9. Read the `GOALS.md` (if it exists) to learn about the user's goals. 
   (If not available, assume medium values for an average adult)
10. Update the daily's `Goal` and `Progress` columns
11. Compute each `Entries` section brief evaluation section
12. Compute the day's brief evaluation section

**IMPORTANT:** You can write the information back into the file, or into a temporary version of the file, multiple times so to guarantee no loss of contextual information.

## Expected Outcome

At the end of the process, the daily note is updated with the new information integrating existing information and the user's prompt request.

A brief recap of the operation and the daily's Nutritional Facts table is produced also in the chat output.

## How to Analyze an Incoming Prompt

A user prompt can contain serveral references to multiple entries section over several days.

### Example n1:

```prompt
Today I had one apple for breakfast
```

The user intention is to provide the full list of items consumed "today" for "breakfast"

### Example n2:

```prompt
Today I also had one apple for breakfast
```

The user intention is to integrate today's breakfast section ADDING one apple

### Example n3:

```prompt
Today I had pasta for lunch, and I forgot to tell you that yesterday I also ate pizza for dinner.
```

The user is provinding information that is relevant to 2 notes:
- today: write the "lunch" section
- yesterday: integrate the "dinner" section adding an entry for a pizza

## How to Guess the Proper "Entry" section

If the user prompt doesn't provide an explicit reference to the section, use the time of the day to make your assumption.

Keep the title of the section so that it matches one of the sections provided in the examples.