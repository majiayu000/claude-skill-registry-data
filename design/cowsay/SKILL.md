---
name: cowsay
description: Generate ASCII art of a cow (or other animals) with a speech bubble containing a message. Use this skill when the user asks you to display a cowsay message, make an ASCII cow speak, or wants fun terminal-style ASCII art output.
---

# Cowsay Skill

> This is an example skill created by [Amp](https://ampcode.com/threads/T-019b3989-cb59-7656-bc7a-88b9687f4cee) to illustrate how [Agent Skills](https://agentskills.io) work.

Generate ASCII art pictures of a cow with a speech bubble containing a message.

## Usage

Run the bundled Python script to generate cowsay output:

```bash
python3 scripts/cowsay.py "Your message here"
```

### Options

- `--eyes CHARS`: Set custom eye characters (default: `oo`)
- `--tongue CHARS`: Set custom tongue characters (default: empty)
- `--width N`: Set speech bubble width (default: 40)
- `--think`: Use thought bubble instead of speech bubble

### Examples

Basic cowsay:
```bash
python3 scripts/cowsay.py "Hello, world!"
```

Dead cow:
```bash
python3 scripts/cowsay.py "I'm not feeling well" --eyes "XX" --tongue "U"
```

Thinking cow:
```bash
python3 scripts/cowsay.py "Hmm, let me think..." --think
```

## Output format

The script outputs ASCII art directly to stdout. Present the output in a code block to preserve formatting.
