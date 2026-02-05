---
name: micropython-repl
description: Interact with MicroPython boards via mpy-repl-tool to push files, execute code, and test MicroPython scripts. Use when working with MicroPython development, testing board functionality, or evaluating MicroPython code on hardware.
allowed-tools: BashExecution, Read, Glob, Grep, FileEditor
---

# MicroPython REPL Skill

This skill enables interaction with MicroPython boards using the `mpy-repl-tool` (via the `there` module). It connects to a board via RFC2217 serial-over-network protocol.

## Connection Details

The board is accessible at: `rfc2217://host.docker.internal:2217`

All commands use this connection string via the `-p` parameter.

## Core Operations

### 1. Push Python Files to Board

Push all Python files in the current directory to the board root:

```bash
python -m there -p rfc2217://host.docker.internal:2217 push *.py /
```

Push a specific file:

```bash
python -m there -p rfc2217://host.docker.internal:2217 push myfile.py /
```

Push to a specific directory on the board:

```bash
python -m there -p rfc2217://host.docker.internal:2217 push myfile.py /lib/
```

### 2. List Files on Board

List files in the root directory:

```bash
python -m there -p rfc2217://host.docker.internal:2217 ls
```

List files in a specific directory:

```bash
python -m there -p rfc2217://host.docker.internal:2217 ls /lib
```

List with details (sizes, etc):

```bash
python -m there -p rfc2217://host.docker.internal:2217 ls -l
```

### 3. Download Files from Board

Download a file from the board:

```bash
python -m there -p rfc2217://host.docker.internal:2217 pull /main.py .
```

View file contents directly:

```bash
python -m there -p rfc2217://host.docker.internal:2217 cat /boot.py
```

### 4. Execute Code on Board

Run a Python file that's already on the board:

```bash
python -m there -p rfc2217://host.docker.internal:2217 run /main.py
```

Execute a one-line Python expression:

```bash
python -m there -p rfc2217://host.docker.internal:2217 -c "print('Hello from MicroPython')"
```

Evaluate and capture output:

```bash
python -m there -p rfc2217://host.docker.internal:2217 -c "2 + 2"
```

### 5. Interactive REPL

Start an interactive REPL session:

```bash
python -m there -p rfc2217://host.docker.internal:2217 -i
```

\_Note: After entering REPL, CTRL+C interrupts a running program, CTRL+D soft-resets the device

### 6. Remove Files from Board

Delete a file:

```bash
python -m there -p rfc2217://host.docker.internal:2217 rm /old_file.py
```

Delete multiple files:

```bash
python -m there -p rfc2217://host.docker.internal:2217 rm *.py
```

Delete all python files:

```bash
python -m there -p rfc2217://host.docker.internal:2217 rm -r *.py
```

### 7. Reset/Soft Reboot Board

Soft reset the board:

```bash
python -m there -p rfc2217://host.docker.internal:2217 --reset
```

## Typical Workflow

1. **Develop**: Edit Python files locally in the workspace
2. **Push**: Upload files to the board using `push *.py /` and reset the board
3. **Execute**: Run or evaluate the code using `run` or via `-c`
4. **Debug**: Check output, modify code, and repeat
5. **Verify**: Use `ls` to confirm files are on the board
6. **Download**: Retrieve any generated files or logs using `cat`

## Example: Complete Test Cycle

```bash
# 1. Push the framebuffer optimization script to the board
python -m there -p rfc2217://host.docker.internal:2217 push fb.py / --reset

# 2. Run the script on the board
python -m there -p rfc2217://host.docker.internal:2217 run /fb_opt.py

# 3. Download any output or log files
python -m there -p rfc2217://host.docker.internal:2217 cat /results.txt
```

## Troubleshooting

- **Connection errors**: Verify the RFC2217 server is running and accessible at `host.docker.internal:2217`
- **File not found**: Use `ls` to check the exact path and filename on the board
- **Import errors**: Ensure all dependent modules are pushed to the board
- **Memory errors**: MicroPython boards have limited RAM; consider optimizing code or using smaller datasets

## Additional Resources

For more advanced usage and commands, see [reference.md](reference.md).
