---
name: Weight Track Database
description: Describes the structure of the weight tracker database that allows to store and read weight records for the user
version: 1.0.0
---

## Overview

The Weight Tracker database uses a JSON file to store weight entries provided by the user.

## File Location

The data file is available at `{root}/db/weight-tracker.json`

## Writing to the db

1. Before writing into the db, identify which is the best approach:
  - **in-memory change:** load the entire file in-memory, apply the change, serialize it back 
  - **text-based change:** scan the file in text mode and apply the change as a patch

2. Isolate the atomical change you want to apply

3. Read existing data to understand which kind of operation is needed
  - insert
  - update
  - delete

4. Apply the change with the identified approach.

**ALWAYS:** explain the execution plan to the user as output in the chat


## Reading from the DB

1. Identify the best approach to the read request:
- **in-memory change:** load the entire file in-memory, evaluate logic to perform the read 
- **text-based change:** scan the file in text mode and calculate the expected information as context 

2. Perform the read of the pertinent information

3. Perform aggregations if needed

**ALWAYS:** explain the execution plan to the user as output in the chat


## Data Structure

Always ensure the database keeps a data structure like this:

```json
{
  "2025": {
    "11": {
      "10": 99.0,
      "12": 99.5
    }
  }
}
```

More info:
- the indexing of the data is: year -> month -> day
- the value of a day is a number, the database is unit agnostic
- if a new writing request targets an existing day, override the value for the day