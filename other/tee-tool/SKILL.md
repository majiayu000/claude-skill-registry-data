---
name: tee-tool
description: Read from stdin and write to both stdout and files. Use for saving pipe output while still displaying it on screen.
---
# Tee - I/O Multiplexer

Read standard input and write to both standard output and one or more files simultaneously. Useful for logging command output while monitoring progress.

## Usage
```bash
command | tee-tool [options] <file...>
```

## Options

- `-a`: Append to files instead of overwriting
- `-i`: Ignore interrupt signals

## Examples

```bash
echo "data" | tee-tool output.txt
ls -la | tee-tool -a log.txt
make 2>&1 | tee-tool build.log
```