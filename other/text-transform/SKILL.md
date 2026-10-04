---
name: text-transform
description: Tiny text transformations — upper, lower, reverse. Proves minimal apps work.
commands:
  - id: transform
    run: ./scripts/transform.sh {{mode}} {{text}}
    description: Transform text (upper | lower | reverse)
    output: json
---
# text-transform

Pure-function sample app. Three modes: upper, lower, reverse.