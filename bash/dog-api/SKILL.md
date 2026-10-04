---
name: dog-api
description: Fetch random dog images and breed information from the Dog API (dog.ceo). Use when the user wants dog pictures or information about specific dog breeds. No API key required.
---

# Dog API Skill


Fetch random dog images and breed information from the public Dog API.

## Usage

```bash
python3 scripts/dog_helper.py [COMMAND]
```

### Commands
- `random`: Get a random dog image URL.
- `list`: List all available dog breeds.
- `breed [BREED] [--sub SUBBREED]`: Get a random image of a specific breed.

## Examples
- `python3 scripts/dog_helper.py random`
- `python3 scripts/dog_helper.py breed shiba`

## API Information
- Source: [Dog API (dog.ceo)](https://dog.ceo/dog-api/)
- Auth: No API Key required.
- Free to use for projects.
