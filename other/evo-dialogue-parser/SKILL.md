---
name: evo-dialogue-parser
description: Parses dialogue script text into intermediate section structures using regex, then builds a validated JSON graph schema with typed nodes and edges. Handles section headers, speaker lines, numbered choices with optional tags, and edge targets.
---

# Dialogue Parser

This skill parses raw dialogue script text files into a structured JSON graph.

## Parsing Rules
- Section headers: `[NodeName]` on their own line
- Speaker lines: `Speaker: text -> Target` (target optional)
- Choice lines: `N. [OptionalTag] Choice text -> Target`
- Node type is "choice" if section has numbered choices, else "line"

## Output Schema
```json
{"nodes": [{"id": str, "text": str, "speaker": str, "type": str}], "edges": [{"from": str, "to": str, "text": str}]}
```

## Key Functions
- `parse_dialogue_text(script_text)` - Parse raw text into intermediate sections
- `build_json_graph(sections)` - Convert sections to graph schema
- `validate_graph(graph)` - Validate reachability and edge targets
- `parse_script(script_text)` - End-to-end: parse, build, validate
