---
name: Weight Track App
description: Collects the user's body weight and provide aggregations, charts and trends. Responds to commands like "today I'm 90Kg", "I gained 1Kg since yesterday", "What's my weekly average in the last 2 months?"
version: 1.0.0
---

## Overview

The Weight Tracker App 

Related skills:

- [Weight Tracker DB](../weight-tracker-db/SKILL.md): store weight data
- [Clock](../clock/SKILL.md): get current date/time

## Units

- Always infer the unit from the prompt information (eg. kg, libs, tons, ...), default to "kg"
- Always traspose the prompt's data into the metric system "kg" so to keep consistend data into the db

## Logging Weight

When logging the user's weight, follow this plan:

1. Calculate the entry time:
  1. Get the current date/time using the `Clock` skill
  2. Identify relative time requests in the user prompt 
     (eg. yesterday I was 99Kg)
  3. Calculate the absolute time for the information
     (clock value: 2025-11-10 -> relative reuqest: yesteday -> entry time: 2025-11-09)
2. Calculate the entry absolute value:
  1. Identify the type of user request:
    - absolute: "Today my weight is 99Kg"
    - relative: "I lost 1kg since yesterday"
  2. If needed, calculate the absolute value
    1. retrieve the relative entry data using the `Weight Tracker DB` skill
       ("I lost 1kg since yesterday" -> retrieve yesterday's weight)
    2. perform the math to obtain the absolute entry value
       ("I lost 1kg since yesterday" -> yesterday value: "99Kg" -> absolute value = 99Kg - 1Kg -> entry value: 98Kg)
3. Write the entry to the db

## Reading Weight

When the user asks a specific datapoint, follow this plan:

1. Calculate the entry time:
  1. Get the current date/time using the `Clock` skill
  2. Identify relative time requests in the user prompt 
     (eg. What was yesterday's weight?)
  3. Calculate the absolute time for the information
     (clock value: 2025-11-10 -> relative reuqest: yesteday -> entry time: 2025-11-09)
2. Fetch the value from the database