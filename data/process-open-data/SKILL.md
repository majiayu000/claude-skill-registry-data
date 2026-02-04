---
name: process-open-data
description: Read the csv open data file and process to know the first 5 items by cost. Use when the user need to process the file and get the first 5 items
---

# Process open data

## Instructions

When the user ask to read the open data file, read the file path send and process with the script. 
The result of the script must be processed by the LLM to generate a report with the template.

## Example
The user ask:
```text
please give me the result of the open data in @file/path
```

You have to process the file path send like this:
```bash
go run scripts/main.go @file/path
```

The result of the script should be processed with the template [templates/template.txt](templates/template.txt)

