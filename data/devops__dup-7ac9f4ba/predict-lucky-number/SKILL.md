---
name: predict-lucky-number
description: Generates a random lucky number between 0 and 9999. Use this skill when users ask for a lucky number, random number prediction, or need a number for games, drawings, or decision-making.
---

# Predict Lucky Number

This skill generates a random lucky number between 0 and 9999 for users who need a number for games, decisions, or entertainment.

## When to Use This Skill

Use this skill when users:
- Ask for a lucky number
- Need a random number for a drawing or lottery
- Want a number for decision-making
- Request number predictions
- Need a random value between 0 and 9999

## How It Works

Generate a random number between 0 and 9999 (inclusive) using Python's random module.

## Usage

When this skill is triggered, execute the following Python code to generate the lucky number:

```python
import random
lucky_number = random.randint(0, 9999)
print(f"🍀 Your lucky number is: {lucky_number}")
```

## Output Format

Present the lucky number to the user in a friendly format:
- Display the number prominently
- Add a positive message
- Format with appropriate spacing

Example output:
```
🍀 Your lucky number is: 7342

May this number bring you good fortune!
```

## Notes

- Each generation is truly random
- Numbers range from 0000 to 9999
- The skill can be used multiple times for different results
- Consider formatting numbers with leading zeros if requested (e.g., 0042 instead of 42)
